import fs from "node:fs";
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.getOrCreate();

  const verifier = await ethers.deployContract("Groth16Verifier");
  await verifier.waitForDeployment();
  const verifierAddress = await verifier.getAddress();

  const registry = await ethers.deployContract("DonationRegistry", [
    verifierAddress,
  ]);
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

  const txSet = await registry.setCampaignMaxDonation(campaignId, campaignMax);
  const rcSet = await txSet.wait();
  console.log("setCampaignMaxDonation gasUsed:", rcSet?.gasUsed.toString());

  // 1. Short test payload (22 bytes)
  const shortEnc = ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-value"));
  const tx1 = await registry.recordDonation(
    campaignId,
    commitment,
    shortEnc,
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc1 = await tx1.wait();
  console.log("1. recordDonation (22-byte dummy) gasUsed:", rc1?.gasUsed.toString());

  // 2. Full 512-byte raw Paillier ciphertext (4096-bit binary)
  const fullRaw512 = ethers.hexlify(new Uint8Array(512).fill(0xab));
  const tx2 = await registry.recordDonation(
    campaignId,
    commitment,
    fullRaw512,
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc2 = await tx2.wait();
  console.log("2. recordDonation (512-byte raw Paillier) gasUsed:", rc2?.gasUsed.toString());

  // 3. 1233-byte decimal string Paillier ciphertext (current Go backend behavior)
  const fullDec1233 = ethers.hexlify(ethers.toUtf8Bytes("1".repeat(1233)));
  const tx3 = await registry.recordDonation(
    campaignId,
    commitment,
    fullDec1233,
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc3 = await tx3.wait();
  console.log("3. recordDonation (1233-byte decimal string) gasUsed:", rc3?.gasUsed.toString());

  // 4. Gas breakdown test of Groth16 verifyProof standalone
  // Let's call verifier.verifyProof directly in a transaction to measure its exact gas!
  // To do that, we can estimate gas or send tx if it's not view, or measure via trace.
  // In Groth16Verifier.sol, verifyProof is view. We can estimate gas:
  const gasVerifyEstimate = await verifier.verifyProof.estimateGas(pA, pB, pC, pubSignals);
  console.log("Standalone verifyProof estimateGas:", gasVerifyEstimate.toString());
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
