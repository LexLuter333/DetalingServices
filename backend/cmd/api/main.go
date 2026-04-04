package main

import (
	"deteleng-backend/internal/config"
	"deteleng-backend/internal/database"
	"deteleng-backend/internal/handlers"
	"deteleng-backend/internal/middleware"
	"deteleng-backend/internal/repository"
	"deteleng-backend/internal/services"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	// Чтение переменного окружения .env
	if _, err := os.Stat(".env"); err == nil {
		log.Println("📄 Loading .env file...")
		if err := godotenv.Load(); err != nil {
			log.Println("⚠️  Warning: Failed to load .env file:", err)
		}
	}

	cfg := config.Load()

	if os.Getenv("GIN_MODE") == "" {
		gin.SetMode(gin.ReleaseMode)
	}

	// Инициализация базы данных
	err := database.InitDB()
	if err != nil {
		log.Fatalf("❌ Failed to initialize database: %v", err)
	}
	defer database.CloseDB()

	// Запуск миграции БД
	err = runMigrations()
	if err != nil {
		log.Fatalf("❌ Failed to run migrations: %v", err)
	}

	err = seedData()
	if err != nil {
		log.Fatalf("❌ Failed to seed data: %v", err)
	}

	// Start background job for deleting old bookings
	go func() {
		ticker := time.NewTicker(24 * time.Hour) // Run once per day
		defer ticker.Stop()
		for range ticker.C {
			repo := repository.NewDatabaseRepository()
			err := repo.DeleteOldCompletedBookings()
			if err != nil {
				log.Printf("⚠️  Error deleting old bookings: %v", err)
			} else {
				log.Println("✅ Old completed bookings deleted successfully")
			}
		}
	}()

	// Initialize repository
	repo := repository.NewDatabaseRepository()

	// Initialize services
	bookingService := services.NewBookingService(repo)
	authService := services.NewAuthService(repo)
	adminService := services.NewAdminService(repo)
	serviceService := services.NewServiceService(repo)
	reviewService := services.NewReviewService(repo)

	// Initialize handlers
	bookingHandler := handlers.NewBookingHandler(bookingService)
	authHandler := handlers.NewAuthHandler(authService)
	adminHandler := handlers.NewAdminHandler(adminService, authService)
	serviceHandler := handlers.NewServiceHandler(serviceService)
	reviewHandler := handlers.NewReviewHandler(reviewService)

	// Create Gin router
	r := gin.Default()

	// CORS configuration - allow all origins for development
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization", "Accept", "X-Requested-With"},
		ExposeHeaders:    []string{"Content-Length", "Content-Range"},
		AllowCredentials: true,
		MaxAge:           12 * 3600,
	}))

	// API routes
	api := r.Group("/api")
	{
		// Public routes
		api.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{"message": "pong"})
		})

		// Services routes (public)
		services := api.Group("/services")
		{
			services.GET("/", serviceHandler.GetPublicServices)
		}

		// Reviews routes (public)
		reviews := api.Group("/reviews")
		{
			reviews.GET("/", reviewHandler.GetPublicReviews)
		}

		// Booking routes
		bookings := api.Group("/bookings")
		{
			bookings.POST("/", bookingHandler.CreateBooking)
			bookings.GET("/", bookingHandler.GetAllBookings)
			bookings.GET("/:id", bookingHandler.GetBooking)
		}

		// Auth routes
		auth := api.Group("/auth")
		{
			auth.POST("/login", authHandler.Login)
			auth.POST("/register", authHandler.Register)
		}

		// Admin routes (protected)
		admin := api.Group("/admin")
		admin.Use(middleware.AuthMiddleware())
		{
			admin.GET("/dashboard", adminHandler.Dashboard)
			admin.GET("/bookings", adminHandler.GetAllBookings)
			admin.PUT("/bookings/:id/status", adminHandler.UpdateBookingStatus)
			admin.DELETE("/bookings/:id", adminHandler.DeleteBooking)
			admin.GET("/stats", adminHandler.GetStats)

			// Admin services management
			admin.GET("/services", serviceHandler.GetAllServices)
			admin.POST("/services", serviceHandler.CreateService)
			admin.PUT("/services/:id", serviceHandler.UpdateService)
			admin.DELETE("/services/:id", serviceHandler.DeleteService)

			// Admin reviews management
			admin.GET("/reviews", reviewHandler.GetAllReviews)
			admin.POST("/reviews", reviewHandler.CreateReview)
			admin.PUT("/reviews/:id", reviewHandler.UpdateReview)
			admin.DELETE("/reviews/:id", reviewHandler.DeleteReview)
			admin.POST("/reviews/parse", reviewHandler.ParseReviews)
			admin.GET("/reviews/stats", reviewHandler.GetReviewStats)

			// Admin review sources management
			admin.GET("/review-sources", reviewHandler.GetReviewSources)
			admin.POST("/review-sources", reviewHandler.CreateReviewSource)
			admin.PUT("/review-sources/:id", reviewHandler.UpdateReviewSource)
			admin.DELETE("/review-sources/:id", reviewHandler.DeleteReviewSource)
		}
	}

	// Start server with timeouts for production readiness
	log.Printf("🚀 Server starting on port %s", cfg.ServerPort)

	srv := &http.Server{
		Addr:              ":" + cfg.ServerPort,
		Handler:           r,
		ReadTimeout:       5 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       120 * time.Second,
		ReadHeaderTimeout: 2 * time.Second,
	}

	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("❌ Failed to start server: %v", err)
	}
}

