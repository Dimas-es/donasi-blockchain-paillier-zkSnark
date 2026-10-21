# LAPORAN REVIEW NASKAH
**Jurnal Simasi: Jurnal Ilmiah Sistem Informasi**

**Judul:** Pengembangan dan Evaluasi Kinerja Sistem Donasi Terdesentralisasi dengan Agregasi Homomorfik Paillier dan ZK-SNARK (TrustGive)

**Catatan:** Review ini mencakup teks, tabel, dan referensi naskah. Gambar 1–7 tidak terbaca pada ekstraksi teks, sehingga tidak dinilai.

---

## 1. Ringkasan dan Penilaian Umum

Naskah ini mengusulkan TrustGive, prototipe donasi hibrida. Nominal donasi dienkripsi dengan Paillier dan diagregasi di luar rantai (*off-chain*). Rentang nominal dibuktikan dengan Groth16 (sirkuit Circom) dan diverifikasi di kontrak pintar EVM. Ada pula mekanisme idempotensi dan rekonsiliasi untuk masalah *dual-write*.

**Kekuatan:**
- Penulis terbuka soal keterbatasan (Tabel 3, baris 10–13). Ini jarang dan patut dihargai.
- Rekayasa keandalan (idempotensi, *unique constraint*, *reconciliation worker*) dijelaskan cukup konkret.
- Struktur naskah jelas dan abstrak dwibahasa lengkap.

**Masalah utama:** Properti keamanan yang menjadi alasan sistem ini ada, yaitu privasi nominal dan integritas agregat, justru tidak terpenuhi oleh prototipe. Namun abstrak, judul, dan kesimpulan masih menulis seolah-olah tujuan itu tercapai.

**Rekomendasi: REVISI MAYOR**

| Aspek | Skor (1–5) |
|---|---|
| Orisinalitas / kebaruan | 2 |
| Kontribusi ilmiah | 2 |
| Kebenaran teknis & validitas klaim | 2 |
| Metodologi & rigor evaluasi | 2 |
| Kejelasan penulisan & struktur | 3 |
| Kualitas & relevansi pustaka | 2 |

---

## 2. Kelemahan Mayor

### M1. Model ancaman tidak didefinisikan, dan desain tidak konsisten dengan motivasinya

Bagian "Model Kepercayaan" tidak berisi model ancaman formal: siapa penyerangnya, apa asumsinya, dan properti apa yang dijamin. Akibatnya ada beberapa kontradiksi:

- Server menerima nominal *plaintext*, membangkitkan bukti, memverifikasinya sendiri, lalu mengenkripsi dengan Paillier. Dari sisi server, enkripsi dan bukti ZK tidak menambah perlindungan apa pun. Server bisa memilih *witness* sesuka hati.
- Kunci privat Paillier juga ada di server (Bagian 6c), jadi server mampu mendekripsi semuanya.
- Motivasi naskah adalah *trust deficit* dan manipulasi oleh pengelola platform. Padahal pengelola inilah yang paling diuntungkan oleh *binding gap*. Penulis menyebut celah itu hanya terjadi jika "server dikompromikan", padahal operator itu sendiri adalah penyerang yang relevan.
- Total agregat dihitung di PostgreSQL, didekripsi oleh organizer, dan dipublikasikan tanpa bukti dekripsi yang dapat diverifikasi. Naskah tidak menjelaskan bagaimana auditor bisa memverifikasi total tersebut.

Mohon tambahkan model ancaman eksplisit (tabel penyerang × properti × mitigasi). Setelah itu, nilai ulang klaim "menyelaraskan transparansi dan privasi".

### M2. Klaim dalam abstrak, kesimpulan, dan judul berlebihan dibanding temuan

Kesimpulan menyatakan sistem "terbukti mampu menyelaraskan" transparansi dan privasi. Tabel 3 baris 10 dan 11 justru menunjukkan serangan substitusi *ciphertext* diterima dan nominal terbuka bagi server. Selain itu:

- Kata "terbukti tangguh" disandarkan pada uji 20 permintaan paralel.
- Tidak ada aliran dana nyata (token/escrow/pencairan). Sistem hanya mencatat donasi, sehingga klaim akuntabilitas "alokasi dana" tidak didukung.

Selaraskan klaim dengan bukti. Pilihannya: (a) implementasikan *proof-to-ciphertext binding* lalu evaluasi ulang, atau (b) ubah bingkai naskah menjadi studi desain dan kinerja dengan cakupan terbatas, termasuk judul dan abstrak.

### M3. Angka gas 243.518 sulit direkonsiliasi dan interpretasinya inkonsisten

