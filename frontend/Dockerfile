# Stage 1: Build React app
FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built files to nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# Copy optional custom nginx config
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5173  
CMD ["nginx", "-g", "daemon off;"]
