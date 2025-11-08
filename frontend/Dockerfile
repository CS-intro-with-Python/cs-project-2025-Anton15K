# syntax=docker/dockerfile:1.5

FROM node:20-alpine AS build

WORKDIR /app
COPY package.json pnpm-lock.yaml* package-lock.json* yarn.lock* ./

RUN if [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install; \
    elif [ -f yarn.lock ]; then corepack enable && yarn install; \
    else npm install; fi

COPY . .

RUN if [ -f pnpm-lock.yaml ]; then pnpm run build; \
    elif [ -f yarn.lock ]; then yarn build; \
    else npm run build; fi

FROM nginx:1.27-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
