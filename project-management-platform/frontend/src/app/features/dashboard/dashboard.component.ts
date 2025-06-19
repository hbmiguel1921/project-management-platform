import { Component, OnInit } from '@angular/core';
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
