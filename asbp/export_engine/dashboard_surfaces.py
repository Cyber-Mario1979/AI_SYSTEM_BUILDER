"""Dashboard and status summary export surfaces for the M13.4 checkpoint."""

from __future__ import annotations

from typing import Any

from .export_contracts import (
    DASHBOARD_SNAPSHOT_OUTPUT_KIND,
    DASHBOARD_STATUS_EXPORT_FAMILY,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    build_export_request_payload,
)

DASHBOARD_SURFACE_CHECKPOINT_ID = "M13.4"
DASHBOARD_SURFACE_CONTRACT_VERSION = "dashboard-status-summary-surface-v1"

DASHBOARD_SNAPSHOT_SURFACE_TYPE = "dashboard_snapshot"
STATUS_SUMMARY_SURFACE_TYPE = "status_summary"
KPI_SUMMARY_SURFACE_TYPE = "kpi_summary"
PROGRESS_SUMMARY_SURFACE_TYPE = "progress_summary"

SUPPORTED_DASHBOARD_SURFACE_TYPES = (
    DASHBOARD_SNAPSHOT_SURFACE_TYPE,
    STATUS_SUMMARY_SURFACE_TYPE,
    KPI_SUMMARY_SURFACE_TYPE,
    PROGRESS_SUMMARY_SURFACE_TYPE,
)

SUPPORTED_DASHBOARD_OUTPUT_KINDS = (
    DASHBOARD_SNAPSHOT_OUTPUT_KIND,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
)

STATUS_DASHBOARD_VISIBILITY_FIELD = "status"
PROGRESS_DASHBOARD_VISIBILITY_FIELD = "progress"
KPI_DASHBOARD_VISIBILITY_FIELD = "kpi"
RISK_BLOCKER_DASHBOARD_VISIBILITY_FIELD = "risk_blocker"
SOURCE_REFERENCE_DASHBOARD_VISIBILITY_FIELD = "source_reference"
SUMMARY_CATEGORY_DASHBOARD_VISIBILITY_FIELD = "summary_category"

SUPPORTED_DASHBOARD_VISIBILITY_FIELDS = (
    STATUS_DASHBOARD_VISIBILITY_FIELD,
    PROGRESS_DASHBOARD_VISIBILITY_FIELD,
    KPI_DASHBOARD_VISIBILITY_FIELD,
    RISK_BLOCKER_DASHBOARD_VISIBILITY_FIELD,
    SOURCE_REFERENCE_DASHBOARD_VISIBILITY_FIELD,
    SUMMARY_CATEGORY_DASHBOARD_VISIBILITY_FIELD,
)

DASHBOARD_SNAPSHOT_SHAPE = "dashboard_snapshot_payload"
STRUCTURED_DASHBOARD_REPORT_PAYLOAD_SHAPE = "structured_dashboard_report_payload"

_DASHBOARD_OUTPUT_SHAPES = {
    DASHBOARD_SNAPSHOT_OUTPUT_KIND: DASHBOARD_SNAPSHOT_SHAPE,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND: STRUCTURED_DASHBOARD_REPORT_PAYLOAD_SHAPE,
}

DASHBOARD_RENDERING_BOUNDARY = (
    "dashboard_surface_defines_summary_payload_only_renderer_is_downstream"
)

KPI_OBJECT_BOUNDARY = (
    "kpi_is_declared_metric_object_only_no_cqv_catalog_formula_threshold_or_interpretation"
)

_PROHIBITED_KPI_FIELDS = (
    "calculation_method",
    "calculation_formula",
    "threshold",
    "acceptance_limit",
    "cqv_interpretation_rule",
)

_REQUIRED_STATUS_ITEM_FIELDS = (
    "item_id",
    "label",
    "status",
    "progress_value",
    "summary_category",
    "source_ref",
)

_REQUIRED_KPI_FIELDS = (
    "kpi_id",
    "label",
    "value",
    "unit",
    "source_ref",
)


