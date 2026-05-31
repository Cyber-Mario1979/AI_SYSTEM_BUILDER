from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TrialScenarioCoverageLibraryStatus = Literal["mvp_trial_scenario_coverage_source"]
TrialScenarioCoverageRecordStatus = Literal["mvp_trial_scenario_coverage_record"]
TrialScenarioPriority = Literal["P0", "P1", "P2"]
TrialScenarioDomain = Literal[
    "cleanroom_hvac",
    "process_equipment",
    "utilities",
    "csv",
    "qc_lab_equipment",
    "decommissioning",
    "manual_fallback",
]
TrialScenarioType = Literal[
    "local_review_flow",
    "fat_sat_commissioning_qualification_flow",
    "manual_fallback_safety_route",
]

REQUIRED_TRIAL_SCENARIO_COVERAGE_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_uat_acceptance",
    "does_not_release_or_deploy_documents",
    "does_not_create_customer_ready_output",
    "does_not_create_qms_approval_records",
    "does_not_generate_documents",
    "does_not_productize_or_deploy_outputs",
}


class TrialScenarioCoverageRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(
        min_length=1,
        pattern=r"^TRIALCOV-[A-Z0-9-]+@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialScenarioCoverageRecordStatus = "mvp_trial_scenario_coverage_record"
    display_name: str = Field(min_length=1)
    domain: TrialScenarioDomain
    priority: TrialScenarioPriority = "P0"
    scenario_type: TrialScenarioType = "local_review_flow"
    lifecycle_event: str = Field(min_length=1)
    asset_archetype: str | None = Field(default=None, min_length=1)
    utility_system: str | None = Field(default=None, min_length=1)
    urs_dcf_required: bool
    urs_dcf_route_ref: str | None = Field(default=None, pattern=r"^DCF-[A-Z0-9-]+@v[0-9]+$")
    task_pool_refs: list[str] = Field(min_length=1)
    profile_refs: list[str] = Field(min_length=1)
    planning_basis_refs: list[str] = Field(min_length=1)
    mapping_refs: list[str] = Field(min_length=1)
    document_refs: list[str] = Field(min_length=1)
    downstream_dependency_refs: list[str] = Field(min_length=1)
    standards_policy_refs: list[str] = Field(min_length=1)
    vendor_source_refs: list[str] = Field(default_factory=list)
    output_validation_expectations: list[str] = Field(min_length=1)
    coverage_controls: list[str] = Field(min_length=1)
    local_review_only: bool = True
    uat_acceptance_claimed: bool = False
    customer_ready_release_claimed: bool = False
    productization_claimed: bool = False
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "task_pool_refs",
        "profile_refs",
        "planning_basis_refs",
        "mapping_refs",
        "document_refs",
        "downstream_dependency_refs",
        "standards_policy_refs",
        "vendor_source_refs",
        "output_validation_expectations",
        "coverage_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank trial scenario coverage value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_scenario_coverage_boundary(self):
        self._validate_version_alignment()
        self._validate_domain_specific_fields()
        self._validate_urs_dcf_boundary()
        self._validate_vendor_source_boundary()
        self._validate_no_completion_claims()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_version_alignment(self) -> None:
        if not self.scenario_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Trial scenario coverage version must match scenario_id suffix: "
                f"{self.scenario_id} / {self.version}"
            )

    def _validate_domain_specific_fields(self) -> None:
        if self.domain == "process_equipment" and self.asset_archetype is None:
            raise ValueError(
                "Process equipment trial scenario coverage requires asset_archetype: "
                f"{self.scenario_id}"
            )
        if self.domain == "utilities" and self.utility_system is None:
            raise ValueError(
                "Utilities trial scenario coverage requires utility_system: "
                f"{self.scenario_id}"
            )
        if self.domain != "process_equipment" and self.asset_archetype is not None:
            raise ValueError(
                "Only process equipment trial scenario coverage may include "
                f"asset_archetype: {self.scenario_id}"
            )
        if self.domain != "utilities" and self.utility_system is not None:
            raise ValueError(
                "Only utilities trial scenario coverage may include "
                f"utility_system: {self.scenario_id}"
            )

    def _validate_urs_dcf_boundary(self) -> None:
        if self.urs_dcf_required:
            if self.urs_dcf_route_ref is None:
                raise ValueError(
                    "URS DCF-required trial scenario requires urs_dcf_route_ref: "
                    f"{self.scenario_id}"
                )
            if "URS" not in self.document_refs:
                raise ValueError(
                    "URS DCF-required trial scenario must include URS document ref: "
                    f"{self.scenario_id}"
                )
            if "URS" not in self.urs_dcf_route_ref:
                raise ValueError(
                    "DCF route refs must remain URS-oriented: "
                    f"{self.scenario_id} -> {self.urs_dcf_route_ref}"
                )
        elif self.urs_dcf_route_ref is not None:
            raise ValueError(
                "Trial scenario without URS DCF requirement must not include "
                f"urs_dcf_route_ref: {self.scenario_id}"
            )

    def _validate_vendor_source_boundary(self) -> None:
        if "VENDOR_DOC_EXTRACTION_SOURCE" in self.document_refs and not self.vendor_source_refs:
            raise ValueError(
                "Vendor document extraction trial scenario must include vendor_source_refs: "
                f"{self.scenario_id}"
            )

    def _validate_no_completion_claims(self) -> None:
        if not self.local_review_only:
            raise ValueError(
                "Trial scenario coverage must remain local-review-only: "
                f"{self.scenario_id}"
            )
        if self.uat_acceptance_claimed:
            raise ValueError(
                "Trial scenario coverage must not claim UAT acceptance: "
                f"{self.scenario_id}"
            )
        if self.customer_ready_release_claimed:
            raise ValueError(
                "Trial scenario coverage must not claim customer-ready release: "
                f"{self.scenario_id}"
            )
        if self.productization_claimed:
            raise ValueError(
                "Trial scenario coverage must not claim productization: "
                f"{self.scenario_id}"
            )

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_TRIAL_SCENARIO_COVERAGE_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Trial scenario coverage record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class TrialScenarioCoverageLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(
        min_length=1,
        pattern=r"^M29_MVP_TRIAL_SCENARIO_COVERAGE_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialScenarioCoverageLibraryStatus = "mvp_trial_scenario_coverage_source"
    scenarios: list[TrialScenarioCoverageRecordModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank trial scenario coverage library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_scenario_coverage_library_boundary(self):
        self._validate_unique_scenario_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_scenario_ids(self) -> None:
        scenario_ids: set[str] = set()
        for scenario in self.scenarios:
            if scenario.scenario_id in scenario_ids:
                raise ValueError(
                    "Duplicate trial scenario coverage id is not allowed: "
                    f"{scenario.scenario_id}"
                )
            scenario_ids.add(scenario.scenario_id)

    def _validate_required_non_implementation_claims(self) -> None:
        missing_claims = sorted(
            REQUIRED_TRIAL_SCENARIO_COVERAGE_NON_IMPLEMENTATION_CLAIMS
            - set(self.explicit_non_implementation_claims)
        )
        if missing_claims:
            raise ValueError(
                "Trial scenario coverage library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
