# SOP: Release 1.0 - Foundation (Python)

## 1. Подготовка инфраструктуры

### 1.1. Настройка проекта ✅
- [x] Создать структуру проекта
  ```
  xrouter/
  ├── src/
  │   └── xrouter/
  │       ├── api/           # API Gateway
  │       │   ├── __init__.py
  │       │   ├── routes/
  │       │   └── middleware/
  │       ├── usage/         # Usage Service
  │       │   ├── __init__.py
  │       │   ├── service.py
  │       │   └── models.py
  │       ├── providers/     # Provider Manager
  │       │   ├── __init__.py
  │       │   ├── base.py
  │       │   └── gigachat/
  │       ├── router/        # Router Service
  │       │   ├── __init__.py
  │       │   └── service.py
  │       ├── core/          # Общие компоненты
  │       │   ├── __init__.py
  │       │   ├── config.py
  │       │   └── errors.py
  │       └── db/           # Работа с БД
  │           ├── __init__.py
  │           └── models.py
  ├── tests/
  │   ├── unit/
  │   └── integration/
  ├── docs/
  └── scripts/
  ```

- [x] Настроить Poetry
  ```toml
  [tool.poetry]
  name = "xrouter"
  version = "1.0.0"
  description = "Russian LLM Router"

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

- [x] Настроить линтеры и форматтеры
  ```ini
  # .flake8
  [flake8]
  max-line-length = 88
  extend-ignore = E203
  exclude = .git,__pycache__,build,dist

  # pyproject.toml
  [tool.black]
  line-length = 88
  target-version = ['py311']
  include = '\.pyi?$'

  [tool.isort]
  profile = "black"
  multi_line_output = 3
  ```

- [x] Настроить pre-commit hooks
  ```yaml
  # .pre-commit-config.yaml
  repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  ```

### 1.2. Настройка хранилищ

#### SQLite
- [x] Создать схему базы данных
  ```sql
  -- api_keys.sql
  CREATE TABLE api_keys (
      id TEXT PRIMARY KEY,
      key_hash TEXT NOT NULL,
      name TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      expires_at TIMESTAMP,
      last_used_at TIMESTAMP
  );

  -- usage.sql
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

  -- provider_status.sql
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

- [x] Настроить SQLAlchemy модели с современным синтаксисом 2.0
  ```python
  # db/models.py
  from datetime import datetime
  from typing import Optional
  from uuid import UUID

  from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
  from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

  class Base(DeclarativeBase):
      """Base class for all SQLAlchemy models."""

  class APIKey(Base):
      __tablename__ = "api_keys"

      id: Mapped[UUID] = mapped_column(primary_key=True)
      key_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
      name: Mapped[Optional[str]] = mapped_column(String(255))
      created_at: Mapped[datetime] = mapped_column(
          DateTime(timezone=True), server_default=func.now()
      )
      expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
      last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

      # Relationships
      usage_records: Mapped[list["Usage"]] = relationship(back_populates="api_key")

  class Usage(Base):
      __tablename__ = "usage"

      id: Mapped[UUID] = mapped_column(primary_key=True)
      api_key_id: Mapped[UUID] = mapped_column(ForeignKey("api_keys.id"))
      provider: Mapped[str] = mapped_column(String(50), nullable=False)
      model: Mapped[str] = mapped_column(String(50), nullable=False)
      tokens_input: Mapped[int] = mapped_column(Integer, nullable=False)
      tokens_output: Mapped[int] = mapped_column(Integer, nullable=False)
      cost: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
      created_at: Mapped[datetime] = mapped_column(
          DateTime(timezone=True), server_default=func.now()
      )

      # Relationships
      api_key: Mapped["APIKey"] = relationship(back_populates="usage_records")
  ```

- [x] Настроить асинхронную работу с базой данных
  ```python
  # db/database.py
  from contextlib import asynccontextmanager
  from typing import AsyncGenerator

  from sqlalchemy.ext.asyncio import (
      AsyncEngine,
      AsyncSession,
      async_sessionmaker,
      create_async_engine,
  )

  class Database:
      def __init__(self) -> None:
          self.engine: AsyncEngine = create_async_engine(
              settings.SQLITE_URL,
              echo=settings.DB_ECHO,
              pool_pre_ping=True,
          )
          self.async_session_maker = async_sessionmaker(
              self.engine,
              class_=AsyncSession,
              expire_on_commit=False,
          )

      @asynccontextmanager
      async def session(self) -> AsyncGenerator[AsyncSession, None]:
          async with self.async_session_maker() as session:
              try:
                  yield session
                  await session.commit()
              except Exception:
                  await session.rollback()
                  raise
  ```

