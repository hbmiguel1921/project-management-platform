import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Report {
  id: string;
  name: string;
  description?: string;
  type: 'task_summary' | 'project_progress' | 'time_tracking' | 'team_performance' | 'sprint_burndown' | 'velocity_chart' | 'budget_analysis' | 'custom';
  project_id?: string;
  user_id: string;
  is_public: boolean;
  schedule?: string;
  config: {[key: string]: any};
  filters: {[key: string]: any};
  last_generated?: string;
  created_at: string;
  updated_at: string;
}

export interface ReportData {
  id: string;
  name: string;
  type: string;
  generated_at: string;
  data: {[key: string]: any};
  charts: ChartData[];
  tables: TableData[];
  summary: ReportSummary;
}

export interface ChartData {
  title: string;
  type: string;
  data: {[key: string]: any};
  config: {[key: string]: any};
}

export interface TableData {
  title: string;
  headers: string[];
  rows: any[][];
  summary: {[key: string]: any};
}

export interface ReportSummary {
  total_items: number;
  completed_items: number;
  metrics: {[key: string]: any};
  insights: string[];
}

export interface CreateReportRequest {
  name: string;
  description?: string;
  type: string;
  project_id?: string;
  is_public: boolean;
  config: {[key: string]: any};
  filters: {[key: string]: any};
  schedule?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  constructor(private http: HttpClient) { }

  getReports(projectId?: string): Observable<Report[]> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<Report[]>(`${environment.apiUrl}/reports`, { params });
  }

  getReport(reportId: string): Observable<Report> {
    return this.http.get<Report>(`${environment.apiUrl}/reports/${reportId}`);
  }

  createReport(reportData: CreateReportRequest): Observable<Report> {
    return this.http.post<Report>(`${environment.apiUrl}/reports`, reportData);
  }

  updateReport(reportId: string, reportData: Partial<CreateReportRequest>): Observable<Report> {
    return this.http.put<Report>(`${environment.apiUrl}/reports/${reportId}`, reportData);
  }

  deleteReport(reportId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/reports/${reportId}`);
  }

  generateReport(reportId: string): Observable<ReportData> {
    return this.http.post<ReportData>(`${environment.apiUrl}/reports/${reportId}/generate`, {});
  }

  getReportData(reportId: string): Observable<ReportData> {
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/${reportId}/data`);
  }

  // Reportes específicos
  getProjectSummaryReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/project-summary`, { params });
  }

  getTimeTrackingReport(projectId?: string, userId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (userId) params = params.set('user_id', userId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/time-tracking`, { params });
  }

  getTeamPerformanceReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/team-performance`, { params });
  }

  getSprintBurndownReport(sprintId: string): Observable<ReportData> {
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/sprint-burndown/${sprintId}`);
  }

  getVelocityChartReport(projectId: string, sprintCount = 10): Observable<ReportData> {
    const params = new HttpParams().set('sprint_count', sprintCount.toString());
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/velocity-chart/${projectId}`, { params });
  }

  getBudgetAnalysisReport(projectId?: string, startDate?: Date, endDate?: Date): Observable<ReportData> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<ReportData>(`${environment.apiUrl}/reports/budget-analysis`, { params });
  }

  // Dashboard y métricas
  getDashboardMetrics(projectId?: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/dashboard/metrics`, { params });
  }

  getProjectMetrics(projectId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/metrics`, { params });
  }

  getUserMetrics(userId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    if (startDate) params = params.set('start_date', startDate.toISOString().split('T')[0]);
    if (endDate) params = params.set('end_date', endDate.toISOString().split('T')[0]);
    
    return this.http.get<any>(`${environment.apiUrl}/users/${userId}/metrics`, { params });
  }

  // Exportación
  exportReport(reportId: string, format: 'pdf' | 'excel' | 'csv'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/reports/${reportId}/export/${format}`, {
      responseType: 'blob'
    });
  }

  exportDashboard(format: 'pdf' | 'excel', filters?: any): Observable<Blob> {
    let params = new HttpParams();
    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined) {
          params = params.set(key, filters[key]);
        }
      });
    }
    
    return this.http.get(`${environment.apiUrl}/dashboard/export/${format}`, {
      params,
      responseType: 'blob'
    });
  }

  // Programación de reportes
  scheduleReport(reportId: string, schedule: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/reports/${reportId}/schedule`, {
      schedule
    });
  }

  getScheduledReports(): Observable<Report[]> {
    return this.http.get<Report[]>(`${environment.apiUrl}/reports/scheduled`);
  }

  // Widgets de dashboard
  getDashboardWidgets(projectId?: string): Observable<any[]> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    
    return this.http.get<any[]>(`${environment.apiUrl}/dashboard/widgets`, { params });
  }

  createDashboardWidget(widgetData: any): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}/dashboard/widgets`, widgetData);
  }

  updateDashboardWidget(widgetId: string, widgetData: any): Observable<any> {
    return this.http.put<any>(`${environment.apiUrl}/dashboard/widgets/${widgetId}`, widgetData);
  }

  deleteDashboardWidget(widgetId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/dashboard/widgets/${widgetId}`);
  }

  // Utilidades
  generateQuickReport(type: string, filters?: any): Observable<ReportData> {
    return this.http.post<ReportData>(`${environment.apiUrl}/reports/quick/${type}`, filters || {});
  }

  getReportTemplates(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/reports/templates`);
  }

  createReportFromTemplate(templateId: string, config: any): Observable<Report> {
    return this.http.post<Report>(`${environment.apiUrl}/reports/from-template/${templateId}`, config);
  }
}
