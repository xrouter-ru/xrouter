# XRouter API Examples

## Базовые примеры

### Простой запрос к модели
```typescript
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [
      {
        role: "user",
        content: "Привет! Как дела?"
      }
    ]
  })
});
```

### Streaming ответ
```typescript
const response = await fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [
      {
        role: "user",
        content: "Напиши длинную историю о космосе"
      }
    ],
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {value, done} = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      // Обработка chunk'а
      console.log(data.choices[0].delta.content);
    }
  }
}
```

## Продвинутые сценарии

### Маршрутизация запросов
```typescript
// Приоритет провайдеров
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [{
      role: "user",
      content: "Анализ текста на русском языке"
    }],
    provider: {
      order: ["GigaChat", "YandexGPT"],
      allow_fallbacks: true
    }
  })
});

// Требование поддержки параметров
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [{
      role: "user",
      content: "Генерация JSON"
    }],
    provider: {
      require_parameters: true
    },
    response_format: {
      type: "json_object"
    }
  })
});
```

### Function Calling
```typescript
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [{
      role: "user",
      content: "Какая погода в Москве?"
    }],
    tools: [{
      type: "function",
      function: {
        name: "get_weather",
        description: "Получить текущую погоду",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "Город"
            },
            units: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"]
        }
      }
    }]
  })
});
```

### Мультимодальные запросы
```typescript
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro-vision",
    messages: [{
      role: "user",
      content: [
        {
          type: "text",
          text: "Что на этой картинке?"
        },
        {
          type: "image_url",
          image_url: {
            url: "data:image/jpeg;base64,..."
          }
        }
      ]
    }]
  })
});
```

### Структурированные ответы
```typescript
fetch("https://api.xrouter.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gigachat/pro",
    messages: [{
      role: "user",
      content: "Проанализируй текст и верни структурированный ответ"
    }],
    response_format: {
      type: "json_schema",
      json_schema: {
        type: "object",
        properties: {
          sentiment: {
            type: "string",
            enum: ["positive", "negative", "neutral"]
          },
          keywords: {
            type: "array",
            items: { type: "string" }
          },
          summary: {
            type: "string"
          }
        },
        required: ["sentiment", "keywords", "summary"]
      }
    }
  })
});
```

## Обработка ошибок

### Retry механизм
```typescript
async function makeRequestWithRetry(payload, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch("https://api.xrouter.ru/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const error = await response.json();
        
        // Не повторяем запрос при определенных ошибках
        if (error.error.code === 401 || error.error.code === 403) {
          throw new Error(error.error.message);
        }
        
        // Для остальных ошибок пробуем еще раз
        continue;
      }

      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      // Экспоненциальная задержка
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
}
```

### Отмена запроса
```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 sec timeout

try {
  const response = await fetch("https://api.xrouter.ru/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gigachat/pro",
      messages: [{
        role: "user",
        content: "Длинный запрос..."
      }],
      stream: true
    }),
    signal: controller.signal
  });

  clearTimeout(timeoutId);
  
  // Обработка ответа
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request was aborted');
  } else {
    console.error('Request failed:', error);
  }
}
```

## SDK Examples

### Python (OpenAI SDK)
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

### Node.js (OpenAI SDK)
```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'your-api-key',
  baseURL: 'https://api.xrouter.ru/v1'
});

const response = await openai.chat.completions.create({
  model: 'gigachat/pro',
  messages: [
    { role: 'user', content: 'Привет!' }
  ]
});

console.log(response.choices[0].message.content);