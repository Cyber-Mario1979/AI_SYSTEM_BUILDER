"""Deterministic UI document/export/reporting visibility surfaces for ASBP.

M20.4 defines display-only visibility contracts for existing output records. It
does not introduce document generation, report generation, export generation,
renderer behavior, framework behavior, command execution, or raw state access.
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


class UiDocumentOutputVisibilitySurfaceName(StrEnum):
    """Stable supported UI output visibility surface vocabulary."""

    OUTPUT_TARGET_STATUS = "output_target_status"
    DOCUMENT_OUTPUT_STATUS = "document_output_status"
    EXPORT_OUTPUT_STATUS = "export_output_status"
    REPORTING_OUTPUT_STATUS = "reporting_output_status"


class UiDocumentOutputKind(StrEnum):
    """Stable existing-output kind vocabulary for UI visibility."""

    OUTPUT_TARGET = "output_target"
    DOCUMENT = "document"
    EXPORT = "export"
    REPORT = "report"


class UiDocumentOutputStatus(StrEnum):
    """Stable existing-output availability/status vocabulary."""

    AVAILABLE = "available"
    NOT_AVAILABLE = "not_available"
    BLOCKED = "blocked"
    ERROR = "error"
    UNKNOWN = "unknown"


ALLOWED_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES: tuple[str, ...] = (
    "api_read_surface",
    "service_read_surface",
    "api_service_read_boundary",
    "approved_output_boundary",
    "output_target_metadata",
)

FORBIDDEN_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES: tuple[str, ...] = (
    "document_generation_engine",
    "report_generation_engine",
    "export_generation_engine",
    "renderer_engine",
    "raw_state_storage",
    "raw_persistence_helpers",
    "direct_state_mutation",
    "ui_generated_output",
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("metadata and display_payload values must be mappings")

    return MappingProxyType(dict(value))


def normalize_ui_document_output_visibility_surface(
    value: UiDocumentOutputVisibilitySurfaceName | str,
) -> UiDocumentOutputVisibilitySurfaceName:
    """Normalize a document/export/reporting visibility surface or fail closed."""

    if isinstance(value, UiDocumentOutputVisibilitySurfaceName):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI document output visibility surface must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiDocumentOutputVisibilitySurfaceName(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI document output visibility surface: {value}") from exc


def normalize_ui_document_output_kind(value: UiDocumentOutputKind | str) -> UiDocumentOutputKind:
    """Normalize an existing-output kind or fail closed."""

    if isinstance(value, UiDocumentOutputKind):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI document output kind must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiDocumentOutputKind(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI document output kind: {value}") from exc


def normalize_ui_document_output_status(value: UiDocumentOutputStatus | str) -> UiDocumentOutputStatus:
    """Normalize an existing-output status or fail closed."""

    if isinstance(value, UiDocumentOutputStatus):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI document output status must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    try:
        return UiDocumentOutputStatus(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported UI document output status: {value}") from exc


def normalize_ui_document_output_source_boundary(value: str) -> str:
    """Normalize an output visibility source boundary or fail closed."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UI document output source boundary must be a non-empty string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")

    if normalized in FORBIDDEN_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES:
        raise ValueError(f"forbidden UI document output source boundary: {value}")

    if normalized not in ALLOWED_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES:
        raise ValueError(f"unsupported UI document output source boundary: {value}")

    return normalized


@dataclass(frozen=True)
class UiDocumentOutputVisibilitySurfaceContract:
    """Static contract describing one document/export/reporting visibility surface."""

    name: UiDocumentOutputVisibilitySurfaceName
    output_kind: UiDocumentOutputKind
    interaction_flow: UiInteractionFlowName
    mode: UiInteractionMode
    source_boundary_expectations: tuple[str, ...]
    display_constraints: tuple[str, ...]
    visibility_safety_rules: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]


