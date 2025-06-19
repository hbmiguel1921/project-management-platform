import { Routes } from '@angular/router';
import { AuthGuard } from '@core/guards/auth.guard';

export const routes: Routes = [
  // Redirección por defecto
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },

  // Rutas públicas (sin autenticación)
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },

  // Rutas protegidas (requieren autenticación)
  {
    path: 'dashboard',
    canActivate: [AuthGuard],
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },

  // Proyectos
  {
    path: 'projects',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/projects/project.routes').then(m => m.PROJECT_ROUTES)
  },

  // Tareas
  {
    path: 'tasks',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/tasks/task.routes').then(m => m.TASK_ROUTES)
  },

  // Kanban
  {
    path: 'kanban',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/kanban/kanban.routes').then(m => m.KANBAN_ROUTES)
  },

  // Sprints
  {
    path: 'sprints',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/sprints/sprint.routes').then(m => m.SPRINT_ROUTES)
  },

  // Seguimiento de tiempo
  {
    path: 'time-tracking',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/time-tracking/time-tracking.routes').then(m => m.TIME_TRACKING_ROUTES)
  },

  // Chat
  {
    path: 'chat',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/chat/chat.routes').then(m => m.CHAT_ROUTES)
  },

  // Wiki
  {
    path: 'wiki',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/wiki/wiki.routes').then(m => m.WIKI_ROUTES)
  },

  // Reportes
  {
    path: 'reports',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/reports/reports.routes').then(m => m.REPORTS_ROUTES)
  },

  // Notificaciones
  {
    path: 'notifications',
    canActivate: [AuthGuard],
    loadComponent: () => import('./features/notifications/notifications-page.component').then(m => m.NotificationsPageComponent)
  },

  // Perfil de usuario
  {
    path: 'profile',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/profile/profile.routes').then(m => m.PROFILE_ROUTES)
  },

  // Administración
  {
    path: 'admin',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/admin/admin.routes').then(m => m.ADMIN_ROUTES)
  },

  // Configuración
  {
    path: 'settings',
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/settings/settings.routes').then(m => m.SETTINGS_ROUTES)
  },

  // Páginas de error
  {
    path: '404',
    loadComponent: () => import('./shared/components/error-pages/not-found.component').then(m => m.NotFoundComponent)
  },
  {
    path: '403',
    loadComponent: () => import('./shared/components/error-pages/forbidden.component').then(m => m.ForbiddenComponent)
  },
  {
    path: '500',
    loadComponent: () => import('./shared/components/error-pages/server-error.component').then(m => m.ServerErrorComponent)
  },

  // Ruta catch-all (debe ser la última)
  { path: '**', redirectTo: '/404' }
];
