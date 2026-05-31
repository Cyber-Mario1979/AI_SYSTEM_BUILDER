from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentInputSchemaLibraryStatus = Literal["runtime_facing_document_input_schema_source"]
DocumentInputSchemaRecordStatus = Literal["runtime_facing_document_input_schema_record"]
DocumentInputFieldRequirement = Literal["required", "optional", "conditional"]
DocumentInputValueType = Literal[
    "string",
    "text",
    "boolean",
    "integer",
    "number",
    "date",
    "list",
    "object",
]
DocumentInputRouteRef = Literal["ROUTE-DCF", "ROUTE-SKIP-DCF"]
DocumentInputFieldRouteRef = Literal["ROUTE-DCF", "ROUTE-SKIP-DCF"]
DocumentInputPlaceholderPolicy = Literal[
    "placeholder_required_when_missing",
    "placeholder_allowed_when_missing",
    "placeholder_not_allowed",
]
DocumentInputMissingDataBehavior = Literal[
    "block_until_provided",
    "allow_visible_placeholder",
    "allow_limited_scaffold",
    "review_required",
]
DocumentInputNormalizationRule = Literal[
    "trim_whitespace",
    "collapse_whitespace",
    "preserve_user_text",
    "normalize_identifier",
    "normalize_date_candidate",
    "none",
]

REQUIRED_DOCUMENT_INPUT_SCHEMA_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_draft_document_content",
    "does_not_generate_documents",
    "does_not_validate_final_document_output",
    "does_not_render_or_export_documents",
}


class DocumentInputSchemaFieldModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    display_name: str = Field(min_length=1)
    requirement_status: DocumentInputFieldRequirement
    value_type: DocumentInputValueType
    applies_to_routes: list[DocumentInputFieldRouteRef] = Field(min_length=1)
    placeholder_policy: DocumentInputPlaceholderPolicy
    missing_data_behavior: DocumentInputMissingDataBehavior
    normalization_rules: list[DocumentInputNormalizationRule] = Field(min_length=1)
    source_input_refs: list[str] = Field(default_factory=list)
    section_binding_refs: list[str] = Field(default_factory=list)
    conditional_reason: str | None = Field(default=None, min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator("source_input_refs", "section_binding_refs", "notes")
    @classmethod
    def validate_no_blank_string_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document input schema field value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_field_boundary(self):
        self._validate_unique_route_refs()
        self._validate_unique_normalization_rules()
        self._validate_conditional_reason()
        return self

    def _validate_unique_route_refs(self) -> None:
        if len(set(self.applies_to_routes)) != len(self.applies_to_routes):
            raise ValueError(
                "Duplicate document input field route ref is not allowed: "
                f"{self.field_id}"
            )

    def _validate_unique_normalization_rules(self) -> None:
        if len(set(self.normalization_rules)) != len(self.normalization_rules):
            raise ValueError(
                "Duplicate document input field normalization rule is not allowed: "
                f"{self.field_id}"
            )

    def _validate_conditional_reason(self) -> None:
        if self.requirement_status == "conditional" and self.conditional_reason is None:
            raise ValueError(
                "Conditional document input schema field requires conditional_reason: "
                f"{self.field_id}"
            )


class DocumentInputRouteMappingModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_ref: DocumentInputRouteRef
    field_ids: list[str] = Field(min_length=1)
    mapping_controls: list[str] = Field(min_length=1)

    @field_validator("field_ids", "mapping_controls")
    @classmethod
    def validate_no_blank_route_mapping_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document input route mapping value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_route_mapping_boundary(self):
        if len(set(self.field_ids)) != len(self.field_ids):
            raise ValueError(
                "Duplicate document input route mapping field_id is not allowed: "
                f"{self.route_ref}"
            )
        return self


class DocumentInputSchemaRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputSchemaRecordStatus = "runtime_facing_document_input_schema_record"
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    document_family_id: str = Field(min_length=1, pattern=r"^DOCF-[A-Z0-9-]+$")
    document_type: str = Field(min_length=1)
    required_fields: list[DocumentInputSchemaFieldModel] = Field(min_length=1)
    optional_fields: list[DocumentInputSchemaFieldModel] = Field(default_factory=list)
    conditional_fields: list[DocumentInputSchemaFieldModel] = Field(default_factory=list)
    dcf_intake_mapping: DocumentInputRouteMappingModel
    skip_dcf_minimum_input_mapping: DocumentInputRouteMappingModel
    missing_data_controls: list[str] = Field(min_length=1)
    schema_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "missing_data_controls",
        "schema_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_schema_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document input schema value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_schema_record_boundary(self):
        self._validate_schema_id_version_alignment()
        self._validate_field_requirement_buckets()
        self._validate_unique_field_ids()
        self._validate_route_mapping_roles()
        self._validate_route_mapping_field_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _all_fields(self) -> list[DocumentInputSchemaFieldModel]:
        return [*self.required_fields, *self.optional_fields, *self.conditional_fields]

    def _validate_schema_id_version_alignment(self) -> None:
        if not self.schema_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Document input schema version must match schema_id suffix: "
                f"{self.schema_id} / {self.version}"
            )

    def _validate_field_requirement_buckets(self) -> None:
        bucket_expectations = [
            ("required_fields", self.required_fields, "required"),
            ("optional_fields", self.optional_fields, "optional"),
            ("conditional_fields", self.conditional_fields, "conditional"),
        ]
        for bucket_name, fields, expected_requirement in bucket_expectations:
            for field in fields:
                if field.requirement_status != expected_requirement:
                    raise ValueError(
                        "Document input schema field is in the wrong requirement "
                        f"bucket: {bucket_name} -> {field.field_id}"
                    )

    def _validate_unique_field_ids(self) -> None:
        field_ids: set[str] = set()
        for field in self._all_fields():
            if field.field_id in field_ids:
                raise ValueError(
                    "Duplicate document input schema field_id is not allowed: "
                    f"{field.field_id}"
                )
            field_ids.add(field.field_id)

    def _validate_route_mapping_roles(self) -> None:
        if self.dcf_intake_mapping.route_ref != "ROUTE-DCF":
            raise ValueError("dcf_intake_mapping must use ROUTE-DCF")
        if self.skip_dcf_minimum_input_mapping.route_ref != "ROUTE-SKIP-DCF":
            raise ValueError("skip_dcf_minimum_input_mapping must use ROUTE-SKIP-DCF")

    def _validate_route_mapping_field_ids(self) -> None:
        known_field_ids = {field.field_id for field in self._all_fields()}
        for mapping in [self.dcf_intake_mapping, self.skip_dcf_minimum_input_mapping]:
            unknown_field_ids = sorted(set(mapping.field_ids) - known_field_ids)
            if unknown_field_ids:
                raise ValueError(
                    "Document input route mapping references unknown field_id(s): "
                    f"{mapping.route_ref} -> {', '.join(unknown_field_ids)}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_DOCUMENT_INPUT_SCHEMA_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.4 document input schema is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentInputSchemaLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(
        min_length=1,
        pattern=r"^M29_DOCUMENT_INPUT_SCHEMA_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputSchemaLibraryStatus = "runtime_facing_document_input_schema_source"
    schema_records: list[DocumentInputSchemaRecordModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document input schema library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_schema_library_boundary(self):
        self._validate_unique_schema_ids()
        self._validate_unique_template_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_schema_ids(self) -> None:
        schema_ids: set[str] = set()
        for schema in self.schema_records:
            if schema.schema_id in schema_ids:
                raise ValueError(
                    "Duplicate document input schema id is not allowed: "
                    f"{schema.schema_id}"
                )
            schema_ids.add(schema.schema_id)

    def _validate_unique_template_ids(self) -> None:
        template_ids: set[str] = set()
        for schema in self.schema_records:
            if schema.template_id in template_ids:
                raise ValueError(
                    "Duplicate document input schema template_id is not allowed: "
                    f"{schema.template_id}"
                )
            template_ids.add(schema.template_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_DOCUMENT_INPUT_SCHEMA_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.4 document input schema library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
