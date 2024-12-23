"""Request-level dependency container."""
from fastapi import Depends

from xrouter.core.cache import RedisClient
from xrouter.core.config import Settings
from xrouter.db.database import Database
from xrouter.providers.base import ProviderManager
from xrouter.router.service import RouterService
from xrouter.usage.rate_limiter import RateLimiter
from xrouter.usage.service import UsageService
from xrouter.usage.token_counter import TokenCounter

from .application import ApplicationContainer

# FastAPI dependency providers
SETTINGS = Depends(ApplicationContainer.get_settings)
REDIS_CLIENT = Depends(ApplicationContainer.get_redis_client)
DATABASE = Depends(ApplicationContainer.get_database)
PROVIDER_MANAGER = Depends(ApplicationContainer.get_provider_manager)


class RequestContainer:
    """Container for request-level dependencies.

    Creates new instances for each request:
    - RateLimiter: Request rate limiting
    - TokenCounter: Token usage tracking
    - UsageService: API usage tracking

    Uses singleton services from ApplicationContainer:
    - Settings: Application configuration
    - Database: Database connection
    - RedisClient: Redis connection
    - ProviderManager: LLM providers
    - RouterService: Main routing service
    """

    @staticmethod
    def get_rate_limiter(
        redis_client: RedisClient = REDIS_CLIENT,
        settings: Settings = SETTINGS,
    ) -> RateLimiter:
        """Create new RateLimiter for request.

        Uses:
        - RedisClient singleton for rate limiting
        - Settings singleton for configuration
        """
        return RateLimiter(redis_client=redis_client, settings=settings)

    # Create dependency for rate limiter
    rate_limiter = Depends(get_rate_limiter)

    @staticmethod
    def get_token_counter(
        provider_manager: ProviderManager = PROVIDER_MANAGER,
        settings: Settings = SETTINGS,
    ) -> TokenCounter:
        """Create new TokenCounter for request.

        Uses:
        - ProviderManager singleton for token counting rules
        - Settings singleton for configuration
        """
        return TokenCounter(provider_manager=provider_manager, settings=settings)

    # Create dependency for token counter
    token_counter = Depends(get_token_counter)

    @staticmethod
    def get_usage_service(
        database: Database = DATABASE,
        token_counter: TokenCounter = token_counter,
        settings: Settings = SETTINGS,
    ) -> UsageService:
        """Create new UsageService for request.

        Uses:
        - Database singleton for storage
        - New TokenCounter instance
        - Settings singleton for configuration
        """
        return UsageService(
            database=database,
            token_counter=token_counter,
            settings=settings,
        )

    # Create dependency for usage service
    usage_service = Depends(get_usage_service)

    @staticmethod
    def get_router_service(
        provider_manager: ProviderManager = PROVIDER_MANAGER,
        rate_limiter: RateLimiter = rate_limiter,
        usage_service: UsageService = usage_service,
        settings: Settings = SETTINGS,
    ) -> RouterService:
        """Get router service with request-level dependencies.

        Uses:
        - ProviderManager singleton
        - New RateLimiter instance
        - New UsageService instance
        - Settings singleton
        """
        return RouterService(
            provider_manager=provider_manager,
            rate_limiter=rate_limiter,
            usage_service=usage_service,
            settings=settings,
        )

    # Create dependency for router service
    router_service = Depends(get_router_service)
