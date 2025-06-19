import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';

export interface ChatChannel {
  id: string;
  name: string;
  description?: string;
  type: 'project' | 'general' | 'private' | 'direct';
  project_id?: string;
  is_private: boolean;
  creator_id: string;
  created_at: string;
  updated_at: string;
  members?: ChannelMember[];
  project?: any;
}

export interface ChannelMember {
  id: string;
  channel_id: string;
  user_id: string;
  role: 'admin' | 'member';
  joined_at: string;
  last_read?: string;
  user?: any;
}

export interface ChatMessage {
  id: string;
  content: string;
  channel_id: string;
  user_id: string;
  type: 'text' | 'file' | 'image' | 'system' | 'task_link' | 'project_link';
  is_edited: boolean;
  edited_at?: string;
  reply_to_id?: string;
  created_at: string;
  updated_at: string;
  user?: any;
  reply_to?: ChatMessage;
  reactions?: MessageReaction[];
  attachments?: MessageAttachment[];
}

export interface MessageReaction {
  id: string;
  message_id: string;
  user_id: string;
  emoji: string;
  created_at: string;
  user?: any;
}

export interface MessageAttachment {
  id: string;
  message_id: string;
  file_name: string;
  file_url: string;
  file_size: number;
  mime_type: string;
}

export interface CreateChannelRequest {
  name: string;
  description?: string;
  type: 'project' | 'general' | 'private' | 'direct';
  project_id?: string;
  is_private: boolean;
  members: string[];
}

export interface SendMessageRequest {
  content: string;
  type?: string;
  reply_to_id?: string;
  attachments?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(private http: HttpClient) { }

  getChannels(projectId?: string): Observable<ChatChannel[]> {
    let params = new HttpParams();
    if (projectId) {
      params = params.set('project_id', projectId);
    }
    
    return this.http.get<ChatChannel[]>(`${environment.apiUrl}/chat/channels`, { params });
  }

  getChannel(channelId: string): Observable<ChatChannel> {
    return this.http.get<ChatChannel>(`${environment.apiUrl}/chat/channels/${channelId}`);
  }

  createChannel(channelData: CreateChannelRequest): Observable<ChatChannel> {
    return this.http.post<ChatChannel>(`${environment.apiUrl}/chat/channels`, channelData);
  }

  getMessages(channelId: string, limit = 50, offset = 0): Observable<ChatMessage[]> {
    const params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    
    return this.http.get<ChatMessage[]>(`${environment.apiUrl}/chat/channels/${channelId}/messages`, { params });
  }

  sendMessage(channelId: string, messageData: SendMessageRequest): Observable<ChatMessage> {
    return this.http.post<ChatMessage>(`${environment.apiUrl}/chat/channels/${channelId}/messages`, messageData);
  }

  editMessage(channelId: string, messageId: string, content: string): Observable<ChatMessage> {
    return this.http.put<ChatMessage>(`${environment.apiUrl}/chat/channels/${channelId}/messages/${messageId}`, {
      content
    });
  }

  deleteMessage(channelId: string, messageId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/chat/channels/${channelId}/messages/${messageId}`);
  }

  addReaction(messageId: string, emoji: string): Observable<MessageReaction | null> {
    return this.http.post<MessageReaction | null>(`${environment.apiUrl}/chat/messages/${messageId}/reactions`, {
      emoji
    });
  }

  markChannelAsRead(channelId: string): Observable<void> {
    return this.http.post<void>(`${environment.apiUrl}/chat/channels/${channelId}/read`, {});
  }

  addMemberToChannel(channelId: string, userId: string): Observable<ChannelMember> {
    return this.http.post<ChannelMember>(`${environment.apiUrl}/chat/channels/${channelId}/members`, {
      user_id: userId
    });
  }

  removeMemberFromChannel(channelId: string, userId: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/chat/channels/${channelId}/members/${userId}`);
  }

  uploadFile(file: File): Observable<{file_url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{file_url: string}>(`${environment.apiUrl}/chat/upload`, formData);
  }

  searchMessages(query: string, channelId?: string): Observable<ChatMessage[]> {
    let params = new HttpParams().set('q', query);
    if (channelId) {
      params = params.set('channel_id', channelId);
    }
    
    return this.http.get<ChatMessage[]>(`${environment.apiUrl}/chat/search`, { params });
  }
}
