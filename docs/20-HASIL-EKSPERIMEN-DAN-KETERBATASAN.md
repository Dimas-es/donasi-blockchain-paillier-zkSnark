# Hasil Eksperimen, Keterbatasan Kriptografi, dan Panduan Sidang

Dokumen ini menyajikan rangkuman hasil pengujian empiris sistem, analisis mendalam terhadap **4 keterbatasan kriptografi utama**, serta **panduan antisipasi pertanyaan dosen penguji** dalam sidang skripsi.

---

## 1. Rangkuman Hasil Eksperimen Empiris

Berdasarkan pengujian benchmark yang dijalankan pada lingkungan lokal (`zk/scripts/benchmark-zk.js` dan Hardhat local node):

| Metrik Komputasi | Hasil Eksperimen | Standar Industri / Toleransi | Evaluasi |
| :--- | :--- | :--- | :--- |
| **Waktu Proof Generation (Client)** | $\approx 235.98\text{ ms}$ | $< 1000\text{ ms}$ (1 detik) | **Sangat Baik** (Dapat dieksekusi instan di peramban/client) |
| **Waktu Verifikasi Off-Chain (Backend)** | $\approx 16.80\text{ ms}$ | $< 50\text{ ms}$ | **Sangat Cepat** (Throughput tinggi untuk server Go) |
| **Konsumsi Gas Verifikasi On-Chain (EVM)** | $\approx 245.000\text{ gas}$ | $< 350.000\text{ gas}$ | **Hemat** (Memanfaatkan precompile `alt_bn128` di alamat `0x08`) |
| **Ukuran Bukti (Groth16 Proof)** | $\approx 723\text{ bytes}$ (JSON raw: 130 byte) | $< 1\text{ KB}$ | **Paling Ringkas** (Jauh lebih hemat daripada STARK ~100 KB) |
| **Ukuran Kunci Setup (`zkey`)** | $\approx 308.1\text{ KB}$ | $< 5\text{ MB}$ | **Ringan** (Mudah di-load di memori aplikasi) |

---

## 2. Empat Keterbatasan Kritis Sistem & Jawaban Ujian Sidang

Berikut adalah 4 hal paling fundamental yang menjadi batasan arsitektur saat ini dan strategi ilmiah menjawabnya saat diuji oleh dosen atau penguji kriptografi:

---

### Keterbatasan 1: Ketiadaan Ikatan Langsung ke Paillier (*The Proof-to-Ciphertext Binding Problem*)

* **Deskripsi Masalah:**  
  Sirkuit zk-SNARK Groth16 dan Enkripsi Paillier beroperasi pada domain aljabar yang terpisah (*Algebraic Mismatch*):
  * **zk-SNARK:** Beroperasi pada kurva eliptik BN254 di atas lapangan prima berorde $r \approx 2^{254}$.
  * **Paillier:** Beroperasi pada ring komposit $\mathbb{Z}_{n^2}^*$ berukuran modulus RSA $2048\text{ bit}$ ($n^2 \approx 4096\text{ bit}$).
  * Sirkuit [DonationProof.circom](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system-main/zk/circuits/DonationProof.circom) saat ini hanya membuktikan: *"Ada nominal $m$ yang sah ($0 < m \le \text{max}$) di dalam komitmen Poseidon ini."*
  * Sirkuit tidak menyentuh ciphertext Paillier $c = g^m r^n \bmod n^2$.
* **Celah Potensial (*Substitution Attack*):**  
  Penyerang jahat secara teoretis dapat men-generate proof valid untuk nominal Rp 50.000, tetapi mengirimkan ciphertext Paillier berisi Rp 5.000.000. Sistem mencatat donasi karena proof valid, sehingga agregat dana terdistorsi.
* **Arah Solusi Penelitian Lanjutan:**
  1. *In-Circuit Paillier (Direct):* Membuktikan operasi eksponensiasi 2048-bit di dalam sirkuit R1CS. (Sangat mahal: butuh $\ge 500.000$ constraints, tidak layak untuk browser).
  2. *Hash-Transcript Binding (Pragmatis):* Menghash ciphertext $c$ menjadi $h_c \in \mathbb{F}_r$ dan memasukkannya sebagai public input sirkuit yang mengikat komitmen: $C = \text{Poseidon}(m, s, h_c)$ (Lihat rancangan teknis lengkap di `docs/13-PROOF-TO-CIPHERTEXT-BINDING.md`).
  3. *Skema Homomorfik Ramah Kurva:* Mengganti Paillier dengan Exponential ElGamal atau Pedersen Commitment di atas kurva eliptik yang sama (BN254 atau BabyJubjub).
* **Jawaban Resmi ke Dosen:**  
  > *"Ketiadaan verifikasi in-circuit Paillier adalah batasan yang disengaja akibat trade-off 'The Algebraic Mismatch' antara kurva BN254 dan modulus RSA 2048-bit. Memaksakan modular 2048-bit ke dalam R1CS akan melonjakkan constraints hingga lebih dari 500.000 gerbang yang membuat browser crash. Sebagai mitigasi desain, kami merumuskan Hash-Transcript Binding pada dokumen spesifikasi Bab Keterbatasan sebagai roadmap masa depan."*

