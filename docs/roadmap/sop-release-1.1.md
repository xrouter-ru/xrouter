# SOP: Release 1.1 - YandexGPT & OAuth

## 1. Подготовка инфраструктуры

### 1.1. Миграция на PostgreSQL
- [ ] Настроить PostgreSQL
  - [ ] Установить PostgreSQL
  - [ ] Создать базу данных
  - [ ] Настроить пользователей
- [ ] Подготовить миграцию данных
  ```sql
  -- Users для OAuth
  CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );

  -- API Keys с user_id
  CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
  );

  -- Usage с расширенной аналитикой
  CREATE TABLE usage (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,  -- Включая версию, например "yandexgpt-lite:latest"
    tokens_input INTEGER NOT NULL,
    tokens_output INTEGER NOT NULL,
    cost DECIMAL(10,6) NOT NULL,
    metadata JSONB,  -- Дополнительные метаданные использования
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
  );

  -- Provider Status с версиями
  CREATE TABLE provider_status (
    id UUID PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,  -- Включая версию
    status VARCHAR(20) NOT NULL,
    latency INTEGER,
    error_rate DECIMAL(5,2),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [ ] Реализовать миграцию данных
  - [ ] Скрипт миграции SQLite → PostgreSQL
  - [ ] Валидация данных
  - [ ] Тестовый прогон

### 1.2. Расширение Redis
- [ ] Обновить схемы кэширования
  - [ ] Добавить OAuth сессии
  - [ ] Расширить статистику использования
  - [ ] Добавить кэши для версий YandexGPT
- [ ] Обновить rate limiting
  - [ ] Добавить лимиты по пользователям
  - [ ] Настроить квоты по версиям
  - [ ] Обновить метрики

### 1.3. Обновление мониторинга
- [ ] Расширить метрики Prometheus
  - [ ] OAuth метрики
  - [ ] Метрики по версиям YandexGPT
  - [ ] Расширенные метрики использования
- [ ] Обновить дашборды Grafana
  - [ ] Панели OAuth статистики
  - [ ] Сравнение провайдеров
  - [ ] Аналитика использования

## 2. OAuth Implementation

### 2.1. OAuth Service
- [ ] Реализовать OAuth 2.0 с PKCE
  ```python
  class OAuthService:
      async def initiate_auth(self, client_id: str, code_challenge: str) -> str:
          pass

      async def handle_callback(self, code: str, code_verifier: str) -> Token:
          pass

      async def refresh_token(self, refresh_token: str) -> Token:
          pass

      async def revoke_token(self, token: str) -> None:
          pass
  ```
- [ ] Добавить управление пользователями
- [ ] Реализовать JWT токены
- [ ] Настроить безопасность

### 2.2. API Gateway Updates
- [ ] Добавить OAuth endpoints
  - [ ] /authorize endpoint
  - [ ] /token endpoint
  - [ ] /revoke endpoint
- [ ] Обновить аутентификацию
  - [ ] Поддержка Bearer JWT
  - [ ] Валидация токенов
  - [ ] Проверка scope

### 2.3. User Management
- [ ] Реализовать управление пользователями
  - [ ] Регистрация
  - [ ] Профили
  - [ ] API ключи
- [ ] Добавить UI для управления
  - [ ] Страница профиля
  - [ ] Управление ключами
  - [ ] Статистика использования

## 3. YandexGPT Integration

### 3.1. YandexGPT Provider
- [ ] Реализовать базовый адаптер
  - [ ] YandexGPTProvider класс
  - [ ] Аутентификация
  - [ ] API методы
- [ ] Добавить версионность
  - [ ] Поддержка :latest, :rc, :deprecated
  - [ ] Маппинг моделей
  - [ ] Обработка ошибок

### 3.2. Router Service Updates
- [ ] Обновить маршрутизацию
  - [ ] Поддержка версий
  - [ ] Приоритеты моделей
  - [ ] Fallback логика
- [ ] Расширить трансформацию
  - [ ] Маппинг параметров
  - [ ] Нормализация ответов
  - [ ] Обработка ошибок

## 4. Usage Analytics

### 4.1. Enhanced Usage Service
- [ ] Расширить функционал Usage Service
  ```python
  class UsageService:
      async def get_detailed_stats(
          self,
          user_id: UUID,
          period: Period,
          grouping: GroupBy
      ) -> DetailedStats:
          pass

      async def analyze_usage_patterns(
          self,
          user_id: UUID
      ) -> UsagePatterns:
          pass

      async def generate_usage_report(
          self,
          user_id: UUID,
          format: ReportFormat
      ) -> Report:
          pass
  ```
- [ ] Добавить аналитику
  - [ ] Паттерны использования
  - [ ] Прогнозирование расхода
  - [ ] Рекомендации оптимизации

### 4.2. Reporting System
- [ ] Реализовать систему отчетов
  - [ ] Ежедневные отчеты
  - [ ] Уведомления о лимитах
  - [ ] Экспорт данных
- [ ] Добавить визуализации
  - [ ] Графики использования
  - [ ] Сравнение провайдеров
  - [ ] Анализ трендов

## 5. Testing

### 5.1. Unit Testing
- [ ] OAuth тесты
  - [ ] PKCE flow
  - [ ] Token management
  - [ ] User management
- [ ] YandexGPT тесты
  - [ ] Provider functionality
  - [ ] Version handling
  - [ ] Error cases
- [ ] Analytics тесты
  - [ ] Usage calculation
  - [ ] Report generation
  - [ ] Data accuracy

### 5.2. Integration Testing
- [ ] OAuth integration
  - [ ] Full auth flow
  - [ ] Token refresh
  - [ ] Revocation
- [ ] YandexGPT integration
  - [ ] All model versions
  - [ ] Fallback scenarios
  - [ ] Performance
- [ ] Analytics integration
  - [ ] Data collection
  - [ ] Report generation
  - [ ] Alerting

## 6. Documentation

### 6.1. API Documentation
- [ ] OAuth documentation
  - [ ] Auth flows
  - [ ] Endpoints
  - [ ] Security
- [ ] YandexGPT documentation
  - [ ] Version support
  - [ ] Model differences
  - [ ] Best practices
- [ ] Analytics documentation
  - [ ] Available metrics
  - [ ] Report types
  - [ ] API endpoints

### 6.2. Migration Guide
- [ ] Database migration
  - [ ] Preparation steps
  - [ ] Execution process
  - [ ] Verification
- [ ] OAuth migration
  - [ ] User setup
  - [ ] Token migration
  - [ ] Testing steps
- [ ] Analytics migration
  - [ ] Data transfer
  - [ ] Report migration
  - [ ] Verification steps

## 7. Критерии приемки

### 7.1. Функциональные требования
- [ ] OAuth 2.0 с PKCE работает
- [ ] YandexGPT интеграция функционирует
- [ ] Миграция на PostgreSQL успешна
- [ ] Расширенная аналитика доступна
- [ ] Все версии моделей поддерживаются

### 7.2. Нефункциональные требования
- [ ] Latency < 500ms
- [ ] Error rate < 0.5%
- [ ] Успешная обработка 200 req/s
- [ ] Нулевая потеря данных при миграции
- [ ] Обратная совместимость API сохранена