#!/usr/bin/env python3
"""
Script para crear la integración y configuración final del sistema:
- Configuración completa del backend
- Scripts de base de datos
- Rutas del API completas
- Configuración del router del frontend
- Variables de entorno
- Scripts de inicialización
- Configuración de producción
"""

import os

def create_integration_config():
    """Crear configuración e integración final del sistema"""
    
    backend_dir = "/workspace/project-management-platform/backend"
    frontend_dir = "/workspace/project-management-platform/frontend"
    root_dir = "/workspace/project-management-platform"
    
    # Backend - Configuración final
    create_backend_config(backend_dir)
    
    # Backend - Rutas del API
    create_api_routes(backend_dir)
    
    # Backend - Main application
    create_main_application(backend_dir)
    
    # Base de datos - Scripts completos
    create_database_scripts(root_dir)
    
    # Frontend - Routing y configuración
    create_frontend_routing(frontend_dir)
    
    # Configuración de entorno
    create_environment_configs(root_dir)
    
    # Scripts de inicialización
    create_initialization_scripts(root_dir)
    
    print("✓ Integración y configuración final completada")

def create_backend_config(backend_dir):
    """Crear configuración completa del backend"""
    
    # go.mod actualizado
    go_mod_content = """module github.com/company/project-management-platform

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/google/uuid v1.4.0
	github.com/joho/godotenv v1.4.0
	github.com/golang-jwt/jwt/v5 v5.2.0
	gorm.io/gorm v1.25.5
	gorm.io/driver/postgres v1.5.4
	golang.org/x/crypto v0.16.0
	github.com/gorilla/websocket v1.5.1
)

require (
	github.com/bytedance/sonic v1.9.1 // indirect
	github.com/chenzhuoyu/base64x v0.0.0-20221115062448-fe3a3abad311 // indirect
	github.com/gabriel-vasile/mimetype v1.4.2 // indirect
	github.com/gin-contrib/sse v0.1.0 // indirect
	github.com/go-playground/locales v0.14.1 // indirect
	github.com/go-playground/universal-translator v0.18.1 // indirect
	github.com/go-playground/validator/v10 v10.14.0 // indirect
	github.com/goccy/go-json v0.10.2 // indirect
	github.com/jackc/pgpassfile v1.0.0 // indirect
	github.com/jackc/pgservicefile v0.0.0-20221227161230-091c0ba34f0a // indirect
	github.com/jackc/pgx/v5 v5.4.3 // indirect
	github.com/jinzhu/inflection v1.0.0 // indirect
	github.com/jinzhu/now v1.1.5 // indirect
	github.com/json-iterator/go v1.1.12 // indirect
	github.com/klauspost/cpuid/v2 v2.2.4 // indirect
	github.com/leodido/go-urn v1.2.4 // indirect
	github.com/mattn/go-isatty v0.0.19 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.2 // indirect
	github.com/pelletier/go-toml/v2 v2.0.8 // indirect
	github.com/twitchyliquid64/golang-asm v0.15.1 // indirect
	github.com/ugorji/go/codec v1.2.11 // indirect
	golang.org/x/arch v0.3.0 // indirect
	golang.org/x/net v0.19.0 // indirect
	golang.org/x/sys v0.15.0 // indirect
	golang.org/x/text v0.14.0 // indirect
	google.golang.org/protobuf v1.30.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)
"""
    
    go_mod_path = os.path.join(backend_dir, "go.mod")
    with open(go_mod_path, "w", encoding="utf-8") as f:
        f.write(go_mod_content)
    
    # internal/config/config.go actualizado
    config_content = """package config

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
)

type Config struct {
	// Server configuration
	Server ServerConfig `json:"server"`
	
	// Database configuration
	Database DatabaseConfig `json:"database"`
	
	// JWT configuration
	JWT JWTConfig `json:"jwt"`
	
	// Redis configuration
	Redis RedisConfig `json:"redis"`
	
	// Email configuration
	Email EmailConfig `json:"email"`
	
	// File storage configuration
	Storage StorageConfig `json:"storage"`
	
	// WebSocket configuration
	WebSocket WebSocketConfig `json:"websocket"`
	
	// Environment
	Environment string `json:"environment"`
	
	// Logging
	LogLevel string `json:"log_level"`
	
	// CORS
	CORS CORSConfig `json:"cors"`
}

type ServerConfig struct {
	Host         string        `json:"host"`
	Port         int           `json:"port"`
	ReadTimeout  time.Duration `json:"read_timeout"`
	WriteTimeout time.Duration `json:"write_timeout"`
	IdleTimeout  time.Duration `json:"idle_timeout"`
}

type DatabaseConfig struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	User     string `json:"user"`
	Password string `json:"password"`
	Name     string `json:"name"`
	SSLMode  string `json:"ssl_mode"`
	Timezone string `json:"timezone"`
	
	// Connection pool settings
	MaxOpenConns    int           `json:"max_open_conns"`
	MaxIdleConns    int           `json:"max_idle_conns"`
	ConnMaxLifetime time.Duration `json:"conn_max_lifetime"`
}

type JWTConfig struct {
	SecretKey       string        `json:"secret_key"`
	ExpirationTime  time.Duration `json:"expiration_time"`
	RefreshTime     time.Duration `json:"refresh_time"`
	Issuer          string        `json:"issuer"`
}

type RedisConfig struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	Password string `json:"password"`
	DB       int    `json:"db"`
}

type EmailConfig struct {
	SMTPHost     string `json:"smtp_host"`
	SMTPPort     int    `json:"smtp_port"`
	SMTPUser     string `json:"smtp_user"`
	SMTPPassword string `json:"smtp_password"`
	FromEmail    string `json:"from_email"`
	FromName     string `json:"from_name"`
}

type StorageConfig struct {
	Type       string `json:"type"` // local, s3, gcs
	LocalPath  string `json:"local_path"`
	S3Bucket   string `json:"s3_bucket"`
	S3Region   string `json:"s3_region"`
	S3AccessKey string `json:"s3_access_key"`
	S3SecretKey string `json:"s3_secret_key"`
}

type WebSocketConfig struct {
	ReadBufferSize  int           `json:"read_buffer_size"`
	WriteBufferSize int           `json:"write_buffer_size"`
	CheckOrigin     bool          `json:"check_origin"`
	PingPeriod      time.Duration `json:"ping_period"`
	PongWait        time.Duration `json:"pong_wait"`
	WriteWait       time.Duration `json:"write_wait"`
}

type CORSConfig struct {
	AllowedOrigins   []string `json:"allowed_origins"`
	AllowedMethods   []string `json:"allowed_methods"`
	AllowedHeaders   []string `json:"allowed_headers"`
	AllowCredentials bool     `json:"allow_credentials"`
}

var cfg *Config

func Load() (*Config, error) {
	// Load .env file
	if err := godotenv.Load(); err != nil {
		// .env file is optional in production
		fmt.Println("Warning: .env file not found")
	}

	cfg = &Config{
		Server: ServerConfig{
			Host:         getEnv("SERVER_HOST", "localhost"),
			Port:         getEnvInt("SERVER_PORT", 8080),
			ReadTimeout:  time.Duration(getEnvInt("SERVER_READ_TIMEOUT", 30)) * time.Second,
			WriteTimeout: time.Duration(getEnvInt("SERVER_WRITE_TIMEOUT", 30)) * time.Second,
			IdleTimeout:  time.Duration(getEnvInt("SERVER_IDLE_TIMEOUT", 120)) * time.Second,
		},
		Database: DatabaseConfig{
			Host:            getEnv("DB_HOST", "localhost"),
			Port:            getEnvInt("DB_PORT", 5432),
			User:            getEnv("DB_USER", "postgres"),
			Password:        getEnv("DB_PASSWORD", ""),
			Name:            getEnv("DB_NAME", "project_management"),
			SSLMode:         getEnv("DB_SSL_MODE", "disable"),
			Timezone:        getEnv("DB_TIMEZONE", "UTC"),
			MaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", 25),
			MaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", 25),
			ConnMaxLifetime: time.Duration(getEnvInt("DB_CONN_MAX_LIFETIME", 300)) * time.Second,
		},
		JWT: JWTConfig{
			SecretKey:      getEnv("JWT_SECRET_KEY", "your-secret-key-change-in-production"),
			ExpirationTime: time.Duration(getEnvInt("JWT_EXPIRATION_HOURS", 24)) * time.Hour,
			RefreshTime:    time.Duration(getEnvInt("JWT_REFRESH_HOURS", 168)) * time.Hour, // 7 days
			Issuer:         getEnv("JWT_ISSUER", "project-management-platform"),
		},
		Redis: RedisConfig{
			Host:     getEnv("REDIS_HOST", "localhost"),
			Port:     getEnvInt("REDIS_PORT", 6379),
			Password: getEnv("REDIS_PASSWORD", ""),
			DB:       getEnvInt("REDIS_DB", 0),
		},
		Email: EmailConfig{
			SMTPHost:     getEnv("SMTP_HOST", "localhost"),
			SMTPPort:     getEnvInt("SMTP_PORT", 587),
			SMTPUser:     getEnv("SMTP_USER", ""),
			SMTPPassword: getEnv("SMTP_PASSWORD", ""),
			FromEmail:    getEnv("FROM_EMAIL", "noreply@example.com"),
			FromName:     getEnv("FROM_NAME", "Project Management Platform"),
		},
		Storage: StorageConfig{
			Type:        getEnv("STORAGE_TYPE", "local"),
			LocalPath:   getEnv("STORAGE_LOCAL_PATH", "./uploads"),
			S3Bucket:    getEnv("S3_BUCKET", ""),
			S3Region:    getEnv("S3_REGION", ""),
			S3AccessKey: getEnv("S3_ACCESS_KEY", ""),
			S3SecretKey: getEnv("S3_SECRET_KEY", ""),
		},
		WebSocket: WebSocketConfig{
			ReadBufferSize:  getEnvInt("WS_READ_BUFFER_SIZE", 1024),
			WriteBufferSize: getEnvInt("WS_WRITE_BUFFER_SIZE", 1024),
			CheckOrigin:     getEnvBool("WS_CHECK_ORIGIN", false),
			PingPeriod:      time.Duration(getEnvInt("WS_PING_PERIOD", 54)) * time.Second,
			PongWait:        time.Duration(getEnvInt("WS_PONG_WAIT", 60)) * time.Second,
			WriteWait:       time.Duration(getEnvInt("WS_WRITE_WAIT", 10)) * time.Second,
		},
		Environment: getEnv("APP_ENV", "development"),
		LogLevel:    getEnv("LOG_LEVEL", "info"),
		CORS: CORSConfig{
			AllowedOrigins: []string{
				getEnv("CORS_ALLOWED_ORIGINS", "http://localhost:4200,http://localhost:3000"),
			},
			AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
			AllowedHeaders: []string{
				"Accept", "Authorization", "Content-Type", "X-CSRF-Token",
				"X-Requested-With", "Origin", "X-Forwarded-For",
			},
			AllowCredentials: getEnvBool("CORS_ALLOW_CREDENTIALS", true),
		},
	}

	return cfg, nil
}

func Get() *Config {
	if cfg == nil {
		panic("Config not loaded. Call Load() first.")
	}
	return cfg
}

func (c *Config) GetDatabaseDSN() string {
	return fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=%s TimeZone=%s",
		c.Database.Host,
		c.Database.Port,
		c.Database.User,
		c.Database.Password,
		c.Database.Name,
		c.Database.SSLMode,
		c.Database.Timezone,
	)
}

func (c *Config) IsProduction() bool {
	return c.Environment == "production"
}

func (c *Config) IsDevelopment() bool {
	return c.Environment == "development"
}

func (c *Config) IsTest() bool {
	return c.Environment == "test"
}

// Helper functions
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}
"""
    
    config_path = os.path.join(backend_dir, "internal", "config", "config.go")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✓ Configuración del backend creada")

