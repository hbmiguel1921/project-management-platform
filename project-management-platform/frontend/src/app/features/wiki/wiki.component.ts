import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TreeModule } from 'primeng/tree';
import { TagModule } from 'primeng/tag';
import { MenuModule } from 'primeng/menu';
import { BreadcrumbModule } from 'primeng/breadcrumb';
import { PageHeaderComponent } from '@shared/components/page-header/page-header.component';
import { WikiService, WikiPage } from '@core/services/wiki.service';

@Component({
  selector: 'app-wiki',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    TreeModule,
    TagModule,
    MenuModule,
    BreadcrumbModule,
    PageHeaderComponent
  ],
  template: `
    <app-page-header
      title="Base de Conocimientos"
      description="Documentación y recursos del proyecto"
      titleIcon="pi pi-book"
      [actions]="headerActions">
    </app-page-header>

    <div class="wiki-container">
      <!-- Sidebar de navegación -->
      <div class="wiki-sidebar">
        <div class="sidebar-header">
          <h3>Páginas</h3>
          <div class="sidebar-actions">
            <p-button 
              icon="pi pi-plus"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="createPage()"
              pTooltip="Nueva página">
            </p-button>
            <p-button 
              icon="pi pi-search"
              severity="secondary"
              [text]="true"
              size="small"
              (onClick)="toggleSearch()"
              pTooltip="Buscar">
            </p-button>
          </div>
        </div>

        <!-- Búsqueda -->
        <div class="search-container" *ngIf="showSearch">
          <input 
            type="text"
            placeholder="Buscar páginas..."
            [(ngModel)]="searchQuery"
            (keyup)="onSearch()"
            class="search-input">
        </div>

        <!-- Árbol de páginas -->
        <div class="pages-tree">
          <p-tree 
            [value]="pageTree"
            selectionMode="single"
            [(selection)]="selectedPage"
            (onNodeSelect)="onPageSelect($event)"
            [loading]="loadingPages">
            
            <ng-template let-node pTemplate="default">
              <div class="tree-node">
                <i [class]="getPageIcon(node.data)" class="page-icon"></i>
                <span class="page-title">{{ node.label }}</span>
                <p-tag 
                  *ngIf="!node.data.is_published"
                  value="Borrador"
                  severity="warning"
                  class="page-status">
                </p-tag>
              </div>
            </ng-template>
          </p-tree>
        </div>

        <!-- Páginas recientes -->
        <div class="recent-pages">
          <h4>Páginas Recientes</h4>
          <div class="recent-list">
            <div 
              *ngFor="let page of recentPages"
              class="recent-item"
              [routerLink]="['/wiki', page.id]">
              <span class="recent-title">{{ page.title }}</span>
              <small class="recent-time">{{ page.updated_at | date:'dd/MM' }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="wiki-content">
        <router-outlet></router-outlet>
        
        <!-- Vista por defecto cuando no hay página seleccionada -->
        <div class="wiki-home" *ngIf="!selectedPage">
          <div class="welcome-section">
            <h2>Bienvenido a la Base de Conocimientos</h2>
            <p>Aquí encontrarás toda la documentación y recursos del proyecto.</p>
            
            <div class="quick-actions">
              <p-button 
                label="Crear Primera Página"
                icon="pi pi-plus"
                (onClick)="createPage()">
              </p-button>
              <p-button 
                label="Explorar Plantillas"
                icon="pi pi-file"
                severity="secondary"
                [outlined]="true"
                (onClick)="showTemplates()">
              </p-button>
            </div>
          </div>

          <!-- Estadísticas -->
          <div class="wiki-stats">
            <div class="stats-grid">
              <div class="stat-item">
                <h3>{{ totalPages }}</h3>
                <p>Páginas Total</p>
              </div>
              <div class="stat-item">
                <h3>{{ publishedPages }}</h3>
                <p>Publicadas</p>
              </div>
              <div class="stat-item">
                <h3>{{ draftPages }}</h3>
                <p>Borradores</p>
              </div>
              <div class="stat-item">
                <h3>{{ totalContributors }}</h3>
                <p>Colaboradores</p>
              </div>
            </div>
          </div>

          <!-- Páginas populares -->
          <div class="popular-pages" *ngIf="popularPages.length > 0">
            <h3>Páginas Populares</h3>
            <div class="pages-grid">
              <p-card 
                *ngFor="let page of popularPages"
                class="page-card"
                [routerLink]="['/wiki', page.id]">
                
                <div class="page-card-content">
                  <h4>{{ page.title }}</h4>
                  <p>{{ page.content | slice:0:150 }}...</p>
                  
                  <div class="page-meta">
                    <span class="author">Por {{ page.author?.first_name }} {{ page.author?.last_name }}</span>
                    <span class="date">{{ page.updated_at | date:'dd/MM/yyyy' }}</span>
                  </div>

                  <div class="page-tags" *ngIf="page.tags && page.tags.length > 0">
                    <p-tag 
                      *ngFor="let tag of page.tags | slice:0:3"
                      [value]="tag"
                      severity="info">
                    </p-tag>
                  </div>
                </div>
              </p-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .wiki-container {
      display: flex;
      height: calc(100vh - 180px);
      gap: 1rem;
      padding: 0 2rem 2rem;
    }

    /* Sidebar */
    .wiki-sidebar {
      width: 300px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
      background: #f8f9fa;
    }

    .sidebar-header h3 {
      margin: 0;
      color: #333;
    }

    .sidebar-actions {
      display: flex;
      gap: 0.25rem;
    }

    .search-container {
      padding: 1rem;
      border-bottom: 1px solid #e0e0e0;
    }

    .search-input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      outline: none;
    }

    .search-input:focus {
      border-color: #007bff;
    }

    .pages-tree {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem;
    }

    .tree-node {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      width: 100%;
    }

    .page-icon {
      color: #6c757d;
    }

    .page-title {
      flex: 1;
      font-size: 0.9rem;
    }

    .page-status {
      font-size: 0.7rem !important;
    }

    .recent-pages {
      border-top: 1px solid #e0e0e0;
      padding: 1rem;
    }

    .recent-pages h4 {
      margin: 0 0 0.75rem 0;
      color: #666;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .recent-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0;
      cursor: pointer;
      border-bottom: 1px solid #f0f0f0;
      transition: background 0.2s ease;
    }

    .recent-item:hover {
      background: #f8f9fa;
    }

    .recent-title {
      font-size: 0.85rem;
      color: #333;
    }

    .recent-time {
      font-size: 0.75rem;
      color: #999;
    }

    /* Contenido principal */
    .wiki-content {
      flex: 1;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
    }

    .wiki-home {
      padding: 2rem;
      height: 100%;
      overflow-y: auto;
    }

    .welcome-section {
      text-align: center;
      margin-bottom: 3rem;
    }

    .welcome-section h2 {
      margin: 0 0 1rem 0;
      color: #333;
    }

    .welcome-section p {
      margin: 0 0 2rem 0;
      color: #666;
      font-size: 1.1rem;
    }

    .quick-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }

    .wiki-stats {
      margin-bottom: 3rem;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
    }

    .stat-item {
      text-align: center;
      padding: 1.5rem;
      background: #f8f9fa;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
    }

    .stat-item h3 {
      margin: 0 0 0.5rem 0;
      font-size: 2rem;
      color: #007bff;
    }

    .stat-item p {
      margin: 0;
      color: #666;
      font-size: 0.9rem;
    }

    .popular-pages h3 {
      margin: 0 0 1.5rem 0;
      color: #333;
    }

    .pages-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1rem;
    }

    .page-card {
      cursor: pointer;
      transition: transform 0.2s ease;
    }

    .page-card:hover {
      transform: translateY(-2px);
    }

    .page-card-content h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
      font-size: 1.1rem;
    }

    .page-card-content p {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.9rem;
      line-height: 1.4;
    }

    .page-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
      font-size: 0.8rem;
      color: #999;
    }

    .page-tags {
      display: flex;
      gap: 0.25rem;
      flex-wrap: wrap;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .wiki-container {
        flex-direction: column;
        height: auto;
        padding: 0 1rem 1rem;
      }

      .wiki-sidebar {
        width: 100%;
        height: auto;
        margin-bottom: 1rem;
      }

      .stats-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .pages-grid {
        grid-template-columns: 1fr;
      }

      .quick-actions {
        flex-direction: column;
        align-items: center;
      }
    }
  `]
})
export class WikiComponent implements OnInit {
  pageTree: any[] = [];
  selectedPage: any = null;
  recentPages: WikiPage[] = [];
  popularPages: WikiPage[] = [];
  
