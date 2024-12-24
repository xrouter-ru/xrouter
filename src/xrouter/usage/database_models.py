"""Database models for the usage service."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from xrouter.db.models import APIKey, Base


class ModelRate(Base):
    """Model for storing token pricing rates."""

    __tablename__ = "model_rates"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    model_id: Mapped[str] = mapped_column(String(100), nullable=False)
    input_rate: Mapped[float] = mapped_column(
        Numeric(10, 6), nullable=False, comment="Cost per input token in RUB"
    )
    output_rate: Mapped[float] = mapped_column(
        Numeric(10, 6), nullable=False, comment="Cost per output token in RUB"
    )
    description: Mapped[Optional[str]] = mapped_column(String(500))
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Generation(Base):
    """Model for storing detailed generation statistics."""

    __tablename__ = "generations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    api_key_id: Mapped[UUID] = mapped_column(ForeignKey("api_keys.id"))
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    app_id: Mapped[Optional[str]] = mapped_column(String(100))

    # Token counts
    tokens_input: Mapped[int] = mapped_column(Integer, nullable=False)
    tokens_output: Mapped[int] = mapped_column(Integer, nullable=False)
    tokens_total: Mapped[int] = mapped_column(Integer, nullable=False)

    # Cost tracking
    cost_amount: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    cost_breakdown: Mapped[dict] = mapped_column(
        JSON, nullable=False, comment="Cost breakdown by token type"
    )
    balance_after: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Performance metrics
    generation_time: Mapped[float] = mapped_column(
        Numeric(10, 3), nullable=False, comment="Time taken for generation in seconds"
    )
    speed: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, comment="Tokens per second"
    )

    # Status
    success: Mapped[bool] = mapped_column(default=True)
    error: Mapped[Optional[str]] = mapped_column(String(500))
    is_streaming: Mapped[bool] = mapped_column(default=False)

    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    api_key: Mapped["APIKey"] = relationship("APIKey", backref="generations")


class Usage(Base):
    """Model for tracking aggregated API usage."""

    __tablename__ = "usage"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    api_key_id: Mapped[UUID] = mapped_column(ForeignKey("api_keys.id"))
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Daily aggregates
    total_requests: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens_input: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens_output: Mapped[int] = mapped_column(Integer, default=0)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 6), default=0)

    # Performance metrics
    average_latency: Mapped[float] = mapped_column(Numeric(10, 3), default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    api_key: Mapped["APIKey"] = relationship("APIKey", backref="usage_records")
