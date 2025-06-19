package services

import (
	"errors"
	"fmt"
	"time"

	"github.com/company/project-management-platform/internal/models"
	"github.com/golang-jwt/jwt/v4"
	"gorm.io/gorm"
)

type AuthService struct {
	db        *gorm.DB
	jwtSecret string
	accessDuration  time.Duration
	refreshDuration time.Duration
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

type LoginResponse struct {
	User         *models.UserProfile `json:"user"`
	AccessToken  string              `json:"access_token"`
	RefreshToken string              `json:"refresh_token"`
	ExpiresAt    time.Time           `json:"expires_at"`
}

type TokenClaims struct {
	UserID   string `json:"user_id"`
	Username string `json:"username"`
	Role     string `json:"role"`
	jwt.RegisteredClaims
}

func NewAuthService(db *gorm.DB, jwtSecret string, accessDuration, refreshDuration time.Duration) *AuthService {
	return &AuthService{
		db:              db,
		jwtSecret:       jwtSecret,
		accessDuration:  accessDuration,
		refreshDuration: refreshDuration,
	}
}

func (s *AuthService) Login(req *LoginRequest) (*LoginResponse, error) {
	var user models.User
	if err := s.db.Where("email = ? AND is_active = ?", req.Email, true).First(&user).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, errors.New("credenciales inválidas")
		}
		return nil, err
	}

	if !user.CheckPassword(req.Password) {
		return nil, errors.New("credenciales inválidas")
	}

	// Actualizar último login
	now := time.Now()
	user.LastLoginAt = &now
	s.db.Save(&user)

	// Generar tokens
	accessToken, err := s.generateAccessToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando access token: %w", err)
	}

	refreshToken, err := s.generateRefreshToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando refresh token: %w", err)
	}

	return &LoginResponse{
		User:         user.ToProfile(),
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    time.Now().Add(s.accessDuration),
	}, nil
}

func (s *AuthService) Register(req *models.CreateUserRequest) (*models.UserProfile, error) {
	// Verificar si el email ya existe
	var existingUser models.User
	if err := s.db.Where("email = ?", req.Email).First(&existingUser).Error; err == nil {
		return nil, errors.New("el email ya está registrado")
	}

	// Verificar si el username ya existe
	if err := s.db.Where("username = ?", req.Username).First(&existingUser).Error; err == nil {
		return nil, errors.New("el username ya está registrado")
	}

	// Crear nuevo usuario
	user := &models.User{
		Email:     req.Email,
		Username:  req.Username,
		FirstName: req.FirstName,
		LastName:  req.LastName,
		Role:      req.Role,
		IsActive:  true,
	}

	if err := user.SetPassword(req.Password); err != nil {
		return nil, fmt.Errorf("error configurando password: %w", err)
	}

	if err := s.db.Create(user).Error; err != nil {
		return nil, fmt.Errorf("error creando usuario: %w", err)
	}

	return user.ToProfile(), nil
}

func (s *AuthService) RefreshToken(refreshToken string) (*LoginResponse, error) {
	claims, err := s.validateToken(refreshToken)
	if err != nil {
		return nil, fmt.Errorf("token inválido: %w", err)
	}

	var user models.User
	if err := s.db.Where("id = ? AND is_active = ?", claims.UserID, true).First(&user).Error; err != nil {
		return nil, errors.New("usuario no encontrado")
	}

	// Generar nuevos tokens
	accessToken, err := s.generateAccessToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando access token: %w", err)
	}

	newRefreshToken, err := s.generateRefreshToken(&user)
	if err != nil {
		return nil, fmt.Errorf("error generando refresh token: %w", err)
	}

	return &LoginResponse{
		User:         user.ToProfile(),
		AccessToken:  accessToken,
		RefreshToken: newRefreshToken,
		ExpiresAt:    time.Now().Add(s.accessDuration),
	}, nil
}

func (s *AuthService) ValidateToken(tokenString string) (*TokenClaims, error) {
	return s.validateToken(tokenString)
}

func (s *AuthService) generateAccessToken(user *models.User) (string, error) {
	claims := &TokenClaims{
		UserID:   user.ID.String(),
		Username: user.Username,
		Role:     string(user.Role),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.accessDuration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   user.ID.String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.jwtSecret))
}

func (s *AuthService) generateRefreshToken(user *models.User) (string, error) {
	claims := &TokenClaims{
		UserID:   user.ID.String(),
		Username: user.Username,
		Role:     string(user.Role),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.refreshDuration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   user.ID.String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.jwtSecret))
}

func (s *AuthService) validateToken(tokenString string) (*TokenClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &TokenClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("método de firma inesperado: %v", token.Header["alg"])
		}
		return []byte(s.jwtSecret), nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*TokenClaims)
	if !ok || !token.Valid {
		return nil, errors.New("token inválido")
	}

	return claims, nil
}

func (s *AuthService) GetUserByID(userID string) (*models.User, error) {
	var user models.User
	if err := s.db.Where("id = ? AND is_active = ?", userID, true).First(&user).Error; err != nil {
		return nil, err
	}
	return &user, nil
}

func (s *AuthService) ChangePassword(userID string, req *models.ChangePasswordRequest) error {
	var user models.User
	if err := s.db.Where("id = ?", userID).First(&user).Error; err != nil {
		return err
	}

	if !user.CheckPassword(req.CurrentPassword) {
		return errors.New("contraseña actual incorrecta")
	}

	if err := user.SetPassword(req.NewPassword); err != nil {
		return fmt.Errorf("error configurando nueva contraseña: %w", err)
	}

	return s.db.Save(&user).Error
}
