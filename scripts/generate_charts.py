import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('assets/jurnal', exist_ok=True)

# Set global styles for clean academic look
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# -------------------------------------------------------------
# Chart 1: Perbandingan Konsumsi Gas EVM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))

categories = [
    'Baseline\nPlaintext',
    'Baseline\nCommitment',
    'VerifyProof\nStandalone',
    'Proyeksi Optimasi\n(Hash+Log)',
    'RecordDonation\n(Dummy 22B)',
    'RecordDonation\n(Biner 512B)',
    'RecordDonation\n(Desimal 1233B)'
]

gas_values = [
    45000,
    68000,
    225035,
    270000,
    613607,
    959421,
    1481690
]

colors = [
    '#95a5a6',  # grey
    '#7f8c8d',  # grey
    '#3498db',  # blue
    '#2ecc71',  # green (optimized)
    '#f39c12',  # orange (dummy)
    '#e74c3c',  # red (real 512B)
    '#c0392b'   # dark red
]

bars = ax.bar(categories, [v / 1000 for v in gas_values], color=colors, width=0.6, edgecolor='#2c3e50', linewidth=1)

ax.set_ylabel('Konsumsi Gas (kiloGas / 1.000 Units)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_title('Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat (Cancun)', fontsize=12, fontweight='bold', pad=14)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# Annotate values on top of bars
for bar, val in zip(bars, gas_values):
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
gas_chart_path = 'assets/jurnal/grafik_konsumsi_gas.png'
plt.savefig(gas_chart_path, dpi=300)
plt.close()
print(f'Saved: {gas_chart_path}')

# -------------------------------------------------------------
# Chart 2: Komposisi Latensi End-to-End Transaksi Donasi
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1.3, 1]})

components = [
    'Witness Generation\n(185 ms / 5.4%)',
    'Groth16 Prover\n(1.350 ms / 39.1%)',
    'Verifikasi Lokal SnarkJS\n(1.850 ms / 53.5%)',
    'Enkripsi Paillier 2048-bit\n(36 ms / 1.0%)',
    'Eksekusi EVM Tx\n(~35 ms / 1.0%)'
]

latency_ms = [185, 1350, 1850, 36, 35]
chart_colors = ['#f1c40f', '#e67e22', '#e74c3c', '#3498db', '#2ecc71']

# Horizontal bar chart on ax1
y_pos = np.arange(len(components))
bars_h = ax1.barh(y_pos, latency_ms, color=chart_colors, edgecolor='#2c3e50', height=0.6)
ax1.set_yticks(y_pos)
ax1.set_yticklabels([c.split('(')[0].strip() for c in components], fontsize=9.5)
ax1.invert_yaxis()  # top-down
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

# Donut chart on ax2
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

ax2.set_title('Proporsi Total Latensi\n(~3.456 ms / ~3,45 detik)', fontsize=11, fontweight='bold')
ax2.legend(
    wedges,
    ['Witness (185 ms)', 'Prover (1.350 ms)', 'Verify SnarkJS (1.850 ms)', 'Paillier Enc (36 ms)', 'EVM Tx (35 ms)'],
    title="Tahapan Transaksi",
    loc="center left",
    bbox_to_anchor=(0.95, 0.5),
    fontsize=8
)

plt.tight_layout()
latency_chart_path = 'assets/jurnal/grafik_latensi_e2e.png'
plt.savefig(latency_chart_path, dpi=300, bbox_inches='tight')
plt.close()
print(f'Saved: {latency_chart_path}')
