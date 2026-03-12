
# Implementation Plan - MVP Персональная лента научных статей

## Обзор плана

Этот документ содержит детальный план реализации MVP с оценками времени и приоритетами. План разбит на фазы для последовательной разработки.

## Фаза 1: Инфраструктура и настройка (3-4 часа)

### 1.1 Структура проекта (30 мин)

Создать базовую структуру директорий:

```
mvp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   └── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── data/
│   └── articles.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

### 1.2 Docker Compose (1 час)

**Файл: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: mvp_postgres
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
    networks:
      - mvp_network

  backend:
    build: ./backend
    container_name: mvp_backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./data:/data
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://mvp_user:mvp_password@postgres:5432/mvp_articles
      SECRET_KEY: dev-secret-key-change-in-production-min-32-chars
      CORS_ORIGINS: http://localhost:3000
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - mvp_network

  frontend:
    build: ./frontend
    container_name: mvp_frontend
    command: npm start
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
      CHOKIDAR_USEPOLLING: "true"
    depends_on:
      - backend
    networks:
      - mvp_network

volumes:
  postgres_data:

networks:
  mvp_network:
    driver: bridge
```

### 1.3 Backend Dockerfile (30 мин)

**Файл: `backend/Dockerfile`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директории для данных
RUN mkdir -p /data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.4 Frontend Dockerfile (30 мин)

**Файл: `frontend/Dockerfile`**

```dockerfile
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
```

### 1.5 Backend requirements.txt (30 мин)

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
alembic==1.13.1
fastapi-users[sqlalchemy]==12.1.3
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
scikit-learn==1.4.0
numpy==1.26.3
pandas==2.2.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

### 1.6 Frontend package.json (30 мин)

```json
{
  "name": "mvp-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@emotion/react": "^11.11.3",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.5",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

## Фаза 2: Backend - Модели и БД (3-4 часа)

### 2.1 Конфигурация (30 мин)

**Файл: `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2.2 Database setup (30 мин)

**Файл: `backend/app/database.py`**

```python
from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### 2.3 User Model (1 час)

**Файл: `backend/app/models/user.py`**

```python
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLAlchemyBaseUserTableUUID, SQLModel, table=True):
    __tablename__ = "user"
    
    full_name: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2.4 Article Model (1 час)

**Файл: `backend/app/models/article.py`**

```python
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime, date
from uuid import UUID, uuid4
from typing import Optional

class Article(SQLModel, table=True):
    __tablename__ = "article"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    abstract: str
    summary: str
    authors: dict = Field(sa_column=Column(JSON))
    source: str = Field(index=True)
    doi: Optional[str] = None
    publication_date: date
    topics: list[str] = Field(default=[], sa_column=Column(JSON))
    url: Optional[str] = None
    tfidf_vector: Optional[str] = None  # Сериализованный numpy array
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2.5 UserInteraction Model (30 мин)

**Файл: `backend/app/models/interaction.py`**

```python
from sqlmodel import SQLModel, Field, Enum
from datetime import datetime
from uuid import UUID, uuid4
import enum

class InteractionType(str, enum.Enum):
    VIEW = "view"
    LIKE = "like"
    SAVE = "save"
    HIDE = "hide"

class UserInteraction(SQLModel, table=True):
    __tablename__ = "userinteraction"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    article_id: UUID = Field(foreign_key="article.id", index=True)
    interaction_type: InteractionType
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

### 2.6 UserPreference Model (30 мин)

**Файл: `backend/app/models/preference.py`**

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class UserPreference(SQLModel, table=True):
    __tablename__ = "userpreference"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    topic: str = Field(index=True)
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Фаза 3: Backend - Аутентификация (2-3 часа)

### 3.1 FastAPI Users setup (1.5 часа)

**Файл: `backend/app/api/auth.py`**

```python
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from app.models.user import User
from app.config import settings
from uuid import UUID

# Cookie transport
cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600 * 24 * 7,
    cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="lax"
)

# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600 * 24 * 7)

# Auth backend
auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

# Current user dependency
current_active_user = fastapi_users.current_user(active=True)

# Router
auth_router = APIRouter()
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
```

