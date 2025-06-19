import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface Sprint {
  id: string;
  name: string;
  description?: string;
  project_id: string;
  start_date: string;
  end_date: string;
  status: 'planning' | 'active' | 'completed' | 'cancelled';
  goal?: string;
  capacity: number;
  committed_points: number;
  completed_points: number;
  velocity: number;
  created_at: string;
  updated_at: string;
  
  // Relaciones
  project?: any;
  tasks?: any[];
  events?: SprintEvent[];
}

export interface SprintEvent {
  id: string;
  sprint_id: string;
  type: 'planning' | 'daily' | 'review' | 'retrospective' | 'custom';
  title: string;
  content?: string;
  user_id: string;
  date: string;
  user?: any;
}

export interface CreateSprintRequest {
  name: string;
  description?: string;
  start_date: Date;
  end_date: Date;
  goal?: string;
  capacity?: number;
}

export interface UpdateSprintRequest {
  name?: string;
  description?: string;
  start_date?: Date;
  end_date?: Date;
  goal?: string;
  capacity?: number;
}

@Injectable({
  providedIn: 'root'
})
export class SprintService {

  constructor(private http: HttpClient) { }

  getSprints(projectId: string, status?: string | null): Observable<Sprint[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set('status', status);
    }
    
    return this.http.get<Sprint[]>(`${environment.apiUrl}/projects/${projectId}/sprints`, { params });
  }

  getSprint(sprintId: string): Observable<Sprint> {
    return this.http.get<Sprint>(`${environment.apiUrl}/sprints/${sprintId}`);
  }

  createSprint(projectId: string, sprintData: CreateSprintRequest): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/projects/${projectId}/sprints`, sprintData);
  }

  updateSprint(sprintId: string, sprintData: UpdateSprintRequest): Observable<Sprint> {
    return this.http.put<Sprint>(`${environment.apiUrl}/sprints/${sprintId}`, sprintData);
  }

  startSprint(sprintId: string): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/sprints/${sprintId}/start`, {});
  }

  completeSprint(sprintId: string): Observable<Sprint> {
    return this.http.post<Sprint>(`${environment.apiUrl}/sprints/${sprintId}/complete`, {});
  }

  addTaskToSprint(sprintId: string, taskId: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/sprints/${sprintId}/tasks`, {
      task_id: taskId
    });
  }

  removeTaskFromSprint(sprintId: string, taskId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/sprints/${sprintId}/tasks/${taskId}`);
  }

  getSprintEvents(sprintId: string): Observable<SprintEvent[]> {
    return this.http.get<SprintEvent[]>(`${environment.apiUrl}/sprints/${sprintId}/events`);
  }

  createSprintEvent(sprintId: string, eventData: {
    type: string;
    title: string;
    content?: string;
  }): Observable<SprintEvent> {
    return this.http.post<SprintEvent>(`${environment.apiUrl}/sprints/${sprintId}/events`, eventData);
  }

  getBurndownData(sprintId: string): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}/sprints/${sprintId}/burndown`);
  }

  getSprintMetrics(sprintId: string): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}/sprints/${sprintId}/metrics`);
  }

  getVelocityChart(projectId: string, sprintCount = 10): Observable<any> {
    const params = new HttpParams().set('sprint_count', sprintCount.toString());
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/velocity`, { params });
  }
}
