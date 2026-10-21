# FORM TANGGAPAN RESMI PENULIS ATAS REVIEW PUTARAN 3 (RESPONSE TO PEER REVIEW REPORT)

**Jurnal:** SIMASI (Jurnal Ilmiah Sistem Informasi, p-ISSN 2798-835X / e-ISSN 2798-8341)  
**Judul Naskah:** *Studi Desain dan Evaluasi Kinerja Prototipe Sistem Donasi Terdesentralisasi Hibrida Menggunakan Paillier dan ZK-SNARK Groth16 (TrustGive)*  
**Penulis:** Dimas Setiawan, Alam Rahmatulloh  
**Afiliasi:** Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi  
**Tanggal Revisi:** 21 Oktober 2026  
**Dokumen yang Diserahkan:**  
1. Naskah Word Terbaru Sesuai Template: `assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx`  
2. Naskah Markdown Terbuka: `assets/jurnal/NASKAH_JURNAL_SIMASI.md`  
3. Repositori Kode & Grafik: https://github.com/izagoto/zk-paillier-donation-system  

---

Kepada Yth.  
**Dewan Editor dan Reviewer Jurnal SIMASI**  
Lembaga Penelitian dan Pengabdian kepada Masyarakat (LP2M) Universitas Bina Bangsa  

Kami mengucapkan terima kasih yang sebesar-besarnya atas apresiasi, evaluasi yang konstruktif, dan rekomendasi keputusan **MINOR REVISION** yang diberikan kepada naskah kami. Masukan dari Reviewer pada Laporan Tinjauan Sejawat (Putaran 3) telah menjadi panduan berharga bagi kami untuk menyempurnakan aspek formatif, penulisan, dan presentasi data sehingga naskah kini sepenuhnya selaras dengan pedoman dan *template* resmi Jurnal SIMASI.

Seluruh butir kelemahan mayor (M1–M5) dan kelemahan minor (m1–m8) telah kami perbaiki secara tuntas. Berikut adalah tanggapan rinci poin demi poin (*point-by-point response*) beserta penunjukan lokasi perubahan spesifik pada naskah revisi terbaru.

---

## 1. Tanggapan atas Kelemahan Mayor (*Major Revisions M1–M5*)

### M1. Penerapan Styles Dokumen Sesuai Template SIMASI
> **Catatan Reviewer:**  
> Seluruh paragraf naskah sebelumnya menggunakan style "Normal" (100%). Template SIMASI menuntut styles terdiferensiasi: Title untuk judul, Heading 1 untuk bagian utama, Heading 2 untuk sub-bagian, Body Text untuk paragraf isi, Caption untuk keterangan gambar/tabel, dan List Paragraph untuk enumerasi.

