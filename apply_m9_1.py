from pathlib import Path

ROOT = Path.cwd()


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def replace_once(path: Path, old: str, new: str) -> None:
    text = read_text(path)
    if old not in text:
        raise RuntimeError(f'Expected snippet not found in {path}')
    write_text(path, text.replace(old, new, 1))


runtime_boundary_logic = '''from asbp.orchestration_logic import build_work_package_orchestration_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

MODEL_MAY: list[str] = [
    "consume only validated deterministic facts exposed through this boundary payload",
    "transform those facts into bounded language outputs only after a future prompt contract is defined",
    "return only fields explicitly requested by a future runtime contract",
]

MODEL_MAY_NOT: list[str] = [
    "mutate persisted state",
    "invent facts, statuses, dates, dependencies, or identifiers",
    "change selected work package, selected plan, task scope, or collection scope",
    "resolve blocked deterministic state by inference",
    "bypass deterministic validation or acceptance rules",
]


def build_work_package_runtime_boundary_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    orchestration_payload = build_work_package_orchestration_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if orchestration_payload is None:
        return None

    orchestration_stage = orchestration_payload["orchestration_stage"]
    eligible_for_prompt_contract = orchestration_stage == "execution_ready"

    return {
        "wp_id": orchestration_payload["wp_id"],
        "runtime_boundary_state": (
            "eligible_for_prompt_contract"
            if eligible_for_prompt_contract
            else "deterministic_blocked"
        ),
        "eligible_for_prompt_contract": eligible_for_prompt_contract,
        "selected_plan_id": orchestration_payload["selected_plan_id"],
        "deterministic_facts": {
            "work_package_status": orchestration_payload["work_package_status"],
            "orchestration_stage": orchestration_stage,
            "blocking_conditions": list(orchestration_payload["blocking_conditions"]),
            "next_actions": list(orchestration_payload["next_actions"]),
            "selector_context_ready": orchestration_payload["selector_context_ready"],
            "work_package_task_ids": list(orchestration_payload["work_package_task_ids"]),
            "bound_committed_collection_ids": list(
                orchestration_payload["bound_committed_collection_ids"]
            ),
            "bound_committed_task_ids": list(
                orchestration_payload["bound_committed_task_ids"]
            ),
            "plan_ids": list(orchestration_payload["plan_ids"]),
        },
        "model_may": list(MODEL_MAY),
        "model_may_not": list(MODEL_MAY_NOT),
    }
'''


test_runtime_boundary_logic = '''from datetime import datetime, timezone

from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
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


def test_runtime_boundary_returns_none_for_missing_work_package():
    payload = build_work_package_runtime_boundary_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_runtime_boundary_reports_deterministic_blocked_when_orchestration_is_not_execution_ready():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_runtime_boundary_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
        "runtime_boundary_state": "deterministic_blocked",
        "eligible_for_prompt_contract": False,
        "selected_plan_id": None,
        "deterministic_facts": {
            "work_package_status": "open",
            "orchestration_stage": "binding_context_required",
            "blocking_conditions": ["selector_context_missing"],
            "next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "selector_context_ready": False,
            "work_package_task_ids": [],
            "bound_committed_collection_ids": [],
            "bound_committed_task_ids": [],
            "plan_ids": [],
        },
        "model_may": [
            "consume only validated deterministic facts exposed through this boundary payload",
            "transform those facts into bounded language outputs only after a future prompt contract is defined",
            "return only fields explicitly requested by a future runtime contract",
        ],
        "model_may_not": [
            "mutate persisted state",
            "invent facts, statuses, dates, dependencies, or identifiers",
            "change selected work package, selected plan, task scope, or collection scope",
            "resolve blocked deterministic state by inference",
            "bypass deterministic validation or acceptance rules",
        ],
    }


def test_runtime_boundary_reports_prompt_contract_eligibility_when_execution_ready():
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

    payload = build_work_package_runtime_boundary_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
        "runtime_boundary_state": "eligible_for_prompt_contract",
        "eligible_for_prompt_contract": True,
        "selected_plan_id": "PLAN-001",
        "deterministic_facts": {
            "work_package_status": "open",
            "orchestration_stage": "execution_ready",
            "blocking_conditions": [],
            "next_actions": [
                "Execution-ready deterministic state reached."
            ],
            "selector_context_ready": True,
            "work_package_task_ids": ["TASK-001"],
            "bound_committed_collection_ids": ["TC-001"],
            "bound_committed_task_ids": ["TASK-001"],
            "plan_ids": ["PLAN-001"],
        },
        "model_may": [
            "consume only validated deterministic facts exposed through this boundary payload",
            "transform those facts into bounded language outputs only after a future prompt contract is defined",
            "return only fields explicitly requested by a future runtime contract",
        ],
        "model_may_not": [
            "mutate persisted state",
            "invent facts, statuses, dates, dependencies, or identifiers",
            "change selected work package, selected plan, task scope, or collection scope",
            "resolve blocked deterministic state by inference",
            "bypass deterministic validation or acceptance rules",
        ],
    }
'''


