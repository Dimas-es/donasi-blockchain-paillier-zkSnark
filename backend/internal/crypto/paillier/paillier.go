package paillier

import (
	"crypto/rand"
	"errors"
	"math/big"
)

type PublicKey struct {
	N  *big.Int
	N2 *big.Int
	G  *big.Int
}

type PrivateKey struct {
	PublicKey
	Lambda *big.Int
	Mu     *big.Int
}

func GenerateKeypair(bits int) (*PublicKey, *PrivateKey, error) {
	if bits < 512 {
		return nil, nil, errors.New("key size must be at least 512 bits")
	}

	p, err := rand.Prime(rand.Reader, bits/2)
	if err != nil {
		return nil, nil, err
	}

	q, err := rand.Prime(rand.Reader, bits/2)
	if err != nil {
		return nil, nil, err
	}

	for p.Cmp(q) == 0 {
		q, err = rand.Prime(rand.Reader, bits/2)
		if err != nil {
			return nil, nil, err
		}
	}

	n := new(big.Int).Mul(p, q)
	n2 := new(big.Int).Mul(n, n)

	g := new(big.Int).Add(n, big.NewInt(1))

	pMinusOne := new(big.Int).Sub(p, big.NewInt(1))
	qMinusOne := new(big.Int).Sub(q, big.NewInt(1))

	lambda := lcm(pMinusOne, qMinusOne)

	gLambda := new(big.Int).Exp(g, lambda, n2)

	lValue := new(big.Int).Sub(gLambda, big.NewInt(1))
	lValue.Div(lValue, n)

	mu := new(big.Int).ModInverse(lValue, n)
	if mu == nil {
		return nil, nil, errors.New("failed to calculate modular inverse")
	}

	publicKey := &PublicKey{
		N:  n,
		N2: n2,
		G:  g,
	}

	privateKey := &PrivateKey{
		PublicKey: *publicKey,
		Lambda:    lambda,
		Mu:        mu,
	}

	return publicKey, privateKey, nil
}

func (pk *PublicKey) Encrypt(message *big.Int) (*big.Int, error) {
	if message == nil {
		return nil, errors.New("message cannot be nil")
	}

	if message.Sign() < 0 {
		return nil, errors.New("message cannot be negative")
	}

	if message.Cmp(pk.N) >= 0 {
		return nil, errors.New("message must be smaller than n")
	}

	r, err := randomCoprime(pk.N)
	if err != nil {
		return nil, err
	}

	gm := new(big.Int).Exp(pk.G, message, pk.N2)
	rn := new(big.Int).Exp(r, pk.N, pk.N2)

	ciphertext := new(big.Int).Mul(gm, rn)
	ciphertext.Mod(ciphertext, pk.N2)

	return ciphertext, nil
}

func (sk *PrivateKey) Decrypt(ciphertext *big.Int) (*big.Int, error) {
	if ciphertext == nil {
		return nil, errors.New("ciphertext cannot be nil")
	}

	if ciphertext.Sign() < 0 {
		return nil, errors.New("ciphertext cannot be negative")
	}

	if ciphertext.Cmp(sk.N2) >= 0 {
		return nil, errors.New("ciphertext must be smaller than n²")
	}

	u := new(big.Int).Exp(
		ciphertext,
		sk.Lambda,
		sk.N2,
	)

	lValue := new(big.Int).Sub(u, big.NewInt(1))
	lValue.Div(lValue, sk.N)

	message := new(big.Int).Mul(lValue, sk.Mu)
	message.Mod(message, sk.N)

	return message, nil
}

func (pk *PublicKey) Add(
	ciphertext1 *big.Int,
	ciphertext2 *big.Int,
) (*big.Int, error) {
	if ciphertext1 == nil || ciphertext2 == nil {
		return nil, errors.New("ciphertexts cannot be nil")
	}

	if ciphertext1.Sign() < 0 || ciphertext2.Sign() < 0 {
		return nil, errors.New("ciphertexts cannot be negative")
	}

	if ciphertext1.Cmp(pk.N2) >= 0 || ciphertext2.Cmp(pk.N2) >= 0 {
		return nil, errors.New("ciphertexts must be smaller than n²")
	}

	result := new(big.Int).Mul(ciphertext1, ciphertext2)
	result.Mod(result, pk.N2)

	return result, nil
}

// EncryptWithRandomness performs Paillier encryption with a specific randomness r.
// Useful for reproducible tests and opening (M, R) verification schemes.
func (pk *PublicKey) EncryptWithRandomness(message, r *big.Int) (*big.Int, error) {
	if message == nil || r == nil {
		return nil, errors.New("inputs cannot be nil")
	}

	if message.Sign() < 0 {
		return nil, errors.New("message cannot be negative")
	}

	if message.Cmp(pk.N) >= 0 {
		return nil, errors.New("message must be smaller than n")
	}

	// c = g^m * r^n mod n^2
	gm := new(big.Int).Exp(pk.G, message, pk.N2)
	rn := new(big.Int).Exp(r, pk.N, pk.N2)

	ciphertext := new(big.Int).Mul(gm, rn)
	ciphertext.Mod(ciphertext, pk.N2)

	return ciphertext, nil
}

// VerifyOpening performs zero-knowledge public opening verification on aggregated ciphertext:
// Checks congruence: c_agg == (1 + M*n) * R^n mod n^2 using only the public key.
// Returns true if M and R correctly open c_agg without requiring the private key.
func (pk *PublicKey) VerifyOpening(cAgg, m, r *big.Int) bool {
	if cAgg == nil || m == nil || r == nil {
		return false
	}

	if cAgg.Sign() < 0 || cAgg.Cmp(pk.N2) >= 0 {
		return false
	}

	if m.Sign() < 0 || m.Cmp(pk.N) >= 0 {
		return false
	}

	if r.Sign() <= 0 || r.Cmp(pk.N) >= 0 {
		return false
	}

	// Term 1: (1 + M*n) mod n^2
	onePlusMn := new(big.Int).Mul(m, pk.N)
	onePlusMn.Add(onePlusMn, big.NewInt(1))
	onePlusMn.Mod(onePlusMn, pk.N2)

	// Term 2: R^n mod n^2
	rn := new(big.Int).Exp(r, pk.N, pk.N2)

	// Expected: (1 + M*n) * R^n mod n^2
	expected := new(big.Int).Mul(onePlusMn, rn)
	expected.Mod(expected, pk.N2)

	return cAgg.Cmp(expected) == 0
}

func lcm(a, b *big.Int) *big.Int {
	gcd := new(big.Int).GCD(nil, nil, a, b)

	result := new(big.Int).Mul(a, b)
	result.Div(result, gcd)

	return result
}

func randomCoprime(n *big.Int) (*big.Int, error) {
	for {
		r, err := rand.Int(rand.Reader, n)
		if err != nil {
			return nil, err
		}

		if r.Sign() == 0 {
			continue
		}

		gcd := new(big.Int).GCD(nil, nil, r, n)

		if gcd.Cmp(big.NewInt(1)) == 0 {
			return r, nil
		}
	}
}
