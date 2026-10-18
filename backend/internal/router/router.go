package router

import (
	"time"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/auth"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/blockchain"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/campaign"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/crypto/paillier"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/donation"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/middleware"
	"github.com/Dimas-es/donasi-blockchain-paillier-zkSnark/internal/zk"
)

func Setup(
	db *pgxpool.Pool,
	jwtSecret string,
	paillierPublicKey *paillier.PublicKey,
	paillierPrivateKey *paillier.PrivateKey,
	zkVerifier *zk.Verifier,
	zkProver *zk.Prover,
	blockchainRegistry *blockchain.Registry,
	blockchainSigner *blockchain.Signer,
) *gin.Engine {
	r := gin.Default()
	r.Use(middleware.CORS())

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status": "ok",
		})
	})

	userRepository := auth.NewUserRepository(db)
	authService := auth.NewService(userRepository)

	jwtManager := auth.NewJWTManager(
		jwtSecret,
		24*time.Hour,
	)

	authHandler := auth.NewHandler(
		authService,
		jwtManager,
	)

	campaignRepository := campaign.NewRepository(db)
	campaignService := campaign.NewService(
		campaignRepository,
		blockchainRegistry,
		blockchainSigner,
	)
	campaignHandler := campaign.NewHandler(campaignService)

	donationRepository := donation.NewRepository(db)
	donationService := donation.NewService(
		donationRepository,
		campaignRepository,
		paillierPublicKey,
		paillierPrivateKey,
		zkVerifier,
		zkProver,
		blockchainRegistry,
		blockchainSigner,
	)
	donationHandler := donation.NewHandler(donationService)

	api := r.Group("/api")
	{
		authRoutes := api.Group("/auth")
		{
			authRoutes.POST("/register", authHandler.Register)
			authRoutes.POST("/login", authHandler.Login)

			protected := authRoutes.Group("")
			protected.Use(auth.AuthMiddleware(jwtManager))
			{
				protected.GET("/me", authHandler.Me)
			}
		}

		campaignRoutes := api.Group("/campaigns")
		{
			campaignRoutes.GET("", campaignHandler.FindAll)
			campaignRoutes.GET(
				"/:id/donations",
				donationHandler.FindByCampaignID,
			)
			campaignRoutes.GET(
				"/:id/aggregate",
				donationHandler.GetCampaignAggregate,
			)
			campaignRoutes.GET("/:id", campaignHandler.FindByID)

			protectedCampaignRoutes := campaignRoutes.Group("")
			protectedCampaignRoutes.Use(auth.AuthMiddleware(jwtManager))
			{
				protectedCampaignRoutes.POST("", campaignHandler.Create)
			}
		}

		donationRoutes := api.Group("/donations")
		{
			donationRoutes.GET("/:id", donationHandler.FindByID)

			protectedDonationRoutes := donationRoutes.Group("")
			protectedDonationRoutes.Use(auth.AuthMiddleware(jwtManager))
			{
				protectedDonationRoutes.POST("", donationHandler.Create)
				protectedDonationRoutes.POST(
					"/generate-proof",
					donationHandler.GenerateProof,
				)
			}
		}
	}

	return r
}
