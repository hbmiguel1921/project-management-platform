package main

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
