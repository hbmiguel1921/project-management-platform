import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { ProgressBarModule } from 'primeng/progressbar';
import { CalendarModule } from 'primeng/calendar';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { ChartModule } from 'primeng/chart';
import { TimelineModule } from 'primeng/timeline';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { SprintService, Sprint } from '@core/services/sprint.service';

@Component({
  selector: 'app-sprint-board',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    TagModule,
    ProgressBarModule,
    CalendarModule,
    InputTextModule,
    InputTextareaModule,
    DialogModule,
    DropdownModule,
    ChartModule,
    TimelineModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Gestión de Sprints"
      description="Planifica y gestiona sprints ágiles"
      titleIcon="pi pi-chart-line"
      [actions]="headerActions">
    </app-page-header>

    <div class="sprint-container">
      <!-- Sprint actual -->
      <div class="current-sprint" *ngIf="currentSprint">
        <p-card>
          <ng-template pTemplate="header">
            <div class="sprint-header">
              <div class="sprint-info">
                <h2>{{ currentSprint.name }}</h2>
                <p-tag 
                  [value]="getStatusLabel(currentSprint.status)"
                  [severity]="getStatusSeverity(currentSprint.status)">
                </p-tag>
              </div>
              <div class="sprint-actions">
                <p-button 
                  *ngIf="currentSprint.status === 'planning'"
                  label="Iniciar Sprint"
                  icon="pi pi-play"
                  (onClick)="startSprint(currentSprint)">
                </p-button>
                <p-button 
                  *ngIf="currentSprint.status === 'active'"
                  label="Completar Sprint"
                  icon="pi pi-check"
                  severity="success"
                  (onClick)="completeSprint(currentSprint)">
                </p-button>
                <p-button 
                  icon="pi pi-cog"
                  severity="secondary"
                  [text]="true"
                  (onClick)="editSprint(currentSprint)">
                </p-button>
              </div>
            </div>
          </ng-template>

          <div class="sprint-content">
            <div class="sprint-details">
              <p class="sprint-goal" *ngIf="currentSprint.goal">
                <strong>Objetivo:</strong> {{ currentSprint.goal }}
              </p>
              <div class="sprint-dates">
                <span><strong>Inicio:</strong> {{ currentSprint.start_date | date:'dd/MM/yyyy' }}</span>
                <span><strong>Fin:</strong> {{ currentSprint.end_date | date:'dd/MM/yyyy' }}</span>
                <span *ngIf="currentSprint.status === 'active'">
                  <strong>Días restantes:</strong> {{ getDaysRemaining(currentSprint) }}
                </span>
              </div>
            </div>

            <!-- Métricas del sprint -->
            <div class="sprint-metrics" *ngIf="currentSprint.status === 'active' || currentSprint.status === 'completed'">
              <div class="metrics-grid">
                <div class="metric-item">
                  <h4>{{ currentSprint.completed_points }}</h4>
                  <p>Puntos Completados</p>
                </div>
                <div class="metric-item">
                  <h4>{{ currentSprint.committed_points }}</h4>
                  <p>Puntos Comprometidos</p>
                </div>
                <div class="metric-item">
                  <h4>{{ currentSprint.velocity }}%</h4>
                  <p>Velocidad</p>
                </div>
                <div class="metric-item">
                  <h4>{{ getTasksCount(currentSprint) }}</h4>
                  <p>Tareas</p>
                </div>
              </div>

              <!-- Barra de progreso -->
              <div class="progress-section">
                <label>Progreso del Sprint</label>
                <p-progressBar 
                  [value]="getSprintProgress(currentSprint)"
                  [showValue]="true">
                </p-progressBar>
              </div>
            </div>

            <!-- Chart de burndown -->
            <div class="burndown-chart" *ngIf="currentSprint.status === 'active' && burndownData">
              <h3>Burndown Chart</h3>
              <p-chart 
                type="line" 
                [data]="burndownData" 
                [options]="burndownOptions"
                width="100%"
                height="300px">
              </p-chart>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Lista de sprints -->
      <div class="sprints-list">
        <div class="list-header">
          <h3>Todos los Sprints</h3>
          <div class="list-filters">
            <p-dropdown 
              [options]="statusOptions"
              [(ngModel)]="selectedStatus"
              placeholder="Filtrar por estado"
              (onChange)="onStatusFilter()"
              [showClear]="true">
            </p-dropdown>
          </div>
        </div>

        <div class="sprints-grid">
          <p-card 
            *ngFor="let sprint of sprints; trackBy: trackBySprint"
            class="sprint-card"
            [class.current]="sprint.id === currentSprint?.id">
            
            <ng-template pTemplate="header">
              <div class="card-header">
                <h4>{{ sprint.name }}</h4>
                <p-tag 
                  [value]="getStatusLabel(sprint.status)"
                  [severity]="getStatusSeverity(sprint.status)">
                </p-tag>
              </div>
            </ng-template>

            <div class="card-content">
              <p class="sprint-description" *ngIf="sprint.description">
                {{ sprint.description }}
              </p>
              
              <div class="sprint-dates">
                <small>{{ sprint.start_date | date:'dd/MM' }} - {{ sprint.end_date | date:'dd/MM/yyyy' }}</small>
              </div>

              <div class="sprint-stats" *ngIf="sprint.status !== 'planning'">
                <div class="stat">
                  <span class="label">Progreso:</span>
                  <span class="value">{{ getSprintProgress(sprint) }}%</span>
                </div>
                <div class="stat">
                  <span class="label">Tareas:</span>
                  <span class="value">{{ getTasksCount(sprint) }}</span>
                </div>
              </div>
            </div>

            <ng-template pTemplate="footer">
              <div class="card-actions">
                <p-button 
                  label="Ver Detalles"
                  icon="pi pi-eye"
                  [text]="true"
                  size="small"
                  [routerLink]="['/sprints', sprint.id]">
                </p-button>
                <p-button 
                  *ngIf="sprint.status === 'planning'"
                  label="Editar"
                  icon="pi pi-pencil"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="editSprint(sprint)">
                </p-button>
                <p-button 
                  *ngIf="sprint.status === 'planning'"
                  label="Iniciar"
                  icon="pi pi-play"
                  size="small"
                  (onClick)="startSprint(sprint)">
                </p-button>
              </div>
            </ng-template>
          </p-card>
        </div>
      </div>
    </div>

    <!-- Dialog para crear/editar sprint -->
    <p-dialog 
      header="{{ editingSprintId ? 'Editar Sprint' : 'Nuevo Sprint' }}"
      [(visible)]="showSprintDialog"
      [modal]="true"
      [style]="{width: '600px'}"
      [closable]="true">
      
      <form class="sprint-form">
        <div class="form-group">
          <label>Nombre del Sprint *</label>
          <input 
            type="text"
            pInputText
            [(ngModel)]="sprintForm.name"
            name="name"
            placeholder="Ej: Sprint 1"
            class="form-control">
        </div>

        <div class="form-group">
          <label>Descripción</label>
          <textarea 
            pInputTextarea
            [(ngModel)]="sprintForm.description"
            name="description"
            rows="3"
            placeholder="Descripción del sprint"
            class="form-control">
          </textarea>
        </div>

        <div class="form-group">
          <label>Objetivo del Sprint</label>
          <textarea 
            pInputTextarea
            [(ngModel)]="sprintForm.goal"
            name="goal"
            rows="2"
            placeholder="¿Qué se quiere lograr en este sprint?"
            class="form-control">
          </textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha de Inicio *</label>
            <p-calendar 
              [(ngModel)]="sprintForm.start_date"
              name="start_date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>

          <div class="form-group">
            <label>Fecha de Fin *</label>
            <p-calendar 
              [(ngModel)]="sprintForm.end_date"
              name="end_date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>
        </div>

        <div class="form-group">
          <label>Capacidad (Story Points)</label>
          <input 
            type="number"
            pInputText
            [(ngModel)]="sprintForm.capacity"
            name="capacity"
            min="0"
            placeholder="0"
            class="form-control">
        </div>
      </form>

      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [text]="true"
          (onClick)="cancelSprintDialog()">
        </p-button>
        <p-button 
          [label]="editingSprintId ? 'Actualizar' : 'Crear'"
          (onClick)="saveSprint()"
          [loading]="savingSprint">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .sprint-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Sprint actual */
    .current-sprint {
      margin-bottom: 2rem;
    }

    .sprint-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      margin: -1rem -1rem 0 -1rem;
    }

    .sprint-header h2 {
      margin: 0 0 0.5rem 0;
      color: white;
    }

    .sprint-actions {
      display: flex;
      gap: 0.5rem;
    }

    .sprint-content {
      padding: 1.5rem;
    }

    .sprint-details {
      margin-bottom: 1.5rem;
    }

    .sprint-goal {
      margin: 0 0 1rem 0;
      padding: 1rem;
      background: #f8f9fa;
      border-left: 4px solid #007bff;
      border-radius: 4px;
    }

    .sprint-dates {
      display: flex;
      gap: 2rem;
      font-size: 0.9rem;
      color: #666;
    }

    .sprint-dates span {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* Métricas */
    .sprint-metrics {
      margin-bottom: 2rem;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .metric-item {
      text-align: center;
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .metric-item h4 {
      margin: 0 0 0.5rem 0;
      font-size: 1.8rem;
      color: #007bff;
    }

    .metric-item p {
      margin: 0;
      font-size: 0.9rem;
      color: #666;
    }

    .progress-section {
      margin-top: 1rem;
    }

    .progress-section label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 600;
      color: #333;
    }

    /* Burndown chart */
    .burndown-chart {
      margin-top: 2rem;
      padding: 1.5rem;
      background: #f8f9fa;
      border-radius: 8px;
    }

    .burndown-chart h3 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    /* Lista de sprints */
    .list-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .list-header h3 {
      margin: 0;
      color: #333;
    }

    .list-filters {
      display: flex;
      gap: 1rem;
    }

    .sprints-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 1.5rem;
    }

    .sprint-card {
      transition: transform 0.2s ease;
    }

    .sprint-card:hover {
      transform: translateY(-2px);
    }

    .sprint-card.current {
      border: 2px solid #007bff;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .card-header h4 {
      margin: 0;
      color: #333;
    }

    .card-content {
      padding: 1rem;
    }

    .sprint-description {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.9rem;
      line-height: 1.4;
    }

    .sprint-stats {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
    }

    .stat {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }

    .stat .label {
      font-size: 0.8rem;
      color: #999;
    }

    .stat .value {
      font-weight: 600;
      color: #333;
    }

    .card-actions {
      display: flex;
      gap: 0.5rem;
      justify-content: flex-end;
      padding: 1rem;
      background: #f8f9fa;
      margin: 0 -1rem -1rem -1rem;
    }

    /* Dialog de sprint */
    .sprint-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-weight: 600;
      color: #333;
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    .form-control {
      width: 100%;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .sprint-container {
        padding: 0 1rem 1rem;
      }

      .sprint-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
      }

      .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .sprints-grid {
        grid-template-columns: 1fr;
      }

      .list-header {
        flex-direction: column;
        gap: 1rem;
        align-items: stretch;
      }

      .sprint-dates {
        flex-direction: column;
        gap: 0.5rem;
      }

      .form-row {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class SprintBoardComponent implements OnInit {
  sprints: Sprint[] = [];
  currentSprint: Sprint | null = null;
  selectedStatus: string | null = null;
  burndownData: any = null;
  burndownOptions: any = {};

  // Dialog
  showSprintDialog = false;
  editingSprintId: string | null = null;
  savingSprint = false;

  sprintForm = {
    name: '',
    description: '',
    goal: '',
    start_date: new Date(),
    end_date: new Date(),
    capacity: 0
  };

  statusOptions = [
    { label: 'Planificación', value: 'planning' },
    { label: 'Activo', value: 'active' },
    { label: 'Completado', value: 'completed' },
    { label: 'Cancelado', value: 'cancelled' }
  ];

  headerActions = [
    {
      label: 'Nuevo Sprint',
      icon: 'pi pi-plus',
      onClick: () => this.createSprint()
    }
  ];

  constructor(private sprintService: SprintService) {
    this.setupBurndownChart();
  }

  ngOnInit(): void {
    this.loadSprints();
  }

  private loadSprints(): void {
    // Obtener proyecto actual del contexto/ruta
    const projectId = 'current-project-id'; // TODO: Obtener del contexto

    this.sprintService.getSprints(projectId, this.selectedStatus).subscribe(
      sprints => {
        this.sprints = sprints;
        this.currentSprint = sprints.find(s => s.status === 'active') || null;
        
        if (this.currentSprint) {
          this.loadBurndownData();
        }
      }
    );
  }

  private loadBurndownData(): void {
    if (!this.currentSprint) return;

    this.sprintService.getBurndownData(this.currentSprint.id).subscribe(
      data => {
        this.burndownData = {
          labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5'],
          datasets: [
            {
              label: 'Trabajo Restante',
              data: [100, 80, 60, 30, 10],
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.1)',
              tension: 0.4
            },
            {
              label: 'Línea Ideal',
              data: [100, 75, 50, 25, 0],
              borderColor: '#6c757d',
              borderDash: [5, 5],
              tension: 0.4
            }
          ]
        };
      }
    );
  }

  private setupBurndownChart(): void {
    this.burndownOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Story Points'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Días del Sprint'
          }
        }
      },
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      }
    };
  }

  createSprint(): void {
    this.editingSprintId = null;
    this.resetSprintForm();
    this.showSprintDialog = true;
  }

  editSprint(sprint: Sprint): void {
    this.editingSprintId = sprint.id;
    this.sprintForm = {
      name: sprint.name,
      description: sprint.description || '',
      goal: sprint.goal || '',
      start_date: new Date(sprint.start_date),
      end_date: new Date(sprint.end_date),
      capacity: sprint.capacity || 0
    };
    this.showSprintDialog = true;
  }

  saveSprint(): void {
    this.savingSprint = true;
    const projectId = 'current-project-id'; // TODO: Obtener del contexto

    const request = {
      name: this.sprintForm.name,
      description: this.sprintForm.description,
      goal: this.sprintForm.goal,
      start_date: this.sprintForm.start_date,
      end_date: this.sprintForm.end_date,
      capacity: this.sprintForm.capacity
    };

    const operation = this.editingSprintId
      ? this.sprintService.updateSprint(this.editingSprintId, request)
      : this.sprintService.createSprint(projectId, request);

    operation.subscribe(
      () => {
        this.showSprintDialog = false;
        this.savingSprint = false;
        this.loadSprints();
      },
      error => {
        console.error('Error saving sprint:', error);
        this.savingSprint = false;
      }
    );
  }

  startSprint(sprint: Sprint): void {
    this.sprintService.startSprint(sprint.id).subscribe(
      () => {
        this.loadSprints();
      }
    );
  }

  completeSprint(sprint: Sprint): void {
    this.sprintService.completeSprint(sprint.id).subscribe(
      () => {
        this.loadSprints();
      }
    );
  }

  onStatusFilter(): void {
    this.loadSprints();
  }

  cancelSprintDialog(): void {
    this.showSprintDialog = false;
    this.resetSprintForm();
  }

  private resetSprintForm(): void {
    this.sprintForm = {
      name: '',
      description: '',
      goal: '',
      start_date: new Date(),
      end_date: new Date(),
      capacity: 0
    };
  }

  getStatusLabel(status: string): string {
    const labels = {
      'planning': 'Planificación',
      'active': 'Activo',
      'completed': 'Completado',
      'cancelled': 'Cancelado'
    };
    return labels[status as keyof typeof labels] || status;
  }

  getStatusSeverity(status: string): string {
    const severities = {
      'planning': 'warning',
      'active': 'info',
      'completed': 'success',
      'cancelled': 'danger'
    };
    return severities[status as keyof typeof severities] || 'secondary';
  }

  getSprintProgress(sprint: Sprint): number {
    if (sprint.committed_points === 0) return 0;
    return Math.round((sprint.completed_points / sprint.committed_points) * 100);
  }

  getTasksCount(sprint: Sprint): number {
    return sprint.tasks ? sprint.tasks.length : 0;
  }

  getDaysRemaining(sprint: Sprint): number {
    const today = new Date();
    const endDate = new Date(sprint.end_date);
    const diffTime = endDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(0, diffDays);
  }

  trackBySprint(index: number, sprint: Sprint): string {
    return sprint.id;
  }
}
