package models

import (
	"time"
	"github.com/google/uuid"
)

type TaskType string

const (
	TaskTypeStory    TaskType = "story"
	TaskTypeTask     TaskType = "task"
	TaskTypeBug      TaskType = "bug"
	TaskTypeEpic     TaskType = "epic"
	TaskTypeSubtask  TaskType = "subtask"
)

type TaskStatus string

const (
	TaskStatusTodo       TaskStatus = "todo"
	TaskStatusInProgress TaskStatus = "in_progress"
	TaskStatusInReview   TaskStatus = "in_review"
	TaskStatusDone       TaskStatus = "done"
	TaskStatusBlocked    TaskStatus = "blocked"
	TaskStatusCancelled  TaskStatus = "cancelled"
)

type TaskPriority string

const (
	TaskPriorityLowest  TaskPriority = "lowest"
	TaskPriorityLow     TaskPriority = "low"
	TaskPriorityMedium  TaskPriority = "medium"
	TaskPriorityHigh    TaskPriority = "high"
	TaskPriorityHighest TaskPriority = "highest"
)

type Task struct {
	BaseModel
	Title       string       `json:"title" gorm:"not null"`
	Description string       `json:"description"`
	Type        TaskType     `json:"type" gorm:"default:'task'"`
	Status      TaskStatus   `json:"status" gorm:"default:'todo'"`
	Priority    TaskPriority `json:"priority" gorm:"default:'medium'"`
	
	// Estimación y tiempo
	StoryPoints    *int           `json:"story_points"`
	EstimatedHours *float64       `json:"estimated_hours"`
	LoggedHours    float64        `json:"logged_hours" gorm:"default:0"`
	
	// Fechas
	StartDate *time.Time `json:"start_date"`
	DueDate   *time.Time `json:"due_date"`
	
	// Relaciones
	ProjectID  uuid.UUID  `json:"project_id" gorm:"not null"`
	EpicID     *uuid.UUID `json:"epic_id"`
	SprintID   *uuid.UUID `json:"sprint_id"`
	ParentID   *uuid.UUID `json:"parent_id"` // Para subtareas
	AssigneeID *uuid.UUID `json:"assignee_id"`
	CreatorID  uuid.UUID  `json:"creator_id" gorm:"not null"`
	
	// Entidades relacionadas
	Project    *Project `json:"project,omitempty"`
	Epic       *Epic    `json:"epic,omitempty"`
	Sprint     *Sprint  `json:"sprint,omitempty"`
	Parent     *Task    `json:"parent,omitempty"`
	Assignee   *User    `json:"assignee,omitempty"`
	Creator    *User    `json:"creator,omitempty"`
	
	// Relaciones inversas
	Subtasks     []Task         `json:"subtasks,omitempty" gorm:"foreignKey:ParentID"`
	Comments     []Comment      `json:"comments,omitempty"`
	Attachments  []Attachment   `json:"attachments,omitempty"`
	Dependencies []TaskDependency `json:"dependencies,omitempty" gorm:"foreignKey:TaskID"`
	Blockers     []TaskDependency `json:"blockers,omitempty" gorm:"foreignKey:DependsOnID"`
	TimeEntries  []TimeEntry    `json:"time_entries,omitempty"`
	
	// Campos personalizados
	CustomFields map[string]interface{} `json:"custom_fields" gorm:"type:jsonb"`
	
	// Metadata
	Tags     []string `json:"tags" gorm:"type:jsonb"`
	Labels   []string `json:"labels" gorm:"type:jsonb"`
	Position int      `json:"position" gorm:"default:0"` // Para ordenamiento
}

type TaskDependency struct {
	BaseModel
	TaskID      uuid.UUID      `json:"task_id" gorm:"not null"`
	DependsOnID uuid.UUID      `json:"depends_on_id" gorm:"not null"`
	Type        DependencyType `json:"type" gorm:"default:'blocks'"`
	
	// Relaciones
	Task      *Task `json:"task,omitempty"`
	DependsOn *Task `json:"depends_on,omitempty"`
}

type DependencyType string

const (
	DependencyTypeBlocks     DependencyType = "blocks"
	DependencyTypeFinishStart DependencyType = "finish_start"
	DependencyTypeStartStart  DependencyType = "start_start"
)

