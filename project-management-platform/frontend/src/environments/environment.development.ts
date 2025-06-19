export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api/v1',
  wsUrl: 'ws://localhost:8080/api/v1/ws',
  appName: 'Plataforma de Gestión de Proyectos [DEV]',
  version: '1.0.0-dev',
  features: {
    enableChat: true,
    enableTimeTracking: true,
    enableReports: true,
    enableNotifications: true,
    enableWiki: true,
    enableDebugMode: true
  },
  storage: {
    tokenKey: 'auth_token_dev',
    refreshTokenKey: 'refresh_token_dev',
    userKey: 'current_user_dev'
  },
  pagination: {
    defaultPageSize: 10,
    pageSizeOptions: [5, 10, 20, 50]
  },
  upload: {
    maxFileSize: 5 * 1024 * 1024, // 5MB for development
    allowedImageTypes: ['image/jpeg', 'image/png', 'image/gif'],
    allowedFileTypes: ['application/pdf', 'application/msword', 'text/plain']
  }
};