def create_api_routes(backend_dir):
    """Crear rutas completas del API"""
    
    # internal/api/routes/routes.go
    routes_content = """package routes

import (
	"github.com/company/project-management-platform/internal/api/handlers"
	"github.com/company/project-management-platform/internal/api/middleware"
	"github.com/company/project-management-platform/internal/services"
	"github.com/company/project-management-platform/internal/websocket"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func SetupRoutes(
	router *gin.Engine,
	db *gorm.DB,
	authService *services.AuthService,
	projectService *services.ProjectService,
	taskService *services.TaskService,
	sprintService *services.SprintService,
	timeTrackingService *services.TimeTrackingService,
	chatService *services.ChatService,
	notificationService *services.NotificationService,
	wikiService *services.WikiService,
	wsHub *websocket.Hub,
) {
	// Initialize handlers
	authHandler := handlers.NewAuthHandler(authService)
	projectHandler := handlers.NewProjectHandler(projectService)
	taskHandler := handlers.NewTaskHandler(taskService)
	sprintHandler := handlers.NewSprintHandler(sprintService)
	timeTrackingHandler := handlers.NewTimeTrackingHandler(timeTrackingService)
	chatHandler := handlers.NewChatHandler(chatService)
	notificationHandler := handlers.NewNotificationHandler(notificationService)
	wikiHandler := handlers.NewWikiHandler(wikiService)
	wsHandler := handlers.NewWebSocketHandler(wsHub)

	// CORS middleware
	router.Use(middleware.CORSMiddleware())

	// API v1 routes
	v1 := router.Group("/api/v1")
	{
		// Public routes (no authentication required)
		auth := v1.Group("/auth")
		{
			auth.POST("/register", authHandler.Register)
			auth.POST("/login", authHandler.Login)
			auth.POST("/refresh", authHandler.RefreshToken)
			auth.POST("/forgot-password", authHandler.ForgotPassword)
			auth.POST("/reset-password", authHandler.ResetPassword)
			auth.POST("/verify-email", authHandler.VerifyEmail)
		}

		// Protected routes (authentication required)
		protected := v1.Group("")
		protected.Use(middleware.AuthMiddleware(authService))
		{
			// User routes
			users := protected.Group("/users")
			{
				users.GET("/me", authHandler.GetCurrentUser)
				users.PUT("/me", authHandler.UpdateProfile)
				users.PUT("/me/password", authHandler.ChangePassword)
				users.GET("", authHandler.GetUsers) // Admin only
				users.GET("/:id", authHandler.GetUser)
				users.PUT("/:id", authHandler.UpdateUser) // Admin only
				users.DELETE("/:id", authHandler.DeleteUser) // Admin only
			}

			// Project routes
			projects := protected.Group("/projects")
			{
				projects.GET("", projectHandler.GetProjects)
				projects.POST("", projectHandler.CreateProject)
				projects.GET("/:id", projectHandler.GetProject)
				projects.PUT("/:id", projectHandler.UpdateProject)
				projects.DELETE("/:id", projectHandler.DeleteProject)

				// Project members
				projects.GET("/:id/members", projectHandler.GetProjectMembers)
				projects.POST("/:id/members", projectHandler.AddProjectMember)
				projects.PUT("/:id/members/:user_id", projectHandler.UpdateProjectMember)
				projects.DELETE("/:id/members/:user_id", projectHandler.RemoveProjectMember)

				// Project tasks
				projects.GET("/:id/tasks", taskHandler.GetProjectTasks)
				projects.POST("/:id/tasks", taskHandler.CreateTask)

				// Project sprints
				projects.GET("/:project_id/sprints", sprintHandler.GetSprints)
				projects.POST("/:project_id/sprints", sprintHandler.CreateSprint)

				// Project time tracking
				projects.POST("/:project_id/time-entries", timeTrackingHandler.StartTimeEntry)
				projects.GET("/:project_id/time-reports", timeTrackingHandler.GetTeamTimeReports)

				// Project metrics and reports
				projects.GET("/:id/metrics", projectHandler.GetProjectMetrics)
				projects.GET("/:id/dashboard", projectHandler.GetProjectDashboard)
			}

			// Task routes
			tasks := protected.Group("/tasks")
			{
				tasks.GET("", taskHandler.GetTasks)
				tasks.GET("/:id", taskHandler.GetTask)
				tasks.PUT("/:id", taskHandler.UpdateTask)
				tasks.DELETE("/:id", taskHandler.DeleteTask)
				tasks.POST("/:id/assign", taskHandler.AssignTask)
				tasks.POST("/:id/comments", taskHandler.AddComment)
				tasks.GET("/:id/comments", taskHandler.GetComments)
				tasks.PUT("/:id/status", taskHandler.UpdateTaskStatus)
				tasks.POST("/:id/attachments", taskHandler.UploadAttachment)
			}

			// Sprint routes
			sprints := protected.Group("/sprints")
			{
				sprints.GET("/:id", sprintHandler.GetSprint)
				sprints.PUT("/:id", sprintHandler.UpdateSprint)
				sprints.POST("/:id/start", sprintHandler.StartSprint)
				sprints.POST("/:id/complete", sprintHandler.CompleteSprint)
				sprints.POST("/:id/tasks", sprintHandler.AddTaskToSprint)
				sprints.DELETE("/:id/tasks/:task_id", sprintHandler.RemoveTaskFromSprint)
				sprints.GET("/:id/events", sprintHandler.GetSprintEvents)
				sprints.POST("/:id/events", sprintHandler.CreateSprintEvent)
				sprints.GET("/:id/burndown", sprintHandler.GetSprintBurndown)
			}

			// Time tracking routes
			timeTracking := protected.Group("/time-entries")
			{
				timeTracking.GET("", timeTrackingHandler.GetTimeEntries)
				timeTracking.GET("/active", timeTrackingHandler.GetActiveTimeEntry)
				timeTracking.GET("/:id", timeTrackingHandler.GetTimeEntry)
				timeTracking.PUT("/:id", timeTrackingHandler.UpdateTimeEntry)
				timeTracking.PUT("/:id/stop", timeTrackingHandler.StopTimeEntry)
				timeTracking.DELETE("/:id", timeTrackingHandler.DeleteTimeEntry)
			}

			// Time reports
			timeReports := protected.Group("/time-reports")
			{
				timeReports.GET("", timeTrackingHandler.GetTimeReports)
			}

			// Timesheet routes
			timesheet := protected.Group("/timesheet")
			{
				timesheet.GET("/entries", timeTrackingHandler.GetTimesheetEntries)
				timesheet.POST("/entries", timeTrackingHandler.CreateTimesheetEntry)
				timesheet.POST("/submit", timeTrackingHandler.SubmitTimesheet)
			}

			// Chat routes
			chat := protected.Group("/chat")
			{
				chat.GET("/channels", chatHandler.GetChannels)
				chat.POST("/channels", chatHandler.CreateChannel)
				chat.GET("/channels/:id", chatHandler.GetChannel)
				chat.POST("/channels/:id/messages", chatHandler.SendMessage)
				chat.GET("/channels/:id/messages", chatHandler.GetMessages)
				chat.PUT("/channels/:id/messages/:message_id", chatHandler.EditMessage)
				chat.DELETE("/channels/:id/messages/:message_id", chatHandler.DeleteMessage)
				chat.POST("/messages/:message_id/reactions", chatHandler.AddReaction)
				chat.POST("/channels/:id/read", chatHandler.MarkChannelAsRead)
			}

			// Notification routes
			notifications := protected.Group("/notifications")
			{
				notifications.GET("", notificationHandler.GetNotifications)
				notifications.GET("/unread-count", notificationHandler.GetUnreadCount)
				notifications.PUT("/:id/read", notificationHandler.MarkAsRead)
				notifications.PUT("/read-all", notificationHandler.MarkAllAsRead)
				notifications.DELETE("/:id", notificationHandler.DeleteNotification)
			}

			// Wiki routes
			wiki := protected.Group("/wiki")
			{
				wiki.GET("/pages", wikiHandler.GetPages)
				wiki.POST("/projects/:project_id/pages", wikiHandler.CreatePage)
				wiki.GET("/pages/:id", wikiHandler.GetPage)
				wiki.PUT("/pages/:id", wikiHandler.UpdatePage)
				wiki.DELETE("/pages/:id", wikiHandler.DeletePage)
				wiki.POST("/pages/:id/publish", wikiHandler.PublishPage)
				wiki.GET("/pages/:id/revisions", wikiHandler.GetPageRevisions)
				wiki.GET("/pages/:id/comments", wikiHandler.GetPageComments)
				wiki.POST("/pages/:id/comments", wikiHandler.AddPageComment)
				wiki.GET("/search", wikiHandler.SearchPages)
				wiki.GET("/stats", wikiHandler.GetWikiStats)
			}

			// File upload routes
			uploads := protected.Group("/uploads")
			{
				uploads.POST("/files", handlers.UploadFile)
				uploads.POST("/images", handlers.UploadImage)
			}

			// Dashboard routes
			dashboard := protected.Group("/dashboard")
			{
				dashboard.GET("/metrics", handlers.GetDashboardMetrics)
				dashboard.GET("/widgets", handlers.GetDashboardWidgets)
				dashboard.POST("/widgets", handlers.CreateDashboardWidget)
				dashboard.PUT("/widgets/:id", handlers.UpdateDashboardWidget)
				dashboard.DELETE("/widgets/:id", handlers.DeleteDashboardWidget)
			}

			// Report routes
			reports := protected.Group("/reports")
			{
				reports.GET("", handlers.GetReports)
				reports.POST("", handlers.CreateReport)
				reports.GET("/:id", handlers.GetReport)
				reports.PUT("/:id", handlers.UpdateReport)
				reports.DELETE("/:id", handlers.DeleteReport)
				reports.POST("/:id/generate", handlers.GenerateReport)
				reports.GET("/:id/data", handlers.GetReportData)
				reports.GET("/templates", handlers.GetReportTemplates)
				reports.POST("/quick/:type", handlers.GenerateQuickReport)
			}

			// Admin routes
			admin := protected.Group("/admin")
			admin.Use(middleware.AdminMiddleware())
			{
				admin.GET("/users", authHandler.GetUsers)
				admin.POST("/users", authHandler.CreateUser)
				admin.PUT("/users/:id/role", authHandler.UpdateUserRole)
				admin.GET("/system/stats", handlers.GetSystemStats)
				admin.GET("/logs", handlers.GetSystemLogs)
			}
		}

		// WebSocket endpoint
		v1.GET("/ws", wsHandler.HandleWebSocket)

		// Health check
		v1.GET("/health", handlers.HealthCheck)
		v1.GET("/version", handlers.GetVersion)
	}

	// Serve static files
	router.Static("/uploads", "./uploads")
	router.Static("/assets", "./assets")

	// Catch-all route for SPA
	router.NoRoute(handlers.SPAHandler())
}
"""
    
    routes_path = os.path.join(backend_dir, "internal", "api", "routes")
    os.makedirs(routes_path, exist_ok=True)
    routes_file_path = os.path.join(routes_path, "routes.go")
    with open(routes_file_path, "w", encoding="utf-8") as f:
        f.write(routes_content)
    
    # internal/api/middleware/cors.go
    cors_middleware_content = """package middleware

import (
	"strings"

	"github.com/company/project-management-platform/internal/config"
	"github.com/gin-gonic/gin"
)

func CORSMiddleware() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		cfg := config.Get()
		
		origin := c.Request.Header.Get("Origin")
		
		// Check if origin is allowed
		allowedOrigins := strings.Split(cfg.CORS.AllowedOrigins[0], ",")
		isAllowed := false
		for _, allowedOrigin := range allowedOrigins {
			if strings.TrimSpace(allowedOrigin) == origin {
				isAllowed = true
				break
			}
		}
		
		if isAllowed {
			c.Writer.Header().Set("Access-Control-Allow-Origin", origin)
		}
		
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", strings.Join(cfg.CORS.AllowedHeaders, ", "))
		c.Writer.Header().Set("Access-Control-Allow-Methods", strings.Join(cfg.CORS.AllowedMethods, ", "))

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})
}
"""
    
    middleware_path = os.path.join(backend_dir, "internal", "api", "middleware")
    os.makedirs(middleware_path, exist_ok=True)
    cors_middleware_path = os.path.join(middleware_path, "cors.go")
    with open(cors_middleware_path, "w", encoding="utf-8") as f:
        f.write(cors_middleware_content)
    
    # internal/api/middleware/admin.go
    admin_middleware_content = """package middleware

import (
	"net/http"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/utils"
	"github.com/gin-gonic/gin"
)

func AdminMiddleware() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		userRole := c.GetString("user_role")
		
		if userRole != string(models.RoleAdmin) && userRole != string(models.RoleManager) {
			utils.ErrorResponse(c, http.StatusForbidden, "Acceso denegado: se requieren permisos de administrador")
			c.Abort()
			return
		}
		
		c.Next()
	})
}
"""
    
    admin_middleware_path = os.path.join(middleware_path, "admin.go")
    with open(admin_middleware_path, "w", encoding="utf-8") as f:
        f.write(admin_middleware_content)
    
    print("✓ Rutas del API creadas")

