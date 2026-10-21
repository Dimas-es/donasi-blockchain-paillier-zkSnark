package donation

import (
	"context"
	"errors"
	"testing"

	"github.com/google/uuid"

	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/zk"
)

func TestCreate_RequiresIdempotencyKey(t *testing.T) {
	s := &Service{}

	_, replay, err := s.Create(
		context.Background(),
		uuid.New(),
		uuid.New(),
		"1000",
		"0xabc",
		zk.Proof{},
		"   ",
	)
	if !errors.Is(err, ErrIdempotencyKeyRequired) {
		t.Fatalf("expected ErrIdempotencyKeyRequired, got %v", err)
	}
	if replay {
		t.Fatal("replay should be false")
	}
}
