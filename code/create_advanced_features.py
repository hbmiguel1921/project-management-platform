#!/usr/bin/env python3
"""
Script para crear las funcionalidades avanzadas del sistema:
- Gestión de sprints y metodologías ágiles
- Seguimiento de tiempo y timetracking
- Sistema de reportes y analytics
- Dashboards avanzados
- Integración con herramientas externas
- Gestión de riesgos y issues
"""

import os

def create_advanced_features():
    """Crear funcionalidades avanzadas completas"""
    
    backend_dir = "/workspace/project-management-platform/backend"
    frontend_dir = "/workspace/project-management-platform/frontend"
    
    # Backend - Modelos avanzados
    create_advanced_models(backend_dir)
    
    # Backend - Servicios avanzados
    create_advanced_services(backend_dir)
    
    # Backend - Handlers avanzados
    create_advanced_handlers(backend_dir)
    
    # Frontend - Componentes de sprint
    create_sprint_components(frontend_dir)
    
    # Frontend - Sistema de timetracking
    create_timetracking_components(frontend_dir)
    
    # Frontend - Sistema de reportes
    create_reporting_components(frontend_dir)
    
    print("✓ Funcionalidades avanzadas completadas")

def create_advanced_models(backend_dir):
    """Crear modelos para funcionalidades avanzadas"""
    
    # internal/models/sprint.go
    sprint_model_content = """package models

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
"""
    
    sprint_model_path = os.path.join(backend_dir, "internal", "models", "sprint.go")
    with open(sprint_model_path, "w", encoding="utf-8") as f:
        f.write(sprint_model_content)
    
    # internal/models/timetracking.go
    timetracking_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
)

type TimeEntry struct {
	BaseModel
	Description string    `json:"description" gorm:"not null"`
	StartTime   time.Time `json:"start_time" gorm:"not null"`
	EndTime     *time.Time `json:"end_time"`
	Duration    int       `json:"duration"` // En minutos
	TaskID      *uuid.UUID `json:"task_id"`
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	UserID      uuid.UUID `json:"user_id" gorm:"not null"`
	IsBillable  bool      `json:"is_billable" gorm:"default:true"`
	HourlyRate  *float64  `json:"hourly_rate"`
	Tags        []string  `json:"tags" gorm:"type:jsonb"`
	
	// Relaciones
	Task    *Task    `json:"task,omitempty"`
	Project *Project `json:"project,omitempty"`
	User    *User    `json:"user,omitempty"`
}

type TimesheetEntry struct {
	BaseModel
	Date        time.Time `json:"date" gorm:"not null"`
	UserID      uuid.UUID `json:"user_id" gorm:"not null"`
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	TaskID      *uuid.UUID `json:"task_id"`
	Hours       float64   `json:"hours" gorm:"not null"`
	Description string    `json:"description"`
	IsBillable  bool      `json:"is_billable" gorm:"default:true"`
	Status      TimesheetStatus `json:"status" gorm:"default:'draft'"`
	
	// Relaciones
	User    *User    `json:"user,omitempty"`
	Project *Project `json:"project,omitempty"`
	Task    *Task    `json:"task,omitempty"`
}

type TimesheetStatus string

const (
	TimesheetStatusDraft     TimesheetStatus = "draft"
	TimesheetStatusSubmitted TimesheetStatus = "submitted"
	TimesheetStatusApproved  TimesheetStatus = "approved"
	TimesheetStatusRejected  TimesheetStatus = "rejected"
)

type CreateTimeEntryRequest struct {
	Description string     `json:"description" binding:"required"`
	StartTime   time.Time  `json:"start_time" binding:"required"`
	EndTime     *time.Time `json:"end_time"`
	TaskID      *uuid.UUID `json:"task_id"`
	IsBillable  bool       `json:"is_billable"`
	Tags        []string   `json:"tags"`
}

type UpdateTimeEntryRequest struct {
	Description string     `json:"description,omitempty"`
	StartTime   time.Time  `json:"start_time,omitempty"`
	EndTime     *time.Time `json:"end_time,omitempty"`
	IsBillable  *bool      `json:"is_billable,omitempty"`
	Tags        []string   `json:"tags,omitempty"`
}

type CreateTimesheetEntryRequest struct {
	Date        time.Time  `json:"date" binding:"required"`
	ProjectID   uuid.UUID  `json:"project_id" binding:"required"`
	TaskID      *uuid.UUID `json:"task_id"`
	Hours       float64    `json:"hours" binding:"required,min=0.1,max=24"`
	Description string     `json:"description" binding:"required"`
	IsBillable  bool       `json:"is_billable"`
}

func (te *TimeEntry) CalculateDuration() int {
	if te.EndTime != nil {
		return int(te.EndTime.Sub(te.StartTime).Minutes())
	}
	return 0
}

func (te *TimeEntry) IsRunning() bool {
	return te.EndTime == nil
}

func (te *TimeEntry) Stop() {
	now := time.Now()
	te.EndTime = &now
	te.Duration = te.CalculateDuration()
}

func (te *TimeEntry) CalculateAmount() float64 {
	if te.HourlyRate != nil && te.IsBillable {
		hours := float64(te.Duration) / 60.0
		return hours * *te.HourlyRate
	}
	return 0
}
"""
    
    timetracking_model_path = os.path.join(backend_dir, "internal", "models", "timetracking.go")
    with open(timetracking_model_path, "w", encoding="utf-8") as f:
        f.write(timetracking_model_content)
    
    # internal/models/report.go
    report_model_content = """package models

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
"""
    
    report_model_path = os.path.join(backend_dir, "internal", "models", "report.go")
    with open(report_model_path, "w", encoding="utf-8") as f:
        f.write(report_model_content)
    
    print("✓ Modelos avanzados creados")

def create_advanced_services(backend_dir):
    """Crear servicios para funcionalidades avanzadas"""
    
    # internal/services/sprint_service.go
    sprint_service_content = """package services

import (
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type SprintService struct {
	db *gorm.DB
	notificationService *NotificationService
}

func NewSprintService(db *gorm.DB, notificationService *NotificationService) *SprintService {
	return &SprintService{
		db:                  db,
		notificationService: notificationService,
	}
}

func (s *SprintService) CreateSprint(projectID, userID uuid.UUID, req *models.CreateSprintRequest) (*models.Sprint, error) {
	// Validar fechas
	if req.EndDate.Before(req.StartDate) {
		return nil, fmt.Errorf("la fecha de fin debe ser posterior a la fecha de inicio")
	}

	sprint := &models.Sprint{
		Name:        req.Name,
		Description: req.Description,
		ProjectID:   projectID,
		StartDate:   req.StartDate,
		EndDate:     req.EndDate,
		Goal:        req.Goal,
		Capacity:    req.Capacity,
		Status:      models.SprintStatusPlanning,
	}

	if err := s.db.Create(sprint).Error; err != nil {
		return nil, fmt.Errorf("error creando sprint: %w", err)
	}

	return s.GetSprint(sprint.ID, userID)
}

func (s *SprintService) GetSprints(projectID, userID uuid.UUID, status *models.SprintStatus) ([]models.Sprint, error) {
	var sprints []models.Sprint
	
	query := s.db.Where("project_id = ?", projectID).
		Preload("Project").
		Preload("Events").
		Order("created_at DESC")

	if status != nil {
		query = query.Where("status = ?", *status)
	}

	if err := query.Find(&sprints).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprints: %w", err)
	}

	return sprints, nil
}

func (s *SprintService) GetSprint(sprintID, userID uuid.UUID) (*models.Sprint, error) {
	var sprint models.Sprint
	
	if err := s.db.Preload("Project").
		Preload("Tasks").
		Preload("Events").
		Preload("Events.User").
		First(&sprint, sprintID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprint: %w", err)
	}

	return &sprint, nil
}

func (s *SprintService) UpdateSprint(sprintID, userID uuid.UUID, req *models.UpdateSprintRequest) (*models.Sprint, error) {
	var sprint models.Sprint
	
	if err := s.db.First(&sprint, sprintID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprint: %w", err)
	}

	// Solo permitir actualizaciones en sprints no activos o completados
	if sprint.Status == models.SprintStatusActive || sprint.Status == models.SprintStatusCompleted {
		return nil, fmt.Errorf("no se puede modificar un sprint activo o completado")
	}

	// Actualizar campos
	if req.Name != "" {
		sprint.Name = req.Name
	}
	if req.Description != "" {
		sprint.Description = req.Description
	}
	if !req.StartDate.IsZero() {
		sprint.StartDate = req.StartDate
	}
	if !req.EndDate.IsZero() {
		sprint.EndDate = req.EndDate
	}
	if req.Goal != "" {
		sprint.Goal = req.Goal
	}
	if req.Capacity > 0 {
		sprint.Capacity = req.Capacity
	}

	if err := s.db.Save(&sprint).Error; err != nil {
		return nil, fmt.Errorf("error actualizando sprint: %w", err)
	}

	return s.GetSprint(sprintID, userID)
}

func (s *SprintService) StartSprint(sprintID, userID uuid.UUID) (*models.Sprint, error) {
	var sprint models.Sprint
	
	if err := s.db.First(&sprint, sprintID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprint: %w", err)
	}

	if sprint.Status != models.SprintStatusPlanning {
		return nil, fmt.Errorf("el sprint debe estar en estado de planificación para iniciarse")
	}

	// Verificar que no hay otro sprint activo en el proyecto
	var activeSprint models.Sprint
	if err := s.db.Where("project_id = ? AND status = ?", sprint.ProjectID, models.SprintStatusActive).
		First(&activeSprint).Error; err == nil {
		return nil, fmt.Errorf("ya hay un sprint activo en este proyecto")
	}

	sprint.Status = models.SprintStatusActive

	if err := s.db.Save(&sprint).Error; err != nil {
		return nil, fmt.Errorf("error iniciando sprint: %w", err)
	}

	// Crear evento de inicio
	s.CreateSprintEvent(sprintID, userID, models.SprintEventTypePlanning, "Sprint iniciado", "El sprint ha sido iniciado")

	// Notificar al equipo
	go s.notifySprintStarted(&sprint, userID)

	return s.GetSprint(sprintID, userID)
}

func (s *SprintService) CompleteSprint(sprintID, userID uuid.UUID) (*models.Sprint, error) {
	var sprint models.Sprint
	
	if err := s.db.Preload("Tasks").First(&sprint, sprintID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprint: %w", err)
	}

	if sprint.Status != models.SprintStatusActive {
		return nil, fmt.Errorf("el sprint debe estar activo para completarse")
	}

	sprint.Status = models.SprintStatusCompleted

	// Calcular métricas finales
	s.CalculateSprintMetrics(&sprint)

	if err := s.db.Save(&sprint).Error; err != nil {
		return nil, fmt.Errorf("error completando sprint: %w", err)
	}

	// Crear evento de finalización
	s.CreateSprintEvent(sprintID, userID, models.SprintEventTypeReview, "Sprint completado", "El sprint ha sido completado")

	// Notificar al equipo
	go s.notifySprintCompleted(&sprint, userID)

	return s.GetSprint(sprintID, userID)
}

func (s *SprintService) AddTaskToSprint(sprintID, taskID, userID uuid.UUID) error {
	// Verificar que el sprint existe y está en planificación o activo
	var sprint models.Sprint
	if err := s.db.First(&sprint, sprintID).Error; err != nil {
		return fmt.Errorf("sprint no encontrado: %w", err)
	}

	if sprint.Status == models.SprintStatusCompleted || sprint.Status == models.SprintStatusCancelled {
		return fmt.Errorf("no se pueden agregar tareas a un sprint completado o cancelado")
	}

	// Actualizar la tarea
	if err := s.db.Model(&models.Task{}).
		Where("id = ?", taskID).
		Update("sprint_id", sprintID).Error; err != nil {
		return fmt.Errorf("error agregando tarea al sprint: %w", err)
	}

	// Recalcular métricas del sprint
	s.CalculateSprintMetrics(&sprint)
	s.db.Save(&sprint)

	return nil
}

func (s *SprintService) RemoveTaskFromSprint(sprintID, taskID, userID uuid.UUID) error {
	if err := s.db.Model(&models.Task{}).
		Where("id = ? AND sprint_id = ?", taskID, sprintID).
		Update("sprint_id", nil).Error; err != nil {
		return fmt.Errorf("error removiendo tarea del sprint: %w", err)
	}

	// Recalcular métricas del sprint
	var sprint models.Sprint
	if err := s.db.First(&sprint, sprintID).Error; err == nil {
		s.CalculateSprintMetrics(&sprint)
		s.db.Save(&sprint)
	}

	return nil
}

func (s *SprintService) CreateSprintEvent(sprintID, userID uuid.UUID, eventType models.SprintEventType, title, content string) (*models.SprintEvent, error) {
	event := &models.SprintEvent{
		SprintID: sprintID,
		Type:     eventType,
		Title:    title,
		Content:  content,
		UserID:   userID,
		Date:     time.Now(),
	}

	if err := s.db.Create(event).Error; err != nil {
		return nil, fmt.Errorf("error creando evento de sprint: %w", err)
	}

	return event, nil
}

