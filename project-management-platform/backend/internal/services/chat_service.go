package services

import (
	"errors"
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type ChatService struct {
	db *gorm.DB
	notificationService *NotificationService
}

func NewChatService(db *gorm.DB, notificationService *NotificationService) *ChatService {
	return &ChatService{
		db:                  db,
		notificationService: notificationService,
	}
}

func (s *ChatService) CreateChannel(userID uuid.UUID, req *models.CreateChannelRequest) (*models.ChatChannel, error) {
	channel := &models.ChatChannel{
		Name:        req.Name,
		Description: req.Description,
		Type:        req.Type,
		ProjectID:   req.ProjectID,
		IsPrivate:   req.IsPrivate,
		CreatorID:   userID,
	}

	if err := s.db.Create(channel).Error; err != nil {
		return nil, fmt.Errorf("error creando canal: %w", err)
	}

	// Agregar creador como miembro administrador
	creatorMember := &models.ChannelMember{
		ChannelID: channel.ID,
		UserID:    userID,
		Role:      "admin",
		JoinedAt:  time.Now(),
	}

	if err := s.db.Create(creatorMember).Error; err != nil {
		return nil, fmt.Errorf("error agregando creador como miembro: %w", err)
	}

	// Agregar otros miembros
	for _, memberID := range req.Members {
		if memberID != userID {
			member := &models.ChannelMember{
				ChannelID: channel.ID,
				UserID:    memberID,
				Role:      "member",
				JoinedAt:  time.Now(),
			}
			s.db.Create(member)
		}
	}

	return s.GetChannel(channel.ID, userID)
}

func (s *ChatService) GetChannels(userID uuid.UUID, projectID *uuid.UUID) ([]models.ChatChannel, error) {
	var channels []models.ChatChannel
	
	query := s.db.Joins("JOIN channel_members ON channel_members.channel_id = chat_channels.id").
		Where("channel_members.user_id = ?", userID).
		Preload("Members").
		Preload("Members.User").
		Preload("Project")

	if projectID != nil {
		query = query.Where("chat_channels.project_id = ?", *projectID)
	}

	if err := query.Find(&channels).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo canales: %w", err)
	}

	return channels, nil
}

func (s *ChatService) GetChannel(channelID, userID uuid.UUID) (*models.ChatChannel, error) {
	var channel models.ChatChannel
	
	if err := s.db.Preload("Members").
		Preload("Members.User").
		Preload("Project").
		First(&channel, channelID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo canal: %w", err)
	}

	// Verificar acceso
	if !channel.CanUserAccess(userID, models.RoleDeveloper) {
		return nil, errors.New("acceso denegado al canal")
	}

	return &channel, nil
}

func (s *ChatService) SendMessage(channelID, userID uuid.UUID, req *models.SendMessageRequest) (*models.ChatMessage, error) {
	// Verificar acceso al canal
	channel, err := s.GetChannel(channelID, userID)
	if err != nil {
		return nil, err
	}

	message := &models.ChatMessage{
		Content:   req.Content,
		ChannelID: channelID,
		UserID:    userID,
		Type:      req.Type,
		ReplyToID: req.ReplyToID,
	}

	if err := s.db.Create(message).Error; err != nil {
		return nil, fmt.Errorf("error enviando mensaje: %w", err)
	}

	// Cargar relaciones
	if err := s.db.Preload("User").
		Preload("ReplyTo").
		Preload("ReplyTo.User").
		First(message, message.ID).Error; err != nil {
		return nil, fmt.Errorf("error cargando mensaje: %w", err)
	}

	// Procesar menciones
	if err := s.processMentions(message); err != nil {
		// Log error pero no fallar
		fmt.Printf("Error procesando menciones: %v", err)
	}

	// Agregar adjuntos
	if err := s.processAttachments(message, req.Attachments); err != nil {
		// Log error pero no fallar
		fmt.Printf("Error procesando adjuntos: %v", err)
	}

	// Notificar a miembros del canal
	go s.notifyChannelMembers(channel, message)

	return message, nil
}

