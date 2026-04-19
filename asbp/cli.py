import argparse
import json
from pathlib import Path

from pydantic import ValidationError

import asbp.state_store as state_store

from asbp.state_model import StateModel, TaskModel, WorkPackageModel
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
from asbp.collection_logic import (
    add_task_to_collection,
    build_task_collection_ids,
    build_work_package_collection_ids,
    clear_collection_work_package,
    create_collection,
    filter_collections,
    find_collection_by_id,
    remove_task_from_collection,
    set_collection_work_package,
    update_collection_state,
    update_collection_title,
    validate_task_delete_membership,
)
from asbp.work_package_logic import (
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
from asbp.orchestration_logic import build_work_package_orchestration_payload
from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.planning_logic import validate_task_plan_membership_delete

VERSION = "0.1.0"


def get_state_file_path() -> Path:
    return state_store.get_state_file_path()


def load_raw_state(state_file_path: Path) -> dict:
    return state_store.load_raw_state(state_file_path)


def load_validated_state(state_file_path: Path) -> StateModel:
    return state_store.load_validated_state(state_file_path)


def save_validated_state(state: StateModel) -> None:
    state_store.save_validated_state_to_path(state, get_state_file_path())


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


def handle_wp_list(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    work_packages = filter_work_packages(
        state.work_packages,
        tasks=state.tasks,
        status=args.status,
        title=args.title,
        wp_id=args.wp_id,
        task_id=args.task_id,
    )

    if getattr(args, "collection_id", None) is not None:
        collection = find_collection_by_id(
            state.task_collections,
            args.collection_id,
        )
        if collection is None or collection.work_package_id is None:
            work_packages = []
        else:
            work_packages = [
                work_package
                for work_package in work_packages
                if work_package.wp_id == collection.work_package_id
            ]

    if not work_packages:
        print("No work packages found.")
        return

    print("Work Packages:")
    for work_package in work_packages:
        line_parts = [
            f"- {work_package.wp_id}",
            work_package.status,
        ]

        if getattr(args, "show_task_ids", False):
            task_ids = build_work_package_task_ids(
                state.tasks,
                wp_id=work_package.wp_id,
            )
            if task_ids:
                line_parts.append(f"task_ids=[{', '.join(task_ids)}]")
            else:
                line_parts.append("task_ids=[]")

        if getattr(args, "show_collection_ids", False):
            collection_ids = build_work_package_collection_ids(
                state.task_collections,
                wp_id=work_package.wp_id,
            )
            if collection_ids:
                line_parts.append(f"collection_ids=[{', '.join(collection_ids)}]")
            else:
                line_parts.append("collection_ids=[]")

        line_parts.append(work_package.title)
        print(" | ".join(line_parts))


def _normalize_selector_context_payload_for_output(
    selector_context: dict | None,
) -> dict | None:
    if selector_context is None:
        return None

    normalized_selector_context = {
        key: value
        for key, value in selector_context.items()
        if value is not None and value != []
    }
    return normalized_selector_context or None


def handle_wp_show(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    work_package = find_work_package_by_id(state.work_packages, args.wp_id)
    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    work_package_payload = work_package.model_dump()

    if getattr(args, "show_task_ids", False):
        work_package_payload["task_ids"] = build_work_package_task_ids(
            state.tasks,
            wp_id=work_package.wp_id,
        )

    if getattr(args, "show_collection_ids", False):
        work_package_payload["collection_ids"] = build_work_package_collection_ids(
            state.task_collections,
            wp_id=work_package.wp_id,
        )

    if getattr(args, "show_selector_context", False):
        work_package_payload["selector_context"] = (
            _normalize_selector_context_payload_for_output(
                work_package_payload.get("selector_context", None)
            )
        )
    else:
        work_package_payload.pop("selector_context", None)

    print(json.dumps(work_package_payload, indent=2))


def handle_wp_add(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        new_work_package = create_work_package(
            state.work_packages,
            wp_id=args.wp_id,
            title=args.title,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return
    except ValueError as e:
        print(str(e))
        return

    state.work_packages.append(new_work_package)
    save_validated_state(state)
    print(
        f"Work Package added: {new_work_package.wp_id} - "
        f"{new_work_package.title}"
    )


def handle_wp_update_status(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    work_package = update_work_package_status(
        state.work_packages,
        wp_id=args.wp_id,
        status=args.status,
    )
    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    save_validated_state(state)
    print(f"Work Package status updated: {work_package.wp_id} -> {args.status}")


def handle_wp_delete(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    updated_work_packages, deleted_flag, error_message = delete_work_package_by_id(
        state.work_packages,
        state.tasks,
        state.task_collections,
        state.plans,
        wp_id=args.wp_id,
    )

    if error_message is not None:
        print(error_message)
        return

    if not deleted_flag:
        print(f"Work Package not found: {args.wp_id}")
        return

    state.work_packages = updated_work_packages
    save_validated_state(state)
    print(f"Work Package deleted: {args.wp_id}")


def handle_wp_update_title(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        work_package = update_work_package_title(
            state.work_packages,
            wp_id=args.wp_id,
            title=args.title,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return

    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    save_validated_state(state)
    print(f"Work Package title updated: {work_package.wp_id} -> {work_package.title}")



def handle_wp_set_selector_type(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        work_package = set_work_package_selector_type(
            state.work_packages,
            wp_id=args.wp_id,
            system_type=args.system_type,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return

    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    assert work_package.selector_context is not None

    save_validated_state(state)
    print(
        f"Work Package selector type updated: "
        f"{work_package.wp_id} -> {work_package.selector_context.system_type}"
    )



def handle_wp_set_preset(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        work_package = set_work_package_preset(
            state.work_packages,
            wp_id=args.wp_id,
            preset_id=args.preset_id,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return

    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    assert work_package.selector_context is not None

    save_validated_state(state)
    print(
        f"Work Package preset updated: "
        f"{work_package.wp_id} -> {work_package.selector_context.preset_id}"
    )


def handle_wp_set_standards_bundles(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        work_package = set_work_package_standards_bundles(
            state.work_packages,
            wp_id=args.wp_id,
            add_on_bundle_ids=args.add_on_bundle_ids,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return
    except ValueError as e:
        print(str(e))
        return

    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    assert work_package.selector_context is not None

    save_validated_state(state)
    bundle_display = ", ".join(work_package.selector_context.standards_bundles)
    print(
        f"Work Package standards bundles updated: "
        f"{work_package.wp_id} -> [{bundle_display}]"
    )


def handle_wp_set_scope_intent(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        work_package = set_work_package_scope_intent(
            state.work_packages,
            wp_id=args.wp_id,
            scope_intent=args.scope_intent,
        )
    except ValidationError as e:
        print("Work Package validation failed:")
        print(e)
        return
    except ValueError as e:
        print(str(e))
        return

    if work_package is None:
        print(f"Work Package not found: {args.wp_id}")
        return

    assert work_package.selector_context is not None

    save_validated_state(state)
    print(
        f"Work Package scope intent updated: "
        f"{work_package.wp_id} -> {work_package.selector_context.scope_intent}"
    )


def handle_collection_add(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        new_collection = create_collection(
            state.task_collections,
            title=args.title,
            collection_state=args.collection_state,
        )
    except ValidationError as e:
        print("Collection validation failed:")
        print(e)
        return
    except ValueError as e:
        print(str(e))
        return

    state.task_collections.append(new_collection)
    save_validated_state(state)
    print(
        f"Collection added: {new_collection.collection_id} - "
        f"{new_collection.title} ({new_collection.collection_state})"
    )


def handle_collection_list(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    collections = filter_collections(
        state.task_collections,
        collection_state=args.collection_state,
        title=args.title,
        collection_id=args.collection_id,
        work_package_id=getattr(args, "work_package_id", None),
        task_id=getattr(args, "task_id", None),
    )

    if not collections:
        print("No collections found.")
        return

    print("Collections:")
    for collection in collections:
        line_parts = _build_collection_list_row_parts(
            collection,
            show_work_package_id=getattr(args, "show_work_package_id", False),
            show_task_ids=getattr(args, "show_task_ids", False),
        )
        print(" | ".join(line_parts))


def _build_collection_list_row_parts(
    collection,
    *,
    show_work_package_id: bool = False,
    show_task_ids: bool = False,
):
    line_parts = [
        f"- {collection.collection_id}",
        collection.collection_state,
    ]

    if show_work_package_id:
        work_package_id_display = collection.work_package_id or "<none>"
        line_parts.append(f"work_package_id={work_package_id_display}")

    if show_task_ids:
        if collection.task_ids:
            line_parts.append(f"task_ids=[{', '.join(collection.task_ids)}]")
        else:
            line_parts.append("task_ids=[]")

    line_parts.append(collection.title)
    return line_parts


def _prepare_collection_read_payload(
    collection,
    *,
    show_work_package_id: bool = False,
):
    payload = collection.model_dump()

    if show_work_package_id:
        payload["work_package_id"] = collection.work_package_id
    else:
        payload.pop("work_package_id", None)

    return payload


def handle_collection_show(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    collection = find_collection_by_id(
        state.task_collections,
        args.collection_id,
    )
    if collection is None:
        print(f"Collection not found: {args.collection_id}")
        return

    payload = _prepare_collection_read_payload(
        collection,
        show_work_package_id=getattr(args, "show_work_package_id", False),
    )
    print(json.dumps(payload, indent=2))


def handle_collection_add_task(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        collection, target_task, error_message = add_task_to_collection(
            state.tasks,
            state.task_collections,
            collection_id=args.collection_id,
            task_ref=args.task_ref,
        )
    except ValueError as e:
        print(str(e))
        return

    if error_message is not None:
        print(error_message)
        return

    if collection is None or target_task is None:
        return

    save_validated_state(state)
    print(f"Task added to collection: {collection.collection_id} <- {target_task.task_id}")


def handle_collection_remove_task(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        collection, target_task, error_message = remove_task_from_collection(
            state.tasks,
            state.task_collections,
            collection_id=args.collection_id,
            task_ref=args.task_ref,
        )
    except ValueError as e:
        print(str(e))
        return

    if error_message is not None:
        print(error_message)
        return

    if collection is None or target_task is None:
        return

    save_validated_state(state)
    print(
        f"Task removed from collection: "
        f"{collection.collection_id} <- {target_task.task_id}"
    )


def handle_collection_update_title(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        collection = update_collection_title(
            state.task_collections,
            collection_id=args.collection_id,
            title=args.title,
        )
    except ValidationError as e:
        print("Collection validation failed:")
        print(e)
        return

    if collection is None:
        print(f"Collection not found: {args.collection_id}")
        return

    save_validated_state(state)
    print(
        f"Collection title updated: "
        f"{collection.collection_id} -> {collection.title}"
    )


def handle_collection_update_state(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        collection = update_collection_state(
            state.task_collections,
            collection_id=args.collection_id,
            collection_state=args.collection_state,
        )
    except ValueError as e:
        print(str(e))
        return

    if collection is None:
        print(f"Collection not found: {args.collection_id}")
        return

    save_validated_state(state)
    print(
        f"Collection state updated: "
        f"{collection.collection_id} -> {collection.collection_state}"
    )

def handle_collection_set_work_package(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    try:
        collection, error_message = set_collection_work_package(
            state.tasks,
            state.task_collections,
            state.work_packages,
            collection_id=args.collection_id,
            wp_id=args.wp_id,
        )
    except ValueError as e:
        print(str(e))
        return

    if error_message is not None:
        print(error_message)
        return

    if collection is None:
        print(f"Collection not found: {args.collection_id}")
        return

    save_validated_state(state)
    print(
        f"Collection work package updated: "
        f"{collection.collection_id} -> {collection.work_package_id}"
    )


def handle_collection_clear_work_package(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    collection = clear_collection_work_package(
        state.task_collections,
        collection_id=args.collection_id,
    )
    if collection is None:
        print(f"Collection not found: {args.collection_id}")
        return

    save_validated_state(state)
    print(f"Collection work package cleared: {collection.collection_id}")


def handle_orchestrate_wp(args):
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
    

def _coerce_task_payload(task):
    if hasattr(task, "model_dump"):
        return task.model_dump()
    return dict(task)


def _reference_views_requested(
    *,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    return show_dependency_refs or show_dependent_refs


def _parse_optional_bool_filter(value):
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def _resolve_task_list_reference_filter_task_id(tasks, reference):
    if reference is None:
        return None, False

    target_task = find_task_by_reference(tasks, reference)
    if target_task is None:
        return None, True
    return target_task.task_id, False


def _prepare_task_list_reference_filters(
    tasks,
    *,
    task_ref=None,
    dependency_ref=None,
    dependent_ref=None,
):
    resolved_task_id_filter, task_ref_missing = (
        _resolve_task_list_reference_filter_task_id(tasks, task_ref)
    )
    resolved_dependency_task_id_filter, dependency_ref_missing = (
        _resolve_task_list_reference_filter_task_id(tasks, dependency_ref)
    )
    resolved_dependent_task_id_filter, dependent_ref_missing = (
        _resolve_task_list_reference_filter_task_id(tasks, dependent_ref)
    )

    return {
        "resolved_task_id_filter": resolved_task_id_filter,
        "resolved_dependency_task_id_filter": resolved_dependency_task_id_filter,
        "resolved_dependent_task_id_filter": resolved_dependent_task_id_filter,
        "should_return_no_tasks": (
            task_ref_missing
            or dependency_ref_missing
            or dependent_ref_missing
        ),
    }


def _attach_reference_views_to_task_payload(
    tasks,
    task_payload,
    *,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    if show_dependency_refs:
        task_payload["dependency_refs"] = build_dependency_reference_view(
            tasks,
            task_payload.get("dependencies", []),
        )

    if show_dependent_refs:
        task_payload["dependent_refs"] = build_dependent_reference_view(
            tasks,
            task_payload["task_id"],
        )

    return task_payload


def _format_reference_view_for_task_list(field_name, reference_view):
    if reference_view:
        reference_view_display = ", ".join(
            f'{reference["task_id"]}:{reference["task_key"]}'
            for reference in reference_view
        )
        return f"{field_name}=[{reference_view_display}]"

    return f"{field_name}=[]"


def _build_task_list_row_parts(
    task_payload,
    *,
    show_task_key=False,
    show_work_package_id=False,
    show_collection_ids=False,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    line_parts = [f'- {task_payload["task_id"]}', task_payload["status"]]

    if show_task_key:
        task_key_display = normalize_task_key(task_payload.get("task_key")) or "<none>"
        line_parts.append(f"task_key={task_key_display}")

    if show_work_package_id:
        work_package_id_display = task_payload.get("work_package_id") or "<none>"
        line_parts.append(f"work_package_id={work_package_id_display}")

    if show_collection_ids:
        collection_ids = task_payload.get("collection_ids", [])
        if collection_ids:
            line_parts.append(f"collection_ids=[{', '.join(collection_ids)}]")
        else:
            line_parts.append("collection_ids=[]")

    if show_dependency_refs:
        line_parts.append(
            _format_reference_view_for_task_list(
                "dependency_refs",
                task_payload["dependency_refs"],
            )
        )

    if show_dependent_refs:
        line_parts.append(
            _format_reference_view_for_task_list(
                "dependent_refs",
                task_payload["dependent_refs"],
            )
        )

    line_parts.append(task_payload["title"])
    return line_parts


def _prepare_task_list_filter_inputs(args, tasks):
    normalized_task_key_filter = None
    if args.task_key is not None:
        normalized_task_key_filter = normalize_task_key(args.task_key)

    resolved_reference_filters = _prepare_task_list_reference_filters(
        tasks,
        task_ref=args.task_ref,
        dependency_ref=args.dependency_ref,
        dependent_ref=args.dependent_ref,
    )

    return {
        "has_dependencies": _parse_optional_bool_filter(args.has_dependencies),
        "has_dependents": _parse_optional_bool_filter(args.has_dependents),
        "has_task_key": _parse_optional_bool_filter(args.has_task_key),
        "normalized_task_key_filter": normalized_task_key_filter,
        "resolved_task_id_filter": resolved_reference_filters["resolved_task_id_filter"],
        "resolved_dependency_task_id_filter": (
            resolved_reference_filters["resolved_dependency_task_id_filter"]
        ),
        "resolved_dependent_task_id_filter": (
            resolved_reference_filters["resolved_dependent_task_id_filter"]
        ),
        "should_return_no_tasks": resolved_reference_filters["should_return_no_tasks"],
        "task_key_filter_requested_and_invalid": (
            args.task_key is not None and normalized_task_key_filter is None
        ),
    }


def _prepare_reference_visibility_options(args):
    return {
        "show_collection_ids": getattr(args, "show_collection_ids", False),
        "show_dependency_refs": args.show_dependency_refs,
        "show_dependent_refs": args.show_dependent_refs,
    }

def _prepare_task_read_payload(
    tasks,
    task_collections,
    task,
    *,
    show_collection_ids=False,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    task_payload = _coerce_task_payload(task)

    if show_collection_ids:
        task_payload["collection_ids"] = build_task_collection_ids(
            task_collections,
            task_id=task_payload["task_id"],
        )

    if not _reference_views_requested(
        show_dependency_refs=show_dependency_refs,
        show_dependent_refs=show_dependent_refs,
    ):
        return task_payload

    return _attach_reference_views_to_task_payload(
        tasks,
        task_payload,
        show_dependency_refs=show_dependency_refs,
        show_dependent_refs=show_dependent_refs,
    )






def handle_task_list(args):
    state = load_state_or_none()

    if state is None:
        print("No state file found. Run 'state init' first.")
        return

    tasks = [task.model_dump() for task in state.tasks]

    try:
        prepared_filters = _prepare_task_list_filter_inputs(args, state.tasks)
    except ValueError as e:
        print(str(e))
        return

    if (
        prepared_filters["should_return_no_tasks"]
        or prepared_filters["task_key_filter_requested_and_invalid"]
    ):
        tasks = []
    else:
        tasks = filter_tasks(
            tasks,
            status=args.status,
            has_dependencies=prepared_filters["has_dependencies"],
            has_dependents=prepared_filters["has_dependents"],
            has_task_key=prepared_filters["has_task_key"],
            task_key=prepared_filters["normalized_task_key_filter"],
            task_id=prepared_filters["resolved_task_id_filter"],
            dependency_task_id=prepared_filters["resolved_dependency_task_id_filter"],
            dependent_task_id=prepared_filters["resolved_dependent_task_id_filter"],
            work_package_id=getattr(args, "work_package_id", None),
        )

    if getattr(args, "collection_id", None) is not None:
        collection = find_collection_by_id(
            state.task_collections,
            args.collection_id,
        )
        if collection is None:
            tasks = []
        else:
            collection_task_ids = set(collection.task_ids)
            tasks = [
                task
                for task in tasks
                if task.get("task_id") in collection_task_ids
            ]

    if not tasks:
        print("No tasks found.")
        return

    reference_visibility_options = _prepare_reference_visibility_options(args)
    print("Tasks:")
    for task in tasks:
        task_output = _prepare_task_read_payload(
            state.tasks,
            state.task_collections,
            task,
            **reference_visibility_options,
        )

        line_parts = _build_task_list_row_parts(
            task_output,
            show_task_key=args.show_task_key,
            show_work_package_id=args.show_work_package_id,
            **reference_visibility_options,
        )
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

    membership_error = validate_task_delete_membership(
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
    reference_visibility_options = _prepare_reference_visibility_options(args)
    task_payload = _prepare_task_read_payload(
        state.tasks,
        state.task_collections,
        task,
        **reference_visibility_options,
    )

    if getattr(args, "show_work_package_id", False):
        task_payload["work_package_id"] = task_payload.get("work_package_id", None)
    else:
        task_payload.pop("work_package_id", None)

    if not getattr(args, "show_collection_ids", False):
        task_payload.pop("collection_ids", None)

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


def handle_task_set_work_package(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task, error_message = set_task_work_package(
            state.tasks,
            state.work_packages,
            state.task_collections,
            task_ref=args.task_id,
            wp_id=args.wp_id,
        )
    except ValueError as e:
        print(str(e))
        return

    if error_message is not None:
        print(error_message)
        return

    if target_task is None:
        return

    save_validated_state(state)
    print(
        f"Task work package updated: "
        f"{target_task.task_id} -> {target_task.work_package_id}"
    )


def handle_task_clear_work_package(args):
    state = load_state_or_none()
    if state is None:
        return

    try:
        target_task, error_message = clear_task_work_package(
            state.tasks,
            state.task_collections,
            state.plans,
            task_ref=args.task_id,
        )
    except ValueError as e:
        print(str(e))
        return

    if error_message is not None:
        print(error_message)
        return

    if target_task is None:
        return

    save_validated_state(state)
    print(f"Task work package cleared: {target_task.task_id}")


def build_parser():
    parser = argparse.ArgumentParser(prog="asbp")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command")

    state_parser = subparsers.add_parser("state", help="State file operations")
    state_subparsers = state_parser.add_subparsers(dest="state_command")

    state_init_parser = state_subparsers.add_parser(
        "init",
        help="Initialize the state file",
    )
    state_init_parser.set_defaults(func=handle_state_init)

    state_show_parser = state_subparsers.add_parser(
        "show",
        help="Show current state",
    )
    state_show_parser.set_defaults(func=handle_state_show)

    state_set_version_parser = state_subparsers.add_parser(
        "set-version",
        help="Set state version",
    )
    state_set_version_parser.add_argument("value", help="New version value")
    state_set_version_parser.set_defaults(func=handle_state_set_version)

    state_set_status_parser = state_subparsers.add_parser(
        "set-status",
        help="Set state status",
    )
    state_set_status_parser.add_argument(
        "value",
        choices=["not_started", "in_flight", "completed"],
        help="New status value",
    )
    state_set_status_parser.set_defaults(func=handle_state_set_status)

    wp_parser = subparsers.add_parser("wp", help="Work Package operations")
    wp_subparsers = wp_parser.add_subparsers(dest="wp_command")


    wp_list_parser = wp_subparsers.add_parser("list", help="List all work packages")
    wp_list_parser.add_argument(
        "--status",
        choices=["open", "in_progress", "completed"],
        help="Filter work packages by status",
    )
    wp_list_parser.add_argument(
        "--title",
        help="Filter work packages by exact title",
    )
    wp_list_parser.add_argument(
        "--wp-id",
        help="Filter work packages by exact work package ID",
    )
    wp_list_parser.add_argument(
        "--task-id",
        help="Filter work packages by exact associated task_id",
    )
    wp_list_parser.add_argument(
        "--collection-id",
        help="Filter work packages by exact bound collection_id",
    )
    wp_list_parser.add_argument(
        "--show-task-ids",
        action="store_true",
        help="Show associated task_ids in list output",
    )
    wp_list_parser.add_argument(
        "--show-collection-ids",
        action="store_true",
        help="Show bound collection_ids in list output",
    )
    wp_list_parser.set_defaults(func=handle_wp_list)
    

    wp_show_parser = wp_subparsers.add_parser("show", help="Show a work package by ID")
    wp_show_parser.add_argument("wp_id", help="Work Package ID to show")
    wp_show_parser.add_argument(
        "--show-task-ids",
        action="store_true",
        help="Show associated task_ids in work package output",
    )
    wp_show_parser.add_argument(
        "--show-collection-ids",
        action="store_true",
        help="Show bound collection_ids in work package output",
    )
    wp_show_parser.add_argument(
        "--show-selector-context",
        action="store_true",
        help="Show selector_context in work package output",
    )
    wp_show_parser.set_defaults(func=handle_wp_show)

    wp_add_parser = wp_subparsers.add_parser("add", help="Add a new work package")
    wp_add_parser.add_argument("wp_id", help="Work Package ID to add")
    wp_add_parser.add_argument("title", help="Work Package title")
    wp_add_parser.set_defaults(func=handle_wp_add)

    wp_update_status_parser = wp_subparsers.add_parser(
        "update-status",
        help="Update work package status",
    )
    wp_update_status_parser.add_argument("wp_id", help="Work Package ID to update")
    wp_update_status_parser.add_argument(
        "status",
        choices=["open", "in_progress", "completed"],
        help="New work package status",
    )
    wp_update_status_parser.set_defaults(func=handle_wp_update_status)

    wp_delete_parser = wp_subparsers.add_parser(
        "delete",
        help="Delete a work package",
    )
    wp_delete_parser.add_argument("wp_id", help="Work Package ID to delete")
    wp_delete_parser.set_defaults(func=handle_wp_delete)

    wp_update_title_parser = wp_subparsers.add_parser(
        "update-title",
        help="Update work package title",
    )
    wp_update_title_parser.add_argument("wp_id", help="Work Package ID to update")
    wp_update_title_parser.add_argument("title", help="New work package title")
    wp_update_title_parser.set_defaults(func=handle_wp_update_title)


    wp_set_selector_type_parser = wp_subparsers.add_parser(
        "set-selector-type",
        help="Set work package selector system_type",
    )
    wp_set_selector_type_parser.add_argument(
        "wp_id",
        help="Work Package ID to update",
    )
    wp_set_selector_type_parser.add_argument(
        "system_type",
        help="Selector system_type value",
    )
    wp_set_selector_type_parser.set_defaults(func=handle_wp_set_selector_type)


    wp_set_preset_parser = wp_subparsers.add_parser(
        "set-preset",
        help="Set work package preset binding seed",
    )
    wp_set_preset_parser.add_argument(
        "wp_id",
        help="Work Package ID to update",
    )
    wp_set_preset_parser.add_argument(
        "preset_id",
        help="Preset binding seed value",
    )
    wp_set_preset_parser.set_defaults(func=handle_wp_set_preset)

    wp_set_standards_bundles_parser = wp_subparsers.add_parser(
        "set-standards-bundles",
        help="Set work package standards bundle binding",
    )
    wp_set_standards_bundles_parser.add_argument(
        "wp_id",
        help="Work Package ID to update",
    )
    wp_set_standards_bundles_parser.add_argument(
        "add_on_bundle_ids",
        nargs="*",
        choices=["cleanroom-hvac", "automation"],
        help=(
            "Optional add-on standards bundles; cqv-core is always included "
            "as the baseline bundle"
        ),
    )
    wp_set_standards_bundles_parser.set_defaults(
        func=handle_wp_set_standards_bundles
    )

    wp_set_scope_intent_parser = wp_subparsers.add_parser(
        "set-scope-intent",
        help="Set work package scope / intent selector value",
    )
    wp_set_scope_intent_parser.add_argument(
        "wp_id",
        help="Work Package ID to update",
    )
    wp_set_scope_intent_parser.add_argument(
        "scope_intent",
        choices=[
            "end-to-end",
            "qualification-only",
            "commissioning-only",
            "periodic-verification",
            "post-change",
            "post-deviation",
        ],
        help="Scope / intent selector value",
    )
    wp_set_scope_intent_parser.set_defaults(
        func=handle_wp_set_scope_intent
    )

    collection_parser = subparsers.add_parser("collection", help="Collection operations")
    collection_subparsers = collection_parser.add_subparsers(dest="collection_command")

    collection_list_parser = collection_subparsers.add_parser(
        "list",
        help="List all collections",
    )
    collection_list_parser.add_argument(
        "--collection-state",
        choices=["source", "staged", "committed", "refined"],
        help="Filter collections by workflow state",
    )
    collection_list_parser.add_argument(
        "--title",
        help="Filter collections by exact title",
    )
    collection_list_parser.add_argument(
        "--collection-id",
        help="Filter collections by exact collection ID",
    )
    collection_list_parser.add_argument(
        "--work-package-id",
        help="Filter collections by exact bound work_package_id",
    )
    collection_list_parser.add_argument(
        "--task-id",
        help="Filter collections by exact member task_id",
    )
    collection_list_parser.add_argument(
        "--show-work-package-id",
        action="store_true",
        help="Show bound work_package_id in list output",
    )
    collection_list_parser.add_argument(
        "--show-task-ids",
        action="store_true",
        help="Show member task_ids in list output",
    )
    collection_list_parser.set_defaults(func=handle_collection_list)

    collection_add_parser = collection_subparsers.add_parser(
        "add",
        help="Add a new collection",
    )
    collection_add_parser.add_argument("title", help="Collection title")
    collection_add_parser.add_argument(
        "--collection-state",
        default="source",
        choices=["source", "staged", "committed", "refined"],
        help="Collection workflow state",
    )
    collection_add_parser.set_defaults(func=handle_collection_add)

    collection_update_title_parser = collection_subparsers.add_parser(
        "update-title",
        help="Update collection title",
    )
    collection_update_title_parser.add_argument(
        "collection_id",
        help="Collection ID to update",
    )
    collection_update_title_parser.add_argument(
        "title",
        help="New collection title",
    )
    collection_update_title_parser.set_defaults(func=handle_collection_update_title)

    collection_update_state_parser = collection_subparsers.add_parser(
        "update-state",
        help="Update collection state",
    )
    collection_update_state_parser.add_argument(
        "collection_id",
        help="Collection ID to update",
    )
    collection_update_state_parser.add_argument(
        "collection_state",
        choices=["source", "staged", "committed", "refined"],
        help="New collection workflow state",
    )
    collection_update_state_parser.set_defaults(func=handle_collection_update_state)
    collection_set_work_package_parser = collection_subparsers.add_parser(
        "set-work-package",
        help="Set collection work package association",
    )
    collection_set_work_package_parser.add_argument(
        "collection_id",
        help="Collection ID to update",
    )
    collection_set_work_package_parser.add_argument(
        "wp_id",
        help="Work Package ID to associate",
    )
    collection_set_work_package_parser.set_defaults(
        func=handle_collection_set_work_package
    )

    collection_clear_work_package_parser = collection_subparsers.add_parser(
        "clear-work-package",
        help="Clear collection work package association",
    )
    collection_clear_work_package_parser.add_argument(
        "collection_id",
        help="Collection ID to clear",
    )
    collection_clear_work_package_parser.set_defaults(
        func=handle_collection_clear_work_package
    )

    collection_show_parser = collection_subparsers.add_parser(
        "show",
        help="Show a collection by ID",
    )
    collection_show_parser.add_argument(
        "collection_id",
        help="Collection ID to show",
    )
    collection_show_parser.add_argument(
        "--show-work-package-id",
        action="store_true",
        help="Show bound work_package_id in collection output",
    )
    collection_show_parser.set_defaults(func=handle_collection_show)
   
    collection_add_task_parser = collection_subparsers.add_parser(
        "add-task",
        help="Add a task to a collection",
    )
    collection_add_task_parser.add_argument(
        "collection_id",
        help="Collection ID to update",
    )
    collection_add_task_parser.add_argument(
        "task_ref",
        help="Task reference to add (task_id first, task_key second)",
    )
    collection_add_task_parser.set_defaults(func=handle_collection_add_task)

    collection_remove_task_parser = collection_subparsers.add_parser(
        "remove-task",
        help="Remove a task from a collection",
    )
    collection_remove_task_parser.add_argument(
        "collection_id",
        help="Collection ID to update",
    )
    collection_remove_task_parser.add_argument(
        "task_ref",
        help="Task reference to remove (task_id first, task_key second)",
    )
    collection_remove_task_parser.set_defaults(func=handle_collection_remove_task)

    orchestrate_parser = subparsers.add_parser(
        "orchestrate",
        help="Deterministic orchestration surfaces",
    )
    orchestrate_subparsers = orchestrate_parser.add_subparsers(
        dest="orchestrate_command"
    )

    orchestrate_wp_parser = orchestrate_subparsers.add_parser(
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
    task_subparsers = task_parser.add_subparsers(dest="task_command")

    task_add_parser = task_subparsers.add_parser("add", help="Add a new task")
    task_add_parser.add_argument("title", help="Task title")
    task_add_parser.add_argument(
        "--description",
        default=None,
        help="Optional task description",
    )
    task_add_parser.add_argument(
        "--owner",
        default=None,
        help="Optional task owner",
    )
    task_add_parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Optional task duration in days",
    )
    task_add_parser.add_argument(
        "--start-date",
        default=None,
        help="Optional task start date",
    )
    task_add_parser.add_argument(
        "--end-date",
        default=None,
        help="Optional task end date",
    )
    task_add_parser.add_argument(
        "--task-key",
        default=None,
        help="Optional deterministic task key",
    )
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
        "--has-dependents",
        choices=["true", "false"],
        help="Filter tasks by whether dependents exist",
    )
    task_list_parser.add_argument(
        "--show-task-key",
        action="store_true",
        help="Show task_key in list output",
    )
    task_list_parser.add_argument(
        "--show-work-package-id",
        action="store_true",
        help="Show work_package_id in list output",
    )
    task_list_parser.add_argument(
        "--show-dependency-refs",
        action="store_true",
        help="Show resolved dependency references in list output",
    )
    task_list_parser.add_argument(
        "--show-dependent-refs",
        action="store_true",
        help="Show resolved dependent references in list output",
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
    task_list_parser.add_argument(
        "--dependent-ref",
        default=None,
        help="Filter tasks by one dependent reference (task_id first, task_key second)",
    )
    task_list_parser.add_argument(
        "--work-package-id",
        default=None,
        help="Filter tasks by exact work_package_id",
    )
    task_list_parser.add_argument(
        "--collection-id",
        default=None,
        help="Filter tasks by exact collection_id membership",
    )
    task_list_parser.add_argument(
        "--show-collection-ids",
        action="store_true",
        help="Show collection_ids in list output",
    )
    task_list_parser.set_defaults(func=handle_task_list)

    task_show_parser = task_subparsers.add_parser("show", help="Show a task by ID")
    task_show_parser.add_argument("task_id", help="Task ID to show")
    task_show_parser.add_argument(
        "--show-dependency-refs",
        action="store_true",
        help="Show resolved dependency references in task output",
    )
    task_show_parser.add_argument(
        "--show-dependent-refs",
        action="store_true",
        help="Show resolved dependent references in task output",
    )
    task_show_parser.add_argument(
        "--show-work-package-id",
        action="store_true",
        help="Show work_package_id in task output",
    )
    task_show_parser.add_argument(
        "--show-collection-ids",
        action="store_true",
        help="Show collection_ids in task output",
    )
    task_show_parser.set_defaults(func=handle_task_show)

    task_set_key_parser = task_subparsers.add_parser("set-key", help="Set task key")
    task_set_key_parser.add_argument("task_id", help="Task ID to update")
    task_set_key_parser.add_argument("task_key", help="New deterministic task key")
    task_set_key_parser.set_defaults(func=handle_task_set_key)

    task_clear_key_parser = task_subparsers.add_parser("clear-key", help="Clear task key")
    task_clear_key_parser.add_argument("task_id", help="Task ID to update")
    task_clear_key_parser.set_defaults(func=handle_task_clear_key)

    task_update_status_parser = task_subparsers.add_parser(
        "update-status",
        help="Update task status",
    )
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
    task_set_dependencies_parser.set_defaults(func=handle_task_set_dependencies)

    task_set_work_package_parser = task_subparsers.add_parser(
        "set-work-package",
        help="Set task work package association",
    )
    task_set_work_package_parser.add_argument(
        "task_id",
        help="Task reference to update",
    )
    task_set_work_package_parser.add_argument(
        "wp_id",
        help="Work Package ID to associate",
    )
    task_set_work_package_parser.set_defaults(func=handle_task_set_work_package)

    task_clear_work_package_parser = task_subparsers.add_parser(
        "clear-work-package",
        help="Clear task work package association",
    )
    task_clear_work_package_parser.add_argument(
        "task_id",
        help="Task reference to clear",
    )
    task_clear_work_package_parser.set_defaults(func=handle_task_clear_work_package)

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
    
    if args.command == "wp" and args.wp_command is None:
        parser.parse_args(["wp", "-h"])
        return

    if args.command == "collection" and args.collection_command is None:
        parser.parse_args(["collection", "-h"])
        return

    if args.command == "orchestrate" and args.orchestrate_command is None:
        parser.parse_args(["orchestrate", "-h"])
        return

    if args.command == "runtime" and args.runtime_command is None:
        parser.parse_args(["runtime", "-h"])
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




