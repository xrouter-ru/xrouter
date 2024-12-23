# Type Checking Guide

## MyPy Configuration

We use MyPy for static type checking in the project. The configuration is defined in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.11"
plugins = []
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
ignore_missing_imports = true
follow_imports = "silent"
disallow_any_generics = false
disallow_subclassing_any = false

[[tool.mypy.overrides]]
module = "redis.*"
ignore_missing_imports = true
follow_imports = "skip"
```

### Key Settings Explained

- `disallow_untyped_defs = true`: All functions must have type annotations
- `check_untyped_defs = true`: Check the body of functions without type annotations
- `ignore_missing_imports = true`: Don't complain about missing stubs for third-party packages
- `follow_imports = "silent"`: Don't complain about followed imports
- `disallow_any_generics = false`: Allow using Any in generics (needed for some third-party packages)
- `disallow_subclassing_any = false`: Allow subclassing Any (needed for Pydantic and SQLAlchemy)

### Redis Type Hints

For Redis, we use version 5.0.1+ which includes built-in type hints. However, MyPy might still have issues with the async module. We handle this by:

1. Using explicit type hints for Redis instances:
```python
from redis.asyncio import Redis

class RedisClient:
    def __init__(self, redis: Redis[Any]) -> None:
        self.redis = redis
```

2. Adding a MyPy override to skip type checking for Redis modules:
```toml
[[tool.mypy.overrides]]
module = "redis.*"
ignore_missing_imports = true
follow_imports = "skip"
```

### SQLAlchemy Models

For SQLAlchemy models, we use the new SQLAlchemy 2.0 type annotations:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

class MyModel(Base):
    __tablename__ = "my_table"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    optional_field: Mapped[Optional[str]] = mapped_column(String(255))
```

### Pydantic Settings

For Pydantic settings, we use the new Pydantic V2 syntax with field validators:

```python
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    @field_validator("some_field", mode="before")
    @classmethod
    def validate_field(cls, v: str) -> str:
        return v
```

## Common Issues and Solutions

1. **Missing Type Stubs**
   - Problem: `Library stubs not installed for "package"`
   - Solution: Install type stubs (`types-package`) or add to mypy overrides

2. **Any in Generics**
   - Problem: `Incompatible types in assignment (expression has type "Any")`
   - Solution: Use explicit type parameters or disable `disallow_any_generics`

3. **Subclassing Any**
   - Problem: `Class cannot subclass "BaseModel" (has type "Any")`
   - Solution: Disable `disallow_subclassing_any` for Pydantic and SQLAlchemy

4. **Untyped Decorators**
   - Problem: `Untyped decorator makes function untyped`
   - Solution: Use `@classmethod` with field validators or add type hints to decorators
