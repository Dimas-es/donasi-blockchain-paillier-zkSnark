# 📋 LAPORAN TINJAUAN SEJAWAT (PEER REVIEW REPORT)

**Jurnal:** SIMASI (p-ISSN 2798-835X / e-ISSN 2798-8341)  
**Judul Naskah:** *Studi Desain dan Evaluasi Kinerja Prototipe Sistem Donasi Terdesentralisasi Hibrida Menggunakan Paillier dan ZK-SNARK Groth16 (TrustGive)*  
**Penulis:** Dimas Setiawan, Alam Rahmatulloh  
**Afiliasi:** Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi  
**Tanggal Review:** 21 Oktober 2026  
**Reviewer:** Anonim

---

## 1. Kesesuaian Topik dan Ruang Lingkup Jurnal

| Aspek | Penilaian |
|-------|-----------|
| Kesesuaian Topik | ✅ **Sangat Sesuai** |
| Bidang Jurnal yang Relevan | Keamanan Komputer, Rekayasa Perangkat Lunak, Sistem Terdistribusi, Tata Kelola TI |

### Analisis:
Naskah membahas desain dan evaluasi prototipe sistem donasi terdesentralisasi yang mengintegrasikan kriptografi Paillier Homomorphic Encryption, zk-SNARK Groth16, dan kontrak pintar EVM. Topik ini **sangat relevan** dengan *focus and scope* jurnal SIMASI, khususnya pada bidang:

- **Keamanan Komputer / Keamanan Jaringan Komputer** — penggunaan kriptografi homomorfik dan zero-knowledge proofs
- **Rekayasa Perangkat Lunak** — siklus hidup, arsitektur 3-layer, dan proses rekayasa sistem
- **Sistem Komputasi Terdistribusi** — arsitektur hibrida off-chain/on-chain berbasis blockchain EVM
- **Teknik Data / Pemodelan Data** — pola transactional idempotency, model data PostgreSQL, dan ERD

> [!TIP]
> Kesesuaian topik sangat kuat. Naskah menjembatani beberapa subdomain SIMASI secara koheren.

---

## 2. Kebaruan (Novelty) dan Kontribusi Ilmiah

| Aspek | Penilaian |
|-------|-----------|
| Kebaruan | ⚠️ **Cukup Baik dengan Catatan** |
| Kontribusi | ✅ **Teridentifikasi Jelas** |

### Analisis:

**Kekuatan:**
1. **Integrasi teknis unik**: Kombinasi Paillier AHE + Groth16 zk-SNARK + EVM smart contract pada domain donasi terdesentralisasi belum ditemukan pada implementasi prototipe sebelumnya (berdasarkan tinjauan komparatif Tabel 1 di naskah).
2. **Kontribusi tiga-pilar terformulasi eksplisit**:
   - Arsitektur hibrida 3-layer dengan pembagian beban off-chain/on-chain
   - Evaluasi kinerja empiris terukur (gas consumption, latency, throughput)
   - Pemetaan batasan arsitektur yang jujur dan transparan (honest-but-curious model, binding gap)
3. **Analisis komparatif mendalam** terhadap 5 sistem terdahulu (UpHaaR, Astraea, He et al., Eisdspa, ZeeStar) dengan properti teknis yang spesifik.
4. **Kejujuran akademik**: Penulis secara terbuka mengakui keterbatasan (server HbC, proof-to-ciphertext binding gap, single-party trusted setup) — hal ini justru memperkuat kredibilitas ilmiah.

**Catatan Kritis:**
1. **Bukan sistem baru yang siap produksi**, melainkan studi desain dan evaluasi prototipe. Namun, penulis sudah mengklaim ini dengan tepat pada judul dan kontribusi ("studi desain dan evaluasi kinerja prototipe"). Hal ini dapat diterima.
2. **Perbandingan fair namun belum apple-to-apple sepenuhnya**: Sistem pembanding (Astraea, ZeeStar, Eisdspa) diuji pada platform dan lingkungan yang berbeda. Perbandingan gas bersifat indikatif, bukan benchmarking head-to-head. Penulis sudah menyiratkan hal ini, tetapi perlu dieksplisitkan.

