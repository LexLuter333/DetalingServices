package services

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/repository"
	"errors"
)

type BookingService struct {
	repo repository.Repository
}

func NewBookingService(repo repository.Repository) *BookingService {
	return &BookingService{repo: repo}
}

func (s *BookingService) CreateBooking(req *models.CreateBookingRequest) (*models.Booking, error) {
	service, err := s.repo.GetService(req.ServiceID)
	if err != nil {
		return nil, errors.New("service not found")
	}

	booking := &models.Booking{
		CustomerName:  req.CustomerName,
		CustomerPhone: req.CustomerPhone,
		CarBrand:      req.CarBrand,
		CarModel:      req.CarModel,
		ServiceID:     req.ServiceID,
		ServiceName:   service.Name,
		Price:         service.Price,
		Status:        models.StatusPending,
		Comment:       req.Comment,
	}

	if err := s.repo.CreateBooking(booking); err != nil {
		return nil, err
	}

	return booking, nil
}

func (s *BookingService) GetBooking(id string) (*models.Booking, error) {
	return s.repo.GetBooking(id)
}

func (s *BookingService) GetAllBookings(limit int) ([]models.Booking, error) {
	return s.repo.GetAllBookings(limit)
}

func (s *BookingService) UpdateBookingStatus(id string, status models.BookingStatus) (*models.Booking, error) {
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

func (s *BookingService) DeleteBooking(id string) error {
	return s.repo.DeleteBooking(id)
}