  showSearch = false;
  searchQuery = '';
  loadingPages = false;

  // Estadísticas
  totalPages = 0;
  publishedPages = 0;
  draftPages = 0;
  totalContributors = 0;

  headerActions = [
    {
      label: 'Nueva Página',
      icon: 'pi pi-plus',
      onClick: () => this.createPage()
    },
    {
      label: 'Configuración',
      icon: 'pi pi-cog',
      severity: 'secondary' as any,
      onClick: () => this.showSettings()
    }
  ];

  constructor(private wikiService: WikiService) {}

  ngOnInit(): void {
    this.loadPages();
    this.loadStats();
    this.loadRecentPages();
    this.loadPopularPages();
  }

  private loadPages(): void {
    this.loadingPages = true;
    this.wikiService.getPages().subscribe(
      response => {
        this.buildPageTree(response.data);
        this.loadingPages = false;
      },
      error => {
        console.error('Error loading pages:', error);
        this.loadingPages = false;
      }
    );
  }

  private buildPageTree(pages: WikiPage[]): void {
    // Construir árbol jerárquico de páginas
    const pageMap = new Map<string, any>();
    const rootPages: any[] = [];

    // Crear nodos para todas las páginas
    pages.forEach(page => {
      const node = {
        key: page.id,
        label: page.title,
        data: page,
        children: [],
        expandedIcon: 'pi pi-folder-open',
        collapsedIcon: 'pi pi-folder',
        leaf: false
      };
      pageMap.set(page.id, node);
    });

    // Organizar jerarquía
    pages.forEach(page => {
      const node = pageMap.get(page.id);
      if (page.parent_id && pageMap.has(page.parent_id)) {
        pageMap.get(page.parent_id).children.push(node);
        node.leaf = true;
      } else {
        rootPages.push(node);
      }
    });

    // Marcar hojas
    rootPages.forEach(this.markLeafNodes);
    
    this.pageTree = rootPages;
  }

