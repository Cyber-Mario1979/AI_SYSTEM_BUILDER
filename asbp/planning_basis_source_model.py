from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PlanningBasisSourceStatus = Literal["starter_runtime_source", "mvp_remediation_source"]
DurationEstimateType = Literal["starter_estimate", "human_confirmed_estimate", "site_defined_estimate", "future_mapping_expected"]
DurationUnit = Literal["working_day"]
EstimationSourceStatus = Literal["starter_baseline", "sme_estimate_required", "site_input_required", "future_confirmation_required"]
ScopeComplexity = Literal["simple", "standard", "complex", "not_applicable"]
CalendarDependencyStatus = Literal["calendar_aware_no_capacity_calculation", "calendar_required_before_scheduling", "not_applicable"]


class DurationRangeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_days: float = Field(ge=0)
    typical_days: float = Field(ge=0)
    max_days: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_duration_order(self):
        if not self.min_days <= self.typical_days <= self.max_days:
            raise ValueError("Duration range must satisfy min_days <= typical_days <= max_days")
        return self


class ScopeRuleModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    scope_complexity: ScopeComplexity
    condition: str = Field(min_length=1)
    adjustment_guidance: str = Field(min_length=1)
    user_amendable: bool = True


class TaskSourceLinkModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_pool_id: str = Field(min_length=1, pattern=r"^TP-[A-Z0-9-]+@v[0-9]+$")
    atomic_task_id: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")


class DurationSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_ref_id: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*_DUR$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: PlanningBasisSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    estimate_type: DurationEstimateType
    estimation_source_status: EstimationSourceStatus
    duration_unit: DurationUnit = "working_day"
    duration_range: DurationRangeModel
    scope_rules: list[ScopeRuleModel] = Field(min_length=1)
    calendar_dependency_status: CalendarDependencyStatus
    linked_task_sources: list[TaskSourceLinkModel] = Field(min_length=1)
    user_amendable: bool = True
    assumption_controls: list[str] = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator("assumption_controls", "notes")
    @classmethod
    def validate_no_blank_strings(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank planning-basis value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_duration_source_boundary(self):
        if self.estimate_type == "future_mapping_expected" and self.duration_range.typical_days > 0:
            raise ValueError("future_mapping_expected duration source cannot include a non-zero typical estimate: " f"{self.duration_ref_id}")
        link_ids: set[tuple[str, str]] = set()
        for linked_task_source in self.linked_task_sources:
            link_id = (linked_task_source.task_pool_id, linked_task_source.atomic_task_id)
            if link_id in link_ids:
                raise ValueError("Duplicate linked task source is not allowed for " f"{self.duration_ref_id}: {linked_task_source.task_pool_id}::{linked_task_source.atomic_task_id}")
            link_ids.add(link_id)
        return self


class PlanningBasisLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: PlanningBasisSourceStatus = "starter_runtime_source"
    duration_sources: list[DurationSourceModel] = Field(min_length=1)
    library_controls: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_duration_refs(self):
        duration_ref_ids: set[str] = set()
        for duration_source in self.duration_sources:
            if duration_source.duration_ref_id in duration_ref_ids:
                raise ValueError(f"Duplicate duration_ref_id is not allowed: {duration_source.duration_ref_id}")
            duration_ref_ids.add(duration_source.duration_ref_id)
        return self


def collect_task_pool_duration_refs(task_pool_library: Any) -> set[str]:
    duration_refs: set[str] = set()
    for task_pool in task_pool_library.task_pools:
        for task in task_pool.tasks:
            duration_refs.add(task.duration_ref.duration_ref_id)
    return duration_refs


def collect_planning_basis_duration_refs(library: PlanningBasisLibraryModel) -> set[str]:
    return {duration_source.duration_ref_id for duration_source in library.duration_sources}