### 3.2 Pydantic Schemas (1 час)

**Файл: `backend/app/schemas/user.py`**

```python
from fastapi_users import schemas
from uuid import UUID

class UserRead(schemas.BaseUser[UUID]):
    full_name: str | None

class UserCreate(schemas.BaseUserCreate):
    full_name: str | None

class UserUpdate(schemas.BaseUserUpdate):
    full_name: str | None
```

## Фаза 4: Backend - Рекомендательная система (2-3 часа)

### 4.1 TF-IDF Recommender (2 часа)

**Файл: `backend/app/services/recommender.py`**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from typing import List
from uuid import UUID

class TFIDFRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        self.article_ids = []
    
    def fit(self, articles: List):
        """Обучить на корпусе статей"""
        texts = [f"{a.title} {a.abstract}" for a in articles]
        self.article_ids = [a.id for a in articles]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        return self
    
    def get_vector(self, text: str) -> np.ndarray:
        """Получить TF-IDF вектор для текста"""
        return self.vectorizer.transform([text]).toarray()[0]
    
    def serialize_vector(self, vector: np.ndarray) -> str:
        """Сериализовать вектор в строку"""
        return pickle.dumps(vector).hex()
    
    def deserialize_vector(self, vector_str: str) -> np.ndarray:
        """Десериализовать вектор из строки"""
        return pickle.loads(bytes.fromhex(vector_str))
    
    def build_user_profile(
        self,
        interactions: List,
        preferences: List
    ) -> np.ndarray:
        """Построить профиль пользователя"""
        weighted_vectors = []
        
        # Веса для типов взаимодействий
        weights = {
            'like': 1.0,
            'save': 0.8,
            'view': 0.3,
            'hide': -0.5
        }
        
        # Добавляем векторы из взаимодействий
        for interaction in interactions:
            if interaction.article.tfidf_vector:
                vector = self.deserialize_vector(interaction.article.tfidf_vector)
                weight = weights.get(interaction.interaction_type, 0.5)
                weighted_vectors.append(vector * weight)
        
        # Добавляем векторы из предпочтений
        for pref in preferences:
            topic_vector = self.get_vector(pref.topic)
            weighted_vectors.append(topic_vector * pref.weight)
        
        if not weighted_vectors:
            # Если нет данных, возвращаем нулевой вектор
            return np.zeros(self.tfidf_matrix.shape[1])
        
        return np.mean(weighted_vectors, axis=0)
    
    def recommend(
        self,
        user_profile: np.ndarray,
        n: int = 20,
        exclude_ids: List[UUID] = None,
        exploration_rate: float = 0.1
    ) -> List[UUID]:
        """Получить рекомендации"""
        if exclude_ids is None:
            exclude_ids = []
        
        # Вычисляем сходство
        similarities = cosine_similarity(
            user_profile.reshape(1, -1),
            self.tfidf_matrix
        )[0]
        
        # Создаем маску для исключенных статей
        mask = np.ones(len(similarities), dtype=bool)
        for i, article_id in enumerate(self.article_ids):
            if article_id in exclude_ids:
                mask[i] = False
        
        # Применяем маску
        filtered_similarities = similarities.copy()
        filtered_similarities[~mask] = -np.inf
        
        # Exploitation: топ статьи по релевантности
        n_exploit = int(n * (1 - exploration_rate))
        top_indices = np.argsort(filtered_similarities)[::-1][:n_exploit]
        
        # Exploration: случайные статьи
        n_explore = n - n_exploit
        available_indices = np.where(mask)[0]
        explore_indices = np.random.choice(
            available_indices,
            size=min(n_explore, len(available_indices)),
            replace=False
        )
        
        # Объединяем
        all_indices = np.concatenate([top_indices, explore_indices])
        
        return [self.article_ids[i] for i in all_indices]
