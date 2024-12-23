# XRouter API Specification

## Overview
XRouter предоставляет API для доступа к российским LLM провайдерам, управления моделями и мониторинга.

## Release Plan

### Release 1.0 (Current)
- API key аутентификация
- GigaChat интеграция
- SQLite для хранения данных
- Redis для rate limiting

### Release 1.1 (Planned)
- OAuth 2.0 с PKCE
- YandexGPT интеграция
- Миграция на PostgreSQL
- Расширенное использование Redis

## Base URL
```
https://api.xrouter.ru/v1
```

## Authentication
API использует Bearer token аутентификацию:
```http
Authorization: Bearer YOUR_API_KEY
```

В Release 1.1 будет добавлена поддержка OAuth 2.0 с PKCE.

## Endpoints

### 1. Models
```http
GET /v1/models
```

Получение списка доступных моделей.

#### Parameters
- supported_parameters (query, optional): Фильтр по поддерживаемым параметрам
- provider (query, optional): Фильтр по провайдеру (gigachat, yandexgpt*)

*YandexGPT будет доступен в Release 1.1

#### Response
```typescript
interface ModelsResponse {
  data: {
    id: string;              // Например: "gigachat/pro"
    name: string;            // Человекочитаемое название
    provider: string;        // "gigachat" | "yandexgpt"*
    version: string;         // Для YandexGPT*: "latest" | "rc" | "deprecated"
    created: number;         // Unix timestamp
    description: string;     // Описание модели
    pricing: {
      prompt: string;        // Стоимость за 1K токенов промпта
      completion: string;    // Стоимость за 1K токенов ответа
    };
    context_length: number;  // Максимальная длина контекста
    architecture: {
      tokenizer: string;     // Используемый токенизатор
      instruct_type: string; // Тип инструкций
      modality: string;      // Поддерживаемые модальности (text, images)
    };
    limits: {
      max_tokens: number;    // Максимальное количество токенов в ответе
      max_images: number;    // Максимальное количество изображений в запросе
    };
    supported_features: string[]; // ["streaming", "function-calling", "json-mode"]
    supported_parameters: string[]; // Список поддерживаемых параметров
    default_parameters: {    // Значения по умолчанию
      temperature: number;
      top_p: number;
      repetition_penalty: number;
    };
  }[];
}
```

*Поля, связанные с YandexGPT, будут доступны в Release 1.1

### 2. Parameters
```http
GET /v1/parameters/{modelId}
```

Получение поддерживаемых параметров для модели.

#### Parameters
- modelId (path, required): ID модели (например, "gigachat/pro", "yandexgpt-lite:latest"*)

*YandexGPT модели будут доступны в Release 1.1

#### Response
```typescript
interface ParametersResponse {
  data: {
    model: string;
    supported_parameters: string[];
    temperature_p50: number;
    top_p_p50?: number;
    repetition_penalty_p50: number;
  };
}
```

### 3. Generation Stats
```http
GET /v1/generation
```

Получение статистики по конкретной генерации.

#### Parameters
- id (query, required): ID генерации

#### Response
```typescript
interface GenerationResponse {
  data: {
    id: string;
    model: string;
    provider: string;
    streamed: boolean;
    generation_time: number;
    created_at: string;
    tokens_prompt: number;
    tokens_completion: number;
    total_cost: number;
  };
}
```

### 4. Authentication

#### Get API Key Info
```http
GET /v1/auth/key
```

Проверка API ключа и получение информации о лимитах.

##### Response
```typescript
interface AuthKeyResponse {
  data: {
    label: string;
    usage: number;
    limit: number | null;
    is_free_tier: boolean;
    rate_limit: {
      requests: number;
      interval: string;
    };
  };
}
```

#### Create API Key
```http
POST /v1/auth/key
```

Создание нового API ключа.

##### Request
```typescript
interface CreateKeyRequest {
  label: string;           // Метка для ключа
  expires_at?: string;     // Опционально: дата истечения
}
```

##### Response
```typescript
interface CreateKeyResponse {
  data: {
    key: string;          // Новый API ключ
    label: string;
    created_at: string;
    expires_at?: string;
  };
}
```

#### Revoke API Key
```http
DELETE /v1/auth/key/{keyId}
```

Отзыв API ключа.

### 5. Provider Status
```http
GET /v1/providers/status
```

Получение статуса провайдеров.

#### Response
```typescript
interface ProviderStatusResponse {
  data: {
    gigachat: {
      status: "operational" | "degraded" | "down";
      latency: number;
      success_rate: number;
      last_updated: string;
    };
    // Release 1.1
    yandexgpt?: {
      status: "operational" | "degraded" | "down";
      latency: number;
      success_rate: number;
      last_updated: string;
    };
  };
}
```

## Error Handling

### Error Response Format
```typescript
interface ErrorResponse {
  error: {
    code: number;
    message: string;
    metadata?: {
      provider_name?: string;
      raw?: unknown;
      reasons?: string[];
    };
  };
}
```

### Common Error Codes
- 400: Bad Request (неверные параметры)
- 401: Invalid credentials (неверный API ключ)
- 402: Insufficient credits
- 429: Rate limit exceeded
- 500: Internal Server Error
- 503: Service Unavailable

## Rate Limiting
Rate limiting реализован с использованием Redis.

### Free tier
- 20 req/min
- 200 req/day

### Paid tier
- 1 req/credit/sec до 500 req/sec
- Для более высоких лимитов необходимо связаться с поддержкой

## Модели и провайдеры

### Release 1.0 - GigaChat
- GigaChat (Lite) - легкая модель для простых задач
- GigaChat-Pro - продвинутая модель для сложных задач
- GigaChat-Max - продвинутая модель для задач с высокими требованиями
- Особенности:
  - Контекст: 32768 токенов для всех моделей
  - Поддержка: streaming, function calling, json mode
  - Нативная поддержка всех параметров

### Release 1.1 - YandexGPT
- yandexgpt-lite - стандартная модель для задач в реальном времени
- yandexgpt - продвинутая модель для сложных запросов
- yandexgpt-32k - модель с расширенным контекстом
- Версии:
  - latest - стабильная версия
  - rc - ранний доступ к новым возможностям
  - deprecated - устаревшая версия (поддержка 1 месяц)
- Особенности:
  - Контекст: 8192 токенов (32k для yandexgpt-32k)
  - Поддержка: streaming, json mode
  - Эмуляция function calling через промпты

## Хранение данных

### Release 1.0
- SQLite
  - Хранение API ключей
  - Статистика использования
  - Логи генераций
- Redis
  - Rate limiting
  - Кэширование API ключей
  - Статусы провайдеров

### Release 1.1
- PostgreSQL
  - Миграция с SQLite
  - Улучшенная производительность
  - Поддержка сложных запросов
- Redis
  - Расширенное кэширование
  - Очереди задач
  - Распределенные блокировки