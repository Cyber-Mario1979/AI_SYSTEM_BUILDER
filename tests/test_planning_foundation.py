import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from asbp.planning_logic import (
    build_plan_review_payload,
    commit_plan,
    generate_next_plan_id,
    generate_plan_baseline,
    list_plan_review_rows,
    set_plan_planned_start_at,
    set_plan_planning_basis,
    set_plan_planning_calendar,
)
from asbp.state_model import (
    GeneratedTaskPlanModel,
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    StateModel,
    TaskCollectionModel,
    TaskModel,
)
from asbp.state_store import build_persisted_state_payload, load_validated_state



def write_state_file(state_file, payload: dict) -> None:
    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_load_validated_state_defaults_missing_plans_to_empty_list(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [],
            "task_collections": [],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == []


def test_build_persisted_state_payload_omits_empty_plans_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
    )

    payload = build_persisted_state_payload(state)

    assert "plans" not in payload


def test_generate_next_plan_id_uses_plan_namespace_and_existing_max():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        ),
        PlanningModel(
            plan_id="PLAN-007",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]

    assert generate_next_plan_id(plans) == "PLAN-008"


def test_load_validated_state_accepts_plan_linked_to_existing_work_package(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]


def test_load_validated_state_rejects_duplicate_plan_ids(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                },
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "committed",
                },
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Duplicate plan_id is not allowed: PLAN-001" in str(exc_info.value)


def test_load_validated_state_rejects_dangling_plan_work_package_link(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-999",
                    "plan_state": "draft",
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert (
        "Persisted plan work_package_id does not exist: PLAN-001 -> WP-999"
        in str(exc_info.value)
    )


def test_set_plan_planning_basis_attaches_duration_source_to_target_plan_only():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]

    updated_plan = set_plan_planning_basis(
        plans,
        plan_id="PLAN-001",
        duration_source="task_duration",
        basis_label="Task duration baseline",
    )

    assert updated_plan is plans[0]
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]


def test_set_plan_planning_basis_returns_none_for_missing_plan_id():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]

    updated_plan = set_plan_planning_basis(
        plans,
        plan_id="PLAN-999",
        duration_source="task_duration",
    )

    assert updated_plan is None
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]


def test_load_validated_state_accepts_plan_with_planning_basis(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                        "basis_label": "Task duration baseline",
                    },
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
        )
    ]


def test_build_persisted_state_payload_omits_null_planning_basis_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
        }
    ]


def test_build_persisted_state_payload_omits_null_basis_label_inside_planning_basis():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
                planning_basis=PlanningBasisModel(
                    duration_source="task_duration",
                ),
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
            "planning_basis": {
                "duration_source": "task_duration",
            },
        }
    ]


def test_load_validated_state_rejects_invalid_duration_source_in_planning_basis(
    tmp_path,
):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "manual-entry",
                    },
                }
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "duration_source" in str(exc_info.value)


def test_set_plan_planned_start_at_updates_target_plan_only():
    planned_start_at = datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc)

    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]

    updated_plan = set_plan_planned_start_at(
        plans,
        plan_id="PLAN-001",
        planned_start_at=planned_start_at,
    )

    assert updated_plan is plans[0]
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=planned_start_at,
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]


def test_set_plan_planned_start_at_returns_none_for_missing_plan_id():
    planned_start_at = datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc)

    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]

    updated_plan = set_plan_planned_start_at(
        plans,
        plan_id="PLAN-999",
        planned_start_at=planned_start_at,
    )

    assert updated_plan is None
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]


def test_load_validated_state_accepts_timezone_aware_planned_start_at(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planned_start_at": "2026-04-15T08:30:00+00:00",
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planned_start_at=datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc),
        )
    ]


def test_build_persisted_state_payload_omits_null_planned_start_at_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
        }
    ]


def test_build_persisted_state_payload_persists_timezone_aware_planned_start_at():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
                planned_start_at=datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc),
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
            "planned_start_at": "2026-04-15T08:30:00Z",
        }
    ]


def test_load_validated_state_rejects_naive_planned_start_at(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planned_start_at": "2026-04-15T08:30:00",
                }
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "planned_start_at" in str(exc_info.value)


