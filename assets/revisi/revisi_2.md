# LAPORAN REVIEW PUTARAN 2
**Jurnal Simasi: Jurnal Ilmiah Sistem Informasi**

**Naskah:** Studi Desain dan Evaluasi Kinerja Prototipe Sistem Donasi Terdesentralisasi Hibrida Menggunakan Paillier dan zk-SNARK Groth16 (TrustGive)
**Dokumen yang ditelaah:** naskah revisi (`JURNAL_SIMASI_TRUSTGIVE_1.docx`) dan surat tanggapan penulis (`tanggapan_reviewer.md`)
**Catatan:** Gambar tidak ikut dinilai. Isi header/footer dokumen tidak terbaca pada ekstraksi teks.

---

## 1. Penilaian Umum

Terima kasih atas revisi dan tanggapan yang tertib. Kemajuan nyata ada pada hal-hal berikut:

- Pembingkaian ulang naskah menjadi studi desain dan kelayakan (Opsi b), termasuk judul, abstrak, dan kesimpulan.
- Model ancaman (Tabel 2), tabel komparatif (Tabel 1), rujukan Paillier (1999), konteks UU PDP, dan penghapusan sisa templat lama.
- Pengakuan atas penyebab angka 243.518 gas, yaitu muatan uji yang tidak representatif.

Namun naskah **belum dapat diterima**. Ada tiga kelompok masalah:

1. Beberapa klaim di surat tanggapan **tidak tercermin di naskah**.
2. **Aritmetika rekonsiliasi gas tidak menutup**, dan beberapa perbaikan baru memuat klaim yang keliru atau terlalu kuat.
3. Pertanyaan konseptual inti (nilai tambah ZK, verifikasi total, justifikasi Paillier) dijawab hanya sebagian.

**Rekomendasi: REVISI MAYOR (putaran 2, terbatas pada poin di bawah).**

---

## 2. Verifikasi Klaim Surat Tanggapan terhadap Naskah

| Klaim di surat | Temuan di naskah | Status |
|---|---|---|
| Judul, abstrak, kesimpulan dibingkai ulang (Opsi b) | Judul baru ada; abstrak dan kesimpulan memuat batasan | Terpenuhi (lihat catatan "terbukti" di bawah) |
| Model ancaman formal (Tabel 2) | Ada | Terpenuhi, tetapi lihat T2 |
| Tabel komparatif (Tabel 1) | Ada | Terpenuhi, tetapi lihat T7 |
| Paillier (1999) ditambahkan | Ada di teks dan pustaka | Terpenuhi |
| UU PDP ditambahkan | Ada di paragraf 2 Pendahuluan | Terpenuhi (belum masuk Daftar Pustaka) |
| Sisa templat ("Juni 2024", "78 77") dibersihkan | Tidak ada di badan teks | Terpenuhi; mohon periksa juga header/footer |
| "Catatan keterbatasan *hot-row* dan finalitas Hardhat/L2 ditambahkan" | Kata *hot row*, finalitas, *reorg*, L2 **tidak ditemukan** | **Tidak terpenuhi** |
| "Informasi akses kode dan skrip benchmark disertakan di naskah" | Tidak ada URL, repositori, atau DOI arsip | **Tidak terpenuhi** |
| Kata subjektif ("jujur", "objektif") dihapus | Masih ada: abstrak ID ("secara objektif"), abstrak EN ("rigorous", "objective empirical baseline"), Pembahasan ("secara objektif"), Kesimpulan ("secara jujur") | **Tidak terpenuhi** |
| "Phase 4 Roadmap" diganti istilah netral | Diganti menjadi "Roadmap Skripsi" (3 kali) | **Tidak memadai**: istilah skripsi tidak pantas dalam artikel jurnal |
| "Terbukti" dihapus | "terbukti efektif meniadakan anomali" masih ada di abstrak dan kesimpulan, padahal dasarnya uji 20 permintaan | **Tidak terpenuhi** |
| Spesifikasi lingkungan dirinci | Masih "Intel Core i7 / AMD Ryzen 7" dan "Windows/Linux" (alternatif, bukan satu mesin) | **Tidak memadai** |
| Rata-rata 100 iterasi | Ada, tetapi tanpa simpangan baku/persentil | Sebagian |
| Semua referensi (He, Li, Burgos, Moti, Wang) disitasi di teks | Moti & Gujar dan Wang et al. dihapus dari pustaka (bukan disitasi). Burgos & Alchieri masih di pustaka tetapi **tidak disitasi di teks** | **Tidak akurat** |
| Rujukan preprint/Circom diperbarui | Muñoz-Tapia (TechRxiv), Yang, Damle, Habib Nayan, dll. tidak berubah | **Tidak terpenuhi** |
| Latensi *end-to-end* 1,5–1,8 s dan *throughput* >60.000 op/s | Hanya ada di surat, tidak di naskah; juga bertentangan dengan Tabel 4 (lihat T5) | **Tidak terpenuhi dan tidak konsisten** |
| Uji soundness/forged proof (M6) | Tabel 5 tidak berubah; tidak ada uji baru | **Tidak ditanggapi** |
| Baseline pembanding (M4) | Tidak ada | **Tidak ditanggapi** |

