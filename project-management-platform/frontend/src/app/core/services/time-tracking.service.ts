import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface TimeEntry {
  id: string;
  description: string;
  start_time: string;
  end_time?: string;
  duration: number; // en minutos
  task_id?: string;
  project_id: string;
  user_id: string;
  is_billable: boolean;
  hourly_rate?: number;
  tags: string[];
  created_at: string;
  updated_at: string;
  
  // Relaciones
  task?: any;
  project?: any;
  user?: any;
}

export interface TimesheetEntry {
  id: string;
  date: string;
  user_id: string;
  project_id: string;
  task_id?: string;
  hours: number;
  description: string;
  is_billable: boolean;
  status: 'draft' | 'submitted' | 'approved' | 'rejected';
  
  // Relaciones
  user?: any;
  project?: any;
  task?: any;
}

export interface CreateTimeEntryRequest {
  description: string;
  start_time: Date;
  end_time?: Date;
  task_id?: string;
  is_billable: boolean;
  tags?: string[];
}

export interface CreateTimesheetEntryRequest {
  date: Date;
  project_id: string;
  task_id?: string;
  hours: number;
  description: string;
  is_billable: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TimeTrackingService {

  constructor(private http: HttpClient) { }

  // Time Entries
  startTimer(projectId: string, entryData: CreateTimeEntryRequest): Observable<TimeEntry> {
    return this.http.post<TimeEntry>(`${environment.apiUrl}/projects/${projectId}/time-entries`, entryData);
  }

  stopTimer(entryId: string, endTime?: Date): Observable<TimeEntry> {
    return this.http.put<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}/stop`, {
      end_time: endTime
    });
  }

  getTimeEntries(projectId?: string | null, startDate?: Date, endDate?: Date): Observable<TimeEntry[]> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<TimeEntry[]>(`${environment.apiUrl}/time-entries`, { params });
  }

  getTimeEntry(entryId: string): Observable<TimeEntry> {
    return this.http.get<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}`);
  }

  updateTimeEntry(entryId: string, entryData: Partial<CreateTimeEntryRequest>): Observable<TimeEntry> {
    return this.http.put<TimeEntry>(`${environment.apiUrl}/time-entries/${entryId}`, entryData);
  }

  deleteTimeEntry(entryId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/time-entries/${entryId}`);
  }

  getActiveEntry(): Observable<{active_entry: TimeEntry | null}> {
    return this.http.get<{active_entry: TimeEntry | null}>(`${environment.apiUrl}/time-entries/active`);
  }

  // Time Reports
  getTimeReports(projectId?: string | null, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<any>(`${environment.apiUrl}/time-reports`, { params });
  }

  getTeamTimeReports(projectId: string, startDate?: Date, endDate?: Date): Observable<any> {
    let params = new HttpParams();
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<any>(`${environment.apiUrl}/projects/${projectId}/time-reports`, { params });
  }

  // Timesheet Entries
  createTimesheetEntry(entryData: CreateTimesheetEntryRequest): Observable<TimesheetEntry> {
    return this.http.post<TimesheetEntry>(`${environment.apiUrl}/timesheet-entries`, entryData);
  }

  getTimesheetEntries(startDate?: Date, endDate?: Date): Observable<TimesheetEntry[]> {
    let params = new HttpParams();
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get<TimesheetEntry[]>(`${environment.apiUrl}/timesheet-entries`, { params });
  }

  submitTimesheet(startDate: Date, endDate: Date): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/timesheet/submit`, {
      start_date: startDate,
      end_date: endDate
    });
  }

  // Utilities
  calculateDuration(startTime: Date, endTime: Date): number {
    return Math.floor((endTime.getTime() - startTime.getTime()) / 60000); // en minutos
  }

  formatDuration(minutes: number): string {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours === 0) {
      return `${mins}m`;
    } else if (mins === 0) {
      return `${hours}h`;
    } else {
      return `${hours}h ${mins}m`;
    }
  }

  exportTimesheet(format: 'csv' | 'excel' | 'pdf', startDate?: Date, endDate?: Date): Observable<Blob> {
    let params = new HttpParams().set('format', format);
    
    if (startDate) {
      params = params.set('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params = params.set('end_date', endDate.toISOString().split('T')[0]);
    }
    
    return this.http.get(`${environment.apiUrl}/time-entries/export`, {
      params,
      responseType: 'blob'
    });
  }
}