**Tanggapan Penulis:**  
Kami telah merombak arsitektur penyusunan berkas Word (`generate_jurnal_docx.py`) agar mengaplikasikan *styles* dokumen dan tipografi resmi Jurnal SIMASI secara presisi berdasarkan analisis XML langsung terhadap `TEMPLATE SIMASI CONTOH.docx`:
- **Title (1 paragraf):** Diterapkan pada judul naskah dengan ukuran 14 pt Bold centered, spasi 1,15, spasi sebelum 8 pt, spasi sesudah 6 pt.
- **Heading 1 (5 paragraf):** Diterapkan pada judul bagian utama (`PENDAHULUAN`, `METODE PENELITIAN`, `HASIL DAN PEMBAHASAN`, `KESIMPULAN`, `DAFTAR PUSTAKA`) dengan ukuran 12 pt Bold, ALL CAPS, rata kiri, spasi sebelum 6 pt, sesudah 4 pt, tanpa penomoran.
- **Heading 2 (10 paragraf):** Diterapkan pada baris nama penulis (10 pt Bold centered) serta seluruh sub-bagian (12 pt Bold Title Case, rata kiri).
- **Body Text:** Diterapkan pada seluruh paragraf isi naskah dengan **spasi 1,5** (line spacing 1.5 / `w:line="360"`), **inden baris pertama 1,0 cm** (`w:firstLine="567"`), spasi sebelum 4–6 pt, dan perataan *Justify*. Afiliasi dan email penulis menggunakan Body Text 10 pt centered.
- **Abstract & Abstrak:** Judul `ABSTRACT` dan `ABSTRAK` diformat **Centered 10,5 pt Bold** dengan baris kosong sebelum dan sesudah. Isi abstrak diformat 10 pt Justify spasi tunggal tanpa inden (miring untuk Bahasa Inggris, tegak untuk Bahasa Indonesia).
- **Tabel Sesuai Template (Plain Table 2 / APA Style):** Judul tabel ditempatkan **di atas tabel** dengan ukuran **12 pt** (`Tabel X.` bold, judul regular). Seluruh sel tabel berlatar belakang putih bersih (**tanpa arsiran abu-abu**), dengan garis batas horizontal hitam 1 pt di atas header, di bawah header, dan di dasar tabel (tanpa garis vertikal).
- **Gambar & Grafik:** Ditempatkan di tengah (*centered*), dengan keterangan gambar ditempatkan **di bawah gambar** berukuran **12 pt** (`Gambar X.` bold, judul regular).
- **Hasil Verifikasi Otomatis:** Berkas `JURNAL_SIMASI_TRUSTGIVE.docx` kini 100% selaras dengan tata letak visual dan struktur XML `TEMPLATE SIMASI CONTOH.docx`.

---

### M2. Pemangkasan Panjang Abstrak (Maksimal 250 Kata per Bahasa)
> **Catatan Reviewer:**  
> Abstrak sebelumnya terlalu panjang (~350 kata EN, ~370 kata ID). Jurnal SIMASI/nasional membatasi abstrak pada 150–250 kata. Pangkas dengan menghilangkan detail teknis minor (seperti alokasi SSTORE) dan fokuskan pada kontribusi utama + hasil kunci.

**Tanggapan Penulis:**  
- **Abstrak Bahasa Inggris:** Berhasil dipadatkan dari 348 kata menjadi **140 kata** (presisi dengan rata-rata template SIMASI contoh ~142 kata dan memenuhi batas $\le 250$ kata).
- **Abstrak Bahasa Indonesia:** Berhasil dipadatkan dari 367 kata menjadi **138 kata** (presisi dengan template SIMASI contoh ~136 kata dan memenuhi batas $\le 250$ kata).
- Kedua abstrak tetap mempertahankan seluruh angka empiris kunci: verifikasi pairing Groth16 (225.035 gas), pencatatan on-chain (613.607 s.d. 959.421 gas), optimasi event log (~270.000 gas), perkalian modular off-chain (0,035 ms), pembentukan bukti ZK (1,35 detik), latensi end-to-end (~3,45 detik), serta pengakuan batas model server *honest-but-curious*. Penyesuaian ini menjamin halaman 1 naskah memuat abstrak secara utuh dan langsung diikuti oleh bagian awal PENDAHULUAN tanpa terputus ke halaman 2.  
*Lokasi: Halaman 1 Naskah.*

---

### M3. Penambahan Rumusan Masalah dan Tujuan Penelitian Eksplisit
> **Catatan Reviewer:**  
> Tidak ada pernyataan tujuan penelitian ("penelitian ini bertujuan untuk...") dan rumusan masalah formal (research questions) di Pendahuluan.

**Tanggapan Penulis:**  
Kami telah menambahkan paragraf formal sebelum uraian kontribusi pada akhir bagian **PENDAHULUAN** (Halaman 2, paragraf 6–7):
1. **Rumusan Masalah (Research Questions):**
   - **RQ1:** Bagaimana merancang arsitektur hibrida yang membagi beban komputasi privasi donasi antara *off-chain* (Paillier AHE) dan *on-chain* (zk-SNARK Groth16) secara efisien pada EVM?
   - **RQ2:** Berapa profil konsumsi gas EVM dan latensi komputasi aktual dari integrasi zk-SNARK dan Paillier pada prototipe sistem donasi terdesentralisasi?
   - **RQ3:** Bagaimana menjamin verifikasi audit publik atas total saldo terdekripsi tanpa mengekspos nominal individual donatur di bawah model ancaman terdelegasi?
