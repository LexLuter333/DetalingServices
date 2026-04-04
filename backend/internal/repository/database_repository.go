package repository

import (
	"context"
	"database/sql"
	"deteleng-backend/internal/database"
	"deteleng-backend/internal/models"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type DatabaseRepository struct {
	db *sql.DB
}

func (r *DatabaseRepository) ctxWithTimeout() (context.Context, context.CancelFunc) {
	return context.WithTimeout(context.Background(), 5*time.Second)
}

func NewDatabaseRepository() *DatabaseRepository {
	return &DatabaseRepository{
		db: database.DB,
	}
}

func (r *DatabaseRepository) GetAllServices() ([]models.Service, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	rows, err := r.db.QueryContext(ctx, `
		SELECT id, name, description, price, duration, available, created_at, updated_at
		FROM services ORDER BY name
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var services []models.Service
	for rows.Next() {
		var s models.Service
		err := rows.Scan(&s.ID, &s.Name, &s.Description, &s.Price, &s.Duration, &s.Available, &s.CreatedAt, &s.UpdatedAt)
		if err != nil {
			return nil, err
		}
		services = append(services, s)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}
	return services, nil
}

func (r *DatabaseRepository) GetService(id string) (*models.Service, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	var s models.Service
	err := r.db.QueryRowContext(ctx, `
		SELECT id, name, description, price, duration, available, created_at, updated_at
		FROM services WHERE id = $1
	`, id).Scan(&s.ID, &s.Name, &s.Description, &s.Price, &s.Duration, &s.Available, &s.CreatedAt, &s.UpdatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("service not found")
		}
		return nil, err
	}
	return &s, nil
}

func (r *DatabaseRepository) CreateService(service *models.Service) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	service.ID = uuid.New().String()
	service.CreatedAt = time.Now()
	service.UpdatedAt = time.Now()

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO services (id, name, description, price, duration, available, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`, service.ID, service.Name, service.Description, service.Price, service.Duration, service.Available, service.CreatedAt, service.UpdatedAt)
	return err
}

func (r *DatabaseRepository) UpdateService(service *models.Service) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	service.UpdatedAt = time.Now()
	_, err := r.db.ExecContext(ctx, `
		UPDATE services
		SET name = $1, description = $2, price = $3, duration = $4, available = $5, updated_at = $6
		WHERE id = $7
	`, service.Name, service.Description, service.Price, service.Duration, service.Available, service.UpdatedAt, service.ID)
	return err
}

func (r *DatabaseRepository) DeleteService(id string) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	_, err := r.db.ExecContext(ctx, "DELETE FROM services WHERE id = $1", id)
	return err
}

