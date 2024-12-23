# Dependency Injection Architecture

## Overview

The application uses constructor-based dependency injection with two levels of containers:
1. Application Container - for long-lived singleton services
2. Request Container - for request-scoped services

## Release Plan

### Release 1.0 - Foundation

#### Application Container
```python
class ApplicationContainer:
    def __init__(self, config: Config):
        # Core services
        self.config = config
        self.database = DatabaseService(config)  # SQLite
        self.cache = CacheService(config)        # Redis

        # Business services
        self.usage_service = UsageService(
            database=self.database,
            cache=self.cache
        )

        self.provider_manager = ProviderManager(
            config=self.config,
            cache=self.cache
        )

        self.router = RouterService(
            provider_manager=self.provider_manager,
            usage_service=self.usage_service
        )

    def create_request_container(self) -> 'RequestContainer':
        return RequestContainer(self)
```

#### Request Container
```python
class RequestContainer:
    def __init__(self, app: ApplicationContainer):
        # Core services
        self.config = app.config
        self.database = app.database
        self.cache = app.cache

        # Request-scoped services
        self.rate_limiter = RateLimiter(
            cache=self.cache,
            config=self.config
        )

        self.token_counter = TokenCounter(
            provider_manager=app.provider_manager
        )

        self.usage_tracker = UsageTracker(
            database=self.database,
            cache=self.cache
        )
```

### Release 1.1 - Enhancement

#### Application Container
```python
class ApplicationContainer:
    def __init__(self, config: Config):
        # Core services
        self.config = config
        self.logger = LoggerService(config)
        self.database = DatabaseService(config)  # PostgreSQL
        self.cache = CacheService(config)        # Redis
        self.metrics = MetricsService(config)    # Prometheus

        # Business services
        self.usage_service = UsageService(
            database=self.database,
            cache=self.cache,
            metrics=self.metrics,
            logger=self.logger
        )

        self.provider_manager = ProviderManager(
            config=self.config,
            metrics=self.metrics,
            logger=self.logger
        )

        self.router = RouterService(
            provider_manager=self.provider_manager,
            usage_service=self.usage_service,
            metrics=self.metrics,
            logger=self.logger
        )

    def create_request_container(self) -> 'RequestContainer':
        return RequestContainer(self)
```

#### Request Container
```python
class RequestContainer:
    def __init__(self, app: ApplicationContainer):
        # Core services
        self.config = app.config
        self.logger = app.logger
        self.database = app.database
        self.cache = app.cache
        self.metrics = app.metrics

        # Request-scoped services
        self.rate_limiter = RateLimiter(
            cache=self.cache,
            metrics=self.metrics,
            logger=self.logger
        )

        self.token_counter = TokenCounter(
            provider_manager=app.provider_manager,
            metrics=self.metrics
        )

        self.usage_tracker = UsageTracker(
            database=self.database,
            cache=self.cache,
            metrics=self.metrics,
            logger=self.logger
        )
```

## Service Dependencies

### Release 1.0
- Core Services:
  * Config: Application settings
  * Database: SQLite connection and migrations
  * Cache: Redis for rate limiting and caching

- Business Services:
  * Usage Service: Token counting and usage tracking
  * Provider Manager: GigaChat integration
  * Router Service: Basic request routing

- Request Services:
  * Rate Limiter: Basic rate limiting
  * Token Counter: Token estimation
  * Usage Tracker: Usage recording

### Release 1.1
- Core Services:
  * Config: Enhanced settings
  * Logger: Structured logging
  * Database: PostgreSQL with migrations
  * Cache: Enhanced Redis functionality
  * Metrics: Prometheus metrics

- Business Services:
  * Usage Service: Advanced usage tracking
  * Provider Manager: Multiple providers
  * Router Service: Smart routing

- Request Services:
  * Rate Limiter: Advanced rate limiting
  * Token Counter: Precise token counting
  * Usage Tracker: Detailed usage tracking

## Benefits

1. Clear Separation of Concerns
   - Application-level services are singletons
   - Request-level services are created per request
   - Dependencies are explicit through constructors

2. Easy Testing
   - Services can be easily mocked
   - Dependencies can be replaced for testing
   - No global state

3. Resource Management
   - Database connections are shared
   - Redis connections are reused
   - Metrics are centralized

4. Flexibility
   - New providers can be easily added
   - Services can be extended
   - Dependencies can be modified

## Guidelines

1. Always use constructor injection
2. Keep application services stateless
3. Document service dependencies
4. Use type hints for better IDE support
5. Consider service lifecycle when designing
