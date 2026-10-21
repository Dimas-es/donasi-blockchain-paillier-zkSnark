import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_architecture_gambar6_style():
    # Figure dimensions matching Gambar 6 layout proportions
    fig_w, fig_h = 11.8, 10.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis('off')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']

    # Exact palette from Gambar 6 (scratch/generate_simple_style_v2.py)
    bkg_color = '#ECECFF'
    border_color = '#9370DB'
    text_color = '#1E1B4B'
    sub_color = '#334155'
    arrow_color = '#475569'

    layer_bg = '#FAFAFE'
    layer_border = '#B8A9D9'
    layer_title_color = '#312E81'

    def draw_layer_container(x, y, w, h, title):
        container = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='square,pad=0.0',
            facecolor=layer_bg, edgecolor=layer_border, linewidth=1.2, linestyle='--', zorder=1
        )
        ax.add_patch(container)

        badge_h = 0.34
        badge_w = 6.4
        badge_x = x + 0.3
        badge_y = y + h - badge_h - 0.12
        badge = patches.FancyBboxPatch(
            (badge_x, badge_y), badge_w, badge_h,
            boxstyle='square,pad=0.0',
            facecolor='#EDE9FE', edgecolor='#8B5CF6', linewidth=1.2, zorder=2
        )
        ax.add_patch(badge)
        ax.text(badge_x + badge_w/2, badge_y + badge_h/2, title,
                ha='center', va='center', fontsize=8.8, fontweight='bold', color=layer_title_color, zorder=3)

    def draw_node_box(x, y, w, h, title, subtitle_lines, fs_sub=7.8, sp=0.21):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='square,pad=0.0',
            facecolor=bkg_color, edgecolor=border_color, linewidth=1.6, zorder=3
        )
        ax.add_patch(box)

        title_y = y + h - 0.26
        ax.text(x + w/2, title_y, title, ha='center', va='center',
                fontsize=9.2, fontweight='bold', color=text_color, zorder=4)

        n_lines = len(subtitle_lines)
        total_sub_h = (n_lines - 1) * sp
        sub_top = y + (h - 0.35) / 2 + total_sub_h / 2
        for i, line in enumerate(subtitle_lines):
            ax.text(x + w/2, sub_top - (i * sp), line,
                    ha='center', va='center', fontsize=fs_sub, color=sub_color, zorder=4, linespacing=1.15)

    def draw_interlayer_arrow(y_top, y_bot, label):
        x = fig_w / 2
        p1 = (x, y_top)
        p2 = (x, y_bot)

        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='-|>,head_length=6.5,head_width=4.2',
            color=arrow_color, linewidth=1.6, zorder=5
        )
        ax.add_patch(arrow)

        ly = (y_top + y_bot) / 2
        ax.text(x, ly, label, ha='center', va='center', fontsize=8.2, fontweight='bold', color='#1E293B',
                bbox=dict(boxstyle='square,pad=0.26', facecolor='#FFFFFF', edgecolor='#CBD5E1',
                         linewidth=0.8, alpha=0.98), zorder=6, linespacing=1.2)

    # -----------------------------------------------------------------
    # Coordinates Layout
    # -----------------------------------------------------------------
    margin_x = 0.6
    layer_w = fig_w - (2 * margin_x)  # 10.6

    # 1. LAYER 1: CLIENT LAYER (Top)
    l1_h = 1.90
    l1_y = 8.45
    draw_layer_container(margin_x, l1_y, layer_w, l1_h, "1. CLIENT LAYER (Antarmuka Pengguna & Frontend)")

    card1_w = 3.25
    card1_h = 1.10
    gap1 = (layer_w - 0.5 - (3 * card1_w)) / 2

    c1_x = margin_x + 0.25
    c1_y = l1_y + 0.20
    draw_node_box(c1_x, c1_y, card1_w, card1_h,
                  "Donatur (Web UI / dApp)",
                  ["Formulir Donasi Aman & Pemilihan Kampanye",
                   "Enkripsi Nilai di Sisi Peramban (Client-Side)",
                   "Penerimaan Bukti & Idempotency Key"])

    c2_x = c1_x + card1_w + gap1
    draw_node_box(c2_x, c1_y, card1_w, card1_h,
                  "Pengelola Kampanye (Organizer)",
                  ["Setup Kampanye & Konfigurasi Target Dana",
                   "Penetapan Batas Threshold Maksimal Donasi",
                   "Permintaan Dekripsi Homomorfik Akhir Periode"])

    c3_x = c2_x + card1_w + gap1
    draw_node_box(c3_x, c1_y, card1_w, card1_h,
                  "Auditor & Publik Independen",
                  ["Pemantauan Transparansi Komitmen Saldo",
                   "Verifikasi Matematis Bukti ZK-SNARK Publik",
                   "Pengecekan Status Kepatuhan Real-Time"])

    # -----------------------------------------------------------------
    # ARROW 1: Between Layer 1 and Layer 2
    # -----------------------------------------------------------------
    l2_h = 3.75
    l2_y = 3.80
    draw_interlayer_arrow(l1_y, l2_y + l2_h,
                          "HTTPS / RESTful API Gateway\n(JSON Payload, Autentikasi JWT, & Header Idempotency-Key)")

    # -----------------------------------------------------------------
    # 2. LAYER 2: OFF-CHAIN BACKEND LAYER (Middle)
    # -----------------------------------------------------------------
    draw_layer_container(margin_x, l2_y, layer_w, l2_h, "2. OFF-CHAIN BACKEND LAYER (Go Gin & Mesin Kriptografi)")

    card2_w = 4.88
    card2_h = 1.30
    gap2_x = layer_w - 0.5 - (2 * card2_w)
    col1_x = margin_x + 0.25
    col2_x = col1_x + card2_w + gap2_x

    row_top_y = l2_y + 1.82
    row_bot_y = l2_y + 0.22

    # Node 2.1: API Gateway
    draw_node_box(col1_x, row_top_y, card2_w, card2_h,
                  "RESTful API Gateway & Middleware",
                  ["Framework Go Gin: HTTP Routing, CORS, & Rate Limiter",
                   "Autentikasi JWT & Validasi Idempotency Key (Anti-Duplikasi)",
                   "Sanitasi & Validasi Skema Payload Permintaan Donasi"])

    # Node 2.2: Core Processing
    draw_node_box(col2_x, row_top_y, card2_w, card2_h,
                  "Core Services & Business Logic",
                  ["Donation Processing Service & Campaign Lifecycle",
                   "Two-Phase Transaction Handler (Pending -> Confirmed)",
                   "Background Worker: Sinkronisasi Status & Polling Receipt"])

    # Node 2.3: Cryptographic Engine
    draw_node_box(col1_x, row_bot_y, card2_w, card2_h,
                  "Cryptographic Computation Engine",
                  ["Paillier Homomorphic Encryption (AHE): Enkripsi Nilai",
                   "Penjumlahan Ciphertext Homomorfik Tanpa Buka Kunci",
                   "ZK Witness & Proof Generator (Groth16 / circom / snarkjs)"])

    # Node 2.4: PostgreSQL Storage
    draw_node_box(col2_x, row_bot_y, card2_w, card2_h,
                  "PostgreSQL Persistent Storage",
                  ["Penyimpanan Relasional ACID: Users, Campaigns, Donations",
                   "Tabel Idempotency Keys: Hash Request & Status Locking",
                   "Akumulasi Ciphertext Donasi & Audit Trail Permanen"])

    # -----------------------------------------------------------------
    # ARROW 2: Between Layer 2 and Layer 3
    # -----------------------------------------------------------------
    l3_h = 2.40
    l3_y = 0.50
    draw_interlayer_arrow(l2_y, l3_y + l3_h,
                          "JSON-RPC over WebSockets / HTTPS\n(EVM Signed Transactions, Receipt Polling, & Event Logs)")

    # -----------------------------------------------------------------
    # 3. LAYER 3: ON-CHAIN BLOCKCHAIN LAYER (Bottom)
    # -----------------------------------------------------------------
    draw_layer_container(margin_x, l3_y, layer_w, l3_h, "3. ON-CHAIN BLOCKCHAIN LAYER (Smart Contracts & EVM Ledger)")

    card3_w = 3.25
    card3_h = 1.62
    c3_y = l3_y + 0.20

    draw_node_box(c1_x, c3_y, card3_w, card3_h,
                  "EVM RPC Client & Relayer",
                  ["Relayer Transaksi Off-Chain ke On-Chain",
                   "Manajemen Private Key & ECDSA Signing",
                   "Pengelolaan Nonce & Estimasi Gas Dinamis",
                   "Polling Konfirmasi Transaction Receipt On-Chain"],
                  fs_sub=7.7, sp=0.20)

    draw_node_box(c2_x, c3_y, card3_w, card3_h,
                  "Smart Contract Ecosystem",
                  ["DonationRegistry.sol: State & Akumulasi Saldo",
                   "Groth16Verifier.sol: Verifikasi Proof (alt_bn128)",
                   "Pencatatan Hash Donasi & Anti-Replay On-Chain",
                   "Mekanisme Kontrol Akses Berbasis Role (Ownable)"],
                  fs_sub=7.7, sp=0.20)

    draw_node_box(c3_x, c3_y, card3_w, card3_h,
                  "EVM Immutable Ledger",
                  ["Konsensus Terdistribusi & Finalitas Blok (EVM)",
                   "Penyimpanan State Blockchain Terdesentralisasi",
                   "Emisi Event Logs (DonationRecorded, dll)",
                   "Jaminan Transparansi, Auditabilitas, & Integritas"],
                  fs_sub=7.7, sp=0.20)

    for out_path in ["assets/gambar/preview_gambar1_simple_style.png", "assets/gambar/gambar1_arsitektur_sistem.png"]:
        plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', edgecolor='none', bbox_inches='tight')
        print(f"Successfully generated {out_path}")
    plt.close()

if __name__ == '__main__':
    generate_architecture_gambar6_style()
