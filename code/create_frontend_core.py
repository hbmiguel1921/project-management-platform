#!/usr/bin/env python3
"""
Script para crear la implementación completa del frontend en Angular + PrimeNG
con todas las funcionalidades requeridas según las historias de usuario.
"""

import os

def create_frontend_core():
    """Crear implementación completa del frontend"""
    
    frontend_dir = "/workspace/project-management-platform/frontend"
    
    # Core services
    create_core_services(frontend_dir)
    
    # Shared components
    create_shared_components(frontend_dir)
    
    # Feature modules
    create_feature_modules(frontend_dir)
    
    # Layout components
    create_layout_components(frontend_dir)
    
    # Guards y interceptors
    create_guards_interceptors(frontend_dir)
    
    print("✓ Frontend core completado")

def create_core_services(frontend_dir):
    """Crear servicios core del frontend"""
    
    # src/app/core/services/auth.service.ts
    auth_service_content = """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '@environments/environment';

export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  avatar?: string;
  role: string;
  is_active: boolean;
  timezone: string;
  language: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  expires_at: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.loadStoredAuth();
  }

  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${environment.apiUrl}/auth/login`, credentials)
      .pipe(
        tap(response => {
          this.setSession(response);
        })
      );
  }

  register(userData: RegisterRequest): Observable<{user: User}> {
    return this.http.post<{user: User}>(`${environment.apiUrl}/auth/register`, userData);
  }

  logout(): void {
    this.clearSession();
    this.router.navigate(['/auth/login']);
  }

  refreshToken(): Observable<LoginResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    return this.http.post<LoginResponse>(`${environment.apiUrl}/auth/refresh`, {
      refresh_token: refreshToken
    }).pipe(
      tap(response => {
        this.setSession(response);
      })
    );
  }

  getProfile(): Observable<{user: User}> {
    return this.http.get<{user: User}>(`${environment.apiUrl}/auth/me`);
  }

  updateProfile(userData: Partial<User>): Observable<{user: User}> {
    return this.http.put<{user: User}>(`${environment.apiUrl}/auth/me`, userData)
      .pipe(
        tap(response => {
          this.currentUserSubject.next(response.user);
        })
      );
  }

  changePassword(passwordData: {current_password: string, new_password: string}): Observable<any> {
    return this.http.post(`${environment.apiUrl}/auth/change-password`, passwordData);
  }

  private setSession(authResponse: LoginResponse): void {
    localStorage.setItem('access_token', authResponse.access_token);
    localStorage.setItem('refresh_token', authResponse.refresh_token);
    localStorage.setItem('expires_at', authResponse.expires_at);
    localStorage.setItem('user', JSON.stringify(authResponse.user));
    
    this.currentUserSubject.next(authResponse.user);
    this.isAuthenticatedSubject.next(true);
  }

  private clearSession(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('expires_at');
    localStorage.removeItem('user');
    
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
  }

  private loadStoredAuth(): void {
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user');
    const expiresAt = localStorage.getItem('expires_at');

    if (token && userStr && expiresAt) {
      const isExpired = new Date().getTime() > new Date(expiresAt).getTime();
      
      if (!isExpired) {
        const user = JSON.parse(userStr);
        this.currentUserSubject.next(user);
        this.isAuthenticatedSubject.next(true);
      } else {
        this.clearSession();
      }
    }
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  hasRole(role: string): boolean {
    const user = this.getCurrentUser();
    return user?.role === role || user?.role === 'admin';
  }

  hasAnyRole(roles: string[]): boolean {
    const user = this.getCurrentUser();
    return roles.includes(user?.role || '') || user?.role === 'admin';
  }
}
"""
    
    auth_service_path = os.path.join(frontend_dir, "src/app/core/services/auth.service.ts")
    os.makedirs(os.path.dirname(auth_service_path), exist_ok=True)
    with open(auth_service_path, "w", encoding="utf-8") as f:
        f.write(auth_service_content)
    
    # src/app/core/services/project.service.ts
    project_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Project {
  id: string;
  name: string;
  key: string;
  description?: string;
  status: 'planning' | 'active' | 'on_hold' | 'completed' | 'archived';
  start_date?: string;
  end_date?: string;
  budget?: number;
  is_public: boolean;
  settings: ProjectSettings;
  created_at: string;
  updated_at: string;
}

export interface ProjectSettings {
  allow_external_users: boolean;
  default_task_type: string;
  workflow_states: string[];
  estimation_unit: string;
}

export interface ProjectMember {
  id: string;
  project_id: string;
  user_id: string;
  role: 'owner' | 'manager' | 'developer' | 'tester' | 'viewer';
  joined_at: string;
  user?: any;
}

export interface ProjectStats {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  todo_tasks: number;
  total_members: number;
  active_sprints: number;
}

export interface ProjectDashboard {
  project: Project;
  stats: ProjectStats;
  recent_tasks: any[];
  active_sprint?: any;
}

export interface CreateProjectRequest {
  name: string;
  key: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  budget?: number;
  is_public: boolean;
  settings: ProjectSettings;
  members: {user_id: string, role: string}[];
}

@Injectable({
  providedIn: 'root'
})
export class ProjectService {

  constructor(private http: HttpClient) { }

  getProjects(params?: any): Observable<{data: Project[], total: number}> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    
    return this.http.get<{data: Project[], total: number}>(`${environment.apiUrl}/projects`, { params: httpParams });
  }

  getProject(id: string): Observable<Project> {
    return this.http.get<Project>(`${environment.apiUrl}/projects/${id}`);
  }

  createProject(project: CreateProjectRequest): Observable<Project> {
    return this.http.post<Project>(`${environment.apiUrl}/projects`, project);
  }

  updateProject(id: string, project: Partial<Project>): Observable<Project> {
    return this.http.put<Project>(`${environment.apiUrl}/projects/${id}`, project);
  }

  deleteProject(id: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/projects/${id}`);
  }

  getProjectDashboard(id: string): Observable<ProjectDashboard> {
    return this.http.get<ProjectDashboard>(`${environment.apiUrl}/projects/${id}/dashboard`);
  }

  getProjectMembers(id: string): Observable<ProjectMember[]> {
    return this.http.get<ProjectMember[]>(`${environment.apiUrl}/projects/${id}/members`);
  }

  addProjectMember(id: string, member: {user_id: string, role: string}): Observable<ProjectMember> {
    return this.http.post<ProjectMember>(`${environment.apiUrl}/projects/${id}/members`, member);
  }

  updateProjectMember(projectId: string, userId: string, data: {role: string}): Observable<ProjectMember> {
    return this.http.put<ProjectMember>(`${environment.apiUrl}/projects/${projectId}/members/${userId}`, data);
  }

  removeProjectMember(projectId: string, userId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/projects/${projectId}/members/${userId}`);
  }

  archiveProject(id: string): Observable<Project> {
    return this.updateProject(id, { status: 'archived' });
  }

  reactivateProject(id: string): Observable<Project> {
    return this.updateProject(id, { status: 'active' });
  }
}
"""
    
    project_service_path = os.path.join(frontend_dir, "src/app/core/services/project.service.ts")
    with open(project_service_path, "w", encoding="utf-8") as f:
        f.write(project_service_content)
    
    # src/app/core/services/task.service.ts
    task_service_content = """import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Task {
  id: string;
  title: string;
  description?: string;
  type: 'story' | 'task' | 'bug' | 'epic' | 'subtask';
  status: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked' | 'cancelled';
  priority: 'lowest' | 'low' | 'medium' | 'high' | 'highest';
  story_points?: number;
  estimated_hours?: number;
  logged_hours: number;
  start_date?: string;
  due_date?: string;
  project_id: string;
  epic_id?: string;
  sprint_id?: string;
  parent_id?: string;
  assignee_id?: string;
  creator_id: string;
  tags: string[];
  labels: string[];
  position: number;
  custom_fields: {[key: string]: any};
  created_at: string;
  updated_at: string;
  
  // Entidades relacionadas
  project?: any;
  epic?: any;
  sprint?: any;
  parent?: Task;
  assignee?: any;
  creator?: any;
  subtasks?: Task[];
  comments?: Comment[];
  attachments?: any[];
  time_entries?: any[];
}

