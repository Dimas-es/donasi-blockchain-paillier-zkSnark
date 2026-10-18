# Tinjauan Keamanan Kunci dan Trusted Setup

Dokumen ini menyajikan analisis keamanan menyeluruh terhadap material kunci kriptografi, siklus hidup parameter rahasia, serta prosedur *trusted setup* zk-SNARK dan Paillier pada sistem donasi terdesentralisasi.

---

## 1. Keamanan Kunci Kriptosistem Paillier

Kriptosistem Paillier menggunakan sepasang kunci:
* **Kunci Publik:** Modulus $n = p \cdot q$ dan generator $g \in \mathbb{Z}_{n^2}^*$.
* **Kunci Privat:** Parameter $(\lambda, \mu)$ dengan $\lambda = \text{lcm}(p-1, q-1)$ dan $\mu = (L(g^\lambda \bmod n^2))^{-1} \bmod n$.

### A. Analisis Risiko Prototipe Saat Ini
1. **Single Point of Failure & Compromise:**
   Pada implementasi MVP, kunci privat disimpan pada filesystem lokal server backend. Jika server disusupi, penyerang dapat mendekripsi seluruh ciphertext donasi masa lalu secara sepihak.
2. **Ketergantungan pada Integritas Operator:**
   Donatur harus mempercayai bahwa operator tidak menyalahgunakan kunci privat untuk mengintip nominal sebelum waktu penutupan kampanye.

### B. Arsitektur Mitigasi Jangka Panjang

```
             +---------------------------------------+
             |            Donation System            |
             +---------------------------------------+
                                 |
                                 v
               Ciphertext Total: Enc(Total) mod n^2
                                 |
        +------------------------+------------------------+
        |                        |                        |
        v                        v                        v
+---------------+        +---------------+        +---------------+
|   Trustee A   |        |   Trustee B   |        |   Trustee C   |
| (Auditor Org) |        | (Foundation)  |        |  (Community)  |
|  Share sk_1   |        |  Share sk_2   |        |  Share sk_3   |
+---------------+        +---------------+        +---------------+
        |                        |                        |
        +------------------------+------------------------+
                                 |
                                 v
                   Threshold Decryption Combine (k-of-n)
                                 |
                                 v
                     Plaintext Total Terverifikasi
```

1. **Threshold Paillier Cryptosystem (Fouque, Poupard, Stern 2000):**
   * Kunci privat dibagi menjadi $n$ pecahan (*shares*) menggunakan skema $(k, n)$-threshold sharing (misal: $2\text{ dari }3$ atau $3\text{ dari }5$).
   * Pihak pemegang kunci (*Trustees*): Pengelola kampanye, auditor independen, dan perwakilan donatur.
   * Tidak ada satu pihak pun yang memegang kunci utuh. Dekripsi hanya dapat dilakukan jika minimal $k$ pihak menghasilkan *partial decryption proofs* yang sah.
2. **Isolasi Kunci per Kampanye (*Per-Campaign Keypairs*):**
   * Setiap kampanye donasi wajib memiliki pasangan kunci Paillier independen.
   * Kompromi kunci pada satu kampanye terisolasi dan tidak berdampak pada kampanye lainnya.
3. **Penyimpanan Terproteksi (*Hardware Security Module / KMS*):**
   * Pada tahap staging/produksi, private key wajib dienkripsi saat diam (*at-rest*) menggunakan AWS KMS, HashiCorp Vault, atau HSM fisik berstandar FIPS 140-2 Level 3.

---

## 2. Keamanan Trusted Setup zk-SNARK Groth16

Protokol Groth16 menawarkan ukuran bukti paling ringkas (3 elemen grup kurva eliptik) dan verifikasi on-chain termurah di EVM, namun memerlukan **Circuit-Specific Trusted Setup**.

### A. Risiko Kritis: *Toxic Waste*
Selama proses pembentukan proving key (`.zkey`) dan verification key (`verification_key.json`), dibangkitkan parameter rahasia skalar:
$$\text{Toxic Waste} = (\alpha, \beta, \gamma, \delta, x) \in \mathbb{F}_r^5$$

* **Dampak Kebocoran:**
  Jika nilai-nilai skalar ini tidak dihancurkan (*not securely destroyed*), pihak yang mengetahuinya dapat membuat **pembuktian palsu (*fake proof*) yang valid** untuk pernyataan matematika apa pun tanpa mengetahui witness asli.
