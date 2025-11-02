package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"publicscannerapi/internal/services"
)

// TargetHandler handles target endpoints
type TargetHandler struct {
	targetService *services.TargetService
}

// NewTargetHandler creates a new target handler
func NewTargetHandler(targetService *services.TargetService) *TargetHandler {
	return &TargetHandler{
		targetService: targetService,
	}
}

// Create handles target creation
// POST /api/v1/targets
func (h *TargetHandler) Create(c *gin.Context) {
	var req services.CreateTargetRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request data",
			"details": err.Error(),
		})
		return
	}

	// Get user and organization from context (set by auth middleware)
	userID := c.MustGet("user_id").(uuid.UUID)
	organizationID := c.MustGet("organization_id").(uuid.UUID)

	target, err := h.targetService.CreateTarget(&req, userID, organizationID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to create target",
		})
		return
	}

	c.JSON(http.StatusCreated, target)
}

// Get handles retrieving a single target
// GET /api/v1/targets/:id
func (h *TargetHandler) Get(c *gin.Context) {
	targetID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid target ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	target, err := h.targetService.GetTarget(targetID, organizationID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Target not found",
		})
		return
	}

	c.JSON(http.StatusOK, target)
}

// List handles listing all targets for an organization
// GET /api/v1/targets
func (h *TargetHandler) List(c *gin.Context) {
	organizationID := c.MustGet("organization_id").(uuid.UUID)

	targets, err := h.targetService.ListTargets(organizationID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve targets",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"targets": targets,
		"total":   len(targets),
	})
}

// Update handles updating a target
// PATCH /api/v1/targets/:id
func (h *TargetHandler) Update(c *gin.Context) {
	targetID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid target ID",
		})
		return
	}

	var req services.UpdateTargetRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request data",
			"details": err.Error(),
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	target, err := h.targetService.UpdateTarget(targetID, organizationID, &req)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Target not found",
		})
		return
	}

	c.JSON(http.StatusOK, target)
}

// Delete handles deleting a target
// DELETE /api/v1/targets/:id
func (h *TargetHandler) Delete(c *gin.Context) {
	targetID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid target ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	if err := h.targetService.DeleteTarget(targetID, organizationID); err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Target not found",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Target deleted successfully",
	})
}
