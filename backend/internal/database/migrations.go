package database

import (
	"log"
)

func CreateMigrationsTable() error {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS schema_migrations (
			version TEXT PRIMARY KEY,
			applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		return err
	}
	log.Println("✅ Migrations tracking table ready")
	return nil
}

func IsMigrationApplied(version string) (bool, error) {
	var exists bool
	err := DB.QueryRow(`
		SELECT EXISTS(SELECT 1 FROM schema_migrations WHERE version = $1)
	`, version).Scan(&exists)
	if err != nil {
		return false, err
	}
	return exists, nil
}

func MarkMigrationApplied(version string) error {
	_, err := DB.Exec(`
		INSERT INTO schema_migrations (version) VALUES ($1)
		ON CONFLICT (version) DO NOTHING
	`, version)
	return err
}

func TableExists(tableName string) (bool, error) {
	var exists bool
	err := DB.QueryRow(`
		SELECT EXISTS (
			SELECT FROM information_schema.tables 
			WHERE table_schema = 'public' 
			AND table_name = $1
		)
	`, tableName).Scan(&exists)
	return exists, err
}

func TableHasData(tableName string) (bool, error) {
	var count int
	err := DB.QueryRow(`SELECT COUNT(*) FROM ` + tableName).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}