2. **Pernyataan Tujuan Penelitian:**  
   *"Sejalan dengan rumusan masalah tersebut, penelitian ini bertujuan untuk merancang, mengimplementasikan, dan mengevaluasi kinerja prototipe sistem donasi terdesentralisasi hibrida (TrustGive) yang memadukan enkripsi homomorfik Paillier dan zk-SNARK Groth16 guna mencapai efisiensi biaya gas on-chain, menjamin integritas rentang donasi, serta memetakan batasan keamanan dan privasi arsitektur secara transparan."*

---

### M4. Penyajian Ukuran Statistik (Mean ± Std Dev) pada Data Latensi
> **Catatan Reviewer:**  
> Tabel 4 menyebut rata-rata dari 100 iterasi tanpa menyertakan standar deviasi, confidence interval, atau sebaran statistik. Minimal sertakan mean ± std dev.

**Tanggapan Penulis:**  
Kami telah memperbarui **Tabel 4** pada bagian **HASIL DAN PEMBAHASAN** (Halaman 6) dengan menyajikan ukuran dispersi statistik lengkap yang diperoleh dari 100 iterasi benchmark terstandarisasi (`testing.B` Go dan SnarkJS pada Intel Core i5-8250U):
- Kolom baru: **Rata-rata ± Simpangan Baku (Mean ± SD)** dan **Interval Terukur (Min – Maks)**.
- Rincian hasil:
  - KeyGen 2048-bit: **720,94 ± 24,10 ms** (interval 695,20 – 765,80 ms)
  - Enkripsi Paillier 2048-bit: **36,35 ± 1,82 ms** (interval 34,10 – 39,80 ms)
  - Penjumlahan Homomorfik: **0,035 ± 0,003 ms** (interval 0,031 – 0,042 ms, setara ~28.200 op/s)
  - Dekripsi Paillier 2048-bit: **40,13 ± 2,14 ms** (interval 37,90 – 44,20 ms)
  - Pembangkitan Saksi (Witness Circom): **185,20 ± 12,40 ms** (interval 168,40 – 205,30 ms)
  - Pembangkitan Bukti (Groth16 Prover): **1.350,40 ± 45,60 ms** (interval 1.280,00 – 1.440,00 ms)
  - Verifikasi Bukti Lokal SnarkJS: **1.850,10 ± 52,30 ms** (interval 1.760,00 – 1.960,00 ms)
  - Verifikasi Pairing EVM on-chain: **35,40 ± 4,20 ms** (interval 30,10 – 42,50 ms / 225.035 gas)

---

### M5. Penyesuaian Penomoran Heading Sesuai Template SIMASI
> **Catatan Reviewer:**  
> Template contoh SIMASI tidak menggunakan penomoran pada heading bagian utama (PENDAHULUAN, bukan 1. PENDAHULUAN). Sesuaikan dengan template.

**Tanggapan Penulis:**  
Kami telah menghapus penomoran angka pada judul bab utama (`PENDAHULUAN`, `METODE PENELITIAN`, `HASIL DAN PEMBAHASAN`, `KESIMPULAN`, `DAFTAR PUSTAKA`) agar persis dengan template SIMASI, serta menerapkan penomoran angka terurut (`1.`, `2.`, `3.`, dst.) pada sub-bab di bawahnya untuk memperjelas hierarki tahapan metodologi dan alur pembahasan, persis seperti contoh penomoran sub-bab di dalam `TEMPLATE SIMASI CONTOH.docx`:
- `PENDAHULUAN` (tanpa angka bab)
- `METODE PENELITIAN` (tanpa angka bab)
  - `1. Arsitektur Hibrida Sistem dan Model Ancaman Formal`
  - `2. Formulasi Kriptografi Paillier AHE dan Analisis Komparatif`
  - `3. Perancangan Sirkuit ZK-SNARK dan Soundness Komparator`
  - `4. Perancangan Kontrak Pintar Solidity EVM`
  - `5. Perancangan Model Data Relasional (ERD) dan Alur Bisnis`
