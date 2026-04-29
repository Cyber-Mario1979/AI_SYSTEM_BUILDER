import pytest

from asbp.export_engine import (
    DAY_TIMESCALE,
    DEPENDENCIES_VISIBILITY_FIELD,
    DURATION_VISIBILITY_FIELD,
    FINISH_TO_START_DEPENDENCY_TYPE,
    GANTT_PLANNING_EXPORT_FAMILY,
    GANTT_RENDERING_BOUNDARY,
    GANTT_SURFACE_CHECKPOINT_ID,
    GANTT_SURFACE_CONTRACT_VERSION,
    GANTT_TIMELINE_OUTPUT_KIND,
    GANTT_TIMELINE_SHAPE,
    STATUS_VISIBILITY_FIELD,
    UNGROUPED_GANTT_GROUPING_MODE,
    WORK_PACKAGE_GANTT_GROUPING_MODE,
    build_gantt_dependency_ref,
    build_gantt_planning_export_payload,
    build_gantt_planning_export_request,
    build_gantt_planning_item,
    build_gantt_planning_visualization_surface_baseline,
    build_gantt_timeline_basis,
    validate_export_request_payload,
)


def _planning_items() -> list[dict[str, object]]:
    return [
        build_gantt_planning_item(
            item_id="PLAN-001",
            label="Prepare URS",
            start_date="2026-05-01",
            finish_date="2026-05-02",
            duration="2d",
            status="planned",
            grouping_key="WP-001",
        ),
        build_gantt_planning_item(
            item_id="PLAN-002",
            label="Review URS",
            start_date="2026-05-03",
            finish_date="2026-05-03",
            duration="1d",
            status="planned",
            grouping_key="WP-001",
            dependency_refs=["PLAN-001"],
        ),
    ]


def _dependency_refs() -> list[dict[str, object]]:
    return [
        build_gantt_dependency_ref(
            predecessor_id="PLAN-001",
            successor_id="PLAN-002",
            dependency_type=FINISH_TO_START_DEPENDENCY_TYPE,
        )
    ]


def _timeline_basis() -> dict[str, object]:
    return build_gantt_timeline_basis(
        calendar_ref="CAL-STANDARD-5D",
        timescale=DAY_TIMESCALE,
    )


def test_build_gantt_planning_visualization_surface_baseline_exposes_m13_3_rules() -> None:
    baseline = build_gantt_planning_visualization_surface_baseline()

    assert baseline["checkpoint"] == GANTT_SURFACE_CHECKPOINT_ID
    assert baseline["contract_version"] == GANTT_SURFACE_CONTRACT_VERSION
    assert baseline["export_family"] == GANTT_PLANNING_EXPORT_FAMILY
    assert baseline["supported_output_kind"] == GANTT_TIMELINE_OUTPUT_KIND
    assert WORK_PACKAGE_GANTT_GROUPING_MODE in baseline["supported_grouping_modes"]
    assert DEPENDENCIES_VISIBILITY_FIELD in baseline["supported_visibility_fields"]
    assert FINISH_TO_START_DEPENDENCY_TYPE in baseline["supported_dependency_types"]
    assert baseline["timeline_shape"] == GANTT_TIMELINE_SHAPE
    assert baseline["rendering_boundary"] == GANTT_RENDERING_BOUNDARY


def test_build_gantt_planning_item_returns_valid_item_contract() -> None:
    item = build_gantt_planning_item(
        item_id="PLAN-001",
        label="Prepare URS",
        start_date="2026-05-01",
        finish_date="2026-05-02",
        duration="2d",
        status="planned",
        grouping_key="WP-001",
    )

    assert item["checkpoint"] == GANTT_SURFACE_CHECKPOINT_ID
    assert item["contract_version"] == GANTT_SURFACE_CONTRACT_VERSION
    assert item["item_id"] == "PLAN-001"


