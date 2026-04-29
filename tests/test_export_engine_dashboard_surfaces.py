import pytest

from asbp.export_engine import (
    DASHBOARD_RENDERING_BOUNDARY,
    DASHBOARD_SNAPSHOT_OUTPUT_KIND,
    DASHBOARD_SNAPSHOT_SHAPE,
    DASHBOARD_SNAPSHOT_SURFACE_TYPE,
    DASHBOARD_STATUS_EXPORT_FAMILY,
    DASHBOARD_SURFACE_CHECKPOINT_ID,
    DASHBOARD_SURFACE_CONTRACT_VERSION,
    KPI_DASHBOARD_VISIBILITY_FIELD,
    KPI_OBJECT_BOUNDARY,
    KPI_SUMMARY_SURFACE_TYPE,
    PROGRESS_DASHBOARD_VISIBILITY_FIELD,
    SOURCE_REFERENCE_DASHBOARD_VISIBILITY_FIELD,
    STATUS_DASHBOARD_VISIBILITY_FIELD,
    STATUS_SUMMARY_SURFACE_TYPE,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    build_dashboard_kpi_metric,
    build_dashboard_snapshot_basis,
    build_dashboard_status_export_payload,
    build_dashboard_status_export_request,
    build_dashboard_status_item,
    build_dashboard_status_summary_surface_baseline,
    validate_export_request_payload,
)


def _summary_metrics() -> list[dict[str, object]]:
    return [
        build_dashboard_kpi_metric(
            kpi_id="KPI-001",
            label="Open Tasks",
            value=4,
            unit="count",
            source_ref="WP-001",
        ),
        build_dashboard_kpi_metric(
            kpi_id="KPI-002",
            label="Planned Progress",
            value="60",
            unit="percent",
            source_ref="PLAN-001",
        ),
    ]


def _status_items() -> list[dict[str, object]]:
    return [
        build_dashboard_status_item(
            item_id="DASH-001",
            label="URS Preparation",
            status="in_progress",
            progress_value=60,
            summary_category="document_work",
            source_ref="TASK-001",
            kpi_refs=["KPI-002"],
        ),
        build_dashboard_status_item(
            item_id="DASH-002",
            label="Protocol Readiness",
            status="planned",
            progress_value=0,
            summary_category="protocol_work",
            source_ref="TASK-002",
            kpi_refs=["KPI-001"],
        ),
    ]


def _snapshot_basis() -> dict[str, object]:
    return build_dashboard_snapshot_basis(
        snapshot_id="DASH-SNAP-001",
        as_of="2026-05-01T09:00:00",
        source_context_ref="WP-001",
    )


def test_build_dashboard_status_summary_surface_baseline_exposes_m13_4_rules() -> None:
    baseline = build_dashboard_status_summary_surface_baseline()

    assert baseline["checkpoint"] == DASHBOARD_SURFACE_CHECKPOINT_ID
    assert baseline["contract_version"] == DASHBOARD_SURFACE_CONTRACT_VERSION
    assert baseline["export_family"] == DASHBOARD_STATUS_EXPORT_FAMILY
    assert DASHBOARD_SNAPSHOT_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert STATUS_SUMMARY_SURFACE_TYPE in baseline["supported_surface_types"]
    assert KPI_DASHBOARD_VISIBILITY_FIELD in baseline["supported_visibility_fields"]
    assert baseline["output_shapes"][DASHBOARD_SNAPSHOT_OUTPUT_KIND] == (
        DASHBOARD_SNAPSHOT_SHAPE
    )
    assert baseline["kpi_boundary"] == KPI_OBJECT_BOUNDARY


def test_build_dashboard_kpi_metric_returns_black_box_metric_object() -> None:
    metric = build_dashboard_kpi_metric(
        kpi_id="KPI-001",
        label="Open Tasks",
        value=4,
        unit="count",
        source_ref="WP-001",
    )

    assert metric["checkpoint"] == DASHBOARD_SURFACE_CHECKPOINT_ID
    assert metric["contract_version"] == DASHBOARD_SURFACE_CONTRACT_VERSION
    assert metric["kpi_id"] == "KPI-001"
    assert metric["interpretation_boundary"] == KPI_OBJECT_BOUNDARY


def test_dashboard_kpi_metric_rejects_calculation_method_inside_m13_4() -> None:
    metric = build_dashboard_kpi_metric(
        kpi_id="KPI-001",
        label="Open Tasks",
        value=4,
        unit="count",
        source_ref="WP-001",
    )
    metric["calculation_method"] = "count open tasks"

    with pytest.raises(ValueError, match="calculation_method is not allowed"):
        from asbp.export_engine import validate_dashboard_kpi_metric

        validate_dashboard_kpi_metric(metric)


def test_build_dashboard_status_item_rejects_progress_outside_range() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        build_dashboard_status_item(
            item_id="DASH-001",
            label="URS Preparation",
            status="in_progress",
            progress_value=101,
            summary_category="document_work",
            source_ref="TASK-001",
        )


