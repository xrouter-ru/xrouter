# XRouter Data Flow Documentation

## Request Flow

### 1. Client Request Processing
```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant Router as Router Service
    participant Provider as Provider Manager
    participant Cache as Cache Service
    
    Client->>Gateway: Send Request
    Gateway->>Gateway: Validate Request
    Gateway->>Gateway: Authenticate
    Gateway->>Router: Forward Request
    Router->>Cache: Check Cache
    alt Cache Hit
        Cache-->>Router: Return Cached Response
        Router-->>Gateway: Return Response
        Gateway-->>Client: Return Response
    else Cache Miss
        Router->>Provider: Forward to Provider
        Provider->>Provider: Transform Request
        Provider->>LLM: Send to LLM
        LLM-->>Provider: LLM Response
        Provider->>Provider: Normalize Response
        Provider-->>Router: Return Response
        Router->>Cache: Cache Response
        Router-->>Gateway: Return Response
        Gateway-->>Client: Return Response
    end
```

### 2. Request Transformation
```typescript
interface ClientRequest {
  model: string;
  messages: Message[];
  parameters: ModelParameters;
  stream?: boolean;
}

interface ProviderRequest {
  prompt: string;
  max_tokens: number;
  temperature: number;
  provider_specific_params: Record<string, any>;
}

// Transformation Process
function transformRequest(request: ClientRequest, provider: Provider): ProviderRequest {
  return {
    prompt: formatPrompt(request.messages),
    max_tokens: calculateMaxTokens(request.parameters),
    temperature: request.parameters.temperature ?? provider.defaults.temperature,
    provider_specific_params: mapProviderParams(request.parameters, provider)
  };
}
```

## Response Flow

### 1. Standard Response Processing
```mermaid
sequenceDiagram
    participant LLM as LLM Provider
    participant Provider as Provider Manager
    participant Router as Router Service
    participant Cache as Cache Service
    participant Client
    
    LLM->>Provider: Raw Response
    Provider->>Provider: Normalize Response
    Provider->>Router: Normalized Response
    Router->>Cache: Cache Response
    Router->>Client: Return Response
```

### 2. Streaming Response Processing
```mermaid
sequenceDiagram
    participant LLM as LLM Provider
    participant Provider as Provider Manager
    participant Router as Router Service
    participant Client
    
    LLM->>Provider: Stream Chunk
    Provider->>Provider: Normalize Chunk
    Provider->>Router: Forward Chunk
    Router->>Client: Stream Chunk
    Note over LLM,Client: Repeat until stream ends
```

## Error Handling

### 1. Error Types
```typescript
interface ServiceError {
  code: ErrorCode;
  message: string;
  details?: Record<string, any>;
  retryable: boolean;
}

enum ErrorCode {
  AUTHENTICATION_ERROR = 'auth_error',
  VALIDATION_ERROR = 'validation_error',
  PROVIDER_ERROR = 'provider_error',
  RATE_LIMIT_ERROR = 'rate_limit_error',
  INTERNAL_ERROR = 'internal_error'
}
```

### 2. Error Flow
```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant Router as Router Service
    participant Provider as Provider Manager
    participant Fallback as Fallback Provider
    
    Client->>Gateway: Request
    Gateway->>Router: Forward Request
    Router->>Provider: Process Request
    Provider->>Provider: Error Occurs
    Provider-->>Router: Return Error
    
    alt Retryable Error
        Router->>Fallback: Retry with Fallback
        Fallback-->>Router: Success Response
        Router-->>Gateway: Return Response
        Gateway-->>Client: Return Response
    else Non-Retryable Error
        Router-->>Gateway: Return Error
        Gateway-->>Client: Return Error Response
    end
```

## Fallback Mechanism

### 1. Provider Fallback
```typescript
interface FallbackStrategy {
  shouldFallback(error: ServiceError): boolean;
  getFallbackProvider(currentProvider: Provider): Provider;
  maxRetries: number;
}

class ProviderFallback {
  async executeWithFallback(request: ClientRequest): Promise<Response> {
    let attempts = 0;
    let lastError: ServiceError;
    
    while (attempts < this.strategy.maxRetries) {
      try {
        const provider = this.getNextProvider(attempts);
        return await provider.execute(request);
      } catch (error) {
        lastError = error;
        if (!this.strategy.shouldFallback(error)) {
          throw error;
        }
        attempts++;
      }
    }
    
    throw lastError;
  }
}
```

### 2. Fallback Flow
```mermaid
sequenceDiagram
    participant Client
    participant Router as Router Service
    participant Primary as Primary Provider
    participant Secondary as Secondary Provider
    participant Tertiary as Tertiary Provider
    
    Client->>Router: Request
    Router->>Primary: Try Primary
    Primary-->>Router: Error
    Router->>Secondary: Fallback to Secondary
    Secondary-->>Router: Error
    Router->>Tertiary: Fallback to Tertiary
    Tertiary-->>Router: Success
    Router->>Client: Response
```

## Caching Strategy

### 1. Cache Levels
```typescript
interface CacheStrategy {
  shouldCache(request: ClientRequest): boolean;
  getCacheKey(request: ClientRequest): string;
  getTTL(request: ClientRequest): number;
}

interface CacheEntry {
  response: Response;
  created: Date;
  expires: Date;
  metadata: CacheMetadata;
}
```

### 2. Cache Flow
```mermaid
sequenceDiagram
    participant Client
    participant Router as Router Service
    participant Cache as Cache Service
    participant Provider as Provider Manager
    
    Client->>Router: Request
    Router->>Cache: Check Cache
    alt Cache Hit
        Cache-->>Router: Return Cached
        Router-->>Client: Return Response
    else Cache Miss
        Router->>Provider: Forward Request
        Provider-->>Router: Response
        Router->>Cache: Store in Cache
        Router-->>Client: Return Response
    end
```

## Rate Limiting

### 1. Rate Limit Implementation
```typescript
interface RateLimiter {
  checkLimit(key: string): Promise<RateLimitResult>;
  incrementUsage(key: string): Promise<void>;
  resetUsage(key: string): Promise<void>;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  reset: Date;
}
```

### 2. Rate Limit Flow
```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant RateLimit as Rate Limiter
    participant Router as Router Service
    
    Client->>Gateway: Request
    Gateway->>RateLimit: Check Limits
    alt Limit Exceeded
        RateLimit-->>Gateway: Reject
        Gateway-->>Client: 429 Too Many Requests
    else Limit OK
        RateLimit-->>Gateway: Accept
        Gateway->>Router: Forward Request
        Router-->>Client: Response
    end
```

## Monitoring and Metrics

### 1. Metric Collection
```typescript
interface MetricCollector {
  recordLatency(operation: string, duration: number): void;
  recordError(operation: string, error: ServiceError): void;
  recordUsage(provider: string, tokens: number): void;
  recordCacheHit(operation: string): void;
  recordCacheMiss(operation: string): void;
}
```

### 2. Metric Flow
```mermaid
sequenceDiagram
    participant Service
    participant Metrics as Metric Collector
    participant Prometheus
    participant Grafana
    
    Service->>Metrics: Record Metric
    Metrics->>Prometheus: Store Metric
    Grafana->>Prometheus: Query Metrics
    Note over Grafana: Display Dashboard