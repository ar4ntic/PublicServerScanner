package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
	"publicscannerapi/internal/api/handlers"
	"publicscannerapi/internal/api/middleware"
	"publicscannerapi/internal/config"
	"publicscannerapi/internal/repository"
	"publicscannerapi/internal/services"
)

func main() {
	// Load configuration
	cfg := config.Load()

	// Initialize database connection
	db, err := initDatabase(cfg)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	log.Println("✅ Database connected successfully")

	// Initialize repositories
	userRepo := repository.NewUserRepository(db)
	targetRepo := repository.NewTargetRepository(db)
	scanRepo := repository.NewScanRepository(db)
	reportRepo := repository.NewReportRepository(db)

	// Initialize services
	authService := services.NewAuthService(
		userRepo,
		cfg.JWT.Secret,
		cfg.JWT.AccessTokenTTL,
		cfg.JWT.RefreshTokenTTL,
	)
	targetService := services.NewTargetService(targetRepo)
	scanService := services.NewScanService(scanRepo, targetRepo, cfg.Redis.URL())
	reportService := services.NewReportService(reportRepo, scanRepo, cfg.App.StoragePath)

	// Initialize handlers
	authHandler := handlers.NewAuthHandler(authService)
	targetHandler := handlers.NewTargetHandler(targetService)
	scanHandler := handlers.NewScanHandler(scanService)
	reportHandler := handlers.NewReportHandler(reportService)

	// Initialize Gin router
	router := gin.Default()

	// CORS middleware (allow frontend to make requests)
	router.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})

	// Health check endpoint
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":  "ok",
			"service": "PublicScanner API",
		})
	})

	// API v1 routes
	v1 := router.Group("/api/v1")
	{
		// Public auth routes
		auth := v1.Group("/auth")
		{
			auth.POST("/register", authHandler.Register)
			auth.POST("/login", authHandler.Login)
			auth.POST("/refresh", authHandler.RefreshToken)
		}

		// Protected routes (require authentication)
		protected := v1.Group("/")
		protected.Use(middleware.AuthMiddleware(cfg.JWT.Secret))
		{
			// User routes
			users := protected.Group("/users")
			{
				users.GET("/me", authHandler.GetCurrentUser)
			}

			// Target routes
			targets := protected.Group("/targets")
			{
				targets.GET("", targetHandler.List)
				targets.POST("", targetHandler.Create)
				targets.GET("/:id", targetHandler.Get)
				targets.PATCH("/:id", targetHandler.Update)
				targets.DELETE("/:id", targetHandler.Delete)
			}

			// Scan routes
			scans := protected.Group("/scans")
			{
				scans.GET("", scanHandler.List)
				scans.POST("", scanHandler.Create)
				scans.GET("/:id", scanHandler.Get)
				scans.GET("/:id/results", scanHandler.GetResults)
				scans.POST("/:id/cancel", scanHandler.Cancel)
			}

			// Report routes
			reports := protected.Group("/reports")
			{
				reports.GET("", reportHandler.List)
				reports.POST("/generate", reportHandler.Generate)
				reports.GET("/:id", reportHandler.Get)
				reports.GET("/:id/download", reportHandler.Download)
				reports.DELETE("/:id", reportHandler.Delete)
			}
		}
	}

	// Start server
	addr := fmt.Sprintf(":%s", cfg.Server.Port)
	log.Printf("🚀 Server starting on %s", addr)
	if err := router.Run(addr); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

// initDatabase initializes the database connection
func initDatabase(cfg *config.Config) (*sql.DB, error) {
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		cfg.Database.Host,
		cfg.Database.Port,
		cfg.Database.User,
		cfg.Database.Password,
		cfg.Database.DBName,
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, err
	}

	// Test connection
	if err := db.Ping(); err != nil {
		return nil, err
	}

	// Set connection pool settings
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(5)
	db.SetConnMaxLifetime(5 * time.Minute)

	return db, nil
}
