export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api/v1',
  wsUrl: 'ws://localhost:8080/api/v1/ws',
  appName: 'Plataforma de Gestión de Proyectos',
  version: '1.0.0',
  features: {
    enableChat: true,
    enableTimeTracking: true,
    enableReports: true,
    enableNotifications: true,
    enableWiki: true
  },
  storage: {
    tokenKey: 'auth_token',
    refreshTokenKey: 'refresh_token',
    userKey: 'current_user'
  },
  pagination: {
    defaultPageSize: 20,
    pageSizeOptions: [10, 20, 50, 100]
  },
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedImageTypes: ['image/jpeg', 'image/png', 'image/gif'],
    allowedFileTypes: ['application/pdf', 'application/msword', 'text/plain']
  }
};
