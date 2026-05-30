from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


RendererOutputContractStatus = Literal["runtime_facing_renderer_output_contract"]
RendererOutputArtifactStatus = Literal["controlled_renderer_output_artifact"]
RendererOutputFormat = Literal["markdown", "csv_summary", "docx", "pdf", "excel"]
RendererSupportedOutputFormat = Literal["markdown", "csv_summary"]

REQUIRED_RENDERER_OUTPUT_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_product_ready_documents",
    "does_not_mutate_lifecycle_or_review_state",
    "does_not_create_signed_or_approved_records",
    "does_not_call_ai_or_retrieve_standards",
}


class RendererOutputContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
        min_length=1,
        pattern=r"^M29_RENDERER_OUTPUT_CONTRACT@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: RendererOutputContractStatus = "runtime_facing_renderer_output_contract"
    supported_formats: list[RendererSupportedOutputFormat] = Field(min_length=1)
    blocked_formats: list[RendererOutputFormat] = Field(default_factory=list)
    metadata_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "supported_formats",
        "blocked_formats",
        "metadata_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_contract_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank renderer output contract value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_contract_boundary(self):
        self._validate_contract_id_version_alignment()
        self._validate_unique_supported_formats()
        self._validate_blocked_formats()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_contract_id_version_alignment(self) -> None:
        if not self.contract_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Renderer output contract version must match contract_id suffix: "
                f"{self.contract_id} / {self.version}"
            )

    def _validate_unique_supported_formats(self) -> None:
        if len(set(self.supported_formats)) != len(self.supported_formats):
            raise ValueError("Duplicate renderer supported_formats are not allowed")

    def _validate_blocked_formats(self) -> None:
        overlap = sorted(set(self.supported_formats) & set(self.blocked_formats))
        if overlap:
            raise ValueError(
                "Renderer output formats cannot be both supported and blocked: "
                f"{', '.join(overlap)}"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_RENDERER_OUTPUT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.7 renderer output contract is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class RendererArtifactMetadataModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1, pattern=r"^ART-[A-Z0-9-]+@v[0-9]+$")
    output_format: RendererSupportedOutputFormat
    artifact_filename: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    source_draft_id: str = Field(min_length=1, pattern=r"^DRAFT-[A-Z0-9-]+@v[0-9]+$")
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    standards_control_packet_id: str = Field(
        min_length=1,
        pattern=r"^STDOUT-[A-Z0-9-]+@v[0-9]+$",
    )
    placeholder_present: bool
    limitation_present: bool
    standards_warning_present: bool
    non_product_ready: bool = True
    lifecycle_state_mutated: bool = False
    approval_claimed: bool = False

    @model_validator(mode="after")
    def validate_metadata_boundary(self):
        self._validate_media_type_matches_format()
        self._validate_non_product_ready_boundary()
        return self

    def _validate_media_type_matches_format(self) -> None:
        expected_media_type = {
            "markdown": "text/markdown",
            "csv_summary": "text/csv",
        }[self.output_format]
        if self.media_type != expected_media_type:
            raise ValueError(
                "Renderer artifact media_type does not match output_format: "
                f"{self.output_format} -> {self.media_type}"
            )

    def _validate_non_product_ready_boundary(self) -> None:
        if not self.non_product_ready:
            raise ValueError("M29.7 renderer artifacts must remain non-product-ready")
        if self.lifecycle_state_mutated:
            raise ValueError("M29.7 renderer must not mutate lifecycle state")
        if self.approval_claimed:
            raise ValueError("M29.7 renderer must not claim approval or signature state")


class RendererOutputArtifactModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1, pattern=r"^ART-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: RendererOutputArtifactStatus = "controlled_renderer_output_artifact"
    output_format: RendererSupportedOutputFormat
    artifact_filename: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    metadata: RendererArtifactMetadataModel
    rendered_content: str = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_artifact_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank renderer output artifact value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_artifact_boundary(self):
        self._validate_artifact_id_version_alignment()
        self._validate_metadata_alignment()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_artifact_id_version_alignment(self) -> None:
        if not self.artifact_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Renderer artifact version must match artifact_id suffix: "
                f"{self.artifact_id} / {self.version}"
            )

    def _validate_metadata_alignment(self) -> None:
        if self.metadata.artifact_id != self.artifact_id:
            raise ValueError("Renderer artifact metadata artifact_id mismatch")
        if self.metadata.output_format != self.output_format:
            raise ValueError("Renderer artifact metadata output_format mismatch")
        if self.metadata.artifact_filename != self.artifact_filename:
            raise ValueError("Renderer artifact metadata filename mismatch")
        if self.metadata.media_type != self.media_type:
            raise ValueError("Renderer artifact metadata media_type mismatch")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_RENDERER_OUTPUT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.7 renderer output artifact is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
