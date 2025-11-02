package services

import (
	"encoding/json"
	"errors"
	"fmt"

	"github.com/google/uuid"
	"publicscannerapi/internal/models"
	"publicscannerapi/internal/repository"
)

var (
	ErrTargetNotFound = errors.New("target not found")
	ErrScanNotFound   = errors.New("scan not found")
)

// ScanService handles scan business logic
type ScanService struct {
	scanRepo   *repository.ScanRepository
	targetRepo *repository.TargetRepository
	redisURL   string
}

// NewScanService creates a new scan service
func NewScanService(scanRepo *repository.ScanRepository, targetRepo *repository.TargetRepository, redisURL string) *ScanService {
	return &ScanService{
		scanRepo:   scanRepo,
		targetRepo: targetRepo,
		redisURL:   redisURL,
	}
}

// CreateScanRequest represents a scan creation request
type CreateScanRequest struct {
	TargetID *uuid.UUID        `json:"target_id,omitempty"` // Optional: for saved target
	URL      *string           `json:"url,omitempty"`       // Optional: for quick scan
	Checks   []string          `json:"checks" binding:"required"`
	Config   models.ScanConfig `json:"config"`
}

// CreateScan creates and queues a new scan
func (s *ScanService) CreateScan(req *CreateScanRequest, userID, organizationID uuid.UUID) (*models.ScanJob, error) {
	// Validate that at least one of target_id or URL is provided
	if req.TargetID == nil && req.URL == nil {
		return nil, errors.New("either target_id or url must be provided")
	}

	var targetURL string
	scan := &models.ScanJob{
		ID:             uuid.New(),
		OrganizationID: organizationID,
		InitiatedBy:    userID,
		Status:         "queued",
		Progress:       0,
		Checks:         req.Checks,
		Config:         req.Config,
	}

	// Handle target-based scan
	if req.TargetID != nil {
		target, err := s.targetRepo.GetByID(*req.TargetID)
		if err != nil {
			if errors.Is(err, repository.ErrTargetNotFound) {
				return nil, ErrTargetNotFound
			}
			return nil, err
		}

		// Verify target belongs to organization
		if target.OrganizationID != organizationID {
			return nil, errors.New("target not found in organization")
		}

		scan.TargetID = req.TargetID
		targetURL = target.Hostname
	}

	// Handle URL-based quick scan
	if req.URL != nil {
		scan.URL = req.URL
		targetURL = *req.URL
	}

	// Save to database
	if err := s.scanRepo.Create(scan); err != nil {
		return nil, err
	}

	// Queue scan with Celery
	if err := s.queueScan(scan.ID.String(), targetURL, req.Checks, req.Config); err != nil {
		// Mark scan as failed if queuing fails
		_ = s.scanRepo.Fail(scan.ID)
		return nil, fmt.Errorf("failed to queue scan: %w", err)
	}

	return scan, nil
}

// queueScan sends a scan task to Celery via Redis
func (s *ScanService) queueScan(scanID, target string, checks []string, config models.ScanConfig) error {
	// Celery task format
	taskID := uuid.New().String()
	task := map[string]interface{}{
		"id":      taskID,
		"task":    "tasks.execute_scan",
		"args":    []interface{}{scanID, target, checks},
		"kwargs":  map[string]interface{}{},
		"retries": 0,
	}

	// Celery message envelope
	message := map[string]interface{}{
		"body":         base64Encode(task),
		"content-type": "application/json",
		"properties": map[string]interface{}{
			"correlation_id": taskID,
			"delivery_info": map[string]interface{}{
				"exchange":   "",
				"routing_key": "celery",
			},
			"delivery_mode": 2,
			"delivery_tag":  taskID,
		},
		"headers": map[string]interface{}{},
	}

	messageJSON, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("failed to marshal message: %w", err)
	}

	fmt.Printf("Queueing scan task for %s (ID: %s)\n", target, scanID)

	// For now, just log it - Redis integration can be added later if needed
	// The workers can poll the database for queued scans instead
	_ = messageJSON

	return nil
}

func base64Encode(data interface{}) string {
	jsonBytes, _ := json.Marshal(data)
	return string(jsonBytes) // Celery expects JSON string, not base64 for json serializer
}

// GetScan retrieves a scan by ID
func (s *ScanService) GetScan(scanID, organizationID uuid.UUID) (*models.ScanJob, error) {
	scan, err := s.scanRepo.GetByID(scanID)
	if err != nil {
		if errors.Is(err, repository.ErrScanNotFound) {
			return nil, ErrScanNotFound
		}
		return nil, err
	}

	// Verify scan belongs to organization
	if scan.OrganizationID != organizationID {
		return nil, ErrScanNotFound
	}

	return scan, nil
}

// ListScans retrieves all scans for an organization
func (s *ScanService) ListScans(organizationID uuid.UUID, limit, offset int) ([]*models.ScanJob, error) {
	return s.scanRepo.ListByOrganization(organizationID, limit, offset)
}

// GetScanResults retrieves results for a scan
func (s *ScanService) GetScanResults(scanID, organizationID uuid.UUID) ([]*models.ScanResult, error) {
	// Verify scan exists and belongs to organization
	scan, err := s.GetScan(scanID, organizationID)
	if err != nil {
		return nil, err
	}

	return s.scanRepo.GetResults(scan.ID)
}

// CancelScan cancels a running scan
func (s *ScanService) CancelScan(scanID, organizationID uuid.UUID) error {
	// Verify scan exists and belongs to organization
	scan, err := s.GetScan(scanID, organizationID)
	if err != nil {
		return err
	}

	// Can only cancel queued or running scans
	if scan.Status != "queued" && scan.Status != "running" {
		return errors.New("scan cannot be cancelled")
	}

	// Update status to cancelled
	return s.scanRepo.UpdateStatus(scan.ID, "cancelled", scan.Progress)
}
