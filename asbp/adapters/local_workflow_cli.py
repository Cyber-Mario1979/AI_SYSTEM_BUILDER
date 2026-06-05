"""CLI-enhanced local workflow adapter for M32.3/M32.4/M32.5/M32.6/M32.7/M32.8/M33.6."""

from __future__ import annotations

import argparse
import json

from pydantic import ValidationError

import asbp.state_store as state_store
from asbp.local_workflow_failure_logic import (
    build_invalid_reference_failure_payload,
    build_invalid_state_failure_payload,
    build_missing_input_failure_payload,
    build_missing_state_failure_payload,
)
from asbp.local_workflow_input_logic import configure_local_workflow_inputs
from asbp.local_workflow_logic import build_local_workflow_plan_payload
from asbp.local_workflow_output_logic import build_local_workflow_output_payload
from asbp.local_workflow_scenario_logic import (
    build_empty_local_workflow_scenario_state,
    stage_local_workflow_scenario,
)
from asbp.local_workflow_trial_summary_logic import (
    build_local_workflow_trial_summary_payload,
)
from asbp.local_workflow_visibility_logic import build_local_workflow_visibility_payload
from asbp.state_model import StateModel


def _print_payload(payload: dict) -> None:
    print(json.dumps(payload, indent=2))


class LocalWorkflowArgumentParser(argparse.ArgumentParser):
    """Argument parser that reports local workflow input failures safely."""

    def error(self, message: str) -> None:
        _print_payload(
            build_missing_input_failure_payload(
                command=self.prog,
                message=message,
            )
        )
        raise SystemExit(2)


def build_parser() -> argparse.ArgumentParser:
    parser = LocalWorkflowArgumentParser(prog="asbp-local-workflow")
    subparsers = parser.add_subparsers(
        dest="command",
        parser_class=LocalWorkflowArgumentParser,
    )

    scenario_parser = subparsers.add_parser(
        "scenario",
        help="Stage an approved end-to-end local workflow scenario",
    )
    scenario_parser.add_argument(
        "--scenario-id",
        required=True,
        choices=["cleanroom-hvac-qualification-basic"],
        help="Approved local workflow scenario ID to stage",
    )
    scenario_parser.set_defaults(func=handle_scenario)

    plan_parser = subparsers.add_parser(
        "plan",
        help="Show a read-only local workflow planning payload",
    )
    plan_parser.add_argument(
        "--wp-id",
        required=True,
        help="Work Package ID to use as the local workflow anchor",
    )
    plan_parser.set_defaults(func=handle_plan)

    configure_parser = subparsers.add_parser(
        "configure",
        help="Apply controlled local workflow input selections",
    )
    configure_parser.add_argument(
        "--wp-id",
        required=True,
        help="Work Package ID to configure",
    )
    configure_parser.add_argument(
        "--system-type",
        required=True,
        choices=["cleanroom-hvac", "automation"],
        help="Controlled system/profile type selection",
    )
    configure_parser.add_argument(
        "--preset-id",
        required=True,
        choices=[
            "cqv-cleanroom-hvac-basic",
            "cqv-automation-basic",
        ],
        help="Controlled preset/profile selection",
    )
    configure_parser.add_argument(
        "--scope-intent",
        required=True,
        choices=[
            "end-to-end",
            "qualification-only",
            "commissioning-only",
            "periodic-verification",
            "post-change",
            "post-deviation",
        ],
        help="Controlled workflow scope intent",
    )
    configure_parser.add_argument(
        "--standards-bundle",
        action="append",
        choices=["cleanroom-hvac", "automation"],
        default=[],
        help=(
            "Optional add-on standards bundle. cqv-core is always included "
            "as the baseline bundle. Repeat for multiple add-on bundles."
        ),
    )
    configure_parser.set_defaults(func=handle_configure)

    status_parser = subparsers.add_parser(
        "status",
        help="Show read-only workflow visibility state and limitations",
    )
    status_parser.add_argument(
        "--wp-id",
        required=True,
        help="Work Package ID to use as the local workflow visibility anchor",
    )
    status_parser.set_defaults(func=handle_status)

    outputs_parser = subparsers.add_parser(
        "outputs",
        help="Show read-only output review/access state and limitations",
    )
    outputs_parser.add_argument(
        "--wp-id",
        required=True,
        help="Work Package ID to use as the local output review anchor",
    )
    outputs_parser.set_defaults(func=handle_outputs)

    trial_summary_parser = subparsers.add_parser(
        "trial-summary",
        help="Show a compact read-only local workflow trial summary",
    )
    trial_summary_parser.add_argument(
        "--wp-id",
        required=True,
        help="Work Package ID to use as the local trial summary anchor",
    )
    trial_summary_parser.set_defaults(func=handle_trial_summary)

    return parser


