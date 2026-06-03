"""CLI-enhanced local workflow adapter for M32.3."""

from __future__ import annotations

import argparse
import json

from pydantic import ValidationError

import asbp.state_store as state_store
from asbp.local_workflow_logic import build_local_workflow_plan_payload


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

    return parser


def handle_plan(args: argparse.Namespace) -> None:
    try:
        state = state_store.load_validated_state(state_store.get_state_file_path())
    except FileNotFoundError:
        print(f"State file not found: {state_store.get_state_file_path()}")
        print("No state file found. Run 'state init' first.")
        return
    except ValidationError as exc:
        print("State validation failed:")
        print(exc)
        return
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in state file: {exc}")
        return
    except ValueError as exc:
        print("State validation failed:")
        print(exc)
        return

    try:
        payload = build_local_workflow_plan_payload(state, wp_id=args.wp_id)
    except ValueError as exc:
        print(str(exc))
        return

    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "plan":
        args.func(args)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
