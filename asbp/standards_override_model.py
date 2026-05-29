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

ControlledOverrideStatus = Literal["runtime_facing_contract"]
ControlledOverrideDecisionStatus = Literal[
    "approved",
    "pending_approval",
    "rejected",
]
ControlledOverrideRequirementRole = Literal[
    "stricter_requirement",
    "selected_less_strict_requirement",
]

_FORBIDDEN_OVERRIDE_CLAIMS = (
    "regulatory equivalence achieved",
    "legally equivalent",
    "equivalent to regulation",
    "equivalent to the regulation",
    "closes the source",
    "source closure achieved",
    "source is closed",
    "reclassifies the source",
    "makes the source verified",
    "turns recommendation into mandatory",
    "audit-ready equivalence",
)


def _validate_no_forbidden_override_claims(value: str, field_name: str) -> None:
    normalized_value = value.casefold()
    for forbidden_claim in _FORBIDDEN_OVERRIDE_CLAIMS:
        if forbidden_claim in normalized_value:
            raise ValueError(
                "Controlled override records must not claim regulatory equivalence, "
                "source closure, source reclassification, or verification closure: "
                f"{field_name}"
            )


class StandardsOverrideApproverModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approver_id: str = Field(min_length=1)
    approver_name: str = Field(min_length=1)
    approver_role: str = Field(min_length=1)
    decision_status: ControlledOverrideDecisionStatus
    decision_reference: str = Field(min_length=1)
    decision_date: str | None = Field(default=None, min_length=1)

    @field_validator(
        "approver_id",
        "approver_name",
        "approver_role",
        "decision_reference",
        "decision_date",
    )
    @classmethod
    def validate_approver_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Blank controlled override approver value is not allowed")
        _validate_no_forbidden_override_claims(value, "approver")
        return value


class StandardsOverrideRequirementReferenceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_id: str = Field(
        min_length=1,
        pattern=r"^REQ-[A-Z0-9-]+@v[0-9]+$",
    )
    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    requirement_role: ControlledOverrideRequirementRole
    requirement_reference: str = Field(min_length=1)
    requirement_summary: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    limitation_statements: list[str] = Field(default_factory=list)

    @field_validator(
        "requirement_reference",
        "requirement_summary",
    )
    @classmethod
    def validate_requirement_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Blank controlled override requirement value is not allowed")
        _validate_no_forbidden_override_claims(value, "requirement_reference")
        return value

    @field_validator("limitation_statements")
    @classmethod
    def validate_no_blank_limitation_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError(
                    "Blank controlled override requirement limitation is not allowed"
                )
            _validate_no_forbidden_override_claims(value, "requirement limitation")
        return values

    @model_validator(mode="after")
    def validate_requirement_reference_boundary(self):
        if self.requires_visible_limitations() and not self.limitation_statements:
            raise ValueError(
                "Limited controlled override requirement reference requires "
                f"limitation_statements: {self.requirement_id}"
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


class StandardsControlledOverrideRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    override_id: str = Field(
        min_length=1,
        pattern=r"^OVR-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    comparison_id: str = Field(
        min_length=1,
        pattern=r"^CMP-[A-Z0-9-]+@v[0-9]+$",
    )
    stricter_requirement_id: str = Field(
        min_length=1,
        pattern=r"^REQ-[A-Z0-9-]+@v[0-9]+$",
    )
    selected_requirement_id: str = Field(
        min_length=1,
        pattern=r"^REQ-[A-Z0-9-]+@v[0-9]+$",
    )
    source_comparison_references: list[StandardsOverrideRequirementReferenceModel] = Field(
        min_length=2
    )
    approver: StandardsOverrideApproverModel
    reason_for_override: str = Field(min_length=1)
    risk_quality_justification: str = Field(min_length=1)
    residual_risk_statement: str = Field(min_length=1)
    applicability_boundary: list[str] = Field(min_length=1)
    limitation_statement: str = Field(min_length=1)
    non_equivalence_statement: str = Field(min_length=1)
    source_closure_boundary_statement: str = Field(min_length=1)
    override_controls: list[str] = Field(min_length=1)
    downstream_use_limits: list[str] = Field(default_factory=list)

    @field_validator(
        "reason_for_override",
        "risk_quality_justification",
        "residual_risk_statement",
        "limitation_statement",
        "non_equivalence_statement",
        "source_closure_boundary_statement",
    )
    @classmethod
    def validate_record_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Blank controlled override record value is not allowed")
        _validate_no_forbidden_override_claims(value, "override record")
        return value

    @field_validator(
        "applicability_boundary",
        "override_controls",
        "downstream_use_limits",
    )
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled override list value is not allowed")
            _validate_no_forbidden_override_claims(value, "override list value")
        return values

    @model_validator(mode="after")
    def validate_controlled_override_boundary(self):
        self._validate_selected_requirement_is_less_strict_path()
        self._validate_requirement_reference_roles()
        self._validate_required_boundary_statements()
        self._validate_downstream_limit_visibility()
        return self

    def _validate_selected_requirement_is_less_strict_path(self) -> None:
        if self.selected_requirement_id == self.stricter_requirement_id:
            raise ValueError(
                "Controlled override requires selected_requirement_id to differ "
                f"from stricter_requirement_id: {self.override_id}"
            )

    def _validate_requirement_reference_roles(self) -> None:
        role_by_requirement: dict[str, str] = {}

        for reference in self.source_comparison_references:
            existing_role = role_by_requirement.get(reference.requirement_id)
            if existing_role is not None:
                raise ValueError(
                    "Duplicate controlled override requirement reference is not allowed: "
                    f"{reference.requirement_id}"
                )
            role_by_requirement[reference.requirement_id] = reference.requirement_role

        expected_roles = {
            self.stricter_requirement_id: "stricter_requirement",
            self.selected_requirement_id: "selected_less_strict_requirement",
        }
        for requirement_id, expected_role in expected_roles.items():
            actual_role = role_by_requirement.get(requirement_id)
            if actual_role != expected_role:
                raise ValueError(
                    "Controlled override source comparison references must identify "
                    "the stricter and selected less-strict requirements: "
                    f"{requirement_id}"
                )

    def _validate_required_boundary_statements(self) -> None:
        normalized_non_equivalence = self.non_equivalence_statement.casefold()
        if not (
            "not" in normalized_non_equivalence
            and (
                "equivalent" in normalized_non_equivalence
                or "equivalence" in normalized_non_equivalence
            )
        ):
            raise ValueError(
                "Controlled override non_equivalence_statement must explicitly state "
                f"non-equivalence: {self.override_id}"
            )

        normalized_source_closure = self.source_closure_boundary_statement.casefold()
        if not (
            ("not" in normalized_source_closure or "does not" in normalized_source_closure)
            and ("source" in normalized_source_closure or "registry" in normalized_source_closure)
        ):
            raise ValueError(
                "Controlled override source_closure_boundary_statement must state "
                f"that no source or registry closure occurs: {self.override_id}"
            )

    def _validate_downstream_limit_visibility(self) -> None:
        if not self.downstream_use_limits:
            raise ValueError(
                "Controlled override requires downstream_use_limits: "
                f"{self.override_id}"
            )


class StandardsControlledOverrideContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_6_STANDARDS_CONTROLLED_OVERRIDE_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: ControlledOverrideStatus = "runtime_facing_contract"
    override_records: list[StandardsControlledOverrideRecordModel] = Field(min_length=1)
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank controlled override contract value is not allowed")
            _validate_no_forbidden_override_claims(value, "override contract")
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_override_records()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_override_records(self) -> None:
        override_ids: set[str] = set()
        for override in self.override_records:
            if override.override_id in override_ids:
                raise ValueError(
                    "Duplicate controlled override_id is not allowed: "
                    f"{override.override_id}"
                )
            override_ids.add(override.override_id)

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_create_regulatory_equivalence",
            "does_not_close_or_reclassify_sources",
            "does_not_approve_standards_without_human_decision",
            "does_not_generate_product_ready_standards_output",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.6 controlled override contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
