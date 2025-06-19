import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
import { SidebarModule } from 'primeng/sidebar';
import { MenuModule } from 'primeng/menu';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { BadgeModule } from 'primeng/badge';
import { AuthService, User } from '@core/services/auth.service';
import { WebSocketService } from '@core/services/websocket.service';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterModule,
    SidebarModule,
    MenuModule,
    AvatarModule,
    ButtonModule,
    BadgeModule
  ],
  template: `
    <div class="layout-wrapper">
      <!-- Sidebar -->
      <div class="layout-sidebar" [class.sidebar-collapsed]="sidebarCollapsed">
        <div class="sidebar-header">
          <div class="logo">
            <i class="pi pi-th-large"></i>
            <span *ngIf="!sidebarCollapsed">PM Platform</span>
          </div>
          <p-button 
            [icon]="sidebarCollapsed ? 'pi pi-angle-right' : 'pi pi-angle-left'"
            severity="secondary"
            [text]="true"
            size="small"
            (onClick)="toggleSidebar()">
          </p-button>
        </div>

        <nav class="sidebar-nav">
          <ul class="nav-menu">
            <li class="nav-item">
              <a routerLink="/dashboard" routerLinkActive="active" class="nav-link">
                <i class="pi pi-th-large"></i>
                <span *ngIf="!sidebarCollapsed">Dashboard</span>
              </a>
            </li>
            
            <li class="nav-item">
              <a routerLink="/projects" routerLinkActive="active" class="nav-link">
                <i class="pi pi-folder"></i>
                <span *ngIf="!sidebarCollapsed">Proyectos</span>
                <p-badge 
                  *ngIf="!sidebarCollapsed && projectCount > 0"
                  [value]="projectCount"
                  severity="info">
                </p-badge>
              </a>
            </li>
            
            <li class="nav-item">
              <a routerLink="/tasks" routerLinkActive="active" class="nav-link">
                <i class="pi pi-check-square"></i>
                <span *ngIf="!sidebarCollapsed">Mis Tareas</span>
                <p-badge 
                  *ngIf="!sidebarCollapsed && myTaskCount > 0"
                  [value]="myTaskCount"
                  severity="warning">
                </p-badge>
              </a>
            </li>
            
            <li class="nav-divider" *ngIf="!sidebarCollapsed">
              <span>Herramientas</span>
            </li>
            
            <li class="nav-item">
              <a routerLink="/kanban" routerLinkActive="active" class="nav-link">
                <i class="pi pi-table"></i>
                <span *ngIf="!sidebarCollapsed">Tableros</span>
              </a>
            </li>
            
            <li class="nav-item">
              <a routerLink="/gantt" routerLinkActive="active" class="nav-link">
                <i class="pi pi-chart-line"></i>
                <span *ngIf="!sidebarCollapsed">Cronograma</span>
              </a>
            </li>
            
            <li class="nav-item">
              <a routerLink="/reports" routerLinkActive="active" class="nav-link">
                <i class="pi pi-chart-bar"></i>
                <span *ngIf="!sidebarCollapsed">Reportes</span>
              </a>
            </li>
            
            <li class="nav-item">
              <a routerLink="/chat" routerLinkActive="active" class="nav-link">
                <i class="pi pi-comments"></i>
                <span *ngIf="!sidebarCollapsed">Chat</span>
                <p-badge 
                  *ngIf="!sidebarCollapsed && unreadMessages > 0"
                  [value]="unreadMessages"
                  severity="danger">
                </p-badge>
              </a>
            </li>
            
            <li class="nav-divider" *ngIf="!sidebarCollapsed && currentUser?.role === 'admin'">
              <span>Administración</span>
            </li>
            
            <li class="nav-item" *ngIf="currentUser?.role === 'admin'">
              <a routerLink="/admin/users" routerLinkActive="active" class="nav-link">
                <i class="pi pi-users"></i>
                <span *ngIf="!sidebarCollapsed">Usuarios</span>
              </a>
            </li>
            
            <li class="nav-item" *ngIf="currentUser?.role === 'admin'">
              <a routerLink="/admin/settings" routerLinkActive="active" class="nav-link">
                <i class="pi pi-cog"></i>
                <span *ngIf="!sidebarCollapsed">Configuración</span>
              </a>
            </li>
          </ul>
        </nav>

        <div class="sidebar-footer">
          <div class="user-info" *ngIf="currentUser">
            <p-avatar 
              [image]="currentUser.avatar"
              [label]="getUserInitials(currentUser)"
              size="normal"
              shape="circle">
            </p-avatar>
            <div class="user-details" *ngIf="!sidebarCollapsed">
              <span class="user-name">{{ currentUser.first_name }} {{ currentUser.last_name }}</span>
              <span class="user-role">{{ getRoleLabel(currentUser.role) }}</span>
            </div>
          </div>
          
          <div class="sidebar-actions" *ngIf="!sidebarCollapsed">
            <p-button 
              icon="pi pi-user" 
              severity="secondary"
              [text]="true"
              size="small"
              routerLink="/profile"
              pTooltip="Mi Perfil">
            </p-button>
            <p-button 
              icon="pi pi-sign-out" 
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="logout()"
              pTooltip="Cerrar Sesión">
            </p-button>
          </div>
        </div>
      </div>

      <!-- Topbar -->
      <div class="layout-topbar" [style.margin-left]="getTopbarMargin()">
        <div class="topbar-content">
          <div class="topbar-left">
            <h2 class="page-title">{{ currentPageTitle }}</h2>
          </div>
          
          <div class="topbar-right">
            <!-- Indicador de conexión WebSocket -->
            <div class="connection-status">
              <i 
                [class]="wsConnected ? 'pi pi-circle-fill connected' : 'pi pi-circle-fill disconnected'"
                [pTooltip]="wsConnected ? 'Conectado' : 'Desconectado'">
              </i>
            </div>

            <!-- Notificaciones -->
            <p-button 
              icon="pi pi-bell"
              severity="secondary"
              [text]="true"
              [badge]="notificationCount > 0 ? notificationCount.toString() : null"
              badgeClass="p-badge-danger"
              (onClick)="showNotifications()"
              pTooltip="Notificaciones">
            </p-button>

            <!-- Búsqueda rápida -->
            <p-button 
              icon="pi pi-search"
              severity="secondary"
              [text]="true"
              (onClick)="showQuickSearch()"
              pTooltip="Búsqueda rápida (Ctrl+K)">
            </p-button>

            <!-- Usuario -->
            <div class="user-menu">
              <p-avatar 
                [image]="currentUser?.avatar"
                [label]="getUserInitials(currentUser)"
                size="normal"
                shape="circle"
                (click)="toggleUserMenu()"
                style="cursor: pointer;">
              </p-avatar>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="layout-content" [style.margin-left]="getContentMargin()">
        <router-outlet></router-outlet>
      </div>

      <!-- Overlay para móvil -->
      <div 
        *ngIf="showMobileOverlay" 
        class="mobile-overlay"
        (click)="closeMobileSidebar()">
      </div>
    </div>

    <!-- Sidebar móvil -->
    <p-sidebar 
      [(visible)]="showMobileSidebar"
      position="left"
      [modal]="true"
      styleClass="mobile-sidebar">
      
      <!-- Contenido del sidebar para móvil -->
      <div class="mobile-sidebar-content">
        <!-- Replica del contenido del sidebar -->
      </div>
    </p-sidebar>
  `,
  styles: [`
    .layout-wrapper {
      min-height: 100vh;
      background: #f5f5f5;
    }

    /* Sidebar */
    .layout-sidebar {
      position: fixed;
      top: 0;
      left: 0;
      width: 260px;
      height: 100vh;
      background: #1e293b;
      color: white;
      z-index: 1000;
      transition: width 0.3s ease;
      display: flex;
      flex-direction: column;
    }

    .layout-sidebar.sidebar-collapsed {
      width: 70px;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #374151;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
      font-size: 1.1rem;
    }

    .logo i {
      font-size: 1.5rem;
      color: #3b82f6;
    }

    .sidebar-nav {
      flex: 1;
      overflow-y: auto;
      padding: 1rem 0;
    }

    .nav-menu {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .nav-item {
      margin-bottom: 0.25rem;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      color: #cbd5e1;
      text-decoration: none;
      transition: all 0.2s ease;
      position: relative;
    }

    .nav-link:hover {
      background: #374151;
      color: white;
    }

    .nav-link.active {
      background: #3b82f6;
      color: white;
    }

    .nav-link.active::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      width: 3px;
      background: #60a5fa;
    }

    .nav-link i {
      font-size: 1.1rem;
      min-width: 20px;
    }

    .nav-divider {
      padding: 1rem 1rem 0.5rem 1rem;
      font-size: 0.75rem;
      font-weight: 600;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .sidebar-footer {
      border-top: 1px solid #374151;
      padding: 1rem;
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
    }

    .user-details {
      flex: 1;
      min-width: 0;
    }

    .user-name {
      display: block;
      font-weight: 500;
      font-size: 0.9rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .user-role {
      display: block;
      font-size: 0.75rem;
      color: #9ca3af;
    }

    .sidebar-actions {
      display: flex;
      gap: 0.5rem;
      justify-content: center;
    }

    /* Topbar */
    .layout-topbar {
      position: fixed;
      top: 0;
      right: 0;
      height: 60px;
      background: white;
      border-bottom: 1px solid #e5e7eb;
      z-index: 999;
      transition: margin-left 0.3s ease;
    }

    .topbar-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 100%;
      padding: 0 1.5rem;
    }

    .page-title {
      margin: 0;
      font-size: 1.25rem;
      font-weight: 600;
      color: #1f2937;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .connection-status i.connected {
      color: #10b981;
    }

    .connection-status i.disconnected {
      color: #ef4444;
    }

    .user-menu {
      cursor: pointer;
    }

    /* Contenido principal */
    .layout-content {
      margin-top: 60px;
      transition: margin-left 0.3s ease;
      min-height: calc(100vh - 60px);
    }

    /* Responsive */
    @media (max-width: 768px) {
      .layout-sidebar {
        transform: translateX(-100%);
      }

      .layout-topbar {
        margin-left: 0 !important;
      }

      .layout-content {
        margin-left: 0 !important;
      }

      .mobile-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1001;
      }
    }

    /* Animaciones */
    .layout-sidebar,
    .layout-topbar,
    .layout-content {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Badges */
    ::ng-deep .p-badge {
      min-width: 1.2rem;
      height: 1.2rem;
      line-height: 1.2rem;
      font-size: 0.7rem;
    }
  `]
})
export class MainLayoutComponent implements OnInit {
  sidebarCollapsed = false;
  showMobileSidebar = false;
  showMobileOverlay = false;
  currentUser: User | null = null;
  currentPageTitle = 'Dashboard';
  
