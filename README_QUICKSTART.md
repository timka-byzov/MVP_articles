# MVP Articles - Quick Start Guide

## 🚀 Быстрый запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Шаг 1: Клонирование и запуск

```bash
# Перейти в директорию проекта
cd mvp

# Запустить все сервисы
docker-compose up -d

# Подождать пока сервисы запустятся (30-60 секунд)
docker-compose logs -f backend
```

### Шаг 2: Импорт данных

```bash
# Импортировать примеры статей
docker-compose exec backend python -m app.migrations.import_articles --file /data/example_articles.json

# Вы должны увидеть:
# ✓ Successfully imported 5 articles
```

### Шаг 3: Открыть приложение

Откройте браузер и перейдите на:
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs

## 📝 Первое использование

1. **Регистрация**
   - Откройте http://localhost:3000
   - Нажмите "Зарегистрироваться"
   - Заполните форму (имя, email, пароль)

2. **Выбор тем**
   - После регистрации выберите интересующие темы
   - Например: "machine learning", "deep learning", "nlp"
   - Нажмите "Продолжить"

3. **Просмотр ленты**
   - Вы увидите персонализированную ленту статей
   - Взаимодействуйте со статьями:
     - ❤️ Лайк - статья вам нравится
     - 🔖 Сохранить - сохранить на потом
     - 👁️ Скрыть - больше не показывать

## 🔧 Полезные команды

### Управление Docker

```bash
# Остановить все сервисы
docker-compose down

# Перезапустить сервисы
docker-compose restart

# Посмотреть логи
docker-compose logs -f

# Посмотреть логи конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Работа с данными

```bash
# Импортировать свои статьи
docker-compose exec backend python -m app.migrations.import_articles --file /data/articles.json

# Очистить и импортировать заново
docker-compose exec backend python -m app.migrations.import_articles --file /data/articles.json --clean

# Подключиться к PostgreSQL
docker-compose exec postgres psql -U mvp_user -d mvp_articles
```

### Разработка

```bash
# Backend - установить зависимости локально
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend - установить зависимости локально
cd frontend
npm install
```

## 📊 Структура проекта

```
mvp/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # SQLModel модели
│   │   ├── api/         # API endpoints
│   │   ├── services/    # Бизнес-логика (TF-IDF)
│   │   └── migrations/  # Скрипты импорта
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React компоненты
│   │   └── services/    # API клиент
│   └── package.json
├── data/
│   └── example_articles.json  # Примеры статей
└── docker-compose.yml
```

## 🎯 Основные функции

### Backend (FastAPI)
- ✅ Аутентификация через FastAPI Users (cookie-based)
- ✅ CRUD операции для статей
- ✅ TF-IDF рекомендательная система
- ✅ Отслеживание взаимодействий пользователя
- ✅ Персонализация на основе предпочтений

### Frontend (React + Material-UI)
- ✅ Регистрация и вход
- ✅ Выбор интересующих тем
- ✅ Персонализированная лента
- ✅ Взаимодействие со статьями (like, save, hide)
- ✅ Адаптивный дизайн

## 🔍 API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация
- `POST /auth/cookie/login` - Вход
- `POST /auth/cookie/logout` - Выход
- `GET /users/me` - Текущий пользователь

### Лента
- `GET /api/feed` - Получить персонализированную ленту
  - Query: `limit` (default: 20), `offset` (default: 0)

### Статьи
- `GET /api/articles/{id}` - Получить статью
- `POST /api/articles/{id}/interact` - Взаимодействие
  - Body: `{"interaction_type": "like|save|hide|view"}`
- `GET /api/articles/saved/list` - Сохраненные статьи
- `GET /api/articles/liked/list` - Лайкнутые статьи

### Предпочтения
- `POST /api/preferences` - Установить предпочтения
- `GET /api/preferences` - Получить предпочтения

## 📦 Формат данных для импорта

Создайте файл `data/articles.json`:

```json
{
  "articles": [
    {
      "title": "Название статьи",
      "abstract": "Полный abstract статьи...",
      "summary": "Краткое резюме от LLM...",
      "authors": [
        {"name": "Автор 1", "affiliation": "Организация"}
      ],
      "source": "arXiv",
      "doi": "10.1234/example",
      "publication_date": "2024-01-01",
      "topics": ["topic1", "topic2"],
      "url": "https://arxiv.org/abs/..."
    }
  ]
}
```

## 🐛 Troubleshooting

### Backend не запускается

```bash
# Проверить логи
docker-compose logs backend

# Пересоздать контейнер
docker-compose up -d --force-recreate backend
```

### Frontend не подключается к API

1. Проверьте что backend запущен: http://localhost:8000/docs
2. Проверьте CORS настройки в `backend/app/config.py`
3. Убедитесь что `REACT_APP_API_URL=http://localhost:8000` в frontend

### База данных пустая

```bash
# Импортировать примеры
docker-compose exec backend python -m app.migrations.import_articles --file /data/example_articles.json
```

### Ошибка "No articles to import"

Убедитесь что файл `data/example_articles.json` существует и имеет правильный формат.

## 📚 Дополнительная документация

- [`ARCHITECTURE.md`](ARCHITECTURE.md) - Полная архитектура проекта
- [`SETUP_GUIDE.md`](SETUP_GUIDE.md) - Детальное руководство по настройке
- [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) - План реализации с примерами кода

## 🚀 Следующие шаги

1. **Добавить свои статьи**
   - Создайте JSON файл с вашими статьями
   - Импортируйте через скрипт

2. **Настроить под себя**
   - Измените темы в `TopicSelector.jsx`
   - Настройте веса в TF-IDF рекомендателе
   - Добавьте новые типы взаимодействий

3. **Деплой**
   - Backend: Railway, Render, DigitalOcean
   - Frontend: Vercel, Netlify
   - Database: Supabase, Neon

## 💡 Советы

- Чем больше взаимодействий, тем лучше рекомендации
- Периодически обновляйте предпочтения
- Используйте "скрыть" для нерелевантных статей
- Сохраняйте интересные статьи для чтения позже

## 🤝 Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker-compose logs -f`
2. Перезапустите сервисы: `docker-compose restart`
3. Очистите и пересоздайте: `docker-compose down -v && docker-compose up -d`

---

**Готово! Приложение запущено и готово к использованию! 🎉**