import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { ChartModule } from 'primeng/chart';
import { DropdownModule } from 'primeng/dropdown';
import { CalendarModule } from 'primeng/calendar';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ProgressBarModule } from 'primeng/progressbar';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { ReportService } from '@core/services/report.service';

@Component({
  selector: 'app-reports-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    ChartModule,
    DropdownModule,
    CalendarModule,
    TableModule,
    TagModule,
    ProgressBarModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Centro de Reportes"
      description="Analiza el rendimiento de proyectos, equipos y tiempo"
      titleIcon="pi pi-chart-bar"
      [actions]="headerActions">
    </app-page-header>

    <div class="reports-container">
      <!-- Filtros globales -->
      <div class="filters-section">
        <p-card>
          <div class="filters-content">
            <div class="filter-group">
              <label>Proyecto</label>
              <p-dropdown 
                [options]="projectOptions"
                [(ngModel)]="selectedProject"
                placeholder="Todos los proyectos"
                [showClear]="true"
                (onChange)="onFiltersChange()">
              </p-dropdown>
            </div>

            <div class="filter-group">
              <label>Período</label>
              <p-dropdown 
                [options]="periodOptions"
                [(ngModel)]="selectedPeriod"
                (onChange)="onPeriodChange()">
              </p-dropdown>
            </div>

            <div class="filter-group" *ngIf="selectedPeriod === 'custom'">
              <label>Fecha Inicio</label>
              <p-calendar 
                [(ngModel)]="customStartDate"
                dateFormat="dd/mm/yy"
                [showIcon]="true"
                (onSelect)="onFiltersChange()">
              </p-calendar>
            </div>

            <div class="filter-group" *ngIf="selectedPeriod === 'custom'">
              <label>Fecha Fin</label>
              <p-calendar 
                [(ngModel)]="customEndDate"
                dateFormat="dd/mm/yy"
                [showIcon]="true"
                (onSelect)="onFiltersChange()">
              </p-calendar>
            </div>

            <div class="filter-actions">
              <p-button 
                label="Aplicar Filtros"
                icon="pi pi-search"
                (onClick)="applyFilters()">
              </p-button>
              <p-button 
                label="Limpiar"
                severity="secondary"
                [text]="true"
                (onClick)="clearFilters()">
              </p-button>
            </div>
          </div>
        </p-card>
      </div>

      <!-- KPIs principales -->
      <div class="kpis-section">
        <div class="kpis-grid">
          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">📊</div>
              <div class="kpi-data">
                <h3>{{ kpis.totalProjects }}</h3>
                <p>Proyectos Activos</p>
                <span class="kpi-trend" [class.positive]="kpis.projectsTrend > 0">
                  <i [class]="kpis.projectsTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                  {{ Math.abs(kpis.projectsTrend) }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">✅</div>
              <div class="kpi-data">
                <h3>{{ kpis.completedTasks }}</h3>
                <p>Tareas Completadas</p>
                <span class="kpi-trend positive">
                  <i class="pi pi-arrow-up"></i>
                  {{ kpis.tasksTrend }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">⏱️</div>
              <div class="kpi-data">
                <h3>{{ kpis.totalHours }}h</h3>
                <p>Horas Trabajadas</p>
                <span class="kpi-trend positive">
                  <i class="pi pi-arrow-up"></i>
                  {{ kpis.hoursTrend }}%
                </span>
              </div>
            </div>
          </p-card>

          <p-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-icon">🚀</div>
              <div class="kpi-data">
                <h3>{{ kpis.teamVelocity }}</h3>
                <p>Velocidad del Equipo</p>
                <span class="kpi-trend" [class.positive]="kpis.velocityTrend > 0">
                  <i [class]="kpis.velocityTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                  {{ Math.abs(kpis.velocityTrend) }}%
                </span>
              </div>
            </div>
          </p-card>
        </div>
      </div>

      <!-- Gráficos principales -->
      <div class="charts-section">
        <div class="charts-grid">
          <!-- Gráfico de progreso de proyectos -->
          <p-card class="chart-card">
            <ng-template pTemplate="header">
              <h3>Progreso de Proyectos</h3>
            </ng-template>
            
            <p-chart 
              type="bar" 
              [data]="projectProgressChart" 
              [options]="barChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Gráfico de distribución de tiempo -->
          <p-card class="chart-card">
            <ng-template pTemplate="header">
              <h3>Distribución de Tiempo</h3>
            </ng-template>
            
            <p-chart 
              type="doughnut" 
              [data]="timeDistributionChart" 
              [options]="doughnutChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Gráfico de velocidad del equipo -->
          <p-card class="chart-card wide">
            <ng-template pTemplate="header">
              <h3>Velocidad del Equipo (Story Points)</h3>
            </ng-template>
            
            <p-chart 
              type="line" 
              [data]="velocityChart" 
              [options]="lineChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>

          <!-- Burndown chart -->
          <p-card class="chart-card wide">
            <ng-template pTemplate="header">
              <h3>Burndown Chart - Sprint Actual</h3>
            </ng-template>
            
            <p-chart 
              type="line" 
              [data]="burndownChart" 
              [options]="burndownChartOptions"
              width="100%"
              height="300px">
            </p-chart>
          </p-card>
        </div>
      </div>

      <!-- Tablas de datos -->
      <div class="tables-section">
        <div class="tables-grid">
          <!-- Top performers -->
          <p-card class="table-card">
            <ng-template pTemplate="header">
              <h3>Top Performers</h3>
            </ng-template>
            
            <p-table [value]="topPerformers" responsiveLayout="scroll">
              <ng-template pTemplate="header">
                <tr>
                  <th>Usuario</th>
                  <th>Tareas</th>
                  <th>Horas</th>
                  <th>Puntos</th>
                </tr>
              </ng-template>
              <ng-template pTemplate="body" let-performer>
                <tr>
                  <td>
                    <div class="user-info">
                      <img [src]="performer.avatar" [alt]="performer.name" class="user-avatar">
                      <span>{{ performer.name }}</span>
                    </div>
                  </td>
                  <td>{{ performer.completedTasks }}</td>
                  <td>{{ performer.hoursWorked }}h</td>
                  <td>{{ performer.storyPoints }}</td>
                </tr>
              </ng-template>
            </p-table>
          </p-card>

          <!-- Proyectos críticos -->
          <p-card class="table-card">
            <ng-template pTemplate="header">
              <h3>Proyectos Críticos</h3>
            </ng-template>
            
            <p-table [value]="criticalProjects" responsiveLayout="scroll">
              <ng-template pTemplate="header">
                <tr>
                  <th>Proyecto</th>
                  <th>Progreso</th>
                  <th>Estado</th>
                  <th>Riesgo</th>
                </tr>
              </ng-template>
              <ng-template pTemplate="body" let-project>
                <tr>
                  <td>{{ project.name }}</td>
                  <td>
                    <p-progressBar 
                      [value]="project.progress"
                      [showValue]="true">
                    </p-progressBar>
                  </td>
                  <td>
                    <p-tag 
                      [value]="project.status"
                      [severity]="getStatusSeverity(project.status)">
                    </p-tag>
                  </td>
                  <td>
                    <p-tag 
                      [value]="project.risk"
                      [severity]="getRiskSeverity(project.risk)">
                    </p-tag>
                  </td>
                </tr>
              </ng-template>
            </p-table>
          </p-card>
        </div>
      </div>

      <!-- Reportes rápidos -->
      <div class="quick-reports">
        <p-card>
          <ng-template pTemplate="header">
            <h3>Reportes Rápidos</h3>
          </ng-template>

          <div class="quick-reports-grid">
            <div class="report-item" (click)="generateQuickReport('project-summary')">
              <i class="pi pi-folder report-icon"></i>
              <h4>Resumen de Proyectos</h4>
              <p>Estado general de todos los proyectos</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('time-analysis')">
              <i class="pi pi-clock report-icon"></i>
              <h4>Análisis de Tiempo</h4>
              <p>Distribución y eficiencia temporal</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('team-performance')">
              <i class="pi pi-users report-icon"></i>
              <h4>Rendimiento del Equipo</h4>
              <p>Métricas de productividad individual</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('budget-tracking')">
              <i class="pi pi-dollar report-icon"></i>
              <h4>Seguimiento de Presupuesto</h4>
              <p>Análisis financiero y costos</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('quality-metrics')">
              <i class="pi pi-star report-icon"></i>
              <h4>Métricas de Calidad</h4>
              <p>Bugs, testing y calidad del código</p>
            </div>

            <div class="report-item" (click)="generateQuickReport('sprint-analysis')">
              <i class="pi pi-chart-line report-icon"></i>
              <h4>Análisis de Sprints</h4>
              <p>Velocidad y burndown histórico</p>
            </div>
          </div>
        </p-card>
      </div>
    </div>
  `,
  styles: [`
    .reports-container {
      padding: 0 2rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }

    /* Filtros */
    .filters-content {
      display: flex;
      gap: 1rem;
      align-items: end;
      flex-wrap: wrap;
    }

    .filter-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      min-width: 150px;
    }

    .filter-group label {
      font-weight: 600;
      color: #333;
      font-size: 0.9rem;
    }

    .filter-actions {
      display: flex;
      gap: 0.5rem;
      margin-left: auto;
    }

    /* KPIs */
    .kpis-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.5rem;
    }

    .kpi-card {
      border-left: 4px solid #007bff;
    }

    .kpi-content {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
    }

    .kpi-icon {
      font-size: 2.5rem;
      opacity: 0.8;
    }

    .kpi-data h3 {
      margin: 0 0 0.25rem 0;
      font-size: 1.8rem;
      color: #333;
    }

    .kpi-data p {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.9rem;
    }

    .kpi-trend {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.8rem;
      font-weight: 600;
      color: #dc3545;
    }

    .kpi-trend.positive {
      color: #28a745;
    }

    /* Gráficos */
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }

    .chart-card.wide {
      grid-column: span 2;
    }

    .chart-card h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    /* Tablas */
    .tables-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }

    .table-card h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .user-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
    }

    /* Reportes rápidos */
    .quick-reports h3 {
      margin: 0;
      padding: 1rem;
      background: #f8f9fa;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
    }

    .quick-reports-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      padding: 1rem;
    }

    .report-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 1.5rem;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .report-item:hover {
      background: #f8f9fa;
      border-color: #007bff;
      transform: translateY(-2px);
    }

    .report-icon {
      font-size: 2rem;
      color: #007bff;
      margin-bottom: 1rem;
    }

    .report-item h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }

    .report-item p {
      margin: 0;
      color: #666;
      font-size: 0.9rem;
    }

    /* Responsive */
    @media (max-width: 1200px) {
      .charts-grid {
        grid-template-columns: 1fr;
      }

      .chart-card.wide {
        grid-column: span 1;
      }
    }

    @media (max-width: 768px) {
      .reports-container {
        padding: 0 1rem 1rem;
      }

      .filters-content {
        flex-direction: column;
        align-items: stretch;
      }

      .filter-actions {
        margin-left: 0;
        justify-content: stretch;
      }

      .kpis-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .tables-grid {
        grid-template-columns: 1fr;
      }

      .quick-reports-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 480px) {
      .kpis-grid {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class ReportsDashboardComponent implements OnInit {
  // Filtros
  selectedProject: string | null = null;
  selectedPeriod = 'last_30_days';
  customStartDate = new Date();
  customEndDate = new Date();

  projectOptions = [
    { label: 'Proyecto Alpha', value: 'alpha' },
    { label: 'Proyecto Beta', value: 'beta' },
    { label: 'Proyecto Gamma', value: 'gamma' }
  ];

  periodOptions = [
    { label: 'Últimos 7 días', value: 'last_7_days' },
    { label: 'Últimos 30 días', value: 'last_30_days' },
    { label: 'Último trimestre', value: 'last_quarter' },
    { label: 'Año actual', value: 'current_year' },
    { label: 'Personalizado', value: 'custom' }
  ];

  // KPIs
  kpis = {
    totalProjects: 8,
    projectsTrend: 12,
    completedTasks: 156,
    tasksTrend: 18,
    totalHours: 342,
    hoursTrend: 8,
    teamVelocity: 85,
    velocityTrend: -5
  };

  // Data
  topPerformers: any[] = [];
  criticalProjects: any[] = [];

  // Charts
  projectProgressChart: any = {};
  timeDistributionChart: any = {};
  velocityChart: any = {};
  burndownChart: any = {};

  // Chart options
  barChartOptions: any = {};
  doughnutChartOptions: any = {};
  lineChartOptions: any = {};
  burndownChartOptions: any = {};

  headerActions = [
    {
      label: 'Exportar Dashboard',
      icon: 'pi pi-download',
      onClick: () => this.exportDashboard()
    },
    {
      label: 'Programar Reporte',
      icon: 'pi pi-calendar',
      onClick: () => this.scheduleReport()
    }
  ];

  Math = Math; // Para usar en template

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.setupChartOptions();
    this.loadDashboardData();
  }

  private setupChartOptions(): void {
    this.barChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    };

    this.doughnutChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    };

    this.lineChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };

    this.burndownChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Story Points'
          }
        }
      }
    };
  }

  private loadDashboardData(): void {
    this.loadTopPerformers();
    this.loadCriticalProjects();
    this.loadChartData();
  }

  private loadTopPerformers(): void {
    this.topPerformers = [
      {
        name: 'Ana García',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 23,
        hoursWorked: 45,
        storyPoints: 89
      },
      {
        name: 'Carlos López',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 19,
        hoursWorked: 38,
        storyPoints: 76
      },
      {
        name: 'María Rodríguez',
        avatar: 'https://via.placeholder.com/32',
        completedTasks: 17,
        hoursWorked: 42,
        storyPoints: 72
      }
    ];
  }

  private loadCriticalProjects(): void {
    this.criticalProjects = [
      {
        name: 'Proyecto Alpha',
        progress: 75,
        status: 'En Progreso',
        risk: 'Bajo'
      },
      {
        name: 'Proyecto Beta',
        progress: 45,
        status: 'Retrasado',
        risk: 'Alto'
      },
      {
        name: 'Proyecto Gamma',
        progress: 90,
        status: 'Casi Completo',
        risk: 'Medio'
      }
    ];
  }

  private loadChartData(): void {
    // Progreso de proyectos
    this.projectProgressChart = {
      labels: ['Alpha', 'Beta', 'Gamma', 'Delta'],
      datasets: [{
        label: 'Progreso (%)',
        data: [75, 45, 90, 60],
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545']
      }]
    };

    // Distribución de tiempo
    this.timeDistributionChart = {
      labels: ['Desarrollo', 'Testing', 'Documentación', 'Reuniones'],
      datasets: [{
        data: [40, 25, 20, 15],
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#fd7e14']
      }]
    };

    // Velocidad del equipo
    this.velocityChart = {
      labels: ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5'],
      datasets: [{
        label: 'Velocidad',
        data: [65, 72, 68, 85, 78],
        borderColor: '#007bff',
        backgroundColor: 'rgba(0, 123, 255, 0.1)',
        tension: 0.4
      }]
    };

    // Burndown chart
    this.burndownChart = {
      labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5'],
      datasets: [
        {
          label: 'Trabajo Restante',
          data: [100, 80, 65, 40, 20],
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

  onFiltersChange(): void {
    // Implementar lógica de filtros
  }

  onPeriodChange(): void {
    if (this.selectedPeriod !== 'custom') {
      this.calculateDateRange();
    }
    this.onFiltersChange();
  }

  private calculateDateRange(): void {
    const now = new Date();
    
    switch (this.selectedPeriod) {
      case 'last_7_days':
        this.customStartDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        this.customEndDate = now;
        break;
      case 'last_30_days':
        this.customStartDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        this.customEndDate = now;
        break;
      case 'last_quarter':
        const quarter = Math.floor(now.getMonth() / 3);
        this.customStartDate = new Date(now.getFullYear(), quarter * 3 - 3, 1);
        this.customEndDate = new Date(now.getFullYear(), quarter * 3, 0);
        break;
      case 'current_year':
        this.customStartDate = new Date(now.getFullYear(), 0, 1);
        this.customEndDate = now;
        break;
    }
  }

  applyFilters(): void {
    console.log('Aplicando filtros:', {
      project: this.selectedProject,
      period: this.selectedPeriod,
      startDate: this.customStartDate,
      endDate: this.customEndDate
    });
    
    this.loadDashboardData();
  }

  clearFilters(): void {
    this.selectedProject = null;
    this.selectedPeriod = 'last_30_days';
    this.customStartDate = new Date();
    this.customEndDate = new Date();
    this.loadDashboardData();
  }

  generateQuickReport(reportType: string): void {
    console.log('Generando reporte rápido:', reportType);
    // TODO: Implementar generación de reportes
  }

  exportDashboard(): void {
    console.log('Exportando dashboard');
    // TODO: Implementar exportación
  }

  scheduleReport(): void {
    console.log('Programando reporte');
    // TODO: Implementar programación de reportes
  }

  getStatusSeverity(status: string): string {
    const severities = {
      'En Progreso': 'info',
      'Retrasado': 'danger',
      'Casi Completo': 'success',
      'Completado': 'success'
    };
    return severities[status as keyof typeof severities] || 'secondary';
  }

  getRiskSeverity(risk: string): string {
    const severities = {
      'Bajo': 'success',
      'Medio': 'warning',
      'Alto': 'danger'
    };
    return severities[risk as keyof typeof severities] || 'secondary';
  }
}
