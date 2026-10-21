package paillier

import (
	"math/big"
	"testing"
)

func TestEncryptDecrypt(t *testing.T) {
	publicKey, privateKey, err := GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	amount := big.NewInt(100000)

	ciphertext, err := publicKey.Encrypt(amount)
	if err != nil {
		t.Fatalf("failed to encrypt: %v", err)
	}

	decrypted, err := privateKey.Decrypt(ciphertext)
	if err != nil {
		t.Fatalf("failed to decrypt: %v", err)
	}

	if decrypted.Cmp(amount) != 0 {
		t.Fatalf(
			"decrypted value mismatch: got %s, want %s",
			decrypted.String(),
			amount.String(),
		)
	}
}

func TestHomomorphicAddition(t *testing.T) {
	publicKey, privateKey, err := GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	amount1 := big.NewInt(100000)
	amount2 := big.NewInt(250000)

	ciphertext1, err := publicKey.Encrypt(amount1)
	if err != nil {
		t.Fatalf("failed to encrypt amount1: %v", err)
	}

	ciphertext2, err := publicKey.Encrypt(amount2)
	if err != nil {
		t.Fatalf("failed to encrypt amount2: %v", err)
	}

	encryptedTotal, err := publicKey.Add(
		ciphertext1,
		ciphertext2,
	)
	if err != nil {
		t.Fatalf("failed to add ciphertexts: %v", err)
	}

	decryptedTotal, err := privateKey.Decrypt(encryptedTotal)
	if err != nil {
		t.Fatalf("failed to decrypt total: %v", err)
	}

	expected := new(big.Int).Add(amount1, amount2)

	if decryptedTotal.Cmp(expected) != 0 {
		t.Fatalf(
			"homomorphic addition mismatch: got %s, want %s",
			decryptedTotal.String(),
			expected.String(),
		)
	}
}

func TestSaveAndLoadKeypair(t *testing.T) {
	publicKey, privateKey, err := GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	keyPath := t.TempDir() + "/paillier.json"

	if err := SaveKeypair(
		keyPath,
		publicKey,
		privateKey,
	); err != nil {
		t.Fatalf("failed to save keypair: %v", err)
	}

	loadedPublicKey, loadedPrivateKey, err := LoadKeypair(keyPath)
	if err != nil {
		t.Fatalf("failed to load keypair: %v", err)
	}

	if loadedPublicKey.N.Cmp(publicKey.N) != 0 {
		t.Fatal("loaded public key N does not match")
	}

	if loadedPublicKey.N2.Cmp(publicKey.N2) != 0 {
		t.Fatal("loaded public key N2 does not match")
	}

	if loadedPublicKey.G.Cmp(publicKey.G) != 0 {
		t.Fatal("loaded public key G does not match")
	}

	if loadedPrivateKey.Lambda.Cmp(privateKey.Lambda) != 0 {
		t.Fatal("loaded private key lambda does not match")
	}

	if loadedPrivateKey.Mu.Cmp(privateKey.Mu) != 0 {
		t.Fatal("loaded private key mu does not match")
	}

	amount := big.NewInt(100000)

	ciphertext, err := loadedPublicKey.Encrypt(amount)
	if err != nil {
		t.Fatalf("failed to encrypt with loaded key: %v", err)
	}

	decrypted, err := loadedPrivateKey.Decrypt(ciphertext)
	if err != nil {
		t.Fatalf("failed to decrypt with loaded key: %v", err)
	}

	if decrypted.Cmp(amount) != 0 {
		t.Fatalf(
			"decrypted value mismatch: got %s, want %s",
			decrypted.String(),
			amount.String(),
		)
	}
}

func TestKeyManagerLoadOrGenerate(t *testing.T) {
	keyPath := t.TempDir() + "/paillier.json"

	manager := NewKeyManager(keyPath, 512)

	if err := manager.LoadOrGenerate(); err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	if manager.PublicKey == nil {
		t.Fatal("public key is nil")
	}

	if manager.PrivateKey == nil {
		t.Fatal("private key is nil")
	}

	firstN := new(big.Int).Set(manager.PublicKey.N)

	manager2 := NewKeyManager(keyPath, 512)

	if err := manager2.LoadOrGenerate(); err != nil {
		t.Fatalf("failed to load keypair: %v", err)
	}

	if manager2.PublicKey == nil {
		t.Fatal("loaded public key is nil")
	}

	if manager2.PrivateKey == nil {
		t.Fatal("loaded private key is nil")
	}

	if manager2.PublicKey.N.Cmp(firstN) != 0 {
		t.Fatal("loaded keypair does not match original keypair")
	}
}

