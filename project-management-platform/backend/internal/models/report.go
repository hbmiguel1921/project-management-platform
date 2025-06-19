package models

import (
	"time"
	"github.com/google/uuid"
)

type Report struct {
	BaseModel
	Name        string     `json:"name" gorm:"not null"`
	Description string     `json:"description"`
	Type        ReportType `json:"type" gorm:"not null"`
	ProjectID   *uuid.UUID `json:"project_id"`
	UserID      uuid.UUID  `json:"user_id" gorm:"not null"`
	IsPublic    bool       `json:"is_public" gorm:"default:false"`
	Schedule    string     `json:"schedule"` // Cron expression para reportes automáticos
	
	// Configuración del reporte
	Config      map[string]interface{} `json:"config" gorm:"type:jsonb"`
	Filters     map[string]interface{} `json:"filters" gorm:"type:jsonb"`
	
	// Timestamps
	LastGenerated *time.Time `json:"last_generated"`
	
	// Relaciones
	Project *Project `json:"project,omitempty"`
	User    *User    `json:"user,omitempty"`
}

type ReportType string

const (
	ReportTypeTaskSummary      ReportType = "task_summary"
	ReportTypeProjectProgress  ReportType = "project_progress"
	ReportTypeTimeTracking     ReportType = "time_tracking"
	ReportTypeTeamPerformance  ReportType = "team_performance"
	ReportTypeSprintBurndown   ReportType = "sprint_burndown"
	ReportTypeVelocityChart    ReportType = "velocity_chart"
	ReportTypeBudgetAnalysis   ReportType = "budget_analysis"
	ReportTypeCustom           ReportType = "custom"
)

type ReportData struct {
	ID          string                 `json:"id"`
	Name        string                 `json:"name"`
	Type        ReportType             `json:"type"`
	GeneratedAt time.Time              `json:"generated_at"`
	Data        map[string]interface{} `json:"data"`
	Charts      []ChartData            `json:"charts"`
	Tables      []TableData            `json:"tables"`
	Summary     ReportSummary          `json:"summary"`
}

type ChartData struct {
	Title  string                 `json:"title"`
	Type   string                 `json:"type"` // line, bar, pie, etc.
	Data   map[string]interface{} `json:"data"`
	Config map[string]interface{} `json:"config"`
}

type TableData struct {
	Title   string                   `json:"title"`
	Headers []string                 `json:"headers"`
	Rows    [][]interface{}          `json:"rows"`
	Summary map[string]interface{}   `json:"summary"`
}

type ReportSummary struct {
	TotalItems     int                    `json:"total_items"`
	CompletedItems int                    `json:"completed_items"`
	Metrics        map[string]interface{} `json:"metrics"`
	Insights       []string               `json:"insights"`
}

type CreateReportRequest struct {
	Name        string                 `json:"name" binding:"required,min=2,max=100"`
	Description string                 `json:"description"`
	Type        ReportType             `json:"type" binding:"required"`
	ProjectID   *uuid.UUID             `json:"project_id"`
	IsPublic    bool                   `json:"is_public"`
	Config      map[string]interface{} `json:"config"`
	Filters     map[string]interface{} `json:"filters"`
	Schedule    string                 `json:"schedule"`
}

type UpdateReportRequest struct {
	Name        string                 `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Description string                 `json:"description,omitempty"`
	IsPublic    *bool                  `json:"is_public,omitempty"`
	Config      map[string]interface{} `json:"config,omitempty"`
	Filters     map[string]interface{} `json:"filters,omitempty"`
	Schedule    string                 `json:"schedule,omitempty"`
}

// Modelos para métricas y analytics
type ProjectMetrics struct {
	ProjectID       uuid.UUID `json:"project_id"`
	TasksTotal      int       `json:"tasks_total"`
	TasksCompleted  int       `json:"tasks_completed"`
	TasksInProgress int       `json:"tasks_in_progress"`
	TasksOverdue    int       `json:"tasks_overdue"`
	CompletionRate  float64   `json:"completion_rate"`
	
	// Métricas de tiempo
	TotalTimeSpent   int     `json:"total_time_spent"`   // En minutos
	AverageTaskTime  float64 `json:"average_task_time"`  // En horas
	EstimatedVsActual float64 `json:"estimated_vs_actual"` // Ratio
	
	// Métricas del equipo
	ActiveMembers    int     `json:"active_members"`
	Velocity         float64 `json:"velocity"`
	BurndownRate     float64 `json:"burndown_rate"`
	
	// Periodo de cálculo
	PeriodStart time.Time `json:"period_start"`
	PeriodEnd   time.Time `json:"period_end"`
}

type UserMetrics struct {
	UserID         uuid.UUID `json:"user_id"`
	TasksCompleted int       `json:"tasks_completed"`
	TasksAssigned  int       `json:"tasks_assigned"`
	TimeSpent      int       `json:"time_spent"` // En minutos
	Productivity   float64   `json:"productivity"`
	
	// Métricas de colaboración
	CommentsPosted int `json:"comments_posted"`
	WikiContributions int `json:"wiki_contributions"`
	
	PeriodStart time.Time `json:"period_start"`
	PeriodEnd   time.Time `json:"period_end"`
}

type DashboardWidget struct {
	BaseModel
	Title       string                 `json:"title" gorm:"not null"`
	Type        string                 `json:"type" gorm:"not null"` // chart, metric, table, list
	Size        string                 `json:"size"`                 // small, medium, large
	Position    int                    `json:"position"`
	UserID      uuid.UUID              `json:"user_id" gorm:"not null"`
	ProjectID   *uuid.UUID             `json:"project_id"`
	Config      map[string]interface{} `json:"config" gorm:"type:jsonb"`
	IsVisible   bool                   `json:"is_visible" gorm:"default:true"`
	
	// Relaciones
	User    *User    `json:"user,omitempty"`
	Project *Project `json:"project,omitempty"`
}
