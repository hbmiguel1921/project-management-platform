package models

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
