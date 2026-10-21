# Naskah Publikasi Ilmiah Jurnal SIMASI (TrustGive)

Folder ini berisi berkas naskah artikel ilmiah publikasi untuk **JURNAL SIMASI** (*Jurnal Ilmiah Sistem Informasi*, LPPM Universitas Bina Bangsa, p-ISSN: 2798-835X, e-ISSN: 2798-8341) yang disusun secara presisi mengikuti template resmi [`assets/template/TEMPLATE SIMASI CONTOH.docx`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/template/TEMPLATE%20SIMASI%20CONTOH.docx) dan panduan aturan [`assets/template/rules_template.md`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/template/rules_template.md).

---

## 1. Berkas Utama Artikel Ilmiah

| Nama Berkas | Format | Keterangan Dokumen |
|---|:---:|---|
| [`JURNAL_SIMASI_TRUSTGIVE.docx`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx) | **DOCX (Word)** | **Berkas Final Siap Submit**. Memuat kop resmi SIMASI dengan logo SIMASI dan UNISBA, tipografi Times New Roman presisi (14 pt Judul, 12 pt Isi spasi 1.5, First Line Indent 1.0 cm, Margin 2.54 cm all sides), 7 diagram gambar resolusi tinggi (300 DPI), 3 tabel evaluasi ilmiah, serta 28 daftar pustaka format APA 7th Style (hanging indent 1.0 cm). |
| [`NASKAH_JURNAL_SIMASI.md`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/jurnal/NASKAH_JURNAL_SIMASI.md) | **Markdown** | Naskah teks lengkap bahasa Indonesia & Inggris untuk dokumentasi repositori, penelaahan teks cepat, dan sinkronisasi Git. |
| [`simasi.png`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/jurnal/simasi.png) | **PNG** | Logo resmi Jurnal SIMASI (LPPM Universitas Bina Bangsa) pada kop halaman pertama sebelah kiri. |
| [`unisba.png`](file:///c:/Users/dimaa/Documents/blockchain/zk-paillier-donation-system/assets/jurnal/unisba.png) | **PNG** | Logo resmi Universitas Islam Bandung (UNISBA) pada kop halaman pertama sebelah kanan. |

---

## 2. Identitas Naskah

- **Judul Artikel (Indonesia):**  
  **PENGEMBANGAN DAN EVALUASI KINERJA SISTEM DONASI TERDESENTRALISASI DENGAN AGREGASI HOMOMORFIK PAILLIER DAN ZK-SNARK**
- **Title (English):**  
  **DEVELOPMENT AND PERFORMANCE EVALUATION OF A DECENTRALIZED DONATION SYSTEM USING PAILLIER HOMOMORPHIC AGGREGATION AND ZK-SNARKS**
- **Penulis & Afiliasi:**  
  1. Dimas Setiawan (Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi)  
  2. Alam Rahmatulloh (Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi)
- **Korespondensi:** `dimaasadjy@gmail.com`, `alam@unsil.ac.id`

---

## 3. Struktur Dokumen dan Aset Tersemat

### A. Tabel Data Ilmiah (Judul di ATAS Tabel, Rata Tengah, Font 10 pt)
1. **Tabel 1. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat**  
   - Menampilkan perbandingan gas untuk *deployment* verifier (~594k gas), registri donasi (~887k gas), konfigurasi pagu kampanye (~46k gas), dan fungsi `recordDonation` dengan verifikasi Groth16 on-chain (**243.518 gas**).
2. **Tabel 2. Evaluasi Waktu Komputasi Kriptografi (Paillier & zk-SNARK)**  
   - Menampilkan waktu latensi komputasi *keygen* Paillier 2048-bit (42,5 ms), enkripsi nominal (2,4 ms), perkalian modular agregasi homomorfik (**0,015 ms**), *witness generation* (185 ms), pembentukan bukti Groth16 SnarkJS (~1.350 ms), dan verifikasi *pairing* off-chain Go (~1.850 ms via subprocess).
3. **Tabel 3. Matriks Hasil Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan Sistem**  
   - Menampilkan pengujian empiris berimbang (13 skenario): 9 skenario fungsional & reliabilitas berhasil (**PASS**), serta 4 skenario pemetaan batasan/celah keamanan yang jujur (**BELUM TERPENUHI / KETERBATASAN** mencakup *Proof-to-Ciphertext Binding Gap*, *Plaintext to Backend*, *Hardhat Node Reset*, dan *In-Memory Rate Limiting*).

### B. Gambar dan Diagram (Judul di BAWAH Gambar, Rata Tengah, Font 12 pt, Format: **Gambar X.** Keterangan)
1. **Gambar 1.** Arsitektur Hibrida Sistem Donasi Terdesentralisasi TrustGive (Metode Penelitian - 2.1)
2. **Gambar 2.** Skema Agregasi Aditif Homomorfik Paillier (AHE) (Metode Penelitian - 2.2)
3. **Gambar 3.** Struktur Constraint Sirkuit ZK-SNARK Pembuktian Donasi (Circom) (Metode Penelitian - 2.3)
4. **Gambar 4.** Diagram Relasi Entitas (ERD) Model Data Sistem (Hasil dan Pembahasan - 3.1)
5. **Gambar 5.** Diagram Alur Transaksi Donasi Konfidensial End-to-End (Hasil dan Pembahasan - 3.2)
6. **Gambar 6.** Siklus Hidup dan Status Kampanye Donasi (Hasil dan Pembahasan - 3.3)
7. **Gambar 7.** Alur Logika Idempotensi dan Rekonsiliasi State Transaksi (Hasil dan Pembahasan - 3.4)

### C. Analisis Keterbatasan & Batas Privasi (Phase 4 Roadmap)
Naskah menyajikan analisis kritis sesuai prinsip integritas akademik:
- Keterbatasan prototipe saat ini di mana backend bertindak sebagai *honest-but-curious server* yang menerima nominal plaintext.
- Tantangan *Proof-to-Ciphertext Binding* (sirkuit ZK membuktikan komitmen Poseidon dan rentang nominal, namun belum mengikat secara kriptografis ke *ciphertext* Paillier).
- Tiga arah solusi ilmiah Fase 4: Opsi A (*public input ciphertext digest*), Opsi B (*verifiable encryption* SAVER - *Lee et al., 2019*), dan Opsi C (*deterministic audit logging*).
- Roadmap mitigasi sentralisasi kunci privat melalui arsitektur *Threshold Paillier* (*Dewangan & Msahli, 2026*).

### D. Daftar Pustaka (APA 7th Style, Urut A–Z, Hanging Indent 1.0 cm)
Memuat 28 referensi ilmiah terkini (fokus 2020–2026) dari USENIX Security, IEEE S&P, IEEE TDSC, Elsevier, Springer, Dagstuhl LIPIcs, dan IACR ePrint dengan tautan DOI/URL aktif.

---

## 4. Skrip Pembuat Dokumen Otomatis

Untuk memperbarui atau meregenerasi dokumen Word sewaktu-waktu:
```bash
python scripts/generate_jurnal_docx.py
```
Skrip ini membaca template dasar, menyalin layout dan border kop asli, memperbarui logo, mengaplikasikan section margin 2.54 cm dan running footer penomoran halaman, lalu merakit naskah dan gambar secara otomatis.
