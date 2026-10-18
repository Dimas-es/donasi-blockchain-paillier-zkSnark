package donation

import (
	"context"
	"math/big"
	"sync"
	"testing"

	"github.com/google/uuid"

	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/config"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/crypto/paillier"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/database"
)

func TestGuardedStateTransitions(t *testing.T) {
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

	// 1. Create a dummy campaign and user if needed, or use existing campaign
	var campaignID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM campaigns LIMIT 1").Scan(&campaignID)
	if err != nil {
		t.Skipf("skipping test: no campaign available in database: %v", err)
	}

	var donorID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM users LIMIT 1").Scan(&donorID)
	if err != nil {
		t.Skipf("skipping test: no user available in database: %v", err)
	}

	idempotencyKey := "test-idemp-" + uuid.New().String()
	commitment := "test-commitment-" + uuid.New().String()

	// Step 1: Create pending donation
	donation, err := repo.Create(
		ctx,
		campaignID,
		donorID,
		commitment,
		"1234567890",
		`{"mock": true}`,
		idempotencyKey,
	)
	if err != nil {
		t.Fatalf("failed to create pending donation: %v", err)
	}
	defer func() {
		// Clean up test donation
		_, _ = pool.Exec(ctx, "DELETE FROM donations WHERE id = $1", donation.ID)
	}()

	if donation.Status != StatusPending {
		t.Fatalf("expected status %s, got %s", StatusPending, donation.Status)
	}

	// Step 2: Invalid transition: pending -> confirmed (MUST FAIL because it hasn't been submitted)
	err = repo.TransitionToConfirmed(ctx, donation.ID)
	if err != ErrInvalidStateTransition {
		t.Fatalf("expected ErrInvalidStateTransition for pending -> confirmed, got: %v", err)
	}

	// Step 3: Valid transition: pending -> submitted
	testTxHash := "0x" + uuid.New().String()
	err = repo.TransitionToSubmitted(ctx, donation.ID, testTxHash)
	if err != nil {
		t.Fatalf("failed to transition pending -> submitted: %v", err)
	}

	// Verify status in DB
	dSubmitted, err := repo.FindByID(ctx, donation.ID)
	if err != nil {
		t.Fatalf("failed to reload donation: %v", err)
	}
	if dSubmitted.Status != StatusSubmitted || dSubmitted.TxHash != testTxHash {
		t.Fatalf("expected status %s and tx %s, got %s and %s", StatusSubmitted, testTxHash, dSubmitted.Status, dSubmitted.TxHash)
	}

	// Step 4: Invalid transition: submitted -> submitted (MUST FAIL because fromStatus is pending)
	err = repo.TransitionToSubmitted(ctx, donation.ID, "0xanother")
	if err != ErrInvalidStateTransition {
		t.Fatalf("expected ErrInvalidStateTransition for duplicate submitted transition, got: %v", err)
	}

	// Step 5: Valid transition: submitted -> confirmed
	err = repo.TransitionToConfirmed(ctx, donation.ID)
	if err != nil {
		t.Fatalf("failed to transition submitted -> confirmed: %v", err)
	}

	dConfirmed, err := repo.FindByID(ctx, donation.ID)
	if err != nil {
		t.Fatalf("failed to reload donation: %v", err)
	}
	if dConfirmed.Status != StatusConfirmed {
		t.Fatalf("expected status %s, got %s", StatusConfirmed, dConfirmed.Status)
	}

	// Step 6: CRITICAL GUARD: confirmed -> failed (MUST NEVER BE ALLOWED)
	err = repo.TransitionToFailed(ctx, donation.ID)
	if err != ErrInvalidStateTransition {
		t.Fatalf("CRITICAL SECURITY VIOLATION: confirmed donation was transitioned to failed! got: %v", err)
	}

	// Verify status remains confirmed
	dAfterGuard, err := repo.FindByID(ctx, donation.ID)
	if err != nil {
		t.Fatalf("failed to reload donation: %v", err)
	}
	if dAfterGuard.Status != StatusConfirmed {
		t.Fatalf("status should remain confirmed, got %s", dAfterGuard.Status)
	}
}