> [!NOTE]
> Kontribusi utama terletak pada **empirical baseline dan transparansi evaluasi arsitektural**, bukan pada terobosan kriptografis baru. Ini legitimate dan bernilai untuk komunitas riset.

---

## 3. Kualitas Setiap Bagian Naskah

### 3.1 Abstrak (Bahasa Inggris & Indonesia)

| Aspek | Penilaian |
|-------|-----------|
| Kelengkapan | ✅ Sangat Baik |
| Kejelasan | ✅ Baik |
| Angka Kuantitatif | ✅ Disertakan |

**Kekuatan:**
- Abstrak bilingual (EN & ID) tersedia, sesuai standar jurnal Indonesia.
- Abstrak memuat: latar belakang masalah, metode, angka hasil kuantitatif (225.035 gas, 613.607 gas, 959.421 gas, 0,035 ms, 1,35 s, ~3,45 s), dan batasan.
- Keywords relevan dan spesifik.

**Catatan Perbaikan:**

> [!WARNING]
> **Abstrak terlalu panjang.** Abstrak bahasa Inggris ~350 kata, abstrak bahasa Indonesia ~370 kata. Sebagian besar jurnal SIMASI/nasional membatasi abstrak pada **150–250 kata**. 
> 
> **Rekomendasi:** Pangkas abstrak menjadi maksimal 250 kata per bahasa. Hilangkan detail teknis minor (misalnya detail SSTORE, event log pattern) dan fokuskan pada kontribusi utama + hasil kunci.

### 3.2 Pendahuluan (Bagian 1)

| Aspek | Penilaian |
|-------|-----------|
| Identifikasi Masalah | ✅ Sangat Baik |
| Kajian Literatur | ✅ Baik |
| Research Gap | ✅ Teridentifikasi |
| Rumusan Kontribusi | ✅ Jelas |

**Kekuatan:**
- Alur argumentasi logis: krisis kepercayaan filantropi → transparansi blockchain → paradoks privasi → solusi kriptografis → tantangan implementasi → kontribusi TrustGive.
- Penyertaan regulasi hukum (GDPR, UU PDP No. 27/2022) menambah relevansi kontekstual.
- Tabel komparatif (Tabel 1) sangat informatif dan memperkuat posisi research gap.
- Tiga tantangan implementasi (biaya gas EVM, dual-write problem, non-native field) diuraikan dengan sitasi yang tepat.

**Catatan Perbaikan:**
1. **Tidak ada pernyataan tujuan penelitian eksplisit** ("penelitian ini bertujuan untuk..."). Meskipun kontribusi tersirat dari teks, pernyataan tujuan formal diperlukan untuk kejelasan akademik.
2. **Tidak ada rumusan masalah formal** (research questions). Penambahan 2-3 research questions akan memperkuat fokus.

### 3.3 Metode Penelitian (Bagian 2)

| Aspek | Penilaian |
|-------|-----------|
| Kejelasan Metodologi | ✅ Sangat Baik |
| Reprodusibilitas | ✅ Baik (Repositori tersedia) |
| Kedalaman Teknis | ✅ Tinggi |
| Struktur | ✅ Terorganisir |

**Kekuatan:**
- Metode diformulasikan dalam 5 tahapan terstruktur yang jelas.
- Formulasi kriptografi Paillier (keygen, enkripsi, akumulasi homomorfik, opening verification) disajikan secara matematis dan benar.
- Analisis komparatif 3 skema (Paillier vs Pedersen vs Exponential ElGamal) sangat mendalam dan informatif, menunjukkan pemahaman kriptografis yang kuat.
- Model ancaman formal (Tabel 2) dengan 7 entitas threat actor merupakan kontribusi arsitektural yang bernilai.
- Sirkuit ZK-SNARK (DonationProof.circom) dideskripsikan dengan sinyal I/O, batasan R1CS, dan analisis soundness field wrapping.
- ERD, diagram alur, dan siklus hidup kampanye tersedia (Gambar 1–5).
- Kode sumber tersedia di GitHub (reprodusibilitas).

