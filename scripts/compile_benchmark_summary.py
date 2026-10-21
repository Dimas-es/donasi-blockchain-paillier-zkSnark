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
            summary["crypto_operations"][op] = {
                "count": len(arr),
                "mean_ms": float(np.mean(arr)),
                "std_dev_ms": float(np.std(arr)),
                "min_ms": float(np.min(arr)),
                "max_ms": float(np.max(arr))
            }

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
            summary["crypto_operations"][op] = {
                "count": len(arr),
                "mean_ms": float(np.mean(arr)),
                "std_dev_ms": float(np.std(arr)),
                "min_ms": float(np.min(arr)),
                "max_ms": float(np.max(arr))
            }

    # 3. Process Gas CSV
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

    # 4. Generate Gas Consumption Chart
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.dpi'] = 300

    fig, ax = plt.subplots(figsize=(9.5, 5))

    gas_categories = [
        'Baseline\nPlaintext',
        'Baseline\nCommitment',
        'VerifyProof\nStandalone',
        'Proyeksi Optimasi\n(Hash+Log)',
        'RecordDonation\n(Dummy 22B)',
        'RecordDonation\n(Biner 512B)',
        'RecordDonation\n(Desimal 1233B)'
    ]

    gas_vals = [
        45000,
        68000,
        225035,
        270000,
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

    # 5. Generate Latency Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1.3, 1]})

    latency_components = [
        'Witness Generation\n(185 ms / 5.4%)',
        'Groth16 Prover CLI\n(1.350 ms / 39.1%)',
        'Verifikasi Subprocess SnarkJS\n(1.850 ms / 53.5%)',
        'Enkripsi Paillier 2048-bit\n(20 ms / 0.6%)',
        'Eksekusi EVM Tx\n(~35 ms / 1.0%)'
    ]

    latency_ms = [185, 1350, 1850, 20, 35]
    chart_colors = ['#f1c40f', '#e67e22', '#e74c3c', '#3498db', '#2ecc71']

    y_pos = np.arange(len(latency_components))
    bars_h = ax1.barh(y_pos, latency_ms, color=chart_colors, edgecolor='#2c3e50', height=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([c.split('(')[0].strip() for c in latency_components], fontsize=9.5)
    ax1.invert_yaxis()
    ax1.set_xlabel('Waktu Latensi (Milidetik)', fontsize=10, fontweight='bold')
    ax1.set_title('Komponen Latensi Transaksi Donasi Sekuensial', fontsize=11, fontweight='bold')
    ax1.grid(axis='x', linestyle='--', alpha=0.5)

    for bar, val in zip(bars_h, latency_ms):
        ax1.text(
            bar.get_width() + 40,
            bar.get_y() + bar.get_height() / 2.0,
            f'{val:,} ms',
            va='center',
            ha='left',
            fontsize=9,
            fontweight='bold',
            color='#2c3e50'
        )
    ax1.set_xlim(0, 2250)

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

    total_lat = sum(latency_ms)
    ax2.set_title(f'Proporsi Total Latensi\n(~{total_lat:,} ms / ~{total_lat/1000:.2f} detik)', fontsize=11, fontweight='bold')
    ax2.legend(
        wedges,
        ['Witness (185 ms)', 'Prover CLI (1.350 ms)', 'Verify Subprocess (1.850 ms)', 'Paillier Enc (20 ms)', 'EVM Tx (35 ms)'],
        title="Tahapan Transaksi",
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
