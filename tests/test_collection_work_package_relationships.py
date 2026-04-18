import json
from datetime import datetime, timezone

import pytest

from asbp.planning_logic import generate_plan_baseline
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    StateModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
    SelectorContextModel,
)
from asbp.state_store import build_persisted_state_payload, load_validated_state


def write_state_file(state_file, payload: dict) -> None:
    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_load_validated_state_accepts_collection_bound_to_existing_work_package(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [
                {
                    "collection_id": "TC-001",
                    "title": "Committed Selection",
                    "collection_state": "committed",
                    "work_package_id": "WP-001",
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.task_collections == [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            work_package_id="WP-001",
        )
    ]


def test_build_persisted_state_payload_persists_collection_work_package_id():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        work_packages=[
            WorkPackageModel(
                wp_id="WP-001",
                title="Tablet press qualification",
                status="open",
            )
        ],
        task_collections=[
            TaskCollectionModel(
                collection_id="TC-001",
                title="Committed Selection",
                collection_state="committed",
                work_package_id="WP-001",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Committed Selection",
            "collection_state": "committed",
            "work_package_id": "WP-001",
        }
    ]


def test_load_validated_state_rejects_dangling_collection_work_package_id(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [],
            "task_collections": [
                {
                    "collection_id": "TC-001",
                    "title": "Committed Selection",
                    "collection_state": "committed",
                    "work_package_id": "WP-999",
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert (
        "Persisted collection work_package_id does not exist: TC-001 -> WP-999"
        in str(exc_info.value)
    )


def test_generate_plan_baseline_prefers_work_package_bound_committed_collection_scope():
    plan_start = datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc)

    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=plan_start,
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
            selector_context=SelectorContextModel(
                preset_id="oral-solid-dose-standard",
                scope_intent="qualification-only",
                standards_bundles=["cqv-core", "automation"],
            ),
        )
    ]
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Legacy committed task",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="WP-bound committed task",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
    ]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Legacy committed selection",
            collection_state="committed",
            task_ids=["TASK-001"],
        ),
        TaskCollectionModel(
            collection_id="TC-002",
            title="WP-bound committed selection",
            collection_state="committed",
            work_package_id="WP-001",
            task_ids=["TASK-002"],
        ),
    ]

    updated_plan = generate_plan_baseline(
        plans,
        work_packages,
        tasks,
        task_collections,
        plan_id="PLAN-001",
    )

    assert updated_plan is plans[0]
    assert [task_plan.task_id for task_plan in plans[0].generated_task_plans] == [
        "TASK-002"
    ]