Perbedaan antara surat dan naskah ini perlu diperbaiki lebih dulu. Surat tanggapan harus mencerminkan isi naskah secara akurat, dan hanya naskah yang dinilai.

---

## 3. Masalah Teknis yang Masih Terbuka

### T1. Rekonsiliasi gas: aritmetika tidak menutup, dan sampel uji tidak representatif

- Rincian pada Tabel 3 baris 4 berjumlah 21.000 + 4.500 + 181.000 + 22.100 + 1.500 = **230.100**, bukan 243.518. Selisih ±13.400 tidak dijelaskan. Dugaan saya, selisih itu berasal dari operasi skalar/penjumlahan kurva untuk *public input* (ecMul/ecAdd), padahal naskah menulis angka 181.000 sebagai "pairing beserta skalar publik".
- Proyeksi **563.500** tidak sesuai komponennya. Baris 5 berjumlah 21.000 + 181.000 + 8.000 + 320.000 + 1.500 = **531.500**. Angka 563.500 tampaknya hasil 243.518 + 320.000, yang menghitung ganda satu slot dan calldata.
- Biaya satu slot *storage* baru adalah 22.100 (bukan 20.000 seperti di Tabel 3 baris 5), sehingga 16 slot ≈ 353.600.
- Struct `Donation` memiliki enam bidang (`campaignId`, `commitment`, `encryptedAmount`, `zkProof`, `submitter`, `timestamp`). Tidak mungkin semuanya muat di **satu** slot. Bukti Groth16 mentah (256 byte) saja ≈ 8 slot jika disimpan.
- Artinya angka utama pada abstrak (243.518 gas) diukur dengan muatan tiruan, bukan sistem yang sebenarnya.

**Yang diminta:** ukur ulang dengan muatan nyata (*ciphertext* 512 byte dan bukti asli), gunakan *gas reporter* atau *trace* per-opcode (bukan estimasi manual), dan sajikan satu rincian yang jumlahnya persis sama dengan angka terukur. Pertimbangkan juga desain umum untuk menurunkan biaya: simpan hanya *hash* (`keccak256`) dari *ciphertext* dan bukti di *storage*, lalu pancarkan data lengkap lewat *event*. Biaya log ±8 gas/byte jauh lebih murah dan tetap dapat diaudit di luar rantai.

### T2. Model ancaman (Tabel 2) memiliki inkonsistensi internal

