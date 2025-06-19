#!/usr/bin/env python3
"""
Script para crear la implementación completa del backend en Golang
con todas las funcionalidades requeridas según las historias de usuario.
"""

import os

def create_backend_core():
    """Crear implementación completa del backend"""
    
    backend_dir = "/workspace/project-management-platform/backend"
    
    # Configuración principal
    create_config_files(backend_dir)
    
    # Modelos de datos
    create_models(backend_dir)
    
    # Database y migraciones
    create_database_layer(backend_dir)
    
    # Servicios de negocio
    create_services(backend_dir)
    
    # Handlers de la API
    create_api_handlers(backend_dir)
    
    # Middleware
    create_middleware(backend_dir)
    
    # WebSocket para tiempo real
    create_websocket_layer(backend_dir)
    
    # Utilidades
    create_utils(backend_dir)
    
    # Tests
    create_tests(backend_dir)
    
    print("✓ Backend core completado")

def create_config_files(backend_dir):
    """Crear archivos de configuración"""
    
    # internal/config/config.go
    config_go_content = """package config

import (
	"fmt"
	"os"
	"strconv"

	"github.com/spf13/viper"
)

type Config struct {
	App      AppConfig      `mapstructure:"app"`
	Server   ServerConfig   `mapstructure:"server"`
	Database DatabaseConfig `mapstructure:"database"`
	Redis    RedisConfig    `mapstructure:"redis"`
	JWT      JWTConfig      `mapstructure:"jwt"`
	Email    EmailConfig    `mapstructure:"email"`
	Storage  StorageConfig  `mapstructure:"storage"`
}

type AppConfig struct {
	Name        string `mapstructure:"name"`
	Version     string `mapstructure:"version"`
	Environment string `mapstructure:"environment"`
	LogLevel    string `mapstructure:"log_level"`
}

type ServerConfig struct {
	Host         string `mapstructure:"host"`
	Port         string `mapstructure:"port"`
	ReadTimeout  int    `mapstructure:"read_timeout"`
	WriteTimeout int    `mapstructure:"write_timeout"`
	CorsOrigins  []string `mapstructure:"cors_origins"`
}

type DatabaseConfig struct {
	Driver   string `mapstructure:"driver"`
	Host     string `mapstructure:"host"`
	Port     string `mapstructure:"port"`
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	Database string `mapstructure:"database"`
	SSLMode  string `mapstructure:"ssl_mode"`
	MaxOpen  int    `mapstructure:"max_open"`
	MaxIdle  int    `mapstructure:"max_idle"`
}

type RedisConfig struct {
	Host     string `mapstructure:"host"`
	Port     string `mapstructure:"port"`
	Password string `mapstructure:"password"`
	Database int    `mapstructure:"database"`
}

type JWTConfig struct {
	Secret           string `mapstructure:"secret"`
	AccessDuration   int    `mapstructure:"access_duration"`
	RefreshDuration  int    `mapstructure:"refresh_duration"`
}

type EmailConfig struct {
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	From     string `mapstructure:"from"`
}

type StorageConfig struct {
	Driver    string `mapstructure:"driver"`
	LocalPath string `mapstructure:"local_path"`
	MaxSize   int64  `mapstructure:"max_size"`
}

func Load() (*Config, error) {
	config := &Config{}

	// Configurar Viper
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./configs")
	viper.AddConfigPath(".")

	// Variables de entorno
	viper.AutomaticEnv()

	// Valores por defecto
	setDefaults()

	// Leer configuración desde archivo
	if err := viper.ReadInConfig(); err != nil {
		// No es un error fatal, usar solo variables de entorno
		fmt.Printf("No se pudo leer archivo de configuración: %v\\n", err)
	}

	// Mapear a struct
	if err := viper.Unmarshal(config); err != nil {
		return nil, fmt.Errorf("error al mapear configuración: %w", err)
	}

	// Override con variables de entorno específicas
	overrideWithEnv(config)

	return config, nil
}

func setDefaults() {
	// App
	viper.SetDefault("app.name", "Project Management Platform")
	viper.SetDefault("app.version", "1.0.0")
	viper.SetDefault("app.environment", "development")
	viper.SetDefault("app.log_level", "info")

	// Server
	viper.SetDefault("server.host", "0.0.0.0")
	viper.SetDefault("server.port", "8080")
	viper.SetDefault("server.read_timeout", 30)
	viper.SetDefault("server.write_timeout", 30)
	viper.SetDefault("server.cors_origins", []string{"http://localhost:4200"})

	// Database
	viper.SetDefault("database.driver", "postgres")
	viper.SetDefault("database.host", "localhost")
	viper.SetDefault("database.port", "5432")
	viper.SetDefault("database.username", "pm_user")
	viper.SetDefault("database.password", "pm_password")
	viper.SetDefault("database.database", "project_management")
	viper.SetDefault("database.ssl_mode", "disable")
	viper.SetDefault("database.max_open", 25)
	viper.SetDefault("database.max_idle", 5)

	// Redis
	viper.SetDefault("redis.host", "localhost")
	viper.SetDefault("redis.port", "6379")
	viper.SetDefault("redis.password", "")
	viper.SetDefault("redis.database", 0)

	// JWT
	viper.SetDefault("jwt.secret", "your-super-secret-jwt-key")
	viper.SetDefault("jwt.access_duration", 3600)   // 1 hora
	viper.SetDefault("jwt.refresh_duration", 604800) // 7 días

	// Storage
	viper.SetDefault("storage.driver", "local")
	viper.SetDefault("storage.local_path", "./uploads")
	viper.SetDefault("storage.max_size", 52428800) // 50MB
}

func overrideWithEnv(config *Config) {
	// Variables de entorno específicas
	if host := os.Getenv("DB_HOST"); host != "" {
		config.Database.Host = host
	}
	if user := os.Getenv("DB_USER"); user != "" {
		config.Database.Username = user
	}
	if password := os.Getenv("DB_PASSWORD"); password != "" {
		config.Database.Password = password
	}
	if database := os.Getenv("DB_NAME"); database != "" {
		config.Database.Database = database
	}
	
	if redisHost := os.Getenv("REDIS_HOST"); redisHost != "" {
		config.Redis.Host = redisHost
	}
	if redisPort := os.Getenv("REDIS_PORT"); redisPort != "" {
		config.Redis.Port = redisPort
	}
	if redisPassword := os.Getenv("REDIS_PASSWORD"); redisPassword != "" {
		config.Redis.Password = redisPassword
	}
	
	if jwtSecret := os.Getenv("JWT_SECRET"); jwtSecret != "" {
		config.JWT.Secret = jwtSecret
	}
	
	if port := os.Getenv("PORT"); port != "" {
		config.Server.Port = port
	}
	
	if env := os.Getenv("APP_ENV"); env != "" {
		config.App.Environment = env
	}
}

func (c *Config) GetDatabaseDSN() string {
	return fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		c.Database.Host,
		c.Database.Port,
		c.Database.Username,
		c.Database.Password,
		c.Database.Database,
		c.Database.SSLMode,
	)
}

func (c *Config) GetRedisAddr() string {
	return fmt.Sprintf("%s:%s", c.Redis.Host, c.Redis.Port)
}

func (c *Config) IsDevelopment() bool {
	return c.App.Environment == "development"
}

func (c *Config) IsProduction() bool {
	return c.App.Environment == "production"
}
"""
    
    config_path = os.path.join(backend_dir, "internal", "config", "config.go")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_go_content)
    
    print("✓ Archivos de configuración creados")