- [x] Настроить миграции с Alembic
  ```ini
  # alembic.ini
  [alembic]
  script_location = migrations
  sqlalchemy.url = sqlite+aiosqlite:///xrouter.db

  [loggers]
  keys = root,sqlalchemy,alembic
  ```
  ```python
  # migrations/env.py
  from alembic import context
  from sqlalchemy import pool
  from sqlalchemy.ext.asyncio import async_engine_from_config

  from xrouter.db.models import Base

  target_metadata = Base.metadata

  async def run_migrations() -> None:
      configuration = config.get_section(config.config_ini_section)
      configuration["sqlalchemy.url"] = settings.SQLITE_URL
      connectable = async_engine_from_config(
          configuration,
          prefix="sqlalchemy.",
          poolclass=pool.NullPool,
      )

      async with connectable.connect() as connection:
          await connection.run_sync(do_run_migrations)
  ```

#### Redis
- [x] Настроить схемы кэширования и rate limiting
  ```python
  # core/cache.py
  from typing import Any, Optional
  from redis.asyncio import Redis

  class RedisKeys:
      # Rate Limiting
      RATE_LIMIT = "rate:{api_key}:{window}"

      # Usage Stats
      USAGE_COUNTER = "usage:{api_key}:counter"
      USAGE_HISTORY = "usage:{api_key}:history"

      # Provider Status
      PROVIDER_STATUS = "provider:{name}:status"
      MODEL_STATUS = "model:{name}:status"
  ```

- [x] Реализовать базовый Redis клиент с типизацией
  ```python
  # core/cache.py
  class RedisClient:
      def __init__(self, redis: Redis[Any]) -> None:
          self.redis = redis

      async def get_rate_limit(self, api_key: str) -> int:
          key = RedisKeys.RATE_LIMIT.format(api_key=api_key)
          count: Optional[bytes] = await self.redis.get(key)
          return int(count.decode()) if count else 0

      async def increment_rate_limit(self, api_key: str) -> int:
          key = RedisKeys.RATE_LIMIT.format(api_key=api_key)
          count = await self.redis.incr(key)
          if count == 1:
              await self.redis.expire(key, 60)  # 1 minute window
          return count

      async def get_usage_counter(self, api_key: str) -> int:
          key = RedisKeys.USAGE_COUNTER.format(api_key=api_key)
          count: Optional[bytes] = await self.redis.get(key)
          return int(count.decode()) if count else 0
  ```

- [x] Настроить mypy для работы с Redis
  ```toml
  # pyproject.toml
  [tool.mypy]
  python_version = "3.11"
  plugins = []
  warn_return_any = true
  warn_unused_configs = true
  disallow_untyped_defs = true
  check_untyped_defs = true
  ignore_missing_imports = true
  follow_imports = "silent"
  disallow_any_generics = false
  disallow_subclassing_any = false

  [[tool.mypy.overrides]]
  module = "redis.*"
  ignore_missing_imports = true
  follow_imports = "skip"
  ```

## 2. Разработка сервисов

### 2.1. Usage Service

#### Реализация
- [ ] Создать базовые модели данных
  ```python
  # usage/models.py
  from pydantic import BaseModel
  from datetime import datetime
  from decimal import Decimal

  class TokenCount(BaseModel):
      input: int
      output: int
      total: int
      model: str

  class Cost(BaseModel):
      amount: Decimal
      currency: str
      breakdown: dict[str, Decimal]

  class Usage(BaseModel):
      id: str
      api_key: str
      provider: str
      model: str
      tokens: TokenCount
      cost: Cost
      timestamp: datetime
  ```

- [ ] Реализовать основной сервис
  ```python
  # usage/service.py
  class UsageService:
      def __init__(self, db: Database, cache: RedisClient):
          self.db = db
          self.cache = cache

      async def calculate_tokens(self, request: Request) -> TokenCount:
          # Подсчет токенов через tiktoken
          encoding = tiktoken.encoding_for_model(request.model)
          input_tokens = sum(len(encoding.encode(msg.content))
                           for msg in request.messages)
          return TokenCount(
              input=input_tokens,
              output=request.max_tokens or self.get_default_max_tokens(request.model),
              total=input_tokens + output_tokens,
              model=request.model
          )

      async def record_usage(self, usage: Usage) -> None:
          # Запись в БД
          await self.db.insert_usage(usage)
          # Обновление кэша
          await self.cache.increment_usage(usage.api_key, usage.tokens.total)
          # Метрики
          await self.record_metrics(usage)
  ```

