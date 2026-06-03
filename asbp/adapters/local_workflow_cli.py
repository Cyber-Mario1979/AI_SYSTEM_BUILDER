"""CLI-enhanced local workflow adapter for M32.3/M32.4."""

from __future__ import annotations

import argparse
import json

from pydantic import ValidationError

import asbp.state_store as state_store
from asbp.local_workflow_input_logic import configure_local_workflow_inputs
from asbp.local_workflow_logic import build_local_workflow_plan_payload
from asbp.state_model import StateModel


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="asbp-local-workflow")
    subparsers = parser.add_subparsers(dest="command")

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

    return parser


def _load_state_or_report() -> StateModel | None:
    try:
        return state_store.load_validated_state(state_store.get_state_file_path())
    except FileNotFoundError:
        print(f"State file not found: {state_store.get_state_file_path()}")
        print("No state file found. Run 'state init' first.")
        return None
    except ValidationError as exc:
        print("State validation failed:")
        print(exc)
        return None
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in state file: {exc}")
        return None
    except ValueError as exc:
        print("State validation failed:")
        print(exc)
        return None


def handle_plan(args: argparse.Namespace) -> None:
    state = _load_state_or_report()
    if state is None:
        return

    try:
        payload = build_local_workflow_plan_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        print(str(exc))
        return

    print(json.dumps(payload, indent=2))


def handle_configure(args: argparse.Namespace) -> None:
    state = _load_state_or_report()
    if state is None:
        return

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
        print(str(exc))
        return

    state_store.save_validated_state_to_path(state, state_store.get_state_file_path())
    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in {"plan", "configure"}:
        args.func(args)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
