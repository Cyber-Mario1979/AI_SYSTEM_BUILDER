from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


BaselineSourceStatus = Literal["starter_runtime_source"]
SourceFamilyId = Literal[
    "task_pools",
    "profiles",
    "calendars",
    "planning_basis",
    "mappings",
]


class SourceFamilyBaselineModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family_id: SourceFamilyId
    library_id: str = Field(min_length=1)
    expected_status: BaselineSourceStatus = "starter_runtime_source"
    source_path: str = Field(min_length=1)
    implementation_checkpoint: str = Field(
        min_length=1,
        pattern=r"^M27\.[0-9]+$",
    )


class SourceLibraryBaselineModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    baseline_id: str = Field(
        min_length=1,
        pattern=r"^M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: BaselineSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    source_families: list[SourceFamilyBaselineModel] = Field(min_length=1)
    integration_controls: list[str] = Field(min_length=1)

    @field_validator("integration_controls")
    @classmethod
    def validate_no_blank_controls(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank integration control is not allowed")
        return values

    @model_validator(mode="after")
    def validate_family_baseline_identity(self):
        family_ids: set[str] = set()

        for source_family in self.source_families:
            if source_family.family_id in family_ids:
                raise ValueError(
                    "Duplicate source family is not allowed in baseline: "
                    f"{source_family.family_id}"
                )
            family_ids.add(source_family.family_id)

        required_families = {
            "task_pools",
            "profiles",
            "calendars",
            "planning_basis",
            "mappings",
        }
        missing_families = sorted(required_families - family_ids)
        if missing_families:
            raise ValueError(
                "M27.8 baseline is missing source families: "
                f"{', '.join(missing_families)}"
            )

        return self


class SourceLibraryBaselineRuntimeModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    baseline: SourceLibraryBaselineModel
    task_pool_library: object
    profile_library: object
    calendar_library: object
    planning_basis_library: object
    mapping_library: object