#### Тестирование
- [ ] Unit тесты
  ```python
  # tests/unit/test_usage_service.py
  async def test_calculate_tokens():
      service = UsageService(db_mock, cache_mock)
      request = ChatRequest(
          messages=[Message(role="user", content="Hello")],
          model="gigachat-pro"
      )
      tokens = await service.calculate_tokens(request)
      assert tokens.input == 1  # "Hello" = 1 token
      assert tokens.total == tokens.input + tokens.output

  async def test_record_usage():
      service = UsageService(db_mock, cache_mock)
      usage = Usage(...)
      await service.record_usage(usage)
      db_mock.insert_usage.assert_called_once_with(usage)
      cache_mock.increment_usage.assert_called_once()
  ```

- [ ] Интеграционные тесты
  ```python
  # tests/integration/test_usage_service.py
  async def test_usage_flow():
      # Создаем реальные БД и Redis для тестов
      db = create_test_db()
      cache = create_test_cache()
      service = UsageService(db, cache)

      # Тестируем полный flow
      request = ChatRequest(...)
      tokens = await service.calculate_tokens(request)
      usage = Usage(...)
      await service.record_usage(usage)

      # Проверяем запись в БД
      stored = await db.get_usage(usage.id)
      assert stored == usage

      # Проверяем кэш
      cached = await cache.get_usage(usage.api_key)
      assert cached == usage.tokens.total
  ```

#### Критерии приемки
- [ ] Точный подсчет токенов
  - Проверка на разных моделях
  - Проверка на разных языках
  - Сравнение с реальными результатами от провайдеров
- [ ] Корректная запись использования
  - Все поля сохраняются
  - Транзакционность работает
  - Кэш обновляется
- [ ] Производительность
  - Подсчет токенов < 10ms
  - Запись использования < 50ms
  - Чтение статистики < 100ms

### 2.2. Provider Manager

#### Реализация
- [ ] Создать базовый интерфейс провайдера
  ```python
  # providers/base.py
  class Provider(ABC):
      @abstractmethod
      async def create_completion(
          self,
          messages: list[Message],
          **kwargs
      ) -> CompletionResponse:
          pass

      @abstractmethod
      async def calculate_tokens(
          self,
          messages: list[Message]
      ) -> TokenCount:
          pass
  ```

- [ ] Реализовать GigaChat провайдер
  ```python
  # providers/gigachat/provider.py
  class GigaChatProvider(Provider):
      def __init__(self, client: GigaChatClient):
          self.client = client
          self.models = {
              "gigachat": {"max_tokens": 8192},
              "gigachat-pro": {"max_tokens": 32768},
          }

      async def create_completion(
          self,
          messages: list[Message],
          **kwargs
      ) -> CompletionResponse:
          request = self.transform_request(messages, kwargs)
          response = await self.client.create_completion(request)
          return self.transform_response(response)

      async def calculate_tokens(
          self,
          messages: list[Message]
      ) -> TokenCount:
          # GigaChat использует GPT-3.5 tokenizer
          encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
          return TokenCount(
              input=sum(len(encoding.encode(msg.content))
                       for msg in messages),
              output=0,  # Будет заполнено после ответа
              model=self.model
          )
  ```

#### Тестирование
- [ ] Unit тесты
  ```python
  # tests/unit/test_gigachat_provider.py
  async def test_create_completion():
      client = MockGigaChatClient()
      provider = GigaChatProvider(client)

      messages = [Message(role="user", content="Hello")]
      response = await provider.create_completion(messages)

      assert response.choices[0].message.content
      assert response.usage.total_tokens > 0

  async def test_calculate_tokens():
      provider = GigaChatProvider(mock_client)
      messages = [Message(role="user", content="Hello")]
      tokens = await provider.calculate_tokens(messages)
      assert tokens.input == 1  # "Hello" = 1 token
  ```