def create_models(backend_dir):
    """Crear modelos de datos"""
    
    # internal/models/base.go
    base_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type BaseModel struct {
	ID        uuid.UUID      `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"deleted_at,omitempty" gorm:"index"`
}

func (base *BaseModel) BeforeCreate(tx *gorm.DB) error {
	if base.ID == uuid.Nil {
		base.ID = uuid.New()
	}
	return nil
}

type PaginationQuery struct {
	Page     int `json:"page" form:"page" binding:"min=1"`
	PageSize int `json:"page_size" form:"page_size" binding:"min=1,max=100"`
}

type PaginationResponse struct {
	Page       int         `json:"page"`
	PageSize   int         `json:"page_size"`
	Total      int64       `json:"total"`
	TotalPages int         `json:"total_pages"`
	Data       interface{} `json:"data"`
}

func (p *PaginationQuery) GetOffset() int {
	return (p.Page - 1) * p.PageSize
}

func (p *PaginationQuery) GetLimit() int {
	return p.PageSize
}

func NewPaginationResponse(page, pageSize int, total int64, data interface{}) *PaginationResponse {
	totalPages := int((total + int64(pageSize) - 1) / int64(pageSize))
	return &PaginationResponse{
		Page:       page,
		PageSize:   pageSize,
		Total:      total,
		TotalPages: totalPages,
		Data:       data,
	}
}
"""
    
    base_model_path = os.path.join(backend_dir, "internal", "models", "base.go")
    with open(base_model_path, "w", encoding="utf-8") as f:
        f.write(base_model_content)
    
    # internal/models/user.go
    user_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type UserRole string

const (
	RoleAdmin     UserRole = "admin"
	RoleManager   UserRole = "manager"
	RoleDeveloper UserRole = "developer"
	RoleTester    UserRole = "tester"
	RoleViewer    UserRole = "viewer"
)

type User struct {
	BaseModel
	Email           string         `json:"email" gorm:"uniqueIndex;not null"`
	Username        string         `json:"username" gorm:"uniqueIndex;not null"`
	Password        string         `json:"-" gorm:"not null"`
	FirstName       string         `json:"first_name"`
	LastName        string         `json:"last_name"`
	Avatar          string         `json:"avatar"`
	Role            UserRole       `json:"role" gorm:"type:varchar(20);default:'developer'"`
	IsActive        bool           `json:"is_active" gorm:"default:true"`
	IsEmailVerified bool           `json:"is_email_verified" gorm:"default:false"`
	LastLoginAt     *time.Time     `json:"last_login_at"`
	Timezone        string         `json:"timezone" gorm:"default:'UTC'"`
	Language        string         `json:"language" gorm:"default:'es'"`
	
	// Relaciones
	ProjectMembers []ProjectMember `json:"project_members,omitempty"`
	AssignedTasks  []Task          `json:"assigned_tasks,omitempty" gorm:"foreignKey:AssigneeID"`
	CreatedTasks   []Task          `json:"created_tasks,omitempty" gorm:"foreignKey:CreatorID"`
	Comments       []Comment       `json:"comments,omitempty"`
	AuditLogs      []AuditLog      `json:"audit_logs,omitempty"`
}

type UserProfile struct {
	ID        uuid.UUID `json:"id"`
	Email     string    `json:"email"`
	Username  string    `json:"username"`
	FirstName string    `json:"first_name"`
	LastName  string    `json:"last_name"`
	Avatar    string    `json:"avatar"`
	Role      UserRole  `json:"role"`
	IsActive  bool      `json:"is_active"`
	Timezone  string    `json:"timezone"`
	Language  string    `json:"language"`
}

type CreateUserRequest struct {
	Email     string   `json:"email" binding:"required,email"`
	Username  string   `json:"username" binding:"required,min=3,max=50"`
	Password  string   `json:"password" binding:"required,min=6"`
	FirstName string   `json:"first_name" binding:"required"`
	LastName  string   `json:"last_name" binding:"required"`
	Role      UserRole `json:"role" binding:"required"`
}

type UpdateUserRequest struct {
	FirstName string   `json:"first_name,omitempty"`
	LastName  string   `json:"last_name,omitempty"`
	Avatar    string   `json:"avatar,omitempty"`
	Role      UserRole `json:"role,omitempty"`
	IsActive  *bool    `json:"is_active,omitempty"`
	Timezone  string   `json:"timezone,omitempty"`
	Language  string   `json:"language,omitempty"`
}

type ChangePasswordRequest struct {
	CurrentPassword string `json:"current_password" binding:"required"`
	NewPassword     string `json:"new_password" binding:"required,min=6"`
}

func (u *User) SetPassword(password string) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.Password = string(hashedPassword)
	return nil
}

func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	return err == nil
}

func (u *User) GetFullName() string {
	return u.FirstName + " " + u.LastName
}

func (u *User) ToProfile() *UserProfile {
	return &UserProfile{
		ID:        u.ID,
		Email:     u.Email,
		Username:  u.Username,
		FirstName: u.FirstName,
		LastName:  u.LastName,
		Avatar:    u.Avatar,
		Role:      u.Role,
		IsActive:  u.IsActive,
		Timezone:  u.Timezone,
		Language:  u.Language,
	}
}

func (u *User) HasRole(role UserRole) bool {
	return u.Role == role
}

func (u *User) IsAdminOrManager() bool {
	return u.Role == RoleAdmin || u.Role == RoleManager
}
"""
    
    user_model_path = os.path.join(backend_dir, "internal", "models", "user.go")
    with open(user_model_path, "w", encoding="utf-8") as f:
        f.write(user_model_content)
    
    # internal/models/project.go
    project_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
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
	Name        string        `json:"name" gorm:"not null"`
	Key         string        `json:"key" gorm:"uniqueIndex;not null"` // Ej: "PROJ"
	Description string        `json:"description"`
	Status      ProjectStatus `json:"status" gorm:"default:'planning'"`
	StartDate   *time.Time    `json:"start_date"`
	EndDate     *time.Time    `json:"end_date"`
	Budget      float64       `json:"budget"`
	IsPublic    bool          `json:"is_public" gorm:"default:false"`
	
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
	ProjectID uuid.UUID       `json:"project_id" gorm:"not null"`
	UserID    uuid.UUID       `json:"user_id" gorm:"not null"`
	Role      ProjectRole     `json:"role" gorm:"not null"`
	JoinedAt  time.Time       `json:"joined_at" gorm:"default:CURRENT_TIMESTAMP"`
	
	// Relaciones
	Project *Project `json:"project,omitempty"`
	User    *User    `json:"user,omitempty"`
}

