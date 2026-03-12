FROM node:18-alpine

WORKDIR /app

# Копирование package files
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование кода приложения
COPY . .

EXPOSE 3000

CMD ["npm", "start"]