package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/big"
	"time"

	"github.com/izagoto/zk-paillier-donation-system/internal/config"
	"github.com/izagoto/zk-paillier-donation-system/internal/crypto/paillier"
	"github.com/izagoto/zk-paillier-donation-system/internal/database"
)

type CampaignInfo struct {
	ID          string
	Title       string
	MaxDonation string
	Status      string
}

type DonationInfo struct {
	ID              string
	CampaignID      string
	DonorID         string
	Commitment      string
	EncryptedAmount string
	Status          string
	TxHash          string
	IdempotencyKey  string
	CreatedAt       time.Time
}

type ArchiveInfo struct {
	ID              string
	CampaignID      string
	DonorID         string
	Commitment      string
	EncryptedAmount string
	Status          string
	TxHash          string
	ArchiveReason   string
	CreatedAt       time.Time
	ArchivedAt      time.Time
}

func main() {
	reconcileFlag := flag.Bool("reconcile", false, "Jalankan rekonsiliasi aggregate otomatis sesuai SOP")
	cleanTestFlag := flag.Bool("clean-test", false, "Bersihkan record uji test-dup")
	flag.Parse()

	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	db, err := database.NewPool(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}
	defer db.Close()

	ctx := context.Background()

	if *cleanTestFlag {
		_, _ = db.Exec(ctx, "DELETE FROM donations WHERE commitment LIKE 'test-dup-%' OR commitment LIKE 'simulated-dup-%'")
		_, _ = db.Exec(ctx, "DELETE FROM donations_duplicate_archive WHERE commitment LIKE 'test-dup-%' OR commitment LIKE 'simulated-dup-%'")
		_, _ = db.Exec(ctx, "DELETE FROM campaign_aggregates WHERE campaign_id = 'b78d3c14-29b7-4e50-948b-b5d37264b042'")
	}

	keyManager := paillier.NewKeyManager(
		cfg.PaillierKeyPath,
		cfg.PaillierKeySize,
	)
	hasPrivateKey := false
	if err := keyManager.LoadOrGenerate(); err == nil && keyManager.PrivateKey != nil {
		hasPrivateKey = true
	}

	fmt.Println("================================================================================")
	fmt.Println("             TAHAP 1: AUDIT & VERIFIKASI BASELINE DATABASE                     ")
	fmt.Println("================================================================================")

	// 1. Schema Migration Version
	fmt.Println("\n--- 1. SKEMA & MIGRASI ---")
	var version int64
	var dirty bool
	err = db.QueryRow(ctx, "SELECT version, dirty FROM schema_migrations LIMIT 1").Scan(&version, &dirty)
	if err != nil {
		fmt.Printf("Status schema_migrations: %v\n", err)
	} else {
		fmt.Printf("Versi Skema Migrasi: %d (dirty: %v)\n", version, dirty)
	}

	// 2. Campaigns
	fmt.Println("\n--- 2. DAFTAR CAMPAIGN ---")
	campaigns := make(map[string]CampaignInfo)
	cRows, err := db.Query(ctx, "SELECT id, title, max_donation, status FROM campaigns ORDER BY created_at")
	if err != nil {
		log.Fatalf("failed to query campaigns: %v", err)
	}
	for cRows.Next() {
		var c CampaignInfo
		if err := cRows.Scan(&c.ID, &c.Title, &c.MaxDonation, &c.Status); err != nil {
			log.Fatalf("failed to scan campaign: %v", err)
		}
		campaigns[c.ID] = c
		fmt.Printf("- Campaign ID: %s | Title: %s | Max: %s | Status: %s\n", c.ID, c.Title, c.MaxDonation, c.Status)
	}
	cRows.Close()

	// 3. Donations table overview
	fmt.Println("\n--- 3. DATA DONASI (Tabel 'donations') ---")
	dRows, err := db.Query(ctx, `
		SELECT 
			id, campaign_id, donor_id, commitment, encrypted_amount, status,
			COALESCE(tx_hash, ''), COALESCE(idempotency_key, ''), created_at
		FROM donations
		ORDER BY created_at
	`)
	if err != nil {
		log.Fatalf("failed to query donations: %v", err)
	}

	var allDonations []DonationInfo
	statusCounts := make(map[string]int)

	for dRows.Next() {
		var d DonationInfo
		if err := dRows.Scan(
			&d.ID, &d.CampaignID, &d.DonorID, &d.Commitment, &d.EncryptedAmount,
			&d.Status, &d.TxHash, &d.IdempotencyKey, &d.CreatedAt,
		); err != nil {
			log.Fatalf("failed to scan donation: %v", err)
		}
		allDonations = append(allDonations, d)
		statusCounts[d.Status]++
	}
	dRows.Close()

	fmt.Printf("Total donasi tercatat: %d\n", len(allDonations))
	for st, cnt := range statusCounts {
		fmt.Printf("  * Status '%s': %d\n", st, cnt)
	}

	fmt.Println("\nRincian Setiap Donasi:")
	for i, d := range allDonations {
		decryptedStr := "N/A"
		if hasPrivateKey && d.EncryptedAmount != "" {
			cInt, ok := new(big.Int).SetString(d.EncryptedAmount, 10)
			if ok {
				decrypted, err := keyManager.PrivateKey.Decrypt(cInt)
				if err == nil {
					decryptedStr = decrypted.String()
				}
			}
		}

		txDisplay := d.TxHash
		if txDisplay == "" {
			txDisplay = "<NO_TX>"
		}
		idempDisplay := d.IdempotencyKey
		if idempDisplay == "" {
			idempDisplay = "<NULL>"
		}

		fmt.Printf("[%d] ID: %s\n", i+1, d.ID)
		fmt.Printf("    Campaign: %s\n", d.CampaignID)
		fmt.Printf("    Commitment: %s\n", d.Commitment)
		fmt.Printf("    Amount (Decrypted): %s\n", decryptedStr)
		fmt.Printf("    Status: %s | TxHash: %s\n", d.Status, txDisplay)
		fmt.Printf("    IdempotencyKey: %s | Created: %s\n", idempDisplay, d.CreatedAt.Format(time.RFC3339))
	}

	// 4. Check for duplicate commitments
	fmt.Println("\n--- 4. ANALISIS DUPLIKASI COMMITMENT DI 'donations' ---")
	dupRows, err := db.Query(ctx, `
		SELECT campaign_id, commitment, COUNT(*) as cnt
		FROM donations
		GROUP BY campaign_id, commitment
		HAVING COUNT(*) > 1
	`)
	if err != nil {
		log.Fatalf("failed to query duplicates: %v", err)
	}
	hasDuplicates := false
	for dupRows.Next() {
		hasDuplicates = true
		var campID, comm string
		var count int
		if err := dupRows.Scan(&campID, &comm, &count); err == nil {
			fmt.Printf("! TEMUAN DUPLIKAT: Campaign %s memiliki commitment %s sebanyak %d kali!\n", campID, comm, count)
		}
	}
	dupRows.Close()
	if !hasDuplicates {
		fmt.Println("Tidak ada duplikasi (campaign_id, commitment) yang aktif di tabel 'donations'.")
	}

	// 5. Check archive table
	fmt.Println("\n--- 5. TABEL ARSIP ('donations_duplicate_archive') ---")
	archRows, err := db.Query(ctx, `
		SELECT 
			id, campaign_id, donor_id, commitment, encrypted_amount, status,
			COALESCE(tx_hash, ''), archive_reason, created_at, archived_at
		FROM donations_duplicate_archive
		ORDER BY archived_at
	`)
	if err != nil {
		fmt.Printf("Error querying archive table: %v\n", err)
	} else {
		var archives []ArchiveInfo
		for archRows.Next() {
			var a ArchiveInfo
			if err := archRows.Scan(
				&a.ID, &a.CampaignID, &a.DonorID, &a.Commitment, &a.EncryptedAmount,
				&a.Status, &a.TxHash, &a.ArchiveReason, &a.CreatedAt, &a.ArchivedAt,
			); err != nil {
				log.Fatalf("failed to scan archive: %v", err)
			}
			archives = append(archives, a)
		}
		archRows.Close()

		fmt.Printf("Total record di tabel arsip: %d\n", len(archives))
		for i, a := range archives {
			fmt.Printf("[%d] Archived ID: %s | Campaign: %s\n", i+1, a.ID, a.CampaignID)
			fmt.Printf("    Commitment: %s\n", a.Commitment)
			fmt.Printf("    Status Asli: %s | TxHash: %s\n", a.Status, a.TxHash)
			fmt.Printf("    Alasan Arsip: %s\n", a.ArchiveReason)
			fmt.Printf("    Dibuat: %s | Diarsipkan: %s\n", a.CreatedAt.Format(time.RFC3339), a.ArchivedAt.Format(time.RFC3339))
		}
	}

	// 6. Aggregate reconciliation audit
	fmt.Println("\n--- 6. REKONSILIASI AGGREGATE PAILLIER PER CAMPAIGN ---")
	for campID, camp := range campaigns {
		fmt.Printf("\nKampanye: %s (%s)\n", camp.Title, campID)

		// Get stored aggregate
		var storedEncTotal string
		var updatedAt *time.Time
		err := db.QueryRow(ctx, "SELECT encrypted_total, updated_at FROM campaign_aggregates WHERE campaign_id = $1", campID).Scan(&storedEncTotal, &updatedAt)
		hasStoredAgg := (err == nil)

		// Calculate expected aggregate from confirmed donations
		var confirmedCount int
		var expectedSum big.Int
		var homomorphicEncTotal *big.Int

		for _, d := range allDonations {
			if d.CampaignID == campID && d.Status == "confirmed" {
				confirmedCount++
				cInt, ok := new(big.Int).SetString(d.EncryptedAmount, 10)
				if ok {
					if homomorphicEncTotal == nil {
						homomorphicEncTotal = new(big.Int).Set(cInt)
					} else {
						homomorphicEncTotal, _ = keyManager.PublicKey.Add(homomorphicEncTotal, cInt)
					}

					if hasPrivateKey {
						dec, err := keyManager.PrivateKey.Decrypt(cInt)
						if err == nil {
							expectedSum.Add(&expectedSum, dec)
						}
					}
				}
			}
		}

		fmt.Printf("  * Jumlah donasi confirmed di DB: %d\n", confirmedCount)
		fmt.Printf("  * Total nominal yang diharapkan: %s\n", expectedSum.String())

		if !hasStoredAgg {
			fmt.Println("  * Status di campaign_aggregates: BELUM ADA RECORD")
		} else {
			storedDecrypted := "N/A"
			if hasPrivateKey && storedEncTotal != "" && storedEncTotal != "0" {
				sInt, ok := new(big.Int).SetString(storedEncTotal, 10)
				if ok {
					dec, err := keyManager.PrivateKey.Decrypt(sInt)
					if err == nil {
						storedDecrypted = dec.String()
					}
				}
			}
			fmt.Printf("  * Total terdekripsi dari campaign_aggregates: %s\n", storedDecrypted)
			if updatedAt != nil {
				fmt.Printf("  * Terakhir diupdate: %s\n", updatedAt.Format(time.RFC3339))
			}

			if storedDecrypted == expectedSum.String() {
				fmt.Println("  * KESIMPULAN: SINKRON (Tersimpan == Diharapkan)")
			} else {
				fmt.Println("  * KESIMPULAN: TIDAK SINKRON! Nilai tersimpan berbeda dari donasi confirmed!")
				if *reconcileFlag {
					if homomorphicEncTotal != nil {
						_, err := db.Exec(ctx, `
							INSERT INTO campaign_aggregates (campaign_id, encrypted_total, updated_at)
							VALUES ($1, $2, NOW())
							ON CONFLICT (campaign_id) DO UPDATE SET encrypted_total = EXCLUDED.encrypted_total, updated_at = NOW()
						`, campID, homomorphicEncTotal.String())
						if err == nil {
							fmt.Printf("  * [REKONSILIASI BERHASIL] Aggregate diperbarui ke total donasi sah (%s).\n", expectedSum.String())
						}
					} else {
						_, _ = db.Exec(ctx, "DELETE FROM campaign_aggregates WHERE campaign_id = $1", campID)
						fmt.Println("  * [REKONSILIASI BERHASIL] Aggregate dikosongkan karena tidak ada donasi confirmed.")
					}
				}
			}
		}
	}
	fmt.Println("\n================================================================================")
}