func TestIncrementalHomomorphicAggregation(t *testing.T) {
	publicKey, privateKey, err := GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	amounts := []*big.Int{
		big.NewInt(100000),
		big.NewInt(250000),
		big.NewInt(50000),
	}

	var encryptedTotal *big.Int

	for _, amount := range amounts {
		ciphertext, err := publicKey.Encrypt(amount)
		if err != nil {
			t.Fatalf("failed to encrypt amount: %v", err)
		}

		if encryptedTotal == nil {
			encryptedTotal = ciphertext
			continue
		}

		encryptedTotal, err = publicKey.Add(
			encryptedTotal,
			ciphertext,
		)
		if err != nil {
			t.Fatalf("failed to add ciphertext: %v", err)
		}
	}

	decryptedTotal, err := privateKey.Decrypt(encryptedTotal)
	if err != nil {
		t.Fatalf("failed to decrypt total: %v", err)
	}

	expected := big.NewInt(400000)

	if decryptedTotal.Cmp(expected) != 0 {
		t.Fatalf(
			"incremental aggregation mismatch: got %s, want %s",
			decryptedTotal.String(),
			expected.String(),
		)
	}
}

func TestZeroKnowledgeOpeningVerification(t *testing.T) {
	publicKey, privateKey, err := GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	// 1. Setup 3 simulated donation amounts
	amounts := []*big.Int{
		big.NewInt(150000), // donation 1: Rp 150.000
		big.NewInt(350000), // donation 2: Rp 350.000
		big.NewInt(500000), // donation 3: Rp 500.000
	}

	// 2. Sample 3 explicit random coprimes r_i
	rValues := make([]*big.Int, len(amounts))
	for i := range amounts {
		r, err := randomCoprime(publicKey.N)
		if err != nil {
			t.Fatalf("failed to sample coprime: %v", err)
		}
		rValues[i] = r
	}

	// 3. Encrypt donations deterministically using r_i
	var cAgg *big.Int
	totalM := big.NewInt(0)
	totalR := big.NewInt(1)

	for i, m := range amounts {
		c, err := publicKey.EncryptWithRandomness(m, rValues[i])
		if err != nil {
			t.Fatalf("failed to encrypt donation %d: %v", i+1, err)
		}

		totalM.Add(totalM, m)
		totalR.Mul(totalR, rValues[i])
		totalR.Mod(totalR, publicKey.N)

		if cAgg == nil {
			cAgg = c
		} else {
			cAgg, err = publicKey.Add(cAgg, c)
			if err != nil {
				t.Fatalf("failed to homomorphically aggregate ciphertext %d: %v", i+1, err)
			}
		}
	}

	// Verify standard private key decryption matches M
	decryptedM, err := privateKey.Decrypt(cAgg)
	if err != nil {
		t.Fatalf("failed to decrypt cAgg: %v", err)
	}
	if decryptedM.Cmp(totalM) != 0 {
		t.Fatalf("decryption mismatch: got %s, want %s", decryptedM, totalM)
	}

	// 4. Test Case 1: Valid Opening (M, R) verification WITHOUT private key
	// Anyone can verify cAgg == (1 + M*n) * R^n mod n^2 using only publicKey
	if !publicKey.VerifyOpening(cAgg, totalM, totalR) {
		t.Fatalf("valid opening (M, R) failed verification!")
	}

	// 5. Test Case 2: Tampered M (Wrong amount) MUST FAIL
	forgedM := new(big.Int).Add(totalM, big.NewInt(1000)) // attacker claims extra Rp 1.000
	if publicKey.VerifyOpening(cAgg, forgedM, totalR) {
		t.Fatalf("tampered M was accepted! Soundness violation!")
	}

	forgedM2 := new(big.Int).Sub(totalM, big.NewInt(50000)) // attacker under-reports
	if publicKey.VerifyOpening(cAgg, forgedM2, totalR) {
		t.Fatalf("under-reported M was accepted! Soundness violation!")
	}

	// 6. Test Case 3: Tampered R (Wrong randomness) MUST FAIL
	forgedR := new(big.Int).Add(totalR, big.NewInt(1))
	if publicKey.VerifyOpening(cAgg, totalM, forgedR) {
		t.Fatalf("tampered R was accepted! Soundness violation!")
	}
}
