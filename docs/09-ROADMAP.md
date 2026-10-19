# Roadmap Pengembangan

## Phase 1 — Fondasi backend dan kriptografi

**Status:** pengujian awal selesai.  
Cakupan: auth, campaign, Paillier, circuit dan Groth16, smart contract, API donasi, aggregate, E2E happy path.

## Phase 2 — Integritas data dan reliability

**Status:** selesai diuji.

- [x] Investigasi duplicate historis.
- [x] Backup database sebelum perbaikan.
- [x] Migration 000005 membuat tabel archive.
- [x] Verifikasi isi tabel archive dan rencana reconciliation.
- [x] Tetapkan canonical record dengan bukti yang memadai.
- [x] Pertahankan audit trail dan rekonsiliasi aggregate bila diperlukan.
- [x] Terapkan idempotency key pada database dan service (migration 000006).
- [x] Terapkan state machine yang aman.
- [x] Implementasikan retry dan recovery transaksi blockchain.
- [x] Uji duplicate, concurrency, kegagalan DB/RPC, dan aggregate.

**Exit criteria:** retry tidak menggandakan donasi; status dan aggregate dapat direkonsiliasi; bukti historis tetap terpelihara.

## Phase 3 — Frontend MVP

**Status:** MVP selesai untuk demo lokal.

- [x] Login dan registrasi.
- [x] Daftar/detail campaign.
- [x] Form donasi (generate proof via API + submit).
- [x] Status transaksi dan riwayat donasi.
- [x] Ringkasan aggregate (termasuk dekripsi demo di backend).

**Exit criteria:** pengguna menyelesaikan happy path tanpa terminal/API client.

## Phase 4 — Penguatan protokol kriptografi

**Status:** selesai dirumuskan dan dievaluasi.

- [x] Definisikan threat model dan properti privasi. (lihat docs/12-THREAT-MODEL-DAN-PRIVASI.md)
- [x] Desain proof-to-ciphertext binding. (lihat docs/13-PROOF-TO-CIPHERTEXT-BINDING.md)
- [x] Evaluasi client-side encryption dan pengelolaan randomness. (lihat docs/14-EVALUASI-CLIENT-SIDE-ENKRIPSI.md)
- [x] Benchmark proof generation/verification serta Paillier. (lihat docs/15-BENCHMARK-KRIPTOGRAFI.md)
- [x] Tinjau keamanan kunci dan trusted setup. (lihat docs/16-TINJAUAN-KEAMANAN-KUNCI-DAN-TRUSTED-SETUP.md)

**Exit criteria:** klaim kriptografi dibuktikan melalui desain, test, dan evaluasi yang dapat direproduksi.

## Phase 5 — Pengujian dan staging

**Status:** Selesai 100%.

- [x] Integration/E2E/security tests. (lihat docs/17-RENCANA-PENGUJIAN-DAN-SECURITY-TESTS.md dan backend/internal/donation/security_test.go)
- [x] Observability, backup, recovery, staging. (lihat docs/18-OBSERVABILITY-BACKUP-RECOVERY-STAGING.md)
- [x] Evaluasi correctness, privacy, performance, reliability. (lihat docs/19-EVALUASI-SISTEM-4-PILAR.md)
- [x] Dokumentasi hasil eksperimen dan keterbatasan. (lihat docs/20-HASIL-EKSPERIMEN-DAN-KETERBATASAN.md)

## Status Keseluruhan Proyek

Seluruh tahapan pengembangan dari Phase 1 hingga Phase 5 telah selesai diimplementasikan, diverifikasi, dan didokumentasikan secara komprehensif, mencakup arsitektur backend, frontend MVP, protokol kriptografi (zk-SNARK & Paillier), smart contract, integritas data/reliability, serta evaluasi keterbatasan akademik.


