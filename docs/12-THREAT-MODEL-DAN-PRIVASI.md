# Threat Model dan Properti Privasi

Dokumen ini mendefinisikan model ancaman (*threat model*), asumsi kepercayaan, properti keamanan dan privasi, serta landasan teori akademis untuk sistem donasi terdesentralisasi berbasis zk-SNARK dan Paillier Homomorphic Encryption.

---

## 1. Landasan Teori dan Literatur Pendukung

Perancangan protokol ini merujuk pada prinsip-prinsip kriptografi formal dan literatur *peer-reviewed*:

1. **Paillier Cryptosystem (EUROCRYPT 1999)**:
   *Pascal Paillier, "Public-Key Cryptosystems Based on Composite Degree Residuosity Classes"*.
   Membuktikan sifat aditif homomorfik $\text{Dec}(c_1 \cdot c_2 \bmod n^2) = (m_1 + m_2) \bmod n$ dan keamanan semantik **IND-CPA** di bawah asumsi *Decisional Composite Residuosity* (DCR). Menjadi dasar agregasi nominal donasi tanpa mendekripsi nilai individual.
2. **zk-SNARK Groth16 (EUROCRYPT 2016)**:
   *Jens Groth, "On the Size of Pairing-based Non-interactive Arguments"*.
   Menjamin efisiensi verifikasi on-chain (3 elemen kurva pairing $G_1, G_2$) serta membuktikan sifat *Computational Soundness* (pemalsu tidak dapat membuat bukti palsu) dan *Perfect Zero-Knowledge* (witness privat tidak bocor).
3. **Verifiable Encryption (CRYPTO 2003)**:
   *Jan Camenisch & Victor Shoup, "Practical Verifiable Encryption and Decryption of Discrete Logarithms"*.
   Fondasi pembuktian bahwa ciphertext mengenkripsi nilai yang memenuhi relasi atau batas tertentu tanpa membuka plaintext kepada verifier/server.
4. **Homomorphic Tallying & Validity Proofs (EUROCRYPT 1997 & FOSSACS 2001)**:
   *Ronald Cramer et al. (1997)* dan *Olivier Baudron et al. (2001)*.
   Preseden arsitektur yang mewajibkan bukti zero-knowledge untuk setiap input terenkripsi guna mencegah manipulasi agregat sebelum ciphertext dijumlahkan secara homomorfik.
5. **Privacy-Preserving On-Chain Verification (Financial Cryptography 2020)**:
   *Bünz et al., "Zether: Towards Privacy in a Smart Contract World"*.
   Membuktikan integrasi antara status terenkripsi, zero-knowledge range proof, dan ledger publik untuk auditabilitas transaksi privat.

---

## 2. Model Entitas dan Asumsi Kepercayaan (*Trust Assumptions*)

| Entitas | Peran | Asumsi Kepercayaan | Pengetahuan Data |
|---|---|---|---|
| **Donatur (Client)** | Pembuat donasi, generator proof | **Untrusted / Malicious**. Berpotensi memanipulasi nominal, me-replay proof, atau memalsukan ciphertext. | Memegang nominal $m$, secret $s$, commitment $C$, dan randomness enkripsi $r$. |
| **Backend Operator** | Orkestrator API, database, relayer transaksi | **Semi-Honest (*Honest-but-Curious*)**. Menjalankan protokol sesuai alur, namun berpotensi menganalisis nominal donatur. | **Prototipe saat ini:** menerima plaintext $m$.<br>**Target Phase 4:** *Zero-knowledge* terhadap nominal $m$. |
| **Blockchain / EVM** | Penyimpan ledger publik & verifier kontrak | **Trusted for Integrity, Untrusted for Privacy**. Mengeksekusi verifikasi deterministik; seluruh data on-chain dapat dibaca publik. | Membaca public inputs (`campaign_max`, `commitment`), status verifikasi ZK, ciphertext agregat, dan metadata transaksi. |
| **Key Custodian** | Pemegang private key Paillier kampanye | **Trusted for Threshold Decryption**. Hanya mendekripsi agregat akhir kampanye, bukan ciphertext individual. | Memegang kunci privat $(\lambda, \mu)$ atau share kunci desentralisasi. |
| **Public Observer** | Pihak ketiga di jaringan publik | **Malicious Passive / Active**. Mengamati ledger, event log, dan mempool untuk mengorbankan privasi donatur. | Hanya mengakses data publik on-chain dan event. |

---

## 3. Threat Model dan Vektor Serangan

Sistem dirancang untuk memitigasi vektor serangan berikut:

1. **Malicious Range Injection ($m \le 0$ atau $m > \text{campaign\_max}$)**
   * *Vektor Serangan:* Donatur mengirim nominal negatif (mengurangi agregat dana secara curang) atau nominal melebihi batas kampanye.
   * *Mitigasi:* Verifikasi on-chain Groth16 atas batasan sirkuit $0 < m \le \text{campaign\_max}$.
