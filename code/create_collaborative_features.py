#!/usr/bin/env python3
"""
Script para crear las funcionalidades colaborativas:
- Chat integrado con canales por proyecto
- Sistema de comentarios en tareas
- Notificaciones en tiempo real
- Menciones (@usuario) y adjuntos de archivos
- Feed de actividad y muro de proyecto
- Wiki/base de conocimientos integrada
"""

import os

def create_collaborative_features():
    """Crear funcionalidades colaborativas completas"""
    
    backend_dir = "/workspace/project-management-platform/backend"
    frontend_dir = "/workspace/project-management-platform/frontend"
    
    # Backend - Modelos colaborativos
    create_collaborative_models(backend_dir)
    
    # Backend - Servicios colaborativos
    create_collaborative_services(backend_dir)
    
    # Backend - Handlers colaborativos
    create_collaborative_handlers(backend_dir)
    
    # Frontend - Componentes de chat
    create_chat_components(frontend_dir)
    
    # Frontend - Sistema de notificaciones
    create_notification_system(frontend_dir)
    
    # Frontend - Componentes de wiki
    create_wiki_components(frontend_dir)
    
    print("✓ Funcionalidades colaborativas completadas")

def create_collaborative_models(backend_dir):
    """Crear modelos para funcionalidades colaborativas"""
    
    # internal/models/comment.go
    comment_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
)

type Comment struct {
	BaseModel
	Content    string    `json:"content" gorm:"not null"`
	TaskID     uuid.UUID `json:"task_id" gorm:"not null"`
	UserID     uuid.UUID `json:"user_id" gorm:"not null"`
	ParentID   *uuid.UUID `json:"parent_id"` // Para respuestas a comentarios
	IsEdited   bool      `json:"is_edited" gorm:"default:false"`
	EditedAt   *time.Time `json:"edited_at"`
	
	// Relaciones
	Task     *Task     `json:"task,omitempty"`
	User     *User     `json:"user,omitempty"`
	Parent   *Comment  `json:"parent,omitempty"`
	Replies  []Comment `json:"replies,omitempty" gorm:"foreignKey:ParentID"`
	
	// Menciones y adjuntos
	Mentions    []CommentMention    `json:"mentions,omitempty"`
	Attachments []CommentAttachment `json:"attachments,omitempty"`
}

type CommentMention struct {
	BaseModel
	CommentID    uuid.UUID `json:"comment_id" gorm:"not null"`
	MentionedUserID uuid.UUID `json:"mentioned_user_id" gorm:"not null"`
	Position     int       `json:"position"` // Posición en el texto
	
	// Relaciones
	Comment      *Comment `json:"comment,omitempty"`
	MentionedUser *User    `json:"mentioned_user,omitempty"`
}

type CommentAttachment struct {
	BaseModel
	CommentID uuid.UUID `json:"comment_id" gorm:"not null"`
	FileName  string    `json:"file_name" gorm:"not null"`
	FileURL   string    `json:"file_url" gorm:"not null"`
	FileSize  int64     `json:"file_size"`
	MimeType  string    `json:"mime_type"`
	
	// Relación
	Comment *Comment `json:"comment,omitempty"`
}

type CreateCommentRequest struct {
	Content     string      `json:"content" binding:"required,min=1,max=2000"`
	ParentID    *uuid.UUID  `json:"parent_id"`
	Mentions    []uuid.UUID `json:"mentions"`
	Attachments []string    `json:"attachments"` // URLs de archivos
}

type UpdateCommentRequest struct {
	Content string `json:"content" binding:"required,min=1,max=2000"`
}

func (c *Comment) CanBeEditedBy(userID uuid.UUID) bool {
	return c.UserID == userID
}

func (c *Comment) CanBeDeletedBy(userID uuid.UUID, userRole UserRole) bool {
	return c.UserID == userID || userRole == RoleAdmin || userRole == RoleManager
}

func (c *Comment) ExtractMentions(content string) []string {
	// TODO: Implementar extracción de menciones @usuario
	return []string{}
}
"""
    
    comment_model_path = os.path.join(backend_dir, "internal", "models", "comment.go")
    with open(comment_model_path, "w", encoding="utf-8") as f:
        f.write(comment_model_content)
    
    # internal/models/chat.go
    chat_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
)

type ChatChannel struct {
	BaseModel
	Name        string      `json:"name" gorm:"not null"`
	Description string      `json:"description"`
	Type        ChannelType `json:"type" gorm:"default:'project'"`
	ProjectID   *uuid.UUID  `json:"project_id"`
	IsPrivate   bool        `json:"is_private" gorm:"default:false"`
	CreatorID   uuid.UUID   `json:"creator_id" gorm:"not null"`
	
	// Relaciones
	Project  *Project         `json:"project,omitempty"`
	Creator  *User            `json:"creator,omitempty"`
	Members  []ChannelMember  `json:"members,omitempty"`
	Messages []ChatMessage    `json:"messages,omitempty"`
}

type ChannelType string

const (
	ChannelTypeProject ChannelType = "project"
	ChannelTypeGeneral ChannelType = "general"
	ChannelTypePrivate ChannelType = "private"
	ChannelTypeDirect  ChannelType = "direct"
)

type ChannelMember struct {
	BaseModel
	ChannelID uuid.UUID `json:"channel_id" gorm:"not null"`
	UserID    uuid.UUID `json:"user_id" gorm:"not null"`
	Role      string    `json:"role" gorm:"default:'member'"` // admin, member
	JoinedAt  time.Time `json:"joined_at" gorm:"default:CURRENT_TIMESTAMP"`
	LastRead  *time.Time `json:"last_read"`
	
	// Relaciones
	Channel *ChatChannel `json:"channel,omitempty"`
	User    *User        `json:"user,omitempty"`
}

type ChatMessage struct {
	BaseModel
	Content   string    `json:"content" gorm:"not null"`
	ChannelID uuid.UUID `json:"channel_id" gorm:"not null"`
	UserID    uuid.UUID `json:"user_id" gorm:"not null"`
	Type      MessageType `json:"type" gorm:"default:'text'"`
	IsEdited  bool      `json:"is_edited" gorm:"default:false"`
	EditedAt  *time.Time `json:"edited_at"`
	ReplyToID *uuid.UUID `json:"reply_to_id"`
	
	// Relaciones
	Channel     *ChatChannel       `json:"channel,omitempty"`
	User        *User              `json:"user,omitempty"`
	ReplyTo     *ChatMessage       `json:"reply_to,omitempty"`
	Replies     []ChatMessage      `json:"replies,omitempty" gorm:"foreignKey:ReplyToID"`
	Reactions   []MessageReaction  `json:"reactions,omitempty"`
	Attachments []MessageAttachment `json:"attachments,omitempty"`
	Mentions    []MessageMention   `json:"mentions,omitempty"`
}

type MessageType string

const (
	MessageTypeText         MessageType = "text"
	MessageTypeFile         MessageType = "file"
	MessageTypeImage        MessageType = "image"
	MessageTypeSystem       MessageType = "system"
	MessageTypeTaskLink     MessageType = "task_link"
	MessageTypeProjectLink  MessageType = "project_link"
)

type MessageReaction struct {
	BaseModel
	MessageID uuid.UUID `json:"message_id" gorm:"not null"`
	UserID    uuid.UUID `json:"user_id" gorm:"not null"`
	Emoji     string    `json:"emoji" gorm:"not null"`
	
	// Relaciones
	Message *ChatMessage `json:"message,omitempty"`
	User    *User        `json:"user,omitempty"`
}

type MessageAttachment struct {
	BaseModel
	MessageID uuid.UUID `json:"message_id" gorm:"not null"`
	FileName  string    `json:"file_name" gorm:"not null"`
	FileURL   string    `json:"file_url" gorm:"not null"`
	FileSize  int64     `json:"file_size"`
	MimeType  string    `json:"mime_type"`
	
	// Relación
	Message *ChatMessage `json:"message,omitempty"`
}

type MessageMention struct {
	BaseModel
	MessageID       uuid.UUID `json:"message_id" gorm:"not null"`
	MentionedUserID uuid.UUID `json:"mentioned_user_id" gorm:"not null"`
	Position        int       `json:"position"`
	
	// Relaciones
	Message       *ChatMessage `json:"message,omitempty"`
	MentionedUser *User        `json:"mentioned_user,omitempty"`
}

type CreateChannelRequest struct {
	Name        string      `json:"name" binding:"required,min=2,max=50"`
	Description string      `json:"description"`
	Type        ChannelType `json:"type"`
	ProjectID   *uuid.UUID  `json:"project_id"`
	IsPrivate   bool        `json:"is_private"`
	Members     []uuid.UUID `json:"members"`
}

type SendMessageRequest struct {
	Content     string      `json:"content" binding:"required,min=1,max=2000"`
	Type        MessageType `json:"type"`
	ReplyToID   *uuid.UUID  `json:"reply_to_id"`
	Attachments []string    `json:"attachments"`
}

type UpdateMessageRequest struct {
	Content string `json:"content" binding:"required,min=1,max=2000"`
}

func (ch *ChatChannel) CanUserAccess(userID uuid.UUID, userRole UserRole) bool {
	if userRole == RoleAdmin {
		return true
	}
	
	if !ch.IsPrivate && ch.Type == ChannelTypeGeneral {
		return true
	}
	
	// Verificar membresía
	for _, member := range ch.Members {
		if member.UserID == userID {
			return true
		}
	}
	
	return false
}

func (m *ChatMessage) CanBeEditedBy(userID uuid.UUID) bool {
	return m.UserID == userID && time.Since(m.CreatedAt) < 24*time.Hour
}

func (m *ChatMessage) CanBeDeletedBy(userID uuid.UUID, userRole UserRole) bool {
	return m.UserID == userID || userRole == RoleAdmin
}
"""
    
    chat_model_path = os.path.join(backend_dir, "internal", "models", "chat.go")
    with open(chat_model_path, "w", encoding="utf-8") as f:
        f.write(chat_model_content)
    
    # internal/models/notification.go
    notification_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
)