// Migration definition
type Migration struct {
	Version string
	Name    string
	SQL     string
}

// runMigrations runs SQL migration files with tracking
func runMigrations() error {
	log.Println("📦 Running database migrations...")

	// Create migrations tracking table
	if err := database.CreateMigrationsTable(); err != nil {
		log.Fatalf("❌ Failed to create migrations table: %v", err)
	}

	// Define migrations
	migrations := []Migration{
		{
			Version: "001",
			Name:    "Create tables",
			SQL:     loadMigrationFile("database/migrations/001_create_tables.sql"),
		},
		{
			Version: "003",
			Name:    "Update reviews table",
			SQL:     loadMigrationFile("database/migrations/003_update_reviews_table.sql"),
		},
	}

	// Run migrations
	for _, migration := range migrations {
		// Check if migration was already applied
		applied, err := database.IsMigrationApplied(migration.Version)
		if err != nil {
			log.Printf("⚠️  Error checking migration %s: %v", migration.Version, err)
			continue
		}

		if applied {
			log.Printf("✅ Migration %s (%s) already applied, skipping", migration.Version, migration.Name)
			continue
		}

		log.Printf("📄 Applying migration %s: %s", migration.Version, migration.Name)

		_, err = database.DB.Exec(migration.SQL)
		if err != nil {
			log.Printf("⚠️  Error applying migration %s: %v", migration.Version, err)
			continue
		}

		// Mark migration as applied
		err = database.MarkMigrationApplied(migration.Version)
		if err != nil {
			log.Printf("⚠️  Error marking migration %s as applied: %v", migration.Version, err)
		}

		log.Printf("✅ Migration %s (%s) applied successfully", migration.Version, migration.Name)
	}

	// Verify tables exist
	verifyTablesExist()

	log.Println("✅ All migrations completed successfully")
	return nil
}

// loadMigrationFile loads a migration SQL file
func loadMigrationFile(path string) string {
	sqlFile, err := os.ReadFile(path)
	if err != nil {
		log.Printf("⚠️  Error reading migration file %s: %v", path, err)
		return ""
	}
	return string(sqlFile)
}

// verifyTablesExist checks if all required tables exist
func verifyTablesExist() {
	tables := []string{"users", "services", "bookings", "reviews"}

	for _, table := range tables {
		exists, err := database.TableExists(table)
		if err != nil {
			log.Printf("⚠️  Error checking table %s: %v", table, err)
			continue
		}
		if !exists {
			log.Printf("⚠️  Table %s does not exist!", table)
			continue
		}
		log.Printf("✅ Table %s exists", table)
	}
}

// seedData seeds the database with default data if needed
func seedData() error {
	log.Println("🌱 Seeding default data...")

	// Load and execute seed data SQL
	seedSQL := loadMigrationFile("database/migrations/002_seed_data.sql")
	if seedSQL == "" {
		log.Println("⚠️  Seed data file not found")
		return nil
	}

	_, err := database.DB.Exec(seedSQL)
	if err != nil {
		log.Printf("⚠️  Error seeding data: %v", err)
		return err
	}

	// Verify seeded data
	verifySeedData()

	log.Println("✅ Default data seeded successfully")
	return nil
}

// verifySeedData checks if seed data was inserted correctly
func verifySeedData() {
	// Check admin user
	var userCount int
	err := database.DB.QueryRow("SELECT COUNT(*) FROM users WHERE email = $1", "admin@deteleng.com").Scan(&userCount)
	if err != nil {
		log.Printf("⚠️  Error checking admin user: %v", err)
	} else if userCount > 0 {
		log.Println("✅ Admin user exists (admin@deteleng.com)")
	}

	// Check services
	var serviceCount int
	err = database.DB.QueryRow("SELECT COUNT(*) FROM services").Scan(&serviceCount)
	if err != nil {
		log.Printf("⚠️  Error checking services: %v", err)
	} else {
		log.Printf("✅ Services count: %d", serviceCount)
		if serviceCount == 0 {
			log.Println("⚠️  Warning: No services found in database!")
		}
	}
}
