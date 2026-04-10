from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


CollectionState = Literal["source", "staged", "committed", "refined"]


class TaskModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    order: int = Field(ge=1)
    title: str = Field(min_length=1)
    description: str | None = None
    owner: str | None = None
    duration: int | None = Field(default=None, ge=1)
    start_date: str | None = Field(default=None, min_length=1)
    end_date: str | None = Field(default=None, min_length=1)
    task_key: str | None = None
    work_package_id: str | None = None
    status: Literal["planned", "in_progress", "completed", "over_due"]
    dependencies: list[str] = Field(default_factory=list)


class TaskCollectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    collection_id: str = Field(pattern=r"^TC-\d{3}$")
    title: str = Field(min_length=1)
    collection_state: CollectionState


class WorkPackageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wp_id: str = Field(pattern=r"^WP-\d{3}$")
    title: str = Field(min_length=1)
    status: Literal["open", "in_progress", "completed"]


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project: str
    version: str
    status: Literal["not_started", "in_flight", "completed"]
    tasks: list[TaskModel] = Field(default_factory=list)
    work_packages: list[WorkPackageModel] = Field(default_factory=list)
    task_collections: list[TaskCollectionModel] = Field(default_factory=list)

    @field_validator("work_packages")
    @classmethod
    def validate_unique_work_package_ids(
        cls,
        work_packages: list[WorkPackageModel],
    ) -> list[WorkPackageModel]:
        seen_wp_ids: set[str] = set()

        for work_package in work_packages:
            if work_package.wp_id in seen_wp_ids:
                raise ValueError(
                    f"Duplicate wp_id is not allowed: {work_package.wp_id}"
                )
            seen_wp_ids.add(work_package.wp_id)

        return work_packages

    @field_validator("task_collections")
    @classmethod
    def validate_unique_task_collection_ids(
        cls,
        task_collections: list[TaskCollectionModel],
    ) -> list[TaskCollectionModel]:
        seen_collection_ids: set[str] = set()

        for task_collection in task_collections:
            if task_collection.collection_id in seen_collection_ids:
                raise ValueError(
                    "Duplicate collection_id is not allowed: "
                    f"{task_collection.collection_id}"
                )
            seen_collection_ids.add(task_collection.collection_id)

        return task_collections