func (s *SprintService) GetSprintEvents(sprintID uuid.UUID) ([]models.SprintEvent, error) {
	var events []models.SprintEvent
	
	if err := s.db.Where("sprint_id = ?", sprintID).
		Preload("User").
		Order("date DESC").
		Find(&events).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo eventos del sprint: %w", err)
	}

	return events, nil
}

func (s *SprintService) CalculateSprintMetrics(sprint *models.Sprint) {
	// Obtener tareas del sprint
	var tasks []models.Task
	s.db.Where("sprint_id = ?", sprint.ID).Find(&tasks)

	committedPoints := 0
	completedPoints := 0

	for _, task := range tasks {
		if task.StoryPoints > 0 {
			committedPoints += task.StoryPoints
			if task.Status == models.TaskStatusCompleted {
				completedPoints += task.StoryPoints
			}
		}
	}

	sprint.CommittedPoints = committedPoints
	sprint.CompletedPoints = completedPoints
	sprint.Velocity = sprint.CalculateVelocity()
}

func (s *SprintService) GetSprintBurndownData(sprintID uuid.UUID) (map[string]interface{}, error) {
	var sprint models.Sprint
	if err := s.db.Preload("Tasks").First(&sprint, sprintID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo sprint: %w", err)
	}

	// Calcular datos de burndown por día
	burndownData := make(map[string]interface{})
	
	// TODO: Implementar cálculo detallado de burndown chart
	burndownData["sprint_id"] = sprintID
	burndownData["total_points"] = sprint.CommittedPoints
	burndownData["completed_points"] = sprint.CompletedPoints
	burndownData["remaining_points"] = sprint.CommittedPoints - sprint.CompletedPoints
	burndownData["days_remaining"] = sprint.GetDaysRemaining()
	
	return burndownData, nil
}

func (s *SprintService) notifySprintStarted(sprint *models.Sprint, userID uuid.UUID) {
	// Obtener miembros del proyecto
	var members []models.ProjectMember
	s.db.Where("project_id = ?", sprint.ProjectID).Find(&members)

	userIDs := make([]uuid.UUID, len(members))
	for i, member := range members {
		userIDs[i] = member.UserID
	}

	s.notificationService.CreateNotifications(&models.CreateNotificationRequest{
		Title:      "Sprint iniciado",
		Content:    fmt.Sprintf("El sprint '%s' ha sido iniciado", sprint.Name),
		Type:       models.NotificationTypeSprintStarted,
		UserIDs:    userIDs,
		ActionURL:  fmt.Sprintf("/sprints/%s", sprint.ID),
		EntityType: "sprint",
		EntityID:   &sprint.ID,
	})
}

func (s *SprintService) notifySprintCompleted(sprint *models.Sprint, userID uuid.UUID) {
	// Similar a notifySprintStarted pero para finalización
	var members []models.ProjectMember
	s.db.Where("project_id = ?", sprint.ProjectID).Find(&members)

	userIDs := make([]uuid.UUID, len(members))
	for i, member := range members {
		userIDs[i] = member.UserID
	}

	s.notificationService.CreateNotifications(&models.CreateNotificationRequest{
		Title:      "Sprint completado",
		Content:    fmt.Sprintf("El sprint '%s' ha sido completado", sprint.Name),
		Type:       models.NotificationTypeSprintEnded,
		UserIDs:    userIDs,
		ActionURL:  fmt.Sprintf("/sprints/%s", sprint.ID),
		EntityType: "sprint",
		EntityID:   &sprint.ID,
	})
}
"""
    
    sprint_service_path = os.path.join(backend_dir, "internal", "services", "sprint_service.go")
    with open(sprint_service_path, "w", encoding="utf-8") as f:
        f.write(sprint_service_content)
    
    # internal/services/timetracking_service.go
    timetracking_service_content = """package services

import (
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type TimeTrackingService struct {
	db *gorm.DB
}

func NewTimeTrackingService(db *gorm.DB) *TimeTrackingService {
	return &TimeTrackingService{
		db: db,
	}
}

func (s *TimeTrackingService) StartTimeEntry(userID, projectID uuid.UUID, req *models.CreateTimeEntryRequest) (*models.TimeEntry, error) {
	// Verificar que no hay otra entrada de tiempo activa
	var activeEntry models.TimeEntry
	if err := s.db.Where("user_id = ? AND end_time IS NULL", userID).First(&activeEntry).Error; err == nil {
		return nil, fmt.Errorf("ya tienes una entrada de tiempo activa. Detén la anterior antes de iniciar una nueva")
	}

	entry := &models.TimeEntry{
		Description: req.Description,
		StartTime:   req.StartTime,
		TaskID:      req.TaskID,
		ProjectID:   projectID,
		UserID:      userID,
		IsBillable:  req.IsBillable,
		Tags:        req.Tags,
	}

	if err := s.db.Create(entry).Error; err != nil {
		return nil, fmt.Errorf("error iniciando seguimiento de tiempo: %w", err)
	}

	return s.GetTimeEntry(entry.ID, userID)
}

func (s *TimeTrackingService) StopTimeEntry(entryID, userID uuid.UUID, endTime *time.Time) (*models.TimeEntry, error) {
	var entry models.TimeEntry
	
	if err := s.db.Where("id = ? AND user_id = ?", entryID, userID).First(&entry).Error; err != nil {
		return nil, fmt.Errorf("entrada de tiempo no encontrada: %w", err)
	}

	if entry.EndTime != nil {
		return nil, fmt.Errorf("la entrada de tiempo ya está detenida")
	}

	if endTime == nil {
		now := time.Now()
		endTime = &now
	}

	entry.EndTime = endTime
	entry.Duration = entry.CalculateDuration()

	if err := s.db.Save(&entry).Error; err != nil {
		return nil, fmt.Errorf("error deteniendo seguimiento de tiempo: %w", err)
	}

	return s.GetTimeEntry(entryID, userID)
}

func (s *TimeTrackingService) GetTimeEntries(userID uuid.UUID, projectID *uuid.UUID, startDate, endDate *time.Time) ([]models.TimeEntry, error) {
	query := s.db.Where("user_id = ?", userID).
		Preload("Task").
		Preload("Project").
		Order("start_time DESC")

	if projectID != nil {
		query = query.Where("project_id = ?", *projectID)
	}

	if startDate != nil {
		query = query.Where("start_time >= ?", *startDate)
	}

	if endDate != nil {
		query = query.Where("start_time <= ?", *endDate)
	}

	var entries []models.TimeEntry
	if err := query.Find(&entries).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo entradas de tiempo: %w", err)
	}

	return entries, nil
}

func (s *TimeTrackingService) GetTimeEntry(entryID, userID uuid.UUID) (*models.TimeEntry, error) {
	var entry models.TimeEntry
	
	if err := s.db.Where("id = ? AND user_id = ?", entryID, userID).
		Preload("Task").
		Preload("Project").
		First(&entry).Error; err != nil {
		return nil, fmt.Errorf("entrada de tiempo no encontrada: %w", err)
	}

	return &entry, nil
}

func (s *TimeTrackingService) UpdateTimeEntry(entryID, userID uuid.UUID, req *models.UpdateTimeEntryRequest) (*models.TimeEntry, error) {
	var entry models.TimeEntry
	
	if err := s.db.Where("id = ? AND user_id = ?", entryID, userID).First(&entry).Error; err != nil {
		return nil, fmt.Errorf("entrada de tiempo no encontrada: %w", err)
	}

	// Actualizar campos
	if req.Description != "" {
		entry.Description = req.Description
	}
	if !req.StartTime.IsZero() {
		entry.StartTime = req.StartTime
	}
	if req.EndTime != nil {
		entry.EndTime = req.EndTime
		entry.Duration = entry.CalculateDuration()
	}
	if req.IsBillable != nil {
		entry.IsBillable = *req.IsBillable
	}
	if req.Tags != nil {
		entry.Tags = req.Tags
	}

	if err := s.db.Save(&entry).Error; err != nil {
		return nil, fmt.Errorf("error actualizando entrada de tiempo: %w", err)
	}

	return s.GetTimeEntry(entryID, userID)
}

func (s *TimeTrackingService) DeleteTimeEntry(entryID, userID uuid.UUID) error {
	result := s.db.Where("id = ? AND user_id = ?", entryID, userID).Delete(&models.TimeEntry{})
	
	if result.Error != nil {
		return fmt.Errorf("error eliminando entrada de tiempo: %w", result.Error)
	}

	if result.RowsAffected == 0 {
		return fmt.Errorf("entrada de tiempo no encontrada")
	}

	return nil
}

func (s *TimeTrackingService) GetActiveTimeEntry(userID uuid.UUID) (*models.TimeEntry, error) {
	var entry models.TimeEntry
	
	if err := s.db.Where("user_id = ? AND end_time IS NULL", userID).
		Preload("Task").
		Preload("Project").
		First(&entry).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil // No hay entrada activa
		}
		return nil, fmt.Errorf("error obteniendo entrada de tiempo activa: %w", err)
	}

	return &entry, nil
}

// Timesheet methods
func (s *TimeTrackingService) CreateTimesheetEntry(userID uuid.UUID, req *models.CreateTimesheetEntryRequest) (*models.TimesheetEntry, error) {
	entry := &models.TimesheetEntry{
		Date:        req.Date,
		UserID:      userID,
		ProjectID:   req.ProjectID,
		TaskID:      req.TaskID,
		Hours:       req.Hours,
		Description: req.Description,
		IsBillable:  req.IsBillable,
		Status:      models.TimesheetStatusDraft,
	}

	if err := s.db.Create(entry).Error; err != nil {
		return nil, fmt.Errorf("error creando entrada de timesheet: %w", err)
	}

	return s.GetTimesheetEntry(entry.ID, userID)
}

func (s *TimeTrackingService) GetTimesheetEntry(entryID, userID uuid.UUID) (*models.TimesheetEntry, error) {
	var entry models.TimesheetEntry
	
	if err := s.db.Where("id = ? AND user_id = ?", entryID, userID).
		Preload("User").
		Preload("Project").
		Preload("Task").
		First(&entry).Error; err != nil {
		return nil, fmt.Errorf("entrada de timesheet no encontrada: %w", err)
	}

	return &entry, nil
}

func (s *TimeTrackingService) GetTimesheetEntries(userID uuid.UUID, startDate, endDate time.Time) ([]models.TimesheetEntry, error) {
	var entries []models.TimesheetEntry
	
	if err := s.db.Where("user_id = ? AND date >= ? AND date <= ?", userID, startDate, endDate).
		Preload("Project").
		Preload("Task").
		Order("date DESC").
		Find(&entries).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo entradas de timesheet: %w", err)
	}

	return entries, nil
}

func (s *TimeTrackingService) SubmitTimesheet(userID uuid.UUID, startDate, endDate time.Time) error {
	result := s.db.Model(&models.TimesheetEntry{}).
		Where("user_id = ? AND date >= ? AND date <= ? AND status = ?", 
			userID, startDate, endDate, models.TimesheetStatusDraft).
		Update("status", models.TimesheetStatusSubmitted)

	if result.Error != nil {
		return fmt.Errorf("error enviando timesheet: %w", result.Error)
	}

	return nil
}

func (s *TimeTrackingService) GetTimeReports(userID uuid.UUID, projectID *uuid.UUID, startDate, endDate time.Time) (map[string]interface{}, error) {
	query := s.db.Model(&models.TimeEntry{}).Where("user_id = ? AND start_time >= ? AND start_time <= ?", userID, startDate, endDate)
	
	if projectID != nil {
		query = query.Where("project_id = ?", *projectID)
	}

	// Total de tiempo
	var totalMinutes int
	query.Select("COALESCE(SUM(duration), 0)").Scan(&totalMinutes)

	// Tiempo por proyecto
	var projectTime []struct {
		ProjectID uuid.UUID `json:"project_id"`
		ProjectName string  `json:"project_name"`
		TotalMinutes int    `json:"total_minutes"`
	}
	
	s.db.Model(&models.TimeEntry{}).
		Select("time_entries.project_id, projects.name as project_name, COALESCE(SUM(time_entries.duration), 0) as total_minutes").
		Joins("LEFT JOIN projects ON projects.id = time_entries.project_id").
		Where("time_entries.user_id = ? AND time_entries.start_time >= ? AND time_entries.start_time <= ?", userID, startDate, endDate).
		Group("time_entries.project_id, projects.name").
		Scan(&projectTime)

	// Tiempo por día
	var dailyTime []struct {
		Date string `json:"date"`
		TotalMinutes int `json:"total_minutes"`
	}
	
	s.db.Model(&models.TimeEntry{}).
		Select("DATE(start_time) as date, COALESCE(SUM(duration), 0) as total_minutes").
		Where("user_id = ? AND start_time >= ? AND start_time <= ?", userID, startDate, endDate).
		Group("DATE(start_time)").
		Order("date").
		Scan(&dailyTime)

	return map[string]interface{}{
		"total_hours":    float64(totalMinutes) / 60.0,
		"total_minutes":  totalMinutes,
		"project_breakdown": projectTime,
		"daily_breakdown":   dailyTime,
		"period_start":   startDate,
		"period_end":     endDate,
	}, nil
}

