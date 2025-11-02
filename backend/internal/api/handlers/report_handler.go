package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"publicscannerapi/internal/services"
)

// ReportHandler handles report endpoints
type ReportHandler struct {
	reportService *services.ReportService
}

// NewReportHandler creates a new report handler
func NewReportHandler(reportService *services.ReportService) *ReportHandler {
	return &ReportHandler{
		reportService: reportService,
	}
}

// Generate handles report generation
// POST /api/v1/reports/generate
func (h *ReportHandler) Generate(c *gin.Context) {
	var req services.GenerateReportRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request data",
			"details": err.Error(),
		})
		return
	}

	// Get user and organization from context
	userID := c.MustGet("user_id").(uuid.UUID)
	organizationID := c.MustGet("organization_id").(uuid.UUID)

	report, err := h.reportService.GenerateReport(&req, userID, organizationID)
	if err != nil {
		if err == services.ErrScanNotFound {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Scan not found",
			})
			return
		}
		if err == services.ErrInvalidFormat {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "Invalid report format",
			})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, report)
}

// Get handles retrieving a single report
// GET /api/v1/reports/:id
func (h *ReportHandler) Get(c *gin.Context) {
	reportID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid report ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	report, err := h.reportService.GetReport(reportID, organizationID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Report not found",
		})
		return
	}

	c.JSON(http.StatusOK, report)
}

// List handles listing all reports for an organization
// GET /api/v1/reports
func (h *ReportHandler) List(c *gin.Context) {
	organizationID := c.MustGet("organization_id").(uuid.UUID)

	// Parse pagination parameters
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "50"))
	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))

	reports, err := h.reportService.ListReports(organizationID, limit, offset)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to retrieve reports",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"reports": reports,
		"total":   len(reports),
		"limit":   limit,
		"offset":  offset,
	})
}

// Download handles downloading a report file
// GET /api/v1/reports/:id/download
func (h *ReportHandler) Download(c *gin.Context) {
	reportID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid report ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	report, err := h.reportService.GetReport(reportID, organizationID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Report not found",
		})
		return
	}

	// Set appropriate headers
	c.Header("Content-Description", "File Transfer")
	c.Header("Content-Transfer-Encoding", "binary")
	c.Header("Content-Disposition", "attachment; filename="+report.FileName)
	c.Header("Content-Type", getContentType(report.Format))

	c.File(report.FilePath)
}

// Delete handles deleting a report
// DELETE /api/v1/reports/:id
func (h *ReportHandler) Delete(c *gin.Context) {
	reportID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid report ID",
		})
		return
	}

	organizationID := c.MustGet("organization_id").(uuid.UUID)

	if err := h.reportService.DeleteReport(reportID, organizationID); err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Report not found",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Report deleted successfully",
	})
}

// getContentType returns the MIME type for a report format
func getContentType(format string) string {
	switch format {
	case "json":
		return "application/json"
	case "csv":
		return "text/csv"
	case "pdf":
		return "application/pdf"
	case "html":
		return "text/html"
	default:
		return "application/octet-stream"
	}
}