  private markLeafNodes(node: any): void {
    if (node.children.length === 0) {
      node.leaf = true;
      node.icon = 'pi pi-file';
    } else {
      node.children.forEach((child: any) => this.markLeafNodes(child));
    }
  }

  private loadStats(): void {
    // Cargar estadísticas de la wiki
    this.wikiService.getStats().subscribe(
      stats => {
        this.totalPages = stats.total_pages;
        this.publishedPages = stats.published_pages;
        this.draftPages = stats.draft_pages;
        this.totalContributors = stats.total_contributors;
      }
    );
  }

  private loadRecentPages(): void {
    this.wikiService.getRecentPages(5).subscribe(
      pages => {
        this.recentPages = pages;
      }
    );
  }

  private loadPopularPages(): void {
    this.wikiService.getPopularPages(6).subscribe(
      pages => {
        this.popularPages = pages;
      }
    );
  }

  onPageSelect(event: any): void {
    const page = event.node.data;
    // Navegar a la página seleccionada
    // this.router.navigate(['/wiki', page.id]);
  }

  createPage(): void {
    // Navegar a crear nueva página
    // this.router.navigate(['/wiki/new']);
  }

  showTemplates(): void {
    // Mostrar plantillas de páginas
  }

  showSettings(): void {
    // Mostrar configuración de la wiki
  }

  toggleSearch(): void {
    this.showSearch = !this.showSearch;
    if (!this.showSearch) {
      this.searchQuery = '';
      this.loadPages(); // Recargar todas las páginas
    }
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.wikiService.searchPages(this.searchQuery).subscribe(
        pages => {
          this.buildPageTree(pages);
        }
      );
    } else {
      this.loadPages();
    }
  }

  getPageIcon(page: WikiPage): string {
    if (!page.is_published) {
      return 'pi pi-file-edit';
    }
    return 'pi pi-file';
  }
}