- [ ] Интеграционные тесты
  ```python
  # tests/integration/test_gigachat_provider.py
  async def test_real_api_call():
      client = GigaChatClient(os.getenv("GIGACHAT_API_KEY"))
      provider = GigaChatProvider(client)

      messages = [Message(role="user", content="Привет")]
      response = await provider.create_completion(messages)

      assert response.choices[0].message.content
      assert isinstance(response.choices[0].message.content, str)
      assert response.usage.total_tokens > 0
  ```

#### Критерии приемки
- [ ] Успешное подключение к GigaChat
  - Аутентификация работает
  - API вызовы проходят
  - Ошибки обрабатываются
- [ ] Корректная трансформация
  - Запросы преобразуются правильно
  - Ответы нормализуются
  - Токены считаются точно
- [ ] Производительность
  - Overhead на трансформацию < 5ms
  - Retry механизм работает
  - Таймауты настроены

### 2.3. Router Service

#### Реализация
- [ ] Создать базовый роутер
  ```python
  # router/service.py
  class RouterService:
      def __init__(
          self,
          providers: dict[str, Provider],
          usage_service: UsageService
      ):
          self.providers = providers
          self.usage_service = usage_service

      async def route_request(
          self,
          request: ChatRequest,
          api_key: str
      ) -> ChatResponse:
          # Проверяем лимиты
          tokens = await self.usage_service.calculate_tokens(request)
          if not await self.usage_service.check_limits(api_key, tokens):
              raise UsageLimitExceeded()

          # Получаем провайдера
          provider = self.get_provider(request.model)

          # Выполняем запрос
          response = await provider.create_completion(
              request.messages,
              **request.parameters
          )

          # Записываем использование
          await self.usage_service.record_usage(Usage(
              api_key=api_key,
              provider=provider.name,
              model=request.model,
              tokens=response.usage,
              cost=self.calculate_cost(response.usage)
          ))

          return response
  ```

#### Тестирование
- [ ] Unit тесты
  ```python
  # tests/unit/test_router_service.py
  async def test_route_request():
      providers = {"gigachat": MockProvider()}
      usage_service = MockUsageService()
      router = RouterService(providers, usage_service)

      request = ChatRequest(
          messages=[Message(role="user", content="Hello")],
          model="gigachat"
      )
      response = await router.route_request(request, "test-key")

      assert response.choices[0].message.content
      usage_service.record_usage.assert_called_once()

  async def test_usage_limit_exceeded():
      usage_service = MockUsageService(should_exceed=True)
      router = RouterService({"gigachat": MockProvider()}, usage_service)

      with pytest.raises(UsageLimitExceeded):
          await router.route_request(request, "test-key")
  ```

- [ ] Интеграционные тесты
  ```python
  # tests/integration/test_router_service.py
  async def test_full_request_flow():
      # Создаем реальные сервисы
      provider = GigaChatProvider(create_test_client())
      usage_service = create_test_usage_service()
      router = RouterService({"gigachat": provider}, usage_service)

      # Тестируем полный flow
      request = ChatRequest(...)
      response = await router.route_request(request, "test-key")

      # Проверяем результат
      assert response.choices[0].message.content

      # Проверяем запись использования
      usage = await usage_service.get_usage("test-key")
      assert usage.tokens.total > 0
  ```

#### Критерии приемки
- [ ] Корректная маршрутизация
  - Правильный выбор провайдера
  - Проверка лимитов работает
  - Запись использования происходит
- [ ] Обработка ошибок
  - Ошибки провайдера обрабатываются
  - Ошибки лимитов обрабатываются
  - Retry логика работает
- [ ] Производительность
  - Overhead на маршрутизацию < 10ms
  - Параллельные запросы работают
  - Нет блокировок

### 2.4. API Gateway

#### Реализация
- [ ] Создать FastAPI приложение
  ```python
  # api/app.py
  from fastapi import FastAPI, Depends, HTTPException
  from fastapi.middleware.cors import CORSMiddleware

  app = FastAPI(title="XRouter")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  @app.post("/v1/chat/completions")
  async def create_chat_completion(
      request: ChatRequest,
      api_key: str = Depends(get_api_key),
      router: RouterService = Depends(get_router)
  ):
      try:
          return await router.route_request(request, api_key)
      except UsageLimitExceeded:
          raise HTTPException(402, "Usage limit exceeded")
      except ProviderError as e:
          raise HTTPException(502, str(e))
  ```

