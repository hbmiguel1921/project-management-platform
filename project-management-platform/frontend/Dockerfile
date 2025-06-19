FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de package
COPY package*.json ./
RUN npm ci

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build:prod

# Imagen final con Nginx
FROM nginx:alpine

# Copiar archivos construidos
COPY --from=builder /app/dist/project-management-app /usr/share/nginx/html

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