**Catatan Perbaikan:**
1. **Justifikasi pemilihan metode "experimental systems engineering"** kurang disertai referensi metodologis. Penulis perlu menyitasi kerangka metodologis ini (misalnya dari literatur software engineering research methodology).
2. **Sub-bagian 2.5 (ERD dan Alur Bisnis)** relatif singkat dibandingkan sub-bagian lainnya. Deskripsi ERD hanya menyebut "disajikan pada Gambar 2" tanpa menjelaskan entitas utama dan relasinya secara naratif.

### 3.4 Hasil dan Pembahasan (Bagian 3)

| Aspek | Penilaian |
|-------|-----------|
| Penyajian Data | ✅ Sangat Baik |
| Analisis Kuantitatif | ✅ Mendalam |
| Rekonsiliasi Aritmetika | ✅ Transparan |
| Identifikasi Keterbatasan | ✅ Jujur & Komprehensif |

**Kekuatan:**
- **Tabel 3 (Profil Gas)**: 10 skenario operasi dengan rincian komponen gas per opcode (base tx, calldata, SSTORE, pairing). Rekonsiliasi aritmetika komponen gas ditunjukkan secara eksplisit — ini merupakan praktik terbaik yang jarang ditemukan.
- **Tabel 4 (Latency)**: 9 operasi kriptografis dengan rata-rata latensi, algoritma, lingkungan eksekusi, dan karakteristik memori.
- **Tabel 5 (Matriks Pengujian)**: 13 skenario uji mencakup fungsional, negatif ZK, reliabilitas, keamanan, dan privasi. Penulis secara eksplisit memberi status "BELUM TERPENUHI (VULNERABLE)" dan "BELUM TERPENUHI (EXPOSED)" — kejujuran ilmiah yang terpuji.
- **Analisis end-to-end latency** dihitung secara transparan: 185ms + 1350ms + 1850ms + 36ms + 35ms ≈ 3.456 ms.
- **Desain optimasi** (hash-in-storage + event log) ~270.000 gas sebagai proyeksi perbaikan.
- **Pembahasan hot-row contention** dan finalitas jaringan publik menunjukkan kesadaran terhadap skalabilitas.

**Catatan Perbaikan:**

> [!IMPORTANT]
> 1. **Pengujian pada Hardhat lokal ≠ jaringan produksi.** Meskipun penulis sudah menyebutkan keterbatasan ini (finalitas instan, tanpa konfirmasi blok), klaim performa harus lebih eksplisit menyatakan bahwa ini adalah **lingkungan terisolasi** dan hasil dapat berbeda signifikan pada mainnet/testnet publik.
> 2. **Iterasi pengujian**: Tabel 4 menyebut "rata-rata dari 100 iterasi independen" — ini baik. Namun, **tidak ada standar deviasi, confidence interval, atau distribusi statistik** yang dilaporkan. Untuk riset eksperimental, minimal sertakan mean ± std dev.
> 3. **Tidak ada grafik/chart**: Seluruh data disajikan dalam tabel. Penambahan grafik batang (bar chart) untuk perbandingan gas atau line chart untuk latency akan meningkatkan readability.
> 4. **Sub-bagian 3.4 (Analisis Keamanan dan Agenda Lanjutan)** lebih tepat dipisahkan: analisis keamanan di bagian Pembahasan, dan agenda lanjutan di bagian Kesimpulan atau bagian terpisah "Future Work."

### 3.5 Kesimpulan (Bagian 4)

| Aspek | Penilaian |
|-------|-----------|
| Ringkasan Temuan | ✅ Lengkap |
| Kesesuaian dengan Tujuan | ✅ Konsisten |
| Future Work | ✅ Spesifik |

**Kekuatan:**
- Kesimpulan merangkum temuan utama secara kuantitatif (mengulang angka kunci).
- Agenda penelitian lanjutan (SAVER, client-side prover, replay protection) spesifik dan actionable.
- Penulis tidak overclaim hasil melebihi apa yang dievaluasi.

