"""Internal normalization helpers for external-surface modules.

This module is private to ``asbp.external_surface``. It consolidates repeated
normalization helper logic without changing the public external-surface contract.
"""

from __future__ import annotations

from typing import Iterable


def normalize_token(value: str) -> str:
    """Normalize a non-empty string token or fail closed."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("value must be a non-empty string")

    return value.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_labels(values: Iterable[str], *, field_name: str) -> tuple[str, ...]:
    """Normalize an iterable of label strings or fail closed."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of strings")

    normalized: list[str] = []

    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must contain non-empty strings")

        normalized.append(normalize_token(value))

    return tuple(normalized)
