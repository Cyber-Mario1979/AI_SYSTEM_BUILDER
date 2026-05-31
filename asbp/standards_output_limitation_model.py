from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from asbp.standards_registry_model import (
    StandardsAuthorityStatus,
    StandardsCitationDepth,
    StandardsMandatoryFlag,
    StandardsVerificationStatus,
)


OutputLimitationContractStatus = Literal["runtime_facing_contract"]
StandardsOutputContext = Literal[
    "planning",
    "gap_analysis",
    "source_traceability",
    "cqv_document_future_contract",
    "standards_output_future_contract",
]
StandardsOutputWarningVisibility = Literal["visible", "hidden", "not_required"]

_CITATION_DEPTH_ORDER: dict[StandardsCitationDepth, int] = {
    "document": 1,
    "version": 2,
    "section": 3,
    "clause": 4,
    "table_row": 4,
    "requirement": 5,
}


class StandardsOutputSourceLimitationModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    version_or_effective_date: str = Field(min_length=1)
    available_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    requested_citation_depth: StandardsCitationDepth
    rendered_citation_depth: StandardsCitationDepth
    source_limitations: list[str] = Field(default_factory=list)
    limitation_statements: list[str] = Field(default_factory=list)
    warning_text: str | None = Field(default=None, min_length=1)
    warning_visibility: StandardsOutputWarningVisibility = "not_required"
    audit_ready_claimed: bool = False
    product_ready_claimed: bool = False

    @field_validator(
        "available_citation_depths",
        "source_limitations",
        "limitation_statements",
    )
    @classmethod
    def validate_no_blank_source_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards output limitation value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_limitation_boundary(self):
        self._validate_unique_citation_depths()
        self._validate_rendered_depth_available()
        self._validate_rendered_depth_not_more_specific_than_requested()
        self._validate_citation_depth_support()
        self._validate_visible_limitation_behavior()
        self._validate_output_claim_boundaries()
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
            or self._requested_depth_is_downgraded()
        )

    def _requested_depth_is_downgraded(self) -> bool:
        return (
            _CITATION_DEPTH_ORDER[self.requested_citation_depth]
            > _CITATION_DEPTH_ORDER[self.rendered_citation_depth]
        )

    def _validate_unique_citation_depths(self) -> None:
        if len(set(self.available_citation_depths)) != len(self.available_citation_depths):
            raise ValueError(
                "Duplicate available output citation depth is not allowed: "
                f"{self.std_id}"
            )

    def _validate_rendered_depth_available(self) -> None:
        if self.rendered_citation_depth not in self.available_citation_depths:
            raise ValueError(
                "Rendered citation depth is not available for standards output source: "
                f"{self.std_id} -> {self.rendered_citation_depth}"
            )

    def _validate_rendered_depth_not_more_specific_than_requested(self) -> None:
        if (
            _CITATION_DEPTH_ORDER[self.rendered_citation_depth]
            > _CITATION_DEPTH_ORDER[self.requested_citation_depth]
        ):
            raise ValueError(
                "Rendered citation depth cannot be more specific than requested "
                f"citation depth: {self.std_id}"
            )

    def _validate_citation_depth_support(self) -> None:
        if (
            self.rendered_citation_depth == "version"
            and self.version_or_effective_date.strip().upper() == "TBD"
        ):
            raise ValueError(
                "Version-level output citation requires known version or effective "
                f"date: {self.std_id}"
            )

        if (
            self.rendered_citation_depth in {"section", "clause"}
            and self.verification_status != "verified"
        ):
            raise ValueError(
                "Section or clause output citation requires verified source evidence: "
                f"{self.std_id}"
            )

    def _validate_visible_limitation_behavior(self) -> None:
        if self.warning_visibility == "hidden":
            raise ValueError(
                "Standards output limitations must not be hidden: "
                f"{self.std_id}"
            )

        if not self.requires_visible_limitations():
            return

        if not self.limitation_statements:
            raise ValueError(
                "Limited standards output source requires limitation_statements: "
                f"{self.std_id}"
            )

        if self.warning_visibility != "visible" or self.warning_text is None:
            raise ValueError(
                "Limited standards output source requires visible warning text: "
                f"{self.std_id}"
            )

    def _validate_output_claim_boundaries(self) -> None:
        if self.product_ready_claimed:
            raise ValueError(
                "M28.9 does not support product-ready standards output claims: "
                f"{self.std_id}"
            )

        if self.audit_ready_claimed and self.requires_visible_limitations():
            raise ValueError(
                "Audit-ready standards output is not allowed for limited source: "
                f"{self.std_id}"
            )

        if self.audit_ready_claimed and self.verification_status != "verified":
            raise ValueError(
                "Audit-ready standards output requires verified source evidence: "
                f"{self.std_id}"
            )


class StandardsOutputLimitationRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    limitation_id: str = Field(
        min_length=1,
        pattern=r"^LIM-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    output_context: StandardsOutputContext
    registry_version: str = Field(min_length=1)
    source_limitations: list[StandardsOutputSourceLimitationModel] = Field(min_length=1)
    output_warning_text: str | None = Field(default=None, min_length=1)
    output_warning_visibility: StandardsOutputWarningVisibility = "not_required"
    limitation_summary: list[str] = Field(default_factory=list)
    downstream_use_limits: list[str] = Field(default_factory=list)
    audit_ready_output_claimed: bool = False
    product_ready_output_claimed: bool = False

    @field_validator("limitation_summary", "downstream_use_limits")
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards output limitation record value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_limitation_record_boundary(self):
        self._validate_source_registry_versions()
        self._validate_visible_record_warning()
        self._validate_output_claim_boundaries()
        return self

    def has_limited_sources(self) -> bool:
        return any(source.requires_visible_limitations() for source in self.source_limitations)

    def _validate_source_registry_versions(self) -> None:
        for source in self.source_limitations:
            if source.registry_version != self.registry_version:
                raise ValueError(
                    "Standards output source registry_version must match output "
                    f"registry_version: {source.std_id}"
                )

    def _validate_visible_record_warning(self) -> None:
        if self.output_warning_visibility == "hidden":
            raise ValueError(
                "Standards output limitation warning must not be hidden: "
                f"{self.limitation_id}"
            )

        if not self.has_limited_sources():
            return

        if not self.limitation_summary:
            raise ValueError(
                "Standards output with limited sources requires limitation_summary: "
                f"{self.limitation_id}"
            )

        if self.output_warning_visibility != "visible" or self.output_warning_text is None:
            raise ValueError(
                "Standards output with limited sources requires visible output warning: "
                f"{self.limitation_id}"
            )

    def _validate_output_claim_boundaries(self) -> None:
        if self.product_ready_output_claimed:
            raise ValueError(
                "M28.9 does not support product-ready standards output claims: "
                f"{self.limitation_id}"
            )

        if self.audit_ready_output_claimed and self.has_limited_sources():
            raise ValueError(
                "Audit-ready standards output is not allowed when limited sources "
                f"are present: {self.limitation_id}"
            )


class StandardsOutputLimitationContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M28_9_STANDARDS_OUTPUT_LIMITATION_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: OutputLimitationContractStatus = "runtime_facing_contract"
    registry_version: str = Field(min_length=1)
    limitation_records: list[StandardsOutputLimitationRecordModel] = Field(min_length=1)
    contract_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("contract_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards output limitation contract value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_unique_limitation_records()
        self._validate_record_registry_versions()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_limitation_records(self) -> None:
        limitation_ids: set[str] = set()
        for record in self.limitation_records:
            if record.limitation_id in limitation_ids:
                raise ValueError(
                    "Duplicate standards output limitation_id is not allowed: "
                    f"{record.limitation_id}"
                )
            limitation_ids.add(record.limitation_id)

    def _validate_record_registry_versions(self) -> None:
        for record in self.limitation_records:
            if record.registry_version != self.registry_version:
                raise ValueError(
                    "Standards output limitation record registry_version must match "
                    f"contract registry_version: {record.limitation_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_generate_product_ready_standards_output",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_render_documents_or_exports",
            "does_not_hide_source_or_citation_limitations",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.9 standards output limitation contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
