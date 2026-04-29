"""Gantt and planning visualization export surfaces for the M13.3 checkpoint."""

from __future__ import annotations

from typing import Any

from .export_contracts import (
    GANTT_PLANNING_EXPORT_FAMILY,
    GANTT_TIMELINE_OUTPUT_KIND,
    build_export_request_payload,
)

GANTT_SURFACE_CHECKPOINT_ID = "M13.3"
GANTT_SURFACE_CONTRACT_VERSION = "gantt-planning-visualization-surface-v1"

UNGROUPED_GANTT_GROUPING_MODE = "ungrouped"
WORK_PACKAGE_GANTT_GROUPING_MODE = "by_work_package"
COLLECTION_GANTT_GROUPING_MODE = "by_collection"
OWNER_GANTT_GROUPING_MODE = "by_owner"
STATUS_GANTT_GROUPING_MODE = "by_status"

SUPPORTED_GANTT_GROUPING_MODES = (
    UNGROUPED_GANTT_GROUPING_MODE,
    WORK_PACKAGE_GANTT_GROUPING_MODE,
    COLLECTION_GANTT_GROUPING_MODE,
    OWNER_GANTT_GROUPING_MODE,
    STATUS_GANTT_GROUPING_MODE,
)

START_FINISH_VISIBILITY_FIELD = "start_finish"
STATUS_VISIBILITY_FIELD = "status"
DEPENDENCIES_VISIBILITY_FIELD = "dependencies"
GROUPING_VISIBILITY_FIELD = "grouping"
DURATION_VISIBILITY_FIELD = "duration"

SUPPORTED_GANTT_VISIBILITY_FIELDS = (
    START_FINISH_VISIBILITY_FIELD,
    STATUS_VISIBILITY_FIELD,
    DEPENDENCIES_VISIBILITY_FIELD,
    GROUPING_VISIBILITY_FIELD,
    DURATION_VISIBILITY_FIELD,
)

FINISH_TO_START_DEPENDENCY_TYPE = "finish_to_start"
START_TO_START_DEPENDENCY_TYPE = "start_to_start"
FINISH_TO_FINISH_DEPENDENCY_TYPE = "finish_to_finish"
START_TO_FINISH_DEPENDENCY_TYPE = "start_to_finish"

SUPPORTED_GANTT_DEPENDENCY_TYPES = (
    FINISH_TO_START_DEPENDENCY_TYPE,
    START_TO_START_DEPENDENCY_TYPE,
    FINISH_TO_FINISH_DEPENDENCY_TYPE,
    START_TO_FINISH_DEPENDENCY_TYPE,
)

DAY_TIMESCALE = "day"
WEEK_TIMESCALE = "week"
MONTH_TIMESCALE = "month"

SUPPORTED_GANTT_TIMESCALES = (
    DAY_TIMESCALE,
    WEEK_TIMESCALE,
    MONTH_TIMESCALE,
)

ISO_DATE_FORMAT = "iso_date"

GANTT_TIMELINE_SHAPE = "gantt_timeline_payload"
GANTT_RENDERING_BOUNDARY = (
    "gantt_surface_defines_visualization_payload_only_renderer_is_downstream"
)

_REQUIRED_GANTT_ITEM_FIELDS = (
    "item_id",
    "label",
    "start_date",
    "finish_date",
    "duration",
    "status",
)

_REQUIRED_DEPENDENCY_FIELDS = (
    "predecessor_id",
    "successor_id",
    "dependency_type",
)


def build_gantt_planning_visualization_surface_baseline() -> dict[str, Any]:
    """Return the explicit M13.3 Gantt/planning visualization surface baseline."""

    return {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "export_family": GANTT_PLANNING_EXPORT_FAMILY,
        "supported_output_kind": GANTT_TIMELINE_OUTPUT_KIND,
        "supported_grouping_modes": list(SUPPORTED_GANTT_GROUPING_MODES),
        "supported_visibility_fields": list(SUPPORTED_GANTT_VISIBILITY_FIELDS),
        "supported_dependency_types": list(SUPPORTED_GANTT_DEPENDENCY_TYPES),
        "supported_timescales": list(SUPPORTED_GANTT_TIMESCALES),
        "timeline_shape": GANTT_TIMELINE_SHAPE,
        "rendering_boundary": GANTT_RENDERING_BOUNDARY,
        "surface_boundary": (
            "gantt_surfaces_define_payload_grouping_dependency_and_visibility_contracts_not_chart_rendering"
        ),
    }