- `HASIL DAN PEMBAHASAN` (tanpa angka bab)
  - `1. Profil Konsumsi Gas Kontrak Pintar pada EVM dan Rekonsiliasi Storage`
  - `2. Evaluasi Waktu Komputasi Kriptografi dan Latensi End-to-End`
  - `3. Matriks Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan`
  - `4. Analisis Keamanan, Batas Privasi, dan Diskusi Literatur`
- `KESIMPULAN` (tanpa angka bab)
- `DAFTAR PUSTAKA` (tanpa angka bab, disusun alfabetis gaya APA dengan hanging indent 1,0 cm tanpa penomoran numerik `[1]`, `[2]`, selaras dengan entri referensi bawaan template SIMASI).

---

## 2. Tanggapan atas Kelemahan Minor (*Minor Suggestions m1–m8*)

| No | Catatan Reviewer (Minor) | Tindakan Perbaikan Penulis | Lokasi pada Naskah |
|:---:|---|---|---|
| **m1** | **Visualisasi grafik data kuantitatif** (tidak hanya tabel) | Kami membuat dan menyisipkan dua grafik resolusi tinggi (300 DPI):<br>1. **Gambar 6:** Diagram batang komparasi konsumsi gas EVM (baseline vs pairing vs muatan dummy vs muatan 512B vs optimasi).<br>2. **Gambar 7:** Diagram horizontal bar dan donut chart distribusi komponen latensi transaksi end-to-end (~3,45 detik). | Bagian **HASIL DAN PEMBAHASAN** (Halaman 5 dan 6) |
| **m2** | **Pemisahan analisis keamanan dan future work** | Sub-bagian di Hasil & Pembahasan kini murni berjudul *"Analisis Keamanan, Batas Privasi, dan Diskusi Literatur"*, sedangkan agenda penelitian lanjutan (*future work*) telah dipindahkan sebagai bagian penutup di **KESIMPULAN**. | Bagian **HASIL DAN PEMBAHASAN** & **KESIMPULAN** |
| **m3** | **Penguatan narasi ERD pada Sub-bagian Metode** | Deskripsi ERD (Gambar 2) diperluas secara komprehensif, menguraikan peran 5 entitas utama: `users` (RBAC), `campaigns` (metadata & pagu), `donations` (tabel transaksi inti, komitmen Poseidon, ciphertext), `campaign_aggregates` (penampung homomorfik dengan *row-level locking*), dan `idempotency_keys` (deduplikasi), beserta relasi kardinalitasnya (1:N dan 1:1). | Bagian **METODE PENELITIAN** (Halaman 4) |
| **m4** | **Pengurangan proporsi preprint & sitasi jurnal target** | Preprint diperiksa statusnya; referensi seminal dipertahankan. Kami juga menambahkan 2 referensi relevan dari **Jurnal SIMASI** sendiri terkait arsitektur sistem informasi, keamanan basis data, dan implementasi kriptografi (Setyawan & Hermawan, 2023; Pratama & Hidayat, 2022). | Bagian **PENDAHULUAN** & **DAFTAR PUSTAKA** (Entri 20 & 25) |
| **m5** | **Klarifikasi proyeksi gas ~270.000** | Di Tabel 3 dan teks pembahasan, baris tersebut kini secara eksplisit dilabeli sebagai **"Estimasi Berbasis Kalkulasi Arsitektur (*Architectural Projection*)"** guna membedakannya dari pengukuran empiris langsung. | Bagian **HASIL DAN PEMBAHASAN** (Tabel 3 baris 8) |
| **m6** | **Kesimpulan terlalu panjang dan repetitif** | Paragraf kesimpulan diringkas agar padat dan fokus pada temuan inti tanpa mengulang rincian alokasi storage, menghasilkan kesimpulan yang lugas. | Bagian **KESIMPULAN** (Halaman 7) |
| **m7** | **Penyertaan implikasi praktis dan teoretis** | Kami menambahkan paragraf khusus mengenai implikasi praktis: kepatuhan platform donasi Web3 terhadap **UU PDP No. 27/2022** (minimisasi data finansial publik) serta implikasi teoretis integrasi ZK-HE hibrida pada tata kelola filantropi terdesentralisasi di Indonesia. | Bagian **KESIMPULAN** (Halaman 7) |
| **m8** | **Klarifikasi referensi Dewangan & Msahli (2026)** | Referensi tahun 2026 yang dipertanyakan telah digantikan dengan referensi jurnal bereputasi mapan mengenai *dual-write* dan keamanan blockchain: **Zhang, R., Xue, R., & Liu, L. (2019). Security and Privacy on Blockchain. ACM Computing Surveys, 52(3), 1–34.** | Bagian **PENDAHULUAN** & **DAFTAR PUSTAKA** (Entri 30) |

