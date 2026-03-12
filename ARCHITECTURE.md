# MVP Architecture Plan - Персональная лента научных статей

## Общая архитектура

```mermaid
graph TB
    User[Пользователь] --> Frontend[React Frontend]
    Frontend --> API[FastAPI Backend]
    API --> Auth[FastAPI Users Auth]
    API --> DB[(PostgreSQL)]
    API --> Recommender[TF-IDF Recommender]
    Colab[Google Colab] --> JSON[articles.json]
    JSON --> Migration[DB Migration Script]
    Migration --> DB
```

## Технологический стек

### Backend
- **FastAPI** - современный, быстрый веб-фреймворк
- **SQLModel** - ORM для работы с PostgreSQL
- **FastAPI Users** - готовая система аутентификации
- **Alembic** - миграции БД
- **scikit-learn** - TF-IDF для рекомендаций
- **Pydantic** - валидация данных

### Frontend
- **React** - UI библиотека
- **Material-UI (MUI)** - готовые компоненты
- **Axios** - HTTP клиент
- **React Router** - навигация

### Infrastructure
- **PostgreSQL** - основная БД
- **Docker Compose** - оркестрация сервисов
- **Nginx** (опционально) - reverse proxy

## Структура проекта

```
mvp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI приложение
│   │   ├── config.py               # Конфигурация
│   │   ├── database.py             # Подключение к БД
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User модель
│   │   │   ├── article.py          # Article модель
│   │   │   ├── interaction.py      # UserInteraction модель
│   │   │   └── preference.py       # UserPreference модель
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # Pydantic схемы для User
│   │   │   ├── article.py          # Pydantic схемы для Article
│   │   │   └── feed.py             # Схемы для ленты
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Эндпоинты аутентификации
│   │   │   ├── feed.py             # Эндпоинты ленты
│   │   │   ├── articles.py         # Эндпоинты статей
│   │   │   └── preferences.py      # Эндпоинты предпочтений
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── recommender.py      # TF-IDF рекомендации
│   │   │   └── user_profile.py     # Профиль пользователя
│   │   └── migrations/
│   │       └── import_articles.py  # Импорт из JSON
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/                    # Alembic миграции
│       ├── env.py
│       └── versions/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── Feed/
│   │   │   │   ├── ArticleCard.jsx
│   │   │   │   ├── FeedList.jsx
│   │   │   │   └── ArticleActions.jsx
│   │   │   ├── Onboarding/
│   │   │   │   └── TopicSelector.jsx
│   │   │   └── Layout/
│   │   │       ├── Header.jsx
│   │   │       └── Navigation.jsx
│   │   ├── services/
│   │   │   └── api.js              # API клиент
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── Dockerfile
├── data/
│   ├── articles.json               # Данные из Colab
│   └── example_article.json        # Пример структуры
├── docker-compose.yml
└── README_SETUP.md
```

## База данных

### Схема БД

```mermaid
erDiagram
    User ||--o{ UserInteraction : has
    User ||--o{ UserPreference : has
    Article ||--o{ UserInteraction : receives
    
    User {
        uuid id PK
        string email UK
        string hashed_password
        string full_name
        boolean is_active
        boolean is_verified
        datetime created_at
    }
    
    Article {
        uuid id PK
        string title
        text abstract
        text summary
        json authors
        string source
        string doi
        date publication_date
        text tfidf_vector
        datetime created_at
    }
    
    UserInteraction {
        uuid id PK
        uuid user_id FK
        uuid article_id FK
        string interaction_type
        datetime created_at
    }
    
    UserPreference {
        uuid id PK
        uuid user_id FK
        string topic
        float weight
        datetime created_at
    }
```

### Модели SQLModel

**User** (через FastAPI Users):
- id: UUID
- email: str (unique)
- hashed_password: str
- full_name: str
- is_active: bool
- is_verified: bool
- created_at: datetime

**Article**:
- id: UUID
- title: str
- abstract: text
- summary: text (из LLM)
- authors: JSON (список авторов)
- source: str (arXiv, PubMed, etc.)
- doi: str (optional)
- publication_date: date
- tfidf_vector: text (сериализованный numpy array)
- created_at: datetime

**UserInteraction**:
- id: UUID
- user_id: UUID (FK)
- article_id: UUID (FK)
- interaction_type: enum ('view', 'like', 'save', 'hide')
- created_at: datetime

