package models

import "time"

type BookingStatus string

const (
	StatusPending   BookingStatus = "pending"
	StatusConfirmed BookingStatus = "confirmed"
	StatusCompleted BookingStatus = "completed"
	StatusCancelled BookingStatus = "cancelled"
)

type Booking struct {
	ID            string        `json:"id"`
	CustomerName  string        `json:"customer_name"`
	CustomerPhone string        `json:"customer_phone"`
	CarBrand      string        `json:"car_brand"`
	CarModel      string        `json:"car_model"`
	ServiceID     string        `json:"service_id"`
	ServiceName   string        `json:"service_name"`
	Price         float64       `json:"price"`
	Status        BookingStatus `json:"status"`
	Comment       string        `json:"comment,omitempty"`
	CreatedAt     time.Time     `json:"created_at"`
	UpdatedAt     time.Time     `json:"updated_at"`
}

type Service struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Price       float64   `json:"price"`
	Duration    int       `json:"duration_minutes"`
	Available   bool      `json:"available"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

type User struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	Role      string    `json:"role"`
	CreatedAt time.Time `json:"created_at"`
}

type DashboardStats struct {
	TotalBookings   int64                  `json:"total_bookings"`
	PendingBookings int64                  `json:"pending_bookings"`
	ConfirmedBookings int64                `json:"confirmed_bookings"`
	CompletedBookings int64                `json:"completed_bookings"`
	TotalRevenue    float64                `json:"total_revenue"`
	RecentBookings  []Booking              `json:"recent_bookings"`
	StatusBreakdown map[BookingStatus]int64 `json:"status_breakdown"`
}

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LoginResponse struct {
	Token string `json:"token"`
	User  User   `json:"user"`
}

type CreateBookingRequest struct {
	CustomerName  string  `json:"customer_name" binding:"required"`
	CustomerPhone string  `json:"customer_phone" binding:"required"`
	CarBrand      string  `json:"car_brand" binding:"required"`
	CarModel      string  `json:"car_model"`
	ServiceID     string  `json:"service_id" binding:"required"`
	Comment       string  `json:"comment"`
	UserID    *int      `json:"user_id"`
    StartTime *string   `json:"start_time"`
}

type UpdateBookingStatusRequest struct {
	Status BookingStatus `json:"status" binding:"required"`
}

type Review struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`      // Имя клиента
	CarBrand  string    `json:"car_brand"` // Марка автомобиля
	CarModel  string    `json:"car_model"` // Модель автомобиля
	Rating    int       `json:"rating"`    // Рейтинг (1-5)
	Text      string    `json:"text"`      // Текст отзыва
	CreatedAt time.Time `json:"created_at"`
}

// ReviewSource is deprecated but kept for backward compatibility
type ReviewSource struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	URL       string    `json:"url"`
	IsActive  bool      `json:"is_active"`
	LastParse time.Time `json:"last_parse,omitempty"`
}

type ReviewStats struct {
	TotalReviews   int64           `json:"total_reviews"`
	AverageRating  float64         `json:"average_rating"`
	RatingBreakdown map[int]int64  `json:"rating_breakdown"`
	RecentReviews   []Review       `json:"recent_reviews"`
}
