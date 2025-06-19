package models

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
