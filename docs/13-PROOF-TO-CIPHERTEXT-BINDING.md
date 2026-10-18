# Desain Proof-to-Ciphertext Binding

Dokumen ini memaparkan rancangan teknis dan arsitektur kriptografi untuk mengatasi kesenjangan konsistensi antara pembuktian zk-SNARK dan ciphertext Paillier (*proof-to-ciphertext binding*).

---

## 1. Masalah Kesenjangan Aljabar (*The Algebraic Mismatch*)

Dalam sistem donasi ini, terdapat dua domain kriptografi dengan struktur aljabar yang berbeda:

1. **Sirkuit zk-SNARK (Groth16):**
   * Beroperasi pada kurva eliptik BN254 (alt_bn128) di atas *finite field* prima $\mathbb{F}_r$ berorde $r \approx 2^{254}$.
   * Dirancang optimal untuk operasi aritmetika polinomial derajat rendah di $\mathbb{F}_r$.
2. **Kriptosistem Paillier:**
   * Beroperasi pada ring residu komposit $\mathbb{Z}_{n^2}^*$ dengan modulus RSA $n = p \cdot q$ berukuran $2048\text{ bit}$ (sehingga $n^2 \approx 4096\text{ bit}$).
   * Enkripsi melibatkan eksponensiasi modular bernilai besar: $c = g^m \cdot r_{\text{enc}}^n \bmod n^2$.

### Dampak Tanpa Binding (*Substitution Attack*)
Pada prototipe awal:
* Sirkuit Groth16 memverifikasi batasan rentang: $0 < m \le \text{campaign\_max}$ dan komitmen $C = \text{Poseidon}(m, s)$.
* Ciphertext Paillier $c$ dienkripsi terpisah di luar sirkuit.
* **Celah:** Penyerang atau server perantara yang tidak jujur dapat membuat proof valid untuk $m_1 = 100.000$, tetapi menyodorkan ciphertext $c = \text{Enc}(10.000.000)$ atau $c = \text{Enc}(0)$. Kontrak dan verifier akan menerima transaksi karena proof valid, sehingga agregat terenkripsi terdistorsi tanpa terdeteksi.

---

## 2. Taksonomi Opsi Desain

| Kriteria | Opsi 1: In-Circuit Paillier (Direct) | Opsi 2: Hash-Transcript Binding (Pragmatic Target) | Opsi 3: Hybrid ZK + NIZK Equality (Camenisch-Shoup) |
|---|---|---|---|
| **Mekanisme** | Menghitung eksponensiasi $g^m r^n \bmod n^2$ langsung di dalam R1CS Circom menggunakan *big-integer library*. | Ciphertext $c$ di-hash ($h_c \in \mathbb{F}_r$). $h_c$ dijadikan public input sirkuit dan diikat ke commitment: $C = \text{Poseidon}(m, s, h_c)$. | ZK membuktikan rentang $m$. Protokol NIZK terpisah membuktikan kesetaraan nilai $m$ antara komitmen kurva dan ciphertext Paillier. |
| **Beban R1CS Constraints** | Ekstrem ($\ge 500.000$ constraints). | Sangat ringan ($< 500$ constraints tambahan). | Sedang (SNARK tetap kecil, NIZK proof terpisah $\approx 1.5\text{ KB}$). |
| **Kelayakan Client-Side (Browser)** | Tidak layak (membutuhkan RAM multi-GB dan waktu pembuktian hitungan menit). | **Sangat layak** (waktu pembuktian $< 1$ detik di browser). | Layak (membutuhkan implementasi library NIZK di JavaScript/Go). |
| **Jaminan Kriptografi** | Soundness 100% monolitik dalam satu sirkuit. | Mengikat proof mati ke $c$ tertentu (*non-malleability* & anti-substitusi). | Soundness formal penuh tanpa komputasi modular non-native di sirkuit. |

---

## 3. Spesifikasi Arsitektur Pilihan: Opsi 2 (Hash-Transcript Binding)