- Perkiraan kasar: biaya dasar transaksi 21.000, ditambah verifikasi *pairing* Groth16 (~181.000 untuk 4 pasangan, belum termasuk operasi skalar per *public input*), sudah mendekati 205.000. Sisanya kurang dari ±40.000.
- Namun Bagian 4b menyebut kontrak menyimpan `encryptedAmount` (*ciphertext* 4096-bit ≈ 512 byte), `zkProof`, `commitment`, `submitter`, dan `timestamp`. Satu slot baru saja sudah 22.100 gas.
- Jadi sebagian data pasti tidak disimpan di *storage*, atau angkanya perlu diperiksa ulang.
- Tabel 2 juga mengatribusikan 243.518 gas ke "verifikasi bukti on-chain" saja, padahal Tabel 1 menyebutnya mencakup *storage* dan *event*.

Sajikan rincian gas per komponen (basis transaksi, kalldata, verifier, *storage*, *event*) dan jelaskan data apa yang benar-benar disimpan.

### M4. Rigor pengukuran dan beberapa angka kinerja perlu dibuktikan

- Tidak ada jumlah iterasi, *warm-up*, simpangan baku, median/persentil, atau keluaran *benchmark* mentah. Spesifikasi lingkungan juga kabur ("Windows/Linux", "Cancun/Prague", CPU tidak disebut).
- *Keygen* Paillier 2048-bit 42,5 ms dan enkripsi 2,40 ms tampak sangat cepat untuk eksponensiasi modulus 4096-bit. Mohon periksa metode ukur dan pustakanya.
- Metrik yang disorot (0,015 ms agregasi) bukan *bottleneck*. Biaya dominan ada pada pembuktian (1,35 s) dan verifikasi (1,85 s), padahal ini yang membatasi pengalaman pengguna. Latensi *end-to-end* dan *throughput* tidak diukur.
- Pembaruan agregat pada satu baris `campaign_aggregates` berpotensi menjadi titik kontensi (*hot row*) dan tidak dievaluasi.
- Tidak ada *baseline*. Bandingkan setidaknya dengan: donasi *plaintext* on-chain, *commitment*-saja, dan alternatif homomorfik yang ramah-sirkuit.
- Perbandingan dengan Zether (">1,5 juta gas") tidak bersumber dan tidak sepadan. Fitur dan model ancamannya berbeda.
- Hardhat memiliki finalitas instan. Tidak ada diskusi *reorg*, jumlah konfirmasi, atau estimasi biaya pada jaringan publik/L2.

### M5. Pemilihan Paillier tidak dijustifikasi

Paillier dengan modulus 2048-bit tidak ramah sirkuit, dan itulah sebab terjadinya *binding gap* (Opsi A yang diuraikan penulis sendiri). Mengapa tidak menggunakan *Pedersen commitment* atau ElGamal eksponensial (seperti ZeeStar), yang bersifat homomorfik aditif dan dapat diverifikasi langsung di dalam sirkuit atau on-chain? Dengan skema semacam itu, total agregat bahkan bisa diverifikasi publik tanpa kepercayaan pada *server*. Diskusi perbandingan ini wajib ada.

### M6. Celah keamanan sirkuit dan protokol yang belum dibahas

Karena naskah sendiri mengutip Chaliasos et al. (2024), hal-hal berikut perlu dijawab:

