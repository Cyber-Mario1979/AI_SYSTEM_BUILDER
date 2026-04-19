from pathlib import Path

ROOT = Path.cwd()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read_text(path)
    if old not in text:
        raise RuntimeError(f"Expected snippet not found in {path}")
    write_text(path, text.replace(old, new, 1))


retry_fail_logic = '''from asbp.output_validation_logic import validate_work_package_candidate_response
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def evaluate_work_package_candidate_response_attempt(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: dict,
    attempt_number: int,
    max_attempts: int,
) -> dict | None:
    validation_payload = validate_work_package_candidate_response(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
    )
    if validation_payload is None:
        return None

    decision_rationale: list[str] = []
    validation_state = validation_payload["validation_state"]

    if max_attempts < 1:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:max_attempts_must_be_positive")
    elif attempt_number < 1:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:attempt_number_must_be_positive")
    elif attempt_number > max_attempts:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:attempt_number_exceeds_max_attempts")
    elif validation_state == "accepted":
        decision_state = "accepted"
        fallback_action = "use_validated_output"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append("validated_output_accepted")
    elif attempt_number < max_attempts:
        decision_state = "retry_allowed"
        fallback_action = "request_new_candidate_from_same_handoff_contract"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append("validation_rejected_but_retry_budget_remaining")
    else:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("validation_rejected_and_retry_budget_exhausted")

    return {
        "wp_id": validation_payload["wp_id"],
        "handoff_contract_id": validation_payload["handoff_contract_id"],
        "validation_state": validation_state,
        "decision_state": decision_state,
        "fallback_action": fallback_action,
        "retry_policy": {
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "retries_remaining": retries_remaining,
        },
        "decision_rationale": decision_rationale,
        "validation_errors": list(validation_payload["errors"]),
        "validated_output": validation_payload["validated_output"],
    }
'''

test_retry_fail_logic = '''from datetime import datetime, timezone

from asbp.retry_fail_logic import evaluate_work_package_candidate_response_attempt
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


def test_retry_fail_returns_none_for_missing_work_package():
    payload = evaluate_work_package_candidate_response_attempt(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
        candidate_output={},
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is None


def test_retry_fail_accepts_valid_candidate_output():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "blocked_explainer",
            "operator_message": "Selector context is still required.",
            "recommended_next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.next_actions",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload["validation_state"] == "accepted"
    assert payload["decision_state"] == "accepted"
    assert payload["fallback_action"] == "use_validated_output"
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == ["validated_output_accepted"]


def test_retry_fail_allows_retry_when_validation_rejects_and_budget_remains():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": "not-a-list",
            "grounded_input_fields_used": [
                "wp_id",
                "disallowed.field",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload["validation_state"] == "rejected"
    assert payload["decision_state"] == "retry_allowed"
    assert payload["fallback_action"] == "request_new_candidate_from_same_handoff_contract"
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_but_retry_budget_remaining"
    ]


def test_retry_fail_closes_when_validation_rejects_and_budget_is_exhausted():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": "not-a-list",
            "grounded_input_fields_used": [
                "wp_id",
                "disallowed.field",
            ],
        },
        attempt_number=2,
        max_attempts=2,
    )

    assert payload["validation_state"] == "rejected"
    assert payload["decision_state"] == "fail_closed"
    assert payload["fallback_action"] == "return_deterministic_rejection_without_acceptance"
    assert payload["retry_policy"] == {
        "attempt_number": 2,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_and_retry_budget_exhausted"
    ]


def test_retry_fail_closes_on_invalid_retry_control_state():
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

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "The work package is ready for generation.",
            "recommended_next_actions": [
                "Execution-ready deterministic state reached."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "selected_plan_id",
                "deterministic_facts.orchestration_stage",
            ],
        },
        attempt_number=3,
        max_attempts=2,
    )

    assert payload["validation_state"] == "accepted"
    assert payload["decision_state"] == "fail_closed"
    assert payload["fallback_action"] == "return_deterministic_rejection_without_acceptance"
    assert payload["retry_policy"] == {
        "attempt_number": 3,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
    ]
'''

test_retry_fail_cli = '''import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"
CANDIDATE_FILE = REPO_ROOT / "data" / "state" / "candidate_response.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def restore_files():
    state_exists = STATE_FILE.exists()
    state_text = STATE_FILE.read_text(encoding="utf-8") if state_exists else None
    candidate_exists = CANDIDATE_FILE.exists()
    candidate_text = (
        CANDIDATE_FILE.read_text(encoding="utf-8")
        if candidate_exists
        else None
    )

    yield

    if state_exists and state_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(state_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()

    if candidate_exists and candidate_text is not None:
        CANDIDATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CANDIDATE_FILE.write_text(candidate_text, encoding="utf-8")
    elif CANDIDATE_FILE.exists():
        CANDIDATE_FILE.unlink()


def test_runtime_decide_response_wp_cli_returns_retry_decision_payload(
    restore_files,
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
    CANDIDATE_FILE.write_text(
        json.dumps(
            {
                "response_mode": "blocked_explainer",
                "operator_message": "Selector context is still required.",
                "recommended_next_actions": [
                    "Complete deterministic selector context before orchestration can proceed."
                ],
                "grounded_input_fields_used": [
                    "wp_id",
                    "deterministic_facts.orchestration_stage",
                    "deterministic_facts.next_actions",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "runtime",
        "decide-response-wp",
        "WP-001",
        str(CANDIDATE_FILE),
        "1",
        "2",
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["wp_id"] == "WP-001"
    assert payload["decision_state"] == "accepted"


def test_runtime_decide_response_wp_cli_reports_missing_work_package(
    restore_files,
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
    CANDIDATE_FILE.write_text(
        json.dumps(
            {
                "response_mode": "blocked_explainer",
                "operator_message": "Selector context is still required.",
                "recommended_next_actions": [
                    "Complete deterministic selector context before orchestration can proceed."
                ],
                "grounded_input_fields_used": [
                    "wp_id",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "runtime",
        "decide-response-wp",
        "WP-404",
        str(CANDIDATE_FILE),
        "1",
        "2",
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Work Package not found: WP-404"
'''

