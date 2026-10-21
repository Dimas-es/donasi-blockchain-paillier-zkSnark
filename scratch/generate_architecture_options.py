import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Shared styling constants - Soft pastel purple theme matching Gambar 5 & 6
BKG_NODE = '#ECECFF'
BORDER_NODE = '#9370DB'
TEXT_TITLE = '#1E1B4B'
TEXT_SUB = '#334155'
ARROW_COLOR = '#475569'

LAYER_BKG = '#F8FAFC'
LAYER_BORDER = '#94A3B8'
HEADER_BKG = '#EDE9FE'
HEADER_BORDER = '#7C3AED'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']

def draw_layer_container(ax, x, y, w, h, title, badge_x=None, badge_w=None):
    # Outer layer box
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.04,rounding_size=0.18',
        facecolor=LAYER_BKG, edgecolor=LAYER_BORDER, linewidth=1.3, zorder=1
    )
    ax.add_patch(box)
    
    # Title badge
    bw = badge_w if badge_w else min(w * 0.75, 5.8)
    bx = badge_x if badge_x else (x + 0.18)
    badge = patches.FancyBboxPatch(
        (bx, y + h - 0.44), bw, 0.38,
        boxstyle='round,pad=0.03,rounding_size=0.1',
        facecolor=HEADER_BKG, edgecolor=HEADER_BORDER, linewidth=1.0, zorder=2
    )
    ax.add_patch(badge)
    ax.text(bx + 0.14, y + h - 0.25, title, ha='left', va='center',
            fontsize=9.0, fontweight='bold', color='#4C1D95', zorder=3)

def draw_node(ax, x, y, w, h, title, subtitle='', is_db=False):
    if is_db:
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.03,rounding_size=0.22',
            facecolor='#F3E8FF', edgecolor='#7E22CE', linewidth=1.5, zorder=3
        )
    else:
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='square,pad=0.0',
            facecolor=BKG_NODE, edgecolor=BORDER_NODE, linewidth=1.4, zorder=3
        )
    ax.add_patch(box)

    if subtitle:
        ax.text(x + w/2, y + h/2 + 0.16, title, ha='center', va='center',
                fontsize=8.8, fontweight='bold', color=TEXT_TITLE, zorder=4)
        ax.text(x + w/2, y + h/2 - 0.16, subtitle, ha='center', va='center',
                fontsize=7.3, color=TEXT_SUB, zorder=4, linespacing=1.15)
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                fontsize=8.8, fontweight='bold', color=TEXT_TITLE, zorder=4)

def draw_arrow(ax, p1, p2, label='', label_pos=(0, 0), rad=0.0, label_align='center'):
    arrow = patches.FancyArrowPatch(
        p1, p2, connectionstyle=f'arc3,rad={rad}',
        arrowstyle='-|>,head_length=5.5,head_width=3.6',
        color=ARROW_COLOR, linewidth=1.4, zorder=5
    )
    ax.add_patch(arrow)
    if label:
        lx = (p1[0] + p2[0])/2 + label_pos[0]
        ly = (p1[1] + p2[1])/2 + label_pos[1]
        ax.text(lx, ly, label, ha=label_align, va='center', fontsize=6.8, color='#0F172A',
                bbox=dict(boxstyle='square,pad=0.18', facecolor='#FFFFFF', edgecolor='#CBD5E1',
                         linewidth=0.7, alpha=0.96), zorder=6, linespacing=1.15)


