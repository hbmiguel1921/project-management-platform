package models

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
