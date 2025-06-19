import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { BadgeModule } from 'primeng/badge';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { DividerModule } from 'primeng/divider';
import { AvatarModule } from 'primeng/avatar';
import { Subscription } from 'rxjs';
import { NotificationService, Notification } from '@core/services/notification.service';
import { WebSocketService } from '@core/services/websocket.service';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ButtonModule,
    BadgeModule,
    OverlayPanelModule,
    DividerModule,
    AvatarModule
  ],
  template: `
    <div class="notifications-container">
      <p-button 
        icon="pi pi-bell"
        severity="secondary"
        [text]="true"
        [badge]="unreadCount > 0 ? unreadCount.toString() : null"
        badgeClass="p-badge-danger"
        (onClick)="togglePanel($event)"
        class="notification-trigger">
      </p-button>

      <p-overlayPanel 
        #notificationPanel 
        [style]="{width: '400px', maxHeight: '500px'}"
        [showCloseIcon]="true">
        
        <div class="notifications-panel">
          <div class="panel-header">
            <h3>Notificaciones</h3>
            <div class="header-actions">
              <p-button 
                label="Marcar todas como leídas"
                size="small"
                [text]="true"
                [disabled]="unreadCount === 0"
                (onClick)="markAllAsRead()">
              </p-button>
            </div>
          </div>

          <div class="notifications-list" *ngIf="notifications.length > 0; else noNotifications">
            <div 
              *ngFor="let notification of notifications; trackBy: trackByNotification"
              class="notification-item"
              [class.unread]="!notification.is_read"
              (click)="handleNotificationClick(notification)">
              
              <div class="notification-icon">
                <i [class]="getNotificationIcon(notification.type)" 
                   [style.color]="getNotificationColor(notification.type)"></i>
              </div>

              <div class="notification-content">
                <h4 class="notification-title">{{ notification.title }}</h4>
                <p class="notification-message">{{ notification.content }}</p>
                <div class="notification-meta">
                  <span class="notification-time">{{ getRelativeTime(notification.created_at) }}</span>
                  <span class="notification-type">{{ getTypeLabel(notification.type) }}</span>
                </div>
              </div>

              <div class="notification-actions">
                <p-button 
                  *ngIf="!notification.is_read"
                  icon="pi pi-check"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="markAsRead($event, notification)"
                  pTooltip="Marcar como leída">
                </p-button>
                <p-button 
                  icon="pi pi-times"
                  severity="danger"
                  [text]="true"
                  size="small"
                  (onClick)="deleteNotification($event, notification)"
                  pTooltip="Eliminar">
                </p-button>
              </div>
            </div>
          </div>

          <ng-template #noNotifications>
            <div class="empty-notifications">
              <i class="pi pi-bell empty-icon"></i>
              <h4>No hay notificaciones</h4>
              <p>Todas las notificaciones aparecerán aquí</p>
            </div>
          </ng-template>

          <div class="panel-footer" *ngIf="notifications.length > 0">
            <p-button 
              label="Ver todas las notificaciones"
              [text]="true"
              routerLink="/notifications"
              (onClick)="closePanel()">
            </p-button>
          </div>
        </div>
      </p-overlayPanel>
    </div>
  `,
  styles: [`
    .notification-trigger {
      position: relative;
    }

    .notifications-panel {
      padding: 0;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .panel-header h3 {
      margin: 0;
      color: #333;
      font-size: 1.1rem;
    }

    .notifications-list {
      max-height: 350px;
      overflow-y: auto;
    }

    .notification-item {
      display: flex;
      gap: 0.75rem;
      padding: 1rem;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .notification-item:hover {
      background: #f8f9fa;
    }

    .notification-item.unread {
      background: #f0f8ff;
      border-left: 3px solid #007bff;
    }

    .notification-icon {
      flex-shrink: 0;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f9fa;
      border-radius: 50%;
      font-size: 1.2rem;
    }

    .notification-content {
      flex: 1;
      min-width: 0;
    }

    .notification-title {
      margin: 0 0 0.25rem 0;
      font-size: 0.9rem;
      font-weight: 600;
      color: #333;
      line-height: 1.3;
    }

    .notification-message {
      margin: 0 0 0.5rem 0;
      font-size: 0.85rem;
      color: #666;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .notification-meta {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }

    .notification-time {
      font-size: 0.75rem;
      color: #999;
    }

    .notification-type {
      font-size: 0.7rem;
      background: #e9ecef;
      color: #495057;
      padding: 0.1rem 0.4rem;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .notification-actions {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .notification-item:hover .notification-actions {
      opacity: 1;
    }

    .empty-notifications {
      text-align: center;
      padding: 3rem 1rem;
      color: #666;
    }

    .empty-icon {
      font-size: 2.5rem;
      color: #ccc;
      margin-bottom: 1rem;
    }

    .empty-notifications h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }

    .empty-notifications p {
      margin: 0;
      font-size: 0.9rem;
    }

    .panel-footer {
      padding: 1rem;
      border-top: 1px solid #e0e0e0;
      text-align: center;
    }

    /* Badge personalizado */
    ::ng-deep .p-badge {
      min-width: 1.2rem;
      height: 1.2rem;
      line-height: 1.2rem;
      font-size: 0.7rem;
    }
  `]
})
export class NotificationsComponent implements OnInit, OnDestroy {
  notifications: Notification[] = [];
  unreadCount = 0;
  
