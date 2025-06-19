package models

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
