import { Routes } from '@angular/router';

export const SPRINT_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./sprints.component').then(m => m.SprintsComponent)
  },
  // Agregar más rutas específicas del módulo aquí
];
