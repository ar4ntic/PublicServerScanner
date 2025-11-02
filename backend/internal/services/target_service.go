package services

import (
	"github.com/google/uuid"
	"publicscannerapi/internal/models"
	"publicscannerapi/internal/repository"
)

// TargetService handles target business logic
type TargetService struct {
	targetRepo *repository.TargetRepository
}

// NewTargetService creates a new target service
func NewTargetService(targetRepo *repository.TargetRepository) *TargetService {
	return &TargetService{
		targetRepo: targetRepo,
	}
}

// CreateTargetRequest represents a target creation request
type CreateTargetRequest struct {
	Name        string   `json:"name" binding:"required"`
	Hostname    string   `json:"hostname" binding:"required"`
	Description string   `json:"description"`
	Tags        []string `json:"tags"`
}

// UpdateTargetRequest represents a target update request
type UpdateTargetRequest struct {
	Name        string   `json:"name"`
	Hostname    string   `json:"hostname"`
	Description string   `json:"description"`
	Tags        []string `json:"tags"`
	IsActive    *bool    `json:"is_active"`
}

// CreateTarget creates a new target
func (s *TargetService) CreateTarget(req *CreateTargetRequest, userID, organizationID uuid.UUID) (*models.Target, error) {
	target := &models.Target{
		ID:             uuid.New(),
		OrganizationID: organizationID,
		Name:           req.Name,
		Hostname:       req.Hostname,
		Description:    req.Description,
		Tags:           req.Tags,
		IsActive:       true,
		CreatedBy:      userID,
	}

	if err := s.targetRepo.Create(target); err != nil {
		return nil, err
	}

	return target, nil
}

// GetTarget retrieves a target by ID
func (s *TargetService) GetTarget(targetID, organizationID uuid.UUID) (*models.Target, error) {
	target, err := s.targetRepo.GetByID(targetID)
	if err != nil {
		return nil, err
	}

	// Verify target belongs to organization
	if target.OrganizationID != organizationID {
		return nil, repository.ErrTargetNotFound
	}

	return target, nil
}

// ListTargets retrieves all targets for an organization
func (s *TargetService) ListTargets(organizationID uuid.UUID) ([]*models.Target, error) {
	return s.targetRepo.ListByOrganization(organizationID)
}

// UpdateTarget updates a target
func (s *TargetService) UpdateTarget(targetID, organizationID uuid.UUID, req *UpdateTargetRequest) (*models.Target, error) {
	// Get existing target
	target, err := s.GetTarget(targetID, organizationID)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.Name != "" {
		target.Name = req.Name
	}
	if req.Hostname != "" {
		target.Hostname = req.Hostname
	}
	if req.Description != "" {
		target.Description = req.Description
	}
	if req.Tags != nil {
		target.Tags = req.Tags
	}
	if req.IsActive != nil {
		target.IsActive = *req.IsActive
	}

	// Save updates
	if err := s.targetRepo.Update(target); err != nil {
		return nil, err
	}

	return target, nil
}

// DeleteTarget deletes a target
func (s *TargetService) DeleteTarget(targetID, organizationID uuid.UUID) error {
	// Verify target exists and belongs to organization
	_, err := s.GetTarget(targetID, organizationID)
	if err != nil {
		return err
	}

	return s.targetRepo.Delete(targetID)
}
