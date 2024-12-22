# XRouter API Specification

## Overview
XRouter предоставляет OpenAI-совместимый API для доступа к различным российским LLM моделям. API построен по принципам REST и поддерживает как синхронные, так и streaming запросы.

## Base URL
```
https://api.xrouter.ru/v1
```

## Authentication
API использует Bearer token аутентификацию:
```http
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Chat Completions
```http
POST /v1/chat/completions
```

Основной эндпоинт для взаимодействия с моделями.

#### Request
```typescript
interface ChatCompletionRequest {
  // Обязательные параметры
  model: string;              // Идентификатор модели (например, "gigachat/pro")
  messages: Message[];        // Массив сообщений

  // Опциональные параметры
  temperature?: number;       // Диапазон: [0.0, 2.0], по умолчанию 1.0
  max_tokens?: number;       // Максимальное количество токенов
  stream?: boolean;          // Включить streaming ответов
  
  // Параметры маршрутизации
  provider?: {
    order?: string[];        // Приоритет провайдеров
    allow_fallbacks?: boolean; // Разрешить фоллбэки
    require_parameters?: boolean; // Требовать поддержку всех параметров
    data_collection?: "allow" | "deny"; // Политика сбора данных
  };

  // Дополнительные параметры
  tools?: Tool[];           // Инструменты для function calling
  response_format?: {       // Формат ответа
    type: "json_object" | "text"
  };
}

interface Message {
  role: "system" | "user" | "assistant" | "tool";
  content: string | ContentPart[];
  name?: string;           // Опционально для non-OpenAI моделей
}

interface ContentPart {
  type: "text" | "image_url";
  text?: string;
  image_url?: {
    url: string;          // URL или base64 изображения
    detail?: string;      // Опционально, по умолчанию "auto"
  };
}

interface Tool {
  type: "function";
  function: {
    name: string;
    description?: string;
    parameters: object;   // JSON Schema
  };
}
```

#### Response
```typescript
interface ChatCompletionResponse {
  id: string;
  object: "chat.completion" | "chat.completion.chunk";
  created: number;
  model: string;
  choices: {
    index: number;
    message: {
      role: string;
      content: string;
      tool_calls?: ToolCall[];
    };
    finish_reason: string;
  }[];
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

interface ToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: string;
  };
}
```

### 2. Models
```http
GET /v1/models
```

Получение списка доступных моделей.

#### Parameters
- supported_parameters (query, optional): Фильтр по поддерживаемым параметрам

#### Response
```typescript
interface ModelsResponse {
  data: {
    id: string;
    name: string;
    created: number;
    description: string;
    pricing: {
      prompt: string;
      completion: string;
      request: string;
    };
    context_length: number;
    architecture: {
      tokenizer: string;
      instruct_type: string;
      modality: string;
    };
    top_provider: {
      context_length: number;
      max_completion_tokens: number;
      is_moderated: boolean;
    };
    per_request_limits: {
      prompt_tokens: number | null;
      completion_tokens: number | null;
    };
  }[];
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
    streamed: boolean;
    generation_time: number;
    created_at: string;
    tokens_prompt: number;
    tokens_completion: number;
    native_tokens_prompt: number;
    native_tokens_completion: number;
    total_cost: number;
    cache_discount: number | null;
  };
}
```

### 4. Parameters
```http
GET /v1/parameters/{modelId}
```

Получение поддерживаемых параметров для модели.

#### Parameters
- modelId (path, required): ID модели
- provider (query, optional): Имя провайдера

#### Response
```typescript
interface ParametersResponse {
  data: {
    model: string;
    supported_parameters: string[];
    temperature_p50: number;
    top_p_p50: number;
    frequency_penalty_p50: number;
    presence_penalty_p50: number;
    // ... другие параметры
  };
}
```

### 5. Authentication
```http
GET /v1/auth/key
```

Проверка API ключа и получение информации о лимитах.

#### Response
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

## Error Handling

### Error Response Format
```typescript
interface ErrorResponse {
  error: {
    code: number;
    message: string;
    metadata?: Record<string, unknown>;
  };
}
```

### Common Error Codes
- 400: Bad Request (неверные параметры)
- 401: Invalid credentials (неверный API ключ)
- 402: Insufficient credits
- 403: Content moderation failed
- 408: Request timeout
- 429: Rate limit exceeded
- 502: Provider error
- 503: No available providers

### Moderation Errors
```typescript
interface ModerationErrorMetadata {
  reasons: string[];
  flagged_input: string;
  provider_name: string;
  model_slug: string;
}
```

### Provider Errors
```typescript
interface ProviderErrorMetadata {
  provider_name: string;
  raw: unknown;
}
```

## Rate Limiting
- Free tier: 20 req/min, 200 req/day
- Paid tier: 1 req/credit/sec до 500 req/sec
- DDoS protection через Cloudflare

## Streaming
Поддерживается Server-Sent Events (SSE) для streaming ответов.
- Установите `stream: true` в запросе
- Обрабатывайте события в формате SSE
- Игнорируйте комментарии ": OPENROUTER PROCESSING"

## Caching
- Автоматическое кэширование для поддерживаемых провайдеров
- Cache control через HTTP заголовки
- Поддержка cache breakpoints для больших промптов