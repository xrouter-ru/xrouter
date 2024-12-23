"""Application-level dependency container."""
from typing import Optional

from redis.asyncio import Redis

from xrouter.core.cache import RedisClient
from xrouter.core.config import Settings
from xrouter.db.database import Database
from xrouter.providers.base import ProviderManager
from xrouter.router.service import RouterService
from xrouter.usage.service import UsageService


class ApplicationContainer:
    """Container for application-level dependencies.

    Contains only singleton services that should be shared across requests:
    - Core Services:
        - Settings: Application configuration
        - Database: SQLite connection and migrations
        - RedisClient: Redis for rate limiting and caching

    - Business Services:
        - Usage Service: Token counting and usage tracking
        - Provider Manager: GigaChat integration
        - Router Service: Basic request routing
    """

    # Singleton instances
    _settings: Optional[Settings] = None
    _database: Optional[Database] = None
    _redis_client: Optional[RedisClient] = None
    _usage_service: Optional[UsageService] = None
    _provider_manager: Optional[ProviderManager] = None
    _router_service: Optional[RouterService] = None

    @classmethod
    def configure(cls, settings: Settings) -> None:
        """Configure container with application settings.

        Initializes singleton services that are shared across requests:
        - Settings: Application configuration
        - Database: Database connection and migrations
        - RedisClient: Redis connection and caching
        - Usage Service: Token counting and usage tracking
        - Provider Manager: LLM providers setup
        - Router Service: Main routing service setup

        Args:
            settings: Application settings
        """
        cls._settings = settings

        # Initialize database
        cls._database = Database()

        # Initialize Redis client
        redis = Redis.from_url(str(settings.REDIS_URL))
        cls._redis_client = RedisClient(redis)

        # Initialize usage service
        cls._usage_service = UsageService(
            database=cls._database, redis_client=cls._redis_client
        )

        # Initialize provider manager
        cls._provider_manager = ProviderManager(
            settings=settings, redis_client=cls._redis_client
        )

        # Initialize router service
        cls._router_service = RouterService(
            provider_manager=cls._provider_manager, usage_service=cls._usage_service
        )

    @classmethod
    def get_settings(cls) -> Settings:
        """Get application settings."""
        if cls._settings is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._settings

    @classmethod
    def get_database(cls) -> Database:
        """Get database instance."""
        if cls._database is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._database

    @classmethod
    def get_redis_client(cls) -> RedisClient:
        """Get Redis client instance."""
        if cls._redis_client is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._redis_client

    @classmethod
    def get_usage_service(cls) -> UsageService:
        """Get usage service instance."""
        if cls._usage_service is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._usage_service

    @classmethod
    def get_provider_manager(cls) -> ProviderManager:
        """Get provider manager instance."""
        if cls._provider_manager is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._provider_manager

    @classmethod
    def get_router_service(cls) -> RouterService:
        """Get router service instance."""
        if cls._router_service is None:
            raise RuntimeError("Container not configured. Call configure() first.")
        return cls._router_service

    @classmethod
    def reset(cls) -> None:
        """Reset singleton services state."""
        cls._settings = None
        cls._database = None
        cls._redis_client = None
        cls._usage_service = None
        cls._provider_manager = None
        cls._router_service = None