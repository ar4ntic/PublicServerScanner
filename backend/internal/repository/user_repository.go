package repository

import (
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"publicscannerapi/internal/models"
)

var (
	ErrUserNotFound     = errors.New("user not found")
	ErrEmailExists      = errors.New("email already exists")
	ErrInvalidPassword  = errors.New("invalid password")
)

// UserRepository handles user database operations
type UserRepository struct {
	db *sql.DB
}

// NewUserRepository creates a new user repository
func NewUserRepository(db *sql.DB) *UserRepository {
	return &UserRepository{db: db}
}

// Create creates a new user
func (r *UserRepository) Create(user *models.User) error {
	query := `
		INSERT INTO users (id, email, password_hash, first_name, last_name, is_active)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING created_at, updated_at
	`

	err := r.db.QueryRow(
		query,
		user.ID,
		user.Email,
		user.PasswordHash,
		user.FirstName,
		user.LastName,
		user.IsActive,
	).Scan(&user.CreatedAt, &user.UpdatedAt)

	if err != nil {
		// Check for unique constraint violation
		if err.Error() == `pq: duplicate key value violates unique constraint "users_email_key"` {
			return ErrEmailExists
		}
		return err
	}

	return nil
}

// GetByID retrieves a user by ID
func (r *UserRepository) GetByID(id uuid.UUID) (*models.User, error) {
	user := &models.User{}
	query := `
		SELECT id, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		WHERE id = $1
	`

	err := r.db.QueryRow(query, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.FirstName,
		&user.LastName,
		&user.IsActive,
		&user.CreatedAt,
		&user.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, ErrUserNotFound
	}
	if err != nil {
		return nil, err
	}

	return user, nil
}

// GetByEmail retrieves a user by email
func (r *UserRepository) GetByEmail(email string) (*models.User, error) {
	user := &models.User{}
	query := `
		SELECT id, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		WHERE email = $1
	`

	err := r.db.QueryRow(query, email).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.FirstName,
		&user.LastName,
		&user.IsActive,
		&user.CreatedAt,
		&user.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, ErrUserNotFound
	}
	if err != nil {
		return nil, err
	}

	return user, nil
}

// Update updates a user
func (r *UserRepository) Update(user *models.User) error {
	query := `
		UPDATE users
		SET email = $2, first_name = $3, last_name = $4, is_active = $5
		WHERE id = $1
		RETURNING updated_at
	`

	err := r.db.QueryRow(
		query,
		user.ID,
		user.Email,
		user.FirstName,
		user.LastName,
		user.IsActive,
	).Scan(&user.UpdatedAt)

	if err == sql.ErrNoRows {
		return ErrUserNotFound
	}
	return err
}

// Delete deletes a user
func (r *UserRepository) Delete(id uuid.UUID) error {
	query := `DELETE FROM users WHERE id = $1`
	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrUserNotFound
	}

	return nil
}

// GetUserOrganization retrieves the first organization a user belongs to
func (r *UserRepository) GetUserOrganization(userID uuid.UUID) (*uuid.UUID, error) {
	var orgID uuid.UUID
	query := `
		SELECT organization_id
		FROM organization_members
		WHERE user_id = $1
		LIMIT 1
	`

	err := r.db.QueryRow(query, userID).Scan(&orgID)
	if err == sql.ErrNoRows {
		return nil, nil // No organization found, return nil
	}
	if err != nil {
		return nil, err
	}

	return &orgID, nil
}
