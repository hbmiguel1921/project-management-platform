package config

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
