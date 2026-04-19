from pathlib import Path

ROOT = Path.cwd()


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding='utf-8')


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f'Expected snippet not found in {path}')
    write(path, text.replace(old, new, 1))


def insert_after(path: Path, anchor: str, insertion: str) -> None:
    text = read(path)
    if insertion.strip() in text:
        return
    if anchor not in text:
        raise RuntimeError(f'Anchor not found in {path}')
    write(path, text.replace(anchor, anchor + insertion, 1))


orchestration_logic = '''from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def _find_work_package_by_id(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
) -> WorkPackageModel | None:
    for work_package in work_packages:
        if work_package.wp_id == wp_id:
            return work_package
    return None


def _build_bound_committed_collections(
    task_collections: list[TaskCollectionModel],
    *,
    wp_id: str,
) -> list[TaskCollectionModel]:
    return [
        task_collection
        for task_collection in task_collections
        if task_collection.collection_state == "committed"
        and task_collection.work_package_id == wp_id
    ]


def _build_committed_task_ids(
    task_collections: list[TaskCollectionModel],
) -> list[str]:
    committed_task_ids: set[str] = set()
    for task_collection in task_collections:
        committed_task_ids.update(task_collection.task_ids)
    return sorted(committed_task_ids)


def _build_work_package_task_ids(
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> list[str]:
    return sorted(
        task.task_id
        for task in tasks
        if task.work_package_id == wp_id
    )


def _build_work_package_plans(
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> list[PlanningModel]:
    return [
        plan
        for plan in plans
        if plan.work_package_id == wp_id
    ]


def _build_binding_context_blockers(
    work_package: WorkPackageModel,
) -> list[str]:
    selector_context = work_package.selector_context
    if selector_context is None:
        return ["selector_context_missing"]

    blockers: list[str] = []
    if selector_context.scope_intent is None:
        blockers.append("scope_intent_missing")
    if not selector_context.standards_bundles:
        blockers.append("standards_bundles_missing")
    return blockers


def build_work_package_orchestration_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    work_package = _find_work_package_by_id(work_packages, wp_id=wp_id)
    if work_package is None:
        return None

    binding_context_blockers = _build_binding_context_blockers(work_package)
    bound_committed_collections = _build_bound_committed_collections(
        task_collections,
        wp_id=wp_id,
    )
    bound_committed_collection_ids = [
        task_collection.collection_id
        for task_collection in bound_committed_collections
    ]
    bound_committed_task_ids = _build_committed_task_ids(
        bound_committed_collections,
    )
    work_package_task_ids = _build_work_package_task_ids(tasks, wp_id=wp_id)
    work_package_plans = _build_work_package_plans(plans, wp_id=wp_id)
    plan_ids = [plan.plan_id for plan in work_package_plans]

    payload = {
        "wp_id": work_package.wp_id,
        "work_package_status": work_package.status,
        "orchestration_stage": "",
        "blocking_conditions": [],
        "next_actions": [],
        "selector_context_ready": not binding_context_blockers,
        "work_package_task_ids": work_package_task_ids,
        "bound_committed_collection_ids": bound_committed_collection_ids,
        "bound_committed_task_ids": bound_committed_task_ids,
        "plan_ids": plan_ids,
        "selected_plan_id": None,
    }

    if binding_context_blockers:
        payload["orchestration_stage"] = "binding_context_required"
        payload["blocking_conditions"] = binding_context_blockers
        payload["next_actions"] = [
            "Complete deterministic selector context before orchestration can proceed."
        ]
        return payload

    if not bound_committed_collection_ids:
        payload["orchestration_stage"] = "selection_required"
        payload["blocking_conditions"] = ["bound_committed_collection_missing"]
        payload["next_actions"] = [
            "Bind at least one committed collection to the Work Package."
        ]
        return payload

    if not bound_committed_task_ids:
        payload["orchestration_stage"] = "selection_required"
        payload["blocking_conditions"] = ["committed_task_scope_empty"]
        payload["next_actions"] = [
            "Add committed task membership before planning orchestration can proceed."
        ]
        return payload

    committed_plans = [
        plan
        for plan in work_package_plans
        if plan.plan_state == "committed"
    ]
    draft_plans = [
        plan
        for plan in work_package_plans
        if plan.plan_state == "draft"
    ]

    if len(committed_plans) > 1:
        payload["orchestration_stage"] = "blocked"
        payload["blocking_conditions"] = ["multiple_committed_plans"]
        payload["next_actions"] = [
            "Reduce the Work Package to one committed plan before orchestration can continue."
        ]
        return payload

    if not committed_plans and len(draft_plans) > 1:
        payload["orchestration_stage"] = "blocked"
        payload["blocking_conditions"] = ["multiple_draft_plans"]
        payload["next_actions"] = [
            "Reduce the Work Package to one draft plan before orchestration can continue."
        ]
        return payload

    if committed_plans:
        selected_plan = committed_plans[0]
        payload["selected_plan_id"] = selected_plan.plan_id
        payload["orchestration_stage"] = "execution_ready"
        payload["next_actions"] = [
            "Execution-ready deterministic state reached."
        ]
        return payload

    if not draft_plans:
        payload["orchestration_stage"] = "planning_setup_required"
        payload["blocking_conditions"] = ["draft_plan_missing"]
        payload["next_actions"] = [
            "Create one draft plan for the Work Package."
        ]
        return payload

    selected_plan = draft_plans[0]
    payload["selected_plan_id"] = selected_plan.plan_id

    planning_setup_blockers: list[str] = []
    if selected_plan.planning_basis is None:
        planning_setup_blockers.append("planning_basis_missing")
    if selected_plan.planned_start_at is None:
        planning_setup_blockers.append("planned_start_at_missing")
    if selected_plan.planning_calendar is None:
        planning_setup_blockers.append("planning_calendar_missing")

    if planning_setup_blockers:
        payload["orchestration_stage"] = "planning_setup_required"
        payload["blocking_conditions"] = planning_setup_blockers
        payload["next_actions"] = [
            "Complete planning basis, planned start, and planning calendar on the selected draft plan."
        ]
        return payload

    if not selected_plan.generated_task_plans:
        payload["orchestration_stage"] = "plan_generation_required"
        payload["next_actions"] = [
            "Generate baseline task plan from committed task scope."
        ]
        return payload

    payload["orchestration_stage"] = "plan_commit_required"
    payload["next_actions"] = [
        "Commit the generated draft plan."
    ]
    return payload
'''