test_runtime_boundary_cli = '''import json
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


def test_runtime_wp_cli_returns_runtime_boundary_payload_for_existing_work_package(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
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
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("runtime", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["wp_id"] == "WP-001"
    assert payload["runtime_boundary_state"] == "deterministic_blocked"
    assert payload["eligible_for_prompt_contract"] is False


def test_runtime_wp_cli_reports_missing_work_package(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("runtime", "wp", "WP-404")

    assert result.returncode == 0
    assert result.stdout.strip() == "Work Package not found: WP-404"
'''

write_text(ROOT / 'asbp' / 'runtime_boundary_logic.py', runtime_boundary_logic)
write_text(ROOT / 'tests' / 'test_runtime_boundary_logic.py', test_runtime_boundary_logic)
write_text(ROOT / 'tests' / 'test_runtime_boundary_cli.py', test_runtime_boundary_cli)

cli_path = ROOT / 'asbp' / 'cli.py'

replace_once(
    cli_path,
    'from asbp.orchestration_logic import build_work_package_orchestration_payload\n',
    'from asbp.orchestration_logic import build_work_package_orchestration_payload\n'
    'from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload\n',
)

replace_once(
    cli_path,
    '''def handle_orchestrate_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    payload = build_work_package_orchestration_payload(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))
''',
    '''def handle_orchestrate_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    payload = build_work_package_orchestration_payload(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))


def handle_runtime_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    payload = build_work_package_runtime_boundary_payload(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))
''',
)

replace_once(
    cli_path,
    '''    orchestrate_wp_parser = orchestrate_subparsers.add_parser(
        "wp",
        help="Show deterministic Work Package orchestration state",
    )
    orchestrate_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID to orchestrate",
    )
    orchestrate_wp_parser.set_defaults(func=handle_orchestrate_wp)

    task_parser = subparsers.add_parser("task", help="Task operations")
''',
    '''    orchestrate_wp_parser = orchestrate_subparsers.add_parser(
        "wp",
        help="Show deterministic Work Package orchestration state",
    )
    orchestrate_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID to orchestrate",
    )
    orchestrate_wp_parser.set_defaults(func=handle_orchestrate_wp)

    runtime_parser = subparsers.add_parser(
        "runtime",
        help="Runtime boundary definition surfaces",
    )
    runtime_subparsers = runtime_parser.add_subparsers(dest="runtime_command")

    runtime_wp_parser = runtime_subparsers.add_parser(
        "wp",
        help="Show Work Package runtime boundary payload",
    )
    runtime_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for runtime boundary inspection",
    )
    runtime_wp_parser.set_defaults(func=handle_runtime_wp)

    task_parser = subparsers.add_parser("task", help="Task operations")
''',
)

replace_once(
    cli_path,
    '''    if args.command == "orchestrate" and args.orchestrate_command is None:
        parser.parse_args(["orchestrate", "-h"])
        return

    if args.command == "task" and args.task_command is None:
''',
    '''    if args.command == "orchestrate" and args.orchestrate_command is None:
        parser.parse_args(["orchestrate", "-h"])
        return

    if args.command == "runtime" and args.runtime_command is None:
        parser.parse_args(["runtime", "-h"])
        return

    if args.command == "task" and args.task_command is None:
''',
)

print('M9.1 patch applied.')
