import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_preview():
    # Dimensions for 2 cols x 3 rows with generous horizontal gap
    fig, ax = plt.subplots(figsize=(11.8, 7.8), dpi=300)
    ax.set_xlim(0, 11.8)
    ax.set_ylim(0, 7.8)
    ax.axis('off')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']

    # Exact colors from Gambar 5 (Mermaid pastel theme)
    bkg_color = '#ECECFF'
    border_color = '#9370DB'
    text_color = '#1E1B4B'
    sub_color = '#334155'
    arrow_color = '#475569'

    def draw_node(ax, x, y, w, h, title, subtitle='', is_oval=False):
        if is_oval:
            box = patches.FancyBboxPatch(
                (x, y), w, h,
                boxstyle='round,pad=0.03,rounding_size=0.35',
                facecolor=bkg_color, edgecolor=border_color, linewidth=1.6, zorder=3
            )
        else:
            box = patches.FancyBboxPatch(
                (x, y), w, h,
                boxstyle='square,pad=0.0',
                facecolor=bkg_color, edgecolor=border_color, linewidth=1.6, zorder=3
            )
        ax.add_patch(box)
        
        if subtitle:
            ax.text(x + w/2, y + h/2 + 0.18, title, ha='center', va='center',
                    fontsize=9.6, fontweight='bold', color=text_color, zorder=4)
            ax.text(x + w/2, y + h/2 - 0.19, subtitle, ha='center', va='center',
                    fontsize=8.0, color=sub_color, zorder=4, linespacing=1.2)
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                    fontsize=9.4, fontweight='bold', color=text_color, zorder=4)

    # Box dimensions
    w_box = 3.85
    h_box = 1.15
    col1_x = 0.6
    col2_x = 7.35

    row1_y = 5.1
    row2_y = 3.1
    row3_y = 1.1

    def draw_arrow_plain(ax, p1, p2):
        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='-|>,head_length=6.5,head_width=4.2',
            color=arrow_color, linewidth=1.6, zorder=5
        )
        ax.add_patch(arrow)

    def draw_horizontal_arrow(ax, x1, x2, y, label):
        p1 = (x1, y)
        p2 = (x2, y)
        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='-|>,head_length=6.5,head_width=4.2',
            color=arrow_color, linewidth=1.6, zorder=5
        )
        ax.add_patch(arrow)
        # Position label ABOVE the horizontal arrow line with clear whitespace
        lx = (x1 + x2) / 2
        ly = y + 0.36
        ax.text(lx, ly, label, ha='center', va='bottom', fontsize=7.6, color='#1E293B',
                bbox=dict(boxstyle='square,pad=0.22', facecolor='#FFFFFF', edgecolor='#CBD5E1',
                         linewidth=0.7, alpha=0.96), zorder=6, linespacing=1.2)

    def draw_vertical_arrow(ax, x, y1, y2, label, label_side='right'):
        p1 = (x, y1)
        p2 = (x, y2)
        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='-|>,head_length=6.5,head_width=4.2',
            color=arrow_color, linewidth=1.6, zorder=5
        )
        ax.add_patch(arrow)
        ly = (y1 + y2) / 2
        if label_side == 'right':
            lx = x + 0.22
            ha = 'left'
        else:
            lx = x - 0.22
            ha = 'right'
        ax.text(lx, ly, label, ha=ha, va='center', fontsize=7.6, color='#1E293B',
                bbox=dict(boxstyle='square,pad=0.22', facecolor='#FFFFFF', edgecolor='#CBD5E1',
                         linewidth=0.7, alpha=0.96), zorder=6, linespacing=1.2)

    # 1. Start Oval (Top Left)
    start_oval_w = 2.8
    draw_node(ax, col1_x + (w_box - start_oval_w)/2, 7.0, start_oval_w, 0.52, "Mulai: Inisiasi Kampanye", is_oval=True)
    draw_arrow_plain(ax, (col1_x + w_box/2, 7.0), (col1_x + w_box/2, row1_y + h_box))

    # --- BARIS 1 ---
    # Node 1: Draft (Kiri Atas)
    draw_node(ax, col1_x, row1_y, w_box, h_box,
              "1. Status: Draft",
              "Pengelola Input Data & Pagu Kampanye")

    # Arrow 1 -> 2 (Kanan: Garis terlihat jelas & teks di atasnya)
    draw_horizontal_arrow(ax, col1_x + w_box, col2_x, row1_y + h_box/2,
                          "Backend Panggil\nsetCampaignMaxDonation()")

    # Node 2: Registered_OnChain (Kanan Atas)
    draw_node(ax, col2_x, row1_y, w_box, h_box,
              "2. Status: Registered_OnChain",
              "Batas Pagu Terkunci di Smart Contract EVM")

    # Arrow 2 -> 3 (Bawah)
    draw_vertical_arrow(ax, col2_x + w_box/2, row1_y, row2_y + h_box,
                        "Aktivasi Otomatis Gerbang Donasi", label_side='right')

    # --- BARIS 2 ---
    # Node 3: Active (Kanan Tengah)
    draw_node(ax, col2_x, row2_y, w_box, h_box,
              "3. Status: Active",
              "Menerima Donasi & Akumulasi Paillier\n(Dapat di-pause darurat jika ada anomali)")

    # Arrow 3 -> 4 (Kiri: Garis terlihat jelas & teks di atasnya)
    draw_horizontal_arrow(ax, col2_x, col1_x + w_box, row2_y + h_box/2,
                          "Target Donasi Terpenuhi /\nBatas Waktu Kampanye Berakhir")

    # Node 4: Completed (Kiri Tengah)
    draw_node(ax, col1_x, row2_y, w_box, h_box,
              "4. Status: Completed",
              "Penggalangan Selesai, Gerbang Ditutup Permanen")

    # Arrow 4 -> 5 (Bawah)
    draw_vertical_arrow(ax, col1_x + w_box/2, row2_y, row3_y + h_box,
                        "Penyerahan Kunci Privat Paillier", label_side='right')

    # --- BARIS 3 ---
    # Node 5: Dekripsi Agregat (Kiri Bawah)
    draw_node(ax, col1_x, row3_y, w_box, h_box,
              "5. Proses: Dekripsi Kunci Privat",
              "Dekripsi Tunggal terhadap Total Saldo Agregat")

    # Arrow 5 -> 6 (Kanan: Garis terlihat jelas & teks di atasnya)
    draw_horizontal_arrow(ax, col1_x + w_box, col2_x, row3_y + h_box/2,
                          "Publikasi Total Dana &\nRekonsiliasi Audit Publik")

    # Node 6: Audited (Kanan Bawah)
    draw_node(ax, col2_x, row3_y, w_box, h_box,
              "6. Status: Audited",
              "Total Dana Terverifikasi Publik & Transparan")

    # Arrow 6 -> End (Bawah)
    end_oval_w = 3.2
    draw_arrow_plain(ax, (col2_x + w_box/2, row3_y), (col2_x + w_box/2, 0.65))

    # End Oval (Kanan Bawah)
    draw_node(ax, col2_x + (w_box - end_oval_w)/2, 0.15, end_oval_w, 0.5, "Selesai: Penyaluran Dana Terbuka", is_oval=True)

    for out_path in ['assets/gambar/preview_gambar6_simple_style.png', 'assets/gambar/gambar7_lifecycle_kampanye.png']:
        plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Generated {out_path} successfully!")
    plt.close()

if __name__ == '__main__':
    generate_preview()