- **Honest-but-curious vs. serangan aktif.** Baris "Server Backend" berasumsi *honest-but-curious*, tetapi ancaman yang dimodelkan di baris itu, yaitu substitusi *ciphertext*, adalah serangan **aktif** (*malicious*). Server yang jujur-tapi-penasaran, menurut definisinya, tidak melakukannya. Pilih satu model dan konsisten.
- **Motivasi vs. asumsi.** Pendahuluan memotivasi karya ini dengan risiko manipulasi oleh pengelola terpusat, tetapi Tabel 2 mengasumsikan pengelola tidak memanipulasi. Ini menghilangkan ancaman yang menjadi alasan sistem dibangun.
- **Nilai tambah ZK tidak dijustifikasi.** Pertanyaan inti dari putaran 1 belum dijawab: server membangkitkan *witness*, membangkitkan bukti, dan memverifikasinya sendiri. Pada server jujur, pemeriksaan rentang cukup dilakukan di server. Pada server jahat, bukti tidak bernilai karena server memilih *witness*. Jelaskan secara eksplisit ancaman apa yang hanya dapat ditangani oleh bukti ZK di arsitektur ini. Jelaskan juga siapa yang boleh memanggil `recordDonation` (kontrol akses). Jika fungsinya publik, jelaskan dampaknya.
- **Mitigasi *replay* diklaim terlalu kuat.**
  - Pengecekan `pubSignals[0] == campaignMaxDonation[campaignId]` hanya mencocokkan pagu, **bukan** mengikat bukti ke kampanye tertentu. Dua kampanye dengan pagu yang sama dapat memakai bukti yang sama.
  - `Idempotency-Key` ditentukan klien, sehingga kunci baru dapat dibuat pada setiap percobaan.
  - Keunikan *commitment* hanya ditegakkan di PostgreSQL, tidak di kontrak. Siapa pun yang dapat memanggil kontrak langsung tidak terhalang.
  - Karena itu baris "Donatur Jahat: TERMITIGASI" sebaiknya menjadi "SEBAGIAN". Perbaikan yang disarankan: masukkan `campaign_id` ke sinyal publik atau ke *preimage* komitmen, dan tambahkan `mapping(bytes32 => bool) usedCommitment` di kontrak.
- **Ancaman yang belum ada di tabel:** organizer yang mempublikasikan total hasil dekripsi yang salah; *trusted setup* yang dapat dipalsukan (lihat T6); administrator basis data.
- **Narasi menyesatkan.** Judul Bagian 3.2 ("Konfidensial") dan kalimat di Bagian 3.3 ("tanpa pernah membuka rincian nominal masing-masing donatur") bertentangan dengan Tabel 5 baris 11, yaitu server mengetahui semua nominal. Koreksi kedua bagian itu.

### T3. Jawaban atas "bagaimana auditor memverifikasi total" belum cukup

Auditor yang mengalikan seluruh *ciphertext* hanya dapat memastikan **agregasinya**. Auditor tidak dapat memastikan **hasil dekripsi** yang dipublikasikan, karena tidak memiliki kunci privat.

Ada perbaikan murah yang tidak memerlukan *Threshold Paillier*. Pada Paillier, pemegang kunci dapat memulihkan nilai acak `r` dari `c_agg · g^(−m) mod n²`. Dengan mempublikasikan pasangan `(m, r)`, siapa pun dapat memeriksa bahwa `c_agg = g^m · r^n mod n²`. Ini membuat total yang dipublikasikan dapat diverifikasi publik. Perbaikan ini tidak menutup *binding gap* atau pencurian kunci, tetapi menutup celah manipulasi total pada langkah dekripsi. Pertimbangkan menambahkannya ke prototipe atau, minimal, ke agenda penelitian lanjutan.

### T4. Justifikasi pemilihan Paillier masih sebagian

- Jawaban hanya membahas Exponential ElGamal. *Pedersen commitment*, alternatif yang saya tanyakan dan yang bahkan muncul di Tabel 1 (baris Eisdspa), tidak dibahas sama sekali. Dengan Pedersen, komitmen dapat diagregasi secara publik (bahkan di on-chain), dan total dibuka dengan menyingkap `(total, jumlah faktor *blinding*)` tanpa pencarian logaritma diskrit dan tanpa kunci privat tunggal.
- Argumen batas 2³²–2⁴⁰ untuk BSGS dilebih-lebihkan sebagai "kendala praktis". Dalam rupiah, 2⁴⁰ ≈ Rp1,1 triliun per kampanye, di atas total hampir semua kampanye donasi. Kuantifikasikan argumen ini dengan rentang total kampanye yang realistis.
- Tambahkan paragraf yang menyatakan kapan pilihan Paillier unggul dan kapan alternatif lebih baik.