---

### Keterbatasan 2: Pengikat Transaksi On-Chain (*Replay Attack*)

* **Deskripsi Masalah:**  
  Bukti zk-SNARK yang berdiri sendiri bersifat agnostik terhadap transaksi. Tanpa identifier transaksi atau nullifier, bukti yang pernah disubmit oleh Alice secara teoretis dapat disalin dari mempool/blockchain oleh Bob dan dikirim ulang.
* **Status Mitigasi Sistem Saat Ini:**
  * Di backend (`internal/donation/service.go`), anti-replay diterapkan melalui pengecekan keunikan *commitment* di database (`ErrDuplicateCommitment`).
  * Di level smart contract [DonationRegistry.sol](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system-main/blockchain/contracts/DonationRegistry.sol), mapping keunikan commitment belum dikunci secara eksplisit:
* **Rekomendasi Implementasi:**
  Menambahkan pemetaan pada smart contract:
  ```solidity
  mapping(bytes32 => bool) public isCommitmentUsed;
  require(!isCommitmentUsed[commitment], "commitment already used");
  isCommitmentUsed[commitment] = true;
  ```
* **Jawaban Resmi ke Dosen:**  
  > *"Pencegahan replay attack pada prototipe ini ditangani pada lapisan service backend melalui verifikasi keunikan komitmen Poseidon sebelum dispatch on-chain. Untuk level desentralisasi penuh, rekomendasi pengembangannya adalah memindahkan tabel nullifier/commitment mapping ke storage smart contract."*

---

### Keterbatasan 3: Penguncian Rentang Eksplisit Bit-Size (*Num2Bits*)

* **Deskripsi Masalah:**  
  Komponen komparator Circom (`GreaterThan(64)` dan `LessEqThan(64)`) mengasumsikan input berada pada rentang $[0, 2^{64}-1]$.
  Di dalam medan hingga (finite field) BN254, elemen sebenarnya berorde $p \approx 2^{254}$. Jika penyerang menyuntikkan angka raksasa di atas $2^{64}$ (misal $p - 1$), komparator tanpa pengecekan bit eksplisit berisiko mengalami *field underflow/overflow* yang dapat memanipulasi logika pertidaksamaan.
* **Solusi Penegasan:**  
  Menambahkan konversi eksplisit `Num2Bits(64)` pada sinyal `amount` di dalam [DonationProof.circom](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system-main/zk/circuits/DonationProof.circom):
  ```circom
  component n2b = Num2Bits(64);
  n2b.in <== amount;
  ```
* **Jawaban Resmi ke Dosen:**  
  > *"Pada prototipe awal, batas atas diproteksi melalui sinyal public campaign_max dan logic comparator 64-bit. Sebagai penguatan formal keamanan sirkuit dari potensi field wraparound attack, penambahan constraint Num2Bits(64) telah kami dokumentasikan sebagai rekomendasi pengetatan sirkuit."*

---

### Keterbatasan 4: Keamanan Trusted Setup (*Powers of Tau*)

* **Deskripsi Masalah:**  
  Algoritma zk-SNARK Groth16 membutuhkan parameter awal (*Common Reference String / CRS*) melalui proses 2 tahap:
  * **Phase 1:** *Powers of Tau* universal.
  * **Phase 2:** *Circuit-specific ceremony* untuk [DonationProof.circom](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system-main/zk/circuits/DonationProof.circom).
  Jika proses setup dijalankan oleh satu pihak secara tertutup di laptop lokal tanpa memusnahkan parameter acak (*toxic waste*), pihak tersebut secara teoretis dapat memalsukan bukti tanpa terdeteksi.
* **Jawaban Resmi ke Dosen:**  
  > *"File `pot12` dan `.zkey` pada repositori ini dibuat khusus untuk keperluan eksperimen laboratorium lokal. Untuk implementasi produksi di mainnet publik, sistem ini wajib mengimpor CRS dari upacara publik multi-partai yang telah terbukti aman (seperti **Perpetual Powers of Tau** milik Ethereum Foundation/Hermez dengan ribuan kontributor global)."*

---

## 3. Strategi Pembuktian saat Sidang Skripsi

1. **Jangan Berhenti pada Demo Sukses:** Dosen penguji menyukai pengujian negatif (*fail case*). Tunjukkan bahwa sistem Anda otomatis menolak donasi dengan angka negatif atau nominal melebihi batas (sebagaimana terbukti pada `node zk/scripts/generate-donation-proof.js`).
2. **Akui Keterbatasan Secara Terbuka:** Mengakui 4 keterbatasan di atas pada Bab 5 Skripsi membuktikan bahwa Anda tidak sekadar menjadi *skrip-kiddie* pemakai library, melainkan **benar-benar memahami arsitektur internal matematika kriptografi** yang Anda bangun.
