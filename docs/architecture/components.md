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
- Load balancing
- SSL/TLS termination

#### Dependencies
- Authentication Service
- Rate Limiter Service
- Monitoring Service

---

### 2. Router Service
```typescript
interface RouterService {
  determineProvider(request: RoutingRequest): Promise<Provider>;
  transformRequest(request: Request, provider: Provider): Promise<TransformedRequest>;
  handleResponse(response: ProviderResponse): Promise<NormalizedResponse>;
  handleError(error: ProviderError): Promise<Response>;
}

interface RoutingRequest {
  model: string;
  prompt: string;
  parameters: ModelParameters;
  preferences: ProviderPreferences;
}
```

#### Key Features
- Provider selection logic
- Request transformation
- Response normalization
- Error handling and recovery
- Load balancing between providers
- Fallback management

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
Each LLM provider has a dedicated adapter implementing the Provider interface:

##### GigaChat Adapter
```typescript
class GigaChatAdapter implements Provider {
  capabilities: {
    maxTokens: 4096,
    supportedModels: ['GigaChat', 'GigaChat-Pro'],
    features: ['streaming', 'function-calling']
  };
}
```

##### Yandex GPT Adapter
```typescript
class YandexGPTAdapter implements Provider {
  capabilities: {
    maxTokens: 8192,
    supportedModels: ['YandexGPT', 'YandexGPT-Lite'],
    features: ['streaming']
  };
}
```

##### MTS AI Adapter
```typescript
class MTSAdapter implements Provider {
  capabilities: {
    maxTokens: 4096,
    supportedModels: ['MTS-LLM', 'MTS-LLM-Pro'],
    features: ['function-calling']
  };
}
```

##### T-Bank Adapter
```typescript
class TBankAdapter implements Provider {
  capabilities: {
    maxTokens: 4096,
    supportedModels: ['GEN-T'],
    features: ['streaming']
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
  constructor(private redis: Redis) {}
  
  async get(key: string): Promise<CachedData | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }
  
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
}

interface AlertingService {
  createAlert(alert: Alert): Promise<void>;
  resolveAlert(alertId: string): Promise<void>;
  getActiveAlerts(): Promise<Alert[]>;
}
```

#### Key Features
- Performance metrics collection
- Error tracking and reporting
- Health checking
- Alert management
- Dashboard generation

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
  model VARCHAR(50) NOT NULL,
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