func (s *TimeTrackingService) GetTeamTimeReports(projectID uuid.UUID, startDate, endDate time.Time) (map[string]interface{}, error) {
	// Tiempo por usuario
	var userTime []struct {
		UserID uuid.UUID `json:"user_id"`
		FirstName string `json:"first_name"`
		LastName string  `json:"last_name"`
		TotalMinutes int `json:"total_minutes"`
	}
	
	s.db.Model(&models.TimeEntry{}).
		Select("time_entries.user_id, users.first_name, users.last_name, COALESCE(SUM(time_entries.duration), 0) as total_minutes").
		Joins("LEFT JOIN users ON users.id = time_entries.user_id").
		Where("time_entries.project_id = ? AND time_entries.start_time >= ? AND time_entries.start_time <= ?", projectID, startDate, endDate).
		Group("time_entries.user_id, users.first_name, users.last_name").
		Scan(&userTime)

	// Total del equipo
	var totalMinutes int
	s.db.Model(&models.TimeEntry{}).
		Select("COALESCE(SUM(duration), 0)").
		Where("project_id = ? AND start_time >= ? AND start_time <= ?", projectID, startDate, endDate).
		Scan(&totalMinutes)

	return map[string]interface{}{
		"total_hours":      float64(totalMinutes) / 60.0,
		"total_minutes":    totalMinutes,
		"user_breakdown":   userTime,
		"period_start":     startDate,
		"period_end":       endDate,
	}, nil
}
"""
    
    timetracking_service_path = os.path.join(backend_dir, "internal", "services", "timetracking_service.go")
    with open(timetracking_service_path, "w", encoding="utf-8") as f:
        f.write(timetracking_service_content)
    
    print("✓ Servicios avanzados creados")

def create_advanced_handlers(backend_dir):
    """Crear handlers para funcionalidades avanzadas"""
    
    # internal/api/handlers/sprint_handler.go
    sprint_handler_content = """package handlers

import (
	"net/http"
	"strconv"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/services"
	"github.com/company/project-management-platform/internal/utils"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type SprintHandler struct {
	sprintService *services.SprintService
}

func NewSprintHandler(sprintService *services.SprintService) *SprintHandler {
	return &SprintHandler{
		sprintService: sprintService,
	}
}

func (h *SprintHandler) CreateSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	projectID, err := uuid.Parse(c.Param("project_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de proyecto inválido")
		return
	}

	var req models.CreateSprintRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	sprint, err := h.sprintService.CreateSprint(projectID, userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, sprint)
}

func (h *SprintHandler) GetSprints(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	projectID, err := uuid.Parse(c.Param("project_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de proyecto inválido")
		return
	}

	var status *models.SprintStatus
	if statusStr := c.Query("status"); statusStr != "" {
		s := models.SprintStatus(statusStr)
		status = &s
	}

	sprints, err := h.sprintService.GetSprints(projectID, userID, status)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, sprints)
}

func (h *SprintHandler) GetSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	sprint, err := h.sprintService.GetSprint(sprintID, userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusNotFound, err.Error())
		return
	}

	utils.SuccessResponse(c, sprint)
}

func (h *SprintHandler) UpdateSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	var req models.UpdateSprintRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	sprint, err := h.sprintService.UpdateSprint(sprintID, userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, sprint)
}

func (h *SprintHandler) StartSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	sprint, err := h.sprintService.StartSprint(sprintID, userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, sprint)
}

func (h *SprintHandler) CompleteSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	sprint, err := h.sprintService.CompleteSprint(sprintID, userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, sprint)
}

func (h *SprintHandler) AddTaskToSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	var req struct {
		TaskID uuid.UUID `json:"task_id" binding:"required"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	if err := h.sprintService.AddTaskToSprint(sprintID, req.TaskID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Tarea agregada al sprint"})
}

func (h *SprintHandler) RemoveTaskFromSprint(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	taskID, err := uuid.Parse(c.Param("task_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de tarea inválido")
		return
	}

	if err := h.sprintService.RemoveTaskFromSprint(sprintID, taskID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Tarea removida del sprint"})
}

func (h *SprintHandler) CreateSprintEvent(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	var req struct {
		Type    models.SprintEventType `json:"type" binding:"required"`
		Title   string                 `json:"title" binding:"required"`
		Content string                 `json:"content"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	event, err := h.sprintService.CreateSprintEvent(sprintID, userID, req.Type, req.Title, req.Content)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, event)
}

func (h *SprintHandler) GetSprintEvents(c *gin.Context) {
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	events, err := h.sprintService.GetSprintEvents(sprintID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, events)
}

func (h *SprintHandler) GetSprintBurndown(c *gin.Context) {
	sprintID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de sprint inválido")
		return
	}

	burndownData, err := h.sprintService.GetSprintBurndownData(sprintID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, burndownData)
}
"""
    
    sprint_handler_path = os.path.join(backend_dir, "internal", "api", "handlers", "sprint_handler.go")
    with open(sprint_handler_path, "w", encoding="utf-8") as f:
        f.write(sprint_handler_content)
    
    # internal/api/handlers/timetracking_handler.go
    timetracking_handler_content = """package handlers

import (
	"net/http"
	"strconv"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/services"
	"github.com/company/project-management-platform/internal/utils"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type TimeTrackingHandler struct {
	timeTrackingService *services.TimeTrackingService
}

func NewTimeTrackingHandler(timeTrackingService *services.TimeTrackingService) *TimeTrackingHandler {
	return &TimeTrackingHandler{
		timeTrackingService: timeTrackingService,
	}
}

func (h *TimeTrackingHandler) StartTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	projectID, err := uuid.Parse(c.Param("project_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de proyecto inválido")
		return
	}

	var req models.CreateTimeEntryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	entry, err := h.timeTrackingService.StartTimeEntry(userID, projectID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, entry)
}

func (h *TimeTrackingHandler) StopTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	entryID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de entrada inválido")
		return
	}

	var req struct {
		EndTime *time.Time `json:"end_time"`
	}
	c.ShouldBindJSON(&req)

	entry, err := h.timeTrackingService.StopTimeEntry(entryID, userID, req.EndTime)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, entry)
}

func (h *TimeTrackingHandler) GetTimeEntries(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	
	var projectID *uuid.UUID
	if projectIDStr := c.Query("project_id"); projectIDStr != "" {
		if id, err := uuid.Parse(projectIDStr); err == nil {
			projectID = &id
		}
	}

	var startDate, endDate *time.Time
	if startDateStr := c.Query("start_date"); startDateStr != "" {
		if t, err := time.Parse("2006-01-02", startDateStr); err == nil {
			startDate = &t
		}
	}
	if endDateStr := c.Query("end_date"); endDateStr != "" {
		if t, err := time.Parse("2006-01-02", endDateStr); err == nil {
			endDate = &t
		}
	}

	entries, err := h.timeTrackingService.GetTimeEntries(userID, projectID, startDate, endDate)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, entries)
}

func (h *TimeTrackingHandler) GetTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	entryID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de entrada inválido")
		return
	}

	entry, err := h.timeTrackingService.GetTimeEntry(entryID, userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusNotFound, err.Error())
		return
	}

	utils.SuccessResponse(c, entry)
}

func (h *TimeTrackingHandler) UpdateTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	entryID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de entrada inválido")
		return
	}

	var req models.UpdateTimeEntryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	entry, err := h.timeTrackingService.UpdateTimeEntry(entryID, userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, entry)
}

func (h *TimeTrackingHandler) DeleteTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	entryID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de entrada inválido")
		return
	}

	if err := h.timeTrackingService.DeleteTimeEntry(entryID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Entrada de tiempo eliminada"})
}

func (h *TimeTrackingHandler) GetActiveTimeEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	entry, err := h.timeTrackingService.GetActiveTimeEntry(userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	if entry == nil {
		c.JSON(http.StatusOK, gin.H{"active_entry": nil})
		return
	}

	utils.SuccessResponse(c, gin.H{"active_entry": entry})
}