def test_build_dashboard_status_export_payload_returns_m13_1_compatible_shape() -> None:
    payload = build_dashboard_status_export_payload(
        requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
        surface_type=DASHBOARD_SNAPSHOT_SURFACE_TYPE,
        status_items=_status_items(),
        summary_metrics=_summary_metrics(),
        snapshot_basis=_snapshot_basis(),
        visible_fields=[
            STATUS_DASHBOARD_VISIBILITY_FIELD,
            PROGRESS_DASHBOARD_VISIBILITY_FIELD,
            KPI_DASHBOARD_VISIBILITY_FIELD,
            SOURCE_REFERENCE_DASHBOARD_VISIBILITY_FIELD,
        ],
    )

    assert payload["checkpoint"] == DASHBOARD_SURFACE_CHECKPOINT_ID
    assert payload["contract_version"] == DASHBOARD_SURFACE_CONTRACT_VERSION
    assert payload["surface_type"] == DASHBOARD_SNAPSHOT_SURFACE_TYPE
    assert "status_items" in payload
    assert "summary_metrics" in payload
    assert "snapshot_basis" in payload
    assert payload["output_shape"]["dashboard_shape"] == DASHBOARD_SNAPSHOT_SHAPE
    assert payload["output_shape"]["rendering_boundary"] == DASHBOARD_RENDERING_BOUNDARY


def test_build_dashboard_status_export_request_returns_valid_m13_1_request() -> None:
    request = build_dashboard_status_export_request(
        export_job_id="EXPJOB-004",
        export_id="DASHBOARD-001",
        export_version="1.0.0",
        requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
        source_context_kind="work_package",
        source_context_ref="WP-001",
        surface_type=DASHBOARD_SNAPSHOT_SURFACE_TYPE,
        status_items=_status_items(),
        summary_metrics=_summary_metrics(),
        snapshot_basis=_snapshot_basis(),
    )

    assert request["export_family"] == DASHBOARD_STATUS_EXPORT_FAMILY
    assert request["requested_output_kind"] == DASHBOARD_SNAPSHOT_OUTPUT_KIND
    assert request["input_payload"]["checkpoint"] == DASHBOARD_SURFACE_CHECKPOINT_ID
    validate_export_request_payload(request)


def test_build_dashboard_status_export_payload_accepts_structured_report_payload_shape() -> None:
    payload = build_dashboard_status_export_payload(
        requested_output_kind=STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
        surface_type=KPI_SUMMARY_SURFACE_TYPE,
        status_items=_status_items(),
        summary_metrics=_summary_metrics(),
        snapshot_basis=_snapshot_basis(),
    )

    assert payload["output_shape"]["requested_output_kind"] == (
        STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND
    )


def test_build_dashboard_status_export_payload_rejects_unsupported_surface_type() -> None:
    with pytest.raises(ValueError, match="Unsupported dashboard surface type"):
        build_dashboard_status_export_payload(
            requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
            surface_type="executive_slide_deck",
            status_items=_status_items(),
            summary_metrics=_summary_metrics(),
            snapshot_basis=_snapshot_basis(),
        )


def test_build_dashboard_status_export_payload_rejects_unsupported_visibility_field() -> None:
    with pytest.raises(ValueError, match="Unsupported dashboard visibility field"):
        build_dashboard_status_export_payload(
            requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
            surface_type=DASHBOARD_SNAPSHOT_SURFACE_TYPE,
            status_items=_status_items(),
            summary_metrics=_summary_metrics(),
            snapshot_basis=_snapshot_basis(),
            visible_fields=["status", "chart_color"],
        )


def test_build_dashboard_status_export_payload_rejects_duplicate_item_ids() -> None:
    item = _status_items()[0]
    with pytest.raises(ValueError, match="Duplicate dashboard item_id"):
        build_dashboard_status_export_payload(
            requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
            surface_type=DASHBOARD_SNAPSHOT_SURFACE_TYPE,
            status_items=[item, item],
            summary_metrics=_summary_metrics(),
            snapshot_basis=_snapshot_basis(),
        )


def test_build_dashboard_status_export_payload_rejects_unknown_kpi_reference() -> None:
    status_items = [
        build_dashboard_status_item(
            item_id="DASH-001",
            label="URS Preparation",
            status="in_progress",
            progress_value=60,
            summary_category="document_work",
            source_ref="TASK-001",
            kpi_refs=["KPI-404"],
        )
    ]

    with pytest.raises(ValueError, match="unknown KPI"):
        build_dashboard_status_export_payload(
            requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
            surface_type=DASHBOARD_SNAPSHOT_SURFACE_TYPE,
            status_items=status_items,
            summary_metrics=_summary_metrics(),
            snapshot_basis=_snapshot_basis(),
        )
