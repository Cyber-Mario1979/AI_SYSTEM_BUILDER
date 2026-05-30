from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ControlledDraftingLibraryStatus = Literal["runtime_facing_controlled_drafting_source"]
ControlledDraftingModeDefinitionStatus = Literal["runtime_facing_controlled_drafting_mode"]
ControlledDraftingMode = Literal[
    "strong_input_fill",
    "partial_bounded_completion",
    "minimal_scaffold_with_placeholders",
    "rationale_bound_section_drafting",
]
ControlledDraftPacketStatus = Literal["controlled_draft_packet"]

REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_product_ready_documents",
    "does_not_render_or_export_documents",
    "does_not_apply_standards_backed_output_controls",
    "does_not_mutate_lifecycle_or_review_state",
}


class ControlledDraftingModeDefinitionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drafting_mode_id: str = Field(min_length=1, pattern=r"^DRAFTMODE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ControlledDraftingModeDefinitionStatus = "runtime_facing_controlled_drafting_mode"
    drafting_mode: ControlledDraftingMode
    display_name: str = Field(min_length=1)
    supported_template_ids: list[str] = Field(min_length=1)
    supported_schema_ids: list[str] = Field(min_length=1)
    mode_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "supported_template_ids",
        "supported_schema_ids",
        "mode_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_mode_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled drafting mode value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_mode_definition_boundary(self):
        self._validate_mode_id_version_alignment()
        self._validate_supported_reference_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_mode_id_version_alignment(self) -> None:
        if not self.drafting_mode_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Controlled drafting mode version must match drafting_mode_id suffix: "
                f"{self.drafting_mode_id} / {self.version}"
            )

    def _validate_supported_reference_ids(self) -> None:
        if len(set(self.supported_template_ids)) != len(self.supported_template_ids):
            raise ValueError(
                "Duplicate controlled drafting supported_template_ids are not allowed: "
                f"{self.drafting_mode_id}"
            )
        if len(set(self.supported_schema_ids)) != len(self.supported_schema_ids):
            raise ValueError(
                "Duplicate controlled drafting supported_schema_ids are not allowed: "
                f"{self.drafting_mode_id}"
            )

        for template_id in self.supported_template_ids:
            if not template_id.startswith("TPL-") or "@" not in template_id:
                raise ValueError(
                    "Controlled drafting supported_template_ids must use TPL-...@v... IDs: "
                    f"{template_id}"
                )
        for schema_id in self.supported_schema_ids:
            if not schema_id.startswith("SCHEMA-") or "@" not in schema_id:
                raise ValueError(
                    "Controlled drafting supported_schema_ids must use SCHEMA-...@v... IDs: "
                    f"{schema_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.5 controlled drafting mode is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class ControlledDraftingLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_CONTROLLED_DRAFTING_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ControlledDraftingLibraryStatus = "runtime_facing_controlled_drafting_source"
    drafting_modes: list[ControlledDraftingModeDefinitionModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled drafting library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_drafting_library_boundary(self):
        self._validate_unique_mode_ids()
        self._validate_unique_drafting_modes()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_mode_ids(self) -> None:
        mode_ids: set[str] = set()
        for mode in self.drafting_modes:
            if mode.drafting_mode_id in mode_ids:
                raise ValueError(
                    "Duplicate controlled drafting mode id is not allowed: "
                    f"{mode.drafting_mode_id}"
                )
            mode_ids.add(mode.drafting_mode_id)

    def _validate_unique_drafting_modes(self) -> None:
        modes: set[str] = set()
        for mode in self.drafting_modes:
            if mode.drafting_mode in modes:
                raise ValueError(
                    "Duplicate controlled drafting mode is not allowed: "
                    f"{mode.drafting_mode}"
                )
            modes.add(mode.drafting_mode)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.5 controlled drafting library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class ControlledDraftInputFieldValueModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    value: str = Field(min_length=1)
    source_ref: str | None = Field(default=None, min_length=1)


class ControlledDraftPlaceholderModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    placeholder_text: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class ControlledDraftSectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    section_title: str = Field(min_length=1)
    draft_text: str = Field(min_length=1)
    field_ids: list[str] = Field(min_length=1)
    rationale_refs: list[str] = Field(default_factory=list)
    limitation_statements: list[str] = Field(default_factory=list)
    reviewer_attention_points: list[str] = Field(default_factory=list)

    @field_validator(
        "field_ids",
        "rationale_refs",
        "limitation_statements",
        "reviewer_attention_points",
    )
    @classmethod
    def validate_no_blank_section_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled draft section value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_section_boundary(self):
        if len(set(self.field_ids)) != len(self.field_ids):
            raise ValueError(
                "Duplicate controlled draft section field_ids are not allowed: "
                f"{self.section_id}"
            )
        return self


class ControlledDraftPacketModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    draft_id: str = Field(min_length=1, pattern=r"^DRAFT-[A-Z0-9-]+@v[0-9]+$")
    status: ControlledDraftPacketStatus = "controlled_draft_packet"
    drafting_mode_id: str = Field(min_length=1, pattern=r"^DRAFTMODE-[A-Z0-9-]+@v[0-9]+$")
    drafting_mode: ControlledDraftingMode
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    supplied_field_values: list[ControlledDraftInputFieldValueModel] = Field(default_factory=list)
    missing_required_field_ids: list[str] = Field(default_factory=list)
    placeholders: list[ControlledDraftPlaceholderModel] = Field(default_factory=list)
    section_drafts: list[ControlledDraftSectionModel] = Field(min_length=1)
    limitation_statements: list[str] = Field(min_length=1)
    reviewer_attention_points: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "missing_required_field_ids",
        "limitation_statements",
        "reviewer_attention_points",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_packet_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled draft packet value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_draft_packet_boundary(self):
        self._validate_unique_supplied_field_ids()
        self._validate_unique_placeholder_field_ids()
        self._validate_unique_section_ids()
        self._validate_strong_input_fill_boundary()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_supplied_field_ids(self) -> None:
        field_ids = [field.field_id for field in self.supplied_field_values]
        if len(set(field_ids)) != len(field_ids):
            raise ValueError("Duplicate controlled draft supplied field_id is not allowed")

    def _validate_unique_placeholder_field_ids(self) -> None:
        field_ids = [placeholder.field_id for placeholder in self.placeholders]
        if len(set(field_ids)) != len(field_ids):
            raise ValueError("Duplicate controlled draft placeholder field_id is not allowed")

    def _validate_unique_section_ids(self) -> None:
        section_ids = [section.section_id for section in self.section_drafts]
        if len(set(section_ids)) != len(section_ids):
            raise ValueError("Duplicate controlled draft section_id is not allowed")

    def _validate_strong_input_fill_boundary(self) -> None:
        if self.drafting_mode != "strong_input_fill":
            return
        if self.missing_required_field_ids:
            raise ValueError(
                "Strong input fill controlled draft cannot include missing required fields"
            )
        if self.placeholders:
            raise ValueError("Strong input fill controlled draft cannot include placeholders")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.5 controlled draft packet is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