func (h *TimeTrackingHandler) GetTimeReports(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	
	var projectID *uuid.UUID
	if projectIDStr := c.Query("project_id"); projectIDStr != "" {
		if id, err := uuid.Parse(projectIDStr); err == nil {
			projectID = &id
		}
	}

	startDate, err := time.Parse("2006-01-02", c.DefaultQuery("start_date", time.Now().AddDate(0, 0, -30).Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de inicio inválida")
		return
	}

	endDate, err := time.Parse("2006-01-02", c.DefaultQuery("end_date", time.Now().Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de fin inválida")
		return
	}

	reports, err := h.timeTrackingService.GetTimeReports(userID, projectID, startDate, endDate)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, reports)
}

func (h *TimeTrackingHandler) GetTeamTimeReports(c *gin.Context) {
	projectID, err := uuid.Parse(c.Param("project_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de proyecto inválido")
		return
	}

	startDate, err := time.Parse("2006-01-02", c.DefaultQuery("start_date", time.Now().AddDate(0, 0, -30).Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de inicio inválida")
		return
	}

	endDate, err := time.Parse("2006-01-02", c.DefaultQuery("end_date", time.Now().Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de fin inválida")
		return
	}

	reports, err := h.timeTrackingService.GetTeamTimeReports(projectID, startDate, endDate)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, reports)
}

// Timesheet endpoints
func (h *TimeTrackingHandler) CreateTimesheetEntry(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	var req models.CreateTimesheetEntryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	entry, err := h.timeTrackingService.CreateTimesheetEntry(userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, entry)
}

func (h *TimeTrackingHandler) GetTimesheetEntries(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	startDate, err := time.Parse("2006-01-02", c.DefaultQuery("start_date", time.Now().AddDate(0, 0, -7).Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de inicio inválida")
		return
	}

	endDate, err := time.Parse("2006-01-02", c.DefaultQuery("end_date", time.Now().Format("2006-01-02")))
	if err != nil {
		utils.ValidationErrorResponse(c, "Fecha de fin inválida")
		return
	}

	entries, err := h.timeTrackingService.GetTimesheetEntries(userID, startDate, endDate)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, entries)
}

func (h *TimeTrackingHandler) SubmitTimesheet(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	var req struct {
		StartDate time.Time `json:"start_date" binding:"required"`
		EndDate   time.Time `json:"end_date" binding:"required"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	if err := h.timeTrackingService.SubmitTimesheet(userID, req.StartDate, req.EndDate); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Timesheet enviado para aprobación"})
}
"""
    
    timetracking_handler_path = os.path.join(backend_dir, "internal", "api", "handlers", "timetracking_handler.go")
    with open(timetracking_handler_path, "w", encoding="utf-8") as f:
        f.write(timetracking_handler_content)
    
    print("✓ Handlers avanzados creados")

def create_sprint_components(frontend_dir):
    """Crear componentes de sprint para el frontend"""
    
    # src/app/features/sprints/sprint-board.component.ts
    sprint_board_content = """import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { ProgressBarModule } from 'primeng/progressbar';
import { CalendarModule } from 'primeng/calendar';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { ChartModule } from 'primeng/chart';
import { TimelineModule } from 'primeng/timeline';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { SprintService, Sprint } from '@core/services/sprint.service';

@Component({
  selector: 'app-sprint-board',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    TagModule,
    ProgressBarModule,
    CalendarModule,
    InputTextModule,
    InputTextareaModule,
    DialogModule,
    DropdownModule,
    ChartModule,
    TimelineModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Gestión de Sprints"
      description="Planifica y gestiona sprints ágiles"
      titleIcon="pi pi-chart-line"
      [actions]="headerActions">
    </app-page-header>

    <div class="sprint-container">
      <!-- Sprint actual -->
      <div class="current-sprint" *ngIf="currentSprint">
        <p-card>
          <ng-template pTemplate="header">
            <div class="sprint-header">
              <div class="sprint-info">
                <h2>{{ currentSprint.name }}</h2>
                <p-tag 
                  [value]="getStatusLabel(currentSprint.status)"
                  [severity]="getStatusSeverity(currentSprint.status)">
                </p-tag>
              </div>
              <div class="sprint-actions">
                <p-button 
                  *ngIf="currentSprint.status === 'planning'"
                  label="Iniciar Sprint"
                  icon="pi pi-play"
                  (onClick)="startSprint(currentSprint)">
                </p-button>
                <p-button 
                  *ngIf="currentSprint.status === 'active'"
                  label="Completar Sprint"
                  icon="pi pi-check"
                  severity="success"
                  (onClick)="completeSprint(currentSprint)">
                </p-button>
                <p-button 
                  icon="pi pi-cog"
                  severity="secondary"
                  [text]="true"
                  (onClick)="editSprint(currentSprint)">
                </p-button>
              </div>
            </div>
          </ng-template>

          <div class="sprint-content">
            <div class="sprint-details">
              <p class="sprint-goal" *ngIf="currentSprint.goal">
                <strong>Objetivo:</strong> {{ currentSprint.goal }}
              </p>
              <div class="sprint-dates">
                <span><strong>Inicio:</strong> {{ currentSprint.start_date | date:'dd/MM/yyyy' }}</span>
                <span><strong>Fin:</strong> {{ currentSprint.end_date | date:'dd/MM/yyyy' }}</span>
                <span *ngIf="currentSprint.status === 'active'">
                  <strong>Días restantes:</strong> {{ getDaysRemaining(currentSprint) }}
                </span>
              </div>
            </div>

            <!-- Métricas del sprint -->
            <div class="sprint-metrics" *ngIf="currentSprint.status === 'active' || currentSprint.status === 'completed'">
              <div class="metrics-grid">
                <div class="metric-item">
                  <h4>{{ currentSprint.completed_points }}</h4>
                  <p>Puntos Completados</p>
                </div>
                <div class="metric-item">
                  <h4>{{ currentSprint.committed_points }}</h4>
                  <p>Puntos Comprometidos</p>
                </div>
                <div class="metric-item">
                  <h4>{{ currentSprint.velocity }}%</h4>
                  <p>Velocidad</p>
                </div>
                <div class="metric-item">
                  <h4>{{ getTasksCount(currentSprint) }}</h4>
                  <p>Tareas</p>
                </div>
              </div>

              <!-- Barra de progreso -->
              <div class="progress-section">
                <label>Progreso del Sprint</label>
                <p-progressBar 
                  [value]="getSprintProgress(currentSprint)"
                  [showValue]="true">
                </p-progressBar>
              </div>
            </div>

            <!-- Chart de burndown -->
            <div class="burndown-chart" *ngIf="currentSprint.status === 'active' && burndownData">
              <h3>Burndown Chart</h3>
              <p-chart 
                type="line" 
                [data]="burndownData" 
                [options]="burndownOptions"
                width="100%"
                height="300px">
              </p-chart>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Lista de sprints -->
      <div class="sprints-list">
        <div class="list-header">
          <h3>Todos los Sprints</h3>
          <div class="list-filters">
            <p-dropdown 
              [options]="statusOptions"
              [(ngModel)]="selectedStatus"
              placeholder="Filtrar por estado"
              (onChange)="onStatusFilter()"
              [showClear]="true">
            </p-dropdown>
          </div>
        </div>

        <div class="sprints-grid">
          <p-card 
            *ngFor="let sprint of sprints; trackBy: trackBySprint"
            class="sprint-card"
            [class.current]="sprint.id === currentSprint?.id">
            
            <ng-template pTemplate="header">
              <div class="card-header">
                <h4>{{ sprint.name }}</h4>
                <p-tag 
                  [value]="getStatusLabel(sprint.status)"
                  [severity]="getStatusSeverity(sprint.status)">
                </p-tag>
              </div>
            </ng-template>

            <div class="card-content">
              <p class="sprint-description" *ngIf="sprint.description">
                {{ sprint.description }}
              </p>
              
              <div class="sprint-dates">
                <small>{{ sprint.start_date | date:'dd/MM' }} - {{ sprint.end_date | date:'dd/MM/yyyy' }}</small>
              </div>

              <div class="sprint-stats" *ngIf="sprint.status !== 'planning'">
                <div class="stat">
                  <span class="label">Progreso:</span>
                  <span class="value">{{ getSprintProgress(sprint) }}%</span>
                </div>
                <div class="stat">
                  <span class="label">Tareas:</span>
                  <span class="value">{{ getTasksCount(sprint) }}</span>
                </div>
              </div>
            </div>

            <ng-template pTemplate="footer">
              <div class="card-actions">
                <p-button 
                  label="Ver Detalles"
                  icon="pi pi-eye"
                  [text]="true"
                  size="small"
                  [routerLink]="['/sprints', sprint.id]">
                </p-button>
                <p-button 
                  *ngIf="sprint.status === 'planning'"
                  label="Editar"
                  icon="pi pi-pencil"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="editSprint(sprint)">
                </p-button>
                <p-button 
                  *ngIf="sprint.status === 'planning'"
                  label="Iniciar"
                  icon="pi pi-play"
                  size="small"
                  (onClick)="startSprint(sprint)">
                </p-button>
              </div>
            </ng-template>
          </p-card>
        </div>
      </div>
    </div>

    <!-- Dialog para crear/editar sprint -->
    <p-dialog 
      header="{{ editingSprintId ? 'Editar Sprint' : 'Nuevo Sprint' }}"
      [(visible)]="showSprintDialog"
      [modal]="true"
      [style]="{width: '600px'}"
      [closable]="true">
      
      <form class="sprint-form">
        <div class="form-group">
          <label>Nombre del Sprint *</label>
          <input 
            type="text"
            pInputText
            [(ngModel)]="sprintForm.name"
            name="name"
            placeholder="Ej: Sprint 1"
            class="form-control">
        </div>

        <div class="form-group">
          <label>Descripción</label>
          <textarea 
            pInputTextarea
            [(ngModel)]="sprintForm.description"
            name="description"
            rows="3"
            placeholder="Descripción del sprint"
            class="form-control">
          </textarea>
        </div>

        <div class="form-group">
          <label>Objetivo del Sprint</label>
          <textarea 
            pInputTextarea
            [(ngModel)]="sprintForm.goal"
            name="goal"
            rows="2"
            placeholder="¿Qué se quiere lograr en este sprint?"
            class="form-control">
          </textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha de Inicio *</label>
            <p-calendar 
              [(ngModel)]="sprintForm.start_date"
              name="start_date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>

          <div class="form-group">
            <label>Fecha de Fin *</label>
            <p-calendar 
              [(ngModel)]="sprintForm.end_date"
              name="end_date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>
        </div>

        <div class="form-group">
          <label>Capacidad (Story Points)</label>
          <input 
            type="number"
            pInputText
            [(ngModel)]="sprintForm.capacity"
            name="capacity"
            min="0"
            placeholder="0"
            class="form-control">
        </div>
      </form>

      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [text]="true"
          (onClick)="cancelSprintDialog()">
        </p-button>
        <p-button 
          [label]="editingSprintId ? 'Actualizar' : 'Crear'"
          (onClick)="saveSprint()"
          [loading]="savingSprint">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .sprint-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Sprint actual */
    .current-sprint {
      margin-bottom: 2rem;
    }

    .sprint-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      margin: -1rem -1rem 0 -1rem;
    }

    .sprint-header h2 {
      margin: 0 0 0.5rem 0;
      color: white;
    }

    .sprint-actions {
      display: flex;
      gap: 0.5rem;
    }

    .sprint-content {
      padding: 1.5rem;
    }

    .sprint-details {
      margin-bottom: 1.5rem;
    }

    .sprint-goal {
      margin: 0 0 1rem 0;
      padding: 1rem;
      background: #f8f9fa;
      border-left: 4px solid #007bff;
      border-radius: 4px;
    }

    .sprint-dates {
      display: flex;
      gap: 2rem;
      font-size: 0.9rem;
      color: #666;
    }

    .sprint-dates span {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* Métricas */
    .sprint-metrics {
      margin-bottom: 2rem;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .metric-item {
      text-align: center;
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .metric-item h4 {
      margin: 0 0 0.5rem 0;
      font-size: 1.8rem;
      color: #007bff;
    }

    .metric-item p {
      margin: 0;
      font-size: 0.9rem;
      color: #666;
    }

    .progress-section {
      margin-top: 1rem;
    }

    .progress-section label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 600;
      color: #333;
    }

    /* Burndown chart */
    .burndown-chart {
      margin-top: 2rem;
      padding: 1.5rem;
      background: #f8f9fa;
      border-radius: 8px;
    }

    .burndown-chart h3 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    /* Lista de sprints */
    .list-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .list-header h3 {
      margin: 0;
      color: #333;
    }

    .list-filters {
      display: flex;
      gap: 1rem;
    }

    .sprints-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 1.5rem;
    }

    .sprint-card {
      transition: transform 0.2s ease;
    }

    .sprint-card:hover {
      transform: translateY(-2px);
    }

    .sprint-card.current {
      border: 2px solid #007bff;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .card-header h4 {
      margin: 0;
      color: #333;
    }

    .card-content {
      padding: 1rem;
    }

    .sprint-description {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.9rem;
      line-height: 1.4;
    }

    .sprint-stats {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
    }

    .stat {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }

    .stat .label {
      font-size: 0.8rem;
      color: #999;
    }

    .stat .value {
      font-weight: 600;
      color: #333;
    }

    .card-actions {
      display: flex;
      gap: 0.5rem;
      justify-content: flex-end;
      padding: 1rem;
      background: #f8f9fa;
      margin: 0 -1rem -1rem -1rem;
    }

    /* Dialog de sprint */
    .sprint-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-weight: 600;
      color: #333;
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    .form-control {
      width: 100%;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .sprint-container {
        padding: 0 1rem 1rem;
      }

      .sprint-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
      }

      .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .sprints-grid {
        grid-template-columns: 1fr;
      }

      .list-header {
        flex-direction: column;
        gap: 1rem;
        align-items: stretch;
      }

      .sprint-dates {
        flex-direction: column;
        gap: 0.5rem;
      }

      .form-row {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class SprintBoardComponent implements OnInit {
  sprints: Sprint[] = [];
  currentSprint: Sprint | null = null;
  selectedStatus: string | null = null;
  burndownData: any = null;
  burndownOptions: any = {};

  // Dialog
  showSprintDialog = false;
  editingSprintId: string | null = null;
  savingSprint = false;

  sprintForm = {
    name: '',
    description: '',
    goal: '',
    start_date: new Date(),
    end_date: new Date(),
    capacity: 0
  };

  statusOptions = [
    { label: 'Planificación', value: 'planning' },
    { label: 'Activo', value: 'active' },
    { label: 'Completado', value: 'completed' },
    { label: 'Cancelado', value: 'cancelled' }
  ];

  headerActions = [
    {
      label: 'Nuevo Sprint',
      icon: 'pi pi-plus',
      onClick: () => this.createSprint()
    }
  ];

  constructor(private sprintService: SprintService) {
    this.setupBurndownChart();
  }

  ngOnInit(): void {
    this.loadSprints();
  }

  private loadSprints(): void {
    // Obtener proyecto actual del contexto/ruta
    const projectId = 'current-project-id'; // TODO: Obtener del contexto

    this.sprintService.getSprints(projectId, this.selectedStatus).subscribe(
      sprints => {
        this.sprints = sprints;
        this.currentSprint = sprints.find(s => s.status === 'active') || null;
        
        if (this.currentSprint) {
          this.loadBurndownData();
        }
      }
    );
  }

  private loadBurndownData(): void {
    if (!this.currentSprint) return;

    this.sprintService.getBurndownData(this.currentSprint.id).subscribe(
      data => {
        this.burndownData = {
          labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5'],
          datasets: [
            {
              label: 'Trabajo Restante',
              data: [100, 80, 60, 30, 10],
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.1)',
              tension: 0.4
            },
            {
              label: 'Línea Ideal',
              data: [100, 75, 50, 25, 0],
              borderColor: '#6c757d',
              borderDash: [5, 5],
              tension: 0.4
            }
          ]
        };
      }
    );
  }

  private setupBurndownChart(): void {
    this.burndownOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Story Points'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Días del Sprint'
          }
        }
      },
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      }
    };
  }

  createSprint(): void {
    this.editingSprintId = null;
    this.resetSprintForm();
    this.showSprintDialog = true;
  }

  editSprint(sprint: Sprint): void {
    this.editingSprintId = sprint.id;
    this.sprintForm = {
      name: sprint.name,
      description: sprint.description || '',
      goal: sprint.goal || '',
      start_date: new Date(sprint.start_date),
      end_date: new Date(sprint.end_date),
      capacity: sprint.capacity || 0
    };
    this.showSprintDialog = true;
  }

  saveSprint(): void {
    this.savingSprint = true;
    const projectId = 'current-project-id'; // TODO: Obtener del contexto

    const request = {
      name: this.sprintForm.name,
      description: this.sprintForm.description,
      goal: this.sprintForm.goal,
      start_date: this.sprintForm.start_date,
      end_date: this.sprintForm.end_date,
      capacity: this.sprintForm.capacity
    };

    const operation = this.editingSprintId
      ? this.sprintService.updateSprint(this.editingSprintId, request)
      : this.sprintService.createSprint(projectId, request);

    operation.subscribe(
      () => {
        this.showSprintDialog = false;
        this.savingSprint = false;
        this.loadSprints();
      },
      error => {
        console.error('Error saving sprint:', error);
        this.savingSprint = false;
      }
    );
  }

  startSprint(sprint: Sprint): void {
    this.sprintService.startSprint(sprint.id).subscribe(
      () => {
        this.loadSprints();
      }
    );
  }

  completeSprint(sprint: Sprint): void {
    this.sprintService.completeSprint(sprint.id).subscribe(
      () => {
        this.loadSprints();
      }
    );
  }

  onStatusFilter(): void {
    this.loadSprints();
  }

  cancelSprintDialog(): void {
    this.showSprintDialog = false;
    this.resetSprintForm();
  }

  private resetSprintForm(): void {
    this.sprintForm = {
      name: '',
      description: '',
      goal: '',
      start_date: new Date(),
      end_date: new Date(),
      capacity: 0
    };
  }

  getStatusLabel(status: string): string {
    const labels = {
      'planning': 'Planificación',
      'active': 'Activo',
      'completed': 'Completado',
      'cancelled': 'Cancelado'
    };
    return labels[status as keyof typeof labels] || status;
  }

  getStatusSeverity(status: string): string {
    const severities = {
      'planning': 'warning',
      'active': 'info',
      'completed': 'success',
      'cancelled': 'danger'
    };
    return severities[status as keyof typeof severities] || 'secondary';
  }

  getSprintProgress(sprint: Sprint): number {
    if (sprint.committed_points === 0) return 0;
    return Math.round((sprint.completed_points / sprint.committed_points) * 100);
  }

  getTasksCount(sprint: Sprint): number {
    return sprint.tasks ? sprint.tasks.length : 0;
  }

  getDaysRemaining(sprint: Sprint): number {
    const today = new Date();
    const endDate = new Date(sprint.end_date);
    const diffTime = endDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(0, diffDays);
  }

  trackBySprint(index: number, sprint: Sprint): string {
    return sprint.id;
  }
}
"""
    
    sprint_board_path = os.path.join(frontend_dir, "src/app/features/sprints/sprint-board.component.ts")
    os.makedirs(os.path.dirname(sprint_board_path), exist_ok=True)
    with open(sprint_board_path, "w", encoding="utf-8") as f:
        f.write(sprint_board_content)
    
    # src/app/core/services/sprint.service.ts
    sprint_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Sprint {
  id: string;
  name: string;
  description?: string;
  project_id: string;
  start_date: string;
  end_date: string;
  status: 'planning' | 'active' | 'completed' | 'cancelled';
  goal?: string;
  capacity: number;
  committed_points: number;
  completed_points: number;
  velocity: number;
  created_at: string;
  updated_at: string;
  
  // Relaciones
  project?: any;
  tasks?: any[];
  events?: SprintEvent[];
}

export interface SprintEvent {
  id: string;
  sprint_id: string;
  type: 'planning' | 'daily' | 'review' | 'retrospective' | 'custom';
  title: string;
  content?: string;
  user_id: string;
  date: string;
  user?: any;
}

export interface CreateSprintRequest {
  name: string;
  description?: string;
  start_date: Date;
  end_date: Date;
  goal?: string;
  capacity?: number;
}

export interface UpdateSprintRequest {
  name?: string;
  description?: string;
  start_date?: Date;
  end_date?: Date;
  goal?: string;
  capacity?: number;
}

@Injectable({
  providedIn: 'root'
})
export class SprintService {

  constructor(private http: HttpClient) { }

  getSprints(projectId: string, status?: string | null): Observable<Sprint[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set('status', status);
    }
    
    return this.http.get<Sprint[]>(`${environment.apiUrl}/projects/${projectId}/sprints`, { params });
  }

  getSprint(sprintId: string): Observable<Sprint> {
    return this.http.get<Sprint>(`${environment.apiUrl}/sprints/${sprintId}`);
  }

  createSprint(projectId: string, sprintData: CreateSprintRequest): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/projects/${projectId}/sprints`, sprintData);
  }

  updateSprint(sprintId: string, sprintData: UpdateSprintRequest): Observable<Sprint> {
    return this.http.put<Sprint>(`${environment.apiUrl}/sprints/${sprintId}`, sprintData);
  }

  startSprint(sprintId: string): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/sprints/${sprintId}/start`, {});
  }

  completeSprint(sprintId: string): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/sprints/${sprintId}/complete`, {});
  }

  addTaskToSprint(sprintId: string, taskId: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/sprints/${sprintId}/tasks`, {
      task_id: taskId
    });
  }

  removeTaskFromSprint(sprintId: string, taskId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/sprints/${sprintId}/tasks/${taskId}`);
  }

  getSprintEvents(sprintId: string): Observable<SprintEvent[]> {
    return this.http.get<SprintEvent[]>(`${environment.apiUrl}/sprints/${sprintId}/events`);
  }

  createSprintEvent(sprintId: string, eventData: {
    type: string;
    title: string;
    content?: string;
  }): Observable<SprintEvent> {
    return this.http.post<SprintEvent>(`${environment.apiUrl}/sprints/${sprintId}/events`, eventData);
  }

  getBurndownData(sprintId: string): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}/sprints/${sprintId}/burndown`);
  }

  getSprintMetrics(sprintId: string): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}/sprints/${sprintId}/metrics`);
  }

  getVelocityChart(projectId: string, sprintCount = 10): Observable<any> {
    const params = new HttpParams().set('sprint_count', sprintCount.toString());
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/velocity`, { params });
  }
}
"""
    
    sprint_service_path = os.path.join(frontend_dir, "src/app/core/services/sprint.service.ts")
    with open(sprint_service_path, "w", encoding="utf-8") as f:
        f.write(sprint_service_content)
    
    print("✓ Componentes de sprint creados")

def create_timetracking_components(frontend_dir):
    """Crear componentes de timetracking para el frontend"""
    
    # src/app/features/time-tracking/time-tracker.component.ts
    time_tracker_content = """import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { TagModule } from 'primeng/tag';
import { CalendarModule } from 'primeng/calendar';
import { ChartModule } from 'primeng/chart';
import { TableModule } from 'primeng/table';
import { DialogModule } from 'primeng/dialog';
import { Subscription, interval } from 'rxjs';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { TimeTrackingService, TimeEntry } from '@core/services/time-tracking.service';

@Component({
  selector: 'app-time-tracker',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    TagModule,
    CalendarModule,
    ChartModule,
    TableModule,
    DialogModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Seguimiento de Tiempo"
      description="Registra y gestiona el tiempo dedicado a proyectos y tareas"
      titleIcon="pi pi-clock"
      [actions]="headerActions">
    </app-page-header>

    <div class="time-tracking-container">
      <!-- Timer activo -->
      <div class="active-timer" *ngIf="activeEntry">
        <p-card>
          <ng-template pTemplate="header">
            <div class="timer-header">
              <h3>⏱️ Tiempo en curso</h3>
              <p-tag 
                value="ACTIVO"
                severity="success"
                [rounded]="true">
              </p-tag>
            </div>
          </ng-template>

          <div class="timer-content">
            <div class="timer-display">
              <h2 class="elapsed-time">{{ formatDuration(elapsedSeconds) }}</h2>
              <p class="timer-description">{{ activeEntry.description }}</p>
              <div class="timer-meta">
                <span *ngIf="activeEntry.task">
                  <i class="pi pi-bookmark"></i>
                  {{ activeEntry.task?.title }}
                </span>
                <span>
                  <i class="pi pi-folder"></i>
                  {{ activeEntry.project?.name }}
                </span>
                <span>
                  <i class="pi pi-calendar"></i>
                  {{ activeEntry.start_time | date:'HH:mm' }}
                </span>
              </div>
            </div>

            <div class="timer-actions">
              <p-button 
                label="Detener"
                icon="pi pi-stop"
                severity="danger"
                (onClick)="stopTimer()">
              </p-button>
              <p-button 
                label="Editar"
                icon="pi pi-pencil"
                severity="secondary"
                [text]="true"
                (onClick)="editActiveEntry()">
              </p-button>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Iniciar nuevo timer -->
      <div class="start-timer" *ngIf="!activeEntry">
        <p-card>
          <ng-template pTemplate="header">
            <h3>🚀 Iniciar seguimiento</h3>
          </ng-template>

          <form class="timer-form">
            <div class="form-group">
              <label>¿En qué estás trabajando? *</label>
              <input 
                type="text"
                pInputText
                [(ngModel)]="newEntryForm.description"
                name="description"
                placeholder="Describe la actividad..."
                class="form-control">
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Proyecto *</label>
                <p-dropdown 
                  [options]="projectOptions"
                  [(ngModel)]="newEntryForm.project_id"
                  name="project_id"
                  placeholder="Seleccionar proyecto"
                  optionLabel="name"
                  optionValue="id"
                  class="form-control">
                </p-dropdown>
              </div>

              <div class="form-group">
                <label>Tarea (Opcional)</label>
                <p-dropdown 
                  [options]="taskOptions"
                  [(ngModel)]="newEntryForm.task_id"
                  name="task_id"
                  placeholder="Seleccionar tarea"
                  optionLabel="title"
                  optionValue="id"
                  [showClear]="true"
                  class="form-control">
                </p-dropdown>
              </div>
            </div>

            <div class="form-actions">
              <p-button 
                label="Iniciar Timer"
                icon="pi pi-play"
                (onClick)="startTimer()"
                [disabled]="!canStartTimer()">
              </p-button>
              <p-button 
                label="Entrada Manual"
                icon="pi pi-plus"
                severity="secondary"
                [outlined]="true"
                (onClick)="showManualEntryDialog()">
              </p-button>
            </div>
          </form>
        </p-card>
      </div>

      <!-- Resumen del día -->
      <div class="daily-summary">
        <p-card>
          <ng-template pTemplate="header">
            <div class="summary-header">
              <h3>📊 Resumen de hoy</h3>
              <p-calendar 
                [(ngModel)]="selectedDate"
                (onSelect)="onDateChange()"
                dateFormat="dd/mm/yy"
                [showIcon]="true">
              </p-calendar>
            </div>
          </ng-template>

          <div class="summary-content">
            <div class="summary-stats">
              <div class="stat-item">
                <h4>{{ todayStats.total_hours }}h</h4>
                <p>Total</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.billable_hours }}h</h4>
                <p>Facturable</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.entries_count }}</h4>
                <p>Entradas</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.projects_count }}</h4>
                <p>Proyectos</p>
              </div>
            </div>

            <!-- Gráfico de distribución -->
            <div class="time-distribution" *ngIf="chartData">
              <h4>Distribución por proyecto</h4>
              <p-chart 
                type="doughnut" 
                [data]="chartData" 
                [options]="chartOptions"
                width="100%"
                height="300px">
              </p-chart>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Lista de entradas -->
      <div class="time-entries">
        <p-card>
          <ng-template pTemplate="header">
            <div class="entries-header">
              <h3>📝 Entradas de tiempo</h3>
              <div class="header-filters">
                <p-dropdown 
                  [options]="projectFilterOptions"
                  [(ngModel)]="selectedProjectFilter"
                  placeholder="Filtrar por proyecto"
                  [showClear]="true"
                  (onChange)="onProjectFilter()">
                </p-dropdown>
              </div>
            </div>
          </ng-template>

          <p-table 
            [value]="timeEntries"
            [loading]="loadingEntries"
            [paginator]="true"
            [rows]="10"
            responsiveLayout="scroll">
            
            <ng-template pTemplate="header">
              <tr>
                <th>Descripción</th>
                <th>Proyecto</th>
                <th>Tarea</th>
                <th>Inicio</th>
                <th>Duración</th>
                <th>Facturable</th>
                <th>Acciones</th>
              </tr>
            </ng-template>

            <ng-template pTemplate="body" let-entry>
              <tr>
                <td>{{ entry.description }}</td>
                <td>
                  <span class="project-badge">{{ entry.project?.name }}</span>
                </td>
                <td>
                  <span *ngIf="entry.task" class="task-badge">{{ entry.task?.title }}</span>
                  <span *ngIf="!entry.task" class="no-task">Sin tarea</span>
                </td>
                <td>{{ entry.start_time | date:'dd/MM HH:mm' }}</td>
                <td>
                  <span class="duration">{{ formatDuration(entry.duration * 60) }}</span>
                </td>
                <td>
                  <p-tag 
                    [value]="entry.is_billable ? 'Sí' : 'No'"
                    [severity]="entry.is_billable ? 'success' : 'secondary'">
                  </p-tag>
                </td>
                <td>
                  <div class="entry-actions">
                    <p-button 
                      icon="pi pi-pencil"
                      severity="secondary"
                      [text]="true"
                      size="small"
                      (onClick)="editEntry(entry)"
                      pTooltip="Editar">
                    </p-button>
                    <p-button 
                      icon="pi pi-trash"
                      severity="danger"
                      [text]="true"
                      size="small"
                      (onClick)="deleteEntry(entry)"
                      pTooltip="Eliminar">
                    </p-button>
                  </div>
                </td>
              </tr>
            </ng-template>

            <ng-template pTemplate="emptymessage">
              <tr>
                <td colspan="7" class="text-center">
                  No hay entradas de tiempo para mostrar
                </td>
              </tr>
            </ng-template>
          </p-table>
        </p-card>
      </div>
    </div>

    <!-- Dialog para entrada manual -->
    <p-dialog 
      header="Entrada Manual de Tiempo"
      [(visible)]="showManualDialog"
      [modal]="true"
      [style]="{width: '500px'}"
      [closable]="true">
      
      <form class="manual-form">
        <div class="form-group">
          <label>Descripción *</label>
          <input 
            type="text"
            pInputText
            [(ngModel)]="manualForm.description"
            name="description"
            placeholder="¿En qué trabajaste?"
            class="form-control">
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Proyecto *</label>
            <p-dropdown 
              [options]="projectOptions"
              [(ngModel)]="manualForm.project_id"
              name="project_id"
              placeholder="Seleccionar"
              optionLabel="name"
              optionValue="id"
              class="form-control">
            </p-dropdown>
          </div>

          <div class="form-group">
            <label>Tarea</label>
            <p-dropdown 
              [options]="taskOptions"
              [(ngModel)]="manualForm.task_id"
              name="task_id"
              placeholder="Opcional"
              optionLabel="title"
              optionValue="id"
              [showClear]="true"
              class="form-control">
            </p-dropdown>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha *</label>
            <p-calendar 
              [(ngModel)]="manualForm.date"
              name="date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>

          <div class="form-group">
            <label>Horas *</label>
            <input 
              type="number"
              pInputText
              [(ngModel)]="manualForm.hours"
              name="hours"
              min="0.1"
              max="24"
              step="0.25"
              placeholder="0.5"
              class="form-control">
          </div>
        </div>

        <div class="form-group">
          <div class="checkbox-wrapper">
            <input 
              type="checkbox"
              id="billable"
              [(ngModel)]="manualForm.is_billable"
              name="is_billable">
            <label for="billable">Tiempo facturable</label>
          </div>
        </div>
      </form>

      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [text]="true"
          (onClick)="cancelManualDialog()">
        </p-button>
        <p-button 
          label="Guardar"
          (onClick)="saveManualEntry()"
          [loading]="savingEntry">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .time-tracking-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Timer activo */
    .timer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
      color: white;
      margin: -1rem -1rem 0 -1rem;
    }

    .timer-header h3 {
      margin: 0;
      color: white;
    }

    .timer-content {
      padding: 1.5rem;
      text-align: center;
    }

    .elapsed-time {
      font-size: 3rem;
      font-weight: 300;
      color: #28a745;
      margin: 0 0 0.5rem 0;
      font-family: 'Courier New', monospace;
    }

    .timer-description {
      font-size: 1.2rem;
      color: #333;
      margin: 0 0 1rem 0;
    }

    .timer-meta {
      display: flex;
      justify-content: center;
      gap: 2rem;
      margin-bottom: 2rem;
      font-size: 0.9rem;
      color: #666;
    }

    .timer-meta span {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .timer-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }

    /* Formulario de inicio */
    .timer-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-weight: 600;
      color: #333;
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    .form-control {
      width: 100%;
    }

    .form-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
      margin-top: 1rem;
    }

    /* Resumen del día */
    .summary-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .summary-header h3 {
      margin: 0;
      color: #333;
    }

    .summary-content {
      padding: 1.5rem;
    }

    .summary-stats {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .stat-item {
      text-align: center;
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .stat-item h4 {
      margin: 0 0 0.5rem 0;
      font-size: 1.5rem;
      color: #007bff;
    }

    .stat-item p {
      margin: 0;
      font-size: 0.9rem;
      color: #666;
    }

    .time-distribution h4 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    /* Lista de entradas */
    .entries-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .entries-header h3 {
      margin: 0;
      color: #333;
    }

    .header-filters {
      display: flex;
      gap: 1rem;
    }

    .project-badge {
      display: inline-block;
      padding: 0.25rem 0.5rem;
      background: #007bff;
      color: white;
      border-radius: 4px;
      font-size: 0.8rem;
    }

    .task-badge {
      display: inline-block;
      padding: 0.25rem 0.5rem;
      background: #28a745;
      color: white;
      border-radius: 4px;
      font-size: 0.8rem;
    }

    .no-task {
      color: #999;
      font-style: italic;
      font-size: 0.9rem;
    }

    .duration {
      font-family: 'Courier New', monospace;
      font-weight: 600;
      color: #333;
    }

    .entry-actions {
      display: flex;
      gap: 0.25rem;
    }

    /* Dialog manual */
    .manual-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .checkbox-wrapper {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .checkbox-wrapper input[type="checkbox"] {
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .time-tracking-container {
        padding: 0 1rem 1rem;
      }

      .timer-meta {
        flex-direction: column;
        gap: 0.5rem;
      }

      .form-row {
        grid-template-columns: 1fr;
      }

      .summary-stats {
        grid-template-columns: repeat(2, 1fr);
      }

      .form-actions {
        flex-direction: column;
      }

      .timer-actions {
        flex-direction: column;
      }
    }

    /* Animaciones */
    .elapsed-time {
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.7; }
      100% { opacity: 1; }
    }
  `]
})
export class TimeTrackerComponent implements OnInit, OnDestroy {
  activeEntry: TimeEntry | null = null;
  timeEntries: TimeEntry[] = [];
  projectOptions: any[] = [];
  taskOptions: any[] = [];
  projectFilterOptions: any[] = [];
  
