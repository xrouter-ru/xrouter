# XRouter API Parameters

## Основные параметры

### Temperature
- Key: `temperature`
- Тип: float
- Диапазон: [0.0, 2.0]
- По умолчанию: 1.0
- Поддержка: GigaChat ✓, YandexGPT ✓

Влияет на разнообразие ответов модели. Низкие значения делают ответы более предсказуемыми, высокие - более разнообразными. При 0 модель всегда дает одинаковый ответ на одинаковый ввод.

### Max Tokens
- Key: `max_tokens`
- Тип: integer
- Диапазон: [1, context_length - prompt_length]
- По умолчанию: Зависит от модели
- Поддержка: GigaChat ✓, YandexGPT ✓

Максимальное количество токенов в ответе.

### Stream
- Key: `stream`
- Тип: boolean
- По умолчанию: false
- Поддержка: GigaChat ✓, YandexGPT ✓

Включает потоковую генерацию ответа.

### Repetition Penalty
- Key: `repetition_penalty`
- Тип: float
- Диапазон: [0.0, 2.0]
- По умолчанию: 1.0
- Поддержка: GigaChat ✓, YandexGPT ✓

Помогает уменьшить повторения. Штраф основан на исходной вероятности токена.

## Дополнительные параметры (поддержка зависит от провайдера)

### Top P (Nucleus Sampling)
- Key: `top_p`
- Тип: float
- Диапазон: [0.0, 1.0]
- По умолчанию: 1.0
- Поддержка: GigaChat ✓, YandexGPT ✗

Ограничивает выбор токенов процентом вероятности. Модель выбирает только из токенов, чьи вероятности в сумме дают P. Работает как динамический Top K.

### Response Format
- Key: `response_format`
- Тип: object
- Формат:
```typescript
{
  type: "json_object" | "text"
}
```
- Поддержка: GigaChat ✓, YandexGPT ✓

Принудительное форматирование ответа в JSON или текст.

## OpenAI-совместимые параметры (для будущей совместимости)

### Frequency Penalty
- Key: `frequency_penalty`
- Тип: float
- Диапазон: [-2.0, 2.0]
- По умолчанию: 0.0
- Поддержка: Только OpenAI

Штраф за повторение токенов из входного текста. Штраф пропорционален частоте появления токена.

### Presence Penalty
- Key: `presence_penalty`
- Тип: float
- Диапазон: [-2.0, 2.0]
- По умолчанию: 0.0
- Поддержка: Только OpenAI

Штраф за повторение любых токенов из входного текста. Штраф не зависит от частоты появления.

### Logit Bias
- Key: `logit_bias`
- Тип: map
- Диапазон значений: [-100, 100]
- Поддержка: Только OpenAI

Позволяет влиять на вероятность выбора конкретных токенов.

## Ограничения моделей

### GigaChat
```typescript
interface GigaChatLimits {
  context_length: 4096;
  max_tokens: 4096;
  supported_features: [
    "streaming",
    "function-calling",
    "json-mode"
  ];
}
```

### YandexGPT
```typescript
interface YandexGPTLimits {
  context_length: 8192;
  max_tokens: 8192;
  supported_features: [
    "streaming",
    "json-mode"
  ];
}
```

## Поддержка параметров провайдерами

| Параметр | GigaChat | YandexGPT | Примечания |
|----------|----------|-----------|------------|
| temperature | ✅ | ✅ | |
| max_tokens | ✅ | ✅ | |
| stream | ✅ | ✅ | |
| repetition_penalty | ✅ | ✅ | |
| top_p | ✅ | ❌ | |
| response_format | ✅ | ✅ | json_object |
| tools | ✅ | ✅* | *Эмулируется через промпты |
| tool_choice | ✅ | ✅* | *Эмулируется через промпты |

## Обработка неподдерживаемых параметров

1. Если провайдер не поддерживает параметр:
   - Параметр игнорируется
   - Предупреждение не выдается
   - Запрос обрабатывается с оставшимися параметрами

2. Если установлен `provider.require_parameters: true`:
   - Запрос будет маршрутизирован только провайдерам, поддерживающим все указанные параметры
   - При отсутствии таких провайдеров вернется ошибка 503

## Рекомендации по использованию

1. Temperature и Top-P
   - Для творческих задач: высокая temperature (0.7-1.0)
   - Для фактических задач: низкая temperature (0.1-0.3)
   - Top-P использовать только с GigaChat

2. Repetition Penalty
   - Значение 1.0 - нейтральное
   - Значения > 1.0 уменьшают повторения
   - Поддерживается обоими провайдерами

3. Streaming
   - Включайте для интерактивных интерфейсов
   - Отключайте для batch-обработки
   - Поддерживается обоими провайдерами

4. Function Calling
   - Нативная поддержка в GigaChat
   - Эмуляция через промпты в YandexGPT
   - Тестируйте на различных сценариях