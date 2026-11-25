# Async Wallet API

REST API для управления кошельками пользователей с поддержкой конкурентных запросов.

✨ Технологии (Стек)
- Python 3.14.7
- FastAPI — веб-фреймворк
- SQLModel (SQLAlchemy + Pydantic) — ORM
- PostgreSQL — база данных
- Alembic — миграции
- Docker & Docker Compose — контейнеризация
- Pytest — тестирование

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
├── integration/            # Интеграционные тесты (HTTP, БД, репозитории, сервисы)
└── unit/                   # Юнит-тесты (сервисы)
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

📚 Документация После запуска документация будет доступна по адресу:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc