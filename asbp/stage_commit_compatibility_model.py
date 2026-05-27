from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asbp.state_model import TaskCollectionModel, TaskModel


CompatibilityStatus = Literal["compatible"]
SourceSelectionMode = Literal["selector_mapping"]
PlanningInputState = Literal["ready_for_planning_input"]


class SourceSelectionCompatibilityModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selector_context_id: str = Field(min_length=1)
    selection_mode: SourceSelectionMode = "selector_mapping"
    task_pool_id: str = Field(
        min_length=1,
        pattern=r"^TP-[A-Z0-9-]+@v[0-9]+$",
    )


class InstantiatedTaskCompatibilityModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    task: TaskModel
    atomic_task_id: str = Field(
        min_length=1,
        pattern=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    )
    duration_ref_id: str = Field(
        min_length=1,
        pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*_DUR$",
    )


class PlanningInputCompatibilityModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    work_package_id: str = Field(pattern=r"^WP-\d{3}$")
    committed_collection_id: str = Field(pattern=r"^TC-\d{3}$")
    source_task_pool_id: str = Field(
        min_length=1,
        pattern=r"^TP-[A-Z0-9-]+@v[0-9]+$",
    )
    task_ids: list[str] = Field(min_length=1)
    duration_ref_ids: list[str] = Field(min_length=1)
    planning_basis_library_id: str = Field(min_length=1)
    calendar_id: str = Field(min_length=1)
    planning_input_state: PlanningInputState = "ready_for_planning_input"


class StageCommitCompatibilityResultModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    status: CompatibilityStatus = "compatible"
    source_selection: SourceSelectionCompatibilityModel
    staged_tasks: list[InstantiatedTaskCompatibilityModel] = Field(min_length=1)
    staged_collection: TaskCollectionModel
    committed_collection: TaskCollectionModel
    planning_input: PlanningInputCompatibilityModel