def create_main_application(backend_dir):
    """Crear aplicación principal del backend"""
    
    # cmd/main.go
    main_content = """package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/company/project-management-platform/internal/api"
	"github.com/company/project-management-platform/internal/api/routes"
	"github.com/company/project-management-platform/internal/config"
	"github.com/company/project-management-platform/internal/database"
	"github.com/company/project-management-platform/internal/services"
	"github.com/company/project-management-platform/internal/websocket"
	"github.com/gin-gonic/gin"
)

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Set Gin mode
	if cfg.IsProduction() {
		gin.SetMode(gin.ReleaseMode)
	}

	// Initialize database
	db, err := database.Initialize(cfg.GetDatabaseDSN())
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Run migrations
	if err := database.RunMigrations(db); err != nil {
		log.Fatalf("Failed to run migrations: %v", err)
	}

	// Initialize services
	authService := services.NewAuthService(db, cfg)
	projectService := services.NewProjectService(db)
	taskService := services.NewTaskService(db)
	sprintService := services.NewSprintService(db, nil) // Will be set after notification service
	timeTrackingService := services.NewTimeTrackingService(db)
	notificationService := services.NewNotificationService(db, nil) // Will be set after websocket hub
	chatService := services.NewChatService(db, notificationService)
	wikiService := services.NewWikiService(db)

	// Initialize WebSocket hub
	wsHub := websocket.NewHub()
	go wsHub.Run()

	// Update services with WebSocket hub
	notificationService = services.NewNotificationService(db, wsHub)
	sprintService = services.NewSprintService(db, notificationService)

	// Initialize Gin router
	router := gin.New()

	// Add middlewares
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	// Setup routes
	routes.SetupRoutes(
		router,
		db,
		authService,
		projectService,
		taskService,
		sprintService,
		timeTrackingService,
		chatService,
		notificationService,
		wikiService,
		wsHub,
	)

	// Create HTTP server
	server := &http.Server{
		Addr:         fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port),
		Handler:      router,
		ReadTimeout:  cfg.Server.ReadTimeout,
		WriteTimeout: cfg.Server.WriteTimeout,
		IdleTimeout:  cfg.Server.IdleTimeout,
	}

	// Start server in a goroutine
	go func() {
		log.Printf("Starting server on %s:%d", cfg.Server.Host, cfg.Server.Port)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")

	// Give the server 30 seconds to finish current requests
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("Server exited")
}
"""
    
    main_path = os.path.join(backend_dir, "cmd", "main.go")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_content)
    
    # internal/database/database.go actualizado
    database_content = """package database

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
"""
    
    database_path = os.path.join(backend_dir, "internal", "database", "database.go")
    with open(database_path, "w", encoding="utf-8") as f:
        f.write(database_content)
    
    print("✓ Aplicación principal del backend creada")

