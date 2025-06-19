import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface WikiPage {
  id: string;
  title: string;
  slug: string;
  content: string;
  project_id: string;
  author_id: string;
  is_published: boolean;
  version: number;
  parent_id?: string;
  tags: string[];
  metadata: {[key: string]: any};
  created_at: string;
  updated_at: string;
  published_at?: string;
  last_edited_at: string;
  
  // Relaciones
  project?: any;
  author?: any;
  parent?: WikiPage;
  children?: WikiPage[];
  revisions?: WikiRevision[];
}

export interface WikiRevision {
  id: string;
  page_id: string;
  title: string;
  content: string;
  author_id: string;
  version: number;
  summary: string;
  created_at: string;
  author?: any;
}

export interface WikiComment {
  id: string;
  content: string;
  page_id: string;
  user_id: string;
  parent_id?: string;
  created_at: string;
  updated_at: string;
  user?: any;
  replies?: WikiComment[];
}

export interface CreatePageRequest {
  title: string;
  content?: string;
  parent_id?: string;
  is_published: boolean;
  tags?: string[];
  metadata?: {[key: string]: any};
}

export interface UpdatePageRequest {
  title?: string;
  content?: string;
  is_published?: boolean;
  tags?: string[];
  summary?: string;
  metadata?: {[key: string]: any};
}

export interface WikiStats {
  total_pages: number;
  published_pages: number;
  draft_pages: number;
  total_contributors: number;
  total_views: number;
}

@Injectable({
  providedIn: 'root'
})
export class WikiService {

  constructor(private http: HttpClient) { }

  getPages(projectId?: string, filter?: any): Observable<{data: WikiPage[], total: number}> {
    let params = new HttpParams();
    
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    if (filter) {
      Object.keys(filter).forEach(key => {
        if (filter[key] !== null && filter[key] !== undefined) {
          if (Array.isArray(filter[key])) {
            filter[key].forEach((value: any) => {
              params = params.append(key, value);
            });
          } else {
            params = params.set(key, filter[key]);
          }
        }
      });
    }
    
    return this.http.get<{data: WikiPage[], total: number}>(`${environment.apiUrl}/wiki/pages`, { params });
  }

  getPage(pageId: string): Observable<WikiPage> {
    return this.http.get<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}`);
  }

  getPageBySlug(projectId: string, slug: string): Observable<WikiPage> {
    return this.http.get<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages/${slug}`);
  }

  createPage(projectId: string, pageData: CreatePageRequest): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages`, pageData);
  }

  updatePage(pageId: string, pageData: UpdatePageRequest): Observable<WikiPage> {
    return this.http.put<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}`, pageData);
  }

  deletePage(pageId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/wiki/pages/${pageId}`);
  }

  publishPage(pageId: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/publish`, {});
  }

  unpublishPage(pageId: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/unpublish`, {});
  }

  getPageRevisions(pageId: string): Observable<WikiRevision[]> {
    return this.http.get<WikiRevision[]>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions`);
  }

  getPageRevision(pageId: string, version: number): Observable<WikiRevision> {
    return this.http.get<WikiRevision>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions/${version}`);
  }

  restorePageRevision(pageId: string, version: number): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/revisions/${version}/restore`, {});
  }

  getPageComments(pageId: string): Observable<WikiComment[]> {
    return this.http.get<WikiComment[]>(`${environment.apiUrl}/wiki/pages/${pageId}/comments`);
  }

  addPageComment(pageId: string, content: string, parentId?: string): Observable<WikiComment> {
    return this.http.post<WikiComment>(`${environment.apiUrl}/wiki/pages/${pageId}/comments`, {
      content,
      parent_id: parentId
    });
  }

  updatePageComment(commentId: string, content: string): Observable<WikiComment> {
    return this.http.put<WikiComment>(`${environment.apiUrl}/wiki/comments/${commentId}`, {
      content
    });
  }

  deletePageComment(commentId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/wiki/comments/${commentId}`);
  }

  searchPages(query: string, projectId?: string): Observable<WikiPage[]> {
    let params = new HttpParams().set('q', query);
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/search`, { params });
  }

  getRecentPages(limit = 10): Observable<WikiPage[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/pages/recent`, { params });
  }

  getPopularPages(limit = 10): Observable<WikiPage[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/pages/popular`, { params });
  }

  getStats(projectId?: string): Observable<WikiStats> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<WikiStats>(`${environment.apiUrl}/wiki/stats`, { params });
  }

  uploadFile(file: File): Observable<{file_url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{file_url: string}>(`${environment.apiUrl}/wiki/upload`, formData);
  }

  getPageHierarchy(projectId: string): Observable<WikiPage[]> {
    return this.http.get<WikiPage[]>(`${environment.apiUrl}/wiki/projects/${projectId}/hierarchy`);
  }

  movePage(pageId: string, newParentId?: string): Observable<WikiPage> {
    return this.http.put<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/move`, {
      parent_id: newParentId
    });
  }

  duplicatePage(pageId: string, newTitle?: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/pages/${pageId}/duplicate`, {
      title: newTitle
    });
  }

  // Plantillas de páginas
  getPageTemplates(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/wiki/templates`);
  }

  createPageFromTemplate(projectId: string, templateId: string, title: string): Observable<WikiPage> {
    return this.http.post<WikiPage>(`${environment.apiUrl}/wiki/projects/${projectId}/pages/from-template`, {
      template_id: templateId,
      title
    });
  }

  // Exportar páginas
  exportPage(pageId: string, format: 'pdf' | 'html' | 'markdown'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/wiki/pages/${pageId}/export/${format}`, {
      responseType: 'blob'
    });
  }

  exportProject(projectId: string, format: 'pdf' | 'html' | 'markdown'): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/wiki/projects/${projectId}/export/${format}`, {
      responseType: 'blob'
    });
  }
}
