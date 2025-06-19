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

type ChatHandler struct {
	chatService *services.ChatService
}

func NewChatHandler(chatService *services.ChatService) *ChatHandler {
	return &ChatHandler{
		chatService: chatService,
	}
}

func (h *ChatHandler) CreateChannel(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	
	var req models.CreateChannelRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	channel, err := h.chatService.CreateChannel(userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, channel)
}

func (h *ChatHandler) GetChannels(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	
	var projectID *uuid.UUID
	if projectIDStr := c.Query("project_id"); projectIDStr != "" {
		if id, err := uuid.Parse(projectIDStr); err == nil {
			projectID = &id
		}
	}

	channels, err := h.chatService.GetChannels(userID, projectID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusInternalServerError, err.Error())
		return
	}

	utils.SuccessResponse(c, channels)
}

func (h *ChatHandler) GetChannel(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	channelID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de canal inválido")
		return
	}

	channel, err := h.chatService.GetChannel(channelID, userID)
	if err != nil {
		utils.ErrorResponse(c, http.StatusNotFound, err.Error())
		return
	}

	utils.SuccessResponse(c, channel)
}

func (h *ChatHandler) SendMessage(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	channelID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de canal inválido")
		return
	}

	var req models.SendMessageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	message, err := h.chatService.SendMessage(channelID, userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.CreatedResponse(c, message)
}

func (h *ChatHandler) GetMessages(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	channelID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de canal inválido")
		return
	}

	// Paginación
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "50"))
	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))

	if limit > 100 {
		limit = 100
	}

	messages, err := h.chatService.GetMessages(channelID, userID, limit, offset)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, gin.H{
		"messages": messages,
		"limit":    limit,
		"offset":   offset,
	})
}

func (h *ChatHandler) EditMessage(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	messageID, err := uuid.Parse(c.Param("message_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de mensaje inválido")
		return
	}

	var req models.UpdateMessageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	message, err := h.chatService.EditMessage(messageID, userID, &req)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	utils.SuccessResponse(c, message)
}

func (h *ChatHandler) DeleteMessage(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	userRole := models.UserRole(c.GetString("user_role"))
	messageID, err := uuid.Parse(c.Param("message_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de mensaje inválido")
		return
	}

	if err := h.chatService.DeleteMessage(messageID, userID, userRole); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Mensaje eliminado"})
}

func (h *ChatHandler) AddReaction(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	messageID, err := uuid.Parse(c.Param("message_id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de mensaje inválido")
		return
	}

	var req struct {
		Emoji string `json:"emoji" binding:"required"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		utils.ValidationErrorResponse(c, err.Error())
		return
	}

	reaction, err := h.chatService.AddReaction(messageID, userID, req.Emoji)
	if err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	if reaction != nil {
		utils.CreatedResponse(c, reaction)
	} else {
		c.JSON(http.StatusOK, gin.H{"message": "Reacción eliminada"})
	}
}

func (h *ChatHandler) MarkChannelAsRead(c *gin.Context) {
	userID, _ := uuid.Parse(c.GetString("user_id"))
	channelID, err := uuid.Parse(c.Param("id"))
	if err != nil {
		utils.ValidationErrorResponse(c, "ID de canal inválido")
		return
	}

	if err := h.chatService.UpdateLastRead(channelID, userID); err != nil {
		utils.ErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Canal marcado como leído"})
}
