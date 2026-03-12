# Setup Guide - MVP Персональная лента научных статей

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git
- Node.js 18+ (для локальной разработки frontend)
- Python 3.11+ (для локальной разработки backend)

### Запуск проекта

```bash
# Клонировать репозиторий
git clone <repo-url>
cd mvp

# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps

# Применить миграции БД
docker-compose exec backend alembic upgrade head

# Импортировать данные статей
docker-compose exec backend python -m app.migrations.import_articles

# Открыть приложение
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Структура JSON файла с данными статей

Создайте файл `data/articles.json` со следующей структурой:

```json
{
  "articles": [
    {
      "title": "Attention Is All You Need",
      "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
      "summary": "Статья представляет архитектуру Transformer, которая использует только механизмы внимания без рекуррентных или сверточных слоев. Это революционный подход к обработке последовательностей, который стал основой для современных языковых моделей.",
      "authors": [
        {
          "name": "Ashish Vaswani",
          "affiliation": "Google Brain"
        },
        {
          "name": "Noam Shazeer",
          "affiliation": "Google Brain"
        },
        {
          "name": "Niki Parmar",
          "affiliation": "Google Research"
        }
      ],
      "source": "arXiv",
      "doi": "10.48550/arXiv.1706.03762",
      "publication_date": "2017-06-12",
      "topics": [
        "machine learning",
        "deep learning",
        "natural language processing",
        "transformers",
        "attention mechanism"
      ],
      "url": "https://arxiv.org/abs/1706.03762"
    },
    {
      "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
      "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
      "summary": "BERT - это модель предобучения для понимания естественного языка, которая использует двунаправленные трансформеры. Модель обучается на больших объемах текста и может быть дообучена для различных задач NLP с минимальными изменениями архитектуры.",
      "authors": [
        {
          "name": "Jacob Devlin",
          "affiliation": "Google AI Language"
        },
        {
          "name": "Ming-Wei Chang",
          "affiliation": "Google AI Language"
        },
        {
          "name": "Kenton Lee",
          "affiliation": "Google AI Language"
        }
      ],
      "source": "arXiv",
      "doi": "10.48550/arXiv.1810.04805",
      "publication_date": "2018-10-11",
      "topics": [
        "natural language processing",
        "transformers",
        "pre-training",
        "language models",
        "transfer learning"
      ],
      "url": "https://arxiv.org/abs/1810.04805"
    },
    {
      "title": "Deep Residual Learning for Image Recognition",
      "abstract": "Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions.",
      "summary": "ResNet представляет концепцию остаточных связей (skip connections), которые позволяют обучать очень глубокие нейронные сети. Эта архитектура решает проблему затухающих градиентов и позволяет создавать сети с сотнями слоев.",
      "authors": [
        {
          "name": "Kaiming He",
          "affiliation": "Microsoft Research"
        },
        {
          "name": "Xiangyu Zhang",
          "affiliation": "Microsoft Research"
        },
        {
          "name": "Shaoqing Ren",
          "affiliation": "Microsoft Research"
        },
        {
          "name": "Jian Sun",
          "affiliation": "Microsoft Research"
        }
      ],
      "source": "arXiv",
      "doi": "10.48550/arXiv.1512.03385",
      "publication_date": "2015-12-10",
      "topics": [
        "computer vision",
        "deep learning",
        "convolutional neural networks",
        "image recognition",
        "residual networks"
      ],
      "url": "https://arxiv.org/abs/1512.03385"
    },
    {
      "title": "Generative Adversarial Networks",
      "abstract": "We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data rather than G.",
      "summary": "GAN - это архитектура для генеративного моделирования, где две нейронные сети соревнуются друг с другом. Генератор создает синтетические данные, а дискриминатор пытается отличить их от реальных. Этот подход произвел революцию в генерации изображений, текста и других данных.",
      "authors": [
        {
          "name": "Ian Goodfellow",
          "affiliation": "Université de Montréal"
        },
        {
          "name": "Jean Pouget-Abadie",
          "affiliation": "Université de Montréal"
        },
        {
          "name": "Mehdi Mirza",
          "affiliation": "Université de Montréal"
        }
      ],
      "source": "arXiv",
      "doi": "10.48550/arXiv.1406.2661",
      "publication_date": "2014-06-10",
      "topics": [
        "generative models",
        "deep learning",
        "adversarial training",
        "image generation",
        "unsupervised learning"
      ],
      "url": "https://arxiv.org/abs/1406.2661"
    },
    {
      "title": "Neural Machine Translation by Jointly Learning to Align and Translate",
      "abstract": "Neural machine translation is a recently proposed approach to machine translation. Unlike the traditional statistical machine translation, the neural machine translation aims at building a single neural network that can be jointly tuned to maximize the translation performance.",
      "summary": "Статья представляет механизм внимания (attention mechanism) для нейронного машинного перевода. Это позволяет модели фокусироваться на релевантных частях входного предложения при генерации каждого слова перевода, значительно улучшая качество перевода.",
      "authors": [
        {
          "name": "Dzmitry Bahdanau",
          "affiliation": "Jacobs University Bremen"
        },
        {
          "name": "Kyunghyun Cho",
          "affiliation": "Université de Montréal"
        },
        {
          "name": "Yoshua Bengio",
          "affiliation": "Université de Montréal"
        }
      ],
      "source": "arXiv",
      "doi": "10.48550/arXiv.1409.0473",
      "publication_date": "2014-09-01",
      "topics": [
        "machine translation",
        "attention mechanism",
        "sequence to sequence",
        "natural language processing",
        "neural networks"
      ],
      "url": "https://arxiv.org/abs/1409.0473"
    }
  ]
}
```

### Поля JSON структуры

- **title** (string, required): Название статьи
- **abstract** (string, required): Полный abstract статьи
- **summary** (string, required): Краткое резюме, сгенерированное LLM в Google Colab
- **authors** (array, required): Список авторов
  - **name** (string): Имя автора
  - **affiliation** (string): Организация
- **source** (string, required): Источник (arXiv, PubMed, etc.)
- **doi** (string, optional): DOI идентификатор
- **publication_date** (string, required): Дата публикации в формате YYYY-MM-DD
- **topics** (array, required): Список тематик/тегов
- **url** (string, optional): Ссылка на статью

## Локальная разработка

### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
export DATABASE_URL="postgresql://mvp_user:mvp_password@localhost:5432/mvp_articles"
export SECRET_KEY="your-secret-key-for-development"

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Настроить переменные окружения
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Запустить dev сервер
npm start
```

