from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentTemplateLibraryStatus = Literal["runtime_facing_template_source"]
DocumentTemplateRecordStatus = Literal["runtime_facing_template_record"]
DocumentTemplateLifecycleStatus = Literal["active", "draft", "retired"]
DocumentTemplateSchemaBindingStatus = Literal[
    "schema_binding_pending_m29_4",
    "schema_bound",
]


class DocumentTemplateRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentTemplateRecordStatus = "runtime_facing_template_record"
    lifecycle_status: DocumentTemplateLifecycleStatus = "active"
    display_name: str = Field(min_length=1)
    document_family_id: str = Field(min_length=1, pattern=r"^DOCF-[A-Z0-9-]+$")
    document_type: str = Field(min_length=1)
    source_location: str = Field(min_length=1)
    applicability: list[str] = Field(min_length=1)
    schema_binding_status: DocumentTemplateSchemaBindingStatus
    schema_binding_ref: str = Field(min_length=1)
    standards_bundle_refs: list[str] = Field(default_factory=list)
    intake_route_refs: list[str] = Field(min_length=1)
    template_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "applicability",
        "standards_bundle_refs",
        "intake_route_refs",
        "template_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_list_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_template_record_boundary(self):
        self._validate_template_id_version_alignment()
        self._validate_standards_bundle_refs()
        self._validate_intake_route_refs()
        self._validate_schema_binding_boundary()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_template_id_version_alignment(self) -> None:
        if not self.template_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Template record version must match template_id suffix: "
                f"{self.template_id} / {self.version}"
            )

    def _validate_standards_bundle_refs(self) -> None:
        seen_refs: set[str] = set()

        for bundle_ref in self.standards_bundle_refs:
            if not bundle_ref.startswith("SB-") or "@" not in bundle_ref:
                raise ValueError(
                    "Template standards bundle refs must use SB-...@v... IDs: "
                    f"{bundle_ref}"
                )

            if bundle_ref in seen_refs:
                raise ValueError(
                    "Duplicate template standards bundle ref is not allowed: "
                    f"{self.template_id} -> {bundle_ref}"
                )
            seen_refs.add(bundle_ref)

    def _validate_intake_route_refs(self) -> None:
        allowed_route_refs = {"ROUTE-DCF", "ROUTE-SKIP-DCF"}
        provided_route_refs = set(self.intake_route_refs)
        unknown_route_refs = sorted(provided_route_refs - allowed_route_refs)

        if unknown_route_refs:
            raise ValueError(
                "Document template intake_route_refs include unsupported route(s): "
                f"{', '.join(unknown_route_refs)}"
            )

    def _validate_schema_binding_boundary(self) -> None:
        if (
            self.schema_binding_status == "schema_bound"
            and not self.schema_binding_ref.strip()
        ):
            raise ValueError(
                "Schema-bound template records require schema_binding_ref: "
                f"{self.template_id}"
            )

        if (
            self.schema_binding_status == "schema_binding_pending_m29_4"
            and not self.schema_binding_ref.startswith("SCHEMA-FUTURE-")
        ):
            raise ValueError(
                "M29.2 pending schema bindings must use SCHEMA-FUTURE-* refs "
                f"until M29.4 resolves document input schemas: {self.template_id}"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_select_or_load_templates",
            "does_not_generate_documents",
            "does_not_validate_document_input_schemas",
            "does_not_render_or_export_documents",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M29.2 document template record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentTemplateLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_DOCUMENT_TEMPLATE_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentTemplateLibraryStatus = "runtime_facing_template_source"
    template_records: list[DocumentTemplateRecordModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_template_library_boundary(self):
        self._validate_unique_template_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_template_ids(self) -> None:
        template_ids: set[str] = set()

        for template in self.template_records:
            if template.template_id in template_ids:
                raise ValueError(
                    "Duplicate document template id is not allowed: "
                    f"{template.template_id}"
                )
            template_ids.add(template.template_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_select_or_load_templates",
            "does_not_generate_documents",
            "does_not_validate_document_input_schemas",
            "does_not_render_or_export_documents",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M29.2 document template library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
