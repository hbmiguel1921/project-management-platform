import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { DividerModule } from 'primeng/divider';
import { MenuModule } from 'primeng/menu';
import { BadgeModule } from 'primeng/badge';
import { FileUploadModule } from 'primeng/fileupload';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { Subscription } from 'rxjs';
import { ChatService, ChatChannel, ChatMessage } from '@core/services/chat.service';
import { WebSocketService } from '@core/services/websocket.service';
import { AuthService, User } from '@core/services/auth.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    CardModule,
    InputTextModule,
    ButtonModule,
    AvatarModule,
    ScrollPanelModule,
    DividerModule,
    MenuModule,
    BadgeModule,
    FileUploadModule,
    OverlayPanelModule
  ],
  template: `
    <div class="chat-container">
      <!-- Sidebar de canales -->
      <div class="chat-sidebar">
        <div class="sidebar-header">
          <h3>Canales</h3>
          <p-button 
            icon="pi pi-plus"
            severity="secondary"
            [text]="true"
            size="small"
            (onClick)="showCreateChannelDialog()"
            pTooltip="Crear canal">
          </p-button>
        </div>

        <div class="channels-list">
          <div 
            *ngFor="let channel of channels"
            class="channel-item"
            [class.active]="selectedChannel?.id === channel.id"
            (click)="selectChannel(channel)">
            
            <div class="channel-info">
              <i class="pi pi-hashtag channel-icon"></i>
              <span class="channel-name">{{ channel.name }}</span>
            </div>
            
            <p-badge 
              *ngIf="getUnreadCount(channel.id) > 0"
              [value]="getUnreadCount(channel.id)"
              severity="danger">
            </p-badge>
          </div>
        </div>

        <!-- Mensajes directos -->
        <div class="direct-messages">
          <h4>Mensajes Directos</h4>
          <!-- Lista de conversaciones directas -->
        </div>
      </div>

      <!-- Área principal del chat -->
      <div class="chat-main" *ngIf="selectedChannel">
        <!-- Header del canal -->
        <div class="chat-header">
          <div class="channel-info">
            <h3># {{ selectedChannel.name }}</h3>
            <p *ngIf="selectedChannel.description">{{ selectedChannel.description }}</p>
          </div>
          
          <div class="channel-actions">
            <p-button 
              icon="pi pi-users"
              severity="secondary"
              [text]="true"
              (onClick)="showChannelMembers()"
              pTooltip="Miembros del canal">
            </p-button>
            <p-button 
              icon="pi pi-cog"
              severity="secondary"
              [text]="true"
              (onClick)="showChannelSettings()"
              pTooltip="Configuración">
            </p-button>
          </div>
        </div>

        <!-- Mensajes -->
        <div class="messages-container" #messagesContainer>
          <div 
            *ngFor="let message of messages; trackBy: trackByMessage"
            class="message-group"
            [class.own-message]="message.user_id === currentUser?.id">
            
            <div class="message-avatar" *ngIf="!isConsecutiveMessage(message)">
              <p-avatar 
                [image]="message.user?.avatar"
                [label]="getUserInitials(message.user)"
                size="normal"
                shape="circle">
              </p-avatar>
            </div>

            <div class="message-content">
              <div class="message-header" *ngIf="!isConsecutiveMessage(message)">
                <span class="message-author">{{ message.user?.first_name }} {{ message.user?.last_name }}</span>
                <span class="message-time">{{ message.created_at | date:'dd/MM HH:mm' }}</span>
              </div>

              <div class="message-body">
                <div class="message-text" [innerHTML]="formatMessageContent(message.content)"></div>
                
                <!-- Adjuntos -->
                <div class="message-attachments" *ngIf="message.attachments && message.attachments.length > 0">
                  <div 
                    *ngFor="let attachment of message.attachments"
                    class="attachment">
                    <!-- Renderizar según tipo de archivo -->
                  </div>
                </div>

                <!-- Respuesta a mensaje -->
                <div class="message-reply" *ngIf="message.reply_to">
                  <div class="reply-content">
                    <small>{{ message.reply_to.user?.first_name }}: {{ message.reply_to.content | slice:0:50 }}...</small>
                  </div>
                </div>
              </div>

              <!-- Reacciones -->
              <div class="message-reactions" *ngIf="message.reactions && message.reactions.length > 0">
                <span 
                  *ngFor="let reaction of getGroupedReactions(message.reactions)"
                  class="reaction"
                  [class.user-reacted]="hasUserReacted(reaction, currentUser?.id)"
                  (click)="toggleReaction(message.id, reaction.emoji)">
                  {{ reaction.emoji }} {{ reaction.count }}
                </span>
              </div>

              <!-- Acciones del mensaje -->
              <div class="message-actions">
                <p-button 
                  icon="pi pi-smile"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="showEmojiPicker(message)"
                  pTooltip="Reaccionar">
                </p-button>
                <p-button 
                  icon="pi pi-reply"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="replyToMessage(message)"
                  pTooltip="Responder">
                </p-button>
                <p-button 
                  *ngIf="message.user_id === currentUser?.id"
                  icon="pi pi-pencil"
                  severity="secondary"
                  [text]="true"
                  size="small"
                  (onClick)="editMessage(message)"
                  pTooltip="Editar">
                </p-button>
              </div>
            </div>
          </div>

          <!-- Indicador de usuario escribiendo -->
          <div class="typing-indicator" *ngIf="typingUsers.length > 0">
            <span>{{ getTypingText() }}</span>
          </div>
        </div>

        <!-- Input de mensaje -->
        <div class="message-input-container">
          <!-- Respuesta a mensaje -->
          <div class="reply-preview" *ngIf="replyingTo">
            <div class="reply-info">
              <small>Respondiendo a {{ replyingTo.user?.first_name }}</small>
              <p>{{ replyingTo.content | slice:0:100 }}</p>
            </div>
            <p-button 
              icon="pi pi-times"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="cancelReply()">
            </p-button>
          </div>

          <div class="input-area">
            <div class="input-actions">
              <p-button 
                icon="pi pi-paperclip"
                severity="secondary"
                [text]="true"
                (onClick)="showFileUpload()"
                pTooltip="Adjuntar archivo">
              </p-button>
            </div>

            <input 
              type="text"
              placeholder="Escribe un mensaje..."
              [(ngModel)]="newMessage"
              (keyup.enter)="sendMessage()"
              (keyup)="onTyping()"
              class="message-input"
              #messageInput>

            <p-button 
              icon="pi pi-send"
              [disabled]="!newMessage.trim()"
              (onClick)="sendMessage()">
            </p-button>
          </div>
        </div>
      </div>

      <!-- Panel vacío cuando no hay canal seleccionado -->
      <div class="chat-empty" *ngIf="!selectedChannel">
        <div class="empty-content">
          <i class="pi pi-comments empty-icon"></i>
          <h3>Selecciona un canal</h3>
          <p>Elige un canal de la lista para comenzar a chatear</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chat-container {
      display: flex;
      height: calc(100vh - 120px);
      background: white;
      border-radius: 8px;
      overflow: hidden;
    }

    /* Sidebar */
    .chat-sidebar {
      width: 300px;
      background: #f8f9fa;
      border-right: 1px solid #e0e0e0;
      display: flex;
      flex-direction: column;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
    }

    .sidebar-header h3 {
      margin: 0;
      color: #333;
    }

    .channels-list {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem 0;
    }

    .channel-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .channel-item:hover {
      background: #e9ecef;
    }

    .channel-item.active {
      background: #007bff;
      color: white;
    }

    .channel-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .channel-icon {
      color: #6c757d;
    }

    .channel-item.active .channel-icon {
      color: white;
    }

    .channel-name {
      font-weight: 500;
    }

    .direct-messages {
      border-top: 1px solid #e0e0e0;
      padding: 1rem;
    }

    .direct-messages h4 {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Chat principal */
    .chat-main {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #e0e0e0;
      background: white;
    }

    .chat-header h3 {
      margin: 0;
      color: #333;
    }

    .chat-header p {
      margin: 0.25rem 0 0 0;
      color: #666;
      font-size: 0.9rem;
    }

    .channel-actions {
      display: flex;
      gap: 0.5rem;
    }

    /* Mensajes */
    .messages-container {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .message-group {
      display: flex;
      gap: 0.75rem;
      padding: 0.25rem 0;
    }

    .message-group.own-message {
      flex-direction: row-reverse;
    }

    .message-avatar {
      flex-shrink: 0;
      width: 40px;
    }

    .message-content {
      flex: 1;
      min-width: 0;
    }

    .message-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.25rem;
    }

    .message-author {
      font-weight: 600;
      color: #333;
    }

    .message-time {
      font-size: 0.8rem;
      color: #999;
    }

    .message-body {
      background: #f8f9fa;
      padding: 0.75rem;
      border-radius: 8px;
      position: relative;
    }

    .own-message .message-body {
      background: #007bff;
      color: white;
    }

    .message-text {
      line-height: 1.4;
      word-wrap: break-word;
    }

    .message-reply {
      margin-top: 0.5rem;
      padding: 0.5rem;
      background: rgba(0,0,0,0.1);
      border-radius: 4px;
      border-left: 3px solid #007bff;
    }

    .message-reactions {
      display: flex;
      gap: 0.25rem;
      margin-top: 0.5rem;
    }

    .reaction {
      background: #e9ecef;
      border: 1px solid #dee2e6;
      border-radius: 12px;
      padding: 0.2rem 0.4rem;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .reaction:hover {
      background: #dee2e6;
    }

    .reaction.user-reacted {
      background: #007bff;
      color: white;
      border-color: #007bff;
    }

    .message-actions {
      display: flex;
      gap: 0.25rem;
      margin-top: 0.5rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .message-group:hover .message-actions {
      opacity: 1;
    }

    .typing-indicator {
      padding: 0.5rem 1rem;
      font-style: italic;
      color: #666;
      font-size: 0.9rem;
    }

    /* Input de mensaje */
    .message-input-container {
      border-top: 1px solid #e0e0e0;
      background: white;
    }

    .reply-preview {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      background: #f8f9fa;
      border-bottom: 1px solid #e0e0e0;
    }

    .reply-info small {
      display: block;
      color: #007bff;
      font-weight: 500;
    }

    .reply-info p {
      margin: 0.25rem 0 0 0;
      color: #666;
    }

    .input-area {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 1rem;
    }

    .input-actions {
      display: flex;
      gap: 0.25rem;
    }

    .message-input {
      flex: 1;
      border: 1px solid #e0e0e0;
      border-radius: 20px;
      padding: 0.75rem 1rem;
      outline: none;
      font-size: 0.95rem;
    }

    .message-input:focus {
      border-color: #007bff;
    }

    /* Estado vacío */
    .chat-empty {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .empty-content {
      text-align: center;
      color: #666;
    }

    .empty-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      opacity: 0.3;
    }

    .empty-content h3 {
      margin: 0 0 0.5rem 0;
    }

    .empty-content p {
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .chat-sidebar {
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        z-index: 1000;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
      }

      .chat-sidebar.mobile-open {
        transform: translateX(0);
      }

      .chat-main {
        width: 100%;
      }
    }
  `]
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('messageInput') messageInput!: ElementRef;

  channels: ChatChannel[] = [];
  selectedChannel: ChatChannel | null = null;
  messages: ChatMessage[] = [];
  newMessage = '';
  replyingTo: ChatMessage | null = null;
  currentUser: User | null = null;
  typingUsers: string[] = [];

  private subscriptions: Subscription[] = [];

  constructor(
    private chatService: ChatService,
    private wsService: WebSocketService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadCurrentUser();
    this.loadChannels();
    this.subscribeToMessages();
    this.subscribeToTyping();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadCurrentUser(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  private loadChannels(): void {
    this.chatService.getChannels().subscribe(
      channels => {
        this.channels = channels;
        if (channels.length > 0 && !this.selectedChannel) {
          this.selectChannel(channels[0]);
        }
      }
    );
  }

  private subscribeToMessages(): void {
    const messagesSub = this.wsService.onChatMessage().subscribe(
      (data: any) => {
        if (data.channel_id === this.selectedChannel?.id) {
          this.messages.push(data.message);
          this.scrollToBottom();
        }
      }
    );
    this.subscriptions.push(messagesSub);
  }

  private subscribeToTyping(): void {
    // Implementar indicador de escritura
  }

  selectChannel(channel: ChatChannel): void {
    this.selectedChannel = channel;
    this.loadMessages();
    this.wsService.subscribeToProject(channel.project_id || '');
  }

  private loadMessages(): void {
    if (!this.selectedChannel) return;

    this.chatService.getMessages(this.selectedChannel.id).subscribe(
      messages => {
        this.messages = messages;
        setTimeout(() => this.scrollToBottom(), 100);
      }
    );
  }

  sendMessage(): void {
    if (!this.newMessage.trim() || !this.selectedChannel) return;

    const messageData = {
      content: this.newMessage,
      reply_to_id: this.replyingTo?.id
    };

    this.chatService.sendMessage(this.selectedChannel.id, messageData).subscribe(
      message => {
        this.messages.push(message);
        this.newMessage = '';
        this.replyingTo = null;
        this.scrollToBottom();
      }
    );
  }

  onTyping(): void {
    // Implementar indicador de escritura
    this.wsService.emit('typing', {
      channel_id: this.selectedChannel?.id,
      user_id: this.currentUser?.id
    });
  }

  replyToMessage(message: ChatMessage): void {
    this.replyingTo = message;
    this.messageInput.nativeElement.focus();
  }

  cancelReply(): void {
    this.replyingTo = null;
  }

  editMessage(message: ChatMessage): void {
    // Implementar edición de mensajes
  }

  toggleReaction(messageId: string, emoji: string): void {
    this.chatService.addReaction(messageId, emoji).subscribe();
  }

  showEmojiPicker(message: ChatMessage): void {
    // Implementar selector de emojis
  }

  showFileUpload(): void {
    // Implementar carga de archivos
  }

  showCreateChannelDialog(): void {
    // Implementar creación de canales
  }

  showChannelMembers(): void {
    // Mostrar miembros del canal
  }

  showChannelSettings(): void {
    // Mostrar configuración del canal
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const container = this.messagesContainer?.nativeElement;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }, 50);
  }

  formatMessageContent(content: string): string {
    // Implementar formateo de mensajes (markdown, menciones, enlaces)
    return content.replace(/
/g, '<br>');
  }

  getUserInitials(user: any): string {
    if (!user) return '';
    return (user.first_name?.[0] || '') + (user.last_name?.[0] || '');
  }

  isConsecutiveMessage(message: ChatMessage): boolean {
    const index = this.messages.indexOf(message);
    if (index === 0) return false;
    
    const prevMessage = this.messages[index - 1];
    return prevMessage.user_id === message.user_id &&
           (new Date(message.created_at).getTime() - new Date(prevMessage.created_at).getTime()) < 300000; // 5 minutos
  }

  getGroupedReactions(reactions: any[]): any[] {
    const grouped: {[emoji: string]: any} = {};
    
    reactions.forEach(reaction => {
      if (!grouped[reaction.emoji]) {
        grouped[reaction.emoji] = {
          emoji: reaction.emoji,
          count: 0,
          users: []
        };
      }
      grouped[reaction.emoji].count++;
      grouped[reaction.emoji].users.push(reaction.user);
    });
    
    return Object.values(grouped);
  }

  hasUserReacted(reaction: any, userId?: string): boolean {
    return reaction.users.some((user: any) => user.id === userId);
  }

  getUnreadCount(channelId: string): number {
    // Implementar conteo de mensajes no leídos
    return 0;
  }

  getTypingText(): string {
    if (this.typingUsers.length === 1) {
      return `${this.typingUsers[0]} está escribiendo...`;
    } else if (this.typingUsers.length === 2) {
      return `${this.typingUsers[0]} y ${this.typingUsers[1]} están escribiendo...`;
    } else if (this.typingUsers.length > 2) {
      return `${this.typingUsers.length} personas están escribiendo...`;
    }
    return '';
  }

  trackByMessage(index: number, message: ChatMessage): string {
    return message.id;
  }
}
