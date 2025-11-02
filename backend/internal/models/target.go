package models

import (
	"time"

	"github.com/google/uuid"
)

type Target struct {
	ID             uuid.UUID `json:"id" db:"id"`
	OrganizationID uuid.UUID `json:"organization_id" db:"organization_id"`
	Name           string    `json:"name" db:"name"`
	Hostname       string    `json:"hostname" db:"hostname"`
	Description    string    `json:"description" db:"description"`
	Tags           []string  `json:"tags" db:"tags"`
	IsActive       bool      `json:"is_active" db:"is_active"`
	CreatedBy      uuid.UUID `json:"created_by" db:"created_by"`
	CreatedAt      time.Time `json:"created_at" db:"created_at"`
	UpdatedAt      time.Time `json:"updated_at" db:"updated_at"`
}

type CreateTargetRequest struct {
	Name        string   `json:"name" binding:"required,min=3,max=100"`
	Hostname    string   `json:"hostname" binding:"required"`
	Description string   `json:"description"`
	Tags        []string `json:"tags"`
}

type UpdateTargetRequest struct {
	Name        string   `json:"name"`
	Description string   `json:"description"`
	Tags        []string `json:"tags"`
	IsActive    *bool    `json:"is_active"`
}
