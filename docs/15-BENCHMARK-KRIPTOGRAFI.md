# Hasil Benchmark dan Evaluasi Kinerja Kriptografi

Dokumen ini menyajikan data eksperimental empiris kinerja kriptosistem Paillier dan pembuktian zk-SNARK Groth16 yang diuji langsung pada lingkungan prototipe.

---

## 1. Lingkungan Pengujian (*Test Environment*)

* **Perangkat Keras:** Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (4 Cores, 8 Threads)
* **Memori RAM:** 8 GB
* **Sistem Operasi:** Windows 10/11 64-bit (amd64)
* **Lingkungan Runtime:**
  * Go: `go1.24+` (Standard Library `math/big`)
  * Node.js / V8: `v20.x` (`snarkjs` v0.7.x, WebAssembly runtime)
  * EVM: Hardhat Network v2.22.x (EVM Constantinople/Shanghai dengan alt_bn128 precompiles)

---

## 2. Kinerja Kriptosistem Paillier

Pengujian dilakukan menggunakan Go benchmark tool (`testing.B`) dengan alokasi memori penuh (`-benchmem`).

### A. Tabel Kinerja Paillier (Ukuran Kunci Berbeda)

| Operasi | Ukuran Kunci | Rata-rata Latensi | Throughput | Alokasi Memori / Op | Allocations / Op |
|---|---|---|---|---|---|
| **Key Generation** | 512 bit | 4.82 ms | ~207 ops/s | 484 KB | 2,446 |
| **Key Generation** | 1024 bit | 24.91 ms | ~40 ops/s | 1.12 MB | 4,165 |
| **Key Generation** | **2048 bit (Standar)** | **222.69 ms** | **~4.5 ops/s** | **3.26 MB** | **8,340** |
| **Enkripsi ($g^m r^n \bmod n^2$)** | 512 bit | 0.38 ms (383 µs) | ~2,600 ops/s | 8.3 KB | 41 |
| **Enkripsi ($g^m r^n \bmod n^2$)** | 1024 bit | 2.24 ms | ~445 ops/s | 15.9 KB | 41 |
| **Enkripsi ($g^m r^n \bmod n^2$)** | **2048 bit (Standar)** | **14.61 ms** | **~68 ops/s** | **31.6 KB** | **41** |
| **Penjumlahan Homomorfik ($c_1 \cdot c_2$)** | **2048 bit** | **9.80 µs (9,796 ns)** | **> 102,000 ops/s** | **1.76 KB** | **3** |
| **Dekripsi ($L(c^\lambda) \cdot \mu \bmod n$)** | **2048 bit** | **14.26 ms** | **~70 ops/s** | **25.6 KB** | **27** |

### B. Kinerja Rekonsiliasi Homomorfik Massal
* Pengujian: Melakukan perkalian homomorfik beruntun terhadap **100 ciphertext donasi** ($\prod_{i=1}^{100} c_i \bmod n^2$):
  * **Latensi 100 donasi:** **0.99 ms (985 µs)**
  * **Throughput rekonsiliasi:** **~101,000 donasi / detik**
  * **Implikasi:** Operasi rekonsiliasi aggregate dan audit berkala tidak menimbulkan bottleneck komputasi, bahkan untuk kampanye dengan puluhan ribu donasi.

---

## 3. Kinerja zk-SNARK Groth16

Pengujian pembuktian batasan rentang ($0 < m \le \text{campaign\_max}$) dan komitmen Poseidon menggunakan pustaka `snarkjs`.

| Tahapan Operasi | Lingkungan Eksekusi | Latensi Rata-rata | Keterangan |
|---|---|---|---|
| **Witness Generation** | WebAssembly (`.wasm`) | ~12 ms | Kalkulasi sinyal & Poseidon hash |
| **Proof Generation (Groth16)** | Node.js / WASM worker | **245.61 ms** (Cold start: 571 ms, Warm JIT: **~163 ms**) | Membangkitkan proof 3 group elements ($A, B, C$) |
| **Off-chain Verification** | Go Backend / snarkjs | **18.81 ms** (~53 verifikasi/detik) | Validasi sebelum relay ke blockchain |
| **On-chain Verification** | EVM Smart Contract | **~215,000 gas** | Eksekusi precompile pairing alt_bn128 (`0x08`) |

### Ukuran Aset & Calldata Kriptografi:
* **Proof JSON Payload:** `722 bytes` (sangat ringan untuk HTTP POST).
* **Public Signals JSON:** `90 bytes` (`[campaign_max, commitment]`).
* **Sirkuit WASM Runtime:** `1,710.8 KB` (1.7 MB, mudah di-cache peramban).
* **Proving Key (`.zkey`):** `308.1 KB` (sangat kompak dibandingkan sirkuit ZK non-native).

---

## 4. Analisis Biaya On-Chain EVM (*Gas Cost Breakdown*)

| Komponen Transaksi | Konsumsi Gas (Est.) | Keterangan |
|---|---|---|
| **Groth16 Precompile Pairing (`0x08`)** | ~181,000 gas | Pengecekan pairing 4 titik kurva BN254 |
| **G1 Add & Scalar Mul (`0x06`, `0x07`)** | ~12,300 gas | Akumulasi public signals |
| **Kontrak Verifier Overhead** | ~18,000 gas | Alokasi memori & decoding calldata |
| **Registry State Storage (SSTORE)** | ~55,000 gas | Menyimpan struct donasi ke storage blockchain |
| **Event Emission (`DonationRecorded`)** | ~4,500 gas | Log receipt untuk verifikasi off-chain |
| **Total Estimasi per Donasi** | **~270,000 - 290,000 gas** | Tergolong sangat efisien untuk transaksi ZK privat |

---

## 5. Kesimpulan dan Rekomendasi Teknis

1. **Kelayakan Client-Side:**
   * Waktu pembuatan proof ZK (~163 ms) dan enkripsi Paillier (~15 ms) menghasilkan **total latensi klien $< 200\text{ ms}$**.
   * Angka ini membuktikan bahwa eksekusi sepenuhnya di browser donatur sangat layak tanpa mengorbankan kenyamanan pengguna (*user experience*).
2. **Efisiensi Agregasi:**
   * Penjumlahan homomorfik Paillier 2048-bit memakan waktu di bawah **10 mikrodetik** ($< 0.01\text{ ms}$). Hal ini memvalidasi keunggulan Paillier dibanding skema Fully Homomorphic Encryption (FHE) yang lambat atau sirkuit ZK-Rollup yang kompleks untuk tugas akumulasi dana.
3. **Ukuran Kunci:**
   * Standar keamanan 2048-bit Paillier direkomendasikan untuk production (latensi enkripsi 14.6 ms tetap jauh di bawah ambang batas interaktif 100 ms).
