# flake8: noqa  # type: ignore
"""Type stubs for SQLAlchemy to help with mypy checking.

This module provides type annotations for SQLAlchemy constructs
that are challenging for mypy to understand.

IMPORTANT: This module is for use with type checkers ONLY and should NOT
be imported at runtime. Always import the actual SQLAlchemy functions and
classes in your runtime code.

Example usage in a .py file:
    # In runtime code:
    from sqlalchemy import select

    # For type checking only (in a stub file or with TYPE_CHECKING):
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from app.services.sa_types import Select
"""
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


# Add type stubs for SQLAlchemy select constructs
class Select(Generic[T]):
    """Type stub for SQLAlchemy's Select object."""

    def filter(self, *criterion: Any) -> "Select[T]":
        """Filter rows using the provided expressions."""
        return self  # type: ignore

    def filter_by(self, **kwargs: Any) -> "Select[T]":
        """Filter by the given key value pairs."""
        return self  # type: ignore

    def limit(self, limit: int) -> "Select[T]":
        """Apply a LIMIT to the query."""
        return self  # type: ignore

    def offset(self, offset: int) -> "Select[T]":
        """Apply an OFFSET to the query."""
        return self  # type: ignore

    def order_by(self, *clauses: Any) -> "Select[T]":
        """Apply ORDER BY to the query."""
        return self  # type: ignore

    def with_for_update(self, skip_locked: bool = False) -> "Select[T]":
        """Apply FOR UPDATE to the query."""
        return self  # type: ignore


# Type for select function
SelectFunc = Callable[..., Select[T]]


# Make select available as a convenience
def select(*entities: Any, **kwargs: Any) -> Select[T]:
    """Create a SELECT statement."""
    return Select()  # type: ignore
