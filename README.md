# MVP - Персональная лента научных статей

Веб-приложение для персонализированной ленты научных статей с рекомендациями на основе TF-IDF и предпочтений пользователя.

## 🚀 Быстрый старт

```bash
# 1. Запустить все сервисы
docker-compose up -d

# 2. Импортировать примеры статей
docker-compose exec backend python -m app.migrations.import_articles --file /data/example_articles.json

# 3. Открыть приложение
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**Готово!** Зарегистрируйтесь, выберите темы и начните пользоваться лентой.

## 📋 Что реализовано

### Backend (FastAPI)
- ✅ **Аутентификация** - FastAPI Users с cookie-based JWT
- ✅ **База данных** - PostgreSQL + SQLModel
- ✅ **Рекомендации** - TF-IDF алгоритм для персонализации
- ✅ **API** - RESTful endpoints для всех операций
- ✅ **Импорт данных** - Скрипт для загрузки статей из JSON

### Frontend (React + Material-UI)
- ✅ **Регистрация и вход** - Полный auth flow
- ✅ **Онбординг** - Выбор интересующих тем
- ✅ **Лента статей** - Персонализированная выдача
- ✅ **Взаимодействия** - Like, Save, Hide
- ✅ **Адаптивный дизайн** - Material-UI компоненты

### Инфраструктура
- ✅ **Docker Compose** - Все сервисы в контейнерах
- ✅ **PostgreSQL** - Надежная БД с персистентностью
- ✅ **Hot Reload** - Автоматическая перезагрузка при разработке

## 🏗️ Архитектура

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   React     │─────▶│   FastAPI    │─────▶│ PostgreSQL │
│  Frontend   │      │   Backend    │      │  Database  │
│  (port 3000)│◀─────│  (port 8000) │◀─────│ (port 5432)│
└─────────────┘      └──────────────┘      └────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  TF-IDF      │
                     │  Recommender │
                     └──────────────┘
```

## 📁 Структура проекта

```
mvp/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── models/         # SQLModel модели (User, Article, etc.)
│   │   ├── api/            # API endpoints (auth, feed, articles)
│   │   ├── services/       # Бизнес-логика (TF-IDF рекомендатель)
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── migrations/     # Скрипты импорта данных
│   │   ├── config.py       # Конфигурация
│   │   ├── database.py     # Подключение к БД
│   │   └── main.py         # Главный файл приложения
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React приложение
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   │   ├── Auth/      # Login, Register
│   │   │   ├── Feed/      # ArticleCard, FeedList
│   │   │   ├── Onboarding/# TopicSelector
│   │   │   └── Layout/    # Header
│   │   ├── services/      # API клиент (axios)
│   │   ├── App.jsx        # Главный компонент
│   │   └── index.jsx      # Entry point
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── data/
│   └── example_articles.json  # Примеры статей
├── docker-compose.yml      # Оркестрация сервисов
├── README.md              # Этот файл
├── README_QUICKSTART.md   # Быстрый старт
├── ARCHITECTURE.md        # Детальная архитектура
├── SETUP_GUIDE.md         # Руководство по настройке
└── IMPLEMENTATION_PLAN.md # План реализации
```

## 🔧 Технологии

### Backend
- **FastAPI** 0.109.0 - Современный веб-фреймворк
- **SQLModel** 0.0.14 - ORM с Pydantic интеграцией
- **FastAPI Users** 12.1.3 - Готовая аутентификация
- **PostgreSQL** 15 - Реляционная БД
- **scikit-learn** 1.4.0 - TF-IDF для рекомендаций
- **Pydantic** 2.5.3 - Валидация данных

### Frontend
- **React** 18.2.0 - UI библиотека
- **Material-UI** 5.15.0 - Компоненты дизайна
- **Axios** 1.6.5 - HTTP клиент
- **React Router** 6.21.3 - Навигация

### Infrastructure
- **Docker** & **Docker Compose** - Контейнеризация
- **Nginx** (опционально) - Reverse proxy

## 📖 Документация

- **[README_QUICKSTART.md](README_QUICKSTART.md)** - Быстрый старт и основные команды
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Полная архитектура системы
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Детальное руководство по настройке
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - План реализации с примерами кода

## 🎯 Основные функции

