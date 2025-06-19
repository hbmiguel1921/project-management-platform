import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { TooltipModule } from 'primeng/tooltip';
import { Task } from '@core/services/task.service';

@Component({
  selector: 'app-task-card',
  standalone: true,
  imports: [
    CommonModule, 
    CardModule, 
    TagModule, 
    ButtonModule, 
    AvatarModule, 
    TooltipModule
  ],
  template: `
    <p-card 
      class="task-card"
      [ngClass]="'task-card-' + task.priority"
      (click)="onCardClick()">
      
      <ng-template pTemplate="header">
        <div class="task-header">
          <div class="task-type-icon">
            <i [class]="getTypeIcon(task.type)" [style.color]="getTypeColor(task.type)"></i>
          </div>
          <div class="task-actions" *ngIf="showActions">
            <p-button 
              icon="pi pi-pencil" 
              severity="secondary" 
              [text]="true"
              size="small"
              (onClick)="onEdit($event)"
              pTooltip="Editar tarea">
            </p-button>
            <p-button 
              icon="pi pi-ellipsis-v" 
              severity="secondary" 
              [text]="true"
              size="small"
              (onClick)="onMenu($event)"
              pTooltip="Más opciones">
            </p-button>
          </div>
        </div>
      </ng-template>

      <div class="task-content">
        <h4 class="task-title">{{ task.title }}</h4>
        
        <p class="task-description" *ngIf="task.description">
          {{ task.description | slice:0:100 }}
          <span *ngIf="task.description.length > 100">...</span>
        </p>

        <div class="task-meta">
          <div class="task-tags" *ngIf="task.tags && task.tags.length > 0">
            <p-tag 
              *ngFor="let tag of task.tags | slice:0:3" 
              [value]="tag" 
              severity="info"
              class="task-tag">
            </p-tag>
            <span *ngIf="task.tags.length > 3" class="more-tags">
              +{{ task.tags.length - 3 }} más
            </span>
          </div>

          <div class="task-priority">
            <p-tag 
              [value]="getPriorityLabel(task.priority)"
              [severity]="getPrioritySeverity(task.priority)"
              [icon]="getPriorityIcon(task.priority)">
            </p-tag>
          </div>
        </div>

        <div class="task-footer">
          <div class="task-assignee" *ngIf="task.assignee">
            <p-avatar 
              [image]="task.assignee.avatar" 
              [label]="getInitials(task.assignee.first_name, task.assignee.last_name)"
              size="small"
              shape="circle"
              [pTooltip]="task.assignee.first_name + ' ' + task.assignee.last_name">
            </p-avatar>
          </div>

          <div class="task-due-date" *ngIf="task.due_date">
            <i class="pi pi-calendar" 
               [ngClass]="{'text-danger': isOverdue(task.due_date)}"></i>
            <span [ngClass]="{'text-danger': isOverdue(task.due_date)}">
              {{ task.due_date | date:'dd/MM' }}
            </span>
          </div>

          <div class="task-story-points" *ngIf="task.story_points">
            <i class="pi pi-chart-bar"></i>
            <span>{{ task.story_points }}pts</span>
          </div>
        </div>
      </div>
    </p-card>
  `,
  styles: [`
    .task-card {
      cursor: pointer;
      transition: all 0.2s ease;
      margin-bottom: 0.75rem;
      border-left: 4px solid #ddd;
    }

    .task-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .task-card-highest { border-left-color: #dc3545; }
    .task-card-high { border-left-color: #fd7e14; }
    .task-card-medium { border-left-color: #ffc107; }
    .task-card-low { border-left-color: #28a745; }
    .task-card-lowest { border-left-color: #6c757d; }

    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: #f8f9fa;
      margin: -1rem -1rem 0 -1rem;
    }

    .task-type-icon {
      font-size: 1.1rem;
    }

    .task-actions {
      display: flex;
      gap: 0.25rem;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .task-card:hover .task-actions {
      opacity: 1;
    }

    .task-content {
      padding: 1rem;
    }

    .task-title {
      margin: 0 0 0.5rem 0;
      font-size: 0.95rem;
      font-weight: 600;
      color: #333;
      line-height: 1.3;
    }

    .task-description {
      margin: 0 0 0.75rem 0;
      font-size: 0.85rem;
      color: #666;
      line-height: 1.4;
    }

    .task-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }

    .task-tags {
      display: flex;
      gap: 0.25rem;
      flex-wrap: wrap;
      align-items: center;
    }

    .task-tag {
      font-size: 0.7rem !important;
      padding: 0.2rem 0.4rem !important;
    }

    .more-tags {
      font-size: 0.75rem;
      color: #666;
    }

    .task-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }

    .task-assignee {
      flex-shrink: 0;
    }

    .task-due-date,
    .task-story-points {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.8rem;
      color: #666;
    }

    .text-danger {
      color: #dc3545 !important;
    }

    @media (max-width: 576px) {
      .task-footer {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
      }
      
      .task-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
      }
    }
  `]
})
export class TaskCardComponent {
  @Input() task!: Task;
  @Input() showActions = true;
  
  @Output() cardClick = new EventEmitter<Task>();
  @Output() edit = new EventEmitter<Task>();
  @Output() menu = new EventEmitter<{event: Event, task: Task}>();

  onCardClick(): void {
    this.cardClick.emit(this.task);
  }

  onEdit(event: Event): void {
    event.stopPropagation();
    this.edit.emit(this.task);
  }

  onMenu(event: Event): void {
    event.stopPropagation();
    this.menu.emit({ event, task: this.task });
  }

  getTypeIcon(type: string): string {
    const icons = {
      'story': 'pi pi-bookmark',
      'task': 'pi pi-check-square',
      'bug': 'pi pi-exclamation-triangle',
      'epic': 'pi pi-star',
      'subtask': 'pi pi-angle-right'
    };
    return icons[type as keyof typeof icons] || 'pi pi-circle';
  }

  getTypeColor(type: string): string {
    const colors = {
      'story': '#28a745',
      'task': '#007bff',
      'bug': '#dc3545',
      'epic': '#6f42c1',
      'subtask': '#6c757d'
    };
    return colors[type as keyof typeof colors] || '#6c757d';
  }

  getPriorityLabel(priority: string): string {
    const labels = {
      'highest': 'Muy Alta',
      'high': 'Alta',
      'medium': 'Media',
      'low': 'Baja',
      'lowest': 'Muy Baja'
    };
    return labels[priority as keyof typeof labels] || priority;
  }

  getPrioritySeverity(priority: string): any {
    const severities = {
      'highest': 'danger',
      'high': 'warning',
      'medium': 'info',
      'low': 'success',
      'lowest': 'secondary'
    };
    return severities[priority as keyof typeof severities] || 'info';
  }

  getPriorityIcon(priority: string): string {
    const icons = {
      'highest': 'pi pi-angle-double-up',
      'high': 'pi pi-angle-up',
      'medium': 'pi pi-minus',
      'low': 'pi pi-angle-down',
      'lowest': 'pi pi-angle-double-down'
    };
    return icons[priority as keyof typeof icons] || 'pi pi-minus';
  }

  getInitials(firstName: string, lastName: string): string {
    return (firstName?.[0] || '') + (lastName?.[0] || '');
  }

  isOverdue(dueDate: string): boolean {
    return new Date(dueDate) < new Date() && this.task.status !== 'done';
  }
}
