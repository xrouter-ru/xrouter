"""Request-level dependency container."""
from fastapi import Depends

from xrouter.core.cache import RedisClient
from xrouter.core.config import Settings
from xrouter.providers.base import ProviderManager
from xrouter.usage.rate_limiter import RateLimiter
from xrouter.usage.token_counter import TokenCounter

from .application import ApplicationContainer

# FastAPI dependency providers for application-level services
SETTINGS = Depends(ApplicationContainer.get_settings)
REDIS_CLIENT = Depends(ApplicationContainer.get_redis_client)
PROVIDER_MANAGER = Depends(ApplicationContainer.get_provider_manager)
USAGE_SERVICE = Depends(ApplicationContainer.get_usage_service)
ROUTER_SERVICE = Depends(ApplicationContainer.get_router_service)


class RequestContainer:
    """Container for request-level dependencies.

    Creates new instances for each request:
    - RateLimiter: Request rate limiting
    - TokenCounter: Token usage tracking

    Uses singleton services from ApplicationContainer:
    - Settings: Application configuration
    - RedisClient: Redis connection
    - ProviderManager: LLM providers
    - UsageService: Usage tracking
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
