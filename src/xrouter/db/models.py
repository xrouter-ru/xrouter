"""Core database models for the xrouter application."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


class APIKey(Base):
    """Model for storing API keys."""

    __tablename__ = "api_keys"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    key_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Balance tracking
    current_balance: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    credit_limit: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, default=500.00
    )


class ProviderStatus(Base):
    """Model for tracking provider status."""

    __tablename__ = "provider_status"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    latency: Mapped[Optional[int]] = mapped_column(Integer)  # in milliseconds
    error_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))  # percentage
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    class Status:
        """Status constants."""

        OPERATIONAL = "operational"
        DEGRADED = "degraded"
        DOWN = "down"