type Notification struct {
	BaseModel
	Title       string           `json:"title" gorm:"not null"`
	Content     string           `json:"content" gorm:"not null"`
	Type        NotificationType `json:"type" gorm:"not null"`
	UserID      uuid.UUID        `json:"user_id" gorm:"not null"`
	IsRead      bool             `json:"is_read" gorm:"default:false"`
	ReadAt      *time.Time       `json:"read_at"`
	ActionURL   string           `json:"action_url"`
	EntityType  string           `json:"entity_type"` // task, project, comment, etc.
	EntityID    *uuid.UUID       `json:"entity_id"`
	
	// Datos adicionales
	Metadata map[string]interface{} `json:"metadata" gorm:"type:jsonb"`
	
	// Relaciones
	User *User `json:"user,omitempty"`
}

type NotificationType string

const (
	NotificationTypeTaskAssigned     NotificationType = "task_assigned"
	NotificationTypeTaskUpdated      NotificationType = "task_updated"
	NotificationTypeTaskCompleted    NotificationType = "task_completed"
	NotificationTypeTaskOverdue      NotificationType = "task_overdue"
	NotificationTypeCommentAdded     NotificationType = "comment_added"
	NotificationTypeCommentMention   NotificationType = "comment_mention"
	NotificationTypeProjectInvite    NotificationType = "project_invite"
	NotificationTypeProjectUpdate    NotificationType = "project_update"
	NotificationTypeChatMention      NotificationType = "chat_mention"
	NotificationTypeChatMessage      NotificationType = "chat_message"
	NotificationTypeSprintStarted    NotificationType = "sprint_started"
	NotificationTypeSprintEnded      NotificationType = "sprint_ended"
	NotificationTypeSystemAlert      NotificationType = "system_alert"
)

type NotificationPreference struct {
	BaseModel
	UserID          uuid.UUID        `json:"user_id" gorm:"not null"`
	Type            NotificationType `json:"type" gorm:"not null"`
	InApp           bool             `json:"in_app" gorm:"default:true"`
	Email           bool             `json:"email" gorm:"default:true"`
	Push            bool             `json:"push" gorm:"default:true"`
	
	// Relación
	User *User `json:"user,omitempty"`
}

type CreateNotificationRequest struct {
	Title      string                 `json:"title" binding:"required"`
	Content    string                 `json:"content" binding:"required"`
	Type       NotificationType       `json:"type" binding:"required"`
	UserIDs    []uuid.UUID            `json:"user_ids" binding:"required"`
	ActionURL  string                 `json:"action_url"`
	EntityType string                 `json:"entity_type"`
	EntityID   *uuid.UUID             `json:"entity_id"`
	Metadata   map[string]interface{} `json:"metadata"`
}

type NotificationFilter struct {
	IsRead     *bool              `json:"is_read" form:"is_read"`
	Type       []NotificationType `json:"type" form:"type"`
	EntityType string             `json:"entity_type" form:"entity_type"`
}

func (n *Notification) MarkAsRead() {
	now := time.Now()
	n.IsRead = true
	n.ReadAt = &now
}

func (n *Notification) GetPriority() int {
	priorities := map[NotificationType]int{
		NotificationTypeSystemAlert:      1,
		NotificationTypeTaskOverdue:      2,
		NotificationTypeProjectInvite:    3,
		NotificationTypeTaskAssigned:     4,
		NotificationTypeCommentMention:   5,
		NotificationTypeChatMention:      5,
		NotificationTypeTaskCompleted:    6,
		NotificationTypeCommentAdded:     7,
		NotificationTypeTaskUpdated:      8,
		NotificationTypeProjectUpdate:    9,
		NotificationTypeChatMessage:      10,
		NotificationTypeSprintStarted:    11,
		NotificationTypeSprintEnded:      12,
	}
	
	if priority, exists := priorities[n.Type]; exists {
		return priority
	}
	return 99
}

func GetDefaultNotificationPreferences(userID uuid.UUID) []NotificationPreference {
	types := []NotificationType{
		NotificationTypeTaskAssigned,
		NotificationTypeTaskUpdated,
		NotificationTypeTaskCompleted,
		NotificationTypeTaskOverdue,
		NotificationTypeCommentAdded,
		NotificationTypeCommentMention,
		NotificationTypeProjectInvite,
		NotificationTypeProjectUpdate,
		NotificationTypeChatMention,
		NotificationTypeChatMessage,
		NotificationTypeSprintStarted,
		NotificationTypeSprintEnded,
		NotificationTypeSystemAlert,
	}
	
	preferences := make([]NotificationPreference, len(types))
	for i, notifType := range types {
		preferences[i] = NotificationPreference{
			UserID: userID,
			Type:   notifType,
			InApp:  true,
			Email:  true,
			Push:   true,
		}
	}
	
	return preferences
}
"""
    
    notification_model_path = os.path.join(backend_dir, "internal", "models", "notification.go")
    with open(notification_model_path, "w", encoding="utf-8") as f:
        f.write(notification_model_content)
    
    # internal/models/wiki.go
    wiki_model_content = """package models

import (
	"time"
	"github.com/google/uuid"
)

type WikiPage struct {
	BaseModel
	Title       string    `json:"title" gorm:"not null"`
	Slug        string    `json:"slug" gorm:"uniqueIndex;not null"`
	Content     string    `json:"content" gorm:"type:text"`
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	AuthorID    uuid.UUID `json:"author_id" gorm:"not null"`
	IsPublished bool      `json:"is_published" gorm:"default:false"`
	Version     int       `json:"version" gorm:"default:1"`
	ParentID    *uuid.UUID `json:"parent_id"` // Para jerarquía de páginas
	
	// Metadata
	Tags        []string               `json:"tags" gorm:"type:jsonb"`
	Metadata    map[string]interface{} `json:"metadata" gorm:"type:jsonb"`
	
	// Relaciones
	Project    *Project       `json:"project,omitempty"`
	Author     *User          `json:"author,omitempty"`
	Parent     *WikiPage      `json:"parent,omitempty"`
	Children   []WikiPage     `json:"children,omitempty" gorm:"foreignKey:ParentID"`
	Revisions  []WikiRevision `json:"revisions,omitempty"`
	Comments   []WikiComment  `json:"comments,omitempty"`
	
	// Timestamps adicionales
	PublishedAt *time.Time `json:"published_at"`
	LastEditedAt time.Time `json:"last_edited_at" gorm:"default:CURRENT_TIMESTAMP"`
}

type WikiRevision struct {
	BaseModel
	PageID    uuid.UUID `json:"page_id" gorm:"not null"`
	Title     string    `json:"title" gorm:"not null"`
	Content   string    `json:"content" gorm:"type:text"`
	AuthorID  uuid.UUID `json:"author_id" gorm:"not null"`
	Version   int       `json:"version" gorm:"not null"`
	Summary   string    `json:"summary"` // Resumen de cambios
	
	// Relaciones
	Page   *WikiPage `json:"page,omitempty"`
	Author *User     `json:"author,omitempty"`
}

type WikiComment struct {
	BaseModel
	Content  string    `json:"content" gorm:"not null"`
	PageID   uuid.UUID `json:"page_id" gorm:"not null"`
	UserID   uuid.UUID `json:"user_id" gorm:"not null"`
	ParentID *uuid.UUID `json:"parent_id"`
	
	// Relaciones
	Page    *WikiPage     `json:"page,omitempty"`
	User    *User         `json:"user,omitempty"`
	Parent  *WikiComment  `json:"parent,omitempty"`
	Replies []WikiComment `json:"replies,omitempty" gorm:"foreignKey:ParentID"`
}

type WikiAttachment struct {
	BaseModel
	PageID   uuid.UUID `json:"page_id" gorm:"not null"`
	FileName string    `json:"file_name" gorm:"not null"`
	FileURL  string    `json:"file_url" gorm:"not null"`
	FileSize int64     `json:"file_size"`
	MimeType string    `json:"mime_type"`
	
	// Relación
	Page *WikiPage `json:"page,omitempty"`
}

type CreateWikiPageRequest struct {
	Title       string                 `json:"title" binding:"required,min=2,max=200"`
	Content     string                 `json:"content"`
	ParentID    *uuid.UUID             `json:"parent_id"`
	IsPublished bool                   `json:"is_published"`
	Tags        []string               `json:"tags"`
	Metadata    map[string]interface{} `json:"metadata"`
}

type UpdateWikiPageRequest struct {
	Title       string                 `json:"title,omitempty" binding:"omitempty,min=2,max=200"`
	Content     string                 `json:"content,omitempty"`
	IsPublished *bool                  `json:"is_published,omitempty"`
	Tags        []string               `json:"tags,omitempty"`
	Summary     string                 `json:"summary"` // Resumen de cambios
	Metadata    map[string]interface{} `json:"metadata,omitempty"`
}

type WikiPageFilter struct {
	IsPublished *bool    `json:"is_published" form:"is_published"`
	AuthorID    *uuid.UUID `json:"author_id" form:"author_id"`
	ParentID    *uuid.UUID `json:"parent_id" form:"parent_id"`
	Search      string   `json:"search" form:"search"`
	Tags        []string `json:"tags" form:"tags"`
}

func (wp *WikiPage) GenerateSlug() string {
	// TODO: Implementar generación de slug a partir del título
	return "wiki-page-slug"
}

func (wp *WikiPage) CanBeEditedBy(userID uuid.UUID, userRole UserRole) bool {
	if userRole == RoleAdmin || userRole == RoleManager {
		return true
	}
	
	return wp.AuthorID == userID
}

func (wp *WikiPage) CanBeViewedBy(userID uuid.UUID, projectMember bool) bool {
	if wp.IsPublished {
		return projectMember
	}
	
	// Solo el autor puede ver páginas no publicadas
	return wp.AuthorID == userID
}

func (wp *WikiPage) CreateRevision(authorID uuid.UUID, summary string) *WikiRevision {
	return &WikiRevision{
		PageID:   wp.ID,
		Title:    wp.Title,
		Content:  wp.Content,
		AuthorID: authorID,
		Version:  wp.Version,
		Summary:  summary,
	}
}
"""
    
    wiki_model_path = os.path.join(backend_dir, "internal", "models", "wiki.go")
    with open(wiki_model_path, "w", encoding="utf-8") as f:
        f.write(wiki_model_content)
    
    print("✓ Modelos colaborativos creados")

def create_collaborative_services(backend_dir):
    """Crear servicios para funcionalidades colaborativas"""
    
    # internal/services/chat_service.go
    chat_service_content = """package services

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
"""
    
    chat_service_path = os.path.join(backend_dir, "internal", "services", "chat_service.go")
    with open(chat_service_path, "w", encoding="utf-8") as f:
        f.write(chat_service_content)
    
    # internal/services/notification_service.go
    notification_service_content = """package services