export interface TaskFilter {
  status?: string[];
  priority?: string[];
  type?: string[];
  assignee_id?: string;
  epic_id?: string;
  sprint_id?: string;
  search?: string;
  tags?: string[];
  labels?: string[];
  due_soon?: boolean;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  type?: string;
  priority?: string;
  story_points?: number;
  estimated_hours?: number;
  start_date?: string;
  due_date?: string;
  epic_id?: string;
  sprint_id?: string;
  parent_id?: string;
  assignee_id?: string;
  tags?: string[];
  labels?: string[];
  custom_fields?: {[key: string]: any};
}

export interface Comment {
  id: string;
  content: string;
  task_id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  user?: any;
}

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  constructor(private http: HttpClient) { }

  getTasks(projectId?: string, filter?: TaskFilter): Observable<{data: Task[], total: number}> {
    let httpParams = new HttpParams();
    
    if (filter) {
      Object.keys(filter).forEach(key => {
        const value = (filter as any)[key];
        if (value !== null && value !== undefined) {
          if (Array.isArray(value)) {
            value.forEach(v => httpParams = httpParams.append(key, v));
          } else {
            httpParams = httpParams.set(key, value);
          }
        }
      });
    }

    const url = projectId 
      ? `${environment.apiUrl}/projects/${projectId}/tasks`
      : `${environment.apiUrl}/tasks`;
    
    return this.http.get<{data: Task[], total: number}>(url, { params: httpParams });
  }

  getTask(id: string): Observable<Task> {
    return this.http.get<Task>(`${environment.apiUrl}/tasks/${id}`);
  }

  createTask(projectId: string, task: CreateTaskRequest): Observable<Task> {
    return this.http.post<Task>(`${environment.apiUrl}/projects/${projectId}/tasks`, task);
  }

  updateTask(id: string, task: Partial<CreateTaskRequest>): Observable<Task> {
    return this.http.put<Task>(`${environment.apiUrl}/tasks/${id}`, task);
  }

  deleteTask(id: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/tasks/${id}`);
  }

  updateTaskStatus(id: string, status: string): Observable<Task> {
    return this.updateTask(id, { status } as any);
  }

  assignTask(id: string, assigneeId: string): Observable<Task> {
    return this.updateTask(id, { assignee_id: assigneeId } as any);
  }

  addComment(taskId: string, content: string): Observable<Comment> {
    return this.http.post<Comment>(`${environment.apiUrl}/tasks/${taskId}/comments`, { content });
  }

  getComments(taskId: string): Observable<Comment[]> {
    return this.http.get<Comment[]>(`${environment.apiUrl}/tasks/${taskId}/comments`);
  }

  moveTaskToPosition(taskId: string, newPosition: number, newStatus?: string): Observable<Task> {
    const updateData: any = { position: newPosition };
    if (newStatus) {
      updateData.status = newStatus;
    }
    return this.updateTask(taskId, updateData);
  }

  getTasksByStatus(projectId: string, status: string): Observable<Task[]> {
    return this.getTasks(projectId, { status: [status] }).pipe(
      map(response => response.data)
    );
  }

  getMyTasks(): Observable<Task[]> {
    // Obtener tareas asignadas al usuario actual
    return this.getTasks(undefined, {}).pipe(
      map(response => response.data)
    );
  }

  searchTasks(query: string, projectId?: string): Observable<Task[]> {
    return this.getTasks(projectId, { search: query }).pipe(
      map(response => response.data)
    );
  }

  getTasksWithFilter(filter: TaskFilter): Observable<Task[]> {
    return this.getTasks(undefined, filter).pipe(
      map(response => response.data)
    );
  }
}
"""
    
    task_service_path = os.path.join(frontend_dir, "src/app/core/services/task.service.ts")
    with open(task_service_path, "w", encoding="utf-8") as f:
        f.write(task_service_content)
    
    # src/app/core/services/websocket.service.ts
    websocket_service_content = """import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@environments/environment';
import { AuthService } from './auth.service';

export interface WebSocketMessage {
  type: string;
  project_id?: string;
  user_id?: string;
  data: any;
  timestamp: number;
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private connectedSubject = new BehaviorSubject<boolean>(false);
  public connected$ = this.connectedSubject.asObservable();

  private socket?: Socket;

  constructor(private authService: AuthService) {
    this.initializeConnection();
  }

  private initializeConnection(): void {
    this.authService.isAuthenticated$.subscribe(isAuth => {
      if (isAuth && !this.socket) {
        this.connect();
      } else if (!isAuth && this.socket) {
        this.disconnect();
      }
    });
  }

  private connect(): void {
    const token = this.authService.getToken();
    if (!token) return;

    // Crear configuración de socket con autenticación
    const socketConfig = {
      url: environment.wsUrl,
      options: {
        auth: {
          token: token
        },
        transports: ['websocket']
      }
    };

    this.socket = new Socket(socketConfig);

    this.socket.on('connect', () => {
      console.log('WebSocket conectado');
      this.connectedSubject.next(true);
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket desconectado');
      this.connectedSubject.next(false);
    });

    this.socket.on('error', (error: any) => {
      console.error('Error de WebSocket:', error);
    });

    this.socket.connect();
  }

  private disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = undefined;
      this.connectedSubject.next(false);
    }
  }

  // Suscribirse a un proyecto para recibir actualizaciones
  subscribeToProject(projectId: string): void {
    if (this.socket) {
      this.socket.emit('subscribe_project', projectId);
    }
  }

  // Desuscribirse de un proyecto
  unsubscribeFromProject(projectId: string): void {
    if (this.socket) {
      this.socket.emit('unsubscribe_project', projectId);
    }
  }

  // Escuchar mensajes de un tipo específico
  listen<T>(eventType: string): Observable<T> {
    if (!this.socket) {
      return new Observable(observer => {
        observer.error('Socket no está conectado');
      });
    }

    return new Observable(observer => {
      this.socket!.on(eventType, (data: T) => {
        observer.next(data);
      });

      // Cleanup cuando se desuscriba
      return () => {
        if (this.socket) {
          this.socket.off(eventType);
        }
      };
    });
  }

  // Enviar mensaje
  emit(eventType: string, data: any): void {
    if (this.socket) {
      this.socket.emit(eventType, data);
    }
  }

  // Eventos específicos para la aplicación
  onTaskUpdated(): Observable<any> {
    return this.listen('task_updated');
  }

  onTaskCreated(): Observable<any> {
    return this.listen('task_created');
  }

  onTaskDeleted(): Observable<any> {
    return this.listen('task_deleted');
  }

  onTaskMoved(): Observable<any> {
    return this.listen('task_moved');
  }

  onCommentAdded(): Observable<any> {
    return this.listen('comment_added');
  }

  onProjectUpdated(): Observable<any> {
    return this.listen('project_updated');
  }

  onUserJoinedProject(): Observable<any> {
    return this.listen('user_joined_project');
  }

  onUserLeftProject(): Observable<any> {
    return this.listen('user_left_project');
  }

  onNotification(): Observable<any> {
    return this.listen('notification');
  }

  // Chat en tiempo real
  onChatMessage(): Observable<any> {
    return this.listen('chat_message');
  }

  sendChatMessage(projectId: string, message: string): void {
    this.emit('send_chat_message', {
      project_id: projectId,
      message: message
    });
  }

  // Presencia de usuarios
  onUserPresence(): Observable<any> {
    return this.listen('user_presence');
  }

  updatePresence(status: 'online' | 'away' | 'busy' | 'offline'): void {
    this.emit('update_presence', { status });
  }

  isConnected(): boolean {
    return this.connectedSubject.value;
  }
}
"""
    
    websocket_service_path = os.path.join(frontend_dir, "src/app/core/services/websocket.service.ts")
    with open(websocket_service_path, "w", encoding="utf-8") as f:
        f.write(websocket_service_content)
    
    print("✓ Servicios core creados")

def create_shared_components(frontend_dir):
    """Crear componentes compartidos"""
    
    # src/app/shared/components/page-header/page-header.component.ts
    page_header_component_content = """import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { BreadcrumbModule } from 'primeng/breadcrumb';

export interface BreadcrumbItem {
  label: string;
  routerLink?: string;
  icon?: string;
}

export interface ActionButton {
  label: string;
  icon: string;
  onClick: () => void;
  severity?: 'success' | 'info' | 'warning' | 'danger' | 'help' | 'primary' | 'secondary';
  disabled?: boolean;
}

@Component({
  selector: 'app-page-header',
  standalone: true,
  imports: [CommonModule, ButtonModule, BreadcrumbModule],
  template: `
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-main">
          <h1 class="page-title">
            <i [class]="titleIcon" *ngIf="titleIcon"></i>
            {{ title }}
          </h1>
          <p class="page-description" *ngIf="description">{{ description }}</p>
          
          <p-breadcrumb 
            [model]="breadcrumbItems" 
            [home]="homeItem"
            *ngIf="breadcrumbs && breadcrumbs.length > 0">
          </p-breadcrumb>
        </div>
        
        <div class="page-header-actions" *ngIf="actions && actions.length > 0">
          <p-button 
            *ngFor="let action of actions"
            [label]="action.label"
            [icon]="action.icon"
            [severity]="action.severity || 'primary'"
            [disabled]="action.disabled"
            (onClick)="action.onClick()"
            class="action-button">
          </p-button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .page-header {
      background: white;
      border-bottom: 1px solid #e0e0e0;
      padding: 1.5rem 2rem;
      margin-bottom: 1.5rem;
    }

    .page-header-content {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      max-width: 100%;
    }

    .page-header-main {
      flex: 1;
    }

    .page-title {
      margin: 0 0 0.5rem 0;
      font-size: 1.75rem;
      font-weight: 600;
      color: #333;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .page-description {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.95rem;
    }

    .page-header-actions {
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
    }

    .action-button {
      white-space: nowrap;
    }

    @media (max-width: 768px) {
      .page-header {
        padding: 1rem;
      }

      .page-header-content {
        flex-direction: column;
        gap: 1rem;
      }

      .page-header-actions {
        width: 100%;
        justify-content: flex-end;
      }

      .page-title {
        font-size: 1.5rem;
      }
    }
  `]
})
export class PageHeaderComponent {
  @Input() title: string = '';
  @Input() description?: string;
  @Input() titleIcon?: string;
  @Input() breadcrumbs?: BreadcrumbItem[];
  @Input() actions?: ActionButton[];

  breadcrumbItems: any[] = [];
  homeItem = { icon: 'pi pi-home', routerLink: '/dashboard' };

  ngOnInit() {
    if (this.breadcrumbs) {
      this.breadcrumbItems = this.breadcrumbs.map(item => ({
        label: item.label,
        routerLink: item.routerLink,
        icon: item.icon
      }));
    }
  }
}
"""
    
    page_header_path = os.path.join(frontend_dir, "src/app/shared/components/page-header/page-header.component.ts")
    os.makedirs(os.path.dirname(page_header_path), exist_ok=True)
    with open(page_header_path, "w", encoding="utf-8") as f:
        f.write(page_header_component_content)
    
    # src/app/shared/components/task-card/task-card.component.ts
    task_card_component_content = """import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { TooltipModule } from 'primeng/tooltip';
import { Task } from '@core/services/task.service';

@Component({
  selector: 'app-task-card',
  standalone: true,
  imports: [
    CommonModule, 
    CardModule, 
    TagModule, 
    ButtonModule, 
    AvatarModule, 
    TooltipModule
  ],
  template: `
    <p-card 
      class="task-card"
      [ngClass]="'task-card-' + task.priority"
      (click)="onCardClick()">
      
      <ng-template pTemplate="header">
        <div class="task-header">
          <div class="task-type-icon">
            <i [class]="getTypeIcon(task.type)" [style.color]="getTypeColor(task.type)"></i>
          </div>
          <div class="task-actions" *ngIf="showActions">
            <p-button 
              icon="pi pi-pencil" 
              severity="secondary" 
              [text]="true"
              size="small"
              (onClick)="onEdit($event)"
              pTooltip="Editar tarea">
            </p-button>
            <p-button 
              icon="pi pi-ellipsis-v" 
              severity="secondary" 
              [text]="true"
              size="small"
              (onClick)="onMenu($event)"
              pTooltip="Más opciones">
            </p-button>
          </div>
        </div>
      </ng-template>

      <div class="task-content">
        <h4 class="task-title">{{ task.title }}</h4>
        
        <p class="task-description" *ngIf="task.description">
          {{ task.description | slice:0:100 }}
          <span *ngIf="task.description.length > 100">...</span>
        </p>

        <div class="task-meta">
          <div class="task-tags" *ngIf="task.tags && task.tags.length > 0">
            <p-tag 
              *ngFor="let tag of task.tags | slice:0:3" 
              [value]="tag" 
              severity="info"
              class="task-tag">
            </p-tag>
            <span *ngIf="task.tags.length > 3" class="more-tags">
              +{{ task.tags.length - 3 }} más
            </span>
          </div>

          <div class="task-priority">
            <p-tag 
              [value]="getPriorityLabel(task.priority)"
              [severity]="getPrioritySeverity(task.priority)"
              [icon]="getPriorityIcon(task.priority)">
            </p-tag>
          </div>
        </div>

        <div class="task-footer">
          <div class="task-assignee" *ngIf="task.assignee">
            <p-avatar 
              [image]="task.assignee.avatar" 
              [label]="getInitials(task.assignee.first_name, task.assignee.last_name)"
              size="small"
              shape="circle"
              [pTooltip]="task.assignee.first_name + ' ' + task.assignee.last_name">
            </p-avatar>
          </div>

          <div class="task-due-date" *ngIf="task.due_date">
            <i class="pi pi-calendar" 
               [ngClass]="{'text-danger': isOverdue(task.due_date)}"></i>
            <span [ngClass]="{'text-danger': isOverdue(task.due_date)}">
              {{ task.due_date | date:'dd/MM' }}
            </span>
          </div>

          <div class="task-story-points" *ngIf="task.story_points">
            <i class="pi pi-chart-bar"></i>
            <span>{{ task.story_points }}pts</span>
          </div>
        </div>
      </div>
    </p-card>
  `,
  styles: [`
    .task-card {
      cursor: pointer;
      transition: all 0.2s ease;
      margin-bottom: 0.75rem;
      border-left: 4px solid #ddd;
    }

    .task-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .task-card-highest { border-left-color: #dc3545; }
    .task-card-high { border-left-color: #fd7e14; }
    .task-card-medium { border-left-color: #ffc107; }
    .task-card-low { border-left-color: #28a745; }
    .task-card-lowest { border-left-color: #6c757d; }

    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .task-type-icon {
      font-size: 1.1rem;
    }

    .task-actions {
      display: flex;
      gap: 0.25rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .task-card:hover .task-actions {
      opacity: 1;
    }

    .task-content {
      padding: 1rem;
    }

    .task-title {
      margin: 0 0 0.5rem 0;
      font-size: 0.95rem;
      font-weight: 600;
      color: #333;
      line-height: 1.3;
    }

    .task-description {
      margin: 0 0 0.75rem 0;
      font-size: 0.85rem;
      color: #666;
      line-height: 1.4;
    }

    .task-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }

    .task-tags {
      display: flex;
      gap: 0.25rem;
      flex-wrap: wrap;
      align-items: center;
    }

    .task-tag {
      font-size: 0.7rem !important;
      padding: 0.2rem 0.4rem !important;
    }

    .more-tags {
      font-size: 0.75rem;
      color: #666;
    }

    .task-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }

    .task-assignee {
      flex-shrink: 0;
    }

    .task-due-date,
    .task-story-points {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.8rem;
      color: #666;
    }

    .text-danger {
      color: #dc3545 !important;
    }

    @media (max-width: 576px) {
      .task-footer {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
      }
      
      .task-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
      }
    }
  `]
})
export class TaskCardComponent {
  @Input() task!: Task;
  @Input() showActions = true;
  
  @Output() cardClick = new EventEmitter<Task>();
  @Output() edit = new EventEmitter<Task>();
  @Output() menu = new EventEmitter<{event: Event, task: Task}>();

  onCardClick(): void {
    this.cardClick.emit(this.task);
  }

  onEdit(event: Event): void {
    event.stopPropagation();
    this.edit.emit(this.task);
  }

  onMenu(event: Event): void {
    event.stopPropagation();
    this.menu.emit({ event, task: this.task });
  }

  getTypeIcon(type: string): string {
    const icons = {
      'story': 'pi pi-bookmark',
      'task': 'pi pi-check-square',
      'bug': 'pi pi-exclamation-triangle',
      'epic': 'pi pi-star',
      'subtask': 'pi pi-angle-right'
    };
    return icons[type as keyof typeof icons] || 'pi pi-circle';
  }

  getTypeColor(type: string): string {
    const colors = {
      'story': '#28a745',
      'task': '#007bff',
      'bug': '#dc3545',
      'epic': '#6f42c1',
      'subtask': '#6c757d'
    };
    return colors[type as keyof typeof colors] || '#6c757d';
  }

  getPriorityLabel(priority: string): string {
    const labels = {
      'highest': 'Muy Alta',
      'high': 'Alta',
      'medium': 'Media',
      'low': 'Baja',
      'lowest': 'Muy Baja'
    };
    return labels[priority as keyof typeof labels] || priority;
  }

  getPrioritySeverity(priority: string): any {
    const severities = {
      'highest': 'danger',
      'high': 'warning',
      'medium': 'info',
      'low': 'success',
      'lowest': 'secondary'
    };
    return severities[priority as keyof typeof severities] || 'info';
  }

  getPriorityIcon(priority: string): string {
    const icons = {
      'highest': 'pi pi-angle-double-up',
      'high': 'pi pi-angle-up',
      'medium': 'pi pi-minus',
      'low': 'pi pi-angle-down',
      'lowest': 'pi pi-angle-double-down'
    };
    return icons[priority as keyof typeof icons] || 'pi pi-minus';
  }

  getInitials(firstName: string, lastName: string): string {
    return (firstName?.[0] || '') + (lastName?.[0] || '');
  }

  isOverdue(dueDate: string): boolean {
    return new Date(dueDate) < new Date() && this.task.status !== 'done';
  }
}
"""
    
    task_card_path = os.path.join(frontend_dir, "src/app/shared/components/task-card/task-card.component.ts")
    os.makedirs(os.path.dirname(task_card_path), exist_ok=True)
    with open(task_card_path, "w", encoding="utf-8") as f:
        f.write(task_card_component_content)
    
    print("✓ Componentes compartidos creados")

def create_feature_modules(frontend_dir):
    """Crear módulos de características principales"""
    
    # src/app/features/dashboard/dashboard.component.ts
    dashboard_component_content = """import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ChartModule } from 'primeng/chart';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { ProgressBarModule } from 'primeng/progressbar';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { ProjectService, Project } from '@core/services/project.service';
import { TaskService, Task } from '@core/services/task.service';
import { AuthService } from '@core/services/auth.service';

interface DashboardStats {
  totalProjects: number;
  activeProjects: number;
  totalTasks: number;
  completedTasks: number;
  myTasks: number;
  overdueTasks: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    CardModule,
    ChartModule,
    TableModule,
    TagModule,
    ButtonModule,
    ProgressBarModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Panel de Control"
      description="Resumen general de tus proyectos y tareas"
      titleIcon="pi pi-th-large">
    </app-page-header>

    <div class="dashboard-container">
      <!-- Estadísticas principales -->
      <div class="stats-grid">
        <p-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon projects">
              <i class="pi pi-folder"></i>
            </div>
            <div class="stat-details">
              <h3>{{ stats.totalProjects }}</h3>
              <p>Proyectos Total</p>
              <small>{{ stats.activeProjects }} activos</small>
            </div>
          </div>
        </p-card>

        <p-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon tasks">
              <i class="pi pi-check-square"></i>
            </div>
            <div class="stat-details">
              <h3>{{ stats.totalTasks }}</h3>
              <p>Tareas Total</p>
              <small>{{ stats.completedTasks }} completadas</small>
            </div>
          </div>
        </p-card>

        <p-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon my-tasks">
              <i class="pi pi-user"></i>
            </div>
            <div class="stat-details">
              <h3>{{ stats.myTasks }}</h3>
              <p>Mis Tareas</p>
              <small>Asignadas a mí</small>
            </div>
          </div>
        </p-card>

        <p-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon overdue">
              <i class="pi pi-clock"></i>
            </div>
            <div class="stat-details">
              <h3>{{ stats.overdueTasks }}</h3>
              <p>Vencidas</p>
              <small>Requieren atención</small>
            </div>
          </div>
        </p-card>
      </div>

      <div class="dashboard-content">
        <!-- Proyectos recientes -->
        <div class="dashboard-section">
          <p-card header="Proyectos Recientes">
            <ng-template pTemplate="header">
              <div class="card-header">
                <h4>Proyectos Recientes</h4>
                <p-button 
                  label="Ver todos" 
                  icon="pi pi-arrow-right" 
                  [text]="true"
                  routerLink="/projects">
                </p-button>
              </div>
            </ng-template>

            <div class="projects-list" *ngIf="recentProjects.length > 0; else noProjects">
              <div 
                *ngFor="let project of recentProjects" 
                class="project-item"
                [routerLink]="['/projects', project.id]">
                <div class="project-info">
                  <h5>{{ project.name }}</h5>
                  <p>{{ project.description || 'Sin descripción' }}</p>
                  <div class="project-meta">
                    <p-tag 
                      [value]="getStatusLabel(project.status)"
                      [severity]="getStatusSeverity(project.status)">
                    </p-tag>
                    <span class="project-key">{{ project.key }}</span>
                  </div>
                </div>
                <div class="project-progress">
                  <p-progressBar 
                    [value]="getProjectProgress(project)"
                    [showValue]="false">
                  </p-progressBar>
                  <small>{{ getProjectProgress(project) }}% completado</small>
                </div>
              </div>
            </div>

            <ng-template #noProjects>
              <div class="empty-state">
                <i class="pi pi-folder empty-icon"></i>
                <h4>No hay proyectos</h4>
                <p>Crea tu primer proyecto para comenzar</p>
                <p-button 
                  label="Crear Proyecto" 
                  icon="pi pi-plus"
                  routerLink="/projects/new">
                </p-button>
              </div>
            </ng-template>
          </p-card>
        </div>

        <!-- Mis tareas pendientes -->
        <div class="dashboard-section">
          <p-card header="Mis Tareas Pendientes">
            <ng-template pTemplate="header">
              <div class="card-header">
                <h4>Mis Tareas Pendientes</h4>
                <p-button 
                  label="Ver todas" 
                  icon="pi pi-arrow-right" 
                  [text]="true"
                  routerLink="/tasks">
                </p-button>
              </div>
            </ng-template>

            <div class="tasks-list" *ngIf="myTasks.length > 0; else noTasks">
              <div *ngFor="let task of myTasks" class="task-item">
                <div class="task-priority">
                  <i [class]="getPriorityIcon(task.priority)" 
                     [style.color]="getPriorityColor(task.priority)"></i>
                </div>
                <div class="task-content">
                  <h6>{{ task.title }}</h6>
                  <p>{{ task.project?.name }}</p>
                  <div class="task-meta">
                    <p-tag 
                      [value]="getTaskStatusLabel(task.status)"
                      [severity]="getTaskStatusSeverity(task.status)">
                    </p-tag>
                    <span *ngIf="task.due_date" 
                          class="task-due"
                          [ngClass]="{'overdue': isTaskOverdue(task.due_date)}">
                      <i class="pi pi-calendar"></i>
                      {{ task.due_date | date:'dd/MM/yyyy' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <ng-template #noTasks>
              <div class="empty-state">
                <i class="pi pi-check empty-icon"></i>
                <h4>¡Todo al día!</h4>
                <p>No tienes tareas pendientes</p>
              </div>
            </ng-template>
          </p-card>
        </div>
      </div>

      <!-- Gráfico de actividad -->
      <div class="dashboard-chart">
        <p-card header="Actividad de Tareas">
          <p-chart 
            type="line" 
            [data]="chartData" 
            [options]="chartOptions"
            width="100%"
            height="300px">
          </p-chart>
        </p-card>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 0 2rem 2rem;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    .stat-card {
      border-left: 4px solid #007bff;
    }

    .stat-content {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      color: white;
    }

    .stat-icon.projects { background: #007bff; }
    .stat-icon.tasks { background: #28a745; }
    .stat-icon.my-tasks { background: #17a2b8; }
    .stat-icon.overdue { background: #dc3545; }

    .stat-details h3 {
      margin: 0;
      font-size: 2rem;
      font-weight: 700;
      color: #333;
    }

    .stat-details p {
      margin: 0;
      color: #666;
      font-weight: 500;
    }

    .stat-details small {
      color: #999;
    }

    .dashboard-content {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin-bottom: 2rem;
    }

    .dashboard-chart {
      grid-column: 1 / -1;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      background: #f8f9fa;
      margin: -1.5rem -1.5rem 1.5rem -1.5rem;
    }

    .card-header h4 {
      margin: 0;
      color: #333;
    }

    .projects-list, .tasks-list {
      max-height: 400px;
      overflow-y: auto;
    }

    .project-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border: 1px solid #eee;
      border-radius: 8px;
      margin-bottom: 0.75rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .project-item:hover {
      background: #f8f9fa;
      border-color: #007bff;
    }

    .project-info h5 {
      margin: 0 0 0.25rem 0;
      color: #333;
    }

    .project-info p {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.9rem;
    }

    .project-meta {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }

    .project-key {
      background: #e9ecef;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.8rem;
      font-weight: 500;
    }

    .project-progress {
      min-width: 120px;
      text-align: right;
    }

    .project-progress small {
      display: block;
      margin-top: 0.25rem;
      color: #666;
    }

    .task-item {
      display: flex;
      gap: 1rem;
      padding: 0.75rem;
      border: 1px solid #eee;
      border-radius: 8px;
      margin-bottom: 0.5rem;
    }

    .task-priority {
      flex-shrink: 0;
      display: flex;
      align-items: center;
    }

    .task-content {
      flex: 1;
    }

    .task-content h6 {
      margin: 0 0 0.25rem 0;
      color: #333;
    }

    .task-content p {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.85rem;
    }

    .task-meta {
      display: flex;
      gap: 0.75rem;
      align-items: center;
    }

    .task-due {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.8rem;
      color: #666;
    }

    .task-due.overdue {
      color: #dc3545;
    }

    .empty-state {
      text-align: center;
      padding: 3rem 1rem;
      color: #666;
    }

    .empty-icon {
      font-size: 3rem;
      color: #ccc;
      margin-bottom: 1rem;
    }

    .empty-state h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }

    .empty-state p {
      margin: 0 0 1.5rem 0;
    }

    @media (max-width: 768px) {
      .dashboard-container {
        padding: 0 1rem 1rem;
      }

      .dashboard-content {
        grid-template-columns: 1fr;
        gap: 1rem;
      }

      .stats-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
      }

      .stat-content {
        gap: 0.75rem;
      }

      .stat-icon {
        width: 50px;
        height: 50px;
        font-size: 1.25rem;
      }

      .project-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
      }

      .project-progress {
        width: 100%;
        min-width: auto;
      }
    }
  `]
})
export class DashboardComponent implements OnInit {
  stats: DashboardStats = {
    totalProjects: 0,
    activeProjects: 0,
    totalTasks: 0,
    completedTasks: 0,
    myTasks: 0,
    overdueTasks: 0
  };

  recentProjects: Project[] = [];
  myTasks: Task[] = [];
  
  chartData: any;
  chartOptions: any;

  constructor(
    private projectService: ProjectService,
    private taskService: TaskService,
    private authService: AuthService
  ) {
    this.initializeChart();
  }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  private loadDashboardData(): void {
    // Cargar proyectos recientes
    this.projectService.getProjects({ page: 1, page_size: 5 }).subscribe(
      response => {
        this.recentProjects = response.data;
        this.stats.totalProjects = response.total;
        this.stats.activeProjects = response.data.filter(p => p.status === 'active').length;
      }
    );

    // Cargar mis tareas
    this.taskService.getMyTasks().subscribe(
      tasks => {
        this.myTasks = tasks.slice(0, 8);
        this.stats.myTasks = tasks.length;
        this.stats.totalTasks = tasks.length; // Esto debería venir de una API específica
        this.stats.completedTasks = tasks.filter(t => t.status === 'done').length;
        this.stats.overdueTasks = tasks.filter(t => this.isTaskOverdue(t.due_date)).length;
      }
    );
  }

  private initializeChart(): void {
    this.chartData = {
      labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
      datasets: [
        {
          label: 'Tareas Completadas',
          data: [12, 19, 3, 5, 2, 3, 9],
          borderColor: '#007bff',
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'Tareas Creadas',
          data: [5, 8, 12, 7, 15, 4, 11],
          borderColor: '#28a745',
          backgroundColor: 'rgba(40, 167, 69, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    };

    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };
  }

  getStatusLabel(status: string): string {
    const labels = {
      'planning': 'Planificación',
      'active': 'Activo',
      'on_hold': 'En Pausa',
      'completed': 'Completado',
      'archived': 'Archivado'
    };
    return labels[status as keyof typeof labels] || status;
  }

  getStatusSeverity(status: string): any {
    const severities = {
      'planning': 'info',
      'active': 'success',
      'on_hold': 'warning',
      'completed': 'info',
      'archived': 'secondary'
    };
    return severities[status as keyof typeof severities] || 'info';
  }

  getTaskStatusLabel(status: string): string {
    const labels = {
      'todo': 'Por Hacer',
      'in_progress': 'En Progreso',
      'in_review': 'En Revisión',
      'done': 'Completado',
      'blocked': 'Bloqueado'
    };
    return labels[status as keyof typeof labels] || status;
  }

  getTaskStatusSeverity(status: string): any {
    const severities = {
      'todo': 'secondary',
      'in_progress': 'info',
      'in_review': 'warning',
      'done': 'success',
      'blocked': 'danger'
    };
    return severities[status as keyof typeof severities] || 'info';
  }

  getPriorityIcon(priority: string): string {
    const icons = {
      'highest': 'pi pi-angle-double-up',
      'high': 'pi pi-angle-up',
      'medium': 'pi pi-minus',
      'low': 'pi pi-angle-down',
      'lowest': 'pi pi-angle-double-down'
    };
    return icons[priority as keyof typeof icons] || 'pi pi-minus';
  }

  getPriorityColor(priority: string): string {
    const colors = {
      'highest': '#dc3545',
      'high': '#fd7e14',
      'medium': '#ffc107',
      'low': '#28a745',
      'lowest': '#6c757d'
    };
    return colors[priority as keyof typeof colors] || '#6c757d';
  }

  getProjectProgress(project: Project): number {
    // Lógica simulada para calcular progreso
    // En una implementación real, esto vendría de la API
    return Math.floor(Math.random() * 100);
  }

  isTaskOverdue(dueDate: string | undefined): boolean {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date();
  }
}
"""
    
    dashboard_path = os.path.join(frontend_dir, "src/app/features/dashboard/dashboard.component.ts")
    os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_component_content)
    
    # src/app/features/kanban/kanban-board.component.ts
    kanban_component_content = """import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DragDropModule, CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { TaskCardComponent } from '@shared/components/task-card/task-card.component';
import { TaskService, Task } from '@core/services/task.service';
import { WebSocketService } from '@core/services/websocket.service';

interface BoardColumn {
  id: string;
  title: string;
  status: string;
  tasks: Task[];
  wipLimit?: number;
  color: string;
}

@Component({
  selector: 'app-kanban-board',
  standalone: true,
  imports: [
    CommonModule,
    DragDropModule,
    CardModule,
    ButtonModule,
    DialogModule,
    TaskCardComponent
  ],
  template: `
    <div class="kanban-board">
      <div class="board-header">
        <h2>Tablero Kanban</h2>
        <div class="board-actions">
          <p-button 
            label="Agregar Tarea"
            icon="pi pi-plus"
            (onClick)="showCreateTaskDialog()">
          </p-button>
          <p-button 
            label="Configurar Tablero"
            icon="pi pi-cog"
            severity="secondary"
            [outlined]="true"
            (onClick)="showBoardConfig()">
          </p-button>
        </div>
      </div>

      <div class="board-columns" cdkDropListGroup>
        <div 
          *ngFor="let column of columns; trackBy: trackByColumn"
          class="board-column"
          [style.border-top-color]="column.color">
          
          <div class="column-header">
            <div class="column-title">
              <h3>{{ column.title }}</h3>
              <span class="task-count">{{ column.tasks.length }}</span>
              <span 
                *ngIf="column.wipLimit && column.tasks.length > column.wipLimit"
                class="wip-violation">
                ⚠️ WIP Limit: {{ column.wipLimit }}
              </span>
            </div>
            <div class="column-actions">
              <p-button 
                icon="pi pi-plus"
                severity="secondary"
                [text]="true"
                size="small"
                (onClick)="addTaskToColumn(column)"
                pTooltip="Agregar tarea">
              </p-button>
            </div>
          </div>

          <div 
            class="column-content"
            cdkDropList
            [cdkDropListData]="column.tasks"
            [id]="column.id"
            (cdkDropListDropped)="onTaskDrop($event)">
            
            <div 
              *ngFor="let task of column.tasks; trackBy: trackByTask"
              cdkDrag
              [cdkDragData]="task"
              class="task-wrapper">
              
              <app-task-card
                [task]="task"
                (cardClick)="openTaskDetail($event)"
                (edit)="editTask($event)"
                (menu)="showTaskMenu($event)">
              </app-task-card>

              <!-- Placeholder para drag -->
              <div 
                *cdkDragPlaceholder 
                class="task-placeholder">
                Soltar aquí...
              </div>
            </div>

            <!-- Zona de drop vacía -->
            <div 
              *ngIf="column.tasks.length === 0"
              class="empty-column">
              <i class="pi pi-inbox"></i>
              <p>No hay tareas</p>
              <small>Arrastra tareas aquí o crea una nueva</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialog para crear/editar tarea -->
    <p-dialog 
      header="Crear Tarea"
      [(visible)]="showTaskDialog"
      [modal]="true"
      [style]="{width: '600px'}"
      [closable]="true">
      
      <!-- Aquí iría el formulario de tarea -->
      <p>Formulario de crear/editar tarea (por implementar)</p>
      
      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [outlined]="true"
          (onClick)="closeTaskDialog()">
        </p-button>
        <p-button 
          label="Guardar"
          (onClick)="saveTask()">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .kanban-board {
      height: 100%;
      display: flex;
      flex-direction: column;
      background: #f5f5f5;
    }

    .board-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 2rem;
      background: white;
      border-bottom: 1px solid #e0e0e0;
    }

    .board-header h2 {
      margin: 0;
      color: #333;
    }

    .board-actions {
      display: flex;
      gap: 0.5rem;
    }

    .board-columns {
      display: flex;
      gap: 1rem;
      padding: 1rem;
      overflow-x: auto;
      flex: 1;
      min-height: 0;
    }

    .board-column {
      flex: 0 0 300px;
      background: white;
      border-radius: 8px;
      border-top: 4px solid #007bff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      max-height: calc(100vh - 200px);
    }

    .column-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .column-title h3 {
      margin: 0;
      font-size: 1rem;
      color: #333;
    }

    .task-count {
      background: #6c757d;
      color: white;
      padding: 0.2rem 0.5rem;
      border-radius: 12px;
      font-size: 0.75rem;
      margin-left: 0.5rem;
    }

    .wip-violation {
      color: #dc3545;
      font-size: 0.75rem;
      margin-left: 0.5rem;
    }

    .column-content {
      flex: 1;
      padding: 0.5rem;
      overflow-y: auto;
      min-height: 200px;
    }

    .task-wrapper {
      margin-bottom: 0.5rem;
    }

    .task-placeholder {
      background: #e9ecef;
      border: 2px dashed #adb5bd;
      border-radius: 4px;
      padding: 1rem;
      text-align: center;
      color: #6c757d;
      margin-bottom: 0.5rem;
    }

    .empty-column {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
      text-align: center;
      color: #6c757d;
      min-height: 150px;
    }

    .empty-column i {
      font-size: 2rem;
      margin-bottom: 0.5rem;
      opacity: 0.5;
    }

    .empty-column p {
      margin: 0 0 0.25rem 0;
      font-weight: 500;
    }

    .empty-column small {
      opacity: 0.7;
    }

    /* Drag and drop styles */
    .cdk-drag-preview {
      box-sizing: border-box;
      border-radius: 4px;
      box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
                  0 8px 10px 1px rgba(0, 0, 0, 0.14),
                  0 3px 14px 2px rgba(0, 0, 0, 0.12);
      transform: rotate(5deg);
    }

    .cdk-drag-animating {
      transition: transform 250ms cubic-bezier(0, 0, 0.2, 1);
    }

    .cdk-drop-list-dragging .cdk-drag:not(.cdk-drag-placeholder) {
      transition: transform 250ms cubic-bezier(0, 0, 0.2, 1);
    }

    .cdk-drop-list-receiving {
      background: rgba(0, 123, 255, 0.05);
    }

    @media (max-width: 768px) {
      .board-header {
        flex-direction: column;
        gap: 1rem;
        align-items: flex-start;
      }

      .board-columns {
        flex-direction: column;
        padding: 0.5rem;
      }

      .board-column {
        flex: none;
        max-height: 400px;
      }
    }
  `]
})
export class KanbanBoardComponent implements OnInit {
  @Input() projectId!: string;

  columns: BoardColumn[] = [
    {
      id: 'todo',
      title: 'Por Hacer',
      status: 'todo',
      tasks: [],
      color: '#6c757d'
    },
    {
      id: 'in_progress',
      title: 'En Progreso',
      status: 'in_progress',
      tasks: [],
      wipLimit: 3,
      color: '#007bff'
    },
    {
      id: 'in_review',
      title: 'En Revisión',
      status: 'in_review',
      tasks: [],
      wipLimit: 2,
      color: '#ffc107'
    },
    {
      id: 'done',
      title: 'Completado',
      status: 'done',
      tasks: [],
      color: '#28a745'
    }
  ];

  showTaskDialog = false;
  selectedTask: Task | null = null;

  constructor(
    private taskService: TaskService,
    private wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.loadTasks();
    this.subscribeToUpdates();
  }

  private loadTasks(): void {
    if (!this.projectId) return;

    this.taskService.getTasks(this.projectId).subscribe(
      response => {
        this.distributeTasks(response.data);
      }
    );
  }

  private distributeTasks(tasks: Task[]): void {
    // Limpiar columnas
    this.columns.forEach(column => column.tasks = []);

    // Distribuir tareas por estado
    tasks.forEach(task => {
      const column = this.columns.find(col => col.status === task.status);
      if (column) {
        column.tasks.push(task);
      }
    });

    // Ordenar tareas por posición
    this.columns.forEach(column => {
      column.tasks.sort((a, b) => a.position - b.position);
    });
  }

  private subscribeToUpdates(): void {
    if (!this.projectId) return;

    // Suscribirse al proyecto para recibir actualizaciones
    this.wsService.subscribeToProject(this.projectId);

    // Escuchar actualizaciones de tareas
    this.wsService.onTaskUpdated().subscribe(update => {
      this.handleTaskUpdate(update);
    });

    this.wsService.onTaskCreated().subscribe(task => {
      this.handleTaskCreated(task);
    });

    this.wsService.onTaskMoved().subscribe(update => {
      this.handleTaskMoved(update);
    });
  }

  onTaskDrop(event: CdkDragDrop<Task[]>): void {
    if (event.previousContainer === event.container) {
      // Mover dentro de la misma columna
      moveItemInArray(
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    } else {
      // Mover a otra columna
      const task = event.previousContainer.data[event.previousIndex];
      const targetColumn = this.columns.find(col => 
        col.tasks === event.container.data
      );

      if (targetColumn) {
        // Verificar WIP limit
        if (targetColumn.wipLimit && 
            event.container.data.length >= targetColumn.wipLimit) {
          // Mostrar mensaje de error o manejar violación de WIP limit
          console.warn(`WIP limit exceeded for column ${targetColumn.title}`);
          return;
        }

        transferArrayItem(
          event.previousContainer.data,
          event.container.data,
          event.previousIndex,
          event.currentIndex
        );

        // Actualizar estado en el backend
        this.updateTaskStatus(task, targetColumn.status, event.currentIndex);
      }
    }
  }

  private updateTaskStatus(task: Task, newStatus: string, newPosition: number): void {
    this.taskService.moveTaskToPosition(task.id, newPosition, newStatus).subscribe(
      updatedTask => {
        // Actualizar tarea local
        const taskIndex = this.findTaskIndex(task.id);
        if (taskIndex) {
          taskIndex.column.tasks[taskIndex.index] = updatedTask;
        }
      },
      error => {
        console.error('Error updating task:', error);
        // Revertir cambio visual si hay error
        this.loadTasks();
      }
    );
  }

  private findTaskIndex(taskId: string): {column: BoardColumn, index: number} | null {
    for (const column of this.columns) {
      const index = column.tasks.findIndex(t => t.id === taskId);
      if (index !== -1) {
        return { column, index };
      }
    }
    return null;
  }

  private handleTaskUpdate(update: any): void {
    const taskIndex = this.findTaskIndex(update.task.id);
    if (taskIndex) {
      taskIndex.column.tasks[taskIndex.index] = update.task;
    }
  }

  private handleTaskCreated(task: Task): void {
    const column = this.columns.find(col => col.status === task.status);
    if (column) {
      column.tasks.push(task);
    }
  }

  private handleTaskMoved(update: any): void {
    // Recargar tareas para reflejar el movimiento
    this.loadTasks();
  }

  trackByColumn(index: number, column: BoardColumn): string {
    return column.id;
  }

  trackByTask(index: number, task: Task): string {
    return task.id;
  }

  showCreateTaskDialog(): void {
    this.selectedTask = null;
    this.showTaskDialog = true;
  }

  addTaskToColumn(column: BoardColumn): void {
    // Lógica para agregar tarea directamente a una columna
    this.showCreateTaskDialog();
  }

  openTaskDetail(task: Task): void {
    // Abrir modal de detalle de tarea
    console.log('Open task detail:', task);
  }

  editTask(task: Task): void {
    this.selectedTask = task;
    this.showTaskDialog = true;
  }

  showTaskMenu(event: {event: Event, task: Task}): void {
    // Mostrar menú contextual para la tarea
    console.log('Show task menu:', event);
  }

  showBoardConfig(): void {
    // Mostrar configuración del tablero
    console.log('Show board config');
  }

  closeTaskDialog(): void {
    this.showTaskDialog = false;
    this.selectedTask = null;
  }

  saveTask(): void {
    // Guardar tarea
    console.log('Save task');
    this.closeTaskDialog();
  }
}
"""
    
    kanban_path = os.path.join(frontend_dir, "src/app/features/kanban/kanban-board.component.ts")
    os.makedirs(os.path.dirname(kanban_path), exist_ok=True)
    with open(kanban_path, "w", encoding="utf-8") as f:
        f.write(kanban_component_content)
    
    print("✓ Módulos de características creados")

def create_layout_components(frontend_dir):
    """Crear componentes de layout"""
    
    # src/app/layout/main-layout/main-layout.component.ts
    layout_component_content = """import { Component, OnInit } from '@angular/core';
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
"""
    
    layout_path = os.path.join(frontend_dir, "src/app/layout/main-layout/main-layout.component.ts")
    os.makedirs(os.path.dirname(layout_path), exist_ok=True)
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_component_content)
    
    print("✓ Componentes de layout creados")

def create_guards_interceptors(frontend_dir):
    """Crear guards e interceptors"""
    
    # src/app/core/guards/auth.guard.ts
    auth_guard_content = """import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable, map } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): Observable<boolean | UrlTree> {
    return this.authService.isAuthenticated$.pipe(
      map(isAuthenticated => {
        if (isAuthenticated) {
          return true;
        } else {
          return this.router.createUrlTree(['/auth/login']);
        }
      })
    );
  }
}
"""
    
    auth_guard_path = os.path.join(frontend_dir, "src/app/core/guards/auth.guard.ts")
    os.makedirs(os.path.dirname(auth_guard_path), exist_ok=True)
    with open(auth_guard_path, "w", encoding="utf-8") as f:
        f.write(auth_guard_content)
    
    # src/app/core/interceptors/auth.interceptor.ts
    auth_interceptor_content = """import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, switchMap, catchError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Agregar token de autorización si existe
    const token = this.authService.getToken();
    
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          // Token expirado o inválido
          return this.handle401Error(request, next);
        }
        
        return throwError(() => error);
      })
    );
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Intentar renovar el token
    return this.authService.refreshToken().pipe(
      switchMap(() => {
        // Reintentar la petición original con el nuevo token
        const newToken = this.authService.getToken();
        request = request.clone({
          setHeaders: {
            Authorization: `Bearer ${newToken}`
          }
        });
        return next.handle(request);
      }),
      catchError((refreshError) => {
        // Si la renovación falla, cerrar sesión
        this.authService.logout();
        this.router.navigate(['/auth/login']);
        return throwError(() => refreshError);
      })
    );
  }
}
"""
    
    auth_interceptor_path = os.path.join(frontend_dir, "src/app/core/interceptors/auth.interceptor.ts")
    os.makedirs(os.path.dirname(auth_interceptor_path), exist_ok=True)
    with open(auth_interceptor_path, "w", encoding="utf-8") as f:
        f.write(auth_interceptor_content)
    
    print("✓ Guards e interceptors creados")

if __name__ == "__main__":
    create_frontend_core()
