package handlers

import (
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

type ServiceHandler struct {
	service *services.ServiceService
}

func NewServiceHandler(service *services.ServiceService) *ServiceHandler {
	return &ServiceHandler{service: service}
}

// GET /api/admin/services
func (h *ServiceHandler) GetAllServices(c *gin.Context) {
	services, err := h.service.GetAllServices()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"services": services})
}

// GetPublicServices handles GET /api/services (for public website)
func (h *ServiceHandler) GetPublicServices(c *gin.Context) {
	services, err := h.service.GetAvailableServices()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"services": services})
}

// CreateService handles POST /api/admin/services
func (h *ServiceHandler) CreateService(c *gin.Context) {
	var req models.Service

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.service.CreateService(&req); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "Service created successfully",
		"service": req,
	})
}

// UpdateService handles PUT /api/admin/services/:id
func (h *ServiceHandler) UpdateService(c *gin.Context) {
	id := c.Param("id")

	var req models.Service
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	req.ID = id
	updated, err := h.service.UpdateService(&req)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Service updated successfully",
		"service": updated,
	})
}

// DeleteService handles DELETE /api/admin/services/:id
func (h *ServiceHandler) DeleteService(c *gin.Context) {
	id := c.Param("id")

	if err := h.service.DeleteService(id); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Service deleted successfully"})
}