**UserPreference**:
- id: UUID
- user_id: UUID (FK)
- topic: str
- weight: float (0.0 - 1.0)
- created_at: datetime

## Формат JSON данных из Google Colab

```json
{
  "articles": [
    {
      "title": "Deep Learning for Natural Language Processing",
      "abstract": "This paper presents a comprehensive survey...",
      "summary": "Краткое резюме статьи, сгенерированное LLM...",
      "authors": [
        {"name": "John Doe", "affiliation": "MIT"},
        {"name": "Jane Smith", "affiliation": "Stanford"}
      ],
      "source": "arXiv",
      "doi": "10.1234/arxiv.2024.12345",
      "publication_date": "2024-03-15",
      "topics": ["machine learning", "nlp", "deep learning"],
      "embedding": [0.123, 0.456, 0.789, ...]
    }
  ]
}
```

## API Endpoints

### Аутентификация (FastAPI Users)
- `POST /auth/register` - регистрация
- `POST /auth/login` - вход (устанавливает cookie)
- `POST /auth/logout` - выход
- `GET /auth/me` - текущий пользователь

### Предпочтения
- `POST /api/preferences` - установить начальные темы
- `GET /api/preferences` - получить предпочтения
- `PUT /api/preferences` - обновить предпочтения

### Лента
- `GET /api/feed` - получить персонализированную ленту
  - Query params: `limit`, `offset`, `topics` (optional filter)
- `GET /api/feed/recommendations` - рекомендации на основе TF-IDF

### Статьи
- `GET /api/articles/{article_id}` - получить статью
- `POST /api/articles/{article_id}/interact` - взаимодействие
  - Body: `{"interaction_type": "like|save|hide|view"}`
- `GET /api/articles/saved` - сохраненные статьи
- `GET /api/articles/liked` - лайкнутые статьи

## Система рекомендаций (TF-IDF)

### Алгоритм

1. **Инициализация**:
   - При импорте статей вычисляем TF-IDF векторы для всех abstracts
   - Сохраняем векторы в БД

2. **Построение профиля пользователя**:
   - Собираем все статьи с положительными взаимодействиями (like, save, view)
   - Усредняем их TF-IDF векторы с весами:
     - like: 1.0
     - save: 0.8
     - view: 0.3
   - Учитываем выбранные темы (UserPreference)

3. **Генерация ленты**:
   - Вычисляем косинусное сходство между профилем пользователя и всеми статьями
   - Исключаем уже просмотренные/скрытые статьи
   - Сортируем по релевантности
   - Добавляем элемент случайности (exploration) - 10% случайных статей

4. **Обновление профиля**:
   - После каждого взаимодействия пересчитываем профиль
   - Постепенно снижаем вес старых взаимодействий (time decay)

### Реализация

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TFIDFRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def fit_articles(self, articles):
        # Обучаем на всех abstracts
        texts = [a.abstract for a in articles]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
    
    def get_user_profile(self, user_interactions, user_preferences):
        # Строим профиль из взаимодействий
        weighted_vectors = []
        for interaction in user_interactions:
            weight = self._get_interaction_weight(interaction.type)
            vector = self._get_article_vector(interaction.article_id)
            weighted_vectors.append(vector * weight)
        
        # Добавляем веса из предпочтений
        for pref in user_preferences:
            topic_vector = self._get_topic_vector(pref.topic)
            weighted_vectors.append(topic_vector * pref.weight)
        
        return np.mean(weighted_vectors, axis=0)
    
    def recommend(self, user_profile, n=20, exclude_ids=None):
        # Вычисляем сходство
        similarities = cosine_similarity(user_profile, self.tfidf_matrix)
        
        # Сортируем и фильтруем
        top_indices = similarities.argsort()[::-1]
        
        # Добавляем exploration (10% случайных)
        n_explore = int(n * 0.1)
        n_exploit = n - n_explore
        
        recommendations = top_indices[:n_exploit]
        random_indices = np.random.choice(len(self.tfidf_matrix), n_explore)
        
        return np.concatenate([recommendations, random_indices])
```

## Аутентификация (FastAPI Users)

### Конфигурация

```python
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

# Cookie transport
cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600 * 24 * 7,  # 7 дней
    cookie_secure=False,  # True в production
    cookie_httponly=True,
    cookie_samesite="lax"
)

# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600 * 24 * 7)