def create_database_scripts(root_dir):
    """Crear scripts completos de base de datos"""
    
    # database/migrations/001_init.sql actualizado
    init_sql_content = """-- Plataforma de Gestión de Proyectos de Software
-- Script de inicialización de base de datos
-- Versión: 1.0

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tipos ENUM
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'developer', 'tester', 'client');
CREATE TYPE project_status AS ENUM ('planning', 'active', 'completed', 'cancelled', 'on_hold');
CREATE TYPE project_member_role AS ENUM ('owner', 'manager', 'developer', 'tester', 'viewer');
CREATE TYPE task_status AS ENUM ('todo', 'in_progress', 'review', 'completed', 'cancelled');
CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high', 'urgent');
CREATE TYPE sprint_status AS ENUM ('planning', 'active', 'completed', 'cancelled');
CREATE TYPE notification_type AS ENUM ('task_assigned', 'task_updated', 'task_completed', 'task_overdue', 'comment_added', 'comment_mention', 'project_invite', 'project_update', 'chat_mention', 'chat_message', 'sprint_started', 'sprint_ended', 'system_alert');
CREATE TYPE timesheet_status AS ENUM ('draft', 'submitted', 'approved', 'rejected');
CREATE TYPE channel_type AS ENUM ('project', 'general', 'private', 'direct');
CREATE TYPE message_type AS ENUM ('text', 'file', 'image', 'system', 'task_link', 'project_link');
CREATE TYPE sprint_event_type AS ENUM ('planning', 'daily', 'review', 'retrospective', 'custom');

-- Función para actualizar timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'developer',
    avatar VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de proyectos
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status project_status NOT NULL DEFAULT 'planning',
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    repository_url VARCHAR(500),
    documentation_url VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de miembros de proyecto
CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role project_member_role NOT NULL DEFAULT 'developer',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);

-- Tabla de sprints
CREATE TABLE sprints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status sprint_status NOT NULL DEFAULT 'planning',
    goal TEXT,
    capacity INTEGER DEFAULT 0,
    committed_points INTEGER DEFAULT 0,
    completed_points INTEGER DEFAULT 0,
    velocity DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de tareas
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    assignee_id UUID REFERENCES users(id) ON DELETE SET NULL,
    reporter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sprint_id UUID REFERENCES sprints(id) ON DELETE SET NULL,
    status task_status NOT NULL DEFAULT 'todo',
    priority task_priority NOT NULL DEFAULT 'medium',
    story_points INTEGER DEFAULT 0,
    estimated_hours DECIMAL(5,2),
    actual_hours DECIMAL(5,2) DEFAULT 0,
    due_date DATE,
    tags TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de asignaciones de tareas
CREATE TABLE task_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(task_id, user_id)
);

-- Tabla de comentarios
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    is_edited BOOLEAN DEFAULT false,
    edited_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de menciones en comentarios
CREATE TABLE comment_mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    mentioned_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de adjuntos de comentarios
CREATE TABLE comment_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de eventos de sprint
CREATE TABLE sprint_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sprint_id UUID NOT NULL REFERENCES sprints(id) ON DELETE CASCADE,
    type sprint_event_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de seguimiento de tiempo
CREATE TABLE time_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    description TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration INTEGER DEFAULT 0, -- en minutos
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_billable BOOLEAN DEFAULT true,
    hourly_rate DECIMAL(8,2),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de hojas de tiempo
CREATE TABLE timesheet_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    hours DECIMAL(4,2) NOT NULL,
    description TEXT,
    is_billable BOOLEAN DEFAULT true,
    status timesheet_status DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de canales de chat
CREATE TABLE chat_channels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type channel_type NOT NULL DEFAULT 'project',
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    is_private BOOLEAN DEFAULT false,
    creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de miembros de canales
CREATE TABLE channel_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    channel_id UUID NOT NULL REFERENCES chat_channels(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read TIMESTAMP,
    UNIQUE(channel_id, user_id)
);

-- Tabla de mensajes de chat
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    channel_id UUID NOT NULL REFERENCES chat_channels(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type message_type DEFAULT 'text',
    is_edited BOOLEAN DEFAULT false,
    edited_at TIMESTAMP,
    reply_to_id UUID REFERENCES chat_messages(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reacciones a mensajes
CREATE TABLE message_reactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    emoji VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(message_id, user_id, emoji)
);

-- Tabla de adjuntos de mensajes
CREATE TABLE message_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de menciones en mensajes
CREATE TABLE message_mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    mentioned_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de notificaciones
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    type notification_type NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    action_url VARCHAR(500),
    entity_type VARCHAR(50),
    entity_id UUID,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de preferencias de notificaciones
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type notification_type NOT NULL,
    in_app BOOLEAN DEFAULT true,
    email BOOLEAN DEFAULT true,
    push BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, type)
);

-- Tabla de páginas wiki
CREATE TABLE wiki_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    content TEXT,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_published BOOLEAN DEFAULT false,
    version INTEGER DEFAULT 1,
    parent_id UUID REFERENCES wiki_pages(id) ON DELETE SET NULL,
    tags TEXT[],
    metadata JSONB,
    published_at TIMESTAMP,
    last_edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de revisiones de wiki
CREATE TABLE wiki_revisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_id UUID NOT NULL REFERENCES wiki_pages(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    summary VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de comentarios de wiki
CREATE TABLE wiki_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    page_id UUID NOT NULL REFERENCES wiki_pages(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES wiki_comments(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de adjuntos de wiki
CREATE TABLE wiki_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_id UUID NOT NULL REFERENCES wiki_pages(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reportes
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_public BOOLEAN DEFAULT false,
    schedule VARCHAR(100), -- Cron expression
    config JSONB,
    filters JSONB,
    last_generated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de widgets de dashboard
CREATE TABLE dashboard_widgets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    size VARCHAR(20),
    position INTEGER,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    config JSONB,
    is_visible BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear triggers para updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_comments_updated_at BEFORE UPDATE ON comments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sprints_updated_at BEFORE UPDATE ON sprints FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_time_entries_updated_at BEFORE UPDATE ON time_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_timesheet_entries_updated_at BEFORE UPDATE ON timesheet_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_chat_channels_updated_at BEFORE UPDATE ON chat_channels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_chat_messages_updated_at BEFORE UPDATE ON chat_messages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_notifications_updated_at BEFORE UPDATE ON notifications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_notification_preferences_updated_at BEFORE UPDATE ON notification_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_wiki_pages_updated_at BEFORE UPDATE ON wiki_pages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_wiki_comments_updated_at BEFORE UPDATE ON wiki_comments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_dashboard_widgets_updated_at BEFORE UPDATE ON dashboard_widgets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Crear índices para optimización
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at);

CREATE INDEX idx_project_members_project_id ON project_members(project_id);
CREATE INDEX idx_project_members_user_id ON project_members(user_id);

CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assignee_id ON tasks(assignee_id);
CREATE INDEX idx_tasks_reporter_id ON tasks(reporter_id);
CREATE INDEX idx_tasks_sprint_id ON tasks(sprint_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

CREATE INDEX idx_sprints_project_id ON sprints(project_id);
CREATE INDEX idx_sprints_status ON sprints(status);
CREATE INDEX idx_sprints_start_date ON sprints(start_date);
CREATE INDEX idx_sprints_end_date ON sprints(end_date);

CREATE INDEX idx_time_entries_user_id ON time_entries(user_id);
CREATE INDEX idx_time_entries_project_id ON time_entries(project_id);
CREATE INDEX idx_time_entries_task_id ON time_entries(task_id);
CREATE INDEX idx_time_entries_start_time ON time_entries(start_time);

CREATE INDEX idx_chat_messages_channel_id ON chat_messages(channel_id);
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

CREATE INDEX idx_wiki_pages_project_id ON wiki_pages(project_id);
CREATE INDEX idx_wiki_pages_author_id ON wiki_pages(author_id);
CREATE INDEX idx_wiki_pages_slug ON wiki_pages(slug);
CREATE INDEX idx_wiki_pages_is_published ON wiki_pages(is_published);
CREATE INDEX idx_wiki_pages_parent_id ON wiki_pages(parent_id);

-- Comentarios en tablas
COMMENT ON TABLE users IS 'Usuarios del sistema';
COMMENT ON TABLE projects IS 'Proyectos de desarrollo de software';
COMMENT ON TABLE project_members IS 'Miembros asignados a proyectos';
COMMENT ON TABLE tasks IS 'Tareas de los proyectos';
COMMENT ON TABLE comments IS 'Comentarios en tareas';
COMMENT ON TABLE sprints IS 'Sprints ágiles de los proyectos';
COMMENT ON TABLE time_entries IS 'Registro de tiempo trabajado';
COMMENT ON TABLE chat_channels IS 'Canales de comunicación';
COMMENT ON TABLE chat_messages IS 'Mensajes de chat';
COMMENT ON TABLE notifications IS 'Notificaciones del sistema';
COMMENT ON TABLE wiki_pages IS 'Páginas de documentación wiki';

-- Datos iniciales (seeds)
INSERT INTO users (id, first_name, last_name, email, username, password_hash, role, is_active, email_verified) VALUES
(uuid_generate_v4(), 'Administrador', 'Sistema', 'admin@example.com', 'admin', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin', true, true);

-- Configuraciones iniciales
INSERT INTO notification_preferences (user_id, type, in_app, email, push)
SELECT u.id, t.type, true, true, true
FROM users u
CROSS JOIN (
    VALUES 
    ('task_assigned'::notification_type),
    ('task_updated'::notification_type),
    ('task_completed'::notification_type),
    ('comment_added'::notification_type),
    ('project_invite'::notification_type)
) t(type)
WHERE u.email = 'admin@example.com';
"""
    
    init_sql_path = os.path.join(root_dir, "database", "migrations", "001_init.sql")
    with open(init_sql_path, "w", encoding="utf-8") as f:
        f.write(init_sql_content)
    
    # database/seeds/development.sql
    dev_seeds_content = """-- Datos de desarrollo para la plataforma de gestión de proyectos

-- Usuarios de prueba
INSERT INTO users (id, first_name, last_name, email, username, password_hash, role, is_active, email_verified) VALUES
(uuid_generate_v4(), 'Ana', 'García', 'ana.garcia@example.com', 'ana.garcia', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'manager', true, true),
(uuid_generate_v4(), 'Carlos', 'López', 'carlos.lopez@example.com', 'carlos.lopez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true),
(uuid_generate_v4(), 'María', 'Rodríguez', 'maria.rodriguez@example.com', 'maria.rodriguez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true),
(uuid_generate_v4(), 'Juan', 'Martínez', 'juan.martinez@example.com', 'juan.martinez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'tester', true, true),
(uuid_generate_v4(), 'Laura', 'Hernández', 'laura.hernandez@example.com', 'laura.hernandez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true);

-- Proyectos de ejemplo
DO $$
DECLARE
    admin_id UUID;
    ana_id UUID;
    carlos_id UUID;
    maria_id UUID;
    juan_id UUID;
    laura_id UUID;
    proyecto_alpha_id UUID;
    proyecto_beta_id UUID;
    sprint_alpha_id UUID;
    task1_id UUID;
    task2_id UUID;
    channel_alpha_id UUID;
BEGIN
    -- Obtener IDs de usuarios
    SELECT id INTO admin_id FROM users WHERE email = 'admin@example.com';
    SELECT id INTO ana_id FROM users WHERE email = 'ana.garcia@example.com';
    SELECT id INTO carlos_id FROM users WHERE email = 'carlos.lopez@example.com';
    SELECT id INTO maria_id FROM users WHERE email = 'maria.rodriguez@example.com';
    SELECT id INTO juan_id FROM users WHERE email = 'juan.martinez@example.com';
    SELECT id INTO laura_id FROM users WHERE email = 'laura.hernandez@example.com';

    -- Crear proyecto Alpha
    proyecto_alpha_id := uuid_generate_v4();
    INSERT INTO projects (id, name, description, status, owner_id, start_date, end_date, budget) VALUES
    (proyecto_alpha_id, 'Proyecto Alpha', 'Sistema de gestión de inventario para empresa de retail', 'active', ana_id, '2024-01-15', '2024-06-30', 75000.00);

    -- Crear proyecto Beta
    proyecto_beta_id := uuid_generate_v4();
    INSERT INTO projects (id, name, description, status, owner_id, start_date, end_date, budget) VALUES
    (proyecto_beta_id, 'Proyecto Beta', 'Aplicación móvil para delivery de comida', 'planning', admin_id, '2024-03-01', '2024-08-15', 120000.00);

    -- Agregar miembros al proyecto Alpha
    INSERT INTO project_members (project_id, user_id, role) VALUES
    (proyecto_alpha_id, ana_id, 'manager'),
    (proyecto_alpha_id, carlos_id, 'developer'),
    (proyecto_alpha_id, maria_id, 'developer'),
    (proyecto_alpha_id, juan_id, 'tester');

    -- Agregar miembros al proyecto Beta
    INSERT INTO project_members (project_id, user_id, role) VALUES
    (proyecto_beta_id, admin_id, 'owner'),
    (proyecto_beta_id, laura_id, 'developer'),
    (proyecto_beta_id, juan_id, 'tester');

    -- Crear sprint para proyecto Alpha
    sprint_alpha_id := uuid_generate_v4();
    INSERT INTO sprints (id, name, description, project_id, start_date, end_date, status, goal, capacity) VALUES
    (sprint_alpha_id, 'Sprint 1 - Alpha', 'Configuración inicial del proyecto y módulo de autenticación', proyecto_alpha_id, '2024-01-15', '2024-01-29', 'completed', 'Establecer la base del proyecto con autenticación segura', 40);

    -- Crear tareas para el proyecto Alpha
    task1_id := uuid_generate_v4();
    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, sprint_id, status, priority, story_points, estimated_hours) VALUES
    (task1_id, 'Configurar arquitectura del proyecto', 'Establecer la estructura base del proyecto, configurar base de datos y servicios principales', proyecto_alpha_id, carlos_id, ana_id, sprint_alpha_id, 'completed', 'high', 8, 16.0);

    task2_id := uuid_generate_v4();
    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, sprint_id, status, priority, story_points, estimated_hours) VALUES
    (task2_id, 'Implementar sistema de autenticación', 'Desarrollar login, registro y gestión de sesiones con JWT', proyecto_alpha_id, maria_id, ana_id, sprint_alpha_id, 'in_progress', 'high', 5, 12.0);

    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, status, priority, story_points, estimated_hours) VALUES
    (uuid_generate_v4(), 'Diseñar interfaz de usuario principal', 'Crear wireframes y prototipos de la interfaz principal del sistema', proyecto_alpha_id, carlos_id, ana_id, 'todo', 'medium', 3, 8.0);

    -- Crear comentarios en tareas
    INSERT INTO comments (content, task_id, user_id) VALUES
    ('He completado la configuración inicial. La base de datos está funcionando correctamente.', task1_id, carlos_id),
    ('Excelente trabajo! Ahora podemos continuar con el siguiente módulo.', task1_id, ana_id),
    ('Estoy trabajando en la implementación de JWT. Tengo algunas dudas sobre la configuración de seguridad.', task2_id, maria_id);

    -- Crear entradas de tiempo
    INSERT INTO time_entries (description, start_time, end_time, duration, task_id, project_id, user_id, is_billable) VALUES
    ('Configuración inicial del proyecto', '2024-01-15 09:00:00', '2024-01-15 17:00:00', 480, task1_id, proyecto_alpha_id, carlos_id, true),
    ('Investigación sobre JWT y configuración de seguridad', '2024-01-16 09:00:00', '2024-01-16 12:00:00', 180, task2_id, proyecto_alpha_id, maria_id, true),
    ('Desarrollo de endpoints de autenticación', '2024-01-16 14:00:00', '2024-01-16 18:00:00', 240, task2_id, proyecto_alpha_id, maria_id, true);

    -- Crear canal de chat para proyecto Alpha
    channel_alpha_id := uuid_generate_v4();
    INSERT INTO chat_channels (id, name, description, type, project_id, creator_id) VALUES
    (channel_alpha_id, 'general-alpha', 'Canal general del Proyecto Alpha', 'project', proyecto_alpha_id, ana_id);

    -- Agregar miembros al canal
    INSERT INTO channel_members (channel_id, user_id, role) VALUES
    (channel_alpha_id, ana_id, 'admin'),
    (channel_alpha_id, carlos_id, 'member'),
    (channel_alpha_id, maria_id, 'member'),
    (channel_alpha_id, juan_id, 'member');

    -- Crear mensajes en el canal
    INSERT INTO chat_messages (content, channel_id, user_id, type) VALUES
    ('¡Bienvenidos al canal del Proyecto Alpha! Aquí coordinaremos nuestro trabajo diario.', channel_alpha_id, ana_id, 'text'),
    ('Perfecto! Ya tenemos la base configurada y lista para desarrollo.', channel_alpha_id, carlos_id, 'text'),
    ('Excelente. ¿Alguien puede revisar la documentación de la API que subí?', channel_alpha_id, maria_id, 'text');

    -- Crear página wiki para el proyecto
    INSERT INTO wiki_pages (title, slug, content, project_id, author_id, is_published, version) VALUES
    ('Documentación del Proyecto Alpha', 'proyecto-alpha-docs', '# Proyecto Alpha - Sistema de Gestión de Inventario

## Objetivo
Desarrollar un sistema completo de gestión de inventario para empresas de retail.

## Tecnologías
- Backend: Golang con Gin
- Frontend: Angular con PrimeNG
- Base de datos: PostgreSQL
- Autenticación: JWT

## Arquitectura
El sistema sigue una arquitectura de microservicios con las siguientes capas:
- API REST
- Capa de servicios
- Capa de datos
- Frontend SPA

## Configuración del Entorno
...', proyecto_alpha_id, ana_id, true, 1);

    -- Crear notificaciones de ejemplo
    INSERT INTO notifications (title, content, type, user_id, action_url, entity_type, entity_id) VALUES
    ('Nueva tarea asignada', 'Se te ha asignado la tarea: Implementar sistema de autenticación', 'task_assigned', maria_id, '/tasks/' || task2_id, 'task', task2_id),
    ('Comentario en tarea', 'Carlos López ha comentado en tu tarea', 'comment_added', maria_id, '/tasks/' || task2_id, 'task', task2_id),
    ('Tarea completada', 'Carlos López ha completado la tarea: Configurar arquitectura del proyecto', 'task_completed', ana_id, '/tasks/' || task1_id, 'task', task1_id);

END $$;
"""
    
    seeds_path = os.path.join(root_dir, "database", "seeds")
    os.makedirs(seeds_path, exist_ok=True)
    dev_seeds_path = os.path.join(seeds_path, "development.sql")
    with open(dev_seeds_path, "w", encoding="utf-8") as f:
        f.write(dev_seeds_content)
    
    print("✓ Scripts de base de datos creados")

