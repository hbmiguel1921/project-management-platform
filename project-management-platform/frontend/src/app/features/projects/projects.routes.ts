import { Routes } from '@angular/router';

export const PROJECT_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./projects.component').then(m => m.ProjectsComponent)
  },
  // Agregar más rutas específicas del módulo aquí
];
