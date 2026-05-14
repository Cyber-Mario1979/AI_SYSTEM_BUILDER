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
from .service_boundary import (
    ALLOWED_API_DEPENDENCY_TARGETS,
    FORBIDDEN_API_DEPENDENCY_TARGETS,
    ApiDependencyDecision,
    ApiDependencyTarget,
    evaluate_api_dependency_target,
    is_api_dependency_target_allowed,
    normalize_dependency_target,
)

__all__ = [
    "ALLOWED_API_DEPENDENCY_TARGETS",
    "API_BOUNDARY_CONTRACT",
    "ApiDependencyDecision",
    "ApiDependencyTarget",
    "ApiError",
    "ApiRequest",
    "ApiResponse",
    "ApiResult",
    "ApiStatus",
    "FORBIDDEN_API_DEPENDENCY_TARGETS",
    "build_error_response",
    "build_success_response",
    "evaluate_api_dependency_target",
    "get_api_boundary_contract",
    "is_api_dependency_target_allowed",
    "normalize_dependency_target",
]
