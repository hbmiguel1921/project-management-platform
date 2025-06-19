package middleware

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
