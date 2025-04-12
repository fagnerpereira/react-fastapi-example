FROM node:23-alpine AS builder

# WORKDIR /app

# # Copy package files
# COPY package.json package-lock.json* ./

# # Install dependencies (including dev dependencies)
# RUN npm install

# # Set development environment
# ENV NODE_ENV=development

# # Mount the source code at runtime, so don't COPY here
# # (This happens in docker-compose with volumes)

# EXPOSE 5173

# # Use the development script
# # CMD ["npm", "run", "dev"]
# CMD ["npm", "run", "dev", "--", "--host"]
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code
COPY . .

# Build the application for production
ENV NODE_ENV=production
RUN npm run build

# Runtime stage - using nginx to serve static files
FROM nginx:alpine

# Copy built assets to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config that handles SPA routing
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
