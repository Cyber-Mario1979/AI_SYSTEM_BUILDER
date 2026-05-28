from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


StandardsApplicabilityTrigger = Literal[
    "registry_presence",
    "gmp_relevance",
    "sterile_nonsterile_scope",
    "cleanroom_scope",
    "room_classification",
    "equipment_type",
    "system_type",
    "computerized_system",
    "electronic_records_or_signatures",
    "process_area",
    "lifecycle_phase",
    "regulatory_market",
    "company_site_client_standard",
    "project_acceptance_criteria",
    "urs_or_design_basis",
    "user_selection",
]

StandardsApplicabilityDecisionState = Literal[
    "applicable",
    "not_applicable",
    "conditional",
    "insufficient_evidence",
    "rejected",
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

ApplicabilityInputSource = Literal[
    "user_input",
    "selector_context",
    "profile_context",
    "source_mapping",
    "registry_record",
    "future_contract",
]

ContractStatus = Literal["runtime_facing_contract"]


class ApplicabilityInputDimensionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension_id: str = Field(
        min_length=1,
        pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$",
    )
    value: str = Field(min_length=1)
    value_source: ApplicabilityInputSource
    notes: str | None = Field(default=None, min_length=1)


class StandardsApplicabilitySourceCandidateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    applicability_scope: list[str] = Field(min_length=1)
    source_limitations: list[str] = Field(default_factory=list)
    internal_approval_reference: str | None = Field(default=None, min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator("applicability_scope", "source_limitations", "notes")
    @classmethod
    def validate_no_blank_source_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards applicability source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_authority_boundary(self):
        if self.requires_visible_limitations() and not self.source_limitations:
            raise ValueError(
                "Source limitations are required for limited standards source "
                f"candidate: {self.std_id}"
            )

        if (
            self.authority_status == "internal"
            and self.mandatory_flag in {"mandatory", "mandatory_when_applicable"}
            and self.verification_status == "not_externally_verifiable"
            and self.internal_approval_reference is None
        ):
            raise ValueError(
                "Internal mandatory standards source candidate requires "
                f"internal_approval_reference: {self.std_id}"
            )

        if (
            self.authority_status
            in {"recommendation", "draft", "retired", "tbd"}
            and self.mandatory_flag in {"mandatory", "mandatory_when_applicable"}
        ):
            raise ValueError(
                "Non-authoritative standards source candidate cannot be mandatory: "
                f"{self.std_id}"
            )

        return self

    def requires_visible_limitations(self) -> bool:
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
        )


class StandardsApplicabilityDecisionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(
        min_length=1,
        pattern=r"^APP-[A-Z0-9-]+@v[0-9]+$",
    )
    standard: StandardsApplicabilitySourceCandidateModel
    applicability_triggers: list[StandardsApplicabilityTrigger] = Field(min_length=1)
    input_dimensions: list[ApplicabilityInputDimensionModel] = Field(default_factory=list)
    decision_state: StandardsApplicabilityDecisionState
    decision_rationale: str = Field(min_length=1)
    mandatory_use_allowed: bool = False
    limitation_statements: list[str] = Field(default_factory=list)
    rejection_cases: list[str] = Field(default_factory=list)
    downstream_use_limits: list[str] = Field(default_factory=list)

    @field_validator(
        "limitation_statements",
        "rejection_cases",
        "downstream_use_limits",
    )
    @classmethod
    def validate_no_blank_decision_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank standards applicability decision value is not allowed"
                )
        return values

    @model_validator(mode="after")
    def validate_applicability_decision_boundary(self):
        self._validate_unique_input_dimensions()
        self._validate_registry_presence_boundary()
        self._validate_required_input_dimensions()
        self._validate_limitation_propagation()
        self._validate_rejection_cases()
        self._validate_mandatory_use_boundary()
        return self

    def _validate_unique_input_dimensions(self) -> None:
        dimension_ids: set[str] = set()

        for dimension in self.input_dimensions:
            if dimension.dimension_id in dimension_ids:
                raise ValueError(
                    "Duplicate applicability input dimension is not allowed: "
                    f"{dimension.dimension_id}"
                )
            dimension_ids.add(dimension.dimension_id)

    def _validate_registry_presence_boundary(self) -> None:
        trigger_set = set(self.applicability_triggers)

        if trigger_set == {"registry_presence"} and self.decision_state in {
            "applicable",
            "conditional",
        }:
            raise ValueError(
                "Registry presence alone cannot make a standard applicable "
                f"or conditional: {self.standard.std_id}"
            )

        if trigger_set == {"registry_presence"} and self.mandatory_use_allowed:
            raise ValueError(
                "Registry presence alone cannot allow mandatory standards use: "
                f"{self.standard.std_id}"
            )

    def _validate_required_input_dimensions(self) -> None:
        if self.decision_state in {"applicable", "conditional"}:
            if not self.input_dimensions:
                raise ValueError(
                    "Applicable or conditional standards decisions require "
                    f"input_dimensions: {self.decision_id}"
                )

    def _validate_limitation_propagation(self) -> None:
        if self.standard.requires_visible_limitations() and not self.limitation_statements:
            raise ValueError(
                "Source limitations must propagate to applicability decision: "
                f"{self.standard.std_id}"
            )

    def _validate_rejection_cases(self) -> None:
        if self.decision_state in {
            "not_applicable",
            "insufficient_evidence",
            "rejected",
        }:
            if self.mandatory_use_allowed:
                raise ValueError(
                    "Non-applicable, insufficient-evidence, or rejected standards "
                    f"decisions cannot allow mandatory use: {self.decision_id}"
                )

            if not self.rejection_cases:
                raise ValueError(
                    "Non-applicable, insufficient-evidence, or rejected standards "
                    f"decisions require rejection_cases: {self.decision_id}"
                )

    def _validate_mandatory_use_boundary(self) -> None:
        if not self.mandatory_use_allowed:
            return

        if self.decision_state != "applicable":
            raise ValueError(
                "Mandatory standards use requires an applicable decision: "
                f"{self.decision_id}"
            )

        if self.standard.authority_status not in {"authoritative", "internal"}:
            raise ValueError(
                "Mandatory standards use requires authoritative or internal "
                f"authority status: {self.standard.std_id}"
            )

        if self.standard.mandatory_flag not in {
            "mandatory",
            "mandatory_when_applicable",
        }:
            raise ValueError(
                "Mandatory standards use requires a mandatory source flag: "
                f"{self.standard.std_id}"
            )

        if self.standard.verification_status == "verified":
            return

        if (
            self.standard.authority_status == "internal"
            and self.standard.verification_status == "not_externally_verifiable"
            and self.standard.internal_approval_reference is not None
        ):
            return

        raise ValueError(
            "Mandatory standards use requires verified source evidence or "
            "approved internal source evidence: "
            f"{self.standard.std_id}"
        )


class StandardsApplicabilityContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_2_STANDARDS_APPLICABILITY_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ContractStatus = "runtime_facing_contract"
    registry_version: str = Field(min_length=1)
    decision_records: list[StandardsApplicabilityDecisionModel] = Field(min_length=1)
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank standards applicability contract value is not allowed"
                )
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_decision_records()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_decision_records(self) -> None:
        decision_ids: set[str] = set()

        for decision in self.decision_records:
            if decision.decision_id in decision_ids:
                raise ValueError(
                    "Duplicate standards applicability decision_id is not allowed: "
                    f"{decision.decision_id}"
                )
            decision_ids.add(decision.decision_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_parse_runtime_registry",
            "does_not_validate_citations",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
        }

        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.2 contract is missing explicit non-implementation claims: "
                f"{', '.join(missing_claims)}"
            )
