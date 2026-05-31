from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.standards_intake_model import (
    StandardsIntakeContractModel,
    StandardsIntakeRecordModel,
)


def _approved_internal_record_payload() -> dict:
    return {
        "intake_id": "INTAKE-LOCAL-CLEANROOM@v1",
        "version": "v1",
        "status": "approved_internal",
        "std_id": "STD-LOCAL-CLEANROOM-NONSTERILE",
        "source_name": "Local non-sterile cleanroom standard",
        "source_type": "local_standard",
        "source_owner": "Project Owner",
        "source_location": "user-provided local matrix reference",
        "authority_status": "internal",
        "verification_status": "not_externally_verifiable",
        "mandatory_flag": "mandatory_when_applicable",
        "version_or_effective_date": "v1 internal approval",
        "jurisdiction_or_owner": "Project Owner / local site",
        "applicability_scope": ["non-sterile cleanroom", "HVAC qualification"],
        "applicability_conditions": [
            "Applies only when internally approved for the declared site scope."
        ],
        "citation_depths": ["document", "requirement", "table_row"],
        "authority_decision": {
            "decision_status": "approved_binding_internal",
            "decision_owner": "Project Owner",
            "decision_reference": "INT-APPROVAL-LOCAL-CLEANROOM@v1",
            "decision_rationale": "Approved as internal cleanroom baseline for planning.",
            "residual_limitations": [
                "Internal approval is not public regulation or regulatory equivalence."
            ],
        },
        "comparison_control": {
            "comparison_status": "comparison_completed",
            "applicable_baseline_source_ids": ["STD-ISO-14644"],
            "comparison_id": "CMP-LOCAL-CLEANROOM-ISO14644@v1",
            "selected_less_strict_than_baseline": False,
            "comparison_limitations": [
                "Comparison is limited to the supplied local matrix fields."
            ],
        },
        "may_drive_mandatory_use": True,
        "limitation_statements": [
            "Internal/local source is binding only inside the approved scope.",
            "This intake record is not public regulation.",
        ],
        "public_regulation_claimed": False,
    }


def _draft_record_payload() -> dict:
    payload = _approved_internal_record_payload()
    payload.update(
        {
            "intake_id": "INTAKE-COMPANY-DRAFT@v1",
            "status": "draft_source_record",
            "std_id": "STD-COMPANY-DRAFT-CQV",
            "source_type": "company_standard",
            "source_name": "Draft company CQV standard",
            "authority_status": "tbd",
            "verification_status": "user_provided",
            "mandatory_flag": "not_mandatory_until_internal_approval",
            "version_or_effective_date": "TBD",
            "may_drive_mandatory_use": False,
            "authority_decision": {
                "decision_status": "pending_decision",
            },
            "comparison_control": {
                "comparison_status": "comparison_required",
                "applicable_baseline_source_ids": ["STD-EU-GMP-ANNEX-15"],
                "comparison_limitations": [
                    "Comparison cannot support mandatory use before authority decision."
                ],
            },
            "limitation_statements": [
                "Draft user-provided source remains pending authority decision."
            ],
        }
    )
    return payload


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_parse_uploaded_standard_files",
        "does_not_mutate_runtime_registry",
        "does_not_verify_public_regulation_status",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_generate_product_ready_standards_output",
    ]


def _contract_payload(record: dict | None = None) -> dict:
    return {
        "contract_id": "M28_7_STANDARDS_INTAKE_CONTRACT@v1",
        "version": "v1",
        "intake_records": [record or _approved_internal_record_payload()],
        "contract_controls": [
            "Local/company/site/client standards intake records are controlled source contracts."
        ],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_intake_contract_accepts_approved_internal_source_with_comparison_path():
    contract = StandardsIntakeContractModel(**_contract_payload())

    record = contract.intake_records[0]
    assert record.std_id == "STD-LOCAL-CLEANROOM-NONSTERILE"
    assert record.may_drive_mandatory_use is True
    assert record.comparison_control.comparison_id == "CMP-LOCAL-CLEANROOM-ISO14644@v1"


def test_draft_user_provided_source_is_allowed_with_visible_limitations():
    record = StandardsIntakeRecordModel(**_draft_record_payload())

    assert record.status == "draft_source_record"
    assert record.may_drive_mandatory_use is False
    assert record.authority_decision.decision_status == "pending_decision"


def test_std_id_must_use_local_company_site_or_client_prefix():
    payload = _approved_internal_record_payload()
    payload["std_id"] = "STD-PUBLIC-ISO14644"

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "String should match pattern" in str(exc_info.value)


def test_source_type_must_match_std_id_prefix():
    payload = _approved_internal_record_payload()
    payload["source_type"] = "company_standard"

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "source type does not match std_id prefix" in str(exc_info.value)


def test_limited_intake_requires_visible_limitations():
    payload = _draft_record_payload()
    payload["limitation_statements"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "requires limitation_statements" in str(exc_info.value)


def test_approved_internal_decision_requires_owner_reference_and_rationale():
    payload = _approved_internal_record_payload()
    payload["authority_decision"]["decision_owner"] = None

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "Approved internal standards intake decision requires" in str(exc_info.value)
    assert "decision_owner" in str(exc_info.value)


def test_mandatory_use_requires_approved_binding_internal_decision():
    payload = _approved_internal_record_payload()
    payload["authority_decision"] = {"decision_status": "pending_decision"}

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "approved_internal intake status requires approved_binding_internal" in str(
        exc_info.value
    )


def test_mandatory_use_requires_completed_m28_5_comparison_path():
    payload = _approved_internal_record_payload()
    payload["comparison_control"] = {
        "comparison_status": "comparison_required",
        "applicable_baseline_source_ids": ["STD-ISO-14644"],
        "comparison_limitations": ["Comparison pending."],
    }

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "requires completed comparison path" in str(exc_info.value)


def test_less_strict_internal_selection_requires_override_path():
    payload = _approved_internal_record_payload()
    payload["comparison_control"] = {
        "comparison_status": "override_completed",
        "applicable_baseline_source_ids": ["STD-ISO-14644"],
        "comparison_id": "CMP-LOCAL-CLEANROOM-ISO14644@v1",
        "selected_less_strict_than_baseline": True,
        "comparison_limitations": [
            "Selected local requirement is less strict and requires override."
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "requires override_id" in str(exc_info.value)


def test_public_regulation_claim_is_rejected_for_local_intake():
    payload = _approved_internal_record_payload()
    payload["public_regulation_claimed"] = True

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeRecordModel(**payload)

    assert "must not claim public regulation status" in str(exc_info.value)


def test_contract_rejects_duplicate_std_ids():
    first = _approved_internal_record_payload()
    second = deepcopy(first)
    second["intake_id"] = "INTAKE-LOCAL-CLEANROOM-DUPLICATE@v1"
    payload = _contract_payload(first)
    payload["intake_records"].append(second)

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeContractModel(**payload)

    assert "Duplicate standards intake std_id is not allowed" in str(exc_info.value)


def test_contract_requires_explicit_non_implementation_claims():
    payload = _contract_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_parse_uploaded_standard_files",
    ]

    with pytest.raises(ValidationError) as exc_info:
        StandardsIntakeContractModel(**payload)

    assert "M28.7 standards intake contract is missing" in str(exc_info.value)
