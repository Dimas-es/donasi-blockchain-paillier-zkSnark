Saya mulai dengan membaca kedua file lampiran, lalu repositori GitHub branch `dev`.

Naskah sudah terbaca penuh. Sekarang template SIMASI.

Isi kedua dokumen sudah saya baca. Selanjutnya saya periksa format fisik docx (margin, kolom, font, gambar, jumlah halaman) untuk perbandingan dengan template.

Naskah 17 halaman. Sekarang repositori branch `dev`.

Repo berhasil di-clone (branch `dev`, 1 commit). Saya lihat sisa daftar file dan stack teknologinya.

Skrip gas hanya mengukur `recordDonation` (payload 22-byte, 512-byte, dan 1233-byte) dan `verifyProof.estimateGas`. Saya telusuri apakah angka-angka lain di Tabel 3 dan 4 punya sumber di repo.

Angka Tabel 3 dan 4 hanya muncul di skrip penghasil naskah dan generator grafik (di-hardcode), bukan di log pengukuran. Saya cek `generate_charts.py`, benchmark Paillier, dan dokumen revisi.

Skema nyata: **4 entitas** utama (+ tabel arsip duplikasi); `idempotency_key` hanyalah kolom pada `donations`, bukan entitas `idempotency_keys` seperti di naskah. Saya cek tes yang mendasari Tabel 5.

Implementasi Paillier sendiri benar secara fungsional. Saya cek bagaimana ciphertext dikemas ke kontrak (menentukan gas riil sistem) dan penyimpanan kunci privat.

Kontrak/backend tidak memiliki `finalize`, `withdraw`, `createCampaign`, `donateVerify`, `donateOptimized`, `payable`, atau audit log. Sekarang aturan template dan perbandingan visual halaman.

Header (Vol/No/DOI/“hal. 1-14”) disalin apa adanya dari template. Saya periksa ukuran font tabel, spasi, jumlah kata abstrak, dan format sitasi secara terprogram.

Semua 27 referensi tersitir di teks. Sekarang saya periksa isi gambar (arsitektur, ERD, grafik gas) karena itu yang langsung dibandingkan dengan repo.

Gambar 1 sendiri menyebut **Go Gin** (teks naskah: "Go Fiber") dan tampaknya menyebut enkripsi *client-side* dan *anti-replay on-chain*. Saya perbesar untuk membaca persis.

Gambar 1 menyebut enkripsi *client-side*, *anti-replay on-chain*, dan "tabel Idempotency Keys", yang semuanya bertentangan dengan kode. Saya lihat halaman ERD dan grafik gas.

Saya sudah memeriksa naskah, template, dan repositori branch `dev`. Laporan ini hanya memuat yang benar-benar saya baca atau jalankan. Hal yang tidak sempat saya periksa ada di akhir.

**Kesimpulan awal:** naskah belum layak disubmit, dan rekomendasi saya **Major Revision**. Banyak klaim implementasi di naskah tidak ada di kode, sebagian besar angka Tabel 3 dan 4 tidak punya sumber pengukuran di repositori, dan klaim keamanan lebih kuat daripada yang dibuktikan implementasi. Bagian keterbatasan di naskah jujur, tetapi bagian lain mengontradiksinya.

Naskah yang Anda unggah identik byte-per-byte (SHA-256 sama) dengan `assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx` di branch `dev`, commit `8ae35e6` ("nyusun jurnal"), satu-satunya commit. Repositori ini bisa di-clone tanpa login, jadi reviewer bisa memeriksanya seperti yang saya lakukan.

## A. Ringkasan penelitian dan kontribusi yang diklaim

TrustGive adalah prototipe donasi berbasis Ethereum. Nominal dienkripsi Paillier off-chain dan diagregasi dengan perkalian ciphertext. Keabsahan nominal (positif dan ≤ pagu) dibuktikan dengan Groth16 di BN254 dan diverifikasi kontrak. Tiga kontribusi diklaim: arsitektur 3-layer dengan pola idempotensi dan rekonsiliasi, evaluasi gas dan latensi, serta pemetaan batasan keamanan. Ada tiga RQ: arsitektur hibrida, profil gas/latensi, dan verifikasi audit total tanpa membuka nominal individual.

