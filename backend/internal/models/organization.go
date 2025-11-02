package models

import (
	"time"

	"github.com/google/uuid"
)

type Organization struct {
	ID        uuid.UUID `json:"id" db:"id"`
	Name      string    `json:"name" db:"name"`
	OwnerID   uuid.UUID `json:"owner_id" db:"owner_id"`
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

type OrganizationMember struct {
	ID             uuid.UUID `json:"id" db:"id"`
	OrganizationID uuid.UUID `json:"organization_id" db:"organization_id"`
	UserID         uuid.UUID `json:"user_id" db:"user_id"`
	Role           string    `json:"role" db:"role"` // owner, admin, member, viewer
	JoinedAt       time.Time `json:"joined_at" db:"joined_at"`
}

type Role string

const (
	RoleOwner  Role = "owner"
	RoleAdmin  Role = "admin"
	RoleMember Role = "member"
	RoleViewer Role = "viewer"
)

type CreateOrganizationRequest struct {
	Name string `json:"name" binding:"required,min=3,max=100"`
}
