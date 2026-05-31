from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PresetFamilyId = Literal[
    "PF-CLEANROOM",
    "PF-PROCESS-EQUIPMENT",
    "PF-QC-LAB-EQUIPMENT",
    "PF-UTILITIES",
    "PF-COMPUTERIZED-SYSTEMS",
    "PF-MANUAL-FALLBACK",
]
TaskPoolSourceStatus = Literal[
    "starter_runtime_source",
    "mvp_remediation_source",
]
TaskDependencyType = Literal["FS"]
DocumentExpectationStatus = Literal[
    "future_expected",
    "not_applicable",
    "tbd",
]


class DurationReferenceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_ref_id: str = Field(
        min_length=1,
        pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*_DUR$",
    )
    resolution_checkpoint: Literal["M27.6"] = "M27.6"


class DocumentExpectationModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_ref: str = Field(min_length=1)
    status: DocumentExpectationStatus = "future_expected"
    notes: str | None = Field(default=None, min_length=1)


class TaskDependencyModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    atomic_task_id: str = Field(
        min_length=1,
        pattern=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    )
    dependency_type: TaskDependencyType = "FS"
    lag_days: int = Field(default=0, ge=0)


class AtomicTaskSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    atomic_task_id: str = Field(
        min_length=1,
        pattern=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    )
    title: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    task_type: str = Field(min_length=1)
    owner_role: str = Field(min_length=1)
    prerequisites: list[str] = Field(default_factory=list)
    dependencies: list[TaskDependencyModel] = Field(default_factory=list)
    duration_ref: DurationReferenceModel
    document_expectations: list[DocumentExpectationModel] = Field(
        default_factory=list,
    )
    notes: list[str] = Field(default_factory=list)

    @field_validator("prerequisites", "notes")
    @classmethod
    def validate_no_blank_strings(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank string is not allowed")
        return values


class TaskPoolSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_pool_id: str = Field(
        min_length=1,
        pattern=r"^TP-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TaskPoolSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    preset_family: PresetFamilyId
    selector_context_tags: list[str] = Field(min_length=1)
    lifecycle_events: list[str] = Field(min_length=1)
    qualification_validation_intents: list[str] = Field(min_length=1)
    tasks: list[AtomicTaskSourceModel] = Field(min_length=1)
    domain: str | None = Field(default=None, min_length=1)
    asset_archetype: str | None = Field(default=None, min_length=1)
    utility_system: str | None = Field(default=None, min_length=1)
    lifecycle_route: str | None = Field(default=None, min_length=1)
    source_limitations: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(default_factory=list)

    @field_validator(
        "selector_context_tags",
        "lifecycle_events",
        "qualification_validation_intents",
        "source_limitations",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_context_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank selector/context value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_atomic_task_identity_and_dependencies(self):
        task_ids: set[str] = set()

        for task in self.tasks:
            if task.atomic_task_id in task_ids:
                raise ValueError(
                    f"Duplicate atomic_task_id is not allowed: "
                    f"{task.atomic_task_id}"
                )
            task_ids.add(task.atomic_task_id)

        for task in self.tasks:
            for dependency in task.dependencies:
                if dependency.atomic_task_id == task.atomic_task_id:
                    raise ValueError(
                        "Atomic task cannot depend on itself: "
                        f"{task.atomic_task_id}"
                    )
                if dependency.atomic_task_id not in task_ids:
                    raise ValueError(
                        "Atomic task dependency does not exist in task pool "
                        f"{self.task_pool_id}: {task.atomic_task_id} -> "
                        f"{dependency.atomic_task_id}"
                    )

        return self


class TaskPoolLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TaskPoolSourceStatus = "starter_runtime_source"
    task_pools: list[TaskPoolSourceModel] = Field(min_length=1)
    library_controls: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(default_factory=list)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank task-pool library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_unique_task_pool_ids(self):
        task_pool_ids: set[str] = set()

        for task_pool in self.task_pools:
            if task_pool.task_pool_id in task_pool_ids:
                raise ValueError(
                    f"Duplicate task_pool_id is not allowed: "
                    f"{task_pool.task_pool_id}"
                )
            task_pool_ids.add(task_pool.task_pool_id)

        return self