def _load_state_or_report(command: str) -> StateModel | None:
    state_file_path = state_store.get_state_file_path()

    try:
        return state_store.load_validated_state(state_file_path)
    except FileNotFoundError:
        _print_payload(
            build_missing_state_failure_payload(
                command=command,
                state_file_path=state_file_path,
            )
        )
        return None
    except ValidationError as exc:
        _print_payload(
            build_invalid_state_failure_payload(
                command=command,
                message="State validation failed.",
                detail=str(exc),
            )
        )
        return None
    except json.JSONDecodeError as exc:
        _print_payload(
            build_invalid_state_failure_payload(
                command=command,
                message=f"Invalid JSON in state file: {exc}",
                detail="State file must contain valid JSON before local workflow commands can continue.",
            )
        )
        return None
    except ValueError as exc:
        _print_payload(
            build_invalid_state_failure_payload(
                command=command,
                message="State validation failed.",
                detail=str(exc),
            )
        )
        return None


def _load_or_initialize_state_for_scenario() -> StateModel:
    try:
        return state_store.load_validated_state(state_store.get_state_file_path())
    except FileNotFoundError:
        return build_empty_local_workflow_scenario_state()


def handle_scenario(args: argparse.Namespace) -> int:
    try:
        state = _load_or_initialize_state_for_scenario()
        payload = stage_local_workflow_scenario(
            state,
            scenario_id=args.scenario_id,
        )
    except ValidationError as exc:
        _print_payload(
            build_invalid_state_failure_payload(
                command=args.command,
                message="State validation failed.",
                detail=str(exc),
            )
        )
        return 1
    except json.JSONDecodeError as exc:
        _print_payload(
            build_invalid_state_failure_payload(
                command=args.command,
                message=f"Invalid JSON in state file: {exc}",
                detail="State file must contain valid JSON before local workflow scenario staging can continue.",
            )
        )
        return 1
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    state_store.save_validated_state_to_path(state, state_store.get_state_file_path())
    _print_payload(payload)
    return 0


def handle_plan(args: argparse.Namespace) -> int:
    state = _load_state_or_report(args.command)
    if state is None:
        return 1

    try:
        payload = build_local_workflow_plan_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    _print_payload(payload)
    return 0


def handle_configure(args: argparse.Namespace) -> int:
    state = _load_state_or_report(args.command)
    if state is None:
        return 1

    try:
        payload = configure_local_workflow_inputs(
            state,
            wp_id=args.wp_id,
            system_type=args.system_type,
            preset_id=args.preset_id,
            scope_intent=args.scope_intent,
            standards_bundle_ids=args.standards_bundle,
        )
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    state_store.save_validated_state_to_path(state, state_store.get_state_file_path())
    _print_payload(payload)
    return 0


def handle_status(args: argparse.Namespace) -> int:
    state = _load_state_or_report(args.command)
    if state is None:
        return 1

    try:
        payload = build_local_workflow_visibility_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    _print_payload(payload)
    return 0


def handle_outputs(args: argparse.Namespace) -> int:
    state = _load_state_or_report(args.command)
    if state is None:
        return 1

    try:
        payload = build_local_workflow_output_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    _print_payload(payload)
    return 0


def handle_trial_summary(args: argparse.Namespace) -> int:
    state = _load_state_or_report(args.command)
    if state is None:
        return 1

    try:
        payload = build_local_workflow_trial_summary_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        _print_payload(
            build_invalid_reference_failure_payload(
                command=args.command,
                message=str(exc),
            )
        )
        return 1

    _print_payload(payload)
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    handler = getattr(args, "func", None)
    if handler is None:
        _print_payload(
            build_missing_input_failure_payload(
                command=args.command,
                message="No local workflow command supplied.",
            )
        )
        return 2

    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