## B. Penilaian awal

Topiknya relevan dan masalahnya nyata. Namun hasilnya tidak bisa dipertahankan di hadapan reviewer yang membuka repositori. Jalur perbaikan paling murah adalah menyelaraskan naskah dengan kode yang ada, bukan sebaliknya. Jika temuan Kritis di bawah tidak diselesaikan, saya akan merekomendasikan Reject.

## C. Substansi ilmiah

- **Kebaruan:** kombinasi HE dan zk-SNARK pada smart contract sudah ada (ZeeStar, Cloak, yang Anda sitasi sendiri). Kontribusi di sini hanya implementasi prototipe dan angka gas. Itu tipis, apalagi tiga properti utamanya (privasi terhadap operator, keterikatan proof-ciphertext, total yang dapat diaudit) belum tercapai.
- **Pemilihan Paillier tidak dijustifikasi.** Modulus 2048-bit tidak cocok dengan field SNARK, dan ciphertext hanya disimpan sebagai blob di kontrak. Reviewer akan bertanya mengapa tidak memakai komitmen Pedersen atau EC-ElGamal, yang menyatu dengan SNARK dan menjaga sifat aditif on-chain. Naskah tidak membahasnya.
- **Tabel 1:** estimasi gas pembanding (UpHaaR ~45.000, Astraea >1.200.000, He et al. ~120.000, Eisdspa ~650.000, ZeeStar >800.000) tidak punya sumber yang disebut. Folder `referens/` tidak memuat PDF UpHaaR, Astraea, He et al., maupun Eisdspa. Angka 45.000 sama dengan "Baseline Plaintext" yang di-hardcode di `generate_charts.py` tanpa sumber. Angka ini tampak sebagai estimasi penulis dan harus diberi label begitu atau dihapus.
- **Dua klaim konseptual keliru di Tabel 2:** "Sirkuit Groth16 non-malleability" salah, karena bukti Groth16 dapat di-rerandomize. "Kerahasiaan terjamin selama soundess BN254 terpenuhi" mencampur soundness dengan sifat zero-knowledge (ada juga typo "soundess").
- **Klaim regulasi:** kesimpulan menyatakan prototipe membantu memenuhi minimisasi data UU PDP. Padahal operator melihat nominal plaintext. UU PDP juga tidak dirujuk sebagai sumber primer di daftar pustaka.
- **Referensi:** seluruh 27 entri tersitir di teks. Beberapa kecocokannya lemah: Sameera et al. (survei federated learning) untuk HE/ZKP, Wang et al. (zkBID) untuk ketegangan audit-privasi, Zhang et al. (2019) untuk dual-write. Sameera et al. juga memberi DOI arXiv untuk artikel jurnal. Tahun Morais et al. (2020) perlu dicek ulang karena setahu saya terbit 2019. Saya tidak bisa memverifikasi eksistensi tiap referensi ke basis data ilmiah di sesi ini. Berkas `revisi_4.md` di repo adalah audit buatan AI atas daftar lama, yang saya tidak jadikan dasar.

## D. Verifikasi terhadap repositori (branch `dev`)

**Terverifikasi dari kode:**

