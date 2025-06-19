package database

import (
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

func Initialize(dsn string) (*gorm.DB, error) {
	config := &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	}

	db, err := gorm.Open(postgres.Open(dsn), config)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	// Configure connection pool
	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed to get underlying sql.DB: %w", err)
	}

	sqlDB.SetMaxOpenConns(25)
	sqlDB.SetMaxIdleConns(25)
	sqlDB.SetConnMaxLifetime(5 * time.Minute)

	return db, nil
}

func RunMigrations(db *gorm.DB) error {
	// Auto-migrate all models
	models := []interface{}{
		&models.User{},
		&models.Project{},
		&models.ProjectMember{},
		&models.Task{},
		&models.TaskAssignment{},
		&models.Comment{},
		&models.CommentMention{},
		&models.CommentAttachment{},
		&models.Sprint{},
		&models.SprintEvent{},
		&models.TimeEntry{},
		&models.TimesheetEntry{},
		&models.ChatChannel{},
		&models.ChannelMember{},
		&models.ChatMessage{},
		&models.MessageReaction{},
		&models.MessageAttachment{},
		&models.MessageMention{},
		&models.Notification{},
		&models.NotificationPreference{},
		&models.WikiPage{},
		&models.WikiRevision{},
		&models.WikiComment{},
		&models.WikiAttachment{},
		&models.Report{},
		&models.DashboardWidget{},
	}

	for _, model := range models {
		if err := db.AutoMigrate(model); err != nil {
			return fmt.Errorf("failed to migrate %T: %w", model, err)
		}
	}

	// Create indexes
	if err := createIndexes(db); err != nil {
		return fmt.Errorf("failed to create indexes: %w", err)
	}

	return nil
}

func createIndexes(db *gorm.DB) error {
	// User indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
	
	// Project indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at)")
	
	// Task indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_assignee_id ON tasks(assignee_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_tasks_sprint_id ON tasks(sprint_id)")
	
	// Time entry indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_time_entries_user_id ON time_entries(user_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_time_entries_project_id ON time_entries(project_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_time_entries_start_time ON time_entries(start_time)")
	
	// Chat indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_chat_messages_channel_id ON chat_messages(channel_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at)")
	
	// Notification indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at)")
	
	// Wiki indexes
	db.Exec("CREATE INDEX IF NOT EXISTS idx_wiki_pages_project_id ON wiki_pages(project_id)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_wiki_pages_slug ON wiki_pages(slug)")
	db.Exec("CREATE INDEX IF NOT EXISTS idx_wiki_pages_is_published ON wiki_pages(is_published)")

	return nil
}

func SeedData(db *gorm.DB) error {
	// Check if data already exists
	var userCount int64
	db.Model(&models.User{}).Count(&userCount)
	if userCount > 0 {
		return nil // Data already seeded
	}

	// Create admin user
	adminUser := &models.User{
		FirstName: "Administrador",
		LastName:  "Sistema",
		Email:     "admin@example.com",
		Username:  "admin",
		Role:      models.RoleAdmin,
		IsActive:  true,
	}
	
	// Set password (should be hashed in real implementation)
	if err := adminUser.SetPassword("admin123"); err != nil {
		return fmt.Errorf("failed to set admin password: %w", err)
	}
	
	if err := db.Create(adminUser).Error; err != nil {
		return fmt.Errorf("failed to create admin user: %w", err)
	}

	// Create sample project
	sampleProject := &models.Project{
		Name:        "Proyecto de Ejemplo",
		Description: "Este es un proyecto de ejemplo para demostrar las funcionalidades de la plataforma",
		Status:      models.ProjectStatusActive,
		OwnerID:     adminUser.ID,
	}
	
	if err := db.Create(sampleProject).Error; err != nil {
		return fmt.Errorf("failed to create sample project: %w", err)
	}

	// Add admin as project member
	adminMember := &models.ProjectMember{
		ProjectID: sampleProject.ID,
		UserID:    adminUser.ID,
		Role:      models.ProjectRoleOwner,
	}
	
	if err := db.Create(adminMember).Error; err != nil {
		return fmt.Errorf("failed to add admin as project member: %w", err)
	}

	return nil
}
