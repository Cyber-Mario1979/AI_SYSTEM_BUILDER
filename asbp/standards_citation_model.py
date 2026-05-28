from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


StandardsCitationDepth = Literal[
    "document",
    "version",
    "section",
    "clause",
    "table_row",
    "requirement",
]

StandardsAuthorityStatus = Literal[
    "authoritative",
    "reference",
    "internal",
    "recommendation",
    "draft",
    "retired",
    "tbd",
]

StandardsVerificationStatus = Literal[
    "verified",
    "user_provided",
    "pending_verification",
    "unavailable",
    "not_externally_verifiable",
]

CitationContext = Literal[
    "planning",
    "gap_analysis",
    "source_traceability",
    "cqv_document_future_contract",
    "standards_output_future_contract",
]

CitationLimitationAcceptance = Literal[
    "not_applicable",
    "visible_limitation",
    "explicitly_accepted",
]

ContractStatus = Literal["runtime_facing_contract"]

_CITATION_DEPTH_ORDER: dict[StandardsCitationDepth, int] = {
    "document": 1,
    "version": 2,
    "section": 3,
    "clause": 4,
    "table_row": 4,
    "requirement": 5,
}


class StandardsCitationSourceRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    version_or_effective_date: str | None = Field(default=None, min_length=1)
    available_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    available_section_refs: list[str] = Field(default_factory=list)
    available_clause_refs: list[str] = Field(default_factory=list)
    available_table_rows: list[str] = Field(default_factory=list)
    available_requirement_ids: list[str] = Field(default_factory=list)
    source_limitations: list[str] = Field(default_factory=list)
    source_location: str | None = Field(default=None, min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator(
        "available_section_refs",
        "available_clause_refs",
        "available_table_rows",
        "available_requirement_ids",
        "source_limitations",
        "notes",
    )
    @classmethod
    def validate_no_blank_source_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards citation source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_record_boundary(self):
        self._validate_unique_depths()
        self._validate_depth_supporting_records()
        self._validate_visible_source_limitations()
        return self

    def requires_visible_limitations(self) -> bool:
        version_is_limited = self.version_or_effective_date is None
        if self.version_or_effective_date is not None:
            version_is_limited = self.version_or_effective_date.strip().upper() == "TBD"

        return (
            self.authority_status
            in {"reference", "recommendation", "draft", "retired", "tbd"}
            or self.verification_status
            in {
                "user_provided",
                "pending_verification",
                "unavailable",
                "not_externally_verifiable",
            }
            or version_is_limited
        )

    def _validate_unique_depths(self) -> None:
        if len(set(self.available_citation_depths)) != len(self.available_citation_depths):
            raise ValueError(
                f"Duplicate available citation depth is not allowed: {self.std_id}"
            )

    def _validate_depth_supporting_records(self) -> None:
        if "section" in self.available_citation_depths and not self.available_section_refs:
            raise ValueError(
                "Section citation depth requires available_section_refs: "
                f"{self.std_id}"
            )

        if "clause" in self.available_citation_depths and not self.available_clause_refs:
            raise ValueError(
                "Clause citation depth requires available_clause_refs: "
                f"{self.std_id}"
            )

        if "table_row" in self.available_citation_depths and not self.available_table_rows:
            raise ValueError(
                "Table-row citation depth requires available_table_rows: "
                f"{self.std_id}"
            )

        if (
            "requirement" in self.available_citation_depths
            and not self.available_requirement_ids
        ):
            raise ValueError(
                "Requirement citation depth requires available_requirement_ids: "
                f"{self.std_id}"
            )

    def _validate_visible_source_limitations(self) -> None:
        if self.requires_visible_limitations() and not self.source_limitations:
            raise ValueError(
                "Limited standards citation source requires source_limitations: "
                f"{self.std_id}"
            )


class StandardsCitationReferenceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    citation_level: StandardsCitationDepth
    requested_citation_depth: StandardsCitationDepth | None = None
    version_or_effective_date: str | None = Field(default=None, min_length=1)
    section_ref: str | None = Field(default=None, min_length=1)
    clause_ref: str | None = Field(default=None, min_length=1)
    table_id: str | None = Field(default=None, min_length=1)
    row_id: str | None = Field(default=None, min_length=1)
    requirement_id: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_reference_shape(self):
        if self.requested_citation_depth is None:
            self.requested_citation_depth = self.citation_level

        if self.citation_level == "version" and self.version_or_effective_date is None:
            raise ValueError("Version-level citation requires version_or_effective_date")

        if self.citation_level == "section" and self.section_ref is None:
            raise ValueError("Section-level citation requires section_ref")

        if self.citation_level == "clause" and self.clause_ref is None:
            raise ValueError("Clause-level citation requires clause_ref")

        if self.citation_level == "table_row":
            if self.table_id is None or self.row_id is None:
                raise ValueError("Table-row citation requires table_id and row_id")

        if self.citation_level == "requirement" and self.requirement_id is None:
            raise ValueError("Requirement-level citation requires requirement_id")

        return self


class StandardsCitationRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    citation_id: str = Field(
        min_length=1,
        pattern=r"^CIT-[A-Z0-9-]+@v[0-9]+$",
    )
    source: StandardsCitationSourceRecordModel
    reference: StandardsCitationReferenceModel
    applicability_decision_id: str | None = Field(
        default=None,
        pattern=r"^APP-[A-Z0-9-]+@v[0-9]+$",
    )
    citation_context: CitationContext
    limitation_statements: list[str] = Field(default_factory=list)
    limitation_acceptance: CitationLimitationAcceptance = "not_applicable"
    audit_ready_claimed: bool = False
    source_text_claim: str | None = Field(default=None, min_length=1)
    regulatory_meaning_claim: str | None = Field(default=None, min_length=1)
    downstream_use_limits: list[str] = Field(default_factory=list)

    @field_validator("limitation_statements", "downstream_use_limits")
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards citation record value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_citation_record_boundary(self):
        self._validate_no_fabricated_source_content()
        self._validate_citation_depth_is_available()
        self._validate_visible_limitations_for_limited_sources()
        self._validate_audit_ready_boundary()
        self._validate_exact_reference_support()
        self._validate_missing_requested_depth_limitations()
        return self

    def _has_visible_limitation_acceptance(self) -> bool:
        return self.limitation_acceptance in {
            "visible_limitation",
            "explicitly_accepted",
        }

    def _validate_no_fabricated_source_content(self) -> None:
        if self.source_text_claim is not None:
            raise ValueError(
                "M28.3 citation records must not carry source text claims: "
                f"{self.citation_id}"
            )

        if self.regulatory_meaning_claim is not None:
            raise ValueError(
                "M28.3 citation records must not carry regulatory meaning claims: "
                f"{self.citation_id}"
            )

    def _validate_citation_depth_is_available(self) -> None:
        if self.reference.citation_level not in self.source.available_citation_depths:
            raise ValueError(
                "Citation depth is not available for source record: "
                f"{self.source.std_id} -> {self.reference.citation_level}"
            )

    def _validate_visible_limitations_for_limited_sources(self) -> None:
        if not self.source.requires_visible_limitations():
            return

        if not self.limitation_statements or not self._has_visible_limitation_acceptance():
            raise ValueError(
                "Limited standards sources require visible citation limitations: "
                f"{self.source.std_id}"
            )

    def _validate_audit_ready_boundary(self) -> None:
        if not self.audit_ready_claimed:
            return

        if self.source.requires_visible_limitations():
            raise ValueError(
                "Audit-ready citation is not allowed for limited standards source: "
                f"{self.source.std_id}"
            )

        if self.source.verification_status != "verified":
            raise ValueError(
                "Audit-ready citation requires verified source evidence: "
                f"{self.source.std_id}"
            )

        if self.reference.citation_level in {"section", "clause"}:
            self._validate_section_or_clause_verified()

    def _validate_exact_reference_support(self) -> None:
        if self.reference.citation_level == "section":
            if self.source.verification_status != "verified":
                raise ValueError(
                    "Section-level citation requires verified source evidence: "
                    f"{self.source.std_id}"
                )

            if self.reference.section_ref not in self.source.available_section_refs:
                raise ValueError(
                    "Section-level citation requires an available verified section "
                    f"reference: {self.reference.section_ref}"
                )

        if self.reference.citation_level == "clause":
            self._validate_section_or_clause_verified()

        if self.reference.citation_level == "table_row":
            if self.reference.row_id not in self.source.available_table_rows:
                raise ValueError(
                    "Table-row citation requires an available table row reference: "
                    f"{self.reference.row_id}"
                )

        if self.reference.citation_level == "requirement":
            if self.reference.requirement_id not in self.source.available_requirement_ids:
                raise ValueError(
                    "Requirement-level citation requires an available requirement "
                    f"reference: {self.reference.requirement_id}"
                )

    def _validate_section_or_clause_verified(self) -> None:
        if self.source.verification_status != "verified":
            raise ValueError(
                "Clause-level citation requires verified source evidence: "
                f"{self.source.std_id}"
            )

        if self.reference.clause_ref not in self.source.available_clause_refs:
            raise ValueError(
                "Clause-level citation requires an available verified clause "
                f"reference: {self.reference.clause_ref}"
            )

    def _validate_missing_requested_depth_limitations(self) -> None:
        requested_depth = self.reference.requested_citation_depth
        if requested_depth is None:
            return

        requested_order = _CITATION_DEPTH_ORDER[requested_depth]
        actual_order = _CITATION_DEPTH_ORDER[self.reference.citation_level]

        if requested_order <= actual_order:
            return

        if not self.limitation_statements or not self._has_visible_limitation_acceptance():
            raise ValueError(
                "Missing requested citation depth requires visible limitation: "
                f"{self.citation_id}"
            )


class StandardsCitationContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_3_STANDARDS_CITATION_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ContractStatus = "runtime_facing_contract"
    registry_version: str = Field(min_length=1)
    citation_records: list[StandardsCitationRecordModel] = Field(min_length=1)
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards citation contract value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_citation_records()
        self._validate_registry_version_traceability()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_citation_records(self) -> None:
        citation_ids: set[str] = set()

        for citation_record in self.citation_records:
            if citation_record.citation_id in citation_ids:
                raise ValueError(
                    "Duplicate standards citation_id is not allowed: "
                    f"{citation_record.citation_id}"
                )
            citation_ids.add(citation_record.citation_id)

    def _validate_registry_version_traceability(self) -> None:
        for citation_record in self.citation_records:
            if citation_record.source.registry_version != self.registry_version:
                raise ValueError(
                    "Citation record registry_version must match contract "
                    f"registry_version: {citation_record.citation_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_parse_runtime_registry",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
            "does_not_claim_audit_ready_clause_authority",
            "does_not_store_or_fabricate_source_text",
            "does_not_interpret_regulatory_meaning",
            "does_not_close_ddr_005_or_ddr_006",
        }

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.3 contract is missing explicit non-implementation claims: "
                f"{', '.join(missing_claims)}"
            )
