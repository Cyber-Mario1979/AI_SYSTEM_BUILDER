"""Deterministic UI workflow visibility surfaces for ASBP.

M20.3 defines display-only workflow visibility contracts. It does not introduce
screens, framework behavior, workflow execution, command mutation, or raw state
access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .interaction_flow import UiInteractionFlowName, UiInteractionMode


class UiWorkflowVisibilitySurfaceName(StrEnum):
    """Stable supported UI workflow visibility surface vocabulary."""

    WORKFLOW_OVERVIEW = "workflow_overview"
    WORK_PACKAGE_STATUS = "work_package_status"
    TASK_STATUS = "task_status"
    VALIDATION_STATUS = "validation_status"


ALLOWED_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES: tuple[str, ...] = (
    "api_read_surface",
    "service_read_surface",
    "api_service_read_boundary",
    "approved_api_service_boundary",
)

FORBIDDEN_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES: tuple[str, ...] = (
    "raw_state_storage",
    "raw_persistence_helpers",
    "direct_state_mutation",
    "ui_owned_state",
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata and display_payload values must be mappings")

    return MappingProxyType(dict(value))


def normalize_ui_workflow_visibility_surface(
    value: UiWorkflowVisibilitySurfaceName | str,
) -> UiWorkflowVisibilitySurfaceName:
    """Normalize a workflow visibility surface name or fail closed."""

    if isinstance(value, UiWorkflowVisibilitySurfaceName):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI workflow visibility surface must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiWorkflowVisibilitySurfaceName(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI workflow visibility surface: {value}") from exc


def normalize_ui_workflow_visibility_source_boundary(value: str) -> str:
    """Normalize a workflow visibility source boundary or fail closed."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI workflow visibility source boundary must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    if normalized in FORBIDDEN_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES:
        raise ValueError(f"forbidden UI workflow visibility source boundary: {value}")

    if normalized not in ALLOWED_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES:
        raise ValueError(f"unsupported UI workflow visibility source boundary: {value}")

    return normalized


@dataclass(frozen=True)
class UiWorkflowVisibilitySurfaceContract:
    """Static contract describing one governed workflow visibility surface."""

    name: UiWorkflowVisibilitySurfaceName
    interaction_flow: UiInteractionFlowName
    mode: UiInteractionMode
    source_boundary_expectations: tuple[str, ...]
    display_responsibilities: tuple[str, ...]
    visibility_safety_rules: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]


