from __future__ import annotations

import json
from pathlib import Path

from asbp.task_pool_source_model import (
    AtomicTaskSourceModel,
    TaskPoolLibraryModel,
    TaskPoolSourceModel,
)


TASK_POOL_SOURCE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "task_pools"
)

DEFAULT_TASK_POOL_SOURCE_PATH = TASK_POOL_SOURCE_DIR / "starter_task_pools.json"

MVP_TASK_POOL_SOURCE_PATHS = [
    TASK_POOL_SOURCE_DIR / "mvp_cleanroom_hvac_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_process_equipment_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_utilities_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_csv_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_qc_lab_equipment_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_decommissioning_task_pools.json",
    TASK_POOL_SOURCE_DIR / "mvp_manual_fallback_task_pools.json",
]


def load_task_pool_library_from_payload(payload: dict) -> TaskPoolLibraryModel:
    if "task_pools" not in payload:
        raise ValueError("task-pool library payload must include task_pools")

    return TaskPoolLibraryModel(**payload)


def load_task_pool_library_from_path(path: Path) -> TaskPoolLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_task_pool_library_from_payload(payload)


def load_default_task_pool_library() -> TaskPoolLibraryModel:
    return load_task_pool_library_from_path(DEFAULT_TASK_POOL_SOURCE_PATH)


def load_mvp_task_pool_libraries() -> list[TaskPoolLibraryModel]:
    return [
        load_task_pool_library_from_path(path)
        for path in MVP_TASK_POOL_SOURCE_PATHS
    ]


def list_task_pool_ids(library: TaskPoolLibraryModel) -> list[str]:
    return [task_pool.task_pool_id for task_pool in library.task_pools]


def get_task_pool_by_id(
    library: TaskPoolLibraryModel,
    task_pool_id: str,
) -> TaskPoolSourceModel:
    for task_pool in library.task_pools:
        if task_pool.task_pool_id == task_pool_id:
            return task_pool

    raise ValueError(f"Task pool source definition not found: {task_pool_id}")


def get_atomic_task_by_id(
    task_pool: TaskPoolSourceModel,
    atomic_task_id: str,
) -> AtomicTaskSourceModel:
    for atomic_task in task_pool.tasks:
        if atomic_task.atomic_task_id == atomic_task_id:
            return atomic_task

    raise ValueError(
        "Atomic task source definition not found: "
        f"{task_pool.task_pool_id}::{atomic_task_id}"
    )


def build_task_source_definition_id(
    task_pool_id: str,
    atomic_task_id: str,
) -> str:
    return f"{task_pool_id}::{atomic_task_id}"
