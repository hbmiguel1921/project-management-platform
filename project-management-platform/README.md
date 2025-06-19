# Plataforma de Gestión de Proyectos de Software

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
