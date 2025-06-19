import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { BreadcrumbModule } from 'primeng/breadcrumb';

export interface BreadcrumbItem {
  label: string;
  routerLink?: string;
  icon?: string;
}

export interface ActionButton {
  label: string;
  icon: string;
  onClick: () => void;
  severity?: 'success' | 'info' | 'warning' | 'danger' | 'help' | 'primary' | 'secondary';
  disabled?: boolean;
}

@Component({
  selector: 'app-page-header',
  standalone: true,
  imports: [CommonModule, ButtonModule, BreadcrumbModule],
  template: `
    <div class="page-header">
      <div class="page-header-content">
        <div class="page-header-main">
          <h1 class="page-title">
            <i [class]="titleIcon" *ngIf="titleIcon"></i>
            {{ title }}
          </h1>
          <p class="page-description" *ngIf="description">{{ description }}</p>
          
          <p-breadcrumb 
            [model]="breadcrumbItems" 
            [home]="homeItem"
            *ngIf="breadcrumbs && breadcrumbs.length > 0">
          </p-breadcrumb>
        </div>
        
        <div class="page-header-actions" *ngIf="actions && actions.length > 0">
          <p-button 
            *ngFor="let action of actions"
            [label]="action.label"
            [icon]="action.icon"
            [severity]="action.severity || 'primary'"
            [disabled]="action.disabled"
            (onClick)="action.onClick()"
            class="action-button">
          </p-button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .page-header {
      background: white;
      border-bottom: 1px solid #e0e0e0;
      padding: 1.5rem 2rem;
      margin-bottom: 1.5rem;
    }

    .page-header-content {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      max-width: 100%;
    }

    .page-header-main {
      flex: 1;
    }

    .page-title {
      margin: 0 0 0.5rem 0;
      font-size: 1.75rem;
      font-weight: 600;
      color: #333;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .page-description {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.95rem;
    }

    .page-header-actions {
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
    }

    .action-button {
      white-space: nowrap;
    }

    @media (max-width: 768px) {
      .page-header {
        padding: 1rem;
      }

      .page-header-content {
        flex-direction: column;
        gap: 1rem;
      }

      .page-header-actions {
        width: 100%;
        justify-content: flex-end;
      }

      .page-title {
        font-size: 1.5rem;
      }
    }
  `]
})
export class PageHeaderComponent {
  @Input() title: string = '';
  @Input() description?: string;
  @Input() titleIcon?: string;
  @Input() breadcrumbs?: BreadcrumbItem[];
  @Input() actions?: ActionButton[];

  breadcrumbItems: any[] = [];
  homeItem = { icon: 'pi pi-home', routerLink: '/dashboard' };

  ngOnInit() {
    if (this.breadcrumbs) {
      this.breadcrumbItems = this.breadcrumbs.map(item => ({
        label: item.label,
        routerLink: item.routerLink,
        icon: item.icon
      }));
    }
  }
}
