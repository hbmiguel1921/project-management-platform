#!/bin/bash

# Script para iniciar el entorno de desarrollo

set -e

echo "🚀 Iniciando entorno de desarrollo..."

# Función para mostrar mensajes
print_status() {
    echo -e "\033[0;32m[INFO]\033[0m $1"
}

# Verificar que .env existe
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado. Ejecuta scripts/setup.sh primero."
    exit 1
fi

# Cargar variables de entorno
export $(cat .env | grep -v '^#' | xargs)

# Iniciar servicios con Docker Compose
print_status "Iniciando servicios..."
docker-compose up -d postgres redis

# Esperar a que los servicios estén listos
print_status "Esperando a que los servicios estén listos..."
sleep 5

# Si Go está instalado localmente, usar desarrollo local
if command -v go &> /dev/null; then
    print_status "Iniciando backend en modo desarrollo..."
    cd backend
    go mod tidy
    go run cmd/main.go &
    BACKEND_PID=$!
    cd ..
else
    print_status "Iniciando backend con Docker..."
    docker-compose up -d backend &
fi

# Si Node.js está instalado localmente, usar desarrollo local
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    print_status "Iniciando frontend en modo desarrollo..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        print_status "Instalando dependencias del frontend..."
        npm install
    fi
    npm start &
    FRONTEND_PID=$!
    cd ..
else
    print_status "Iniciando frontend con Docker..."
    docker-compose up -d frontend &
fi

print_status "✅ Entorno de desarrollo iniciado!"
print_status "Frontend: http://localhost:4200"
print_status "Backend API: http://localhost:8080"
print_status "Base de datos: localhost:5432"

# Función para limpiar procesos al salir
cleanup() {
    print_status "Deteniendo servicios de desarrollo..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    docker-compose down
}

# Configurar trap para limpiar al salir
trap cleanup EXIT

# Mantener el script ejecutándose
wait