import (
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type NotificationService struct {
	db *gorm.DB
	wsHub *websocket.Hub // Para notificaciones en tiempo real
}

func NewNotificationService(db *gorm.DB, wsHub *websocket.Hub) *NotificationService {
	return &NotificationService{
		db:    db,
		wsHub: wsHub,
	}
}

func (s *NotificationService) CreateNotifications(req *models.CreateNotificationRequest) error {
	for _, userID := range req.UserIDs {
		notification := &models.Notification{
			Title:      req.Title,
			Content:    req.Content,
			Type:       req.Type,
			UserID:     userID,
			ActionURL:  req.ActionURL,
			EntityType: req.EntityType,
			EntityID:   req.EntityID,
			Metadata:   req.Metadata,
		}

		if err := s.db.Create(notification).Error; err != nil {
			return fmt.Errorf("error creando notificación: %w", err)
		}

		// Enviar notificación en tiempo real via WebSocket
		go s.sendRealTimeNotification(notification)

		// Enviar por email si está habilitado
		go s.sendEmailNotification(notification)
	}

	return nil
}

func (s *NotificationService) GetUserNotifications(userID uuid.UUID, filter *models.NotificationFilter, limit, offset int) ([]models.Notification, int64, error) {
	query := s.db.Where("user_id = ?", userID)

	// Aplicar filtros
	if filter != nil {
		if filter.IsRead != nil {
			query = query.Where("is_read = ?", *filter.IsRead)
		}
		if len(filter.Type) > 0 {
			query = query.Where("type IN ?", filter.Type)
		}
		if filter.EntityType != "" {
			query = query.Where("entity_type = ?", filter.EntityType)
		}
	}

	// Contar total
	var total int64
	query.Model(&models.Notification{}).Count(&total)

	// Obtener notificaciones
	var notifications []models.Notification
	if err := query.Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&notifications).Error; err != nil {
		return nil, 0, fmt.Errorf("error obteniendo notificaciones: %w", err)
	}

	return notifications, total, nil
}

func (s *NotificationService) MarkAsRead(notificationID, userID uuid.UUID) error {
	result := s.db.Model(&models.Notification{}).
		Where("id = ? AND user_id = ?", notificationID, userID).
		Updates(map[string]interface{}{
			"is_read":  true,
			"read_at":  time.Now(),
		})

	if result.Error != nil {
		return fmt.Errorf("error marcando notificación como leída: %w", result.Error)
	}

	if result.RowsAffected == 0 {
		return fmt.Errorf("notificación no encontrada")
	}

	return nil
}

func (s *NotificationService) MarkAllAsRead(userID uuid.UUID) error {
	return s.db.Model(&models.Notification{}).
		Where("user_id = ? AND is_read = ?", userID, false).
		Updates(map[string]interface{}{
			"is_read":  true,
			"read_at":  time.Now(),
		}).Error
}

func (s *NotificationService) DeleteNotification(notificationID, userID uuid.UUID) error {
	result := s.db.Where("id = ? AND user_id = ?", notificationID, userID).
		Delete(&models.Notification{})

	if result.Error != nil {
		return fmt.Errorf("error eliminando notificación: %w", result.Error)
	}

	if result.RowsAffected == 0 {
		return fmt.Errorf("notificación no encontrada")
	}

	return nil
}

func (s *NotificationService) GetUnreadCount(userID uuid.UUID) (int64, error) {
	var count int64
	err := s.db.Model(&models.Notification{}).
		Where("user_id = ? AND is_read = ?", userID, false).
		Count(&count).Error

	return count, err
}

// Métodos de conveniencia para tipos específicos de notificaciones

func (s *NotificationService) NotifyTaskAssigned(taskID, assigneeID, assignerID uuid.UUID, taskTitle string) error {
	return s.CreateNotifications(&models.CreateNotificationRequest{
		Title:      "Nueva tarea asignada",
		Content:    fmt.Sprintf("Se te ha asignado la tarea: %s", taskTitle),
		Type:       models.NotificationTypeTaskAssigned,
		UserIDs:    []uuid.UUID{assigneeID},
		ActionURL:  fmt.Sprintf("/tasks/%s", taskID),
		EntityType: "task",
		EntityID:   &taskID,
		Metadata: map[string]interface{}{
			"assigner_id": assignerID,
			"task_title":  taskTitle,
		},
	})
}

func (s *NotificationService) NotifyCommentAdded(taskID, commentID, commenterID uuid.UUID, taskTitle, commentContent string, mentionedUsers []uuid.UUID) error {
	// Notificar a usuarios mencionados
	if len(mentionedUsers) > 0 {
		s.CreateNotifications(&models.CreateNotificationRequest{
			Title:      "Te mencionaron en un comentario",
			Content:    fmt.Sprintf("Te mencionaron en la tarea: %s", taskTitle),
			Type:       models.NotificationTypeCommentMention,
			UserIDs:    mentionedUsers,
			ActionURL:  fmt.Sprintf("/tasks/%s#comment-%s", taskID, commentID),
			EntityType: "comment",
			EntityID:   &commentID,
			Metadata: map[string]interface{}{
				"task_id":         taskID,
				"commenter_id":    commenterID,
				"comment_content": commentContent,
			},
		})
	}

	// TODO: Notificar a seguidores de la tarea (implementar sistema de seguimiento)
	
	return nil
}

func (s *NotificationService) NotifyProjectInvite(projectID, invitedUserID, inviterID uuid.UUID, projectName string) error {
	return s.CreateNotifications(&models.CreateNotificationRequest{
		Title:      "Invitación a proyecto",
		Content:    fmt.Sprintf("Has sido invitado al proyecto: %s", projectName),
		Type:       models.NotificationTypeProjectInvite,
		UserIDs:    []uuid.UUID{invitedUserID},
		ActionURL:  fmt.Sprintf("/projects/%s", projectID),
		EntityType: "project",
		EntityID:   &projectID,
		Metadata: map[string]interface{}{
			"inviter_id":   inviterID,
			"project_name": projectName,
		},
	})
}

func (s *NotificationService) sendRealTimeNotification(notification *models.Notification) {
	if s.wsHub != nil {
		// Enviar notificación via WebSocket
		s.wsHub.BroadcastToUser(notification.UserID.String(), &websocket.Message{
			Type:   "notification",
			UserID: notification.UserID.String(),
			Data:   notification,
			Timestamp: time.Now().Unix(),
		})
	}
}

func (s *NotificationService) sendEmailNotification(notification *models.Notification) {
	// TODO: Implementar envío de emails
	// Verificar preferencias del usuario
	// Usar servicio de email configurado
	fmt.Printf("Sending email notification to user %s: %s\n", notification.UserID, notification.Title)
}
"""
    
    notification_service_path = os.path.join(backend_dir, "internal", "services", "notification_service.go")
    with open(notification_service_path, "w", encoding="utf-8") as f:
        f.write(notification_service_content)
    
    print("✓ Servicios colaborativos creados")

def create_collaborative_handlers(backend_dir):
    """Crear handlers para funcionalidades colaborativas"""
    
    # internal/api/handlers/chat_handler.go
    chat_handler_content = """package handlers

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
"""
    
    chat_handler_path = os.path.join(backend_dir, "internal", "api", "handlers", "chat_handler.go")
    with open(chat_handler_path, "w", encoding="utf-8") as f:
        f.write(chat_handler_content)
    
    # internal/api/handlers/notification_handler.go
    notification_handler_content = """package handlers

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
"""
    
    notification_handler_path = os.path.join(backend_dir, "internal", "api", "handlers", "notification_handler.go")
    with open(notification_handler_path, "w", encoding="utf-8") as f:
        f.write(notification_handler_content)
    
    print("✓ Handlers colaborativos creados")

def create_chat_components(frontend_dir):
    """Crear componentes de chat para el frontend"""
    
    # src/app/features/chat/chat.component.ts
    chat_component_content = """import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { DividerModule } from 'primeng/divider';