def build_dashboard_status_summary_surface_baseline() -> dict[str, Any]:
    """Return the explicit M13.4 dashboard/status summary surface baseline."""

    return {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "export_family": DASHBOARD_STATUS_EXPORT_FAMILY,
        "supported_output_kinds": list(SUPPORTED_DASHBOARD_OUTPUT_KINDS),
        "supported_surface_types": list(SUPPORTED_DASHBOARD_SURFACE_TYPES),
        "supported_visibility_fields": list(SUPPORTED_DASHBOARD_VISIBILITY_FIELDS),
        "output_shapes": dict(_DASHBOARD_OUTPUT_SHAPES),
        "kpi_boundary": KPI_OBJECT_BOUNDARY,
        "prohibited_kpi_fields": list(_PROHIBITED_KPI_FIELDS),
        "surface_boundary": (
            "dashboard_surfaces_define_snapshot_status_kpi_and_progress_summary_contracts_not_ui_rendering"
        ),
        "snapshot_report_dashboard_distinctions": {
            "dashboard_snapshot": (
                "point_in_time_status_surface_for_downstream_dashboard_rendering"
            ),
            "status_summary": "compact_operational_status_summary_payload",
            "kpi_summary": "metric_focused_summary_payload_without_cqv_calculation_logic",
            "structured_report_payload": (
                "downstream_reporting_input_payload_not_full_report_rendering"
            ),
        },
    }


def build_dashboard_kpi_metric(
    *,
    kpi_id: str,
    label: str,
    value: int | float | str,
    unit: str,
    source_ref: str,
) -> dict[str, Any]:
    """Build one declared dashboard KPI object.

    M13.4 treats KPI as a metric object only. It does not define CQV KPI
    catalog membership, calculation formulas, thresholds, or interpretation rules.
    """

    metric = {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "kpi_id": kpi_id,
        "label": label,
        "value": value,
        "unit": unit,
        "source_ref": source_ref,
        "interpretation_boundary": KPI_OBJECT_BOUNDARY,
    }
    validate_dashboard_kpi_metric(metric)
    return metric


def build_dashboard_status_item(
    *,
    item_id: str,
    label: str,
    status: str,
    progress_value: int | float,
    summary_category: str,
    source_ref: str,
    kpi_refs: list[str] | None = None,
    risk_blocker_refs: list[str] | None = None,
) -> dict[str, Any]:
    """Build one deterministic dashboard status item."""

    item = {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "item_id": item_id,
        "label": label,
        "status": status,
        "progress_value": progress_value,
        "summary_category": summary_category,
        "source_ref": source_ref,
        "kpi_refs": list(kpi_refs or []),
        "risk_blocker_refs": list(risk_blocker_refs or []),
    }
    validate_dashboard_status_item(item)
    return item


def build_dashboard_snapshot_basis(
    *,
    snapshot_id: str,
    as_of: str,
    source_context_ref: str,
) -> dict[str, Any]:
    """Build a point-in-time dashboard snapshot basis."""

    basis = {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "snapshot_id": snapshot_id,
        "as_of": as_of,
        "source_context_ref": source_context_ref,
        "snapshot_truth_boundary": (
            "snapshot_basis_identifies_point_in_time_view_not_execution_truth"
        ),
    }
    validate_dashboard_snapshot_basis(basis)
    return basis