* **Konsekuensi Sistem Donasi:**
  Penyerang dapat membuat transaksi donasi fiktif atau meloloskan nominal di luar batas kampanye ($m > \text{campaign\_max}$) tanpa terdeteksi oleh verifier smart contract.

### B. Metodologi Trusted Setup Aman (*MPC Ceremony*)

Untuk menjamin *soundness*, trusted setup dibagi menjadi 2 fase terstruktur:

1. **Fase 1: Powers of Tau (Universal Setup):**
   * Upacara multi-partisipan (*Multi-Party Computation* / MPC) global.
   * Proyek menggunakan file standar komunitas terverifikasi (`pot12_final.ptau`) yang telah melalui upacara MPC dengan ratusan partisipan terpercaya (Ethereum Community Tau Ceremony).
2. **Fase 2: Circuit-Specific Ceremony (`DonationProof`):**
   * Upacara kontribusi acak khusus sirkuit donasi.
   * Prinsip Keamanan Matematika:
     $$\text{Sistem Aman} \iff \text{Minimal 1 Partisipan Menghancurkan Nilai Rahasianya}$$
   * Setiap partisipan menambahkan entropi ke file `.zkey` secara berurutan dan mempublikasikan *cryptographic transcript* (hash kontribusi) yang dapat diaudit publik.
   * Kontribusi terakhir disegel dengan *Random Beacon* publik (misalnya hash blok Bitcoin atau Ethereum pada ketinggian tertentu) untuk mencegah serangan front-running/last-actor manipulation.

### C. Analisis Alternatif: Sistem Proof Tanpa Trusted Setup Spesifik

| Sistem ZK | Kebutuhan Trusted Setup | Toxic Waste | Ukuran Proof | Biaya Gas Verifikasi EVM | Status Evaluasi |
|---|---|---|---|---|---|
| **Groth16 (Saat Ini)** | **Per-circuit Setup** | **Ada** | **~256 bytes** | **~215.000 gas** | **Dipilih untuk MVP & Riset (Paling Efisien On-Chain)** |
| **PLONK** | Universal Setup (sekali saja) | Ada (di Fase 1 saja) | ~500 bytes | ~300.000 gas | Alternatif jika sirkuit sering berubah |
| **Halo2 / Bulletproofs** | **Transparent (Tanpa Setup)** | **Tidak Ada** | ~1.5 - 5 KB | Sangat mahal di EVM ($> 1.000.000$ gas) | Kurang ideal untuk smart contract L1 |

---

## 3. Manajemen Kunci Operasional Sistem

Selain kunci kriptografi matematika, sistem memiliki dua kategori kunci operasional:

### A. Kunci Penandatangan EVM (*Relayer Private Key*)
* **Peran:** Menandatangani transaksi `recordDonation` saat backend melakukan relay dari client ke smart contract.
* **Mitigasi:**
  * Alamat relayer tidak memegang hak istimewa administratif pada smart contract (`onlyOwner` dipisahkan ke cold wallet multi-sig).
  * Batasi saldo ETH/gas pada hot wallet relayer ke ambang operasional minimum (misal untuk 50–100 transaksi).
  * Implementasi monitoring otomatis: peringatan jika saldo di bawah ambang batas atau frekuensi transaksi melonjak tidak wajar.

### B. Rahasia Autentikasi JWT
* **Peran:** Melindungi sesi login pengguna dan donatur terdaftar.
* **Mitigasi:**
  * Migrasi dari simetris (HS256) ke asimetris (RS256/ES256) sehingga backend worker hanya memegang public key untuk validasi token.
  * Terapkan masa berlaku token pendek (15–30 menit) disertai *refresh token rotation*.

---

## 4. Kesimpulan Rekomendasi Keamanan

1. **Untuk Prototipe Penelitian Saat Ini:**
   Setup Groth16 yang dihasilkan snarkjs dengan universal Powers-of-Tau (`pot12`) sudah memadai untuk membuktikan kebenaran matematis prototipe dan benchmark kinerja.
2. **Keterbatasan yang Wajib Diungkapkan pada Laporan/Paper:**
   Sistem prototipe masih menggunakan *single-party setup* untuk Fase 2 dan *single private key* Paillier di backend; implementasi produksi wajib beralih ke *Threshold Paillier* dan *Phase 2 MPC Ceremony*.