import { MenuModule } from 'primeng/menu';
import { BadgeModule } from 'primeng/badge';
import { FileUploadModule } from 'primeng/fileupload';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { Subscription } from 'rxjs';
import { ChatService, ChatChannel, ChatMessage } from '@core/services/chat.service';
import { WebSocketService } from '@core/services/websocket.service';
import { AuthService, User } from '@core/services/auth.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    CardModule,
    InputTextModule,
    ButtonModule,
    AvatarModule,
    ScrollPanelModule,
    DividerModule,
    MenuModule,
    BadgeModule,
    FileUploadModule,
    OverlayPanelModule
  ],
  template: `
    <div class="chat-container">
      <!-- Sidebar de canales -->
      <div class="chat-sidebar">
        <div class="sidebar-header">
          <h3>Canales</h3>
          <p-button 
            icon="pi pi-plus"
            severity="secondary"
            [text]="true"
            size="small"
            (onClick)="showCreateChannelDialog()"
            pTooltip="Crear canal">
          </p-button>
        </div>

        <div class="channels-list">
          <div 
            *ngFor="let channel of channels"
            class="channel-item"
            [class.active]="selectedChannel?.id === channel.id"
            (click)="selectChannel(channel)">
            
            <div class="channel-info">
              <i class="pi pi-hashtag channel-icon"></i>
              <span class="channel-name">{{ channel.name }}</span>
            </div>
            
            <p-badge 
              *ngIf="getUnreadCount(channel.id) > 0"
              [value]="getUnreadCount(channel.id)"
              severity="danger">
            </p-badge>
          </div>
        </div>

        <!-- Mensajes directos -->
        <div class="direct-messages">
          <h4>Mensajes Directos</h4>
          <!-- Lista de conversaciones directas -->
        </div>
      </div>

      <!-- Área principal del chat -->
      <div class="chat-main" *ngIf="selectedChannel">
        <!-- Header del canal -->
        <div class="chat-header">
          <div class="channel-info">
            <h3># {{ selectedChannel.name }}</h3>
            <p *ngIf="selectedChannel.description">{{ selectedChannel.description }}</p>
          </div>
          
          <div class="channel-actions">
            <p-button 
              icon="pi pi-users"
              severity="secondary"
              [text]="true"
              (onClick)="showChannelMembers()"
              pTooltip="Miembros del canal">
            </p-button>
            <p-button 
              icon="pi pi-cog"
              severity="secondary"
              [text]="true"
              (onClick)="showChannelSettings()"
              pTooltip="Configuración">
            </p-button>
          </div>
        </div>

        <!-- Mensajes -->
        <div class="messages-container" #messagesContainer>
          <div 
            *ngFor="let message of messages; trackBy: trackByMessage"
            class="message-group"
            [class.own-message]="message.user_id === currentUser?.id">
            
            <div class="message-avatar" *ngIf="!isConsecutiveMessage(message)">
              <p-avatar 
                [image]="message.user?.avatar"
                [label]="getUserInitials(message.user)"
                size="normal"
                shape="circle">
              </p-avatar>
            </div>

            <div class="message-content">
              <div class="message-header" *ngIf="!isConsecutiveMessage(message)">
                <span class="message-author">{{ message.user?.first_name }} {{ message.user?.last_name }}</span>
                <span class="message-time">{{ message.created_at | date:'dd/MM HH:mm' }}</span>
              </div>

              <div class="message-body">
                <div class="message-text" [innerHTML]="formatMessageContent(message.content)"></div>
                
                <!-- Adjuntos -->
                <div class="message-attachments" *ngIf="message.attachments && message.attachments.length > 0">
                  <div 
                    *ngFor="let attachment of message.attachments"
                    class="attachment">
                    <!-- Renderizar según tipo de archivo -->
                  </div>
                </div>

                <!-- Respuesta a mensaje -->
                <div class="message-reply" *ngIf="message.reply_to">
                  <div class="reply-content">
                    <small>{{ message.reply_to.user?.first_name }}: {{ message.reply_to.content | slice:0:50 }}...</small>
                  </div>
                </div>
              </div>

              <!-- Reacciones -->
              <div class="message-reactions" *ngIf="message.reactions && message.reactions.length > 0">
                <span 
                  *ngFor="let reaction of getGroupedReactions(message.reactions)"
                  class="reaction"
                  [class.user-reacted]="hasUserReacted(reaction, currentUser?.id)"
                  (click)="toggleReaction(message.id, reaction.emoji)">
                  {{ reaction.emoji }} {{ reaction.count }}
                </span>
              </div>

              <!-- Acciones del mensaje -->
              <div class="message-actions">
                <p-button 
                  icon="pi pi-smile"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="showEmojiPicker(message)"
                  pTooltip="Reaccionar">
                </p-button>
                <p-button 
                  icon="pi pi-reply"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="replyToMessage(message)"
                  pTooltip="Responder">
                </p-button>
                <p-button 
                  *ngIf="message.user_id === currentUser?.id"
                  icon="pi pi-pencil"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="editMessage(message)"
                  pTooltip="Editar">
                </p-button>
              </div>
            </div>
          </div>

          <!-- Indicador de usuario escribiendo -->
          <div class="typing-indicator" *ngIf="typingUsers.length > 0">
            <span>{{ getTypingText() }}</span>
          </div>
        </div>

        <!-- Input de mensaje -->
        <div class="message-input-container">
          <!-- Respuesta a mensaje -->
          <div class="reply-preview" *ngIf="replyingTo">
            <div class="reply-info">
              <small>Respondiendo a {{ replyingTo.user?.first_name }}</small>
              <p>{{ replyingTo.content | slice:0:100 }}</p>
            </div>
            <p-button 
              icon="pi pi-times"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="cancelReply()">
            </p-button>
          </div>

          <div class="input-area">
            <div class="input-actions">
              <p-button 
                icon="pi pi-paperclip"
                severity="secondary"
                [text]="true"
                (onClick)="showFileUpload()"
                pTooltip="Adjuntar archivo">
              </p-button>
            </div>

            <input 
              type="text"
              placeholder="Escribe un mensaje..."
              [(ngModel)]="newMessage"
              (keyup.enter)="sendMessage()"
              (keyup)="onTyping()"
              class="message-input"
              #messageInput>

            <p-button 
              icon="pi pi-send"
              [disabled]="!newMessage.trim()"
              (onClick)="sendMessage()">
            </p-button>
          </div>
        </div>
      </div>

      <!-- Panel vacío cuando no hay canal seleccionado -->
      <div class="chat-empty" *ngIf="!selectedChannel">
        <div class="empty-content">
          <i class="pi pi-comments empty-icon"></i>
          <h3>Selecciona un canal</h3>
          <p>Elige un canal de la lista para comenzar a chatear</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chat-container {
      display: flex;
      height: calc(100vh - 120px);
      background: white;
      border-radius: 8px;
      overflow: hidden;
    }

    /* Sidebar */
    .chat-sidebar {
      width: 300px;
      background: #f8f9fa;
      border-right: 1px solid #e0e0e0;
      display: flex;
      flex-direction: column;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
    }

    .sidebar-header h3 {
      margin: 0;
      color: #333;
    }

    .channels-list {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem 0;
    }

    .channel-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .channel-item:hover {
      background: #e9ecef;
    }

    .channel-item.active {
      background: #007bff;
      color: white;
    }

    .channel-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .channel-icon {
      color: #6c757d;
    }

    .channel-item.active .channel-icon {
      color: white;
    }

    .channel-name {
      font-weight: 500;
    }

    .direct-messages {
      border-top: 1px solid #e0e0e0;
      padding: 1rem;
    }

    .direct-messages h4 {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Chat principal */
    .chat-main {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #e0e0e0;
      background: white;
    }

    .chat-header h3 {
      margin: 0;
      color: #333;
    }

    .chat-header p {
      margin: 0.25rem 0 0 0;
      color: #666;
      font-size: 0.9rem;
    }

    .channel-actions {
      display: flex;
      gap: 0.5rem;
    }

    /* Mensajes */
    .messages-container {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .message-group {
      display: flex;
      gap: 0.75rem;
      padding: 0.25rem 0;
    }

    .message-group.own-message {
      flex-direction: row-reverse;
    }

    .message-avatar {
      flex-shrink: 0;
      width: 40px;
    }

    .message-content {
      flex: 1;
      min-width: 0;
    }

    .message-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.25rem;
    }

    .message-author {
      font-weight: 600;
      color: #333;
    }

    .message-time {
      font-size: 0.8rem;
      color: #999;
    }

    .message-body {
      background: #f8f9fa;
      padding: 0.75rem;
      border-radius: 8px;
      position: relative;
    }

    .own-message .message-body {
      background: #007bff;
      color: white;
    }

    .message-text {
      line-height: 1.4;
      word-wrap: break-word;
    }

    .message-reply {
      margin-top: 0.5rem;
      padding: 0.5rem;
      background: rgba(0,0,0,0.1);
      border-radius: 4px;
      border-left: 3px solid #007bff;
    }

    .message-reactions {
      display: flex;
      gap: 0.25rem;
      margin-top: 0.5rem;
    }

    .reaction {
      background: #e9ecef;
      border: 1px solid #dee2e6;
      border-radius: 12px;
      padding: 0.2rem 0.4rem;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .reaction:hover {
      background: #dee2e6;
    }

    .reaction.user-reacted {
      background: #007bff;
      color: white;
      border-color: #007bff;
    }

    .message-actions {
      display: flex;
      gap: 0.25rem;
      margin-top: 0.5rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .message-group:hover .message-actions {
      opacity: 1;
    }

    .typing-indicator {
      padding: 0.5rem 1rem;
      font-style: italic;
      color: #666;
      font-size: 0.9rem;
    }

    /* Input de mensaje */
    .message-input-container {
      border-top: 1px solid #e0e0e0;
      background: white;
    }

    .reply-preview {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      background: #f8f9fa;
      border-bottom: 1px solid #e0e0e0;
    }

    .reply-info small {
      display: block;
      color: #007bff;
      font-weight: 500;
    }

    .reply-info p {
      margin: 0.25rem 0 0 0;
      color: #666;
    }

    .input-area {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 1rem;
    }

    .input-actions {
      display: flex;
      gap: 0.25rem;
    }

    .message-input {
      flex: 1;
      border: 1px solid #e0e0e0;
      border-radius: 20px;
      padding: 0.75rem 1rem;
      outline: none;
      font-size: 0.95rem;
    }

    .message-input:focus {
      border-color: #007bff;
    }

    /* Estado vacío */
    .chat-empty {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .empty-content {
      text-align: center;
      color: #666;
    }

    .empty-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      opacity: 0.3;
    }

    .empty-content h3 {
      margin: 0 0 0.5rem 0;
    }

    .empty-content p {
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .chat-sidebar {
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        z-index: 1000;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
      }

      .chat-sidebar.mobile-open {
        transform: translateX(0);
      }

      .chat-main {
        width: 100%;
      }
    }
  `]
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('messageInput') messageInput!: ElementRef;

  channels: ChatChannel[] = [];
  selectedChannel: ChatChannel | null = null;
  messages: ChatMessage[] = [];
  newMessage = '';
  replyingTo: ChatMessage | null = null;
  currentUser: User | null = null;
  typingUsers: string[] = [];

  private subscriptions: Subscription[] = [];

  constructor(
    private chatService: ChatService,
    private wsService: WebSocketService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadCurrentUser();
    this.loadChannels();
    this.subscribeToMessages();
    this.subscribeToTyping();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadCurrentUser(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  private loadChannels(): void {
    this.chatService.getChannels().subscribe(
      channels => {
        this.channels = channels;
        if (channels.length > 0 && !this.selectedChannel) {
          this.selectChannel(channels[0]);
        }
      }
    );
  }

  private subscribeToMessages(): void {
    const messagesSub = this.wsService.onChatMessage().subscribe(
      (data: any) => {
        if (data.channel_id === this.selectedChannel?.id) {
          this.messages.push(data.message);
          this.scrollToBottom();
        }
      }
    );
    this.subscriptions.push(messagesSub);
  }

  private subscribeToTyping(): void {
    // Implementar indicador de escritura
  }

  selectChannel(channel: ChatChannel): void {
    this.selectedChannel = channel;
    this.loadMessages();
    this.wsService.subscribeToProject(channel.project_id || '');
  }

  private loadMessages(): void {
    if (!this.selectedChannel) return;

    this.chatService.getMessages(this.selectedChannel.id).subscribe(
      messages => {
        this.messages = messages;
        setTimeout(() => this.scrollToBottom(), 100);
      }
    );
  }

  sendMessage(): void {
    if (!this.newMessage.trim() || !this.selectedChannel) return;

    const messageData = {
      content: this.newMessage,
      reply_to_id: this.replyingTo?.id
    };

    this.chatService.sendMessage(this.selectedChannel.id, messageData).subscribe(
      message => {
        this.messages.push(message);
        this.newMessage = '';
        this.replyingTo = null;
        this.scrollToBottom();
      }
    );
  }

  onTyping(): void {
    // Implementar indicador de escritura
    this.wsService.emit('typing', {
      channel_id: this.selectedChannel?.id,
      user_id: this.currentUser?.id
    });
  }

  replyToMessage(message: ChatMessage): void {
    this.replyingTo = message;
    this.messageInput.nativeElement.focus();
  }

  cancelReply(): void {
    this.replyingTo = null;
  }

  editMessage(message: ChatMessage): void {
    // Implementar edición de mensajes
  }

  toggleReaction(messageId: string, emoji: string): void {
    this.chatService.addReaction(messageId, emoji).subscribe();
  }

  showEmojiPicker(message: ChatMessage): void {
    // Implementar selector de emojis
  }

  showFileUpload(): void {
    // Implementar carga de archivos
  }

  showCreateChannelDialog(): void {
    // Implementar creación de canales
  }

  showChannelMembers(): void {
    // Mostrar miembros del canal
  }

  showChannelSettings(): void {
    // Mostrar configuración del canal
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const container = this.messagesContainer?.nativeElement;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }, 50);
  }

  formatMessageContent(content: string): string {
    // Implementar formateo de mensajes (markdown, menciones, enlaces)
    return content.replace(/\n/g, '<br>');
  }

  getUserInitials(user: any): string {
    if (!user) return '';
    return (user.first_name?.[0] || '') + (user.last_name?.[0] || '');
  }

  isConsecutiveMessage(message: ChatMessage): boolean {
    const index = this.messages.indexOf(message);
    if (index === 0) return false;
    
    const prevMessage = this.messages[index - 1];
    return prevMessage.user_id === message.user_id &&
           (new Date(message.created_at).getTime() - new Date(prevMessage.created_at).getTime()) < 300000; // 5 minutos
  }

  getGroupedReactions(reactions: any[]): any[] {
    const grouped: {[emoji: string]: any} = {};
    
    reactions.forEach(reaction => {
      if (!grouped[reaction.emoji]) {
        grouped[reaction.emoji] = {
          emoji: reaction.emoji,
          count: 0,
          users: []
        };
      }
      grouped[reaction.emoji].count++;
      grouped[reaction.emoji].users.push(reaction.user);
    });
    
    return Object.values(grouped);
  }

  hasUserReacted(reaction: any, userId?: string): boolean {
    return reaction.users.some((user: any) => user.id === userId);
  }

  getUnreadCount(channelId: string): number {
    // Implementar conteo de mensajes no leídos
    return 0;
  }

  getTypingText(): string {
    if (this.typingUsers.length === 1) {
      return `${this.typingUsers[0]} está escribiendo...`;
    } else if (this.typingUsers.length === 2) {
      return `${this.typingUsers[0]} y ${this.typingUsers[1]} están escribiendo...`;
    } else if (this.typingUsers.length > 2) {
      return `${this.typingUsers.length} personas están escribiendo...`;
    }
    return '';
  }

  trackByMessage(index: number, message: ChatMessage): string {
    return message.id;
  }
}
"""
    
    chat_component_path = os.path.join(frontend_dir, "src/app/features/chat/chat.component.ts")
    os.makedirs(os.path.dirname(chat_component_path), exist_ok=True)
    with open(chat_component_path, "w", encoding="utf-8") as f:
        f.write(chat_component_content)
    
    # src/app/core/services/chat.service.ts
    chat_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface ChatChannel {
  id: string;
  name: string;
  description?: string;
  type: 'project' | 'general' | 'private' | 'direct';
  project_id?: string;
  is_private: boolean;
  creator_id: string;
  created_at: string;
  updated_at: string;
  members?: ChannelMember[];
  project?: any;
}

export interface ChannelMember {
  id: string;
  channel_id: string;
  user_id: string;
  role: 'admin' | 'member';
  joined_at: string;
  last_read?: string;
  user?: any;
}

export interface ChatMessage {
  id: string;
  content: string;
  channel_id: string;
  user_id: string;
  type: 'text' | 'file' | 'image' | 'system' | 'task_link' | 'project_link';
  is_edited: boolean;
  edited_at?: string;
  reply_to_id?: string;
  created_at: string;
  updated_at: string;
  user?: any;
  reply_to?: ChatMessage;
  reactions?: MessageReaction[];
  attachments?: MessageAttachment[];
}

export interface MessageReaction {
  id: string;
  message_id: string;
  user_id: string;
  emoji: string;
  created_at: string;
  user?: any;
}

export interface MessageAttachment {
  id: string;
  message_id: string;
  file_name: string;
  file_url: string;
  file_size: number;
  mime_type: string;
}

export interface CreateChannelRequest {
  name: string;
  description?: string;
  type: 'project' | 'general' | 'private' | 'direct';
  project_id?: string;
  is_private: boolean;
  members: string[];
}

export interface SendMessageRequest {
  content: string;
  type?: string;
  reply_to_id?: string;
  attachments?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(private http: HttpClient) { }

  getChannels(projectId?: string): Observable<ChatChannel[]> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<ChatChannel[]>(`${environment.apiUrl}/chat/channels`, { params });
  }

  getChannel(channelId: string): Observable<ChatChannel> {
    return this.http.get<ChatChannel>(`${environment.apiUrl}/chat/channels/${channelId}`);
  }

  createChannel(channelData: CreateChannelRequest): Observable<ChatChannel> {
    return this.http.post<ChatChannel>(`${environment.apiUrl}/chat/channels`, channelData);
  }

  getMessages(channelId: string, limit = 50, offset = 0): Observable<ChatMessage[]> {
    const params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    
    return this.http.get<ChatMessage[]>(`${environment.apiUrl}/chat/channels/${channelId}/messages`, { params });
  }

  sendMessage(channelId: string, messageData: SendMessageRequest): Observable<ChatMessage> {
    return this.http.post<ChatMessage>(`${environment.apiUrl}/chat/channels/${channelId}/messages`, messageData);
  }

  editMessage(channelId: string, messageId: string, content: string): Observable<ChatMessage> {
    return this.http.put<ChatMessage>(`${environment.apiUrl}/chat/channels/${channelId}/messages/${messageId}`, {
      content
    });
  }

  deleteMessage(channelId: string, messageId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/chat/channels/${channelId}/messages/${messageId}`);
  }

  addReaction(messageId: string, emoji: string): Observable<MessageReaction | null> {
    return this.http.post<MessageReaction | null>(`${environment.apiUrl}/chat/messages/${messageId}/reactions`, {
      emoji
    });
  }

  markChannelAsRead(channelId: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/chat/channels/${channelId}/read`, {});
  }

  addMemberToChannel(channelId: string, userId: string): Observable<ChannelMember> {
    return this.http.post<ChannelMember>(`${environment.apiUrl}/chat/channels/${channelId}/members`, {
      user_id: userId
    });
  }

  removeMemberFromChannel(channelId: string, userId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/chat/channels/${channelId}/members/${userId}`);
  }

  uploadFile(file: File): Observable<{file_url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{file_url: string}>(`${environment.apiUrl}/chat/upload`, formData);
  }

  searchMessages(query: string, channelId?: string): Observable<ChatMessage[]> {
    let params = new HttpParams().set('q', query);
    if (channelId) {
      params = params.set('channel_id', channelId);
    }
    
    return this.http.get<ChatMessage[]>(`${environment.apiUrl}/chat/search`, { params });
  }
}
"""
    
    chat_service_path = os.path.join(frontend_dir, "src/app/core/services/chat.service.ts")
    with open(chat_service_path, "w", encoding="utf-8") as f:
        f.write(chat_service_content)
    
    print("✓ Componentes de chat creados")

