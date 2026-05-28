import pytest
from pydantic import ValidationError

from asbp.standards_applicability_model import (
    StandardsApplicabilityContractModel,
    StandardsApplicabilityDecisionModel,
    StandardsApplicabilitySourceCandidateModel,
)


def _verified_annex_15_source() -> StandardsApplicabilitySourceCandidateModel:
    return StandardsApplicabilitySourceCandidateModel(
        std_id="STD-EU-GMP-ANNEX-15",
        registry_version="v0.1",
        authority_status="authoritative",
        verification_status="verified",
        mandatory_flag="mandatory_when_applicable",
        citation_depths=["document", "section", "clause"],
        applicability_scope=["qualification", "validation"],
    )


def _applicable_annex_15_decision() -> StandardsApplicabilityDecisionModel:
    return StandardsApplicabilityDecisionModel(
        decision_id="APP-EU-GMP-ANNEX-15-QUALIFICATION@v1",
        standard=_verified_annex_15_source(),
        applicability_triggers=["gmp_relevance", "lifecycle_phase"],
        input_dimensions=[
            {
                "dimension_id": "lifecycle_phase",
                "value": "qualification",
                "value_source": "selector_context",
            }
        ],
        decision_state="applicable",
        decision_rationale="Qualification scope is GMP-relevant.",
        mandatory_use_allowed=True,
        downstream_use_limits=[
            "Citation depth must not exceed verified clause evidence."
        ],
    )


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_parse_runtime_registry",
        "does_not_validate_citations",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_generate_product_ready_standards_output",
    ]


def test_applicability_contract_accepts_verified_applicable_mandatory_source():
    contract = StandardsApplicabilityContractModel(
        contract_id="M28_2_STANDARDS_APPLICABILITY_CONTRACT@v1",
        version="v1",
        registry_version="v0.1",
        decision_records=[_applicable_annex_15_decision()],
        contract_controls=[
            "A standards source must be applicable before downstream use."
        ],
        explicit_non_implementation_claims=_required_non_implementation_claims(),
    )

    assert contract.contract_id == "M28_2_STANDARDS_APPLICABILITY_CONTRACT@v1"
    assert contract.decision_records[0].mandatory_use_allowed is True


def test_registry_presence_alone_cannot_make_source_applicable():
    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilityDecisionModel(
            decision_id="APP-REGISTRY-PRESENCE-ONLY@v1",
            standard=_verified_annex_15_source(),
            applicability_triggers=["registry_presence"],
            input_dimensions=[
                {
                    "dimension_id": "registry_version",
                    "value": "v0.1",
                    "value_source": "registry_record",
                }
            ],
            decision_state="applicable",
            decision_rationale="The source is listed in the registry.",
            mandatory_use_allowed=True,
        )

    assert "Registry presence alone cannot make a standard applicable" in str(
        exc_info.value
    )


def test_limited_source_requires_visible_source_limitations():
    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilitySourceCandidateModel(
            std_id="STD-EU-GMP-ANNEX-11",
            registry_version="v0.1",
            authority_status="authoritative",
            verification_status="pending_verification",
            mandatory_flag="mandatory_when_applicable",
            citation_depths=["document"],
            applicability_scope=["computerized_systems"],
        )

    assert "Source limitations are required for limited standards source candidate" in str(
        exc_info.value
    )


def test_source_limitations_must_propagate_to_applicability_decision():
    pending_source = StandardsApplicabilitySourceCandidateModel(
        std_id="STD-FDA-21CFR11",
        registry_version="v0.1",
        authority_status="authoritative",
        verification_status="pending_verification",
        mandatory_flag="mandatory_when_applicable",
        citation_depths=["document"],
        applicability_scope=["electronic_records"],
        source_limitations=[
            "Version and effective date are pending verification."
        ],
    )

    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilityDecisionModel(
            decision_id="APP-FDA-21CFR11-ERS@v1",
            standard=pending_source,
            applicability_triggers=["electronic_records_or_signatures"],
            input_dimensions=[
                {
                    "dimension_id": "electronic_records",
                    "value": "in_scope",
                    "value_source": "user_input",
                }
            ],
            decision_state="conditional",
            decision_rationale="Electronic records may be in scope.",
        )

    assert "Source limitations must propagate to applicability decision" in str(
        exc_info.value
    )


def test_reference_source_cannot_drive_mandatory_output():
    reference_source = StandardsApplicabilitySourceCandidateModel(
        std_id="STD-ASTM-E2500",
        registry_version="v0.1",
        authority_status="reference",
        verification_status="verified",
        mandatory_flag="not_mandatory_unless_adopted",
        citation_depths=["document"],
        applicability_scope=["verification_strategy"],
        source_limitations=[
            "Reference source cannot drive mandatory output unless adopted."
        ],
    )

    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilityDecisionModel(
            decision_id="APP-ASTM-E2500-MANDATORY@v1",
            standard=reference_source,
            applicability_triggers=["gmp_relevance", "project_acceptance_criteria"],
            input_dimensions=[
                {
                    "dimension_id": "acceptance_basis",
                    "value": "verification_strategy",
                    "value_source": "user_input",
                }
            ],
            decision_state="applicable",
            decision_rationale="ASTM E2500 is relevant to the verification strategy.",
            mandatory_use_allowed=True,
            limitation_statements=[
                "Reference source cannot drive mandatory output unless adopted."
            ],
        )

    assert "Mandatory standards use requires authoritative or internal authority status" in str(
        exc_info.value
    )


def test_rejected_decision_requires_rejection_case():
    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilityDecisionModel(
            decision_id="APP-ANNEX-11-REJECTED@v1",
            standard=_verified_annex_15_source(),
            applicability_triggers=["system_type"],
            input_dimensions=[
                {
                    "dimension_id": "system_type",
                    "value": "manual_process",
                    "value_source": "selector_context",
                }
            ],
            decision_state="rejected",
            decision_rationale="Computerized-system scope is not present.",
        )

    assert "rejected standards decisions require rejection_cases" in str(
        exc_info.value
    )


def test_contract_requires_explicit_non_implementation_claims():
    with pytest.raises(ValidationError) as exc_info:
        StandardsApplicabilityContractModel(
            contract_id="M28_2_STANDARDS_APPLICABILITY_CONTRACT@v1",
            version="v1",
            registry_version="v0.1",
            decision_records=[_applicable_annex_15_decision()],
            contract_controls=[
                "A standards source must be applicable before downstream use."
            ],
            explicit_non_implementation_claims=[
                "does_not_parse_runtime_registry",
            ],
        )

    assert "M28.2 contract is missing explicit non-implementation claims" in str(
        exc_info.value
    )
