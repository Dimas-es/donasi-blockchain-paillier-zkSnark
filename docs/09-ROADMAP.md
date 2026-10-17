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

**Status:** penelitian lanjutan.

- [x] Definisikan threat model dan properti privasi. (lihat docs/12-THREAT-MODEL-DAN-PRIVASI.md)
- [ ] Desain proof-to-ciphertext binding.
- [ ] Evaluasi client-side encryption dan pengelolaan randomness.
- [ ] Benchmark proof generation/verification serta Paillier.
- [ ] Tinjau keamanan kunci dan trusted setup.

**Exit criteria:** klaim kriptografi dibuktikan melalui desain, test, dan evaluasi yang dapat direproduksi.

## Phase 5 — Pengujian dan staging

**Status:** direncanakan.

- [ ] Integration/E2E/security tests.
- [ ] Observability, backup, recovery, staging.
- [ ] Evaluasi correctness, privacy, performance, reliability.
- [ ] Dokumentasi hasil eksperimen dan keterbatasan.

## Next step langsung

Item threat model dan properti privasi selesai didokumentasikan di `docs/12-THREAT-MODEL-DAN-PRIVASI.md`. Langkah selanjutnya adalah Phase 4 item kedua: **Desain proof-to-ciphertext binding**.