```

### 4.2 User Profile Service (1 час)

**Файл: `backend/app/services/user_profile.py`**

```python
from sqlmodel import Session, select
from app.models.interaction import UserInteraction
from app.models.preference import UserPreference
from uuid import UUID
from datetime import datetime, timedelta

class UserProfileService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_recent_interactions(
        self,
        user_id: UUID,
        days: int = 30
    ) -> list[UserInteraction]:
        """Получить недавние взаимодействия"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        statement = select(UserInteraction).where(
            UserInteraction.user_id == user_id,
            UserInteraction.created_at >= cutoff_date
        )
        return self.session.exec(statement).all()
    
    def get_preferences(self, user_id: UUID) -> list[UserPreference]:
        """Получить предпочтения пользователя"""
        statement = select(UserPreference).where(
            UserPreference.user_id == user_id
        )
        return self.session.exec(statement).all()
    
    def get_interacted_article_ids(self, user_id: UUID) -> list[UUID]:
        """Получить ID статей с которыми взаимодействовал пользователь"""
        statement = select(UserInteraction.article_id).where(
            UserInteraction.user_id == user_id
        )
        return [row for row in self.session.exec(statement).all()]
```

## Фаза 5: Backend - API Endpoints (2-3 часа)

### 5.1 Feed API (1.5 часа)

**Файл: `backend/app/api/feed.py`**

```python
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from app.models.user import User
from app.models.article import Article
from app.api.auth import current_active_user
from app.database import get_session
from app.services.recommender import TFIDFRecommender
from app.services.user_profile import UserProfileService
from typing import List
from uuid import UUID

router = APIRouter(prefix="/api/feed", tags=["feed"])

@router.get("/")
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить персонализированную ленту"""
    
    # Получаем профиль пользователя
    profile_service = UserProfileService(session)
    interactions = profile_service.get_recent_interactions(user.id)
    preferences = profile_service.get_preferences(user.id)
    exclude_ids = profile_service.get_interacted_article_ids(user.id)
    
    # Получаем все статьи
    articles = session.exec(select(Article)).all()
    
    # Инициализируем рекомендатель
    recommender = TFIDFRecommender()
    recommender.fit(articles)
    
    # Строим профиль пользователя
    user_profile = recommender.build_user_profile(interactions, preferences)
    
    # Получаем рекомендации
    recommended_ids = recommender.recommend(
        user_profile,
        n=limit + offset,
        exclude_ids=exclude_ids
    )
    
    # Применяем пагинацию
    page_ids = recommended_ids[offset:offset + limit]
    
    # Получаем статьи
    recommended_articles = []
    for article_id in page_ids:
        article = session.get(Article, article_id)
        if article:
            recommended_articles.append(article)
    
    return {
        "articles": recommended_articles,
        "total": len(recommended_ids),
        "limit": limit,
        "offset": offset
    }
```

### 5.2 Articles API (1 час)

**Файл: `backend/app/api/articles.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.models.article import Article
from app.models.interaction import UserInteraction, InteractionType
from app.api.auth import current_active_user
from app.database import get_session
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/api/articles", tags=["articles"])

class InteractionCreate(BaseModel):
    interaction_type: InteractionType

