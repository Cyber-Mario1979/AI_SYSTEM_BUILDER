from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


 

CollectionState = Literal["source", "staged", "committed", "refined"]
StandardsBundleId = Literal["cqv-core", "cleanroom-hvac", "automation"]
ScopeIntentId = Literal[
    "end-to-end",
    "qualification-only",
    "commissioning-only",
    "periodic-verification",
    "post-change",
    "post-deviation",
]


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
    task_ids: list[str] = Field(default_factory=list)


class SelectorContextModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_type: str | None = Field(default=None, min_length=1)
    preset_id: str | None = Field(default=None, min_length=1)
    scope_intent: ScopeIntentId | None = None
    standards_bundles: list[StandardsBundleId] = Field(default_factory=list)

    @field_validator("standards_bundles")
    @classmethod
    def validate_standards_bundles(
        cls,
        standards_bundles: list[StandardsBundleId],
    ) -> list[StandardsBundleId]:
        if len(standards_bundles) != len(set(standards_bundles)):
            raise ValueError("Duplicate standards bundle is not allowed")

        if standards_bundles and "cqv-core" not in standards_bundles:
            raise ValueError(
                "standards_bundles must include cqv-core as the baseline bundle"
            )

        return standards_bundles

    @model_validator(mode="after")
    def validate_at_least_one_selector_seed(self):
        if self.system_type is None and self.preset_id is None:
            raise ValueError(
                "selector_context must include at least one selector seed"
            )
        return self

class WorkPackageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wp_id: str = Field(pattern=r"^WP-\d{3}$")
    title: str = Field(min_length=1)
    status: Literal["open", "in_progress", "completed"]
    selector_context: SelectorContextModel | None = None


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