func (s *ChatService) GetMessages(channelID, userID uuid.UUID, limit, offset int) ([]models.ChatMessage, error) {
	// Verificar acceso al canal
	if _, err := s.GetChannel(channelID, userID); err != nil {
		return nil, err
	}

	var messages []models.ChatMessage
	
	if err := s.db.Where("channel_id = ?", channelID).
		Preload("User").
		Preload("ReplyTo").
		Preload("ReplyTo.User").
		Preload("Reactions").
		Preload("Reactions.User").
		Preload("Attachments").
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&messages).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo mensajes: %w", err)
	}

	// Invertir orden para tener mensajes más antiguos primero
	for i := len(messages)/2 - 1; i >= 0; i-- {
		opp := len(messages) - 1 - i
		messages[i], messages[opp] = messages[opp], messages[i]
	}

	return messages, nil
}

func (s *ChatService) EditMessage(messageID, userID uuid.UUID, req *models.UpdateMessageRequest) (*models.ChatMessage, error) {
	var message models.ChatMessage
	
	if err := s.db.First(&message, messageID).Error; err != nil {
		return nil, fmt.Errorf("error obteniendo mensaje: %w", err)
	}

	if !message.CanBeEditedBy(userID) {
		return nil, errors.New("no tienes permisos para editar este mensaje")
	}

	now := time.Now()
	message.Content = req.Content
	message.IsEdited = true
	message.EditedAt = &now

	if err := s.db.Save(&message).Error; err != nil {
		return nil, fmt.Errorf("error editando mensaje: %w", err)
	}

	return &message, nil
}

func (s *ChatService) DeleteMessage(messageID, userID uuid.UUID, userRole models.UserRole) error {
	var message models.ChatMessage
	
	if err := s.db.First(&message, messageID).Error; err != nil {
		return fmt.Errorf("error obteniendo mensaje: %w", err)
	}

	if !message.CanBeDeletedBy(userID, userRole) {
		return errors.New("no tienes permisos para eliminar este mensaje")
	}

	if err := s.db.Delete(&message).Error; err != nil {
		return fmt.Errorf("error eliminando mensaje: %w", err)
	}

	return nil
}

func (s *ChatService) AddReaction(messageID, userID uuid.UUID, emoji string) (*models.MessageReaction, error) {
	// Verificar si ya existe la reacción
	var existingReaction models.MessageReaction
	if err := s.db.Where("message_id = ? AND user_id = ? AND emoji = ?", 
		messageID, userID, emoji).First(&existingReaction).Error; err == nil {
		// Ya existe, eliminarla (toggle)
		s.db.Delete(&existingReaction)
		return nil, nil
	}

	reaction := &models.MessageReaction{
		MessageID: messageID,
		UserID:    userID,
		Emoji:     emoji,
	}

	if err := s.db.Create(reaction).Error; err != nil {
		return nil, fmt.Errorf("error agregando reacción: %w", err)
	}

	return reaction, nil
}

func (s *ChatService) UpdateLastRead(channelID, userID uuid.UUID) error {
	now := time.Now()
	return s.db.Model(&models.ChannelMember{}).
		Where("channel_id = ? AND user_id = ?", channelID, userID).
		Update("last_read", now).Error
}

func (s *ChatService) processMentions(message *models.ChatMessage) error {
	// TODO: Implementar extracción y procesamiento de menciones
	// Buscar patrones @username en el contenido
	// Crear registros MessageMention
	// Enviar notificaciones a usuarios mencionados
	return nil
}

func (s *ChatService) processAttachments(message *models.ChatMessage, attachments []string) error {
	for _, attachmentURL := range attachments {
		attachment := &models.MessageAttachment{
			MessageID: message.ID,
			FileURL:   attachmentURL,
			// TODO: Extraer nombre, tamaño y tipo MIME del archivo
		}
		s.db.Create(attachment)
	}
	return nil
}

func (s *ChatService) notifyChannelMembers(channel *models.ChatChannel, message *models.ChatMessage) {
	for _, member := range channel.Members {
		if member.UserID != message.UserID {
			// Crear notificación
			notification := &models.CreateNotificationRequest{
				Title:      fmt.Sprintf("Nuevo mensaje en #%s", channel.Name),
				Content:    message.Content,
				Type:       models.NotificationTypeChatMessage,
				UserIDs:    []uuid.UUID{member.UserID},
				ActionURL:  fmt.Sprintf("/chat/channels/%s", channel.ID),
				EntityType: "chat_message",
				EntityID:   &message.ID,
			}
			s.notificationService.CreateNotifications(notification)
		}
	}
}