def create_notification_system(frontend_dir):
    """Crear sistema de notificaciones para el frontend"""
    
    # src/app/shared/components/notifications/notifications.component.ts
    notifications_component_content = """import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { BadgeModule } from 'primeng/badge';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { DividerModule } from 'primeng/divider';
import { AvatarModule } from 'primeng/avatar';
import { Subscription } from 'rxjs';
import { NotificationService, Notification } from '@core/services/notification.service';
import { WebSocketService } from '@core/services/websocket.service';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ButtonModule,
    BadgeModule,
    OverlayPanelModule,
    DividerModule,
    AvatarModule
  ],
  template: `
    <div class="notifications-container">
      <p-button 
        icon="pi pi-bell"
        severity="secondary"
        [text]="true"
        [badge]="unreadCount > 0 ? unreadCount.toString() : null"
        badgeClass="p-badge-danger"
        (onClick)="togglePanel($event)"
        class="notification-trigger">
      </p-button>

      <p-overlayPanel 
        #notificationPanel 
        [style]="{width: '400px', maxHeight: '500px'}"
        [showCloseIcon]="true">
        
        <div class="notifications-panel">
          <div class="panel-header">
            <h3>Notificaciones</h3>
            <div class="header-actions">
              <p-button 
                label="Marcar todas como leídas"
                size="small"
                [text]="true"
                [disabled]="unreadCount === 0"
                (onClick)="markAllAsRead()">
              </p-button>
            </div>
          </div>

          <div class="notifications-list" *ngIf="notifications.length > 0; else noNotifications">
            <div 
              *ngFor="let notification of notifications; trackBy: trackByNotification"
              class="notification-item"
              [class.unread]="!notification.is_read"
              (click)="handleNotificationClick(notification)">
              
              <div class="notification-icon">
                <i [class]="getNotificationIcon(notification.type)" 
                   [style.color]="getNotificationColor(notification.type)"></i>
              </div>

              <div class="notification-content">
                <h4 class="notification-title">{{ notification.title }}</h4>
                <p class="notification-message">{{ notification.content }}</p>
                <div class="notification-meta">
                  <span class="notification-time">{{ getRelativeTime(notification.created_at) }}</span>
                  <span class="notification-type">{{ getTypeLabel(notification.type) }}</span>
                </div>
              </div>

              <div class="notification-actions">
                <p-button 
                  *ngIf="!notification.is_read"
                  icon="pi pi-check"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="markAsRead($event, notification)"
                  pTooltip="Marcar como leída">
                </p-button>
                <p-button 
                  icon="pi pi-times"
                  severity="danger"
                  [text]="true"
                  size="small"
                  (onClick)="deleteNotification($event, notification)"
                  pTooltip="Eliminar">
                </p-button>
              </div>
            </div>
          </div>

          <ng-template #noNotifications>
            <div class="empty-notifications">
              <i class="pi pi-bell empty-icon"></i>
              <h4>No hay notificaciones</h4>
              <p>Todas las notificaciones aparecerán aquí</p>
            </div>
          </ng-template>

          <div class="panel-footer" *ngIf="notifications.length > 0">
            <p-button 
              label="Ver todas las notificaciones"
              [text]="true"
              routerLink="/notifications"
              (onClick)="closePanel()">
            </p-button>
          </div>
        </div>
      </p-overlayPanel>
    </div>
  `,
  styles: [`
    .notification-trigger {
      position: relative;
    }

    .notifications-panel {
      padding: 0;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .panel-header h3 {
      margin: 0;
      color: #333;
      font-size: 1.1rem;
    }

    .notifications-list {
      max-height: 350px;
      overflow-y: auto;
    }

    .notification-item {
      display: flex;
      gap: 0.75rem;
      padding: 1rem;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .notification-item:hover {
      background: #f8f9fa;
    }

    .notification-item.unread {
      background: #f0f8ff;
      border-left: 3px solid #007bff;
    }

    .notification-icon {
      flex-shrink: 0;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f9fa;
      border-radius: 50%;
      font-size: 1.2rem;
    }

    .notification-content {
      flex: 1;
      min-width: 0;
    }

    .notification-title {
      margin: 0 0 0.25rem 0;
      font-size: 0.9rem;
      font-weight: 600;
      color: #333;
      line-height: 1.3;
    }

    .notification-message {
      margin: 0 0 0.5rem 0;
      font-size: 0.85rem;
      color: #666;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .notification-meta {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }

    .notification-time {
      font-size: 0.75rem;
      color: #999;
    }

    .notification-type {
      font-size: 0.7rem;
      background: #e9ecef;
      color: #495057;
      padding: 0.1rem 0.4rem;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .notification-actions {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .notification-item:hover .notification-actions {
      opacity: 1;
    }

    .empty-notifications {
      text-align: center;
      padding: 3rem 1rem;
      color: #666;
    }

    .empty-icon {
      font-size: 2.5rem;
      color: #ccc;
      margin-bottom: 1rem;
    }

    .empty-notifications h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }

    .empty-notifications p {
      margin: 0;
      font-size: 0.9rem;
    }

    .panel-footer {
      padding: 1rem;
      border-top: 1px solid #e0e0e0;
      text-align: center;
    }

    /* Badge personalizado */
    ::ng-deep .p-badge {
      min-width: 1.2rem;
      height: 1.2rem;
      line-height: 1.2rem;
      font-size: 0.7rem;
    }
  `]
})
export class NotificationsComponent implements OnInit, OnDestroy {
  notifications: Notification[] = [];
  unreadCount = 0;
  
  private subscriptions: Subscription[] = [];

  constructor(
    private notificationService: NotificationService,
    private wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.loadNotifications();
    this.subscribeToRealTimeNotifications();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadNotifications(): void {
    this.notificationService.getNotifications(1, 10).subscribe(
      response => {
        this.notifications = response.data;
        this.updateUnreadCount();
      }
    );
  }

  private subscribeToRealTimeNotifications(): void {
    const notificationSub = this.wsService.onNotification().subscribe(
      (notification: Notification) => {
        this.notifications.unshift(notification);
        this.updateUnreadCount();
        this.showToast(notification);
      }
    );
    this.subscriptions.push(notificationSub);
  }

  private updateUnreadCount(): void {
    this.unreadCount = this.notifications.filter(n => !n.is_read).length;
  }

  private showToast(notification: Notification): void {
    // Integrar con servicio de toast/mensajes
    console.log('Nueva notificación:', notification.title);
  }

  togglePanel(event: Event): void {
    // El panel se maneja automáticamente por PrimeNG
  }

  closePanel(): void {
    // Cerrar panel si es necesario
  }

  handleNotificationClick(notification: Notification): void {
    if (!notification.is_read) {
      this.markAsRead(null, notification);
    }

    if (notification.action_url) {
      // Navegar a la URL de acción
      // this.router.navigate([notification.action_url]);
    }
  }

  markAsRead(event: Event | null, notification: Notification): void {
    if (event) {
      event.stopPropagation();
    }

    this.notificationService.markAsRead(notification.id).subscribe(
      () => {
        notification.is_read = true;
        notification.read_at = new Date().toISOString();
        this.updateUnreadCount();
      }
    );
  }

  markAllAsRead(): void {
    this.notificationService.markAllAsRead().subscribe(
      () => {
        this.notifications.forEach(n => {
          n.is_read = true;
          n.read_at = new Date().toISOString();
        });
        this.updateUnreadCount();
      }
    );
  }

  deleteNotification(event: Event, notification: Notification): void {
    event.stopPropagation();

    this.notificationService.deleteNotification(notification.id).subscribe(
      () => {
        const index = this.notifications.indexOf(notification);
        if (index > -1) {
          this.notifications.splice(index, 1);
          this.updateUnreadCount();
        }
      }
    );
  }

  getNotificationIcon(type: string): string {
    const icons = {
      'task_assigned': 'pi pi-user',
      'task_updated': 'pi pi-refresh',
      'task_completed': 'pi pi-check-circle',
      'task_overdue': 'pi pi-clock',
      'comment_added': 'pi pi-comment',
      'comment_mention': 'pi pi-at',
      'project_invite': 'pi pi-users',
      'project_update': 'pi pi-folder',
      'chat_mention': 'pi pi-comments',
      'chat_message': 'pi pi-comment',
      'sprint_started': 'pi pi-play',
      'sprint_ended': 'pi pi-stop',
      'system_alert': 'pi pi-exclamation-triangle'
    };
    return icons[type as keyof typeof icons] || 'pi pi-bell';
  }

  getNotificationColor(type: string): string {
    const colors = {
      'task_assigned': '#007bff',
      'task_updated': '#6f42c1',
      'task_completed': '#28a745',
      'task_overdue': '#dc3545',
      'comment_added': '#17a2b8',
      'comment_mention': '#fd7e14',
      'project_invite': '#007bff',
      'project_update': '#6c757d',
      'chat_mention': '#fd7e14',
      'chat_message': '#17a2b8',
      'sprint_started': '#28a745',
      'sprint_ended': '#6c757d',
      'system_alert': '#dc3545'
    };
    return colors[type as keyof typeof colors] || '#6c757d';
  }

  getTypeLabel(type: string): string {
    const labels = {
      'task_assigned': 'Tarea',
      'task_updated': 'Tarea',
      'task_completed': 'Tarea',
      'task_overdue': 'Tarea',
      'comment_added': 'Comentario',
      'comment_mention': 'Mención',
      'project_invite': 'Proyecto',
      'project_update': 'Proyecto',
      'chat_mention': 'Chat',
      'chat_message': 'Chat',
      'sprint_started': 'Sprint',
      'sprint_ended': 'Sprint',
      'system_alert': 'Sistema'
    };
    return labels[type as keyof typeof labels] || 'General';
  }

  getRelativeTime(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Ahora';
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}d`;
    
    return date.toLocaleDateString();
  }

  trackByNotification(index: number, notification: Notification): string {
    return notification.id;
  }
}
"""
    
    notifications_component_path = os.path.join(frontend_dir, "src/app/shared/components/notifications/notifications.component.ts")
    os.makedirs(os.path.dirname(notifications_component_path), exist_ok=True)
    with open(notifications_component_path, "w", encoding="utf-8") as f:
        f.write(notifications_component_content)
    
    # src/app/core/services/notification.service.ts  
    notification_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '@environments/environment';

