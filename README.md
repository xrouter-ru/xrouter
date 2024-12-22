# XRouter

XRouter - это универсальный API Gateway для российских LLM моделей, предоставляющий единый OpenAI-совместимый интерфейс для работы с различными провайдерами.

## Возможности

- 🔄 OpenAI-совместимый API
- 🔐 OAuth 2.0 с PKCE и API ключи
- 🚦 Интеллектуальная маршрутизация
- 📊 Прозрачная тарификация
- 📈 Мониторинг и метрики

## Поддерживаемые модели

### GigaChat
- gigachat-pro
- gigachat-plus
- gigachat-basic

### YandexGPT
- yandexgpt:latest       # Pro версия
- yandexgpt:rc          # Release Candidate
- yandexgpt:deprecated  # Предыдущая версия

- yandexgpt-lite:latest
- yandexgpt-lite:rc
- yandexgpt-lite:deprecated

- yandexgpt-32k:latest
- yandexgpt-32k:rc
- yandexgpt-32k:deprecated

## Документация

### API
- [Спецификация API](docs/api/api-spec.md)
- [Параметры API](docs/api/api-parameters.md)
- [Примеры использования](docs/api/api-examples.md)
- [Маппинг провайдеров](docs/api/provider-mapping.md)
- [Спецификации провайдеров](docs/api/provider-api-spec.md)
- [Спецификация роутера](docs/api/router-api-spec.md)
- [Обработка ошибок](docs/api/errors.md)
- [Rate Limits](docs/api/rate-limits.md)
- [Аутентификация](docs/api/auth.md)

### Архитектура
- [Обзор системы](docs/architecture/system-overview.md)
- [Компоненты](docs/architecture/components.md)
- [Потоки данных](docs/architecture/data-flow.md)
- [Развертывание](docs/architecture/deployment.md)
- [Мониторинг](docs/architecture/monitoring.md)
- [Безопасность](docs/architecture/security.md)
- [Масштабирование](docs/architecture/scaling.md)

### Roadmap
- [План релизов](docs/roadmap/release-plan.md)
- [MVP план](docs/roadmap/mvp-release-plan.md)
- [MVP roadmap](docs/roadmap/mvp-roadmap.md)
- [SOP релиза 1.0](docs/roadmap/sop-release-1.0.md)
- [SOP релиза 1.1](docs/roadmap/sop-release-1.1.md)
- [SOP релиза 1.2](docs/roadmap/sop-release-1.2.md)
- [Гайд по миграции](docs/roadmap/migration-guide.md)
- [Стратегия тестирования](docs/roadmap/testing-strategy.md)

## Быстрый старт

### Установка
```bash
# Python
pip install openai

# Node.js
npm install openai
```

### Использование
```python
from openai import OpenAI

# API ключ
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.xrouter.ru/v1"
)

# OAuth токен
client = OpenAI(
    api_key="Bearer your-oauth-token",
    base_url="https://api.xrouter.ru/v1"
)

response = client.chat.completions.create(
    model="gigachat-pro",  # или yandexgpt:latest
    messages=[
        {"role": "user", "content": "Привет!"}
    ]
)

print(response.choices[0].message.content)
```

## Разработка

### Требования
- Python 3.11+ (MVP)
- Go 1.21+ (Production)
- Redis
- SQLite/PostgreSQL

### Локальная разработка
```bash
# Клонирование репозитория
git clone https://github.com/xrouter-ru/xrouter.git
cd xrouter

# Установка зависимостей
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск тестов
pytest

# Запуск линтеров
flake8
black .
isort .
```

## Дополнительные ресурсы

### Основные документы
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Terms of Service](TERMS.md)
- [Privacy Policy](PRIVACY.md)
- [Changelog](CHANGELOG.md)

### Поддержка
- [GitHub Issues](https://github.com/xrouter-ru/xrouter/issues)
- [Telegram Support](https://t.me/xrouter_support)
- Email: support@xrouter.ru

## Лицензия

XRouter распространяется под лицензией MIT. Смотрите [LICENSE](LICENSE) для деталей.