### T5. Pengukuran dan klaim kinerja

- Penjelasan g = n + 1 hanya menjelaskan suku g^m. Suku dominan adalah r^n mod n² (eksponen ±2048-bit, modulus ±4096-bit), yang menurut perkiraan saya lazimnya berada pada orde puluhan milidetik di Go. Angka enkripsi 2,40 ms, dekripsi 3,10 ms, dan *keygen* 42,5 ms masih memerlukan bukti. Lampirkan keluaran mentah `go test -bench`, nama dan versi pustaka Paillier, apakah CRT atau *pool* r^n dipakai, dan satu model CPU yang tepat.
- Latensi *end-to-end* 1,5–1,8 s di surat tidak konsisten dengan Tabel 4. Langkah berurutan (witness 185 ms + bukti 1.350 ms + verifikasi lokal 1.850 ms) saja sudah ±3,4 s, belum termasuk enkripsi, transaksi on-chain, dan basis data. Ukur latensi dan *throughput* sistem secara nyata (dengan beban terukur, bukan hanya 20 permintaan), lalu masukkan ke naskah.
- ">60.000 operasi/detik" adalah *micro-benchmark* perkalian modular, bukan *throughput* sistem. Jangan menyebutnya sebagai *throughput* agregasi sistem.
- Laporkan simpangan baku dan persentil. Tambahkan *baseline* (minimal: donasi *plaintext* on-chain dan komitmen-saja) agar angka 243.518/563.500 gas memiliki pembanding.
- Tambahkan catatan nyata di naskah tentang *hot row* pada `campaign_aggregates` serta finalitas instan Hardhat (jumlah konfirmasi, *reorg*, biaya di L2/jaringan publik).

### T6. Sirkuit dan *trusted setup*

- Kalimat "komparator mengasumsikan input < 2⁶⁴" menyatakan asumsi, bukan batasan. Tegakkan dengan `Num2Bits(64)` eksplisit pada `amount` dan `campaign_max`, atau lampirkan argumen *soundness* yang terperinci. Jalankan alat analisis sirkuit (mis. `circomspect`) dan laporkan hasilnya.
- Tambahkan uji negatif yang menyerang di luar sirkuit: nilai *field-wrapped* (p − k), bukti untuk pernyataan lain, bukti yang dipakai ulang lintas kampanye, dan substitusi publik-sinyal. Uji #4 dan #5 hanya menunjukkan pembangkitan *witness* gagal, bukan *soundness* verifier.
- *Trusted setup* oleh satu pihak (tim peneliti sendiri) berarti pihak itu mengetahui *toxic waste* dan dapat memalsukan bukti. Ini wajar untuk prototipe, tetapi harus dinyatakan sebagai keterbatasan dan masuk Tabel 2. Sebutkan jumlah kontributor, sumber fase 1 (mis. *Perpetual Powers of Tau* publik), kontribusi dan *beacon* fase 2, serta *hash* berkas `.zkey`. Istilah "seremoni" sebaiknya tidak dipakai untuk pelaksanaan satu pihak.

### T7. Tabel 1 dan tinjauan pustaka

- Tabel 1 memuat klaim spesifik tentang sistem pihak ketiga (mis. UpHaaR "SHA-256 & IPFS" dan "Plaintext Smart Contract", Astraea "biaya gas tinggi", Eisdspa "Pedersen"). Saya tidak dapat memverifikasinya dari naskah. Cantumkan bagian/halaman sumber dan angka kuantitatif jika tersedia, dan pastikan setiap sel dapat ditelusuri ke sumbernya.
- Kolom saat ini membandingkan paradigma dan keterbatasan, bukan properti. Tambahkan kolom properti, misalnya: nominal tersembunyi dari operator, total dapat diverifikasi publik, anonimitas donatur, biaya gas, dan asumsi *trusted setup*. Dengan begitu pembaca dapat melihat di mana TrustGive unggul dan di mana tidak.
- Kalimat bahwa sistem lain "membebani gas" memerlukan angka dan sumber.
- "Hasil dan Pembahasan" masih tidak memuat pembahasan terhadap literatur. Tambahkan subbagian yang membandingkan temuan Anda dengan Tabel 1.