def test_set_plan_planning_calendar_updates_target_plan_only():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc),
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]

    updated_plan = set_plan_planning_calendar(
        plans,
        plan_id="PLAN-001",
        working_days=["friday", "monday", "wednesday"],
        workday_hours=8,
        workmonth_mode="calendar_month",
    )

    assert updated_plan is plans[0]
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="committed",
        ),
    ]


def test_set_plan_planning_calendar_returns_none_for_missing_plan_id():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]

    updated_plan = set_plan_planning_calendar(
        plans,
        plan_id="PLAN-999",
        working_days=["monday", "tuesday", "wednesday"],
        workday_hours=8,
    )

    assert updated_plan is None
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
        )
    ]


def test_load_validated_state_accepts_plan_with_planning_calendar(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]


def test_build_persisted_state_payload_omits_null_planning_calendar_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
        }
    ]


def test_build_persisted_state_payload_persists_planning_calendar():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
                planning_calendar=PlanningCalendarModel(
                    working_days=["monday", "wednesday", "friday"],
                    workday_hours=8,
                    workmonth_mode="calendar_month",
                ),
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
            "planning_calendar": {
                "working_days": ["monday", "wednesday", "friday"],
                "workday_hours": 8,
                "workmonth_mode": "calendar_month",
            },
        }
    ]


def test_load_validated_state_normalizes_working_days_to_canonical_order(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_calendar": {
                        "working_days": ["friday", "monday", "wednesday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]


def test_load_validated_state_rejects_duplicate_working_days_in_planning_calendar(
    tmp_path,
):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_calendar": {
                        "working_days": ["monday", "monday", "wednesday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                }
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Duplicate working day is not allowed" in str(exc_info.value)


def test_load_validated_state_rejects_invalid_workday_hours_in_planning_calendar(
    tmp_path,
):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 0,
                        "workmonth_mode": "calendar_month",
                    },
                }
            ],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "workday_hours" in str(exc_info.value)
def test_generate_plan_baseline_builds_serialized_dependency_aware_plan():
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
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            duration=2,
            work_package_id="WP-001",
            status="planned",
            dependencies=["TASK-001"],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Not committed",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
    ]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            task_ids=["TASK-002", "TASK-001"],
        )
    ]

    updated_plan = generate_plan_baseline(
        plans,
        tasks,
        task_collections,
        plan_id="PLAN-001",
    )

    assert updated_plan is plans[0]
    assert plans[0].generated_task_plans == [
        GeneratedTaskPlanModel(
            task_id="TASK-001",
            sequence_order=1,
            duration_days=1,
            dependency_task_ids=[],
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planned_finish_at=datetime(2026, 4, 13, 16, 30, tzinfo=timezone.utc),
        ),
        GeneratedTaskPlanModel(
            task_id="TASK-002",
            sequence_order=2,
            duration_days=2,
            dependency_task_ids=["TASK-001"],
            planned_start_at=datetime(2026, 4, 15, 8, 30, tzinfo=timezone.utc),
            planned_finish_at=datetime(2026, 4, 17, 16, 30, tzinfo=timezone.utc),
        ),
    ]


def test_generate_plan_baseline_returns_none_for_missing_plan_id():
    updated_plan = generate_plan_baseline(
        [],
        [],
        [],
        plan_id="PLAN-999",
    )

    assert updated_plan is None


def test_generate_plan_baseline_rejects_missing_planning_basis():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
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
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            task_ids=["TASK-001"],
        )
    ]

    with pytest.raises(ValueError) as exc_info:
        generate_plan_baseline(
            plans,
            tasks,
            task_collections,
            plan_id="PLAN-001",
        )

    assert "planning_basis must exist" in str(exc_info.value)


def test_generate_plan_baseline_rejects_dependency_outside_eligible_committed_scope():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
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
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
            dependencies=["TASK-003"],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Outside committed scope",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        ),
    ]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            task_ids=["TASK-001", "TASK-002"],
        )
    ]

    with pytest.raises(ValueError) as exc_info:
        generate_plan_baseline(
            plans,
            tasks,
            task_collections,
            plan_id="PLAN-001",
        )

    assert "outside eligible committed plan scope" in str(exc_info.value)


