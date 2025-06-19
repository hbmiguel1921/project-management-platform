package services

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
