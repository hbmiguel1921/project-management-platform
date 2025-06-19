package unit

import (
	"testing"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/company/project-management-platform/internal/services"
	"github.com/stretchr/testify/assert"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDB() *gorm.DB {
	db, _ := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	db.AutoMigrate(&models.User{})
	return db
}

func TestAuthService_Login(t *testing.T) {
	db := setupTestDB()
	authService := services.NewAuthService(db, "test-secret", time.Hour, time.Hour*24)

	// Crear usuario de prueba
	user := &models.User{
		Email:     "test@example.com",
		Username:  "testuser",
		FirstName: "Test",
		LastName:  "User",
		Role:      models.RoleDeveloper,
		IsActive:  true,
	}
	user.SetPassword("password123")
	db.Create(user)

	// Test login exitoso
	loginReq := &services.LoginRequest{
		Email:    "test@example.com",
		Password: "password123",
	}

	response, err := authService.Login(loginReq)
	assert.NoError(t, err)
	assert.NotNil(t, response)
	assert.Equal(t, "testuser", response.User.Username)
	assert.NotEmpty(t, response.AccessToken)
	assert.NotEmpty(t, response.RefreshToken)

	// Test login con credenciales incorrectas
	loginReq.Password = "wrongpassword"
	response, err = authService.Login(loginReq)
	assert.Error(t, err)
	assert.Nil(t, response)
}

func TestAuthService_Register(t *testing.T) {
	db := setupTestDB()
	authService := services.NewAuthService(db, "test-secret", time.Hour, time.Hour*24)

	// Test registro exitoso
	registerReq := &models.CreateUserRequest{
		Email:     "newuser@example.com",
		Username:  "newuser",
		Password:  "password123",
		FirstName: "New",
		LastName:  "User",
		Role:      models.RoleDeveloper,
	}

	user, err := authService.Register(registerReq)
	assert.NoError(t, err)
	assert.NotNil(t, user)
	assert.Equal(t, "newuser", user.Username)

	// Test registro con email duplicado
	_, err = authService.Register(registerReq)
	assert.Error(t, err)
}
