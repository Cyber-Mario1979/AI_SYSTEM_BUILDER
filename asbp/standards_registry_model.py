from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


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

StandardsMandatoryFlag = Literal[
    "mandatory",
    "mandatory_when_applicable",
    "not_mandatory",
    "not_mandatory_unless_adopted",
    "not_mandatory_unless_adopted_or_required",
    "not_mandatory_until_internal_approval",
]

StandardsCitationDepth = Literal[
    "document",
    "version",
    "section",
    "clause",
    "table_row",
    "requirement",
]

StandardsRegistrySourceStatus = Literal["runtime_registry_source"]
StandardsRegistryApprovalStatus = Literal["approved_source_authority_model"]


class StandardsRegistrySourceRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    source_name: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    version_or_effective_date: str = Field(min_length=1)
    jurisdiction_or_owner: str = Field(min_length=1)
    applicability_scope: list[str] = Field(min_length=1)
    applicability_conditions: list[str] = Field(default_factory=list)
    citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    source_location: str | None = Field(default=None, min_length=1)
    mandatory_flag: StandardsMandatoryFlag
    source_limitations: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    internal_approval_reference: str | None = Field(default=None, min_length=1)

    @field_validator(
        "applicability_scope",
        "applicability_conditions",
        "source_limitations",
        "notes",
    )
    @classmethod
    def validate_no_blank_list_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards registry source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_record_boundary(self):
        self._validate_unique_citation_depths()
        self._validate_verified_version_boundary()
        self._validate_citation_depth_boundary()
        self._validate_visible_limitations()
        self._validate_mandatory_flag_boundary()
        return self

    def requires_visible_limitations(self) -> bool:
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
            or self.mandatory_flag
            in {
                "not_mandatory",
                "not_mandatory_unless_adopted",
                "not_mandatory_unless_adopted_or_required",
                "not_mandatory_until_internal_approval",
            }
            or version_is_limited
        )

    def can_support_mandatory_use(self) -> bool:
        if self.authority_status not in {"authoritative", "internal"}:
            return False

        if self.mandatory_flag not in {"mandatory", "mandatory_when_applicable"}:
            return False

        if self.verification_status == "verified":
            return True

        return (
            self.authority_status == "internal"
            and self.verification_status == "not_externally_verifiable"
            and self.internal_approval_reference is not None
        )

    def _validate_unique_citation_depths(self) -> None:
        if len(set(self.citation_depths)) != len(self.citation_depths):
            raise ValueError(
                "Duplicate standards registry citation depth is not allowed: "
                f"{self.std_id}"
            )

    def _validate_visible_limitations(self) -> None:
        if self.requires_visible_limitations() and not self.source_limitations:
            raise ValueError(
                "Limited standards registry source requires source_limitations: "
                f"{self.std_id}"
            )

    def _validate_verified_version_boundary(self) -> None:
        if (
            self.verification_status == "verified"
            and self.version_or_effective_date.strip().upper() == "TBD"
        ):
            raise ValueError(
                "Verified standards registry source cannot have TBD version or "
                f"effective date: {self.std_id}"
            )

    def _validate_citation_depth_boundary(self) -> None:
        if (
            self.version_or_effective_date.strip().upper() == "TBD"
            and "version" in self.citation_depths
        ):
            raise ValueError(
                "Version-level citation requires known version or effective date: "
                f"{self.std_id}"
            )

        if self.verification_status == "verified":
            return

        if any(depth in {"section", "clause"} for depth in self.citation_depths):
            raise ValueError(
                "Section or clause citation depth requires verified source evidence: "
                f"{self.std_id}"
            )

    def _validate_mandatory_flag_boundary(self) -> None:
        if self.mandatory_flag not in {"mandatory", "mandatory_when_applicable"}:
            return

        if self.authority_status in {"authoritative", "internal"}:
            return

        raise ValueError(
            "Mandatory registry source flag requires authoritative or internal "
            f"authority status: {self.std_id}"
        )


class StandardsRegistryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    registry_id: str = Field(
        min_length=1,
        pattern=r"^STANDARDS_SOURCE_REGISTRY@v[0-9]+(?:\.[0-9]+)?$",
    )
    registry_version: str = Field(min_length=1)
    status: StandardsRegistrySourceStatus = "runtime_registry_source"
    approval_status: StandardsRegistryApprovalStatus = "approved_source_authority_model"
    source_authority_reference: str = Field(min_length=1)
    source_records: list[StandardsRegistrySourceRecordModel] = Field(min_length=1)
    registry_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("registry_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_registry_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards registry value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_registry_boundary(self):
        self._validate_unique_source_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_source_ids(self) -> None:
        source_ids: set[str] = set()

        for source in self.source_records:
            if source.std_id in source_ids:
                raise ValueError(
                    "Duplicate standards registry source id is not allowed: "
                    f"{source.std_id}"
                )
            source_ids.add(source.std_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_embed_controlled_standards_text",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
            "does_not_verify_public_regulatory_meaning",
        }

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.8 runtime standards registry is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