  selectedDate = new Date();
  selectedProjectFilter: string | null = null;
  loadingEntries = false;
  
  // Timer
  elapsedSeconds = 0;
  timerSubscription?: Subscription;
  
  // Forms
  newEntryForm = {
    description: '',
    project_id: '',
    task_id: null,
    is_billable: true
  };
  
  manualForm = {
    description: '',
    project_id: '',
    task_id: null,
    date: new Date(),
    hours: 0,
    is_billable: true
  };
  
  // Stats
  todayStats = {
    total_hours: 0,
    billable_hours: 0,
    entries_count: 0,
    projects_count: 0
  };
  
  // Chart
  chartData: any = null;
  chartOptions: any = {};
  
  // Dialog
  showManualDialog = false;
  savingEntry = false;
  
  headerActions = [
    {
      label: 'Reportes',
      icon: 'pi pi-chart-bar',
      onClick: () => this.goToReports()
    },
    {
      label: 'Exportar',
      icon: 'pi pi-download',
      onClick: () => this.exportTimesheet()
    }
  ];

  constructor(private timeTrackingService: TimeTrackingService) {
    this.setupChart();
  }

  ngOnInit(): void {
    this.loadActiveEntry();
    this.loadTimeEntries();
    this.loadProjects();
    this.loadTodayStats();
  }

