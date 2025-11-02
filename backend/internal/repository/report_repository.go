package repository

import (
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"publicscannerapi/internal/models"
)

var (
	ErrReportNotFound = errors.New("report not found")
)

// ReportRepository handles report database operations
type ReportRepository struct {
	db *sql.DB
}

// NewReportRepository creates a new report repository
func NewReportRepository(db *sql.DB) *ReportRepository {
	return &ReportRepository{db: db}
}

// Create creates a new report
func (r *ReportRepository) Create(report *models.Report) error {
	query := `
		INSERT INTO reports (id, scan_id, organization_id, generated_by, format, file_name, file_path, file_size)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING created_at
	`

	err := r.db.QueryRow(
		query,
		report.ID,
		report.ScanID,
		report.OrganizationID,
		report.GeneratedBy,
		report.Format,
		report.FileName,
		report.FilePath,
		report.FileSize,
	).Scan(&report.CreatedAt)

	return err
}

// GetByID retrieves a report by ID
func (r *ReportRepository) GetByID(id uuid.UUID) (*models.Report, error) {
	report := &models.Report{}
	query := `
		SELECT id, scan_id, organization_id, generated_by, format, file_name, file_path, file_size, created_at
		FROM reports
		WHERE id = $1
	`

	err := r.db.QueryRow(query, id).Scan(
		&report.ID,
		&report.ScanID,
		&report.OrganizationID,
		&report.GeneratedBy,
		&report.Format,
		&report.FileName,
		&report.FilePath,
		&report.FileSize,
		&report.CreatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, ErrReportNotFound
	}
	if err != nil {
		return nil, err
	}

	return report, nil
}

// ListByOrganization retrieves all reports for an organization
func (r *ReportRepository) ListByOrganization(organizationID uuid.UUID, limit, offset int) ([]*models.Report, error) {
	query := `
		SELECT id, scan_id, organization_id, generated_by, format, file_name, file_path, file_size, created_at
		FROM reports
		WHERE organization_id = $1
		ORDER BY created_at DESC
		LIMIT $2 OFFSET $3
	`

	rows, err := r.db.Query(query, organizationID, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var reports []*models.Report
	for rows.Next() {
		report := &models.Report{}

		err := rows.Scan(
			&report.ID,
			&report.ScanID,
			&report.OrganizationID,
			&report.GeneratedBy,
			&report.Format,
			&report.FileName,
			&report.FilePath,
			&report.FileSize,
			&report.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		reports = append(reports, report)
	}

	return reports, nil
}

// ListByScan retrieves all reports for a scan
func (r *ReportRepository) ListByScan(scanID uuid.UUID) ([]*models.Report, error) {
	query := `
		SELECT id, scan_id, organization_id, generated_by, format, file_name, file_path, file_size, created_at
		FROM reports
		WHERE scan_id = $1
		ORDER BY created_at DESC
	`

	rows, err := r.db.Query(query, scanID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var reports []*models.Report
	for rows.Next() {
		report := &models.Report{}

		err := rows.Scan(
			&report.ID,
			&report.ScanID,
			&report.OrganizationID,
			&report.GeneratedBy,
			&report.Format,
			&report.FileName,
			&report.FilePath,
			&report.FileSize,
			&report.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		reports = append(reports, report)
	}

	return reports, nil
}

// Delete deletes a report
func (r *ReportRepository) Delete(id uuid.UUID) error {
	query := `DELETE FROM reports WHERE id = $1`
	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrReportNotFound
	}

	return nil
}
