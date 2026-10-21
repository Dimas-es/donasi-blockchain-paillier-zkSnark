# Katalog Aset Gambar Ilmiah (TrustGive)

Folder ini berisi seluruh aset gambar resmi yang aktif dan disematkan langsung ke dalam naskah Word / Jurnal SIMASI dalam format **PNG resolusi tinggi (300 DPI)** dengan latar belakang putih murni (*white background*).

Berkas kode sumber diagram Mermaid (**`.mmd`**) telah dipisahkan ke dalam subfolder [`mermaid/`](mermaid/). Seluruh berkas eksperimen/draf yang tidak dipakai telah dipisahkan ke dalam subfolder [`arsip_tidak_terpakai/`](arsip_tidak_terpakai/).

---

## Daftar Gambar Resmi yang Aktif dalam Naskah

| No. Gambar di Naskah | Berkas Gambar PNG | Berkas Sumber Diagram | Judul Keterangan Gambar (*Caption*) | Penempatan Bab |
|:---:|---|---|---|---|
| **Gambar 1** | [`gambar1_arsitektur_sistem.png`](gambar1_arsitektur_sistem.png) | `scratch/generate_architecture_block.py` | **Gambar 1. Arsitektur Hibrida Sistem Donasi Terdesentralisasi TrustGive** | **METODE PENELITIAN** (Sub-bab Perancangan Arsitektur) |
| **Gambar 2** | [`gambar2_erd_database.png`](gambar2_erd_database.png) | [`mermaid/gambar2_erd_database.mmd`](mermaid/gambar2_erd_database.mmd) | **Gambar 2. Diagram Relasi Entitas (ERD) Model Data Sistem** | **METODE PENELITIAN** (Sub-bab Desain Basis Data) |
| **Gambar 3** | [`gambar3_workflow_donasi.png`](gambar3_workflow_donasi.png) | [`mermaid/gambar3_workflow_donasi.mmd`](mermaid/gambar3_workflow_donasi.mmd) | **Gambar 3. Diagram Alur Transaksi Donasi End-to-End** | **METODE PENELITIAN** (Sub-bab Alur Transaksi) |
| **Gambar 4** | [`gambar7_lifecycle_kampanye.png`](gambar7_lifecycle_kampanye.png) | `scratch/generate_simple_style_v2.py` | **Gambar 4. Siklus Hidup dan Status Kampanye Donasi** | **METODE PENELITIAN** (Sub-bab Tata Kelola Kampanye) |
| **Gambar 5** | [`gambar5_alur_idempotensi_recovery.png`](gambar5_alur_idempotensi_recovery.png) | [`mermaid/gambar5_alur_idempotensi_recovery.mmd`](mermaid/gambar5_alur_idempotensi_recovery.mmd) | **Gambar 5. Pola Transaksional Idempotensi dan Rekonsiliasi Dual-Write** | **METODE PENELITIAN** (Sub-bab Reliabilitas Transaksi) |
| **Gambar 6** | `assets/jurnal/grafik_konsumsi_gas.png` | `scripts/generate_charts.py` | **Gambar 6. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat** | **HASIL DAN PEMBAHASAN** (Sub-bab Profil Gas) |
| **Gambar 7** | `assets/jurnal/grafik_latensi_e2e.png` | `scripts/generate_charts.py` | **Gambar 7. Distribusi Komponen Latensi End-to-End Transaksi Donasi Sekuensial** | **HASIL DAN PEMBAHASAN** (Sub-bab Latensi E2E) |

---

## Struktur Subfolder
- **[`mermaid/`](mermaid/)**: Memuat seluruh berkas sumber diagram Mermaid (`.mmd`).
- **[`arsip_tidak_terpakai/`](arsip_tidak_terpakai/)**: Memuat seluruh berkas draf, opsi preview, dan skrip uji coba diagram lama yang tidak lagi digunakan dalam naskah.
