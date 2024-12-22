# XRouter Components Documentation

## Core Services

### 1. API Gateway Service
```typescript
interface APIGateway {
  validateRequest(request: Request): Promise<ValidationResult>;
  authenticateRequest(request: Request): Promise<AuthResult>;
  routeRequest(request: Request): Promise<Response>;
  handleRateLimit(key: string): Promise<RateLimitResult>;
}
```

#### Key Features
- Request validation and sanitization
- Authentication and authorization
- Rate limiting and quota management
- Request logging and monitoring
- SSL/TLS termination

#### Dependencies
- Authentication Service
- Rate Limiter Service
- Monitoring Service

---

### 2. Router Service
```typescript
interface RouterService {
  resolveProvider(model: string): Promise<Provider>;
  transformRequest(request: Request, provider: Provider): Promise<TransformedRequest>;
  handleResponse(response: ProviderResponse): Promise<NormalizedResponse>;
  handleError(error: ProviderError): Promise<Response>;
}

interface ModelInfo {
  id: string;              // e.g. "gigachat-pro" или "yandexgpt-lite:latest"
  provider: string;        // "gigachat" | "yandexgpt"
  capabilities: {
    contextLength: number;
    maxTokens: number;
    features: string[];    // ["streaming", "function-calling", "json-mode"]
  };
}
```

#### Key Features
- Model resolution to provider
- Request transformation
- Response normalization
- Error handling

#### Dependencies
- Provider Manager
- Cache Service
- Monitoring Service

---

### 3. Provider Manager
```typescript
interface ProviderManager {
  getProvider(id: string): Promise<Provider>;
  checkHealth(provider: Provider): Promise<HealthStatus>;
  executeRequest(request: TransformedRequest, provider: Provider): Promise<ProviderResponse>;
  handleRetry(request: TransformedRequest, error: Error): Promise<ProviderResponse>;
}

interface Provider {
  id: string;
  name: string;
  endpoint: string;
  capabilities: ModelCapabilities;
  authenticate(): Promise<void>;
  execute(request: TransformedRequest): Promise<ProviderResponse>;
}
```

#### Provider Adapters

##### GigaChat Adapter
```typescript
class GigaChatAdapter implements Provider {
  capabilities: {
    maxTokens: 32768,
    supportedModels: [
      'gigachat',      // Lite версия
      'gigachat-pro',  // Pro версия
      'gigachat-max'   // Max версия
    ],
    features: ['streaming', 'function-calling', 'json-mode', 'images']
  };
}
```

##### YandexGPT Adapter
```typescript
class YandexGPTAdapter implements Provider {
  capabilities: {
    supportedModels: [
      // Lite версии
      'yandexgpt-lite:latest',
      'yandexgpt-lite:rc',
      'yandexgpt-lite:deprecated',
      // Pro версии
      'yandexgpt:latest',
      'yandexgpt:rc',
      'yandexgpt:deprecated',
      // 32k версии
      'yandexgpt-32k:latest',
      'yandexgpt-32k:rc',
      'yandexgpt-32k:deprecated'
    ],
    maxTokens: {
      'yandexgpt-lite': 8192,
      'yandexgpt': 8192,
      'yandexgpt-32k': 32768
    },
    features: ['streaming', 'json-mode']
  };
}
```

---

### 4. Authentication Service
```typescript
interface AuthService {
  validateToken(token: string): Promise<TokenValidation>;
  generateToken(user: User): Promise<Token>;
  revokeToken(token: string): Promise<void>;
  validateAPIKey(key: string): Promise<APIKeyValidation>;
}

interface OAuthService {
  initiateOAuth(request: OAuthRequest): Promise<OAuthResponse>;
  handleCallback(code: string): Promise<TokenResponse>;
  refreshToken(refreshToken: string): Promise<TokenResponse>;
}
```

#### Key Features
- OAuth 2.0 with PKCE implementation
- API key management
- Token validation and refresh
- Permission management
- User management

#### Dependencies
- Database Service
- Cache Service
- Monitoring Service

---

### 5. Cache Service
```typescript
interface CacheService {
  get(key: string): Promise<CachedData | null>;
  set(key: string, value: any, ttl?: number): Promise<void>;
  delete(key: string): Promise<void>;
  invalidate(pattern: string): Promise<void>;
}

interface CacheConfig {
  defaultTTL: number;
  modelTTL: {
    [modelId: string]: number;  // Разные TTL для разных моделей
  };
}
```

#### Key Features
- Response caching
- Session management
- Rate limit tracking
- Token caching
- Provider state caching

#### Implementation
```typescript
class RedisCacheService implements CacheService {
  constructor(
    private redis: Redis,
    private config: CacheConfig
  ) {}
  
  async set(key: string, value: any, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value);
    if (ttl) {
      await this.redis.setex(key, ttl, serialized);
    } else {
      await this.redis.set(key, serialized);
    }
  }
}
```

---

### 6. Monitoring Service
```typescript
interface MonitoringService {
  recordMetric(metric: Metric): Promise<void>;
  recordError(error: Error): Promise<void>;
  checkHealth(service: string): Promise<HealthStatus>;
  getMetrics(query: MetricQuery): Promise<MetricData[]>;
  getProviderStatus(provider: string): Promise<ProviderStatus>;
}

interface ProviderStatus {
  status: "operational" | "degraded" | "down";
  latency: number;
  success_rate: number;
  last_updated: string;
  models: {
    [modelId: string]: {
      status: string;
      last_updated: string;
    };
  };
}
```

#### Key Features
- Performance metrics collection
- Error tracking and reporting
- Health checking
- Provider status monitoring
- Model status tracking

#### Metrics Collected
- Request latency
- Error rates
- Provider availability
- Token usage
- Cache hit rates
- Resource utilization

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### API Keys Table
```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  key_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP WITH TIME ZONE,
  last_used_at TIMESTAMP WITH TIME ZONE,
  CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### Usage Table
```sql
CREATE TABLE usage (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  provider VARCHAR(50) NOT NULL,
  model VARCHAR(100) NOT NULL,  -- Включая версию, например "yandexgpt-lite:latest"
  tokens_input INTEGER NOT NULL,
  tokens_output INTEGER NOT NULL,
  cost DECIMAL(10,6) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### Provider Status Table
```sql
CREATE TABLE provider_status (
  id UUID PRIMARY KEY,
  provider VARCHAR(50) NOT NULL,
  model VARCHAR(100) NOT NULL,  -- Включая версию
  status VARCHAR(20) NOT NULL,
  latency INTEGER,
  error_rate DECIMAL(5,2),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## Service Communication

### Internal Communication
- REST APIs between services
- gRPC for high-performance internal communication
- Redis pub/sub for real-time updates
- PostgreSQL for persistent storage
- Redis for caching and session management

### External Communication
- REST APIs for client communication
- WebSocket for streaming responses
- HTTPS for secure communication
- OAuth 2.0 for authentication

### Message Formats
```typescript
interface ServiceMessage {
  id: string;
  type: MessageType;
  payload: any;
  timestamp: Date;
  source: string;
  destination: string;
}

interface ServiceResponse {
  id: string;
  status: ResponseStatus;
  data?: any;
  error?: ServiceError;
  timestamp: Date;
}