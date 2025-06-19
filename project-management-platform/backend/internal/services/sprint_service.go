package services

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
