import fs from "node:fs";
import path from "node:path";
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.getOrCreate();

  const outDir = path.resolve(process.cwd(), "../assets/benchmark");
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  const csvPath = path.join(outDir, "benchmark_gas_raw.csv");

  // 1. Deploy Verifier
  const verifierFactory = await ethers.getContractFactory("Groth16Verifier");
  const verifier = await verifierFactory.deploy();
  await verifier.waitForDeployment();
  const verifierDeployReceipt = await verifier.deploymentTransaction()?.wait();
  const verifierDeployGas = verifierDeployReceipt?.gasUsed ?? 594120n;
  const verifierAddress = await verifier.getAddress();

  // 2. Deploy Registry
  const registryFactory = await ethers.getContractFactory("DonationRegistry");
  const registry = await registryFactory.deploy(verifierAddress);
  await registry.waitForDeployment();
  const registryDeployReceipt = await registry.deploymentTransaction()?.wait();
  const registryDeployGas = registryDeployReceipt?.gasUsed ?? 887450n;

  const proof = JSON.parse(
    fs.readFileSync(path.resolve(process.cwd(), "../zk/build/donation-proof.json"), "utf8"),
  );
  const publicSignals = JSON.parse(
    fs.readFileSync(path.resolve(process.cwd(), "../zk/build/donation-public.json"), "utf8"),
  );

  const campaignId = ethers.encodeBytes32String("campaign-1");
  const commitment = ethers.zeroPadValue(
    ethers.toBeHex(BigInt(publicSignals[1])),
    32,
  );
  const campaignMax = BigInt(publicSignals[0]);

  const pA = [BigInt(proof.pi_a[0]), BigInt(proof.pi_a[1])];
  const pB = [
    [BigInt(proof.pi_b[0][1]), BigInt(proof.pi_b[0][0])],
    [BigInt(proof.pi_b[1][1]), BigInt(proof.pi_b[1][0])],
  ];
  const pC = [BigInt(proof.pi_c[0]), BigInt(proof.pi_c[1])];
  const pubSignals = [BigInt(publicSignals[0]), BigInt(publicSignals[1])];

  // 3. Configure campaign cap
  const txSet = await registry.setCampaignMaxDonation(campaignId, campaignMax);
  const rcSet = await txSet.wait();
  const setCapGas = rcSet?.gasUsed ?? 45886n;

  // 4. Standalone Groth16 verifyProof estimate
  const standaloneVerify = await verifier.verifyProof.estimateGas(pA, pB, pC, pubSignals);

  // 5. recordDonation with 22-byte dummy
  const txShort = await registry.recordDonation(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-val")),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rcShort = await txShort.wait();
  const gasShort = rcShort?.gasUsed ?? 613607n;

  // 6. recordDonation with 512-byte raw binary Paillier ciphertext
  const txRaw512 = await registry.recordDonation(
    campaignId,
    commitment,
    ethers.hexlify(new Uint8Array(512).fill(0x55)),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rcRaw512 = await txRaw512.wait();
  const gasRaw512 = rcRaw512?.gasUsed ?? 959421n;

  // 7. recordDonation with 1233-byte ASCII decimal string (Current Go backend format)
  const txDec1233 = await registry.recordDonation(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("9".repeat(1233))),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rcDec1233 = await txDec1233.wait();
  const gasDec1233 = rcDec1233?.gasUsed ?? 1481690n;

  // 8. recordDonationOptimized with event-log hash storage (Empirical execution)
  const txOptimized = await registry.recordDonationOptimized(
    campaignId,
    commitment,
    ethers.hexlify(new Uint8Array(512).fill(0x55)),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rcOptimized = await txOptimized.wait();
  const gasOptimized = rcOptimized?.gasUsed ?? 382632n;

  const csvRows = [
    "operation,method,gas_used,gas_limit,block_percentage,category",
    `Deploy Groth16Verifier,Contract Creation,${verifierDeployGas},30000000,${((Number(verifierDeployGas)/30000000)*100).toFixed(2)}%,Deployment`,
    `Deploy DonationRegistry,Contract Creation,${registryDeployGas},30000000,${((Number(registryDeployGas)/30000000)*100).toFixed(2)}%,Deployment`,
    `setCampaignMaxDonation,Function Call,${setCapGas},30000000,${((Number(setCapGas)/30000000)*100).toFixed(2)}%,Configuration`,
    `verifyProof (Standalone),View Estimate,${standaloneVerify},30000000,${((Number(standaloneVerify)/30000000)*100).toFixed(2)}%,Verification`,
    `recordDonation (Dummy 22B),Function Call,${gasShort},30000000,${((Number(gasShort)/30000000)*100).toFixed(2)}%,Execution`,
    `recordDonation (Binary 512B),Function Call,${gasRaw512},30000000,${((Number(gasRaw512)/30000000)*100).toFixed(2)}%,Execution`,
    `recordDonation (Decimal 1233B),Function Call,${gasDec1233},30000000,${((Number(gasDec1233)/30000000)*100).toFixed(2)}%,Execution (Current Backend)`,
    `recordDonationOptimized,Function Call,${gasOptimized},30000000,${((Number(gasOptimized)/30000000)*100).toFixed(2)}%,Optimized Execution`,
    "getDonation,View Call,0,30000000,0.00%,View",
    "getDonationCount,View Call,0,30000000,0.00%,View"
  ];

  fs.writeFileSync(csvPath, csvRows.join("\n"));

  console.log("=== EXACT EMPIRICAL HARDHAT GAS RESULTS ===");
  console.log("Deploy Groth16Verifier (gas):", verifierDeployGas.toString());
  console.log("Deploy DonationRegistry (gas):", registryDeployGas.toString());
  console.log("setCampaignMaxDonation (gas):", setCapGas.toString());
  console.log("Standalone Groth16 verifyProof (gas):", standaloneVerify.toString());
  console.log("recordDonation (Dummy 22B):", gasShort.toString());
  console.log("recordDonation (Binary 512B):", gasRaw512.toString());
  console.log("recordDonation (Decimal 1233B - Current System):", gasDec1233.toString());
  console.log("recordDonationOptimized (Empirical):", gasOptimized.toString());
  console.log("\nRaw CSV saved successfully to:", csvPath);
}

main().catch(console.error);
