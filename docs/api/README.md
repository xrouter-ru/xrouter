# XRouter API Documentation

## Обзор
XRouter предоставляет единый API для доступа к различным российским LLM моделям. API совместим с OpenAI Chat API, что позволяет легко интегрировать его с существующими приложениями и инструментами.

## Основные возможности
- OpenAI-совместимый API
- Поддержка российских LLM моделей (GigaChat, YandexGPT, и др.)
- Интеллектуальная маршрутизация запросов
- Streaming ответов
- Function calling
- Структурированные ответы в формате JSON
- Мультимодальные запросы (текст + изображения)

## Документация

### [API Specification](api-spec.md)
Полная спецификация API, включая:
- Endpoints
- Форматы запросов и ответов
- Аутентификация
- Обработка ошибок
- Rate limiting

### [API Parameters](api-parameters.md)
Детальное описание параметров API:
- Sampling параметры
- Ограничения моделей
- Поддержка параметров провайдерами
- Рекомендации по использованию

### [API Examples](api-examples.md)
Примеры использования API для различных сценариев:
- Базовые запросы
- Streaming
- Function calling
- Маршрутизация
- Обработка ошибок
- SDK примеры

## Quick Start

### Установка
```bash
# Python
pip install openai
# или
pip install xrouter-python  # Наш SDK (coming soon)

# Node.js
npm install openai
# или
npm install xrouter-node  # Наш SDK (coming soon)
```

### Базовый пример
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.xrouter.ru/v1"
)

response = client.chat.completions.create(
    model="gigachat/pro",
    messages=[
        {"role": "user", "content": "Привет!"}
    ]
)

print(response.choices[0].message.content)
```

## Поддерживаемые модели

### GigaChat
- gigachat/pro
- gigachat/plus
- gigachat/basic

### Yandex GPT
- yandex/yandexgpt
- yandex/yandexgpt-lite

### MTS AI
- mts/mts-llm
- mts/mts-llm-pro

### T-Bank
- tbank/gen-t

## Rate Limits
- Free tier: 20 req/min, 200 req/day
- Paid tier: 1 req/credit/sec до 500 req/sec
- DDoS protection через Cloudflare

## Безопасность
- Аутентификация через API ключи
- HTTPS для всех запросов
- Модерация контента
- Мониторинг подозрительной активности

## Поддержка
- [GitHub Issues](https://github.com/xrouter-ru/xrouter/issues)
- [Telegram Support](https://t.me/xrouter_support)
- Email: support@xrouter.ru

## Дополнительные ресурсы
- [Changelog](../CHANGELOG.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)
- [Terms of Service](../TERMS.md)
- [Privacy Policy](../PRIVACY.md)