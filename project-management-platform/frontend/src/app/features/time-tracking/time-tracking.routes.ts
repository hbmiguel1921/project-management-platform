import { Routes } from '@angular/router';

export const TIME_TRACKING_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./time-tracking.component').then(m => m.TimetrackingComponent)
  },
  // Agregar más rutas específicas del módulo aquí
];
