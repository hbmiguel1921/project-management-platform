package routes

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
