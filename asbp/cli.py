import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from asbp.state_model import StateModel, TaskModel
from asbp.task_logic import generate_next_task_id

VERSION = "0.1.0"


def get_state_file_path() -> Path:
    return Path("data/state/state.json")


def load_raw_state() -> dict:
    state_file = get_state_file_path()

    if not state_file.exists():
        raise FileNotFoundError(f"State file not found: {state_file}")

    with state_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_validated_state() -> StateModel:
    raw_state = load_raw_state()
    return StateModel(**raw_state)


def save_validated_state(state: StateModel) -> None:
    state_file = get_state_file_path()
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as f:
        json.dump(state.model_dump(), f, indent=2)


def handle_state_init(args):
    state_file = get_state_file_path()
    state_file.parent.mkdir(parents=True, exist_ok=True)

    initial_state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.1.0",
        status="not_started",
    )

    save_validated_state(initial_state)
    print(f"State initialized at: {state_file}")


def load_state_or_none() -> StateModel | None:
    try:
        return load_validated_state()
    except FileNotFoundError as e:
        print(e)
        return None
    except ValidationError as e:
        print("State validation failed:")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in state file: {e}")
        return None


def handle_state_show(args):
    state = load_state_or_none()
    if state is None:
        return

    print(json.dumps(state.model_dump(), indent=2))


def update_state_field(field_name: str, new_value: str) -> bool:
    state = load_state_or_none()
    if state is None:
        return False

    setattr(state, field_name, new_value)
    save_validated_state(state)
    return True


def handle_state_set_version(args):
    success = update_state_field("version", args.value)
    if not success:
        return

    print(f"State version updated to: {args.value}")


def handle_state_set_status(args):
    success = update_state_field("status", args.value)
    if not success:
        return

    print(f"State status updated to: {args.value}")

def handle_task_add(args):
    state = load_state_or_none()
    if state is None:
        return

    next_task_id = generate_next_task_id(state.tasks)

    new_task = TaskModel(
        task_id=next_task_id,
        title=args.title,
        status="planned",
    )

    state.tasks.append(new_task)
    save_validated_state(state)

    print(f"Task added: {new_task.task_id} - {new_task.title}")    
    
def build_parser():
    parser = argparse.ArgumentParser(prog="asbp")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command")

    state_parser = subparsers.add_parser("state", help="State file operations")
    state_subparsers = state_parser.add_subparsers(dest="state_command")

    state_init_parser = state_subparsers.add_parser("init", help="Initialize the state file")
    state_init_parser.set_defaults(func=handle_state_init)

    state_show_parser = state_subparsers.add_parser("show", help="Show current state")
    state_show_parser.set_defaults(func=handle_state_show)

    state_set_version_parser = state_subparsers.add_parser("set-version", help="Set state version")
    state_set_version_parser.add_argument("value", help="New version value")
    state_set_version_parser.set_defaults(func=handle_state_set_version)

    state_set_status_parser = state_subparsers.add_parser("set-status", help="Set state status")
    state_set_status_parser.add_argument(
        "value",
        choices=["not_started", "in_flight", "completed"],
        help="New status value",
    )
    state_set_status_parser.set_defaults(func=handle_state_set_status)

    task_parser = subparsers.add_parser("task", help="Task operations")
    task_subparsers = task_parser.add_subparsers(dest="task_command")

    task_add_parser = task_subparsers.add_parser("add", help="Add a new task")
    task_add_parser.add_argument("title", help="Task title")
    task_add_parser.set_defaults(func=handle_task_add)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "state" and args.state_command is None:
        parser.parse_args(["state", "-h"])
        return

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
