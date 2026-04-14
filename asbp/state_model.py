from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


CollectionState = Literal["source", "staged", "committed", "refined"]
PlanState = Literal["draft", "committed"]
DurationSourceId = Literal["task_duration"]
WeekdayId = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
WorkmonthModeId = Literal["calendar_month"]
StandardsBundleId = Literal["cqv-core", "cleanroom-hvac", "automation"]
ScopeIntentId = Literal[
    "end-to-end",
    "qualification-only",
    "commissioning-only",
    "periodic-verification",
    "post-change",
    "post-deviation",
]

CANONICAL_WEEKDAY_ORDER: tuple[WeekdayId, ...] = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)
_WEEKDAY_ORDER_INDEX = {
    weekday: index for index, weekday in enumerate(CANONICAL_WEEKDAY_ORDER)
}


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


class PlanningBasisModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_source: DurationSourceId
    basis_label: str | None = Field(default=None, min_length=1)


class PlanningCalendarModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    working_days: list[WeekdayId] = Field(min_length=1, max_length=7)
    workday_hours: int = Field(ge=1, le=24)
    workmonth_mode: WorkmonthModeId

    @field_validator("working_days")
    @classmethod
    def validate_and_normalize_working_days(
        cls,
        working_days: list[WeekdayId],
    ) -> list[WeekdayId]:
        if len(working_days) != len(set(working_days)):
            raise ValueError("Duplicate working day is not allowed")

        return sorted(
            working_days,
            key=lambda weekday: _WEEKDAY_ORDER_INDEX[weekday],
        )


class GeneratedTaskPlanModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    sequence_order: int = Field(ge=1)
    duration_days: int = Field(ge=1)
    dependency_task_ids: list[str] = Field(default_factory=list)
    planned_start_at: datetime
    planned_finish_at: datetime

    @field_validator("planned_start_at", "planned_finish_at")
    @classmethod
    def validate_generated_task_plan_timestamps_are_timezone_aware(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("generated task plan timestamp must be timezone-aware")
        return value

    @model_validator(mode="after")
    def validate_finish_after_start(self):
        if self.planned_finish_at <= self.planned_start_at:
            raise ValueError("planned_finish_at must be after planned_start_at")
        return self


class PlanningModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(pattern=r"^PLAN-\d{3}$")
    work_package_id: str = Field(pattern=r"^WP-\d{3}$")
    plan_state: PlanState
    planning_basis: PlanningBasisModel | None = None
    planned_start_at: datetime | None = None
    planning_calendar: PlanningCalendarModel | None = None
    generated_task_plans: list[GeneratedTaskPlanModel] = Field(default_factory=list)

    @field_validator("planned_start_at")
    @classmethod
    def validate_planned_start_at_is_timezone_aware(
        cls,
        planned_start_at: datetime | None,
    ) -> datetime | None:
        if planned_start_at is None:
            return None

        if (
            planned_start_at.tzinfo is None
            or planned_start_at.utcoffset() is None
        ):
            raise ValueError("planned_start_at must be timezone-aware")

        return planned_start_at


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project: str
    version: str
    status: Literal["not_started", "in_flight", "completed"]
    tasks: list[TaskModel] = Field(default_factory=list)
    work_packages: list[WorkPackageModel] = Field(default_factory=list)
    task_collections: list[TaskCollectionModel] = Field(default_factory=list)
    plans: list[PlanningModel] = Field(default_factory=list)

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

    @field_validator("plans")
    @classmethod
    def validate_unique_plan_ids(
        cls,
        plans: list[PlanningModel],
    ) -> list[PlanningModel]:
        seen_plan_ids: set[str] = set()

        for plan in plans:
            if plan.plan_id in seen_plan_ids:
                raise ValueError(
                    f"Duplicate plan_id is not allowed: {plan.plan_id}"
                )
            seen_plan_ids.add(plan.plan_id)

        return plans