  ngOnDestroy(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }

  private loadActiveEntry(): void {
    this.timeTrackingService.getActiveEntry().subscribe(
      response => {
        this.activeEntry = response.active_entry;
        if (this.activeEntry) {
          this.startElapsedTimer();
        }
      }
    );
  }

  private loadTimeEntries(): void {
    this.loadingEntries = true;
    
    const startDate = new Date(this.selectedDate);
    startDate.setHours(0, 0, 0, 0);
    
    const endDate = new Date(this.selectedDate);
    endDate.setHours(23, 59, 59, 999);
    
    this.timeTrackingService.getTimeEntries(
      this.selectedProjectFilter,
      startDate,
      endDate
    ).subscribe(
      entries => {
        this.timeEntries = entries;
        this.loadingEntries = false;
      },
      error => {
        console.error('Error loading entries:', error);
        this.loadingEntries = false;
      }
    );
  }

  private loadProjects(): void {
    // TODO: Cargar desde ProjectService
    this.projectOptions = [
      { id: '1', name: 'Proyecto Alpha' },
      { id: '2', name: 'Proyecto Beta' }
    ];
    
    this.projectFilterOptions = [
      { label: 'Todos los proyectos', value: null },
      ...this.projectOptions.map(p => ({ label: p.name, value: p.id }))
    ];
  }

  private loadTodayStats(): void {
    const startDate = new Date(this.selectedDate);
    startDate.setHours(0, 0, 0, 0);
    
    const endDate = new Date(this.selectedDate);
    endDate.setHours(23, 59, 59, 999);
    
    this.timeTrackingService.getTimeReports(null, startDate, endDate).subscribe(
      stats => {
        this.todayStats = {
          total_hours: Math.round(stats.total_hours * 100) / 100,
          billable_hours: Math.round(stats.billable_hours * 100) / 100,
          entries_count: this.timeEntries.length,
          projects_count: stats.project_breakdown?.length || 0
        };
        
        this.updateChart(stats.project_breakdown || []);
      }
    );
  }

  private setupChart(): void {
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    };
  }

  private updateChart(projectData: any[]): void {
    if (projectData.length === 0) {
      this.chartData = null;
      return;
    }
    
    this.chartData = {
      labels: projectData.map(p => p.project_name),
      datasets: [{
        data: projectData.map(p => Math.round(p.total_minutes / 60 * 100) / 100),
        backgroundColor: [
          '#007bff',
          '#28a745',
          '#ffc107',
          '#dc3545',
          '#6f42c1',
          '#fd7e14'
        ]
      }]
    };
  }

  private startElapsedTimer(): void {
    if (!this.activeEntry) return;
    
    const startTime = new Date(this.activeEntry.start_time);
    
    this.timerSubscription = interval(1000).subscribe(() => {
      const now = new Date();
      this.elapsedSeconds = Math.floor((now.getTime() - startTime.getTime()) / 1000);
    });
  }

  startTimer(): void {
    if (!this.canStartTimer()) return;
    
    const request = {
      description: this.newEntryForm.description,
      start_time: new Date(),
      task_id: this.newEntryForm.task_id,
      is_billable: this.newEntryForm.is_billable
    };
    
    this.timeTrackingService.startTimer(this.newEntryForm.project_id, request).subscribe(
      entry => {
        this.activeEntry = entry;
        this.startElapsedTimer();
        this.resetNewEntryForm();
      }
    );
  }

  stopTimer(): void {
    if (!this.activeEntry) return;
    
    this.timeTrackingService.stopTimer(this.activeEntry.id).subscribe(
      () => {
        this.activeEntry = null;
        this.elapsedSeconds = 0;
        
        if (this.timerSubscription) {
          this.timerSubscription.unsubscribe();
        }
        
        this.loadTimeEntries();
        this.loadTodayStats();
      }
    );
  }

  editActiveEntry(): void {
    if (!this.activeEntry) return;
    // TODO: Implementar edición de entrada activa
  }

  editEntry(entry: TimeEntry): void {
    // TODO: Implementar edición de entrada
  }

  deleteEntry(entry: TimeEntry): void {
    this.timeTrackingService.deleteTimeEntry(entry.id).subscribe(
      () => {
        this.loadTimeEntries();
        this.loadTodayStats();
      }
    );
  }

  showManualEntryDialog(): void {
    this.showManualDialog = true;
  }

  saveManualEntry(): void {
    this.savingEntry = true;
    
    const request = {
      description: this.manualForm.description,
      project_id: this.manualForm.project_id,
      task_id: this.manualForm.task_id,
      date: this.manualForm.date,
      hours: this.manualForm.hours,
      is_billable: this.manualForm.is_billable
    };
    
    this.timeTrackingService.createTimesheetEntry(request).subscribe(
      () => {
        this.showManualDialog = false;
        this.savingEntry = false;
        this.resetManualForm();
        this.loadTimeEntries();
        this.loadTodayStats();
      },
      error => {
        console.error('Error saving manual entry:', error);
        this.savingEntry = false;
      }
    );
  }

  cancelManualDialog(): void {
    this.showManualDialog = false;
    this.resetManualForm();
  }

  onDateChange(): void {
    this.loadTimeEntries();
    this.loadTodayStats();
  }

  onProjectFilter(): void {
    this.loadTimeEntries();
  }

  canStartTimer(): boolean {
    return !!this.newEntryForm.description.trim() && !!this.newEntryForm.project_id;
  }

  formatDuration(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  private resetNewEntryForm(): void {
    this.newEntryForm = {
      description: '',
      project_id: '',
      task_id: null,
      is_billable: true
    };
  }

  private resetManualForm(): void {
    this.manualForm = {
      description: '',
      project_id: '',
      task_id: null,
      date: new Date(),
      hours: 0,
      is_billable: true
    };
  }

  goToReports(): void {
    // TODO: Navegar a reportes
  }

  exportTimesheet(): void {
    // TODO: Implementar exportación
  }
}
"""
    
    time_tracker_path = os.path.join(frontend_dir, "src/app/features/time-tracking/time-tracker.component.ts")
    os.makedirs(os.path.dirname(time_tracker_path), exist_ok=True)
    with open(time_tracker_path, "w", encoding="utf-8") as f:
        f.write(time_tracker_content)
    
    # src/app/core/services/time-tracking.service.ts
    time_tracking_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface TimeEntry {
  id: string;
  description: string;
  start_time: string;
  end_time?: string;
  duration: number; // en minutos
  task_id?: string;
  project_id: string;
  user_id: string;
  is_billable: boolean;
  hourly_rate?: number;
  tags: string[];
  created_at: string;
  updated_at: string;
  
  // Relaciones
  task?: any;
  project?: any;
  user?: any;
}

export interface TimesheetEntry {
  id: string;
  date: string;
  user_id: string;
  project_id: string;
  task_id?: string;
  hours: number;
  description: string;
  is_billable: boolean;
  status: 'draft' | 'submitted' | 'approved' | 'rejected';
  
  // Relaciones
  user?: any;
  project?: any;
  task?: any;
}

export interface CreateTimeEntryRequest {
  description: string;
  start_time: Date;
  end_time?: Date;
  task_id?: string;
  is_billable: boolean;
  tags?: string[];
}

export interface CreateTimesheetEntryRequest {
  date: Date;
  project_id: string;
  task_id?: string;
  hours: number;
  description: string;
  is_billable: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TimeTrackingService {

  constructor(private http: HttpClient) { }

  // Time Entries
  startTimer(projectId: string, entryData: CreateTimeEntryRequest): Observable<TimeEntry> {
    return this.http.post<TimeEntry>(`${environment.apiUrl}/projects/${projectId}/time-entries`, entryData);
  }

  stopTimer(entryId: string, endTime?: Date): Observable<TimeEntry> {
    return this.http.put<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}/stop`, {
      end_time: endTime
    });
  }

  getTimeEntries(projectId?: string | null, startDate?: Date, endDate?: Date): Observable<TimeEntry[]> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<TimeEntry[]>(`${environment.apiUrl}/time-entries`, { params });
  }

  getTimeEntry(entryId: string): Observable<TimeEntry> {
    return this.http.get<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}`);
  }

  updateTimeEntry(entryId: string, entryData: Partial<CreateTimeEntryRequest>): Observable<TimeEntry> {
    return this.http.put<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}`, entryData);
  }

  deleteTimeEntry(entryId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/time-entries/${entryId}`);
  }

  getActiveEntry(): Observable<{active_entry: TimeEntry | null}> {
    return this.http.get<{active_entry: TimeEntry | null}>(`${environment.apiUrl}/time-entries/active`);
  }

  // Time Reports
  getTimeReports(projectId?: string | null, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<any>(`${environment.apiUrl}/time-reports`, { params });
  }

  getTeamTimeReports(projectId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/time-reports`, { params });
  }

  // Timesheet Entries
  createTimesheetEntry(entryData: CreateTimesheetEntryRequest): Observable<TimesheetEntry> {
    return this.http.post<TimesheetEntry>(`${environment.apiUrl}/timesheet-entries`, entryData);
  }

  getTimesheetEntries(startDate?: Date, endDate?: Date): Observable<TimesheetEntry[]> {
    let params = new HttpParams();
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<TimesheetEntry[]>(`${environment.apiUrl}/timesheet-entries`, { params });
  }

  submitTimesheet(startDate: Date, endDate: Date): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/timesheet/submit`, {
      start_date: startDate,
      end_date: endDate
    });
  }

  // Utilities
  calculateDuration(startTime: Date, endTime: Date): number {
    return Math.floor((endTime.getTime() - startTime.getTime()) / 60000); // en minutos
  }

  formatDuration(minutes: number): string {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours === 0) {
      return `${mins}m`;
    } else if (mins === 0) {
      return `${hours}h`;
    } else {
      return `${hours}h ${mins}m`;
    }
  }

  exportTimesheet(format: 'csv' | 'excel' | 'pdf', startDate?: Date, endDate?: Date): Observable<Blob> {
    let params = new HttpParams().set('format', format);
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get(`${environment.apiUrl}/time-entries/export`, {
      params,
      responseType: 'blob'
    });
  }
}
"""
    
    time_tracking_service_path = os.path.join(frontend_dir, "src/app/core/services/time-tracking.service.ts")
    with open(time_tracking_service_path, "w", encoding="utf-8") as f:
        f.write(time_tracking_service_content)
    
    print("✓ Componentes de timetracking creados")

