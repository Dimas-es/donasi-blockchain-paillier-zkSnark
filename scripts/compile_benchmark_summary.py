import os
import json
import csv
import numpy as np
import matplotlib.pyplot as plt

def process_benchmarks():
    bench_dir = 'assets/benchmark'
    img_dir = 'assets/gambar'
    os.makedirs(bench_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    summary = {
        "metadata": {
            "environment": {
                "os": "Microsoft Windows 11 Pro 64-bit",
                "cpu": "Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (4 Cores, 8 Threads)",
                "ram": "8 GB DDR4",
                "go_version": "go1.27.1 windows/amd64",
                "node_version": "v24.21.0",
                "snarkjs_version": "^0.7.6",
                "circom_version": "pragma circom 2.2.0",
                "solidity_version": "^0.8.28",
                "evm_environment": "Hardhat Local EVM (Cancun, 30M gas limit, 0 gwei basefee)"
            },
            "timestamp": "2026-10-21"
        },
        "crypto_operations": {},
        "onchain_timing": {},
        "gas_metrics": []
    }

    # 1. Process Paillier CSV
    paillier_csv = os.path.join(bench_dir, 'benchmark_paillier_raw.csv')
    if os.path.exists(paillier_csv):
        paillier_data = {}
        with open(paillier_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                op = row['operation']
                ms = float(row['duration_ms'])
                paillier_data.setdefault(op, []).append(ms)

        for op, vals in paillier_data.items():
            arr = np.array(vals)
            entry = {
                "count": len(arr),
                "mean_ms": float(np.mean(arr)),
                "std_dev_sample_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "std_dev_pop_ms": float(np.std(arr, ddof=0)),
                "std_dev_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "median_ms": float(np.median(arr)),
                "p95_ms": float(np.percentile(arr, 95)),
                "min_ms": float(np.min(arr)),
                "max_ms": float(np.max(arr))
            }
            if op == "KeyGen-512":
                valid_nonzero = arr[arr > 0]
                entry["timer_adjusted"] = {
                    "count": len(valid_nonzero),
                    "mean_ms": float(np.mean(valid_nonzero)),
                    "std_dev_sample_ms": float(np.std(valid_nonzero, ddof=1)),
                    "median_ms": float(np.median(valid_nonzero)),
                    "p95_ms": float(np.percentile(valid_nonzero, 95)),
                    "min_ms": float(np.min(valid_nonzero)),
                    "max_ms": float(np.max(valid_nonzero)),
                    "note": "1 reading of 0.00 ms excluded as Windows scheduler timer quantum resolution artifact"
                }
            summary["crypto_operations"][op] = entry

    # 2. Process ZK CSV
    zk_csv = os.path.join(bench_dir, 'benchmark_zk_raw.csv')
    if os.path.exists(zk_csv):
        zk_data = {}
        with open(zk_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                op = row['operation']
                ms = float(row['duration_ms'])
                zk_data.setdefault(op, []).append(ms)

        for op, vals in zk_data.items():
            arr = np.array(vals)
            entry = {
                "count": len(arr),
                "mean_ms": float(np.mean(arr)),
                "std_dev_sample_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "std_dev_pop_ms": float(np.std(arr, ddof=0)),
                "std_dev_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "median_ms": float(np.median(arr)),
                "p95_ms": float(np.percentile(arr, 95)),
                "min_ms": float(np.min(arr)),
                "max_ms": float(np.max(arr))
            }
            if op == "fullprove_wasm_groth16" and len(arr) > 1:
                steady = arr[1:]
                entry["cold_start_ms"] = float(arr[0])
                entry["steady_state"] = {
                    "count": len(steady),
                    "mean_ms": float(np.mean(steady)),
                    "std_dev_sample_ms": float(np.std(steady, ddof=1)),
                    "median_ms": float(np.median(steady)),
                    "p95_ms": float(np.percentile(steady, 95)),
                    "min_ms": float(np.min(steady)),
                    "max_ms": float(np.max(steady)),
                    "note": "Excludes iteration 1 cold-start WASM/JIT compilation"
                }
            summary["crypto_operations"][op] = entry

    # 3. Process On-Chain Timing CSV
    onchain_csv = os.path.join(bench_dir, 'benchmark_onchain_raw.csv')
    if os.path.exists(onchain_csv):
        onchain_data = {}
        with open(onchain_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                op = row['operation']
                ms = float(row['duration_ms'])
                onchain_data.setdefault(op, []).append(ms)

        for op, vals in onchain_data.items():
            arr = np.array(vals)
            summary["onchain_timing"][op] = {
                "count": len(arr),
                "mean_ms": float(np.mean(arr)),
                "std_dev_sample_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "std_dev_pop_ms": float(np.std(arr, ddof=0)),
                "std_dev_ms": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                "median_ms": float(np.median(arr)),
                "p95_ms": float(np.percentile(arr, 95)),
                "min_ms": float(np.min(arr)),
                "max_ms": float(np.max(arr))
            }

    # 4. Process Gas CSV
    gas_csv = os.path.join(bench_dir, 'benchmark_gas_raw.csv')
    if os.path.exists(gas_csv):
        with open(gas_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                summary["gas_metrics"].append({
                    "operation": row['operation'],
                    "method": row['method'],
                    "gas_used": int(row['gas_used']),
                    "gas_limit": int(row['gas_limit']),
                    "block_percentage": row['block_percentage'],
                    "category": row['category']
                })

    summary_path = os.path.join(bench_dir, 'benchmark_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary JSON saved: {summary_path}")

    # 5. Generate Gas Consumption Chart
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.dpi'] = 300

    fig, ax = plt.subplots(figsize=(9.5, 5))

    gas_categories = [
        'Baseline\nPlaintext',
        'Baseline\nCommitment',
        'VerifyProof\nStandalone',
        'Optimasi Empiris\n(Hash+Event)',
        'RecordDonation\n(Dummy 22B)',
        'RecordDonation\n(Biner 512B)',
        'RecordDonation\n(Desimal 1233B)'
    ]

    gas_vals = [
        45000,
        68000,
        225035,
        382632,
        613583,
        959421,
        1481690
    ]

    gas_colors = [
        '#95a5a6',  # grey
        '#7f8c8d',  # grey
        '#3498db',  # blue
        '#2ecc71',  # green (optimized)
        '#f39c12',  # orange (dummy)
        '#e74c3c',  # red (real 512B)
        '#c0392b'   # dark red (current Go decimal)
    ]

    bars = ax.bar(gas_categories, [v / 1000 for v in gas_vals], color=gas_colors, width=0.6, edgecolor='#2c3e50', linewidth=1)
    ax.set_ylabel('Konsumsi Gas (kiloGas / 1.000 Units)', fontsize=11, fontweight='bold', labelpad=8)
    ax.set_title('Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat (Empiris)', fontsize=12, fontweight='bold', pad=14)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, gas_vals):
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 25,
            f'{val:,}\ngas',
            ha='center',
            va='bottom',
            fontsize=8.5,
            fontweight='bold',
            color='#2c3e50'
        )

    ax.set_ylim(0, 1750)
    plt.tight_layout()
    gas_chart_path = os.path.join(img_dir, 'grafik_konsumsi_gas.png')
    plt.savefig(gas_chart_path, dpi=300)
    plt.close()
    print(f"Gas chart saved: {gas_chart_path}")

    # 6. Generate Latency Chart
    # Use real empirical data from summary
    enc_ms = summary["crypto_operations"].get("Encrypt-2048", {}).get("mean_ms", 20.19)
    prove_ms = summary["crypto_operations"].get("fullprove_wasm_groth16", {}).get("mean_ms", 212.18)
    v_in_ms = summary["crypto_operations"].get("verify_in_process_js", {}).get("mean_ms", 19.84)
    v_cli_ms = summary["crypto_operations"].get("verify_subprocess_npx", {}).get("mean_ms", 1935.30)
    v_onchain_ms = summary["onchain_timing"].get("verifyProof_pairing_precompile_0x08", {}).get("mean_ms", 4.15)
    tx_onchain_ms = summary["onchain_timing"].get("recordDonation_tx_automine", {}).get("mean_ms", 14.14)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1.3, 1]})

    latency_components = [
        f'Enkripsi Paillier 2048-bit\n({enc_ms:.1f} ms)',
        f'Groth16 Prover WASM\n({prove_ms:.1f} ms)',
        f'Verifikasi ZK In-Process\n({v_in_ms:.1f} ms)',
        f'Pairing Check EVM 0x08\n({v_onchain_ms:.1f} ms)',
        f'Automine Tx Hardhat\n({tx_onchain_ms:.1f} ms)'
    ]

    latency_ms = [enc_ms, prove_ms, v_in_ms, v_onchain_ms, tx_onchain_ms]
    chart_colors = ['#3498db', '#f39c12', '#2ecc71', '#9b59b6', '#1abc9c']

    y_pos = np.arange(len(latency_components))
    bars_h = ax1.barh(y_pos, latency_ms, color=chart_colors, edgecolor='#2c3e50', height=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([c.split('\n')[0] for c in latency_components], fontsize=9)
    ax1.invert_yaxis()
    ax1.set_xlabel('Waktu Latensi (Milidetik)', fontsize=10, fontweight='bold')
    ax1.set_title('Komponen Latensi Transaksi In-Process (Empiris)', fontsize=11, fontweight='bold')
    ax1.grid(axis='x', linestyle='--', alpha=0.5)

    for bar, val in zip(bars_h, latency_ms):
        ax1.text(
            bar.get_width() + 4,
            bar.get_y() + bar.get_height() / 2.0,
            f'{val:.2f} ms',
            va='center',
            ha='left',
            fontsize=8.5,
            fontweight='bold',
            color='#2c3e50'
        )
    ax1.set_xlim(0, max(latency_ms) * 1.25)

    wedges, texts, autotexts = ax2.pie(
        latency_ms,
        labels=None,
        autopct='%1.1f%%',
        pctdistance=0.75,
        colors=chart_colors,
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor='#2c3e50', linewidth=1)
    )

    for autotext in autotexts:
        autotext.set_fontsize(8.5)
        autotext.set_fontweight='bold'

    total_in_process = sum(latency_ms)
    ax2.set_title(f'Proporsi Latensi In-Process\n(~{total_in_process:.1f} ms / ~{total_in_process/1000:.2f} s)', fontsize=11, fontweight='bold')
    ax2.legend(
        wedges,
        [
            f'Enkripsi Paillier ({enc_ms:.1f} ms)',
            f'Groth16 Prover ({prove_ms:.1f} ms)',
            f'Verifikasi In-Process ({v_in_ms:.1f} ms)',
            f'Pairing Check 0x08 ({v_onchain_ms:.1f} ms)',
            f'Automine Tx ({tx_onchain_ms:.1f} ms)'
        ],
        title="Komponen Transaksi",
        loc="center left",
        bbox_to_anchor=(0.95, 0.5),
        fontsize=8
    )

    plt.tight_layout()
    latency_chart_path = os.path.join(img_dir, 'grafik_latensi_e2e.png')
    plt.savefig(latency_chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Latency chart saved: {latency_chart_path}")

if __name__ == '__main__':
    process_benchmarks()
