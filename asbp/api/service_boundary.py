"""API service-boundary consumption rules for ASBP.

M19.3 defines how API adapters may depend on approved service/runtime/core
boundaries. It does not introduce routes, framework behavior, endpoint behavior,
command execution, domain logic duplication, or persistence access.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .contracts import ApiResponse, build_error_response, build_success_response


class ApiDependencyTarget(StrEnum):
    """Stable dependency-target vocabulary for API adapter boundary checks."""

    SERVICE = "service"
    RUNTIME = "runtime"
    CORE = "core"
    RAW_STATE = "raw_state"
    RAW_PERSISTENCE = "raw_persistence"
    DIRECT_STORAGE = "direct_storage"


ALLOWED_API_DEPENDENCY_TARGETS = frozenset(
    {
        ApiDependencyTarget.SERVICE.value,
        ApiDependencyTarget.RUNTIME.value,
        ApiDependencyTarget.CORE.value,
    }
)

FORBIDDEN_API_DEPENDENCY_TARGETS = frozenset(
    {
        ApiDependencyTarget.RAW_STATE.value,
        ApiDependencyTarget.RAW_PERSISTENCE.value,
        ApiDependencyTarget.DIRECT_STORAGE.value,
    }
)


@dataclass(frozen=True)
class ApiDependencyDecision:
    """Deterministic decision for one proposed API dependency target."""

    target: str
    normalized_target: str
    allowed: bool
    reason: str
    response: ApiResponse

    def to_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "normalized_target": self.normalized_target,
            "allowed": self.allowed,
            "reason": self.reason,
            "response": self.response.to_dict(),
        }


def normalize_dependency_target(target: str) -> str:
    """Normalize a proposed dependency target without guessing its meaning."""

    if not isinstance(target, str) or not target.strip():
        raise ValueError("dependency target must be a non-empty string")

    return target.strip().lower().replace("-", "_").replace(" ", "_")


def evaluate_api_dependency_target(target: str) -> ApiDependencyDecision:
    """Evaluate whether an API adapter dependency target is allowed."""

    normalized_target = normalize_dependency_target(target)

    if normalized_target in ALLOWED_API_DEPENDENCY_TARGETS:
        return ApiDependencyDecision(
            target=target,
            normalized_target=normalized_target,
            allowed=True,
            reason="approved_api_boundary_target",
            response=build_success_response(
                payload={
                    "target": normalized_target,
                    "allowed": True,
                    "reason": "approved_api_boundary_target",
                }
            ),
        )

    if normalized_target in FORBIDDEN_API_DEPENDENCY_TARGETS:
        return ApiDependencyDecision(
            target=target,
            normalized_target=normalized_target,
            allowed=False,
            reason="forbidden_raw_state_or_persistence_target",
            response=build_error_response(
                code="API_BOUNDARY_FORBIDDEN_TARGET",
                message=(
                    "API adapters must not depend on raw state, raw persistence, "
                    "or direct storage targets."
                ),
                details={
                    "target": normalized_target,
                    "allowed_targets": sorted(ALLOWED_API_DEPENDENCY_TARGETS),
                },
            ),
        )

    return ApiDependencyDecision(
        target=target,
        normalized_target=normalized_target,
        allowed=False,
        reason="unknown_unapproved_api_dependency_target",
        response=build_error_response(
            code="API_BOUNDARY_UNKNOWN_TARGET",
            message="API adapter dependency target is not approved.",
            details={
                "target": normalized_target,
                "allowed_targets": sorted(ALLOWED_API_DEPENDENCY_TARGETS),
            },
        ),
    )


def is_api_dependency_target_allowed(target: str) -> bool:
    """Return whether a proposed API dependency target is approved."""

    return evaluate_api_dependency_target(target).allowed
