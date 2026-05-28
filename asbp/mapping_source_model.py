from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


MappingSourceStatus = Literal["starter_runtime_source"]
MappingKind = Literal[
    "preset_to_profile",
    "selector_to_task_pool",
    "task_to_document",
    "standard_to_template",
]
ReferenceType = Literal[
    "preset_family",
    "selector_context",
    "task_pool",
    "profile",
    "atomic_task",
    "document_expectation",
    "standard_bundle",
    "template",
]
ReferenceStatus = Literal[
    "resolved_source",
    "future_expected",
    "placeholder_not_runtime_authority",
]


class MappingReferenceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_id: str = Field(min_length=1)
    reference_type: ReferenceType
    reference_status: ReferenceStatus
    resolution_checkpoint: str | None = Field(default=None, min_length=1)
    notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_future_or_placeholder_resolution(self):
        if (
            self.reference_status != "resolved_source"
            and self.resolution_checkpoint is None
        ):
            raise ValueError(
                "Future or placeholder mapping reference requires "
                f"resolution_checkpoint: {self.reference_id}"
            )

        if (
            self.reference_status == "resolved_source"
            and self.resolution_checkpoint is not None
        ):
            raise ValueError(
                "Resolved mapping reference cannot include "
                f"resolution_checkpoint: {self.reference_id}"
            )

        return self


class MappingSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mapping_id: str = Field(
        min_length=1,
        pattern=r"^MAP-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: MappingSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    mapping_kind: MappingKind
    source_refs: list[MappingReferenceModel] = Field(min_length=1)
    target_refs: list[MappingReferenceModel] = Field(min_length=1)
    applicability_tags: list[str] = Field(min_length=1)
    mapping_controls: list[str] = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator("applicability_tags", "mapping_controls", "notes")
    @classmethod
    def validate_no_blank_strings(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank mapping source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_mapping_reference_boundary(self):
        self._validate_no_duplicate_references()
        self._validate_reference_types_by_kind()
        self._validate_reference_status_by_kind()
        return self

    def _validate_no_duplicate_references(self) -> None:
        seen_refs: set[tuple[str, str]] = set()

        for reference in [*self.source_refs, *self.target_refs]:
            reference_key = (reference.reference_type, reference.reference_id)
            if reference_key in seen_refs:
                raise ValueError(
                    f"Duplicate mapping reference is not allowed in "
                    f"{self.mapping_id}: "
                    f"{reference.reference_type}::{reference.reference_id}"
                )
            seen_refs.add(reference_key)

    def _validate_reference_types_by_kind(self) -> None:
        expected_types: dict[str, tuple[set[str], set[str]]] = {
            "preset_to_profile": ({"preset_family"}, {"profile"}),
            "selector_to_task_pool": ({"selector_context"}, {"task_pool"}),
            "task_to_document": ({"atomic_task"}, {"document_expectation"}),
            "standard_to_template": ({"standard_bundle"}, {"template"}),
        }

        allowed_source_types, allowed_target_types = expected_types[
            self.mapping_kind
        ]

        for reference in self.source_refs:
            if reference.reference_type not in allowed_source_types:
                raise ValueError(
                    f"{self.mapping_kind} mapping has invalid source "
                    f"reference_type: {reference.reference_type}"
                )

        for reference in self.target_refs:
            if reference.reference_type not in allowed_target_types:
                raise ValueError(
                    f"{self.mapping_kind} mapping has invalid target "
                    f"reference_type: {reference.reference_type}"
                )

    def _validate_reference_status_by_kind(self) -> None:
        if self.mapping_kind in {
            "preset_to_profile",
            "selector_to_task_pool",
        }:
            for reference in [*self.source_refs, *self.target_refs]:
                if reference.reference_status != "resolved_source":
                    raise ValueError(
                        f"{self.mapping_kind} mapping requires resolved_source "
                        f"references: {reference.reference_id}"
                    )

        if self.mapping_kind == "task_to_document":
            for reference in self.source_refs:
                if reference.reference_status != "resolved_source":
                    raise ValueError(
                        "task_to_document source atomic_task must be "
                        f"resolved_source: {reference.reference_id}"
                    )
            for reference in self.target_refs:
                if reference.reference_status == "resolved_source":
                    raise ValueError(
                        "task_to_document document targets must remain future "
                        f"or placeholder references in M27.7: "
                        f"{reference.reference_id}"
                    )

        if self.mapping_kind == "standard_to_template":
            for reference in self.source_refs:
                if reference.reference_status != "resolved_source":
                    raise ValueError(
                        "standard_to_template source standard_bundle must be "
                        f"resolved_source after M28.4: {reference.reference_id}"
                    )

            for reference in self.target_refs:
                if reference.reference_status == "resolved_source":
                    raise ValueError(
                        "standard_to_template template targets must remain future "
                        f"or placeholder references until M29: "
                        f"{reference.reference_id}"
                    )


class MappingLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: MappingSourceStatus = "starter_runtime_source"
    mappings: list[MappingSourceModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_mapping_ids(self):
        mapping_ids: set[str] = set()

        for mapping in self.mappings:
            if mapping.mapping_id in mapping_ids:
                raise ValueError(
                    f"Duplicate mapping_id is not allowed: "
                    f"{mapping.mapping_id}"
                )
            mapping_ids.add(mapping.mapping_id)

        return self
