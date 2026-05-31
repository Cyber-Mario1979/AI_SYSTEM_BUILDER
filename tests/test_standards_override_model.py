from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.standards_override_model import (
    StandardsControlledOverrideContractModel,
    StandardsControlledOverrideRecordModel,
)


def _stricter_requirement_reference() -> dict:
    return {
        "requirement_id": "REQ-EU-GMP-ANNEX-15-STRICT@v1",
        "std_id": "STD-EU-GMP-ANNEX-15",
        "requirement_role": "stricter_requirement",
        "requirement_reference": "STD-EU-GMP-ANNEX-15 document-level requirement",
        "requirement_summary": "The stricter applicable qualification expectation.",
        "authority_status": "authoritative",
        "verification_status": "verified",
        "mandatory_flag": "mandatory_when_applicable",
    }


def _selected_less_strict_requirement_reference() -> dict:
    return {
        "requirement_id": "REQ-ASTM-E2500-LESS-STRICT@v1",
        "std_id": "STD-ASTM-E2500",
        "requirement_role": "selected_less_strict_requirement",
        "requirement_reference": "STD-ASTM-E2500 planning reference",
        "requirement_summary": "A less strict verification-strategy reference.",
        "authority_status": "reference",
        "verification_status": "verified",
        "mandatory_flag": "not_mandatory_unless_adopted",
        "limitation_statements": [
            "Reference source cannot override stricter mandatory GMP expectations unless controlled and approved."
        ],
    }


def _valid_override_record_payload() -> dict:
    return {
        "override_id": "OVR-CQV-GMP-LESS-STRICT@v1",
        "version": "v1",
        "comparison_id": "CMP-CQV-GMP-STRICTNESS@v1",
        "stricter_requirement_id": "REQ-EU-GMP-ANNEX-15-STRICT@v1",
        "selected_requirement_id": "REQ-ASTM-E2500-LESS-STRICT@v1",
        "source_comparison_references": [
            _stricter_requirement_reference(),
            _selected_less_strict_requirement_reference(),
        ],
        "approver": {
            "approver_id": "APPROVER-QA-001",
            "approver_name": "QA Decision Owner",
            "approver_role": "Quality approval authority",
            "decision_status": "approved",
            "decision_reference": "QA-DECISION-001",
            "decision_date": "2026-05-29",
        },
        "reason_for_override": "Project-specific verification strategy is approved for the declared bounded scope.",
        "risk_quality_justification": "Residual GMP impact is controlled by additional review and documented acceptance.",
        "residual_risk_statement": "Residual risk remains visible and accepted only for this declared scope.",
        "applicability_boundary": [
            "Applies only to the named CQV planning decision and approved project scope."
        ],
        "limitation_statement": "Override weakens the selected requirement against the stricter applicable source and remains visibly limited.",
        "non_equivalence_statement": "This controlled override is not equivalent to regulatory approval.",
        "source_closure_boundary_statement": "This override does not close any standards source or registry limitation.",
        "override_controls": [
            "Override record must reference the source comparison decision.",
            "Override must not be treated as source closure.",
        ],
        "downstream_use_limits": [
            "May be used only as controlled planning evidence until later product output controls exist."
        ],
    }


def _valid_contract_payload(record: dict | None = None) -> dict:
    return {
        "contract_id": "M28_6_STANDARDS_CONTROLLED_OVERRIDE_CONTRACT@v1",
        "version": "v1",
        "override_records": [record or _valid_override_record_payload()],
        "contract_controls": [
            "Controlled overrides record bounded decisions; they do not create regulatory equivalence."
        ],
        "explicit_non_implementation_claims": [
            "does_not_create_regulatory_equivalence",
            "does_not_close_or_reclassify_sources",
            "does_not_approve_standards_without_human_decision",
            "does_not_generate_product_ready_standards_output",
        ],
    }


def test_controlled_override_contract_accepts_valid_less_strict_selection():
    contract = StandardsControlledOverrideContractModel(**_valid_contract_payload())

    override = contract.override_records[0]
    assert override.override_id == "OVR-CQV-GMP-LESS-STRICT@v1"
    assert override.selected_requirement_id == "REQ-ASTM-E2500-LESS-STRICT@v1"
    assert override.approver.decision_status == "approved"


def test_override_record_requires_approver():
    payload = _valid_override_record_payload()
    del payload["approver"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "approver" in str(exc_info.value)


def test_override_record_requires_residual_risk_statement():
    payload = _valid_override_record_payload()
    del payload["residual_risk_statement"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "residual_risk_statement" in str(exc_info.value)


def test_override_record_requires_applicability_boundary():
    payload = _valid_override_record_payload()
    payload["applicability_boundary"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "applicability_boundary" in str(exc_info.value)


def test_override_record_rejects_selecting_the_stricter_requirement():
    payload = _valid_override_record_payload()
    payload["selected_requirement_id"] = payload["stricter_requirement_id"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "selected_requirement_id to differ" in str(exc_info.value)


def test_override_record_requires_source_comparison_to_cover_selected_and_stricter():
    payload = _valid_override_record_payload()
    payload["source_comparison_references"][1][
        "requirement_role"
    ] = "stricter_requirement"

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "stricter and selected less-strict requirements" in str(exc_info.value)


def test_limited_selected_requirement_requires_visible_limitation():
    payload = _valid_override_record_payload()
    payload["source_comparison_references"][1]["limitation_statements"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "Limited controlled override requirement reference requires" in str(
        exc_info.value
    )


def test_override_record_rejects_regulatory_equivalence_claim():
    payload = _valid_override_record_payload()
    payload[
        "risk_quality_justification"
    ] = "This override is legally equivalent to regulation for the project."

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "must not claim regulatory equivalence" in str(exc_info.value)


def test_override_record_rejects_source_closure_claim():
    payload = _valid_override_record_payload()
    payload[
        "source_closure_boundary_statement"
    ] = "Source closure achieved for the selected standard."

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "source closure" in str(exc_info.value)


def test_override_record_requires_downstream_use_limits():
    payload = _valid_override_record_payload()
    payload["downstream_use_limits"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideRecordModel(**payload)

    assert "downstream_use_limits" in str(exc_info.value)


def test_override_contract_rejects_duplicate_override_ids():
    record = _valid_override_record_payload()
    payload = _valid_contract_payload(record)
    payload["override_records"].append(deepcopy(record))

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideContractModel(**payload)

    assert "Duplicate controlled override_id" in str(exc_info.value)


def test_override_contract_requires_explicit_non_implementation_claims():
    payload = _valid_contract_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_create_regulatory_equivalence"
    ]

    with pytest.raises(ValidationError) as exc_info:
        StandardsControlledOverrideContractModel(**payload)

    assert "M28.6 controlled override contract is missing" in str(exc_info.value)
