# Evaluasi Client-Side Encryption dan Pengelolaan Randomness

Dokumen ini menganalisis kelayakan teknis, arsitektur komputasi, dan pengelolaan keacakan (*randomness*) untuk menjalankan enkripsi Paillier dan pembuktian zk-SNARK sepenuhnya di sisi klien (*client-side browser*).

---

## 1. Urgensi Privasi: Eliminasi Server sebagai Trusted Party

Pada prototipe awal:
* Donatur mengirimkan nominal donasi dalam bentuk *plaintext* (`amount`) ke backend API.
* Server menjalankan fungsi `paillier.Encrypt(amount)` dan membangkitkan proof.
* **Kelemahan Model:** Server operator menjadi *trusted party* yang memiliki visibilitas total atas kontribusi finansial individual setiap donatur.

**Target Phase 4:**
Memindahkan seluruh eksekusi kriptografi privat ke peramban (browser) pengguna. Server backend dan database hanya menerima data terenkripsi dan bukti matematika:
$$\text{Payload} = \{ \text{campaign\_id}, \text{encrypted\_amount}, \text{commitment}, \text{ciphertext\_hash}, \text{proof} \}$$
Dengan arsitektur ini, backend berstatus **Zero-Knowledge** terhadap nilai nominal individual donatur ($m$).

---

## 2. Komputasi Enkripsi Paillier di Sisi Klien

Enkripsi Paillier memerlukan perhitungan:
$$c = g^m \cdot r^n \pmod{n^2}$$
dengan parameter:
* $n$: bilangan komposit 2048-bit ($n^2 \approx 4096\text{ bit}$).
* $g = n + 1$ (varian efisien Paillier): $g^m \equiv (1 + m \cdot n) \pmod{n^2}$, sehingga bagian ini hanya memerlukan **satu perkalian modular** sederhana.
* $r^n \bmod n^2$: eksponensiasi modular penuh dengan basis 2048-bit dan eksponen 2048-bit terhadap modulus 4096-bit.

### Analisis Kinerja JavaScript Modern:
1. **Dukungan Native `BigInt`:** Mesin JavaScript modern (V8, JavaScriptCore, SpiderMonkey) mendukung bilangan bulat arbitrer tanpa batas presisi.
2. **Algoritma Eksponensiasi Modular:**
   Dengan implementasi *binary exponentiation* (*square-and-multiply*) atau *Montgomery multiplication*:
   * Total operasi: $\approx 2048$ perkalian dan $2048$ pemangkatan dua modulo 4096-bit.
   * **Waktu eksekusi rata-rata:** $\mathbf{8\text{ ms} - 25\text{ ms}}$ pada CPU desktop/laptop standar, dan $\mathbf{\approx 40\text{ ms}}$ pada perangkat seluler.
3. **Dampak UI:** Eksekusi di bawah $50\text{ ms}$ dapat dijalankan langsung pada micro-task, atau didelegasikan ke **Web Worker** agar UI browser tidak mengalami *frame drop* (stutter).

---

## 3. Pengelolaan Randomness dan Entropi Kriptografis

Keamanan semantik Paillier (IND-CPA) dan sifat *hiding* dari komitmen Poseidon sangat bergantung pada kualitas keacakan nilai $r$ dan rahasia $s$.

### A. Sumber Entropi Wajib (*CSPRNG*)
* **Wajib:** Menggunakan Web Cryptography API: `window.crypto.getRandomValues(new Uint8Array(256))`.
  Sumber ini terhubung langsung ke CSPRNG kernel sistem operasi (`/dev/urandom` pada Unix/macOS atau `BCryptGenRandom` pada Windows).
* **Dilarang Keras:** Penggunaan `Math.random()` karena berbasis algoritma non-kriptografis deterministik (Xoroshiro128+) yang dapat diprediksi balik oleh penyerang.

### B. Distribusi Nilai Keacakan $r \in \mathbb{Z}_n^*$
1. **Uniform Sampling:**
   Nilai $r$ dibangkitkan sepanjang 2048 bit. Jika nilai acak $r \ge n$, lakukan *rejection sampling* (buang dan bangkitkan ulang) untuk mencegah *modulo bias*.