1. Kontrak bernama `DonationRegistry.sol` (Solidity 0.8.28), bukan `TrustGive.sol` 0.8.20. Fungsinya hanya `setCampaignMaxDonation`, `recordDonation`, `getDonation`, `getDonationCount`. **Tidak ada** `donateVerify()`, `createCampaign()`, `finalize()`, `donateOptimized()`, fungsi `payable`, atau transfer dana. Baris Tabel 3 untuk Create Campaign, Finalize, dan "Optimasi Event Log" tidak punya kode, dan kalimat "pairing + SSTORE komitmen + transfer" salah.
2. Backend memakai **Go Gin** (`go.mod`) dan frontend **React + Vite**. Naskah menulis "Go Fiber" dan "Next.js", sedangkan Gambar 1 sendiri menulis "Go Gin".
3. Backend menerima nominal **plaintext**, mengecek pagu di Go, lalu mengenkripsi dan menyimpan. Backend juga yang membuat proof (`GenerateProof` mengembalikan `secret`), jadi *delegated prover*. Gambar 1 menyatakan "Enkripsi Nilai di Sisi Peramban (Client-Side)", yang bertentangan dengan kode dan dengan `docs/16-KETERBATASAN-DEMO.md`.
4. Proof diverifikasi terpisah dari ciphertext yang dienkripsi dan diagregasi. Tidak ada keterikatan di antara keduanya.
5. Sirkuit nyata (`DonationProof.circom`): `commitment = Poseidon(amount, secret)`, **tanpa `campaignId`**. Naskah menulis `Poseidon(amount, donorSecret, campaignId)` dan menyebutnya "mengikat bukti pada identitas kampanye". Pembandingnya memakai `GreaterThan(64)` dan `LessEqThan(64)`, bukan `Num2Bits(64)` langsung.
6. Skema DB: `users`, `campaigns`, `donations`, `campaign_aggregates`, dan `donations_duplicate_archive`. `idempotency_key` adalah **kolom** di `donations` dengan unique index parsial, bukan entitas `idempotency_keys` seperti di naskah.
7. Status kampanye di kode hanya `active` dan `closed`. Gambar 4 menggambar enam status plus penyerahan kunci privat dan penyaluran dana, yang tidak ada.
8. Ciphertext dikirim ke kontrak sebagai **string desimal ASCII** (`[]byte(payload.EncryptedAmount)`, sekitar 1.233 byte). Skrip pengukuran sendiri berkomentar bahwa ini "current Go backend behavior".
9. Kontrak tidak mengecek keunikan `commitment`, dan tabel `donations` tidak punya unique constraint-nya. Skrip benchmark mengirim proof yang sama tiga kali berturut-turut. Gambar 1 menyebut "Anti-Replay On-Chain", yang tidak ada di kode.
10. Semua transaksi ditandatangani satu kunci relayer server (`signer.go`). Wallet donatur tidak pernah muncul di chain, sehingga baris "Pseudonim wallet" di Tabel 1 dan "alamat wallet donatur publik" di Tabel 2 tidak sesuai implementasi.
11. Tidak ada kode untuk "audit log terdistribusi", "isolasi proses enkripsi", "verifikasi opening (M, R)", atau pencairan dana yang terikat bukti (Tabel 1 dan 2). `cmd/verify-aggregate` hanya dekripsi manual dengan UUID kampanye yang di-hardcode.
12. Alur `finalizeOnChain` tidak atomik: tx on-chain, lalu simpan tx hash, lalu status `confirmed`, lalu `IncrementAggregate`. Kegagalan di tengah meninggalkan donasi `confirmed` tanpa agregat terbarui.
13. Paillier (`g = n+1`, `r` koprima, rentang pesan dicek, mod n²) diimplementasikan dengan benar. Kunci disimpan dengan izin 0600 dan `keys/` di-gitignore.

**Hasil uji saya sendiri (bukan dari tes repo):**

- Saya mengompilasi `DonationProof.circom` (circom2 0.2.23 + circomlib 2.0.5): **655 constraint** (374 non-linear + 281 linear), bukan 1.240. Kompilernya bukan 2.1.6 seperti di naskah, tetapi selisih sebesar itu tidak mungkin berasal dari versi.
- Pembangkitan witness menolak nominal 0, p−1, p−500, nominal > pagu, dan nominal di luar 64-bit, serta menerima nominal valid dan nominal = pagu. Ini mendukung klaim "negatif/melebihi pagu ditolak".
- Sirkuit menolak donasi sah (`amount=5`) jika `campaign_max` ≥ 2⁶⁴. DB mengizinkan `max_donation` hingga `NUMERIC(20,0)` (~10²⁰ > 2⁶⁴ ≈ 1,8×10¹⁹), sehingga kampanye dengan pagu sebesar itu tidak bisa menerima donasi.

