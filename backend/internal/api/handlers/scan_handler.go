package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"publicscannerapi/internal/services"
)

// ScanHandler handles scan endpoints
type ScanHandler struct {
	scanService *services.ScanService
}

// NewScanHandler creates a new scan handler
func NewScanHandler(scanService *services.ScanService) *ScanHandler {
	return &ScanHandler{
		scanService: scanService,
	}
}

// Create handles scan creation
// POST /api/v1/scans
func (h *ScanHandler) Create(c *gin.Context) {
	var req services.CreateScanRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request data",
			"details": err.Error(),
		})
		return
	}

	// Get user and organization from context
	userID := c.MustGet("user_id").(uuid.UUID)

	// Check if organization_id exists in context
	orgID, exists := c.Get("organization_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error": "No organization found. Please log out and log back in.",
		})
		return
	}
	organizationID := orgID.(uuid.UUID)

	scan, err := h.scanService.CreateScan(&req, userID, organizationID)
	if err != nil {
		if err == services.ErrTargetNotFound {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Target not found",
			})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to create scan",
		})
		return
	}

	c.JSON(http.StatusCreated, scan)
}

// Get handles retrieving a single scan
// GET /api/v1/scans/:id
func (h *ScanHandler) Get(c *gin.Context) {
	scanID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid scan ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	scan, err := h.scanService.GetScan(scanID, organizationID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Scan not found",
		})
		return
	}

	c.JSON(http.StatusOK, scan)
}

// List handles listing all scans for an organization
// GET /api/v1/scans
func (h *ScanHandler) List(c *gin.Context) {
	organizationID := c.MustGet("organization_id").(uuid.UUID)

	// Parse pagination parameters
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "50"))
	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))

	scans, err := h.scanService.ListScans(organizationID, limit, offset)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve scans",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"scans":  scans,
		"total":  len(scans),
		"limit":  limit,
		"offset": offset,
	})
}

// GetResults handles retrieving scan results
// GET /api/v1/scans/:id/results
func (h *ScanHandler) GetResults(c *gin.Context) {
	scanID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid scan ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	results, err := h.scanService.GetScanResults(scanID, organizationID)
	if err != nil {
		if err == services.ErrScanNotFound {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Scan not found",
			})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve scan results",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"results": results,
		"total":   len(results),
	})
}

// Cancel handles cancelling a scan
// POST /api/v1/scans/:id/cancel
func (h *ScanHandler) Cancel(c *gin.Context) {
	scanID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid scan ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	if err := h.scanService.CancelScan(scanID, organizationID); err != nil {
		if err == services.ErrScanNotFound {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Scan not found",
			})
			return
		}
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Scan cancelled successfully",
	})
}