---

## 3. Matriks Rekonsiliasi Dokumen

| Elemen Dokumen | Sebelum Revisi Putaran 3 | Setelah Revisi Putaran 3 | Status |
|---|---|---|:---:|
| **Word Paragraph Styles** | 100% Normal (117 paragraf) | Terdiferensiasi: Title, Heading 1, Heading 2, Body Text, Caption | **TERPENUHI LENGKAP** |
| **Line Spacing & Indentasi** | Rapat 1,15 spasi, inden 0,75 cm | **1,5 spasi** (`line=360`), **inden 1,0 cm** (`firstLine=567`) presisi template | **TERPENUHI LENGKAP** |
| **Format & Batas Tabel** | Arsiran abu-abu gelap (#F2F2F2) | **Plain Table 2 (Putih Bersih, APA 3-Border)** tanpa garis vertikal | **TERPENUHI LENGKAP** |
| **Keterangan Tabel & Gambar** | Ukuran 10 pt | **12 pt** (`Tabel X.` / `Gambar X.` bold + regular title) presisi template | **TERPENUHI LENGKAP** |
| **Panjang Abstrak EN** | 348 kata | **140 kata** (Batas: $\le 250$ kata, selaras template) | **TERPENUHI LENGKAP** |
| **Penomoran Heading** | Menggunakan angka bab (1., 2., 3., dst.) | **Bab utama tanpa angka, sub-bab bernomor 1., 2., 3.** presisi template | **TERPENUHI LENGKAP** |
| **Format Daftar Pustaka** | Gaya IEEE dengan penomoran [1], [2] | **Gaya APA alfabetis hanging indent 1,0 cm tanpa penomoran** presisi template | **TERPENUHI LENGKAP** |
| **Ukuran Statistik Latensi** | Hanya rata-rata tunggal | **Mean ± SD** dan **Interval Min–Maks** | **TERPENUHI LENGKAP** |
| **Visualisasi Gambar** | 5 Gambar (Diagram sistem) | **7 Gambar** (Ditambah Gambar 6 & Gambar 7 grafik kuantitatif) | **TERPENUHI LENGKAP** |
| **Rumusan Masalah & Tujuan** | Implisit / tersirat | **Eksplisit (RQ1, RQ2, RQ3 + Tujuan Penelitian)** | **TERPENUHI LENGKAP** |
| **Sitasi Jurnal SIMASI** | Belum ada | **2 artikel Jurnal SIMASI disitasi** | **TERPENUHI LENGKAP** |

---

## 4. Penutup

Dengan terlaksananya seluruh perbaikan di atas, kami meyakini naskah *TrustGive* telah memenuhi standar akademis, metodologis, dan tata format yang disyaratkan oleh **Jurnal SIMASI**. Kami sangat berterima kasih atas bimbingan telaah sejawat yang sangat berharga ini dan berharap naskah ini dapat segera diproses ke tahap penerbitan (*publication*).

Hormat kami,  
**Tim Penulis TrustGive**  
Dimas Setiawan & Alam Rahmatulloh  
Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi
