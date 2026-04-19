from pathlib import Path

ROOT = Path.cwd()


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding='utf-8')


def replace_once(path: Path, old: str, new: str) -> None:
    text = read_text(path)
    if old not in text:
        raise RuntimeError(f'Expected snippet not found in {path}')
    write_text(path, text.replace(old, new, 1))


prompt_contract_logic = '''from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

PROMPT_CONTRACT_ID = "work_package_runtime_prompt_contract_v1"

REQUIRED_INPUT_FIELDS: list[str] = [
    "wp_id",
    "runtime_boundary_state",
    "eligible_for_prompt_contract",
    "selected_plan_id",
    "deterministic_facts.work_package_status",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.blocking_conditions",
    "deterministic_facts.next_actions",
    "deterministic_facts.selector_context_ready",
    "deterministic_facts.work_package_task_ids",
    "deterministic_facts.bound_committed_collection_ids",
    "deterministic_facts.bound_committed_task_ids",
    "deterministic_facts.plan_ids",
]

EXPECTED_OUTPUT_FIELDS: list[str] = [
    "response_mode",
    "operator_message",
    "recommended_next_actions",
    "grounded_input_fields_used",
]

PROHIBITED_FREEFORM_DRIFT: list[str] = [
    "omit required output fields",
    "add output fields outside the declared contract",
    "invent facts outside the validated deterministic inputs",
    "change or reinterpret blocking conditions",
    "change selected plan, task scope, or collection scope",
    "propose state mutation as if it already occurred",
]


def build_work_package_prompt_contract_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    runtime_boundary_payload = build_work_package_runtime_boundary_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if runtime_boundary_payload is None:
        return None

    prompt_contract_ready = runtime_boundary_payload["eligible_for_prompt_contract"]

    return {
        "wp_id": runtime_boundary_payload["wp_id"],
        "prompt_contract_id": PROMPT_CONTRACT_ID,
        "prompt_contract_state": (
            "ready"
            if prompt_contract_ready
            else "blocked"
        ),
        "prompt_contract_mode": (
            "execution_ready_summary"
            if prompt_contract_ready
            else "blocked_explainer"
        ),
        "eligible_for_prompt_contract": prompt_contract_ready,
        "required_input_fields": list(REQUIRED_INPUT_FIELDS),
        "expected_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "prohibited_freeform_drift": list(PROHIBITED_FREEFORM_DRIFT),
        "runtime_boundary": runtime_boundary_payload,
    }
'''

test_prompt_contract_logic = '''from datetime import datetime, timezone

from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload
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


def test_prompt_contract_returns_none_for_missing_work_package():
    payload = build_work_package_prompt_contract_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_prompt_contract_reports_blocked_contract_mode_when_runtime_boundary_is_blocked():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_prompt_contract_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload["wp_id"] == "WP-001"
    assert payload["prompt_contract_id"] == "work_package_runtime_prompt_contract_v1"
    assert payload["prompt_contract_state"] == "blocked"
    assert payload["prompt_contract_mode"] == "blocked_explainer"
    assert payload["eligible_for_prompt_contract"] is False
    assert payload["required_input_fields"] == [
        "wp_id",
        "runtime_boundary_state",
        "eligible_for_prompt_contract",
        "selected_plan_id",
        "deterministic_facts.work_package_status",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
        "deterministic_facts.selector_context_ready",
        "deterministic_facts.work_package_task_ids",
        "deterministic_facts.bound_committed_collection_ids",
        "deterministic_facts.bound_committed_task_ids",
        "deterministic_facts.plan_ids",
    ]
    assert payload["expected_output_fields"] == [
        "response_mode",
        "operator_message",
        "recommended_next_actions",
        "grounded_input_fields_used",
    ]
    assert payload["runtime_boundary"]["runtime_boundary_state"] == "deterministic_blocked"
    assert payload["runtime_boundary"]["deterministic_facts"]["orchestration_stage"] == "binding_context_required"


def test_prompt_contract_reports_ready_contract_mode_when_runtime_boundary_is_execution_ready():
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

    payload = build_work_package_prompt_contract_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload["wp_id"] == "WP-001"
    assert payload["prompt_contract_state"] == "ready"
    assert payload["prompt_contract_mode"] == "execution_ready_summary"
    assert payload["eligible_for_prompt_contract"] is True
    assert payload["runtime_boundary"]["runtime_boundary_state"] == "eligible_for_prompt_contract"
    assert payload["runtime_boundary"]["selected_plan_id"] == "PLAN-001"
'''

test_prompt_contract_cli = '''import json
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


def test_runtime_prompt_contract_wp_cli_returns_prompt_contract_payload(
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

    result = run_cli("runtime", "prompt-contract-wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["wp_id"] == "WP-001"
    assert payload["prompt_contract_id"] == "work_package_runtime_prompt_contract_v1"
    assert payload["prompt_contract_state"] == "blocked"


def test_runtime_prompt_contract_wp_cli_reports_missing_work_package(
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
                "work_packages": [],
                "task_collections": [],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("runtime", "prompt-contract-wp", "WP-404")

    assert result.returncode == 0
    assert result.stdout.strip() == "Work Package not found: WP-404"
'''

write_text(ROOT / 'asbp' / 'prompt_contract_logic.py', prompt_contract_logic)
write_text(ROOT / 'tests' / 'test_prompt_contract_logic.py', test_prompt_contract_logic)
write_text(ROOT / 'tests' / 'test_prompt_contract_cli.py', test_prompt_contract_cli)

cli_path = ROOT / 'asbp' / 'cli.py'

replace_once(
    cli_path,
    "from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload\n",
    "from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload\n"
    "from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload\n",
)

replace_once(
    cli_path,
    '''def handle_runtime_wp(args):
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
    '''def handle_runtime_wp(args):
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


def handle_runtime_prompt_contract_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    payload = build_work_package_prompt_contract_payload(
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
    '''    runtime_wp_parser = runtime_subparsers.add_parser(
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
    '''    runtime_wp_parser = runtime_subparsers.add_parser(
        "wp",
        help="Show Work Package runtime boundary payload",
    )
    runtime_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for runtime boundary inspection",
    )
    runtime_wp_parser.set_defaults(func=handle_runtime_wp)

    runtime_prompt_contract_wp_parser = runtime_subparsers.add_parser(
        "prompt-contract-wp",
        help="Show Work Package prompt contract foundation payload",
    )
    runtime_prompt_contract_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for prompt contract inspection",
    )
    runtime_prompt_contract_wp_parser.set_defaults(
        func=handle_runtime_prompt_contract_wp
    )

    task_parser = subparsers.add_parser("task", help="Task operations")
''',
)

print('M9.2 patch applied.')
