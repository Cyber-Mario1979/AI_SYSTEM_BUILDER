import json
from pathlib import Path

from pydantic import ValidationError

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

    state = StateModel(**raw_state)
    validate_persisted_task_keys(state.tasks)
    validate_persisted_task_work_package_links(
        state.tasks,
        state.work_packages,
    )
    return state


def build_persisted_state_payload(state: StateModel) -> dict:
    payload = state.model_dump()

    for task in payload.get("tasks", []):
        if task.get("work_package_id") is None:
            task.pop("work_package_id", None)

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