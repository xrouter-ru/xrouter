"""Application configuration."""
from typing import Dict, List, Union

from pydantic import AnyHttpUrl, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Project
    PROJECT_NAME: str = "xrouter"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    SQLITE_URL: str = "sqlite+aiosqlite:///xrouter.db"
    DB_ECHO: bool = False

    # Redis
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"
    REDIS_PREFIX: str = "xrouter"

    # Rate Limiting
    RATE_LIMIT_DEFAULT: int = 100  # requests per minute
    RATE_LIMIT_BURST: int = 200

    # Cache
    CACHE_TTL: int = 60 * 60  # 1 hour
    CACHE_PREFIX: str = "cache"

    # API Keys
    API_KEY_LENGTH: int = 32
    API_KEY_PREFIX: str = "xr"

    # Provider Settings
    PROVIDER_TIMEOUT: int = 30  # seconds
    PROVIDER_MAX_RETRIES: int = 3
    PROVIDER_STATUS_TTL: int = 60  # seconds

    # Model Settings
    DEFAULT_MAX_TOKENS: Dict[str, int] = {
        "gigachat": 8192,
        "gigachat-pro": 32768,
    }

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    def get_redis_key(self, key: str) -> str:
        """Get Redis key with prefix.

        Args:
            key: Redis key.

        Returns:
            str: Redis key with prefix.
        """
        return f"{self.REDIS_PREFIX}:{key}"

    def get_cache_key(self, key: str) -> str:
        """Get cache key with prefix.

        Args:
            key: Cache key.

        Returns:
            str: Cache key with prefix.
        """
        return f"{self.REDIS_PREFIX}:{self.CACHE_PREFIX}:{key}"

    def get_rate_limit_key(self, api_key: str) -> str:
        """Get rate limit key for API key.

        Args:
            api_key: API key.

        Returns:
            str: Rate limit key.
        """
        return f"{self.REDIS_PREFIX}:rate_limit:{api_key}"


settings = Settings()
