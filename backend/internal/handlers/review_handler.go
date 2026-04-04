package handlers

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/services"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type ReviewHandler struct {
	service *services.ReviewService
}

func NewReviewHandler(service *services.ReviewService) *ReviewHandler {
	return &ReviewHandler{service: service}
}

// GetPublicReviews handles GET /api/reviews (public, all reviews)
func (h *ReviewHandler) GetPublicReviews(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "50")
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit < 1 || limit > 100 {
		limit = 50
	}

	reviews, err := h.service.GetPublicReviews(limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"reviews": reviews})
}

// GetAllReviews handles GET /api/admin/reviews (admin only, all reviews)
func (h *ReviewHandler) GetAllReviews(c *gin.Context) {
	reviews, err := h.service.GetAllReviews(0) // 0 = no limit
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"reviews": reviews})
}

// CreateReview handles POST /api/admin/reviews
func (h *ReviewHandler) CreateReview(c *gin.Context) {
	var req struct {
		Name     string `json:"name" binding:"required"`
		CarBrand string `json:"car_brand" binding:"required"`
		CarModel string `json:"car_model" binding:"required"`
		Rating   int    `json:"rating" binding:"required,min=1,max=5"`
		Text     string `json:"text" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	review := &models.Review{
		Name:     req.Name,
		CarBrand: req.CarBrand,
		CarModel: req.CarModel,
		Rating:   req.Rating,
		Text:     req.Text,
	}

	if err := h.service.CreateReview(review); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "Review created successfully",
		"review":  review,
	})
}

// UpdateReview handles PUT /api/admin/reviews/:id
func (h *ReviewHandler) UpdateReview(c *gin.Context) {
	id := c.Param("id")

	var req struct {
		Name     string `json:"name" binding:"required"`
		CarBrand string `json:"car_brand" binding:"required"`
		CarModel string `json:"car_model" binding:"required"`
		Rating   int    `json:"rating" binding:"required,min=1,max=5"`
		Text     string `json:"text" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	review := &models.Review{
		ID:       id,
		Name:     req.Name,
		CarBrand: req.CarBrand,
		CarModel: req.CarModel,
		Rating:   req.Rating,
		Text:     req.Text,
	}

	if err := h.service.UpdateReview(review); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Review updated successfully",
		"review":  review,
	})
}

// DeleteReview handles DELETE /api/admin/reviews/:id
func (h *ReviewHandler) DeleteReview(c *gin.Context) {
	id := c.Param("id")

	if err := h.service.DeleteReview(id); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Review deleted successfully"})
}

// ParseReviews handles POST /api/admin/reviews/parse (deprecated, kept for compatibility)
func (h *ReviewHandler) ParseReviews(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "Parse endpoint is deprecated. Use POST /api/admin/reviews to add reviews manually.",
	})
}

// GetReviewStats handles GET /api/admin/reviews/stats
func (h *ReviewHandler) GetReviewStats(c *gin.Context) {
	stats, err := h.service.GetReviewStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"stats": stats})
}

// GetReviewSources handles GET /api/admin/review-sources (deprecated)
func (h *ReviewHandler) GetReviewSources(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"sources": []interface{}{}})
}

// CreateReviewSource handles POST /api/admin/review-sources (deprecated)
func (h *ReviewHandler) CreateReviewSource(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "Review sources are deprecated. Add reviews directly."})
}

// UpdateReviewSource handles PUT /api/admin/review-sources/:id (deprecated)
func (h *ReviewHandler) UpdateReviewSource(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "Review sources are deprecated."})
}

// DeleteReviewSource handles DELETE /api/admin/review-sources/:id (deprecated)
func (h *ReviewHandler) DeleteReviewSource(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "Review sources are deprecated."})
}
