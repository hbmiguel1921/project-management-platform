package handlers

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
