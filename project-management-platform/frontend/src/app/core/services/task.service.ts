import { Injectable } from '@angular/core';
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