def create_frontend_routing(frontend_dir):
    """Crear configuración de routing del frontend"""
    
    # src/app/app.routes.ts actualizado
    app_routes_content = """import { Routes } from '@angular/router';
import { AuthGuard } from '@core/guards/auth.guard';

export const routes: Routes = [
  // Redirección por defecto
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },

  // Rutas públicas (sin autenticación)
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },

  // Rutas protegidas (requieren autenticación)
  {
    path: 'dashboard',
    canActivate: [AuthGuard],
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },

  // Proyectos
  {
    path: 'projects',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/projects/project.routes').then(m => m.PROJECT_ROUTES)
  },

  // Tareas
  {
    path: 'tasks',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/tasks/task.routes').then(m => m.TASK_ROUTES)
  },

  // Kanban
  {
    path: 'kanban',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/kanban/kanban.routes').then(m => m.KANBAN_ROUTES)
  },

  // Sprints
  {
    path: 'sprints',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/sprints/sprint.routes').then(m => m.SPRINT_ROUTES)
  },

  // Seguimiento de tiempo
  {
    path: 'time-tracking',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/time-tracking/time-tracking.routes').then(m => m.TIME_TRACKING_ROUTES)
  },

  // Chat
  {
    path: 'chat',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/chat/chat.routes').then(m => m.CHAT_ROUTES)
  },

  // Wiki
  {
    path: 'wiki',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/wiki/wiki.routes').then(m => m.WIKI_ROUTES)
  },

  // Reportes
  {
    path: 'reports',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/reports/reports.routes').then(m => m.REPORTS_ROUTES)
  },

  // Notificaciones
  {
    path: 'notifications',
    canActivate: [AuthGuard],
    loadComponent: () => import('./features/notifications/notifications-page.component').then(m => m.NotificationsPageComponent)
  },

  // Perfil de usuario
  {
    path: 'profile',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/profile/profile.routes').then(m => m.PROFILE_ROUTES)
  },

  // Administración
  {
    path: 'admin',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/admin/admin.routes').then(m => m.ADMIN_ROUTES)
  },

  // Configuración
  {
    path: 'settings',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/settings/settings.routes').then(m => m.SETTINGS_ROUTES)
  },

  // Páginas de error
  {
    path: '404',
    loadComponent: () => import('./shared/components/error-pages/not-found.component').then(m => m.NotFoundComponent)
  },
  {
    path: '403',
    loadComponent: () => import('./shared/components/error-pages/forbidden.component').then(m => m.ForbiddenComponent)
  },
  {
    path: '500',
    loadComponent: () => import('./shared/components/error-pages/server-error.component').then(m => m.ServerErrorComponent)
  },

  // Ruta catch-all (debe ser la última)
  { path: '**', redirectTo: '/404' }
];
"""
    
    app_routes_path = os.path.join(frontend_dir, "src/app/app.routes.ts")
    with open(app_routes_path, "w", encoding="utf-8") as f:
        f.write(app_routes_content)
    
    # src/app/features/auth/auth.routes.ts
    auth_routes_content = """import { Routes } from '@angular/router';

export const AUTH_ROUTES: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./forgot-password/forgot-password.component').then(m => m.ForgotPasswordComponent)
  },
  {
    path: 'reset-password',
    loadComponent: () => import('./reset-password/reset-password.component').then(m => m.ResetPasswordComponent)
  },
  {
    path: 'verify-email',
    loadComponent: () => import('./verify-email/verify-email.component').then(m => m.VerifyEmailComponent)
  },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];
"""
    
    auth_routes_path = os.path.join(frontend_dir, "src/app/features/auth")
    os.makedirs(auth_routes_path, exist_ok=True)
    auth_routes_file = os.path.join(auth_routes_path, "auth.routes.ts")
    with open(auth_routes_file, "w", encoding="utf-8") as f:
        f.write(auth_routes_content)
    
    # Crear archivos de rutas para cada módulo
    modules_routes = [
        ("projects", "PROJECT_ROUTES"),
        ("tasks", "TASK_ROUTES"),
        ("kanban", "KANBAN_ROUTES"),
        ("sprints", "SPRINT_ROUTES"),
        ("time-tracking", "TIME_TRACKING_ROUTES"),
        ("chat", "CHAT_ROUTES"),
        ("wiki", "WIKI_ROUTES"),
        ("reports", "REPORTS_ROUTES"),
        ("profile", "PROFILE_ROUTES"),
        ("admin", "ADMIN_ROUTES"),
        ("settings", "SETTINGS_ROUTES")
    ]
    
    for module_name, route_const in modules_routes:
        create_module_routes(frontend_dir, module_name, route_const)
    
    print("✓ Routing del frontend configurado")

