import fs from "node:fs";
import path from "node:path";
import { network } from "hardhat";

async function measurePayloadSequence() {
  const { ethers } = await network.getOrCreate();

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

  // Tx 1: Short Dummy (warm up array length)
  const tx1 = await registry.recordDonationOptimized(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-val")),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc1 = await tx1.wait();
  console.log("Tx 1 (Dummy 22B, initial push):", rc1?.gasUsed.toString());

  // Tx 2: Short Dummy (subsequent push)
  const tx2 = await registry.recordDonationOptimized(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("encrypted-paillier-val")),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc2 = await tx2.wait();
  console.log("Tx 2 (Dummy 22B, subsequent push):", rc2?.gasUsed.toString());

  // Tx 3: Binary 512B (subsequent push)
  const tx3 = await registry.recordDonationOptimized(
    campaignId,
    commitment,
    ethers.hexlify(new Uint8Array(512).fill(0x55)),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc3 = await tx3.wait();
  console.log("Tx 3 (Binary 512B, subsequent push):", rc3?.gasUsed.toString());

  // Tx 4: Decimal 1233B (subsequent push)
  const tx4 = await registry.recordDonationOptimized(
    campaignId,
    commitment,
    ethers.hexlify(ethers.toUtf8Bytes("9".repeat(1233))),
    pA,
    pB,
    pC,
    pubSignals,
  );
  const rc4 = await tx4.wait();
  console.log("Tx 4 (Decimal 1233B, subsequent push):", rc4?.gasUsed.toString());
}

measurePayloadSequence().catch(console.error);
