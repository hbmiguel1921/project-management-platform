import { Routes } from '@angular/router';

export const KANBAN_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./kanban.component').then(m => m.KanbanComponent)
  },
  // Agregar más rutas específicas del módulo aquí
];
