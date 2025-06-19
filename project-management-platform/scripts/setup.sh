#!/bin/bash

# Script de configuración inicial para la Plataforma de Gestión de Proyectos
# Este script configura el entorno de desarrollo completo

set -e

echo "🚀 Configurando Plataforma de Gestión de Proyectos..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependencias
print_status "Verificando dependencias..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker y Docker Compose."
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado."
    exit 1
fi

# Verificar Go (opcional para desarrollo)
if ! command -v go &> /dev/null; then
    print_warning "Go no está instalado. Se usará la imagen Docker para el backend."
else
    print_status "Go encontrado: $(go version)"
fi

# Verificar Node.js (opcional para desarrollo)
if ! command -v node &> /dev/null; then
    print_warning "Node.js no está instalado. Se usará la imagen Docker para el frontend."
else
    print_status "Node.js encontrado: $(node --version)"
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    print_status "Creando archivo .env desde template..."
    cp .env.template .env
    print_warning "Por favor, edita el archivo .env con tus configuraciones específicas."
else
    print_status "Archivo .env ya existe."
fi

# Crear directorio de uploads
print_status "Creando directorios necesarios..."
mkdir -p uploads
mkdir -p logs
mkdir -p database/backups

# Configurar permisos
chmod +x scripts/development/start.sh
chmod +x scripts/maintenance/backup.sh

# Construir imágenes Docker
print_status "Construyendo imágenes Docker..."
docker-compose build

# Inicializar base de datos
print_status "Inicializando base de datos..."
docker-compose up -d postgres
sleep 10

# Esperar que PostgreSQL esté listo
print_status "Esperando a que PostgreSQL esté listo..."
until docker-compose exec postgres pg_isready -U postgres; do
    sleep 2
done

# Ejecutar migraciones
print_status "Ejecutando migraciones de base de datos..."
docker-compose exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/001_init.sql

# Cargar datos de desarrollo
if [ "$1" = "--with-sample-data" ]; then
    print_status "Cargando datos de ejemplo..."
    docker-compose exec postgres psql -U postgres -d project_management -f /docker-entrypoint-initdb.d/development.sql
fi

print_status "✅ Configuración completada!"
echo
print_status "Para iniciar la aplicación:"
echo "  docker-compose up -d"
echo
print_status "Para desarrollo:"
echo "  make dev"
echo
print_status "URLs de la aplicación:"
echo "  Frontend: http://localhost:4200"
echo "  Backend API: http://localhost:8080"
echo "  Documentación API: http://localhost:8080/docs"
echo
print_status "Usuario administrador por defecto:"
echo "  Email: admin@example.com"
echo "  Password: admin123"
