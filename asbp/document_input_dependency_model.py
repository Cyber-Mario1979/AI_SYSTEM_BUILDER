from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentInputContractStatus = Literal["mvp_runtime_source"]
DcfDomain = Literal[
    "cleanroom_hvac",
    "process_equipment",
    "utilities",
    "computerized_systems",
]
DcfFieldRequirement = Literal["required", "optional", "conditional"]
DcfValueType = Literal[
    "string",
    "text",
    "boolean",
    "integer",
    "number",
    "date",
    "list",
    "table",
]
DocumentInputMode = Literal[
    "urs_dcf_intake",
    "template_fill_project_context",
    "derived_from_upstream_documents",
    "external_adopted_source",
    "vendor_document_extraction_source",
    "execution_triggered_record",
]
DocumentDependencyInputSource = Literal[
    "DCF_URS_INTAKE",
    "CCF",
    "VMP",
    "SIA",
    "URS",
    "VENDOR_DOCS",
    "RA_FMEA",
    "URS_DEVIATION_LIST",
    "RTM",
    "DQ",
    "CP",
    "QP",
    "FAT_PROTOCOL_REPORT",
    "A0_CERTIFICATE",
    "CTOP",
    "A1_CERTIFICATE",
    "SAT_PROTOCOL_REPORT",
    "CR",
    "A2_CERTIFICATE",
    "IQ_PROTOCOL_REPORT",
    "OQ_PROTOCOL_REPORT",
    "PQ_PROTOCOL_REPORT",
    "DEVIATION_INCIDENT_REPORT",
    "CAPA_CLOSURE_FORM",
    "VSR",
    "TASK_POOLS",
    "PROFILES",
    "MAPPINGS",
    "STANDARDS_BUNDLE_LIMITATIONS",
    "HUMAN_REVIEW",
]
VendorDocumentType = Literal[
    "FDS",
    "SDS",
    "P_AND_ID",
    "MANUAL",
    "DRAWING",
    "CERTIFICATE",
    "DATASHEET",
    "VENDOR_REPORT",
]

REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_generate_documents",
    "does_not_create_uat_acceptance",
    "does_not_approve_release_or_productize",
    "does_not_replace_human_review",
}


class DcfFieldGroupModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1, pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    display_name: str = Field(min_length=1)
    source_section_label: str = Field(min_length=1)
    group_controls: list[str] = Field(min_length=1)

    @field_validator("group_controls")
    @classmethod
    def validate_no_blank_group_controls(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank DCF group control is not allowed")
        return values


class DcfFieldModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    display_name: str = Field(min_length=1)
    group_id: str = Field(min_length=1, pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    requirement_status: DcfFieldRequirement
    value_type: DcfValueType
    source_table_label: str = Field(min_length=1)
    target_urs_section_refs: list[str] = Field(min_length=1)
    extraction_notes: list[str] = Field(default_factory=list)

    @field_validator("target_urs_section_refs", "extraction_notes")
    @classmethod
    def validate_no_blank_field_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank DCF field value is not allowed")
        return values


class UrsDcfIntakeRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dcf_id: str = Field(min_length=1, pattern=r"^DCF-URS-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    domain: DcfDomain
    display_name: str = Field(min_length=1)
    source_file_name: str = Field(min_length=1)
    target_document_ref: Literal["URS"] = "URS"
    target_template_body_ref: str = Field(min_length=1, pattern=r"^TPLBODY-[A-Z0-9-]+@v[0-9]+$")
    supported_asset_scope: list[str] = Field(min_length=1)
    field_groups: list[DcfFieldGroupModel] = Field(min_length=1)
    fields: list[DcfFieldModel] = Field(min_length=1)
    dcf_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "supported_asset_scope",
        "dcf_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank URS DCF intake value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_dcf_record_boundary(self):
        self._validate_version_alignment()
        self._validate_unique_groups_and_fields()
        self._validate_group_references()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_version_alignment(self) -> None:
        if not self.dcf_id.endswith(f"@{self.version}"):
            raise ValueError(
                "URS DCF record version must match dcf_id suffix: "
                f"{self.dcf_id} / {self.version}"
            )

    def _validate_unique_groups_and_fields(self) -> None:
        group_ids = [group.group_id for group in self.field_groups]
        if len(set(group_ids)) != len(group_ids):
            raise ValueError(f"Duplicate DCF field group is not allowed: {self.dcf_id}")

        field_ids = [field.field_id for field in self.fields]
        if len(set(field_ids)) != len(field_ids):
            raise ValueError(f"Duplicate DCF field_id is not allowed: {self.dcf_id}")

    def _validate_group_references(self) -> None:
        known_group_ids = {group.group_id for group in self.field_groups}
        for field in self.fields:
            if field.group_id not in known_group_ids:
                raise ValueError(
                    "DCF field references unknown group_id: "
                    f"{self.dcf_id}::{field.field_id}->{field.group_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "URS DCF intake record is missing explicit non-implementation "
                f"claims: {', '.join(missing_claims)}"
            )


class UrsDcfIntakeCatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    catalog_id: str = Field(min_length=1, pattern=r"^M29_URS_DCF_INTAKE_CATALOG@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    dcf_records: list[UrsDcfIntakeRecordModel] = Field(min_length=1)
    catalog_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("catalog_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_catalog_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank URS DCF catalog value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_catalog_boundary(self):
        dcf_ids = [record.dcf_id for record in self.dcf_records]
        if len(set(dcf_ids)) != len(dcf_ids):
            raise ValueError("Duplicate URS DCF record id is not allowed")

        domains = [record.domain for record in self.dcf_records]
        if len(set(domains)) != len(domains):
            raise ValueError("Duplicate URS DCF domain is not allowed")

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "URS DCF intake catalog is missing explicit non-implementation "
                f"claims: {', '.join(missing_claims)}"
            )
        return self


class DocumentDependencyContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(min_length=1, pattern=r"^DOCCONTRACT-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    document_ref: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*$")
    display_name: str = Field(min_length=1)
    input_mode: DocumentInputMode
    uses_dcf: bool
    upstream_input_sources: list[DocumentDependencyInputSource] = Field(min_length=1)
    target_template_body_ref: str | None = Field(default=None, pattern=r"^TPLBODY-[A-Z0-9-]+@v[0-9]+$")
    derivation_controls: list[str] = Field(min_length=1)
    blocking_conditions: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "upstream_input_sources",
        "derivation_controls",
        "blocking_conditions",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_dependency_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank document dependency contract value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_dependency_contract_boundary(self):
        self._validate_version_alignment()
        self._validate_dcf_scope()
        self._validate_external_boundaries()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_version_alignment(self) -> None:
        if not self.contract_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Document dependency contract version must match contract_id suffix: "
                f"{self.contract_id} / {self.version}"
            )

    def _validate_dcf_scope(self) -> None:
        if self.document_ref == "URS":
            if not self.uses_dcf:
                raise ValueError("URS dependency contract must use URS DCF intake")
            if self.input_mode != "urs_dcf_intake":
                raise ValueError("URS dependency contract must use urs_dcf_intake mode")
            if "DCF_URS_INTAKE" not in self.upstream_input_sources:
                raise ValueError("URS dependency contract must include DCF_URS_INTAKE")
            return

        if self.uses_dcf:
            raise ValueError(
                "Only URS may use DCF intake in Wave 5: "
                f"{self.document_ref}"
            )
        if "DCF_URS_INTAKE" in self.upstream_input_sources:
            raise ValueError(
                "Downstream documents must depend on URS, not raw DCF intake: "
                f"{self.document_ref}"
            )

    def _validate_external_boundaries(self) -> None:
        if self.input_mode == "external_adopted_source" and self.target_template_body_ref is not None:
            raise ValueError(
                "External/adopted documents must not require an ASBP-owned template body: "
                f"{self.document_ref}"
            )

        if self.input_mode == "vendor_document_extraction_source" and self.document_ref != "VENDOR_DOCS":
            raise ValueError(
                "Vendor extraction source contract must use VENDOR_DOCS document_ref"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Document dependency contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentDependencyContractLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_DOCUMENT_DEPENDENCY_CONTRACT_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    dependency_contracts: list[DocumentDependencyContractModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document dependency library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_dependency_library_boundary(self):
        contract_ids = [contract.contract_id for contract in self.dependency_contracts]
        if len(set(contract_ids)) != len(contract_ids):
            raise ValueError("Duplicate document dependency contract id is not allowed")

        document_refs = [contract.document_ref for contract in self.dependency_contracts]
        if len(set(document_refs)) != len(document_refs):
            raise ValueError("Duplicate document dependency document_ref is not allowed")

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Document dependency library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
        return self


class VendorDocumentExtractionSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1, pattern=r"^VENDOR-SOURCE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    vendor_document_type: VendorDocumentType
    display_name: str = Field(min_length=1)
    extraction_targets: list[str] = Field(min_length=1)
    extraction_fields: list[str] = Field(min_length=1)
    extraction_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "extraction_targets",
        "extraction_fields",
        "extraction_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_vendor_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank vendor extraction source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_vendor_source_boundary(self):
        if not self.source_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Vendor document extraction source version must match source_id suffix: "
                f"{self.source_id} / {self.version}"
            )

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Vendor extraction source is missing explicit non-implementation "
                f"claims: {', '.join(missing_claims)}"
            )
        return self


class VendorDocumentExtractionLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_VENDOR_DOCUMENT_EXTRACTION_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentInputContractStatus = "mvp_runtime_source"
    vendor_sources: list[VendorDocumentExtractionSourceModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_vendor_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank vendor extraction library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_vendor_library_boundary(self):
        source_ids = [source.source_id for source in self.vendor_sources]
        if len(set(source_ids)) != len(source_ids):
            raise ValueError("Duplicate vendor extraction source id is not allowed")

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_WAVE5_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "Vendor extraction library is missing explicit non-implementation "
                f"claims: {', '.join(missing_claims)}"
            )
        return self
