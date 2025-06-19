import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '@environments/environment';

export interface Notification {
  id: string;
  title: string;
  content: string;
  type: string;
  user_id: string;
  is_read: boolean;
  read_at?: string;
  action_url?: string;
  entity_type?: string;
  entity_id?: string;
  metadata?: {[key: string]: any};
  created_at: string;
  updated_at: string;
}

export interface NotificationFilter {
  is_read?: boolean;
  type?: string[];
  entity_type?: string;
}

export interface NotificationResponse {
  data: Notification[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private unreadCountSubject = new BehaviorSubject<number>(0);
  public unreadCount$ = this.unreadCountSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadUnreadCount();
  }

  getNotifications(page = 1, pageSize = 20, filter?: NotificationFilter): Observable<NotificationResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (filter) {
      if (filter.is_read !== undefined) {
        params = params.set('is_read', filter.is_read.toString());
      }
      if (filter.entity_type) {
        params = params.set('entity_type', filter.entity_type);
      }
      if (filter.type && filter.type.length > 0) {
        filter.type.forEach(type => {
          params = params.append('type', type);
        });
      }
    }

    return this.http.get<NotificationResponse>(`${environment.apiUrl}/notifications`, { params });
  }

  markAsRead(notificationId: string): Observable<void> {
    return this.http.put<void>(`${environment.apiUrl}/notifications/${notificationId}/read`, {})
      .pipe(
        tap(() => this.decrementUnreadCount())
      );
  }

  markAllAsRead(): Observable<void> {
    return this.http.put<void>(`${environment.apiUrl}/notifications/read-all`, {})
      .pipe(
        tap(() => this.unreadCountSubject.next(0))
      );
  }

  deleteNotification(notificationId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/notifications/${notificationId}`)
      .pipe(
        tap(() => this.decrementUnreadCount())
      );
  }

  getUnreadCount(): Observable<{unread_count: number}> {
    return this.http.get<{unread_count: number}>(`${environment.apiUrl}/notifications/unread-count`)
      .pipe(
        tap(response => this.unreadCountSubject.next(response.unread_count))
      );
  }

  private loadUnreadCount(): void {
    this.getUnreadCount().subscribe();
  }

  private decrementUnreadCount(): void {
    const current = this.unreadCountSubject.value;
    if (current > 0) {
      this.unreadCountSubject.next(current - 1);
    }
  }

  // Métodos para crear notificaciones locales (para testing o casos especiales)
  createLocalNotification(notification: Partial<Notification>): void {
    // Simular notificación local
    const newNotification: Notification = {
      id: Date.now().toString(),
      title: notification.title || '',
      content: notification.content || '',
      type: notification.type || 'general',
      user_id: '',
      is_read: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ...notification
    };

    // Incrementar contador
    this.unreadCountSubject.next(this.unreadCountSubject.value + 1);
  }

  // Configuración de preferencias de notificación
  getNotificationPreferences(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/notifications/preferences`);
  }

  updateNotificationPreferences(preferences: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/notifications/preferences`, preferences);
  }

  // Utilidades para mostrar notificaciones nativas del navegador
  requestNotificationPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      console.warn('Este navegador no soporta notificaciones');
      return Promise.resolve('denied');
    }

    return Notification.requestPermission();
  }

  showBrowserNotification(title: string, options?: NotificationOptions): void {
    if (Notification.permission === 'granted') {
      new Notification(title, {
        icon: '/assets/icons/notification-icon.png',
        badge: '/assets/icons/badge-icon.png',
        ...options
      });
    }
  }

  // Procesamiento de notificaciones en tiempo real
  processRealTimeNotification(notification: Notification): void {
    // Incrementar contador de no leídas
    this.unreadCountSubject.next(this.unreadCountSubject.value + 1);

    // Mostrar notificación nativa si está permitido
    if (Notification.permission === 'granted') {
      this.showBrowserNotification(notification.title, {
        body: notification.content,
        tag: notification.id,
        data: notification
      });
    }
  }
}
