# tests/test_output_target_logic.py

from datetime import datetime, timezone

from asbp.output_target_logic import build_work_package_output_target_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def make_bound_context_work_package(
    wp_id: str = "WP-001",
    title: str = "Tablet press qualification",
) -> WorkPackageModel:
    return WorkPackageModel(
        wp_id=wp_id,
        title=title,
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "automation"],
        ),
    )


def test_output_target_returns_none_for_missing_work_package():
    payload = build_work_package_output_target_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_output_target_reports_blocked_single_work_package_operator_target():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_target_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["output_target_metadata"] == {
        "output_target_id": "work_package_operator_response_target_v1",
        "output_target_family": "single_work_package_operator_response",
        "target_scope": "single_work_package",
        "target_audience": "operator",
        "delivery_format": "chat_text",
        "target_state": "blocked",
        "generation_surface_id": "work_package_controlled_generation_surface_v1",
        "selected_plan_id": None,
        "generation_allowed": False,
    }
    assert payload["allowed_response_modes"] == [
        "blocked_explainer",
        "execution_ready_summary",
    ]
    assert payload["current_response_mode"] == "blocked_explainer"
    assert payload["target_boundaries"] == {
        "multi_work_package_output": False,
        "document_artifact_output": False,
        "file_export_output": False,
    }


def test_output_target_reports_available_single_work_package_operator_target():
    work_packages = [make_bound_context_work_package()]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            work_package_id="WP-001",
            task_ids=["TASK-001"],
        )
    ]
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        )
    ]
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="committed",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]

    payload = build_work_package_output_target_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["output_target_metadata"] == {
        "output_target_id": "work_package_operator_response_target_v1",
        "output_target_family": "single_work_package_operator_response",
        "target_scope": "single_work_package",
        "target_audience": "operator",
        "delivery_format": "chat_text",
        "target_state": "available",
        "generation_surface_id": "work_package_controlled_generation_surface_v1",
        "selected_plan_id": "PLAN-001",
        "generation_allowed": True,
    }
    assert payload["allowed_response_modes"] == [
        "blocked_explainer",
        "execution_ready_summary",
    ]
    assert payload["current_response_mode"] == "execution_ready_summary"
    assert payload["target_boundaries"] == {
        "multi_work_package_output": False,
        "document_artifact_output": False,
        "file_export_output": False,
    }