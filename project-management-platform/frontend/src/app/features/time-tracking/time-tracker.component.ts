import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { TagModule } from 'primeng/tag';
import { CalendarModule } from 'primeng/calendar';
import { ChartModule } from 'primeng/chart';
import { TableModule } from 'primeng/table';
import { DialogModule } from 'primeng/dialog';
import { Subscription, interval } from 'rxjs';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { TimeTrackingService, TimeEntry } from '@core/services/time-tracking.service';

@Component({
  selector: 'app-time-tracker',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    TagModule,
    CalendarModule,
    ChartModule,
    TableModule,
    DialogModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Seguimiento de Tiempo"
      description="Registra y gestiona el tiempo dedicado a proyectos y tareas"
      titleIcon="pi pi-clock"
      [actions]="headerActions">
    </app-page-header>

    <div class="time-tracking-container">
      <!-- Timer activo -->
      <div class="active-timer" *ngIf="activeEntry">
        <p-card>
          <ng-template pTemplate="header">
            <div class="timer-header">
              <h3>⏱️ Tiempo en curso</h3>
              <p-tag 
                value="ACTIVO"
                severity="success"
                [rounded]="true">
              </p-tag>
            </div>
          </ng-template>

          <div class="timer-content">
            <div class="timer-display">
              <h2 class="elapsed-time">{{ formatDuration(elapsedSeconds) }}</h2>
              <p class="timer-description">{{ activeEntry.description }}</p>
              <div class="timer-meta">
                <span *ngIf="activeEntry.task">
                  <i class="pi pi-bookmark"></i>
                  {{ activeEntry.task?.title }}
                </span>
                <span>
                  <i class="pi pi-folder"></i>
                  {{ activeEntry.project?.name }}
                </span>
                <span>
                  <i class="pi pi-calendar"></i>
                  {{ activeEntry.start_time | date:'HH:mm' }}
                </span>
              </div>
            </div>

            <div class="timer-actions">
              <p-button 
                label="Detener"
                icon="pi pi-stop"
                severity="danger"
                (onClick)="stopTimer()">
              </p-button>
              <p-button 
                label="Editar"
                icon="pi pi-pencil"
                severity="secondary"
                [text]="true"
                (onClick)="editActiveEntry()">
              </p-button>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Iniciar nuevo timer -->
      <div class="start-timer" *ngIf="!activeEntry">
        <p-card>
          <ng-template pTemplate="header">
            <h3>🚀 Iniciar seguimiento</h3>
          </ng-template>

          <form class="timer-form">
            <div class="form-group">
              <label>¿En qué estás trabajando? *</label>
              <input 
                type="text"
                pInputText
                [(ngModel)]="newEntryForm.description"
                name="description"
                placeholder="Describe la actividad..."
                class="form-control">
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Proyecto *</label>
                <p-dropdown 
                  [options]="projectOptions"
                  [(ngModel)]="newEntryForm.project_id"
                  name="project_id"
                  placeholder="Seleccionar proyecto"
                  optionLabel="name"
                  optionValue="id"
                  class="form-control">
                </p-dropdown>
              </div>

              <div class="form-group">
                <label>Tarea (Opcional)</label>
                <p-dropdown 
                  [options]="taskOptions"
                  [(ngModel)]="newEntryForm.task_id"
                  name="task_id"
                  placeholder="Seleccionar tarea"
                  optionLabel="title"
                  optionValue="id"
                  [showClear]="true"
                  class="form-control">
                </p-dropdown>
              </div>
            </div>

            <div class="form-actions">
              <p-button 
                label="Iniciar Timer"
                icon="pi pi-play"
                (onClick)="startTimer()"
                [disabled]="!canStartTimer()">
              </p-button>
              <p-button 
                label="Entrada Manual"
                icon="pi pi-plus"
                severity="secondary"
                [outlined]="true"
                (onClick)="showManualEntryDialog()">
              </p-button>
            </div>
          </form>
        </p-card>
      </div>

      <!-- Resumen del día -->
      <div class="daily-summary">
        <p-card>
          <ng-template pTemplate="header">
            <div class="summary-header">
              <h3>📊 Resumen de hoy</h3>
              <p-calendar 
                [(ngModel)]="selectedDate"
                (onSelect)="onDateChange()"
                dateFormat="dd/mm/yy"
                [showIcon]="true">
              </p-calendar>
            </div>
          </ng-template>

          <div class="summary-content">
            <div class="summary-stats">
              <div class="stat-item">
                <h4>{{ todayStats.total_hours }}h</h4>
                <p>Total</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.billable_hours }}h</h4>
                <p>Facturable</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.entries_count }}</h4>
                <p>Entradas</p>
              </div>
              <div class="stat-item">
                <h4>{{ todayStats.projects_count }}</h4>
                <p>Proyectos</p>
              </div>
            </div>

            <!-- Gráfico de distribución -->
            <div class="time-distribution" *ngIf="chartData">
              <h4>Distribución por proyecto</h4>
              <p-chart 
                type="doughnut" 
                [data]="chartData" 
                [options]="chartOptions"
                width="100%"
                height="300px">
              </p-chart>
            </div>
          </div>
        </p-card>
      </div>

      <!-- Lista de entradas -->
      <div class="time-entries">
        <p-card>
          <ng-template pTemplate="header">
            <div class="entries-header">
              <h3>📝 Entradas de tiempo</h3>
              <div class="header-filters">
                <p-dropdown 
                  [options]="projectFilterOptions"
                  [(ngModel)]="selectedProjectFilter"
                  placeholder="Filtrar por proyecto"
                  [showClear]="true"
                  (onChange)="onProjectFilter()">
                </p-dropdown>
              </div>
            </div>
          </ng-template>

          <p-table 
            [value]="timeEntries"
            [loading]="loadingEntries"
            [paginator]="true"
            [rows]="10"
            responsiveLayout="scroll">
            
            <ng-template pTemplate="header">
              <tr>
                <th>Descripción</th>
                <th>Proyecto</th>
                <th>Tarea</th>
                <th>Inicio</th>
                <th>Duración</th>
                <th>Facturable</th>
                <th>Acciones</th>
              </tr>
            </ng-template>

            <ng-template pTemplate="body" let-entry>
              <tr>
                <td>{{ entry.description }}</td>
                <td>
                  <span class="project-badge">{{ entry.project?.name }}</span>
                </td>
                <td>
                  <span *ngIf="entry.task" class="task-badge">{{ entry.task?.title }}</span>
                  <span *ngIf="!entry.task" class="no-task">Sin tarea</span>
                </td>
                <td>{{ entry.start_time | date:'dd/MM HH:mm' }}</td>
                <td>
                  <span class="duration">{{ formatDuration(entry.duration * 60) }}</span>
                </td>
                <td>
                  <p-tag 
                    [value]="entry.is_billable ? 'Sí' : 'No'"
                    [severity]="entry.is_billable ? 'success' : 'secondary'">
                  </p-tag>
                </td>
                <td>
                  <div class="entry-actions">
                    <p-button 
                      icon="pi pi-pencil"
                      severity="secondary"
                      [text]="true"
                      size="small"
                      (onClick)="editEntry(entry)"
                      pTooltip="Editar">
                    </p-button>
                    <p-button 
                      icon="pi pi-trash"
                      severity="danger"
                      [text]="true"
                      size="small"
                      (onClick)="deleteEntry(entry)"
                      pTooltip="Eliminar">
                    </p-button>
                  </div>
                </td>
              </tr>
            </ng-template>

            <ng-template pTemplate="emptymessage">
              <tr>
                <td colspan="7" class="text-center">
                  No hay entradas de tiempo para mostrar
                </td>
              </tr>
            </ng-template>
          </p-table>
        </p-card>
      </div>
    </div>

    <!-- Dialog para entrada manual -->
    <p-dialog 
      header="Entrada Manual de Tiempo"
      [(visible)]="showManualDialog"
      [modal]="true"
      [style]="{width: '500px'}"
      [closable]="true">
      
      <form class="manual-form">
        <div class="form-group">
          <label>Descripción *</label>
          <input 
            type="text"
            pInputText
            [(ngModel)]="manualForm.description"
            name="description"
            placeholder="¿En qué trabajaste?"
            class="form-control">
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Proyecto *</label>
            <p-dropdown 
              [options]="projectOptions"
              [(ngModel)]="manualForm.project_id"
              name="project_id"
              placeholder="Seleccionar"
              optionLabel="name"
              optionValue="id"
              class="form-control">
            </p-dropdown>
          </div>

          <div class="form-group">
            <label>Tarea</label>
            <p-dropdown 
              [options]="taskOptions"
              [(ngModel)]="manualForm.task_id"
              name="task_id"
              placeholder="Opcional"
              optionLabel="title"
              optionValue="id"
              [showClear]="true"
              class="form-control">
            </p-dropdown>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha *</label>
            <p-calendar 
              [(ngModel)]="manualForm.date"
              name="date"
              dateFormat="dd/mm/yy"
              [showIcon]="true"
              class="form-control">
            </p-calendar>
          </div>

          <div class="form-group">
            <label>Horas *</label>
            <input 
              type="number"
              pInputText
              [(ngModel)]="manualForm.hours"
              name="hours"
              min="0.1"
              max="24"
              step="0.25"
              placeholder="0.5"
              class="form-control">
          </div>
        </div>

        <div class="form-group">
          <div class="checkbox-wrapper">
            <input 
              type="checkbox"
              id="billable"
              [(ngModel)]="manualForm.is_billable"
              name="is_billable">
            <label for="billable">Tiempo facturable</label>
          </div>
        </div>
      </form>

      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [text]="true"
          (onClick)="cancelManualDialog()">
        </p-button>
        <p-button 
          label="Guardar"
          (onClick)="saveManualEntry()"
          [loading]="savingEntry">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .time-tracking-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Timer activo */
    .timer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
      color: white;
      margin: -1rem -1rem 0 -1rem;
    }

    .timer-header h3 {
      margin: 0;
      color: white;
    }

    .timer-content {
      padding: 1.5rem;
      text-align: center;
    }

    .elapsed-time {
      font-size: 3rem;
      font-weight: 300;
      color: #28a745;
      margin: 0 0 0.5rem 0;
      font-family: 'Courier New', monospace;
    }

    .timer-description {
      font-size: 1.2rem;
      color: #333;
      margin: 0 0 1rem 0;
    }

    .timer-meta {
      display: flex;
      justify-content: center;
      gap: 2rem;
      margin-bottom: 2rem;
      font-size: 0.9rem;
      color: #666;
    }

    .timer-meta span {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .timer-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }

    /* Formulario de inicio */
    .timer-form {
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

    .form-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
      margin-top: 1rem;
    }

    /* Resumen del día */
    .summary-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .summary-header h3 {
      margin: 0;
      color: #333;
    }

    .summary-content {
      padding: 1.5rem;
    }

    .summary-stats {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .stat-item {
      text-align: center;
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .stat-item h4 {
      margin: 0 0 0.5rem 0;
      font-size: 1.5rem;
      color: #007bff;
    }

    .stat-item p {
      margin: 0;
      font-size: 0.9rem;
      color: #666;
    }

    .time-distribution h4 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    /* Lista de entradas */
    .entries-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .entries-header h3 {
      margin: 0;
      color: #333;
    }

    .header-filters {
      display: flex;
      gap: 1rem;
    }

    .project-badge {
      display: inline-block;
      padding: 0.25rem 0.5rem;
      background: #007bff;
      color: white;
      border-radius: 4px;
      font-size: 0.8rem;
    }

    .task-badge {
      display: inline-block;
      padding: 0.25rem 0.5rem;
      background: #28a745;
      color: white;
      border-radius: 4px;
      font-size: 0.8rem;
    }

    .no-task {
      color: #999;
      font-style: italic;
      font-size: 0.9rem;
    }

    .duration {
      font-family: 'Courier New', monospace;
      font-weight: 600;
      color: #333;
    }

    .entry-actions {
      display: flex;
      gap: 0.25rem;
    }

    /* Dialog manual */
    .manual-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .checkbox-wrapper {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .checkbox-wrapper input[type="checkbox"] {
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .time-tracking-container {
        padding: 0 1rem 1rem;
      }

      .timer-meta {
        flex-direction: column;
        gap: 0.5rem;
      }

      .form-row {
        grid-template-columns: 1fr;
      }

      .summary-stats {
        grid-template-columns: repeat(2, 1fr);
      }

      .form-actions {
        flex-direction: column;
      }

      .timer-actions {
        flex-direction: column;
      }
    }

    /* Animaciones */
    .elapsed-time {
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.7; }
      100% { opacity: 1; }
    }
  `]
})
export class TimeTrackerComponent implements OnInit, OnDestroy {
  activeEntry: TimeEntry | null = null;
  timeEntries: TimeEntry[] = [];
  projectOptions: any[] = [];
  taskOptions: any[] = [];
  projectFilterOptions: any[] = [];
  
  selectedDate = new Date();
  selectedProjectFilter: string | null = null;
  loadingEntries = false;
  
  // Timer
  elapsedSeconds = 0;
  timerSubscription?: Subscription;
  
  // Forms
  newEntryForm = {
    description: '',
    project_id: '',
    task_id: null,
    is_billable: true
  };
  
  manualForm = {
    description: '',
    project_id: '',
    task_id: null,
    date: new Date(),
    hours: 0,
    is_billable: true
  };
  
  // Stats
  todayStats = {
    total_hours: 0,
    billable_hours: 0,
    entries_count: 0,
    projects_count: 0
  };
  
  // Chart
  chartData: any = null;
  chartOptions: any = {};
  
  // Dialog
  showManualDialog = false;
  savingEntry = false;
  
  headerActions = [
    {
      label: 'Reportes',
      icon: 'pi pi-chart-bar',
      onClick: () => this.goToReports()
    },
    {
      label: 'Exportar',
      icon: 'pi pi-download',
      onClick: () => this.exportTimesheet()
    }
  ];

  constructor(private timeTrackingService: TimeTrackingService) {
    this.setupChart();
  }

  ngOnInit(): void {
    this.loadActiveEntry();
    this.loadTimeEntries();
    this.loadProjects();
    this.loadTodayStats();
  }

  ngOnDestroy(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }

  private loadActiveEntry(): void {
    this.timeTrackingService.getActiveEntry().subscribe(
      response => {
        this.activeEntry = response.active_entry;
        if (this.activeEntry) {
          this.startElapsedTimer();
        }
      }
    );
  }

  private loadTimeEntries(): void {
    this.loadingEntries = true;
    
    const startDate = new Date(this.selectedDate);
    startDate.setHours(0, 0, 0, 0);
    
    const endDate = new Date(this.selectedDate);
    endDate.setHours(23, 59, 59, 999);
    
    this.timeTrackingService.getTimeEntries(
      this.selectedProjectFilter,
      startDate,
      endDate
    ).subscribe(
      entries => {
        this.timeEntries = entries;
        this.loadingEntries = false;
      },
      error => {
        console.error('Error loading entries:', error);
        this.loadingEntries = false;
      }
    );
  }

  private loadProjects(): void {
    // TODO: Cargar desde ProjectService
    this.projectOptions = [
      { id: '1', name: 'Proyecto Alpha' },
      { id: '2', name: 'Proyecto Beta' }
    ];
    
    this.projectFilterOptions = [
      { label: 'Todos los proyectos', value: null },
      ...this.projectOptions.map(p => ({ label: p.name, value: p.id }))
    ];
  }

  private loadTodayStats(): void {
    const startDate = new Date(this.selectedDate);
    startDate.setHours(0, 0, 0, 0);
    
    const endDate = new Date(this.selectedDate);
    endDate.setHours(23, 59, 59, 999);
    
    this.timeTrackingService.getTimeReports(null, startDate, endDate).subscribe(
      stats => {
        this.todayStats = {
          total_hours: Math.round(stats.total_hours * 100) / 100,
          billable_hours: Math.round(stats.billable_hours * 100) / 100,
          entries_count: this.timeEntries.length,
          projects_count: stats.project_breakdown?.length || 0
        };
        
        this.updateChart(stats.project_breakdown || []);
      }
    );
  }

  private setupChart(): void {
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    };
  }

  private updateChart(projectData: any[]): void {
    if (projectData.length === 0) {
      this.chartData = null;
      return;
    }
    
    this.chartData = {
      labels: projectData.map(p => p.project_name),
      datasets: [{
        data: projectData.map(p => Math.round(p.total_minutes / 60 * 100) / 100),
        backgroundColor: [
          '#007bff',
          '#28a745',
          '#ffc107',
          '#dc3545',
          '#6f42c1',
          '#fd7e14'
        ]
      }]
    };
  }

  private startElapsedTimer(): void {
    if (!this.activeEntry) return;
    
    const startTime = new Date(this.activeEntry.start_time);
    
    this.timerSubscription = interval(1000).subscribe(() => {
      const now = new Date();
      this.elapsedSeconds = Math.floor((now.getTime() - startTime.getTime()) / 1000);
    });
  }

  startTimer(): void {
    if (!this.canStartTimer()) return;
    
    const request = {
      description: this.newEntryForm.description,
      start_time: new Date(),
      task_id: this.newEntryForm.task_id,
      is_billable: this.newEntryForm.is_billable
    };
    
    this.timeTrackingService.startTimer(this.newEntryForm.project_id, request).subscribe(
      entry => {
        this.activeEntry = entry;
        this.startElapsedTimer();
        this.resetNewEntryForm();
      }
    );
  }

  stopTimer(): void {
    if (!this.activeEntry) return;
    
    this.timeTrackingService.stopTimer(this.activeEntry.id).subscribe(
      () => {
        this.activeEntry = null;
        this.elapsedSeconds = 0;
        
        if (this.timerSubscription) {
          this.timerSubscription.unsubscribe();
        }
        
        this.loadTimeEntries();
        this.loadTodayStats();
      }
    );
  }

  editActiveEntry(): void {
    if (!this.activeEntry) return;
    // TODO: Implementar edición de entrada activa
  }

  editEntry(entry: TimeEntry): void {
    // TODO: Implementar edición de entrada
  }

  deleteEntry(entry: TimeEntry): void {
    this.timeTrackingService.deleteTimeEntry(entry.id).subscribe(
      () => {
        this.loadTimeEntries();
        this.loadTodayStats();
      }
    );
  }

  showManualEntryDialog(): void {
    this.showManualDialog = true;
  }

  saveManualEntry(): void {
    this.savingEntry = true;
    
    const request = {
      description: this.manualForm.description,
      project_id: this.manualForm.project_id,
      task_id: this.manualForm.task_id,
      date: this.manualForm.date,
      hours: this.manualForm.hours,
      is_billable: this.manualForm.is_billable
    };
    
    this.timeTrackingService.createTimesheetEntry(request).subscribe(
      () => {
        this.showManualDialog = false;
        this.savingEntry = false;
        this.resetManualForm();
        this.loadTimeEntries();
        this.loadTodayStats();
      },
      error => {
        console.error('Error saving manual entry:', error);
        this.savingEntry = false;
      }
    );
  }

  cancelManualDialog(): void {
    this.showManualDialog = false;
    this.resetManualForm();
  }

  onDateChange(): void {
    this.loadTimeEntries();
    this.loadTodayStats();
  }

  onProjectFilter(): void {
    this.loadTimeEntries();
  }

  canStartTimer(): boolean {
    return !!this.newEntryForm.description.trim() && !!this.newEntryForm.project_id;
  }

  formatDuration(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  private resetNewEntryForm(): void {
    this.newEntryForm = {
      description: '',
      project_id: '',
      task_id: null,
      is_billable: true
    };
  }

  private resetManualForm(): void {
    this.manualForm = {
      description: '',
      project_id: '',
      task_id: null,
      date: new Date(),
      hours: 0,
      is_billable: true
    };
  }

  goToReports(): void {
    // TODO: Navegar a reportes
  }

  exportTimesheet(): void {
    // TODO: Implementar exportación
  }
}