def test_load_validated_state_accepts_plan_with_generated_task_plans(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        }
                    ],
                }
            ],
        },
    )

    state = load_validated_state(state_file)

    assert state.plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            generated_task_plans=[
                GeneratedTaskPlanModel(
                    task_id="TASK-001",
                    sequence_order=1,
                    duration_days=1,
                    dependency_task_ids=[],
                    planned_start_at=datetime(
                        2026, 4, 13, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 13, 16, 30, tzinfo=timezone.utc
                    ),
                )
            ],
        )
    ]


def test_build_persisted_state_payload_omits_empty_generated_task_plans():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
        }
    ]


def test_build_persisted_state_payload_persists_generated_task_plans():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        plans=[
            PlanningModel(
                plan_id="PLAN-001",
                work_package_id="WP-001",
                plan_state="draft",
                generated_task_plans=[
                    GeneratedTaskPlanModel(
                        task_id="TASK-001",
                        sequence_order=1,
                        duration_days=1,
                        dependency_task_ids=[],
                        planned_start_at=datetime(
                            2026, 4, 13, 8, 30, tzinfo=timezone.utc
                        ),
                        planned_finish_at=datetime(
                            2026, 4, 13, 16, 30, tzinfo=timezone.utc
                        ),
                    )
                ],
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["plans"] == [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
            "generated_task_plans": [
                {
                    "task_id": "TASK-001",
                    "sequence_order": 1,
                    "duration_days": 1,
                    "dependency_task_ids": [],
                    "planned_start_at": "2026-04-13T08:30:00Z",
                    "planned_finish_at": "2026-04-13T16:30:00Z",
                }
            ],
        }
    ]


def test_load_validated_state_rejects_duplicate_generated_task_plan_task_ids(tmp_path):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        },
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 2,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-15T08:30:00+00:00",
                            "planned_finish_at": "2026-04-15T16:30:00+00:00",
                        },
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Duplicate generated task plan task_id is not allowed: TASK-001" in str(
        exc_info.value
    )

def test_list_plan_review_rows_returns_none_for_missing_plan_id():
    rows = list_plan_review_rows(
        [],
        plan_id="PLAN-999",
    )

    assert rows is None


def test_list_plan_review_rows_returns_sequence_ordered_generated_rows():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            generated_task_plans=[
                GeneratedTaskPlanModel(
                    task_id="TASK-002",
                    sequence_order=2,
                    duration_days=2,
                    dependency_task_ids=["TASK-001"],
                    planned_start_at=datetime(
                        2026, 4, 15, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 17, 16, 30, tzinfo=timezone.utc
                    ),
                ),
                GeneratedTaskPlanModel(
                    task_id="TASK-001",
                    sequence_order=1,
                    duration_days=1,
                    dependency_task_ids=[],
                    planned_start_at=datetime(
                        2026, 4, 13, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 13, 16, 30, tzinfo=timezone.utc
                    ),
                ),
            ],
        )
    ]

    rows = list_plan_review_rows(
        plans,
        plan_id="PLAN-001",
    )

    assert rows == [
        {
            "task_id": "TASK-001",
            "sequence_order": 1,
            "duration_days": 1,
            "dependency_task_ids": [],
            "planned_start_at": "2026-04-13T08:30:00Z",
            "planned_finish_at": "2026-04-13T16:30:00Z",
        },
        {
            "task_id": "TASK-002",
            "sequence_order": 2,
            "duration_days": 2,
            "dependency_task_ids": ["TASK-001"],
            "planned_start_at": "2026-04-15T08:30:00Z",
            "planned_finish_at": "2026-04-17T16:30:00Z",
        },
    ]


def test_build_plan_review_payload_returns_none_for_missing_plan_id():
    payload = build_plan_review_payload(
        [],
        plan_id="PLAN-999",
    )

    assert payload is None


