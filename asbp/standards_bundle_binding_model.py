from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from asbp.standards_applicability_model import StandardsMandatoryFlag
from asbp.standards_citation_model import (
    StandardsAuthorityStatus,
    StandardsCitationDepth,
    StandardsVerificationStatus,
)


StandardsBundleBindingStatus = Literal["runtime_facing_source_contract"]
StandardsBundleSourceRole = Literal[
    "primary_authority_candidate",
    "supporting_reference",
    "internal_candidate",
    "traceability_only",
]
StandardsBundleConsumerType = Literal[
    "mapping_record",
    "template_future_contract",
    "document_expectation_future_contract",
]
StandardsBundleConsumerStatus = Literal[
    "resolved_mapping_record",
    "future_expected",
    "placeholder_not_runtime_authority",
]


class StandardsBundleSourceBindingModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    std_id: str = Field(min_length=1, pattern=r"^STD-[A-Z0-9-]+$")
    registry_version: str = Field(min_length=1)
    source_role: StandardsBundleSourceRole
    authority_status: StandardsAuthorityStatus
    verification_status: StandardsVerificationStatus
    mandatory_flag: StandardsMandatoryFlag
    allowed_citation_depths: list[StandardsCitationDepth] = Field(min_length=1)
    applicability_boundaries: list[str] = Field(min_length=1)
    source_limitations: list[str] = Field(default_factory=list)
    supports_mandatory_use: bool = False
    internal_approval_reference: str | None = Field(default=None, min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator(
        "allowed_citation_depths",
        "applicability_boundaries",
        "source_limitations",
        "notes",
    )
    @classmethod
    def validate_no_blank_source_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards bundle source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_source_binding_boundary(self):
        self._validate_unique_citation_depths()
        self._validate_visible_limitations()
        self._validate_section_or_clause_depths()
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

    def _validate_unique_citation_depths(self) -> None:
        if len(set(self.allowed_citation_depths)) != len(self.allowed_citation_depths):
            raise ValueError(
                "Duplicate standards bundle citation depth is not allowed: "
                f"{self.std_id}"
            )

    def _validate_visible_limitations(self) -> None:
        if self.requires_visible_limitations() and not self.source_limitations:
            raise ValueError(
                "Limited standards bundle source requires source_limitations: "
                f"{self.std_id}"
            )

    def _validate_section_or_clause_depths(self) -> None:
        if self.verification_status == "verified":
            return

        if any(
            depth in {"section", "clause"}
            for depth in self.allowed_citation_depths
        ):
            raise ValueError(
                "Section or clause citation depth requires verified source evidence: "
                f"{self.std_id}"
            )

    def _validate_mandatory_use_boundary(self) -> None:
        if not self.supports_mandatory_use:
            return

        if self.authority_status not in {"authoritative", "internal"}:
            raise ValueError(
                "Mandatory standards bundle use requires authoritative or internal "
                f"authority status: {self.std_id}"
            )

        if self.mandatory_flag not in {"mandatory", "mandatory_when_applicable"}:
            raise ValueError(
                "Mandatory standards bundle use requires a mandatory source flag: "
                f"{self.std_id}"
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
            "Mandatory standards bundle use requires verified source evidence or "
            f"approved internal source evidence: {self.std_id}"
        )


class StandardsBundleDownstreamConsumerModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    consumer_id: str = Field(min_length=1)
    consumer_type: StandardsBundleConsumerType
    consumer_status: StandardsBundleConsumerStatus
    resolution_checkpoint: str | None = Field(default=None, min_length=1)
    limitation_statement: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_consumer_boundary(self):
        if (
            self.consumer_status != "resolved_mapping_record"
            and self.resolution_checkpoint is None
        ):
            raise ValueError(
                "Future or placeholder standards bundle consumer requires "
                f"resolution_checkpoint: {self.consumer_id}"
            )

        if (
            self.consumer_status == "resolved_mapping_record"
            and self.resolution_checkpoint is not None
        ):
            raise ValueError(
                "Resolved standards bundle consumer cannot include "
                f"resolution_checkpoint: {self.consumer_id}"
            )

        if (
            self.consumer_status == "resolved_mapping_record"
            and self.consumer_type != "mapping_record"
        ):
            raise ValueError(
                "Only mapping_record consumers may be resolved in M28.4: "
                f"{self.consumer_id}"
            )

        return self


class StandardsBundleBindingModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1, pattern=r"^SB-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsBundleBindingStatus = "runtime_facing_source_contract"
    display_name: str = Field(min_length=1)
    registry_version: str = Field(min_length=1)
    binding_scope: list[str] = Field(min_length=1)
    source_bindings: list[StandardsBundleSourceBindingModel] = Field(min_length=1)
    downstream_consumers: list[StandardsBundleDownstreamConsumerModel] = Field(
        min_length=1
    )
    binding_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "binding_scope",
        "binding_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_binding_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank standards bundle binding value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_bundle_binding_boundary(self):
        self._validate_unique_source_ids()
        self._validate_unique_downstream_consumers()
        self._validate_source_registry_versions()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_source_ids(self) -> None:
        source_ids: set[str] = set()
        for source in self.source_bindings:
            if source.std_id in source_ids:
                raise ValueError(
                    "Duplicate standards bundle source id is not allowed: "
                    f"{source.std_id}"
                )
            source_ids.add(source.std_id)

    def _validate_unique_downstream_consumers(self) -> None:
        consumer_keys: set[tuple[str, str]] = set()
        for consumer in self.downstream_consumers:
            consumer_key = (consumer.consumer_type, consumer.consumer_id)
            if consumer_key in consumer_keys:
                raise ValueError(
                    "Duplicate standards bundle downstream consumer is not allowed: "
                    f"{consumer.consumer_type}::{consumer.consumer_id}"
                )
            consumer_keys.add(consumer_key)

    def _validate_source_registry_versions(self) -> None:
        for source in self.source_bindings:
            if source.registry_version != self.registry_version:
                raise ValueError(
                    "Standards bundle source registry_version must match bundle "
                    f"registry_version: {source.std_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        required_claims = {
            "does_not_execute_runtime_registry_consumption",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_load_or_select_templates",
            "does_not_generate_product_ready_standards_output",
        }
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(required_claims - provided_claims)

        if missing_claims:
            raise ValueError(
                "M28.4 standards bundle binding is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class StandardsBundleBindingLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: StandardsBundleBindingStatus = "runtime_facing_source_contract"
    bindings: list[StandardsBundleBindingModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_bundle_ids(self):
        bundle_ids: set[str] = set()

        for binding in self.bindings:
            if binding.bundle_id in bundle_ids:
                raise ValueError(
                    "Duplicate standards bundle id is not allowed: "
                    f"{binding.bundle_id}"
                )
            bundle_ids.add(binding.bundle_id)

        return self
