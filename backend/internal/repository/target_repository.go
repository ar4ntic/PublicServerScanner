package repository

import (
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"github.com/lib/pq"
	"publicscannerapi/internal/models"
)

var (
	ErrTargetNotFound = errors.New("target not found")
)

// TargetRepository handles target database operations
type TargetRepository struct {
	db *sql.DB
}

// NewTargetRepository creates a new target repository
func NewTargetRepository(db *sql.DB) *TargetRepository {
	return &TargetRepository{db: db}
}

// Create creates a new target
func (r *TargetRepository) Create(target *models.Target) error {
	query := `
		INSERT INTO targets (id, organization_id, name, hostname, description, tags, is_active, created_by)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING created_at, updated_at
	`

	err := r.db.QueryRow(
		query,
		target.ID,
		target.OrganizationID,
		target.Name,
		target.Hostname,
		target.Description,
		pq.Array(target.Tags),
		target.IsActive,
		target.CreatedBy,
	).Scan(&target.CreatedAt, &target.UpdatedAt)

	return err
}

// GetByID retrieves a target by ID
func (r *TargetRepository) GetByID(id uuid.UUID) (*models.Target, error) {
	target := &models.Target{}
	query := `
		SELECT id, organization_id, name, hostname, description, tags, is_active, created_by, created_at, updated_at
		FROM targets
		WHERE id = $1
	`

	var tags pq.StringArray
	err := r.db.QueryRow(query, id).Scan(
		&target.ID,
		&target.OrganizationID,
		&target.Name,
		&target.Hostname,
		&target.Description,
		&tags,
		&target.IsActive,
		&target.CreatedBy,
		&target.CreatedAt,
		&target.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, ErrTargetNotFound
	}
	if err != nil {
		return nil, err
	}

	target.Tags = tags

	return target, nil
}

// ListByOrganization retrieves all targets for an organization
func (r *TargetRepository) ListByOrganization(organizationID uuid.UUID) ([]*models.Target, error) {
	query := `
		SELECT id, organization_id, name, hostname, description, tags, is_active, created_by, created_at, updated_at
		FROM targets
		WHERE organization_id = $1
		ORDER BY created_at DESC
	`

	rows, err := r.db.Query(query, organizationID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var targets []*models.Target
	for rows.Next() {
		target := &models.Target{}
		var tags pq.StringArray

		err := rows.Scan(
			&target.ID,
			&target.OrganizationID,
			&target.Name,
			&target.Hostname,
			&target.Description,
			&tags,
			&target.IsActive,
			&target.CreatedBy,
			&target.CreatedAt,
			&target.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}

		target.Tags = tags
		targets = append(targets, target)
	}

	return targets, nil
}

// Update updates a target
func (r *TargetRepository) Update(target *models.Target) error {
	query := `
		UPDATE targets
		SET name = $2, hostname = $3, description = $4, tags = $5, is_active = $6
		WHERE id = $1
		RETURNING updated_at
	`

	err := r.db.QueryRow(
		query,
		target.ID,
		target.Name,
		target.Hostname,
		target.Description,
		pq.Array(target.Tags),
		target.IsActive,
	).Scan(&target.UpdatedAt)

	if err == sql.ErrNoRows {
		return ErrTargetNotFound
	}
	return err
}

// Delete deletes a target
func (r *TargetRepository) Delete(id uuid.UUID) error {
	query := `DELETE FROM targets WHERE id = $1`
	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrTargetNotFound
	}

	return nil
}
