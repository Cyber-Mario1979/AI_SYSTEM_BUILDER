from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentTemplateBodyLibraryStatus = Literal["mvp_template_body_source"]
DocumentTemplateBodyRecordStatus = Literal["mvp_template_body_record"]
TemplateBodyKind = Literal[
    "authored_template",
    "protocol_template",
    "report_template",
    "matrix_template",
    "external_reference_plan",
    "data_extraction_plan",
    "certificate_record_plan",
    "form_template",
    "checklist_template",
]
TemplateBodyOutputRole = Literal[
    "planning",
    "requirements",
    "risk",
    "traceability",
    "design",
    "commissioning",
    "qualification",
    "deviation_capa",
    "closeout",
    "external_source",
    "certificate",
    "decommissioning",
    "change_control",
]
TemplateBodyPriority = Literal["P0", "P1", "P2"]
TemplateBodyMvpStatus = Literal[
    "must_have",
    "conditional_must_have",
    "source_only",
    "external_vendor_provided",
    "certificate_record",
    "route_gap",
]
TemplateSectionRequirementStatus = Literal["required", "conditional", "optional"]


REQUIRED_TEMPLATE_BODY_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_generate_documents",
    "does_not_create_signed_or_approved_records",
    "does_not_replace_human_review",
    "does_not_claim_product_release",
}


class DocumentTemplateTableModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_id: str = Field(min_length=1, pattern=r"^TBL-[A-Z0-9-]+$")
    title: str = Field(min_length=1)
    columns: list[str] = Field(min_length=1)

    @field_validator("columns")
    @classmethod
    def validate_no_blank_columns(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template table column is not allowed")
        return values


class DocumentTemplateSectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1, pattern=r"^SEC-[A-Z0-9-]+$")
    title: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    requirement_status: TemplateSectionRequirementStatus = "required"
    expected_content_types: list[str] = Field(min_length=1)
    source_input_refs: list[str] = Field(default_factory=list)
    downstream_refs: list[str] = Field(default_factory=list)
    section_controls: list[str] = Field(min_length=1)

    @field_validator(
        "expected_content_types",
        "source_input_refs",
        "downstream_refs",
        "section_controls",
    )
    @classmethod
    def validate_no_blank_section_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template section value is not allowed")
        return values


class DocumentTemplateBodyRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body_id: str = Field(min_length=1, pattern=r"^TBODY-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentTemplateBodyRecordStatus = "mvp_template_body_record"
    document_ref: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*$")
    display_name: str = Field(min_length=1)
    template_body_kind: TemplateBodyKind
    output_role: TemplateBodyOutputRole
    priority: TemplateBodyPriority
    mvp_status: TemplateBodyMvpStatus
    linked_template_id: str | None = Field(default=None, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    linked_schema_id: str | None = Field(default=None, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    source_structure_references: list[str] = Field(min_length=1)
    owner_review_required: bool = True
    sections: list[DocumentTemplateSectionModel] = Field(min_length=1)
    tables: list[DocumentTemplateTableModel] = Field(default_factory=list)
    template_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "source_structure_references",
        "template_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_body_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template body value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_template_body_record_boundary(self):
        self._validate_body_id_version_alignment()
        self._validate_unique_sections()
        self._validate_unique_tables()
        self._validate_required_non_implementation_claims()
        self._validate_external_kind_boundary()
        return self

    def _validate_body_id_version_alignment(self) -> None:
        if not self.body_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Document template body version must match body_id suffix: "
                f"{self.body_id} / {self.version}"
            )

    def _validate_unique_sections(self) -> None:
        section_ids: set[str] = set()
        for section in self.sections:
            if section.section_id in section_ids:
                raise ValueError(
                    "Duplicate document template section_id is not allowed: "
                    f"{self.body_id} -> {section.section_id}"
                )
            section_ids.add(section.section_id)

    def _validate_unique_tables(self) -> None:
        table_ids: set[str] = set()
        for table in self.tables:
            if table.table_id in table_ids:
                raise ValueError(
                    "Duplicate document template table_id is not allowed: "
                    f"{self.body_id} -> {table.table_id}"
                )
            table_ids.add(table.table_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TEMPLATE_BODY_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Wave 4 template body record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )

    def _validate_external_kind_boundary(self) -> None:
        if self.template_body_kind in {"external_reference_plan", "data_extraction_plan"}:
            if self.linked_template_id is not None:
                raise ValueError(
                    "External/data-extraction template body records must not link to "
                    f"authored template records: {self.body_id}"
                )


class DocumentTemplateBodyLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(
        min_length=1,
        pattern=r"^M29_DOCUMENT_TEMPLATE_BODY_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentTemplateBodyLibraryStatus = "mvp_template_body_source"
    source_authority: str = Field(min_length=1)
    body_records: list[DocumentTemplateBodyRecordModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document template body library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_template_body_library_boundary(self):
        self._validate_unique_body_ids()
        self._validate_unique_document_refs()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_body_ids(self) -> None:
        body_ids: set[str] = set()
        for body_record in self.body_records:
            if body_record.body_id in body_ids:
                raise ValueError(
                    "Duplicate document template body_id is not allowed: "
                    f"{body_record.body_id}"
                )
            body_ids.add(body_record.body_id)

    def _validate_unique_document_refs(self) -> None:
        document_refs: set[str] = set()
        for body_record in self.body_records:
            if body_record.document_ref in document_refs:
                raise ValueError(
                    "Duplicate document template document_ref is not allowed: "
                    f"{body_record.document_ref}"
                )
            document_refs.add(body_record.document_ref)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TEMPLATE_BODY_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Wave 4 template body library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
