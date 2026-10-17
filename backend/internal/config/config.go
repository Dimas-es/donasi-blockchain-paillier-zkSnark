package config

import (
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	AppPort              string
	DatabaseURL          string
	JWTSecret            string
	PaillierKeyPath      string
	PaillierKeySize      int
	BlockchainRPCURL     string
	BlockchainContract   string
	BlockchainPrivateKey string
}

func Load() (*Config, error) {
	for _, envPath := range []string{".env", "../.env", "../../.env"} {
		_ = godotenv.Load(envPath)
	}

	keySizeStr := os.Getenv("PAILLIER_KEY_SIZE")
	if keySizeStr == "" {
		keySizeStr = "2048"
	}

	keySize, err := strconv.Atoi(keySizeStr)
	if err != nil {
		return nil, err
	}

	return &Config{
		AppPort:              os.Getenv("APP_PORT"),
		DatabaseURL:          os.Getenv("DATABASE_URL"),
		JWTSecret:            os.Getenv("JWT_SECRET"),
		PaillierKeyPath:      os.Getenv("PAILLIER_KEY_PATH"),
		PaillierKeySize:      keySize,
		BlockchainRPCURL:     os.Getenv("BLOCKCHAIN_RPC_URL"),
		BlockchainContract:   os.Getenv("BLOCKCHAIN_CONTRACT_ADDRESS"),
		BlockchainPrivateKey: os.Getenv("BLOCKCHAIN_PRIVATE_KEY"),
	}, nil
}
