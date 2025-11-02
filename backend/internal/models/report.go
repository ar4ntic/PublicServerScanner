package models

import (
	"time"

	"github.com/google/uuid"
)

type Report struct {
	ID             uuid.UUID `json:"id" db:"id"`
	ScanID         uuid.UUID `json:"scan_id" db:"scan_id"`
	OrganizationID uuid.UUID `json:"organization_id" db:"organization_id"`
	GeneratedBy    uuid.UUID `json:"generated_by" db:"generated_by"`
	Format         string    `json:"format" db:"format"` // pdf, html, json, csv
	FileName       string    `json:"file_name" db:"file_name"`
	FilePath       string    `json:"file_path" db:"file_path"`
	FileSize       int64     `json:"file_size" db:"file_size"`
	CreatedAt      time.Time `json:"created_at" db:"created_at"`
}

type GenerateReportRequest struct {
	ScanID uuid.UUID `json:"scan_id" binding:"required"`
	Format string    `json:"format" binding:"required,oneof=pdf html json csv"`
}
