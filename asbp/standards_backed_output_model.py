from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from asbp.standards_registry_model import (
    StandardsAuthorityStatus,
    StandardsCitationDepth,
    StandardsMandatoryFlag,
    StandardsVerificationStatus,
)

StandardsBackedOutputPacketStatus = Literal["standards_backed_output_control_packet"]
StandardsBackedOutputWarningVisibility = Literal["visible", "not_required"]
StandardsBackedOutputSectionRelevance = Literal[
    "standards_relevant",
    "standards_not_relevant",
    "standards_relevance_pending_review",
]

CITATION_DEPTH_ORDER: dict[StandardsCitationDepth, int] = {
    "document": 1,
    "version": 2,
    "section": 3,
    "clause": 4,
    "table_row": 4,
    "requirement": 5,
}

REQUIRED_STANDARDS_BACKED_OUTPUT_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_generate_product_ready_documents",
    "does_not_render_or_export_documents",
    "does_not_implement_standards_retrieval_or_embedding",
    "does_not_hide_source_or_citation_limitations",
}


class StandardsBackedOutputSourceControlModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    version_or_effective_date: str = Field(min_length=1)
    requested_citation_depth: StandardsCitationDepth
    rendered_citation_depth: StandardsCitationDepth
    available_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    source_limitations: list[str] = Field(default_factory=list)
    limitation_statements: list[str] = Field(default_factory=list)
    assumption_records: list[str] = Field(default_factory=list)
    warning_text: str | None = Field(default=None, min_length=1)
    warning_visibility: StandardsBackedOutputWarningVisibility = "not_required"
    source_record_ref: str = Field(min_length=1)

    @field_validator(
        "available_citation_depths",
        "source_limitations",
        "limitation_statements",
        "assumption_records",
    )
    @classmethod
    def validate_no_blank_source_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank standards-backed output source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_control_boundary(self):
        self._validate_unique_citation_depths()
        self._validate_rendered_depth_available()
        self._validate_rendered_depth_not_more_specific_than_requested()
        self._validate_citation_depth_support()
        self._validate_visible_limitation_behavior()
        return self

    def requires_visible_limitations(self) -> bool:
        version_is_limited = self.version_or_effective_date.strip().upper() == "TBD"
        citation_is_downgraded = (
            CITATION_DEPTH_ORDER[self.requested_citation_depth]
            > CITATION_DEPTH_ORDER[self.rendered_citation_depth]
        )
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
            or citation_is_downgraded
        )

    def _validate_unique_citation_depths(self) -> None:
        if len(set(self.available_citation_depths)) != len(self.available_citation_depths):
            raise ValueError(
                "Duplicate standards-backed output citation depth is not allowed: "
                f"{self.std_id}"
            )

    def _validate_rendered_depth_available(self) -> None:
        if self.rendered_citation_depth not in self.available_citation_depths:
            raise ValueError(
                "Rendered citation depth is not available for standards-backed "
                f"output source: {self.std_id} -> {self.rendered_citation_depth}"
            )

    def _validate_rendered_depth_not_more_specific_than_requested(self) -> None:
        if (
            CITATION_DEPTH_ORDER[self.rendered_citation_depth]
            > CITATION_DEPTH_ORDER[self.requested_citation_depth]
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
                "Version-level standards-backed output citation requires known "
                f"version or effective date: {self.std_id}"
            )

        if (
            self.rendered_citation_depth in {"section", "clause"}
            and self.verification_status != "verified"
        ):
            raise ValueError(
                "Section or clause standards-backed output citation requires "
                f"verified source evidence: {self.std_id}"
            )

    def _validate_visible_limitation_behavior(self) -> None:
        if not self.requires_visible_limitations():
            return

        if not self.limitation_statements:
            raise ValueError(
                "Limited standards-backed output source requires limitation_statements: "
                f"{self.std_id}"
            )

        if self.warning_visibility != "visible" or self.warning_text is None:
            raise ValueError(
                "Limited standards-backed output source requires visible warning text: "
                f"{self.std_id}"
            )


class StandardsBackedOutputSectionControlModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    standards_relevance: StandardsBackedOutputSectionRelevance
    standards_source_refs: list[str] = Field(default_factory=list)
    citation_limitation_statements: list[str] = Field(default_factory=list)
    assumption_records: list[str] = Field(default_factory=list)
    reviewer_attention_points: list[str] = Field(default_factory=list)

    @field_validator(
        "standards_source_refs",
        "citation_limitation_statements",
        "assumption_records",
        "reviewer_attention_points",
    )
    @classmethod
    def validate_no_blank_section_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards-backed output section value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_section_control_boundary(self):
        if len(set(self.standards_source_refs)) != len(self.standards_source_refs):
            raise ValueError(
                "Duplicate standards-backed output section source ref is not allowed: "
                f"{self.section_id}"
            )
        if self.standards_relevance == "standards_relevant" and not self.standards_source_refs:
            raise ValueError(
                "Standards-relevant section requires standards_source_refs: "
                f"{self.section_id}"
            )
        return self


class StandardsBackedOutputControlPacketModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    control_packet_id: str = Field(min_length=1, pattern=r"^STDOUT-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsBackedOutputPacketStatus = "standards_backed_output_control_packet"
    draft_id: str = Field(min_length=1, pattern=r"^DRAFT-[A-Z0-9-]+@v[0-9]+$")
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    standards_bundle_refs: list[str] = Field(min_length=1)
    source_controls: list[StandardsBackedOutputSourceControlModel] = Field(min_length=1)
    section_controls: list[StandardsBackedOutputSectionControlModel] = Field(min_length=1)
    output_warning_text: str | None = Field(default=None, min_length=1)
    output_warning_visibility: StandardsBackedOutputWarningVisibility = "not_required"
    output_limitation_summary: list[str] = Field(default_factory=list)
    assumption_records: list[str] = Field(default_factory=list)
    reviewer_attention_points: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "standards_bundle_refs",
        "output_limitation_summary",
        "assumption_records",
        "reviewer_attention_points",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_packet_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards-backed output packet value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_output_control_packet_boundary(self):
        self._validate_packet_id_version_alignment()
        self._validate_unique_bundle_refs()
        self._validate_unique_source_refs()
        self._validate_unique_section_ids()
        self._validate_visible_packet_warning()
        self._validate_required_non_implementation_claims()
        return self

    def has_limited_sources(self) -> bool:
        return any(source.requires_visible_limitations() for source in self.source_controls)

    def _validate_packet_id_version_alignment(self) -> None:
        if not self.control_packet_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Standards-backed output packet version must match packet id suffix: "
                f"{self.control_packet_id} / {self.version}"
            )

    def _validate_unique_bundle_refs(self) -> None:
        if len(set(self.standards_bundle_refs)) != len(self.standards_bundle_refs):
            raise ValueError("Duplicate standards-backed output bundle ref is not allowed")
        for bundle_ref in self.standards_bundle_refs:
            if not bundle_ref.startswith("SB-") or "@" not in bundle_ref:
                raise ValueError(
                    "Standards-backed output bundle refs must use SB-...@v... IDs: "
                    f"{bundle_ref}"
                )

    def _validate_unique_source_refs(self) -> None:
        source_ids = [source.std_id for source in self.source_controls]
        if len(set(source_ids)) != len(source_ids):
            raise ValueError("Duplicate standards-backed output source control is not allowed")

    def _validate_unique_section_ids(self) -> None:
        section_ids = [section.section_id for section in self.section_controls]
        if len(set(section_ids)) != len(section_ids):
            raise ValueError("Duplicate standards-backed output section control is not allowed")

    def _validate_visible_packet_warning(self) -> None:
        if not self.has_limited_sources():
            return
        if not self.output_limitation_summary:
            raise ValueError(
                "Standards-backed output packet with limited sources requires "
                "output_limitation_summary"
            )
        if self.output_warning_visibility != "visible" or self.output_warning_text is None:
            raise ValueError(
                "Standards-backed output packet with limited sources requires "
                "visible output warning text"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_STANDARDS_BACKED_OUTPUT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.6 standards-backed output control packet is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class StandardsBackedOutputControlLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_STANDARDS_BACKED_OUTPUT_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsBackedOutputPacketStatus = "standards_backed_output_control_packet"
    control_packets: list[StandardsBackedOutputControlPacketModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards-backed output library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_library_boundary(self):
        self._validate_unique_control_packet_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_control_packet_ids(self) -> None:
        control_packet_ids: set[str] = set()
        for packet in self.control_packets:
            if packet.control_packet_id in control_packet_ids:
                raise ValueError(
                    "Duplicate standards-backed output control packet id is not allowed: "
                    f"{packet.control_packet_id}"
                )
            control_packet_ids.add(packet.control_packet_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_STANDARDS_BACKED_OUTPUT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.6 standards-backed output control library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
