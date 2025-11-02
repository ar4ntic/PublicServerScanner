package models

import (
	"database/sql/driver"
	"encoding/json"
	"time"

	"github.com/google/uuid"
)

type ScanStatus string

const (
	ScanStatusQueued     ScanStatus = "queued"
	ScanStatusRunning    ScanStatus = "running"
	ScanStatusCompleted  ScanStatus = "completed"
	ScanStatusFailed     ScanStatus = "failed"
	ScanStatusCancelled  ScanStatus = "cancelled"
)

type ScanJob struct {
	ID             uuid.UUID      `json:"id" db:"id"`
	TargetID       *uuid.UUID     `json:"target_id,omitempty" db:"target_id"` // Optional: for saved targets
	URL            *string        `json:"url,omitempty" db:"url"`              // Optional: for quick scans
	OrganizationID uuid.UUID      `json:"organization_id" db:"organization_id"`
	InitiatedBy    uuid.UUID      `json:"initiated_by" db:"initiated_by"`
	Status         ScanStatus     `json:"status" db:"status"`
	Progress       int            `json:"progress" db:"progress"` // 0-100
	Checks         []string       `json:"checks" db:"checks"`
	Config         ScanConfig     `json:"config" db:"config"`
	StartedAt      *time.Time     `json:"started_at" db:"started_at"`
	CompletedAt    *time.Time     `json:"completed_at" db:"completed_at"`
	CreatedAt      time.Time      `json:"created_at" db:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at" db:"updated_at"`
}

type ScanConfig struct {
	PortScanEnabled     bool   `json:"port_scan_enabled"`
	HeadersCheckEnabled bool   `json:"headers_check_enabled"`
	SSLCheckEnabled     bool   `json:"ssl_check_enabled"`
	DNSCheckEnabled     bool   `json:"dns_check_enabled"`
	BruteforceEnabled   bool   `json:"bruteforce_enabled"`
	PingCheckEnabled    bool   `json:"ping_check_enabled"`
	Timeout             int    `json:"timeout"` // seconds
	CustomWordlist      string `json:"custom_wordlist"`
}

// Implement sql.Scanner and driver.Valuer for ScanConfig
func (sc *ScanConfig) Scan(value interface{}) error {
	bytes, ok := value.([]byte)
	if !ok {
		return nil
	}
	return json.Unmarshal(bytes, sc)
}

func (sc ScanConfig) Value() (driver.Value, error) {
	return json.Marshal(sc)
}

type ScanResult struct {
	ID        uuid.UUID       `json:"id" db:"id"`
	ScanID    uuid.UUID       `json:"scan_id" db:"scan_id"`
	CheckType string          `json:"check_type" db:"check_type"`
	Status    string          `json:"status" db:"status"`
	Data      json.RawMessage `json:"data" db:"data"` // JSONB
	Findings  int             `json:"findings" db:"findings"`
	Severity  string          `json:"severity" db:"severity"`
	CreatedAt time.Time       `json:"created_at" db:"created_at"`
}

type CreateScanRequest struct {
	TargetID *uuid.UUID `json:"target_id,omitempty"` // Optional: for saved target
	URL      *string    `json:"url,omitempty"`       // Optional: for quick scan
	Checks   []string   `json:"checks"`
	Config   ScanConfig `json:"config"`
}

type ScanProgress struct {
	ScanID      uuid.UUID  `json:"scan_id"`
	Status      ScanStatus `json:"status"`
	Progress    int        `json:"progress"`
	CurrentStep string     `json:"current_step"`
	UpdatedAt   time.Time  `json:"updated_at"`
}