def build_gantt_planning_item(
    *,
    item_id: str,
    label: str,
    start_date: str,
    finish_date: str,
    duration: str,
    status: str,
    grouping_key: str | None = None,
    dependency_refs: list[str] | None = None,
) -> dict[str, Any]:
    """Build one deterministic Gantt planning item."""

    item = {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "item_id": item_id,
        "label": label,
        "start_date": start_date,
        "finish_date": finish_date,
        "duration": duration,
        "status": status,
        "grouping_key": grouping_key,
        "dependency_refs": list(dependency_refs or []),
    }
    validate_gantt_planning_item(item)
    return item


def build_gantt_dependency_ref(
    *,
    predecessor_id: str,
    successor_id: str,
    dependency_type: str = FINISH_TO_START_DEPENDENCY_TYPE,
) -> dict[str, Any]:
    """Build one deterministic Gantt dependency reference."""

    dependency = {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "predecessor_id": predecessor_id,
        "successor_id": successor_id,
        "dependency_type": dependency_type,
    }
    validate_gantt_dependency_ref(dependency)
    return dependency


def build_gantt_timeline_basis(
    *,
    calendar_ref: str,
    timescale: str = DAY_TIMESCALE,
    date_format: str = ISO_DATE_FORMAT,
) -> dict[str, Any]:
    """Build a deterministic Gantt timeline basis."""

    _validate_supported_timescale(timescale)
    if not calendar_ref.strip():
        raise ValueError("Gantt timeline basis must declare non-empty calendar_ref.")
    if date_format != ISO_DATE_FORMAT:
        raise ValueError(
            f"Gantt timeline basis supports only {ISO_DATE_FORMAT!r} date_format."
        )

    return {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "calendar_ref": calendar_ref,
        "timescale": timescale,
        "date_format": date_format,
        "timeline_truth_boundary": (
            "timeline_basis_is_input_context_not_rendered_chart_truth"
        ),
    }


