package services

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/repository"
	"errors"
	"sync"
	"time"
)

type ServiceService struct {
	repo        repository.Repository
	cache       []models.Service
	cacheExpiry time.Time
	cacheMu     sync.RWMutex
}

func NewServiceService(repo repository.Repository) *ServiceService {
	return &ServiceService{repo: repo}
}

func (s *ServiceService) invalidateCache() {
	s.cacheMu.Lock()
	s.cache = nil
	s.cacheExpiry = time.Time{}
	s.cacheMu.Unlock()
}

func (s *ServiceService) loadCache() ([]models.Service, error) {
	s.cacheMu.RLock()
	if time.Now().Before(s.cacheExpiry) && len(s.cache) > 0 {
		cached := append([]models.Service(nil), s.cache...)
		s.cacheMu.RUnlock()
		return cached, nil
	}
	s.cacheMu.RUnlock()

	services, err := s.repo.GetAllServices()
	if err != nil {
		return nil, err
	}

	s.cacheMu.Lock()
	s.cache = append([]models.Service(nil), services...)
	s.cacheExpiry = time.Now().Add(5 * time.Second)
	s.cacheMu.Unlock()

	return services, nil
}

func (s *ServiceService) GetAllServices() ([]models.Service, error) {
	return s.loadCache()
}

func (s *ServiceService) GetAvailableServices() ([]models.Service, error) {
	allServices, err := s.loadCache()
	if err != nil {
		return nil, err
	}

	available := make([]models.Service, 0, len(allServices))
	for _, svc := range allServices {
		if svc.Available {
			available = append(available, svc)
		}
	}
	return available, nil
}

func (s *ServiceService) GetService(id string) (*models.Service, error) {
	return s.repo.GetService(id)
}

func (s *ServiceService) CreateService(service *models.Service) error {
	err := s.repo.CreateService(service)
	if err == nil {
		s.invalidateCache()
	}
	return err
}

func (s *ServiceService) UpdateService(service *models.Service) (*models.Service, error) {
	existing, err := s.repo.GetService(service.ID)
	if err != nil {
		return nil, errors.New("service not found")
	}

	if service.Name != "" {
		existing.Name = service.Name
	}
	if service.Description != "" {
		existing.Description = service.Description
	}
	if service.Price > 0 {
		existing.Price = service.Price
	}
	if service.Duration > 0 {
		existing.Duration = service.Duration
	}
	// Keep services always available since we removed the toggle
	existing.Available = true

	if err := s.repo.UpdateService(existing); err != nil {
		return nil, err
	}

	s.invalidateCache()
	return existing, nil
}

func (s *ServiceService) DeleteService(id string) error {
	err := s.repo.DeleteService(id)
	if err == nil {
		s.invalidateCache()
	}
	return err
}
