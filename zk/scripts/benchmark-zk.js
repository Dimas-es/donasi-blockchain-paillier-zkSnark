const path = require("path");
const fs = require("fs");
const circomlibjs = require("circomlibjs");
const snarkjs = require("snarkjs");

async function runBenchmark() {
  console.log("=== Benchmarking zk-SNARK Groth16 ===");
  const buildDir = path.join(__dirname, "..", "build");
  const wasmPath = path.join(buildDir, "DonationProof_js", "DonationProof.wasm");
  const zkeyPath = path.join(buildDir, "DonationProof_final.zkey");
  const vkeyPath = path.join(buildDir, "verification_key.json");

  const vKey = JSON.parse(fs.readFileSync(vkeyPath, "utf8"));
  const poseidon = await circomlibjs.buildPoseidon();

  const amount = 100000n;
  const campaignMax = 1000000n;
  const secret = 12345678901234567890n;
  const hash = poseidon([amount, secret]);
  const commitment = poseidon.F.toString(hash);

  const input = {
    amount: amount.toString(),
    secret: secret.toString(),
    campaign_max: campaignMax.toString(),
    commitment: commitment,
  };

  // 1. Benchmark Proof Generation (10 iterations)
  const iterations = 5;
  const proveTimes = [];
  let proofSample, publicSignalsSample;

  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
      input,
      wasmPath,
      zkeyPath
    );
    const duration = performance.now() - start;
    proveTimes.push(duration);
    proofSample = proof;
    publicSignalsSample = publicSignals;
  }

  const avgProve = proveTimes.reduce((a, b) => a + b, 0) / iterations;
  console.log(`Proof Generation (${iterations} runs): avg ${avgProve.toFixed(2)} ms (samples: ${proveTimes.map(t => t.toFixed(1)).join(", ")} ms)`);

  // 2. Benchmark Off-chain Verification (10 iterations)
  const verifyTimes = [];
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    const valid = await snarkjs.groth16.verify(vKey, publicSignalsSample, proofSample);
    const duration = performance.now() - start;
    if (!valid) throw new Error("Verification failed!");
    verifyTimes.push(duration);
  }

  const avgVerify = verifyTimes.reduce((a, b) => a + b, 0) / iterations;
  console.log(`Off-Chain Verification (${iterations} runs): avg ${avgVerify.toFixed(2)} ms (samples: ${verifyTimes.map(t => t.toFixed(1)).join(", ")} ms)`);

  // 3. Artifact sizes
  const proofJsonStr = JSON.stringify(proofSample);
  const publicSignalsStr = JSON.stringify(publicSignalsSample);
  const zkeyStat = fs.statSync(zkeyPath);
  const wasmStat = fs.statSync(wasmPath);

  console.log(`Artifact Sizes:`);
  console.log(`- Proof JSON: ${Buffer.byteLength(proofJsonStr)} bytes`);
  console.log(`- Public Signals JSON: ${Buffer.byteLength(publicSignalsStr)} bytes`);
  console.log(`- Circuit WASM: ${(wasmStat.size / 1024).toFixed(1)} KB`);
  console.log(`- Final zkey: ${(zkeyStat.size / 1024).toFixed(1)} KB`);
}

runBenchmark().catch(console.error);
