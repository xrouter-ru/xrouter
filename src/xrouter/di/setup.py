"""FastAPI dependency injection setup."""
import logging
from typing import Any, Callable

from fastapi import FastAPI

from xrouter.core.cache import RedisClient
from xrouter.core.config import Settings
from xrouter.db.database import Database
from xrouter.providers.base import ProviderManager
from xrouter.router.service import RouterService
from xrouter.usage.rate_limiter import RateLimiter
from xrouter.usage.service import UsageService
from xrouter.usage.token_counter import TokenCounter

from .containers.application import ApplicationContainer
from .containers.request import RequestContainer

logger = logging.getLogger(__name__)


def setup_di(app: FastAPI, settings: Settings) -> None:
    """Setup dependency injection for FastAPI application.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    logger.info("Configuring dependency injection")

    # Configure application container
    ApplicationContainer.configure(settings)

    # Register application-level dependencies (синглтоны)
    app.dependency_overrides.update(
        {
            Settings: ApplicationContainer.get_settings,
            Database: ApplicationContainer.get_database,
            RedisClient: ApplicationContainer.get_redis_client,
            ProviderManager: ApplicationContainer.get_provider_manager,
        }
    )

    # Register request-level dependencies (новый инстанс на каждый запрос)
    app.dependency_overrides.update(
        {
            RateLimiter: RequestContainer.rate_limiter,
            TokenCounter: RequestContainer.token_counter,
            UsageService: RequestContainer.usage_service,
            RouterService: RequestContainer.router_service,
        }
    )

    logger.info("Dependency injection configured")


def cleanup_di() -> None:
    """Cleanup dependency injection resources."""
    logger.info("Cleaning up dependency injection resources")
    ApplicationContainer.reset()
    logger.info("Dependency injection resources cleaned up")


def get_di_dependencies() -> dict[type, Callable[[], Any]]:
    """Get all registered dependencies.

    Returns:
        Dictionary mapping types to their provider functions
    """
    return {
        # Application-level dependencies
        Settings: ApplicationContainer.get_settings,
        Database: ApplicationContainer.get_database,
        RedisClient: ApplicationContainer.get_redis_client,
        ProviderManager: ApplicationContainer.get_provider_manager,
        # Request-level dependencies
        RateLimiter: RequestContainer.rate_limiter,
        TokenCounter: RequestContainer.token_counter,
        UsageService: RequestContainer.usage_service,
        RouterService: RequestContainer.router_service,
    }
