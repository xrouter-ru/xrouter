# XRouter Authentication

## Overview

XRouter поддерживает два метода аутентификации:
1. OAuth 2.0 с PKCE для веб-приложений
2. API ключи для сервисных приложений

## OAuth 2.0

### Flow
1. Клиент генерирует PKCE challenge
2. Получает код авторизации
3. Обменивает код на токен
4. Использует токен для API запросов

### Endpoints
```
Authorization: https://auth.xrouter.ru/authorize
Token: https://auth.xrouter.ru/token
```

### PKCE Flow Example
```python
import secrets
import base64
import hashlib

# 1. Генерация code_verifier
code_verifier = secrets.token_urlsafe(32)

# 2. Создание code_challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip('=')

# 3. Авторизация
auth_url = (
    "https://auth.xrouter.ru/authorize"
    "?response_type=code"
    "&client_id=YOUR_CLIENT_ID"
    "&redirect_uri=YOUR_REDIRECT_URI"
    "&code_challenge=" + code_challenge +
    "&code_challenge_method=S256"
)

# 4. Обмен кода на токен
token_response = requests.post(
    "https://auth.xrouter.ru/token",
    data={
        "grant_type": "authorization_code",
        "code": auth_code,
        "code_verifier": code_verifier,
        "client_id": "YOUR_CLIENT_ID",
        "redirect_uri": "YOUR_REDIRECT_URI"
    }
)
```

### OAuth Токены
- Время жизни: 1 год
- Автоматический отзыв при разлогине
- Возможность ручного отзыва
- Поддержка refresh токенов не требуется

## API Keys

### Создание ключей
1. Через UI управления
2. Через API (требует OAuth токен)
3. Через поддержку (для enterprise)

### Формат ключей
```
xr-{tier}-{random}-{checksum}
Пример: xr-pro-a1b2c3d4-xyz789
```

### Использование
```python
from openai import OpenAI

# API ключ
client = OpenAI(
    api_key="xr-pro-a1b2c3d4-xyz789",
    base_url="https://api.xrouter.ru/v1"
)

# OAuth токен
client = OpenAI(
    api_key="Bearer your-oauth-token",
    base_url="https://api.xrouter.ru/v1"
)
```

### Безопасность ключей
- Хранятся в хэшированном виде
- Не логируются в системе
- Могут быть отозваны в любой момент
- Поддерживают IP whitelist

## Rate Limiting

### OAuth токены
- Лимиты на уровне пользователя
- Учет всех токенов пользователя
- Возможность увеличения лимитов

### API ключи
- Лимиты на уровне ключа
- Независимые квоты
- Enterprise лимиты

## Security Best Practices

### OAuth
1. Всегда использовать PKCE
2. Безопасно хранить токены
3. Обрабатывать отзыв токенов
4. Использовать HTTPS

### API Keys
1. Не хранить в коде
2. Использовать переменные окружения
3. Регулярно ротировать ключи
4. Использовать минимальные права

## Мониторинг

### Метрики
- Активные токены
- Использование ключей
- Ошибки авторизации
- Rate limit hits

### Алерты
- Множественные ошибки auth
- Превышение rate limits
- Подозрительная активность
- Отозванные токены

## Enterprise Features

### SSO
- SAML 2.0
- OpenID Connect
- Active Directory

### Advanced Security
- IP whitelist
- Audit logs
- Custom token lifetime
- Hardware token support