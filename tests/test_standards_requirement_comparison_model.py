from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.standards_requirement_comparison_model import (
    StandardsComparedRequirementModel,
    StandardsRequirementComparisonContractModel,
    StandardsRequirementComparisonRecordModel,
)


def _annex_15_requirement() -> StandardsComparedRequirementModel:
    return StandardsComparedRequirementModel(
        requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
        std_id="STD-EU-GMP-ANNEX-15",
        registry_version="v0.1",
        requirement_reference="STD-EU-GMP-ANNEX-15 document-level requirement",
        requirement_summary="Qualification acceptance criteria must remain justified and controlled.",
        applicability_decision_id="APP-EU-GMP-ANNEX-15-QUALIFICATION@v1",
        applicability_state="applicable",
        authority_status="authoritative",
        verification_status="verified",
        mandatory_flag="mandatory_when_applicable",
        mandatory_use_allowed=True,
        comparison_basis="acceptance_criteria",
        strictness_rank=90,
        strictness_rationale=(
            "Mandatory applicable GMP qualification expectation controls the "
            "acceptance basis."
        ),
    )


def _astm_e2500_requirement() -> StandardsComparedRequirementModel:
    return StandardsComparedRequirementModel(
        requirement_id="REQ-ASTM-E2500-VERIFICATION@v1",
        std_id="STD-ASTM-E2500",
        registry_version="v0.1",
        requirement_reference="STD-ASTM-E2500 document-level verification approach",
        requirement_summary="Science and risk-based verification approach may support strategy.",
        applicability_state="conditional",
        authority_status="reference",
        verification_status="pending_verification",
        mandatory_flag="not_mandatory_unless_adopted",
        mandatory_use_allowed=False,
        comparison_basis="acceptance_criteria",
        strictness_rank=50,
        strictness_rationale=(
            "Reference approach may support strategy but cannot weaken mandatory "
            "GMP expectations unless adopted and controlled."
        ),
        limitation_statements=[
            "Reference source is pending verification and is not independently mandatory."
        ],
    )


def _comparison_record() -> StandardsRequirementComparisonRecordModel:
    return StandardsRequirementComparisonRecordModel(
        comparison_id="CMP-CQV-ACCEPTANCE-CRITERIA@v1",
        version="v1",
        comparison_scope="Qualification acceptance criteria source comparison.",
        compared_requirements=[
            _annex_15_requirement(),
            _astm_e2500_requirement(),
        ],
        stricter_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
        selected_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
        comparison_outcome="select_stricter_requirement",
        comparison_controls=[
            "Risk-based rationale may support scope and testing strategy.",
            "Risk-based rationale must not silently weaken mandatory applicable requirements.",
        ],
        limitation_statements=[
            "ASTM E2500 remains a reference source unless adopted for the applicable scope."
        ],
    )


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_interpret_standards_text",
        "does_not_implement_controlled_override_records",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_generate_product_ready_standards_output",
    ]


def test_comparison_contract_accepts_selected_stricter_requirement():
    contract = StandardsRequirementComparisonContractModel(
        contract_id="M28_5_STANDARDS_REQUIREMENT_COMPARISON_CONTRACT@v1",
        version="v1",
        comparison_records=[_comparison_record()],
        contract_controls=[
            "The stricter applicable requirement is selected by explicit comparison record."
        ],
        explicit_non_implementation_claims=_required_non_implementation_claims(),
    )

    assert contract.status == "runtime_facing_contract"
    assert contract.comparison_records[0].selected_requirement_id == (
        "REQ-ANNEX15-PQ-ACCEPTANCE@v1"
    )


def test_comparison_record_requires_at_least_two_requirements():
    with pytest.raises(ValidationError) as exc_info:
        StandardsRequirementComparisonRecordModel(
            comparison_id="CMP-SINGLE-SOURCE@v1",
            version="v1",
            comparison_scope="Invalid single-source comparison.",
            compared_requirements=[_annex_15_requirement()],
            stricter_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
            selected_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
            comparison_outcome="select_stricter_requirement",
            comparison_controls=["Single-source comparison is invalid."],
        )

    assert "at least 2 items" in str(exc_info.value)


def test_mandatory_comparison_requires_applicable_source():
    with pytest.raises(ValidationError) as exc_info:
        StandardsComparedRequirementModel(
            requirement_id="REQ-ANNEX15-NOT-APPLICABLE@v1",
            std_id="STD-EU-GMP-ANNEX-15",
            registry_version="v0.1",
            requirement_reference="STD-EU-GMP-ANNEX-15 document-level requirement",
            requirement_summary="Qualification expectation.",
            applicability_state="not_applicable",
            authority_status="authoritative",
            verification_status="verified",
            mandatory_flag="mandatory_when_applicable",
            mandatory_use_allowed=True,
            comparison_basis="acceptance_criteria",
            strictness_rank=90,
            strictness_rationale="Mandatory requirement cannot be used when not applicable.",
        )

    assert "Mandatory standards comparison requires an applicable source" in str(
        exc_info.value
    )


