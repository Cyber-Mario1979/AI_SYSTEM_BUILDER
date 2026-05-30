from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TemplateSelectionRequestStatus = Literal["deterministic_template_selection_request"]
TemplateSelectionResultStatus = Literal["selected", "no_match", "ambiguous"]
TemplateSelectionRejectionReason = Literal[
    "inactive_lifecycle_status",
    "document_family_mismatch",
    "document_type_mismatch",
    "standards_bundle_mismatch",
    "standards_mapping_mismatch",
    "intake_route_mismatch",
]
TemplateSelectionIntakeRoute = Literal["ROUTE-DCF", "ROUTE-SKIP-DCF"]


REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_generate_documents",
    "does_not_validate_document_input_schemas",
    "does_not_render_or_export_documents",
    "does_not_use_ai_to_choose_templates",
}


class TemplateSelectionInputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selection_id: str = Field(min_length=1, pattern=r"^TPLSEL-[A-Z0-9-]+@v[0-9]+$")
    status: TemplateSelectionRequestStatus = "deterministic_template_selection_request"
    document_family_id: str = Field(min_length=1, pattern=r"^DOCF-[A-Z0-9-]+$")
    document_type: str = Field(min_length=1)
    template_intent: str | None = Field(default=None, min_length=1)
    selector_context_ref: str | None = Field(default=None, min_length=1)
    profile_refs: list[str] = Field(default_factory=list)
    standards_bundle_refs: list[str] = Field(default_factory=list)
    task_document_mapping_refs: list[str] = Field(default_factory=list)
    intake_route_ref: TemplateSelectionIntakeRoute
    selection_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "profile_refs",
        "standards_bundle_refs",
        "task_document_mapping_refs",
        "selection_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_list_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank template selection request value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_selection_input_boundary(self):
        self._validate_standards_bundle_refs()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_standards_bundle_refs(self) -> None:
        seen_refs: set[str] = set()

        for bundle_ref in self.standards_bundle_refs:
            if not bundle_ref.startswith("SB-") or "@" not in bundle_ref:
                raise ValueError(
                    "Template selection standards_bundle_refs must use SB-...@v... IDs: "
                    f"{bundle_ref}"
                )

            if bundle_ref in seen_refs:
                raise ValueError(
                    "Duplicate template selection standards_bundle_ref is not allowed: "
                    f"{bundle_ref}"
                )
            seen_refs.add(bundle_ref)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )

        if missing_claims:
            raise ValueError(
                "M29.3 template selection request is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class TemplateSelectionCandidateRejectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    reason_code: TemplateSelectionRejectionReason
    message: str = Field(min_length=1)


class TemplateSelectionResultModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selection_id: str = Field(min_length=1, pattern=r"^TPLSEL-[A-Z0-9-]+@v[0-9]+$")
    status: TemplateSelectionResultStatus
    selected_template_id: str | None = Field(
        default=None,
        pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$",
    )
    candidate_template_ids: list[str] = Field(default_factory=list)
    rejected_candidates: list[TemplateSelectionCandidateRejectionModel] = Field(
        default_factory=list
    )
    source_mapping_ids: list[str] = Field(default_factory=list)
    decision_reason: str | None = Field(default=None, min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "candidate_template_ids",
        "source_mapping_ids",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_result_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank template selection result value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_selection_result_boundary(self):
        self._validate_status_shape()
        self._validate_unique_candidate_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_status_shape(self) -> None:
        if self.status == "selected":
            if self.selected_template_id is None:
                raise ValueError("Selected template result requires selected_template_id")
            if self.decision_reason is None:
                raise ValueError("Selected template result requires decision_reason")
            if self.selected_template_id not in self.candidate_template_ids:
                raise ValueError(
                    "Selected template must be included in candidate_template_ids: "
                    f"{self.selected_template_id}"
                )
            return

        if self.selected_template_id is not None:
            raise ValueError(
                "No-match or ambiguous template selection result cannot include "
                f"selected_template_id: {self.selected_template_id}"
            )

    def _validate_unique_candidate_ids(self) -> None:
        if len(set(self.candidate_template_ids)) != len(self.candidate_template_ids):
            raise ValueError("Duplicate candidate_template_ids are not allowed")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )

        if missing_claims:
            raise ValueError(
                "M29.3 template selection result is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
