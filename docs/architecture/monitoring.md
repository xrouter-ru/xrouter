# XRouter Monitoring

## Overview

XRouter использует комплексный подход к мониторингу для обеспечения надежности и производительности сервиса.

## Компоненты

### Prometheus
- Сбор метрик
- Хранение временных рядов
- Алертинг
- Service discovery

### Grafana
- Визуализация метрик
- Дашборды
- Алерты
- Отчеты

### ELK Stack (Production)
- Сбор логов
- Анализ логов
- Поиск по логам
- Визуализация

## Метрики

### System Metrics
- CPU Usage
- Memory Usage
- Disk I/O
- Network I/O

### Application Metrics
- Request Rate
- Response Time
- Error Rate
- Token Usage

### Provider Metrics
- Provider Latency
- Success Rate
- Error Distribution
- Token Consumption

### Business Metrics
- Active Users
- API Key Usage
- Revenue
- Cost per Request

## Алертинг

### Critical Alerts
- Service Down
- High Error Rate
- Database Issues
- Provider Outages

### Warning Alerts
- High Latency
- Rate Limit Approaching
- Disk Space Low
- Memory Usage High

### Info Alerts
- New Version Deployed
- Config Changed
- Backup Completed
- Maintenance Started

## Дашборды

### Overview Dashboard
```
+------------------+------------------+
|   Request Rate   |   Error Rate    |
+------------------+------------------+
|   Latency p95    |   Success Rate  |
+------------------+------------------+
|   Active Users   |   Token Usage   |
+------------------+------------------+
```

### Provider Dashboard
```
+------------------+------------------+
|  Provider Stats  |  Error Types    |
+------------------+------------------+
|  Response Times  |  Success Rates  |
+------------------+------------------+
|  Token Usage    |  Cost Analysis  |
+------------------+------------------+
```

### System Dashboard
```
+------------------+------------------+
|    CPU Usage    |   Memory Usage   |
+------------------+------------------+
|    Disk I/O     |   Network I/O    |
+------------------+------------------+
|    Processes    |     Alerts      |
+------------------+------------------+
```

## Логирование

### Log Levels
- ERROR: Ошибки требующие внимания
- WARN: Потенциальные проблемы
- INFO: Важные события
- DEBUG: Детальная информация

### Log Format
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "router",
  "trace_id": "abc123",
  "message": "Request processed",
  "details": {
    "provider": "gigachat",
    "model": "pro",
    "latency": 245,
    "tokens": 150
  }
}
```

### Log Retention
- ERROR: 1 год
- WARN: 6 месяцев
- INFO: 3 месяца
- DEBUG: 1 неделя

## Health Checks

### Endpoint Health
```http
GET /health
{
  "status": "healthy",
  "components": {
    "api": "up",
    "db": "up",
    "cache": "up",
    "providers": {
      "gigachat": "up",
      "yandexgpt": "up"
    }
  }
}
```

### Provider Health
```http
GET /health/providers
{
  "gigachat": {
    "status": "up",
    "latency": 245,
    "error_rate": 0.1,
    "last_check": "2024-01-01T12:00:00Z"
  },
  "yandexgpt": {
    "status": "up",
    "latency": 180,
    "error_rate": 0.05,
    "last_check": "2024-01-01T12:00:00Z"
  }
}
```

## Incident Response

### Severity Levels
1. **Critical**: Сервис недоступен
2. **High**: Значительное влияние
3. **Medium**: Частичное влияние
4. **Low**: Минимальное влияние

### Response Time
- Critical: 15 минут
- High: 30 минут
- Medium: 2 часа
- Low: 24 часа

### Escalation Path
1. On-call инженер
2. Team Lead
3. CTO
4. CEO

## Reporting

### Daily Reports
- Request volume
- Error rates
- Provider stats
- Cost analysis

### Weekly Reports
- Performance trends
- Error patterns
- Usage patterns
- Capacity planning

### Monthly Reports
- SLA compliance
- Cost optimization
- Growth trends
- Security incidents