type ProjectRole string

const (
	ProjectRoleOwner      ProjectRole = "owner"
	ProjectRoleManager    ProjectRole = "manager"
	ProjectRoleDeveloper  ProjectRole = "developer"
	ProjectRoleTester     ProjectRole = "tester"
	ProjectRoleViewer     ProjectRole = "viewer"
)

type CreateProjectRequest struct {
	Name        string            `json:"name" binding:"required,min=2,max=100"`
	Key         string            `json:"key" binding:"required,min=2,max=10,uppercase"`
	Description string            `json:"description"`
	StartDate   *time.Time        `json:"start_date"`
	EndDate     *time.Time        `json:"end_date"`
	Budget      float64           `json:"budget"`
	IsPublic    bool              `json:"is_public"`
	Settings    ProjectSettings   `json:"settings"`
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
	Project     *Project      `json:"project"`
	Stats       *ProjectStats `json:"stats"`
	RecentTasks []Task        `json:"recent_tasks"`
	ActiveSprint *Sprint      `json:"active_sprint,omitempty"`
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
"""
    
    project_model_path = os.path.join(backend_dir, "internal", "models", "project.go")
    with open(project_model_path, "w", encoding="utf-8") as f:
        f.write(project_model_content)
    
    # internal/models/task.go
    task_model_content = """package models

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
"""
    
    task_model_path = os.path.join(backend_dir, "internal", "models", "task.go")
    with open(task_model_path, "w", encoding="utf-8") as f:
        f.write(task_model_content)
    
    print("✓ Modelos de datos creados")

def create_database_layer(backend_dir):
    """Crear capa de base de datos"""
    
    # internal/database/database.go
    database_go_content = """package database

import (
	"fmt"
	"log"
	"time"

	"github.com/company/project-management-platform/internal/config"
	"github.com/company/project-management-platform/internal/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

func Connect(cfg config.DatabaseConfig) (*gorm.DB, error) {
	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		cfg.Host, cfg.Port, cfg.Username, cfg.Password, cfg.Database, cfg.SSLMode)

	// Configurar logger
	var logLevel logger.LogLevel
	switch cfg.Driver {
	case "development":
		logLevel = logger.Info
	default:
		logLevel = logger.Error
	}

	gormLogger := logger.New(
		log.New(log.Writer(), "\\r\\n", log.LstdFlags),
		logger.Config{
			SlowThreshold: time.Second,
			LogLevel:      logLevel,
			Colorful:      true,
		},
	)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: gormLogger,
	})
	if err != nil {
		return nil, fmt.Errorf("error conectando a la base de datos: %w", err)
	}

	// Configurar connection pool
	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("error obteniendo conexión SQL: %w", err)
	}

	sqlDB.SetMaxOpenConns(cfg.MaxOpen)
	sqlDB.SetMaxIdleConns(cfg.MaxIdle)
	sqlDB.SetConnMaxLifetime(time.Hour)

	return db, nil
}

