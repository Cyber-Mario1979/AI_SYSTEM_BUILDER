"""Deterministic UI interaction-flow contracts for ASBP.

M20.2 defines stable UI interaction contract shapes only. It does not introduce
screens, framework behavior, route behavior, command execution, or persistence
access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping


class UiInteractionFlowName(StrEnum):
    """Stable supported UI interaction-flow vocabulary."""

    WORKFLOW_VISIBILITY = "workflow_visibility"
    DOCUMENT_OUTPUT_VISIBILITY = "document_output_visibility"
    OPERATOR_COMMAND_INTAKE = "operator_command_intake"
    ERROR_STATUS_PRESENTATION = "error_status_presentation"


class UiInteractionMode(StrEnum):
    """Stable UI interaction behavior mode vocabulary."""

    DISPLAY_ONLY = "display_only"
    COMMAND_CAPABLE = "command_capable"


class UiActionIntakeDecisionResult(StrEnum):
    """Stable UI action/intake decision vocabulary."""

    ACCEPTED_FOR_DISPLAY = "accepted_for_display"
    REQUIRES_API_SERVICE_VALIDATION = "requires_api_service_validation"
    REJECTED = "rejected"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata and payload values must be mappings")

    return MappingProxyType(dict(value))


def normalize_ui_interaction_flow(
    value: UiInteractionFlowName | str,
) -> UiInteractionFlowName:
    """Normalize a UI interaction-flow name or fail closed."""

    if isinstance(value, UiInteractionFlowName):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI interaction flow must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiInteractionFlowName(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI interaction flow: {value}") from exc


def normalize_ui_interaction_mode(value: UiInteractionMode | str) -> UiInteractionMode:
    """Normalize a UI interaction mode or fail closed."""

    if isinstance(value, UiInteractionMode):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI interaction mode must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiInteractionMode(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI interaction mode: {value}") from exc


@dataclass(frozen=True)
class UiInteractionFlowContract:
    """Static contract describing one UI interaction-flow family."""

    name: UiInteractionFlowName
    family: str
    mode: UiInteractionMode
    user_action_expectations: tuple[str, ...]
    invalid_state_presentation: tuple[str, ...]
    execution_boundary: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]


@dataclass(frozen=True)
class UiActionIntakeRequest:
    """Stable UI action/intake envelope for future UI adapter behavior."""

    flow_name: UiInteractionFlowName
    requested_mode: UiInteractionMode
    action_name: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not isinstance(self.action_name, str) or not self.action_name.strip():
            raise ValueError("action_name must be a non-empty string")

        object.__setattr__(
            self,
            "flow_name",
            normalize_ui_interaction_flow(self.flow_name),
        )
        object.__setattr__(
            self,
            "requested_mode",
            normalize_ui_interaction_mode(self.requested_mode),
        )
        object.__setattr__(self, "action_name", self.action_name.strip())
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "flow_name": self.flow_name.value,
            "requested_mode": self.requested_mode.value,
            "action_name": self.action_name,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class UiActionIntakeDecision:
    """Deterministic UI action/intake boundary decision."""

    result: UiActionIntakeDecisionResult
    reason: str
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        result = (
            self.result
            if isinstance(self.result, UiActionIntakeDecisionResult)
            else UiActionIntakeDecisionResult(self.result)
        )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        object.__setattr__(self, "result", result)
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "result": self.result.value,
            "reason": self.reason,
            "required_boundary": self.required_boundary,
        }


SUPPORTED_UI_INTERACTION_FLOWS: tuple[UiInteractionFlowName, ...] = (
    UiInteractionFlowName.WORKFLOW_VISIBILITY,
    UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
    UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
    UiInteractionFlowName.ERROR_STATUS_PRESENTATION,
)


UI_INTERACTION_FLOW_CONTRACTS: Mapping[
    UiInteractionFlowName,
    UiInteractionFlowContract,
] = MappingProxyType(
    {
        UiInteractionFlowName.WORKFLOW_VISIBILITY: UiInteractionFlowContract(
            name=UiInteractionFlowName.WORKFLOW_VISIBILITY,
            family="governed_workflow_visibility",
            mode=UiInteractionMode.DISPLAY_ONLY,
            user_action_expectations=(
                "view_governed_workflow_state",
                "select_visible_workflow_record",
                "request_status_or_error_context",
            ),
            invalid_state_presentation=(
                "present_invalid_state_without_mutation",
                "show_source_boundary_or_validation_message",
            ),
            execution_boundary=(
                "display_only_no_mutation",
                "ui_must_not_become_execution_truth",
            ),
            forbidden_behaviors=(
                "direct_state_mutation",
                "hidden_workflow_rules",
                "api_service_validation_bypass",
            ),
        ),
        UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY: UiInteractionFlowContract(
            name=UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
            family="document_export_reporting_visibility",
            mode=UiInteractionMode.DISPLAY_ONLY,
            user_action_expectations=(
                "view_existing_document_export_reporting_output",
                "select_visible_output_record",
                "request_output_status_or_error_context",
            ),
            invalid_state_presentation=(
                "present_missing_output_without_generation",
                "present_generation_boundary_message",
            ),
            execution_boundary=(
                "display_only_no_generation",
                "ui_must_not_become_document_generation_truth",
            ),
            forbidden_behaviors=(
                "document_generation_from_ui_contract",
                "report_generation_from_ui_contract",
                "api_service_validation_bypass",
            ),
        ),
        UiInteractionFlowName.OPERATOR_COMMAND_INTAKE: UiInteractionFlowContract(
            name=UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
            family="operator_action_intake",
            mode=UiInteractionMode.COMMAND_CAPABLE,
            user_action_expectations=(
                "collect_operator_intent",
                "preview_command_payload",
                "submit_to_api_or_service_boundary_after_validation",
            ),
            invalid_state_presentation=(
                "present_validation_rejection_without_mutation",
                "present_stale_or_invalid_state_as_blocked",
            ),
            execution_boundary=(
                "api_service_validation_required",
                "ui_never_executes_domain_action_directly",
            ),
            forbidden_behaviors=(
                "direct_state_mutation",
                "ui_only_business_rules",
                "api_service_validation_bypass",
            ),
        ),
        UiInteractionFlowName.ERROR_STATUS_PRESENTATION: UiInteractionFlowContract(
            name=UiInteractionFlowName.ERROR_STATUS_PRESENTATION,
            family="operator_facing_error_status_presentation",
            mode=UiInteractionMode.DISPLAY_ONLY,
            user_action_expectations=(
                "view_status_result_or_error",
                "request_human_readable_rejection_context",
                "return_to_safe_flow_after_invalid_state",
            ),
            invalid_state_presentation=(
                "present_error_without_auto_correction",
                "present_no_guess_next_action_message",
            ),
            execution_boundary=(
                "display_only_no_auto_recovery",
                "ui_must_not_silently_mutate_invalid_state",
            ),
            forbidden_behaviors=(
                "silent_error_correction",
                "hidden_retry_or_mutation",
                "api_service_validation_bypass",
            ),
        ),
    }
)


def list_ui_interaction_flow_contracts() -> tuple[UiInteractionFlowContract, ...]:
    """Return supported UI interaction-flow contracts in deterministic order."""

    return tuple(UI_INTERACTION_FLOW_CONTRACTS[name] for name in SUPPORTED_UI_INTERACTION_FLOWS)


def get_ui_interaction_flow_contract(
    value: UiInteractionFlowName | str,
) -> UiInteractionFlowContract:
    """Return the UI interaction-flow contract or fail closed."""

    flow_name = normalize_ui_interaction_flow(value)
    return UI_INTERACTION_FLOW_CONTRACTS[flow_name]


def build_ui_action_intake_request(
    *,
    flow_name: UiInteractionFlowName | str,
    requested_mode: UiInteractionMode | str,
    action_name: str,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> UiActionIntakeRequest:
    """Build a deterministic UI action/intake request envelope."""

    return UiActionIntakeRequest(
        flow_name=normalize_ui_interaction_flow(flow_name),
        requested_mode=normalize_ui_interaction_mode(requested_mode),
        action_name=action_name,
        payload=_freeze_mapping(payload),
        metadata=_freeze_mapping(metadata),
    )


def evaluate_ui_action_intake(
    request: UiActionIntakeRequest,
) -> UiActionIntakeDecision:
    """Evaluate UI action/intake against the static interaction-flow boundary."""

    contract = get_ui_interaction_flow_contract(request.flow_name)

    if request.requested_mode is UiInteractionMode.DISPLAY_ONLY:
        return UiActionIntakeDecision(
            result=UiActionIntakeDecisionResult.ACCEPTED_FOR_DISPLAY,
            reason="display_only_request_allowed_without_mutation",
            required_boundary=None,
        )

    if contract.mode is UiInteractionMode.DISPLAY_ONLY:
        return UiActionIntakeDecision(
            result=UiActionIntakeDecisionResult.REJECTED,
            reason="display_only_flow_cannot_accept_command_intake",
            required_boundary=None,
        )

    return UiActionIntakeDecision(
        result=UiActionIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION,
        reason="command_capable_flow_requires_api_service_validation",
        required_boundary="api/service validation before mutation",
    )