---

## 4. Catatan Minor

1. **Sitasi tidak sesuai:** Chaliasos et al. (2024), sebuah SoK tentang kerentanan SNARK, dikutip untuk klaim bahwa Paillier tidak ramah sirkuit. Sameera et al. (survei *federated learning*), Habib Nayan (*rollup*), dan Dewangan & Msahli (IoT; dipakai untuk dua klaim berbeda) masih tangensial. Klaim sosial (donatur kecil enggan karena stigma) tetap bersandar pada Zhou et al. dan membutuhkan sumber filantropi/perilaku.
2. **Proporsi preprint** masih sekitar separuh dari 28 rujukan. Ganti dengan versi terbitan resmi bila ada. Circom sebaiknya dirujuk ke dokumentasi resmi.
3. **UU PDP** perlu masuk Daftar Pustaka sebagai sumber hukum.
4. **Istilah "Roadmap Skripsi"** dan "agenda skripsi lanjutan" (Bagian 3.6 dan Kesimpulan) diganti "agenda penelitian lanjutan".
5. **Struktur:** Bagian "Hasil" masih memuat desain sistem (ERD, alur, siklus kampanye) yang lebih tepat di Metode. Penomoran subbagian dimulai ulang dengan "1." di setiap bagian, sehingga rujukan di surat ("Bagian 2.1", "Bab 3 Subbab 5a") tidak cocok dengan naskah. Samakan.
6. **Gaya bahasa:** hapus "sangat cepat", "ultra", "rigorous", "objective", "jujur", "objektif" (lihat tabel klaim). Biarkan data yang menunjukkan transparansi.
7. **"Membuktikan"** pada kalimat tentang Tabel 4 ("membuktikan bahwa akumulasi ribuan transaksi...") perlu diganti dengan bahasa yang sesuai bukti (mis. "mengindikasikan").

---

## 5. Daftar Perbaikan Wajib untuk Putaran 3

**Prioritas tinggi (penentu keputusan):**
1. Ukur ulang gas dengan muatan nyata dan sajikan rincian yang jumlahnya sama persis dengan angka terukur. Koreksi proyeksi 563.500 dan biaya slot 22.100 (T1).
2. Konsistenkan model ancaman: HbC vs. serangan aktif, motivasi vs. asumsi, dan jelaskan nilai tambah ZK serta kontrol akses kontrak (T2).
3. Perbaiki atau koreksi klaim *replay* lintas kampanye dan tambahkan proteksi on-chain (T2).
4. Tambahkan jalur verifikasi total (mis. pengungkapan `(m, r)`) atau nyatakan sebagai batasan eksplisit (T3).
5. Selaraskan seluruh klaim di surat dengan isi naskah (Bagian 2 laporan ini): *hot row*/finalitas, tautan kode, kata subjektif, "terbukti", dan referensi.

**Prioritas menengah:**
6. Lengkapi bukti benchmark: keluaran mentah, satu mesin, simpangan baku, latensi dan *throughput* sistem nyata, *baseline* (T5).
7. Tegakkan `Num2Bits(64)` atau lampirkan argumen *soundness*; tambahkan uji serangan di luar sirkuit; dokumentasikan *trusted setup* (T6).
8. Lengkapi pembahasan alternatif Pedersen dan kuantifikasi argumen BSGS (T4).
9. Perkuat Tabel 1 (sumber, kolom properti) dan tambahkan pembahasan terhadap literatur (T7).

**Prioritas rendah:** catatan minor (Bagian 4).

---

## 6. Keputusan

**Revisi Mayor (terbatas).** Arah revisi sudah benar dan kejujuran penulis terhadap keterbatasan sistem patut dihargai. Namun keputusan akhir bergantung pada tiga hal: ketepatan data gas dan benchmark, konsistensi model ancaman dengan klaim, dan kesesuaian surat tanggapan dengan isi naskah. Mohon sertakan pada resubmisi sebuah surat tanggapan yang menunjuk lokasi perubahan (nomor bagian dan halaman) untuk tiap poin di atas.

*Reviewer 1*