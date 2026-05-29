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

RequirementApplicabilityState = Literal[
    "applicable",
    "conditional",
    "not_applicable",
    "insufficient_evidence",
    "rejected",
]

RequirementComparisonBasis = Literal[
    "numeric_limit",
    "mandatory_scope",
    "acceptance_criteria",
    "test_frequency_or_duration",
    "classification_or_grade",
    "qualitative_control",
    "manual_decision",
]

RequirementComparisonOutcome = Literal[
    "select_stricter_requirement",
    "select_less_strict_with_override",
]

ContractStatus = Literal["runtime_facing_contract"]


class StandardsComparedRequirementModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_id: str = Field(
        min_length=1,
        pattern=r"^REQ-[A-Z0-9-]+@v[0-9]+$",
    )
    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    requirement_reference: str = Field(min_length=1)
    requirement_summary: str = Field(min_length=1)
    applicability_decision_id: str | None = Field(
        default=None,
        pattern=r"^APP-[A-Z0-9-]+@v[0-9]+$",
    )
    applicability_state: RequirementApplicabilityState
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    mandatory_use_allowed: bool = False
    comparison_basis: RequirementComparisonBasis
    strictness_rank: int = Field(ge=0, le=100)
    strictness_rationale: str = Field(min_length=1)
    limitation_statements: list[str] = Field(default_factory=list)
    internal_approval_reference: str | None = Field(default=None, min_length=1)

    @field_validator("limitation_statements")
    @classmethod
    def validate_no_blank_limitation_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank standards requirement limitation is not allowed"
                )
        return values

    @model_validator(mode="after")
    def validate_requirement_boundary(self):
        self._validate_visible_limitations()
        self._validate_mandatory_use_boundary()
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

    def _validate_visible_limitations(self) -> None:
        if self.requires_visible_limitations() and not self.limitation_statements:
            raise ValueError(
                "Limited standards comparison requirement requires "
                f"limitation_statements: {self.requirement_id}"
            )

    def _validate_mandatory_use_boundary(self) -> None:
        if not self.mandatory_use_allowed:
            return

        if self.applicability_state != "applicable":
            raise ValueError(
                "Mandatory standards comparison requires an applicable source: "
                f"{self.requirement_id}"
            )

        if self.authority_status not in {"authoritative", "internal"}:
            raise ValueError(
                "Mandatory standards comparison requires authoritative or internal "
                f"authority status: {self.requirement_id}"
            )

        if self.mandatory_flag not in {"mandatory", "mandatory_when_applicable"}:
            raise ValueError(
                "Mandatory standards comparison requires a mandatory source flag: "
                f"{self.requirement_id}"
            )

        if self.verification_status == "verified":
            return

        if (
            self.authority_status == "internal"
            and self.verification_status == "not_externally_verifiable"
            and self.internal_approval_reference is not None
        ):
            return

        raise ValueError(
            "Mandatory standards comparison requires verified source evidence or "
            f"approved internal source evidence: {self.requirement_id}"
        )


class StandardsRequirementComparisonRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comparison_id: str = Field(
        min_length=1,
        pattern=r"^CMP-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    comparison_scope: str = Field(min_length=1)
    compared_requirements: list[StandardsComparedRequirementModel] = Field(
        min_length=2
    )
    stricter_requirement_id: str = Field(min_length=1)
    selected_requirement_id: str = Field(min_length=1)
    comparison_outcome: RequirementComparisonOutcome
    comparison_controls: list[str] = Field(min_length=1)
    limitation_statements: list[str] = Field(default_factory=list)
    risk_based_rationale: str | None = Field(default=None, min_length=1)
    override_path_reference: str | None = Field(default=None, min_length=1)
    override_limitation_statement: str | None = Field(default=None, min_length=1)

    @field_validator("comparison_controls", "limitation_statements")
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank standards requirement comparison value is not allowed"
                )
        return values

    @model_validator(mode="after")
    def validate_comparison_record_boundary(self):
        self._validate_unique_requirement_ids()
        self._validate_selected_and_stricter_ids_exist()
        self._validate_stricter_requirement_matches_rank()
        self._validate_selection_and_override_path()
        self._validate_limited_requirement_propagation()
        return self

    def _requirement_ids(self) -> set[str]:
        return {requirement.requirement_id for requirement in self.compared_requirements}

    def _requirement_by_id(self, requirement_id: str) -> StandardsComparedRequirementModel:
        for requirement in self.compared_requirements:
            if requirement.requirement_id == requirement_id:
                return requirement
        raise ValueError(f"Requirement ID not found in comparison: {requirement_id}")

    def _validate_unique_requirement_ids(self) -> None:
        requirement_ids: set[str] = set()
        for requirement in self.compared_requirements:
            if requirement.requirement_id in requirement_ids:
                raise ValueError(
                    "Duplicate compared requirement_id is not allowed: "
                    f"{requirement.requirement_id}"
                )
            requirement_ids.add(requirement.requirement_id)

    def _validate_selected_and_stricter_ids_exist(self) -> None:
        requirement_ids = self._requirement_ids()

        missing_ids = [
            requirement_id
            for requirement_id in [
                self.stricter_requirement_id,
                self.selected_requirement_id,
            ]
            if requirement_id not in requirement_ids
        ]
        if missing_ids:
            raise ValueError(
                "Selected or stricter requirement ID is not present in compared "
                f"requirements: {', '.join(missing_ids)}"
            )

    def _validate_stricter_requirement_matches_rank(self) -> None:
        maximum_rank = max(
            requirement.strictness_rank
            for requirement in self.compared_requirements
        )
        stricter_requirement = self._requirement_by_id(self.stricter_requirement_id)

        if stricter_requirement.strictness_rank != maximum_rank:
            raise ValueError(
                "stricter_requirement_id must reference the highest strictness_rank: "
                f"{self.stricter_requirement_id}"
            )

    def _validate_selection_and_override_path(self) -> None:
        selects_stricter = self.selected_requirement_id == self.stricter_requirement_id

        if self.comparison_outcome == "select_stricter_requirement":
            if not selects_stricter:
                raise ValueError(
                    "select_stricter_requirement outcome must select the "
                    "stricter_requirement_id"
                )

            if self.override_path_reference is not None:
                raise ValueError(
                    "Override path is not allowed when the stricter requirement "
                    f"is selected: {self.comparison_id}"
                )

            return

        if self.comparison_outcome == "select_less_strict_with_override":
            if selects_stricter:
                raise ValueError(
                    "select_less_strict_with_override outcome requires selecting "
                    "a requirement other than stricter_requirement_id"
                )

            if self.override_path_reference is None:
                raise ValueError(
                    "Selecting a less strict requirement requires "
                    f"override_path_reference: {self.comparison_id}"
                )

            if self.override_limitation_statement is None:
                raise ValueError(
                    "Selecting a less strict requirement requires "
                    f"override_limitation_statement: {self.comparison_id}"
                )

            if not self.limitation_statements:
                raise ValueError(
                    "Selecting a less strict requirement requires visible "
                    f"comparison limitation statements: {self.comparison_id}"
                )

    def _validate_limited_requirement_propagation(self) -> None:
        limited_requirement_ids = [
            requirement.requirement_id
            for requirement in self.compared_requirements
            if requirement.requires_visible_limitations()
        ]

        if limited_requirement_ids and not self.limitation_statements:
            raise ValueError(
                "Limited compared requirements must propagate comparison "
                "limitations: "
                f"{', '.join(sorted(limited_requirement_ids))}"
            )


class StandardsRequirementComparisonContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_5_STANDARDS_REQUIREMENT_COMPARISON_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ContractStatus = "runtime_facing_contract"
    comparison_records: list[StandardsRequirementComparisonRecordModel] = Field(
        min_length=1
    )
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank standards requirement comparison contract value is not allowed"
                )
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_comparison_records()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_comparison_records(self) -> None:
        comparison_ids: set[str] = set()
        for comparison in self.comparison_records:
            if comparison.comparison_id in comparison_ids:
                raise ValueError(
                    "Duplicate standards requirement comparison_id is not allowed: "
                    f"{comparison.comparison_id}"
                )
            comparison_ids.add(comparison.comparison_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_interpret_standards_text",
            "does_not_implement_controlled_override_records",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.5 comparison contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
