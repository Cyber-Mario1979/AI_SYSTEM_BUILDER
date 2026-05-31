from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


StandardsIntakeSourceType = Literal[
    "local_standard",
    "company_standard",
    "site_standard",
    "client_standard",
]
StandardsIntakeStatus = Literal[
    "draft_source_record",
    "metadata_captured",
    "authority_decision_pending",
    "approved_internal",
    "recommendation_only",
    "rejected",
]
StandardsAuthorityStatus = Literal[
    "internal",
    "recommendation",
    "draft",
    "tbd",
]
StandardsVerificationStatus = Literal[
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
AuthorityDecisionStatus = Literal[
    "pending_decision",
    "approved_binding_internal",
    "recommendation_only",
    "rejected",
]
ComparisonStatus = Literal[
    "not_required_yet",
    "comparison_required",
    "comparison_completed",
    "override_required",
    "override_completed",
]
ContractStatus = Literal["runtime_facing_contract"]


class StandardsIntakeAuthorityDecisionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_status: AuthorityDecisionStatus
    decision_owner: str | None = Field(default=None, min_length=1)
    decision_reference: str | None = Field(default=None, min_length=1)
    decision_rationale: str | None = Field(default=None, min_length=1)
    residual_limitations: list[str] = Field(default_factory=list)

    @field_validator("residual_limitations")
    @classmethod
    def validate_no_blank_residual_limitations(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards intake decision limitation is not allowed")
        return values

    @model_validator(mode="after")
    def validate_authority_decision_boundary(self):
        if self.decision_status == "approved_binding_internal":
            missing_fields = []
            if self.decision_owner is None:
                missing_fields.append("decision_owner")
            if self.decision_reference is None:
                missing_fields.append("decision_reference")
            if self.decision_rationale is None:
                missing_fields.append("decision_rationale")
            if missing_fields:
                raise ValueError(
                    "Approved internal standards intake decision requires: "
                    f"{', '.join(missing_fields)}"
                )

        if self.decision_status in {"recommendation_only", "rejected"}:
            if self.decision_rationale is None:
                raise ValueError(
                    "Recommendation-only or rejected standards intake decision "
                    "requires decision_rationale"
                )

        return self


class StandardsIntakeComparisonControlModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comparison_status: ComparisonStatus
    applicable_baseline_source_ids: list[str] = Field(default_factory=list)
    comparison_id: str | None = Field(
        default=None,
        pattern=r"^CMP-[A-Z0-9-]+@v[0-9]+$",
    )
    selected_less_strict_than_baseline: bool = False
    override_id: str | None = Field(
        default=None,
        pattern=r"^OVR-[A-Z0-9-]+@v[0-9]+$",
    )
    comparison_limitations: list[str] = Field(default_factory=list)

    @field_validator("applicable_baseline_source_ids", "comparison_limitations")
    @classmethod
    def validate_no_blank_comparison_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards intake comparison value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_comparison_control_boundary(self):
        if self.comparison_status in {
            "comparison_required",
            "comparison_completed",
            "override_required",
            "override_completed",
        }:
            if not self.applicable_baseline_source_ids:
                raise ValueError(
                    "Standards intake comparison requires applicable baseline source IDs"
                )

        if self.comparison_status in {
            "comparison_completed",
            "override_required",
            "override_completed",
        }:
            if self.comparison_id is None:
                raise ValueError(
                    "Completed standards intake comparison requires comparison_id"
                )

        if self.selected_less_strict_than_baseline:
            if self.comparison_status not in {"override_required", "override_completed"}:
                raise ValueError(
                    "Less-strict local/company/site/client selection requires "
                    "override_required or override_completed comparison status"
                )
            if self.comparison_id is None:
                raise ValueError(
                    "Less-strict local/company/site/client selection requires comparison_id"
                )
            if self.comparison_status == "override_completed" and self.override_id is None:
                raise ValueError(
                    "Completed less-strict local/company/site/client selection "
                    "requires override_id"
                )
            if not self.comparison_limitations:
                raise ValueError(
                    "Less-strict local/company/site/client selection requires "
                    "visible comparison limitations"
                )

        if self.comparison_status != "override_completed" and self.override_id is not None:
            raise ValueError(
                "override_id is allowed only when comparison_status is override_completed"
            )

        return self


class StandardsIntakeRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intake_id: str = Field(
        min_length=1,
        pattern=r"^INTAKE-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsIntakeStatus
    std_id: str = Field(
        min_length=1,
        pattern=r"^STD-(LOCAL|COMPANY|SITE|CLIENT)-[A-Z0-9-]+$",
    )
    source_name: str = Field(min_length=1)
    source_type: StandardsIntakeSourceType
    source_owner: str = Field(min_length=1)
    source_location: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    version_or_effective_date: str | None = Field(default=None, min_length=1)
    jurisdiction_or_owner: str | None = Field(default=None, min_length=1)
    applicability_scope: list[str] = Field(min_length=1)
    applicability_conditions: list[str] = Field(default_factory=list)
    citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    authority_decision: StandardsIntakeAuthorityDecisionModel
    comparison_control: StandardsIntakeComparisonControlModel
    may_drive_mandatory_use: bool = False
    limitation_statements: list[str] = Field(default_factory=list)
    public_regulation_claimed: bool = False

    @field_validator(
        "applicability_scope",
        "applicability_conditions",
        "citation_depths",
        "limitation_statements",
    )
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank standards intake record value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_intake_record_boundary(self):
        self._validate_source_prefix_matches_type()
        self._validate_unique_citation_depths()
        self._validate_visible_limitations()
        self._validate_internal_authority_decision_alignment()
        self._validate_mandatory_use_boundary()
        self._validate_comparison_requirement()
        self._validate_no_public_regulation_claim()
        return self

    def requires_visible_limitations(self) -> bool:
        version_is_limited = self.version_or_effective_date is None
        if self.version_or_effective_date is not None:
            version_is_limited = self.version_or_effective_date.strip().upper() == "TBD"

        return (
            self.status
            in {
                "draft_source_record",
                "metadata_captured",
                "authority_decision_pending",
                "recommendation_only",
                "rejected",
            }
            or self.authority_status in {"recommendation", "draft", "tbd"}
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
                "not_mandatory_until_internal_approval",
            }
            or version_is_limited
        )

    def _validate_source_prefix_matches_type(self) -> None:
        expected_prefix_by_type = {
            "local_standard": "STD-LOCAL-",
            "company_standard": "STD-COMPANY-",
            "site_standard": "STD-SITE-",
            "client_standard": "STD-CLIENT-",
        }
        expected_prefix = expected_prefix_by_type[self.source_type]
        if not self.std_id.startswith(expected_prefix):
            raise ValueError(
                "Standards intake source type does not match std_id prefix: "
                f"{self.source_type} -> {self.std_id}"
            )

    def _validate_unique_citation_depths(self) -> None:
        if len(set(self.citation_depths)) != len(self.citation_depths):
            raise ValueError(
                "Duplicate standards intake citation depth is not allowed: "
                f"{self.std_id}"
            )

    def _validate_visible_limitations(self) -> None:
        if self.requires_visible_limitations() and not self.limitation_statements:
            raise ValueError(
                "Limited local/company/site/client standards intake requires "
                f"limitation_statements: {self.std_id}"
            )

    def _validate_internal_authority_decision_alignment(self) -> None:
        decision_status = self.authority_decision.decision_status

        if decision_status == "approved_binding_internal":
            if self.status != "approved_internal":
                raise ValueError(
                    "Approved binding internal decision requires approved_internal "
                    f"intake status: {self.intake_id}"
                )
            if self.authority_status != "internal":
                raise ValueError(
                    "Approved binding internal decision requires internal authority "
                    f"status: {self.std_id}"
                )

        if self.status == "approved_internal" and decision_status != "approved_binding_internal":
            raise ValueError(
                "approved_internal intake status requires approved_binding_internal "
                f"authority decision: {self.intake_id}"
            )

        if self.status == "recommendation_only" and decision_status != "recommendation_only":
            raise ValueError(
                "recommendation_only intake status requires recommendation_only "
                f"authority decision: {self.intake_id}"
            )

        if self.status == "rejected" and decision_status != "rejected":
            raise ValueError(
                "rejected intake status requires rejected authority decision: "
                f"{self.intake_id}"
            )

    def _validate_mandatory_use_boundary(self) -> None:
        if not self.may_drive_mandatory_use:
            return

        if self.authority_decision.decision_status != "approved_binding_internal":
            raise ValueError(
                "Mandatory internal standards intake use requires approved binding "
                f"internal authority decision: {self.intake_id}"
            )

        if self.authority_status != "internal":
            raise ValueError(
                "Mandatory internal standards intake use requires internal authority "
                f"status: {self.std_id}"
            )

        if self.mandatory_flag not in {"mandatory", "mandatory_when_applicable"}:
            raise ValueError(
                "Mandatory internal standards intake use requires mandatory flag: "
                f"{self.std_id}"
            )

    def _validate_comparison_requirement(self) -> None:
        if not self.may_drive_mandatory_use:
            return

        if self.comparison_control.comparison_status not in {
            "comparison_completed",
            "override_required",
            "override_completed",
        }:
            raise ValueError(
                "Mandatory internal standards intake use requires completed "
                f"comparison path: {self.intake_id}"
            )

        if self.comparison_control.comparison_id is None:
            raise ValueError(
                "Mandatory internal standards intake use requires M28.5 comparison_id: "
                f"{self.intake_id}"
            )

    def _validate_no_public_regulation_claim(self) -> None:
        if self.public_regulation_claimed:
            raise ValueError(
                "Local/company/site/client standards intake must not claim public "
                f"regulation status in M28.7: {self.std_id}"
            )


class StandardsIntakeContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_7_STANDARDS_INTAKE_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ContractStatus = "runtime_facing_contract"
    intake_records: list[StandardsIntakeRecordModel] = Field(min_length=1)
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards intake contract value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_intake_records()
        self._validate_unique_std_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_intake_records(self) -> None:
        intake_ids: set[str] = set()
        for record in self.intake_records:
            if record.intake_id in intake_ids:
                raise ValueError(
                    "Duplicate standards intake_id is not allowed: "
                    f"{record.intake_id}"
                )
            intake_ids.add(record.intake_id)

    def _validate_unique_std_ids(self) -> None:
        std_ids: set[str] = set()
        for record in self.intake_records:
            if record.std_id in std_ids:
                raise ValueError(
                    "Duplicate standards intake std_id is not allowed: "
                    f"{record.std_id}"
                )
            std_ids.add(record.std_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_parse_uploaded_standard_files",
            "does_not_mutate_runtime_registry",
            "does_not_verify_public_regulation_status",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)
        if missing_claims:
            raise ValueError(
                "M28.7 standards intake contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
