FROM node:23-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (including dev dependencies)
RUN npm install

# Set development environment
ENV NODE_ENV=development

# Mount the source code at runtime, so don't COPY here
# (This happens in docker-compose with volumes)

EXPOSE 5173

# Use the development script
# CMD ["npm", "run", "dev"]
CMD ["npm", "run", "dev", "--", "--host"]
