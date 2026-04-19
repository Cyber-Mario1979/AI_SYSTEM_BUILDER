from pathlib import Path

ROOT = Path.cwd()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Expected snippet not found in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, snippet: str) -> None:
    text = path.read_text(encoding="utf-8")
    if snippet.strip() in text:
        return
    path.write_text(text.rstrip() + "\n\n\n" + snippet.strip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------
# asbp/collection_logic.py
# ---------------------------------------------------------------------
collection_logic_path = ROOT / "asbp" / "collection_logic.py"

collection_append = '''
def validate_work_package_collection_membership_delete(
    collections: list[TaskCollectionModel],
    *,
    wp_id: str,
) -> str | None:
    collection_ids = build_work_package_collection_ids(collections, wp_id=wp_id)
    if not collection_ids:
        return None

    collection_ids_display = ", ".join(collection_ids)
    return (
        "Work Package cannot be deleted while collections are bound: "
        f"{wp_id} -> [{collection_ids_display}]"
    )
'''
append_once(collection_logic_path, collection_append)

# ---------------------------------------------------------------------
# asbp/planning_logic.py
# ---------------------------------------------------------------------
planning_logic_path = ROOT / "asbp" / "planning_logic.py"

planning_append = '''
def _build_plan_ids_for_task(
    plans: list[PlanningModel],
    *,
    task_id: str,
) -> list[str]:
    plan_ids: list[str] = []

    for plan in plans:
        if any(
            generated_task_plan.task_id == task_id
            or task_id in generated_task_plan.dependency_task_ids
            for generated_task_plan in plan.generated_task_plans
        ):
            plan_ids.append(plan.plan_id)

    return plan_ids


def validate_work_package_plan_membership_delete(
    plans: list[PlanningModel],
    *,
    work_package_id: str,
) -> str | None:
    plan_ids = [
        plan.plan_id
        for plan in plans
        if plan.work_package_id == work_package_id
    ]
    if not plan_ids:
        return None

    plan_ids_display = ", ".join(plan_ids)
    return (
        "Work Package cannot be deleted while plans are associated: "
        f"{work_package_id} -> [{plan_ids_display}]"
    )


def validate_task_plan_membership_delete(
    plans: list[PlanningModel],
    *,
    task_id: str,
) -> str | None:
    plan_ids = _build_plan_ids_for_task(plans, task_id=task_id)
    if not plan_ids:
        return None

    plan_ids_display = ", ".join(plan_ids)
    return (
        "Task cannot be deleted while plans still reference it: "
        f"{task_id} -> [{plan_ids_display}]"
    )


def validate_task_work_package_plan_clear(
    plans: list[PlanningModel],
    *,
    task_id: str,
) -> str | None:
    plan_refs = [
        f"{plan.plan_id} ({plan.work_package_id})"
        for plan in plans
        if any(
            generated_task_plan.task_id == task_id
            or task_id in generated_task_plan.dependency_task_ids
            for generated_task_plan in plan.generated_task_plans
        )
    ]
    if not plan_refs:
        return None

    plan_refs_display = ", ".join(plan_refs)
    return (
        "Task work package cannot be cleared while plans still reference it: "
        f"{task_id} -> [{plan_refs_display}]"
    )
'''
append_once(planning_logic_path, planning_append)

# ---------------------------------------------------------------------
# asbp/work_package_logic.py
# ---------------------------------------------------------------------
work_package_logic_path = ROOT / "asbp" / "work_package_logic.py"

replace_once(
    work_package_logic_path,
    'from asbp.collection_logic import validate_task_work_package_membership_change\n',
    'from asbp.collection_logic import (\n'
    '    validate_task_work_package_membership_change,\n'
    '    validate_work_package_collection_membership_delete,\n'
    ')\n'
    'from asbp.planning_logic import (\n'
    '    validate_task_work_package_plan_clear,\n'
    '    validate_work_package_plan_membership_delete,\n'
    ')\n',
)

replace_once(
    work_package_logic_path,
    '''def delete_work_package_by_id(
    work_packages: list[WorkPackageModel],
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> tuple[list[WorkPackageModel], bool, str | None]:
''',
    '''def delete_work_package_by_id(
    work_packages: list[WorkPackageModel],
    tasks: list[TaskModel],
    task_collections: list[TaskCollectionModel],
    plans: list,
    *,
    wp_id: str,
) -> tuple[list[WorkPackageModel], bool, str | None]:
''',
)

replace_once(
    work_package_logic_path,
    '''    associated_task_ids = build_work_package_task_ids(tasks, wp_id=wp_id)
    if associated_task_ids:
        task_ids_display = ", ".join(associated_task_ids)
        return (
            list(work_packages),
            False,
            f"Work Package cannot be deleted while tasks are associated: "
            f"{wp_id} -> [{task_ids_display}]",
        )

    updated_work_packages = [
''',
    '''    associated_task_ids = build_work_package_task_ids(tasks, wp_id=wp_id)
    if associated_task_ids:
        task_ids_display = ", ".join(associated_task_ids)
        return (
            list(work_packages),
            False,
            f"Work Package cannot be deleted while tasks are associated: "
            f"{wp_id} -> [{task_ids_display}]",
        )

    collection_membership_error = validate_work_package_collection_membership_delete(
        task_collections,
        wp_id=wp_id,
    )
    if collection_membership_error is not None:
        return list(work_packages), False, collection_membership_error

    plan_membership_error = validate_work_package_plan_membership_delete(
        plans,
        work_package_id=wp_id,
    )
    if plan_membership_error is not None:
        return list(work_packages), False, plan_membership_error

    updated_work_packages = [
''',
)

replace_once(
    work_package_logic_path,
    '''def clear_task_work_package(
    tasks: list[TaskModel],
    task_collections: list[TaskCollectionModel],
    *,
    task_ref: str,
) -> tuple[TaskModel | None, str | None]:
''',
    '''def clear_task_work_package(
    tasks: list[TaskModel],
    task_collections: list[TaskCollectionModel],
    plans: list,
    *,
    task_ref: str,
) -> tuple[TaskModel | None, str | None]:
''',
)

replace_once(
    work_package_logic_path,
    '''    membership_change_error = validate_task_work_package_membership_change(
        task_collections,
        task_id=target_task.task_id,
        target_work_package_id=None,
    )
    if membership_change_error is not None:
        return None, membership_change_error

    target_task.work_package_id = None
''',
    '''    membership_change_error = validate_task_work_package_membership_change(
        task_collections,
        task_id=target_task.task_id,
        target_work_package_id=None,
    )
    if membership_change_error is not None:
        return None, membership_change_error

    plan_membership_error = validate_task_work_package_plan_clear(
        plans,
        task_id=target_task.task_id,
    )
    if plan_membership_error is not None:
        return None, plan_membership_error

    target_task.work_package_id = None
''',
)

# ---------------------------------------------------------------------
# asbp/cli.py
# ---------------------------------------------------------------------
cli_path = ROOT / "asbp" / "cli.py"

replace_once(
    cli_path,
    '''from asbp.work_package_logic import (
    build_work_package_task_ids,
    clear_task_work_package,
    create_work_package,
    delete_work_package_by_id,
    filter_work_packages,
    find_work_package_by_id,
    set_work_package_preset,
    set_work_package_scope_intent,
    set_work_package_selector_type,
    set_work_package_standards_bundles,
    update_work_package_status,
    update_work_package_title,
    set_task_work_package,
)
''',
    '''from asbp.work_package_logic import (
    build_work_package_task_ids,
    clear_task_work_package,
    create_work_package,
    delete_work_package_by_id,
    filter_work_packages,
    find_work_package_by_id,
    set_work_package_preset,
    set_work_package_scope_intent,
    set_work_package_selector_type,
    set_work_package_standards_bundles,
    update_work_package_status,
    update_work_package_title,
    set_task_work_package,
)
from asbp.planning_logic import validate_task_plan_membership_delete
''',
)

replace_once(
    cli_path,
    '''    updated_work_packages, deleted_flag, error_message = delete_work_package_by_id(
        state.work_packages,
        state.tasks,
        wp_id=args.wp_id,
    )
''',
    '''    updated_work_packages, deleted_flag, error_message = delete_work_package_by_id(
        state.work_packages,
        state.tasks,
        state.task_collections,
        state.plans,
        wp_id=args.wp_id,
    )
''',
)

replace_once(
    cli_path,
    '''    membership_error = validate_task_delete_membership(
        state.task_collections,
        task_id=target_task.task_id,
    )
    if membership_error is not None:
        print(membership_error)
        return

    updated_tasks, deleted_flag = delete_task_by_id(state.tasks, target_task.task_id)
''',
    '''    membership_error = validate_task_delete_membership(
        state.task_collections,
        task_id=target_task.task_id,
    )
    if membership_error is not None:
        print(membership_error)
        return

    plan_membership_error = validate_task_plan_membership_delete(
        state.plans,
        task_id=target_task.task_id,
    )
    if plan_membership_error is not None:
        print(plan_membership_error)
        return

    updated_tasks, deleted_flag = delete_task_by_id(state.tasks, target_task.task_id)
''',
)

replace_once(
    cli_path,
    '''        target_task, error_message = clear_task_work_package(
            state.tasks,
            state.task_collections,
            task_ref=args.task_id,
        )
''',
    '''        target_task, error_message = clear_task_work_package(
            state.tasks,
            state.task_collections,
            state.plans,
            task_ref=args.task_id,
        )
''',
)

# ---------------------------------------------------------------------
# tests/test_m8_5c_cross_entity_validation_cli.py
# ---------------------------------------------------------------------
test_path = ROOT / "tests" / "test_m8_5c_cross_entity_validation_cli.py"
test_path.write_text(
    '''import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def restore_state_file():
    original_exists = STATE_FILE.exists()
    original_text = STATE_FILE.read_text(encoding="utf-8") if original_exists else None

    yield

    if original_exists and original_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(original_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()


def make_bound_context_work_package_payload(
    wp_id: str = "WP-001",
    title: str = "Tablet press qualification",
) -> dict:
    return {
        "wp_id": wp_id,
        "title": title,
        "status": "open",
        "selector_context": {
            "preset_id": "oral-solid-dose-standard",
            "scope_intent": "qualification-only",
            "standards_bundles": ["cqv-core", "automation"],
        },
    }


def make_generated_task_plan_payload(task_id: str) -> dict:
    return {
        "task_id": task_id,
        "sequence_order": 1,
        "duration_days": 1,
        "dependency_task_ids": [],
        "planned_start_at": "2026-04-13T08:30:00+00:00",
        "planned_finish_at": "2026-04-13T16:30:00+00:00",
    }


def test_wp_delete_rejects_delete_when_collections_are_still_bound_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
        "work_packages": [
            {
                "wp_id": "WP-001",
                "title": "Tablet press qualification",
                "status": "open",
            },
            {
                "wp_id": "WP-002",
                "title": "Blister line upgrade",
                "status": "open",
            },
        ],
        "task_collections": [
            {
                "collection_id": "TC-001",
                "title": "Committed Selection",
                "collection_state": "committed",
                "work_package_id": "WP-001",
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert (
        "Work Package cannot be deleted while collections are bound: "
        "WP-001 -> [TC-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_wp_delete_rejects_delete_when_plans_are_still_associated_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
            make_bound_context_work_package_payload("WP-002", "Blister line upgrade"),
        ],
        "task_collections": [],
        "plans": [
            {
                "plan_id": "PLAN-001",
                "work_package_id": "WP-001",
                "plan_state": "draft",
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert (
        "Work Package cannot be deleted while plans are associated: "
        "WP-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_clear_work_package_rejects_when_plans_still_reference_task_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [
            {
                "task_id": "TASK-001",
                "order": 1,
                "title": "Prepare FAT",
                "description": None,
                "owner": None,
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "prepare-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": [],
            }
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
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
                    make_generated_task_plan_payload("TASK-001")
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "clear-work-package", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task work package cannot be cleared while plans still reference it: "
        "TASK-001 -> [PLAN-001 (WP-001)]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_delete_rejects_when_generated_plan_still_references_task_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [
            {
                "task_id": "TASK-001",
                "order": 1,
                "title": "Prepare FAT",
                "description": None,
                "owner": None,
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "prepare-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": [],
            }
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
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
                    make_generated_task_plan_payload("TASK-001")
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task cannot be deleted while plans still reference it: "
        "TASK-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_delete_rejects_when_plan_dependencies_still_reference_task_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [
            {
                "task_id": "TASK-001",
                "order": 1,
                "title": "Prepare FAT",
                "description": None,
                "owner": None,
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "prepare-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": [],
            },
            {
                "task_id": "TASK-002",
                "order": 2,
                "title": "Execute FAT",
                "description": None,
                "owner": None,
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "execute-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": ["TASK-001"],
            },
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
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
                        "dependency_task_ids": ["TASK-001"],
                        "planned_start_at": "2026-04-15T08:30:00+00:00",
                        "planned_finish_at": "2026-04-15T16:30:00+00:00",
                    },
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task cannot be deleted while plans still reference it: "
        "TASK-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state
''',
    encoding="utf-8",
)

print("Applied M8.5C patch files.")