export interface Notification {
  id: string;
  title: string;
  content: string;
  type: string;
  user_id: string;
  is_read: boolean;
  read_at?: string;
  action_url?: string;
  entity_type?: string;
  entity_id?: string;
  metadata?: {[key: string]: any};
  created_at: string;
  updated_at: string;
}

export interface NotificationFilter {
  is_read?: boolean;
  type?: string[];
  entity_type?: string;
}

export interface NotificationResponse {
  data: Notification[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private unreadCountSubject = new BehaviorSubject<number>(0);
  public unreadCount$ = this.unreadCountSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadUnreadCount();
  }

  getNotifications(page = 1, pageSize = 20, filter?: NotificationFilter): Observable<NotificationResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (filter) {
      if (filter.is_read !== undefined) {
        params = params.set('is_read', filter.is_read.toString());
      }
      if (filter.entity_type) {
        params = params.set('entity_type', filter.entity_type);
      }
      if (filter.type && filter.type.length > 0) {
        filter.type.forEach(type => {
          params = params.append('type', type);
        });
      }
    }

    return this.http.get<NotificationResponse>(`${environment.apiUrl}/notifications`, { params });
  }

  markAsRead(notificationId: string): Observable<void> {
    return this.http.put<void>(`${environment.apiUrl}/notifications/${notificationId}/read`, {})
      .pipe(
        tap(() => this.decrementUnreadCount())
      );
  }

  markAllAsRead(): Observable<void> {
    return this.http.put<void>(`${environment.apiUrl}/notifications/read-all`, {})
      .pipe(
        tap(() => this.unreadCountSubject.next(0))
      );
  }

  deleteNotification(notificationId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/notifications/${notificationId}`)
      .pipe(
        tap(() => this.decrementUnreadCount())
      );
  }

  getUnreadCount(): Observable<{unread_count: number}> {
    return this.http.get<{unread_count: number}>(`${environment.apiUrl}/notifications/unread-count`)
      .pipe(
        tap(response => this.unreadCountSubject.next(response.unread_count))
      );
  }

  private loadUnreadCount(): void {
    this.getUnreadCount().subscribe();
  }

  private decrementUnreadCount(): void {
    const current = this.unreadCountSubject.value;
    if (current > 0) {
      this.unreadCountSubject.next(current - 1);
    }
  }

  // Métodos para crear notificaciones locales (para testing o casos especiales)
  createLocalNotification(notification: Partial<Notification>): void {
    // Simular notificación local
    const newNotification: Notification = {
      id: Date.now().toString(),
      title: notification.title || '',
      content: notification.content || '',
      type: notification.type || 'general',
      user_id: '',
      is_read: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ...notification
    };

    // Incrementar contador
    this.unreadCountSubject.next(this.unreadCountSubject.value + 1);
  }

  // Configuración de preferencias de notificación
  getNotificationPreferences(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/notifications/preferences`);
  }

  updateNotificationPreferences(preferences: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/notifications/preferences`, preferences);
  }

  // Utilidades para mostrar notificaciones nativas del navegador
  requestNotificationPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      console.warn('Este navegador no soporta notificaciones');
      return Promise.resolve('denied');
    }

    return Notification.requestPermission();
  }

  showBrowserNotification(title: string, options?: NotificationOptions): void {
    if (Notification.permission === 'granted') {
      new Notification(title, {
        icon: '/assets/icons/notification-icon.png',
        badge: '/assets/icons/badge-icon.png',
        ...options
      });
    }
  }

  // Procesamiento de notificaciones en tiempo real
  processRealTimeNotification(notification: Notification): void {
    // Incrementar contador de no leídas
    this.unreadCountSubject.next(this.unreadCountSubject.value + 1);

    // Mostrar notificación nativa si está permitido
    if (Notification.permission === 'granted') {
      this.showBrowserNotification(notification.title, {
        body: notification.content,
        tag: notification.id,
        data: notification
      });
    }
  }
}
"""
    
    notification_service_path = os.path.join(frontend_dir, "src/app/core/services/notification.service.ts")
    with open(notification_service_path, "w", encoding="utf-8") as f:
        f.write(notification_service_content)
    
    print("✓ Sistema de notificaciones creado")

def create_wiki_components(frontend_dir):
    """Crear componentes de wiki para el frontend"""
    
    # src/app/features/wiki/wiki.component.ts (página principal de wiki)
    wiki_component_content = """import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TreeModule } from 'primeng/tree';
import { TagModule } from 'primeng/tag';
import { MenuModule } from 'primeng/menu';
import { BreadcrumbModule } from 'primeng/breadcrumb';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { WikiService, WikiPage } from '@core/services/wiki.service';

@Component({
  selector: 'app-wiki',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    TreeModule,
    TagModule,
    MenuModule,
    BreadcrumbModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Base de Conocimientos"
      description="Documentación y recursos del proyecto"
      titleIcon="pi pi-book"
      [actions]="headerActions">
    </app-page-header>

    <div class="wiki-container">
      <!-- Sidebar de navegación -->
      <div class="wiki-sidebar">
        <div class="sidebar-header">
          <h3>Páginas</h3>
          <div class="sidebar-actions">
            <p-button 
              icon="pi pi-plus"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="createPage()"
              pTooltip="Nueva página">
            </p-button>
            <p-button 
              icon="pi pi-search"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="toggleSearch()"
              pTooltip="Buscar">
            </p-button>
          </div>
        </div>

        <!-- Búsqueda -->
        <div class="search-container" *ngIf="showSearch">
          <input 
            type="text"
            placeholder="Buscar páginas..."
            [(ngModel)]="searchQuery"
            (keyup)="onSearch()"
            class="search-input">
        </div>

        <!-- Árbol de páginas -->
        <div class="pages-tree">
          <p-tree 
            [value]="pageTree"
            selectionMode="single"
            [(selection)]="selectedPage"
            (onNodeSelect)="onPageSelect($event)"
            [loading]="loadingPages">
            
            <ng-template let-node pTemplate="default">
              <div class="tree-node">
                <i [class]="getPageIcon(node.data)" class="page-icon"></i>
                <span class="page-title">{{ node.label }}</span>
                <p-tag 
                  *ngIf="!node.data.is_published"
                  value="Borrador"
                  severity="warning"
                  class="page-status">
                </p-tag>
              </div>
            </ng-template>
          </p-tree>
        </div>

        <!-- Páginas recientes -->
        <div class="recent-pages">
          <h4>Páginas Recientes</h4>
          <div class="recent-list">
            <div 
              *ngFor="let page of recentPages"
              class="recent-item"
              [routerLink]="['/wiki', page.id]">
              <span class="recent-title">{{ page.title }}</span>
              <small class="recent-time">{{ page.updated_at | date:'dd/MM' }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="wiki-content">
        <router-outlet></router-outlet>
        
        <!-- Vista por defecto cuando no hay página seleccionada -->
        <div class="wiki-home" *ngIf="!selectedPage">
          <div class="welcome-section">
            <h2>Bienvenido a la Base de Conocimientos</h2>
            <p>Aquí encontrarás toda la documentación y recursos del proyecto.</p>
            
            <div class="quick-actions">
              <p-button 
                label="Crear Primera Página"
                icon="pi pi-plus"
                (onClick)="createPage()">
              </p-button>
              <p-button 
                label="Explorar Plantillas"
                icon="pi pi-file"
                severity="secondary"
                [outlined]="true"
                (onClick)="showTemplates()">
              </p-button>
            </div>
          </div>

          <!-- Estadísticas -->
          <div class="wiki-stats">
            <div class="stats-grid">
              <div class="stat-item">
                <h3>{{ totalPages }}</h3>
                <p>Páginas Total</p>
              </div>
              <div class="stat-item">
                <h3>{{ publishedPages }}</h3>
                <p>Publicadas</p>
              </div>
              <div class="stat-item">
                <h3>{{ draftPages }}</h3>
                <p>Borradores</p>
              </div>
              <div class="stat-item">
                <h3>{{ totalContributors }}</h3>
                <p>Colaboradores</p>
              </div>
            </div>
          </div>

          <!-- Páginas populares -->
          <div class="popular-pages" *ngIf="popularPages.length > 0">
            <h3>Páginas Populares</h3>
            <div class="pages-grid">
              <p-card 
                *ngFor="let page of popularPages"
                class="page-card"
                [routerLink]="['/wiki', page.id]">
                
                <div class="page-card-content">
                  <h4>{{ page.title }}</h4>
                  <p>{{ page.content | slice:0:150 }}...</p>
                  
                  <div class="page-meta">
                    <span class="author">Por {{ page.author?.first_name }} {{ page.author?.last_name }}</span>
                    <span class="date">{{ page.updated_at | date:'dd/MM/yyyy' }}</span>
                  </div>

                  <div class="page-tags" *ngIf="page.tags && page.tags.length > 0">
                    <p-tag 
                      *ngFor="let tag of page.tags | slice:0:3"
                      [value]="tag"
                      severity="info">
                    </p-tag>
                  </div>
                </div>
              </p-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .wiki-container {
      display: flex;
      height: calc(100vh - 180px);
      gap: 1rem;
      padding: 0 2rem 2rem;
    }

    /* Sidebar */
    .wiki-sidebar {
      width: 300px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .sidebar-header h3 {
      margin: 0;
      color: #333;
    }

    .sidebar-actions {
      display: flex;
      gap: 0.25rem;
    }

    .search-container {
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
    }

    .search-input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      outline: none;
    }

    .search-input:focus {
      border-color: #007bff;
    }

    .pages-tree {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem;
    }

    .tree-node {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      width: 100%;
    }

    .page-icon {
      color: #6c757d;
    }

    .page-title {
      flex: 1;
      font-size: 0.9rem;
    }

    .page-status {
      font-size: 0.7rem !important;
    }

    .recent-pages {
      border-top: 1px solid #e0e0e0;
      padding: 1rem;
    }

    .recent-pages h4 {
      margin: 0 0 0.75rem 0;
      color: #666;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .recent-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0;
      cursor: pointer;
      border-bottom: 1px solid #f0f0f0;
      transition: background 0.2s ease;
    }

    .recent-item:hover {
      background: #f8f9fa;
    }

    .recent-title {
      font-size: 0.85rem;
      color: #333;
    }

    .recent-time {
      font-size: 0.75rem;
      color: #999;
    }

    /* Contenido principal */
    .wiki-content {
      flex: 1;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
    }

    .wiki-home {
      padding: 2rem;
      height: 100%;
      overflow-y: auto;
    }

    .welcome-section {
      text-align: center;
      margin-bottom: 3rem;
    }

    .welcome-section h2 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    .welcome-section p {
      margin: 0 0 2rem 0;
      color: #666;
      font-size: 1.1rem;
    }

    .quick-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }

    .wiki-stats {
      margin-bottom: 3rem;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
    }

    .stat-item {
      text-align: center;
      padding: 1.5rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .stat-item h3 {
      margin: 0 0 0.5rem 0;
      font-size: 2rem;
      color: #007bff;
    }

    .stat-item p {
      margin: 0;
      color: #666;
      font-size: 0.9rem;
    }

    .popular-pages h3 {
      margin: 0 0 1.5rem 0;
      color: #333;
    }

    .pages-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1rem;
    }

    .page-card {
      cursor: pointer;
      transition: transform 0.2s ease;
    }

    .page-card:hover {
      transform: translateY(-2px);
    }

    .page-card-content h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
      font-size: 1.1rem;
    }

    .page-card-content p {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.9rem;
      line-height: 1.4;
    }

    .page-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
      font-size: 0.8rem;
      color: #999;
    }

    .page-tags {
      display: flex;
      gap: 0.25rem;
      flex-wrap: wrap;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .wiki-container {
        flex-direction: column;
        height: auto;
        padding: 0 1rem 1rem;
      }

      .wiki-sidebar {
        width: 100%;
        height: auto;
        margin-bottom: 1rem;
      }

      .stats-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .pages-grid {
        grid-template-columns: 1fr;
      }

      .quick-actions {
        flex-direction: column;
        align-items: center;
      }
    }
  `]
})
export class WikiComponent implements OnInit {
  pageTree: any[] = [];
  selectedPage: any = null;
  recentPages: WikiPage[] = [];
  popularPages: WikiPage[] = [];
  