type CreateTaskRequest struct {
	Title          string                 `json:"title" binding:"required,min=2,max=200"`
	Description    string                 `json:"description"`
	Type           TaskType               `json:"type"`
	Priority       TaskPriority           `json:"priority"`
	StoryPoints    *int                   `json:"story_points" binding:"omitempty,min=1,max=100"`
	EstimatedHours *float64               `json:"estimated_hours" binding:"omitempty,min=0"`
	StartDate      *time.Time             `json:"start_date"`
	DueDate        *time.Time             `json:"due_date"`
	EpicID         *uuid.UUID             `json:"epic_id"`
	SprintID       *uuid.UUID             `json:"sprint_id"`
	ParentID       *uuid.UUID             `json:"parent_id"`
	AssigneeID     *uuid.UUID             `json:"assignee_id"`
	Tags           []string               `json:"tags"`
	Labels         []string               `json:"labels"`
	CustomFields   map[string]interface{} `json:"custom_fields"`
}

type UpdateTaskRequest struct {
	Title          string                 `json:"title,omitempty" binding:"omitempty,min=2,max=200"`
	Description    string                 `json:"description,omitempty"`
	Type           TaskType               `json:"type,omitempty"`
	Status         TaskStatus             `json:"status,omitempty"`
	Priority       TaskPriority           `json:"priority,omitempty"`
	StoryPoints    *int                   `json:"story_points,omitempty" binding:"omitempty,min=1,max=100"`
	EstimatedHours *float64               `json:"estimated_hours,omitempty" binding:"omitempty,min=0"`
	StartDate      *time.Time             `json:"start_date,omitempty"`
	DueDate        *time.Time             `json:"due_date,omitempty"`
	EpicID         *uuid.UUID             `json:"epic_id,omitempty"`
	SprintID       *uuid.UUID             `json:"sprint_id,omitempty"`
	AssigneeID     *uuid.UUID             `json:"assignee_id,omitempty"`
	Tags           []string               `json:"tags,omitempty"`
	Labels         []string               `json:"labels,omitempty"`
	CustomFields   map[string]interface{} `json:"custom_fields,omitempty"`
}

type TaskFilter struct {
	Status     []TaskStatus   `json:"status,omitempty" form:"status"`
	Priority   []TaskPriority `json:"priority,omitempty" form:"priority"`
	Type       []TaskType     `json:"type,omitempty" form:"type"`
	AssigneeID *uuid.UUID     `json:"assignee_id,omitempty" form:"assignee_id"`
	EpicID     *uuid.UUID     `json:"epic_id,omitempty" form:"epic_id"`
	SprintID   *uuid.UUID     `json:"sprint_id,omitempty" form:"sprint_id"`
	Search     string         `json:"search,omitempty" form:"search"`
	Tags       []string       `json:"tags,omitempty" form:"tags"`
	Labels     []string       `json:"labels,omitempty" form:"labels"`
	DueSoon    bool           `json:"due_soon,omitempty" form:"due_soon"`
}

func (t *Task) IsOverdue() bool {
	if t.DueDate == nil {
		return false
	}
	return time.Now().After(*t.DueDate) && t.Status != TaskStatusDone
}

func (t *Task) IsBlocked() bool {
	return t.Status == TaskStatusBlocked
}

func (t *Task) CanBeAssignedTo(userID uuid.UUID) bool {
	// Verificar que el usuario sea miembro del proyecto
	return true // Lógica de verificación se implementará en el servicio
}

func (t *Task) GetProgress() float64 {
	switch t.Status {
	case TaskStatusDone:
		return 100.0
	case TaskStatusInReview:
		return 90.0
	case TaskStatusInProgress:
		return 50.0
	case TaskStatusTodo:
		return 0.0
	default:
		return 0.0
	}
}

func (t *Task) GetTimeSpent() float64 {
	return t.LoggedHours
}

func (t *Task) GetEfficiency() *float64 {
	if t.EstimatedHours == nil || *t.EstimatedHours == 0 {
		return nil
	}
	
	efficiency := (t.LoggedHours / *t.EstimatedHours) * 100
	return &efficiency
}
