# Canonical Record dan Rekonsiliasi

Dokumen ini mendefinisikan aturan canonical record, penanganan duplikasi, serta prosedur rekonsiliasi data donasi dan aggregate terenkripsi.

## 1. Definisi Canonical Record

Sebuah catatan donasi diklasifikasikan sebagai **canonical record** (sah dan berhak masuk ke aggregate) apabila memenuhi kriteria berikut:

1. **Proof zk-SNARK valid**: Memenuhi verifikasi Groth16 terhadap public inputs `campaign_max` (dari database kampanye) dan `commitment`.
2. **Ciphertext Paillier valid**: Nilai `encrypted_amount` merupakan ciphertext yang valid pada grup modulus Paillier kampanye.
3. **Bukti transaksi blockchain**: Memiliki `tx_hash` dengan receipt berstatus sukses (`status == 1`) pada kontrak `DonationRegistry` dan memancarkan event `DonationRecorded`.
4. **Keunikan komitmen**: Pasangan `(campaign_id, commitment)` bersifat unik. Tidak diperkenankan reuse commitment pada kampanye yang sama.

Catatan historis dari node Hardhat yang di-reset tetap diakui sebagai catatan sah masa lalu berdasarkan data snapshot yang tersedia, dan tidak diubah tanpa bukti pembatalan definitif.

## 2. Resolusi Konflik Duplikasi

Jika ditemukan lebih dari satu record dengan pasangan `(campaign_id, commitment)` yang sama:

1. **Record pemenang (canonical)**: Record dengan transaksi on-chain yang pertama kali berhasil di-mine (atau `created_at` terawal bila mined pada blok yang sama).
2. **Record duplikat (archived)**: Record selebihnya disalin ke tabel `donations_duplicate_archive` dan tidak boleh di-hard-delete.
3. Metadata pengarsipan wajib mencakup:
   - `archived_at`: Waktu pemindahan.
   - `archive_reason`: Alasan eksplisit (misal: `duplicate_commitment_replay`, `duplicate_race_condition`).
4. Status record di tabel utama `donations` diubah menjadi `archived` agar terisolasi dari perhitungan aggregate.

## 3. SOP Rekonsiliasi Aggregate Paillier

Agregasi homomorfik Paillier bersifat kumulatif perkalian ($E(m_{\text{total}}) = \prod E(m_i) \pmod{n^2}$). Rekonsiliasi dilakukan untuk menjamin nilai tersimpan sama dengan hasil perkalian donasi confirmed yang sah.

### Pemicu Rekonsiliasi
1. Audit berkala integritas data.
2. Pemulihan transaksi gantung pasca-kegagalan sistem/RPC (*recovery*).
3. Pemindahan record duplikat ke tabel arsip.

### Rumus Rekonsiliasi
$$\text{EncTotal}_{\text{reconciled}} = \prod_{d \in \text{Canonical Confirmed}} \text{EncAmount}_d \pmod{n^2}$$

Bila suatu kampanye belum memiliki donasi confirmed, aggregate diatur bernilai `0`.

### Alur Eksekusi
1. Kunci baris kampanye pada database (`SELECT id FROM campaigns WHERE id = $1 FOR UPDATE`).
2. Muat semua donasi dengan `status = 'confirmed'` untuk kampanye tersebut.
3. Lakukan perkalian homomorfik beruntun terhadap seluruh ciphertext donasi.
4. Bandingkan hasil rekonsiliasi dengan `encrypted_total` pada `campaign_aggregates`.
5. Bila terdapat perbedaan:
   - Catat selisih pada audit log.
   - Perbarui `encrypted_total` dan `updated_at` di tabel `campaign_aggregates`.

## 4. Kebijakan Audit Trail

Setiap aksi mutasi status donasi, pengarsipan record, dan rekonsiliasi aggregate wajib dicatat dalam log terstruktur dengan ketentuan:
- Mencatat: timestamp, tipe aksi, identifier record (`donation_id`, `campaign_id`, `tx_hash`), dan alasan perubahan.
- Dilarang mencatat: private key Paillier, kunci privat signer, JWT signature, atau plaintext nominal donasi.
