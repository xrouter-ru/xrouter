# XRouter Error Handling

## Error Format

Все ошибки возвращаются в едином формате:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human readable message",
    "details": {
      "param": "value"
    }
  }
}
```

## Error Codes

### Authentication Errors (400-499)
- `auth_required`: Требуется аутентификация
- `invalid_token`: Невалидный токен
- `token_expired`: Токен истек
- `invalid_key`: Невалидный API ключ

### Rate Limit Errors
- `rate_limit_exceeded`: Превышен лимит запросов
- `quota_exceeded`: Превышена квота
- `concurrent_limit`: Превышен лимит параллельных запросов

### Provider Errors
- `provider_error`: Ошибка провайдера
- `provider_timeout`: Таймаут провайдера
- `provider_unavailable`: Провайдер недоступен
- `model_not_found`: Модель не найдена

### Validation Errors
- `invalid_request`: Невалидный запрос
- `invalid_model`: Невалидная модель
- `invalid_parameters`: Невалидные параметры
- `content_filter`: Контент не прошел фильтрацию

### System Errors (500-599)
- `internal_error`: Внутренняя ошибка
- `service_unavailable`: Сервис недоступен
- `database_error`: Ошибка базы данных
- `cache_error`: Ошибка кэша

## Error Handling

### Retry Strategy
1. Временные ошибки (429, 503) - retry с exponential backoff
2. Ошибки провайдера - fallback на другого провайдера
3. Постоянные ошибки (400, 401) - не retry

### Fallback Strategy
1. Попытка использовать альтернативную версию модели
2. Попытка использовать альтернативного провайдера
3. Возврат ошибки, если все попытки неуспешны

## Error Examples

### Authentication Error
```json
{
  "error": {
    "code": "invalid_token",
    "message": "The provided token is invalid",
    "details": {
      "token_type": "Bearer"
    }
  }
}
```

### Rate Limit Error
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests",
    "details": {
      "retry_after": 30,
      "limit": 100,
      "remaining": 0
    }
  }
}
```

### Provider Error
```json
{
  "error": {
    "code": "provider_error",
    "message": "Provider API error",
    "details": {
      "provider": "gigachat",
      "status": 503,
      "retry_after": 60
    }
  }
}