def build_dashboard_visibility_config(
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build explicit dashboard visibility settings."""

    fields = list(visible_fields or SUPPORTED_DASHBOARD_VISIBILITY_FIELDS)
    _validate_visibility_fields(fields)

    return {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "visible_fields": fields,
        "visibility_policy": (
            "only_declared_dashboard_visibility_fields_may_be_rendered_downstream"
        ),
    }


def build_dashboard_status_export_payload(
    *,
    requested_output_kind: str,
    surface_type: str,
    status_items: list[dict[str, object]],
    summary_metrics: list[dict[str, object]],
    snapshot_basis: dict[str, object],
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build a validated dashboard/status summary export payload.

    This payload intentionally matches the M13.1 dashboard input contract:
    - status_items
    - summary_metrics
    - snapshot_basis

    It adds M13.4 surface type, visibility boundaries, snapshot/report/dashboard
    distinctions, and contract-only output shapes without rendering a dashboard,
    report, chart, or UI surface.
    """

    _validate_supported_output_kind(requested_output_kind)
    _validate_supported_surface_type(surface_type)
    visibility_config = build_dashboard_visibility_config(visible_fields)

    payload = {
        "checkpoint": DASHBOARD_SURFACE_CHECKPOINT_ID,
        "contract_version": DASHBOARD_SURFACE_CONTRACT_VERSION,
        "surface_type": surface_type,
        "status_items": status_items,
        "summary_metrics": summary_metrics,
        "snapshot_basis": snapshot_basis,
        "visibility": visibility_config,
        "output_shape": {
            "requested_output_kind": requested_output_kind,
            "dashboard_shape": _DASHBOARD_OUTPUT_SHAPES[requested_output_kind],
            "rendering_boundary": DASHBOARD_RENDERING_BOUNDARY,
        },
        "snapshot_report_dashboard_distinctions": {
            "dashboard_snapshot": (
                "point_in_time_status_surface_for_downstream_dashboard_rendering"
            ),
            "status_summary": "compact_operational_status_summary_payload",
            "kpi_summary": "metric_focused_summary_payload_without_cqv_calculation_logic",
            "structured_report_payload": (
                "downstream_reporting_input_payload_not_full_report_rendering"
            ),
        },
    }
    validate_dashboard_status_export_payload(payload)
    return payload


def build_dashboard_status_export_request(
    *,
    export_job_id: str,
    export_id: str,
    export_version: str,
    requested_output_kind: str,
    source_context_kind: str,
    source_context_ref: str,
    surface_type: str,
    status_items: list[dict[str, object]],
    summary_metrics: list[dict[str, object]],
    snapshot_basis: dict[str, object],
    visible_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Build a governed M13.1 export request with an M13.4 dashboard payload."""

    input_payload = build_dashboard_status_export_payload(
        requested_output_kind=requested_output_kind,
        surface_type=surface_type,
        status_items=status_items,
        summary_metrics=summary_metrics,
        snapshot_basis=snapshot_basis,
        visible_fields=visible_fields,
    )

    return build_export_request_payload(
        export_job_id=export_job_id,
        export_family=DASHBOARD_STATUS_EXPORT_FAMILY,
        export_id=export_id,
        export_version=export_version,
        requested_output_kind=requested_output_kind,
        source_context_kind=source_context_kind,
        source_context_ref=source_context_ref,
        input_payload=input_payload,
    )


def validate_dashboard_status_export_payload(payload: dict[str, object]) -> None:
    """Validate a dashboard/status summary export payload."""

    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=DASHBOARD_SURFACE_CHECKPOINT_ID,
        error_prefix="Dashboard status export payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=DASHBOARD_SURFACE_CONTRACT_VERSION,
        error_prefix="Dashboard status export payload",
    )

    surface_type = payload.get("surface_type")
    if not isinstance(surface_type, str):
        raise ValueError("Dashboard status export payload must declare surface_type.")
    _validate_supported_surface_type(surface_type)

    status_items = payload.get("status_items")
    if not isinstance(status_items, list) or not status_items:
        raise ValueError(
            "Dashboard status export payload must declare non-empty status_items."
        )

    summary_metrics = payload.get("summary_metrics")
    if not isinstance(summary_metrics, list):
        raise ValueError(
            "Dashboard status export payload must declare summary_metrics as a list."
        )

    snapshot_basis = payload.get("snapshot_basis")
    if not isinstance(snapshot_basis, dict):
        raise ValueError(
            "Dashboard status export payload must declare snapshot_basis as a mapping."
        )
    validate_dashboard_snapshot_basis(snapshot_basis)

    visibility = payload.get("visibility")
    if not isinstance(visibility, dict):
        raise ValueError(
            "Dashboard status export payload must declare visibility as a mapping."
        )
    validate_dashboard_visibility_config(visibility)

    output_shape = payload.get("output_shape")
    if not isinstance(output_shape, dict):
        raise ValueError(
            "Dashboard status export payload must declare output_shape as a mapping."
        )
    requested_output_kind = output_shape.get("requested_output_kind")
    if not isinstance(requested_output_kind, str):
        raise ValueError("Dashboard output_shape must declare requested_output_kind.")
    _validate_supported_output_kind(requested_output_kind)
    if output_shape.get("dashboard_shape") != _DASHBOARD_OUTPUT_SHAPES[requested_output_kind]:
        raise ValueError("Dashboard output_shape declares an invalid dashboard_shape.")
    if output_shape.get("rendering_boundary") != DASHBOARD_RENDERING_BOUNDARY:
        raise ValueError("Dashboard output_shape declares an invalid rendering boundary.")

    metric_ids: set[str] = set()
    for metric in summary_metrics:
        if not isinstance(metric, dict):
            raise ValueError("Dashboard summary_metrics must contain mappings.")
        validate_dashboard_kpi_metric(metric)
        kpi_id = str(metric["kpi_id"])
        if kpi_id in metric_ids:
            raise ValueError(f"Duplicate dashboard kpi_id {kpi_id!r}.")
        metric_ids.add(kpi_id)

    item_ids: set[str] = set()
    for item in status_items:
        if not isinstance(item, dict):
            raise ValueError("Dashboard status_items must contain mappings.")
        validate_dashboard_status_item(item)
        item_id = str(item["item_id"])
        if item_id in item_ids:
            raise ValueError(f"Duplicate dashboard item_id {item_id!r}.")
        item_ids.add(item_id)

        for kpi_ref in item.get("kpi_refs", []):
            if not isinstance(kpi_ref, str) or not kpi_ref.strip():
                raise ValueError("Dashboard item kpi_refs must be non-empty strings.")
            if kpi_ref not in metric_ids:
                raise ValueError(
                    f"Dashboard item references unknown KPI {kpi_ref!r}."
                )


def validate_dashboard_status_item(item: dict[str, object]) -> None:
    """Validate one dashboard status item."""

    _validate_required_string_fields(
        item,
        (
            "checkpoint",
            "contract_version",
            "item_id",
            "label",
            "status",
            "summary_category",
            "source_ref",
        ),
        error_prefix="Dashboard status item",
    )
    _validate_expected_exact_value(
        item,
        field_name="checkpoint",
        expected_value=DASHBOARD_SURFACE_CHECKPOINT_ID,
        error_prefix="Dashboard status item",
    )
    _validate_expected_exact_value(
        item,
        field_name="contract_version",
        expected_value=DASHBOARD_SURFACE_CONTRACT_VERSION,
        error_prefix="Dashboard status item",
    )

    for field_name in _REQUIRED_STATUS_ITEM_FIELDS:
        if field_name not in item:
            raise ValueError(f"Dashboard status item must declare {field_name}.")

    progress_value = item.get("progress_value")
    if not isinstance(progress_value, (int, float)):
        raise ValueError("Dashboard status item must declare numeric progress_value.")
    if progress_value < 0 or progress_value > 100:
        raise ValueError("Dashboard status item progress_value must be between 0 and 100.")

    kpi_refs = item.get("kpi_refs")
    if not isinstance(kpi_refs, list):
        raise ValueError("Dashboard status item must declare kpi_refs as a list.")

    risk_blocker_refs = item.get("risk_blocker_refs")
    if not isinstance(risk_blocker_refs, list):
        raise ValueError(
            "Dashboard status item must declare risk_blocker_refs as a list."
        )


def validate_dashboard_kpi_metric(metric: dict[str, object]) -> None:
    """Validate one dashboard KPI metric object."""

    for field_name in _PROHIBITED_KPI_FIELDS:
        if field_name in metric:
            raise ValueError(
                f"{field_name} is not allowed in M13.4 dashboard KPI objects."
            )

    _validate_required_string_fields(
        metric,
        ("checkpoint", "contract_version", "kpi_id", "label", "unit", "source_ref"),
        error_prefix="Dashboard KPI metric",
    )
    _validate_expected_exact_value(
        metric,
        field_name="checkpoint",
        expected_value=DASHBOARD_SURFACE_CHECKPOINT_ID,
        error_prefix="Dashboard KPI metric",
    )
    _validate_expected_exact_value(
        metric,
        field_name="contract_version",
        expected_value=DASHBOARD_SURFACE_CONTRACT_VERSION,
        error_prefix="Dashboard KPI metric",
    )

    for field_name in _REQUIRED_KPI_FIELDS:
        if field_name not in metric:
            raise ValueError(f"Dashboard KPI metric must declare {field_name}.")

    value = metric.get("value")
    if not isinstance(value, (int, float, str)):
        raise ValueError(
            "Dashboard KPI metric value must be a string or numeric scalar."
        )

    if metric.get("interpretation_boundary") != KPI_OBJECT_BOUNDARY:
        raise ValueError("Dashboard KPI metric declares an invalid interpretation boundary.")


def validate_dashboard_snapshot_basis(snapshot_basis: dict[str, object]) -> None:
    """Validate dashboard snapshot basis metadata."""

    _validate_expected_exact_value(
        snapshot_basis,
        field_name="checkpoint",
        expected_value=DASHBOARD_SURFACE_CHECKPOINT_ID,
        error_prefix="Dashboard snapshot basis",
    )
    _validate_expected_exact_value(
        snapshot_basis,
        field_name="contract_version",
        expected_value=DASHBOARD_SURFACE_CONTRACT_VERSION,
        error_prefix="Dashboard snapshot basis",
    )
    _validate_required_string_fields(
        snapshot_basis,
        ("snapshot_id", "as_of", "source_context_ref"),
        error_prefix="Dashboard snapshot basis",
    )


def validate_dashboard_visibility_config(
    visibility_config: dict[str, object],
) -> None:
    """Validate dashboard visibility settings."""

    _validate_expected_exact_value(
        visibility_config,
        field_name="checkpoint",
        expected_value=DASHBOARD_SURFACE_CHECKPOINT_ID,
        error_prefix="Dashboard visibility config",
    )
    _validate_expected_exact_value(
        visibility_config,
        field_name="contract_version",
        expected_value=DASHBOARD_SURFACE_CONTRACT_VERSION,
        error_prefix="Dashboard visibility config",
    )
    visible_fields = visibility_config.get("visible_fields")
    if not isinstance(visible_fields, list):
        raise ValueError("Dashboard visibility config must declare visible_fields.")
    _validate_visibility_fields(visible_fields)


def _validate_supported_surface_type(surface_type: str) -> None:
    if surface_type not in SUPPORTED_DASHBOARD_SURFACE_TYPES:
        raise ValueError(
            "Unsupported dashboard surface type. "
            f"Expected one of: {', '.join(SUPPORTED_DASHBOARD_SURFACE_TYPES)}."
        )


def _validate_supported_output_kind(requested_output_kind: str) -> None:
    if requested_output_kind not in SUPPORTED_DASHBOARD_OUTPUT_KINDS:
        raise ValueError(
            "Unsupported dashboard output kind. "
            f"Expected one of: {', '.join(SUPPORTED_DASHBOARD_OUTPUT_KINDS)}."
        )


def _validate_visibility_fields(visible_fields: list[object]) -> None:
    if not visible_fields:
        raise ValueError("Dashboard visibility config must declare visible fields.")

    for field_name in visible_fields:
        if field_name not in SUPPORTED_DASHBOARD_VISIBILITY_FIELDS:
            raise ValueError(
                "Unsupported dashboard visibility field. "
                f"Expected one of: {', '.join(SUPPORTED_DASHBOARD_VISIBILITY_FIELDS)}."
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