**Catatan Perbaikan:**
1. **Kesimpulan terlalu panjang** (2 paragraf padat ~300 kata). Idealnya ringkas dan padat, tanpa mengulang angka detail yang sudah ada di bagian Hasil.
2. **Tidak ada implikasi praktis/teoretis** yang disampaikan secara eksplisit. Tambahkan 1-2 kalimat tentang implikasi temuan terhadap pengembangan sistem donasi digital di Indonesia atau komunitas open-source.

---

## 4. Ketepatan Metodologi, Validitas Data, dan Kekuatan Analisis

| Aspek | Penilaian |
|-------|-----------|
| Validitas Internal | ⚠️ **Cukup Baik (Catatan Penting)** |
| Validitas Eksternal | ⚠️ **Terbatas (Diakui Penulis)** |
| Kekuatan Analisis | ✅ **Baik** |

### Catatan Detail:

1. **Formulasi Kriptografis**: Formulasi Paillier (keygen, enc, homomorphic accumulation, opening verification) **secara matematis benar** dan konsisten dengan literatur (Paillier 1999; Yang et al. 2023).

2. **Analisis Komparatif Paillier vs Pedersen vs ElGamal**: Trade-off analysis ini sangat bernilai dan menunjukkan pemahaman mendalam. Argumentasi pemilihan Paillier (dekripsi langsung vs BSGS ElGamal, vs koordinasi r_i Pedersen) **logis dan terjustifikasi**.

3. **Sirkuit ZK-SNARK**: Deskripsi DonationProof.circom (4 sinyal, batasan R1CS, Poseidon commitment) konsisten. Pembahasan kerentanan field wrapping dan rekomendasi Num2Bits(64) menunjukkan pemahaman soundness.

4. **Pengujian Gas**: Rekonsiliasi aritmetika gas **terverifikasi internal** (penjumlahan komponen = total terukur). Ini menunjukkan data bukan fabricated.

> [!WARNING]
> **Keterbatasan Validitas:**
> - Pengujian dilakukan pada **satu mesin tunggal** (i5-8250U, 8GB RAM). Tidak ada pengujian pada hardware/OS berbeda untuk validasi cross-platform.
> - Hardhat lokal memberikan **kondisi ideal** (tanpa network latency, tanpa mempool congestion, tanpa biaya gas real). 
> - **Tidak ada statistical testing** (t-test, confidence interval) pada data latensi.
> - Angka "~270.000 gas" untuk desain optimasi bersifat **proyeksi/estimasi**, bukan hasil pengujian langsung.

---

## 5. Kualitas Referensi, Relevansi Sitasi, dan Kemutakhiran Pustaka

| Aspek | Penilaian |
|-------|-----------|
| Jumlah Referensi | ✅ Memadai (29 referensi) |
| Kemutakhiran | ✅ Sangat Baik |
| Relevansi | ✅ Tinggi |
| Variasi Sumber | ⚠️ Cukup Baik |

### Analisis Referensi:

**Distribusi Tahun Publikasi:**

| Tahun | Jumlah | Persentase |
|-------|--------|------------|
| 2016 | 1 | 3,4% |
| 1999 | 1 | 3,4% |
| 2019 | 1 | 3,4% |
| 2020 | 2 | 6,9% |
| 2021 | 3 | 10,3% |
| 2022 | 5 | 17,2% |
| 2023 | 4 | 13,8% |
| 2024 | 7 | 24,1% |
| 2025 | 3 | 10,3% |
| 2026 | 1 | 3,4% |
| Regulasi (2022) | 1 | 3,4% |

**Kekuatan:**
- **79,3% referensi dari tahun 2021–2026** — sangat mutakhir dan up-to-date.
- Referensi seminal (Paillier 1999, Groth 2016) disertakan dengan tepat.
- Sitasi bersumber dari venue berkualitas: IEEE S&P, USENIX Security, EUROCRYPT, IEEE TDSC, IEEE OJCOMS, Springer.
- Regulasi nasional (UU PDP 2022) memperkuat relevansi lokal.

**Catatan Perbaikan:**

