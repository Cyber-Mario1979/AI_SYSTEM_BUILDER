import json
from pathlib import Path

from pydantic import ValidationError

from asbp.collection_logic import (
    validate_persisted_collection_task_memberships,
    validate_persisted_collection_work_package_links,
)
from asbp.planning_logic import (
    validate_persisted_generated_task_plan_consistency,
    validate_persisted_plan_work_package_links,
)
from asbp.binding_context_logic import (
    validate_persisted_plan_binding_context_consistency,
)
from asbp.source_of_work_logic import validate_persisted_task_source_contracts
from asbp.state_model import StateModel
from asbp.task_logic import validate_persisted_task_keys
from asbp.work_package_logic import validate_persisted_task_work_package_links


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
        task.setdefault("work_package_id", None)
        task.setdefault("instantiation_mode", "manual")
        task.setdefault("source_definition_kind", None)
        task.setdefault("source_definition_id", None)

    for task_collection in raw_state.get("task_collections", []):
        task_collection.setdefault("work_package_id", None)
        task_collection.setdefault("task_ids", [])

    raw_state.setdefault("plans", [])

    state = StateModel(**raw_state)
    validate_persisted_task_keys(state.tasks)
    validate_persisted_task_source_contracts(state.tasks)
    validate_persisted_task_work_package_links(
        state.tasks,
        state.work_packages,
    )
    validate_persisted_collection_work_package_links(
        state.task_collections,
        state.work_packages,
    )
    validate_persisted_collection_task_memberships(
        state.tasks,
        state.task_collections,
    )
    validate_persisted_plan_work_package_links(
        state.plans,
        state.work_packages,
    )
    validate_persisted_generated_task_plan_consistency(
        state.plans,
        state.tasks,
    )
    validate_persisted_plan_binding_context_consistency(
        state.plans,
        state.work_packages,
    )
    return state


def build_persisted_state_payload(state: StateModel) -> dict:
    payload = state.model_dump(mode="json")

    for task, task_payload in zip(state.tasks, payload.get("tasks", [])):
        if task.work_package_id is None:
            task_payload.pop("work_package_id", None)

        if task.instantiation_mode != "manual":
            task_payload["instantiation_mode"] = task.instantiation_mode

        if task.source_definition_kind is not None:
            task_payload["source_definition_kind"] = task.source_definition_kind

        if task.source_definition_id is not None:
            task_payload["source_definition_id"] = task.source_definition_id

    for work_package in payload.get("work_packages", []):
        selector_context = work_package.get("selector_context")

        if selector_context is None:
            work_package.pop("selector_context", None)
            continue

        if selector_context.get("system_type") is None:
            selector_context.pop("system_type", None)

        if selector_context.get("preset_id") is None:
            selector_context.pop("preset_id", None)

        if selector_context.get("scope_intent") is None:
            selector_context.pop("scope_intent", None)

        if selector_context.get("standards_bundles") == []:
            selector_context.pop("standards_bundles", None)

        if not selector_context:
            work_package.pop("selector_context", None)

    for task_collection, task_collection_payload in zip(
        state.task_collections,
        payload.get("task_collections", []),
    ):
        if task_collection.work_package_id is not None:
            task_collection_payload["work_package_id"] = (
                task_collection.work_package_id
            )

        if task_collection_payload.get("task_ids") == []:
            task_collection_payload.pop("task_ids", None)

    for plan in payload.get("plans", []):
        planning_basis = plan.get("planning_basis")

        if plan.get("generated_task_plans") == []:
            plan.pop("generated_task_plans", None)

        if planning_basis is None:
            plan.pop("planning_basis", None)
        else:
            if planning_basis.get("basis_label") is None:
                planning_basis.pop("basis_label", None)

        if plan.get("planned_start_at") is None:
            plan.pop("planned_start_at", None)

        if plan.get("planning_calendar") is None:
            plan.pop("planning_calendar", None)

    if payload.get("plans") == []:
        payload.pop("plans", None)

    return payload


def save_validated_state_to_path(
    state: StateModel,
    state_file_path: Path,
) -> None:
    state_file_path.parent.mkdir(parents=True, exist_ok=True)

    with state_file_path.open("w", encoding="utf-8") as f:
        json.dump(build_persisted_state_payload(state), f, indent=2)
        f.write("\n")


def save_validated_state(state: StateModel) -> None:
    save_validated_state_to_path(state, get_state_file_path())


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