def create_reporting_components(frontend_dir):
    """Crear componentes de reportes para el frontend"""
    
    # src/app/features/reports/reports-dashboard.component.ts
    reports_dashboard_content = """import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { ChartModule } from 'primeng/chart';
import { DropdownModule } from 'primeng/dropdown';
import { CalendarModule } from 'primeng/calendar';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ProgressBarModule } from 'primeng/progressbar';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { ReportService } from '@core/services/report.service';

@Component({
  selector: 'app-reports-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    ChartModule,
    DropdownModule,
    CalendarModule,
    TableModule,
    TagModule,
    ProgressBarModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Centro de Reportes"
      description="Analiza el rendimiento de proyectos, equipos y tiempo"
      titleIcon="pi pi-chart-bar"
      [actions]="headerActions">
    </app-page-header>

    <div class="reports-container">
      <!-- Filtros globales -->
      <div class="filters-section">
        <p-card>
          <div class="filters-content">
            <div class="filter-group">
              <label>Proyecto</label>
              <p-dropdown 
                [options]="projectOptions"
                [(ngModel)]="selectedProject"
                placeholder="Todos los proyectos"
                [showClear]="true"
                (onChange)="onFiltersChange()">
              </p-dropdown>
            </div>

            <div class="filter-group">
              <label>Período</label>
              <p-dropdown 
                [options]="periodOptions"
                [(ngModel)]="selectedPeriod"
                (onChange)="onPeriodChange()">
              </p-dropdown>
            </div>

            <div class="filter-group" *ngIf="selectedPeriod === 'custom'">
              <label>Fecha Inicio</label>
              <p-calendar 
                [(ngModel)]="customStartDate"
                dateFormat="dd/mm/yy"
                [showIcon]="true"
                (onSelect)="onFiltersChange()">
              </p-calendar>
            </div>

            <div class="filter-group" *ngIf="selectedPeriod === 'custom'">
              <label>Fecha Fin</label>
              <p-calendar 
                [(ngModel)]="customEndDate"
                dateFormat="dd/mm/yy"
                [showIcon]="true"
                (onSelect)="onFiltersChange()">
              </p-calendar>
            </div>

            <div class="filter-actions">
              <p-button 
                label="Aplicar Filtros"
                icon="pi pi-search"
                (onClick)="applyFilters()">
              </p-button>
              <p-button 
                label="Limpiar"
                severity="secondary"
                [text]="true"
                (onClick)="clearFilters()">
              </p-button>
            </div>
          </div>
        </p-card>
      </div>

      <!-- KPIs principales -->
      <div class="kpis-section">
        <div class="kpis-grid">
          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">📊</div>
              <div class="kpi-data">
                <h3>{{ kpis.totalProjects }}</h3>
                <p>Proyectos Activos</p>
                <span class="kpi-trend" [class.positive]="kpis.projectsTrend > 0">
                  <i [class]="kpis.projectsTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                  {{ Math.abs(kpis.projectsTrend) }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">✅</div>
              <div class="kpi-data">
                <h3>{{ kpis.completedTasks }}</h3>
                <p>Tareas Completadas</p>
                <span class="kpi-trend positive">
                  <i class="pi pi-arrow-up"></i>
                  {{ kpis.tasksTrend }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">⏱️</div>
              <div class="kpi-data">
                <h3>{{ kpis.totalHours }}h</h3>
                <p>Horas Trabajadas</p>
                <span class="kpi-trend positive">
                  <i class="pi pi-arrow-up"></i>
                  {{ kpis.hoursTrend }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">🚀</div>
              <div class="kpi-data">
                <h3>{{ kpis.teamVelocity }}</h3>
                <p>Velocidad del Equipo</p>
                <span class="kpi-trend" [class.positive]="kpis.velocityTrend > 0">
                  <i [class]="kpis.velocityTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                  {{ Math.abs(kpis.velocityTrend) }}%
                </span>
              </div>
            </div>
          </p-card>
        </div>
      </div>

      <!-- Gráficos principales -->
      <div class="charts-section">
        <div class="charts-grid">
          <!-- Gráfico de progreso de proyectos -->
          <p-card class="chart-card">
            <ng-template pTemplate="header">
              <h3>Progreso de Proyectos</h3>
            </ng-template>
            
            <p-chart 
              type="bar" 
              [data]="projectProgressChart" 
              [options]="barChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Gráfico de distribución de tiempo -->
          <p-card class="chart-card">
            <ng-template pTemplate="header">
              <h3>Distribución de Tiempo</h3>
            </ng-template>
            
            <p-chart 
              type="doughnut" 
              [data]="timeDistributionChart" 
              [options]="doughnutChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Gráfico de velocidad del equipo -->
          <p-card class="chart-card wide">
            <ng-template pTemplate="header">
              <h3>Velocidad del Equipo (Story Points)</h3>
            </ng-template>
            
            <p-chart 
              type="line" 
              [data]="velocityChart" 
              [options]="lineChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Burndown chart -->
          <p-card class="chart-card wide">
            <ng-template pTemplate="header">
              <h3>Burndown Chart - Sprint Actual</h3>
            </ng-template>
            
            <p-chart 
              type="line" 
              [data]="burndownChart" 
              [options]="burndownChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>
        </div>
      </div>

      <!-- Tablas de datos -->
      <div class="tables-section">
        <div class="tables-grid">
          <!-- Top performers -->
          <p-card class="table-card">
            <ng-template pTemplate="header">
              <h3>Top Performers</h3>
            </ng-template>
            
            <p-table [value]="topPerformers" responsiveLayout="scroll">
              <ng-template pTemplate="header">
                <tr>
                  <th>Usuario</th>
                  <th>Tareas</th>
                  <th>Horas</th>
                  <th>Puntos</th>
                </tr>
              </ng-template>
              <ng-template pTemplate="body" let-performer>
                <tr>
                  <td>
                    <div class="user-info">
                      <img [src]="performer.avatar" [alt]="performer.name" class="user-avatar">
                      <span>{{ performer.name }}</span>
                    </div>
                  </td>
                  <td>{{ performer.completedTasks }}</td>
                  <td>{{ performer.hoursWorked }}h</td>
                  <td>{{ performer.storyPoints }}</td>
                </tr>
              </ng-template>
            </p-table>
          </p-card>

          <!-- Proyectos críticos -->
          <p-card class="table-card">
            <ng-template pTemplate="header">
              <h3>Proyectos Críticos</h3>
            </ng-template>
            
            <p-table [value]="criticalProjects" responsiveLayout="scroll">
              <ng-template pTemplate="header">
                <tr>
                  <th>Proyecto</th>
                  <th>Progreso</th>
                  <th>Estado</th>
                  <th>Riesgo</th>
                </tr>
              </ng-template>
              <ng-template pTemplate="body" let-project>
                <tr>
                  <td>{{ project.name }}</td>
                  <td>
                    <p-progressBar 
                      [value]="project.progress"
                      [showValue]="true">
                    </p-progressBar>
                  </td>
                  <td>
                    <p-tag 
                      [value]="project.status"
                      [severity]="getStatusSeverity(project.status)">
                    </p-tag>
                  </td>
                  <td>
                    <p-tag 
                      [value]="project.risk"
                      [severity]="getRiskSeverity(project.risk)">
                    </p-tag>
                  </td>
                </tr>
              </ng-template>
            </p-table>
          </p-card>
        </div>
      </div>

      <!-- Reportes rápidos -->
      <div class="quick-reports">
        <p-card>
          <ng-template pTemplate="header">
            <h3>Reportes Rápidos</h3>
          </ng-template>

          <div class="quick-reports-grid">
            <div class="report-item" (click)="generateQuickReport('project-summary')">
              <i class="pi pi-folder report-icon"></i>
              <h4>Resumen de Proyectos</h4>
              <p>Estado general de todos los proyectos</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('time-analysis')">
              <i class="pi pi-clock report-icon"></i>
              <h4>Análisis de Tiempo</h4>
              <p>Distribución y eficiencia temporal</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('team-performance')">
              <i class="pi pi-users report-icon"></i>
              <h4>Rendimiento del Equipo</h4>
              <p>Métricas de productividad individual</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('budget-tracking')">
              <i class="pi pi-dollar report-icon"></i>
              <h4>Seguimiento de Presupuesto</h4>
              <p>Análisis financiero y costos</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('quality-metrics')">
              <i class="pi pi-star report-icon"></i>
              <h4>Métricas de Calidad</h4>
              <p>Bugs, testing y calidad del código</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('sprint-analysis')">
              <i class="pi pi-chart-line report-icon"></i>
              <h4>Análisis de Sprints</h4>
              <p>Velocidad y burndown histórico</p>
            </div>
          </div>
        </p-card>
      </div>
    </div>
  `,
  styles: [`
    .reports-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Filtros */
    .filters-content {
      display: flex;
      gap: 1rem;
      align-items: end;
      flex-wrap: wrap;
    }

    .filter-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      min-width: 150px;
    }

    .filter-group label {
      font-weight: 600;
      color: #333;
      font-size: 0.9rem;
    }

    .filter-actions {
      display: flex;
      gap: 0.5rem;
      margin-left: auto;
    }

    /* KPIs */
    .kpis-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.5rem;
    }

    .kpi-card {
      border-left: 4px solid #007bff;
    }

    .kpi-content {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
    }

    .kpi-icon {
      font-size: 2.5rem;
      opacity: 0.8;
    }

    .kpi-data h3 {
      margin: 0 0 0.25rem 0;
      font-size: 1.8rem;
      color: #333;
    }

    .kpi-data p {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.9rem;
    }

    .kpi-trend {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.8rem;
      font-weight: 600;
      color: #dc3545;
    }

    .kpi-trend.positive {
      color: #28a745;
    }

    /* Gráficos */
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }

    .chart-card.wide {
      grid-column: span 2;
    }

    .chart-card h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    /* Tablas */
    .tables-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }

    .table-card h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .user-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
    }

    /* Reportes rápidos */
    .quick-reports h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    .quick-reports-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      padding: 1rem;
    }

    .report-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 1.5rem;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .report-item:hover {
      background: #f8f9fa;
      border-color: #007bff;
      transform: translateY(-2px);
    }

    .report-icon {
      font-size: 2rem;
      color: #007bff;
      margin-bottom: 1rem;
    }

    .report-item h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }

    .report-item p {
      margin: 0;
      color: #666;
      font-size: 0.9rem;
    }

    /* Responsive */
    @media (max-width: 1200px) {
      .charts-grid {
        grid-template-columns: 1fr;
      }

      .chart-card.wide {
        grid-column: span 1;
      }
    }

    @media (max-width: 768px) {
      .reports-container {
        padding: 0 1rem 1rem;
      }

      .filters-content {
        flex-direction: column;
        align-items: stretch;
      }

      .filter-actions {
        margin-left: 0;
        justify-content: stretch;
      }

      .kpis-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .tables-grid {
        grid-template-columns: 1fr;
      }

      .quick-reports-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 480px) {
      .kpis-grid {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class ReportsDashboardComponent implements OnInit {
  // Filtros
  selectedProject: string | null = null;
  selectedPeriod = 'last_30_days';
  customStartDate = new Date();
  customEndDate = new Date();

  projectOptions = [
    { label: 'Proyecto Alpha', value: 'alpha' },
    { label: 'Proyecto Beta', value: 'beta' },
    { label: 'Proyecto Gamma', value: 'gamma' }
  ];

  periodOptions = [
    { label: 'Últimos 7 días', value: 'last_7_days' },
    { label: 'Últimos 30 días', value: 'last_30_days' },
    { label: 'Último trimestre', value: 'last_quarter' },
    { label: 'Año actual', value: 'current_year' },
    { label: 'Personalizado', value: 'custom' }
  ];

  // KPIs
  kpis = {
    totalProjects: 8,
    projectsTrend: 12,
    completedTasks: 156,
    tasksTrend: 18,
    totalHours: 342,
    hoursTrend: 8,
    teamVelocity: 85,
    velocityTrend: -5
  };

  // Data
  topPerformers: any[] = [];
  criticalProjects: any[] = [];

  // Charts
  projectProgressChart: any = {};
  timeDistributionChart: any = {};
  velocityChart: any = {};
  burndownChart: any = {};

  // Chart options
  barChartOptions: any = {};
  doughnutChartOptions: any = {};
  lineChartOptions: any = {};
  burndownChartOptions: any = {};

  headerActions = [
    {
      label: 'Exportar Dashboard',
      icon: 'pi pi-download',
      onClick: () => this.exportDashboard()
    },
    {
      label: 'Programar Reporte',
      icon: 'pi pi-calendar',
      onClick: () => this.scheduleReport()
    }
  ];

  Math = Math; // Para usar en template

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.setupChartOptions();
    this.loadDashboardData();
  }

  private setupChartOptions(): void {
    this.barChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    };

    this.doughnutChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    };

    this.lineChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };

    this.burndownChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Story Points'
          }
        }
      }
    };
  }

  private loadDashboardData(): void {
    this.loadTopPerformers();
    this.loadCriticalProjects();
    this.loadChartData();
  }

  private loadTopPerformers(): void {
    this.topPerformers = [
      {
        name: 'Ana García',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 23,
        hoursWorked: 45,
        storyPoints: 89
      },
      {
        name: 'Carlos López',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 19,
        hoursWorked: 38,
        storyPoints: 76
      },
      {
        name: 'María Rodríguez',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 17,
        hoursWorked: 42,
        storyPoints: 72
      }
    ];
  }

  private loadCriticalProjects(): void {
    this.criticalProjects = [
      {
        name: 'Proyecto Alpha',
        progress: 75,
        status: 'En Progreso',
        risk: 'Bajo'
      },
      {
        name: 'Proyecto Beta',
        progress: 45,
        status: 'Retrasado',
        risk: 'Alto'
      },
      {
        name: 'Proyecto Gamma',
        progress: 90,
        status: 'Casi Completo',
        risk: 'Medio'
      }
    ];
  }

  private loadChartData(): void {
    // Progreso de proyectos
    this.projectProgressChart = {
      labels: ['Alpha', 'Beta', 'Gamma', 'Delta'],
      datasets: [{
        label: 'Progreso (%)',
        data: [75, 45, 90, 60],
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545']
      }]
    };

    // Distribución de tiempo
    this.timeDistributionChart = {
      labels: ['Desarrollo', 'Testing', 'Documentación', 'Reuniones'],
      datasets: [{
        data: [40, 25, 20, 15],
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#fd7e14']
      }]
    };

    // Velocidad del equipo
    this.velocityChart = {
      labels: ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5'],
      datasets: [{
        label: 'Velocidad',
        data: [65, 72, 68, 85, 78],
        borderColor: '#007bff',
        backgroundColor: 'rgba(0, 123, 255, 0.1)',
        tension: 0.4
      }]
    };

    // Burndown chart
    this.burndownChart = {
      labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5'],
      datasets: [
        {
          label: 'Trabajo Restante',
          data: [100, 80, 65, 40, 20],
          borderColor: '#007bff',
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          tension: 0.4
        },
        {
          label: 'Línea Ideal',
          data: [100, 75, 50, 25, 0],
          borderColor: '#6c757d',
          borderDash: [5, 5],
          tension: 0.4
        }
      ]
    };
  }

  onFiltersChange(): void {
    // Implementar lógica de filtros
  }

  onPeriodChange(): void {
    if (this.selectedPeriod !== 'custom') {
      this.calculateDateRange();
    }
    this.onFiltersChange();
  }

  private calculateDateRange(): void {
    const now = new Date();
    
    switch (this.selectedPeriod) {
      case 'last_7_days':
        this.customStartDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        this.customEndDate = now;
        break;
      case 'last_30_days':
        this.customStartDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        this.customEndDate = now;
        break;
      case 'last_quarter':
        const quarter = Math.floor(now.getMonth() / 3);
        this.customStartDate = new Date(now.getFullYear(), quarter * 3 - 3, 1);
        this.customEndDate = new Date(now.getFullYear(), quarter * 3, 0);
        break;
      case 'current_year':
        this.customStartDate = new Date(now.getFullYear(), 0, 1);
        this.customEndDate = now;
        break;
    }
  }

  applyFilters(): void {
    console.log('Aplicando filtros:', {
      project: this.selectedProject,
      period: this.selectedPeriod,
      startDate: this.customStartDate,
      endDate: this.customEndDate
    });
    
    this.loadDashboardData();
  }

  clearFilters(): void {
    this.selectedProject = null;
    this.selectedPeriod = 'last_30_days';
    this.customStartDate = new Date();
    this.customEndDate = new Date();
    this.loadDashboardData();
  }

  generateQuickReport(reportType: string): void {
    console.log('Generando reporte rápido:', reportType);
    // TODO: Implementar generación de reportes
  }

  exportDashboard(): void {
    console.log('Exportando dashboard');
    // TODO: Implementar exportación
  }

  scheduleReport(): void {
    console.log('Programando reporte');
    // TODO: Implementar programación de reportes
  }

  getStatusSeverity(status: string): string {
    const severities = {
      'En Progreso': 'info',
      'Retrasado': 'danger',
      'Casi Completo': 'success',
      'Completado': 'success'
    };
    return severities[status as keyof typeof severities] || 'secondary';
  }

  getRiskSeverity(risk: string): string {
    const severities = {
      'Bajo': 'success',
      'Medio': 'warning',
      'Alto': 'danger'
    };
    return severities[risk as keyof typeof severities] || 'secondary';
  }
}
"""
    
    reports_dashboard_path = os.path.join(frontend_dir, "src/app/features/reports/reports-dashboard.component.ts")
    os.makedirs(os.path.dirname(reports_dashboard_path), exist_ok=True)
    with open(reports_dashboard_path, "w", encoding="utf-8") as f:
        f.write(reports_dashboard_content)
    
    # src/app/core/services/report.service.ts
    report_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Report {
  id: string;
  name: string;
  description?: string;
  type: 'task_summary' | 'project_progress' | 'time_tracking' | 'team_performance' | 'sprint_burndown' | 'velocity_chart' | 'budget_analysis' | 'custom';
  project_id?: string;
  user_id: string;
  is_public: boolean;
  schedule?: string;
  config: {[key: string]: any};
  filters: {[key: string]: any};
  last_generated?: string;
  created_at: string;
  updated_at: string;
}

