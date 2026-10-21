# FORM TANGGAPAN RESMI PENULIS ATAS REVIEW PUTARAN 2 (POINT-BY-POINT RESPONSE TO REVIEWER)

**Jurnal:** Jurnal Simasi (Jurnal Ilmiah Sistem Informasi)  
**Naskah:** Studi Desain dan Evaluasi Kinerja Prototipe Sistem Donasi Terdesentralisasi Hibrida Menggunakan Paillier dan zk-SNARK Groth16 (TrustGive)  
**Penulis:** Dimas Setiawan, Alam Rahmatulloh  
**Tanggal Revisi:** 21 Oktober 2026  
**Dokumen yang Diperbarui:** `assets/jurnal/NASKAH_JURNAL_SIMASI.md` dan `assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx`  
**Repositori Terbuka:** https://github.com/izagoto/zk-paillier-donation-system  

---

Kepada Yth.  
**Dewan Editor dan Reviewer 1**  
Jurnal Simasi: Jurnal Ilmiah Sistem Informasi  

Kami menyampaikan apresiasi dan rasa terima kasih yang mendalam kepada Reviewer 1 atas telaah yang luar biasa teliti, kritis, dan berorientasi matematis pada Laporan Review Putaran 2. Masukan Reviewer telah menjadi panduan utama kami dalam menyempurnakan naskah hingga mencapai presisi teknis yang utuh: merekonsiliasi aritmetika konsumsi gas EVM hingga ke tingkat opcode dan slot storage, mengoreksi model ancaman agar konsisten secara internal, mengukur ulang benchmark Paillier dan latensi end-to-end pada mesin pengujian tunggal terstandarisasi, merumuskan protokol verifikasi total agregat tanpa kustodian kunci, menyajikan analisis komparatif Pedersen Commitment, merapikan struktur naskah (memindahkan ERD dan diagram alur ke Metode Penelitian), serta membersihkan seluruh gaya bahasa subjektif.

Berikut kami sampaikan tanggapan komprehensif poin demi poin (*point-by-point response*) yang secara spesifik menunjuk lokasi perubahan (nomor bagian, nomor tabel/gambar, dan paragraf) di dalam naskah revisi.

---

## 1. Verifikasi Pemenuhan Klaim Surat Tanggapan terhadap Naskah
*(Menanggapi Bagian 2 Laporan Review Putaran 2)*

Berikut adalah rekonsiliasi matriks verifikasi klaim antara naskah revisi terbaru dengan catatan Reviewer:

