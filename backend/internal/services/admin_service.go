package services

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/repository"
)

type AdminService struct {
	repo repository.Repository
}

func NewAdminService(repo repository.Repository) *AdminService {
	return &AdminService{repo: repo}
}

func (s *AdminService) GetDashboardStats() (*models.DashboardStats, error) {
	return s.repo.GetDashboardStats()
}

func (s *AdminService) GetAllBookings(limit int) ([]models.Booking, error) {
	return s.repo.GetAllBookings(limit)
}

func (s *AdminService) UpdateBookingStatus(id string, status models.BookingStatus) (*models.Booking, error) {
	booking, err := s.repo.GetBooking(id)
	if err != nil {
		return nil, err
	}

	booking.Status = status
	if err := s.repo.UpdateBooking(booking); err != nil {
		return nil, err
	}

	return booking, nil
}

func (s *AdminService) DeleteBooking(id string) error {
	return s.repo.DeleteBooking(id)
}

func (s *AdminService) GetBooking(id string) (*models.Booking, error) {
	return s.repo.GetBooking(id)
}
