#!/usr/bin/env python3
"""
Script para crear proyecto Angular manualmente con PrimeNG
"""

import os
import json
import subprocess

def create_angular_project_structure():
    """Crear estructura manual del proyecto Angular"""
    
    frontend_dir = "/workspace/project-management-platform/frontend"
    
    # Crear estructura de directorios Angular
    directories = [
        "src",
        "src/app",
        "src/app/core",
        "src/app/core/auth",
        "src/app/core/guards",
        "src/app/core/interceptors",
        "src/app/core/services",
        "src/app/shared",
        "src/app/shared/components",
        "src/app/shared/pipes",
        "src/app/shared/directives",
        "src/app/features",
        "src/app/features/dashboard",
        "src/app/features/projects",
        "src/app/features/tasks",
        "src/app/features/kanban",
        "src/app/features/gantt",
        "src/app/features/reports",
        "src/app/features/chat",
        "src/app/features/admin",
        "src/assets",
        "src/assets/images",
        "src/assets/icons",
        "src/environments",
    ]
    
    for directory in directories:
        dir_path = os.path.join(frontend_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
    
    # package.json
    package_json = {
        "name": "project-management-frontend",
        "version": "1.0.0",
        "scripts": {
            "ng": "ng",
            "start": "ng serve --host 0.0.0.0 --port 4200",
            "build": "ng build",
            "build:prod": "ng build --configuration production",
            "watch": "ng build --watch --configuration development",
            "test": "ng test",
            "test:ci": "ng test --watch=false --browsers=ChromeHeadless",
            "lint": "ng lint",
            "e2e": "ng e2e"
        },
        "dependencies": {
            "@angular/animations": "^17.3.0",
            "@angular/cdk": "^17.3.0",
            "@angular/common": "^17.3.0",
            "@angular/compiler": "^17.3.0",
            "@angular/core": "^17.3.0",
            "@angular/forms": "^17.3.0",
            "@angular/platform-browser": "^17.3.0",
            "@angular/platform-browser-dynamic": "^17.3.0",
            "@angular/router": "^17.3.0",
            "chart.js": "^4.4.0",
            "ngx-socket-io": "^4.7.0",
            "primeicons": "^7.0.0",
            "primeng": "^17.18.0",
            "rxjs": "~7.8.0",
            "socket.io-client": "^4.7.2",
            "tslib": "^2.3.0",
            "zone.js": "~0.14.0"
        },
        "devDependencies": {
            "@angular-devkit/build-angular": "^17.3.0",
            "@angular/cli": "^17.3.0",
            "@angular/compiler-cli": "^17.3.0",
            "@types/jasmine": "~5.1.0",
            "@types/chart.js": "^2.9.41",
            "@types/socket.io-client": "^3.0.0",
            "jasmine-core": "~5.1.0",
            "karma": "~6.4.0",
            "karma-chrome-headless": "~3.1.0",
            "karma-coverage": "~2.2.0",
            "karma-jasmine": "~5.1.0",
            "karma-jasmine-html-reporter": "~2.1.0",
            "typescript": "~5.4.0"
        }
    }
    
    with open(os.path.join(frontend_dir, "package.json"), "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)
    
    # angular.json
    angular_json = {
        "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
        "version": 1,
        "newProjectRoot": "projects",
        "projects": {
            "project-management-app": {
                "projectType": "application",
                "schematics": {
                    "@schematics/angular:component": {
                        "style": "scss"
                    }
                },
                "root": "",
                "sourceRoot": "src",
                "prefix": "app",
                "architect": {
                    "build": {
                        "builder": "@angular-devkit/build-angular:browser",
                        "options": {
                            "outputPath": "dist/project-management-app",
                            "index": "src/index.html",
                            "main": "src/main.ts",
                            "polyfills": [
                                "zone.js"
                            ],
                            "tsConfig": "tsconfig.app.json",
                            "inlineStyleLanguage": "scss",
                            "assets": [
                                "src/favicon.ico",
                                "src/assets"
                            ],
                            "styles": [
                                "src/styles.scss",
                                "node_modules/primeng/resources/themes/lara-light-blue/theme.css",
                                "node_modules/primeng/resources/primeng.min.css",
                                "node_modules/primeicons/primeicons.css"
                            ],
                            "scripts": []
                        },
                        "configurations": {
                            "production": {
                                "budgets": [
                                    {
                                        "type": "initial",
                                        "maximumWarning": "500kb",
                                        "maximumError": "1mb"
                                    },
                                    {
                                        "type": "anyComponentStyle",
                                        "maximumWarning": "2kb",
                                        "maximumError": "4kb"
                                    }
                                ],
                                "outputHashing": "all"
                            },
                            "development": {
                                "buildOptimizer": False,
                                "optimization": False,
                                "vendorChunk": True,
                                "extractLicenses": False,
                                "sourceMap": True,
                                "namedChunks": True
                            }
                        },
                        "defaultConfiguration": "production"
                    },
                    "serve": {
                        "builder": "@angular-devkit/build-angular:dev-server",
                        "configurations": {
                            "production": {
                                "buildTarget": "project-management-app:build:production"
                            },
                            "development": {
                                "buildTarget": "project-management-app:build:development"
                            }
                        },
                        "defaultConfiguration": "development"
                    },
                    "extract-i18n": {
                        "builder": "@angular-devkit/build-angular:extract-i18n",
                        "options": {
                            "buildTarget": "project-management-app:build"
                        }
                    },
                    "test": {
                        "builder": "@angular-devkit/build-angular:karma",
                        "options": {
                            "polyfills": [
                                "zone.js",
                                "zone.js/testing"
                            ],
                            "tsConfig": "tsconfig.spec.json",
                            "inlineStyleLanguage": "scss",
                            "assets": [
                                "src/favicon.ico",
                                "src/assets"
                            ],
                            "styles": [
                                "src/styles.scss"
                            ],
                            "scripts": []
                        }
                    }
                }
            }
        },
        "cli": {
            "analytics": False
        }
    }
    
    with open(os.path.join(frontend_dir, "angular.json"), "w", encoding="utf-8") as f:
        json.dump(angular_json, f, indent=2)
    
    # tsconfig.json
    tsconfig_json = {
        "compileOnSave": False,
        "compilerOptions": {
            "baseUrl": "./",
            "outDir": "./dist/out-tsc",
            "forceConsistentCasingInFileNames": True,
            "strict": True,
            "noImplicitOverride": True,
            "noPropertyAccessFromIndexSignature": True,
            "noImplicitReturns": True,
            "noFallthroughCasesInSwitch": True,
            "sourceMap": True,
            "declaration": False,
            "downlevelIteration": True,
            "experimentalDecorators": True,
            "moduleResolution": "node",
            "importHelpers": True,
            "target": "ES2022",
            "module": "ES2022",
            "useDefineForClassFields": False,
            "lib": [
                "ES2022",
                "dom"
            ],
            "paths": {
                "@core/*": ["src/app/core/*"],
                "@shared/*": ["src/app/shared/*"],
                "@features/*": ["src/app/features/*"],
                "@environments/*": ["src/environments/*"]
            }
        },
        "angularCompilerOptions": {
            "enableI18nLegacyMessageIdFormat": False,
            "strictInjectionParameters": True,
            "strictInputAccessModifiers": True,
            "strictTemplates": True
        }
    }
    
    with open(os.path.join(frontend_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
        json.dump(tsconfig_json, f, indent=2)
    
    # tsconfig.app.json
    tsconfig_app_json = {
        "extends": "./tsconfig.json",
        "compilerOptions": {
            "outDir": "./out-tsc/app",
            "types": []
        },
        "files": [
            "src/main.ts"
        ],
        "include": [
            "src/**/*.d.ts"
        ]
    }
    
    with open(os.path.join(frontend_dir, "tsconfig.app.json"), "w", encoding="utf-8") as f:
        json.dump(tsconfig_app_json, f, indent=2)
    
    # src/main.ts
    main_ts_content = """import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
"""
    
    with open(os.path.join(frontend_dir, "src", "main.ts"), "w", encoding="utf-8") as f:
        f.write(main_ts_content)
    
    # src/index.html
    index_html_content = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Plataforma de Gestión de Proyectos</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>
"""
    
    with open(os.path.join(frontend_dir, "src", "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html_content)
    
    # src/styles.scss
    styles_scss_content = """/* Estilos globales de la aplicación */
@import 'primeng/resources/themes/lara-light-blue/theme.css';
@import 'primeng/resources/primeng.min.css';
@import 'primeicons/primeicons.css';

/* Variables CSS personalizadas */
:root {
  --primary-color: #2196F3;
  --secondary-color: #FF5722;
  --surface-color: #ffffff;
  --text-color: #333333;
  --border-color: #e0e0e0;
}

/* Reset y estilos base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: #f5f5f5;
}

/* Utilidades */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-5 { margin-top: 3rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.mb-5 { margin-bottom: 3rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 1rem; }
.p-4 { padding: 1.5rem; }
.p-5 { padding: 3rem; }

/* Componentes personalizados */
.card {
  background: var(--surface-color);
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem;
  margin-bottom: 1rem;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.btn-secondary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}

/* Layout principal */
.main-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: var(--surface-color);
  border-right: 1px solid var(--border-color);
}

.content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
}

@media (max-width: 576px) {
  .main-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
  }
}
"""
    
    with open(os.path.join(frontend_dir, "src", "styles.scss"), "w", encoding="utf-8") as f:
        f.write(styles_scss_content)
    
    # src/app/app.component.ts
    app_component_ts_content = """import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, ButtonModule, CardModule],
  template: `
    <div class="main-layout">
      <nav class="sidebar">
        <h2>PM Platform</h2>
        <p>Navegación aquí</p>
      </nav>
      <main class="content">
        <p-card header="Bienvenido a la Plataforma de Gestión de Proyectos">
          <p>Esta es la aplicación principal del sistema.</p>
          <p-button label="Comenzar" icon="pi pi-check"></p-button>
        </p-card>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: []
})
export class AppComponent {
  title = 'project-management-app';
}
"""
    
    with open(os.path.join(frontend_dir, "src/app", "app.component.ts"), "w", encoding="utf-8") as f:
        f.write(app_component_ts_content)
    
    # src/app/app.config.ts
    app_config_ts_content = """import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideAnimations(),
    provideHttpClient(withInterceptorsFromDi()),
  ]
};
"""
    
    with open(os.path.join(frontend_dir, "src/app", "app.config.ts"), "w", encoding="utf-8") as f:
        f.write(app_config_ts_content)
    
    # src/app/app.routes.ts
    app_routes_ts_content = """import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  // Las rutas se agregarán aquí conforme se desarrollen los módulos
];
"""
    
    with open(os.path.join(frontend_dir, "src/app", "app.routes.ts"), "w", encoding="utf-8") as f:
        f.write(app_routes_ts_content)
    
    # environments
    env_dev_content = """export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api',
  wsUrl: 'ws://localhost:8080/ws',
};
"""
    
    with open(os.path.join(frontend_dir, "src/environments", "environment.development.ts"), "w", encoding="utf-8") as f:
        f.write(env_dev_content)
    
    env_prod_content = """export const environment = {
  production: true,
  apiUrl: '/api',
  wsUrl: '/ws',
};
"""
    
    with open(os.path.join(frontend_dir, "src/environments", "environment.ts"), "w", encoding="utf-8") as f:
        f.write(env_prod_content)
    
    print("✓ Estructura del proyecto Angular creada manualmente")
    return True

if __name__ == "__main__":
    create_angular_project_structure()
