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
from .safety import (
    SAFE_API_INTAKE_ACTIONS,
    UNSAFE_API_INTAKE_ACTIONS,
    ApiSafetyAction,
    ApiSafetyDecision,
    evaluate_api_intake_safety,
    is_api_intake_action_allowed,
    normalize_api_intake_action,
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
    "ApiSafetyAction",
    "ApiSafetyDecision",
    "ApiStatus",
    "FORBIDDEN_API_DEPENDENCY_TARGETS",
    "SAFE_API_INTAKE_ACTIONS",
    "UNSAFE_API_INTAKE_ACTIONS",
    "build_error_response",
    "build_success_response",
    "evaluate_api_dependency_target",
    "evaluate_api_intake_safety",
    "get_api_boundary_contract",
    "is_api_dependency_target_allowed",
    "is_api_intake_action_allowed",
    "normalize_api_intake_action",
    "normalize_dependency_target",
]