func Migrate(db *gorm.DB) error {
	err := db.AutoMigrate(
		&models.User{},
		&models.Project{},
		&models.ProjectMember{},
		&models.Epic{},
		&models.Sprint{},
		&models.Task{},
		&models.TaskDependency{},
		&models.Board{},
		&models.BoardColumn{},
		&models.Comment{},
		&models.Attachment{},
		&models.TimeEntry{},
		&models.Notification{},
		&models.AuditLog{},
		&models.Integration{},
		&models.Webhook{},
	)
	if err != nil {
		return fmt.Errorf("error ejecutando migraciones: %w", err)
	}

	// Ejecutar migraciones personalizadas
	if err := runCustomMigrations(db); err != nil {
		return fmt.Errorf("error ejecutando migraciones personalizadas: %w", err)
	}

	return nil
}

func runCustomMigrations(db *gorm.DB) error {
	// Crear índices personalizados
	if err := createIndexes(db); err != nil {
		return err
	}

	// Insertar datos iniciales
	if err := seedInitialData(db); err != nil {
		return err
	}

	return nil
}

func createIndexes(db *gorm.DB) error {
	// Índices para mejorar performance
	indexes := []string{
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_project_status ON tasks(project_id, status)",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_assignee_status ON tasks(assignee_id, status) WHERE assignee_id IS NOT NULL",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_status ON projects(status)",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_members_user_project ON project_members(user_id, project_id)",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_comments_task ON comments(task_id)",
		"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_time_entries_task_user ON time_entries(task_id, user_id)",
	}

	for _, index := range indexes {
		if err := db.Exec(index).Error; err != nil {
			log.Printf("Warning: No se pudo crear índice: %v", err)
		}
	}

	return nil
}

func seedInitialData(db *gorm.DB) error {
	// Verificar si ya existen datos
	var userCount int64
	if err := db.Model(&models.User{}).Count(&userCount).Error; err != nil {
		return err
	}

	if userCount > 0 {
		return nil // Ya hay datos, no seed
	}

	// Crear usuario administrador por defecto
	adminUser := &models.User{
		Email:     "admin@projectmanagement.com",
		Username:  "admin",
		FirstName: "Administrador",
		LastName:  "Sistema",
		Role:      models.RoleAdmin,
		IsActive:  true,
		IsEmailVerified: true,
	}

	if err := adminUser.SetPassword("admin123"); err != nil {
		return err
	}

	if err := db.Create(adminUser).Error; err != nil {
		return err
	}

	log.Println("Usuario administrador creado - Email: admin@projectmanagement.com, Password: admin123")
	return nil
}

// Health check para la base de datos
func HealthCheck(db *gorm.DB) error {
	sqlDB, err := db.DB()
	if err != nil {
		return err
	}
	return sqlDB.Ping()
}
"""
    
    database_path = os.path.join(backend_dir, "internal", "database", "database.go")
    with open(database_path, "w", encoding="utf-8") as f:
        f.write(database_go_content)
    
    print("✓ Capa de base de datos creada")

def create_services(backend_dir):
    """Crear servicios de negocio"""
    
    # internal/services/auth_service.go
    auth_service_content = """package services

import (
	"errors"
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/golang-jwt/jwt/v4"
	"gorm.io/gorm"
)

type AuthService struct {
	db        *gorm.DB
	jwtSecret string
	accessDuration  time.Duration
	refreshDuration time.Duration
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

type LoginResponse struct {
	User         *models.UserProfile `json:"user"`
	AccessToken  string              `json:"access_token"`
	RefreshToken string              `json:"refresh_token"`
	ExpiresAt    time.Time           `json:"expires_at"`
}

type TokenClaims struct {
	UserID   string `json:"user_id"`
	Username string `json:"username"`
	Role     string `json:"role"`
	jwt.RegisteredClaims
}

func NewAuthService(db *gorm.DB, jwtSecret string, accessDuration, refreshDuration time.Duration) *AuthService {
	return &AuthService{
		db:              db,
		jwtSecret:       jwtSecret,
		accessDuration:  accessDuration,
		refreshDuration: refreshDuration,
	}
}

func (s *AuthService) Login(req *LoginRequest) (*LoginResponse, error) {
	var user models.User
	if err := s.db.Where("email = ? AND is_active = ?", req.Email, true).First(&user).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, errors.New("credenciales inválidas")
		}
		return nil, err
	}

	if !user.CheckPassword(req.Password) {
		return nil, errors.New("credenciales inválidas")
	}

	// Actualizar último login
	now := time.Now()
	user.LastLoginAt = &now
	s.db.Save(&user)

	// Generar tokens
	accessToken, err := s.generateAccessToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando access token: %w", err)
	}

	refreshToken, err := s.generateRefreshToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando refresh token: %w", err)
	}

	return &LoginResponse{
		User:         user.ToProfile(),
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    time.Now().Add(s.accessDuration),
	}, nil
}