Untuk sistem donasi terdistribusi yang efisien pada browser dan EVM, **Opsi 2** dipilih sebagai implementasi inti dengan arsitektur berikut:

```
[ Donatur / Client ]
  1. Siapkan m (amount), s (secret), r_enc (Paillier randomness)
  2. Hitung Paillier Ciphertext:
       c = g^m * (r_enc)^n  mod n^2
  3. Hitung Field-Compatible Hash dari Ciphertext:
       h_c = Poseidon(c_chunk_0, c_chunk_1, ...) mod r
  4. Generate zk-SNARK Witness & Proof (Groth16):
       Public Inputs: [ campaign_max, h_c ]
       Public Output: C = Poseidon(amount, secret, h_c)
       Constraint:    0 < amount <= campaign_max
  5. Kirim payload: { c, proof, commitment, h_c }
         |
         v
[ Smart Contract / DonationRegistry.sol ]
  1. Hitung on-chain hash: h_c' = ComputeHash(c)
  2. Validasi kesesuaian: require(h_c' == h_c, "Ciphertext hash mismatch")
  3. Verifikasi Groth16: require(verifier.verifyProof(proof, [campaign_max, h_c, commitment]))
  4. Catat c ke ledger & akumulasi ke agregat jika sukses
```

### Keunggulan Teknis Opsi 2:
1. **Pencegahan Substitusi Penuh:** Jika penyerang mengganti ciphertext $c$ menjadi $c'$, maka $h_c' \neq h_c$. Verifikasi smart contract akan gagal sebelum transaksi dicatat.
2. **Efisiensi Eksekusi:** Tidak ada penambahan biaya gas on-chain yang signifikan dan proof generation di browser tetap instan ($< 1$ detik).
3. **Kompatibilitas:** Mempertahankan kontrak Groth16 verifier standar tanpa dependensi sirkuit non-native yang rapuh.

---

## 4. Opsi 3 sebagai Landasan Formal Penelitian (*Theoretical Extension*)

Sebagai kontribusi akademis pada laporan penelitian/paper, Opsi 3 (*Verifiable Encryption*) dirumuskan sebagai model ideal teoretis:

* **Sirkuit ZK Kurva (BN254):**
  Membuktikan rentang $m \in (0, \text{max}]$ dan mengeluarkan komitmen Pedersen $C_{\text{ped}} = g_1^m h_1^s \in G_1$.
* **Protokol NIZK Proof of Plaintext Equality (PoPE):**
  Membuktikan bahwa ciphertext Paillier $c = g^m r^n \bmod n^2$ dan komitmen Pedersen $C_{\text{ped}} = g_1^m h_1^s$ memuat nilai pesan rahasia $m$ yang identik:
  $$\text{PoPE}\{(m, s, r) : c = g^m r^n \bmod n^2 \;\land\; C_{\text{ped}} = g_1^m h_1^s\}$$
* Pola ini diadopsi dari kerangka kerja *Camenisch-Shoup Verifiable Encryption*, di mana relasi modular cross-group dibuktikan melalui protokol $\Sigma$ non-interaktif via Fiat-Shamir heuristic tanpa membebani R1CS sirkuit.

---

## 5. Rencana Tahapan Implementasi

1. **Sirkuit Circom (`DonationProof.circom`):**
   * Perbarui template sirkuit untuk menyertakan `ciphertext_hash` sebagai input publik.
   * Hubungkan sinyal `ciphertext_hash` ke dalam perhitungan `commitment`.
2. **Utilitas Hash & Proof Generation (`zk/scripts/` & Client):**
   * Buat helper hashing ciphertext berbasis chunk yang kompatibel dengan field BN254.
3. **Smart Contract (`DonationRegistry.sol`):**
   * Tambahkan parameter `ciphertextHash` pada fungsi pencatatan donasi dan validasi terhadap data `encryptedAmount`.
4. **Backend & Test Suite:**
   * Sesuaikan DTO dan validasi backend.
   * Buat pengujian negatif: submit proof sah dengan ciphertext yang dimodifikasi, dan verifikasi bahwa transaksi wajib ditolak.
