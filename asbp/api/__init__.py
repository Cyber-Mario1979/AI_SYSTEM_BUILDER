"""API adapter boundary package.

The API layer is a downstream adapter surface only.
It must consume approved service/runtime/core boundaries and must not own domain logic,
validation truth, or raw persistence access.
"""

from .boundary import API_BOUNDARY_CONTRACT, get_api_boundary_contract
from .contracts import (
    ApiError,
    ApiRequest,
    ApiResponse,
    ApiResult,
    ApiStatus,
    build_error_response,
    build_success_response,
)

__all__ = [
    "API_BOUNDARY_CONTRACT",
    "ApiError",
    "ApiRequest",
    "ApiResponse",
    "ApiResult",
    "ApiStatus",
    "build_error_response",
    "build_success_response",
    "get_api_boundary_contract",
]