def create_module_routes(frontend_dir, module_name, route_const):
    """Crear archivo de rutas para un módulo específico"""
    
    module_path = os.path.join(frontend_dir, f"src/app/features/{module_name}")
    os.makedirs(module_path, exist_ok=True)
    
    routes_content = f"""import {{ Routes }} from '@angular/router';

export const {route_const}: Routes = [
  {{
    path: '',
    loadComponent: () => import('./{module_name}.component').then(m => m.{module_name.replace('-', '').title()}Component)
  }},
  // Agregar más rutas específicas del módulo aquí
];
"""
    
    routes_file = os.path.join(module_path, f"{module_name}.routes.ts")
    with open(routes_file, "w", encoding="utf-8") as f:
        f.write(routes_content)

def create_environment_configs(root_dir):
    """Crear configuraciones de entorno"""
    
    # .env.template
    env_template_content = """# Configuración del Servidor
SERVER_HOST=localhost
SERVER_PORT=8080
SERVER_READ_TIMEOUT=30
SERVER_WRITE_TIMEOUT=30
SERVER_IDLE_TIMEOUT=120

# Configuración de la Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_NAME=project_management
DB_SSL_MODE=disable
DB_TIMEZONE=UTC
DB_MAX_OPEN_CONNS=25
DB_MAX_IDLE_CONNS=25
DB_CONN_MAX_LIFETIME=300

# Configuración JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION_HOURS=24
JWT_REFRESH_HOURS=168
JWT_ISSUER=project-management-platform

# Configuración Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Configuración de Email
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
FROM_EMAIL=noreply@example.com
FROM_NAME=Project Management Platform

# Configuración de Almacenamiento
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=./uploads
S3_BUCKET=
S3_REGION=
S3_ACCESS_KEY=
S3_SECRET_KEY=

# Configuración WebSocket
WS_READ_BUFFER_SIZE=1024
WS_WRITE_BUFFER_SIZE=1024
WS_CHECK_ORIGIN=false
WS_PING_PERIOD=54
WS_PONG_WAIT=60
WS_WRITE_WAIT=10

# Configuración de la Aplicación
APP_ENV=development
LOG_LEVEL=info

# Configuración CORS
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000
CORS_ALLOW_CREDENTIALS=true
"""
    
    env_template_path = os.path.join(root_dir, ".env.template")
    with open(env_template_path, "w", encoding="utf-8") as f:
        f.write(env_template_content)
    
    # .env.development
    env_dev_content = """# Configuración de Desarrollo
SERVER_HOST=localhost
SERVER_PORT=8080

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=project_management_dev

JWT_SECRET_KEY=development-secret-key-not-for-production
JWT_EXPIRATION_HOURS=24

APP_ENV=development
LOG_LEVEL=debug

CORS_ALLOWED_ORIGINS=http://localhost:4200
"""
    
    env_dev_path = os.path.join(root_dir, ".env.development")
    with open(env_dev_path, "w", encoding="utf-8") as f:
        f.write(env_dev_content)
    
    # .env.production
    env_prod_content = """# Configuración de Producción
SERVER_HOST=0.0.0.0
SERVER_PORT=8080

DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=project_management

JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_EXPIRATION_HOURS=24

APP_ENV=production
LOG_LEVEL=info

CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
"""
    
    env_prod_path = os.path.join(root_dir, ".env.production")
    with open(env_prod_path, "w", encoding="utf-8") as f:
        f.write(env_prod_content)
    
    # src/environments/environment.ts actualizado
    environment_content = """export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api/v1',
  wsUrl: 'ws://localhost:8080/api/v1/ws',
  appName: 'Plataforma de Gestión de Proyectos',
  version: '1.0.0',
  features: {
    enableChat: true,
    enableTimeTracking: true,
    enableReports: true,
    enableNotifications: true,
    enableWiki: true
  },
  storage: {
    tokenKey: 'auth_token',
    refreshTokenKey: 'refresh_token',
    userKey: 'current_user'
  },
  pagination: {
    defaultPageSize: 20,
    pageSizeOptions: [10, 20, 50, 100]
  },
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedImageTypes: ['image/jpeg', 'image/png', 'image/gif'],
    allowedFileTypes: ['application/pdf', 'application/msword', 'text/plain']
  }
};
"""
    
    env_ts_path = os.path.join(root_dir, "frontend/src/environments/environment.ts")
    with open(env_ts_path, "w", encoding="utf-8") as f:
        f.write(environment_content)
    
    # src/environments/environment.development.ts
    env_dev_ts_content = """export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api/v1',
  wsUrl: 'ws://localhost:8080/api/v1/ws',
  appName: 'Plataforma de Gestión de Proyectos [DEV]',
  version: '1.0.0-dev',
  features: {
    enableChat: true,
    enableTimeTracking: true,
    enableReports: true,
    enableNotifications: true,
    enableWiki: true,
    enableDebugMode: true
  },
  storage: {
    tokenKey: 'auth_token_dev',
    refreshTokenKey: 'refresh_token_dev',
    userKey: 'current_user_dev'
  },
  pagination: {
    defaultPageSize: 10,
    pageSizeOptions: [5, 10, 20, 50]
  },
  upload: {
    maxFileSize: 5 * 1024 * 1024, // 5MB for development
    allowedImageTypes: ['image/jpeg', 'image/png', 'image/gif'],
    allowedFileTypes: ['application/pdf', 'application/msword', 'text/plain']
  }
};
"""
    
    env_dev_ts_path = os.path.join(root_dir, "frontend/src/environments/environment.development.ts")
    with open(env_dev_ts_path, "w", encoding="utf-8") as f:
        f.write(env_dev_ts_content)
    
    print("✓ Configuraciones de entorno creadas")

