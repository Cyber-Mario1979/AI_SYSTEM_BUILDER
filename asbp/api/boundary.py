"""API boundary foundation for ASBP.

M19.1 establishes the API package as an adapter boundary before endpoint,
framework, deployment, or UI work begins.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiBoundaryContract:
    """Static contract describing the API adapter boundary."""

    layer_name: str
    role: str
    allowed_dependency_direction: tuple[str, ...]
    forbidden_responsibilities: tuple[str, ...]
    forbidden_direct_access: tuple[str, ...]


API_BOUNDARY_CONTRACT = ApiBoundaryContract(
    layer_name="api",
    role="downstream_adapter",
    allowed_dependency_direction=(
        "api -> approved service/runtime/core boundaries",
    ),
    forbidden_responsibilities=(
        "domain_logic_ownership",
        "validation_truth_ownership",
        "source_truth_ownership",
        "workflow_execution_authority",
        "direct_ai_provider_calls",
        "ui_behavior",
        "cloud_or_deployment_behavior",
    ),
    forbidden_direct_access=(
        "raw_state_storage",
        "raw_persistence_helpers",
        "direct_state_mutation",
    ),
)


def get_api_boundary_contract() -> ApiBoundaryContract:
    """Return the static API boundary contract."""

    return API_BOUNDARY_CONTRACT