export interface ReportData {
  id: string;
  name: string;
  type: string;
  generated_at: string;
  data: {[key: string]: any};
  charts: ChartData[];
  tables: TableData[];
  summary: ReportSummary;
}

export interface ChartData {
  title: string;
  type: string;
  data: {[key: string]: any};
  config: {[key: string]: any};
}

export interface TableData {
  title: string;
  headers: string[];
  rows: any[][];
  summary: {[key: string]: any};
}

export interface ReportSummary {
  total_items: number;
  completed_items: number;
  metrics: {[key: string]: any};
  insights: string[];
}

export interface CreateReportRequest {
  name: string;
  description?: string;
  type: string;
  project_id?: string;
  is_public: boolean;
  config: {[key: string]: any};
  filters: {[key: string]: any};
  schedule?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  constructor(private http: HttpClient) { }

  getReports(projectId?: string): Observable<Report[]> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<Report[]>(`${environment.apiUrl}/reports`, { params });
  }

  getReport(reportId: string): Observable<Report> {
    return this.http.get<Report>(`${environment.apiUrl}/reports/${reportId}`);
  }

  createReport(reportData: CreateReportRequest): Observable<Report> {
    return this.http.post<Report>(`${environment.apiUrl}/reports`, reportData);
  }

  updateReport(reportId: string, reportData: Partial<CreateReportRequest>): Observable<Report> {
    return this.http.put<Report>(`${environment.apiUrl}/reports/${reportId}`, reportData);
  }

  deleteReport(reportId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/reports/${reportId}`);
  }

  generateReport(reportId: string): Observable<ReportData> {
    return this.http.post<ReportData>(`${environment.apiUrl}/reports/${reportId}/generate`, {});
  }

  getReportData(reportId: string): Observable<ReportData> {
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/${reportId}/data`);
  }

  // Reportes específicos
  getProjectSummaryReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/project-summary`, { params });
  }

  getTimeTrackingReport(projectId?: string, userId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (userId) params = params.set('user_id', userId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/time-tracking`, { params });
  }

  getTeamPerformanceReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/team-performance`, { params });
  }

  getSprintBurndownReport(sprintId: string): Observable<ReportData> {
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/sprint-burndown/${sprintId}`);
  }

  getVelocityChartReport(projectId: string, sprintCount = 10): Observable<ReportData> {
    const params = new HttpParams().set('sprint_count', sprintCount.toString());
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/velocity-chart/${projectId}`, { params });
  }

  getBudgetAnalysisReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/budget-analysis`, { params });
  }

  // Dashboard y métricas
  getDashboardMetrics(projectId?: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/dashboard/metrics`, { params });
  }

  getProjectMetrics(projectId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/metrics`, { params });
  }

  getUserMetrics(userId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/users/${userId}/metrics`, { params });
  }

  // Exportación
  exportReport(reportId: string, format: 'pdf' | 'excel' | 'csv'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/reports/${reportId}/export/${format}`, {
      responseType: 'blob'
    });
  }

  exportDashboard(format: 'pdf' | 'excel', filters?: any): Observable<Blob> {
    let params = new HttpParams();
    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined) {
          params = params.set(key, filters[key]);
        }
      });
    }
    
    return this.http.get(`${environment.apiUrl}/dashboard/export/${format}`, {
      params,
      responseType: 'blob'
    });
  }

  // Programación de reportes
  scheduleReport(reportId: string, schedule: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/reports/${reportId}/schedule`, {
      schedule
    });
  }

  getScheduledReports(): Observable<Report[]> {
    return this.http.get<Report[]>(`${environment.apiUrl}/reports/scheduled`);
  }

  // Widgets de dashboard
  getDashboardWidgets(projectId?: string): Observable<any[]> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    
    return this.http.get<any[]>(`${environment.apiUrl}/dashboard/widgets`, { params });
  }

  createDashboardWidget(widgetData: any): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}/dashboard/widgets`, widgetData);
  }

  updateDashboardWidget(widgetId: string, widgetData: any): Observable<any> {
    return this.http.put<any>(`${environment.apiUrl}/dashboard/widgets/${widgetId}`, widgetData);
  }

  deleteDashboardWidget(widgetId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/dashboard/widgets/${widgetId}`);
  }

  // Utilidades
  generateQuickReport(type: string, filters?: any): Observable<ReportData> {
    return this.http.post<ReportData>(`${environment.apiUrl}/reports/quick/${type}`, filters || {});
  }

  getReportTemplates(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/reports/templates`);
  }

  createReportFromTemplate(templateId: string, config: any): Observable<Report> {
    return this.http.post<Report>(`${environment.apiUrl}/reports/from-template/${templateId}`, config);
  }
}
"""
    
    report_service_path = os.path.join(frontend_dir, "src/app/core/services/report.service.ts")
    with open(report_service_path, "w", encoding="utf-8") as f:
        f.write(report_service_content)
    
    print("✓ Componentes de reportes creados")

if __name__ == "__main__":
    create_advanced_features()
