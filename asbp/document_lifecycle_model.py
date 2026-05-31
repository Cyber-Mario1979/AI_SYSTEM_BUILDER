from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentLifecycleRuleLibraryStatus = Literal["runtime_facing_document_lifecycle_rule_source"]
DocumentLifecycleRuleStatus = Literal["runtime_facing_document_lifecycle_rule"]
DocumentLifecycleRecordStatus = Literal["runtime_facing_document_lifecycle_record"]
DocumentLifecycleState = Literal[
    "draft",
    "in_review",
    "approved_ready",
    "final_ready",
    "superseded",
]
DocumentLifecycleObligationType = Literal[
    "technical_review",
    "quality_review",
    "approval_readiness",
    "task_closure_dependency",
]

REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS = {
    "does_not_create_qms_approval_records",
    "does_not_create_electronic_signatures",
    "does_not_validate_product_ready_output",
    "does_not_release_or_deploy_documents",
}


class DocumentLifecycleTransitionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_state: DocumentLifecycleState
    to_state: DocumentLifecycleState
    transition_controls: list[str] = Field(min_length=1)

    @field_validator("transition_controls")
    @classmethod
    def validate_no_blank_transition_controls(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document lifecycle transition control is not allowed")
        return values


class DocumentLifecycleObligationModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    obligation_id: str = Field(min_length=1, pattern=r"^OBL-[A-Z0-9-]+@v[0-9]+$")
    obligation_type: DocumentLifecycleObligationType
    description: str = Field(min_length=1)
    required: bool = True
    resolved: bool = False
    source_ref: str | None = Field(default=None, min_length=1)


class DocumentLifecycleRuleModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, pattern=r"^LIFERULE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentLifecycleRuleStatus = "runtime_facing_document_lifecycle_rule"
    allowed_states: list[DocumentLifecycleState] = Field(min_length=1)
    allowed_transitions: list[DocumentLifecycleTransitionModel] = Field(min_length=1)
    required_review_obligations: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    required_approval_obligations: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    required_task_closure_dependencies: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    supersession_controls: list[str] = Field(min_length=1)
    limitation_carry_forward_controls: list[str] = Field(min_length=1)
    rule_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator(
        "supersession_controls",
        "limitation_carry_forward_controls",
        "rule_controls",
        "explicit_non_implementation_claims",
    )
    @classmethod
    def validate_no_blank_rule_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document lifecycle rule value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_rule_boundary(self):
        self._validate_rule_id_version_alignment()
        self._validate_unique_states()
        self._validate_unique_transitions()
        self._validate_obligation_types()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_rule_id_version_alignment(self) -> None:
        if not self.rule_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Document lifecycle rule version must match rule_id suffix: "
                f"{self.rule_id} / {self.version}"
            )

    def _validate_unique_states(self) -> None:
        if len(set(self.allowed_states)) != len(self.allowed_states):
            raise ValueError("Duplicate document lifecycle allowed_states are not allowed")

    def _validate_unique_transitions(self) -> None:
        transition_keys: set[tuple[str, str]] = set()
        for transition in self.allowed_transitions:
            if transition.from_state not in self.allowed_states:
                raise ValueError(
                    "Lifecycle transition from_state must be in allowed_states: "
                    f"{transition.from_state}"
                )
            if transition.to_state not in self.allowed_states:
                raise ValueError(
                    "Lifecycle transition to_state must be in allowed_states: "
                    f"{transition.to_state}"
                )
            key = (transition.from_state, transition.to_state)
            if key in transition_keys:
                raise ValueError(
                    "Duplicate document lifecycle transition is not allowed: "
                    f"{transition.from_state}->{transition.to_state}"
                )
            transition_keys.add(key)

    def _validate_obligation_types(self) -> None:
        for obligation in self.required_review_obligations:
            if obligation.obligation_type not in {"technical_review", "quality_review"}:
                raise ValueError(
                    "Review obligations must use a review obligation type: "
                    f"{obligation.obligation_id}"
                )
        for obligation in self.required_approval_obligations:
            if obligation.obligation_type != "approval_readiness":
                raise ValueError(
                    "Approval obligations must use approval_readiness: "
                    f"{obligation.obligation_id}"
                )
        for obligation in self.required_task_closure_dependencies:
            if obligation.obligation_type != "task_closure_dependency":
                raise ValueError(
                    "Task closure dependencies must use task_closure_dependency: "
                    f"{obligation.obligation_id}"
                )

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.8 document lifecycle rule is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentLifecycleRuleLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1, pattern=r"^M29_DOCUMENT_LIFECYCLE_RULE_LIBRARY@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentLifecycleRuleLibraryStatus = "runtime_facing_document_lifecycle_rule_source"
    lifecycle_rules: list[DocumentLifecycleRuleModel] = Field(min_length=1)
    library_controls: list[str] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("library_controls", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_library_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document lifecycle library value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_lifecycle_rule_library_boundary(self):
        self._validate_unique_rule_ids()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_unique_rule_ids(self) -> None:
        rule_ids: set[str] = set()
        for rule in self.lifecycle_rules:
            if rule.rule_id in rule_ids:
                raise ValueError(
                    "Duplicate document lifecycle rule id is not allowed: "
                    f"{rule.rule_id}"
                )
            rule_ids.add(rule.rule_id)

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.8 document lifecycle rule library is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )


class DocumentLifecycleTransitionHistoryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_state: DocumentLifecycleState | None = None
    to_state: DocumentLifecycleState
    transition_reason: str = Field(min_length=1)


class DocumentLifecycleRecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lifecycle_record_id: str = Field(min_length=1, pattern=r"^LIFECYCLE-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: DocumentLifecycleRecordStatus = "runtime_facing_document_lifecycle_record"
    lifecycle_state: DocumentLifecycleState
    source_artifact_id: str = Field(min_length=1, pattern=r"^ART-[A-Z0-9-]+@v[0-9]+$")
    source_draft_id: str = Field(min_length=1, pattern=r"^DRAFT-[A-Z0-9-]+@v[0-9]+$")
    template_id: str = Field(min_length=1, pattern=r"^TPL-[A-Z0-9-]+@v[0-9]+$")
    schema_id: str = Field(min_length=1, pattern=r"^SCHEMA-[A-Z0-9-]+@v[0-9]+$")
    standards_control_packet_id: str = Field(min_length=1, pattern=r"^STDOUT-[A-Z0-9-]+@v[0-9]+$")
    output_format: str = Field(min_length=1)
    artifact_metadata_ref: str = Field(min_length=1)
    review_obligations: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    approval_obligations: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    task_closure_dependencies: list[DocumentLifecycleObligationModel] = Field(min_length=1)
    supersedes_record_id: str | None = Field(default=None, pattern=r"^LIFECYCLE-[A-Z0-9-]+@v[0-9]+$")
    superseded_by_record_id: str | None = Field(default=None, pattern=r"^LIFECYCLE-[A-Z0-9-]+@v[0-9]+$")
    placeholder_present: bool
    limitation_present: bool
    standards_warning_present: bool
    carried_forward_limitations: list[str] = Field(min_length=1)
    transition_history: list[DocumentLifecycleTransitionHistoryModel] = Field(min_length=1)
    explicit_non_implementation_claims: list[str] = Field(min_length=1)

    @field_validator("carried_forward_limitations", "explicit_non_implementation_claims")
    @classmethod
    def validate_no_blank_record_values(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank document lifecycle record value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_lifecycle_record_boundary(self):
        self._validate_record_id_version_alignment()
        self._validate_unique_obligations()
        self._validate_state_obligations()
        self._validate_supersession_boundary()
        self._validate_required_non_implementation_claims()
        return self

    def _validate_record_id_version_alignment(self) -> None:
        if not self.lifecycle_record_id.endswith(f"@{self.version}"):
            raise ValueError(
                "Document lifecycle record version must match lifecycle_record_id suffix: "
                f"{self.lifecycle_record_id} / {self.version}"
            )

    def _validate_unique_obligations(self) -> None:
        obligation_ids: set[str] = set()
        for obligation in [
            *self.review_obligations,
            *self.approval_obligations,
            *self.task_closure_dependencies,
        ]:
            if obligation.obligation_id in obligation_ids:
                raise ValueError(
                    "Duplicate document lifecycle obligation id is not allowed: "
                    f"{obligation.obligation_id}"
                )
            obligation_ids.add(obligation.obligation_id)

    def _validate_state_obligations(self) -> None:
        if self.lifecycle_state in {"approved_ready", "final_ready"}:
            unresolved_reviews = [
                obligation.obligation_id
                for obligation in self.review_obligations
                if obligation.required and not obligation.resolved
            ]
            if unresolved_reviews:
                raise ValueError(
                    "Approved-ready lifecycle state requires resolved review obligations: "
                    f"{', '.join(unresolved_reviews)}"
                )

        if self.lifecycle_state == "final_ready":
            unresolved_approvals = [
                obligation.obligation_id
                for obligation in self.approval_obligations
                if obligation.required and not obligation.resolved
            ]
            unresolved_dependencies = [
                obligation.obligation_id
                for obligation in self.task_closure_dependencies
                if obligation.required and not obligation.resolved
            ]
            if unresolved_approvals:
                raise ValueError(
                    "Final-ready lifecycle state requires resolved approval obligations: "
                    f"{', '.join(unresolved_approvals)}"
                )
            if unresolved_dependencies:
                raise ValueError(
                    "Final-ready lifecycle state requires resolved task closure dependencies: "
                    f"{', '.join(unresolved_dependencies)}"
                )

    def _validate_supersession_boundary(self) -> None:
        if self.lifecycle_state == "superseded" and self.superseded_by_record_id is None:
            raise ValueError("Superseded lifecycle record requires superseded_by_record_id")
        if self.lifecycle_state != "superseded" and self.superseded_by_record_id is not None:
            raise ValueError("Only superseded lifecycle records may include superseded_by_record_id")

    def _validate_required_non_implementation_claims(self) -> None:
        provided_claims = set(self.explicit_non_implementation_claims)
        missing_claims = sorted(
            REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS - provided_claims
        )
        if missing_claims:
            raise ValueError(
                "M29.8 document lifecycle record is missing explicit "
                f"non-implementation claims: {', '.join(missing_claims)}"
            )
