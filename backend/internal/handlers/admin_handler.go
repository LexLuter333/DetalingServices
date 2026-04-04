package handlers

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/services"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type AdminHandler struct {
	service     *services.AdminService
	authService *services.AuthService
}

func NewAdminHandler(service *services.AdminService, authService *services.AuthService) *AdminHandler {
	return &AdminHandler{
		service:     service,
		authService: authService,
	}
}

// Dashboard handles GET /api/admin/dashboard
func (h *AdminHandler) Dashboard(c *gin.Context) {
	stats, err := h.service.GetDashboardStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"stats": stats})
}

// GetAllBookings handles GET /api/admin/bookings
func (h *AdminHandler) GetAllBookings(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "500")
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit < 1 || limit > 2000 {
		limit = 500
	}

	bookings, err := h.service.GetAllBookings(limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"bookings": bookings})
}

// UpdateBookingStatus handles PUT /api/admin/bookings/:id/status
func (h *AdminHandler) UpdateBookingStatus(c *gin.Context) {
	id := c.Param("id")

	var req models.UpdateBookingStatusRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	booking, err := h.service.UpdateBookingStatus(id, req.Status)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Booking status updated",
		"booking": booking,
	})
}

// DeleteBooking handles DELETE /api/admin/bookings/:id
func (h *AdminHandler) DeleteBooking(c *gin.Context) {
	id := c.Param("id")

	if err := h.service.DeleteBooking(id); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Booking deleted successfully"})
}

// GetStats handles GET /api/admin/stats
func (h *AdminHandler) GetStats(c *gin.Context) {
	stats, err := h.service.GetDashboardStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"stats": stats})
}
