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

ProfileSourceStatus = Literal["starter_runtime_source"]
ProfileType = Literal[
    "area_system",
    "cleanroom_hvac",
    "equipment_system",
    "qualification",
    "manual_fallback",
]
ProfileContextFieldStatus = Literal[
    "human_input_required",
    "starter_default",
    "future_mapping_expected",
    "not_applicable",
]


class ProfileContextFieldModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: str = Field(
        min_length=1,
        pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$",
    )
    label: str = Field(min_length=1)
    value_status: ProfileContextFieldStatus
    value: str | None = Field(default=None, min_length=1)
    allowed_values: list[str] = Field(default_factory=list)
    notes: str | None = Field(default=None, min_length=1)

    @field_validator("allowed_values")
    @classmethod
    def validate_no_blank_allowed_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank allowed value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_value_status(self):
        if self.value_status == "starter_default" and self.value is None:
            raise ValueError(
                "starter_default profile context field requires value: "
                f"{self.field_id}"
            )

        if self.value_status == "not_applicable" and self.value is not None:
            raise ValueError(
                "not_applicable profile context field cannot include value: "
                f"{self.field_id}"
            )

        return self


class ProfileSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(
        min_length=1,
        pattern=r"^PROF-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ProfileSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    profile_type: ProfileType
    related_preset_families: list[PresetFamilyId] = Field(min_length=1)
    selector_context_tags: list[str] = Field(min_length=1)
    lifecycle_events: list[str] = Field(min_length=1)
    qualification_validation_intents: list[str] = Field(min_length=1)
    context_fields: list[ProfileContextFieldModel] = Field(min_length=1)
    assumption_controls: list[str] = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator(
        "selector_context_tags",
        "lifecycle_events",
        "qualification_validation_intents",
        "assumption_controls",
        "notes",
    )
    @classmethod
    def validate_no_blank_context_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank profile context value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_profile_context_field_identity(self):
        field_ids: set[str] = set()

        for context_field in self.context_fields:
            if context_field.field_id in field_ids:
                raise ValueError(
                    f"Duplicate profile context field_id is not allowed: "
                    f"{context_field.field_id}"
                )
            field_ids.add(context_field.field_id)

        return self


class ProfileLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ProfileSourceStatus = "starter_runtime_source"
    profiles: list[ProfileSourceModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_profile_ids(self):
        profile_ids: set[str] = set()

        for profile in self.profiles:
            if profile.profile_id in profile_ids:
                raise ValueError(
                    f"Duplicate profile_id is not allowed: "
                    f"{profile.profile_id}"
                )
            profile_ids.add(profile.profile_id)

        return self
