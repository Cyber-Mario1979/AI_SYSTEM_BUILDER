from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


StandardsDocumentApplicabilityLibraryStatus = Literal[
    "runtime_facing_document_standards_applicability_source"
]
StandardsDocumentApplicabilityRecordStatus = Literal[
    "runtime_facing_document_standards_applicability_record"
]
StandardsDocumentSourceMode = Literal[
    "asbp_owned_template_body",
    "external_or_adopted_document",
    "vendor_document_extraction_source",
    "lifecycle_route_placeholder",
]
StandardsDocumentApplicabilityStatus = Literal[
    "not_required",
    "document_level_traceability",
    "limited_support_with_visible_limitations",
    "future_verified_support_required",
    "external_or_adopted_source_control",
]
StandardsCitationDepth = Literal[
    "document",
    "version",
    "section",
    "clause",
    "table_row",
    "requirement",
]
StandardsCitationPolicyLibraryStatus = Literal[
    "runtime_facing_document_citation_policy_source"
]
StandardsCitationPolicyRecordStatus = Literal[
    "runtime_facing_document_citation_policy_record"
]
StandardsCitationMode = Literal[
    "none_required",
    "document_level_only",
    "visible_limitation_required",
    "future_verified_support_required",
]


REQUIRED_WAVE6_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_embed_controlled_standards_text",
    "does_not_implement_standards_retrieval_or_embedding",
    "does_not_generate_product_ready_standards_output",
    "does_not_claim_audit_ready_output",
    "does_not_accept_uat",
    "does_not_claim_product_release",
}


class DocumentStandardsApplicabilityRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_ref: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsDocumentApplicabilityRecordStatus = (
        "runtime_facing_document_standards_applicability_record"
    )
    document_type: str = Field(min_length=1)
    source_mode: StandardsDocumentSourceMode
    applicability_status: StandardsDocumentApplicabilityStatus
    standards_bundle_refs: list[str] = Field(default_factory=list)
    std_ids: list[str] = Field(default_factory=list)
    allowed_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    visible_limitation_statements: list[str] = Field(default_factory=list)
    applicability_rationale: str = Field(min_length=1)
    downstream_use_limits: list[str] = Field(min_length=1)
    mandatory_use_allowed: bool = False
    audit_ready_claimed: bool = False
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "standards_bundle_refs",
        "std_ids",
        "visible_limitation_statements",
        "downstream_use_limits",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_strings(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards applicability value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_document_applicability_boundary(self):
        self._validate_references()
        self._validate_citation_depth_boundary()
        self._validate_limited_source_visibility()
        self._validate_external_document_boundary()
        self._validate_no_audit_or_mandatory_claims()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_references(self) -> None:
        for bundle_ref in self.standards_bundle_refs:
            if not bundle_ref.startswith("SB-") or "@v" not in bundle_ref:
                raise ValueError(
                    "Standards bundle refs must use SB-...@v... IDs: "
                    f"{self.document_ref} -> {bundle_ref}"
                )
        if len(set(self.standards_bundle_refs)) != len(self.standards_bundle_refs):
            raise ValueError(
                "Duplicate standards bundle ref is not allowed for document: "
                f"{self.document_ref}"
            )

        for std_id in self.std_ids:
            if not std_id.startswith("STD-"):
                raise ValueError(
                    "Standards source refs must use STD-... IDs: "
                    f"{self.document_ref} -> {std_id}"
                )
        if len(set(self.std_ids)) != len(self.std_ids):
            raise ValueError(
                "Duplicate standards source ref is not allowed for document: "
                f"{self.document_ref}"
            )

        if len(set(self.allowed_citation_depths)) != len(self.allowed_citation_depths):
            raise ValueError(
                "Duplicate allowed citation depth is not allowed for document: "
                f"{self.document_ref}"
            )

    def _validate_citation_depth_boundary(self) -> None:
        blocked_without_verified_source = {"version", "section", "clause"}
        if blocked_without_verified_source.intersection(self.allowed_citation_depths):
            raise ValueError(
                "Wave 6 must not allow version/section/clause citation depth "
                "without verified source evidence: "
                f"{self.document_ref}"
            )

    def _validate_limited_source_visibility(self) -> None:
        if self.applicability_status in {
            "limited_support_with_visible_limitations",
            "future_verified_support_required",
            "external_or_adopted_source_control",
        } and not self.visible_limitation_statements:
            raise ValueError(
                "Limited standards applicability records require visible "
                f"limitation statements: {self.document_ref}"
            )

        if self.std_ids and not self.visible_limitation_statements:
            raise ValueError(
                "Document standards source refs require visible limitation "
                f"statements during Wave 6: {self.document_ref}"
            )

    def _validate_external_document_boundary(self) -> None:
        if self.source_mode in {
            "external_or_adopted_document",
            "vendor_document_extraction_source",
        }:
            if self.applicability_status not in {
                "external_or_adopted_source_control",
                "not_required",
                "document_level_traceability",
            }:
                raise ValueError(
                    "External/vendor documents cannot be treated as ASBP-owned "
                    "standards-backed templates: "
                    f"{self.document_ref}"
                )

    def _validate_no_audit_or_mandatory_claims(self) -> None:
        if self.mandatory_use_allowed:
            raise ValueError(
                "Wave 6 does not allow mandatory-use claims without verified or "
                f"approved internal source evidence: {self.document_ref}"
            )
        if self.audit_ready_claimed:
            raise ValueError(
                "Wave 6 must not claim audit-ready standards output: "
                f"{self.document_ref}"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_WAVE6_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Document standards applicability record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentStandardsApplicabilityMatrixModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    matrix_id: str = Field(
        min_length=1,
        pattern=r"^M29_DOCUMENT_STANDARDS_APPLICABILITY_MATRIX@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsDocumentApplicabilityLibraryStatus = (
        "runtime_facing_document_standards_applicability_source"
    )
    document_records: list[DocumentStandardsApplicabilityRecordModel] = Field(
        min_length=1
    )
    matrix_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("matrix_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_matrix_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards applicability matrix value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_matrix_boundary(self):
        self._validate_unique_document_refs()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_document_refs(self) -> None:
        document_refs: set[str] = set()
        for record in self.document_records:
            if record.document_ref in document_refs:
                raise ValueError(
                    "Duplicate document standards applicability document_ref is "
                    f"not allowed: {record.document_ref}"
                )
            document_refs.add(record.document_ref)

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_WAVE6_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Document standards applicability matrix is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentCitationPolicyRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str = Field(min_length=1, pattern=r"^CITPOL-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsCitationPolicyRecordStatus = (
        "runtime_facing_document_citation_policy_record"
    )
    document_ref: str = Field(min_length=1, pattern=r"^[A-Z0-9]+(?:_[A-Z0-9]+)*$")
    citation_mode: StandardsCitationMode
    default_citation_depth: StandardsCitationDepth = "document"
    permitted_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    blocked_citation_depths: list[StandardsCitationDepth] = Field(default_factory=list)
    limitation_statement_required: bool = True
    source_text_storage_allowed: bool = False
    retrieval_or_embedding_allowed: bool = False
    mandatory_use_allowed: bool = False
    audit_ready_claimed: bool = False
    policy_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "permitted_citation_depths",
        "blocked_citation_depths",
        "policy_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_policy_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank citation policy value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_policy_boundary(self):
        self._validate_policy_id_version_alignment()
        self._validate_citation_depths()
        self._validate_no_productized_standards_claims()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_policy_id_version_alignment(self) -> None:
        if not self.policy_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Citation policy version must match policy_id suffix: "
                f"{self.policy_id} / {self.version}"
            )

    def _validate_citation_depths(self) -> None:
        if len(set(self.permitted_citation_depths)) != len(self.permitted_citation_depths):
            raise ValueError(
                "Duplicate permitted citation depth is not allowed: "
                f"{self.document_ref}"
            )
        if len(set(self.blocked_citation_depths)) != len(self.blocked_citation_depths):
            raise ValueError(
                "Duplicate blocked citation depth is not allowed: "
                f"{self.document_ref}"
            )
        if self.default_citation_depth not in self.permitted_citation_depths:
            raise ValueError(
                "Default citation depth must be permitted: "
                f"{self.document_ref}"
            )

        blocked_without_verified_source = {"version", "section", "clause"}
        if blocked_without_verified_source.intersection(self.permitted_citation_depths):
            raise ValueError(
                "Wave 6 citation policy must not permit version/section/clause "
                "citation without verified source evidence: "
                f"{self.document_ref}"
            )

    def _validate_no_productized_standards_claims(self) -> None:
        if self.source_text_storage_allowed:
            raise ValueError(
                "Wave 6 citation policy must not allow controlled standards text "
                f"storage: {self.document_ref}"
            )
        if self.retrieval_or_embedding_allowed:
            raise ValueError(
                "Wave 6 citation policy must not allow standards retrieval or "
                f"embedding: {self.document_ref}"
            )
        if self.mandatory_use_allowed:
            raise ValueError(
                "Wave 6 citation policy must not allow mandatory-use claims: "
                f"{self.document_ref}"
            )
        if self.audit_ready_claimed:
            raise ValueError(
                "Wave 6 citation policy must not claim audit-ready output: "
                f"{self.document_ref}"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_WAVE6_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Document citation policy record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentCitationPolicyLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_library_id: str = Field(
        min_length=1,
        pattern=r"^M29_DOCUMENT_CITATION_POLICY_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsCitationPolicyLibraryStatus = (
        "runtime_facing_document_citation_policy_source"
    )
    policies: list[DocumentCitationPolicyRecordModel] = Field(min_length=1)
    policy_library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("policy_library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_policy_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank citation policy library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_policy_library_boundary(self):
        self._validate_unique_policy_ids()
        self._validate_unique_document_refs()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_policy_ids(self) -> None:
        policy_ids: set[str] = set()
        for policy in self.policies:
            if policy.policy_id in policy_ids:
                raise ValueError(
                    "Duplicate citation policy id is not allowed: "
                    f"{policy.policy_id}"
                )
            policy_ids.add(policy.policy_id)

    def _validate_unique_document_refs(self) -> None:
        document_refs: set[str] = set()
        for policy in self.policies:
            if policy.document_ref in document_refs:
                raise ValueError(
                    "Duplicate citation policy document_ref is not allowed: "
                    f"{policy.document_ref}"
                )
            document_refs.add(policy.document_ref)

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_WAVE6_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Document citation policy library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
