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

type NotificationHandler struct {
	notificationService *services.NotificationService
}

func NewNotificationHandler(notificationService *services.NotificationService) *NotificationHandler {
	return &NotificationHandler{
		notificationService: notificationService,
	}
}

func (h *NotificationHandler) GetNotifications(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	
	// Paginación
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	pageSize, _ := strconv.Atoi(c.DefaultQuery("page_size", "20"))
	
	if pageSize > 100 {
		pageSize = 100
	}
	
	offset := (page - 1) * pageSize

	// Filtros
	var filter models.NotificationFilter
	if isReadStr := c.Query("is_read"); isReadStr != "" {
		if isRead, err := strconv.ParseBool(isReadStr); err == nil {
			filter.IsRead = &isRead
		}
	}
	if entityType := c.Query("entity_type"); entityType != "" {
		filter.EntityType = entityType
	}

	notifications, total, err := h.notificationService.GetUserNotifications(userID, &filter, pageSize, offset)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	response := models.NewPaginationResponse(page, pageSize, total, notifications)
	utils.SuccessResponse(c, response)
}

func (h *NotificationHandler) MarkAsRead(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	notificationID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de notificación inválido")
		return
	}

	if err := h.notificationService.MarkAsRead(notificationID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Notificación marcada como leída"})
}

func (h *NotificationHandler) MarkAllAsRead(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	if err := h.notificationService.MarkAllAsRead(userID); err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Todas las notificaciones marcadas como leídas"})
}

func (h *NotificationHandler) DeleteNotification(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	notificationID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de notificación inválido")
		return
	}

	if err := h.notificationService.DeleteNotification(notificationID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Notificación eliminada"})
}

func (h *NotificationHandler) GetUnreadCount(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))

	count, err := h.notificationService.GetUnreadCount(userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, gin.H{"unread_count": count})
}
