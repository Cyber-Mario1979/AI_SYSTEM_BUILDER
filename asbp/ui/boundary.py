"""UI boundary foundation for ASBP.

M20.1 establishes the UI package as a downstream product-surface boundary
before interaction-flow, visibility, intake, framework, deployment, or SaaS
productization work begins.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UiBoundaryContract:
    """Static contract describing the UI product-surface boundary."""

    layer_name: str
    role: str
    allowed_dependency_direction: tuple[str, ...]
    allowed_display_responsibilities: tuple[str, ...]
    execution_authority: tuple[str, ...]
    forbidden_responsibilities: tuple[str, ...]
    forbidden_direct_access: tuple[str, ...]


UI_BOUNDARY_CONTRACT = UiBoundaryContract(
    layer_name="ui",
    role="downstream_product_surface",
    allowed_dependency_direction=(
        "ui -> api/service boundaries",
    ),
    allowed_display_responsibilities=(
        "governed_workflow_state_visibility",
        "governed_document_export_reporting_visibility",
        "operator_facing_error_and_status_visibility",
    ),
    execution_authority=(
        "no_direct_execution_authority",
        "no_source_truth_authority",
        "no_validation_truth_authority",
        "no_raw_state_mutation_authority",
    ),
    forbidden_responsibilities=(
        "domain_logic_ownership",
        "validation_truth_ownership",
        "source_truth_ownership",
        "execution_truth_ownership",
        "hidden_workflow_rules",
        "cloud_or_deployment_behavior",
        "saas_productization_behavior",
    ),
    forbidden_direct_access=(
        "raw_state_storage",
        "raw_persistence_helpers",
        "direct_state_mutation",
    ),
)


def get_ui_boundary_contract() -> UiBoundaryContract:
    """Return the static UI boundary contract."""

    return UI_BOUNDARY_CONTRACT
