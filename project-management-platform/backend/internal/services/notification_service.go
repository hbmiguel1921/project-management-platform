package services

import (
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	internalws "github.com/company/project-management-platform/internal/websocket"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type NotificationService struct {
	db    *gorm.DB
	wsHub *internalws.Hub // Para notificaciones en tiempo real
}

func NewNotificationService(db *gorm.DB, wsHub *internalws.Hub) *NotificationService {
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
			"is_read": true,
			"read_at": time.Now(),
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
			"is_read": true,
			"read_at": time.Now(),
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
		s.wsHub.BroadcastToUser(notification.UserID.String(), &internalws.Message{
			Type:      "notification",
			UserID:    notification.UserID.String(),
			Data:      notification,
			Timestamp: time.Now().Unix(),
		})
	}
}

func (s *NotificationService) sendEmailNotification(notification *models.Notification) {
	// TODO: Implementar envío de emails
	// Verificar preferencias del usuario
	// Usar servicio de email configurado
	fmt.Printf("Sending email notification to user %s: %s", notification.UserID, notification.Title)
}
