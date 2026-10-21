import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_layered_block_architecture():
    fig_w, fig_h = 12.0, 11.4
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis('off')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']

    # Color Palette matching Gambar 5 and 6
    card_bg = '#ECECFF'
    card_border = '#9370DB'
    text_dark = '#1E1B4B'
    text_sub = '#334155'
    
    protocol_bg = '#F8FAFC'
    protocol_border = '#64748B'
    protocol_text = '#0F172A'

    layer1_bg = '#FAF5FF'
    layer1_border = '#C4B5FD'

    layer2_bg = '#F5F3FF'
    layer2_border = '#A5B4FC'

    layer3_bg = '#EEF2FF'
    layer3_border = '#818CF8'

    def draw_container(x, y, w, h, bg_color, border_color, badge_text):
        container = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.02,rounding_size=0.20',
            facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=1
        )
        ax.add_patch(container)

        # Header Badge INSIDE container at top-left
        badge_w = 6.2
        badge_h = 0.36
        badge_x = x + 0.3
        badge_y = y + h - badge_h - 0.12
        badge = patches.FancyBboxPatch(
            (badge_x, badge_y), badge_w, badge_h,
            boxstyle='round,pad=0.02,rounding_size=0.10',
            facecolor=border_color, edgecolor='none', zorder=2
        )
        ax.add_patch(badge)
        ax.text(badge_x + badge_w/2, badge_y + badge_h/2, badge_text,
                ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF', zorder=3)

    def draw_card(x, y, w, h, title, lines, fs=8.0, spacing=0.22):
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.02,rounding_size=0.16',
            facecolor=card_bg, edgecolor=card_border, linewidth=1.3, zorder=3
        )
        ax.add_patch(card)

        # Title
        ax.text(x + w/2, y + h - 0.22, title,
                ha='center', va='center', fontsize=9.4, fontweight='bold', color=text_dark, zorder=4)

        # Divider line
        ax.plot([x + 0.2, x + w - 0.2], [y + h - 0.38, y + h - 0.38],
                color='#C4B5FD', linewidth=0.8, zorder=4)

        # Content lines
        start_y = y + h - 0.58
        for i, line in enumerate(lines):
            ax.text(x + 0.20, start_y - (i * spacing), line,
                    ha='left', va='center', fontsize=fs, color=text_sub, zorder=4, linespacing=1.15)

    def draw_protocol_bridge(y_top_layer_bot, y_bot_layer_top, text_label):
        y_center = (y_top_layer_bot + y_bot_layer_top) / 2
        w_bridge = 9.4
        h_bridge = 0.42
        x_bridge = (fig_w - w_bridge) / 2
        y_bridge = y_center - h_bridge / 2

        # Protocol pill box
        pill = patches.FancyBboxPatch(
            (x_bridge, y_bridge), w_bridge, h_bridge,
            boxstyle='round,pad=0.02,rounding_size=0.20',
            facecolor=protocol_bg, edgecolor=protocol_border, linewidth=1.2, zorder=5
        )
        ax.add_patch(pill)

        # Text in center
        ax.text(fig_w / 2, y_center, text_label,
                ha='center', va='center', fontsize=8.6, fontweight='bold', color=protocol_text, zorder=6)

        # Vertical connector arrows at 3 symmetrical points (left, center, right)
        arrow_style = dict(arrowstyle='-|>', mutation_scale=13, color='#475569', linewidth=1.5, zorder=6)
        
        # Left and Right downward connector arrows
        for x_arr in [x_bridge + 1.2, fig_w / 2, x_bridge + w_bridge - 1.2]:
            # Arrow from top layer to pill
            arr_top = patches.FancyArrowPatch(
                (x_arr, y_top_layer_bot - 0.03), (x_arr, y_bridge + h_bridge + 0.03),
                **arrow_style
            )
            ax.add_patch(arr_top)
            # Arrow from pill to bottom layer
            arr_bot = patches.FancyArrowPatch(
                (x_arr, y_bridge - 0.03), (x_arr, y_bot_layer_top + 0.03),
                **arrow_style
            )
            ax.add_patch(arr_bot)

    # -------------------------------------------------------------
    # 1. LAYER 1: CLIENT LAYER (Top)
    # -------------------------------------------------------------
    l1_x, l1_y, l1_w, l1_h = 0.6, 9.25, 10.8, 1.80
    draw_container(l1_x, l1_y, l1_w, l1_h, layer1_bg, layer1_border,
                   "LAPISAN 1: CLIENT LAYER (Antarmuka Pengguna & Web3)")

    card1_w = 3.34
    card1_h = 1.12
    card_gap = (l1_w - 0.6 - (3 * card1_w)) / 2

    c1_x = l1_x + 0.3
    c1_y = l1_y + 0.16
    draw_card(c1_x, c1_y, card1_w, card1_h, "Donatur (Web UI / dApp)", [
        "• Formulir donasi aman & pemilihan kampanye",
        "• Pengiriman donasi & pendelegasian ZK",
        "• Penerimaan tanda terima & Idempotency Key"
    ])

    c2_x = c1_x + card1_w + card_gap
    draw_card(c2_x, c1_y, card1_w, card1_h, "Pengelola Kampanye (Organizer)", [
        "• Setup kampanye & konfigurasi target dana",
        "• Penetapan threshold maksimal donasi",
        "• Permintaan dekripsi homomorfik akhir periode"
    ])

    c3_x = c2_x + card1_w + card_gap
    draw_card(c3_x, c1_y, card1_w, card1_h, "Auditor & Publik Independen", [
        "• Pemantauan transparansi komitmen saldo",
        "• Verifikasi bukti matematis ZK-SNARK publik",
        "• Pengecekan status kepatuhan real-time"
    ])

    # -------------------------------------------------------------
    # 2. LAYER 2: OFF-CHAIN BACKEND LAYER (Middle)
    # -------------------------------------------------------------
    l2_x, l2_y, l2_w, l2_h = 0.6, 4.45, 10.8, 3.85
    draw_container(l2_x, l2_y, l2_w, l2_h, layer2_bg, layer2_border,
                   "LAPISAN 2: OFF-CHAIN BACKEND LAYER (Go Gin & Engine Kriptografi)")

    card2_w = 5.0
    card2_h = 1.48
    gap_x2 = l1_w - 0.6 - (2 * card2_w)
    col1_x = l2_x + 0.3
    col2_x = col1_x + card2_w + gap_x2
    row_top_y = l2_y + 1.76
    row_bot_y = l2_y + 0.16

    # Card 2.1: API Gateway
    draw_card(col1_x, row_top_y, card2_w, card2_h, "RESTful API Gateway & Middleware", [
        "• Framework Go Gin: HTTP routing, CORS, & rate limiter",
        "• Autentikasi JWT & validasi izin akses pengguna",
        "• Idempotency Middleware: Pencegahan transaksi duplikat",
        "• Sanitasi & validasi skema payload permintaan donasi"
    ])

    # Card 2.2: Core Processing Service
    draw_card(col2_x, row_top_y, card2_w, card2_h, "Core Services & Business Logic", [
        "• Donation Processing Service: Manajemen alur donasi",
        "• Campaign Management: Lifecycle, target, & metadata",
        "• Two-Phase Transaction Handler: Pending -> Confirmed",
        "• Background Recovery Worker: Sinkronisasi receipt tertunda"
    ])

    # Card 2.3: Cryptographic Computation Engine
    draw_card(col1_x, row_bot_y, card2_w, card2_h, "Cryptographic Computation Engine", [
        "• Paillier Homomorphic Encryption (AHE): Enkripsi nilai",
        "• Penjumlahan Ciphertext homomorfik tanpa membuka kunci",
        "• ZK Witness & Proof Generator: Integrasi circom & snarkjs",
        "• Pembuatan bukti batas donasi (Groth16 Zero-Knowledge)"
    ])

    # Card 2.4: PostgreSQL Storage
    draw_card(col2_x, row_bot_y, card2_w, card2_h, "PostgreSQL Persistent Storage", [
        "• Penyimpanan Relasional ACID: Users, Campaigns, Donations",
        "• Kolom Idempotency Key berindeks unik parsial",
        "• Akumulasi Ciphertext donasi & jejak audit komprehensif",
        "• Log sinkronisasi on-chain & riwayat verifikasi transaksi"
    ])

    # BRIDGE 1 between Layer 1 and Layer 2
    draw_protocol_bridge(l1_y, l2_y + l2_h, "HTTPS / RESTful API (JSON Payload, JWT Auth, & Header Idempotency-Key)")

    # -------------------------------------------------------------
    # 3. LAYER 3: ON-CHAIN BLOCKCHAIN LAYER (Bottom)
    # -------------------------------------------------------------
    l3_x, l3_y, l3_w, l3_h = 0.6, 0.35, 10.8, 3.20
    draw_container(l3_x, l3_y, l3_w, l3_h, layer3_bg, layer3_border,
                   "LAPISAN 3: ON-CHAIN BLOCKCHAIN LAYER (Smart Contracts & EVM Ledger)")

    card3_w = 3.34
    card3_h = 2.50
    c3_y = l3_y + 0.16

    # Card 3.1: EVM RPC Client & Relayer
    draw_card(c1_x, c3_y, card3_w, card3_h, "EVM RPC Client & Relayer", [
        "• Relayer transaksi off-chain ke on-chain",
        "• Manajemen Private Key & ECDSA Signing",
        "• Pengelolaan Nonce & estimasi Gas dinamis",
        "• Polling konfirmasi Transaction Receipt",
        "• Mekanisme retry & failover koneksi RPC",
        "• Pemantauan finalitas blok secara asinkron"
    ], fs=8.0, spacing=0.22)

    # Card 3.2: Smart Contracts
    draw_card(c2_x, c3_y, card3_w, card3_h, "Smart Contract Ecosystem", [
        "• DonationRegistry.sol:",
        "   - Registrasi kampanye & batas maksimal",
        "   - Penyimpanan komitmen akumulasi saldo",
        "   - Pencatatan komitmen donasi & verifikasi ZK",
        "• Groth16Verifier.sol:",
        "   - Verifikasi pairing curve alt_bn128",
        "   - Validasi batas tanpa membuka nilai donasi",
        "• Kontrol Akses berbasis Ownable / Role"
    ], fs=8.0, spacing=0.21)

    # Card 3.3: EVM Distributed Ledger
    draw_card(c3_x, c3_y, card3_w, card3_h, "EVM Immutable Ledger", [
        "• Lapisan konsensus terdesentralisasi (P2P)",
        "• Penyimpanan state blockchain anti-tamper",
        "• Emisi Event Logs (DonationRecorded, dll)",
        "• Penyediaan data publik untuk audit independen",
        "• Keamanan kriptografis berbasis hashing SHA-3",
        "• Jaminan integritas data donasi permanen"
    ], fs=8.0, spacing=0.22)

    # BRIDGE 2 between Layer 2 and Layer 3
    draw_protocol_bridge(l2_y, l3_y + l3_h, "JSON-RPC over WebSockets / HTTPS (EVM Transactions, Receipts, & Event Logs)")

    output_path = "assets/gambar/preview_gambar1_block_layered.png"
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print(f"Successfully generated {output_path}")

if __name__ == '__main__':
    generate_layered_block_architecture()