@router.get("/{article_id}")
async def get_article(
    article_id: UUID,
    session: Session = Depends(get_session)
):
    """Получить статью по ID"""
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/{article_id}/interact")
async def interact_with_article(
    article_id: UUID,
    interaction: InteractionCreate,
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Взаимодействие со статьей"""
    # Проверяем существование статьи
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Создаем взаимодействие
    user_interaction = UserInteraction(
        user_id=user.id,
        article_id=article_id,
        interaction_type=interaction.interaction_type
    )
    session.add(user_interaction)
    session.commit()
    session.refresh(user_interaction)
    
    return {"status": "success", "interaction": user_interaction}

@router.get("/saved")
async def get_saved_articles(
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить сохраненные статьи"""
    statement = select(Article).join(UserInteraction).where(
        UserInteraction.user_id == user.id,
        UserInteraction.interaction_type == InteractionType.SAVE
    )
    articles = session.exec(statement).all()
    return {"articles": articles}
```

### 5.3 Preferences API (30 мин)

**Файл: `backend/app/api/preferences.py`**

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.models.preference import UserPreference
from app.api.auth import current_active_user
from app.database import get_session
from pydantic import BaseModel

router = APIRouter(prefix="/api/preferences", tags=["preferences"])

class TopicPreference(BaseModel):
    topic: str
    weight: float = 1.0

class PreferencesCreate(BaseModel):
    topics: list[TopicPreference]

@router.post("/")
async def set_preferences(
    preferences: PreferencesCreate,
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Установить предпочтения пользователя"""
    # Удаляем старые предпочтения
    statement = select(UserPreference).where(UserPreference.user_id == user.id)
    old_prefs = session.exec(statement).all()
    for pref in old_prefs:
        session.delete(pref)
    
    # Создаем новые
    new_prefs = []
    for topic_pref in preferences.topics:
        pref = UserPreference(
            user_id=user.id,
            topic=topic_pref.topic,
            weight=topic_pref.weight
        )
        session.add(pref)
        new_prefs.append(pref)
    
    session.commit()
    return {"status": "success", "preferences": new_prefs}

@router.get("/")
async def get_preferences(
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить предпочтения пользователя"""
    statement = select(UserPreference).where(UserPreference.user_id == user.id)
    preferences = session.exec(statement).all()
    return {"preferences": preferences}
```

## Фаза 6: Backend - Main App (1 час)

**Файл: `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_db_and_tables
from app.api import auth, feed, articles, preferences

app = FastAPI(title="MVP Articles API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.auth_router)
app.include_router(feed.router)
app.include_router(articles.router)
app.include_router(preferences.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "MVP Articles API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

## Фаза 7: Data Import Script (1-2 часа)

**Файл: `backend/app/migrations/import_articles.py`**

```python
import json
import asyncio
from sqlmodel import Session, select
from app.database import engine
from app.models.article import Article
from app.services.recommender import TFIDFRecommender
from datetime import datetime
import argparse

def import_articles(json_path: str = "/data/articles.json", clean: bool = False):
    """Импортировать статьи из JSON"""
    
    print(f"Loading articles from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles_data = data.get('articles', [])
    print(f"Found {len(articles_data)} articles")
    
    with Session(engine) as session:
        # Очистка если нужно
        if clean:
            print("Cleaning existing articles...")
            session.exec(select(Article)).all()
            for article in session.exec(select(Article)).all():
                session.delete(article)
            session.commit()
        
        # Создаем статьи
        articles = []
        for item in articles_data:
            article = Article(
                title=item['title'],
                abstract=item['abstract'],
                summary=item['summary'],
                authors=item['authors'],
                source=item['source'],
                doi=item.get('doi'),
                publication_date=datetime.strptime(
                    item['publication_date'], '%Y-%m-%d'
                ).date(),
                topics=item.get('topics', []),
                url=item.get('url')
            )
            articles.append(article)
        
        # Вычисляем TF-IDF векторы
        print("Computing TF-IDF vectors...")
        recommender = TFIDFRecommender()
        recommender.fit(articles)
        
        # Сохраняем векторы
        for i, article in enumerate(articles):
            vector = recommender.tfidf_matrix[i].toarray()[0]
            article.tfidf_vector = recommender.serialize_vector(vector)
            session.add(article)
        
        session.commit()
        print(f"Successfully imported {len(articles)} articles")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='/data/articles.json')
    parser.add_argument('--clean', action='store_true')
    args = parser.parse_args()
    
    import_articles(args.file, args.clean)
```

## Фаза 8: Frontend (4-5 часов)

### 8.1 API Client (30 мин)

**Файл: `frontend/src/services/api.js`**

```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const auth = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me'),
};

export const feed = {
  get: (params) => api.get('/api/feed', { params }),
};

export const articles = {
  get: (id) => api.get(`/api/articles/${id}`),
  interact: (id, type)