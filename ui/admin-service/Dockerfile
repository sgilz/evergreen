# etapa de compilación
FROM node:14-alpine as build-stage
WORKDIR /app
ENV VITE_API_URL=http://localhost:5000 VITE_LOGIN_APP=http://localhost:3000
COPY package*.json yarn.lock ./
RUN yarn
COPY . .
RUN yarn build

# etapa de producción
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]