def test_build_plan_review_payload_returns_summary_for_generated_plan():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
            generated_task_plans=[
                GeneratedTaskPlanModel(
                    task_id="TASK-002",
                    sequence_order=2,
                    duration_days=2,
                    dependency_task_ids=["TASK-001"],
                    planned_start_at=datetime(
                        2026, 4, 15, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 17, 16, 30, tzinfo=timezone.utc
                    ),
                ),
                GeneratedTaskPlanModel(
                    task_id="TASK-001",
                    sequence_order=1,
                    duration_days=1,
                    dependency_task_ids=[],
                    planned_start_at=datetime(
                        2026, 4, 13, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 13, 16, 30, tzinfo=timezone.utc
                    ),
                ),
            ],
        )
    ]

    payload = build_plan_review_payload(
        plans,
        plan_id="PLAN-001",
    )

    assert payload == {
        "plan_id": "PLAN-001",
        "work_package_id": "WP-001",
        "plan_state": "draft",
        "planning_basis": {
            "duration_source": "task_duration",
            "basis_label": "Task duration baseline",
        },
        "planned_start_at": "2026-04-13T08:30:00Z",
        "planning_calendar": {
            "working_days": ["monday", "wednesday", "friday"],
            "workday_hours": 8,
            "workmonth_mode": "calendar_month",
        },
        "generated_task_plans": [
            {
                "task_id": "TASK-001",
                "sequence_order": 1,
                "duration_days": 1,
                "dependency_task_ids": [],
                "planned_start_at": "2026-04-13T08:30:00Z",
                "planned_finish_at": "2026-04-13T16:30:00Z",
            },
            {
                "task_id": "TASK-002",
                "sequence_order": 2,
                "duration_days": 2,
                "dependency_task_ids": ["TASK-001"],
                "planned_start_at": "2026-04-15T08:30:00Z",
                "planned_finish_at": "2026-04-17T16:30:00Z",
            },
        ],
        "generated_task_plan_count": 2,
        "generated_schedule_start_at": "2026-04-13T08:30:00Z",
        "generated_schedule_finish_at": "2026-04-17T16:30:00Z",
    }


def test_build_plan_review_payload_returns_empty_generated_summary_when_not_generated():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
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

    payload = build_plan_review_payload(
        plans,
        plan_id="PLAN-001",
    )

    assert payload == {
        "plan_id": "PLAN-001",
        "work_package_id": "WP-001",
        "plan_state": "draft",
        "planning_basis": {
            "duration_source": "task_duration",
            "basis_label": None,
        },
        "planned_start_at": "2026-04-13T08:30:00Z",
        "planning_calendar": {
            "working_days": ["monday", "wednesday", "friday"],
            "workday_hours": 8,
            "workmonth_mode": "calendar_month",
        },
        "generated_task_plans": [],
        "generated_task_plan_count": 0,
        "generated_schedule_start_at": None,
        "generated_schedule_finish_at": None,
    }



def test_commit_plan_returns_none_for_missing_plan_id():
    updated_plan = commit_plan(
        [],
        plan_id="PLAN-999",
    )

    assert updated_plan is None



def test_commit_plan_transitions_draft_plan_to_committed_without_mutating_payload():
    generated_task_plans = [
        GeneratedTaskPlanModel(
            task_id="TASK-001",
            sequence_order=1,
            duration_days=1,
            dependency_task_ids=[],
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planned_finish_at=datetime(2026, 4, 13, 16, 30, tzinfo=timezone.utc),
        )
    ]
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
            generated_task_plans=generated_task_plans,
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="draft",
        ),
    ]

    updated_plan = commit_plan(
        plans,
        plan_id="PLAN-001",
    )

    assert updated_plan is plans[0]
    assert plans == [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="committed",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
                basis_label="Task duration baseline",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
            generated_task_plans=generated_task_plans,
        ),
        PlanningModel(
            plan_id="PLAN-002",
            work_package_id="WP-002",
            plan_state="draft",
        ),
    ]



def test_commit_plan_rejects_already_committed_plan():
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
            generated_task_plans=[
                GeneratedTaskPlanModel(
                    task_id="TASK-001",
                    sequence_order=1,
                    duration_days=1,
                    dependency_task_ids=[],
                    planned_start_at=datetime(
                        2026, 4, 13, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 13, 16, 30, tzinfo=timezone.utc
                    ),
                )
            ],
        )
    ]

    with pytest.raises(ValueError) as exc_info:
        commit_plan(
            plans,
            plan_id="PLAN-001",
        )

    assert "Plan is already committed: PLAN-001" in str(exc_info.value)



def test_commit_plan_rejects_missing_planning_basis():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
            generated_task_plans=[
                GeneratedTaskPlanModel(
                    task_id="TASK-001",
                    sequence_order=1,
                    duration_days=1,
                    dependency_task_ids=[],
                    planned_start_at=datetime(
                        2026, 4, 13, 8, 30, tzinfo=timezone.utc
                    ),
                    planned_finish_at=datetime(
                        2026, 4, 13, 16, 30, tzinfo=timezone.utc
                    ),
                )
            ],
        )
    ]

    with pytest.raises(ValueError) as exc_info:
        commit_plan(
            plans,
            plan_id="PLAN-001",
        )

    assert "planning_basis must exist" in str(exc_info.value)