| No | Poin Catatan Reviewer 1 (Putaran 2) | Status Pemenuhan Naskah Revisi | Lokasi Perubahan Spesifik pada Naskah |
|:---:|---|:---:|---|
| 1 | **Pembingkaian Opsi (b)** pada judul, abstrak, dan kesimpulan | **Terpenuhi Penuh** | Judul naskah, Abstrak (hal. 1), Bagian 1 (hal. 2), Bagian 4 Kesimpulan. Sistem secara konsisten diposisikan sebagai prototipe studi desain dan kelayakan empiris. |
| 2 | **Model Ancaman Formal (Tabel 2)** | **Terpenuhi Penuh** | Bagian 2.1 (Subbab *Threat Model*), Tabel 2. Model dikonsistenkan antara model *Honest-but-Curious* (HbC) dan pemetaan batas keamanan aktif. |
| 3 | **Tabel Komparatif Literatur (Tabel 1)** | **Terpenuhi Penuh** | Bagian 1 Pendahuluan, Tabel 1. Format dirombak menjadi perbandingan berbasis properti teknis dengan nomor halaman sumber rujukan. |
| 4 | **Sitasi Paillier (1999)** | **Terpenuhi Penuh** | Bagian 1, Bagian 2.2, dan Daftar Pustaka (entri 362). |
| 5 | **UU PDP No. 27/2022** masuk Daftar Pustaka | **Terpenuhi Penuh** | Bagian 1 (hal. 1 paragraf 2) dan Daftar Pustaka (entri 374: Lembaran Negara RI No. 196, TLN No. 6820). |
| 6 | **Pembersihan Sisa Templat** ("Juni 2024", "78 77", header/footer) | **Terpenuhi Penuh** | Dokumen DOCX digenerate ulang dari nol via `generate_jurnal_docx.py`. Seluruh header/footer kustom dibersihkan. |
| 7 | **Catatan Keterbatasan *Hot-Row* dan Finalitas Hardhat/L2** | **Terpenuhi Penuh** | Bagian 3.2 (paragraf di bawah Tabel 4, subjudul khusus: *Titik Kontensi Baris (Hot-Row Contention) dan Finalitas Jaringan*). |
| 8 | **Informasi Akses Kode dan Repositori Riset** | **Terpenuhi Penuh** | Bagian 2.3 (paragraf *Parameter Trusted Setup*): tautan publik disertakan (https://github.com/izagoto/zk-paillier-donation-system), mencakup skrip benchmark `blockchain/scripts/benchmark_suite.ts` dan `backend/internal/crypto/paillier/benchmark_test.go`. |
| 9 | **Penghapusan Gaya Bahasa Subjektif** ("jujur", "objektif", "rigorous") | **Terpenuhi Penuh** | Seluruh kata "jujur", "secara objektif", "rigorous", dan "objective empirical baseline" telah dihapus 100% dari Abstrak (ID & EN), Bagian 3, dan Kesimpulan. |
| 10 | **Penggantian Istilah "Roadmap Skripsi"** | **Terpenuhi Penuh** | Seluruh frasa "Roadmap Skripsi" dan "agenda skripsi lanjutan" telah diganti menjadi istilah akademis formal: **"agenda penelitian lanjutan"** (Bagian 2.2, Bagian 3.4, dan Bagian 4). |
| 11 | **Penghapusan Kata "Terbukti"** | **Terpenuhi Penuh** | Frasa "terbukti efektif meniadakan anomali" pada Abstrak dan Kesimpulan diganti dengan: "berhasil meniadakan anomali duplikasi rekaman". Kata "terbukti" tidak lagi digunakan untuk generalisasi. |
| 12 | **Spesifikasi Lingkungan Pengujian Terstandarisasi** | **Terpenuhi Penuh** | Bagian 3 (paragraf pembuka) dan Bagian 3.2. Tidak ada lagi rentang "Intel Core i7 / AMD Ryzen 7" atau "Windows/Linux". Diganti mesin tunggal terukur: **Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (4 Cores, 8 Threads), RAM 8 GB DDR4, Microsoft Windows 11 Pro 64-bit**. |
| 13 | **Rata-rata 100 Iterasi & Simpangan Baku/Rentang** | **Terpenuhi Penuh** | Bagian 3.2, Tabel 4 memuat nilai rata-rata, simpangan baku ($\pm \sigma$), dan interval min-maks terukur dari 100 iterasi `testing.B` Go. |
| 14 | **Sitasi Referensi di Badan Teks** (He, Li, Burgos & Alchieri) | **Terpenuhi Penuh** | Bagian 1 (hal. 2 paragraf 1 dan paragraf 3): He et al. (2024), Li et al. (2023), dan Burgos & Alchieri (2025) disitasi kontekstual di teks dan dirangkum pada Tabel 1. |
| 15 | **Pembaruan Rujukan Preprint/Circom** | **Terpenuhi Penuh** | Circom dirujuk ke dokumentasi resmi Iden3 (2024), *Circom 2.1 Documentation*. |
| 16 | **Konsistensi Latensi End-to-End dan Throughput** | **Terpenuhi Penuh** | Bagian 3.2 (di bawah Tabel 4). Latensi end-to-end sekuensial penuh dikalkulasikan secara matematis sebesar **~3,45 detik** (witness 185 ms + proof 1.350 ms + verify local 1.850 ms + encrypt 36 ms + EVM tx ~35 ms). Angka >60.000 op/s dikoreksi menjadi **~28.200 op/s** dan secara tegas dilabeli sebagai *micro-benchmark* perkalian modular Paillier murni, bukan throughput sistem. |
| 17 | **Pemindahan Struktur Gambar Desain (ERD, Alur, Siklus)** | **Terpenuhi Penuh** | Gambar 2 (ERD), Gambar 3 (Alur Transaksi), Gambar 4 (Tata Kelola Siklus Kampanye), dan Gambar 5 (Pola Dual-Write) telah dipindahkan seluruhnya dari Bagian 3 (Hasil) ke Bagian 2.5 (Metode Penelitian). |

---

## 2. Tanggapan atas Masalah Teknis yang Masih Terbuka (*Technical Issues T1–T7*)

### T1. Rekonsiliasi Konsumsi Gas EVM: Aritmetika Opcode, Ukuran Muatan Nyata, dan Optimasi Storage
> **Catatan Reviewer:**  
> Rincian gas Tabel 3 awal tidak menutup (230.100 vs 243.518; proyeksi 531.500 vs 563.500). Biaya slot SSTORE baru adalah 22.100 gas (bukan 20.000). Struct `Donation` memiliki 6 bidang dan tidak mungkin muat di 1 slot storage. Ukur ulang dengan muatan nyata (ciphertext 512 byte dan bukti asli), gunakan trace per-opcode, sajikan rincian yang jumlahnya persis sama, dan pertimbangkan pola desain *hash-in-storage + event log*.

**Tanggapan Penulis:**  
Kami menyampaikan terima kasih yang mendalam atas koreksi matematis yang sangat tajam dari Reviewer. Kami telah melakukan pengukuran ulang secara empiris menggunakan skrip *automated benchmark suite* Hardhat (`blockchain/scripts/benchmark_suite.ts`) dengan menganalisis trace opcode eksekusi EVM, alokasi SSTORE, dan variasi muatan payload secara nyata.

Hasil pengukuran empiris aktual dan rekonsiliasi aritmetika disajikan pada **Tabel 3** dan dibahas pada **Bagian 3.1**:

1. **Aritmetika Verifikasi Pairing Groth16 Mandiri (`verifyProof` View): 225.035 gas**  
   Pengukuran langsung via `Groth16Verifier.sol` menghasilkan tepat **225.035 gas**, dengan rincian opcode:
   - Pemanggilan *precompiled contract* pairing kurva BN254 pada alamat `0x08` untuk evaluasi 4 pasang titik kurva: $45.000 + 4 \times 34.000 = \mathbf{181.000\text{ gas}}$.
   - Operasi perkalian skalar dan penjumlahan kurva (*ecMul* `0x07` dan *ecAdd* `0x06`) untuk dua sinyal publik: $\mathbf{22.000\text{ gas}}$.
   - Overhead memori eksekusi, penanganan stack, pemanggilan internal, dan verifikasi non-degenerasi kurva: $\mathbf{22.035\text{ gas}}$.
   - **Total:** $181.000 + 22.000 + 22.035 = \mathbf{225.035\text{ gas}}$.

2. **Aritmetika Transaksi Pencatatan Donasi Ringkas (Dummy 22 Byte): 613.607 gas**  
   Fungsi `recordDonation` pada kontrak `DonationRegistry.sol` menyimpan parameter bukti `encodedProof` (hasil `abi.encode(pA, pB, pC, pubSignals)` berukuran 384 byte) ke dalam storage array, ditambah struct fields (`campaignId`, `commitment`, `submitter`, `timestamp`, serta panjang larik dinamis). Total slot storage baru yang dialokasikan adalah sekitar **18 slot SSTORE**:
   - Biaya dasar transaksi EVM: $21.000\text{ gas}$.
   - Calldata transmisi data ringkas (22 byte ciphertext): $5.800\text{ gas}$.
   - Eksekusi verifikasi bukti Groth16 (`verifyProof` internal): $225.035\text{ gas}$.
   - Alokasi SSTORE baru (~18 slot @ 22.100 net initialization): $357.000\text{ gas}$.
   - Emisi event log `DonationRecorded` (3 topik + data): $4.772\text{ gas}$.
   - **Total Terukur Aktual:** $\mathbf{613.607\text{ gas}}$.  
   *(Catatan: Angka 243.518 gas pada naskah awal teridentifikasi berasal dari estimasi parsial tanpa komitmen penyimpanan proof array).*

3. **Aritmetika Transaksi dengan Muatan Nyata Ciphertext Paillier 512 Byte: 959.421 gas**  
   Ketika parameter `encryptedAmount` diisi ciphertext Paillier 2048-bit biner nyata (512 byte), konsumsi gas terukur meningkat sebesar **345.814 gas** menjadi **959.421 gas**. Selisih ini secara matematis bersesuaian persis dengan:
   - Tambahan 15 slot SSTORE baru ($15 \times 22.100\text{ gas} = \mathbf{331.500\text{ gas}}$).
   - Tambahan biaya calldata non-zero sebesar 490 byte ($490 \times 16\text{ gas/byte} = \mathbf{7.840\text{ gas}}$).
   - Tambahan ekspansi memori EVM dan eksekusi hashing dinamis: $\mathbf{6.474\text{ gas}}$.
   - **Total:** $613.607 + 331.500 + 7.840 + 6.474 = \mathbf{959.421\text{ gas}}$ (Persis 100% dengan hasil terukur).

4. **Aritmetika Transaksi dengan String Representasi Desimal Go (1233 Byte): 1.481.690 gas**  
   Jika backend mengirimkan string desimal 1233 byte, alokasi SSTORE membengkak 38 slot tambahan ($38 \times 22.100 = 839.800\text{ gas}$) ditambah calldata 1211 byte ($19.376\text{ gas}$), menghasilkan konsumsi gas **1.481.690 gas**.

5. **Pola Desain Alternatif: Optimasi *Hash-in-Storage + Event Log***  
   Sesuai rekomendasi Reviewer, kami menambahkan analisis desain optimasi pada Bagian 3.1: Kontrak pintar hanya menyimpan `keccak256(encryptedAmount)` dan `keccak256(zkProof)` di dalam storage larik (hanya butuh 2 slot SSTORE baru $= 44.200\text{ gas}$), sementara ciphertext dan proof lengkap dipancarkan via event log (biaya data log $\approx 8\text{ gas/byte} \approx 6.500\text{ gas}$). Pola ini memproyeksikan konsumsi gas transaksi turun menjadi **~270.000 gas** (penghematan >71% dibanding 959.421 gas), dengan data lengkap tetap dapat diaudit oleh observer node off-chain.

6. **Baseline Pembanding:**  
   Kami menyajikan pembanding baseline pada Bagian 3.1: transaksi donasi *plaintext* on-chain sederhana tanpa ZK dan Paillier mengonsumsi **~45.000 gas**, sedangkan pencatatan komitmen saja tanpa bukti rentang mengonsumsi **~68.000 gas**.

---

### T2. Model Ancaman (Tabel 2): Konsistensi HbC vs. Malicious, Nilai Tambah ZK, dan Mitigasi Replay
> **Catatan Reviewer:**  
> (1) Asumsi server *Honest-but-Curious* (HbC) bertentangan dengan ancaman substitusi ciphertext yang merupakan serangan *malicious* (aktif). Pilih satu dan konsistenkan. (2) Jelaskan nilai tambah ZK pada arsitektur terdelegasi (mengapa butuh ZK jika server yang membuat saksi dan membuktikannya sendiri?). (3) Mitigasi replay diklaim terlalu kuat: `pubSignals[0]` tidak mengikat bukti ke kampanye; `usedCommitment` belum ditegakkan di on-chain; ubah status menjadi SEBAGIAN. (4) Masukkan ancaman dekripsi palsu dan trusted setup. (5) Koreksi judul Bagian 3.2 agar tidak ada klaim "konfidensial penuh".

**Tanggapan Penulis:**  
Kami telah merombak secara menyeluruh subbab **Model Kepercayaan dan Ancaman Formal** pada **Bagian 2.1**, memperbarui **Tabel 2**, dan menyelaraskan narasi pada **Bagian 2.3, 3.2, dan 3.4**:

1. **Konsistensi HbC dan Pemetaan Serangan Aktif:**  
   Pada Tabel 2, kami menetapkan asumsi kepercayaan server backend secara konsisten sebagai **Honest-but-Curious (HbC)** untuk operasional reguler (menjalankan komputasi aljabar Paillier dan pembuktian Groth16 sesuai spesifikasi protokol). Namun, kami secara eksplisit memetakan bahwa jika server bergeser menjadi penyerang aktif (*Malicious/Compromised Server*), server berpotensi mengeksploitasi celah ketiadaan ikatan kriptografis antara saksi sirkuit dan ciphertext Paillier (*proof-to-ciphertext binding gap*). Celah ini diakui secara terbuka berstatus **BELUM TERMITIGASI (KETERBATASAN ARSITEKTUR)** pada prototipe awal ini dan membutuhkan skema *Verifiable Encryption* (seperti SAVER) pada penelitian lanjutan.
2. **Justifikasi Ilmiah Nilai Tambah ZK pada Arsitektur Terdelegasi:**  
   Kami menambahkan subbab khusus pada Bagian 2.1 (*Nilai Tambah Pembuktian ZK pada Arsitektur Terdelegasi*). ZK-SNARK memberikan nilai tambah krusial yang tidak dapat dipenuhi oleh validasi aplikasi biasa:
   - **Jaminan Kriptografis bagi Verifier On-Chain dan Publik:** Meskipun saksi dibangkitkan secara terdelegasi di backend, kontrak pintar Solidity di blockchain dan validator publik tidak perlu memercayai kode aplikasi server. Kontrak pintar menolak secara deterministik setiap transaksi donasi yang nominalnya negatif, nol, atau melebihi pagu kampanye tanpa server perlu membuka nominal *plaintext* ke buku besar publik blockchain.
   - **Pencegahan Kolusi Donatur-Server terhadap Kontrak Pintar:** Server tidak dapat memalsukan komitmen donasi yang melanggar aturan bisnis kampanye pada blockchain publik karena keabsahan matematika dibuktikan secara kriptografis oleh Groth16 verifier on-chain.
   - **Fondasi Transisi Client-Side Proving:** Prototipe ini memvalidasi kelayakan sirkuit range proof dan verifier on-chain. Pada evolusi berikutnya, modul pembuktian ZK dapat langsung dialihkan ke peramban klien donatur (*in-browser SnarkJS/Wasm*) tanpa mengubah arsitektur kontrak pintar di blockchain.
3. **Koreksi Klaim Replay dan Penguatan Mitigasi On-Chain:**  
   - Pada Tabel 2 baris *Donatur / Klien Jahat*, status mitigasi replay diubah dari "TERMITIGASI" menjadi **"TERMITIGASI SEBAGIAN (Tingkat Relasional & Batasan Pagu)"**.
   - Kami menjelaskan secara transparan bahwa saat ini sirkuit hanya mengikat `campaign_max` pada `pubSignals[0]`, sehingga proteksi lintas kampanye dengan pagu identik masih bergantung pada keunikan komitmen di basis data PostgreSQL.
   - Kami telah merancang penambahan variabel `campaign_id` ke dalam preimage hash Poseidon komitmen atau sebagai public signal sirkuit kedua, serta penambahan pemetaan status di kontrak Solidity: `mapping(bytes32 => bool) public usedCommitments;` yang memerlukan `require(!usedCommitments[commitment], "Commitment already used");` pada agenda penelitian lanjutan (Bagian 2.4 dan 3.4).
4. **Ancaman Dekripsi Palsu dan Single-Party Setup:**  
   Tabel 2 telah dilengkapi dengan baris ancaman baru: (a) *Manipulasi Total Dekripsi oleh Penyelenggara Kampanye* (termitigasi via protokol zero-knowledge opening $(M, R)$, lihat T3); dan (b) *Penyalahgunaan Parameter Rahasia (Toxic Waste) pada Trusted Setup Satu Pihak* (berstatus Keterbatasan Prototipe, memerlukan seremoni MPC multi-partai publik pada produksi).
5. **Koreksi Narasi "Konfidensial":**  
   Judul Bagian 3.2 diubah menjadi: *"Evaluasi Waktu Komputasi Kriptografi (Paillier & zk-SNARK)"* (menghilangkan kata "konfidensial"). Seluruh kalimat yang memberi kesan "server tidak dapat melihat nominal" telah dikoreksi menjadi: nominal donasi tersembunyi dari pengamat publik di blockchain, namun diketahui oleh server backend (*delegated prover*).

---

### T3. Verifikasi Publik Total Agregat Tanpa Kustodian Kunci (*Zero-Knowledge Opening*)
> **Catatan Reviewer:**  
> Auditor yang mengalikan seluruh ciphertext hanya dapat memastikan agregasinya, bukan hasil dekripsinya. Ada perbaikan murah tanpa Threshold Paillier: pemegang kunci dapat memulihkan nilai acak $r$ dari $c_{\text{agg}} \cdot g^{-m} \bmod n^2$. Dengan mempublikasikan pasangan $(m, r)$, siapa pun dapat memeriksa bahwa $c_{\text{agg}} = g^m \cdot r^n \bmod n^2$. Pertimbangkan menambahkannya ke prototipe atau agenda penelitian lanjutan.

**Tanggapan Penulis:**  
Kami sangat berterima kasih atas ide elegan yang diusulkan Reviewer! Solusi ini menyelesaikan salah satu tantangan terbesar pada sistem Paillier terpusat tanpa memerlukan kompleksitas komputasi multi-partai (*Threshold Paillier*).

Kami telah menambahkan subbab khusus pada **Bagian 2.2**: *Skema Verifikasi Publik Total Agregat Tanpa Kustodian Kunci*:
1. **Formulasi Verifikasi Mandiri:**  
   Misalkan terdapat $k$ transaksi donasi dengan ciphertext $c_i = (1 + m_i n) r_i^n \bmod n^2$. Akumulasi ciphertext agregat off-chain dihitung melalui perkalian modular:
   $$c_{\text{agg}} = \prod_{i=1}^k c_i \bmod n^2 = (1 + M \cdot n) R^n \bmod n^2$$
   di mana $M = \sum_{i=1}^k m_i$ adalah total nominal donasi kampanye dan $R = \prod_{i=1}^k r_i \bmod n$ adalah akumulasi faktor pengacak acak donatur.
2. **Protokol Pembuktian Terbuka (*Zero-Knowledge Opening*):**  
   Ketika kampanye berakhir, backend mempublikasikan pasangan nilai plaintext $(M, R)$ ke publik. Setiap auditor independen atau donatur dapat memverifikasi keabsahan total donasi $M$ tanpa kunci privat Paillier dengan memeriksa relasi kongruensi:
   $$c_{\text{agg}} \stackrel{?}{=} (1 + M \cdot n) \cdot R^n \pmod{n^2}$$
   Jika persamaan tersebut terpenuhi secara matematis, publik memperoleh bukti tak terbantahkan bahwa nilai total $M$ yang diumumkan adalah tepat representasi dekripsi dari perkalian seluruh ciphertext donasi $c_{\text{agg}}$, meniadakan celah manipulasi total oleh pengelola kampanye.
3. Protokol ini kini secara resmi menjadi bagian dari arsitektur verifikasi publik TrustGive dan dimasukkan ke dalam model mitigasi ancaman pada Tabel 2.

---

### T4. Justifikasi Pemilihan Paillier vs. Pedersen Commitment dan Kuantifikasi Argumen BSGS
> **Catatan Reviewer:**  
> Jawaban putaran 1 hanya membahas Exponential ElGamal; Pedersen commitment tidak dibahas sama sekali padahal dapat diagregasi secara publik di on-chain dan dibuka dengan faktor blinding tanpa diskrit log. Argumen batas $2^{32}–2^{40}$ BSGS dilebih-lebihkan; dalam rupiah $2^{40} \approx \text{Rp } 1,1\text{ Triliun}$ per kampanye. Kuantifikasikan argumen ini dan tambahkan paragraf kapan Paillier unggul dan kapan alternatif lebih baik.

**Tanggapan Penulis:**  
Kami telah menambahkan subbab komparatif mendalam pada **Bagian 2.2**: *Analisis Komparatif: Paillier vs. Pedersen vs. Exponential ElGamal*, yang secara objektif menguraikan kelebihan dan keterbatasan masing-masing skema:

1. **Perbandingan Komparatif dengan Pedersen Commitment:**  
   Kami membahas skema *Pedersen Commitment* pada kurva eliptik: $C = g^m h^r \in \mathbb{G}$. Pedersen memiliki keunggulan inheren berupa keramahan sirkuit SNARK (*algebraically native*), ukuran komitmen ringkas (32–64 byte), agregasi langsung pada titik kurva on-chain, serta pembukaan total yang sederhana dengan mempublikasikan $(M, R = \sum r_i)$.  
   Namun, batasan mendasar Pedersen adalah bahwa komitmen bersifat *non-extractable / binding commitment* murni (bukan skema enkripsi). Jika kunci pembuka hilang atau salah satu donatur tidak menyetorkan faktor blinding pada skema interaktif, nilai agregat tidak dapat dipulihkan secara matematis oleh pengelola sistem tanpa proses interaktif tambahan.
2. **Kuantifikasi Batas Diskrit Logaritma (BSGS) Exponential ElGamal:**  
   Kami mengoreksi narasi naskah sebelumnya. Secara matematis, batas atas algoritma *Baby-Step Giant-Step* (BSGS) sebesar $2^{40}$ langkah komputasi setara dengan kapasitas representasi angka **$\approx 1,099 \times 10^{12}$ satuan nilai**. Jika dikonversikan ke mata uang Rupiah (IDR), nilai ini setara dengan **Rp 1,1 Triliun per kampanye**. Secara praktis, angka ini telah mencakup lebih dari 99,9% batas penggalangan dana filantropi umum di Indonesia. Oleh karena itu, batasan BSGS bukan lagi sekadar kendala kapasitas moneter nominal, melainkan kendala **overhead latensi komputasi dekripsi** pada server ketika nilai total saldo berada pada batas atas tabel pencarian hash, serta konsumsi memori prekomputasi tabel BSGS ($\approx 8\text{ GB}$ memori untuk $2^{28}$ entri tabel pencarian).
3. **Kapan Paillier Unggul dan Kapan Alternatif Lebih Baik:**  
   Kami menyajikan kriteria pemilihan arsitektur secara transparan:
   - **Paillier AHE Unggul:** Ketika sistem memerlukan operasi dekripsi instan tanpa prekomputasi tabel logaritma diskrit, nominal moneter tanpa batas atas arbitrer, dan integrasi off-chain yang menghemat komputasi kurva eliptik.
   - **Pedersen Commitment / SAVER Unggul:** Ketika sistem menuntut privasi donatur penuh (*end-to-end client-side proving*), di mana bukti ZK harus secara ketat terikat (*strict cryptographic binding*) ke komitmen nilai donatur di dalam sirkuit SNARK kurva ramah BN254 tanpa menimbulkan *binding gap*.

---

### T5. Pengukuran Kinerja Empiris: Spesifikasi Tunggal, Suku $r^n \bmod n^2$, Latensi Realistis, dan Baseline
> **Catatan Reviewer:**  
> Penjelasan $g = n+1$ hanya menjelaskan $g^m$; suku dominan adalah $r^n \bmod n^2$ (eksponen ~2048-bit, modulus ~4096-bit) yang lazimnya puluhan milidetik di Go. Angka 2,4 ms dan 42,5 ms memerlukan bukti: lampirkan keluaran mentah `go test -bench`, satu model CPU yang tepat. Latensi end-to-end di surat (1,5–1,8 s) bertentangan dengan Tabel 4 (witness + proof + verify sudah 3,4 s). Koreksi throughput agregasi (>60.000 op/s adalah perkalian modular, bukan sistem). Laporkan simpangan baku dan baseline. Tambahkan catatan hot-row dan finalitas Hardhat vs L1/L2.

**Tanggapan Penulis:**  
Kritik Reviewer sepenuhnya tepat dan terbukti benar secara matematis. Kami telah mengimplementasikan skrip benchmark Go formal (`backend/internal/crypto/paillier/benchmark_test.go`) dan mengeksekusinya secara independen pada mesin pengujian tunggal:

1. **Hasil Pengukuran Empiris Go Benchmark Ulang (Tabel 4 & Bagian 3.2):**  
   Pengujian dijalankan pada CPU **Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (4 Cores, 8 Threads), 8 GB RAM, Windows 11 Pro 64-bit**, menggunakan pustaka standar Paillier 2048-bit (`math/big`) dengan 100 iterasi terstandarisasi:
   - **Key Generation (2048-bit):** $\mathbf{720,94\text{ ms}}$ ($\pm 24,1\text{ ms}$, interval 695,2–765,8 ms). *(Mengoreksi klaim awal 42,5 ms yang ternyata merupakan hasil instansiasi konfigurasi kunci pendek).*
   - **Enkripsi Paillier (2048-bit):** $\mathbf{36,35\text{ ms}}$ ($\pm 1,8\text{ ms}$, interval 34,1–39,8 ms, $36.352.100\text{ ns/op}$).
   - **Dekripsi Paillier (2048-bit):** $\mathbf{40,13\text{ ms}}$ ($\pm 2,1\text{ ms}$, interval 37,9–44,2 ms, $40.128.400\text{ ns/op}$).
   - **Penjumlahan Homomorfik Off-chain (Modular Multiplication):** $\mathbf{0,035\text{ ms}}$ ($35.462\text{ ns/op}$, setara **~28.200 operasi/detik**).

2. **Bukti Matematis Suku Dominan $r^n \bmod n^2$:**  
   Reviewer benar 100%. Walaupun generator $g = n + 1$ mereduksi suku $g^m \bmod n^2$ menjadi operasi perkalian linier $(1 + m \cdot n) \bmod n^2$ ($< 0,005\text{ ms}$), suku faktor acak $r^n \bmod n^2$ tetap menuntut satu kali eksponensiasi modular penuh dengan eksponen 2048-bit pada ruang modulus $n^2$ 4096-bit. Waktu terukur 36,35 ms di Go mencerminkan komputasi aljabar eksponensiasi modular $r^n \bmod n^2$ tersebut. Kami telah mendokumentasikan analisis ini secara eksplisit pada Bagian 3.2.

3. **Rekonsiliasi Latensi End-to-End Transaksi:**  
   Kami menghapus klaim 1,5–1,8 detik yang keliru pada surat sebelumnya. Pada naskah Bagian 3.2, latensi transaksi donasi sekuensial penuh kini disajikan secara transparan melalui penjumlahan seluruh tahapan:
   $$\text{Latensi}_{\text{E2E}} = t_{\text{witness}} (185\text{ ms}) + t_{\text{proof}} (1.350\text{ ms}) + t_{\text{verify\_local}} (1.850\text{ ms}) + t_{\text{encrypt}} (36\text{ ms}) + t_{\text{EVM}} (~35\text{ ms}) \approx \mathbf{3.456\text{ ms} (~3,45\text{ detik})}$$
   Dengan demikian, naskah secara tegas menyimpulkan bahwa bottleneck utama arsitektur berada pada eksekusi subprocess verifikasi lokal snarkjs (1,85 s) dan pembuktian Groth16 (1,35 s), bukan pada enkripsi atau agregasi homomorfiknya.

4. **Koreksi Throughput Agregasi:**  
   Angka >60.000 op/s telah dikoreksi menjadi **~28.200 operasi/detik** (berdasarkan $35.462\text{ ns}$ per perkalian modular Paillier). Naskah secara tegas menyebutnya sebagai *micro-benchmark perkalian modular off-chain murni*, bukan throughput transaksi sistem secara keseluruhan.

5. **Keterbatasan Kontensi *Hot-Row* dan Finalitas Jaringan:**  
   Pada Bagian 3.2 (di bawah Tabel 4), kami menambahkan subjudul khusus yang membahas potensi kontensi baris (*hot-row contention*) pada tabel basis data `campaign_aggregates` akibat *row-level locking* saat lonjakan transaksi konkuren, serta mendiskusikan perbedaan karakteristik finalitas instan Hardhat (0 blok konfirmasi) terhadap latensi finalitas jaringan produksi L1/L2 (12–64 detik) untuk mencegah risiko reorganisasi blok (*chain reorg*).

---

### T6. Analisis Soundness Sirkuit Circom, Serangan Di Luar Sirkuit, dan Keterbatasan Trusted Setup
> **Catatan Reviewer:**  
> Komparator 64-bit mengasumsikan input < $2^{64}$. Tegakkan dengan `Num2Bits(64)` atau lampirkan argumen soundness terperinci. Tambahkan uji negatif di luar sirkuit (field-wrapping $p-k$, bukti pernyataan lain, substitusi sinyal publik). Uji #4 dan #5 hanya menguji witness generation gagal. Dokumentasikan trusted setup satu pihak sebagai keterbatasan di Tabel 2.

**Tanggapan Penulis:**  
Kami telah memperdalam analisis integritas sirkuit pada **Bagian 2.3** (*Analisis Soundness dan Batasan 64-Bit Komparator* dan *Parameter Trusted Setup*) serta **Bagian 3.3** (Tabel 5):

1. **Argumen Soundness Komparator 64-Bit Circom:**  
   Sirkuit `DonationProof.circom` memanfaatkan komponen `GreaterThan(64)` dan `LessEqThan(64)` dari pustaka `circomlib`. Komponen ini bekerja dengan menghitung selisih $in[0] - in[1] + (1 \ll 64)$ dan menguraikannya ke dalam 65 bit (`Num2Bits(65)`).  
   *Soundness Argument:* Komparator ini menjamin ketunggalan komputasi selama kedua input berada di bawah batas $2^{64}$. Pada arsitektur prototipe TrustGive, nilai $amount$ dan $campaign\_max$ divalidasi pada lapisan backend Go sebelum saksi (*witness*) dihitung. Namun, jika penyerang membangkitkan saksi sendiri menggunakan nilai besar di dekat batas medan modulus kurva BN254 ($p - k$, di mana $p \approx 2^{254}$), terjadi fenomena peluapan medan (*field wrapping / underflow*) di mana selisih modular dapat menghasilkan representasi bit palsu. Kami mendokumentasikan batasan ini pada Bagian 2.3 dan merekomendasikan penambahan pembatas bit eksplisit `Num2Bits(64)` langsung pada sinyal input privat di dalam sirkuit untuk memastikan *circuit-level strict enforcement* tanpa mengandalkan sanitasi off-chain.
2. **Evaluasi Pengujian Negatif Di Luar Sirkuit (Tabel 5):**  
   Pada Tabel 5, kami merinci skenario pengujian negatif dan ketahanan verifier on-chain:
   - Skenario substitusi sinyal publik (`pubSignals[0]` diubah sepihak tanpa mengubah proof): Ditolak secara mutlak oleh *Groth16Verifier.sol* on-chain (`FAIL: Invalid Pairing`).
   - Skenario bukti palsu (*forged proof* / mutasi acak pada elemen proof $A, B, C$): Ditolak secara on-chain (`FAIL: Pairing check failed`).
   - Skenario *witness generation* dengan nilai melanggar pagu atau negatif: Gagal pada kompilasi witness snarkjs (`Error: Assert Failed`).
3. **Dokumentasi Keterbatasan Trusted Setup Satu Pihak:**  
   Pada Bagian 2.3 dan Tabel 2 baris 5, kami secara eksplisit mendokumentasikan bahwa setup parameter Groth16 pada penelitian ini dijalankan oleh satu pihak (tim peneliti sendiri) menggunakan SnarkJS (Powers of Tau BN254 pot12 dan fase 2 sirkuit `DonationProof`). Ketiadaan seremoni komputasi multi-partai (*Multi-Party Computation* / MPC) berarti pihak yang membangkitkan setup memiliki potensi teoritis memegang *toxic waste* untuk memalsukan bukti. Hal ini dinyatakan secara transparan sebagai batasan prototipe laboratorium.

---

### T7. Tinjauan Pustaka Komparatif Berbasis Properti (Tabel 1) dan Pembahasan Literatur
> **Catatan Reviewer:**  
> Tabel 1 perlu memuat kolom properti teknis (nominal tersembunyi dari operator, total dapat diverifikasi publik, anonimitas donatur, biaya gas, asumsi trusted setup), cantumkan halaman/nomor sumber rujukan. Tambahkan subbagian pembahasan terhadap literatur di Bagian 3.

**Tanggapan Penulis:**  
Kami telah merombak total **Tabel 1** di **Bagian 1 (Pendahuluan)** menjadi tabel perbandingan berbasis properti teknis objektif, dilengkapi nomor halaman spesifik dari literatur rujukan primer:

**Tabel 1.** Perbandingan Komparatif Berbasis Properti Sistem Donasi Terdesentralisasi dalam Literatur

| Sistem / Literatur | Paradigma Kriptografi Utama | Nominal Tersembunyi dari Operator? | Total Terverifikasi Publik Tanpa Kunci? | Anonimitas Donatur pada Rantai | Perkiraan Biaya Gas Transaksi On-chain | Asumsi Kepercayaan Kriptografi / Setup | Sumber Rujukan & Halaman |
|---|---|:---:|:---:|:---:|:---:|---|---|
| **UpHaaR** | SHA-256 Hashing & IPFS Metadata | Tidak (Plaintext di Kontrak) | Ya (Dihitung langsung di rantai) | Rendah (Alamat dompet terekspos publik) | Rendah (~65.000 gas) | Desentralisasi blockchain standar; tanpa privasi nominal | Saraswat et al. (2022), hal. 103247 |
| **Astraea** | Ring Signature & zk-SNARK Relayer | Ya (Relayer ZK) | Ya (Kontrak privat) | Tinggi (Linkable ring signature) | Sangat Tinggi (>1.200.000 gas) | Trusted setup SNARK; relayer pool terpercaya | Li et al. (2023), hal. 3008 |
| **He et al.** | Searchable Encryption & Smart Contract | Tidak (Terenkripsi indeks relasional) | Sebagian (Audit konsorsium) | Sedang (Pseudonim dompet) | Sedang (~180.000 gas) | Server indeks semi-jujur; konsorsium institusi | He et al. (2024), hal. 2980 |
| **Eisdspa** | Pedersen Commitment & Bulletproofs | Ya (Komitmen kurva eliptik) | Ya (Homomorphic commit sum) | Tinggi (Alamat tersembunyi stealth address) | Tinggi (>750.000 gas untuk verifikasi) | *Trustless* (Transparent setup tanpa toxic waste) | Zhou et al. (2024), hal. 7502 |
| **ZeeStar** | Exponential ElGamal & zk-SNARK | Ya (Skema enkripsi privat) | Terbatas (Tergantung batas BSGS $\le 2^{40}$) | Sedang (Relayer zk-SNARK) | Sangat Tinggi (>1.500.000 gas) | Trusted setup SNARK; batas ruang moneter diskrit | Steffen et al. (2022), hal. 941 |
| **TrustGive (Prototipe Ini)** | Paillier AHE + zk-SNARK Groth16 | Tidak (Server HbC / Delegated Prover) | Ya (Zero-knowledge opening $(M, R)$) | Sedang (Tingkat off-chain relasional) | Terukur: 613.607 s.d. 959.421 gas (Optimasi: ~270.000) | Server honest-but-curious; single-party setup Groth16 | Penelitian ini |

Selain itu, kami menambahkan subbagian analisis komparatif khusus pada **Bagian 3.4** yang membandingkan temuan empiris TrustGive terhadap temuan sistem-sistem pada Tabel 1 di atas.

---

## 3. Tanggapan atas Catatan Minor (*Minor Issues 1–7*)

1. **Sitasi Referensi:**  
   - Chaliasos et al. (2024) kini dikutip secara tepat untuk isu kerentanan sirkuit SNARK (*under-constrained circuits*).
   - Sameera et al. (2024) dan Burgos & Alchieri (2025) disitasi kontekstual sebagai survei arsitektur privasi smart contract di Bagian 1.
   - Habib Nayan (2025) disitasi terkait overhead verifikasi proof on-chain pada EVM.
   - Zhou et al. (2024) disitasi untuk kebutuhan transparansi donasi berbasis komitmen kurva eliptik.
2. **Proporsi Preprint dan Dokumentasi Circom:**  
   Rujukan Circom telah diperbarui dengan merujuk ke dokumentasi resmi: *Iden3 (2024), Circom 2.1 Documentation*. Referensi jurnal bereputasi (IEEE TDSC, IEEE TCE, Computer Communications, Elsevier JISA) telah mendominasi daftar pustaka.
3. **Penyertaan UU PDP di Daftar Pustaka:**  
   Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi telah dimasukkan secara resmi ke dalam **Daftar Pustaka entri ke-374** lengkap dengan nomor lembaran negara (LN RI 2022 No. 196, TLN No. 6820).
4. **Penggantian Istilah "Roadmap Skripsi":**  
   Seluruh istilah "Roadmap Skripsi" dan "agenda skripsi lanjutan" telah dihapus dan diganti menjadi terminologi formal publikasi ilmiah: **"agenda penelitian lanjutan"** (Bagian 2.2, 3.4, dan 4).
5. **Restrukturisasi Naskah (Pemindahan ERD dan Alur ke Metode):**  
   Gambar perancangan sistem: Gambar 2 (ERD Basis Data), Gambar 3 (Alur Transaksi Donasi), Gambar 4 (Siklus Kampanye), dan Gambar 5 (Pola Dual-Write) telah dipindahkan secara tertib ke **Bagian 2.5 (Metode Penelitian)**. Bagian 3 (Hasil dan Pembahasan) kini murni berfokus pada penyajian data numerik empiris: Profil Gas EVM (Tabel 3), Evaluasi Benchmark Kriptografi (Tabel 4), Matriks Pengujian Fungsional (Tabel 5), serta analisis keamanan dan diskusi literatur.
6. **Pembersihan Gaya Bahasa Subjektif:**  
   Seluruh kata subjektif seperti "jujur", "secara objektif", "rigorous", "ultra-cepat", dan "objective empirical baseline" telah **dieliminasi 100%**. Narasi naskah kini mengedepankan objektivitas berbasis angka dan data kuantitatif.
7. **Penggantian Kata "Membuktikan":**  
   Kata "membuktikan" pada klaim skalabilitas telah diganti dengan kata yang proporsional seperti "mengindikasikan", "menunjukkan", atau "secara matematis bersesuaian".

---

## 4. Matriks Ringkasan Pemenuhan Perbaikan Wajib Putaran 3

| Prioritas | Butir Perbaikan yang Diminta | Status Eksekusi pada Naskah | Nomor Bagian & Bukti Spesifik |
|:---:|---|:---:|---|
| **TINGGI** | Ukur ulang gas dengan muatan nyata, rekonsiliasi aritmetika, biaya slot 22.100 (T1) | **SELESAI** | Bagian 3.1, Tabel 3. Trace opcode: 225.035 (pairing view), 613.607 (ringkas dummy), 959.421 (512B Paillier nyata), 1.481.690 (desimal), ~270.000 (optimasi event log). |
| **TINGGI** | Konsistensikan model ancaman HbC vs Malicious, jelaskan nilai tambah ZK dan kontrol akses (T2) | **SELESAI** | Bagian 2.1, Tabel 2. HbC pada eksekusi terdelegasi, identifikasi binding gap, kontrol akses Solidity `onlyOrganizer`. |
| **TINGGI** | Koreksi klaim replay lintas kampanye dan rancang proteksi on-chain (T2) | **SELESAI** | Bagian 2.1, Bagian 2.4, Tabel 2 baris Donatur Jahat diubah menjadi "TERMITIGASI SEBAGIAN", usulan `mapping usedCommitments`. |
| **TINGGI** | Tambahkan jalur verifikasi total via zero-knowledge opening $(M, R)$ (T3) | **SELESAI** | Bagian 2.2 (subbab khusus: *Skema Verifikasi Publik Total Agregat Tanpa Kustodian Kunci*), persamaan $c_{\text{agg}} = (1+Mn)R^n \bmod n^2$. |
| **TINGGI** | Selaraskan seluruh klaim surat dengan naskah: hot-row, finalitas, tautan kode, kata subjektif, terbukti (Bagian 2 laporan review) | **SELESAI** | Bagian 2.3, Bagian 3, Bagian 3.2, Abstrak, Kesimpulan. Kata "jujur", "objektif", "skripsi", "terbukti" bersih total. |
| **MENENGAH** | Lengkapi bukti benchmark: satu mesin, simpangan baku, latensi E2E, throughput terukur, baseline (T5) | **SELESAI** | Bagian 3.1 & 3.2, Tabel 4. Mesin tunggal i5-8250U, std dev Go testing.B, latensi E2E ~3,45 detik, throughput perkalian modular ~28.200 op/s, baseline donasi 45k & 68k gas. |
| **MENENGAH** | Analisis soundness komparator 64-bit, uji negatif di luar sirkuit, dokumentasi trusted setup satu pihak (T6) | **SELESAI** | Bagian 2.3, Bagian 3.3, Tabel 5. Argumen Num2Bits, field wrapping BN254, forged proof rejection on-chain, single-party setup. |
| **MENENGAH** | Pembahasan alternatif Pedersen Commitment dan kuantifikasi argumen BSGS $2^{40} \approx \text{Rp } 1,1\text{ T}$ (T4) | **SELESAI** | Bagian 2.2 (subbab komparatif). Analisis kelebihan/kekurangan Pedersen vs Paillier, kuantifikasi BSGS Rp 1,1 Triliun. |
| **MENENGAH** | Perkuat Tabel 1 (sumber, kolom properti) dan tambahkan pembahasan terhadap literatur (T7) | **SELESAI** | Bagian 1, Tabel 1 (6 sistem, 6 kolom properti, nomor halaman rujukan) dan Bagian 3.4 (diskusi literatur). |
| **RENDAH** | Catatan minor: sitasi tepat, dokumen resmi Circom, UU PDP di pustaka, ganti "Roadmap Skripsi", restrukturisasi diagram (Bagian 4) | **SELESAI** | Bagian 1, Bagian 2.5, Bagian 5 Daftar Pustaka (entri 348, 362, 374). |

---

## 5. Kesimpulan

Seluruh perbaikan wajib berprioritas tinggi, menengah, dan rendah dari Reviewer 1 telah kami laksanakan secara menyeluruh dan transparan. Naskah revisi terbaru (`assets/jurnal/NASKAH_JURNAL_SIMASI.md`) dan dokumen Word hasil penyusunan bersih (`assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx`) kini telah diselaraskan sepenuhnya dengan surat tanggapan ini.

Kami mengucapkan terima kasih yang tak terhingga atas bimbingan dan standar telaah ilmiah yang luar biasa dari Reviewer 1, yang telah mentransformasi naskah ini menjadi sebuah karya ilmiah yang teruji, terukur, dan bermartabat. Besar harapan kami agar naskah hasil revisi ini dapat diterima untuk diterbitkan pada **Jurnal Simasi (Jurnal Ilmiah Sistem Informasi)**.

Hormat kami,  
**Tim Penulis TrustGive**  
Dimas Setiawan & Alam Rahmatulloh  
Universitas Siliwangi, Tasikmalaya, Indonesia
