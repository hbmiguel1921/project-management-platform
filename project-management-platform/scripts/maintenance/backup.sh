#!/bin/bash
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