- Apakah `amount` dan `campaign_max` dibatasi 64-bit dengan `Num2Bits`? Komparator Circomlib mengasumsikan masukan berada dalam rentang bit. Tanpa itu, sirkuit rentan *under-constrained*.
- Sinyal publik tidak memuat `campaign_id`/*nonce*, sehingga bukti berpotensi digunakan ulang lintas kampanye. Proteksi *replay* on-chain (keunikan *commitment* atau *nullifier*) tidak dijelaskan. Groth16 juga *malleable*.
- *Trusted setup*: siapa yang melaksanakan seremoni, berapa kontributor, dan bagaimana *toxic waste* ditangani? Ini krusial untuk makalah bertema kepercayaan.
- Pada uji #4 dan #5, hasil "BERHASIL" hanya menunjukkan *witness generation* gagal. Itu menguji pustaka, bukan *soundness* sistem. Perlu uji dengan bukti yang sengaja dipalsukan di luar sirkuit.

### M7. Tidak ada tinjauan pustaka komparatif; kontribusi hanya integrasi komponen

Sistem donasi privat yang paling relevan (Astraea, Eisdspa, He et al., UpHaaR) hanya muncul di daftar pustaka atau dikutip untuk klaim tangensial. Tidak ada tabel perbandingan fitur, model ancaman, dan biaya. Tanpa itu, kebaruan tidak dapat dinilai. Bagian "Hasil dan Pembahasan" juga nyaris tanpa pembahasan terhadap literatur, dan sebagian isinya (ERD, alur, siklus kampanye) adalah desain sistem yang seharusnya masuk Metode.

### M8. Reproduksibilitas

Tidak ada tautan kode, sirkuit, parameter *setup*, dan skrip *benchmark*. Untuk naskah yang menjadikan "evaluasi empiris" sebagai kontribusi, ini wajib (mis. repositori bertag + arsip Zenodo).

---

## 3. Kelemahan Minor

1. **Inkonsistensi alur:** Bagian 1a menyatakan klien mengirim *blinding factor*, sedangkan Hasil langkah 2 menyatakan backend yang membangkitkannya.
2. **Sitasi tidak tepat sasaran:** Paillier dijelaskan dengan merujuk Yang et al. (2023, *e-bills* SCF) dan Damle et al. (2021, voting). Karya aslinya, Paillier (EUROCRYPT 1999), tidak ada di pustaka. Sameera et al. (survei *federated learning*), Habib Nayan (*rollup bottleneck*), dan Dewangan & Msahli (IoT) dipakai untuk klaim yang relevansinya lemah. Dewangan & Msahli juga dipakai untuk dua klaim berbeda, jadi mohon dipastikan isinya memang mendukung keduanya.
3. **Referensi tak disitasi di teks:** He et al. (2024), Li et al. (2023), Burgos & Alchieri (2025), Moti & Gujar (2024), dan Wang et al. (2024).
4. **Proporsi preprint** tinggi (kurang lebih separuh dari 28 rujukan). Prioritaskan artikel terbitan resmi. Rujukan versi Circom 2.2.0 sebaiknya ke dokumentasi resmi, bukan TechRxiv 2022.
5. **Konteks Indonesia hilang:** regulasi yang relevan (UU PDP No. 27/2022, ketentuan pengumpulan uang dan barang) tidak dibahas, sementara GDPR dibahas panjang. Klaim bahwa donatur kecil "terintimidasi secara psikologis" membutuhkan sumber sosiologis/perilaku, bukan makalah kriptografi.
6. **Bahasa dan gaya:** "ultra-cepat", "jujur", "objektif", dan "berbeda dengan klaim idealistis yang kerap..." bersifat subjektif atau tanpa sitasi. Ketransparanan sebaiknya ditunjukkan lewat isi, bukan dinyatakan. "Phase 4 Roadmap" adalah istilah internal yang tidak dikenal pembaca.
7. **Istilah:** "penjumlahan modular" pada abstrak versus perkalian modular pada isi. Perkalian *ciphertext* menghasilkan penjumlahan *plaintext*. Mohon konsisten.
8. **Pola desain dual-write:** Alur yang diterapkan mirip *transactional outbox/saga*. Tulis dan rujuk polanya. Jelaskan juga bagaimana *retry* mencegah pengiriman ganda saat transaksi masih di *mempool* (manajemen *nonce*) dan apakah kontrak menolak *commitment* duplikat.
9. **Templat belum dibersihkan:** Header masih memuat "Vol. 4, No. 1, Juni 2024", DOI artikel, dan hal. 1–14 dari edisi sebelumnya (dua kali), serta ada angka sisa "78 77" di akhir. Pustaka bertahun 2026 membuat header ini janggal. Gunakan templat kosong.
10. **Penomoran dan penulisan:** Sebagian gambar dirujuk tanpa pembahasan substantif. Pastikan semua gambar beresolusi layak dan *font* diagram terbaca.

---

## 4. Pertanyaan untuk Penulis

1. Apa yang mencegah operator mengubah total yang didekripsi, dan bagaimana auditor memverifikasinya secara independen?
2. Apa tepatnya yang disimpan di *storage* kontrak versus *event*/kalldata, dan berapa gas masing-masing?
3. Mengapa Paillier dipilih, bukan skema homomorfik yang ramah-sirkuit?
4. Siapa yang menjalankan *trusted setup*, dan apakah *artifact*-nya dapat diperiksa?
5. Berapa latensi *end-to-end* dan *throughput* pada beban sebenarnya, tidak hanya 20 permintaan?

---

## 5. Keputusan dan Syarat Penerimaan

**Revisi Mayor.** Naskah dapat dipertimbangkan kembali jika penulis:

1. menambah model ancaman dan menyelaraskan seluruh klaim dengan Tabel 3 (M1, M2);
2. memperbaiki dan merinci pengukuran gas serta kinerja disertai statistik, *baseline*, dan latensi *end-to-end* (M3, M4);
3. menjustifikasi pilihan Paillier dan menutup atau, minimal, secara formal membatasi *binding gap* (M5, M6);
4. menambah tinjauan pustaka komparatif dan tautan kode untuk reproduksibilitas (M7, M8);
5. merapikan sitasi dan templat (bagian minor).

Kejujuran penulis tentang keterbatasan sistem patut dihargai. Namun kejujuran itu harus tercermin pada judul, abstrak, dan kesimpulan, bukan hanya pada Tabel 3.

*Reviewer 1*