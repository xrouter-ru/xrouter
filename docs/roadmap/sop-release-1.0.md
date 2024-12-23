# SOP: Release 1.0 - Foundation (Python)

## 1. Подготовка инфраструктуры

### 1.1. Настройка монорепозитория
- [ ] Создать базовую структуру проекта
  - [ ] Настроить директории (src/xrouter, tests, docs)
  - [ ] Создать .gitignore
  - [ ] Настроить editorconfig
- [ ] Настроить Python окружение
  ```toml
  [tool.poetry.dependencies]
  python = "^3.11"
  fastapi = "^0.104.1"
  uvicorn = "^0.24.0"
  sqlalchemy = "^2.0.23"
  aiosqlite = "^0.19.0"
  redis = "^5.0.1"
  pydantic = "^2.5.2"
  httpx = "^0.25.2"
  tiktoken = "^0.5.1"
  prometheus-client = "^0.19.0"
  structlog = "^23.2.0"

  [tool.poetry.dev-dependencies]
  black = "^23.11.0"
  isort = "^5.12.0"
  flake8 = "^6.1.0"
  pytest = "^7.4.3"
  pytest-asyncio = "^0.21.1"
  pytest-cov = "^4.1.0"
  pytest-env = "^1.1.1"
  ```
- [ ] Настроить линтеры и форматтеры
  - [ ] black для форматирования
  - [ ] isort для импортов
  - [ ] flake8 для линтинга
  - [ ] pre-commit хуки

### 1.2. Настройка хранилищ
- [ ] Настроить SQLite
  - [ ] Создать схему базы данных
    ```sql
    -- API Keys
    CREATE TABLE api_keys (
        id TEXT PRIMARY KEY,
        key_hash TEXT NOT NULL,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        last_used_at TIMESTAMP
    );

    -- Usage Records
    CREATE TABLE usage (
        id TEXT PRIMARY KEY,
        api_key_id TEXT REFERENCES api_keys(id),
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        tokens_input INTEGER NOT NULL,
        tokens_output INTEGER NOT NULL,
        cost DECIMAL(10,6) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Provider Status
    CREATE TABLE provider_status (
        id TEXT PRIMARY KEY,
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        status TEXT NOT NULL,
        latency INTEGER,
        error_rate DECIMAL(5,2),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```
  - [ ] Настроить alembic миграции
  - [ ] Настроить бэкапы
- [ ] Настроить Redis
  - [ ] Установить Redis
  - [ ] Настроить rate limiting
  - [ ] Настроить кэширование статистики
- [ ] Настроить SQLAlchemy
  - [ ] Создать модели
  - [ ] Настроить сессии
  - [ ] Настроить миграции

### 1.3. Настройка мониторинга
- [ ] Установить Prometheus
  - [ ] Настроить метрики FastAPI
  - [ ] Создать алерты
  - [ ] Настроить экспортеры
- [ ] Настроить Grafana
  - [ ] Создать дашборды для токенов/кредитов
  - [ ] Настроить визуализации
  - [ ] Настроить алерты
- [ ] Настроить логирование
  - [ ] Настроить structlog
  - [ ] Настроить форматы логов
  - [ ] Настроить ротацию

## 2. Разработка Core API

### 2.1. API Gateway и Auth
- [ ] Создать базовый FastAPI сервер
  ```python
  app/
  ├── api/
  │   ├── __init__.py
  │   ├── router.py
  │   └── endpoints/
  │       ├── __init__.py
  │       └── chat.py
  ├── core/
  │   ├── __init__.py
  │   ├── config.py
  │   └── security.py
  ├── db/
  │   ├── __init__.py
  │   └── models.py
  └── services/
      ├── __init__.py
      ├── usage.py
      └── providers/
          ├── __init__.py
          └── gigachat.py
  ```
- [ ] Настроить middleware
- [ ] Настроить роутинг
- [ ] Добавить валидацию
- [ ] Реализовать API Key аутентификацию
  - [ ] Валидация ключей
  - [ ] Rate limiting
  - [ ] Логирование доступа

### 2.2. Usage Service
- [ ] Реализовать базовый функционал
  ```python
  class UsageService:
      async def calculate_tokens(self, request: Request) -> TokenCount:
          pass
      
      async def record_usage(self, usage: Usage) -> None:
          pass
      
      async def get_usage_stats(self, api_key: str) -> UsageStats:
          pass
      
      async def check_limits(self, api_key: str) -> LimitCheck:
          pass
  ```
- [ ] Добавить подсчет токенов
- [ ] Реализовать учет кредитов
- [ ] Добавить кэширование в Redis
- [ ] Настроить метрики использования

### 2.3. GigaChat Provider
- [ ] Реализовать GigaChat адаптер
  - [ ] Создать базовый класс
  - [ ] Добавить аутентификацию
  - [ ] Реализовать методы API
