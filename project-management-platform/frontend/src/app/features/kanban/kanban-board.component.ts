import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DragDropModule, CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { TaskCardComponent } from '@shared/components/task-card/task-card.component';
import { TaskService, Task } from '@core/services/task.service';
import { WebSocketService } from '@core/services/websocket.service';

interface BoardColumn {
  id: string;
  title: string;
  status: string;
  tasks: Task[];
  wipLimit?: number;
  color: string;
}

@Component({
  selector: 'app-kanban-board',
  standalone: true,
  imports: [
    CommonModule,
    DragDropModule,
    CardModule,
    ButtonModule,
    DialogModule,
    TaskCardComponent
  ],
  template: `
    <div class="kanban-board">
      <div class="board-header">
        <h2>Tablero Kanban</h2>
        <div class="board-actions">
          <p-button 
            label="Agregar Tarea"
            icon="pi pi-plus"
            (onClick)="showCreateTaskDialog()">
          </p-button>
          <p-button 
            label="Configurar Tablero"
            icon="pi pi-cog"
            severity="secondary"
            [outlined]="true"
            (onClick)="showBoardConfig()">
          </p-button>
        </div>
      </div>

      <div class="board-columns" cdkDropListGroup>
        <div 
          *ngFor="let column of columns; trackBy: trackByColumn"
          class="board-column"
          [style.border-top-color]="column.color">
          
          <div class="column-header">
            <div class="column-title">
              <h3>{{ column.title }}</h3>
              <span class="task-count">{{ column.tasks.length }}</span>
              <span 
                *ngIf="column.wipLimit && column.tasks.length > column.wipLimit"
                class="wip-violation">
                ⚠️ WIP Limit: {{ column.wipLimit }}
              </span>
            </div>
            <div class="column-actions">
              <p-button 
                icon="pi pi-plus"
                severity="secondary"
                [text]="true"
                size="small"
                (onClick)="addTaskToColumn(column)"
                pTooltip="Agregar tarea">
              </p-button>
            </div>
          </div>

          <div 
            class="column-content"
            cdkDropList
            [cdkDropListData]="column.tasks"
            [id]="column.id"
            (cdkDropListDropped)="onTaskDrop($event)">
            
            <div 
              *ngFor="let task of column.tasks; trackBy: trackByTask"
              cdkDrag
              [cdkDragData]="task"
              class="task-wrapper">
              
              <app-task-card
                [task]="task"
                (cardClick)="openTaskDetail($event)"
                (edit)="editTask($event)"
                (menu)="showTaskMenu($event)">
              </app-task-card>

              <!-- Placeholder para drag -->
              <div 
                *cdkDragPlaceholder 
                class="task-placeholder">
                Soltar aquí...
              </div>
            </div>

            <!-- Zona de drop vacía -->
            <div 
              *ngIf="column.tasks.length === 0"
              class="empty-column">
              <i class="pi pi-inbox"></i>
              <p>No hay tareas</p>
              <small>Arrastra tareas aquí o crea una nueva</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialog para crear/editar tarea -->
    <p-dialog 
      header="Crear Tarea"
      [(visible)]="showTaskDialog"
      [modal]="true"
      [style]="{width: '600px'}"
      [closable]="true">
      
      <!-- Aquí iría el formulario de tarea -->
      <p>Formulario de crear/editar tarea (por implementar)</p>
      
      <ng-template pTemplate="footer">
        <p-button 
          label="Cancelar"
          severity="secondary"
          [outlined]="true"
          (onClick)="closeTaskDialog()">
        </p-button>
        <p-button 
          label="Guardar"
          (onClick)="saveTask()">
        </p-button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .kanban-board {
      height: 100%;
      display: flex;
      flex-direction: column;
      background: #f5f5f5;
    }

    .board-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 2rem;
      background: white;
      border-bottom: 1px solid #e0e0e0;
    }

    .board-header h2 {
      margin: 0;
      color: #333;
    }

    .board-actions {
      display: flex;
      gap: 0.5rem;
    }

    .board-columns {
      display: flex;
      gap: 1rem;
      padding: 1rem;
      overflow-x: auto;
      flex: 1;
      min-height: 0;
    }

    .board-column {
      flex: 0 0 300px;
      background: white;
      border-radius: 8px;
      border-top: 4px solid #007bff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      max-height: calc(100vh - 200px);
    }

    .column-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .column-title h3 {
      margin: 0;
      font-size: 1rem;
      color: #333;
    }

    .task-count {
      background: #6c757d;
      color: white;
      padding: 0.2rem 0.5rem;
      border-radius: 12px;
      font-size: 0.75rem;
      margin-left: 0.5rem;
    }

    .wip-violation {
      color: #dc3545;
      font-size: 0.75rem;
      margin-left: 0.5rem;
    }

    .column-content {
      flex: 1;
      padding: 0.5rem;
      overflow-y: auto;
      min-height: 200px;
    }

    .task-wrapper {
      margin-bottom: 0.5rem;
    }

    .task-placeholder {
      background: #e9ecef;
      border: 2px dashed #adb5bd;
      border-radius: 4px;
      padding: 1rem;
      text-align: center;
      color: #6c757d;
      margin-bottom: 0.5rem;
    }

    .empty-column {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
      text-align: center;
      color: #6c757d;
      min-height: 150px;
    }

    .empty-column i {
      font-size: 2rem;
      margin-bottom: 0.5rem;
      opacity: 0.5;
    }

    .empty-column p {
      margin: 0 0 0.25rem 0;
      font-weight: 500;
    }

    .empty-column small {
      opacity: 0.7;
    }

    /* Drag and drop styles */
    .cdk-drag-preview {
      box-sizing: border-box;
      border-radius: 4px;
      box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
                  0 8px 10px 1px rgba(0, 0, 0, 0.14),
                  0 3px 14px 2px rgba(0, 0, 0, 0.12);
      transform: rotate(5deg);
    }

    .cdk-drag-animating {
      transition: transform 250ms cubic-bezier(0, 0, 0.2, 1);
    }

    .cdk-drop-list-dragging .cdk-drag:not(.cdk-drag-placeholder) {
      transition: transform 250ms cubic-bezier(0, 0, 0.2, 1);
    }

    .cdk-drop-list-receiving {
      background: rgba(0, 123, 255, 0.05);
    }

    @media (max-width: 768px) {
      .board-header {
        flex-direction: column;
        gap: 1rem;
        align-items: flex-start;
      }

      .board-columns {
        flex-direction: column;
        padding: 0.5rem;
      }

      .board-column {
        flex: none;
        max-height: 400px;
      }
    }
  `]
})
export class KanbanBoardComponent implements OnInit {
  @Input() projectId!: string;