### Для пользователя
1. **Регистрация** - Создание аккаунта с email и паролем
2. **Выбор тем** - Указание интересующих областей науки
3. **Персональная лента** - Статьи подобранные под ваши интересы
4. **Взаимодействия**:
   - ❤️ **Like** - Отметить понравившуюся статью
   - 🔖 **Save** - Сохранить для чтения позже
   - 👁️ **Hide** - Скрыть нерелевантную статью
5. **Адаптация** - Система учится на ваших действиях

### Рекомендательная система
- **TF-IDF векторизация** - Анализ текста статей
- **Профиль пользователя** - На основе взаимодействий и предпочтений
- **Косинусное сходство** - Поиск релевантных статей
- **Exploration/Exploitation** - Баланс между известным и новым (90/10)

## 🔌 API Endpoints

### Аутентификация
```
POST   /auth/register          # Регистрация
POST   /auth/cookie/login      # Вход
POST   /auth/cookie/logout     # Выход
GET    /users/me               # Текущий пользователь
```

### Лента
```
GET    /api/feed               # Персонализированная лента
  ?limit=20&offset=0
```

### Статьи
```
GET    /api/articles/{id}              # Получить статью
POST   /api/articles/{id}/interact     # Взаимодействие
GET    /api/articles/saved/list        # Сохраненные
GET    /api/articles/liked/list        # Лайкнутые
```

### Предпочтения
```
POST   /api/preferences        # Установить темы
GET    /api/preferences        # Получить темы
```

## 📦 Формат данных

Для импорта статей создайте JSON файл:

```json
{
  "articles": [
    {
      "title": "Название статьи",
      "abstract": "Полный abstract...",
      "summary": "Краткое резюме от LLM...",
      "authors": [
        {"name": "Автор", "affiliation": "Организация"}
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

Затем импортируйте:
```bash
docker-compose exec backend python -m app.migrations.import_articles --file /data/your_articles.json
```

## 🚀 Deployment

### Development
```bash
docker-compose up -d
```

### Production

**Backend:**
- Railway, Render, DigitalOcean App Platform
- Используйте managed PostgreSQL (Supabase, Neon)
- Установите `cookie_secure=True`

**Frontend:**
- Vercel, Netlify, Cloudflare Pages
- Настройте `REACT_APP_API_URL` на production backend

**Environment Variables:**
```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://yourdomain.com

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
```

## 🐛 Troubleshooting

### Проблема: Backend не запускается
```bash
docker-compose logs backend
docker-compose up -d --force-recreate backend
```

### Проблема: Нет статей в ленте
```bash
# Импортировать примеры
docker-compose exec backend python -m app.migrations.import_articles --file /data/example_articles.json
```

### Проблема: Frontend не подключается
1. Проверьте backend: http://localhost:8000/docs
2. Проверьте CORS в `backend/app/config.py`
3. Убедитесь что `REACT_APP_API_URL` правильный

## 📈 Следующие шаги

### Улучшения MVP
- [ ] Поиск по статьям
- [ ] Фильтры (дата, источник, сложность)
- [ ] Email дайджесты
- [ ] Экспорт в PDF/BibTeX
- [ ] Комментарии и обсуждения

### Улучшение рекомендаций
- [ ] Использовать эмбеддинги из LLM вместо TF-IDF
- [ ] Collaborative filtering
- [ ] A/B тестирование алгоритмов
- [ ] Учет времени взаимодействия

### Интеграции
- [ ] arXiv API для новых статей
- [ ] Semantic Scholar API
- [ ] PubMed API
- [ ] Google Scholar (scraping)

### Масштабирование
- [ ] Redis для кэширования
- [ ] Celery для фоновых задач
- [ ] CDN для статики
- [ ] Векторная БД (Pinecone, Weaviate)

## 🤝 Contributing

Проект создан как MVP для быстрого прототипирования. Вклад приветствуется!

## 📄 License

MIT License - используйте свободно для своих проектов.

## 🎓 Использование

Этот проект создан для:
- Изучения современного стека (FastAPI + React)
- Прототипирования рекомендательных систем
- Демонстрации full-stack разработки
- Базы для более сложных проектов

---

**Создано с фокусом на простоту, скорость и работоспособность** 🚀
