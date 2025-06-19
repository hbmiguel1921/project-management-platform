import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@environments/environment';
import { AuthService } from './auth.service';

export interface WebSocketMessage {
  type: string;
  project_id?: string;
  user_id?: string;
  data: any;
  timestamp: number;
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private connectedSubject = new BehaviorSubject<boolean>(false);
  public connected$ = this.connectedSubject.asObservable();

  private socket?: Socket;

  constructor(private authService: AuthService) {
    this.initializeConnection();
  }

  private initializeConnection(): void {
    this.authService.isAuthenticated$.subscribe(isAuth => {
      if (isAuth && !this.socket) {
        this.connect();
      } else if (!isAuth && this.socket) {
        this.disconnect();
      }
    });
  }

  private connect(): void {
    const token = this.authService.getToken();
    if (!token) return;

    // Crear configuración de socket con autenticación
    const socketConfig = {
      url: environment.wsUrl,
      options: {
        auth: {
          token: token
        },
        transports: ['websocket']
      }
    };

    this.socket = new Socket(socketConfig);

    this.socket.on('connect', () => {
      console.log('WebSocket conectado');
      this.connectedSubject.next(true);
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket desconectado');
      this.connectedSubject.next(false);
    });

    this.socket.on('error', (error: any) => {
      console.error('Error de WebSocket:', error);
    });

    this.socket.connect();
  }

  private disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = undefined;
      this.connectedSubject.next(false);
    }
  }

  // Suscribirse a un proyecto para recibir actualizaciones
  subscribeToProject(projectId: string): void {
    if (this.socket) {
      this.socket.emit('subscribe_project', projectId);
    }
  }

  // Desuscribirse de un proyecto
  unsubscribeFromProject(projectId: string): void {
    if (this.socket) {
      this.socket.emit('unsubscribe_project', projectId);
    }
  }

  // Escuchar mensajes de un tipo específico
  listen<T>(eventType: string): Observable<T> {
    if (!this.socket) {
      return new Observable(observer => {
        observer.error('Socket no está conectado');
      });
    }

    return new Observable(observer => {
      this.socket!.on(eventType, (data: T) => {
        observer.next(data);
      });

      // Cleanup cuando se desuscriba
      return () => {
        if (this.socket) {
          this.socket.off(eventType);
        }
      };
    });
  }

  // Enviar mensaje
  emit(eventType: string, data: any): void {
    if (this.socket) {
      this.socket.emit(eventType, data);
    }
  }

  // Eventos específicos para la aplicación
  onTaskUpdated(): Observable<any> {
    return this.listen('task_updated');
  }

  onTaskCreated(): Observable<any> {
    return this.listen('task_created');
  }

  onTaskDeleted(): Observable<any> {
    return this.listen('task_deleted');
  }

  onTaskMoved(): Observable<any> {
    return this.listen('task_moved');
  }

  onCommentAdded(): Observable<any> {
    return this.listen('comment_added');
  }

  onProjectUpdated(): Observable<any> {
    return this.listen('project_updated');
  }

  onUserJoinedProject(): Observable<any> {
    return this.listen('user_joined_project');
  }

  onUserLeftProject(): Observable<any> {
    return this.listen('user_left_project');
  }

  onNotification(): Observable<any> {
    return this.listen('notification');
  }

  // Chat en tiempo real
  onChatMessage(): Observable<any> {
    return this.listen('chat_message');
  }

  sendChatMessage(projectId: string, message: string): void {
    this.emit('send_chat_message', {
      project_id: projectId,
      message: message
    });
  }

  // Presencia de usuarios
  onUserPresence(): Observable<any> {
    return this.listen('user_presence');
  }

  updatePresence(status: 'online' | 'away' | 'busy' | 'offline'): void {
    this.emit('update_presence', { status });
  }

  isConnected(): boolean {
    return this.connectedSubject.value;
  }
}