  columns: BoardColumn[] = [
    {
      id: 'todo',
      title: 'Por Hacer',
      status: 'todo',
      tasks: [],
      color: '#6c757d'
    },
    {
      id: 'in_progress',
      title: 'En Progreso',
      status: 'in_progress',
      tasks: [],
      wipLimit: 3,
      color: '#007bff'
    },
    {
      id: 'in_review',
      title: 'En Revisión',
      status: 'in_review',
      tasks: [],
      wipLimit: 2,
      color: '#ffc107'
    },
    {
      id: 'done',
      title: 'Completado',
      status: 'done',
      tasks: [],
      color: '#28a745'
    }
  ];

  showTaskDialog = false;
  selectedTask: Task | null = null;

  constructor(
    private taskService: TaskService,
    private wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.loadTasks();
    this.subscribeToUpdates();
  }

  private loadTasks(): void {
    if (!this.projectId) return;

    this.taskService.getTasks(this.projectId).subscribe(
      response => {
        this.distributeTasks(response.data);
      }
    );
  }

  private distributeTasks(tasks: Task[]): void {
    // Limpiar columnas
    this.columns.forEach(column => column.tasks = []);

    // Distribuir tareas por estado
    tasks.forEach(task => {
      const column = this.columns.find(col => col.status === task.status);
      if (column) {
        column.tasks.push(task);
      }
    });

    // Ordenar tareas por posición
    this.columns.forEach(column => {
      column.tasks.sort((a, b) => a.position - b.position);
    });
  }