- [ ] Реализовать аутентификацию
  ```python
  # api/auth.py
  from fastapi import Security
  from fastapi.security.api_key import APIKeyHeader

  api_key_header = APIKeyHeader(name="X-API-Key")

  async def get_api_key(
      api_key: str = Security(api_key_header),
      db: Database = Depends(get_db)
  ) -> str:
      if not await db.validate_api_key(api_key):
          raise HTTPException(401, "Invalid API key")
      return api_key
  ```

#### Тестирование
- [ ] Unit тесты
  ```python
  # tests/unit/test_api.py
  async def test_create_chat_completion():
      app.dependency_overrides[get_router] = lambda: MockRouter()
      app.dependency_overrides[get_api_key] = lambda: "test-key"

      response = await client.post(
          "/v1/chat/completions",
          json={
              "messages": [{"role": "user", "content": "Hello"}],
              "model": "gigachat"
          },
          headers={"X-API-Key": "test-key"}
      )

      assert response.status_code == 200
      assert response.json()["choices"][0]["message"]["content"]

  async def test_invalid_api_key():
      response = await client.post(
          "/v1/chat/completions",
          json={...},
          headers={"X-API-Key": "invalid"}
      )
      assert response.status_code == 401
  ```

- [ ] Интеграционные тесты
  ```python
  # tests/integration/test_api.py
  async def test_full_api_flow():
      # Создаем тестовое приложение
      app = create_test_app()
      client = TestClient(app)

      # Создаем тестовый API ключ
      api_key = await create_test_api_key()

      # Тестируем запрос
      response = await client.post(
          "/v1/chat/completions",
          json={
              "messages": [{"role": "user", "content": "Test message"}],
              "model": "gigachat"
          },
          headers={"X-API-Key": api_key}
      )

      assert response.status_code == 200
      data = response.json()
      assert data["choices"][0]["message"]["content"]
      assert data["usage"]["total_tokens"] > 0

      # Проверяем запись использования
      usage = await get_test_usage(api_key)
      assert usage.tokens.total == data["usage"]["total_tokens"]
  ```

#### Критерии приемки
- [ ] API работает корректно
  - Все endpoints доступны
  - Валидация работает
  - Ошибки возвращаются правильно
- [ ] Аутентификация надежна
  - API ключи проверяются
  - Rate limiting работает
  - Безопасность обеспечена
- [ ] Производительность
  - Latency < 500ms
  - Concurrent requests работают
  - Rate limiting эффективен

## 3. Развертывание

### 3.1. Подготовка
- [ ] Создать конфигурацию
  ```python
  # core/config.py
  class Settings(BaseSettings):
      # Database
      SQLITE_URL: str = "sqlite:///xrouter.db"

      # Redis
      REDIS_URL: str = "redis://localhost:6379"

      # GigaChat
      GIGACHAT_API_KEY: str
      GIGACHAT_BASE_URL: str = "https://gigachat.api.url"

      # API
      API_CORS_ORIGINS: list[str] = ["*"]
      API_RATE_LIMIT: int = 100  # requests per minute

      class Config:
          env_file = ".env"
  ```

- [ ] Подготовить Docker
  ```dockerfile
  FROM python:3.11-slim

  WORKDIR /app

  RUN pip install poetry
  COPY pyproject.toml poetry.lock ./
  RUN poetry install --no-dev

  COPY . .

  CMD ["poetry", "run", "uvicorn", "xrouter.api.app:app", "--host", "0.0.0.0"]
  ```

### 3.2. Проверка
- [ ] Функциональное тестирование
  - Все endpoints работают
  - Аутентификация работает
  - Использование записывается
- [ ] Нагрузочное тестирование
  - 100 RPS выдерживает
  - Latency в норме
  - Ошибок нет
- [ ] Мониторинг работает
  - Метрики собираются
  - Графики строятся
  - Алерты настроены

## 4. Критерии приемки Release 1.0

### 4.1. Функциональные требования
- [ ] API Gateway работает и доступен
- [ ] API key аутентификация работает корректно
- [ ] Учет токенов и кредитов точный
- [ ] GigaChat интеграция работает
- [ ] Маршрутизация работает правильно
- [ ] Мониторинг предоставляет данные

### 4.2. Нефункциональные требования
- [ ] Latency < 500ms (без учета времени провайдера)
- [ ] Error rate < 1%
- [ ] Успешная обработка 100 req/s
- [ ] Документация полная и актуальная
- [ ] Мониторинг предоставляет все необходимые метрики
