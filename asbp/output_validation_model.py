from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from asbp.document_lifecycle_model import DocumentLifecycleState
from asbp.renderer_output_model import RendererSupportedOutputFormat


OutputValidationRuleLibraryStatus = Literal["runtime_facing_output_validation_rule_source"]
OutputValidationRuleStatus = Literal["runtime_facing_output_validation_rule"]
OutputValidationStatus = Literal["passed", "failed"]
OutputValidationIssueSeverity = Literal["error", "warning"]
OutputValidationCheckType = Literal[
    "artifact_content_presence",
    "metadata_alignment",
    "schema_conformance_reference",
    "citation_or_standards_warning_presence",
    "placeholder_policy",
    "limitation_visibility",
    "lifecycle_state_eligibility",
    "no_approval_or_release_claim",
]
OutputValidationIssueCode = Literal[
    "EMPTY_RENDERED_CONTENT",
    "METADATA_ALIGNMENT_MISMATCH",
    "MISSING_PLACEHOLDER_VISIBILITY",
    "MISSING_LIMITATION_VISIBILITY",
    "MISSING_STANDARDS_WARNING_VISIBILITY",
    "INELIGIBLE_LIFECYCLE_STATE",
    "PRODUCT_READY_CLAIM_NOT_ALLOWED",
    "APPROVAL_OR_RELEASE_CLAIM_NOT_ALLOWED",
    "MISSING_REQUIRED_METADATA",
]


REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_uat_acceptance",
    "does_not_approve_sign_or_release_documents",
    "does_not_generate_trial_document_sets",
    "does_not_deploy_or_productize_outputs",
}


class OutputValidationRuleModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, pattern=r"^OUTVALRULE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: OutputValidationRuleStatus = "runtime_facing_output_validation_rule"
    supported_formats: list[RendererSupportedOutputFormat] = Field(min_length=1)
    allowed_lifecycle_states: list[DocumentLifecycleState] = Field(min_length=1)
    required_checks: list[OutputValidationCheckType] = Field(min_length=1)
    metadata_controls: list[str] = Field(min_length=1)
    placeholder_policy_controls: list[str] = Field(min_length=1)
    limitation_visibility_controls: list[str] = Field(min_length=1)
    standards_warning_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "supported_formats",
        "allowed_lifecycle_states",
        "required_checks",
        "metadata_controls",
        "placeholder_policy_controls",
        "limitation_visibility_controls",
        "standards_warning_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_rule_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank output validation rule value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_rule_boundary(self):
        self._validate_rule_id_version_alignment()
        self._validate_unique_values()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_rule_id_version_alignment(self) -> None:
        if not self.rule_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Output validation rule version must match rule_id suffix: "
                f"{self.rule_id} / {self.version}"
            )

    def _validate_unique_values(self) -> None:
        unique_sets = [
            ("supported_formats", self.supported_formats),
            ("allowed_lifecycle_states", self.allowed_lifecycle_states),
            ("required_checks", self.required_checks),
        ]
        for field_name, values in unique_sets:
            if len(set(values)) != len(values):
                raise ValueError(f"Duplicate output validation {field_name} is not allowed")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.9 output validation rule is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class OutputValidationRuleLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(
        min_length=1,
        pattern=r"^M29_OUTPUT_VALIDATION_RULE_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: OutputValidationRuleLibraryStatus = "runtime_facing_output_validation_rule_source"
    validation_rules: list[OutputValidationRuleModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank output validation library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_rule_library_boundary(self):
        self._validate_unique_rule_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_rule_ids(self) -> None:
        rule_ids: set[str] = set()
        for rule in self.validation_rules:
            if rule.rule_id in rule_ids:
                raise ValueError(
                    "Duplicate output validation rule id is not allowed: "
                    f"{rule.rule_id}"
                )
            rule_ids.add(rule.rule_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.9 output validation rule library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class OutputValidationIssueModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue_code: OutputValidationIssueCode
    severity: OutputValidationIssueSeverity = "error"
    message: str = Field(min_length=1)
    related_ids: list[str] = Field(default_factory=list)

    @field_validator("related_ids")
    @classmethod
    def validate_no_blank_related_ids(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank output validation related_id is not allowed")
        return values


class OutputValidationResultModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    validation_id: str = Field(min_length=1, pattern=r"^OUTVAL-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: OutputValidationStatus
    artifact_id: str = Field(min_length=1, pattern=r"^ART-[A-Z0-9-]+@v[0-9]+$")
    lifecycle_record_id: str = Field(min_length=1, pattern=r"^LIFECYCLE-[A-Z0-9-]+@v[0-9]+$")
    output_format: RendererSupportedOutputFormat
    rule_id: str = Field(min_length=1, pattern=r"^OUTVALRULE-[A-Z0-9-]+@v[0-9]+$")
    checks_performed: list[OutputValidationCheckType] = Field(min_length=1)
    issues: list[OutputValidationIssueModel] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("checks_performed", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_result_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank output validation result value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_result_boundary(self):
        self._validate_validation_id_version_alignment()
        self._validate_unique_checks()
        self._validate_status_matches_error_issues()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_validation_id_version_alignment(self) -> None:
        if not self.validation_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Output validation result version must match validation_id suffix: "
                f"{self.validation_id} / {self.version}"
            )

    def _validate_unique_checks(self) -> None:
        if len(set(self.checks_performed)) != len(self.checks_performed):
            raise ValueError("Duplicate output validation checks_performed are not allowed")

    def _validate_status_matches_error_issues(self) -> None:
        has_error = any(issue.severity == "error" for issue in self.issues)
        if self.status == "passed" and has_error:
            raise ValueError("Output validation result cannot pass with error issues")
        if self.status == "failed" and not has_error:
            raise ValueError("Output validation result cannot fail without error issues")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.9 output validation result is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