## Переменные окружения

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://mvp_user:mvp_password@postgres:5432/mvp_articles

# Security
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# FastAPI Users
VERIFICATION_TOKEN_SECRET=another-secret-key-for-verification
RESET_PASSWORD_TOKEN_SECRET=yet-another-secret-for-password-reset
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
```

## Команды Docker Compose

```bash
# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Пересобрать образы
docker-compose build

# Посмотреть логи
docker-compose logs -f

# Посмотреть логи конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend

# Выполнить команду в контейнере
docker-compose exec backend bash
docker-compose exec postgres psql -U mvp_user -d mvp_articles

# Очистить все данные (включая БД)
docker-compose down -v
```

## Миграции базы данных

```bash
# Создать новую миграцию
docker-compose exec backend alembic revision --autogenerate -m "description"

# Применить миграции
docker-compose exec backend alembic upgrade head

# Откатить миграцию
docker-compose exec backend alembic downgrade -1

# Посмотреть историю миграций
docker-compose exec backend alembic history
```

## Импорт данных

```bash
# Импортировать статьи из JSON
docker-compose exec backend python -m app.migrations.import_articles

# Импортировать с указанием пути
docker-compose exec backend python -m app.migrations.import_articles --file /data/articles.json

# Очистить БД и импортировать заново
docker-compose exec backend python -m app.migrations.import_articles --clean
```

## Тестирование API

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "strongpassword123",
    "full_name": "Test User"
  }'
```

### Вход

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=strongpassword123" \
  -c cookies.txt
```

### Получить текущего пользователя

```bash
curl -X GET http://localhost:8000/auth/me \
  -b cookies.txt
```

### Установить предпочтения

```bash
curl -X POST http://localhost:8000/api/preferences \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "topics": [
      {"topic": "machine learning", "weight": 1.0},
      {"topic": "deep learning", "weight": 0.9},
      {"topic": "natural language processing", "weight": 0.8}
    ]
  }'
```

### Получить ленту

```bash
curl -X GET "http://localhost:8000/api/feed?limit=10&offset=0" \
  -b cookies.txt