  private subscribeToUpdates(): void {
    if (!this.projectId) return;

    // Suscribirse al proyecto para recibir actualizaciones
    this.wsService.subscribeToProject(this.projectId);

    // Escuchar actualizaciones de tareas
    this.wsService.onTaskUpdated().subscribe(update => {
      this.handleTaskUpdate(update);
    });

    this.wsService.onTaskCreated().subscribe(task => {
      this.handleTaskCreated(task);
    });

    this.wsService.onTaskMoved().subscribe(update => {
      this.handleTaskMoved(update);
    });
  }

  onTaskDrop(event: CdkDragDrop<Task[]>): void {
    if (event.previousContainer === event.container) {
      // Mover dentro de la misma columna
      moveItemInArray(
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    } else {
      // Mover a otra columna
      const task = event.previousContainer.data[event.previousIndex];
      const targetColumn = this.columns.find(col => 
        col.tasks === event.container.data
      );

      if (targetColumn) {
        // Verificar WIP limit
        if (targetColumn.wipLimit && 
            event.container.data.length >= targetColumn.wipLimit) {
          // Mostrar mensaje de error o manejar violación de WIP limit
          console.warn(`WIP limit exceeded for column ${targetColumn.title}`);
          return;
        }

        transferArrayItem(
          event.previousContainer.data,
          event.container.data,
          event.previousIndex,
          event.currentIndex
        );

        // Actualizar estado en el backend
        this.updateTaskStatus(task, targetColumn.status, event.currentIndex);
      }
    }
  }

  private updateTaskStatus(task: Task, newStatus: string, newPosition: number): void {
    this.taskService.moveTaskToPosition(task.id, newPosition, newStatus).subscribe(
      updatedTask => {
        // Actualizar tarea local
        const taskIndex = this.findTaskIndex(task.id);
        if (taskIndex) {
          taskIndex.column.tasks[taskIndex.index] = updatedTask;
        }
      },
      error => {
        console.error('Error updating task:', error);
        // Revertir cambio visual si hay error
        this.loadTasks();
      }
    );
  }

  private findTaskIndex(taskId: string): {column: BoardColumn, index: number} | null {
    for (const column of this.columns) {
      const index = column.tasks.findIndex(t => t.id === taskId);
      if (index !== -1) {
        return { column, index };
      }
    }
    return null;
  }

  private handleTaskUpdate(update: any): void {
    const taskIndex = this.findTaskIndex(update.task.id);
    if (taskIndex) {
      taskIndex.column.tasks[taskIndex.index] = update.task;
    }
  }

  private handleTaskCreated(task: Task): void {
    const column = this.columns.find(col => col.status === task.status);
    if (column) {
      column.tasks.push(task);
    }
  }

  private handleTaskMoved(update: any): void {
    // Recargar tareas para reflejar el movimiento
    this.loadTasks();
  }

  trackByColumn(index: number, column: BoardColumn): string {
    return column.id;
  }

  trackByTask(index: number, task: Task): string {
    return task.id;
  }

  showCreateTaskDialog(): void {
    this.selectedTask = null;
    this.showTaskDialog = true;
  }

  addTaskToColumn(column: BoardColumn): void {
    // Lógica para agregar tarea directamente a una columna
    this.showCreateTaskDialog();
  }

  openTaskDetail(task: Task): void {
    // Abrir modal de detalle de tarea
    console.log('Open task detail:', task);
  }

  editTask(task: Task): void {
    this.selectedTask = task;
    this.showTaskDialog = true;
  }

  showTaskMenu(event: {event: Event, task: Task}): void {
    // Mostrar menú contextual para la tarea
    console.log('Show task menu:', event);
  }

  showBoardConfig(): void {
    // Mostrar configuración del tablero
    console.log('Show board config');
  }

  closeTaskDialog(): void {
    this.showTaskDialog = false;
    this.selectedTask = null;
  }

  saveTask(): void {
    // Guardar tarea
    console.log('Save task');
    this.closeTaskDialog();
  }
}
