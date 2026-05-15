"""Deterministic UI safety and execution-truth separation for ASBP.

M20.6 defines cross-cutting UI safety contracts and fail-closed behavior. It
does not introduce new UI features, workflow execution, validation authority,
state authority, framework behavior, raw state access, or API/service boundary
bypass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping


class UiSafetyCheckName(StrEnum):
    """Stable supported UI safety-check vocabulary."""

    SOURCE_TRUTH_CLAIM = "source_truth_claim"
    VALIDATION_TRUTH_CLAIM = "validation_truth_claim"
    EXECUTION_TRUTH_CLAIM = "execution_truth_claim"
    API_SERVICE_BOUNDARY_BYPASS = "api_service_boundary_bypass"
    STALE_UI_STATE = "stale_ui_state"
    INVALID_UI_STATE = "invalid_ui_state"
    SILENT_MUTATION_ATTEMPT = "silent_mutation_attempt"


class UiSafetyState(StrEnum):
    """Stable UI state-safety vocabulary."""

    VALID = "valid"
    STALE = "stale"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class UiSafetyDecisionResult(StrEnum):
    """Stable UI safety decision vocabulary."""

    SAFE_FOR_DISPLAY = "safe_for_display"
    REQUIRES_API_SERVICE_REFRESH = "requires_api_service_refresh"
    REJECTED = "rejected"


ALLOWED_UI_SAFETY_CONTEXT_BOUNDARIES: tuple[str, ...] = (
    "api_service_boundary",
    "api_read_surface",
    "service_read_surface",
    "approved_ui_boundary",
)

FORBIDDEN_UI_SAFETY_CONTEXT_BOUNDARIES: tuple[str, ...] = (
    "raw_state_storage",
    "raw_persistence_helpers",
    "direct_state_mutation",
    "ui_source_truth",
    "ui_validation_truth",
    "ui_execution_truth",
    "api_service_boundary_bypass",
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata values must be mappings")

    return MappingProxyType(dict(value))


def normalize_ui_safety_check(value: UiSafetyCheckName | str) -> UiSafetyCheckName:
    """Normalize a UI safety check name or fail closed."""

    if isinstance(value, UiSafetyCheckName):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI safety check must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiSafetyCheckName(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI safety check: {value}") from exc


def normalize_ui_safety_state(value: UiSafetyState | str) -> UiSafetyState:
    """Normalize a UI safety state or fail closed."""

    if isinstance(value, UiSafetyState):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI safety state must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiSafetyState(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI safety state: {value}") from exc


def normalize_ui_safety_context_boundary(value: str) -> str:
    """Normalize a UI safety context boundary or fail closed."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI safety context boundary must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    if normalized in FORBIDDEN_UI_SAFETY_CONTEXT_BOUNDARIES:
        raise ValueError(f"forbidden UI safety context boundary: {value}")

    if normalized not in ALLOWED_UI_SAFETY_CONTEXT_BOUNDARIES:
        raise ValueError(f"unsupported UI safety context boundary: {value}")

    return normalized


@dataclass(frozen=True)
class UiSafetyRuleContract:
    """Static contract describing one UI safety separation rule."""

    check_name: UiSafetyCheckName
    separation_rule: str
    failure_behavior: str
    no_guess_behavior: str
    forbidden_behaviors: tuple[str, ...]
    required_boundary: str | None


@dataclass(frozen=True)
class UiSafetyEvaluationRequest:
    """Stable request envelope for evaluating UI safety and truth separation."""

    check_name: UiSafetyCheckName
    state: UiSafetyState = UiSafetyState.VALID
    context_boundary: str = "api_service_boundary"
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    claims_source_truth: bool = False
    claims_validation_truth: bool = False
    claims_execution_truth: bool = False
    bypasses_api_service_boundary: bool = False
    mutation_requested: bool = False
    no_guess_required: bool = True

    def __post_init__(self) -> None:
        check_name = normalize_ui_safety_check(self.check_name)
        state = normalize_ui_safety_state(self.state)
        context_boundary = normalize_ui_safety_context_boundary(self.context_boundary)

        for field_name in (
            "claims_source_truth",
            "claims_validation_truth",
            "claims_execution_truth",
            "bypasses_api_service_boundary",
            "mutation_requested",
            "no_guess_required",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be a boolean")

        object.__setattr__(self, "check_name", check_name)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "context_boundary", context_boundary)
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "check_name": self.check_name.value,
            "state": self.state.value,
            "context_boundary": self.context_boundary,
            "metadata": dict(self.metadata),
            "claims_source_truth": self.claims_source_truth,
            "claims_validation_truth": self.claims_validation_truth,
            "claims_execution_truth": self.claims_execution_truth,
            "bypasses_api_service_boundary": self.bypasses_api_service_boundary,
            "mutation_requested": self.mutation_requested,
            "no_guess_required": self.no_guess_required,
        }


