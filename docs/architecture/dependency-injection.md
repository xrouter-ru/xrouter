# Dependency Injection Architecture

## Overview

The application uses constructor-based dependency injection with two levels of containers:
1. Application Container - for long-lived singleton services
2. Request Container - for request-scoped services

## Application Container

### Singleton Services

```python
class DatabaseService:
    def __init__(self, config: Config):
        self.engine = create_engine(config.SQLITE_URL)
        self.session_factory = sessionmaker(bind=self.engine)

class CacheService:
    def __init__(self, config: Config):
        self.redis = Redis.from_url(config.REDIS_URL)

class MetricsService:
    def __init__(self, config: Config):
        self.client = PrometheusClient()

class LoggerService:
    def __init__(self, config: Config):
        self.logger = structlog.get_logger()

class ApplicationContainer:
    def __init__(self, config: Config):
        # Core services
        self.config = config
        self.logger = LoggerService(config)
        self.database = DatabaseService(config)
        self.cache = CacheService(config)
        self.metrics = MetricsService(config)

    def create_request_container(self) -> 'RequestContainer':
        return RequestContainer(self)
```

## Request Container

### Request-Scoped Services

```python
class UsageService:
    def __init__(
        self,
        database: DatabaseService,
        cache: CacheService,
        metrics: MetricsService,
        logger: LoggerService
    ):
        self.database = database
        self.cache = cache
        self.metrics = metrics
        self.logger = logger

class GigaChatProvider:
    def __init__(
        self,
        config: Config,
        metrics: MetricsService,
        logger: LoggerService
    ):
        self.client = GigaChatClient(config.GIGACHAT_API_KEY)
        self.metrics = metrics
        self.logger = logger

class ProviderManager:
    def __init__(
        self,
        config: Config,
        metrics: MetricsService,
        logger: LoggerService
    ):
        self.providers = {
            "gigachat": GigaChatProvider(config, metrics, logger)
        }
        self.metrics = metrics
        self.logger = logger

class RouterService:
    def __init__(
        self,
        provider_manager: ProviderManager,
        usage_service: UsageService,
        metrics: MetricsService,
        logger: LoggerService
    ):
        self.provider_manager = provider_manager
        self.usage_service = usage_service
        self.metrics = metrics
        self.logger = logger

class RequestContainer:
    def __init__(self, app: ApplicationContainer):
        # Application services
        self.config = app.config
        self.logger = app.logger
        self.database = app.database
        self.cache = app.cache
        self.metrics = app.metrics

        # Request services
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
```

## Usage Example

```python
# Application startup
config = Config()
app_container = ApplicationContainer(config)

# Request handling
@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatRequest,
    container: RequestContainer = Depends(get_request_container)
):
    try:
        return await container.router.route_request(request)
    except Exception as e:
        container.logger.error("Request failed", error=e)
        raise

# FastAPI dependency
def get_request_container() -> RequestContainer:
    return app_container.create_request_container()
```

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