**Indikasi, belum terbukti:**

- Angka Tabel 3 di luar tiga angka `recordDonation` dan `verifyProof` (deploy 594.137 dan 1.845.220, create 148.912, finalize 72.450) dan seluruh angka Tabel 4 hanya muncul di skrip pembuat naskah (`generate_jurnal_docx.py`) dan `generate_charts.py`, sebagai konstanta. Tidak ada log atau CSV mentah. `docs/16` menyatakan "laporan benchmark formal" di luar scope MVP.
- `README` lama di `assets/jurnal/` memuat angka berbeda untuk operasi yang sama: keygen 42,5 ms, enkripsi 2,4 ms, agregasi 0,015 ms, `recordDonation` 243.518 gas. Angka naskah berselisih sampai ~15×.
- Statistik KeyGen Tabel 4 (721 ± 24 ms, rentang 695–766) terlalu rapat untuk pencarian prima acak. Koefisien variasinya 3,3%. Pada uji pembanding saya (RSA-2048, OpenSSL, n=40) CV-nya ≈ 66%. Lingkungan dan pustakanya berbeda, jadi ini hanya indikator.
- "Latensi end-to-end ~3,45 s" sama dengan jumlah aritmetika rata-rata komponen (185,20 + 1.350,40 + 1.850,10 + 36,35 + 35,40 = 3.457,45 ms), bukan distribusi terukur. Angka 44,5% juga turunan aritmetika. Waktu on-chain 35 ms adalah automine Hardhat, tanpa waktu blok.
- "Verifikasi lokal 1.850 ms" lebih lambat daripada pembuatan proof 1.350 ms. Penyebabnya prover dan verifier dipanggil sebagai subprocess `node`/`npx snarkjs`, jadi waktunya mencakup *startup* proses. Label "O(1) pairing check" menyesatkan, dan "Circom C++ WitnessCalc" keliru karena repo memakai WASM.
- Naskah menyebut pengukuran gas dengan "Hardhat EVM tracer", padahal skrip memakai `gasUsed` dari receipt dan `estimateGas`. Angka 225.035 adalah `estimateGas`, yang sudah termasuk gas dasar 21.000.
- Teks menyebut payload uji "32-byte". Skrip berkomentar 22B dan string-nya sebenarnya 24 karakter.
- Versi di naskah tidak cocok dengan repo: Go 1.22.0 vs `go.mod` 1.25.3, SnarkJS 0.7.3 vs `^0.7.6`, Circom 2.1.6 vs `pragma circom 2.2.0`, Cancun hardfork vs tidak dikonfigurasi di `hardhat.config.ts`.

**Belum dapat dipastikan** (tidak bisa saya jalankan): apakah tes Go dan Hardhat lulus, dan apakah gas aktual sama dengan angka naskah. Sandbox tidak punya Go dan tidak bisa mengunduh `solc`.

## E. Kesesuaian dengan template SIMASI

Saya hanya punya template `.docx`. `rules_template.md` di repo adalah turunan Anda sendiri, bukan pedoman resmi, dan aims & scope serta batas halaman jurnal tidak tersedia bagi saya.

**Sesuai:** ukuran Letter, margin 2,54 cm, satu kolom, Times New Roman, isi 12 pt spasi 1,5 dengan indent baris pertama, urutan bagian (Abstract, Abstrak, Pendahuluan, Metode, Hasil dan Pembahasan, Kesimpulan, Daftar Pustaka), caption tabel di atas dan gambar di bawah.

