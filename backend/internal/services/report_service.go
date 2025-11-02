package services

import (
	"encoding/csv"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/google/uuid"
	"publicscannerapi/internal/models"
	"publicscannerapi/internal/repository"
)

var (
	ErrReportNotFound    = errors.New("report not found")
	ErrInvalidFormat     = errors.New("invalid report format")
	ErrReportGeneration  = errors.New("failed to generate report")
)

// ReportService handles report business logic
type ReportService struct {
	reportRepo  *repository.ReportRepository
	scanRepo    *repository.ScanRepository
	storagePath string
}

// NewReportService creates a new report service
func NewReportService(reportRepo *repository.ReportRepository, scanRepo *repository.ScanRepository, storagePath string) *ReportService {
	return &ReportService{
		reportRepo:  reportRepo,
		scanRepo:    scanRepo,
		storagePath: storagePath,
	}
}

// GenerateReportRequest represents a report generation request
type GenerateReportRequest struct {
	ScanID uuid.UUID `json:"scan_id" binding:"required"`
	Format string    `json:"format" binding:"required,oneof=json csv pdf html"`
}

// GenerateReport generates a report for a scan
func (s *ReportService) GenerateReport(req *GenerateReportRequest, userID, organizationID uuid.UUID) (*models.Report, error) {
	// Verify scan exists and belongs to organization
	scan, err := s.scanRepo.GetByID(req.ScanID)
	if err != nil {
		if errors.Is(err, repository.ErrScanNotFound) {
			return nil, ErrScanNotFound
		}
		return nil, err
	}

	if scan.OrganizationID != organizationID {
		return nil, ErrScanNotFound
	}

	// Get scan results
	results, err := s.scanRepo.GetResults(req.ScanID)
	if err != nil {
		return nil, err
	}

	// Generate report based on format
	var filePath string
	var fileSize int64

	switch req.Format {
	case "json":
		filePath, fileSize, err = s.generateJSONReport(scan, results)
	case "csv":
		filePath, fileSize, err = s.generateCSVReport(scan, results)
	case "pdf":
		// TODO: Implement PDF generation
		return nil, errors.New("PDF reports not yet implemented")
	case "html":
		// TODO: Implement HTML generation
		return nil, errors.New("HTML reports not yet implemented")
	default:
		return nil, ErrInvalidFormat
	}

	if err != nil {
		return nil, ErrReportGeneration
	}

	// Create report record
	report := &models.Report{
		ID:             uuid.New(),
		ScanID:         req.ScanID,
		OrganizationID: organizationID,
		GeneratedBy:    userID,
		Format:         req.Format,
		FileName:       filepath.Base(filePath),
		FilePath:       filePath,
		FileSize:       fileSize,
	}

	if err := s.reportRepo.Create(report); err != nil {
		// Clean up file if database insert fails
		_ = os.Remove(filePath)
		return nil, err
	}

	return report, nil
}

// generateJSONReport generates a JSON format report
func (s *ReportService) generateJSONReport(scan *models.ScanJob, results []*models.ScanResult) (string, int64, error) {
	// Create report data structure
	reportData := map[string]interface{}{
		"scan_id":    scan.ID,
		"status":     scan.Status,
		"started_at": scan.StartedAt,
		"completed_at": scan.CompletedAt,
		"checks":     scan.Checks,
		"results":    results,
		"generated_at": time.Now(),
	}

	// Marshal to JSON
	jsonData, err := json.MarshalIndent(reportData, "", "  ")
	if err != nil {
		return "", 0, err
	}

	// Create file
	filename := fmt.Sprintf("scan_%s_%s.json", scan.ID, time.Now().Format("20060102_150405"))
	filePath := filepath.Join(s.storagePath, "reports", filename)

	// Ensure directory exists
	if err := os.MkdirAll(filepath.Dir(filePath), 0755); err != nil {
		return "", 0, err
	}

	// Write file
	if err := os.WriteFile(filePath, jsonData, 0644); err != nil {
		return "", 0, err
	}

	// Get file size
	info, err := os.Stat(filePath)
	if err != nil {
		return "", 0, err
	}

	return filePath, info.Size(), nil
}

// generateCSVReport generates a CSV format report
func (s *ReportService) generateCSVReport(scan *models.ScanJob, results []*models.ScanResult) (string, int64, error) {
	// Create file
	filename := fmt.Sprintf("scan_%s_%s.csv", scan.ID, time.Now().Format("20060102_150405"))
	filePath := filepath.Join(s.storagePath, "reports", filename)

	// Ensure directory exists
	if err := os.MkdirAll(filepath.Dir(filePath), 0755); err != nil {
		return "", 0, err
	}

	file, err := os.Create(filePath)
	if err != nil {
		return "", 0, err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write header
	header := []string{"Check Type", "Status", "Findings", "Severity", "Timestamp"}
	if err := writer.Write(header); err != nil {
		return "", 0, err
	}

	// Write results
	for _, result := range results {
		record := []string{
			result.CheckType,
			result.Status,
			fmt.Sprintf("%d", result.Findings),
			result.Severity,
			result.CreatedAt.Format(time.RFC3339),
		}
		if err := writer.Write(record); err != nil {
			return "", 0, err
		}
	}

	// Get file size
	info, err := os.Stat(filePath)
	if err != nil {
		return "", 0, err
	}

	return filePath, info.Size(), nil
}

// GetReport retrieves a report by ID
func (s *ReportService) GetReport(reportID, organizationID uuid.UUID) (*models.Report, error) {
	report, err := s.reportRepo.GetByID(reportID)
	if err != nil {
		if errors.Is(err, repository.ErrReportNotFound) {
			return nil, ErrReportNotFound
		}
		return nil, err
	}

	// Verify report belongs to organization
	if report.OrganizationID != organizationID {
		return nil, ErrReportNotFound
	}

	return report, nil
}

// ListReports retrieves all reports for an organization
func (s *ReportService) ListReports(organizationID uuid.UUID, limit, offset int) ([]*models.Report, error) {
	return s.reportRepo.ListByOrganization(organizationID, limit, offset)
}

// DeleteReport deletes a report and its file
func (s *ReportService) DeleteReport(reportID, organizationID uuid.UUID) error {
	// Get report
	report, err := s.GetReport(reportID, organizationID)
	if err != nil {
		return err
	}

	// Delete file
	if err := os.Remove(report.FilePath); err != nil && !os.IsNotExist(err) {
		// Log error but continue with database deletion
		fmt.Printf("Failed to delete report file: %v\n", err)
	}

	// Delete from database
	return s.reportRepo.Delete(reportID)
}
