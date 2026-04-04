package database

import (
	"database/sql"
	"log"
	"os"
	"strconv"
	"time"

	_ "github.com/lib/pq"
)

var DB *sql.DB

func parseEnvInt(name string, defaultValue int) int {
	value := os.Getenv(name)
	if value == "" {
		return defaultValue
	}
	parsed, err := strconv.Atoi(value)
	if err != nil || parsed <= 0 {
		return defaultValue
	}
	return parsed
}

func InitDB() error {
	var err error

	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		log.Fatal("❌ DATABASE_URL environment variable is required. Please set it in your .env file.")
	}

	DB, err = sql.Open("postgres", connStr)
	if err != nil {
		return err
	}

	DB.SetMaxOpenConns(parseEnvInt("DB_MAX_OPEN_CONNS", 100))
	DB.SetMaxIdleConns(parseEnvInt("DB_MAX_IDLE_CONNS", 25))
	DB.SetConnMaxLifetime(time.Duration(parseEnvInt("DB_CONN_MAX_LIFETIME_MINUTES", 15)) * time.Minute)

	if err = DB.Ping(); err != nil {
		return err
	}

	log.Println("✅ Database connection established")
	return nil
}

func CloseDB() error {
	if DB != nil {
		return DB.Close()
	}
	return nil
}
