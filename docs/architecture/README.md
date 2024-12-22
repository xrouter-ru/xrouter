# XRouter Architecture Documentation

## Overview
This directory contains comprehensive documentation about XRouter's system architecture, designed to provide a unified API for accessing various Russian LLM models (GigaChat, YandexGPT).

## Documentation Structure

### 1. [System Overview](./system-overview.md)
- High-level architecture
- Key components
- System boundaries
- Integration points

### 2. [Components](./components.md)
- Core services
- Provider adapters
- API Gateway
- Authentication & Authorization
- Monitoring & Metrics
- Database design

### 3. [Data Flow](./data-flow.md)
- Request handling
- Provider routing
- Error handling
- Rate limiting
- OAuth flow

### 4. [Deployment](./deployment.md)
- Infrastructure requirements
- Deployment strategies
- Scaling considerations
- Security measures

## Key Architectural Decisions

### 1. Technology Stack

#### MVP Version
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for rate limiting
- **API Gateway**: Nginx for SSL termination
- **Monitoring**: Prometheus & Grafana

#### Production Version
- **Backend**: Go with standard library
- **Database**: PostgreSQL with HA
- **Cache**: Redis Cluster
- **API Gateway**: Kubernetes Ingress
- **Monitoring**: Prometheus & Grafana stack

### 2. Core Principles
- Provider-agnostic API design
- OpenAI-compatible interface
- Transparent pricing and token counting
- Secure by design
- Comprehensive monitoring

### 3. Integration Patterns
- REST API with OpenAI compatibility
- OAuth 2.0 with PKCE (1 year tokens)
- Rate limiting per API key
- Prometheus metrics export

## Development Guidelines

### MVP Code Organization (Python)
```
src/
├── api/            # FastAPI routes
├── core/           # Core business logic
├── providers/      # Provider adapters
├── models/         # Pydantic models
├── services/       # Shared services
└── config/         # Configuration
```

### Production Code Organization (Go)
```
cmd/
├── gateway/        # API Gateway service
└── router/         # Router service
pkg/
├── api/           # API handlers
├── core/          # Core business logic
├── providers/     # Provider adapters
├── models/        # Data models
└── config/        # Configuration
```

### Key Interfaces

#### MVP (Python)
```python
class ProviderAdapter(Protocol):
    async def complete(self, request: ChatRequest) -> ChatResponse: ...
    async def validate_api_key(self, key: str) -> bool: ...

class Router(Protocol):
    async def route_request(self, request: ChatRequest) -> ChatResponse: ...
```

#### Production (Go)
```go
type Provider interface {
    Complete(context.Context, *ChatRequest) (*ChatResponse, error)
    ValidateAPIKey(context.Context, string) (bool, error)
}

type Router interface {
    RouteRequest(context.Context, *ChatRequest) (*ChatResponse, error)
}
```

## Next Steps
1. Implement MVP with Python/FastAPI
2. Set up basic monitoring
3. Deploy MVP version
4. Start Go implementation
5. Set up production infrastructure
6. Migrate to Go version