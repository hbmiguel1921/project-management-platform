# Makefile para Plataforma de Gestión de Proyectos

.PHONY: help setup dev build test clean deploy

# Variables
PROJECT_NAME = project-management-platform
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.yml -f docker-compose.prod.yml

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

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