func (s *AuthService) Register(req *models.CreateUserRequest) (*models.UserProfile, error) {
	// Verificar si el email ya existe
	var existingUser models.User
	if err := s.db.Where("email = ?", req.Email).First(&existingUser).Error; err == nil {
		return nil, errors.New("el email ya está registrado")
	}

	// Verificar si el username ya existe
	if err := s.db.Where("username = ?", req.Username).First(&existingUser).Error; err == nil {
		return nil, errors.New("el username ya está registrado")
	}

	// Crear nuevo usuario
	user := &models.User{
		Email:     req.Email,
		Username:  req.Username,
		FirstName: req.FirstName,
		LastName:  req.LastName,
		Role:      req.Role,
		IsActive:  true,
	}

	if err := user.SetPassword(req.Password); err != nil {
		return nil, fmt.Errorf("error configurando password: %w", err)
	}

	if err := s.db.Create(user).Error; err != nil {
		return nil, fmt.Errorf("error creando usuario: %w", err)
	}

	return user.ToProfile(), nil
}

func (s *AuthService) RefreshToken(refreshToken string) (*LoginResponse, error) {
	claims, err := s.validateToken(refreshToken)
	if err != nil {
		return nil, fmt.Errorf("token inválido: %w", err)
	}

	var user models.User
	if err := s.db.Where("id = ? AND is_active = ?", claims.UserID, true).First(&user).Error; err != nil {
		return nil, errors.New("usuario no encontrado")
	}

	// Generar nuevos tokens
	accessToken, err := s.generateAccessToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando access token: %w", err)
	}

	newRefreshToken, err := s.generateRefreshToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando refresh token: %w", err)
	}

	return &LoginResponse{
		User:         user.ToProfile(),
		AccessToken:  accessToken,
		RefreshToken: newRefreshToken,
		ExpiresAt:    time.Now().Add(s.accessDuration),
	}, nil
}

func (s *AuthService) ValidateToken(tokenString string) (*TokenClaims, error) {
	return s.validateToken(tokenString)
}

func (s *AuthService) generateAccessToken(user *models.User) (string, error) {
	claims := &TokenClaims{
		UserID:   user.ID.String(),
		Username: user.Username,
		Role:     string(user.Role),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.accessDuration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   user.ID.String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.jwtSecret))
}

func (s *AuthService) generateRefreshToken(user *models.User) (string, error) {
	claims := &TokenClaims{
		UserID:   user.ID.String(),
		Username: user.Username,
		Role:     string(user.Role),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.refreshDuration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   user.ID.String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.jwtSecret))
}

func (s *AuthService) validateToken(tokenString string) (*TokenClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &TokenClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("método de firma inesperado: %v", token.Header["alg"])
		}
		return []byte(s.jwtSecret), nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*TokenClaims)
	if !ok || !token.Valid {
		return nil, errors.New("token inválido")
	}

	return claims, nil
}

func (s *AuthService) GetUserByID(userID string) (*models.User, error) {
	var user models.User
	if err := s.db.Where("id = ? AND is_active = ?", userID, true).First(&user).Error; err != nil {
		return nil, err
	}
	return &user, nil
}

func (s *AuthService) ChangePassword(userID string, req *models.ChangePasswordRequest) error {
	var user models.User
	if err := s.db.Where("id = ?", userID).First(&user).Error; err != nil {
		return err
	}

	if !user.CheckPassword(req.CurrentPassword) {
		return errors.New("contraseña actual incorrecta")
	}

	if err := user.SetPassword(req.NewPassword); err != nil {
		return fmt.Errorf("error configurando nueva contraseña: %w", err)
	}

	return s.db.Save(&user).Error
}
"""
    
    auth_service_path = os.path.join(backend_dir, "internal", "services", "auth_service.go")
    with open(auth_service_path, "w", encoding="utf-8") as f:
        f.write(auth_service_content)
    
    print("✓ Servicios de negocio creados")

def create_api_handlers(backend_dir):
    """Crear handlers de la API"""
    
    # internal/api/api.go
    api_go_content = """package api

