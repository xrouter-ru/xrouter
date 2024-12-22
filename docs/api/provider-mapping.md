# Provider Mapping

Документ описывает как XRouter маппит универсальный API на конкретные провайдеры.

## Параметры запросов

### GigaChat

| XRouter параметр | GigaChat параметр | Примечания |
|-----------------|-------------------|------------|
| temperature | temperature | Поддерживается напрямую |
| max_tokens | max_tokens | Поддерживается напрямую |
| stream | stream | Поддерживается напрямую |
| top_p | top_p | Поддерживается напрямую |
| repetition_penalty | repetition_penalty | Поддерживается напрямую |
| prompt | messages | Конвертируется в одно сообщение с role: "user" |
| messages | messages | Поддерживается напрямую |
| tools | functions | Маппится на functions GigaChat |
| tool_choice | function_call | Маппится на function_call GigaChat |

### YandexGPT

| XRouter параметр | YandexGPT параметр | Примечания |
|-----------------|-------------------|------------|
| temperature | temperature | Поддерживается напрямую |
| max_tokens | maxTokens | Поддерживается напрямую |
| stream | stream | Поддерживается напрямую |
| repetition_penalty | repetition_penalty | Поддерживается напрямую |
| prompt | messages | Конвертируется в одно сообщение с role: "user" |
| messages | messages | Маппинг content -> text |
| tools | - | Эмулируется через промпты |
| tool_choice | - | Эмулируется через промпты |

## Маппинг prompt и messages

XRouter поддерживает два взаимоисключающих способа отправки запроса:

1. Через параметр prompt (простой текстовый запрос):
```typescript
{
  "prompt": "Привет, как дела?",
  "temperature": 0.7
}
```

2. Через параметр messages (полный контроль над контекстом):
```typescript
{
  "messages": [
    {"role": "system", "content": "Ты дружелюбный ассистент"},
    {"role": "user", "content": "Привет, как дела?"}
  ],
  "temperature": 0.7
}
```

В запросе должен быть указан ТОЛЬКО ОДИН из этих параметров. Если указаны оба, возвращается ошибка 400 Bad Request.

### Маппинг для GigaChat

```typescript
// Запрос с prompt
{
  "prompt": "Привет, как дела?",
  "temperature": 0.7
}

// Преобразуется в:
{
  "messages": [
    {
      "role": "user",
      "content": "Привет, как дела?"
    }
  ],
  "temperature": 0.7
}

// Запрос с messages передается как есть
{
  "messages": [...],
  "temperature": 0.7
}
```

### Маппинг для YandexGPT

```typescript
// Запрос с prompt
{
  "prompt": "Привет, как дела?",
  "temperature": 0.7
}

// Преобразуется в:
{
  "messages": [
    {
      "role": "user", 
      "text": "Привет, как дела?"
    }
  ],
  "completionOptions": {
    "temperature": 0.7
  }
}

// Запрос с messages
{
  "messages": [
    {"role": "system", "content": "Ты дружелюбный ассистент"},
    {"role": "user", "content": "Привет!"}
  ]
}

// Преобразуется в:
{
  "messages": [
    {"role": "system", "text": "Ты дружелюбный ассистент"},
    {"role": "user", "text": "Привет!"}
  ]
}
```

## Function Calling

### GigaChat
GigaChat поддерживает function calling нативно. XRouter маппит параметры следующим образом:

```typescript
// XRouter запрос
{
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get weather in city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        }
      }
    }
  }]
}

// Преобразуется в GigaChat запрос
{
  "functions": [{
    "name": "get_weather", 
    "description": "Get weather in city",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {"type": "string"}
      }
    }
  }]
}
```

### YandexGPT
YandexGPT не поддерживает function calling нативно. XRouter эмулирует эту функциональность через промпты:

1. Для каждой функции генерируется описание в формате промпта
2. Ответ модели парсится для извлечения аргументов
3. XRouter форматирует ответ в формате function calling

Пример:
```typescript
// XRouter запрос с функцией
{
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get weather in city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        }
      }
    }
  }]
}

// Преобразуется в YandexGPT промпт
{
  "messages": [
    {
      "role": "system",
      "text": "Ты должен отвечать в формате JSON с полями, соответствующими функции get_weather. Функция принимает параметр city типа string."
    },
    {
      "role": "user", 
      "text": "Какая погода в Москве?"
    }
  ]
}
```

## Streaming

### GigaChat
GigaChat поддерживает streaming через SSE. XRouter напрямую транслирует события от GigaChat клиенту.

### YandexGPT
YandexGPT поддерживает streaming через параметр stream. XRouter преобразует ответы в формат SSE.

## Обработка ошибок

XRouter унифицирует коды ошибок от провайдеров:

| XRouter код | GigaChat | YandexGPT | Описание |
|------------|----------|-----------|-----------|
| 400 | 400 | 400 | Неверные параметры |
| 401 | 401 | 401 | Ошибка авторизации |
| 402 | 402 | - | Недостаточно средств |
| 429 | 429 | 429 | Превышен лимит запросов |
| 500 | 500 | 500 | Внутренняя ошибка |

## Рекомендации по использованию

1. Используйте только базовые параметры (temperature, max_tokens, stream) для максимальной совместимости
2. Для function calling предпочтительно использовать GigaChat
3. При необходимости использовать расширенные параметры, проверяйте их поддержку через endpoint /parameters/{modelId}
4. Для streaming используйте стандартный формат SSE
5. Используйте messages вместо prompt для лучшего контроля над контекстом диалога
6. В одном запросе используйте только один из параметров: prompt или messages

## Поддержка параметров по провайдерам

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