```

### Взаимодействие со статьей

```bash
curl -X POST http://localhost:8000/api/articles/{article_id}/interact \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"interaction_type": "like"}'
```

## Структура базы данных

### Таблицы

1. **user** - пользователи (управляется FastAPI Users)
2. **article** - научные статьи
3. **userinteraction** - взаимодействия пользователей со статьями
4. **userpreference** - предпочтения пользователей по темам

### Просмотр данных

```bash
# Подключиться к PostgreSQL
docker-compose exec postgres psql -U mvp_user -d mvp_articles

# Посмотреть таблицы
\dt

# Посмотреть пользователей
SELECT id, email, full_name, is_active FROM "user";

# Посмотреть статьи
SELECT id, title, source, publication_date FROM article LIMIT 5;

# Посмотреть взаимодействия
SELECT u.email, a.title, ui.interaction_type, ui.created_at 
FROM userinteraction ui
JOIN "user" u ON ui.user_id = u.id
JOIN article a ON ui.article_id = a.id
ORDER BY ui.created_at DESC
LIMIT 10;
```

## Troubleshooting

### Backend не запускается

```bash
# Проверить логи
docker-compose logs backend

# Проверить подключение к БД
docker-compose exec backend python -c "from app.database import engine; print(engine.url)"

# Пересоздать контейнер
docker-compose up -d --force-recreate backend
```

### Frontend не подключается к API

1. Проверьте CORS настройки в backend
2. Убедитесь что `REACT_APP_API_URL` правильно настроен
3. Проверьте что backend доступен: `curl http://localhost:8000/docs`

### Проблемы с миграциями

```bash
# Сбросить БД и применить миграции заново
docker-compose down -v
docker-compose up -d postgres
sleep 5
docker-compose up -d backend
docker-compose exec backend alembic upgrade head
```

### Проблемы с импортом данных

```bash
# Проверить формат JSON
cat data/articles.json | python -m json.tool

# Проверить права доступа
ls -la data/

# Импортировать с подробными логами
docker-compose exec backend python -m app.migrations.import_articles --verbose
```

## Production Deployment

### Подготовка к деплою

1. Изменить `SECRET_KEY` на случайную строку длиной 32+ символа
2. Установить `cookie_secure=True` в настройках аутентификации
3. Настроить CORS только для production доменов
4. Использовать managed PostgreSQL (Supabase, Neon, AWS RDS)
5. Добавить Nginx для reverse proxy
6. Настроить SSL сертификаты (Let's Encrypt)

### Рекомендуемые платформы

**Backend:**
- Railway (простой деплой с PostgreSQL)
- Render (бесплатный tier)
- DigitalOcean App Platform
- AWS ECS / Google Cloud Run

**Frontend:**
- Vercel (рекомендуется для React)
- Netlify
- Cloudflare Pages

**Database:**
- Supabase (PostgreSQL + бесплатный tier)
- Neon (serverless PostgreSQL)
- Railway PostgreSQL

### Environment Variables для Production

```env
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<generate-with-openssl-rand-hex-32>
CORS_ORIGINS=https://yourdomain.com
COOKIE_SECURE=true

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
```

## Мониторинг и логирование

### Логи приложения

```bash
# Все логи
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Последние 100 строк
docker-compose logs --tail=100 backend
```

### Метрики PostgreSQL

```bash
# Размер БД
docker-compose exec postgres psql -U mvp_user -d mvp_articles -c "
SELECT pg_size_pretty(pg_database_size('mvp_articles'));"

# Количество записей в таблицах
docker-compose exec postgres psql -U mvp_user -d mvp_articles -c "
SELECT 
  schemaname,
  tablename,
  n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;"
```

## Следующие шаги после MVP

1. **Улучшение рекомендаций:**
   - Добавить collaborative filtering
   - Использовать эмбеддинги из LLM вместо TF-IDF
   - A/B тестирование алгоритмов

2. **Новые функции:**
   - Поиск по статьям
   - Экспорт в PDF/BibTeX
   - Социальные функции (комментарии, обсуждения)
   - Email дайджесты

3. **Интеграции:**
   - Подключение к arXiv API
   - Semantic Scholar API
   - PubMed API
   - Google Scholar (через scraping)

4. **Масштабирование:**
   - Кэширование (Redis)
   - Очереди задач (Celery)
   - CDN для статических файлов
   - Горизонтальное масштабирование

## Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Material-UI](https://mui.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)