def test_build_gantt_planning_export_payload_returns_m13_1_compatible_shape() -> None:
    payload = build_gantt_planning_export_payload(
        planning_items=_planning_items(),
        dependency_refs=_dependency_refs(),
        timeline_basis=_timeline_basis(),
        grouping_mode=WORK_PACKAGE_GANTT_GROUPING_MODE,
        visible_fields=[
            STATUS_VISIBILITY_FIELD,
            DEPENDENCIES_VISIBILITY_FIELD,
            DURATION_VISIBILITY_FIELD,
        ],
    )

    assert payload["checkpoint"] == GANTT_SURFACE_CHECKPOINT_ID
    assert payload["contract_version"] == GANTT_SURFACE_CONTRACT_VERSION
    assert "planning_items" in payload
    assert "dependency_refs" in payload
    assert "timeline_basis" in payload
    assert payload["grouping"]["mode"] == WORK_PACKAGE_GANTT_GROUPING_MODE
    assert payload["output_shape"]["timeline_shape"] == GANTT_TIMELINE_SHAPE
    assert payload["output_shape"]["rendering_boundary"] == GANTT_RENDERING_BOUNDARY


def test_build_gantt_planning_export_request_returns_valid_m13_1_request() -> None:
    request = build_gantt_planning_export_request(
        export_job_id="EXPJOB-003",
        export_id="GANTT-001",
        export_version="1.0.0",
        source_context_kind="plan",
        source_context_ref="PLAN-001",
        planning_items=_planning_items(),
        dependency_refs=_dependency_refs(),
        timeline_basis=_timeline_basis(),
        grouping_mode=WORK_PACKAGE_GANTT_GROUPING_MODE,
    )

    assert request["export_family"] == GANTT_PLANNING_EXPORT_FAMILY
    assert request["requested_output_kind"] == GANTT_TIMELINE_OUTPUT_KIND
    assert request["input_payload"]["checkpoint"] == GANTT_SURFACE_CHECKPOINT_ID
    validate_export_request_payload(request)


def test_build_gantt_planning_export_payload_rejects_unknown_dependency_target() -> None:
    dependency_refs = [
        build_gantt_dependency_ref(
            predecessor_id="PLAN-404",
            successor_id="PLAN-002",
        )
    ]

    with pytest.raises(ValueError, match="unknown predecessor_id"):
        build_gantt_planning_export_payload(
            planning_items=_planning_items(),
            dependency_refs=dependency_refs,
            timeline_basis=_timeline_basis(),
        )


def test_build_gantt_planning_export_payload_rejects_self_dependency() -> None:
    dependency_refs = [
        build_gantt_dependency_ref(
            predecessor_id="PLAN-001",
            successor_id="PLAN-001",
        )
    ]

    with pytest.raises(ValueError, match="same item"):
        build_gantt_planning_export_payload(
            planning_items=_planning_items(),
            dependency_refs=dependency_refs,
            timeline_basis=_timeline_basis(),
        )


def test_build_gantt_planning_export_payload_rejects_item_self_dependency_ref() -> None:
    planning_items = [
        build_gantt_planning_item(
            item_id="PLAN-001",
            label="Prepare URS",
            start_date="2026-05-01",
            finish_date="2026-05-02",
            duration="2d",
            status="planned",
            dependency_refs=["PLAN-001"],
        )
    ]

    with pytest.raises(ValueError, match="cannot depend on itself"):
        build_gantt_planning_export_payload(
            planning_items=planning_items,
            dependency_refs=[],
            timeline_basis=_timeline_basis(),
        )


def test_build_gantt_planning_export_payload_rejects_unsupported_grouping_mode() -> None:
    with pytest.raises(ValueError, match="Unsupported Gantt grouping mode"):
        build_gantt_planning_export_payload(
            planning_items=_planning_items(),
            dependency_refs=_dependency_refs(),
            timeline_basis=_timeline_basis(),
            grouping_mode="by_mood",
        )


def test_build_gantt_planning_export_payload_rejects_unsupported_visibility_field() -> None:
    with pytest.raises(ValueError, match="Unsupported Gantt visibility field"):
        build_gantt_planning_export_payload(
            planning_items=_planning_items(),
            dependency_refs=_dependency_refs(),
            timeline_basis=_timeline_basis(),
            visible_fields=["status", "color_palette"],
        )


def test_build_gantt_planning_export_payload_rejects_duplicate_dependency_ref() -> None:
    dependency_refs = _dependency_refs() + _dependency_refs()

    with pytest.raises(ValueError, match="Duplicate Gantt dependency"):
        build_gantt_planning_export_payload(
            planning_items=_planning_items(),
            dependency_refs=dependency_refs,
            timeline_basis=_timeline_basis(),
            grouping_mode=UNGROUPED_GANTT_GROUPING_MODE,
        )
