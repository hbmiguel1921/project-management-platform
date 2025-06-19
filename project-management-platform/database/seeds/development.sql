-- Datos de desarrollo para la plataforma de gestión de proyectos

-- Usuarios de prueba
INSERT INTO users (id, first_name, last_name, email, username, password_hash, role, is_active, email_verified) VALUES
(uuid_generate_v4(), 'Ana', 'García', 'ana.garcia@example.com', 'ana.garcia', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'manager', true, true),
(uuid_generate_v4(), 'Carlos', 'López', 'carlos.lopez@example.com', 'carlos.lopez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true),
(uuid_generate_v4(), 'María', 'Rodríguez', 'maria.rodriguez@example.com', 'maria.rodriguez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true),
(uuid_generate_v4(), 'Juan', 'Martínez', 'juan.martinez@example.com', 'juan.martinez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'tester', true, true),
(uuid_generate_v4(), 'Laura', 'Hernández', 'laura.hernandez@example.com', 'laura.hernandez', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'developer', true, true);

-- Proyectos de ejemplo
DO $$
DECLARE
    admin_id UUID;
    ana_id UUID;
    carlos_id UUID;
    maria_id UUID;
    juan_id UUID;
    laura_id UUID;
    proyecto_alpha_id UUID;
    proyecto_beta_id UUID;
    sprint_alpha_id UUID;
    task1_id UUID;
    task2_id UUID;
    channel_alpha_id UUID;
BEGIN
    -- Obtener IDs de usuarios
    SELECT id INTO admin_id FROM users WHERE email = 'admin@example.com';
    SELECT id INTO ana_id FROM users WHERE email = 'ana.garcia@example.com';
    SELECT id INTO carlos_id FROM users WHERE email = 'carlos.lopez@example.com';
    SELECT id INTO maria_id FROM users WHERE email = 'maria.rodriguez@example.com';
    SELECT id INTO juan_id FROM users WHERE email = 'juan.martinez@example.com';
    SELECT id INTO laura_id FROM users WHERE email = 'laura.hernandez@example.com';

    -- Crear proyecto Alpha
    proyecto_alpha_id := uuid_generate_v4();
    INSERT INTO projects (id, name, description, status, owner_id, start_date, end_date, budget) VALUES
    (proyecto_alpha_id, 'Proyecto Alpha', 'Sistema de gestión de inventario para empresa de retail', 'active', ana_id, '2024-01-15', '2024-06-30', 75000.00);

    -- Crear proyecto Beta
    proyecto_beta_id := uuid_generate_v4();
    INSERT INTO projects (id, name, description, status, owner_id, start_date, end_date, budget) VALUES
    (proyecto_beta_id, 'Proyecto Beta', 'Aplicación móvil para delivery de comida', 'planning', admin_id, '2024-03-01', '2024-08-15', 120000.00);

    -- Agregar miembros al proyecto Alpha
    INSERT INTO project_members (project_id, user_id, role) VALUES
    (proyecto_alpha_id, ana_id, 'manager'),
    (proyecto_alpha_id, carlos_id, 'developer'),
    (proyecto_alpha_id, maria_id, 'developer'),
    (proyecto_alpha_id, juan_id, 'tester');

    -- Agregar miembros al proyecto Beta
    INSERT INTO project_members (project_id, user_id, role) VALUES
    (proyecto_beta_id, admin_id, 'owner'),
    (proyecto_beta_id, laura_id, 'developer'),
    (proyecto_beta_id, juan_id, 'tester');

    -- Crear sprint para proyecto Alpha
    sprint_alpha_id := uuid_generate_v4();
    INSERT INTO sprints (id, name, description, project_id, start_date, end_date, status, goal, capacity) VALUES
    (sprint_alpha_id, 'Sprint 1 - Alpha', 'Configuración inicial del proyecto y módulo de autenticación', proyecto_alpha_id, '2024-01-15', '2024-01-29', 'completed', 'Establecer la base del proyecto con autenticación segura', 40);

    -- Crear tareas para el proyecto Alpha
    task1_id := uuid_generate_v4();
    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, sprint_id, status, priority, story_points, estimated_hours) VALUES
    (task1_id, 'Configurar arquitectura del proyecto', 'Establecer la estructura base del proyecto, configurar base de datos y servicios principales', proyecto_alpha_id, carlos_id, ana_id, sprint_alpha_id, 'completed', 'high', 8, 16.0);

    task2_id := uuid_generate_v4();
    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, sprint_id, status, priority, story_points, estimated_hours) VALUES
    (task2_id, 'Implementar sistema de autenticación', 'Desarrollar login, registro y gestión de sesiones con JWT', proyecto_alpha_id, maria_id, ana_id, sprint_alpha_id, 'in_progress', 'high', 5, 12.0);

    INSERT INTO tasks (id, title, description, project_id, assignee_id, reporter_id, status, priority, story_points, estimated_hours) VALUES
    (uuid_generate_v4(), 'Diseñar interfaz de usuario principal', 'Crear wireframes y prototipos de la interfaz principal del sistema', proyecto_alpha_id, carlos_id, ana_id, 'todo', 'medium', 3, 8.0);

    -- Crear comentarios en tareas
    INSERT INTO comments (content, task_id, user_id) VALUES
    ('He completado la configuración inicial. La base de datos está funcionando correctamente.', task1_id, carlos_id),
    ('Excelente trabajo! Ahora podemos continuar con el siguiente módulo.', task1_id, ana_id),
    ('Estoy trabajando en la implementación de JWT. Tengo algunas dudas sobre la configuración de seguridad.', task2_id, maria_id);

    -- Crear entradas de tiempo
    INSERT INTO time_entries (description, start_time, end_time, duration, task_id, project_id, user_id, is_billable) VALUES
    ('Configuración inicial del proyecto', '2024-01-15 09:00:00', '2024-01-15 17:00:00', 480, task1_id, proyecto_alpha_id, carlos_id, true),
    ('Investigación sobre JWT y configuración de seguridad', '2024-01-16 09:00:00', '2024-01-16 12:00:00', 180, task2_id, proyecto_alpha_id, maria_id, true),
    ('Desarrollo de endpoints de autenticación', '2024-01-16 14:00:00', '2024-01-16 18:00:00', 240, task2_id, proyecto_alpha_id, maria_id, true);

    -- Crear canal de chat para proyecto Alpha
    channel_alpha_id := uuid_generate_v4();
    INSERT INTO chat_channels (id, name, description, type, project_id, creator_id) VALUES
    (channel_alpha_id, 'general-alpha', 'Canal general del Proyecto Alpha', 'project', proyecto_alpha_id, ana_id);

    -- Agregar miembros al canal
    INSERT INTO channel_members (channel_id, user_id, role) VALUES
    (channel_alpha_id, ana_id, 'admin'),
    (channel_alpha_id, carlos_id, 'member'),
    (channel_alpha_id, maria_id, 'member'),
    (channel_alpha_id, juan_id, 'member');

    -- Crear mensajes en el canal
    INSERT INTO chat_messages (content, channel_id, user_id, type) VALUES
    ('¡Bienvenidos al canal del Proyecto Alpha! Aquí coordinaremos nuestro trabajo diario.', channel_alpha_id, ana_id, 'text'),
    ('Perfecto! Ya tenemos la base configurada y lista para desarrollo.', channel_alpha_id, carlos_id, 'text'),
    ('Excelente. ¿Alguien puede revisar la documentación de la API que subí?', channel_alpha_id, maria_id, 'text');

    -- Crear página wiki para el proyecto
    INSERT INTO wiki_pages (title, slug, content, project_id, author_id, is_published, version) VALUES
    ('Documentación del Proyecto Alpha', 'proyecto-alpha-docs', '# Proyecto Alpha - Sistema de Gestión de Inventario

## Objetivo
Desarrollar un sistema completo de gestión de inventario para empresas de retail.

## Tecnologías
- Backend: Golang con Gin
- Frontend: Angular con PrimeNG
- Base de datos: PostgreSQL
- Autenticación: JWT

## Arquitectura
El sistema sigue una arquitectura de microservicios con las siguientes capas:
- API REST
- Capa de servicios
- Capa de datos
- Frontend SPA

## Configuración del Entorno
...', proyecto_alpha_id, ana_id, true, 1);

    -- Crear notificaciones de ejemplo
    INSERT INTO notifications (title, content, type, user_id, action_url, entity_type, entity_id) VALUES
    ('Nueva tarea asignada', 'Se te ha asignado la tarea: Implementar sistema de autenticación', 'task_assigned', maria_id, '/tasks/' || task2_id, 'task', task2_id),
    ('Comentario en tarea', 'Carlos López ha comentado en tu tarea', 'comment_added', maria_id, '/tasks/' || task2_id, 'task', task2_id),
    ('Tarea completada', 'Carlos López ha completado la tarea: Configurar arquitectura del proyecto', 'task_completed', ana_id, '/tasks/' || task1_id, 'task', task1_id);

END $$;