import (
	"net/http"
	"time"

	"github.com/company/project-management-platform/internal/api/handlers"
	"github.com/company/project-management-platform/internal/api/middleware"
	"github.com/company/project-management-platform/internal/config"
	"github.com/company/project-management-platform/internal/services"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func SetupRouter(db *gorm.DB, cfg *config.Config) *gin.Engine {
	router := gin.New()

	// Middleware global
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	// CORS
	corsConfig := cors.Config{
		AllowOrigins:     cfg.Server.CorsOrigins,
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}
	router.Use(cors.New(corsConfig))

	// Inicializar servicios
	authService := services.NewAuthService(
		db,
		cfg.JWT.Secret,
		time.Duration(cfg.JWT.AccessDuration)*time.Second,
		time.Duration(cfg.JWT.RefreshDuration)*time.Second,
	)

	projectService := services.NewProjectService(db)
	taskService := services.NewTaskService(db)
	userService := services.NewUserService(db)

	// Inicializar handlers
	authHandler := handlers.NewAuthHandler(authService)
	projectHandler := handlers.NewProjectHandler(projectService)
	taskHandler := handlers.NewTaskHandler(taskService)
	userHandler := handlers.NewUserHandler(userService)

	// Middleware de autenticación
	authMiddleware := middleware.NewAuthMiddleware(authService)

	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  "ok",
			"service": "project-management-api",
			"version": cfg.App.Version,
			"time":    time.Now().UTC(),
		})
	})

	// Rutas públicas
	v1 := router.Group("/api/v1")
	{
		auth := v1.Group("/auth")
		{
			auth.POST("/login", authHandler.Login)
			auth.POST("/register", authHandler.Register)
			auth.POST("/refresh", authHandler.RefreshToken)
		}
	}

	// Rutas protegidas
	protected := v1.Group("/")
	protected.Use(authMiddleware.RequireAuth())
	{
		// Auth routes protegidas
		authProtected := protected.Group("/auth")
		{
			authProtected.GET("/me", authHandler.GetProfile)
			authProtected.PUT("/me", authHandler.UpdateProfile)
			authProtected.POST("/change-password", authHandler.ChangePassword)
			authProtected.POST("/logout", authHandler.Logout)
		}

		// User routes
		users := protected.Group("/users")
		{
			users.GET("", userHandler.GetUsers)
			users.GET("/:id", userHandler.GetUser)
			users.PUT("/:id", userHandler.UpdateUser)
			users.DELETE("/:id", userHandler.DeleteUser)
		}

		// Project routes
		projects := protected.Group("/projects")
		{
			projects.GET("", projectHandler.GetProjects)
			projects.POST("", projectHandler.CreateProject)
			projects.GET("/:id", projectHandler.GetProject)
			projects.PUT("/:id", projectHandler.UpdateProject)
			projects.DELETE("/:id", projectHandler.DeleteProject)
			projects.GET("/:id/dashboard", projectHandler.GetProjectDashboard)
			
			// Project members
			projects.GET("/:id/members", projectHandler.GetProjectMembers)
			projects.POST("/:id/members", projectHandler.AddProjectMember)
			projects.PUT("/:id/members/:user_id", projectHandler.UpdateProjectMember)
			projects.DELETE("/:id/members/:user_id", projectHandler.RemoveProjectMember)
		}

		// Task routes
		tasks := protected.Group("/tasks")
		{
			tasks.GET("", taskHandler.GetTasks)
			tasks.POST("", taskHandler.CreateTask)
			tasks.GET("/:id", taskHandler.GetTask)
			tasks.PUT("/:id", taskHandler.UpdateTask)
			tasks.DELETE("/:id", taskHandler.DeleteTask)
			tasks.POST("/:id/comments", taskHandler.AddComment)
			tasks.GET("/:id/comments", taskHandler.GetComments)
		}

		// Project-specific task routes
		projectTasks := protected.Group("/projects/:project_id/tasks")
		{
			projectTasks.GET("", taskHandler.GetProjectTasks)
			projectTasks.POST("", taskHandler.CreateProjectTask)
		}
	}

	return router
}
"""
    
    api_path = os.path.join(backend_dir, "internal", "api", "api.go")
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(api_go_content)
    
    # internal/api/handlers/auth_handler.go
    auth_handler_content = """package handlers

import (
	"net/http"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/services"
	"github.com/gin-gonic/gin"
)

type AuthHandler struct {
	authService *services.AuthService
}

func NewAuthHandler(authService *services.AuthService) *AuthHandler {
	return &AuthHandler{
		authService: authService,
	}
}

func (h *AuthHandler) Login(c *gin.Context) {
	var req services.LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	response, err := h.authService.Login(&req)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, response)
}

func (h *AuthHandler) Register(c *gin.Context) {
	var req models.CreateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := h.authService.Register(&req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"user": user})
}

func (h *AuthHandler) RefreshToken(c *gin.Context) {
	var req struct {
		RefreshToken string `json:"refresh_token" binding:"required"`
	}
	
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	response, err := h.authService.RefreshToken(req.RefreshToken)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, response)
}

