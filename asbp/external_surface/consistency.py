"""Deterministic UI/API consistency rules for external surfaces.

M21.2 defines consistency rules between UI displays and API responses.
It does not introduce routes, screens, endpoint behavior, command execution,
document generation, standards embedding, model/provider integration,
deployment behavior, or SaaS/productization behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from asbp.api import ApiResult, ApiStatus
from asbp.ui import UiActionIntakeDecisionResult

from .contracts import (
    FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    FORBIDDEN_EXTERNAL_BEHAVIORS,
    ExternalSurfaceChannel,
    ExternalSurfaceRole,
    normalize_external_surface_channel,
    normalize_external_surface_role,
)


class OperatorVisibleState(StrEnum):
    """Stable operator-visible state vocabulary for UI/API consistency."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ERROR_VISIBLE = "error_visible"
    VALIDATION_REQUIRED = "validation_required"
    DISPLAY_ONLY = "display_only"
    BLOCKED = "blocked"


class UiApiConsistencyResult(StrEnum):
    """Stable UI/API consistency decision result vocabulary."""

    CONSISTENT = "consistent"
    REJECTED = "rejected"


FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS: tuple[str, ...] = (
    *FORBIDDEN_EXTERNAL_BEHAVIORS,
    "ui_api_hidden_domain_logic",
    "service_boundary_bypass",
    "governed_truth_override",
    "silent_status_translation",
)


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _normalize_labels(values: Iterable[str], *, field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of strings")

    normalized: list[str] = []

    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must contain non-empty strings")

        normalized.append(_normalize_token(value))

    return tuple(normalized)


def _normalize_api_status(value: ApiStatus | str) -> ApiStatus:
    if isinstance(value, ApiStatus):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("API status must be a non-empty string")

    try:
        return ApiStatus(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported API status: {value}") from exc


def _normalize_api_result(value: ApiResult | str) -> ApiResult:
    if isinstance(value, ApiResult):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("API result must be a non-empty string")

    try:
        return ApiResult(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported API result: {value}") from exc


def _normalize_ui_decision_result(
    value: UiActionIntakeDecisionResult | str,
) -> UiActionIntakeDecisionResult:
    if isinstance(value, UiActionIntakeDecisionResult):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI decision result must be a non-empty string")

    try:
        return UiActionIntakeDecisionResult(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported UI decision result: {value}") from exc


def normalize_operator_visible_state(
    value: OperatorVisibleState | str,
) -> OperatorVisibleState:
    """Normalize an operator-visible state or fail closed."""

    if isinstance(value, OperatorVisibleState):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("operator visible state must be a non-empty string")

    try:
        return OperatorVisibleState(_normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported operator visible state: {value}") from exc


@dataclass(frozen=True)
class UiApiConsistencyRule:
    """Static rule for one API response outcome and allowed UI presentation."""

    api_status: ApiStatus
    api_result: ApiResult
    allowed_ui_decision_results: tuple[UiActionIntakeDecisionResult, ...]
    allowed_operator_visible_states: tuple[OperatorVisibleState, ...]
    forbidden_operator_visible_states: tuple[OperatorVisibleState, ...]
    required_truth_boundary: str
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "api_status", _normalize_api_status(self.api_status))
        object.__setattr__(self, "api_result", _normalize_api_result(self.api_result))
        object.__setattr__(
            self,
            "allowed_ui_decision_results",
            tuple(
                _normalize_ui_decision_result(value)
                for value in self.allowed_ui_decision_results
            ),
        )
        object.__setattr__(
            self,
            "allowed_operator_visible_states",
            tuple(
                normalize_operator_visible_state(value)
                for value in self.allowed_operator_visible_states
            ),
        )
        object.__setattr__(
            self,
            "forbidden_operator_visible_states",
            tuple(
                normalize_operator_visible_state(value)
                for value in self.forbidden_operator_visible_states
            ),
        )

        if not isinstance(self.required_truth_boundary, str) or not self.required_truth_boundary.strip():
            raise ValueError("required_truth_boundary must be a non-empty string")

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "required_truth_boundary", self.required_truth_boundary.strip())
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "api_status": self.api_status.value,
            "api_result": self.api_result.value,
            "allowed_ui_decision_results": tuple(
                value.value for value in self.allowed_ui_decision_results
            ),
            "allowed_operator_visible_states": tuple(
                value.value for value in self.allowed_operator_visible_states
            ),
            "forbidden_operator_visible_states": tuple(
                value.value for value in self.forbidden_operator_visible_states
            ),
            "required_truth_boundary": self.required_truth_boundary,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class UiApiConsistencyDecision:
    """Deterministic consistency decision for one UI/API visible-state check."""

    result: UiApiConsistencyResult
    reason: str
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        result = (
            self.result
            if isinstance(self.result, UiApiConsistencyResult)
            else UiApiConsistencyResult(self.result)
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


SUPPORTED_UI_API_CONSISTENCY_RULES: tuple[UiApiConsistencyRule, ...] = (
    UiApiConsistencyRule(
        api_status=ApiStatus.SUCCESS,
        api_result=ApiResult.ACCEPTED,
        allowed_ui_decision_results=(
            UiActionIntakeDecisionResult.ACCEPTED_FOR_DISPLAY,
            UiActionIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION,
        ),
        allowed_operator_visible_states=(
            OperatorVisibleState.ACCEPTED,
            OperatorVisibleState.DISPLAY_ONLY,
            OperatorVisibleState.VALIDATION_REQUIRED,
        ),
        forbidden_operator_visible_states=(
            OperatorVisibleState.REJECTED,
            OperatorVisibleState.ERROR_VISIBLE,
            OperatorVisibleState.BLOCKED,
        ),
        required_truth_boundary="governed engine truth remains authoritative",
        reason="api_success_may_be_displayed_or_require_validation_without_mutation",
    ),
    UiApiConsistencyRule(
        api_status=ApiStatus.ERROR,
        api_result=ApiResult.REJECTED,
        allowed_ui_decision_results=(
            UiActionIntakeDecisionResult.ACCEPTED_FOR_DISPLAY,
            UiActionIntakeDecisionResult.REJECTED,
        ),
        allowed_operator_visible_states=(
            OperatorVisibleState.REJECTED,
            OperatorVisibleState.ERROR_VISIBLE,
            OperatorVisibleState.BLOCKED,
        ),
        forbidden_operator_visible_states=(
            OperatorVisibleState.ACCEPTED,
            OperatorVisibleState.VALIDATION_REQUIRED,
        ),
        required_truth_boundary="governed engine rejection remains visible",
        reason="api_error_must_remain_rejected_or_error_visible",
    ),
)


def list_ui_api_consistency_rules() -> tuple[UiApiConsistencyRule, ...]:
    """Return UI/API consistency rules in deterministic order."""

    return SUPPORTED_UI_API_CONSISTENCY_RULES


def get_ui_api_consistency_rule(
    *,
    api_status: ApiStatus | str,
    api_result: ApiResult | str,
) -> UiApiConsistencyRule:
    """Return the matching UI/API consistency rule or fail closed."""

    normalized_status = _normalize_api_status(api_status)
    normalized_result = _normalize_api_result(api_result)

    for rule in SUPPORTED_UI_API_CONSISTENCY_RULES:
        if rule.api_status is normalized_status and rule.api_result is normalized_result:
            return rule

    raise ValueError(
        "unsupported API status/result combination for UI/API consistency: "
        f"{normalized_status.value}/{normalized_result.value}"
    )


def evaluate_ui_api_consistency(
    *,
    api_status: ApiStatus | str,
    api_result: ApiResult | str,
    ui_decision_result: UiActionIntakeDecisionResult | str,
    operator_visible_state: OperatorVisibleState | str,
    channel: ExternalSurfaceChannel | str = ExternalSurfaceChannel.UI,
    role: ExternalSurfaceRole | str = ExternalSurfaceRole.PRODUCT_VISIBILITY_SURFACE,
    governed_truth_reference: str | None = "governed_engine",
    authority_claims: Iterable[str] = (),
    behaviors: Iterable[str] = (),
) -> UiApiConsistencyDecision:
    """Evaluate whether UI-visible state remains consistent with an API response."""

    normalize_external_surface_channel(channel)
    normalize_external_surface_role(role)

    normalized_status = _normalize_api_status(api_status)
    normalized_result = _normalize_api_result(api_result)
    normalized_ui_decision = _normalize_ui_decision_result(ui_decision_result)
    normalized_visible_state = normalize_operator_visible_state(operator_visible_state)

    normalized_authority_claims = _normalize_labels(
        authority_claims,
        field_name="authority_claims",
    )
    normalized_behaviors = _normalize_labels(behaviors, field_name="behaviors")

    forbidden_claims = set(normalized_authority_claims).intersection(
        FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    )
    if forbidden_claims:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="ui_api_consistency_cannot_claim_inner_authority",
            required_boundary="preserve governed engine source/validation/execution truth",
        )

    forbidden_behaviors = set(normalized_behaviors).intersection(
        FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
    )
    if forbidden_behaviors:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="ui_api_consistency_behavior_outside_m21_2_scope",
            required_boundary="service boundary and future roadmap-authorized checkpoint required",
        )

    if (
        governed_truth_reference is None
        or not isinstance(governed_truth_reference, str)
        or not governed_truth_reference.strip()
    ):
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="missing_governed_truth_reference",
            required_boundary="operator-visible state must reference governed engine truth",
        )

    try:
        rule = get_ui_api_consistency_rule(
            api_status=normalized_status,
            api_result=normalized_result,
        )
    except ValueError:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="unsupported_api_status_result_combination",
            required_boundary="preserve stable API response contract vocabulary",
        )

    if normalized_ui_decision not in rule.allowed_ui_decision_results:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="ui_decision_diverges_from_api_response",
            required_boundary=rule.required_truth_boundary,
        )

    if normalized_visible_state in rule.forbidden_operator_visible_states:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="operator_visible_state_diverges_from_api_response",
            required_boundary=rule.required_truth_boundary,
        )

    if normalized_visible_state not in rule.allowed_operator_visible_states:
        return UiApiConsistencyDecision(
            result=UiApiConsistencyResult.REJECTED,
            reason="unsupported_operator_visible_state_for_api_response",
            required_boundary=rule.required_truth_boundary,
        )

    return UiApiConsistencyDecision(
        result=UiApiConsistencyResult.CONSISTENT,
        reason="ui_api_consistent_with_governed_truth",
        required_boundary=rule.required_truth_boundary,
    )