# Provider API Specification

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

## Chat Completions API

### Endpoint
```http
POST /v1/chat/completions
```

Основной эндпоинт для взаимодействия с моделями.

### Request
```typescript
interface ChatCompletionRequest {
  // Обязательные параметры - один из двух (взаимоисключающие):
  messages?: Message[];        // Массив сообщений
  prompt?: string;            // Текстовый промпт (альтернатива messages)

  // Модель (обязательно)
  model: string;              // ID модели (например, "gigachat-pro")

  // Базовые параметры (поддерживаются всеми провайдерами)
  temperature?: number;       // Диапазон: [0.0, 2.0], по умолчанию 1.0
  max_tokens?: number;       // Максимальное количество токенов
  stream?: boolean;          // Включить streaming ответов
  repetition_penalty?: number; // Диапазон: (0, 2], штраф за повторения

  // Дополнительные параметры (поддержка зависит от провайдера)
  top_p?: number;           // Диапазон: (0, 1], поддерживается GigaChat

  // Function calling
  tools?: Tool[];           // Инструменты для function calling
  tool_choice?: "none" | "auto" | { type: "function"; function: { name: string } };

  // Формат ответа
  response_format?: {
    type: "json_object" | "text"
  };
}

interface Message {
  role: "system" | "user" | "assistant" | "tool";
  content: string | ContentPart[];
  name?: string;           // Опционально для non-OpenAI моделей
  tool_call_id?: string;   // Для сообщений с ролью tool
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
    few_shot_examples?: Array<{
      request: string;
      params: object;
    }>;
  };
}
```

### Response
```typescript
interface ChatCompletionResponse {
  id: string;
  object: "chat.completion" | "chat.completion.chunk";
  created: number;
  model: string;
  system_fingerprint?: string;
  choices: {
    index: number;
    message: {
      role: string;
      content: string;
      tool_calls?: ToolCall[];
    };
    finish_reason: "stop" | "length" | "tool_calls" | "content_filter" | null;
    delta?: {              // Только для streaming
      content?: string;
      role?: string;
      tool_calls?: ToolCall[];
    };
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

## Поддерживаемые модели

### GigaChat
- GigaChat (Lite) - легкая модель для простых задач
- GigaChat-Pro - продвинутая модель для сложных задач
- GigaChat-Max - продвинутая модель для задач с высокими требованиями

Особенности:
- Контекст: 32768 токенов
- Поддержка мультимодальности (текст + изображения)
- Нативная поддержка function calling
- Полная поддержка всех параметров

### YandexGPT
- yandexgpt-lite - стандартная модель
- yandexgpt - продвинутая модель
- yandexgpt-32k - модель с расширенным контекстом

Версии:
- latest - стабильная версия
- rc - ранний доступ к новым возможностям
- deprecated - устаревшая версия (поддержка 1 месяц)

Особенности:
- Контекст: 8192 токенов (32k для yandexgpt-32k)
- Только текстовый ввод
- Эмуляция function calling через промпты

## Поддержка параметров провайдерами

| Параметр | GigaChat | YandexGPT | Примечания |
|----------|----------|-----------|------------|
| temperature | ✅ | ✅ | |
| max_tokens | ✅ | ✅ | |
| stream | ✅ | ✅ | |
| top_p | ✅ | ❌ | |
| repetition_penalty | ✅ | ✅ | |
| prompt | ✅* | ✅* | *Конвертируется в messages |
| messages | ✅ | ✅ | |
| tools | ✅ | ✅* | *Эмулируется через промпты |
| tool_choice | ✅ | ✅* | *Эмулируется через промпты |

## Streaming

Поддерживается Server-Sent Events (SSE) для streaming ответов:
- Установите `stream: true` в запросе
- Обрабатывайте события в формате SSE

Пример streaming ответа:
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1694268190,
  "model": "gigachat-pro",
  "choices": [{
    "index": 0,
    "delta": {
      "content": "Hello"
    }
  }]
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
      flagged_input?: string;
      model_slug?: string;
    };
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
- 503: Service Unavailable

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