**Tidak sesuai atau perlu dicek:**

1. **Header** disalin dari template apa adanya: "Vol. 4, No. 1, Juni 2024 hal. 1-14" dan DOI Article `10.46306/sm.v4i1.67`, yang merupakan metadata artikel contoh. Tanyakan ke editor apakah dikosongkan. Naskah Anda 17 halaman, bukan 1–14.
2. **Font tabel** 7,5–8,5 pt. Template memakai 10 pt. Tabel 4 dan 5 memakai 7,5 pt dengan 6–7 kolom di halaman portrait. Pangkas kolom atau pecah tabel.
3. **Gambar 3** (sequence diagram): teks tampak sangat kecil pada render saya. Periksa keterbacaannya saat dicetak.
4. **Sitasi:** template memakai "dkk." untuk teks Indonesia. Naskah memakai "et al." 29 kali dan "dkk." nol kali.
5. **Baris email:** angka superskrip afiliasi tampak sebagai digit biasa yang menempel pada alamat ("…gmail.com1"). Cek di Word.
6. Pada render LibreOffice, caption Gambar 2 terpisah dari gambarnya (halaman 10 vs gambar di halaman sebelumnya). Cek di Word dan atur *keep with next*.
7. Docx memuat 17 file gambar tetapi hanya 9 yang dipakai, sisanya sisa draf lama.
8. Judul 16 kata (template contoh 12 kata). Layak dipersingkat.

Panjang abstrak (134 dan 133 kata) tidak bermasalah dibanding contoh template (142 kata).

## F. Temuan berdasarkan prioritas

**Kritis**

- **K1. Fungsi dan angka kontrak yang tidak ada.** Lokasi: Metode §4, Tabel 3, Gambar 6, Tabel 5 ("Klaim Dana Tanpa Verifier"), abstrak, kesimpulan. Ini merupakan klaim implementasi yang tidak ada di kode, bukan sekadar beda penamaan. Perbaikan: tulis ulang Metode §4 dan Tabel 3 sesuai `DonationRegistry` (hapus baris `createCampaign`, `finalize`, `donateOptimized`, transfer dana), dan jelaskan bahwa sistem belum memindahkan dana.
- **K2. Asal angka Tabel 3 dan 4.** Tanpa log mentah, reviewer tidak bisa memverifikasi, dan ketidakkonsistenan dengan `README` lama mengundang kecurigaan. Perbaikan: buat skrip benchmark yang menulis CSV/JSON ke repo (100 iterasi, rata-rata, SD, min, maks dihitung dari data), jalankan ulang, dan laporkan lingkungan serta versi yang benar. Pisahkan waktu *in-process* dari overhead subprocess. Ganti "latensi end-to-end terukur" dengan pengukuran E2E sungguhan, atau sebut jumlah komponen sebagai estimasi.
- **K3. Gas yang dilaporkan tidak mewakili sistem.** Backend mengirim payload ~1.233 byte (1.481.690 gas menurut skrip Anda sendiri), yang muncul di Gambar 6 tetapi tidak di Tabel 3, abstrak, atau kesimpulan. Perbaikan: jadikan 1.481.690 gas sebagai angka utama sistem saat ini, dan tulis 613.607 dan 959.421 sebagai skenario payload alternatif. Angka ~270.000 sebut proyeksi dari desain yang belum dibuat, dan jangan masukkan ke abstrak sebagai hasil empiris.
- **K4. Klaim privasi dan keamanan melampaui implementasi.** Lokasi: abstrak, RQ3, Tabel 1, Tabel 2, Tabel 5, kesimpulan. Operator melihat plaintext dan membuat proof. Proof tidak mengikat ciphertext yang diagregasi, jadi jaminan rentang dari ZK tidak berlaku pada total. Total dekripsi berasal dari kunci server tanpa bukti, sehingga RQ3 dan kontribusi (3) ("verifikasi total tanpa kustodian kunci") tidak dijawab. Perbaikan: ubah RQ3 menjadi pertanyaan yang bisa dijawab, ganti "membuktikan kelayakan" dengan "mendemonstrasikan prototipe", dan koreksi baris Tabel 1 dan 2 yang tidak sesuai kode (wallet donatur, opening (M, R), audit log). Hapus klaim UU PDP atau turunkan menjadi "arah menuju".
- **K5. Deskripsi arsitektur bertentangan dengan repo.** Lokasi: Metode §1, §5, Gambar 1, 2, 4. Item: Fiber vs Gin, Next.js vs Vite, client-side vs server-side, tabel `idempotency_keys`, status kampanye, anti-replay. Perbaikan: samakan semuanya dengan kode, lalu cetak ulang gambar dari kode terkini.

