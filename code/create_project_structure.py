#!/usr/bin/env python3
"""
Script para crear la estructura completa del repositorio de la plataforma de gestión de proyectos
según las mejores prácticas de desarrollo de software.
"""

import os
import subprocess
import json
from pathlib import Path

def run_command(command, cwd=None):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {command}")
        print(f"Error: {e.stderr}")
        return None

def create_project_structure():
    """Crear la estructura completa del repositorio"""
    
    # Directorio raíz del proyecto
    project_root = "/workspace/project-management-platform"
    
    # Crear directorio principal
    os.makedirs(project_root, exist_ok=True)
    
    # Estructura de directorios
    directories = [
        # Documentación
        "docs",
        "docs/architecture",
        "docs/api",
        "docs/user-guides",
        "docs/deployment",
        
        # Frontend Angular
        "frontend",
        
        # Backend Golang
        "backend",
        "backend/cmd",
        "backend/internal",
        "backend/internal/api",
        "backend/internal/api/handlers",
        "backend/internal/api/middleware",
        "backend/internal/api/routes",
        "backend/internal/config",
        "backend/internal/database",
        "backend/internal/database/migrations",
        "backend/internal/models",
        "backend/internal/services",
        "backend/internal/utils",
        "backend/internal/websocket",
        "backend/pkg",
        "backend/tests",
        "backend/tests/integration",
        "backend/tests/unit",
        
        # Base de datos
        "database",
        "database/migrations",
        "database/seeds",
        "database/backups",
        
        # Deployment y DevOps
        "deployment",
        "deployment/docker",
        "deployment/kubernetes",
        "deployment/scripts",
        "deployment/nginx",
        
        # Scripts y herramientas
        "scripts",
        "scripts/development",
        "scripts/deployment",
        "scripts/maintenance",
        
        # Configuración
        "configs",
        "configs/development",
        "configs/production",
        "configs/testing",
        
        # Tests e2e
        "tests",
        "tests/e2e",
        "tests/performance",
        
        # Assets y recursos
        "assets",
        "assets/images",
        "assets/templates",
        
        # Logs
        "logs",
    ]
    
    # Crear todos los directorios
    for directory in directories:
        dir_path = os.path.join(project_root, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Creado directorio: {directory}")
    
    return project_root

def create_root_files(project_root):
    """Crear archivos en la raíz del proyecto"""
    
    # README.md principal
    readme_content = """# Plataforma de Gestión de Proyectos de Software

Una plataforma completa de gestión de proyectos diseñada específicamente para equipos de desarrollo de software.

## Características Principales

- 🎯 **Gestión Ágil**: Soporte completo para Scrum y Kanban
- 📊 **Tableros Visuales**: Tableros Kanban/Scrum con drag & drop
- 📈 **Reportes Avanzados**: Analytics y métricas detalladas
- 💬 **Colaboración**: Chat integrado y comentarios en tiempo real
- 🔗 **Integraciones**: GitHub/GitLab, CI/CD, y más
- 🔒 **Seguridad**: SSO, 2FA y control de acceso granular
- 🌐 **Deployment Híbrido**: Cloud o on-premise

## Stack Tecnológico

- **Frontend**: Angular 17+ con PrimeNG
- **Backend**: Golang con Gin Framework
- **Base de Datos**: PostgreSQL
- **Tiempo Real**: WebSockets
- **Contenedores**: Docker & Docker Compose

## Estructura del Proyecto

```
├── frontend/          # Aplicación Angular
├── backend/           # API en Golang
├── database/          # Esquemas y migraciones
├── deployment/        # Configuración de deployment
├── docs/             # Documentación
├── scripts/          # Scripts de automatización
└── tests/            # Tests end-to-end
```

## Inicio Rápido

### Prerrequisitos
- Node.js 18+
- Go 1.21+
- PostgreSQL 15+
- Docker & Docker Compose

### Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd project-management-platform
   ```

2. **Levantar servicios con Docker**
   ```bash
   docker-compose up -d
   ```

3. **Instalar dependencias del frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Ejecutar el backend**
   ```bash
   cd backend
   go mod tidy
   go run cmd/main.go
   ```

### URLs de Desarrollo
- Frontend: http://localhost:4200
- Backend API: http://localhost:8080
- PostgreSQL: localhost:5432

## Deployment

### Docker Compose (Recomendado para desarrollo)
```bash
docker-compose up -d
```

### Kubernetes (Producción)
```bash
kubectl apply -f deployment/kubernetes/
```

### Manual
Ver guías detalladas en `/docs/deployment/`

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Soporte

- 📚 [Documentación](docs/)
- 🐛 [Reportar Bug](issues/)
- 💡 [Solicitar Feature](issues/)
- 📧 Email: support@projectmanagement.com
"""
    
    with open(os.path.join(project_root, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # .gitignore principal
    gitignore_content = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node_modules
node_modules/
*/node_modules/

# IDEs and editors
/.idea
.project
.classpath
.c9/
*.launch
.settings/
*.sublime-workspace

# IDE - VSCode
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history/*

# misc
/.sass-cache
/connect.lock
/coverage
/libpeerconnection.log
testem.log
/typings

# System Files
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Go
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go build
/dist/
/backend/dist/
/backend/bin/

# Go workspace file
go.work

# Database
*.db
*.sqlite
*.sqlite3

# Docker
docker-compose.override.yml

# Logs
/logs/
*.log

# Backups
/database/backups/*
!/database/backups/.gitkeep

# Temporary files
/tmp/
.tmp/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Local development
/configs/local.yaml
/configs/development/local.yaml
"""
    
    with open(os.path.join(project_root, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    # docker-compose.yml
    docker_compose_content = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: pm_postgres
    environment:
      POSTGRES_DB: project_management
      POSTGRES_USER: pm_user
      POSTGRES_PASSWORD: pm_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/migrations:/docker-entrypoint-initdb.d
    networks:
      - pm_network

  redis:
    image: redis:7-alpine
    container_name: pm_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - pm_network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: pm_backend
    environment:
      - DB_HOST=postgres
      - DB_USER=pm_user
      - DB_PASSWORD=pm_password
      - DB_NAME=project_management
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - JWT_SECRET=your-super-secret-jwt-key
      - APP_ENV=development
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
      - ./logs:/app/logs
    networks:
      - pm_network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: pm_frontend
    ports:
      - "4200:4200"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - pm_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: pm_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deployment/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./deployment/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - pm_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  pm_network:
    driver: bridge
"""
    
    with open(os.path.join(project_root, "docker-compose.yml"), "w", encoding="utf-8") as f:
        f.write(docker_compose_content)
    
    # Makefile para automatización
    makefile_content = """# Makefile para Plataforma de Gestión de Proyectos

.PHONY: help install start stop build test clean deploy

# Variables
FRONTEND_DIR := frontend
BACKEND_DIR := backend
DOCKER_COMPOSE := docker-compose

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-30s\\033[0m %s\\n", $$1, $$2}'

install: ## Instalar todas las dependencias
	@echo "Instalando dependencias del frontend..."
	cd $(FRONTEND_DIR) && npm install
	@echo "Instalando dependencias del backend..."
	cd $(BACKEND_DIR) && go mod tidy
	@echo "✓ Dependencias instaladas"

start: ## Iniciar todos los servicios en desarrollo
	$(DOCKER_COMPOSE) up -d postgres redis
	@echo "Esperando que PostgreSQL esté listo..."
	sleep 5
	cd $(BACKEND_DIR) && go run cmd/main.go &
	cd $(FRONTEND_DIR) && npm start &
	@echo "✓ Servicios iniciados"

start-docker: ## Iniciar todos los servicios con Docker
	$(DOCKER_COMPOSE) up -d
	@echo "✓ Servicios Docker iniciados"

stop: ## Detener todos los servicios
	$(DOCKER_COMPOSE) down
	pkill -f "go run cmd/main.go" || true
	pkill -f "ng serve" || true
	@echo "✓ Servicios detenidos"

build: ## Construir aplicaciones para producción
	cd $(FRONTEND_DIR) && npm run build
	cd $(BACKEND_DIR) && go build -o bin/main cmd/main.go
	@echo "✓ Aplicaciones construidas"

test: ## Ejecutar todos los tests
	cd $(FRONTEND_DIR) && npm run test
	cd $(BACKEND_DIR) && go test ./...
	@echo "✓ Tests ejecutados"

test-e2e: ## Ejecutar tests end-to-end
	cd tests/e2e && npm run test
	@echo "✓ Tests E2E ejecutados"

lint: ## Ejecutar linting en ambos proyectos
	cd $(FRONTEND_DIR) && npm run lint
	cd $(BACKEND_DIR) && golangci-lint run
	@echo "✓ Linting completado"

clean: ## Limpiar archivos generados
	cd $(FRONTEND_DIR) && rm -rf dist/ node_modules/
	cd $(BACKEND_DIR) && rm -rf bin/ vendor/
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
	@echo "✓ Limpieza completada"

migrate: ## Ejecutar migraciones de base de datos
	cd $(BACKEND_DIR) && go run cmd/migrate.go
	@echo "✓ Migraciones ejecutadas"

seed: ## Poblar base de datos con datos de prueba
	cd $(BACKEND_DIR) && go run cmd/seed.go
	@echo "✓ Datos de prueba insertados"

deploy-dev: ## Deploy a entorno de desarrollo
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "✓ Deploy de desarrollo completado"

deploy-prod: ## Deploy a entorno de producción
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✓ Deploy de producción completado"

logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Ver logs del backend
	$(DOCKER_COMPOSE) logs -f backend

logs-frontend: ## Ver logs del frontend
	$(DOCKER_COMPOSE) logs -f frontend

backup: ## Crear backup de la base de datos
	./scripts/maintenance/backup.sh
	@echo "✓ Backup creado"

restore: ## Restaurar backup de la base de datos
	./scripts/maintenance/restore.sh
	@echo "✓ Backup restaurado"
"""
    
    with open(os.path.join(project_root, "Makefile"), "w", encoding="utf-8") as f:
        f.write(makefile_content)
    
    print("✓ Archivos raíz creados")
    return True

def create_backend_project(project_root):
    """Crear estructura y archivos del backend en Golang"""
    
    backend_dir = os.path.join(project_root, "backend")
    
    # go.mod
    go_mod_content = """module github.com/company/project-management-platform

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/gin-contrib/cors v1.4.0
	github.com/golang-jwt/jwt/v4 v4.5.0
	github.com/gorilla/websocket v1.5.0
	gorm.io/gorm v1.25.4
	gorm.io/driver/postgres v1.5.2
	github.com/go-redis/redis/v8 v8.11.5
	github.com/spf13/viper v1.16.0
	github.com/stretchr/testify v1.8.4
	golang.org/x/crypto v0.14.0
	github.com/google/uuid v1.3.1
)
"""
    
    with open(os.path.join(backend_dir, "go.mod"), "w", encoding="utf-8") as f:
        f.write(go_mod_content)
    
    # main.go
    main_go_content = """package main

import (
	"log"
	"os"

	"github.com/company/project-management-platform/internal/api"
	"github.com/company/project-management-platform/internal/config"
	"github.com/company/project-management-platform/internal/database"
	"github.com/gin-gonic/gin"
)

func main() {
	// Cargar configuración
	cfg, err := config.Load()
	if err != nil {
		log.Fatal("Error cargando configuración:", err)
	}

	// Conectar a la base de datos
	db, err := database.Connect(cfg.Database)
	if err != nil {
		log.Fatal("Error conectando a la base de datos:", err)
	}

	// Ejecutar migraciones
	if err := database.Migrate(db); err != nil {
		log.Fatal("Error ejecutando migraciones:", err)
	}

	// Configurar Gin según el entorno
	if cfg.App.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	// Inicializar API
	router := api.SetupRouter(db, cfg)

	// Obtener puerto del entorno o usar por defecto
	port := os.Getenv("PORT")
	if port == "" {
		port = cfg.Server.Port
	}

	log.Printf("Servidor iniciando en puerto %s", port)
	log.Fatal(router.Run(":" + port))
}
"""
    
    with open(os.path.join(backend_dir, "cmd", "main.go"), "w", encoding="utf-8") as f:
        f.write(main_go_content)
    
    # Dockerfile del backend
    dockerfile_content = """FROM golang:1.21-alpine AS builder

WORKDIR /app

# Instalar dependencias del sistema
RUN apk add --no-cache git

# Copiar archivos de go modules
COPY go.mod go.sum ./
RUN go mod download

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main cmd/main.go

# Imagen final
FROM alpine:latest

RUN apk --no-cache add ca-certificates
WORKDIR /root/

# Copiar el binario
COPY --from=builder /app/main .

# Exponer puerto
EXPOSE 8080

# Comando por defecto
CMD ["./main"]
"""
    
    with open(os.path.join(backend_dir, "Dockerfile"), "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    print("✓ Estructura del backend creada")
    return True

def create_frontend_project(project_root):
    """Crear proyecto Angular con PrimeNG"""
    
    frontend_dir = os.path.join(project_root, "frontend")
    
    # Navegar al directorio frontend
    os.chdir(frontend_dir)
    
    # Verificar si Angular CLI está instalado
    print("Verificando Angular CLI...")
    result = run_command("ng version")
    if result is None:
        print("Instalando Angular CLI...")
        run_command("npm install -g @angular/cli@17")
    
    # Crear proyecto Angular
    print("Creando proyecto Angular...")
    run_command(f"ng new project-management-app --routing=true --style=scss --skip-git=true --directory=.")
    
    # Instalar PrimeNG y dependencias
    print("Instalando PrimeNG y dependencias...")
    run_command("npm install primeng primeicons")
    run_command("npm install @angular/animations")
    run_command("npm install @angular/cdk")
    run_command("npm install chart.js")
    run_command("npm install socket.io-client")
    run_command("npm install @types/socket.io-client")
    run_command("npm install ngx-socket-io")
    
    # Instalar dependencias de desarrollo
    run_command("npm install --save-dev @types/chart.js")
    
    # package.json personalizado
    package_json = {
        "name": "project-management-frontend",
        "version": "1.0.0",
        "scripts": {
            "ng": "ng",
            "start": "ng serve --host 0.0.0.0 --port 4200",
            "build": "ng build",
            "build:prod": "ng build --configuration production",
            "watch": "ng build --watch --configuration development",
            "test": "ng test",
            "test:ci": "ng test --watch=false --browsers=ChromeHeadless",
            "lint": "ng lint",
            "e2e": "ng e2e"
        },
        "dependencies": {
            "@angular/animations": "^17.0.0",
            "@angular/cdk": "^17.0.0",
            "@angular/common": "^17.0.0",
            "@angular/compiler": "^17.0.0",
            "@angular/core": "^17.0.0",
            "@angular/forms": "^17.0.0",
            "@angular/platform-browser": "^17.0.0",
            "@angular/platform-browser-dynamic": "^17.0.0",
            "@angular/router": "^17.0.0",
            "chart.js": "^4.4.0",
            "ngx-socket-io": "^4.7.0",
            "primeicons": "^6.0.1",
            "primeng": "^17.0.0",
            "rxjs": "~7.8.0",
            "socket.io-client": "^4.7.2",
            "tslib": "^2.3.0",
            "zone.js": "~0.14.0"
        },
        "devDependencies": {
            "@angular-devkit/build-angular": "^17.0.0",
            "@angular/cli": "^17.0.0",
            "@angular/compiler-cli": "^17.0.0",
            "@types/jasmine": "~5.1.0",
            "@types/chart.js": "^2.9.41",
            "@types/socket.io-client": "^3.0.0",
            "jasmine-core": "~5.1.0",
            "karma": "~6.4.0",
            "karma-chrome-headless": "~3.1.0",
            "karma-coverage": "~2.2.0",
            "karma-jasmine": "~5.1.0",
            "karma-jasmine-html-reporter": "~2.1.0",
            "typescript": "~5.2.0"
        }
    }
    
    with open("package.json", "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)
    
    # Dockerfile del frontend
    dockerfile_content = """FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de package
COPY package*.json ./
RUN npm ci

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build:prod

# Imagen final con Nginx
FROM nginx:alpine

# Copiar archivos construidos
COPY --from=builder /app/dist/project-management-app /usr/share/nginx/html

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"""
    
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    # nginx.conf para el frontend
    nginx_conf_content = """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Configuración para Angular routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache para assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Configuración para API proxy (desarrollo)
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket para tiempo real
    location /ws/ {
        proxy_pass http://backend:8080/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    
    with open("nginx.conf", "w", encoding="utf-8") as f:
        f.write(nginx_conf_content)
    
    print("✓ Proyecto Angular con PrimeNG creado")
    return True

def create_database_setup(project_root):
    """Crear setup de base de datos PostgreSQL"""
    
    # Script de inicialización de BD
    init_sql_content = """-- Inicialización de la base de datos para Project Management Platform

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Crear esquemas
CREATE SCHEMA IF NOT EXISTS project_management;
CREATE SCHEMA IF NOT EXISTS audit;

-- Configurar búsqueda de esquemas
SET search_path TO project_management, public;

-- Crear usuario para la aplicación si no existe
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pm_app') THEN
      CREATE ROLE pm_app WITH LOGIN PASSWORD 'pm_app_password';
   END IF;
END
$$;

-- Otorgar permisos
GRANT USAGE ON SCHEMA project_management TO pm_app;
GRANT CREATE ON SCHEMA project_management TO pm_app;
GRANT USAGE ON SCHEMA audit TO pm_app;
GRANT CREATE ON SCHEMA audit TO pm_app;

-- Configurar timezone por defecto
SET timezone = 'UTC';
"""
    
    db_dir = os.path.join(project_root, "database", "migrations")
    with open(os.path.join(db_dir, "001_init.sql"), "w", encoding="utf-8") as f:
        f.write(init_sql_content)
    
    # Docker compose override para desarrollo
    docker_dev_content = """version: '3.8'

services:
  postgres:
    environment:
      POSTGRES_DB: project_management_dev
      POSTGRES_USER: pm_dev_user
      POSTGRES_PASSWORD: pm_dev_password
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  backend:
    environment:
      - APP_ENV=development
      - DB_HOST=postgres
      - DB_USER=pm_dev_user
      - DB_PASSWORD=pm_dev_password
      - DB_NAME=project_management_dev
      - LOG_LEVEL=debug
    volumes:
      - ./backend:/app
      - /app/vendor
    command: ["go", "run", "cmd/main.go"]

  frontend:
    environment:
      - NODE_ENV=development
    command: ["npm", "run", "start"]

volumes:
  postgres_dev_data:
"""
    
    with open(os.path.join(project_root, "docker-compose.dev.yml"), "w", encoding="utf-8") as f:
        f.write(docker_dev_content)
    
    print("✓ Configuración de base de datos creada")
    return True

def create_scripts(project_root):
    """Crear scripts de automatización"""
    
    scripts_dir = os.path.join(project_root, "scripts")
    
    # Script de desarrollo
    dev_script_content = """#!/bin/bash
# Script para iniciar el entorno de desarrollo

set -e

echo "🚀 Iniciando entorno de desarrollo..."

# Verificar prerequisitos
command -v docker >/dev/null 2>&1 || { echo "❌ Docker no está instalado"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose no está instalado"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js no está instalado"; exit 1; }
command -v go >/dev/null 2>&1 || { echo "❌ Go no está instalado"; exit 1; }

echo "✅ Prerequisitos verificados"

# Levantar servicios base
echo "📦 Iniciando servicios base (PostgreSQL, Redis)..."
docker-compose up -d postgres redis

# Esperar que PostgreSQL esté listo
echo "⏳ Esperando que PostgreSQL esté listo..."
until docker-compose exec postgres pg_isready -U pm_user -d project_management; do
  sleep 1
done

echo "✅ PostgreSQL está listo"

# Instalar dependencias si es necesario
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    cd frontend && npm install && cd ..
fi

if [ ! -f "backend/go.sum" ]; then
    echo "📦 Instalando dependencias del backend..."
    cd backend && go mod tidy && cd ..
fi

echo "🎉 Entorno de desarrollo listo!"
echo ""
echo "Para iniciar las aplicaciones:"
echo "  Backend:  cd backend && go run cmd/main.go"
echo "  Frontend: cd frontend && npm start"
echo ""
echo "URLs:"
echo "  Frontend: http://localhost:4200"
echo "  Backend:  http://localhost:8080"
echo "  BD:       postgresql://pm_user:pm_password@localhost:5432/project_management"
"""
    
    dev_script_path = os.path.join(scripts_dir, "development", "start.sh")
    os.makedirs(os.path.dirname(dev_script_path), exist_ok=True)
    with open(dev_script_path, "w", encoding="utf-8") as f:
        f.write(dev_script_content)
    os.chmod(dev_script_path, 0o755)
    
    # Script de backup
    backup_script_content = """#!/bin/bash
# Script para crear backup de la base de datos

set -e

BACKUP_DIR="database/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "🗄️  Creando backup de la base de datos..."

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

# Crear backup
docker-compose exec -T postgres pg_dump -U pm_user project_management > $BACKUP_FILE

# Comprimir backup
gzip $BACKUP_FILE

echo "✅ Backup creado: $BACKUP_FILE.gz"

# Limpiar backups antiguos (mantener últimos 10)
cd $BACKUP_DIR
ls -t *.gz | tail -n +11 | xargs --no-run-if-empty rm

echo "🧹 Backups antiguos limpiados"
"""
    
    backup_script_path = os.path.join(scripts_dir, "maintenance", "backup.sh")
    os.makedirs(os.path.dirname(backup_script_path), exist_ok=True)
    with open(backup_script_path, "w", encoding="utf-8") as f:
        f.write(backup_script_content)
    os.chmod(backup_script_path, 0o755)
    
    print("✓ Scripts de automatización creados")
    return True

def create_deployment_configs(project_root):
    """Crear configuraciones de deployment"""
    
    deployment_dir = os.path.join(project_root, "deployment")
    
    # Nginx principal
    nginx_config_content = """events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8080;
    }

    upstream frontend {
        server frontend:4200;
    }

    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Configuración de proxy
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # Servidor principal
    server {
        listen 80;
        server_name localhost;

        # Redirect HTTP to HTTPS en producción
        # return 301 https://$server_name$request_uri;

        # Frontend
        location / {
            proxy_pass http://frontend;
        }

        # API Backend
        location /api/ {
            proxy_pass http://backend/api/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_cache_bypass $http_upgrade;
        }

        # WebSocket
        location /ws/ {
            proxy_pass http://backend/ws/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check
        location /health {
            proxy_pass http://backend/health;
        }
    }

    # Servidor HTTPS (descomenta para producción)
    # server {
    #     listen 443 ssl;
    #     server_name your-domain.com;
    #     
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #     
    #     location / {
    #         proxy_pass http://frontend;
    #     }
    #     
    #     location /api/ {
    #         proxy_pass http://backend/api/;
    #     }
    # }
}
"""
    
    nginx_config_path = os.path.join(deployment_dir, "nginx", "nginx.conf")
    os.makedirs(os.path.dirname(nginx_config_path), exist_ok=True)
    with open(nginx_config_path, "w", encoding="utf-8") as f:
        f.write(nginx_config_content)
    
    # Docker compose para producción
    docker_prod_content = """version: '3.8'

services:
  postgres:
    environment:
      POSTGRES_DB: project_management_prod
      POSTGRES_USER: pm_prod_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
      - ./database/backups:/backups
    restart: always

  redis:
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}

  backend:
    environment:
      - APP_ENV=production
      - DB_HOST=postgres
      - DB_USER=pm_prod_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=project_management_prod
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - JWT_SECRET=${JWT_SECRET}
      - LOG_LEVEL=info
    restart: always

  frontend:
    environment:
      - NODE_ENV=production
    restart: always

  nginx:
    restart: always

volumes:
  postgres_prod_data:
"""
    
    with open(os.path.join(project_root, "docker-compose.prod.yml"), "w", encoding="utf-8") as f:
        f.write(docker_prod_content)
    
    # Archivo de variables de entorno template
    env_template_content = """# Configuración de entorno - Copiar a .env y modificar

# Base de datos
DB_PASSWORD=your-secure-database-password
DB_HOST=postgres
DB_USER=pm_prod_user
DB_NAME=project_management_prod

# Redis
REDIS_PASSWORD=your-secure-redis-password
REDIS_HOST=redis
REDIS_PORT=6379

# Aplicación
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
APP_ENV=production
LOG_LEVEL=info

# Servicios externos (opcional)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password

# SSL (opcional)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
"""
    
    with open(os.path.join(project_root, ".env.template"), "w", encoding="utf-8") as f:
        f.write(env_template_content)
    
    print("✓ Configuraciones de deployment creadas")
    return True

def main():
    """Función principal"""
    print("🚀 Creando estructura completa del proyecto...")
    print("=" * 60)
    
    # Crear estructura base
    project_root = create_project_structure()
    print(f"📁 Proyecto creado en: {project_root}")
    
    # Crear archivos raíz
    create_root_files(project_root)
    
    # Crear backend
    create_backend_project(project_root)
    
    # Crear frontend
    create_frontend_project(project_root)
    
    # Configurar base de datos
    create_database_setup(project_root)
    
    # Crear scripts
    create_scripts(project_root)
    
    # Configuraciones de deployment
    create_deployment_configs(project_root)
    
    print("\n🎉 Estructura del proyecto creada exitosamente!")
    print("=" * 60)
    print(f"📍 Ubicación: {project_root}")
    print("\n📋 Próximos pasos:")
    print("1. cd project-management-platform")
    print("2. make install")
    print("3. make start-docker")
    print("\n🌐 URLs de desarrollo:")
    print("- Frontend: http://localhost:4200")
    print("- Backend:  http://localhost:8080") 
    print("- DB:       postgresql://pm_user:pm_password@localhost:5432/project_management")
    
    return project_root

if __name__ == "__main__":
    main()
