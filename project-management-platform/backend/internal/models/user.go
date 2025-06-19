package models

import (
	"time"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type UserRole string

const (
	RoleAdmin     UserRole = "admin"
	RoleManager   UserRole = "manager"
	RoleDeveloper UserRole = "developer"
	RoleTester    UserRole = "tester"
	RoleViewer    UserRole = "viewer"
)

type User struct {
	BaseModel
	Email           string         `json:"email" gorm:"uniqueIndex;not null"`
	Username        string         `json:"username" gorm:"uniqueIndex;not null"`
	Password        string         `json:"-" gorm:"not null"`
	FirstName       string         `json:"first_name"`
	LastName        string         `json:"last_name"`
	Avatar          string         `json:"avatar"`
	Role            UserRole       `json:"role" gorm:"type:varchar(20);default:'developer'"`
	IsActive        bool           `json:"is_active" gorm:"default:true"`
	IsEmailVerified bool           `json:"is_email_verified" gorm:"default:false"`
	LastLoginAt     *time.Time     `json:"last_login_at"`
	Timezone        string         `json:"timezone" gorm:"default:'UTC'"`
	Language        string         `json:"language" gorm:"default:'es'"`
	
	// Relaciones
	ProjectMembers []ProjectMember `json:"project_members,omitempty"`
	AssignedTasks  []Task          `json:"assigned_tasks,omitempty" gorm:"foreignKey:AssigneeID"`
	CreatedTasks   []Task          `json:"created_tasks,omitempty" gorm:"foreignKey:CreatorID"`
	Comments       []Comment       `json:"comments,omitempty"`
	AuditLogs      []AuditLog      `json:"audit_logs,omitempty"`
}

type UserProfile struct {
	ID        uuid.UUID `json:"id"`
	Email     string    `json:"email"`
	Username  string    `json:"username"`
	FirstName string    `json:"first_name"`
	LastName  string    `json:"last_name"`
	Avatar    string    `json:"avatar"`
	Role      UserRole  `json:"role"`
	IsActive  bool      `json:"is_active"`
	Timezone  string    `json:"timezone"`
	Language  string    `json:"language"`
}

type CreateUserRequest struct {
	Email     string   `json:"email" binding:"required,email"`
	Username  string   `json:"username" binding:"required,min=3,max=50"`
	Password  string   `json:"password" binding:"required,min=6"`
	FirstName string   `json:"first_name" binding:"required"`
	LastName  string   `json:"last_name" binding:"required"`
	Role      UserRole `json:"role" binding:"required"`
}

type UpdateUserRequest struct {
	FirstName string   `json:"first_name,omitempty"`
	LastName  string   `json:"last_name,omitempty"`
	Avatar    string   `json:"avatar,omitempty"`
	Role      UserRole `json:"role,omitempty"`
	IsActive  *bool    `json:"is_active,omitempty"`
	Timezone  string   `json:"timezone,omitempty"`
	Language  string   `json:"language,omitempty"`
}

type ChangePasswordRequest struct {
	CurrentPassword string `json:"current_password" binding:"required"`
	NewPassword     string `json:"new_password" binding:"required,min=6"`
}

func (u *User) SetPassword(password string) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.Password = string(hashedPassword)
	return nil
}

func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	return err == nil
}

func (u *User) GetFullName() string {
	return u.FirstName + " " + u.LastName
}

func (u *User) ToProfile() *UserProfile {
	return &UserProfile{
		ID:        u.ID,
		Email:     u.Email,
		Username:  u.Username,
		FirstName: u.FirstName,
		LastName:  u.LastName,
		Avatar:    u.Avatar,
		Role:      u.Role,
		IsActive:  u.IsActive,
		Timezone:  u.Timezone,
		Language:  u.Language,
	}
}

func (u *User) HasRole(role UserRole) bool {
	return u.Role == role
}

func (u *User) IsAdminOrManager() bool {
	return u.Role == RoleAdmin || u.Role == RoleManager
}