def test_limited_requirement_requires_visible_limitations():
    with pytest.raises(ValidationError) as exc_info:
        StandardsComparedRequirementModel(
            requirement_id="REQ-ASTM-NO-LIMITS@v1",
            std_id="STD-ASTM-E2500",
            registry_version="v0.1",
            requirement_reference="STD-ASTM-E2500 document-level verification approach",
            requirement_summary="Reference verification approach.",
            applicability_state="conditional",
            authority_status="reference",
            verification_status="pending_verification",
            mandatory_flag="not_mandatory_unless_adopted",
            mandatory_use_allowed=False,
            comparison_basis="acceptance_criteria",
            strictness_rank=50,
            strictness_rationale="Reference source remains limited.",
        )

    assert "Limited standards comparison requirement requires limitation_statements" in str(
        exc_info.value
    )


def test_risk_based_rationale_cannot_select_less_strict_without_override():
    with pytest.raises(ValidationError) as exc_info:
        StandardsRequirementComparisonRecordModel(
            comparison_id="CMP-RISK-WEAKENS-MANDATORY@v1",
            version="v1",
            comparison_scope="Invalid risk-based weakening comparison.",
            compared_requirements=[
                _annex_15_requirement(),
                _astm_e2500_requirement(),
            ],
            stricter_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
            selected_requirement_id="REQ-ASTM-E2500-VERIFICATION@v1",
            comparison_outcome="select_less_strict_with_override",
            comparison_controls=[
                "Risk-based rationale must not weaken mandatory requirements silently."
            ],
            limitation_statements=[
                "Less strict selection would require controlled override evidence."
            ],
            risk_based_rationale="Risk-based approach preferred for project efficiency.",
        )

    assert "requires override_path_reference" in str(exc_info.value)


def test_less_strict_selection_requires_and_accepts_override_path_reference():
    comparison = StandardsRequirementComparisonRecordModel(
        comparison_id="CMP-LESS-STRICT-WITH-OVERRIDE@v1",
        version="v1",
        comparison_scope="Controlled less-strict selection path.",
        compared_requirements=[
            _annex_15_requirement(),
            _astm_e2500_requirement(),
        ],
        stricter_requirement_id="REQ-ANNEX15-PQ-ACCEPTANCE@v1",
        selected_requirement_id="REQ-ASTM-E2500-VERIFICATION@v1",
        comparison_outcome="select_less_strict_with_override",
        comparison_controls=[
            "Less-strict selection requires controlled override evidence."
        ],
        limitation_statements=[
            "Less-strict selection is not regulatory equivalence and requires M28.6 override control."
        ],
        risk_based_rationale="Risk-based strategy proposed by user.",
        override_path_reference="M28.6 controlled override record required before use.",
        override_limitation_statement=(
            "M28.5 records the override path only; it does not implement or approve "
            "the controlled override."
        ),
    )

    assert comparison.selected_requirement_id == "REQ-ASTM-E2500-VERIFICATION@v1"
    assert comparison.override_path_reference is not None


def test_stricter_requirement_id_must_match_highest_strictness_rank():
    with pytest.raises(ValidationError) as exc_info:
        StandardsRequirementComparisonRecordModel(
            comparison_id="CMP-WRONG-STRICTER-ID@v1",
            version="v1",
            comparison_scope="Invalid stricter requirement identity.",
            compared_requirements=[
                _annex_15_requirement(),
                _astm_e2500_requirement(),
            ],
            stricter_requirement_id="REQ-ASTM-E2500-VERIFICATION@v1",
            selected_requirement_id="REQ-ASTM-E2500-VERIFICATION@v1",
            comparison_outcome="select_stricter_requirement",
            comparison_controls=["Strictness identity must match strictness rank."],
            limitation_statements=[
                "Reference source limitation remains visible."
            ],
        )

    assert "highest strictness_rank" in str(exc_info.value)


def test_duplicate_comparison_ids_are_rejected():
    comparison = _comparison_record()

    with pytest.raises(ValidationError) as exc_info:
        StandardsRequirementComparisonContractModel(
            contract_id="M28_5_STANDARDS_REQUIREMENT_COMPARISON_CONTRACT@v1",
            version="v1",
            comparison_records=[
                comparison,
                deepcopy(comparison),
            ],
            contract_controls=["Duplicate comparison records are invalid."],
            explicit_non_implementation_claims=_required_non_implementation_claims(),
        )

    assert "Duplicate standards requirement comparison_id is not allowed" in str(
        exc_info.value
    )


def test_contract_requires_explicit_non_implementation_claims():
    with pytest.raises(ValidationError) as exc_info:
        StandardsRequirementComparisonContractModel(
            contract_id="M28_5_STANDARDS_REQUIREMENT_COMPARISON_CONTRACT@v1",
            version="v1",
            comparison_records=[_comparison_record()],
            contract_controls=["Non-implementation claims must remain explicit."],
            explicit_non_implementation_claims=[
                "does_not_interpret_standards_text",
            ],
        )

    assert "M28.5 comparison contract is missing explicit" in str(exc_info.value)