def test_commit_plan_rejects_missing_generated_task_plans():
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="draft",
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

    with pytest.raises(ValueError) as exc_info:
        commit_plan(
            plans,
            plan_id="PLAN-001",
        )

    assert "generated_task_plans must exist before commit" in str(exc_info.value)

def test_load_validated_state_rejects_committed_plan_without_generated_task_plans(
    tmp_path,
):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "committed",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Committed plan must include generated_task_plans: PLAN-001" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_generated_task_plans_without_planning_basis(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                }
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        }
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Plan with generated_task_plans must include planning_basis: PLAN-001" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_generated_task_plan_with_missing_task_record(
    tmp_path,
):
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
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-999",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        }
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Generated task plan task_id does not exist in tasks: PLAN-001 -> TASK-999" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_generated_task_plan_task_from_different_work_package(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "duration": 1,
                    "work_package_id": "WP-002",
                    "status": "planned",
                }
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                },
                {
                    "wp_id": "WP-002",
                    "title": "Autoclave qualification",
                    "status": "open",
                },
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        }
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Generated task plan task belongs to different work_package: PLAN-001 -> TASK-001 (WP-002)" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_duplicate_generated_task_plan_sequence_order(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                },
                {
                    "task_id": "TASK-002",
                    "order": 2,
                    "title": "Execute FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                },
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        },
                        {
                            "task_id": "TASK-002",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": ["TASK-001"],
                            "planned_start_at": "2026-04-15T08:30:00+00:00",
                            "planned_finish_at": "2026-04-15T16:30:00+00:00",
                        },
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Duplicate generated task plan sequence_order is not allowed: PLAN-001 -> 1" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_non_contiguous_generated_task_plan_sequence_order(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                },
                {
                    "task_id": "TASK-002",
                    "order": 2,
                    "title": "Execute FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                },
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        },
                        {
                            "task_id": "TASK-002",
                            "sequence_order": 3,
                            "duration_days": 1,
                            "dependency_task_ids": ["TASK-001"],
                            "planned_start_at": "2026-04-15T08:30:00+00:00",
                            "planned_finish_at": "2026-04-15T16:30:00+00:00",
                        },
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Generated task plan sequence_order must be contiguous starting at 1: PLAN-001" in str(
        exc_info.value
    )


def test_load_validated_state_rejects_generated_task_plan_dependency_outside_plan_scope(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                },
                {
                    "task_id": "TASK-002",
                    "order": 2,
                    "title": "Execute FAT",
                    "duration": 1,
                    "work_package_id": "WP-001",
                    "status": "planned",
                    "dependencies": ["TASK-001"],
                },
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
            "plans": [
                {
                    "plan_id": "PLAN-001",
                    "work_package_id": "WP-001",
                    "plan_state": "draft",
                    "planning_basis": {
                        "duration_source": "task_duration",
                    },
                    "planned_start_at": "2026-04-13T08:30:00+00:00",
                    "planning_calendar": {
                        "working_days": ["monday", "wednesday", "friday"],
                        "workday_hours": 8,
                        "workmonth_mode": "calendar_month",
                    },
                    "generated_task_plans": [
                        {
                            "task_id": "TASK-001",
                            "sequence_order": 1,
                            "duration_days": 1,
                            "dependency_task_ids": [],
                            "planned_start_at": "2026-04-13T08:30:00+00:00",
                            "planned_finish_at": "2026-04-13T16:30:00+00:00",
                        },
                        {
                            "task_id": "TASK-002",
                            "sequence_order": 2,
                            "duration_days": 1,
                            "dependency_task_ids": ["TASK-999"],
                            "planned_start_at": "2026-04-15T08:30:00+00:00",
                            "planned_finish_at": "2026-04-15T16:30:00+00:00",
                        },
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError) as exc_info:
        load_validated_state(state_file)

    assert "Generated task plan dependency must exist inside plan scope: PLAN-001 -> TASK-002 -> TASK-999" in str(
        exc_info.value
    )

