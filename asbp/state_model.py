from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    status: Literal["planned", "in_progress", "completed", "over_due"]
    dependencies: list[str] = Field(default_factory=list)


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