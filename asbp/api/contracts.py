"""Deterministic API request/response contracts for ASBP.

M19.2 defines stable contract shapes only. It does not introduce routes,
framework behavior, endpoint behavior, command execution, or persistence access.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping


class ApiStatus(StrEnum):
    """Stable high-level API response status vocabulary."""

    SUCCESS = "success"
    ERROR = "error"


class ApiResult(StrEnum):
    """Stable operation-result vocabulary for API contract envelopes."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata and payload values must be mappings")

    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class ApiRequest:
    """Stable request envelope for future API adapter intake."""

    operation: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not isinstance(self.operation, str) or not self.operation.strip():
            raise ValueError("operation must be a non-empty string")

        object.__setattr__(self, "operation", self.operation.strip())
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation": self.operation,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ApiError:
    """Stable error contract for rejected API responses."""

    code: str
    message: str
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("error code must be a non-empty string")

        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("error message must be a non-empty string")

        object.__setattr__(self, "code", self.code.strip())
        object.__setattr__(self, "message", self.message.strip())
        object.__setattr__(self, "details", _freeze_mapping(self.details))

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class ApiResponse:
    """Stable response envelope for future API adapter output."""

    status: ApiStatus
    result: ApiResult
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    error: ApiError | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        status = self.status if isinstance(self.status, ApiStatus) else ApiStatus(self.status)
        result = self.result if isinstance(self.result, ApiResult) else ApiResult(self.result)

        if status is ApiStatus.SUCCESS and self.error is not None:
            raise ValueError("success responses must not include an error")

        if status is ApiStatus.ERROR and self.error is None:
            raise ValueError("error responses must include an error")

        object.__setattr__(self, "status", status)
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "result": self.result.value,
            "payload": dict(self.payload),
            "error": None if self.error is None else self.error.to_dict(),
            "metadata": dict(self.metadata),
        }


def build_success_response(
    *,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ApiResponse:
    """Build a deterministic success response envelope."""

    return ApiResponse(
        status=ApiStatus.SUCCESS,
        result=ApiResult.ACCEPTED,
        payload=_freeze_mapping(payload),
        error=None,
        metadata=_freeze_mapping(metadata),
    )


def build_error_response(
    *,
    code: str,
    message: str,
    details: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ApiResponse:
    """Build a deterministic error response envelope."""

    return ApiResponse(
        status=ApiStatus.ERROR,
        result=ApiResult.REJECTED,
        payload=MappingProxyType({}),
        error=ApiError(code=code, message=message, details=_freeze_mapping(details)),
        metadata=_freeze_mapping(metadata),
    )