# ==============================================================================
# OPSI A: 3 TINGKAT HORIZONTAL SIMETRIS (Top-to-Bottom Stack)
# ==============================================================================
def render_option_a():
    fig, ax = plt.subplots(figsize=(13.2, 10.2), dpi=300)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 10.2)
    ax.axis('off')

    # LAYER 1: CLIENT LAYER (y = 8.4 to 9.8, h = 1.4)
    draw_layer_container(ax, 0.5, 8.4, 12.2, 1.40, "1. Client Layer (Antarmuka Pengguna)")
    w_cli = 3.7
    h_cli = 0.80
    y_cli = 8.58
    draw_node(ax, 0.8, y_cli, w_cli, h_cli, "Publik & Auditor Independen", "Audit Portal Transparansi")
    draw_node(ax, 4.75, y_cli, w_cli, h_cli, "Pengelola Kampanye (Organizer)", "Dashboard Manajemen Kampanye")
    draw_node(ax, 8.7, y_cli, w_cli, h_cli, "Donatur (Web UI)", "Single Page Application (SPA)")

    # LAYER 2: OFF-CHAIN BACKEND LAYER (y = 2.7 to 8.1, h = 5.4)
    draw_layer_container(ax, 0.5, 2.7, 12.2, 5.40, "2. Off-Chain Backend Layer (Go Gin & PostgreSQL)")

    # Baris 1: API Gateway & Auth Service (y = 6.55 to 7.35)
    draw_node(ax, 1.2, 6.55, 6.2, 0.80, "RESTful API Gateway", "Go Gin Web Framework / Route Handlers")
    draw_node(ax, 8.0, 6.55, 4.3, 0.80, "Auth Service", "JWT Session & X-Bootstrap-Token")
    draw_arrow(ax, (7.4, 6.95), (8.0, 6.95), label="Verify JWT", label_pos=(0, 0.16))

    # Panah Client -> Gateway
    draw_arrow(ax, (2.65, 8.58), (2.8, 7.35), label="Audit Transparansi", label_pos=(-0.25, 0.12))
    draw_arrow(ax, (6.6, 8.58), (5.2, 7.35), label="Kelola Kampanye", label_pos=(0, 0.12))
    draw_arrow(ax, (10.55, 8.58), (7.0, 7.35), label="Request Donasi & Proof", label_pos=(0.35, 0.12))

    # Baris 2: Core Services (y = 4.85 to 5.70)
    w_srv = 3.6
    draw_node(ax, 0.8, 4.85, w_srv, 0.85, "Campaign Management Service", "Validasi Pagu, Periode & Status Kampanye")
    draw_node(ax, 4.7, 4.85, w_srv, 0.85, "Donation Processing Service", "Idempotency Lock, ZK Verification & Enkripsi")
    draw_node(ax, 8.6, 3.00, 3.7, 2.70, "PostgreSQL Database", "Users, Campaigns,\nDonations, Aggregates\n\n(Persistent Storage &\nAtomic Constraints)", is_db=True)

    # Gateway -> Services
    draw_arrow(ax, (2.6, 6.55), (2.6, 5.70), label="Route /campaigns", label_pos=(-0.45, 0))
    draw_arrow(ax, (5.8, 6.55), (6.5, 5.70), label="Route /donations", label_pos=(0.45, 0))

    # Baris 3: Crypto Engines (Di bawah Donation Processing & Center)
    draw_node(ax, 4.7, 3.10, 1.75, 0.95, "Paillier Engine", "AHE Modular Mult")
    draw_node(ax, 6.55, 3.10, 1.75, 0.95, "ZK Witness Gen", "snarkjs / BN254")

    # Relasi di Backend
    draw_arrow(ax, (5.3, 4.85), (5.3, 4.05), label="Encrypt", label_pos=(-0.25, 0))
    draw_arrow(ax, (7.4, 4.85), (7.4, 4.05), label="Proof", label_pos=(0.25, 0))
    draw_arrow(ax, (8.3, 5.275), (8.6, 5.275), label="Pending/Confirm", label_pos=(0, 0.16))
    draw_arrow(ax, (4.4, 5.275), (4.7, 5.275))
    draw_arrow(ax, (10.1, 6.55), (10.1, 5.70), label="Auth Users", label_pos=(0.35, 0))

    # LAYER 3: ON-CHAIN BLOCKCHAIN LAYER (y = 0.40 to 2.35, h = 1.95)
    # Badge diletakkan di sebelah kanan agar area kiri bebas untuk panah masuk dari Backend
    draw_layer_container(ax, 0.5, 0.40, 12.2, 1.95, "3. On-Chain Blockchain Layer (EVM Smart Contracts)", badge_x=6.5, badge_w=5.8)

    w_blk = 2.6
    h_blk = 0.90
    y_blk = 0.65
    draw_node(ax, 0.8, y_blk, w_blk, h_blk, "EVM RPC Client / Signer", "Hardhat Node Provider & Signer")
    draw_node(ax, 3.9, y_blk, w_blk, h_blk, "DonationRegistry.sol", "Smart Contract Pencatat Donasi")
    draw_node(ax, 7.0, y_blk, w_blk, h_blk, "Groth16Verifier.sol", "Pairing Precompile alt_bn128 (0x08)")
    draw_node(ax, 10.1, y_blk, 2.2, h_blk, "EVM Ledger", "Commitments & State", is_db=True)

    # Panah Backend ke Blockchain (Rute bersih tanpa tabrakan badge)
    draw_arrow(ax, (1.6, 4.85), (1.6, 1.55), label="setCampaignMaxDonation()", label_pos=(-0.82, 0))
    draw_arrow(ax, (4.7, 5.00), (2.8, 1.55), label="recordDonationWithProof()", label_pos=(-0.25, 0.50), rad=0.06)

    # Alur internal di Blockchain
    draw_arrow(ax, (0.8 + w_blk, y_blk + h_blk/2), (3.9, y_blk + h_blk/2), label="Tx Submit", label_pos=(0, 0.16))
    draw_arrow(ax, (3.9 + w_blk, y_blk + h_blk/2), (7.0, y_blk + h_blk/2), label="verifyProof()", label_pos=(0, 0.16))
    draw_arrow(ax, (7.0 + w_blk, y_blk + h_blk/2), (10.1, y_blk + h_blk/2), label="Commit", label_pos=(0, 0.16))

    out_path = 'assets/gambar/preview_gambar1_opsi_a.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated {out_path} successfully!")