@dataclass(frozen=True)
class UiSafetyDecision:
    """Deterministic UI safety decision."""

    check_name: UiSafetyCheckName
    result: UiSafetyDecisionResult
    accepted_for_display: bool
    execution_allowed: bool
    mutation_allowed: bool
    reason: str
    required_boundary: str | None = None
    no_guess_enforced: bool = True

    def __post_init__(self) -> None:
        check_name = normalize_ui_safety_check(self.check_name)
        result = (
            self.result
            if isinstance(self.result, UiSafetyDecisionResult)
            else UiSafetyDecisionResult(self.result)
        )

        for field_name in (
            "accepted_for_display",
            "execution_allowed",
            "mutation_allowed",
            "no_guess_enforced",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be a boolean")

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "check_name", check_name)
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "check_name": self.check_name.value,
            "result": self.result.value,
            "accepted_for_display": self.accepted_for_display,
            "execution_allowed": self.execution_allowed,
            "mutation_allowed": self.mutation_allowed,
            "reason": self.reason,
            "required_boundary": self.required_boundary,
            "no_guess_enforced": self.no_guess_enforced,
        }


SUPPORTED_UI_SAFETY_CHECKS: tuple[UiSafetyCheckName, ...] = (
    UiSafetyCheckName.SOURCE_TRUTH_CLAIM,
    UiSafetyCheckName.VALIDATION_TRUTH_CLAIM,
    UiSafetyCheckName.EXECUTION_TRUTH_CLAIM,
    UiSafetyCheckName.API_SERVICE_BOUNDARY_BYPASS,
    UiSafetyCheckName.STALE_UI_STATE,
    UiSafetyCheckName.INVALID_UI_STATE,
    UiSafetyCheckName.SILENT_MUTATION_ATTEMPT,
)


UI_SAFETY_RULE_CONTRACTS: Mapping[UiSafetyCheckName, UiSafetyRuleContract] = MappingProxyType(
    {
        UiSafetyCheckName.SOURCE_TRUTH_CLAIM: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.SOURCE_TRUTH_CLAIM,
            separation_rule="ui_must_not_become_source_truth",
            failure_behavior="reject_source_truth_claim",
            no_guess_behavior="display_source_truth_boundary_message",
            forbidden_behaviors=(
                "ui_source_truth_authority",
                "raw_state_storage_access",
                "silent_source_reconciliation",
            ),
            required_boundary="api/service source boundary",
        ),
        UiSafetyCheckName.VALIDATION_TRUTH_CLAIM: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.VALIDATION_TRUTH_CLAIM,
            separation_rule="ui_must_not_become_validation_truth",
            failure_behavior="reject_validation_truth_claim",
            no_guess_behavior="display_validation_boundary_message",
            forbidden_behaviors=(
                "ui_validation_truth_authority",
                "validation_truth_from_ui_display",
                "silent_validation_pass_or_fail",
            ),
            required_boundary="api/service validation boundary",
        ),
        UiSafetyCheckName.EXECUTION_TRUTH_CLAIM: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.EXECUTION_TRUTH_CLAIM,
            separation_rule="ui_must_not_become_execution_truth",
            failure_behavior="reject_execution_truth_claim",
            no_guess_behavior="display_execution_boundary_message",
            forbidden_behaviors=(
                "ui_execution_truth_authority",
                "autonomous_action_execution",
                "direct_state_mutation",
            ),
            required_boundary="api/service execution boundary",
        ),
        UiSafetyCheckName.API_SERVICE_BOUNDARY_BYPASS: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.API_SERVICE_BOUNDARY_BYPASS,
            separation_rule="ui_must_not_bypass_api_service_boundaries",
            failure_behavior="reject_boundary_bypass",
            no_guess_behavior="display_api_service_boundary_required_message",
            forbidden_behaviors=(
                "api_service_boundary_bypass",
                "hidden_business_rule",
                "direct_dependency_on_raw_state",
            ),
            required_boundary="approved API/service boundary",
        ),
        UiSafetyCheckName.STALE_UI_STATE: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.STALE_UI_STATE,
            separation_rule="stale_ui_state_must_not_be_used_as_truth",
            failure_behavior="require_api_service_refresh",
            no_guess_behavior="present_stale_state_as_blocked_or_unknown",
            forbidden_behaviors=(
                "guess_from_stale_display",
                "silent_refresh_with_mutation",
                "execute_from_stale_state",
            ),
            required_boundary="api/service refresh boundary",
        ),
        UiSafetyCheckName.INVALID_UI_STATE: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.INVALID_UI_STATE,
            separation_rule="invalid_ui_state_must_fail_closed",
            failure_behavior="require_api_service_refresh",
            no_guess_behavior="present_invalid_state_without_auto_correction",
            forbidden_behaviors=(
                "silent_error_correction",
                "execute_from_invalid_state",
                "validation_truth_from_ui_display",
            ),
            required_boundary="api/service validation boundary",
        ),
        UiSafetyCheckName.SILENT_MUTATION_ATTEMPT: UiSafetyRuleContract(
            check_name=UiSafetyCheckName.SILENT_MUTATION_ATTEMPT,
            separation_rule="ui_must_not_mutate_without_approved_command_boundary",
            failure_behavior="reject_silent_mutation",
            no_guess_behavior="display_mutation_blocked_message",
            forbidden_behaviors=(
                "silent_mutation",
                "direct_state_mutation",
                "raw_persistence_helper_access",
            ),
            required_boundary="approved command boundary",
        ),
    }
)


def list_ui_safety_rule_contracts() -> tuple[UiSafetyRuleContract, ...]:
    """Return UI safety rule contracts in deterministic order."""

    return tuple(UI_SAFETY_RULE_CONTRACTS[check] for check in SUPPORTED_UI_SAFETY_CHECKS)


def get_ui_safety_rule_contract(value: UiSafetyCheckName | str) -> UiSafetyRuleContract:
    """Return a UI safety rule contract or fail closed."""

    check_name = normalize_ui_safety_check(value)
    return UI_SAFETY_RULE_CONTRACTS[check_name]


def build_ui_safety_evaluation_request(
    *,
    check_name: UiSafetyCheckName | str,
    state: UiSafetyState | str = UiSafetyState.VALID,
    context_boundary: str = "api_service_boundary",
    metadata: Mapping[str, Any] | None = None,
    claims_source_truth: bool = False,
    claims_validation_truth: bool = False,
    claims_execution_truth: bool = False,
    bypasses_api_service_boundary: bool = False,
    mutation_requested: bool = False,
    no_guess_required: bool = True,
) -> UiSafetyEvaluationRequest:
    """Build a deterministic UI safety evaluation request."""

    return UiSafetyEvaluationRequest(
        check_name=normalize_ui_safety_check(check_name),
        state=normalize_ui_safety_state(state),
        context_boundary=normalize_ui_safety_context_boundary(context_boundary),
        metadata=_freeze_mapping(metadata),
        claims_source_truth=claims_source_truth,
        claims_validation_truth=claims_validation_truth,
        claims_execution_truth=claims_execution_truth,
        bypasses_api_service_boundary=bypasses_api_service_boundary,
        mutation_requested=mutation_requested,
        no_guess_required=no_guess_required,
    )


def evaluate_ui_safety(request: UiSafetyEvaluationRequest) -> UiSafetyDecision:
    """Evaluate UI safety without guessing, executing, or mutating state."""

    if request.claims_source_truth:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REJECTED,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="ui_cannot_become_source_truth",
            required_boundary="api/service source boundary",
            no_guess_enforced=request.no_guess_required,
        )

    if request.claims_validation_truth:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REJECTED,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="ui_cannot_become_validation_truth",
            required_boundary="api/service validation boundary",
            no_guess_enforced=request.no_guess_required,
        )

    if request.claims_execution_truth:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REJECTED,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="ui_cannot_become_execution_truth",
            required_boundary="api/service execution boundary",
            no_guess_enforced=request.no_guess_required,
        )

    if request.bypasses_api_service_boundary:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REJECTED,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="api_service_boundary_bypass_rejected",
            required_boundary="approved API/service boundary",
            no_guess_enforced=request.no_guess_required,
        )

    if request.mutation_requested:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REJECTED,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="ui_safety_rejects_silent_or_direct_mutation",
            required_boundary="approved command boundary",
            no_guess_enforced=request.no_guess_required,
        )

    if request.state in {UiSafetyState.STALE, UiSafetyState.INVALID, UiSafetyState.UNKNOWN}:
        return UiSafetyDecision(
            check_name=request.check_name,
            result=UiSafetyDecisionResult.REQUIRES_API_SERVICE_REFRESH,
            accepted_for_display=False,
            execution_allowed=False,
            mutation_allowed=False,
            reason="ui_state_requires_api_service_refresh",
            required_boundary="api/service refresh or validation boundary",
            no_guess_enforced=True,
        )

    return UiSafetyDecision(
        check_name=request.check_name,
        result=UiSafetyDecisionResult.SAFE_FOR_DISPLAY,
        accepted_for_display=True,
        execution_allowed=False,
        mutation_allowed=False,
        reason="ui_state_safe_for_display_only",
        required_boundary=None,
        no_guess_enforced=request.no_guess_required,
    )
