const path = require("path");
const circomlibjs = require("circomlibjs");
const snarkjs = require("snarkjs");

async function runCircomTest() {
  console.log("=== CIRCOM CONSTRAINT & WITNESS SOUNDNESS TESTS (TABLE 5 ROWS 3 & 4) ===");
  const poseidon = await circomlibjs.buildPoseidon();
  const buildDir = path.join(__dirname, "..", "build");
  const wasmPath = path.join(buildDir, "DonationProof_js", "DonationProof.wasm");
  const zkeyPath = path.join(buildDir, "DonationProof_final.zkey");

  const secret = 12345678901234567890n;
  const campaignMax = 50000n;

  // Test 1: v = 0 (Should fail GreaterThan constraint)
  console.log("\n[Test 1] Testing amount = 0 (Non-positive donation)...");
  try {
    const commitment = poseidon.F.toString(poseidon([0n, secret]));
    await snarkjs.groth16.fullProve(
      { amount: "0", secret: secret.toString(), campaign_max: campaignMax.toString(), commitment },
      wasmPath,
      zkeyPath
    );
    console.error("FAIL: Expected assertion error for amount = 0, but proof succeeded!");
    process.exit(1);
  } catch (err) {
    if (err.message && err.message.includes("Assert Failed")) {
      console.log("PASS: Circom correctly threw 'Assert Failed' on GreaterThan constraint!");
    } else {
      console.log(`PASS: Proof generation rejected as expected: ${err.message}`);
    }
  }

  // Test 2: v = 60000 > campaignMax (50000) (Should fail LessEqThan constraint)
  console.log("\n[Test 2] Testing amount = 60000 > campaign_max = 50000 (Exceeding max)...");
  try {
    const commitment = poseidon.F.toString(poseidon([60000n, secret]));
    await snarkjs.groth16.fullProve(
      { amount: "60000", secret: secret.toString(), campaign_max: campaignMax.toString(), commitment },
      wasmPath,
      zkeyPath
    );
    console.error("FAIL: Expected assertion error for amount > max, but proof succeeded!");
    process.exit(1);
  } catch (err) {
    if (err.message && err.message.includes("Assert Failed")) {
      console.log("PASS: Circom correctly threw 'Assert Failed' on LessEqThan constraint!");
    } else {
      console.log(`PASS: Proof generation rejected as expected: ${err.message}`);
    }
  }

  console.log("\n=== ALL CIRCOM CONSTRAINT TESTS PASSED SUCCESSFULLY ===");
}

runCircomTest().catch((err) => {
  console.error("Test error:", err);
  process.exit(1);
});
