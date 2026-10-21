package main

import (
	"fmt"
	"math/big"

	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/crypto/paillier"
)

func main() {
	fmt.Println("=== DEMONSTRASI VERIFIKASI PUBLIK PEMBUKAAN (M, R) PAILLIER ===")
	fmt.Println("Tujuan: Memverifikasi keabsahan total saldo kampanye M tanpa kunci privat!")

	// 1. Inisialisasi public key Paillier (512-bit untuk demonstrasi cepat, 2048-bit untuk produksi)
	pk, _, err := paillier.GenerateKeypair(512)
	if err != nil {
		panic(err)
	}

	// 2. Simulasi 3 donasi masuk
	m1 := big.NewInt(150000) // Donasi 1: Rp 150.000
	m2 := big.NewInt(350000) // Donasi 2: Rp 350.000
	m3 := big.NewInt(500000) // Donasi 3: Rp 500.000

	r1 := big.NewInt(123456789)
	r2 := big.NewInt(987654321)
	r3 := big.NewInt(112233445)

	c1, _ := pk.EncryptWithRandomness(m1, r1)
	c2, _ := pk.EncryptWithRandomness(m2, r2)
	c3, _ := pk.EncryptWithRandomness(m3, r3)

	// 3. Akumulasi homomorfik off-chain
	cAgg, _ := pk.Add(c1, c2)
	cAgg, _ = pk.Add(cAgg, c3)

	// 4. Pengelola kampanye mempublikasikan M dan R
	M := new(big.Int).Add(m1, new(big.Int).Add(m2, m3)) // M = Rp 1.000.000
	R := new(big.Int).Mul(r1, new(big.Int).Mul(r2, r3))
	R.Mod(R, pk.N)

	fmt.Printf("\n[1] Informasi Publik dari Pengelola:\n")
	fmt.Printf("    - Total Saldo Plaintext (M) : Rp %s\n", M.String())
	fmt.Printf("    - Faktor Acak Terbuka (R)   : %s...\n", R.String()[:20])
	fmt.Printf("    - Ciphertext Agregat (c_agg): %s...\n", cAgg.String()[:20])

	// 5. Auditor independen memverifikasi tanpa private key
	fmt.Println("\n[2] Uji Verifikasi Publik Independen:")
	valid := pk.VerifyOpening(cAgg, M, R)
	fmt.Printf("    - Kasus 1 (M Sah = Rp 1.000.000): Hasil Verifikasi = %t (BERHASIL)\n", valid)

	// 6. Uji kasus kecurangan: Pengelola memanipulasi total saldo M
	tamperedM := new(big.Int).Add(M, big.NewInt(100000)) // Mengklaim Rp 1.100.000 (+100k)
	invalid := pk.VerifyOpening(cAgg, tamperedM, R)
	fmt.Printf("    - Kasus 2 (M Palsu = Rp 1.100.000): Hasil Verifikasi = %t (DITOLAK SECARA KRIPTOGRAFIS)\n", invalid)

	if valid && !invalid {
		fmt.Println("\nKESIMPULAN: Skema pembuktian pembukaan (M, R) terbukti secara matematis menjamin integritas audit!")
	}
}