def create_initialization_scripts(root_dir):
    """Crear scripts de inicialización"""
    
    # scripts/setup.sh
    setup_script_content = """#!/bin/bash

# Script de configuración inicial para la Plataforma de Gestión de Proyectos
# Este script configura el entorno de desarrollo completo

set -e

echo "🚀 Configurando Plataforma de Gestión de Proyectos..."

# Colores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Función para mostrar mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependencias
print_status "Verificando dependencias..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker y Docker Compose."
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado."
    exit 1
fi

# Verificar Go (opcional para desarrollo)
if ! command -v go &> /dev/null; then
    print_warning "Go no está instalado. Se usará la imagen Docker para el backend."
else
    print_status "Go encontrado: $(go version)"
fi

# Verificar Node.js (opcional para desarrollo)
if ! command -v node &> /dev/null; then
    print_warning "Node.js no está instalado. Se usará la imagen Docker para el frontend."
else
    print_status "Node.js encontrado: $(node --version)"
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    print_status "Creando archivo .env desde template..."
    cp .env.template .env
    print_warning "Por favor, edita el archivo .env con tus configuraciones específicas."
else
    print_status "Archivo .env ya existe."
fi

# Crear directorio de uploads
print_status "Creando directorios necesarios..."
mkdir -p uploads
mkdir -p logs
mkdir -p database/backups

# Configurar permisos
chmod +x scripts/development/start.sh
chmod +x scripts/maintenance/backup.sh

# Construir imágenes Docker
print_status "Construyendo imágenes Docker..."
docker-compose build

# Inicializar base de datos
print_status "Inicializando base de datos..."
docker-compose up -d postgres
sleep 10

# Esperar que PostgreSQL esté listo
print_status "Esperando a que PostgreSQL esté listo..."
until docker-compose exec postgres pg_isready -U postgres; do
    sleep 2
done

# Ejecutar migraciones
print_status "Ejecutando migraciones de base de datos..."
docker-compose exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/001_init.sql

# Cargar datos de desarrollo
if [ "$1" = "--with-sample-data" ]; then
    print_status "Cargando datos de ejemplo..."
    docker-compose exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/development.sql
fi

print_status "✅ Configuración completada!"
echo
print_status "Para iniciar la aplicación:"
echo "  docker-compose up -d"
echo
print_status "Para desarrollo:"
echo "  make dev"
echo
print_status "URLs de la aplicación:"
echo "  Frontend: http://localhost:4200"
echo "  Backend API: http://localhost:8080"
echo "  Documentación API: http://localhost:8080/docs"
echo
print_status "Usuario administrador por defecto:"
echo "  Email: admin@example.com"
echo "  Password: admin123"
"""
    
    setup_script_path = os.path.join(root_dir, "scripts/setup.sh")
    with open(setup_script_path, "w", encoding="utf-8") as f:
        f.write(setup_script_content)
    
    # scripts/development/start.sh actualizado
    start_script_content = """#!/bin/bash

# Script para iniciar el entorno de desarrollo

set -e

echo "🚀 Iniciando entorno de desarrollo..."

# Función para mostrar mensajes
print_status() {
    echo -e "\\033[0;32m[INFO]\\033[0m $1"
}

# Verificar que .env existe
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado. Ejecuta scripts/setup.sh primero."
    exit 1
fi

# Cargar variables de entorno
export $(cat .env | grep -v '^#' | xargs)

# Iniciar servicios con Docker Compose
print_status "Iniciando servicios..."
docker-compose up -d postgres redis

# Esperar a que los servicios estén listos
print_status "Esperando a que los servicios estén listos..."
sleep 5

# Si Go está instalado localmente, usar desarrollo local
if command -v go &> /dev/null; then
    print_status "Iniciando backend en modo desarrollo..."
    cd backend
    go mod tidy
    go run cmd/main.go &
    BACKEND_PID=$!
    cd ..
else
    print_status "Iniciando backend con Docker..."
    docker-compose up -d backend &
fi

# Si Node.js está instalado localmente, usar desarrollo local
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    print_status "Iniciando frontend en modo desarrollo..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        print_status "Instalando dependencias del frontend..."
        npm install
    fi
    npm start &
    FRONTEND_PID=$!
    cd ..
else
    print_status "Iniciando frontend con Docker..."
    docker-compose up -d frontend &
fi

print_status "✅ Entorno de desarrollo iniciado!"
print_status "Frontend: http://localhost:4200"
print_status "Backend API: http://localhost:8080"
print_status "Base de datos: localhost:5432"

# Función para limpiar procesos al salir
cleanup() {
    print_status "Deteniendo servicios de desarrollo..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    docker-compose down
}

# Configurar trap para limpiar al salir
trap cleanup EXIT

# Mantener el script ejecutándose
wait
"""
    
    start_script_path = os.path.join(root_dir, "scripts/development/start.sh")
    with open(start_script_path, "w", encoding="utf-8") as f:
        f.write(start_script_content)
    
    # Makefile actualizado
    makefile_content = """# Makefile para Plataforma de Gestión de Proyectos

.PHONY: help setup dev build test clean deploy

# Variables
PROJECT_NAME = project-management-platform
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.yml -f docker-compose.prod.yml

# Colores para output
GREEN = \\033[0;32m
YELLOW = \\033[1;33m
RED = \\033[0;31m
NC = \\033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\\n", $$1, $$2}'

setup: ## Configurar el proyecto por primera vez
	@echo "$(GREEN)Configurando proyecto...$(NC)"
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

setup-dev: ## Configurar con datos de ejemplo
	@echo "$(GREEN)Configurando proyecto con datos de ejemplo...$(NC)"
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh --with-sample-data

dev: ## Iniciar entorno de desarrollo
	@echo "$(GREEN)Iniciando entorno de desarrollo...$(NC)"
	@chmod +x scripts/development/start.sh
	@./scripts/development/start.sh

build: ## Construir todas las imágenes
	@echo "$(GREEN)Construyendo imágenes...$(NC)"
	@$(DOCKER_COMPOSE) build

build-prod: ## Construir imágenes para producción
	@echo "$(GREEN)Construyendo imágenes de producción...$(NC)"
	@$(DOCKER_COMPOSE_PROD) build

start: ## Iniciar todos los servicios
	@echo "$(GREEN)Iniciando servicios...$(NC)"
	@$(DOCKER_COMPOSE) up -d

stop: ## Detener todos los servicios
	@echo "$(YELLOW)Deteniendo servicios...$(NC)"
	@$(DOCKER_COMPOSE) down

restart: stop start ## Reiniciar todos los servicios

logs: ## Mostrar logs de todos los servicios
	@$(DOCKER_COMPOSE) logs -f

logs-backend: ## Mostrar logs del backend
	@$(DOCKER_COMPOSE) logs -f backend

logs-frontend: ## Mostrar logs del frontend
	@$(DOCKER_COMPOSE) logs -f frontend

logs-db: ## Mostrar logs de la base de datos
	@$(DOCKER_COMPOSE) logs -f postgres

shell-backend: ## Acceder al shell del backend
	@$(DOCKER_COMPOSE) exec backend sh

shell-frontend: ## Acceder al shell del frontend
	@$(DOCKER_COMPOSE) exec frontend sh

shell-db: ## Acceder al shell de la base de datos
	@$(DOCKER_COMPOSE) exec postgres psql -U postgres -d project_management

test: ## Ejecutar todas las pruebas
	@echo "$(GREEN)Ejecutando pruebas...$(NC)"
	@$(DOCKER_COMPOSE) exec backend go test ./...
	@$(DOCKER_COMPOSE) exec frontend npm test

test-backend: ## Ejecutar pruebas del backend
	@$(DOCKER_COMPOSE) exec backend go test ./...

test-frontend: ## Ejecutar pruebas del frontend
	@$(DOCKER_COMPOSE) exec frontend npm test

lint: ## Ejecutar linters
	@echo "$(GREEN)Ejecutando linters...$(NC)"
	@$(DOCKER_COMPOSE) exec backend golangci-lint run
	@$(DOCKER_COMPOSE) exec frontend npm run lint

format: ## Formatear código
	@echo "$(GREEN)Formateando código...$(NC)"
	@$(DOCKER_COMPOSE) exec backend go fmt ./...
	@$(DOCKER_COMPOSE) exec frontend npm run format

migrate: ## Ejecutar migraciones de base de datos
	@echo "$(GREEN)Ejecutando migraciones...$(NC)"
	@$(DOCKER_COMPOSE) exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/001_init.sql

migrate-dev: ## Ejecutar migraciones y cargar datos de desarrollo
	@echo "$(GREEN)Ejecutando migraciones y cargando datos de desarrollo...$(NC)"
	@$(DOCKER_COMPOSE) exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/001_init.sql
	@$(DOCKER_COMPOSE) exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/development.sql

backup: ## Crear backup de la base de datos
	@echo "$(GREEN)Creando backup...$(NC)"
	@chmod +x scripts/maintenance/backup.sh
	@./scripts/maintenance/backup.sh

clean: ## Limpiar contenedores, imágenes y volúmenes
	@echo "$(YELLOW)Limpiando recursos Docker...$(NC)"
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@docker system prune -f

clean-all: ## Limpiar todo incluyendo imágenes
	@echo "$(RED)Limpiando todos los recursos Docker...$(NC)"
	@$(DOCKER_COMPOSE) down -v --remove-orphans --rmi all
	@docker system prune -af

deploy-staging: ## Desplegar a staging
	@echo "$(GREEN)Desplegando a staging...$(NC)"
	@$(DOCKER_COMPOSE_PROD) up -d

deploy-prod: ## Desplegar a producción
	@echo "$(GREEN)Desplegando a producción...$(NC)"
	@$(DOCKER_COMPOSE_PROD) up -d

status: ## Mostrar estado de los servicios
	@$(DOCKER_COMPOSE) ps

health: ## Verificar salud de los servicios
	@echo "$(GREEN)Verificando salud de los servicios...$(NC)"
	@curl -f http://localhost:8080/api/v1/health || echo "$(RED)Backend no disponible$(NC)"
	@curl -f http://localhost:4200 || echo "$(RED)Frontend no disponible$(NC)"

install-deps: ## Instalar dependencias locales
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	@cd backend && go mod tidy
	@cd frontend && npm install

update-deps: ## Actualizar dependencias
	@echo "$(GREEN)Actualizando dependencias...$(NC)"
	@cd backend && go get -u ./...
	@cd frontend && npm update

# Comandos de desarrollo específicos
dev-backend: ## Iniciar solo el backend en desarrollo
	@cd backend && go run cmd/main.go

dev-frontend: ## Iniciar solo el frontend en desarrollo
	@cd frontend && npm start

dev-db: ## Iniciar solo la base de datos
	@$(DOCKER_COMPOSE) up -d postgres redis

# Comandos de utilidad
version: ## Mostrar versión del proyecto
	@echo "$(GREEN)Plataforma de Gestión de Proyectos v1.0.0$(NC)"

info: ## Mostrar información del proyecto
	@echo "$(GREEN)Información del proyecto:$(NC)"
	@echo "  Nombre: $(PROJECT_NAME)"
	@echo "  Frontend: http://localhost:4200"
	@echo "  Backend: http://localhost:8080"
	@echo "  Base de datos: localhost:5432"
	@echo "  Documentación: http://localhost:8080/docs"
"""
    
    makefile_path = os.path.join(root_dir, "Makefile")
    with open(makefile_path, "w", encoding="utf-8") as f:
        f.write(makefile_content)
    
    # Hacer ejecutables los scripts
    os.chmod(os.path.join(root_dir, "scripts/setup.sh"), 0o755)
    os.chmod(os.path.join(root_dir, "scripts/development/start.sh"), 0o755)
    
    print("✓ Scripts de inicialización creados")

if __name__ == "__main__":
    create_integration_config()