  showSearch = false;
  searchQuery = '';
  loadingPages = false;

  // Estadísticas
  totalPages = 0;
  publishedPages = 0;
  draftPages = 0;
  totalContributors = 0;

  headerActions = [
    {
      label: 'Nueva Página',
      icon: 'pi pi-plus',
      onClick: () => this.createPage()
    },
    {
      label: 'Configuración',
      icon: 'pi pi-cog',
      severity: 'secondary' as any,
      onClick: () => this.showSettings()
    }
  ];

  constructor(private wikiService: WikiService) {}

  ngOnInit(): void {
    this.loadPages();
    this.loadStats();
    this.loadRecentPages();
    this.loadPopularPages();
  }

  private loadPages(): void {
    this.loadingPages = true;
    this.wikiService.getPages().subscribe(
      response => {
        this.buildPageTree(response.data);
        this.loadingPages = false;
      },
      error => {
        console.error('Error loading pages:', error);
        this.loadingPages = false;
      }
    );
  }

  private buildPageTree(pages: WikiPage[]): void {
    // Construir árbol jerárquico de páginas
    const pageMap = new Map<string, any>();
    const rootPages: any[] = [];

    // Crear nodos para todas las páginas
    pages.forEach(page => {
      const node = {
        key: page.id,
        label: page.title,
        data: page,
        children: [],
        expandedIcon: 'pi pi-folder-open',
        collapsedIcon: 'pi pi-folder',
        leaf: false
      };
      pageMap.set(page.id, node);
    });

    // Organizar jerarquía
    pages.forEach(page => {
      const node = pageMap.get(page.id);
      if (page.parent_id && pageMap.has(page.parent_id)) {
        pageMap.get(page.parent_id).children.push(node);
        node.leaf = true;
      } else {
        rootPages.push(node);
      }
    });

    // Marcar hojas
    rootPages.forEach(this.markLeafNodes);
    
    this.pageTree = rootPages;
  }