write(ROOT / 'asbp' / 'orchestration_logic.py', orchestration_logic)

cli_path = ROOT / 'asbp' / 'cli.py'
insert_after(
    cli_path,
    'from asbp.work_package_logic import (\n'
    '    build_work_package_task_ids,\n'
    '    clear_task_work_package,\n'
    '    create_work_package,\n'
    '    delete_work_package_by_id,\n'
    '    filter_work_packages,\n'
    '    find_work_package_by_id,\n'
    '    set_work_package_preset,\n'
    '    set_work_package_scope_intent,\n'
    '    set_work_package_selector_type,\n'
    '    set_work_package_standards_bundles,\n'
    '    update_work_package_status,\n'
    '    update_work_package_title,\n'
    '    set_task_work_package,\n'
    ')\n',
    'from asbp.orchestration_logic import build_work_package_orchestration_payload\n',
)

insert_after(
    cli_path,
    'def handle_collection_clear_work_package(args):\n'
    '    state = load_state_or_none()\n\n'
    '    if state is None:\n'
    '        print("No state file found. Run \'state init\' first.")\n'
    '        return\n\n'
    '    collection = clear_collection_work_package(\n'
    '        state.task_collections,\n'
    '        collection_id=args.collection_id,\n'
    '    )\n'
    '    if collection is None:\n'
    '        print(f"Collection not found: {args.collection_id}")\n'
    '        return\n\n'
    '    save_validated_state(state)\n'
    '    print(f"Collection work package cleared: {collection.collection_id}")\n\n',
    '\n'
    'def handle_orchestrate_wp(args):\n'
    '    state = load_state_or_none()\n\n'
    '    if state is None:\n'
    '        print("No state file found. Run \'state init\' first.")\n'
    '        return\n\n'
    '    payload = build_work_package_orchestration_payload(\n'
    '        state.work_packages,\n'
    '        state.task_collections,\n'
    '        state.tasks,\n'
    '        state.plans,\n'
    '        wp_id=args.wp_id,\n'
    '    )\n'
    '    if payload is None:\n'
    '        print(f"Work Package not found: {args.wp_id}")\n'
    '        return\n\n'
    '    print(json.dumps(payload, indent=2))\n\n',
)