2. **Substitution / Mismatch Attack (Proof vs Ciphertext Mismatch)**
   * *Vektor Serangan:* Donatur atau backend jahat menghasilkan proof valid untuk nilai $m_1$, namun mengirim ciphertext Paillier dari nilai $m_2$ ($m_1 \neq m_2$).
   * *Mitigasi Target (Phase 4):* Pengikatan kriptografis antara witness ZK dan ciphertext Paillier (*proof-to-ciphertext binding*).
3. **Commitment Replay & Double Submission**
   * *Vektor Serangan:* Proof dan commitment yang sama dikirim berulang kali untuk menggandakan donasi tercatat.
   * *Mitigasi:* Pemetaan on-chain `commitments[hash]` dan unique constraint basis data `(campaign_id, commitment)`.
4. **Homomorphic Malleability Exploitation**
   * *Vektor Serangan:* Sifat homomorfik Paillier memungkinkan ciphertext dimanipulasi ($c' = c \cdot g^k \bmod n^2$) tanpa mendekripsi.
   * *Mitigasi:* Verifikasi bukti validitas dan konsistensi sebelum ciphertext digabungkan ke dalam agregat resmi.
5. **Traffic & Metadata Correlation Analysis**
   * *Vektor Serangan:* Penyerang publik menghubungkan pola waktu, alamat IP, atau identitas dompet dengan donasi individual.
   * *Mitigasi:* Pemisahan autentikasi akun, relayer submission dari backend, dan pengaburan identitas donatur melalui Poseidon commitment.

---

## 4. Definisi Properti Keamanan dan Privasi

### A. Properti Keamanan (*Security & Soundness*)

1. **Computational Soundness (zk-SNARK)**:
   Tidak ada penyerang dengan daya komputasi polinomial probabilistik (PPT) yang dapat membuat proof valid $\pi$ untuk pernyataan yang salah ($m \notin (0, \text{max}]$ atau $\text{Poseidon}(m, s) \neq C$), kecuali dengan probabilitas yang dapat diabaikan:
   $$\Pr[\mathcal{V}(\text{vk}, x, \pi) = 1 \mid (x, w) \notin \mathcal{R}] \le \text{negl}(\lambda)$$
2. **Additive Homomorphic Correctness**:
   Untuk setiap himpunan donasi sah $\{m_1, m_2, \dots, m_k\}$ dengan ciphertext Paillier $c_i = g^{m_i} r_i^n \bmod n^2$:
   $$\text{Dec}\left(\prod_{i=1}^k c_i \bmod n^2\right) = \sum_{i=1}^k m_i$$
3. **Idempotency & State Integrity**:
   Setiap transaksi hanya dieksekusi tepat satu kali per kunci idempotensi unik dan per komitmen. Status confirmed bersifat permanen dan tidak dapat ditimpa oleh kegagalan transient.

### B. Properti Privasi (*Privacy & Confidentiality*)

1. **IND-CPA Confidentiality (Paillier)**:
   Ciphertext $c$ memiliki sifat *indistinguishability under chosen-plaintext attack*. Bagi penyerang publik tanpa kunci privat:
   $$|\Pr[\mathcal{A}(c_0) = 1] - \Pr[\mathcal{A}(c_1) = 1]| \le \text{negl}(\lambda)$$
2. **Zero-Knowledge Property (Groth16)**:
   Proof $\pi$ tidak membocorkan informasi apa pun mengenai witness privat $(m, s)$. Terdapat simulator berwaktu polinomial $\mathcal{S}$ yang dapat menghasilkan proof indistinguishable dari proof nyata tanpa mengetahui witness.
3. **Commitment Hiding & Binding (Poseidon)**:
   - *Hiding:* Diberikan $C = \text{Poseidon}(m, s)$, secara komputasi tidak mungkin menemukan $(m, s)$.
   - *Binding:* Mustahil menemukan $(m', s') \neq (m, s)$ sedemikian rupa sehingga $\text{Poseidon}(m', s') = C$.
4. **Aggregate Privacy & Unlinkability**:
   Dekripsi hanya dilakukan pada akhir kampanye atas nilai agregat $\sum m_i$. Nominal donasi individual $m_i$ tetap terenkripsi dan tidak dapat diuraikan oleh pengamat publik.

---

## 5. Analisis Kesenjangan (*Gap Analysis*) Prototipe vs Target Phase 4

| Dimensi | Status Prototipe Saat Ini | Target Akhir Phase 4 |
|---|---|---|
| **Rentang Validitas Nominal** | Terpenuhi via Groth16 verifier | Dipertahankan |
| **Pencegahan Replay/Duplikasi** | Terpenuhi via DB constraint & on-chain mapping | Dipertahankan |
| **Agregasi Homomorfik** | Terpenuhi via perkalian ciphertext $\bmod n^2$ | Dipertahankan |
| **Proof-to-Ciphertext Binding** | **Belum Terpenuhi** (Ciphertext dienkripsi independen dari witness sirkuit) | Pengikatan matematis antara ZK proof dan ciphertext |
| **Privasi terhadap Backend** | **Belum Terpenuhi** (Backend menerima nominal plaintext) | Client-side encryption & client-side proof generation |
| **Key Management** | Kunci privat tunggal di server lokal | Threshold Paillier atau distributed key generation (DKG) |
