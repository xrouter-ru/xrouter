# SOP: XRouter MVP

## 1. Подготовка окружения

### 1.1. Настройка проекта
- [ ] Инициализация проекта
  - [ ] Создать структуру директорий
  - [ ] Настроить Poetry
  - [ ] Создать .gitignore
  - [ ] Настроить pre-commit hooks

### 1.2. Настройка разработки
- [ ] Установить зависимости
  ```toml
  [tool.poetry.dependencies]
  python = "^3.11"
  fastapi = "^0.104.1"
  uvicorn = "^0.24.0"
  sqlalchemy = "^2.0.23"
  pydantic = "^2.5.2"
  httpx = "^0.25.2"
  ```
- [ ] Настроить линтеры
  - [ ] black для форматирования
  - [ ] isort для импортов
  - [ ] flake8 для проверки кода
- [ ] Настроить pytest
  - [ ] pytest-asyncio
  - [ ] pytest-cov
  - [ ] pytest-env

### 1.3. Настройка CI
- [ ] Настроить GitHub Actions
  - [ ] Линтинг
  - [ ] Тесты
  - [ ] Coverage отчеты
- [ ] Настроить pre-commit hooks
  - [ ] black
  - [ ] isort
  - [ ] flake8

## 2. Разработка API Gateway

### 2.1. Базовая структура
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
    └── providers/
        ├── __init__.py
        └── gigachat.py
```

### 2.2. API endpoints
- [ ] Реализовать базовые endpoints
  ```python
  @router.post("/chat/completions")
  async def create_chat_completion(
      request: ChatCompletionRequest,
      api_key: str = Depends(get_api_key)
  ) -> ChatCompletionResponse:
      pass
  ```
- [ ] Добавить валидацию
- [ ] Добавить обработку ошибок
- [ ] Настроить CORS

### 2.3. Аутентификация
- [ ] Реализовать API Key аутентификацию
  ```python
  class APIKey(BaseModel):
      key: str
      user_id: str
      created_at: datetime
      is_active: bool
  ```
- [ ] Добавить валидацию ключей
- [ ] Реализовать rate limiting
- [ ] Добавить логирование доступа

## 3. Интеграция с GigaChat

### 3.1. GigaChat клиент
- [ ] Реализовать базовый клиент
  ```python
  class GigaChatClient:
      def __init__(self, api_key: str):
          self.api_key = api_key
          self.base_url = "https://gigachat.api.url"
          self.client = httpx.AsyncClient()

      async def create_completion(
          self,
          messages: List[Message],
          **kwargs
      ) -> CompletionResponse:
          pass
  ```
- [ ] Добавить аутентификацию
- [ ] Реализовать retry логику
- [ ] Добавить тесты

### 3.2. Обработка запросов/ответов
- [ ] Реализовать маппинг запросов
- [ ] Реализовать маппинг ответов
- [ ] Добавить валидацию
- [ ] Реализовать обработку ошибок

## 4. Роутинг

### 4.1. Базовый роутер
- [ ] Реализовать Router класс
  ```python
  class Router:
      def __init__(self):
          self.providers: Dict[str, BaseProvider] = {}
          
      async def route_request(
          self,
          request: ChatCompletionRequest
      ) -> ChatCompletionResponse:
          pass
  ```
- [ ] Добавить выбор провайдера
- [ ] Реализовать fallback логику
- [ ] Добавить метрики

### 4.2. Обработка ошибок
- [ ] Реализовать retry логику
- [ ] Добавить fallback механизмы
- [ ] Реализовать логирование ошибок
- [ ] Добавить алерты

## 5. Тестирование

### 5.1. Unit тесты
- [ ] Тесты API endpoints
- [ ] Тесты аутентификации
- [ ] Тесты GigaChat клиента
- [ ] Тесты роутера

### 5.2. Интеграционные тесты
- [ ] Тесты API Gateway
- [ ] Тесты GigaChat интеграции
- [ ] Тесты роутинга
- [ ] Тесты ошибок

### 5.3. Нагрузочные тесты
- [ ] Базовые тесты производительности
- [ ] Тесты под нагрузкой
- [ ] Тесты отказоустойчивости

## 6. Документация

### 6.1. API документация
- [ ] OpenAPI спецификация
- [ ] Примеры использования
- [ ] Описание ошибок
- [ ] Инструкции по аутентификации

### 6.2. Документация разработчика
- [ ] Инструкции по установке
- [ ] Гайд по разработке
- [ ] Описание архитектуры
- [ ] Примеры кода

## 7. Критерии приемки MVP

### 7.1. Функциональные требования
- [ ] API Gateway работает и доступен
- [ ] Аутентификация работает корректно
- [ ] GigaChat интеграция функционирует
- [ ] Роутинг работает правильно

### 7.2. Нефункциональные требования
- [ ] Latency < 500ms
- [ ] Error rate < 1%
- [ ] 100 req/s
- [ ] Memory < 500MB

### 7.3. Качество кода
- [ ] Тесты покрывают > 80% кода
- [ ] Все линтеры проходят
- [ ] Документация актуальна
- [ ] CI/CD работает