# Authentication Backend
auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
```

## Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: mvp_user
      POSTGRES_PASSWORD: mvp_password
      POSTGRES_DB: mvp_articles
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mvp_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./data:/data
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://mvp_user:mvp_password@postgres:5432/mvp_articles
      SECRET_KEY: your-secret-key-change-in-production
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build: ./frontend
    command: npm start
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Миграция данных

### Скрипт импорта articles.json

```python
import json
import asyncio
from sqlmodel import Session, select
from app.database import engine
from app.models.article import Article
from app.services.recommender import TFIDFRecommender

async def import_articles(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = []
    for item in data['articles']:
        article = Article(
            title=item['title'],
            abstract=item['abstract'],
            summary=item['summary'],
            authors=item['authors'],
            source=item['source'],
            doi=item.get('doi'),
            publication_date=item['publication_date'],
        )
        articles.append(article)
    
    # Вычисляем TF-IDF векторы
    recommender = TFIDFRecommender()
    recommender.fit_articles(articles)
    
    # Сохраняем в БД
    with Session(engine) as session:
        for i, article in enumerate(articles):
            article.tfidf_vector = recommender.get_vector_string(i)
            session.add(article)
        session.commit()
    
    print(f"Imported {len(articles)} articles")

if __name__ == "__main__":
    asyncio.run(import_articles("/data/articles.json"))
```

## Frontend компоненты

### ArticleCard.jsx

```jsx
import React from 'react';
import { Card, CardContent, CardActions, Typography, IconButton, Chip } from '@mui/material';
import { Favorite, BookmarkAdd, VisibilityOff } from '@mui/icons-material';

function ArticleCard({ article, onInteract }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {article.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {article.summary}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {article.authors.map(a => a.name).join(', ')} • {article.publication_date}
        </Typography>
        <div style={{ marginTop: 8 }}>
          {article.topics?.map(topic => (
            <Chip key={topic} label={topic} size="small" sx={{ mr: 0.5 }} />
          ))}
        </div>
      </CardContent>
      <CardActions>
        <IconButton onClick={() => onInteract(article.id, 'like')}>
          <Favorite />
        </IconButton>
        <IconButton onClick={() => onInteract(article.id, 'save')}>
          <BookmarkAdd />
        </IconButton>
        <IconButton onClick={() => onInteract(article.id, 'hide')}>
          <VisibilityOff />
        </IconButton>
      </CardActions>
    </Card>
  );
}

export default ArticleCard;
```

## Deployment план

1. **Локальная разработка**:
   ```bash
   docker-compose up -d
   # Backend: http://localhost:8000
   # Frontend: http://localhost:3000
   # API Docs: http://localhost:8000/docs
   ```

2. **Импорт данных**:
   ```bash
   docker-compose exec backend python -m app.migrations.import_articles
   ```

3. **Production deployment** (будущее):
   - Backend: Railway, Render, или DigitalOcean
   - Frontend: Vercel, Netlify
   - Database: Managed PostgreSQL (Supabase, Neon)

## Приоритеты для MVP

### Must Have (критично для демо)
1. ✅ Регистрация и вход пользователя
2. ✅ Выбор начальных тем при онбординге
3. ✅ Отображение ленты статей
4. ✅ Базовые взаимодействия (like, save, hide)
5. ✅ TF-IDF рекомендации
6. ✅ Импорт данных из JSON

### Nice to Have (можно добавить позже)
- Поиск по статьям
- Фильтры по дате/источнику
- Профиль пользователя
- Статистика взаимодействий
- Email верификация
- Экспорт сохраненных статей

### Won't Have (не для MVP)
- Collaborative filtering
- Real-time обновления
- Мобильное приложение
- Интеграция с внешними API
- Локальный инференс LLM

## Оценка времени разработки

- Backend setup + models: 2-3 часа
- FastAPI Users integration: 1-2 часа
- TF-IDF recommender: 2-3 часа
- API endpoints: 2-3 часа
- Frontend setup + components: 3-4 часа
- Integration + testing: 2-3 часа
- Docker setup: 1-2 часа
- Documentation: 1 час

**Итого: 14-21 час чистого времени разработки**

## Следующие шаги

1. Создать структуру проекта
2. Настроить Docker Compose
3. Реализовать backend с FastAPI Users
4. Создать frontend с React + MUI
5. Интегрировать TF-IDF рекомендации
6. Подготовить пример JSON и скрипт импорта
7. Протестировать полный flow
8. Задеплоить демо

Готов переходить к реализации?