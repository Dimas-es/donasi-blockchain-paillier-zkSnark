package paillier

import (
	"math/big"
	"testing"
)

func BenchmarkKeygen512(b *testing.B) {
	for b.Loop() {
		_, _, err := GenerateKeypair(512)
		if err != nil {
			b.Fatalf("keygen failed: %v", err)
		}
	}
}

func BenchmarkKeygen1024(b *testing.B) {
	for b.Loop() {
		_, _, err := GenerateKeypair(1024)
		if err != nil {
			b.Fatalf("keygen failed: %v", err)
		}
	}
}

func BenchmarkKeygen2048(b *testing.B) {
	for b.Loop() {
		_, _, err := GenerateKeypair(2048)
		if err != nil {
			b.Fatalf("keygen failed: %v", err)
		}
	}
}

func BenchmarkEncrypt512(b *testing.B) {
	pk, _, err := GenerateKeypair(512)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	amount := big.NewInt(100000)

	for b.Loop() {
		_, err := pk.Encrypt(amount)
		if err != nil {
			b.Fatalf("encrypt failed: %v", err)
		}
	}
}

func BenchmarkEncrypt1024(b *testing.B) {
	pk, _, err := GenerateKeypair(1024)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	amount := big.NewInt(100000)

	for b.Loop() {
		_, err := pk.Encrypt(amount)
		if err != nil {
			b.Fatalf("encrypt failed: %v", err)
		}
	}
}

func BenchmarkEncrypt2048(b *testing.B) {
	pk, _, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	amount := big.NewInt(100000)

	for b.Loop() {
		_, err := pk.Encrypt(amount)
		if err != nil {
			b.Fatalf("encrypt failed: %v", err)
		}
	}
}

func BenchmarkHomomorphicAdd2048(b *testing.B) {
	pk, _, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	c1, err := pk.Encrypt(big.NewInt(100000))
	if err != nil {
		b.Fatalf("encrypt failed: %v", err)
	}
	c2, err := pk.Encrypt(big.NewInt(250000))
	if err != nil {
		b.Fatalf("encrypt failed: %v", err)
	}

	for b.Loop() {
		_, err := pk.Add(c1, c2)
		if err != nil {
			b.Fatalf("add failed: %v", err)
		}
	}
}

func BenchmarkDecrypt2048(b *testing.B) {
	pk, sk, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	c, err := pk.Encrypt(big.NewInt(500000))
	if err != nil {
		b.Fatalf("encrypt failed: %v", err)
	}

	for b.Loop() {
		_, err := sk.Decrypt(c)
		if err != nil {
			b.Fatalf("decrypt failed: %v", err)
		}
	}
}

func BenchmarkReconcile100Donations2048(b *testing.B) {
	pk, _, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatalf("keygen failed: %v", err)
	}
	ciphertexts := make([]*big.Int, 100)
	for i := 0; i < 100; i++ {
		c, err := pk.Encrypt(big.NewInt(int64(10000 * (i + 1))))
		if err != nil {
			b.Fatalf("encrypt failed: %v", err)
		}
		ciphertexts[i] = c
	}

	for b.Loop() {
		total := ciphertexts[0]
		for j := 1; j < 100; j++ {
			total, err = pk.Add(total, ciphertexts[j])
			if err != nil {
				b.Fatalf("add failed: %v", err)
			}
		}
	}
}
