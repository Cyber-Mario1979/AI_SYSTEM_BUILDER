"""Product-surface governance foundation for external API/UI surfaces.

M21.3 defines product-surface governance rules only.
It does not introduce routes, screens, endpoint behavior, command execution,
document generation, standards embedding, model/provider integration,
cloud deployment, tenant/SaaS behavior, commercial productization, or
uncontrolled agentic behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from ._normalization import normalize_labels, normalize_token
from .consistency import FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
from .contracts import (
    FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    ExternalSurfaceChannel,
    ExternalSurfaceRole,
    normalize_external_surface_channel,
    normalize_external_surface_role,
)


class ProductSurfaceExposure(StrEnum):
    """Stable product-surface exposure vocabulary."""

    INTERNAL_GOVERNED = "internal_governed"
    OPERATOR_FACING = "operator_facing"
    PUBLIC_CONSUMER_FACING = "public_consumer_facing"


class ProductSurfaceCapability(StrEnum):
    """Stable product-surface capability vocabulary."""

    VISIBILITY = "visibility"
    COMMAND_INTAKE = "command_intake"
    ERROR_STATUS_PRESENTATION = "error_status_presentation"
    PUBLIC_CONTRACT_REFERENCE = "public_contract_reference"


class ProductSurfaceGovernanceResult(StrEnum):
    """Stable product-surface governance decision vocabulary."""

    ALLOWED = "allowed"
    REJECTED = "rejected"


SUPPORTED_PRODUCT_SURFACE_EXPOSURES: tuple[ProductSurfaceExposure, ...] = (
    ProductSurfaceExposure.INTERNAL_GOVERNED,
    ProductSurfaceExposure.OPERATOR_FACING,
    ProductSurfaceExposure.PUBLIC_CONSUMER_FACING,
)

SUPPORTED_PRODUCT_SURFACE_CAPABILITIES: tuple[ProductSurfaceCapability, ...] = (
    ProductSurfaceCapability.VISIBILITY,
    ProductSurfaceCapability.COMMAND_INTAKE,
    ProductSurfaceCapability.ERROR_STATUS_PRESENTATION,
    ProductSurfaceCapability.PUBLIC_CONTRACT_REFERENCE,
)

FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS: tuple[str, ...] = (
    *FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS,
    "tenant_saas_behavior",
    "commercial_productization",
    "cloud_deployment_implementation",
    "uncontrolled_agentic_behavior",
    "autonomous_action_execution",
    "approval_release_expansion",
    "production_endpoint_behavior",
    "production_ui_screen_behavior",
)


def normalize_product_surface_exposure(
    value: ProductSurfaceExposure | str,
) -> ProductSurfaceExposure:
    """Normalize a product-surface exposure or fail closed."""

    if isinstance(value, ProductSurfaceExposure):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("product surface exposure must be a non-empty string")

    try:
        return ProductSurfaceExposure(normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported product surface exposure: {value}") from exc


def normalize_product_surface_capability(
    value: ProductSurfaceCapability | str,
) -> ProductSurfaceCapability:
    """Normalize a product-surface capability or fail closed."""

    if isinstance(value, ProductSurfaceCapability):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("product surface capability must be a non-empty string")

    try:
        return ProductSurfaceCapability(normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported product surface capability: {value}") from exc


def _normalize_capabilities(
    values: Iterable[ProductSurfaceCapability | str],
) -> tuple[ProductSurfaceCapability, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError("capabilities must be an iterable of product surface capability values")

    return tuple(normalize_product_surface_capability(value) for value in values)


@dataclass(frozen=True)
class ProductSurfaceGovernanceRule:
    """Static governance rule for one external product-surface role."""

    role: ExternalSurfaceRole
    allowed_exposures: tuple[ProductSurfaceExposure, ...]
    allowed_capabilities: tuple[ProductSurfaceCapability, ...]
    command_intake_requires_validation_boundary: bool
    required_truth_boundary: str
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", normalize_external_surface_role(self.role))
        object.__setattr__(
            self,
            "allowed_exposures",
            tuple(normalize_product_surface_exposure(value) for value in self.allowed_exposures),
        )
        object.__setattr__(
            self,
            "allowed_capabilities",
            tuple(
                normalize_product_surface_capability(value)
                for value in self.allowed_capabilities
            ),
        )

        if not isinstance(self.command_intake_requires_validation_boundary, bool):
            raise TypeError("command_intake_requires_validation_boundary must be a bool")

        if not isinstance(self.required_truth_boundary, str) or not self.required_truth_boundary.strip():
            raise ValueError("required_truth_boundary must be a non-empty string")

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "required_truth_boundary", self.required_truth_boundary.strip())
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "role": self.role.value,
            "allowed_exposures": tuple(value.value for value in self.allowed_exposures),
            "allowed_capabilities": tuple(value.value for value in self.allowed_capabilities),
            "command_intake_requires_validation_boundary": (
                self.command_intake_requires_validation_boundary
            ),
            "required_truth_boundary": self.required_truth_boundary,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ProductSurfaceGovernanceDecision:
    """Deterministic product-surface governance decision."""

    result: ProductSurfaceGovernanceResult
    reason: str
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        result = (
            self.result
            if isinstance(self.result, ProductSurfaceGovernanceResult)
            else ProductSurfaceGovernanceResult(self.result)
        )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "result", result)
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, str | None]:
        """Return a deterministic dictionary representation."""

        return {
            "result": self.result.value,
            "reason": self.reason,
            "required_boundary": self.required_boundary,
        }


SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES: tuple[ProductSurfaceGovernanceRule, ...] = (
    ProductSurfaceGovernanceRule(
        role=ExternalSurfaceRole.DOWNSTREAM_ADAPTER,
        allowed_exposures=(
            ProductSurfaceExposure.INTERNAL_GOVERNED,
            ProductSurfaceExposure.PUBLIC_CONSUMER_FACING,
        ),
        allowed_capabilities=(
            ProductSurfaceCapability.PUBLIC_CONTRACT_REFERENCE,
            ProductSurfaceCapability.ERROR_STATUS_PRESENTATION,
        ),
        command_intake_requires_validation_boundary=False,
        required_truth_boundary="inner service/runtime/domain boundaries remain authoritative",
        reason="downstream_adapter_surface_may_expose_contract_reference_only",
    ),
    ProductSurfaceGovernanceRule(
        role=ExternalSurfaceRole.PRODUCT_VISIBILITY_SURFACE,
        allowed_exposures=(
            ProductSurfaceExposure.INTERNAL_GOVERNED,
            ProductSurfaceExposure.OPERATOR_FACING,
            ProductSurfaceExposure.PUBLIC_CONSUMER_FACING,
        ),
        allowed_capabilities=(
            ProductSurfaceCapability.VISIBILITY,
            ProductSurfaceCapability.ERROR_STATUS_PRESENTATION,
            ProductSurfaceCapability.PUBLIC_CONTRACT_REFERENCE,
        ),
        command_intake_requires_validation_boundary=False,
        required_truth_boundary="visibility remains downstream from governed engine truth",
        reason="visibility_surface_may_display_bounded_non_authoritative_state",
    ),
    ProductSurfaceGovernanceRule(
        role=ExternalSurfaceRole.OPERATOR_INTAKE_SURFACE,
        allowed_exposures=(
            ProductSurfaceExposure.INTERNAL_GOVERNED,
            ProductSurfaceExposure.OPERATOR_FACING,
        ),
        allowed_capabilities=(
            ProductSurfaceCapability.COMMAND_INTAKE,
            ProductSurfaceCapability.VISIBILITY,
            ProductSurfaceCapability.ERROR_STATUS_PRESENTATION,
        ),
        command_intake_requires_validation_boundary=True,
        required_truth_boundary="command intake requires API/service validation before mutation",
        reason="operator_intake_surface_collects_intent_without_direct_execution",
    ),
    ProductSurfaceGovernanceRule(
        role=ExternalSurfaceRole.ERROR_STATUS_SURFACE,
        allowed_exposures=(
            ProductSurfaceExposure.INTERNAL_GOVERNED,
            ProductSurfaceExposure.OPERATOR_FACING,
            ProductSurfaceExposure.PUBLIC_CONSUMER_FACING,
        ),
        allowed_capabilities=(
            ProductSurfaceCapability.ERROR_STATUS_PRESENTATION,
            ProductSurfaceCapability.VISIBILITY,
            ProductSurfaceCapability.PUBLIC_CONTRACT_REFERENCE,
        ),
        command_intake_requires_validation_boundary=False,
        required_truth_boundary="error and status presentation remains non-mutating",
        reason="error_status_surface_may_present_bounded_safe_status",
    ),
)


def list_product_surface_governance_rules() -> tuple[ProductSurfaceGovernanceRule, ...]:
    """Return product-surface governance rules in deterministic order."""

    return SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES


def get_product_surface_governance_rule(
    role: ExternalSurfaceRole | str,
) -> ProductSurfaceGovernanceRule:
    """Return the matching product-surface governance rule or fail closed."""

    normalized_role = normalize_external_surface_role(role)

    for rule in SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES:
        if rule.role is normalized_role:
            return rule

    raise ValueError(f"unsupported product-surface governance role: {normalized_role.value}")


def evaluate_product_surface_governance(
    *,
    channel: ExternalSurfaceChannel | str,
    role: ExternalSurfaceRole | str,
    exposure: ProductSurfaceExposure | str,
    capabilities: Iterable[ProductSurfaceCapability | str],
    governed_truth_reference: str | None = "governed_engine",
    validation_boundary: str | None = "api/service validation before mutation",
    authority_claims: Iterable[str] = (),
    behaviors: Iterable[str] = (),
) -> ProductSurfaceGovernanceDecision:
    """Evaluate whether product-surface behavior stays inside M21.3 governance."""

    normalize_external_surface_channel(channel)
    normalized_role = normalize_external_surface_role(role)
    normalized_exposure = normalize_product_surface_exposure(exposure)
    normalized_capabilities = _normalize_capabilities(capabilities)

    normalized_authority_claims = normalize_labels(
        authority_claims,
        field_name="authority_claims",
    )
    normalized_behaviors = normalize_labels(behaviors, field_name="behaviors")

    forbidden_claims = set(normalized_authority_claims).intersection(
        FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    )
    if forbidden_claims:
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="product_surface_cannot_claim_inner_authority",
            required_boundary="preserve governed engine source/validation/execution truth",
        )

    forbidden_behaviors = set(normalized_behaviors).intersection(
        FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    )
    if forbidden_behaviors:
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="product_surface_behavior_outside_phase_7_scope",
            required_boundary="future roadmap-authorized checkpoint required",
        )

    if (
        governed_truth_reference is None
        or not isinstance(governed_truth_reference, str)
        or not governed_truth_reference.strip()
    ):
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="missing_governed_truth_reference",
            required_boundary="product surfaces must remain downstream from governed engine truth",
        )

    rule = get_product_surface_governance_rule(normalized_role)

    if normalized_exposure not in rule.allowed_exposures:
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="product_surface_exposure_not_allowed_for_role",
            required_boundary=rule.required_truth_boundary,
        )

    if (
        normalized_exposure is ProductSurfaceExposure.PUBLIC_CONSUMER_FACING
        and ProductSurfaceCapability.COMMAND_INTAKE in normalized_capabilities
    ):
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="public_consumer_surface_cannot_accept_command_intake",
            required_boundary="public surfaces remain bounded visibility/contract surfaces in Phase 7",
        )

    unsupported_capabilities = tuple(
        value for value in normalized_capabilities if value not in rule.allowed_capabilities
    )
    if unsupported_capabilities:
        if ProductSurfaceCapability.COMMAND_INTAKE in unsupported_capabilities:
            return ProductSurfaceGovernanceDecision(
                result=ProductSurfaceGovernanceResult.REJECTED,
                reason="command_intake_requires_operator_intake_surface",
                required_boundary="operator intake must remain bounded and validated",
            )

        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="product_surface_capability_not_allowed_for_role",
            required_boundary=rule.required_truth_boundary,
        )

    if (
        ProductSurfaceCapability.COMMAND_INTAKE in normalized_capabilities
        and rule.command_intake_requires_validation_boundary
        and (
            validation_boundary is None
            or not isinstance(validation_boundary, str)
            or not validation_boundary.strip()
        )
    ):
        return ProductSurfaceGovernanceDecision(
            result=ProductSurfaceGovernanceResult.REJECTED,
            reason="command_intake_requires_api_service_validation_boundary",
            required_boundary="api/service validation before mutation",
        )

    return ProductSurfaceGovernanceDecision(
        result=ProductSurfaceGovernanceResult.ALLOWED,
        reason="product_surface_governance_allowed",
        required_boundary=rule.required_truth_boundary,
    )
