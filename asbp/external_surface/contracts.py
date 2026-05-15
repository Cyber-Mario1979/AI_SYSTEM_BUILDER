"""Shared external contract discipline for API/UI product surfaces.

M21.1 aligns external API/UI contract vocabulary and boundary rules only.
It does not introduce routes, screens, endpoint behavior, command execution,
document generation, standards embedding, model/provider integration,
deployment behavior, or SaaS/productization behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from asbp.api import ApiResult, ApiStatus
from asbp.ui import UiActionIntakeDecisionResult, UiInteractionFlowName, UiInteractionMode


class ExternalSurfaceChannel(StrEnum):
    """Stable external-surface channel vocabulary."""

    API = "api"
    UI = "ui"


class ExternalSurfaceRole(StrEnum):
    """Stable external-surface role vocabulary."""

    DOWNSTREAM_ADAPTER = "downstream_adapter"
    PRODUCT_VISIBILITY_SURFACE = "product_visibility_surface"
    OPERATOR_INTAKE_SURFACE = "operator_intake_surface"
    ERROR_STATUS_SURFACE = "error_status_surface"


class ExternalContractField(StrEnum):
    """Stable shared external contract field vocabulary."""

    STATUS = "status"
    RESULT = "result"
    ERROR = "error"
    PAYLOAD = "payload"
    METADATA = "metadata"
    REQUEST_ID = "request_id"
    OPERATION = "operation"
    ACTION_NAME = "action_name"
    FLOW_NAME = "flow_name"
    REQUIRED_BOUNDARY = "required_boundary"
    TEMPLATE_ID = "template_id"
    SCHEMA_ID = "schema_id"
    STANDARDS_BUNDLE_REF = "standards_bundle_ref"
    CITATION_REF = "citation_ref"
    LIBRARY_VERSION = "library_version"


class ExternalContractCompatibilityResult(StrEnum):
    """Stable compatibility decision result vocabulary."""

    COMPATIBLE = "compatible"
    REJECTED = "rejected"


SUPPORTED_EXTERNAL_SURFACE_CHANNELS: tuple[ExternalSurfaceChannel, ...] = (
    ExternalSurfaceChannel.API,
    ExternalSurfaceChannel.UI,
)

SUPPORTED_EXTERNAL_SURFACE_ROLES: tuple[ExternalSurfaceRole, ...] = (
    ExternalSurfaceRole.DOWNSTREAM_ADAPTER,
    ExternalSurfaceRole.PRODUCT_VISIBILITY_SURFACE,
    ExternalSurfaceRole.OPERATOR_INTAKE_SURFACE,
    ExternalSurfaceRole.ERROR_STATUS_SURFACE,
)

SUPPORTED_EXTERNAL_CONTRACT_FIELDS: tuple[ExternalContractField, ...] = (
    ExternalContractField.STATUS,
    ExternalContractField.RESULT,
    ExternalContractField.ERROR,
    ExternalContractField.PAYLOAD,
    ExternalContractField.METADATA,
    ExternalContractField.REQUEST_ID,
    ExternalContractField.OPERATION,
    ExternalContractField.ACTION_NAME,
    ExternalContractField.FLOW_NAME,
    ExternalContractField.REQUIRED_BOUNDARY,
    ExternalContractField.TEMPLATE_ID,
    ExternalContractField.SCHEMA_ID,
    ExternalContractField.STANDARDS_BUNDLE_REF,
    ExternalContractField.CITATION_REF,
    ExternalContractField.LIBRARY_VERSION,
)

FUTURE_REFERENCE_PLACEHOLDER_FIELDS: tuple[ExternalContractField, ...] = (
    ExternalContractField.TEMPLATE_ID,
    ExternalContractField.SCHEMA_ID,
    ExternalContractField.STANDARDS_BUNDLE_REF,
    ExternalContractField.CITATION_REF,
    ExternalContractField.LIBRARY_VERSION,
)

FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS: tuple[str, ...] = (
    "source_truth",
    "validation_truth",
    "execution_truth",
    "domain_logic",
    "approval_authority",
    "release_authority",
)

FORBIDDEN_EXTERNAL_BEHAVIORS: tuple[str, ...] = (
    "raw_state_access",
    "raw_persistence_access",
    "direct_storage_access",
    "hidden_domain_mutation",
    "ui_api_source_truth",
    "document_generation",
    "report_generation",
    "export_generation",
    "standards_embedding",
    "standards_citation_authority",
    "model_provider_integration",
    "cloud_deployment",
    "saas_productization",
)


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_external_surface_channel(
    value: ExternalSurfaceChannel | str,
) -> ExternalSurfaceChannel:
    """Normalize an external-surface channel or fail closed."""

    if isinstance(value, ExternalSurfaceChannel):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("external surface channel must be a non-empty string")

    try:
        return ExternalSurfaceChannel(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported external surface channel: {value}") from exc


def normalize_external_surface_role(
    value: ExternalSurfaceRole | str,
) -> ExternalSurfaceRole:
    """Normalize an external-surface role or fail closed."""

    if isinstance(value, ExternalSurfaceRole):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("external surface role must be a non-empty string")

    try:
        return ExternalSurfaceRole(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported external surface role: {value}") from exc


def normalize_external_contract_field(
    value: ExternalContractField | str,
) -> ExternalContractField:
    """Normalize an external contract field or fail closed."""

    if isinstance(value, ExternalContractField):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("external contract field must be a non-empty string")

    try:
        return ExternalContractField(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported external contract field: {value}") from exc


def get_supported_external_contract_fields() -> tuple[ExternalContractField, ...]:
    """Return supported shared external contract fields in deterministic order."""

    return SUPPORTED_EXTERNAL_CONTRACT_FIELDS


@dataclass(frozen=True)
class ExternalContractDiscipline:
    """Static discipline contract for one external API/UI surface role."""

    channel: ExternalSurfaceChannel
    role: ExternalSurfaceRole
    shared_status_values: tuple[str, ...]
    shared_result_values: tuple[str, ...]
    shared_ui_decision_values: tuple[str, ...]
    shared_ui_flow_values: tuple[str, ...]
    shared_ui_mode_values: tuple[str, ...]
    shared_error_fields: tuple[str, ...]
    shared_payload_fields: tuple[str, ...]
    future_reference_placeholders: tuple[str, ...]
    forbidden_authority_claims: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "channel",
            normalize_external_surface_channel(self.channel),
        )
        object.__setattr__(
            self,
            "role",
            normalize_external_surface_role(self.role),
        )

        tuple_fields = (
            "shared_status_values",
            "shared_result_values",
            "shared_ui_decision_values",
            "shared_ui_flow_values",
            "shared_ui_mode_values",
            "shared_error_fields",
            "shared_payload_fields",
            "future_reference_placeholders",
            "forbidden_authority_claims",
            "forbidden_behaviors",
        )

        for field_name in tuple_fields:
            values = getattr(self, field_name)

            if not isinstance(values, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            if any(not isinstance(item, str) or not item.strip() for item in values):
                raise ValueError(f"{field_name} must contain non-empty strings")

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "channel": self.channel.value,
            "role": self.role.value,
            "shared_status_values": self.shared_status_values,
            "shared_result_values": self.shared_result_values,
            "shared_ui_decision_values": self.shared_ui_decision_values,
            "shared_ui_flow_values": self.shared_ui_flow_values,
            "shared_ui_mode_values": self.shared_ui_mode_values,
            "shared_error_fields": self.shared_error_fields,
            "shared_payload_fields": self.shared_payload_fields,
            "future_reference_placeholders": self.future_reference_placeholders,
            "forbidden_authority_claims": self.forbidden_authority_claims,
            "forbidden_behaviors": self.forbidden_behaviors,
        }


@dataclass(frozen=True)
class ExternalContractCompatibilityDecision:
    """Deterministic compatibility decision for external contract terms."""

    result: ExternalContractCompatibilityResult
    reason: str
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        result = (
            self.result
            if isinstance(self.result, ExternalContractCompatibilityResult)
            else ExternalContractCompatibilityResult(self.result)
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


def build_external_contract_discipline(
    *,
    channel: ExternalSurfaceChannel | str,
    role: ExternalSurfaceRole | str,
) -> ExternalContractDiscipline:
    """Build a deterministic shared external-surface discipline contract."""

    return ExternalContractDiscipline(
        channel=normalize_external_surface_channel(channel),
        role=normalize_external_surface_role(role),
        shared_status_values=tuple(status.value for status in ApiStatus),
        shared_result_values=tuple(result.value for result in ApiResult),
        shared_ui_decision_values=tuple(result.value for result in UiActionIntakeDecisionResult),
        shared_ui_flow_values=tuple(flow.value for flow in UiInteractionFlowName),
        shared_ui_mode_values=tuple(mode.value for mode in UiInteractionMode),
        shared_error_fields=("code", "message", "details"),
        shared_payload_fields=tuple(field.value for field in SUPPORTED_EXTERNAL_CONTRACT_FIELDS),
        future_reference_placeholders=tuple(
            field.value for field in FUTURE_REFERENCE_PLACEHOLDER_FIELDS
        ),
        forbidden_authority_claims=FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
        forbidden_behaviors=FORBIDDEN_EXTERNAL_BEHAVIORS,
    )


def _normalize_contract_fields(
    fields: Iterable[ExternalContractField | str],
) -> tuple[ExternalContractField, ...]:
    if isinstance(fields, (str, bytes)):
        raise TypeError("fields must be an iterable of external contract field values")

    return tuple(normalize_external_contract_field(field) for field in fields)


def evaluate_external_contract_compatibility(
    *,
    channel: ExternalSurfaceChannel | str,
    role: ExternalSurfaceRole | str,
    fields: Iterable[ExternalContractField | str],
    authority_claims: Iterable[str] = (),
    behaviors: Iterable[str] = (),
) -> ExternalContractCompatibilityDecision:
    """Evaluate whether external contract terms stay inside M21.1 discipline."""

    normalize_external_surface_channel(channel)
    normalize_external_surface_role(role)
    normalized_fields = _normalize_contract_fields(fields)

    normalized_authority_claims = tuple(_normalize_token(claim) for claim in authority_claims)
    normalized_behaviors = tuple(_normalize_token(behavior) for behavior in behaviors)

    forbidden_claims = set(normalized_authority_claims).intersection(
        FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    )
    if forbidden_claims:
        return ExternalContractCompatibilityDecision(
            result=ExternalContractCompatibilityResult.REJECTED,
            reason="external_surface_cannot_claim_inner_authority",
            required_boundary="preserve governed engine source/validation/execution truth",
        )

    forbidden_behaviors = set(normalized_behaviors).intersection(FORBIDDEN_EXTERNAL_BEHAVIORS)
    if forbidden_behaviors:
        return ExternalContractCompatibilityDecision(
            result=ExternalContractCompatibilityResult.REJECTED,
            reason="external_surface_behavior_outside_m21_1_scope",
            required_boundary="future roadmap-authorized checkpoint required",
        )

    if any(field in FUTURE_REFERENCE_PLACEHOLDER_FIELDS for field in normalized_fields):
        return ExternalContractCompatibilityDecision(
            result=ExternalContractCompatibilityResult.COMPATIBLE,
            reason="compatible_with_deferred_future_reference_placeholders",
            required_boundary=(
                "placeholder reference only; deferred dependency closure required "
                "before productized implementation"
            ),
        )

    return ExternalContractCompatibilityDecision(
        result=ExternalContractCompatibilityResult.COMPATIBLE,
        reason="compatible_with_shared_external_contract_discipline",
        required_boundary=None,
    )