  // Contadores
  projectCount = 0;
  myTaskCount = 0;
  unreadMessages = 0;
  notificationCount = 0;
  
  // Estado de conexión
  wsConnected = false;

  constructor(
    private authService: AuthService,
    private wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.loadCurrentUser();
    this.subscribeToWebSocket();
    this.loadCounters();
  }

  private loadCurrentUser(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  private subscribeToWebSocket(): void {
    this.wsService.connected$.subscribe(connected => {
      this.wsConnected = connected;
    });

    // Escuchar notificaciones
    this.wsService.onNotification().subscribe(notification => {
      this.notificationCount++;
    });
  }

  private loadCounters(): void {
    // Aquí se cargarían los contadores desde los servicios
    // Por ahora valores simulados
    this.projectCount = 5;
    this.myTaskCount = 12;
    this.unreadMessages = 3;
    this.notificationCount = 2;
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  toggleUserMenu(): void {
    // Implementar menú de usuario
    console.log('Toggle user menu');
  }

  showNotifications(): void {
    // Mostrar panel de notificaciones
    console.log('Show notifications');
  }

  showQuickSearch(): void {
    // Mostrar búsqueda rápida
    console.log('Show quick search');
  }

  closeMobileSidebar(): void {
    this.showMobileSidebar = false;
    this.showMobileOverlay = false;
  }

  logout(): void {
    this.authService.logout();
  }

  getUserInitials(user: User | null): string {
    if (!user) return '';
    return (user.first_name?.[0] || '') + (user.last_name?.[0] || '');
  }

  getRoleLabel(role: string): string {
    const roles = {
      'admin': 'Administrador',
      'manager': 'Gerente',
      'developer': 'Desarrollador',
      'tester': 'Tester',
      'viewer': 'Observador'
    };
    return roles[role as keyof typeof roles] || role;
  }

  getTopbarMargin(): string {
    return this.sidebarCollapsed ? '70px' : '260px';
  }

  getContentMargin(): string {
    return this.sidebarCollapsed ? '70px' : '260px';
  }
}
