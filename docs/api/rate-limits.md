# XRouter Rate Limiting

## Overview

XRouter использует многоуровневую систему rate limiting для обеспечения справедливого использования ресурсов и защиты от перегрузок.

## Лимиты

### API Key Limits
| Тип | Запросов в минуту | Запросов в день | Конкурентных запросов |
|-----|-------------------|-----------------|----------------------|
| Free | 20 | 200 | 5 |
| Pro | 100 | 1000 | 20 |
| Enterprise | Custom | Custom | Custom |

### Model Limits
| Модель | Токенов на запрос | Токенов в минуту | Токенов в день |
|--------|-------------------|------------------|----------------|
| gigachat-pro | 4000 | 100000 | 1000000 |
| gigachat-plus | 4000 | 50000 | 500000 |
| gigachat-basic | 2000 | 20000 | 200000 |
| yandexgpt:latest | 4000 | 100000 | 1000000 |
| yandexgpt-lite:latest | 2000 | 50000 | 500000 |

## Rate Limit Headers

XRouter возвращает следующие заголовки с информацией о лимитах:

```http
X-RateLimit-Limit: 100        # Лимит запросов
X-RateLimit-Remaining: 95     # Осталось запросов
X-RateLimit-Reset: 1640995200 # Время сброса (Unix timestamp)
```

## Превышение лимитов

При превышении лимитов API возвращает ошибку 429 Too Many Requests:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded",
    "details": {
      "retry_after": 30,
      "limit": 100,
      "remaining": 0,
      "reset": 1640995200
    }
  }
}
```

## Стратегии

### Retry Strategy
1. Exponential backoff с jitter
2. Максимум 3 попытки
3. Учет заголовка Retry-After

### Burst Handling
1. Token bucket алгоритм
2. Возможность краткосрочного превышения
3. Сглаживание пиков нагрузки

## Мониторинг

### Метрики
- Requests per minute (RPM)
- Tokens per minute (TPM)
- Rate limit hits
- Concurrent requests

### Алерты
- Приближение к лимиту (80%)
- Превышение лимита
- Аномальное использование

## Best Practices

### Оптимизация запросов
1. Батчинг запросов где возможно
2. Кэширование частых запросов
3. Правильный выбор модели

### Обработка ошибок
1. Реализация retry логики
2. Fallback на другие модели
3. Graceful degradation

### Мониторинг использования
1. Отслеживание метрик
2. Настройка алертов
3. Планирование мощностей

## Enterprise Options

### Custom Limits
- Увеличенные лимиты RPM/TPM
- Больше конкурентных запросов
- Приоритетная обработка

### SLA
- 99.9% доступность
- Поддержка 24/7
- Выделенные ресурсы

### Support
- Технический аккаунт менеджер
- Приоритетная поддержка
- Custom интеграции