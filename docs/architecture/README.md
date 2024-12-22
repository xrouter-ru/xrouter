# XRouter Architecture Documentation

## Overview
This directory contains comprehensive documentation about XRouter's system architecture, designed to provide a unified API for accessing various Russian LLM models (GigaChat, Yandex GPT, MTS, T-Bank).

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
- Monitoring & Logging
- Database design

### 3. [Data Flow](./data-flow.md)
- Request handling
- Provider routing
- Error handling
- Fallback mechanisms
- Caching strategies

### 4. [Deployment](./deployment.md)
- Infrastructure requirements
- Deployment strategies
- Scaling considerations
- Security measures

## Key Architectural Decisions

### 1. Technology Stack
- **Backend**: Node.js with Express.js and TypeScript
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for session management and caching
- **API Gateway**: Nginx for load balancing and SSL termination
- **Monitoring**: Prometheus & Grafana

### 2. Core Principles
- Provider-agnostic API design
- Fault tolerance with fallback mechanisms
- Scalable microservices architecture
- Secure by design
- Comprehensive monitoring and logging

### 3. Integration Patterns
- REST API with OpenAI-compatible endpoints
- WebSocket support for streaming responses
- OAuth 2.0 with PKCE for authentication
- Rate limiting and quota management

## Development Guidelines

### Code Organization
```
src/
├── api/            # API routes and controllers
├── core/           # Core business logic
├── providers/      # Provider-specific adapters
├── models/         # Data models and schemas
├── services/       # Shared services
├── utils/          # Utility functions
└── config/         # Configuration management
```

### Key Interfaces
- Provider Adapter Interface
- Model Router Interface
- Authentication Provider Interface
- Monitoring Interface

## Next Steps
1. Review and validate the architectural design
2. Set up development environment
3. Implement core components
4. Develop provider adapters
5. Set up monitoring and logging
6. Deploy initial version