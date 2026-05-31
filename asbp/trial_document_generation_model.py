from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TrialDocumentScenarioLibraryStatus = Literal["runtime_facing_trial_document_scenario_source"]
TrialDocumentScenarioStatus = Literal["runtime_facing_trial_document_scenario_record"]
TrialDocumentSetStatus = Literal["controlled_trial_document_set"]
TrialDocumentSampleStatus = Literal["controlled_trial_document_sample_record"]
TrialDocumentOutputFormat = Literal["markdown", "csv_summary"]
TrialIntakeRouteRef = Literal["ROUTE-DCF", "ROUTE-SKIP-DCF"]
TrialValidationStatus = Literal["passed"]

REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_uat_acceptance",
    "does_not_release_or_deploy_documents",
    "does_not_create_customer_ready_output",
    "does_not_create_qms_approval_records",
}


class TrialDocumentScenarioModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=1, pattern=r"^TRIAL-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialDocumentScenarioStatus = "runtime_facing_trial_document_scenario_record"
    display_name: str = Field(min_length=1)
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    drafting_mode_id: str = Field(min_length=1, pattern=r"^DRAFTMODE-[A-Z0-9-]+@v[0-9]+$")
    standards_bundle_refs: list[str] = Field(min_length=1)
    input_values: dict[str, str] = Field(min_length=1)
    intake_route_ref: TrialIntakeRouteRef = "ROUTE-SKIP-DCF"
    output_formats: list[TrialDocumentOutputFormat] = Field(min_length=1)
    scenario_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "standards_bundle_refs",
        "output_formats",
        "scenario_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_list_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not str(value).strip():
                raise ValueError("Blank trial document scenario value is not allowed")
        return values

    @field_validator("input_values")
    @classmethod
    def validate_no_blank_input_values(cls, values: dict[str, str]) -> dict[str, str]:
        for key, value in values.items():
            if not key.strip() or not str(value).strip():
                raise ValueError("Blank trial document scenario input value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_scenario_boundary(self):
        self._validate_scenario_id_version_alignment()
        self._validate_unique_references()
        self._validate_standards_bundle_refs()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_scenario_id_version_alignment(self) -> None:
        if not self.scenario_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Trial document scenario version must match scenario_id suffix: "
                f"{self.scenario_id} / {self.version}"
            )

    def _validate_unique_references(self) -> None:
        if len(set(self.standards_bundle_refs)) != len(self.standards_bundle_refs):
            raise ValueError(
                "Duplicate trial document standards_bundle_refs are not allowed: "
                f"{self.scenario_id}"
            )
        if len(set(self.output_formats)) != len(self.output_formats):
            raise ValueError(
                "Duplicate trial document output_formats are not allowed: "
                f"{self.scenario_id}"
            )

    def _validate_standards_bundle_refs(self) -> None:
        for bundle_ref in self.standards_bundle_refs:
            if not bundle_ref.startswith("SB-") or "@" not in bundle_ref:
                raise ValueError(
                    "Trial document standards_bundle_refs must use SB-...@v... IDs: "
                    f"{bundle_ref}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.10 trial document scenario is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class TrialDocumentScenarioLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(
        min_length=1,
        pattern=r"^M29_TRIAL_DOCUMENT_SCENARIO_LIBRARY@v[0-9]+$",
    )
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialDocumentScenarioLibraryStatus = "runtime_facing_trial_document_scenario_source"
    scenarios: list[TrialDocumentScenarioModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank trial document scenario library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_scenario_library_boundary(self):
        self._validate_unique_scenario_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_scenario_ids(self) -> None:
        scenario_ids: set[str] = set()
        for scenario in self.scenarios:
            if scenario.scenario_id in scenario_ids:
                raise ValueError(
                    "Duplicate trial document scenario id is not allowed: "
                    f"{scenario.scenario_id}"
                )
            scenario_ids.add(scenario.scenario_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.10 trial document scenario library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class TrialGeneratedArtifactRefModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sample_id: str = Field(min_length=1, pattern=r"^TRIALSAMPLE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialDocumentSampleStatus = "controlled_trial_document_sample_record"
    scenario_id: str = Field(min_length=1, pattern=r"^TRIAL-[A-Z0-9-]+@v[0-9]+$")
    output_format: TrialDocumentOutputFormat
    draft_id: str = Field(min_length=1, pattern=r"^DRAFT-[A-Z0-9-]+@v[0-9]+$")
    standards_control_packet_id: str = Field(min_length=1, pattern=r"^STDOUT-[A-Z0-9-]+@v[0-9]+$")
    artifact_id: str = Field(min_length=1, pattern=r"^ART-[A-Z0-9-]+@v[0-9]+$")
    artifact_filename: str = Field(min_length=1)
    lifecycle_record_id: str = Field(min_length=1, pattern=r"^LIFECYCLE-[A-Z0-9-]+@v[0-9]+$")
    output_validation_result_id: str = Field(min_length=1, pattern=r"^OUTVAL-[A-Z0-9-]+@v[0-9]+$")
    output_validation_status: TrialValidationStatus = "passed"
    placeholder_present: bool
    limitation_present: bool
    standards_warning_present: bool
    limitation_carry_forward: list[str] = Field(min_length=1)
    review_notes: list[str] = Field(min_length=1)
    customer_ready_release_claimed: bool = False
    uat_acceptance_claimed: bool = False
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "limitation_carry_forward",
        "review_notes",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_sample_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank trial generated artifact value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_sample_boundary(self):
        self._validate_sample_id_version_alignment()
        self._validate_no_release_or_uat_claims()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_sample_id_version_alignment(self) -> None:
        if not self.sample_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Trial generated sample version must match sample_id suffix: "
                f"{self.sample_id} / {self.version}"
            )

    def _validate_no_release_or_uat_claims(self) -> None:
        if self.customer_ready_release_claimed:
            raise ValueError("Trial samples must not claim customer-ready release")
        if self.uat_acceptance_claimed:
            raise ValueError("Trial samples must not claim UAT acceptance")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.10 trial generated sample is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class TrialDocumentSetModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trial_set_id: str = Field(min_length=1, pattern=r"^TRIALSET-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: TrialDocumentSetStatus = "controlled_trial_document_set"
    scenario_id: str = Field(min_length=1, pattern=r"^TRIAL-[A-Z0-9-]+@v[0-9]+$")
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    generated_artifacts: list[TrialGeneratedArtifactRefModel] = Field(min_length=1)
    trial_set_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("trial_set_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_set_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank trial document set value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_trial_set_boundary(self):
        self._validate_trial_set_id_version_alignment()
        self._validate_unique_sample_ids()
        self._validate_sample_alignment()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_trial_set_id_version_alignment(self) -> None:
        if not self.trial_set_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Trial document set version must match trial_set_id suffix: "
                f"{self.trial_set_id} / {self.version}"
            )

    def _validate_unique_sample_ids(self) -> None:
        sample_ids: set[str] = set()
        for sample in self.generated_artifacts:
            if sample.sample_id in sample_ids:
                raise ValueError(
                    "Duplicate trial generated sample id is not allowed: "
                    f"{sample.sample_id}"
                )
            sample_ids.add(sample.sample_id)

    def _validate_sample_alignment(self) -> None:
        for sample in self.generated_artifacts:
            if sample.scenario_id != self.scenario_id:
                raise ValueError(
                    "Trial sample scenario_id must match trial set scenario_id: "
                    f"{sample.sample_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.10 trial document set is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