> [!NOTE]
> 1. **Proporsi arXiv preprint cukup tinggi** (~11 dari 29 referensi, ~38%). Meskipun preprint merupakan sumber yang sah dalam bidang kriptografi/blockchain, reviewer editorial mungkin meminta penggantian sebagian preprint dengan versi peer-reviewed (jika tersedia).
> 2. **Tidak ada referensi dari jurnal SIMASI sendiri.** Meskipun bukan wajib, penyertaan 1-2 referensi dari jurnal target menunjukkan familiaritas penulis dengan ekosistem jurnal.
> 3. **Dewangan & Msahli (2026)** — referensi tahun 2026 berpotensi menimbulkan pertanyaan reviewer mengenai status publikasinya (apakah sudah terbit atau masih preprint/forthcoming).

---

## 6. Konsistensi Penulisan, Struktur Artikel, Tata Bahasa, dan Format Jurnal

### 6.1 Kesesuaian dengan Template SIMASI

| Aspek | Status | Detail |
|-------|--------|--------|
| Header Tabel Jurnal | ⚠️ **Perlu Diperiksa** | Template memiliki tabel header dengan ISSN dan logo di halaman pertama. Naskah memiliki tabel header tetapi perlu diverifikasi kesesuaian visual. |
| Styles Dokumen | ❌ **Tidak Sesuai** | Template menggunakan styles bervariasi (Title, Heading 1, Heading 2, Body Text, Caption, List Paragraph). **Naskah menggunakan style "Normal" untuk SELURUH paragraf (117 paragraf, 100% Normal).** |
| Page Layout | ✅ **Sesuai** | Ukuran halaman (Letter), margin (1 inch all sides) — sama. |
| Penomoran Bagian | ⚠️ **Berbeda** | Template: PENDAHULUAN (tanpa nomor) → METODE PENELITIAN → HASIL DAN PEMBAHASAN → KESIMPULAN → DAFTAR PUSTAKA. Naskah: 1. PENDAHULUAN → 2. METODE → 3. HASIL → 4. KESIMPULAN → 5. DAFTAR PUSTAKA (dengan nomor). |

> [!CAUTION]
> **Temuan Format Kritis:**
> 
> **Seluruh paragraf naskah menggunakan style "Normal" (100%).** Template SIMASI menggunakan styles terdiferensiasi:
> - **Title** untuk judul naskah
> - **Heading 1** untuk judul bagian utama (PENDAHULUAN, METODE, dll.)
> - **Heading 2** untuk sub-bagian
> - **Body Text** untuk isi paragraf
> - **Caption** untuk keterangan gambar/tabel
> - **List Paragraph** untuk daftar/enumerasi
> 
> Ini merupakan **ketidaksesuaian format yang signifikan** dan harus diperbaiki sebelum submission.

### 6.2 Penomoran Bagian

| Template SIMASI | Naskah TrustGive |
|-----------------|------------------|
| PENDAHULUAN (tanpa nomor) | 1. PENDAHULUAN |
| METODE PENELITIAN (tanpa nomor) | 2. METODE PENELITIAN |
| HASIL DAN PEMBAHASAN (tanpa nomor) | 3. HASIL DAN PEMBAHASAN |
| KESIMPULAN (tanpa nomor) | 4. KESIMPULAN |
| DAFTAR PUSTAKA (tanpa nomor) | 5. DAFTAR PUSTAKA |

> [!WARNING]
> Template contoh SIMASI **tidak menggunakan penomoran** pada heading bagian utama. Naskah menggunakan penomoran (1., 2., 3., 4., 5.). Sesuaikan dengan template jurnal.

### 6.3 Tata Bahasa dan Kualitas Penulisan

| Aspek | Penilaian |
|-------|-----------|
| Bahasa Indonesia | ✅ Baik — akademis dan formal |
| Bahasa Inggris (Abstract) | ✅ Baik — gramatikal dan koherent |
| Konsistensi Istilah | ⚠️ Catatan minor |
| Ejaan | ✅ Baik |