def build_gantt_visibility_config(
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build explicit visibility settings for a Gantt export payload."""

    fields = list(visible_fields or SUPPORTED_GANTT_VISIBILITY_FIELDS)
    _validate_visibility_fields(fields)

    return {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "visible_fields": fields,
        "visibility_policy": (
            "only_declared_visibility_fields_may_be_rendered_downstream"
        ),
    }


def build_gantt_planning_export_payload(
    *,
    planning_items: list[dict[str, object]],
    dependency_refs: list[dict[str, object]],
    timeline_basis: dict[str, object],
    grouping_mode: str = UNGROUPED_GANTT_GROUPING_MODE,
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build a validated Gantt/planning visualization export payload.

    The payload intentionally matches the M13.1 Gantt input contract:
    - planning_items
    - dependency_refs
    - timeline_basis

    It adds M13.3 grouping, dependency visibility, planning/status visibility,
    and a contract-only Gantt timeline shape without rendering a chart.
    """

    _validate_supported_grouping_mode(grouping_mode)
    visibility_config = build_gantt_visibility_config(visible_fields)

    payload = {
        "checkpoint": GANTT_SURFACE_CHECKPOINT_ID,
        "contract_version": GANTT_SURFACE_CONTRACT_VERSION,
        "planning_items": planning_items,
        "dependency_refs": dependency_refs,
        "timeline_basis": timeline_basis,
        "grouping": {
            "mode": grouping_mode,
            "grouping_truth_boundary": (
                "grouping_controls_visual_organization_only_not_source_ownership"
            ),
        },
        "visibility": visibility_config,
        "output_shape": {
            "requested_output_kind": GANTT_TIMELINE_OUTPUT_KIND,
            "timeline_shape": GANTT_TIMELINE_SHAPE,
            "rendering_boundary": GANTT_RENDERING_BOUNDARY,
        },
    }
    validate_gantt_planning_export_payload(payload)
    return payload


def build_gantt_planning_export_request(
    *,
    export_job_id: str,
    export_id: str,
    export_version: str,
    source_context_kind: str,
    source_context_ref: str,
    planning_items: list[dict[str, object]],
    dependency_refs: list[dict[str, object]],
    timeline_basis: dict[str, object],
    grouping_mode: str = UNGROUPED_GANTT_GROUPING_MODE,
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build a governed M13.1 export request with an M13.3 Gantt payload."""

    input_payload = build_gantt_planning_export_payload(
        planning_items=planning_items,
        dependency_refs=dependency_refs,
        timeline_basis=timeline_basis,
        grouping_mode=grouping_mode,
        visible_fields=visible_fields,
    )

    return build_export_request_payload(
        export_job_id=export_job_id,
        export_family=GANTT_PLANNING_EXPORT_FAMILY,
        export_id=export_id,
        export_version=export_version,
        requested_output_kind=GANTT_TIMELINE_OUTPUT_KIND,
        source_context_kind=source_context_kind,
        source_context_ref=source_context_ref,
        input_payload=input_payload,
    )


def validate_gantt_planning_export_payload(payload: dict[str, object]) -> None:
    """Validate a Gantt/planning visualization export payload."""

    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=GANTT_SURFACE_CHECKPOINT_ID,
        error_prefix="Gantt planning export payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=GANTT_SURFACE_CONTRACT_VERSION,
        error_prefix="Gantt planning export payload",
    )

    planning_items = payload.get("planning_items")
    if not isinstance(planning_items, list) or not planning_items:
        raise ValueError(
            "Gantt planning export payload must declare non-empty planning_items."
        )

    dependency_refs = payload.get("dependency_refs")
    if not isinstance(dependency_refs, list):
        raise ValueError(
            "Gantt planning export payload must declare dependency_refs as a list."
        )

    timeline_basis = payload.get("timeline_basis")
    if not isinstance(timeline_basis, dict):
        raise ValueError(
            "Gantt planning export payload must declare timeline_basis as a mapping."
        )
    validate_gantt_timeline_basis(timeline_basis)

    grouping = payload.get("grouping")
    if not isinstance(grouping, dict):
        raise ValueError(
            "Gantt planning export payload must declare grouping as a mapping."
        )
    grouping_mode = grouping.get("mode")
    if not isinstance(grouping_mode, str):
        raise ValueError("Gantt grouping must declare mode.")
    _validate_supported_grouping_mode(grouping_mode)

    visibility = payload.get("visibility")
    if not isinstance(visibility, dict):
        raise ValueError(
            "Gantt planning export payload must declare visibility as a mapping."
        )
    validate_gantt_visibility_config(visibility)

    output_shape = payload.get("output_shape")
    if not isinstance(output_shape, dict):
        raise ValueError(
            "Gantt planning export payload must declare output_shape as a mapping."
        )
    if output_shape.get("rendering_boundary") != GANTT_RENDERING_BOUNDARY:
        raise ValueError("Gantt output_shape declares an invalid rendering boundary.")

    item_ids: set[str] = set()
    for item in planning_items:
        if not isinstance(item, dict):
            raise ValueError("Gantt planning_items must contain mappings.")
        validate_gantt_planning_item(item)
        item_id = str(item["item_id"])
        if item_id in item_ids:
            raise ValueError(f"Duplicate Gantt planning item_id {item_id!r}.")
        item_ids.add(item_id)

    seen_dependencies: set[tuple[str, str, str]] = set()
    for dependency in dependency_refs:
        if not isinstance(dependency, dict):
            raise ValueError("Gantt dependency_refs must contain mappings.")
        validate_gantt_dependency_ref(dependency)

        predecessor_id = str(dependency["predecessor_id"])
        successor_id = str(dependency["successor_id"])
        dependency_type = str(dependency["dependency_type"])

        if predecessor_id == successor_id:
            raise ValueError("Gantt dependency cannot reference the same item.")
        if predecessor_id not in item_ids:
            raise ValueError(
                f"Gantt dependency references unknown predecessor_id {predecessor_id!r}."
            )
        if successor_id not in item_ids:
            raise ValueError(
                f"Gantt dependency references unknown successor_id {successor_id!r}."
            )

        dependency_key = (predecessor_id, successor_id, dependency_type)
        if dependency_key in seen_dependencies:
            raise ValueError("Duplicate Gantt dependency reference declared.")
        seen_dependencies.add(dependency_key)

    for item in planning_items:
        item_id = str(item["item_id"])
        for dependency_ref in item.get("dependency_refs", []):
            if not isinstance(dependency_ref, str) or not dependency_ref.strip():
                raise ValueError("Gantt item dependency_refs must be non-empty strings.")
            if dependency_ref == item_id:
                raise ValueError("Gantt planning item cannot depend on itself.")
            if dependency_ref not in item_ids:
                raise ValueError(
                    f"Gantt planning item references unknown dependency {dependency_ref!r}."
                )


def validate_gantt_planning_item(item: dict[str, object]) -> None:
    """Validate one Gantt planning item."""

    _validate_required_string_fields(
        item,
        ("checkpoint", "contract_version", *_REQUIRED_GANTT_ITEM_FIELDS),
        error_prefix="Gantt planning item",
    )
    _validate_expected_exact_value(
        item,
        field_name="checkpoint",
        expected_value=GANTT_SURFACE_CHECKPOINT_ID,
        error_prefix="Gantt planning item",
    )
    _validate_expected_exact_value(
        item,
        field_name="contract_version",
        expected_value=GANTT_SURFACE_CONTRACT_VERSION,
        error_prefix="Gantt planning item",
    )

    dependency_refs = item.get("dependency_refs")
    if not isinstance(dependency_refs, list):
        raise ValueError("Gantt planning item must declare dependency_refs as a list.")


def validate_gantt_dependency_ref(dependency_ref: dict[str, object]) -> None:
    """Validate one Gantt dependency reference."""

    _validate_required_string_fields(
        dependency_ref,
        ("checkpoint", "contract_version", *_REQUIRED_DEPENDENCY_FIELDS),
        error_prefix="Gantt dependency reference",
    )
    _validate_expected_exact_value(
        dependency_ref,
        field_name="checkpoint",
        expected_value=GANTT_SURFACE_CHECKPOINT_ID,
        error_prefix="Gantt dependency reference",
    )
    _validate_expected_exact_value(
        dependency_ref,
        field_name="contract_version",
        expected_value=GANTT_SURFACE_CONTRACT_VERSION,
        error_prefix="Gantt dependency reference",
    )
    dependency_type = str(dependency_ref["dependency_type"])
    if dependency_type not in SUPPORTED_GANTT_DEPENDENCY_TYPES:
        raise ValueError(
            "Unsupported Gantt dependency_type. "
            f"Expected one of: {', '.join(SUPPORTED_GANTT_DEPENDENCY_TYPES)}."
        )


def validate_gantt_timeline_basis(timeline_basis: dict[str, object]) -> None:
    """Validate a Gantt timeline basis."""

    _validate_expected_exact_value(
        timeline_basis,
        field_name="checkpoint",
        expected_value=GANTT_SURFACE_CHECKPOINT_ID,
        error_prefix="Gantt timeline basis",
    )
    _validate_expected_exact_value(
        timeline_basis,
        field_name="contract_version",
        expected_value=GANTT_SURFACE_CONTRACT_VERSION,
        error_prefix="Gantt timeline basis",
    )
    _validate_required_string_fields(
        timeline_basis,
        ("calendar_ref", "timescale", "date_format"),
        error_prefix="Gantt timeline basis",
    )
    _validate_supported_timescale(str(timeline_basis["timescale"]))
    if timeline_basis.get("date_format") != ISO_DATE_FORMAT:
        raise ValueError(
            f"Gantt timeline basis supports only {ISO_DATE_FORMAT!r} date_format."
        )


def validate_gantt_visibility_config(visibility_config: dict[str, object]) -> None:
    """Validate Gantt visibility settings."""

    _validate_expected_exact_value(
        visibility_config,
        field_name="checkpoint",
        expected_value=GANTT_SURFACE_CHECKPOINT_ID,
        error_prefix="Gantt visibility config",
    )
    _validate_expected_exact_value(
        visibility_config,
        field_name="contract_version",
        expected_value=GANTT_SURFACE_CONTRACT_VERSION,
        error_prefix="Gantt visibility config",
    )
    visible_fields = visibility_config.get("visible_fields")
    if not isinstance(visible_fields, list):
        raise ValueError("Gantt visibility config must declare visible_fields.")
    _validate_visibility_fields(visible_fields)


def _validate_supported_grouping_mode(grouping_mode: str) -> None:
    if grouping_mode not in SUPPORTED_GANTT_GROUPING_MODES:
        raise ValueError(
            "Unsupported Gantt grouping mode. "
            f"Expected one of: {', '.join(SUPPORTED_GANTT_GROUPING_MODES)}."
        )


def _validate_visibility_fields(visible_fields: list[object]) -> None:
    if not visible_fields:
        raise ValueError("Gantt visibility config must declare visible fields.")

    for field_name in visible_fields:
        if field_name not in SUPPORTED_GANTT_VISIBILITY_FIELDS:
            raise ValueError(
                "Unsupported Gantt visibility field. "
                f"Expected one of: {', '.join(SUPPORTED_GANTT_VISIBILITY_FIELDS)}."
            )


def _validate_supported_timescale(timescale: str) -> None:
    if timescale not in SUPPORTED_GANTT_TIMESCALES:
        raise ValueError(
            "Unsupported Gantt timescale. "
            f"Expected one of: {', '.join(SUPPORTED_GANTT_TIMESCALES)}."
        )


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        value = payload.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )
