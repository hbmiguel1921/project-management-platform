package api

import (
	"net/http"
	"time"

	"github.com/company/project-management-platform/internal/api/handlers"
	"github.com/company/project-management-platform/internal/api/middleware"
	"github.com/company/project-management-platform/internal/config"
	"github.com/company/project-management-platform/internal/services"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func SetupRouter(db *gorm.DB, cfg *config.Config) *gin.Engine {
	router := gin.New()

	// Middleware global
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	// CORS
	corsConfig := cors.Config{
		AllowOrigins:     cfg.Server.CorsOrigins,
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}
	router.Use(cors.New(corsConfig))

	// Inicializar servicios
	authService := services.NewAuthService(
		db,
		cfg.JWT.Secret,
		time.Duration(cfg.JWT.AccessDuration)*time.Second,
		time.Duration(cfg.JWT.RefreshDuration)*time.Second,
	)

	projectService := services.NewProjectService(db)
	taskService := services.NewTaskService(db)
	userService := services.NewUserService(db)

	// Inicializar handlers
	authHandler := handlers.NewAuthHandler(authService)
	projectHandler := handlers.NewProjectHandler(projectService)
	taskHandler := handlers.NewTaskHandler(taskService)
	userHandler := handlers.NewUserHandler(userService)

	// Middleware de autenticación
	authMiddleware := middleware.NewAuthMiddleware(authService)

	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  "ok",
			"service": "project-management-api",
			"version": cfg.App.Version,
			"time":    time.Now().UTC(),
		})
	})

	// Rutas públicas
	v1 := router.Group("/api/v1")
	{
		auth := v1.Group("/auth")
		{
			auth.POST("/login", authHandler.Login)
			auth.POST("/register", authHandler.Register)
			auth.POST("/refresh", authHandler.RefreshToken)
		}
	}

	// Rutas protegidas
	protected := v1.Group("/")
	protected.Use(authMiddleware.RequireAuth())
	{
		// Auth routes protegidas
		authProtected := protected.Group("/auth")
		{
			authProtected.GET("/me", authHandler.GetProfile)
			authProtected.PUT("/me", authHandler.UpdateProfile)
			authProtected.POST("/change-password", authHandler.ChangePassword)
			authProtected.POST("/logout", authHandler.Logout)
		}

		// User routes
		users := protected.Group("/users")
		{
			users.GET("", userHandler.GetUsers)
			users.GET("/:id", userHandler.GetUser)
			users.PUT("/:id", userHandler.UpdateUser)
			users.DELETE("/:id", userHandler.DeleteUser)
		}

		// Project routes
		projects := protected.Group("/projects")
		{
			projects.GET("", projectHandler.GetProjects)
			projects.POST("", projectHandler.CreateProject)
			projects.GET("/:id", projectHandler.GetProject)
			projects.PUT("/:id", projectHandler.UpdateProject)
			projects.DELETE("/:id", projectHandler.DeleteProject)
			projects.GET("/:id/dashboard", projectHandler.GetProjectDashboard)
			
			// Project members
			projects.GET("/:id/members", projectHandler.GetProjectMembers)
			projects.POST("/:id/members", projectHandler.AddProjectMember)
			projects.PUT("/:id/members/:user_id", projectHandler.UpdateProjectMember)
			projects.DELETE("/:id/members/:user_id", projectHandler.RemoveProjectMember)
		}

		// Task routes
		tasks := protected.Group("/tasks")
		{
			tasks.GET("", taskHandler.GetTasks)
			tasks.POST("", taskHandler.CreateTask)
			tasks.GET("/:id", taskHandler.GetTask)
			tasks.PUT("/:id", taskHandler.UpdateTask)
			tasks.DELETE("/:id", taskHandler.DeleteTask)
			tasks.POST("/:id/comments", taskHandler.AddComment)
			tasks.GET("/:id/comments", taskHandler.GetComments)
		}

		// Project-specific task routes
		projectTasks := protected.Group("/projects/:project_id/tasks")
		{
			projectTasks.GET("", taskHandler.GetProjectTasks)
			projectTasks.POST("", taskHandler.CreateProjectTask)
		}
	}

	return router
}