  private subscriptions: Subscription[] = [];

  constructor(
    private notificationService: NotificationService,
    private wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.loadNotifications();
    this.subscribeToRealTimeNotifications();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadNotifications(): void {
    this.notificationService.getNotifications(1, 10).subscribe(
      response => {
        this.notifications = response.data;
        this.updateUnreadCount();
      }
    );
  }

  private subscribeToRealTimeNotifications(): void {
    const notificationSub = this.wsService.onNotification().subscribe(
      (notification: Notification) => {
        this.notifications.unshift(notification);
        this.updateUnreadCount();
        this.showToast(notification);
      }
    );
    this.subscriptions.push(notificationSub);
  }

  private updateUnreadCount(): void {
    this.unreadCount = this.notifications.filter(n => !n.is_read).length;
  }

  private showToast(notification: Notification): void {
    // Integrar con servicio de toast/mensajes
    console.log('Nueva notificación:', notification.title);
  }

  togglePanel(event: Event): void {
    // El panel se maneja automáticamente por PrimeNG
  }

  closePanel(): void {
    // Cerrar panel si es necesario
  }

  handleNotificationClick(notification: Notification): void {
    if (!notification.is_read) {
      this.markAsRead(null, notification);
    }

    if (notification.action_url) {
      // Navegar a la URL de acción
      // this.router.navigate([notification.action_url]);
    }
  }

  markAsRead(event: Event | null, notification: Notification): void {
    if (event) {
      event.stopPropagation();
    }

    this.notificationService.markAsRead(notification.id).subscribe(
      () => {
        notification.is_read = true;
        notification.read_at = new Date().toISOString();
        this.updateUnreadCount();
      }
    );
  }

  markAllAsRead(): void {
    this.notificationService.markAllAsRead().subscribe(
      () => {
        this.notifications.forEach(n => {
          n.is_read = true;
          n.read_at = new Date().toISOString();
        });
        this.updateUnreadCount();
      }
    );
  }

  deleteNotification(event: Event, notification: Notification): void {
    event.stopPropagation();

    this.notificationService.deleteNotification(notification.id).subscribe(
      () => {
        const index = this.notifications.indexOf(notification);
        if (index > -1) {
          this.notifications.splice(index, 1);
          this.updateUnreadCount();
        }
      }
    );
  }

  getNotificationIcon(type: string): string {
    const icons = {
      'task_assigned': 'pi pi-user',
      'task_updated': 'pi pi-refresh',
      'task_completed': 'pi pi-check-circle',
      'task_overdue': 'pi pi-clock',
      'comment_added': 'pi pi-comment',
      'comment_mention': 'pi pi-at',
      'project_invite': 'pi pi-users',
      'project_update': 'pi pi-folder',
      'chat_mention': 'pi pi-comments',
      'chat_message': 'pi pi-comment',
      'sprint_started': 'pi pi-play',
      'sprint_ended': 'pi pi-stop',
      'system_alert': 'pi pi-exclamation-triangle'
    };
    return icons[type as keyof typeof icons] || 'pi pi-bell';
  }

  getNotificationColor(type: string): string {
    const colors = {
      'task_assigned': '#007bff',
      'task_updated': '#6f42c1',
      'task_completed': '#28a745',
      'task_overdue': '#dc3545',
      'comment_added': '#17a2b8',
      'comment_mention': '#fd7e14',
      'project_invite': '#007bff',
      'project_update': '#6c757d',
      'chat_mention': '#fd7e14',
      'chat_message': '#17a2b8',
      'sprint_started': '#28a745',
      'sprint_ended': '#6c757d',
      'system_alert': '#dc3545'
    };
    return colors[type as keyof typeof colors] || '#6c757d';
  }

  getTypeLabel(type: string): string {
    const labels = {
      'task_assigned': 'Tarea',
      'task_updated': 'Tarea',
      'task_completed': 'Tarea',
      'task_overdue': 'Tarea',
      'comment_added': 'Comentario',
      'comment_mention': 'Mención',
      'project_invite': 'Proyecto',
      'project_update': 'Proyecto',
      'chat_mention': 'Chat',
      'chat_message': 'Chat',
      'sprint_started': 'Sprint',
      'sprint_ended': 'Sprint',
      'system_alert': 'Sistema'
    };
    return labels[type as keyof typeof labels] || 'General';
  }

  getRelativeTime(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Ahora';
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}d`;
    
    return date.toLocaleDateString();
  }

  trackByNotification(index: number, notification: Notification): string {
    return notification.id;
  }
}