- [ ] Добавить обработку ошибок
  - [ ] Создать классы ошибок
  - [ ] Добавить retry логику
  - [ ] Настроить логирование
- [ ] Написать тесты
  - [ ] Unit тесты
  - [ ] Интеграционные тесты
  - [ ] Тесты производительности

### 2.4. Router Service
- [ ] Реализовать базовую маршрутизацию
  - [ ] Создать Router класс
  - [ ] Добавить логику выбора провайдера
  - [ ] Реализовать fallback
- [ ] Добавить трансформацию запросов
  - [ ] Нормализация входящих запросов
  - [ ] Трансформация для провайдера
  - [ ] Нормализация ответов
- [ ] Написать тесты
  - [ ] Тесты маршрутизации
  - [ ] Тесты трансформации
  - [ ] Тесты ошибок

## 3. Тестирование

### 3.1. Unit тестирование
- [ ] Тесты API Gateway
  - [ ] Тесты валидации запросов
  - [ ] Тесты API ключей
  - [ ] Тесты rate limiting
- [ ] Тесты Usage Service
  - [ ] Тесты подсчета токенов
  - [ ] Тесты учета кредитов
  - [ ] Тесты лимитов
- [ ] Тесты Provider адаптера
  - [ ] Тесты подключения
  - [ ] Тесты запросов
  - [ ] Тесты ошибок
- [ ] Тесты Router Service
  - [ ] Тесты маршрутизации
  - [ ] Тесты fallback
  - [ ] Тесты трансформации

### 3.2. Интеграционное тестирование
- [ ] Тесты взаимодействия компонентов
  - [ ] Gateway + Usage Service
  - [ ] Gateway + Router
  - [ ] Router + Provider
- [ ] Тесты производительности
  - [ ] Latency тесты
  - [ ] Throughput тесты
  - [ ] Load тесты
- [ ] Тесты отказоустойчивости
  - [ ] Тесты fallback
  - [ ] Тесты recovery
  - [ ] Stress тесты

## 4. Документация

### 4.1. API документация
- [ ] Создать OpenAPI спецификацию
  - [ ] Описать endpoints
  - [ ] Добавить примеры
  - [ ] Описать ошибки
- [ ] Документировать аутентификацию
  - [ ] API ключи
  - [ ] Rate limiting
  - [ ] Лимиты использования
- [ ] Создать примеры использования
  - [ ] Curl примеры
  - [ ] Python примеры
  - [ ] Postman коллекцию

### 4.2. Техническая документация
- [ ] Документировать архитектуру
  - [ ] Компоненты
  - [ ] Взаимодействия
  - [ ] Потоки данных
- [ ] Документировать конфигурацию
  - [ ] Переменные окружения
  - [ ] Poetry зависимости
  - [ ] Примеры настройки
- [ ] Создать руководство по развертыванию
  - [ ] Требования
  - [ ] Шаги установки
  - [ ] Проверки

## 5. Развертывание

### 5.1. Подготовка
- [ ] Проверить зависимости
  - [ ] Python пакеты
  - [ ] Внешние сервисы
  - [ ] Системные требования
- [ ] Подготовить конфигурацию
  - [ ] Создать конфиги
  - [ ] Настроить переменные окружения
  - [ ] Проверить доступы
- [ ] Подготовить скрипты
  - [ ] Скрипты установки
  - [ ] Скрипты бэкапа SQLite
  - [ ] Скрипты проверки

### 5.2. Развертывание
- [ ] Подготовить хранилища
  - [ ] Создать SQLite базу
  - [ ] Настроить Redis
  - [ ] Применить миграции
- [ ] Развернуть сервисы
  - [ ] API Gateway
  - [ ] Usage Service
  - [ ] Router Service
  - [ ] Мониторинг
- [ ] Настроить SSL/TLS
  - [ ] Получить сертификаты
  - [ ] Настроить HTTPS
  - [ ] Проверить безопасность

### 5.3. Пост-развертывание
- [ ] Проверить работоспособность
  - [ ] API endpoints
  - [ ] Учет токенов
  - [ ] Маршрутизация
- [ ] Мониторить производительность
  - [ ] Latency
  - [ ] Error rates
  - [ ] Resource usage
- [ ] Настроить алерты
  - [ ] Prometheus alerts
  - [ ] Email notifications
  - [ ] Slack notifications

## 6. Критерии приемки

### 6.1. Функциональные требования
- [ ] API Gateway работает и доступен
- [ ] API key аутентификация работает корректно
- [ ] Учет токенов и кредитов точный
- [ ] GigaChat интеграция работает
- [ ] Маршрутизация работает правильно
- [ ] Мониторинг предоставляет данные

### 6.2. Нефункциональные требования
- [ ] Latency < 500ms (без учета времени провайдера)
- [ ] Error rate < 1%
- [ ] Успешная обработка 100 req/s
- [ ] Документация полная и актуальная
- [ ] Мониторинг предоставляет все необходимые метрики