package services

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/repository"
	"sync"
	"time"
)

type ReviewService struct {
	repo        repository.Repository
	cache       []models.Review
	cacheExpiry time.Time
	cacheMu     sync.RWMutex
}

func NewReviewService(repo repository.Repository) *ReviewService {
	return &ReviewService{repo: repo}
}

func (s *ReviewService) invalidateCache() {
	s.cacheMu.Lock()
	s.cache = nil
	s.cacheExpiry = time.Time{}
	s.cacheMu.Unlock()
}

func (s *ReviewService) GetAllReviews(limit int) ([]models.Review, error) {
	return s.repo.GetAllReviews(limit)
}

func (s *ReviewService) GetPublicReviews(limit int) ([]models.Review, error) {
	s.cacheMu.RLock()
	if time.Now().Before(s.cacheExpiry) && len(s.cache) > 0 && limit > 0 {
		cached := append([]models.Review(nil), s.cache...)
		s.cacheMu.RUnlock()
		if len(cached) > limit {
			return cached[:limit], nil
		}
		return cached, nil
	}
	s.cacheMu.RUnlock()

	reviews, err := s.repo.GetPublicReviews(limit)
	if err != nil {
		return nil, err
	}

	s.cacheMu.Lock()
	s.cache = append([]models.Review(nil), reviews...)
	s.cacheExpiry = time.Now().Add(30 * time.Second)
	s.cacheMu.Unlock()

	return reviews, nil
}

func (s *ReviewService) CreateReview(review *models.Review) error {
	err := s.repo.CreateReview(review)
	if err == nil {
		s.invalidateCache()
	}
	return err
}

func (s *ReviewService) UpdateReview(review *models.Review) error {
	err := s.repo.UpdateReview(review)
	if err == nil {
		s.invalidateCache()
	}
	return err
}

func (s *ReviewService) DeleteReview(id string) error {
	err := s.repo.DeleteReview(id)
	if err == nil {
		s.invalidateCache()
	}
	return err
}

func (s *ReviewService) GetReviewStats() (*models.ReviewStats, error) {
	return s.repo.GetReviewStats()
}