write_text(ROOT / "asbp" / "retry_fail_logic.py", retry_fail_logic)
write_text(ROOT / "tests" / "test_retry_fail_logic.py", test_retry_fail_logic)
write_text(ROOT / "tests" / "test_retry_fail_cli.py", test_retry_fail_cli)

cli_path = ROOT / "asbp" / "cli.py"

replace_once(
    cli_path,
    'from asbp.output_validation_logic import (\n    load_candidate_response_json,\n    validate_work_package_candidate_response,\n)\n',
    'from asbp.output_validation_logic import (\n    load_candidate_response_json,\n    validate_work_package_candidate_response,\n)\n'
    'from asbp.retry_fail_logic import evaluate_work_package_candidate_response_attempt\n',
)

replace_once(
    cli_path,
    '''def handle_runtime_validate_response_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        candidate_output = load_candidate_response_json(
            Path(args.candidate_json_path)
        )
    except FileNotFoundError:
        print(f"Candidate response file not found: {args.candidate_json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in candidate response file: {e}")
        return
    except ValueError as e:
        print(str(e))
        return

    payload = validate_work_package_candidate_response(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
        candidate_output=candidate_output,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))
''',
    '''def handle_runtime_validate_response_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        candidate_output = load_candidate_response_json(
            Path(args.candidate_json_path)
        )
    except FileNotFoundError:
        print(f"Candidate response file not found: {args.candidate_json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in candidate response file: {e}")
        return
    except ValueError as e:
        print(str(e))
        return

    payload = validate_work_package_candidate_response(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
        candidate_output=candidate_output,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))


def handle_runtime_decide_response_wp(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        candidate_output = load_candidate_response_json(
            Path(args.candidate_json_path)
        )
    except FileNotFoundError:
        print(f"Candidate response file not found: {args.candidate_json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in candidate response file: {e}")
        return
    except ValueError as e:
        print(str(e))
        return

    payload = evaluate_work_package_candidate_response_attempt(
        state.work_packages,
        state.task_collections,
        state.tasks,
        state.plans,
        wp_id=args.wp_id,
        candidate_output=candidate_output,
        attempt_number=args.attempt_number,
        max_attempts=args.max_attempts,
    )
    if payload is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    print(json.dumps(payload, indent=2))
''',
)

replace_once(
    cli_path,
    '''    runtime_validate_response_wp_parser = runtime_subparsers.add_parser(
        "validate-response-wp",
        help="Validate candidate generated response against the Work Package handoff contract",
    )
    runtime_validate_response_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for validation",
    )
    runtime_validate_response_wp_parser.add_argument(
        "candidate_json_path",
        help="Path to candidate response JSON file",
    )
    runtime_validate_response_wp_parser.set_defaults(
        func=handle_runtime_validate_response_wp
    )

    task_parser = subparsers.add_parser("task", help="Task operations")
''',
    '''    runtime_validate_response_wp_parser = runtime_subparsers.add_parser(
        "validate-response-wp",
        help="Validate candidate generated response against the Work Package handoff contract",
    )
    runtime_validate_response_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for validation",
    )
    runtime_validate_response_wp_parser.add_argument(
        "candidate_json_path",
        help="Path to candidate response JSON file",
    )
    runtime_validate_response_wp_parser.set_defaults(
        func=handle_runtime_validate_response_wp
    )

    runtime_decide_response_wp_parser = runtime_subparsers.add_parser(
        "decide-response-wp",
        help="Apply retry / fail decision rules to candidate generated response",
    )
    runtime_decide_response_wp_parser.add_argument(
        "wp_id",
        help="Work Package ID for retry / fail decision",
    )
    runtime_decide_response_wp_parser.add_argument(
        "candidate_json_path",
        help="Path to candidate response JSON file",
    )
    runtime_decide_response_wp_parser.add_argument(
        "attempt_number",
        type=int,
        help="Current candidate attempt number (1-based)",
    )
    runtime_decide_response_wp_parser.add_argument(
        "max_attempts",
        type=int,
        help="Maximum allowed candidate attempts",
    )
    runtime_decide_response_wp_parser.set_defaults(
        func=handle_runtime_decide_response_wp
    )

    task_parser = subparsers.add_parser("task", help="Task operations")
''',
)

print("M9.5 patch applied.")