# ==============================================================================
# OPSI B: ALUR 3 KOLOM KIRI KE KANAN (Left-to-Right Pipeline)
# ==============================================================================
def render_option_b():
    fig, ax = plt.subplots(figsize=(14.2, 8.8), dpi=300)
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0, 8.8)
    ax.axis('off')

    # KOLOM 1: CLIENT LAYER (x = 0.4 to 3.2, w = 2.8)
    draw_layer_container(ax, 0.4, 0.4, 2.8, 8.0, "1. Client Layer")
    w_c1 = 2.4
    h_c1 = 0.95
    draw_node(ax, 0.6, 6.1, w_c1, h_c1, "Donatur", "Web UI (SPA)")
    draw_node(ax, 0.6, 4.1, w_c1, h_c1, "Pengelola Kampanye", "Organizer Dashboard")
    draw_node(ax, 0.6, 2.1, w_c1, h_c1, "Publik & Auditor", "Portal Audit Independen")

    # KOLOM 2: OFF-CHAIN BACKEND LAYER (x = 3.4 to 9.7, w = 6.3)
    draw_layer_container(ax, 3.4, 0.4, 6.3, 8.0, "2. Off-Chain Backend Layer (Go Gin & PostgreSQL)")

    # Baris 1: RESTful API Gateway (Full width di bagian atas Backend)
    draw_node(ax, 3.7, 6.90, 5.7, 0.85, "RESTful API Gateway", "Go Gin Web Framework / Route Handlers")

    # Panah dari Client ke API Gateway
    draw_arrow(ax, (3.0, 6.57), (3.7, 7.50), label="Request Donasi", label_pos=(-0.05, 0.15))
    draw_arrow(ax, (3.0, 4.57), (3.7, 7.20), label="Kelola Kampanye", label_pos=(-0.05, 0.15))
    draw_arrow(ax, (3.0, 2.57), (3.7, 6.90), label="Audit Transparansi", label_pos=(0.02, -0.16), rad=-0.06)

    # Baris 2: Auth Service (Kiri, x=3.7 to 5.3) & Campaign Management Service (Kanan, x=5.9 to 9.4)
    # Celah di antara keduanya (x = 5.3 to 5.9) menjadi jalur bebas hambatan untuk Route /donations
    draw_node(ax, 3.7, 5.50, 1.7, 0.85, "Auth Service", "JWT Session")
    draw_node(ax, 6.0, 5.50, 3.4, 0.85, "Campaign Management Service", "Validasi Pagu, Periode & Status")

    # Panah Gateway -> Auth & Gateway -> Campaign Service
    draw_arrow(ax, (4.55, 6.90), (4.55, 6.35), label="Verify JWT", label_pos=(-0.45, 0))
    draw_arrow(ax, (7.70, 6.90), (7.70, 6.35), label="Route /campaigns", label_pos=(0.62, 0))

    # Baris 3: Donation Processing Service (x = 6.0 to 9.4, y = 4.10 to 4.95)
    draw_node(ax, 6.0, 4.10, 3.4, 0.85, "Donation Processing Service", "Idempotency Lock, ZK Verification & Enkripsi")
    
    # Jalur Route /donations melewati koridor tengah bebas (x = 5.65) langsung ke sisi kiri Donation Service
    draw_arrow(ax, (5.65, 6.90), (6.0, 4.525), rad=0.05, label="Route /donations", label_pos=(-0.35, 0.35))

    # Baris 4: Crypto Engines (Di bawah Donation Service, y = 2.55 to 3.50)
    draw_node(ax, 6.0, 2.55, 1.55, 0.95, "Paillier Engine", "AHE Modular Mult")
    draw_node(ax, 7.85, 2.55, 1.55, 0.95, "ZK Witness Gen", "snarkjs / BN254")

    # Relasi Donasi -> Crypto
    draw_arrow(ax, (6.75, 4.10), (6.75, 3.50), label="Encrypt", label_pos=(-0.25, 0))
    draw_arrow(ax, (8.65, 4.10), (8.65, 3.50), label="Proof", label_pos=(0.25, 0))

    # Database di bagian bawah Column 2 (y = 0.75 to 2.00)
    draw_node(ax, 3.7, 0.75, 5.7, 1.25, "PostgreSQL Database", "Users, Campaigns, Donations, Aggregates\n(Atomic Transactions & Persistent Storage)", is_db=True)

    # Relasi ke DB
    # 1. Auth -> DB di koridor kiri (x = 4.55) 100% lurus bebas hambatan
    draw_arrow(ax, (4.55, 5.50), (4.55, 2.00), label="Sessions & Users", label_pos=(-0.58, 0))
    # 2. Crypto & Services ke DB
    draw_arrow(ax, (6.75, 2.55), (6.75, 2.00))
    draw_arrow(ax, (8.65, 2.55), (8.65, 2.00))

    # KOLOM 3: ON-CHAIN BLOCKCHAIN LAYER (x = 9.9 to 13.8, w = 3.9)
    draw_layer_container(ax, 9.9, 0.4, 3.9, 8.0, "3. Blockchain EVM Layer")
    w_c3 = 3.3
    h_c3 = 0.95
    draw_node(ax, 10.2, 6.05, w_c3, h_c3, "EVM RPC Client / Signer", "Hardhat Node Provider & Signer")
    draw_node(ax, 10.2, 4.35, w_c3, h_c3, "DonationRegistry.sol", "Smart Contract Pencatat Donasi")
    draw_node(ax, 10.2, 2.65, w_c3, h_c3, "Groth16Verifier.sol", "Pairing Precompile alt_bn128 (0x08)")
    draw_node(ax, 10.2, 0.85, w_c3, 1.15, "EVM Immutable Ledger", "State Commitments & Receipts", is_db=True)

    # Alur internal di Blockchain
    draw_arrow(ax, (11.85, 6.05), (11.85, 5.30), label="Tx Submit", label_pos=(0.35, 0))
    draw_arrow(ax, (11.85, 4.35), (11.85, 3.60), label="verifyProof()", label_pos=(0.42, 0))
    draw_arrow(ax, (11.85, 2.65), (11.85, 2.00), label="Commit State", label_pos=(0.42, 0))

    # Panah Backend ke Blockchain (KELUAR LANGSUNG DARI SISI KANAN SERVICES KE RPC TANPA TABRAKAN)
    draw_arrow(ax, (9.4, 5.925), (10.2, 6.65), label="setCampaignMaxDonation()", label_pos=(-0.05, 0.20))
    draw_arrow(ax, (9.4, 4.525), (10.2, 6.25), label="recordDonationWithProof()", label_pos=(0.05, -0.22))

    out_path = 'assets/gambar/preview_gambar1_opsi_b.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated {out_path} successfully!")


if __name__ == '__main__':
    render_option_a()
    render_option_b()
