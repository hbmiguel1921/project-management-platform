package models

import (
	"github.com/google/uuid"
	"time"
)

// Epic represents a high level grouping of tasks
// This is a simplified placeholder so the code compiles
// and can be extended in the future.
type Epic struct {
	BaseModel
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	Name        string    `json:"name" gorm:"not null"`
	Description string    `json:"description"`

	// Relationships
	Project *Project `json:"project,omitempty"`
	Tasks   []Task   `json:"tasks,omitempty"`
}

// Board represents a kanban board within a project.
type Board struct {
	BaseModel
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	Name        string    `json:"name" gorm:"not null"`
	Description string    `json:"description"`

	// Relationship
	Project *Project `json:"project,omitempty"`
}

// Attachment represents a file attached to a task.
type Attachment struct {
	BaseModel
	TaskID   uuid.UUID `json:"task_id" gorm:"not null"`
	FileName string    `json:"file_name" gorm:"not null"`
	FileURL  string    `json:"file_url" gorm:"not null"`
	FileSize int64     `json:"file_size"`
	MimeType string    `json:"mime_type"`

	// Relationship
	Task *Task `json:"task,omitempty"`
}

// AuditLog stores auditing information for user actions.
type AuditLog struct {
	BaseModel
	UserID     uuid.UUID              `json:"user_id" gorm:"not null"`
	Action     string                 `json:"action" gorm:"not null"`
	EntityType string                 `json:"entity_type"`
	EntityID   *uuid.UUID             `json:"entity_id"`
	Metadata   map[string]interface{} `json:"metadata" gorm:"type:jsonb"`

	// Relationship
	User *User `json:"user,omitempty"`
}

// TaskAssignment represents a user assigned to a task.
type TaskAssignment struct {
	BaseModel
	TaskID     uuid.UUID `json:"task_id" gorm:"not null"`
	UserID     uuid.UUID `json:"user_id" gorm:"not null"`
	AssignedAt time.Time `json:"assigned_at" gorm:"default:CURRENT_TIMESTAMP"`
	AssignedBy uuid.UUID `json:"assigned_by" gorm:"not null"`

	// Relationships
	Task *Task `json:"task,omitempty"`
	User *User `json:"user,omitempty"`
}