@dataclass(frozen=True)
class UiDocumentOutputVisibilityPayload:
    """Stable display envelope for existing document/export/reporting output visibility."""

    surface_name: UiDocumentOutputVisibilitySurfaceName
    source_boundary: str
    output_kind: UiDocumentOutputKind
    output_status: UiDocumentOutputStatus = UiDocumentOutputStatus.UNKNOWN
    display_payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    interaction_flow: UiInteractionFlowName = UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY
    mode: UiInteractionMode = UiInteractionMode.DISPLAY_ONLY
    generation_allowed: bool = False
    renderer_allowed: bool = False
    ui_owns_output: bool = False

    def __post_init__(self) -> None:
        surface_name = normalize_ui_document_output_visibility_surface(self.surface_name)
        source_boundary = normalize_ui_document_output_source_boundary(self.source_boundary)
        output_kind = normalize_ui_document_output_kind(self.output_kind)
        output_status = normalize_ui_document_output_status(self.output_status)
        interaction_flow = normalize_ui_interaction_flow(self.interaction_flow)
        mode = normalize_ui_interaction_mode(self.mode)

        if interaction_flow is not UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY:
            raise ValueError("document output visibility payloads must use the document_output_visibility interaction flow")

        if mode is not UiInteractionMode.DISPLAY_ONLY:
            raise ValueError("document output visibility payloads must remain display-only")

        if self.generation_allowed:
            raise ValueError("document output visibility payloads must not allow generation")

        if self.renderer_allowed:
            raise ValueError("document output visibility payloads must not allow renderer behavior")

        if self.ui_owns_output:
            raise ValueError("document output visibility payloads must not make UI the output owner")

        object.__setattr__(self, "surface_name", surface_name)
        object.__setattr__(self, "source_boundary", source_boundary)
        object.__setattr__(self, "output_kind", output_kind)
        object.__setattr__(self, "output_status", output_status)
        object.__setattr__(self, "interaction_flow", interaction_flow)
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "display_payload", _freeze_mapping(self.display_payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic dictionary representation."""

        return {
            "surface_name": self.surface_name.value,
            "interaction_flow": self.interaction_flow.value,
            "mode": self.mode.value,
            "source_boundary": self.source_boundary,
            "output_kind": self.output_kind.value,
            "output_status": self.output_status.value,
            "display_payload": dict(self.display_payload),
            "metadata": dict(self.metadata),
            "generation_allowed": self.generation_allowed,
            "renderer_allowed": self.renderer_allowed,
            "ui_owns_output": self.ui_owns_output,
        }


SUPPORTED_UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACES: tuple[
    UiDocumentOutputVisibilitySurfaceName,
    ...,
] = (
    UiDocumentOutputVisibilitySurfaceName.OUTPUT_TARGET_STATUS,
    UiDocumentOutputVisibilitySurfaceName.DOCUMENT_OUTPUT_STATUS,
    UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS,
    UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS,
)


UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACE_CONTRACTS: Mapping[
    UiDocumentOutputVisibilitySurfaceName,
    UiDocumentOutputVisibilitySurfaceContract,
] = MappingProxyType(
    {
        UiDocumentOutputVisibilitySurfaceName.OUTPUT_TARGET_STATUS: UiDocumentOutputVisibilitySurfaceContract(
            name=UiDocumentOutputVisibilitySurfaceName.OUTPUT_TARGET_STATUS,
            output_kind=UiDocumentOutputKind.OUTPUT_TARGET,
            interaction_flow=UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_existing_output_target_metadata",
                "do_not_calculate_output_target_in_ui",
            ),
            display_constraints=(
                "show_output_target_status_when_supplied",
                "show_generation_allowed_flag_as_visibility_only",
                "show_runtime_control_state_when_supplied",
            ),
            visibility_safety_rules=(
                "display_only_no_generation",
                "preserve_output_target_metadata_truth",
                "present_missing_target_as_not_available",
            ),
            forbidden_behaviors=(
                "output_target_generation_from_ui",
                "renderer_behavior",
                "ui_output_source_truth",
            ),
        ),
        UiDocumentOutputVisibilitySurfaceName.DOCUMENT_OUTPUT_STATUS: UiDocumentOutputVisibilitySurfaceContract(
            name=UiDocumentOutputVisibilitySurfaceName.DOCUMENT_OUTPUT_STATUS,
            output_kind=UiDocumentOutputKind.DOCUMENT,
            interaction_flow=UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_existing_document_output_payload",
                "do_not_generate_document_from_ui",
            ),
            display_constraints=(
                "show_document_identifier_status_and_reference_when_supplied",
                "show_missing_document_as_not_available",
            ),
            visibility_safety_rules=(
                "display_only_no_document_generation",
                "document_engine_remains_authoritative",
                "present_generation_boundary_message_when_requested",
            ),
            forbidden_behaviors=(
                "document_generation_expansion",
                "document_artifact_creation",
                "renderer_product_ready_output",
            ),
        ),
        UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS: UiDocumentOutputVisibilitySurfaceContract(
            name=UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS,
            output_kind=UiDocumentOutputKind.EXPORT,
            interaction_flow=UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_existing_export_output_payload",
                "do_not_generate_export_from_ui",
            ),
            display_constraints=(
                "show_export_identifier_status_format_and_reference_when_supplied",
                "show_missing_export_as_not_available",
            ),
            visibility_safety_rules=(
                "display_only_no_export_generation",
                "export_engine_remains_authoritative",
                "present_export_boundary_message_when_requested",
            ),
            forbidden_behaviors=(
                "export_generation_expansion",
                "file_export_creation",
                "renderer_product_ready_output",
            ),
        ),
        UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS: UiDocumentOutputVisibilitySurfaceContract(
            name=UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS,
            output_kind=UiDocumentOutputKind.REPORT,
            interaction_flow=UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
            mode=UiInteractionMode.DISPLAY_ONLY,
            source_boundary_expectations=(
                "consume_existing_reporting_output_payload",
                "do_not_generate_report_from_ui",
            ),
            display_constraints=(
                "show_report_identifier_status_and_reference_when_supplied",
                "show_missing_report_as_not_available",
            ),
            visibility_safety_rules=(
                "display_only_no_report_generation",
                "reporting_engine_remains_authoritative",
                "present_reporting_boundary_message_when_requested",
            ),
            forbidden_behaviors=(
                "report_generation_expansion",
                "report_artifact_creation",
                "renderer_product_ready_output",
            ),
        ),
    }
)


def list_ui_document_output_visibility_surface_contracts() -> tuple[
    UiDocumentOutputVisibilitySurfaceContract,
    ...,
]:
    """Return document/export/reporting visibility contracts in deterministic order."""

    return tuple(
        UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACE_CONTRACTS[name]
        for name in SUPPORTED_UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACES
    )


def get_ui_document_output_visibility_surface_contract(
    value: UiDocumentOutputVisibilitySurfaceName | str,
) -> UiDocumentOutputVisibilitySurfaceContract:
    """Return a document/export/reporting visibility contract or fail closed."""

    surface_name = normalize_ui_document_output_visibility_surface(value)
    return UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACE_CONTRACTS[surface_name]


def build_ui_document_output_visibility_payload(
    *,
    surface_name: UiDocumentOutputVisibilitySurfaceName | str,
    source_boundary: str,
    output_kind: UiDocumentOutputKind | str,
    output_status: UiDocumentOutputStatus | str = UiDocumentOutputStatus.UNKNOWN,
    display_payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> UiDocumentOutputVisibilityPayload:
    """Build a deterministic display-only existing-output visibility payload."""

    return UiDocumentOutputVisibilityPayload(
        surface_name=normalize_ui_document_output_visibility_surface(surface_name),
        source_boundary=normalize_ui_document_output_source_boundary(source_boundary),
        output_kind=normalize_ui_document_output_kind(output_kind),
        output_status=normalize_ui_document_output_status(output_status),
        display_payload=_freeze_mapping(display_payload),
        metadata=_freeze_mapping(metadata),
    )
