package handlers

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