insert_after(
    cli_path,
    '    collection_remove_task_parser.set_defaults(func=handle_collection_remove_task)\n\n',
    '    orchestrate_parser = subparsers.add_parser(\n'
    '        "orchestrate",\n'
    '        help="Deterministic orchestration surfaces",\n'
    '    )\n'
    '    orchestrate_subparsers = orchestrate_parser.add_subparsers(\n'
    '        dest="orchestrate_command"\n'
    '    )\n\n'
    '    orchestrate_wp_parser = orchestrate_subparsers.add_parser(\n'
    '        "wp",\n'
    '        help="Show deterministic Work Package orchestration state",\n'
    '    )\n'
    '    orchestrate_wp_parser.add_argument(\n'
    '        "wp_id",\n'
    '        help="Work Package ID to orchestrate",\n'
    '    )\n'
    '    orchestrate_wp_parser.set_defaults(func=handle_orchestrate_wp)\n\n',
)

replace_once(
    cli_path,
    '    if args.command == "collection" and args.collection_command is None:\n'
    '        parser.parse_args(["collection", "-h"])\n'
    '        return\n\n'
    '    if args.command == "task" and args.task_command is None:\n',
    '    if args.command == "collection" and args.collection_command is None:\n'
    '        parser.parse_args(["collection", "-h"])\n'
    '        return\n\n'
    '    if args.command == "orchestrate" and args.orchestrate_command is None:\n'
    '        parser.parse_args(["orchestrate", "-h"])\n'
    '        return\n\n'
    '    if args.command == "task" and args.task_command is None:\n',
)

test_text = '''import json
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


def test_orchestrate_wp_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_orchestrate_wp_handles_missing_work_package_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_orchestrate_wp_reports_binding_context_required(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
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
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "binding_context_required"
    assert payload["blocking_conditions"] == ["selector_context_missing"]
    assert payload["selector_context_ready"] is False


def test_orchestrate_wp_reports_selection_required_when_no_bound_committed_collection_exists(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "selection_required"
    assert payload["blocking_conditions"] == ["bound_committed_collection_missing"]
    assert payload["bound_committed_collection_ids"] == []


def test_orchestrate_wp_reports_planning_setup_required_when_no_plan_exists(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "planning_setup_required"
    assert payload["blocking_conditions"] == ["draft_plan_missing"]
    assert payload["bound_committed_task_ids"] == ["TASK-001"]


def test_orchestrate_wp_reports_plan_generation_required_for_ready_draft_plan(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
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
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "plan_generation_required"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_reports_plan_commit_required_for_generated_draft_plan(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
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
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "plan_commit_required"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_reports_execution_ready_for_committed_plan(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
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
                        "generated_task_plans": [
                            make_generated_task_plan_payload("TASK-001")
                        ],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "execution_ready"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_blocks_on_multiple_draft_plans(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "plans": [
                    {
                        "plan_id": "PLAN-001",
                        "work_package_id": "WP-001",
                        "plan_state": "draft",
                    },
                    {
                        "plan_id": "PLAN-002",
                        "work_package_id": "WP-001",
                        "plan_state": "draft",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "blocked"
    assert payload["blocking_conditions"] == ["multiple_draft_plans"]
'''

write(ROOT / 'tests' / 'test_orchestration_cli.py', test_text)

print('Applied M8.6 patch files.')
