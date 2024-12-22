# XRouter API Specification

## Overview
XRouter предоставляет API для работы с различными российскими LLM провайдерами. API разделен на две части:

1. [Router API](router-api-spec.md) - эндпоинты для управления системой:
   - Получение списка моделей
   - Управление параметрами
   - Статистика генераций
   - Авторизация и лимиты
   - Статус провайдеров

2. [Provider API](provider-api-spec.md) - эндпоинты для работы с моделями:
   - Chat completions
   - Streaming
   - Function calling
   - Особенности провайдеров

## Base URL
```
https://api.xrouter.ru/v1
```

## Authentication
API использует Bearer token аутентификацию:
```http
Authorization: Bearer YOUR_API_KEY
```

## Поддерживаемые провайдеры

### GigaChat
- GigaChat (Lite) - легкая модель для простых задач
- GigaChat-Pro - продвинутая модель для сложных задач
- GigaChat-Max - продвинутая модель для задач с высокими требованиями
- Особенности:
  - Контекст: 32768 токенов для всех моделей
  - Поддержка: streaming, function calling, json mode
  - Нативная поддержка всех параметров

### YandexGPT
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

## Rate Limiting

### Free tier
- 20 req/min
- 200 req/day

### Paid tier
- 1 req/credit/sec до 500 req/sec
- Для более высоких лимитов необходимо связаться с поддержкой