**Mayor**

- **M1. Deskripsi sirkuit.** Komitmen tanpa `campaignId` berarti bukti tidak terikat kampanye, dan commitment tidak unik di kontrak maupun DB, sehingga proof bisa diputar ulang. Perbaikan: tambahkan `campaignId` ke komitmen atau enforce unique commitment, dan koreksi rumus serta jumlah constraint (655).
- **M2. Bukti pengujian Tabel 5.** Yang ada di repo hanya dua tes Hardhat (proof valid dan proof tidak valid). Tidak ada tes sirkuit, tes malleability (tes proof tidak valid bukan tes malleability), tes konkurensi untuk donasi berbeda (skrip yang ada menguji `Idempotency-Key` sama), tes injeksi RPC timeout, ataupun tes serangan DDoS. `docs` menyebut CI, tetapi tidak ada file workflow di branch. Perbaikan: tambahkan tes otomatis untuk tiap baris "SUKSES", atau turunkan statusnya menjadi "diamati manual" dengan prosedur dan hasil yang dilampirkan.
- **M3. Klaim dual-write dan race "berhasil diatasi".** Lihat D.12. Perbaikan: ubah menjadi "dimitigasi dengan rekonsiliasi" dan tunjukkan bukti injeksi kegagalan.
- **M4. Justifikasi desain dan pembanding.** Lihat C: Paillier vs Pedersen/EC-ElGamal, dan sumber angka Tabel 1.
- **M5. Reproduktibilitas.** Tidak ada skrip trusted setup (ptau/zkey), `zk/build/` tidak di-track, dan tidak ada perintah build sirkuit. Tabel 1 menulis "Single-party setup" tanpa dokumentasi. Perbaikan: tambahkan skrip setup dan build dari nol, dan jelaskan implikasi toxic waste.
- **M6. Konsep Groth16 dan soundness** (Tabel 2), lihat C.
- **M7. Atribusi dan kebersihan repo.** `go.mod` dan README menunjuk `github.com/izagoto/zk-paillier-donation-system`, bukan repo Anda. Jelaskan hubungan dan kontribusi masing-masing. Repo juga memuat `JURNAL_SIMASI_TRUSTGIVE_BARU.docx`, README yang menggambarkan versi naskah lain (28 referensi, logo UNISBA), file kunci Word `~$RNAL…docx`, file `test_*.docx`, dan 24 PDF makalah berhak cipta di `referens/`. Bersihkan sebelum tautan repo dicantumkan.

**Minor**

- Ketidakcocokan versi (D). Bug pagu ≥ 2⁶⁴ (D).
- Teks menyebut agregasi "O(1)", Tabel 4 menyebut O(k²).
- Satuan nominal (rupiah? wei?) tidak didefinisikan.
- Gas Tabel 3 hanya dari satu proof berulang, dan penyimpanan proof 320 byte di storage kontrak tidak dibahas dalam penjelasan biaya SSTORE.

**Editorial:** butir E.1–E.8 di atas, dan typo "soundess".

## G. Aspek yang kuat

