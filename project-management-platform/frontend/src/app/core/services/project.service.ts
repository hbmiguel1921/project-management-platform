import { Injectable } from '@angular/core';
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