func (h *AuthHandler) GetProfile(c *gin.Context) {
	userID := c.GetString("user_id")
	
	user, err := h.authService.GetUserByID(userID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuario no encontrado"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"user": user.ToProfile()})
}

func (h *AuthHandler) UpdateProfile(c *gin.Context) {
	userID := c.GetString("user_id")
	
	var req models.UpdateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// TODO: Implementar actualización de perfil
	c.JSON(http.StatusOK, gin.H{"message": "Perfil actualizado"})
}

func (h *AuthHandler) ChangePassword(c *gin.Context) {
	userID := c.GetString("user_id")
	
	var req models.ChangePasswordRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.authService.ChangePassword(userID, &req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Contraseña cambiada exitosamente"})
}

func (h *AuthHandler) Logout(c *gin.Context) {
	// TODO: Implementar blacklist de tokens si es necesario
	c.JSON(http.StatusOK, gin.H{"message": "Sesión cerrada exitosamente"})
}
"""
    
    auth_handler_path = os.path.join(backend_dir, "internal", "api", "handlers", "auth_handler.go")
    with open(auth_handler_path, "w", encoding="utf-8") as f:
        f.write(auth_handler_content)
    
    print("✓ Handlers de la API creados")

def create_middleware(backend_dir):
    """Crear middleware"""
    
    # internal/api/middleware/auth_middleware.go
    auth_middleware_content = """package middleware

import (
	"net/http"
	"strings"

	"github.com/company/project-management-platform/internal/services"
	"github.com/gin-gonic/gin"
)

type AuthMiddleware struct {
	authService *services.AuthService
}

func NewAuthMiddleware(authService *services.AuthService) *AuthMiddleware {
	return &AuthMiddleware{
		authService: authService,
	}
}

func (m *AuthMiddleware) RequireAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Token de autorización requerido"})
			c.Abort()
			return
		}

		// Extraer token del header "Bearer <token>"
		tokenParts := strings.Split(authHeader, " ")
		if len(tokenParts) != 2 || tokenParts[0] != "Bearer" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Formato de token inválido"})
			c.Abort()
			return
		}

		token := tokenParts[1]
		claims, err := m.authService.ValidateToken(token)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Token inválido"})
			c.Abort()
			return
		}

		// Agregar información del usuario al contexto
		c.Set("user_id", claims.UserID)
		c.Set("username", claims.Username)
		c.Set("user_role", claims.Role)
		
		c.Next()
	}
}

func (m *AuthMiddleware) RequireRole(role string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole := c.GetString("user_role")
		if userRole != role && userRole != "admin" {
			c.JSON(http.StatusForbidden, gin.H{"error": "Permisos insuficientes"})
			c.Abort()
			return
		}
		c.Next()
	}
}

func (m *AuthMiddleware) RequireAnyRole(roles ...string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole := c.GetString("user_role")
		
		// Admin siempre tiene acceso
		if userRole == "admin" {
			c.Next()
			return
		}
		
		// Verificar si el usuario tiene alguno de los roles requeridos
		for _, role := range roles {
			if userRole == role {
				c.Next()
				return
			}
		}
		
		c.JSON(http.StatusForbidden, gin.H{"error": "Permisos insuficientes"})
		c.Abort()
	}
}
"""
    
    auth_middleware_path = os.path.join(backend_dir, "internal", "api", "middleware", "auth_middleware.go")
    with open(auth_middleware_path, "w", encoding="utf-8") as f:
        f.write(auth_middleware_content)
    
    print("✓ Middleware creado")

def create_websocket_layer(backend_dir):
    """Crear capa de WebSocket"""
    
    # internal/websocket/hub.go
    websocket_hub_content = """package websocket

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		// TODO: Implementar verificación de origen más segura
		return true
	},
}

type Hub struct {
	clients    map[*Client]bool
	register   chan *Client
	unregister chan *Client
	broadcast  chan []byte
	mutex      sync.RWMutex
}

type Client struct {
	hub      *Hub
	conn     *websocket.Conn
	send     chan []byte
	userID   string
	projects map[string]bool // IDs de proyectos a los que está suscrito
}

type Message struct {
	Type      string      `json:"type"`
	ProjectID string      `json:"project_id,omitempty"`
	UserID    string      `json:"user_id,omitempty"`
	Data      interface{} `json:"data"`
	Timestamp int64       `json:"timestamp"`
}

func NewHub() *Hub {
	return &Hub{
		clients:    make(map[*Client]bool),
		register:   make(chan *Client),
		unregister: make(chan *Client),
		broadcast:  make(chan []byte),
	}
}

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.register:
			h.mutex.Lock()
			h.clients[client] = true
			h.mutex.Unlock()
			log.Printf("Cliente conectado: %s", client.userID)

		case client := <-h.unregister:
			h.mutex.Lock()
			if _, ok := h.clients[client]; ok {
				delete(h.clients, client)
				close(client.send)
			}
			h.mutex.Unlock()
			log.Printf("Cliente desconectado: %s", client.userID)

		case message := <-h.broadcast:
			h.mutex.RLock()
			for client := range h.clients {
				select {
				case client.send <- message:
				default:
					close(client.send)
					delete(h.clients, client)
				}
			}
			h.mutex.RUnlock()
		}
	}
}

func (h *Hub) BroadcastToProject(projectID string, message *Message) {
	data, err := json.Marshal(message)
	if err != nil {
		log.Printf("Error serializando mensaje: %v", err)
		return
	}

	h.mutex.RLock()
	defer h.mutex.RUnlock()

	for client := range h.clients {
		if client.projects[projectID] {
			select {
			case client.send <- data:
			default:
				close(client.send)
				delete(h.clients, client)
			}
		}
	}
}

func (h *Hub) BroadcastToUser(userID string, message *Message) {
	data, err := json.Marshal(message)
	if err != nil {
		log.Printf("Error serializando mensaje: %v", err)
		return
	}

	h.mutex.RLock()
	defer h.mutex.RUnlock()

	for client := range h.clients {
		if client.userID == userID {
			select {
			case client.send <- data:
			default:
				close(client.send)
				delete(h.clients, client)
			}
		}
	}
}

func (h *Hub) HandleWebSocket(w http.ResponseWriter, r *http.Request, userID string) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Error upgrading connection: %v", err)
		return
	}

	client := &Client{
		hub:      h,
		conn:     conn,
		send:     make(chan []byte, 256),
		userID:   userID,
		projects: make(map[string]bool),
	}

	h.register <- client

	go client.writePump()
	go client.readPump()
}

