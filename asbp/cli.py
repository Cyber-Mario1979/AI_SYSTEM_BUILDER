import argparse
import json
from pathlib import Path
from pydantic import ValidationError

from asbp.state_model import StateModel, TaskModel
from asbp.task_logic import (
    build_dependent_reference_view,
    build_dependency_reference_view,
    delete_task_by_id,
    filter_tasks,
    filter_tasks_by_status,
    find_task_by_id,
    find_task_by_reference,
    generate_next_task_id,
    generate_next_task_order,
    normalize_task_key,
    prepare_task_key_for_write,
    set_task_dependencies,
    update_task_status,
    validate_persisted_task_keys,
    
)

VERSION = "0.1.0"


def get_state_file_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "state" / "state.json"


def load_raw_state(state_file_path: Path) -> dict:
    with state_file_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    for task in raw.get("tasks", []):
        if "dependencies" not in task:
            task["dependencies"] = []

    return raw


def load_validated_state(state_file_path: Path) -> StateModel:
    raw_state = load_raw_state(state_file_path)
    for task in raw_state.get("tasks", []):
        task.setdefault("description", None)
        task.setdefault("owner", None)
        task.setdefault("duration", None)
        task.setdefault("start_date", None)
        task.setdefault("end_date", None)
        task.setdefault("task_key", None)

    state = StateModel(**raw_state)
    validate_persisted_task_keys(state.tasks)
    return state


def save_validated_state(state: StateModel) -> None:
    state_file = get_state_file_path()
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as f:
        json.dump(state.model_dump(), f, indent=2)
        f.write("\n")


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
    state_file = get_state_file_path()

    try:
        return load_validated_state(state_file)
    except FileNotFoundError:
        print(f"State file not found: {state_file}")
        return None
    except ValidationError as e:
        print("State validation failed:")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in state file: {e}")
        return None
    except ValueError as e:
        print("State validation failed:")
        print(e)
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

    try:
        task_key = prepare_task_key_for_write(
            state.tasks,
            getattr(args, "task_key", None),
        )
    except ValueError as e:
        print(str(e))
        return

    next_task_id = generate_next_task_id(state.tasks)

    new_task = TaskModel(
        task_id=next_task_id,
        order=generate_next_task_order(state.tasks),
        title=args.title,
        description=args.description,
        owner=args.owner,
        duration=args.duration,
        start_date=args.start_date,
        end_date=args.end_date,
        task_key=task_key,
        status="planned",
)

    state.tasks.append(new_task)
    save_validated_state(state)

    print(f"Task added: {new_task.task_id} - {new_task.title}")

def handle_task_list(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    tasks = [task.model_dump() for task in state.tasks]

    has_dependencies = None
    if args.has_dependencies == "true":
        has_dependencies = True
    elif args.has_dependencies == "false":
        has_dependencies = False

    has_task_key = None
    if args.has_task_key == "true":
        has_task_key = True
    elif args.has_task_key == "false":
        has_task_key = False

    normalized_task_key_filter = None
    if args.task_key is not None:
        normalized_task_key_filter = normalize_task_key(args.task_key)

    resolved_task_id_filter = None
    if args.task_ref is not None:
        try:
            target_task = find_task_by_reference(state.tasks, args.task_ref)
        except ValueError as e:
            print(str(e))
            return

        if target_task is None:
            tasks = []
        else:
            resolved_task_id_filter = target_task.task_id

    resolved_dependency_task_id_filter = None
    if args.dependency_ref is not None:
        try:
            dependency_task = find_task_by_reference(state.tasks, args.dependency_ref)
        except ValueError as e:
            print(str(e))
            return

        if dependency_task is None:
            tasks = []
        else:
            resolved_dependency_task_id_filter = dependency_task.task_id

    if args.task_key is not None and normalized_task_key_filter is None:
        tasks = []
    else:
        tasks = filter_tasks(
            tasks,
            status=args.status,
            has_dependencies=has_dependencies,
            has_task_key=has_task_key,
            task_key=normalized_task_key_filter,
            task_id=resolved_task_id_filter,
            dependency_task_id=resolved_dependency_task_id_filter,
        )

    if not tasks:
        print("No tasks found.")
        return

    print("Tasks:")
    for task in tasks:
        line_parts = [f'- {task["task_id"]}', task["status"]]

        if args.show_task_key:
            task_key_display = normalize_task_key(task.get("task_key")) or "<none>"
            line_parts.append(f"task_key={task_key_display}")

        if args.show_dependency_refs:
            dependency_refs = build_dependency_reference_view(
                state.tasks,
                task.get("dependencies", []),
            )

            if dependency_refs:
                dependency_refs_display = ", ".join(
                    f'{dependency_ref["task_id"]}:{dependency_ref["task_key"]}'
                    for dependency_ref in dependency_refs
                )
                line_parts.append(f"dependency_refs=[{dependency_refs_display}]")
            else:
                line_parts.append("dependency_refs=[]")

        line_parts.append(task["title"])
        print(" | ".join(line_parts))

def handle_task_update_status(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print(str(e))
        return

    if target_task is None:
        print(f"Task not found: {args.task_id}")
        return

    update_task_status(state.tasks, target_task.task_id, args.status)
    save_validated_state(state)
    print(f"Task status updated: {target_task.task_id} -> {args.status}")


def handle_task_delete(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print(str(e))
        return

    if target_task is None:
        print(f"Task not found: {args.task_id}")
        return

    updated_tasks, deleted_flag = delete_task_by_id(state.tasks, target_task.task_id)

    if not deleted_flag:
        print(f"Task not found: {args.task_id}")
        return

    state.tasks = updated_tasks
    save_validated_state(state)
    print(f"Task deleted: {target_task.task_id}")

def handle_task_show(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print(str(e))
        return

    if task is None:
        print(f"Task not found: {args.task_id}")
        return

    task_payload = task.model_dump()

    if args.show_dependency_refs:
        task_payload["dependency_refs"] = build_dependency_reference_view(
            state.tasks,
            task_payload["dependencies"],
        )
    if args.show_dependent_refs:
        task_payload["dependent_refs"] = build_dependent_reference_view(
            state.tasks,
            task.task_id,
        )

    print(json.dumps(task_payload, indent=2))


def handle_task_set_key(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print(str(e))
        return

    if target_task is None:
        print(f"Task not found: {args.task_id}")
        return

    try:
        normalized_task_key = prepare_task_key_for_write(
            state.tasks,
            args.task_key,
            current_task_id=target_task.task_id,
        )
    except ValueError as e:
        print(str(e))
        return

    target_task.task_key = normalized_task_key
    save_validated_state(state)
    print(f"Task key updated: {target_task.task_id} -> {normalized_task_key}")


def handle_task_clear_key(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print(str(e))
        return

    if target_task is None:
        print(f"Task not found: {args.task_id}")
        return

    target_task.task_key = None
    save_validated_state(state)
    print(f"Task key cleared: {target_task.task_id}")
    
def handle_task_set_dependencies(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task = find_task_by_reference(state.tasks, args.task_id)
    except ValueError as e:
        print("Dependency validation failed:")
        print(f"- {str(e)}")
        return

    if target_task is None:
        print("Dependency validation failed:")
        print(f"- Task not found: {args.task_id}")
        return

    resolved_dependency_ids = []
    dependency_resolution_errors = []

    for dependency_ref in args.dependencies:
        try:
            dependency_task = find_task_by_reference(state.tasks, dependency_ref)
        except ValueError as e:
            dependency_resolution_errors.append(str(e))
            continue

        if dependency_task is None:
            dependency_resolution_errors.append(
                f"Dependency task not found: {dependency_ref}"
            )
            continue

        resolved_dependency_ids.append(dependency_task.task_id)

    _updated_task, validation_errors = set_task_dependencies(
        state.tasks,
        target_task.task_id,
        resolved_dependency_ids,
    )

    all_errors = dependency_resolution_errors + validation_errors

    if all_errors:
        print("Dependency validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return

    save_validated_state(state)
    print(
        f"Task dependencies updated: {target_task.task_id} -> {resolved_dependency_ids}"
    )

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
    task_add_parser.add_argument("--description", default=None, help="Optional task description")
    task_add_parser.add_argument("--owner", default=None, help="Optional task owner")
    task_add_parser.add_argument("--duration", type=int, default=None, help="Optional task duration in days")
    task_add_parser.add_argument("--start-date", default=None, help="Optional task start date")
    task_add_parser.add_argument("--end-date", default=None, help="Optional task end date")
    task_add_parser.add_argument("--task-key", default=None, help="Optional deterministic task key")
    task_add_parser.set_defaults(func=handle_task_add)

    task_list_parser = task_subparsers.add_parser("list", help="List all tasks")
    task_list_parser.add_argument(
        "--status",
        choices=["planned", "in_progress", "completed", "over_due"],
        help="Filter tasks by status",
    )
    task_list_parser.add_argument(
        "--has-dependencies",
        choices=["true", "false"],
        help="Filter tasks by whether dependencies exist",
    )
    task_list_parser.add_argument(
        "--show-task-key",
        action="store_true",
        help="Show task_key in list output",
    )
    task_list_parser.add_argument(
        "--show-dependency-refs",
        action="store_true",
        help="Show resolved dependency references in list output",
    )
    task_list_parser.add_argument(
        "--has-task-key",
        choices=["true", "false"],
        help="Filter tasks by whether task_key exists",
    )
    task_list_parser.add_argument(
        "--task-key",
        default=None,
        help="Filter tasks by exact normalized task_key",
    )
    task_list_parser.set_defaults(func=handle_task_list)

    task_show_parser = task_subparsers.add_parser("show", help="Show a task by ID")
    task_show_parser.add_argument("task_id", help="Task ID to show")
    task_show_parser.add_argument(
        "--show-dependency-refs",
        action="store_true",
        help="Show resolved dependency references in task output",
    )
    task_show_parser.set_defaults(func=handle_task_show)   

    task_show_parser.add_argument(
        "--show-dependent-refs",
        action="store_true",
        help="Show resolved dependent references in task output",
    )

    task_set_key_parser = task_subparsers.add_parser(
        "set-key",
        help="Set task key",
    )
    task_set_key_parser.add_argument("task_id", help="Task ID to update")
    task_set_key_parser.add_argument("task_key", help="New deterministic task key")
    task_set_key_parser.set_defaults(func=handle_task_set_key)

    task_clear_key_parser = task_subparsers.add_parser(
        "clear-key",
        help="Clear task key",
    )
    task_clear_key_parser.add_argument("task_id", help="Task ID to update")
    task_clear_key_parser.set_defaults(func=handle_task_clear_key)

    task_update_status_parser = task_subparsers.add_parser("update-status", help="Update task status")
    task_update_status_parser.add_argument("task_id", help="Task ID to update")
    task_update_status_parser.add_argument(
    "status",
    choices=["planned", "in_progress", "completed", "over_due"],
    help="New task status",
)
    task_update_status_parser.set_defaults(func=handle_task_update_status)
    task_set_dependencies_parser = task_subparsers.add_parser(
        "set-dependencies",
        help="Set task dependencies",
    )
    task_set_dependencies_parser.add_argument("task_id", help="Task ID to update")
    task_set_dependencies_parser.add_argument(
        "dependencies",
        nargs="*",
        help="Dependency task IDs",
    )
    task_list_parser.add_argument(
        "--task-ref",
        default=None,
        help="Filter tasks by exact task reference (task_id first, task_key second)",
    )    
    task_list_parser.add_argument(
        "--dependency-ref",
        default=None,
        help="Filter tasks by one dependency reference (task_id first, task_key second)",
    )
    task_set_dependencies_parser.set_defaults(func=handle_task_set_dependencies)

    task_delete_parser = task_subparsers.add_parser("delete", help="Delete a task")
    task_delete_parser.add_argument("task_id", help="Task ID to delete")
    task_delete_parser.set_defaults(func=handle_task_delete)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "state" and args.state_command is None:
        parser.parse_args(["state", "-h"])
        return

    if args.command == "task" and args.task_command is None:
        parser.parse_args(["task", "-h"])
        return

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()




