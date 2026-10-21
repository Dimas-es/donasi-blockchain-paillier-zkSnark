const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const circomlibjs = require("circomlibjs");
const snarkjs = require("snarkjs");

function calcStats(name, arr) {
  if (arr.length === 0) return { name, count: 0 };
  const sum = arr.reduce((a, b) => a + b, 0);
  const mean = sum / arr.length;
  const variance = arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / arr.length;
  const stdDev = Math.sqrt(variance);
  const min = Math.min(...arr);
  const max = Math.max(...arr);
  return { name, count: arr.length, mean, stdDev, min, max };
}

async function main() {
  const outDir = path.join(__dirname, "..", "..", "assets", "benchmark");
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const csvPath = path.join(outDir, "benchmark_zk_raw.csv");
  const csvRows = ["iteration,operation,duration_ms"];

  const buildDir = path.join(__dirname, "..", "build");
  const wasmPath = path.join(buildDir, "DonationProof_js", "DonationProof.wasm");
  const zkeyPath = path.join(buildDir, "DonationProof_final.zkey");
  const vkeyPath = path.join(buildDir, "verification_key.json");

  const vKey = JSON.parse(fs.readFileSync(vkeyPath, "utf8"));
  const poseidon = await circomlibjs.buildPoseidon();

  console.log("=== RUNNING EMPIRICAL ZK BENCHMARKS (RAW ITERATIONS) ===");

  const amount = 5000n;
  const campaignMax = 50000n;
  const secret = BigInt("0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef");
  const hash = poseidon([amount, secret]);
  const commitment = poseidon.F.toString(hash);

  const circuitInput = {
    amount: amount.toString(),
    secret: secret.toString(),
    campaign_max: campaignMax.toString(),
    commitment: commitment,
  };

  const N_PROVE = 30; // 30 full iterations
  const durFullProve = [];
  const durLocalVerifySubprocess = [];
  const durLocalVerifyInProcess = [];

  let lastProof = null;
  let lastPublicSignals = null;

  console.log(`Running fullprove (Wasm Witness + Groth16 Prover) (${N_PROVE} iterations)...`);
  for (let i = 0; i < N_PROVE; i++) {
    const t0 = performance.now();
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
      circuitInput,
      wasmPath,
      zkeyPath
    );
    const t1 = performance.now();
    const ms = t1 - t0;
    durFullProve.push(ms);
    csvRows.push(`${i + 1},fullprove_wasm_groth16,${ms.toFixed(4)}`);
    lastProof = proof;
    lastPublicSignals = publicSignals;
    process.stdout.write(".");
  }
  console.log(" DONE");

  // Save sample proof & public signals for subprocess verification
  const tempProofPath = path.join(outDir, "temp_proof.json");
  const tempPublicPath = path.join(outDir, "temp_public.json");
  fs.writeFileSync(tempProofPath, JSON.stringify(lastProof, null, 2));
  fs.writeFileSync(tempPublicPath, JSON.stringify(lastPublicSignals, null, 2));

  console.log(`Running In-Process verifyProof (${N_PROVE} iterations)...`);
  for (let i = 0; i < N_PROVE; i++) {
    const t0 = performance.now();
    const isValid = await snarkjs.groth16.verify(vKey, lastPublicSignals, lastProof);
    const t1 = performance.now();
    if (!isValid) throw new Error("In-process verification failed!");
    const ms = t1 - t0;
    durLocalVerifyInProcess.push(ms);
    csvRows.push(`${i + 1},verify_in_process_js,${ms.toFixed(4)}`);
    process.stdout.write(".");
  }
  console.log(" DONE");

  console.log(`Running Subprocess verifyProof (npx snarkjs groth16 verify) (${N_PROVE} iterations)...`);
  const rootDir = path.join(__dirname, "..", "..");
  for (let i = 0; i < N_PROVE; i++) {
    const t0 = performance.now();
    execSync(
      `npx snarkjs groth16 verify "${vkeyPath}" "${tempPublicPath}" "${tempProofPath}"`,
      { cwd: rootDir, stdio: "ignore" }
    );
    const t1 = performance.now();
    const ms = t1 - t0;
    durLocalVerifySubprocess.push(ms);
    csvRows.push(`${i + 1},verify_subprocess_npx,${ms.toFixed(4)}`);
    process.stdout.write(".");
  }
  console.log(" DONE");

  // Cleanup temp files
  try {
    fs.unlinkSync(tempProofPath);
    fs.unlinkSync(tempPublicPath);
  } catch (e) {}

  fs.writeFileSync(csvPath, csvRows.join("\n"));

  console.log("\n=== SUMMARY OF EMPIRICAL ZK STATISTICAL RESULTS ===");
  const stats = [
    calcStats("FullProve (Witness Wasm + Groth16)", durFullProve),
    calcStats("Verify (In-Process JS)", durLocalVerifyInProcess),
    calcStats("Verify (Subprocess npx snarkjs)", durLocalVerifySubprocess),
  ];

  for (const s of stats) {
    console.log(
      `${s.name.padEnd(38)} | N=${s.count} | Mean: ${s.mean.toFixed(2).padStart(8)} ms | SD: ${s.stdDev.toFixed(2).padStart(7)} ms | Min: ${s.min.toFixed(2).padStart(8)} ms | Max: ${s.max.toFixed(2).padStart(8)} ms`
    );
  }

  console.log(`\nRaw CSV saved successfully to: ${csvPath}`);
}

main().catch(console.error);
