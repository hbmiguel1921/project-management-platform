import { Routes } from '@angular/router';

export const WIKI_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./wiki.component').then(m => m.WikiComponent)
  },
  // Agregar más rutas específicas del módulo aquí
];
