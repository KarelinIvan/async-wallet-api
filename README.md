# Async Wallet API

REST API для управления кошельками пользователей с поддержкой конкурентных запросов.

✨ Технологии (Стек)
- Серверная часть/ORM: Python, FastAPI, SQLModel
- База данных: PostgreSQL (асинхронный доступ через sqlalchemy[asyncio] и asyncpg, синхронный — psycopg2 (psycopg2-binary) для миграций)
- Миграции: Alembic
- Тестирование: Pytest, pytest-asyncio, pytest-cov (для оценки покрытия проекта тестами)
- Контейнеризация: Docker & Docker Compose


📋 Функционал
- Пополнение баланса (`DEPOSIT`)
- Списание средств (`WITHDRAW`) с проверкой на достаточность
- Получение текущего баланса
- Атомарные операции (защита от Race Condition при параллельных запросах)


🏗️ Архитектура проекта
```text
app/
├── api/                    # API эндпоинты FastAPI
├── core/                   # Конфигурация приложения (настройки, переменные окружения)
├── database/               # Работа с базой данных
│   ├── repositories/       # Репозитории: CRUD-операции с БД
│   └── session.py          # Движок, фабрика сессий, зависимость get_session
├── models/                 # ORM-модель SQLModel (описание таблицы)
├── schemas/                # Pydantic-схемы (валидация запросов и ответов API)
├── services/               # Бизнес-логика: правила и проверки
└── main.py                 # Точка входа: сборка FastAPI-приложения
tests/
```

🔐 Переменные окружения

.env:

DATABASE_URL — строка подключения к рабочей БД (postgresql+asyncpg://postgres:password@localhost:5432/database)

🗄️ Миграции базы данных

Проект использует Alembic для управления схемой БД.

Перед первым запуском примените миграции:

- alembic upgrade head

🚀 Запуск проекта
- Клонируйте репозиторий: git clone https://github.com/KarelinIvan/async-wallet-api.git
cd async-wallet-api

Локальный запуск проекта
- Создайте виртуальное окружение: python -m venv venv
- Активация виртуального окружения:
    - Для Windows (CMD/PowerShell): venv\Scripts\activate
    - Для Linux/macOS: source venv/bin/activate
- Установите зависимости: pip install -r requirements.txt
- Скопируйте файл .env.example в корневую директорию как .env. Укажите корректные параметры подключения к вашей базе данных
- Примените миграции: alembic upgrade head
- Запустите сервер разработки: uvicorn app.main:app --reload


🐳 Запуск через Docker Compose
- Соберите и запустите сервисы: docker compose up --build -d
- API доступно на http://127.0.0.1:8000, PostgreSQL — на localhost:5433
- Миграции применяются автоматически при старте контейнера app (alembic upgrade head)
- Тестовая БД wallet_test создаётся при первой инициализации тома (docker/initdb/01-create-test-db.sql). Если том pgdata уже существовал, создайте БД вручную: docker compose exec db createdb -U postgres wallet_test (либо пересоздайте том: docker compose down -v)
- Тесты внутри контейнера: docker compose exec app pytest tests/ -v
- Остановка сервисов: docker compose down


▶️ Запуск тестов
- Создайте тестовую базу данных
- Запустите тесты: pytest tests/ -v
- Проверить покрытие проекта тестами: pytest-cov: pytest --cov=app tests/

📚 Документация После запуска документация будет доступна по адресу:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc