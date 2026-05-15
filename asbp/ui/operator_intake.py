"""Deterministic UI operator action/intake boundary for ASBP.

M20.5 defines limited UI operator-intake contracts over stable API/service
command boundaries. It does not introduce UI-originated business rules, direct
execution, raw state mutation, autonomous action behavior, approval/release
authority, framework behavior, or persistence access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .interaction_flow import (
    UiInteractionFlowName,
    UiInteractionMode,
    normalize_ui_interaction_flow,
    normalize_ui_interaction_mode,
)


class UiOperatorIntakeActionName(StrEnum):
    """Stable supported UI operator-intake action vocabulary."""

    PREVIEW_OPERATOR_ACTION = "preview_operator_action"
    VALIDATE_OPERATOR_ACTION = "validate_operator_action"
    PREPARE_API_SERVICE_INTAKE = "prepare_api_service_intake"


class UiOperatorIntakeDecisionResult(StrEnum):
    """Stable UI operator-intake decision vocabulary."""

    ACCEPTED_FOR_PREVIEW = "accepted_for_preview"
    REQUIRES_API_SERVICE_VALIDATION = "requires_api_service_validation"
    REJECTED = "rejected"


ALLOWED_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES: tuple[str, ...] = (
    "api_command_intake",
    "service_command_boundary",
    "api_service_command_boundary",
    "approved_command_boundary",
)

FORBIDDEN_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES: tuple[str, ...] = (
    "raw_state_storage",
    "raw_persistence_helpers",
    "direct_state_mutation",
    "ui_direct_execution",
    "approval_release_authority",
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata and payload values must be mappings")

    return MappingProxyType(dict(value))


def normalize_ui_operator_intake_action(
    value: UiOperatorIntakeActionName | str,
) -> UiOperatorIntakeActionName:
    """Normalize a UI operator-intake action or fail closed."""

    if isinstance(value, UiOperatorIntakeActionName):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI operator intake action must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    aliases = {
        "preview": UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION.value,
        "preview_action": UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION.value,
        "preview_operator_action": UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION.value,
        "validate": UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION.value,
        "validate_action": UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION.value,
        "validate_operator_action": UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION.value,
        "prepare": UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE.value,
        "prepare_api_service_intake": UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE.value,
        "submit_to_api_service": UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE.value,
    }

    normalized = aliases.get(normalized, normalized)

    try:
        return UiOperatorIntakeActionName(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI operator intake action: {value}") from exc


def normalize_ui_operator_intake_target_boundary(value: str) -> str:
    """Normalize a UI operator-intake target boundary or fail closed."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI operator intake target boundary must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    if normalized in FORBIDDEN_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES:
        raise ValueError(f"forbidden UI operator intake target boundary: {value}")

    if normalized not in ALLOWED_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES:
        raise ValueError(f"unsupported UI operator intake target boundary: {value}")

    return normalized


@dataclass(frozen=True)
class UiOperatorIntakeActionContract:
    """Static contract describing one limited UI operator-intake action."""

    action_name: UiOperatorIntakeActionName
    interaction_flow: UiInteractionFlowName
    mode: UiInteractionMode
    target_boundary_expectations: tuple[str, ...]
    intake_responsibilities: tuple[str, ...]
    validation_rules: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]


@dataclass(frozen=True)
class UiOperatorIntakeRequest:
    """Stable UI operator-intake envelope for future UI adapter behavior."""

    action_name: UiOperatorIntakeActionName
    target_boundary: str = "api_command_intake"
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    interaction_flow: UiInteractionFlowName = UiInteractionFlowName.OPERATOR_COMMAND_INTAKE
    mode: UiInteractionMode = UiInteractionMode.COMMAND_CAPABLE
    execute: bool = False
    approval_release_requested: bool = False

    def __post_init__(self) -> None:
        action_name = normalize_ui_operator_intake_action(self.action_name)
        target_boundary = normalize_ui_operator_intake_target_boundary(self.target_boundary)
        interaction_flow = normalize_ui_interaction_flow(self.interaction_flow)
        mode = normalize_ui_interaction_mode(self.mode)

        if interaction_flow is not UiInteractionFlowName.OPERATOR_COMMAND_INTAKE:
            raise ValueError("operator intake requests must use the operator_command_intake interaction flow")

        if mode is not UiInteractionMode.COMMAND_CAPABLE:
            raise ValueError("operator intake requests must use command-capable mode")

        if not isinstance(self.execute, bool):
            raise TypeError("execute must be a boolean")

        if not isinstance(self.approval_release_requested, bool):
            raise TypeError("approval_release_requested must be a boolean")

        object.__setattr__(self, "action_name", action_name)
        object.__setattr__(self, "target_boundary", target_boundary)
        object.__setattr__(self, "interaction_flow", interaction_flow)
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "action_name": self.action_name.value,
            "interaction_flow": self.interaction_flow.value,
            "mode": self.mode.value,
            "target_boundary": self.target_boundary,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
            "execute": self.execute,
            "approval_release_requested": self.approval_release_requested,
        }


@dataclass(frozen=True)
class UiOperatorIntakeDecision:
    """Deterministic decision for one UI operator-intake request."""

    action_name: UiOperatorIntakeActionName
    target_boundary: str
    result: UiOperatorIntakeDecisionResult
    accepted: bool
    execution_allowed: bool
    validation_required: bool
    reason: str
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        action_name = normalize_ui_operator_intake_action(self.action_name)
        target_boundary = normalize_ui_operator_intake_target_boundary(self.target_boundary)
        result = (
            self.result
            if isinstance(self.result, UiOperatorIntakeDecisionResult)
            else UiOperatorIntakeDecisionResult(self.result)
        )

        if not isinstance(self.accepted, bool):
            raise TypeError("accepted must be a boolean")

        if not isinstance(self.execution_allowed, bool):
            raise TypeError("execution_allowed must be a boolean")

        if not isinstance(self.validation_required, bool):
            raise TypeError("validation_required must be a boolean")

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "action_name", action_name)
        object.__setattr__(self, "target_boundary", target_boundary)
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "action_name": self.action_name.value,
            "target_boundary": self.target_boundary,
            "result": self.result.value,
            "accepted": self.accepted,
            "execution_allowed": self.execution_allowed,
            "validation_required": self.validation_required,
            "reason": self.reason,
            "required_boundary": self.required_boundary,
        }


SUPPORTED_UI_OPERATOR_INTAKE_ACTIONS: tuple[UiOperatorIntakeActionName, ...] = (
    UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION,
    UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION,
    UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE,
)


UI_OPERATOR_INTAKE_ACTION_CONTRACTS: Mapping[
    UiOperatorIntakeActionName,
    UiOperatorIntakeActionContract,
] = MappingProxyType(
    {
        UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION: UiOperatorIntakeActionContract(
            action_name=UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION,
            interaction_flow=UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
            mode=UiInteractionMode.COMMAND_CAPABLE,
            target_boundary_expectations=(
                "no_api_service_mutation_required_for_preview",
                "operator_intent_payload_may_be_previewed_only",
            ),
            intake_responsibilities=(
                "collect_operator_intent",
                "shape_preview_payload",
                "present_preview_without_execution",
            ),
            validation_rules=(
                "preview_does_not_mutate",
                "preview_must_not_become_business_rule",
            ),
            forbidden_behaviors=(
                "direct_state_mutation",
                "hidden_business_rule",
                "autonomous_action_execution",
            ),
        ),
        UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION: UiOperatorIntakeActionContract(
            action_name=UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION,
            interaction_flow=UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
            mode=UiInteractionMode.COMMAND_CAPABLE,
            target_boundary_expectations=(
                "api_service_validation_required",
                "ui_must_not_validate_business_rules_as_truth",
            ),
            intake_responsibilities=(
                "collect_operator_intent",
                "shape_validation_payload",
                "hand_off_to_api_or_service_boundary",
            ),
            validation_rules=(
                "validation_before_mutation",
                "api_service_boundary_remains_validation_authority",
            ),
            forbidden_behaviors=(
                "ui_validation_truth",
                "api_service_validation_bypass",
                "raw_state_mutation",
            ),
        ),
        UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE: UiOperatorIntakeActionContract(
            action_name=UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE,
            interaction_flow=UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
            mode=UiInteractionMode.COMMAND_CAPABLE,
            target_boundary_expectations=(
                "stable_api_service_command_boundary_required",
                "api_service_validation_required_before_mutation",
            ),
            intake_responsibilities=(
                "collect_operator_intent",
                "shape_api_service_intake_payload",
                "prepare_downstream_handoff_without_execution",
            ),
            validation_rules=(
                "validation_before_mutation",
                "execution_not_allowed_from_ui",
            ),
            forbidden_behaviors=(
                "ui_originated_hidden_business_rules",
                "autonomous_action_execution",
                "approval_release_expansion",
            ),
        ),
    }
)