@dataclass(frozen=True)
class UiWorkflowVisibilityPayload:
    """Stable display envelope for governed workflow state visibility."""

    surface_name: UiWorkflowVisibilitySurfaceName
    source_boundary: str
    display_payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    interaction_flow: UiInteractionFlowName = UiInteractionFlowName.WORKFLOW_VISIBILITY
    mode: UiInteractionMode = UiInteractionMode.DISPLAY_ONLY
    mutation_allowed: bool = False
    ui_owns_state: bool = False

    def __post_init__(self) -> None:
        surface_name = normalize_ui_workflow_visibility_surface(self.surface_name)
        source_boundary = normalize_ui_workflow_visibility_source_boundary(self.source_boundary)

        if self.interaction_flow is not UiInteractionFlowName.WORKFLOW_VISIBILITY:
            raise ValueError("workflow visibility payloads must use the workflow_visibility interaction flow")

        if self.mode is not UiInteractionMode.DISPLAY_ONLY:
            raise ValueError("workflow visibility payloads must remain display-only")

        if self.mutation_allowed:
            raise ValueError("workflow visibility payloads must not allow mutation")

        if self.ui_owns_state:
            raise ValueError("workflow visibility payloads must not make UI the state owner")

        object.__setattr__(self, "surface_name", surface_name)
        object.__setattr__(self, "source_boundary", source_boundary)
        object.__setattr__(self, "display_payload", _freeze_mapping(self.display_payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "surface_name": self.surface_name.value,
            "interaction_flow": self.interaction_flow.value,
            "mode": self.mode.value,
            "source_boundary": self.source_boundary,
            "display_payload": dict(self.display_payload),
            "metadata": dict(self.metadata),
            "mutation_allowed": self.mutation_allowed,
            "ui_owns_state": self.ui_owns_state,
        }


SUPPORTED_UI_WORKFLOW_VISIBILITY_SURFACES: tuple[UiWorkflowVisibilitySurfaceName, ...] = (
    UiWorkflowVisibilitySurfaceName.WORKFLOW_OVERVIEW,
    UiWorkflowVisibilitySurfaceName.WORK_PACKAGE_STATUS,
    UiWorkflowVisibilitySurfaceName.TASK_STATUS,
    UiWorkflowVisibilitySurfaceName.VALIDATION_STATUS,
)


UI_WORKFLOW_VISIBILITY_SURFACE_CONTRACTS: Mapping[
    UiWorkflowVisibilitySurfaceName,
    UiWorkflowVisibilitySurfaceContract,
] = MappingProxyType(
    {
        UiWorkflowVisibilitySurfaceName.WORKFLOW_OVERVIEW: UiWorkflowVisibilitySurfaceContract(
            name=UiWorkflowVisibilitySurfaceName.WORKFLOW_OVERVIEW,
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_api_or_service_read_payload",
                "do_not_fetch_raw_state",
            ),
            display_responsibilities=(
                "show_governed_workflow_summary",
                "show_status_and_blocker_context",
            ),
            visibility_safety_rules=(
                "display_only_no_mutation",
                "preserve_api_service_payload_truth",
                "present_invalid_state_without_auto_correction",
            ),
            forbidden_behaviors=(
                "hidden_mutation",
                "ui_workflow_state_ownership",
                "raw_state_storage_access",
            ),
        ),
        UiWorkflowVisibilitySurfaceName.WORK_PACKAGE_STATUS: UiWorkflowVisibilitySurfaceContract(
            name=UiWorkflowVisibilitySurfaceName.WORK_PACKAGE_STATUS,
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_api_or_service_read_payload",
                "do_not_resolve_work_package_state_from_ui",
            ),
            display_responsibilities=(
                "show_work_package_identity_and_status",
                "show_bound_context_or_visibility_context_when_supplied",
            ),
            visibility_safety_rules=(
                "display_only_no_mutation",
                "preserve_work_package_payload_shape",
                "present_missing_context_as_visibility_gap",
            ),
            forbidden_behaviors=(
                "work_package_state_mutation",
                "ui_work_package_source_truth",
                "raw_persistence_helpers",
            ),
        ),
        UiWorkflowVisibilitySurfaceName.TASK_STATUS: UiWorkflowVisibilitySurfaceContract(
            name=UiWorkflowVisibilitySurfaceName.TASK_STATUS,
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_api_or_service_read_payload",
                "do_not_resolve_task_state_from_ui",
            ),
            display_responsibilities=(
                "show_task_identity_status_and_owner_when_supplied",
                "show_dependency_or_blocker_context_when_supplied",
            ),
            visibility_safety_rules=(
                "display_only_no_mutation",
                "preserve_task_payload_shape",
                "present_stale_task_context_as_blocked_or_unknown",
            ),
            forbidden_behaviors=(
                "task_state_mutation",
                "ui_task_source_truth",
                "direct_state_mutation",
            ),
        ),
        UiWorkflowVisibilitySurfaceName.VALIDATION_STATUS: UiWorkflowVisibilitySurfaceContract(
            name=UiWorkflowVisibilitySurfaceName.VALIDATION_STATUS,
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_api_or_service_read_payload",
                "do_not_create_validation_result_from_ui",
            ),
            display_responsibilities=(
                "show_validation_status_when_supplied",
                "show_validation_evidence_reference_when_supplied",
            ),
            visibility_safety_rules=(
                "display_only_no_mutation",
                "validation_truth_remains_outside_ui",
                "present_missing_validation_evidence_as_not_available",
            ),
            forbidden_behaviors=(
                "validation_truth_ownership",
                "hidden_validation_pass_or_fail",
                "api_service_validation_bypass",
            ),
        ),
    }
)


def list_ui_workflow_visibility_surface_contracts() -> tuple[UiWorkflowVisibilitySurfaceContract, ...]:
    """Return workflow visibility surface contracts in deterministic order."""

    return tuple(
        UI_WORKFLOW_VISIBILITY_SURFACE_CONTRACTS[name]
        for name in SUPPORTED_UI_WORKFLOW_VISIBILITY_SURFACES
    )


def get_ui_workflow_visibility_surface_contract(
    value: UiWorkflowVisibilitySurfaceName | str,
) -> UiWorkflowVisibilitySurfaceContract:
    """Return a workflow visibility surface contract or fail closed."""

    surface_name = normalize_ui_workflow_visibility_surface(value)
    return UI_WORKFLOW_VISIBILITY_SURFACE_CONTRACTS[surface_name]


def build_ui_workflow_visibility_payload(
    *,
    surface_name: UiWorkflowVisibilitySurfaceName | str,
    source_boundary: str,
    display_payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> UiWorkflowVisibilityPayload:
    """Build a deterministic display-only workflow visibility payload."""

    normalized_surface = normalize_ui_workflow_visibility_surface(surface_name)
    normalized_source_boundary = normalize_ui_workflow_visibility_source_boundary(source_boundary)

    return UiWorkflowVisibilityPayload(
        surface_name=normalized_surface,
        source_boundary=normalized_source_boundary,
        display_payload=_freeze_mapping(display_payload),
        metadata=_freeze_mapping(metadata),
    )
