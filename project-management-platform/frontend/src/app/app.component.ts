import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, ButtonModule, CardModule],
  template: `
    <div class="main-layout">
      <nav class="sidebar">
        <h2>PM Platform</h2>
        <p>Navegación aquí</p>
      </nav>
      <main class="content">
        <p-card header="Bienvenido a la Plataforma de Gestión de Proyectos">
          <p>Esta es la aplicación principal del sistema.</p>
          <p-button label="Comenzar" icon="pi pi-check"></p-button>
        </p-card>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: []
})
export class AppComponent {
  title = 'project-management-app';
}