- Bagian keterbatasan (Tabel 5 baris BATASAN dan §4) jujur dan konsisten dengan `docs/08`, `16`, dan `17`. Ini yang paling saya hargai.
- Rumusan masalah dan RQ jelas.
- Kontrak memeriksa public input (`pubSignals[0]==campaignMax`, `pubSignals[1]==commitment`) sebelum `verifyProof`, dan pagu diambil dari DB, bukan dari klien.
- Paillier benar secara fungsional dan punya tes homomorfik.
- Sirkuit menolak semua kasus tepi yang saya uji.
- DB tidak menyimpan nominal plaintext.
- Idempotensi memakai unique index parsial dengan penanganan unique violation, dan agregat diperbarui dengan `FOR UPDATE`.
- Semua referensi tersitir dan struktur naskah mengikuti template.

## H. Revisi sebelum submission (berurutan)

1. Pilih jalur: **jelaskan sistem apa adanya** (disarankan untuk waktu yang ada) dan tulis binding serta kunci terdistribusi sebagai future work.
2. Tulis ulang Metode §1, §4, §5 dan Gambar 1, 2, 4 sesuai kode (K1, K5).
3. Buat dan jalankan skrip benchmark dengan keluaran mentah di repo, lalu ganti Tabel 3, 4, Gambar 6, 7 (K2, K3). Contoh perbaikan baris Tabel 3: ganti "Donate Verify (Full 512B)" dengan "recordDonation (payload desimal 1.233 B, perilaku backend saat ini): 1.481.690 gas".
4. Turunkan klaim: abstrak, RQ3, kesimpulan, Tabel 1, 2, 5 (K4). Contoh: ganti "Pengujian empiris membuktikan…" dengan "Pengukuran pada prototipe menunjukkan…", dan beri label estimasi pada angka proyeksi.
5. Koreksi sirkuit (commitment, 655 constraint) dan tambahkan `campaignId` atau uniqueness commitment (M1).
6. Tambahkan tes otomatis untuk tiap baris Tabel 5, atau ubah statusnya (M2, M3).
7. Beri sumber atau hapus angka pembanding di Tabel 1, dan tambahkan justifikasi Paillier vs Pedersen (M4).
8. Tambahkan skrip setup dan build ZK dari nol (M5).
9. Koreksi Tabel 2 (non-malleability, soundness vs zero-knowledge).
10. Verifikasi DOI dan metadata semua referensi lewat Crossref, tambahkan UU PDP sebagai sumber primer jika klaim hukum dipertahankan.
11. Rapikan template (E) dan bersihkan repo (M7).

## I. Rekomendasi keputusan editorial

**Major Revision.** Masalah inti ada pada kesesuaian klaim dan bukti, bukan pada topiknya.

## J. Kesiapan submission

**Belum siap.** Risiko terbesar: reviewer membuka repositori dan menemukan fungsi kontrak yang tidak ada, angka tanpa sumber, dan deskripsi arsitektur yang berbeda dari kode. Itu dapat dibaca sebagai misrepresentasi, bukan sekadar kekeliruan penyajian. Risiko kedua adalah kebaruan yang tipis jika tiga properti utamanya tidak tercapai. Risiko ketiga adalah kesesuaian ruang lingkup: contoh template SIMASI adalah perancangan basis data, sedangkan naskah ini kriptografi terapan. Periksa aims & scope jurnal, yang tidak saya miliki.

## Yang tidak saya periksa

- Tes Go dan Hardhat tidak dijalankan, jadi gas, waktu, dan hasil tes lulus tidak saya reproduksi.
- Gambar 2 (ERD), 5, dan 7 tidak saya lihat langsung. Klaim "5 entitas" saya nilai dari teks naskah dan skema migrasi.
- Kode frontend, `docs/13`, `15`, `19`, `20`, dan worker rekonsiliasi (`service_reconciliation.go`) tidak saya baca penuh.
- Referensi tidak diverifikasi ke basis data ilmiah.
- Pedoman resmi SIMASI selain template `.docx` tidak tersedia bagi saya.