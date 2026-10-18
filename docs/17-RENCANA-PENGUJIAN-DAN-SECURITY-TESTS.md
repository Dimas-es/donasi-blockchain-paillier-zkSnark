# Rencana Pengujian dan Security Tests (Phase 5)

Dokumen ini memuat spesifikasi pengujian integrasi, End-to-End (E2E), dan pengujian keamanan (*security tests*) untuk membuktikan keandalan, integritas data, dan ketahanan sistem terhadap skenario serangan (*adversarial scenarios*).

---

## 1. Matriks Pengujian Sistem

| Kategori | Skenario Pengujian | Komponen Terlibat | Target Hasil |
|---|---|---|---|
| **Kriptografi** | Soundness verifikasi Groth16 | Verifier ZK & Circom | Proof valid lolos; proof salah atau sinyal termanipulasi ditolak. |
| **Kriptografi** | Enkripsi & agregasi Paillier | Paillier Engine | Agregasi aditif homomorfik akurat sesuai $\prod E(m_i) \bmod n^2$. |
| **Keamanan** | SEC-01: Range Violation | ZK Prover / Sirkuit | Donasi $m \le 0$ atau $m > \text{campaign\_max}$ ditolak pada pembentukan witness. |
| **Keamanan** | SEC-02: Public Signal Tampering | Verifier Backend & EVM | Mengubah `campaign_max` atau `commitment` menyebabkan proof invalid. |
| **Keamanan** | SEC-03: Replay Attack Defense | Database & Smart Contract | Commitment yang sudah ada ditolak oleh unique constraint dan contract guard. |
| **Keamanan** | SEC-04: Concurrent Race Condition | Donation Service & Repo | 10 request bersamaan dengan idempotency key yang sama hanya diproses 1 kali. |
| **Keandalan** | SEC-05: State Machine & Rekonsiliasi | DB State Machine & SOP | Status `confirmed` tidak bisa ditimpa; rekonsiliasi aggregate memulihkan inkonsistensi. |

---

## 2. Detail Skenario Security Tests

### SEC-01: Range Violation Attempt
* **Tujuan:** Membuktikan bahwa penyerang tidak dapat menghasilkan proof valid jika nominal donasi melanggar batasan rentang yang sah.
* **Vektor Uji:**
  * Kasus A: $m = 0$ (donasi nol).
  * Kasus B: $m = -10.000$ (donasi negatif).
  * Kasus C: $m = 2.000.000$ pada kampanye dengan batas maksimal $1.000.000$.
* **Hasil Diharapkan:** Pembangkitan witness/proof gagal dengan *constraint violation error*.

### SEC-02: Public Signal Tampering & Proof Forgery
* **Tujuan:** Membuktikan sifat *soundness* Groth16 bahwa memanipulasi sinyal publik (input publik) tanpa mengubah proof akan menggagalkan verifikasi.
* **Vektor Uji:**
  * Menggunakan proof sah $\pi$ dari donasi 100.000, tetapi mengubah `pubSignals[0]` (`campaign_max`) atau `pubSignals[1]` (`commitment`).
* **Hasil Diharapkan:** Verifier backend (`verifier.VerifyProof`) dan smart contract (`verifier.verifyProof`) mengembalikan nilai `false` atau melempar error verifikasi.

### SEC-03: Replay / Double-Submission Defense
* **Tujuan:** Menjamin donatur tidak dapat menggunakan proof dan komitmen yang sama untuk mengklaim donasi ganda.
* **Vektor Uji:**
  * Mengirim payload donasi yang sama dua kali berturut-turut dengan idempotency key berbeda.
* **Hasil Diharapkan:** Request kedua ditolak dengan pesan error duplikasi komitmen (*anti-replay guard*), dan transaksi kedua tidak dipancarkan ke blockchain.

### SEC-04: Idempotency Under Heavy Concurrency
* **Tujuan:** Menjamin ketahanan terhadap *race condition* saat jaringan tidak stabil dan pengguna melakukan multiple click / retry.
* **Vektor Uji:**
  * 10 goroutine secara bersamaan mengirim request donasi dengan payload dan `Idempotency-Key` yang identik.
* **Hasil Diharapkan:**
  * Tepat 1 eksekusi berhasil mengubah state dan memproses transaksi.
  * 9 eksekusi lainnya menerima respon ter-cache secara aman (HTTP 200/201).
  * Database hanya mencatat 1 baris donasi dan aggregate hanya bertambah 1 kali.

### SEC-05: State Machine Guard & Aggregate Reconciliation
* **Tujuan:** Memvalidasi bahwa kegagalan transient atau interupsi RPC tidak merusak konsistensi data.
* **Vektor Uji:**
  * Mencoba menimpa record berstatus `confirmed` kembali menjadi `pending` atau `failed`.
  * Menjalankan fungsi rekonsiliasi matematis untuk menyinkronkan tabel `campaign_aggregates` dengan seluruh donasi `confirmed` yang sah.
* **Hasil Diharapkan:** Transisi ilegal ditolak; aggregate terdekripsi persis sama dengan jumlah seluruh donasi sah.

---

## 3. Prosedur Eksekusi Automated Tests

Pengujian otomatis dijalankan melalui command test suite Go backend:
```bash
go test -v -run "TestSecurity|TestState|TestVerifier" ./internal/...
```
Semua hasil pengujian wajib bernilai **PASS** sebelum sistem memasuki tahap staging.
