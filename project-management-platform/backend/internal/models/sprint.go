package models

import (
	"time"
	"github.com/google/uuid"
)

type Sprint struct {
	BaseModel
	Name        string       `json:"name" gorm:"not null"`
	Description string       `json:"description"`
	ProjectID   uuid.UUID    `json:"project_id" gorm:"not null"`
	StartDate   time.Time    `json:"start_date" gorm:"not null"`
	EndDate     time.Time    `json:"end_date" gorm:"not null"`
	Status      SprintStatus `json:"status" gorm:"default:'planning'"`
	Goal        string       `json:"goal"`
	
	// Métricas del sprint
	Capacity        int     `json:"capacity"`          // Capacidad en story points
	CommittedPoints int     `json:"committed_points"`  // Story points comprometidos
	CompletedPoints int     `json:"completed_points"`  // Story points completados
	Velocity        float64 `json:"velocity"`          // Velocidad del equipo
	
	// Relaciones
	Project *Project `json:"project,omitempty"`
	Tasks   []Task   `json:"tasks,omitempty"`
	Events  []SprintEvent `json:"events,omitempty"`
}

type SprintStatus string

const (
	SprintStatusPlanning SprintStatus = "planning"
	SprintStatusActive   SprintStatus = "active"
	SprintStatusCompleted SprintStatus = "completed"
	SprintStatusCancelled SprintStatus = "cancelled"
)

type SprintEvent struct {
	BaseModel
	SprintID uuid.UUID        `json:"sprint_id" gorm:"not null"`
	Type     SprintEventType  `json:"type" gorm:"not null"`
	Title    string           `json:"title" gorm:"not null"`
	Content  string           `json:"content"`
	UserID   uuid.UUID        `json:"user_id" gorm:"not null"`
	Date     time.Time        `json:"date" gorm:"not null"`
	
	// Relaciones
	Sprint *Sprint `json:"sprint,omitempty"`
	User   *User   `json:"user,omitempty"`
}

type SprintEventType string

const (
	SprintEventTypePlanning    SprintEventType = "planning"
	SprintEventTypeDaily       SprintEventType = "daily"
	SprintEventTypeReview      SprintEventType = "review"
	SprintEventTypeRetrospective SprintEventType = "retrospective"
	SprintEventTypeCustom      SprintEventType = "custom"
)

type CreateSprintRequest struct {
	Name        string    `json:"name" binding:"required,min=2,max=100"`
	Description string    `json:"description"`
	StartDate   time.Time `json:"start_date" binding:"required"`
	EndDate     time.Time `json:"end_date" binding:"required"`
	Goal        string    `json:"goal"`
	Capacity    int       `json:"capacity"`
}

type UpdateSprintRequest struct {
	Name        string    `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Description string    `json:"description,omitempty"`
	StartDate   time.Time `json:"start_date,omitempty"`
	EndDate     time.Time `json:"end_date,omitempty"`
	Goal        string    `json:"goal,omitempty"`
	Capacity    int       `json:"capacity,omitempty"`
}

func (s *Sprint) IsActive() bool {
	now := time.Now()
	return s.Status == SprintStatusActive && 
		   s.StartDate.Before(now) && 
		   s.EndDate.After(now)
}

func (s *Sprint) CalculateVelocity() float64 {
	if s.Capacity > 0 {
		return float64(s.CompletedPoints) / float64(s.Capacity) * 100
	}
	return 0
}

func (s *Sprint) GetDaysRemaining() int {
	if !s.IsActive() {
		return 0
	}
	return int(s.EndDate.Sub(time.Now()).Hours() / 24)
}
