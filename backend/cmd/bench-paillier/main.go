package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"math/big"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"github.com/izagoto/zk-paillier-donation-system/internal/crypto/paillier"
)

type StatResult struct {
	Operation string  `json:"operation"`
	Count     int     `json:"count"`
	MeanMs    float64 `json:"mean_ms"`
	StdDevMs  float64 `json:"std_dev_ms"`
	MinMs     float64 `json:"min_ms"`
	MaxMs     float64 `json:"max_ms"`
}

func calcStats(opName string, durations []float64) StatResult {
	n := len(durations)
	if n == 0 {
		return StatResult{Operation: opName}
	}
	var sum float64
	min := durations[0]
	max := durations[0]
	for _, d := range durations {
		sum += d
		if d < min {
			min = d
		}
		if d > max {
			max = d
		}
	}
	mean := sum / float64(n)

	var varianceSum float64
	for _, d := range durations {
		varianceSum += (d - mean) * (d - mean)
	}
	stdDev := math.Sqrt(varianceSum / float64(n))

	return StatResult{
		Operation: opName,
		Count:     n,
		MeanMs:    mean,
		StdDevMs:  stdDev,
		MinMs:     min,
		MaxMs:     max,
	}
}

func main() {
	outDir := filepath.Join("..", "assets", "benchmark")
	if err := os.MkdirAll(outDir, 0755); err != nil {
		fmt.Printf("Error creating benchmark dir: %v\n", err)
		return
	}

	csvPath := filepath.Join(outDir, "benchmark_paillier_raw.csv")
	file, err := os.Create(csvPath)
	if err != nil {
		fmt.Printf("Error creating csv: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{"iteration", "operation", "duration_ns", "duration_ms"})

	fmt.Println("=== RUNNING EMPIRICAL PAILLIER BENCHMARKS (RAW ITERATIONS) ===")

	// 1. KeyGen 512 (50 iterations)
	fmt.Print("Running KeyGen 512-bit (50 iterations)... ")
	durKeyGen512 := make([]float64, 50)
	for i := 0; i < 50; i++ {
		start := time.Now()
		_, _, _ = paillier.GenerateKeypair(512)
		elapsed := time.Since(start)
		ms := float64(elapsed.Nanoseconds()) / 1e6
		durKeyGen512[i] = ms
		writer.Write([]string{strconv.Itoa(i + 1), "KeyGen-512", strconv.FormatInt(elapsed.Nanoseconds(), 10), fmt.Sprintf("%.4f", ms)})
	}
	fmt.Println("DONE")

	// 2. KeyGen 2048 (30 iterations)
	fmt.Print("Running KeyGen 2048-bit (30 iterations)... ")
	durKeyGen2048 := make([]float64, 30)
	for i := 0; i < 30; i++ {
		start := time.Now()
		_, _, _ = paillier.GenerateKeypair(2048)
		elapsed := time.Since(start)
		ms := float64(elapsed.Nanoseconds()) / 1e6
		durKeyGen2048[i] = ms
		writer.Write([]string{strconv.Itoa(i + 1), "KeyGen-2048", strconv.FormatInt(elapsed.Nanoseconds(), 10), fmt.Sprintf("%.4f", ms)})
	}
	fmt.Println("DONE")

	// Pre-generate 2048-bit keypair for subsequent operations
	pk, sk, err := paillier.GenerateKeypair(2048)
	if err != nil {
		fmt.Printf("KeyGen failed: %v\n", err)
		return
	}

	// 3. Encrypt 2048 (100 iterations)
	fmt.Print("Running Encrypt 2048-bit (100 iterations)... ")
	durEncrypt := make([]float64, 100)
	sampleMsg := big.NewInt(50000)
	for i := 0; i < 100; i++ {
		start := time.Now()
		_, _ = pk.Encrypt(sampleMsg)
		elapsed := time.Since(start)
		ms := float64(elapsed.Nanoseconds()) / 1e6
		durEncrypt[i] = ms
		writer.Write([]string{strconv.Itoa(i + 1), "Encrypt-2048", strconv.FormatInt(elapsed.Nanoseconds(), 10), fmt.Sprintf("%.4f", ms)})
	}
	fmt.Println("DONE")

	// 4. Add 2048 (100 iterations of 1000 batch ops to get accurate sub-millisecond precision)
	fmt.Print("Running Homomorphic Add 2048-bit (100 batches of 1,000 ops)... ")
	durAdd := make([]float64, 100)
	c1, _ := pk.Encrypt(big.NewInt(10000))
	c2, _ := pk.Encrypt(big.NewInt(25000))
	for i := 0; i < 100; i++ {
		start := time.Now()
		for b := 0; b < 1000; b++ {
			_, _ = pk.Add(c1, c2)
		}
		elapsed := time.Since(start)
		nsPerOp := elapsed.Nanoseconds() / 1000
		msPerOp := float64(nsPerOp) / 1e6
		durAdd[i] = msPerOp
		writer.Write([]string{strconv.Itoa(i + 1), "Add-2048", strconv.FormatInt(nsPerOp, 10), fmt.Sprintf("%.6f", msPerOp)})
	}
	fmt.Println("DONE")

	// 5. Decrypt 2048 (100 iterations)
	fmt.Print("Running Decrypt 2048-bit (100 iterations)... ")
	durDecrypt := make([]float64, 100)
	cipherSample, _ := pk.Encrypt(big.NewInt(75000))
	for i := 0; i < 100; i++ {
		start := time.Now()
		_, _ = sk.Decrypt(cipherSample)
		elapsed := time.Since(start)
		ms := float64(elapsed.Nanoseconds()) / 1e6
		durDecrypt[i] = ms
		writer.Write([]string{strconv.Itoa(i + 1), "Decrypt-2048", strconv.FormatInt(elapsed.Nanoseconds(), 10), fmt.Sprintf("%.4f", ms)})
	}
	fmt.Println("DONE")

	fmt.Println("\n=== SUMMARY OF EMPIRICAL STATISTICAL RESULTS ===")
	stats := []StatResult{
		calcStats("KeyGen 512-bit", durKeyGen512),
		calcStats("KeyGen 2048-bit", durKeyGen2048),
		calcStats("Encrypt 2048-bit", durEncrypt),
		calcStats("Homomorphic Add 2048-bit", durAdd),
		calcStats("Decrypt 2048-bit", durDecrypt),
	}

	for _, s := range stats {
		fmt.Printf("%-26s | N=%3d | Mean: %9.4f ms | SD: %7.4f ms | Min: %8.4f ms | Max: %8.4f ms\n",
			s.Operation, s.Count, s.MeanMs, s.StdDevMs, s.MinMs, s.MaxMs)
	}

	fmt.Printf("\nRaw CSV saved successfully to: %s\n", csvPath)
}