**Catatan Minor:**
1. **Konsistensi istilah**: "kontrak pintar" vs "smart contract" — kedua istilah digunakan bergantian. Pilih satu dan gunakan secara konsisten (dengan menyebutkan padanan di kurung pada penggunaan pertama).
2. **Penggunaan tanda baca**: Pemisah desimal menggunakan koma (0,035 ms) untuk bahasa Indonesia dan titik (0.035 ms) di abstract bahasa Inggris — ini **sudah benar** dan konsisten dengan konvensi masing-masing bahasa.
3. **Singkatan**: AHE, EVM, ZK-SNARK, dll. sudah didefinisikan pada penggunaan pertama — ✅ baik.

### 6.4 Struktur Artikel

| Komponen | Status |
|----------|--------|
| Judul | ✅ Informatif dan deskriptif |
| Penulis & Afiliasi | ✅ Tersedia |
| Abstrak EN | ✅ Tersedia (terlalu panjang) |
| Abstrak ID | ✅ Tersedia (terlalu panjang) |
| Keywords | ✅ Tersedia (EN & ID) |
| Pendahuluan | ✅ Tersedia |
| Metode | ✅ Tersedia (5 sub-bagian) |
| Hasil & Pembahasan | ✅ Tersedia (4 sub-bagian) |
| Kesimpulan | ✅ Tersedia |
| Daftar Pustaka | ✅ Tersedia (29 referensi) |
| Gambar | ✅ 5 gambar tersedia |
| Tabel | ✅ 5 tabel tersedia |

---

## 7. Kelemahan, Inkonsistensi, dan Potensi Penolakan

### 7.1 Kelemahan Mayor (Wajib Diperbaiki)

| No | Kelemahan | Dampak | Rekomendasi |
|----|-----------|--------|-------------|
| M1 | **Seluruh paragraf menggunakan style "Normal"** — tidak mengikuti template SIMASI yang menuntut styles terdiferensiasi (Title, Heading 1, Body Text, Caption, dll.) | Dapat menyebabkan pengembalian naskah oleh editorial sebelum review | Aplikasikan styles sesuai template SIMASI pada setiap paragraf |
| M2 | **Abstrak terlalu panjang** (~350 kata EN, ~370 kata ID) | Melebihi batas umum 150-250 kata jurnal nasional | Pangkas menjadi maksimal 250 kata per bahasa |
| M3 | **Tidak ada pernyataan tujuan penelitian dan rumusan masalah eksplisit** di Pendahuluan | Kelemahan struktural standar penulisan ilmiah | Tambahkan paragraf rumusan masalah dan tujuan sebelum kontribusi |
| M4 | **Tidak ada ukuran statistik** (standar deviasi, confidence interval) pada data pengujian latensi | Melemahkan validitas eksperimental | Tambahkan mean ± std dev minimal untuk Tabel 4 |
| M5 | **Penomoran heading** (1., 2., 3., 4., 5.) tidak sesuai template SIMASI yang tidak menggunakan nomor | Ketidaksesuaian format | Sesuaikan dengan template: hapus nomor atau verifikasi dengan editor |

### 7.2 Kelemahan Minor (Disarankan Diperbaiki)

| No | Kelemahan | Rekomendasi |
|----|-----------|-------------|
| m1 | Tidak ada visualisasi grafik (chart/diagram) untuk data kuantitatif | Tambahkan 1-2 bar chart untuk perbandingan gas atau latency |
| m2 | Sub-bagian 3.4 mencampurkan analisis keamanan dengan agenda penelitian lanjutan | Pisahkan: analisis keamanan tetap di Pembahasan, future work ke Kesimpulan |
| m3 | Deskripsi ERD (sub-bagian 2.5) terlalu ringkas | Jelaskan entitas utama dan relasi secara naratif |
| m4 | ~38% referensi adalah arXiv preprint | Ganti dengan versi peer-reviewed jika tersedia |
| m5 | Proyeksi gas ~270.000 belum divalidasi secara empiris | Tandai lebih eksplisit sebagai "estimasi berbasis kalkulasi" atau implementasikan |
| m6 | Kesimpulan terlalu panjang dan repetitif | Ringkas, hindari mengulang angka detail |
| m7 | Tidak ada implikasi praktis/teoretis eksplisit di Kesimpulan | Tambahkan 1-2 kalimat implikasi |
| m8 | Referensi Dewangan & Msahli (2026) — perlu klarifikasi status publikasi | Verifikasi apakah sudah terbit atau masih preprint |

