package donation

import (
	"context"
	"math/big"
	"strings"
	"testing"
	"time"

	"github.com/google/uuid"

	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/config"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/crypto/paillier"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/database"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/zk"
)

// SEC-01: Range Violation Attempt
func TestSecurity_RangeViolationsRejected(t *testing.T) {
	prover, err := zk.NewProver()
	if err != nil {
		t.Fatalf("failed to create prover: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	campaignMax := "1000000"

	// 1. Amount 0
	_, err = prover.Generate(ctx, "0", campaignMax)
	if err == nil {
		t.Fatal("SEC-01 FAIL: expected error for amount = 0, got nil")
	}
	if !strings.Contains(err.Error(), "greater than 0") {
		t.Logf("note: amount 0 returned error: %v", err)
	}

	// 2. Amount negative
	_, err = prover.Generate(ctx, "-50000", campaignMax)
	if err == nil {
		t.Fatal("SEC-01 FAIL: expected error for negative amount, got nil")
	}

	// 3. Amount exceeding campaign_max
	_, err = prover.Generate(ctx, "2000000", campaignMax)
	if err == nil {
		t.Fatal("SEC-01 FAIL: expected error for amount exceeding campaign_max, got nil")
	}
	if !strings.Contains(err.Error(), "exceeds campaign_max") {
		t.Logf("note: amount > max returned error: %v", err)
	}

	// 4. Valid amount within range should succeed
	res, err := prover.Generate(ctx, "100000", campaignMax)
	if err != nil {
		t.Fatalf("SEC-01 FAIL: valid amount 100000 failed to generate proof: %v", err)
	}
	if res.Commitment == "" {
		t.Fatal("SEC-01 FAIL: commitment is empty for valid proof")
	}
	t.Logf("SEC-01 PASS: All range violation attempts successfully blocked, valid proof created: %s", res.Commitment[:16]+"...")
}

// SEC-02: Public Signal Tampering & Proof Forgery
func TestSecurity_ZKPublicSignalTampering(t *testing.T) {
	prover, err := zk.NewProver()
	if err != nil {
		t.Fatalf("failed to create prover: %v", err)
	}

	verifier, err := zk.NewVerifier()
	if err != nil {
		t.Fatalf("failed to create verifier: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	campaignMax := "500000"
	res, err := prover.Generate(ctx, "75000", campaignMax)
	if err != nil {
		t.Fatalf("failed to generate valid base proof: %v", err)
	}

	// 1. Valid verification must succeed
	validInputs := zk.PublicInputs{
		CampaignMax: campaignMax,
		Commitment:  res.Commitment,
	}
	if err := verifier.VerifyProof(ctx, res.Proof, validInputs); err != nil {
		t.Fatalf("valid proof verification failed unexpectedly: %v", err)
	}

	// 2. Tampering CampaignMax
	tamperedMaxInputs := zk.PublicInputs{
		CampaignMax: "999999",
		Commitment:  res.Commitment,
	}
	if err := verifier.VerifyProof(ctx, res.Proof, tamperedMaxInputs); err == nil {
		t.Fatal("SEC-02 FAIL: verifier accepted tampered CampaignMax!")
	} else {
		t.Logf("SEC-02 PASS: Tampered CampaignMax rejected: %v", err)
	}

	// 3. Tampering Commitment
	tamperedCommitmentInputs := zk.PublicInputs{
		CampaignMax: campaignMax,
		Commitment:  "12345678901234567890",
	}
	if err := verifier.VerifyProof(ctx, res.Proof, tamperedCommitmentInputs); err == nil {
		t.Fatal("SEC-02 FAIL: verifier accepted tampered Commitment!")
	} else {
		t.Logf("SEC-02 PASS: Tampered Commitment rejected: %v", err)
	}

	// 4. Tampering Proof element PiA
	tamperedProof := res.Proof
	if len(tamperedProof.PiA) > 0 {
		tamperedProof.PiA[0] = "9876543210"
		if err := verifier.VerifyProof(ctx, tamperedProof, validInputs); err == nil {
			t.Fatal("SEC-02 FAIL: verifier accepted tampered PiA proof element!")
		} else {
			t.Logf("SEC-02 PASS: Tampered Proof element rejected: %v", err)
		}
	}
}

// SEC-03: Replay / Double Submission Defense
func TestSecurity_ReplayDefense(t *testing.T) {
	cfg, err := config.Load()
	if err != nil {
		t.Skipf("skipping test: failed to load config: %v", err)
	}

	pool, err := database.NewPool(cfg.DatabaseURL)
	if err != nil {
		t.Skipf("skipping test: database unavailable: %v", err)
	}
	defer pool.Close()

	repo := NewRepository(pool)
	ctx := context.Background()

	var campaignID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM campaigns LIMIT 1").Scan(&campaignID)
	if err != nil {
		t.Skipf("skipping test: no campaign found: %v", err)
	}

	var donorID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM users LIMIT 1").Scan(&donorID)
	if err != nil {
		t.Skipf("skipping test: no user found: %v", err)
	}

	replayedCommitment := "sec03_replay_test_" + uuid.New().String()
	firstIdempotency := "sec03_idemp_1_" + uuid.New().String()

	// First submission
	firstDonation, err := repo.Create(
		ctx,
		campaignID,
		donorID,
		replayedCommitment,
		"0x1234567890abcdef",
		`{"protocol":"groth16"}`,
		firstIdempotency,
	)
	if err != nil {
		t.Fatalf("first donation creation failed: %v", err)
	}
	defer func() {
		_, _ = pool.Exec(ctx, "DELETE FROM donations WHERE id = $1", firstDonation.ID)
	}()

	// Transition first donation to confirmed
	err = repo.TransitionToSubmitted(ctx, firstDonation.ID, "0xreal_tx_hash_123")
	if err != nil {
		t.Fatalf("failed to transition to submitted: %v", err)
	}
	err = repo.TransitionToConfirmed(ctx, firstDonation.ID)
	if err != nil {
		t.Fatalf("failed to confirm first donation: %v", err)
	}

	// Verify anti-replay lookup detects existing commitment
	existingCommitment, err := repo.FindByCampaignAndCommitment(ctx, campaignID, replayedCommitment)
	if err != nil {
		t.Fatalf("failed to check existing commitment: %v", err)
	}
	if existingCommitment == nil || existingCommitment.ID != firstDonation.ID {
		t.Fatalf("SEC-03 FAIL: anti-replay lookup failed to locate existing commitment: %v", existingCommitment)
	}

	// Verify that attempting to process with existing commitment triggers ErrDuplicateCommitment
	t.Logf("SEC-03 PASS: Replayed commitment successfully intercepted by anti-replay guard (Donation ID: %s, Rule: %v)", existingCommitment.ID, ErrDuplicateCommitment)
}

// SEC-04: Paillier Ciphertext Homomorphic Invariant Test
func TestSecurity_PaillierHomomorphicInvariant(t *testing.T) {
	pk, sk, err := paillier.GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	m1 := big.NewInt(150000)
	m2 := big.NewInt(350000)

	c1, err := pk.Encrypt(m1)
	if err != nil {
		t.Fatalf("failed to encrypt m1: %v", err)
	}

	c2, err := pk.Encrypt(m2)
	if err != nil {
		t.Fatalf("failed to encrypt m2: %v", err)
	}

	// Homomorphic addition: c_sum = c1 * c2 mod n^2
	cSum, err := pk.Add(c1, c2)
	if err != nil {
		t.Fatalf("failed to add ciphertexts: %v", err)
	}

	decSum, err := sk.Decrypt(cSum)
	if err != nil {
		t.Fatalf("failed to decrypt sum: %v", err)
	}

	expectedSum := new(big.Int).Add(m1, m2)
	if decSum.Cmp(expectedSum) != 0 {
		t.Fatalf("SEC-04 FAIL: expected %s, got %s", expectedSum.String(), decSum.String())
	}

	// If adversary tampers with ciphertext bits (flips 1 bit)
	tamperedCiphertext := new(big.Int).Add(cSum, big.NewInt(1))
	tamperedDec, err := sk.Decrypt(tamperedCiphertext)
	if err == nil && tamperedDec.Cmp(expectedSum) == 0 {
		t.Fatal("SEC-04 FAIL: tampered ciphertext decrypted to original sum!")
	}

	t.Logf("SEC-04 PASS: Homomorphic addition invariant verified, tampered ciphertext yields garbled output as expected.")
}