func (r *DatabaseRepository) CreateBooking(booking *models.Booking) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	booking.ID = uuid.New().String()
	booking.CreatedAt = time.Now()
	booking.UpdatedAt = time.Now()
	if booking.Status == "" {
		booking.Status = models.StatusPending
	}

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO bookings (id, customer_name, customer_phone, car_brand, car_model, service_id, service_name, price, status, comment, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
	`, booking.ID, booking.CustomerName, booking.CustomerPhone, booking.CarBrand, booking.CarModel, booking.ServiceID, booking.ServiceName, booking.Price, booking.Status, booking.Comment, booking.CreatedAt, booking.UpdatedAt)
	return err
}

func (r *DatabaseRepository) GetBooking(id string) (*models.Booking, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	var b models.Booking
	err := r.db.QueryRowContext(ctx, `
		SELECT id, customer_name, customer_phone, car_brand, car_model, service_id, service_name, price, status, comment, created_at, updated_at
		FROM bookings WHERE id = $1
	`, id).Scan(&b.ID, &b.CustomerName, &b.CustomerPhone, &b.CarBrand, &b.CarModel, &b.ServiceID, &b.ServiceName, &b.Price, &b.Status, &b.Comment, &b.CreatedAt, &b.UpdatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("booking not found")
		}
		return nil, err
	}
	return &b, nil
}

func (r *DatabaseRepository) GetAllBookings(limit int) ([]models.Booking, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	query := `
		SELECT id, customer_name, customer_phone, car_brand, car_model, service_id, service_name, price, status, comment, created_at, updated_at
		FROM bookings ORDER BY created_at DESC
	`
	var rows *sql.Rows
	var err error
	if limit > 0 {
		query += " LIMIT $1"
		rows, err = r.db.QueryContext(ctx, query, limit)
	} else {
		rows, err = r.db.QueryContext(ctx, query)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var bookings []models.Booking
	for rows.Next() {
		var b models.Booking
		err := rows.Scan(&b.ID, &b.CustomerName, &b.CustomerPhone, &b.CarBrand, &b.CarModel, &b.ServiceID, &b.ServiceName, &b.Price, &b.Status, &b.Comment, &b.CreatedAt, &b.UpdatedAt)
		if err != nil {
			return nil, err
		}
		bookings = append(bookings, b)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}
	return bookings, nil
}

func (r *DatabaseRepository) UpdateBooking(booking *models.Booking) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	booking.UpdatedAt = time.Now()
	_, err := r.db.ExecContext(ctx, `
		UPDATE bookings
		SET customer_name = $1, customer_phone = $2, car_brand = $3, car_model = $4, service_id = $5, service_name = $6, price = $7, status = $8, comment = $9, updated_at = $10
		WHERE id = $11
	`, booking.CustomerName, booking.CustomerPhone, booking.CarBrand, booking.CarModel, booking.ServiceID, booking.ServiceName, booking.Price, booking.Status, booking.Comment, booking.UpdatedAt, booking.ID)
	return err
}

func (r *DatabaseRepository) DeleteBooking(id string) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	_, err := r.db.ExecContext(ctx, "DELETE FROM bookings WHERE id = $1", id)
	return err
}

func (r *DatabaseRepository) DeleteOldCompletedBookings() error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	_, err := r.db.ExecContext(ctx, `
		DELETE FROM bookings 
		WHERE status = $1 
		AND created_at < NOW() - INTERVAL '7 days'
	`, models.StatusCompleted)
	return err
}

func (r *DatabaseRepository) GetUserByEmail(email string) (*models.User, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	var u models.User
	err := r.db.QueryRowContext(ctx, `
		SELECT id, email, password, role, created_at
		FROM users WHERE email = $1
	`, email).Scan(&u.ID, &u.Email, &u.Password, &u.Role, &u.CreatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("user not found")
		}
		return nil, err
	}
	return &u, nil
}

func (r *DatabaseRepository) GetUserByID(id string) (*models.User, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	var u models.User
	err := r.db.QueryRowContext(ctx, `
		SELECT id, email, password, role, created_at
		FROM users WHERE id = $1
	`, id).Scan(&u.ID, &u.Email, &u.Password, &u.Role, &u.CreatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("user not found")
		}
		return nil, err
	}
	return &u, nil
}

func (r *DatabaseRepository) CreateUser(user *models.User) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	user.ID = uuid.New().String()
	user.CreatedAt = time.Now()

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO users (id, email, password, role, created_at)
		VALUES ($1, $2, $3, $4, $5)
	`, user.ID, user.Email, user.Password, user.Role, user.CreatedAt)
	if err != nil {
		if err.Error() == "pq: duplicate key value violates unique constraint" {
			return errors.New("user already exists")
		}
		return err
	}
	return nil
}

// ============ REVIEW OPERATIONS ============