### 7.3 Kekuatan Utama yang Perlu Dipertahankan

| No | Kekuatan |
|----|----------|
| S1 | Formulasi kriptografis yang benar dan mendalam (Paillier, Groth16, Poseidon) |
| S2 | Analisis komparatif 3 skema HE sangat informatif dan menunjukkan pemahaman ahli |
| S3 | Tabel komparatif (Tabel 1) terhadap 5 sistem terdahulu — sangat bernilai |
| S4 | Model ancaman formal 7 entitas (Tabel 2) — jarang ditemukan di jurnal sejenis |
| S5 | Rekonsiliasi aritmetika gas transparan — meningkatkan kepercayaan data |
| S6 | Matriks pengujian 13 skenario dengan kejujuran status (VULNERABLE, EXPOSED) |
| S7 | Repositori GitHub tersedia untuk reprodusibilitas |
| S8 | Referensi sangat mutakhir (79% dari 2021-2026) |
| S9 | Kejujuran akademik dalam mengakui batasan arsitektur |

---

## 8. Rekomendasi Keputusan Editorial

### 🟡 KEPUTUSAN: **MINOR REVISION**

### Alasan:

1. **Kualitas konten ilmiah sangat baik** — formulasi kriptografis benar, evaluasi empiris terukur, analisis mendalam, dan kejujuran akademik terhadap keterbatasan. Naskah menunjukkan penguasaan domain yang kuat di persimpangan kriptografi, rekayasa perangkat lunak, dan teknologi blockchain.

2. **Kebaruan dan kontribusi teridentifikasi jelas** — meskipun bukan terobosan kriptografis, studi desain hibrida dan baseline empiris ini bernilai untuk komunitas riset, terutama mengingat kelangkaan implementasi prototipe yang mengintegrasikan Paillier + Groth16 + EVM pada domain filantropi.

3. **Kesesuaian topik sangat kuat** dengan scope jurnal SIMASI.

4. **Revisi yang diperlukan bersifat formatif, bukan substantif:**
   - Perbaikan format dokumen (styles, heading, abstrak panjang) — ini adalah pekerjaan teknis formatting
   - Penambahan rumusan masalah/tujuan — struktural, tidak mengubah substansi
   - Penambahan statistik deskriptif pada Tabel 4 — menambah rigor tanpa mengubah temuan
   - Penyesuaian penomoran heading — copy editing

5. **Tidak ada cacat metodologis fundamental** yang memerlukan pengulangan eksperimen atau redesain penelitian.

### Ringkasan Revisi yang Diminta:

| Prioritas | Item | Estimasi Upaya |
|-----------|------|----------------|
| **Wajib** | Aplikasikan styles template SIMASI | 1-2 jam |
| **Wajib** | Pangkas abstrak (max 250 kata per bahasa) | 30 menit |
| **Wajib** | Tambahkan rumusan masalah & tujuan penelitian eksplisit | 30 menit |
| **Wajib** | Tambahkan std dev/CI pada data latensi Tabel 4 | 1 jam (re-run benchmark) |
| **Wajib** | Sesuaikan penomoran heading dengan template | 15 menit |
| *Disarankan* | Tambahkan grafik visualisasi data | 1 jam |
| *Disarankan* | Pisahkan analisis keamanan dari future work | 30 menit |
| *Disarankan* | Perkuat deskripsi ERD di sub-bagian 2.5 | 30 menit |

### Perkiraan Kesiapan:

> Setelah revisi minor dilaksanakan (estimasi 1-2 hari kerja), naskah **siap untuk diterbitkan**. Substansi ilmiah, kedalaman teknis, dan integritas akademik naskah sudah memenuhi standar publikasi. Revisi yang diperlukan bersifat formatif dan presentasional.

---

*Demikian laporan tinjauan ini disusun secara objektif berdasarkan isi naskah dan standar publikasi ilmiah. Reviewer mengapresiasi kedalaman teknis dan kejujuran akademik penulis dalam menyajikan studi ini.*
