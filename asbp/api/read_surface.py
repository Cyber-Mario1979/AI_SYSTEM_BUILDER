"""Minimal read-only API surfaces for ASBP.

M19.5 introduces deterministic read-only surfaces over already-governed API
metadata. It does not introduce routes, framework behavior, endpoint behavior,
command execution, state reads, persistence access, or mutation behavior.
"""

from __future__ import annotations

from enum import StrEnum

from .boundary import get_api_boundary_contract
from .contracts import ApiResponse, ApiResult, ApiStatus, build_error_response, build_success_response
from .safety import SAFE_API_INTAKE_ACTIONS, UNSAFE_API_INTAKE_ACTIONS
from .service_boundary import ALLOWED_API_DEPENDENCY_TARGETS, FORBIDDEN_API_DEPENDENCY_TARGETS


class ApiReadSurface(StrEnum):
    """Stable read-only API surface vocabulary."""

    API_BOUNDARY = "api_boundary"
    API_CONTRACTS = "api_contracts"
    SERVICE_BOUNDARY = "service_boundary"
    SAFETY_POLICY = "safety_policy"


SUPPORTED_API_READ_SURFACES = frozenset(surface.value for surface in ApiReadSurface)

_READ_SURFACE_ALIASES = {
    "boundary": ApiReadSurface.API_BOUNDARY.value,
    "api_boundary": ApiReadSurface.API_BOUNDARY.value,
    "contracts": ApiReadSurface.API_CONTRACTS.value,
    "contract": ApiReadSurface.API_CONTRACTS.value,
    "api_contracts": ApiReadSurface.API_CONTRACTS.value,
    "service": ApiReadSurface.SERVICE_BOUNDARY.value,
    "service_boundary": ApiReadSurface.SERVICE_BOUNDARY.value,
    "safety": ApiReadSurface.SAFETY_POLICY.value,
    "safety_policy": ApiReadSurface.SAFETY_POLICY.value,
}


def normalize_api_read_surface(surface: str) -> str:
    """Normalize a read-surface name without guessing unsupported meanings."""

    if not isinstance(surface, str) or not surface.strip():
        raise ValueError("API read surface must be a non-empty string")

    normalized = surface.strip().lower().replace("-", "_").replace(" ", "_")
    return _READ_SURFACE_ALIASES.get(normalized, normalized)


def list_api_read_surfaces() -> ApiResponse:
    """Return the supported read-only API surface names."""

    return build_success_response(
        payload={
            "surfaces": sorted(SUPPORTED_API_READ_SURFACES),
            "read_only": True,
        }
    )


def read_api_surface(surface: str) -> ApiResponse:
    """Read one supported API metadata surface.

    Unknown or invalid surfaces fail closed through deterministic API errors.
    """

    try:
        normalized_surface = normalize_api_read_surface(surface)
    except ValueError as exc:
        return build_error_response(
            code="API_READ_SURFACE_INVALID",
            message=str(exc),
            details={"surface": surface},
        )

    if normalized_surface == ApiReadSurface.API_BOUNDARY.value:
        return build_success_response(
            payload={
                "surface": normalized_surface,
                "read_only": True,
                "data": _api_boundary_payload(),
            }
        )

    if normalized_surface == ApiReadSurface.API_CONTRACTS.value:
        return build_success_response(
            payload={
                "surface": normalized_surface,
                "read_only": True,
                "data": _api_contracts_payload(),
            }
        )

    if normalized_surface == ApiReadSurface.SERVICE_BOUNDARY.value:
        return build_success_response(
            payload={
                "surface": normalized_surface,
                "read_only": True,
                "data": _service_boundary_payload(),
            }
        )

    if normalized_surface == ApiReadSurface.SAFETY_POLICY.value:
        return build_success_response(
            payload={
                "surface": normalized_surface,
                "read_only": True,
                "data": _safety_policy_payload(),
            }
        )

    return build_error_response(
        code="API_READ_SURFACE_UNKNOWN",
        message="API read surface is not recognized and must fail closed.",
        details={
            "surface": normalized_surface,
            "supported_surfaces": sorted(SUPPORTED_API_READ_SURFACES),
        },
    )


def _api_boundary_payload() -> dict[str, object]:
    contract = get_api_boundary_contract()
    return {
        "layer_name": contract.layer_name,
        "role": contract.role,
        "allowed_dependency_direction": list(contract.allowed_dependency_direction),
        "forbidden_responsibilities": list(contract.forbidden_responsibilities),
        "forbidden_direct_access": list(contract.forbidden_direct_access),
    }


def _api_contracts_payload() -> dict[str, object]:
    return {
        "request_fields": ["operation", "payload", "metadata"],
        "response_fields": ["status", "result", "payload", "error", "metadata"],
        "error_fields": ["code", "message", "details"],
        "status_values": sorted(status.value for status in ApiStatus),
        "result_values": sorted(result.value for result in ApiResult),
    }


def _service_boundary_payload() -> dict[str, object]:
    return {
        "allowed_dependency_targets": sorted(ALLOWED_API_DEPENDENCY_TARGETS),
        "forbidden_dependency_targets": sorted(FORBIDDEN_API_DEPENDENCY_TARGETS),
    }


def _safety_policy_payload() -> dict[str, object]:
    return {
        "safe_intake_actions": sorted(SAFE_API_INTAKE_ACTIONS),
        "unsafe_intake_actions": sorted(UNSAFE_API_INTAKE_ACTIONS),
        "fail_closed": True,
    }