func (r *DatabaseRepository) GetAllReviews(limit int) ([]models.Review, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	query := `
		SELECT id, name, car_brand, car_model, rating, text, created_at
		FROM reviews ORDER BY created_at DESC
	`
	var rows *sql.Rows
	var err error
	if limit > 0 {
		query += ` LIMIT $1`
		rows, err = r.db.QueryContext(ctx, query, limit)
	} else {
		rows, err = r.db.QueryContext(ctx, query)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var reviews []models.Review
	for rows.Next() {
		var rev models.Review
		err := rows.Scan(&rev.ID, &rev.Name, &rev.CarBrand, &rev.CarModel, &rev.Rating, &rev.Text, &rev.CreatedAt)
		if err != nil {
			return nil, err
		}
		reviews = append(reviews, rev)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}
	return reviews, nil
}

func (r *DatabaseRepository) GetPublicReviews(limit int) ([]models.Review, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	query := `
		SELECT id, name, car_brand, car_model, rating, text, created_at
		FROM reviews
		ORDER BY created_at DESC
	`
	var rows *sql.Rows
	var err error
	if limit > 0 {
		query += ` LIMIT $1`
		rows, err = r.db.QueryContext(ctx, query, limit)
	} else {
		rows, err = r.db.QueryContext(ctx, query)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var reviews []models.Review
	for rows.Next() {
		var rev models.Review
		err := rows.Scan(&rev.ID, &rev.Name, &rev.CarBrand, &rev.CarModel, &rev.Rating, &rev.Text, &rev.CreatedAt)
		if err != nil {
			return nil, err
		}
		reviews = append(reviews, rev)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}
	return reviews, nil
}

func (r *DatabaseRepository) CreateReview(review *models.Review) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	review.ID = uuid.New().String()
	review.CreatedAt = time.Now()

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO reviews (id, name, car_brand, car_model, rating, text, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
	`, review.ID, review.Name, review.CarBrand, review.CarModel, review.Rating, review.Text, review.CreatedAt)
	return err
}

func (r *DatabaseRepository) UpdateReview(review *models.Review) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	_, err := r.db.ExecContext(ctx, `
		UPDATE reviews
		SET name = $1, car_brand = $2, car_model = $3, rating = $4, text = $5
		WHERE id = $6
	`, review.Name, review.CarBrand, review.CarModel, review.Rating, review.Text, review.ID)
	return err
}

func (r *DatabaseRepository) DeleteReview(id string) error {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	_, err := r.db.ExecContext(ctx, "DELETE FROM reviews WHERE id = $1", id)
	return err
}

func (r *DatabaseRepository) GetReviewStats() (*models.ReviewStats, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	stats := &models.ReviewStats{
		RatingBreakdown: make(map[int]int64),
	}

	query := `
		SELECT COUNT(*) AS total, COALESCE(AVG(rating), 0) AS average
		FROM reviews
	`
	if err := r.db.QueryRowContext(ctx, query).Scan(&stats.TotalReviews, &stats.AverageRating); err != nil {
		return nil, err
	}

	rows, err := r.db.QueryContext(ctx, `
		SELECT rating, COUNT(*)
		FROM reviews
		GROUP BY rating
		ORDER BY rating DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var rating int
		var count int64
		if err := rows.Scan(&rating, &count); err != nil {
			return nil, err
		}
		stats.RatingBreakdown[rating] = count
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	recent, err := r.GetAllReviews(10)
	if err != nil {
		return nil, err
	}
	stats.RecentReviews = recent

	return stats, nil
}

func (r *DatabaseRepository) GetDashboardStats() (*models.DashboardStats, error) {
	ctx, cancel := r.ctxWithTimeout()
	defer cancel()

	stats := &models.DashboardStats{
		StatusBreakdown: make(map[models.BookingStatus]int64),
	}

	query := `
		SELECT COUNT(*) AS total,
		       COUNT(*) FILTER (WHERE status = 'pending') AS pending,
		       COUNT(*) FILTER (WHERE status = 'confirmed') AS confirmed,
		       COUNT(*) FILTER (WHERE status = 'completed') AS completed,
		       COALESCE(SUM(price) FILTER (WHERE status = 'completed'), 0) AS revenue
		FROM bookings
	`
	if err := r.db.QueryRowContext(ctx, query).Scan(&stats.TotalBookings, &stats.PendingBookings, &stats.ConfirmedBookings, &stats.CompletedBookings, &stats.TotalRevenue); err != nil {
		return nil, err
	}

	rows, err := r.db.QueryContext(ctx, `
		SELECT id, customer_name, customer_phone, car_brand, car_model, service_id, service_name, price, status, comment, created_at, updated_at
		FROM bookings
		ORDER BY created_at DESC
		LIMIT 10
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var b models.Booking
		if err := rows.Scan(&b.ID, &b.CustomerName, &b.CustomerPhone, &b.CarBrand, &b.CarModel, &b.ServiceID, &b.ServiceName, &b.Price, &b.Status, &b.Comment, &b.CreatedAt, &b.UpdatedAt); err != nil {
			return nil, err
		}
		stats.RecentBookings = append(stats.RecentBookings, b)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	stats.StatusBreakdown[models.StatusPending] = stats.PendingBookings
	stats.StatusBreakdown[models.StatusConfirmed] = stats.ConfirmedBookings
	stats.StatusBreakdown[models.StatusCompleted] = stats.CompletedBookings

	return stats, nil
}

// ============ REVIEW SOURCE OPERATIONS ============
// Deprecated: Review sources are no longer used

func (r *DatabaseRepository) GetReviewSources() ([]models.ReviewSource, error) {
	return []models.ReviewSource{}, nil
}

func (r *DatabaseRepository) CreateReviewSource(source *models.ReviewSource) error {
	return nil
}

func (r *DatabaseRepository) UpdateReviewSource(source *models.ReviewSource) error {
	return nil
}

func (r *DatabaseRepository) DeleteReviewSource(id string) error {
	return nil
}

// Helper function to check if table exists
func (r *DatabaseRepository) TableExists(tableName string) (bool, error) {
	var exists bool
	err := r.db.QueryRow(`
		SELECT EXISTS (
			SELECT FROM information_schema.tables 
			WHERE table_schema = 'public' 
			AND table_name = $1
		)
	`, tableName).Scan(&exists)
	return exists, err
}

// Helper function to count rows in a table
func (r *DatabaseRepository) CountTable(tableName string) (int, error) {
	var count int
	err := r.db.QueryRow(fmt.Sprintf("SELECT COUNT(*) FROM %s", tableName)).Scan(&count)
	return count, err
}
