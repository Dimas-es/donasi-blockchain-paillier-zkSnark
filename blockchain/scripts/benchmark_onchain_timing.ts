import fs from "node:fs";
import path from "node:path";
import { network } from "hardhat";
import { performance } from "node:perf_hooks";

async function main() {
  const { ethers } = await network.getOrCreate();

  const outDir = path.resolve(process.cwd(), "../assets/benchmark");
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  const csvPath = path.join(outDir, "benchmark_onchain_raw.csv");

  console.log("=== DEPLOYING CONTRACTS FOR ON-CHAIN TIMING BENCHMARK ===");
  const verifierFactory = await ethers.getContractFactory("Groth16Verifier");
  const verifier = await verifierFactory.deploy();
  await verifier.waitForDeployment();
  const verifierAddress = await verifier.getAddress();

  const registryFactory = await ethers.getContractFactory("DonationRegistry");
  const registry = await registryFactory.deploy(verifierAddress);
  await registry.waitForDeployment();

  const proof = JSON.parse(
    fs.readFileSync(path.resolve(process.cwd(), "../zk/build/donation-proof.json"), "utf8"),
  );
  const publicSignals = JSON.parse(
    fs.readFileSync(path.resolve(process.cwd(), "../zk/build/donation-public.json"), "utf8"),
  );

  const campaignId = ethers.encodeBytes32String("campaign-bench");
  const commitment = ethers.zeroPadValue(
    ethers.toBeHex(BigInt(publicSignals[1])),
    32,
  );
  const campaignMax = BigInt(publicSignals[0]);

  await registry.setCampaignMaxDonation(campaignId, campaignMax);

  const pA = [BigInt(proof.pi_a[0]), BigInt(proof.pi_a[1])];
  const pB = [
    [BigInt(proof.pi_b[0][1]), BigInt(proof.pi_b[0][0])],
    [BigInt(proof.pi_b[1][1]), BigInt(proof.pi_b[1][0])],
  ];
  const pC = [BigInt(proof.pi_c[0]), BigInt(proof.pi_c[1])];
  const pubSignals = [BigInt(publicSignals[0]), BigInt(publicSignals[1])];

  const dummyPayload = ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-val"));

  // Warmup runs
  await verifier.verifyProof(pA, pB, pC, pubSignals);
  const txWarm = await registry.recordDonation(campaignId, commitment, dummyPayload, pA, pB, pC, pubSignals);
  await txWarm.wait();

  const N = 30;
  const csvRows: string[] = ["iteration,operation,duration_ms,timestamp"];

  console.log(`Running ${N} iterations for standalone verifyProof (Pairing check precompile 0x08)...`);
  const verifySamples: number[] = [];
  for (let i = 1; i <= N; i++) {
    const t0 = performance.now();
    const ok = await verifier.verifyProof(pA, pB, pC, pubSignals);
    const t1 = performance.now();
    const dur = t1 - t0;
    verifySamples.push(dur);
    csvRows.push(`${i},verifyProof_pairing_precompile_0x08,${dur.toFixed(4)},${new Date().toISOString()}`);
  }

  console.log(`Running ${N} iterations for full recordDonation transaction mining (Hardhat automine)...`);
  const txSamples: number[] = [];
  for (let i = 1; i <= N; i++) {
    const t0 = performance.now();
    const tx = await registry.recordDonation(campaignId, commitment, dummyPayload, pA, pB, pC, pubSignals);
    await tx.wait();
    const t1 = performance.now();
    const dur = t1 - t0;
    txSamples.push(dur);
    csvRows.push(`${i},recordDonation_tx_automine,${dur.toFixed(4)},${new Date().toISOString()}`);
  }

  fs.writeFileSync(csvPath, csvRows.join("\n"), "utf8");
  console.log(`\nRaw empirical CSV saved to: ${csvPath}`);

  function calcStats(samples: number[]) {
    const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
    const variance = samples.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / samples.length;
    const std = Math.sqrt(variance);
    const min = Math.min(...samples);
    const max = Math.max(...samples);
    return { mean, std, min, max };
  }

  const vStats = calcStats(verifySamples);
  const tStats = calcStats(txSamples);

  console.log("\n=== ON-CHAIN BENCHMARK STATISTICAL RESULTS (N=30) ===");
  console.log(`1. verifyProof (Precompile 0x08): Mean=${vStats.mean.toFixed(2)} ms, SD=${vStats.std.toFixed(2)} ms, Min=${vStats.min.toFixed(2)} ms, Max=${vStats.max.toFixed(2)} ms`);
  console.log(`2. recordDonation Tx (Automine):  Mean=${tStats.mean.toFixed(2)} ms, SD=${tStats.std.toFixed(2)} ms, Min=${tStats.min.toFixed(2)} ms, Max=${tStats.max.toFixed(2)} ms`);
}

main().catch(console.error);
