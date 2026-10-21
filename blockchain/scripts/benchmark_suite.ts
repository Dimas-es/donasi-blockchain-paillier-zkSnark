import fs from "node:fs";
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.getOrCreate();

  // Deploy Verifier
  const verifierFactory = await ethers.getContractFactory("Groth16Verifier");
  const verifier = await verifierFactory.deploy();
  await verifier.waitForDeployment();
  const verifierAddress = await verifier.getAddress();

  // Deploy Registry
  const registryFactory = await ethers.getContractFactory("DonationRegistry");
  const registry = await registryFactory.deploy(verifierAddress);
  await registry.waitForDeployment();

  const proof = JSON.parse(
    fs.readFileSync("../zk/build/donation-proof.json", "utf8"),
  );
  const publicSignals = JSON.parse(
    fs.readFileSync("../zk/build/donation-public.json", "utf8"),
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

  await (await registry.setCampaignMaxDonation(campaignId, campaignMax)).wait();

  // 1. Standalone Groth16 verifyProof estimate
  const standaloneVerify = await verifier.verifyProof.estimateGas(pA, pB, pC, pubSignals);

  // 2. recordDonation with 22-byte dummy
  const txShort = await registry.recordDonation(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-value")),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rcShort = await txShort.wait();

  // 3. recordDonation with 512-byte raw Paillier ciphertext
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

  // 4. recordDonation with 1233-byte ASCII decimal string (Go backend format)
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

  console.log("=== EXACT EMPIRICAL HARDHAT GAS RESULTS ===");
  console.log("Standalone Groth16 verifyProof (gas):", standaloneVerify.toString());
  console.log("recordDonation (22-byte dummy):", rcShort?.gasUsed.toString());
  console.log("recordDonation (512-byte binary Paillier):", rcRaw512?.gasUsed.toString());
  console.log("recordDonation (1233-byte decimal Paillier):", rcDec1233?.gasUsed.toString());
}

main().catch(console.error);
