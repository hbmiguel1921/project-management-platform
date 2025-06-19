package models

import (
	"github.com/google/uuid"
	"time"
)

type ProjectStatus string

const (
	ProjectStatusPlanning  ProjectStatus = "planning"
	ProjectStatusActive    ProjectStatus = "active"
	ProjectStatusOnHold    ProjectStatus = "on_hold"
	ProjectStatusCompleted ProjectStatus = "completed"
	ProjectStatusArchived  ProjectStatus = "archived"
)

type Project struct {
	BaseModel
	Name             string                 `json:"name" gorm:"not null"`
	Key              string                 `json:"key" gorm:"uniqueIndex;not null"` // Ej: "PROJ"
	Description      string                 `json:"description"`
	Status           ProjectStatus          `json:"status" gorm:"default:'planning'"`
	OwnerID          uuid.UUID              `json:"owner_id" gorm:"not null"`
	StartDate        *time.Time             `json:"start_date"`
	EndDate          *time.Time             `json:"end_date"`
	Budget           float64                `json:"budget"`
	RepositoryURL    string                 `json:"repository_url"`
	DocumentationURL string                 `json:"documentation_url"`
	Metadata         map[string]interface{} `json:"metadata" gorm:"type:jsonb"`
	IsPublic         bool                   `json:"is_public" gorm:"default:false"`

	// Configuraciones
	Settings ProjectSettings `json:"settings" gorm:"embedded"`

	// Relaciones
	Members []ProjectMember `json:"members,omitempty"`
	Epics   []Epic          `json:"epics,omitempty"`
	Sprints []Sprint        `json:"sprints,omitempty"`
	Tasks   []Task          `json:"tasks,omitempty"`
	Boards  []Board         `json:"boards,omitempty"`
}

type ProjectSettings struct {
	AllowExternalUsers bool     `json:"allow_external_users" gorm:"default:false"`
	DefaultTaskType    string   `json:"default_task_type" gorm:"default:'task'"`
	WorkflowStates     []string `json:"workflow_states" gorm:"type:jsonb"`
	EstimationUnit     string   `json:"estimation_unit" gorm:"default:'hours'"` // hours, points
}

type ProjectMember struct {
	BaseModel
	ProjectID uuid.UUID   `json:"project_id" gorm:"not null"`
	UserID    uuid.UUID   `json:"user_id" gorm:"not null"`
	Role      ProjectRole `json:"role" gorm:"not null"`
	JoinedAt  time.Time   `json:"joined_at" gorm:"default:CURRENT_TIMESTAMP"`

	// Relaciones
	Project *Project `json:"project,omitempty"`
	User    *User    `json:"user,omitempty"`
}

type ProjectRole string

const (
	ProjectRoleOwner     ProjectRole = "owner"
	ProjectRoleManager   ProjectRole = "manager"
	ProjectRoleDeveloper ProjectRole = "developer"
	ProjectRoleTester    ProjectRole = "tester"
	ProjectRoleViewer    ProjectRole = "viewer"
)

type CreateProjectRequest struct {
	Name        string                `json:"name" binding:"required,min=2,max=100"`
	Key         string                `json:"key" binding:"required,min=2,max=10,uppercase"`
	Description string                `json:"description"`
	StartDate   *time.Time            `json:"start_date"`
	EndDate     *time.Time            `json:"end_date"`
	Budget      float64               `json:"budget"`
	IsPublic    bool                  `json:"is_public"`
	Settings    ProjectSettings       `json:"settings"`
	Members     []ProjectMemberInvite `json:"members"`
}

type UpdateProjectRequest struct {
	Name        string          `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Description string          `json:"description,omitempty"`
	Status      ProjectStatus   `json:"status,omitempty"`
	StartDate   *time.Time      `json:"start_date,omitempty"`
	EndDate     *time.Time      `json:"end_date,omitempty"`
	Budget      float64         `json:"budget,omitempty"`
	IsPublic    *bool           `json:"is_public,omitempty"`
	Settings    ProjectSettings `json:"settings,omitempty"`
}

type ProjectMemberInvite struct {
	UserID uuid.UUID   `json:"user_id" binding:"required"`
	Role   ProjectRole `json:"role" binding:"required"`
}

type ProjectStats struct {
	TotalTasks      int `json:"total_tasks"`
	CompletedTasks  int `json:"completed_tasks"`
	InProgressTasks int `json:"in_progress_tasks"`
	TodoTasks       int `json:"todo_tasks"`
	TotalMembers    int `json:"total_members"`
	ActiveSprints   int `json:"active_sprints"`
}

type ProjectDashboard struct {
	Project      *Project      `json:"project"`
	Stats        *ProjectStats `json:"stats"`
	RecentTasks  []Task        `json:"recent_tasks"`
	ActiveSprint *Sprint       `json:"active_sprint,omitempty"`
}

func (p *Project) IsActive() bool {
	return p.Status == ProjectStatusActive
}

func (p *Project) CanUserAccess(userID uuid.UUID, userRole UserRole) bool {
	if userRole == RoleAdmin {
		return true
	}

	if p.IsPublic {
		return true
	}

	// Verificar membresía en el proyecto
	for _, member := range p.Members {
		if member.UserID == userID {
			return true
		}
	}

	return false
}

func (pm *ProjectMember) CanManageProject() bool {
	return pm.Role == ProjectRoleOwner || pm.Role == ProjectRoleManager
}

func (pm *ProjectMember) CanEditTasks() bool {
	return pm.Role != ProjectRoleViewer
}
