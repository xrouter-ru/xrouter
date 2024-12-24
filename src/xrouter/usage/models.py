"""Pydantic models for the usage service.

This module contains data validation and serialization models used in the usage service.
These models are used for API requests/responses and internal data transfer.
"""
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class TokenCount(BaseModel):
    """Token count for a specific operation."""

    input: int = Field(..., description="Number of input tokens")
    output: int = Field(..., description="Number of output tokens")
    total: int = Field(..., description="Total number of tokens")
    model: str = Field(..., description="Model used for token counting")

    @validator("total")
    def validate_total(cls, v: int, values: Dict) -> int:
        """Ensure total matches sum of input and output."""
        if "input" in values and "output" in values:
            expected = values["input"] + values["output"]
            if v != expected:
                msg = (
                    f"Total tokens {v} does not match sum of "
                    f"input ({values['input']}) and output ({values['output']})"
                )
                raise ValueError(msg)
        return v


class Cost(BaseModel):
    """Cost calculation for token usage."""

    amount: Decimal = Field(..., description="Total cost amount")
    currency: str = Field(default="RUB", description="Currency of the cost")
    breakdown: Dict[str, Decimal] = Field(
        ...,
        description="Cost breakdown by token type",
        example={"input": Decimal("0.15"), "output": Decimal("0.25")},
    )


class Balance(BaseModel):
    """User balance information."""

    current_balance: Decimal = Field(..., description="Current balance in RUB")
    credit_limit: Decimal = Field(
        default=Decimal("500.00"), description="Maximum allowed credit in RUB"
    )
    total_spent: Decimal = Field(
        default=Decimal("0.00"), description="Total amount spent"
    )
    last_payment: Optional[Decimal] = Field(None, description="Last payment amount")
    last_payment_date: Optional[datetime] = Field(
        None, description="When the last payment was made"
    )


class GenerationStats(BaseModel):
    """Detailed statistics for a single generation."""

    id: UUID = Field(..., description="Unique generation ID")
    timestamp: datetime = Field(..., description="When the generation occurred")
    model: str = Field(..., description="Model identifier (e.g., gigachat/pro)")
    provider: str = Field(..., description="Provider name (e.g., gigachat)")
    app_id: Optional[str] = Field(
        None, description="Application identifier if provided"
    )
    tokens: TokenCount = Field(..., description="Token usage details")
    cost: Cost = Field(..., description="Cost details")
    generation_time: float = Field(
        ..., description="Time taken for generation in seconds"
    )
    speed: float = Field(
        ..., description="Tokens per second processing speed", example=25.5
    )
    success: bool = Field(default=True, description="Whether generation was successful")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    metadata: Optional[Dict] = Field(
        default=None, description="Additional metadata about the generation"
    )


class GenerationListResponse(BaseModel):
    """API response model for UI generation list."""

    data: List[GenerationStats] = Field(..., description="List of generations")
    total: int = Field(..., description="Total number of records")
    has_more: bool = Field(..., description="Whether more records exist")


class StreamProgress(BaseModel):
    """Progress tracking for streaming responses."""

    request_id: UUID = Field(..., description="Request ID for the stream")
    current_tokens: TokenCount = Field(..., description="Current token count")
    estimated_cost: Cost = Field(..., description="Estimated cost so far")
    last_update: datetime = Field(default_factory=datetime.utcnow)
    is_complete: bool = Field(default=False)


class Usage(BaseModel):
    """Complete usage record."""

    id: UUID = Field(..., description="Unique usage record ID")
    api_key: str = Field(..., description="API key used")
    provider: str = Field(..., description="Provider name (e.g., 'gigachat')")
    model: str = Field(..., description="Model name with version")
    tokens: TokenCount = Field(..., description="Token usage details")
    cost: Cost = Field(..., description="Cost details")
    balance_after: Decimal = Field(..., description="Balance after this operation")
    request_id: UUID = Field(..., description="Request ID for correlation")
    is_streaming: bool = Field(
        default=False, description="Whether this was a streaming request"
    )
    metadata: Optional[Dict] = Field(
        default=None,
        description="Additional metadata",
        example={
            "user_id": "user123",
            "tags": ["production", "api-v1"],
            "session_id": "sess_123",
        },
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UsageStats(BaseModel):
    """Aggregated usage statistics."""

    total_tokens: TokenCount = Field(..., description="Total token usage")
    total_cost: Cost = Field(..., description="Total cost")
    current_balance: Decimal = Field(..., description="Current balance")
    request_count: int = Field(..., description="Number of requests")
    average_latency: float = Field(
        ..., description="Average request latency in seconds"
    )
    error_rate: float = Field(..., description="Error rate percentage")
    usage_by_day: List[Dict] = Field(
        ...,
        description="Daily usage breakdown",
        example=[
            {
                "date": "2024-01-01",
                "tokens": {"input": 100, "output": 200, "total": 300},
                "cost": {"amount": "0.50", "currency": "RUB"},
            }
        ],
    )
    generations: List[GenerationStats] = Field(
        ...,
        description="List of individual generations",
        max_items=1000,  # Limit to last 1000 generations
    )


class ModelRate(BaseModel):
    """Pricing configuration for a model."""

    model_id: str = Field(..., description="Model identifier")
    input_rate: Decimal = Field(..., description="Cost per input token in RUB")
    output_rate: Decimal = Field(..., description="Cost per output token in RUB")
    description: Optional[str] = Field(None, description="Rate description")
    effective_from: datetime = Field(
        default_factory=datetime.utcnow, description="When this rate becomes effective"
    )
