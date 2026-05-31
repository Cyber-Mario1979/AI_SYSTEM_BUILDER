from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ValidationSeverity = Literal["error", "warning"]
ValidationStatus = Literal["passed", "failed"]
ValidationIssueCode = Literal[
    "EMPTY_LIBRARY",
    "UNCOVERED_DURATION_REF",
    "DANGLING_PROFILE_REF",
    "DANGLING_TASK_POOL_REF",
    "DANGLING_ATOMIC_TASK_REF",
    "DANGLING_STANDARDS_BUNDLE_REF",
    "DANGLING_TEMPLATE_REF",
    "DANGLING_DOCUMENT_INPUT_SCHEMA_REF",
    "SCHEMA_TEMPLATE_MISMATCH",
    "UNBOUND_TEMPLATE_SCHEMA_REF",
    "RESOLVED_FUTURE_REF",
    "FUTURE_REF_WITHOUT_RESOLUTION",
    "BLANK_APPLICABILITY_TAG",
]
CheckedFamilyId = Literal[
    "baseline",
    "task_pools",
    "profiles",
    "calendars",
    "planning_basis",
    "mappings",
    "standards_bundles",
    "document_templates",
    "document_input_schemas",
]


class CrossLibraryValidationIssueModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue_code: ValidationIssueCode
    severity: ValidationSeverity = "error"
    source_family: CheckedFamilyId
    message: str = Field(min_length=1)
    related_ids: list[str] = Field(default_factory=list)

    @field_validator("related_ids")
    @classmethod
    def validate_no_blank_related_ids(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank related_id is not allowed")
        return values


class CrossLibraryValidationResultModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ValidationStatus
    checked_families: list[CheckedFamilyId] = Field(min_length=1)
    issues: list[CrossLibraryValidationIssueModel] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_status_matches_error_issues(self):
        has_error = any(issue.severity == "error" for issue in self.issues)

        if self.status == "passed" and has_error:
            raise ValueError(
                "Cross-library validation result cannot pass with error issues"
            )

        if self.status == "failed" and not has_error:
            raise ValueError(
                "Cross-library validation result cannot fail without error issues"
            )

        return self


def build_validation_result(
    issues: list[CrossLibraryValidationIssueModel],
) -> CrossLibraryValidationResultModel:
    return CrossLibraryValidationResultModel(
        status="failed" if any(issue.severity == "error" for issue in issues) else "passed",
        checked_families=[
            "baseline",
            "task_pools",
            "profiles",
            "calendars",
            "planning_basis",
            "mappings",
            "standards_bundles",
            "document_templates",
            "document_input_schemas",
        ],
        issues=issues,
    )
