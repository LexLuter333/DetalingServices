package repository

import (
	"deteleng-backend/internal/models"
)

type Repository interface {
	GetAllServices() ([]models.Service, error)
	GetService(id string) (*models.Service, error)
	CreateService(service *models.Service) error
	UpdateService(service *models.Service) error
	DeleteService(id string) error

	CreateBooking(booking *models.Booking) error
	GetBooking(id string) (*models.Booking, error)
	GetAllBookings(limit int) ([]models.Booking, error)
	UpdateBooking(booking *models.Booking) error
	DeleteBooking(id string) error
	DeleteOldCompletedBookings() error
	GetDashboardStats() (*models.DashboardStats, error)

	GetUserByEmail(email string) (*models.User, error)
	GetUserByID(id string) (*models.User, error)
	CreateUser(user *models.User) error

	GetAllReviews(limit int) ([]models.Review, error)
	GetPublicReviews(limit int) ([]models.Review, error)
	CreateReview(review *models.Review) error
	UpdateReview(review *models.Review) error
	DeleteReview(id string) error
	GetReviewStats() (*models.ReviewStats, error)

	GetReviewSources() ([]models.ReviewSource, error)
	CreateReviewSource(source *models.ReviewSource) error
	UpdateReviewSource(source *models.ReviewSource) error
	DeleteReviewSource(id string) error
}