  private markLeafNodes(node: any): void {
    if (node.children.length === 0) {
      node.leaf = true;
      node.icon = 'pi pi-file';
    } else {
      node.children.forEach((child: any) => this.markLeafNodes(child));
    }
  }

  private loadStats(): void {
    // Cargar estadísticas de la wiki
    this.wikiService.getStats().subscribe(
      stats => {
        this.totalPages = stats.total_pages;
        this.publishedPages = stats.published_pages;
        this.draftPages = stats.draft_pages;
        this.totalContributors = stats.total_contributors;
      }
    );
  }

  private loadRecentPages(): void {
    this.wikiService.getRecentPages(5).subscribe(
      pages => {
        this.recentPages = pages;
      }
    );
  }

  private loadPopularPages(): void {
    this.wikiService.getPopularPages(6).subscribe(
      pages => {
        this.popularPages = pages;
      }
    );
  }

  onPageSelect(event: any): void {
    const page = event.node.data;
    // Navegar a la página seleccionada
    // this.router.navigate(['/wiki', page.id]);
  }

  createPage(): void {
    // Navegar a crear nueva página
    // this.router.navigate(['/wiki/new']);
  }

  showTemplates(): void {
    // Mostrar plantillas de páginas
  }

  showSettings(): void {
    // Mostrar configuración de la wiki
  }

  toggleSearch(): void {
    this.showSearch = !this.showSearch;
    if (!this.showSearch) {
      this.searchQuery = '';
      this.loadPages(); // Recargar todas las páginas
    }
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.wikiService.searchPages(this.searchQuery).subscribe(
        pages => {
          this.buildPageTree(pages);
        }
      );
    } else {
      this.loadPages();
    }
  }

  getPageIcon(page: WikiPage): string {
    if (!page.is_published) {
      return 'pi pi-file-edit';
    }
    return 'pi pi-file';
  }
}
"""
    
    wiki_component_path = os.path.join(frontend_dir, "src/app/features/wiki/wiki.component.ts")
    os.makedirs(os.path.dirname(wiki_component_path), exist_ok=True)
    with open(wiki_component_path, "w", encoding="utf-8") as f:
        f.write(wiki_component_content)
    
    # src/app/core/services/wiki.service.ts
    wiki_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface WikiPage {
  id: string;
  title: string;
  slug: string;
  content: string;
  project_id: string;
  author_id: string;
  is_published: boolean;
  version: number;
  parent_id?: string;
  tags: string[];
  metadata: {[key: string]: any};
  created_at: string;
  updated_at: string;
  published_at?: string;
  last_edited_at: string;
  
  // Relaciones
  project?: any;
  author?: any;
  parent?: WikiPage;
  children?: WikiPage[];
  revisions?: WikiRevision[];
}

export interface WikiRevision {
  id: string;
  page_id: string;
  title: string;
  content: string;
  author_id: string;
  version: number;
  summary: string;
  created_at: string;
  author?: any;
}

export interface WikiComment {
  id: string;
  content: string;
  page_id: string;
  user_id: string;
  parent_id?: string;
  created_at: string;
  updated_at: string;
  user?: any;
  replies?: WikiComment[];
}

export interface CreatePageRequest {
  title: string;
  content?: string;
  parent_id?: string;
  is_published: boolean;
  tags?: string[];
  metadata?: {[key: string]: any};
}

export interface UpdatePageRequest {
  title?: string;
  content?: string;
  is_published?: boolean;
  tags?: string[];
  summary?: string;
  metadata?: {[key: string]: any};
}

export interface WikiStats {
  total_pages: number;
  published_pages: number;
  draft_pages: number;
  total_contributors: number;
  total_views: number;
}

@Injectable({
  providedIn: 'root'
})
export class WikiService {

  constructor(private http: HttpClient) { }

  getPages(projectId?: string, filter?: any): Observable<{data: WikiPage[], total: number}> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    if (filter) {
      Object.keys(filter).forEach(key => {
        if (filter[key] !== null && filter[key] !== undefined) {
          if (Array.isArray(filter[key])) {
            filter[key].forEach((value: any) => {
              params = params.append(key, value);
            });
          } else {
            params = params.set(key, filter[key]);
          }
        }
      });
    }
    
    return this.http.get<{data: WikiPage[], total: number}>(`${environment.apiUrl}/wiki/pages`, { params });
  }

  getPage(pageId: string): Observable<WikiPage> {
    return this.http.get<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}`);
  }

  getPageBySlug(projectId: string, slug: string): Observable<WikiPage> {
    return this.http.get<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages/${slug}`);
  }

  createPage(projectId: string, pageData: CreatePageRequest): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages`, pageData);
  }

  updatePage(pageId: string, pageData: UpdatePageRequest): Observable<WikiPage> {
    return this.http.put<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}`, pageData);
  }

  deletePage(pageId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/wiki/pages/${pageId}`);
  }

  publishPage(pageId: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/publish`, {});
  }

  unpublishPage(pageId: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/unpublish`, {});
  }

  getPageRevisions(pageId: string): Observable<WikiRevision[]> {
    return this.http.get<WikiRevision[]>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions`);
  }

  getPageRevision(pageId: string, version: number): Observable<WikiRevision> {
    return this.http.get<WikiRevision>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions/${version}`);
  }

  restorePageRevision(pageId: string, version: number): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions/${version}/restore`, {});
  }

  getPageComments(pageId: string): Observable<WikiComment[]> {
    return this.http.get<WikiComment[]>(`${environment.apiUrl}/wiki/pages/${pageId}/comments`);
  }

  addPageComment(pageId: string, content: string, parentId?: string): Observable<WikiComment> {
    return this.http.post<WikiComment>(`${environment.apiUrl}/wiki/pages/${pageId}/comments`, {
      content,
      parent_id: parentId
    });
  }

  updatePageComment(commentId: string, content: string): Observable<WikiComment> {
    return this.http.put<WikiComment>(`${environment.apiUrl}/wiki/comments/${commentId}`, {
      content
    });
  }

  deletePageComment(commentId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/wiki/comments/${commentId}`);
  }

  searchPages(query: string, projectId?: string): Observable<WikiPage[]> {
    let params = new HttpParams().set('q', query);
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/search`, { params });
  }

  getRecentPages(limit = 10): Observable<WikiPage[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/pages/recent`, { params });
  }

  getPopularPages(limit = 10): Observable<WikiPage[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/pages/popular`, { params });
  }

  getStats(projectId?: string): Observable<WikiStats> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<WikiStats>(`${environment.apiUrl}/wiki/stats`, { params });
  }

  uploadFile(file: File): Observable<{file_url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{file_url: string}>(`${environment.apiUrl}/wiki/upload`, formData);
  }

  getPageHierarchy(projectId: string): Observable<WikiPage[]> {
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/projects/${projectId}/hierarchy`);
  }

  movePage(pageId: string, newParentId?: string): Observable<WikiPage> {
    return this.http.put<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/move`, {
      parent_id: newParentId
    });
  }

  duplicatePage(pageId: string, newTitle?: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/duplicate`, {
      title: newTitle
    });
  }

  // Plantillas de páginas
  getPageTemplates(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/wiki/templates`);
  }

  createPageFromTemplate(projectId: string, templateId: string, title: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages/from-template`, {
      template_id: templateId,
      title
    });
  }

  // Exportar páginas
  exportPage(pageId: string, format: 'pdf' | 'html' | 'markdown'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/wiki/pages/${pageId}/export/${format}`, {
      responseType: 'blob'
    });
  }

  exportProject(projectId: string, format: 'pdf' | 'html' | 'markdown'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/wiki/projects/${projectId}/export/${format}`, {
      responseType: 'blob'
    });
  }
}
"""
    
    wiki_service_path = os.path.join(frontend_dir, "src/app/core/services/wiki.service.ts")
    with open(wiki_service_path, "w", encoding="utf-8") as f:
        f.write(wiki_service_content)
    
    print("✓ Componentes de wiki creados")

if __name__ == "__main__":
    create_collaborative_features()
