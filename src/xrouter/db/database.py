"""Database connection and session management."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from xrouter.core.config import settings
from xrouter.db.models import Base


class Database:
    """Database connection manager."""

    def __init__(self) -> None:
        """Initialize database connection."""
        self.engine: AsyncEngine = create_async_engine(
            settings.SQLITE_URL,
            echo=settings.DB_ECHO,
            pool_pre_ping=True,
        )
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_database(self) -> None:
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Create a new database session.

        Yields:
            AsyncSession: Database session.
        """
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
