"""Consolidated external-surface boundary contract for API/UI surfaces.

M21.4 consolidates the external-surface boundary created by M21.1 through M21.3.
It does not introduce new behavior, routes, screens, command execution,
deployment, productization, document generation, standards embedding, or
model/provider integration.
"""

from __future__ import annotations

from dataclasses import dataclass

from .consistency import FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
from .contracts import FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS, FORBIDDEN_EXTERNAL_BEHAVIORS
from .governance import FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    """Return values in first-seen deterministic order without duplicates."""

    return tuple(dict.fromkeys(values))


@dataclass(frozen=True)
class ExternalSurfaceBoundaryContract:
    """Consolidated external-surface boundary contract."""

    package_boundary: str
    discipline_modules: tuple[str, ...]
    preserved_authority_boundaries: tuple[str, ...]
    forbidden_authority_claims: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]
    validation_and_failure_alignment: tuple[str, ...]
    explicit_non_goals: tuple[str, ...]

    def __post_init__(self) -> None:
        tuple_fields = (
            "discipline_modules",
            "preserved_authority_boundaries",
            "forbidden_authority_claims",
            "forbidden_behaviors",
            "validation_and_failure_alignment",
            "explicit_non_goals",
        )

        if not isinstance(self.package_boundary, str) or not self.package_boundary.strip():
            raise ValueError("package_boundary must be a non-empty string")

        for field_name in tuple_fields:
            values = getattr(self, field_name)

            if not isinstance(values, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            if any(not isinstance(item, str) or not item.strip() for item in values):
                raise ValueError(f"{field_name} must contain non-empty strings")

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "package_boundary": self.package_boundary,
            "discipline_modules": self.discipline_modules,
            "preserved_authority_boundaries": self.preserved_authority_boundaries,
            "forbidden_authority_claims": self.forbidden_authority_claims,
            "forbidden_behaviors": self.forbidden_behaviors,
            "validation_and_failure_alignment": self.validation_and_failure_alignment,
            "explicit_non_goals": self.explicit_non_goals,
        }


EXTERNAL_SURFACE_BOUNDARY_CONTRACT = ExternalSurfaceBoundaryContract(
    package_boundary="asbp.external_surface",
    discipline_modules=(
        "asbp.external_surface.contracts",
        "asbp.external_surface.consistency",
        "asbp.external_surface.governance",
    ),
    preserved_authority_boundaries=(
        "governed_engine_truth",
        "service_runtime_domain_boundaries",
        "api_service_validation_before_mutation",
        "ui_and_api_remain_downstream_adapters",
        "external_surface_is_not_source_truth",
        "external_surface_is_not_validation_truth",
        "external_surface_is_not_execution_truth",
    ),
    forbidden_authority_claims=FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    forbidden_behaviors=_ordered_unique(
        (
            *FORBIDDEN_EXTERNAL_BEHAVIORS,
            *FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS,
            *FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS,
        )
    ),
    validation_and_failure_alignment=(
        "fail_closed_for_unsupported_terms",
        "preserve_api_error_rejection_visibility",
        "preserve_ui_api_consistency_with_governed_truth",
        "preserve_command_intake_validation_boundary",
        "preserve_product_surface_governance_boundary",
    ),
    explicit_non_goals=(
        "api_routes",
        "ui_screens",
        "endpoint_behavior",
        "framework_behavior",
        "command_execution",
        "document_generation",
        "standards_embedding",
        "model_provider_integration",
        "cloud_deployment",
        "tenant_saas_behavior",
        "commercial_productization",
    ),
)


def get_external_surface_boundary_contract() -> ExternalSurfaceBoundaryContract:
    """Return the consolidated external-surface boundary contract."""

    return EXTERNAL_SURFACE_BOUNDARY_CONTRACT
