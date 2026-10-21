package paillier

import (
	"math/big"
	"testing"
)

func BenchmarkKeyGen512(b *testing.B) {
	for b.Loop() {
		_, _, _ = GenerateKeypair(512)
	}
}

func BenchmarkKeyGen2048(b *testing.B) {
	for b.Loop() {
		_, _, _ = GenerateKeypair(2048)
	}
}

func BenchmarkEncrypt2048(b *testing.B) {
	pk, _, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatal(err)
	}
	msg := big.NewInt(50000)
	for b.Loop() {
		_, _ = pk.Encrypt(msg)
	}
}

func BenchmarkDecrypt2048(b *testing.B) {
	pk, sk, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatal(err)
	}
	msg := big.NewInt(50000)
	cipher, _ := pk.Encrypt(msg)
	for b.Loop() {
		_, _ = sk.Decrypt(cipher)
	}
}

func BenchmarkAdd2048(b *testing.B) {
	pk, _, err := GenerateKeypair(2048)
	if err != nil {
		b.Fatal(err)
	}
	c1, _ := pk.Encrypt(big.NewInt(10000))
	c2, _ := pk.Encrypt(big.NewInt(25000))
	for b.Loop() {
		_, _ = pk.Add(c1, c2)
	}
}