def list_ui_operator_intake_action_contracts() -> tuple[UiOperatorIntakeActionContract, ...]:
    """Return UI operator-intake action contracts in deterministic order."""

    return tuple(
        UI_OPERATOR_INTAKE_ACTION_CONTRACTS[action_name]
        for action_name in SUPPORTED_UI_OPERATOR_INTAKE_ACTIONS
    )


def get_ui_operator_intake_action_contract(
    value: UiOperatorIntakeActionName | str,
) -> UiOperatorIntakeActionContract:
    """Return a UI operator-intake action contract or fail closed."""

    action_name = normalize_ui_operator_intake_action(value)
    return UI_OPERATOR_INTAKE_ACTION_CONTRACTS[action_name]


def build_ui_operator_intake_request(
    *,
    action_name: UiOperatorIntakeActionName | str,
    target_boundary: str = "api_command_intake",
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    execute: bool = False,
    approval_release_requested: bool = False,
) -> UiOperatorIntakeRequest:
    """Build a deterministic UI operator-intake request envelope."""

    return UiOperatorIntakeRequest(
        action_name=normalize_ui_operator_intake_action(action_name),
        target_boundary=normalize_ui_operator_intake_target_boundary(target_boundary),
        payload=_freeze_mapping(payload),
        metadata=_freeze_mapping(metadata),
        execute=execute,
        approval_release_requested=approval_release_requested,
    )


def evaluate_ui_operator_intake(
    request: UiOperatorIntakeRequest,
) -> UiOperatorIntakeDecision:
    """Evaluate UI operator intake without executing or mutating state."""

    if request.execute:
        return UiOperatorIntakeDecision(
            action_name=request.action_name,
            target_boundary=request.target_boundary,
            result=UiOperatorIntakeDecisionResult.REJECTED,
            accepted=False,
            execution_allowed=False,
            validation_required=True,
            reason="ui_operator_intake_never_executes_actions_directly",
            required_boundary="api/service command boundary",
        )

    if request.approval_release_requested:
        return UiOperatorIntakeDecision(
            action_name=request.action_name,
            target_boundary=request.target_boundary,
            result=UiOperatorIntakeDecisionResult.REJECTED,
            accepted=False,
            execution_allowed=False,
            validation_required=True,
            reason="approval_release_expansion_not_authorized_for_ui_intake",
            required_boundary="roadmap-authorized approval/release boundary",
        )

    if request.action_name is UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION:
        return UiOperatorIntakeDecision(
            action_name=request.action_name,
            target_boundary=request.target_boundary,
            result=UiOperatorIntakeDecisionResult.ACCEPTED_FOR_PREVIEW,
            accepted=True,
            execution_allowed=False,
            validation_required=False,
            reason="operator_intent_accepted_for_preview_without_mutation",
            required_boundary=None,
        )

    return UiOperatorIntakeDecision(
        action_name=request.action_name,
        target_boundary=request.target_boundary,
        result=UiOperatorIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION,
        accepted=True,
        execution_allowed=False,
        validation_required=True,
        reason="operator_intake_requires_api_service_validation_before_mutation",
        required_boundary="api/service validation before mutation",
    )