func TestCommitmentAntiReplay(t *testing.T) {
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
		t.Skipf("skipping test: no campaign available in database: %v", err)
	}

	var donorID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM users LIMIT 1").Scan(&donorID)
	if err != nil {
		t.Skipf("skipping test: no user available in database: %v", err)
	}

	sharedCommitment := "replay-test-commitment-" + uuid.New().String()

	// Create first donation
	d1, err := repo.Create(
		ctx,
		campaignID,
		donorID,
		sharedCommitment,
		"100000",
		"{}",
		"key-1-"+uuid.New().String(),
	)
	if err != nil {
		t.Fatalf("failed to create first donation: %v", err)
	}
	defer func() {
		_, _ = pool.Exec(ctx, "DELETE FROM donations WHERE id = $1", d1.ID)
	}()

	// Query by campaign and commitment
	found, err := repo.FindByCampaignAndCommitment(ctx, campaignID, sharedCommitment)
	if err != nil {
		t.Fatalf("failed to find commitment: %v", err)
	}
	if found == nil || found.ID != d1.ID {
		t.Fatalf("expected to find donation %s, got %v", d1.ID, found)
	}
}

func TestReconcileAggregateMath(t *testing.T) {
	pubKey, privKey, err := paillier.GenerateKeypair(512)
	if err != nil {
		t.Fatalf("failed to generate keypair: %v", err)
	}

	amounts := []int64{100000, 200000, 300000}
	var expectedSum int64
	var ciphertexts []*big.Int

	for _, a := range amounts {
		expectedSum += a
		c, err := pubKey.Encrypt(big.NewInt(a))
		if err != nil {
			t.Fatalf("failed to encrypt: %v", err)
		}
		ciphertexts = append(ciphertexts, c)
	}

	// Reconcile by homomorphic addition
	var reconciled *big.Int
	for _, c := range ciphertexts {
		if reconciled == nil {
			reconciled = c
			continue
		}
		reconciled, err = pubKey.Add(reconciled, c)
		if err != nil {
			t.Fatalf("failed to add: %v", err)
		}
	}

	decryptedTotal, err := privKey.Decrypt(reconciled)
	if err != nil {
		t.Fatalf("failed to decrypt reconciled aggregate: %v", err)
	}

	if decryptedTotal.Int64() != expectedSum {
		t.Fatalf("reconciled total mismatch: got %d, want %d", decryptedTotal.Int64(), expectedSum)
	}
}

func TestConcurrentIdempotency(t *testing.T) {
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
		t.Skipf("skipping test: no campaign available in database: %v", err)
	}

	var donorID uuid.UUID
	err = pool.QueryRow(ctx, "SELECT id FROM users LIMIT 1").Scan(&donorID)
	if err != nil {
		t.Skipf("skipping test: no user available in database: %v", err)
	}

	sharedIdempotencyKey := "concurrent-test-" + uuid.New().String()
	numWorkers := 10

	var wg sync.WaitGroup
	var successCount int
	var conflictCount int
	var mu sync.Mutex
	var createdID uuid.UUID

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerIdx int) {
			defer wg.Done()

			d, createErr := repo.Create(
				ctx,
				campaignID,
				donorID,
				uuid.New().String(),
				"100000",
				"{}",
				sharedIdempotencyKey,
			)

			mu.Lock()
			defer mu.Unlock()

			if createErr == nil && d != nil {
				successCount++
				createdID = d.ID
			} else {
				conflictCount++
			}
		}(i)
	}

	wg.Wait()

	if createdID != uuid.Nil {
		defer func() {
			_, _ = pool.Exec(ctx, "DELETE FROM donations WHERE id = $1", createdID)
		}()
	}

	// Exactly 1 worker must succeed in inserting the unique idempotency key
	if successCount != 1 {
		t.Fatalf("expected exactly 1 insert success among concurrent requests, got %d (conflicts: %d)", successCount, conflictCount)
	}

	if conflictCount != numWorkers-1 {
		t.Fatalf("expected %d conflicts, got %d", numWorkers-1, conflictCount)
	}

	// Verify exactly 1 row exists in DB for this idempotency key
	var countInDB int
	err = pool.QueryRow(ctx, "SELECT COUNT(*) FROM donations WHERE idempotency_key = $1", sharedIdempotencyKey).Scan(&countInDB)
	if err != nil {
		t.Fatalf("failed to query count in db: %v", err)
	}
	if countInDB != 1 {
		t.Fatalf("database has %d rows for unique idempotency key, expected 1", countInDB)
	}
}



