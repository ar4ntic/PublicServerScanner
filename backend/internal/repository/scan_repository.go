package repository

import (
	"database/sql"
	"encoding/json"
	"errors"

	"github.com/google/uuid"
	"github.com/lib/pq"
	"publicscannerapi/internal/models"
)

var (
	ErrScanNotFound = errors.New("scan not found")
)

// ScanRepository handles scan database operations
type ScanRepository struct {
	db *sql.DB
}

// NewScanRepository creates a new scan repository
func NewScanRepository(db *sql.DB) *ScanRepository {
	return &ScanRepository{db: db}
}

// Create creates a new scan job
func (r *ScanRepository) Create(scan *models.ScanJob) error {
	query := `
		INSERT INTO scan_jobs (id, target_id, url, organization_id, initiated_by, status, progress, checks, config)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
		RETURNING created_at, updated_at
	`

	err := r.db.QueryRow(
		query,
		scan.ID,
		scan.TargetID,
		scan.URL,
		scan.OrganizationID,
		scan.InitiatedBy,
		scan.Status,
		scan.Progress,
		pq.Array(scan.Checks),
		scan.Config,
	).Scan(&scan.CreatedAt, &scan.UpdatedAt)

	return err
}

// GetByID retrieves a scan by ID
func (r *ScanRepository) GetByID(id uuid.UUID) (*models.ScanJob, error) {
	scan := &models.ScanJob{}
	query := `
		SELECT id, target_id, url, organization_id, initiated_by, status, progress, checks, config,
		       started_at, completed_at, created_at, updated_at
		FROM scan_jobs
		WHERE id = $1
	`

	var checks pq.StringArray

	err := r.db.QueryRow(query, id).Scan(
		&scan.ID,
		&scan.TargetID,
		&scan.URL,
		&scan.OrganizationID,
		&scan.InitiatedBy,
		&scan.Status,
		&scan.Progress,
		&checks,
		&scan.Config,
		&scan.StartedAt,
		&scan.CompletedAt,
		&scan.CreatedAt,
		&scan.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, ErrScanNotFound
	}
	if err != nil {
		return nil, err
	}

	scan.Checks = checks

	return scan, nil
}

// ListByOrganization retrieves all scans for an organization
func (r *ScanRepository) ListByOrganization(organizationID uuid.UUID, limit, offset int) ([]*models.ScanJob, error) {
	query := `
		SELECT id, target_id, url, organization_id, initiated_by, status, progress, checks, config,
		       started_at, completed_at, created_at, updated_at
		FROM scan_jobs
		WHERE organization_id = $1
		ORDER BY created_at DESC
		LIMIT $2 OFFSET $3
	`

	rows, err := r.db.Query(query, organizationID, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var scans []*models.ScanJob
	for rows.Next() {
		scan := &models.ScanJob{}
		var checks pq.StringArray

		err := rows.Scan(
			&scan.ID,
			&scan.TargetID,
			&scan.URL,
			&scan.OrganizationID,
			&scan.InitiatedBy,
			&scan.Status,
			&scan.Progress,
			&checks,
			&scan.Config,
			&scan.StartedAt,
			&scan.CompletedAt,
			&scan.CreatedAt,
			&scan.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}

		scan.Checks = checks
		scans = append(scans, scan)
	}

	return scans, nil
}

// ListByTarget retrieves all scans for a target
func (r *ScanRepository) ListByTarget(targetID uuid.UUID) ([]*models.ScanJob, error) {
	query := `
		SELECT id, target_id, url, organization_id, initiated_by, status, progress, checks, config,
		       started_at, completed_at, created_at, updated_at
		FROM scan_jobs
		WHERE target_id = $1
		ORDER BY created_at DESC
	`

	rows, err := r.db.Query(query, targetID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var scans []*models.ScanJob
	for rows.Next() {
		scan := &models.ScanJob{}
		var checks pq.StringArray

		err := rows.Scan(
			&scan.ID,
			&scan.TargetID,
			&scan.URL,
			&scan.OrganizationID,
			&scan.InitiatedBy,
			&scan.Status,
			&scan.Progress,
			&checks,
			&scan.Config,
			&scan.StartedAt,
			&scan.CompletedAt,
			&scan.CreatedAt,
			&scan.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}

		scan.Checks = checks
		scans = append(scans, scan)
	}

	return scans, nil
}

// UpdateStatus updates a scan's status and progress
func (r *ScanRepository) UpdateStatus(id uuid.UUID, status string, progress int) error {
	query := `
		UPDATE scan_jobs
		SET status = $2, progress = $3
		WHERE id = $1
	`

	result, err := r.db.Exec(query, id, status, progress)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrScanNotFound
	}

	return nil
}

// Complete marks a scan as completed
func (r *ScanRepository) Complete(id uuid.UUID) error {
	query := `
		UPDATE scan_jobs
		SET status = 'completed', progress = 100, completed_at = NOW()
		WHERE id = $1
	`

	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrScanNotFound
	}

	return nil
}

// Fail marks a scan as failed
func (r *ScanRepository) Fail(id uuid.UUID) error {
	query := `
		UPDATE scan_jobs
		SET status = 'failed', completed_at = NOW()
		WHERE id = $1
	`

	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrScanNotFound
	}

	return nil
}

// GetResults retrieves scan results for a scan
func (r *ScanRepository) GetResults(scanID uuid.UUID) ([]*models.ScanResult, error) {
	query := `
		SELECT id, scan_id, check_type, status, data, findings, severity, created_at
		FROM scan_results
		WHERE scan_id = $1
		ORDER BY created_at ASC
	`

	rows, err := r.db.Query(query, scanID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []*models.ScanResult
	for rows.Next() {
		result := &models.ScanResult{}
		var dataJSON []byte

		err := rows.Scan(
			&result.ID,
			&result.ScanID,
			&result.CheckType,
			&result.Status,
			&dataJSON,
			&result.Findings,
			&result.Severity,
			&result.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		if err := json.Unmarshal(dataJSON, &result.Data); err != nil {
			return nil, err
		}

		results = append(results, result)
	}

	return results, nil
}

// CreateResult creates a new scan result
func (r *ScanRepository) CreateResult(result *models.ScanResult) error {
	dataJSON, err := json.Marshal(result.Data)
	if err != nil {
		return err
	}

	query := `
		INSERT INTO scan_results (id, scan_id, check_type, status, data, findings, severity)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
		RETURNING created_at
	`

	err = r.db.QueryRow(
		query,
		result.ID,
		result.ScanID,
		result.CheckType,
		result.Status,
		dataJSON,
		result.Findings,
		result.Severity,
	).Scan(&result.CreatedAt)

	return err
}