2. **Kondisi $\gcd(r, n) = 1$:**
   Karena $n = p \cdot q$ dengan $p, q$ adalah bilangan prima besar ($\approx 1024\text{ bit}$), peluang terpilihnya $r$ yang membagi $n$ adalah:
   $$\Pr[\gcd(r, n) \neq 1] = \frac{p + q - 1}{p \cdot q} \approx 2^{-1023}$$
   Peluang ini secara praktis bernilai $0$. Meskipun demikian, pemeriksaan $\gcd(r, n) == 1$ dapat tetap dijalankan via algoritma Euclidean biner sebagai langkah validasi defensif.

---

## 4. Pembangkitan zk-SNARK Witness dan Proof di Browser

Pembuatan proof di browser menggunakan pustaka `snarkjs` berbasis WebAssembly (WASM):

| Komponen | Spesifikasi Teknis | Ukuran Aset / Biaya |
|---|---|---|
| **Sirkuit** | `DonationProof.circom` (Range check + Poseidon + Ciphertext Hash) | $\approx 450$ R1CS constraints |
| **WASM Prover** | `DonationProof.wasm` | $\approx 1.2\text{ MB}$ (di-cache oleh browser) |
| **Proving Key** | `DonationProof_final.zkey` | $\approx 1.8\text{ MB}$ (di-cache oleh browser) |
| **Proving Time** | `snarkjs.groth16.fullProve()` di WebAssembly | $\mathbf{\approx 250\text{ ms} - 500\text{ ms}}$ |
| **Ukuran Proof** | 3 group elements ($A \in G_1, B \in G_2, C \in G_1$) | $\approx 256\text{ bytes}$ |

Dengan ukuran aset $< 3\text{ MB}$ dan waktu komputasi $< 0.5\text{ detik}$, pembuatan bukti ZK di browser donatur sangat praktis tanpa membutuhkan infrastruktur komputasi khusus.

---

## 5. Dampak Perubahan Skema API dan Basis Data

### A. Format Request Donasi Baru (`POST /api/donations`)
```json
{
  "campaign_id": "c1f24d77-6229-4c28-9721-a472a114704e",
  "encrypted_amount": "0x3a7f...[1024 hex chars]",
  "ciphertext_hash": "0x12ab...[field element hex]",
  "commitment": "0x2bc8...[poseidon hash hex]",
  "proof": {
    "pi_a": ["...", "..."],
    "pi_b": [["...", "..."], ["...", "..."]],
    "pi_c": ["...", "..."],
    "protocol": "groth16",
    "curve": "bn128"
  }
}
```
*Field `amount` dieliminasi total dari body request.*

### B. Isolasi Nilai Plaintext pada Basis Data
* Tabel `donations`:
  * Kolom `amount` dialihkan menjadi `NULLABLE` atau dihapus pada migrasi mendatang.
  * Kolom `encrypted_amount`, `ciphertext_hash`, dan `commitment` menjadi data primer yang direkam ke blockchain.
* Backend bertindak murni sebagai **Relayer Transaksi** dan **Pengelola Status**.

---

## 6. Vektor Risiko Client-Side dan Mitigasinya

1. **Cross-Site Scripting (XSS):**
   * *Risiko:* Skrip injeksi mencuri nilai $m$, $s$, atau $r$ saat donatur mengisi form.
   * *Mitigasi:* Kebijakan Content Security Policy (CSP) ketat, larangan inline scripts, dan audit berkala paket `node_modules`.
2. **Ketersediaan Memori & Worker Isolation:**
   * *Risiko:* Eksekusi WASM `snarkjs` membekukan UI form donasi.
   * *Mitigasi:* Menjalankan perhitungan `snarkjs` dan Paillier di dalam Dedicated Web Worker terpisah dari thread antarmuka.
3. **Integritas Public Key Paillier Kampanye:**
   * *Risiko:* Penyerang memanipulasi public key $n$ kampanye di frontend agar ciphertext dapat didekripsi oleh pihak ketiga.
   * *Mitigasi:* Nilai public key $n$ kampanye wajib diverifikasi langsung dari smart contract atau ditandatangani oleh operator resmi kampanye.