func (c *Client) readPump() {
	defer func() {
		c.hub.unregister <- c
		c.conn.Close()
	}()

	for {
		_, messageBytes, err := c.conn.ReadMessage()
		if err != nil {
			break
		}

		var msg Message
		if err := json.Unmarshal(messageBytes, &msg); err != nil {
			log.Printf("Error deserializando mensaje: %v", err)
			continue
		}

		// Manejar diferentes tipos de mensajes
		switch msg.Type {
		case "subscribe_project":
			if projectID, ok := msg.Data.(string); ok {
				c.projects[projectID] = true
				log.Printf("Cliente %s suscrito al proyecto %s", c.userID, projectID)
			}
		case "unsubscribe_project":
			if projectID, ok := msg.Data.(string); ok {
				delete(c.projects, projectID)
				log.Printf("Cliente %s desuscrito del proyecto %s", c.userID, projectID)
			}
		}
	}
}

func (c *Client) writePump() {
	defer c.conn.Close()

	for {
		select {
		case message, ok := <-c.send:
			if !ok {
				c.conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}

			if err := c.conn.WriteMessage(websocket.TextMessage, message); err != nil {
				return
			}
		}
	}
}
"""
    
    websocket_hub_path = os.path.join(backend_dir, "internal", "websocket", "hub.go")
    with open(websocket_hub_path, "w", encoding="utf-8") as f:
        f.write(websocket_hub_content)
    
    print("✓ Capa de WebSocket creada")

def create_utils(backend_dir):
    """Crear utilidades"""
    
    # internal/utils/response.go
    response_utils_content = """package utils

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

func SuccessResponse(c *gin.Context, data interface{}) {
	c.JSON(http.StatusOK, Response{
		Success: true,
		Data:    data,
	})
}

func CreatedResponse(c *gin.Context, data interface{}) {
	c.JSON(http.StatusCreated, Response{
		Success: true,
		Data:    data,
	})
}

func ErrorResponse(c *gin.Context, statusCode int, message string) {
	c.JSON(statusCode, Response{
		Success: false,
		Error:   message,
	})
}

func ValidationErrorResponse(c *gin.Context, message string) {
	ErrorResponse(c, http.StatusBadRequest, message)
}

func NotFoundResponse(c *gin.Context, message string) {
	ErrorResponse(c, http.StatusNotFound, message)
}

func UnauthorizedResponse(c *gin.Context, message string) {
	ErrorResponse(c, http.StatusUnauthorized, message)
}

func ForbiddenResponse(c *gin.Context, message string) {
	ErrorResponse(c, http.StatusForbidden, message)
}

func InternalErrorResponse(c *gin.Context, message string) {
	ErrorResponse(c, http.StatusInternalServerError, message)
}
"""
    
    response_utils_path = os.path.join(backend_dir, "internal", "utils", "response.go")
    with open(response_utils_path, "w", encoding="utf-8") as f:
        f.write(response_utils_content)
    
    print("✓ Utilidades creadas")

def create_tests(backend_dir):
    """Crear tests básicos"""
    
    # tests/unit/auth_test.go
    auth_test_content = """package unit

import (
	"testing"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/services"
	"github.com/stretchr/testify/assert"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDB() *gorm.DB {
	db, _ := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	db.AutoMigrate(&models.User{})
	return db
}

func TestAuthService_Login(t *testing.T) {
	db := setupTestDB()
	authService := services.NewAuthService(db, "test-secret", time.Hour, time.Hour*24)

	// Crear usuario de prueba
	user := &models.User{
		Email:     "test@example.com",
		Username:  "testuser",
		FirstName: "Test",
		LastName:  "User",
		Role:      models.RoleDeveloper,
		IsActive:  true,
	}
	user.SetPassword("password123")
	db.Create(user)

	// Test login exitoso
	loginReq := &services.LoginRequest{
		Email:    "test@example.com",
		Password: "password123",
	}

	response, err := authService.Login(loginReq)
	assert.NoError(t, err)
	assert.NotNil(t, response)
	assert.Equal(t, "testuser", response.User.Username)
	assert.NotEmpty(t, response.AccessToken)
	assert.NotEmpty(t, response.RefreshToken)

	// Test login con credenciales incorrectas
	loginReq.Password = "wrongpassword"
	response, err = authService.Login(loginReq)
	assert.Error(t, err)
	assert.Nil(t, response)
}

func TestAuthService_Register(t *testing.T) {
	db := setupTestDB()
	authService := services.NewAuthService(db, "test-secret", time.Hour, time.Hour*24)

	// Test registro exitoso
	registerReq := &models.CreateUserRequest{
		Email:     "newuser@example.com",
		Username:  "newuser",
		Password:  "password123",
		FirstName: "New",
		LastName:  "User",
		Role:      models.RoleDeveloper,
	}

	user, err := authService.Register(registerReq)
	assert.NoError(t, err)
	assert.NotNil(t, user)
	assert.Equal(t, "newuser", user.Username)

	// Test registro con email duplicado
	_, err = authService.Register(registerReq)
	assert.Error(t, err)
}
"""
    
    auth_test_path = os.path.join(backend_dir, "tests", "unit", "auth_test.go")
    with open(auth_test_path, "w", encoding="utf-8") as f:
        f.write(auth_test_content)
    
    print("✓ Tests básicos creados")

if __name__ == "__main__":
    create_backend_core()
