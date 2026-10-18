# Observability, Backup, Recovery, dan Staging

Dokumen ini mendefinisikan standar operasional sistem untuk observabilitas (*logging* & metrik), prosedur pencadangan (*backup*), protokol pemulihan bencana (*disaster recovery*), dan arsitektur lingkungan *staging*.

---

## 1. Arsitektur Observabilitas (*Logging* dan Metrik)

Sistem menerapkan observabilitas berlapis untuk melacak status transaksi terdistribusi antara API, PostgreSQL, dan Blockchain tanpa mengorbankan privasi pengguna.

### A. Kebijakan Redaksi Data Sensitif (*Zero-Leak Logging*)
Log sistem dilarang keras mencatat material sensitif:
* **DILARANG:** Kunci privat Paillier $(\lambda, \mu)$, private key EVM relayer, password/hash JWT, secret komitmen $s$, randomness Paillier $r$, dan nominal plaintext donatur (pada mode zero-knowledge).
* **DIIZINKAN:** `donation_id` (UUID), `campaign_id` (UUID), `tx_hash`, `idempotency_key`, durasi eksekusi (`elapsed_ms`), kode status HTTP, dan pesan error terstruktur.

### B. Format Log Terstruktur (JSON)
Seluruh log operasional dipancarkan dalam format terstruktur:
```json
{
  "timestamp": "2026-10-17T13:40:00Z",
  "level": "INFO",
  "service": "donation-service",
  "action": "RECORD_TRANSACTION",
  "donation_id": "c1f24d77-6229-4c28-9721-a472a114704e",
  "campaign_id": "f5a8b291-3810-410a-b283-cf2987102931",
  "tx_hash": "0x4b78c92a...",
  "status_from": "pending",
  "status_to": "submitted",
  "latency_ms": 142
}
```

### C. Metrik Kesehatan Sistem (*Health & Readiness Checks*)
Backend menyediakan endpoint diagnostik:
* `GET /healthz`: Memeriksa konektivitas proses backend.
* `GET /readyz`: Memeriksa koneksi pool PostgreSQL, ketersediaan RPC node blockchain, dan kesiapan key manager Paillier.

---

## 2. Strategi Pencadangan (*Backup & Snapshots*)

Pencadangan dilakukan secara berkala dan sebelum eksekusi migrasi skema baru.

### A. Pencadangan Basis Data PostgreSQL
1. **Jadwal & Retensi:**
   * Snapshot harian otomatis (*daily snapshot*) dengan retensi 30 hari.
   * Format pencadangan: Custom compressed format via `pg_dump -Fc`.
2. **Perintah Pencadangan:**
   ```bash
   pg_dump -U postgres -d zk_paillier_donation -Fc -f "backups/backup_$(date +%Y%m%d_%H%M%S).dump"
   ```
3. **Prioritas Tabel Audit:**
   Tabel `donations_duplicate_archive` dan `donations` wajib dipelihara secara utuh dan tidak boleh dihapus selama siklus pencadangan.

### B. Pencadangan State Blockchain
* Pada jaringan pengembangan (Hardhat): Riwayat blok bersifat volatil. Sebelum restart node, snapshot state dapat diekspor melalui script dump kontrak.
* Pada jaringan publik/testnet: Seluruh state kontrak `DonationRegistry` tercatat permanen pada ledger terdistribusi dan dapat diindeks ulang (*re-indexed*) melalui pembacaan event log `DonationRecorded`.

---

## 3. Protokol Pemulihan Bencana (*Disaster Recovery & Reconciliation*)

### A. Penanganan Transaksi Menggantung (*Stuck Submitted Transactions*)
Jika transaksi terhenti pada status `submitted` akibat gangguan RPC atau timeout jaringan:
1. Scanner latar belakang mengidentifikasi donasi `submitted` yang berumur $> 5\text{ menit}$.
2. Query receipt transaksi on-chain via `eth_getTransactionReceipt(tx_hash)`:
   * Jika receipt sukses (`status == 1`): Transisi status ke `confirmed`.
   * Jika receipt gagal (`status == 0`): Transisi status ke `failed`.
   * Jika transaksi tidak ditemukan: Lakukan *resubmit* atau batalkan status dengan log audit.

### B. Prosedur Rekonsiliasi Aggregate (*Automated Aggregate Reconciliation*)
Jika terjadi selisih antara `encrypted_total` dengan penjumlahan riil:
1. Kunci baris kampanye pada database (`SELECT ... FOR UPDATE`).
2. Jalankan perkalian homomorfik Paillier kumulatif atas seluruh donasi sah:
   $$\text{EncTotal}_{\text{reconciled}} = \prod_{d \in \text{Canonical Confirmed}} \text{EncAmount}_d \bmod n^2$$
3. Perbarui `campaign_aggregates` dan catat riwayat rekonsiliasi.
4. Tool CLI pemulihan:
   ```bash
   go run ./cmd/inspect-db -reconcile
   ```

---

## 4. Kriteria Kesiapan Lingkungan Staging (*Staging Readiness*)

Lingkungan staging difungsikan untuk mereplikasi kondisi produksi nyata:

| Komponen | Konfigurasi Lingkungan Lokal (Dev) | Konfigurasi Lingkungan Staging |
|---|---|---|
| **Blockchain** | Hardhat Local Node (Chain ID 31337) | Ethereum Testnet publik (Sepolia / Arbitrum Sepolia) |
| **Database** | PostgreSQL lokal tanpa SSL | PostgreSQL Cloud (AWS RDS / Supabase) dengan `sslmode=require` |
| **Backend** | Go run lokal via terminal | Kontainer Docker terisolasi dengan non-root user |
| **Frontend** | Vite dev server (`http://localhost:5173`) | Production bundle statis di-hosting via HTTPS (Vercel/Cloudflare) |
| **Key Custody** | File lokal `.env` / directory `keys/` | Secret Manager (AWS Secrets Manager / Doppler) |
| **RPC Endpoint** | `http://127.0.0.1:8545` | Dedicated RPC Provider (Alchemy / Infura) dengan rate-limiting |
