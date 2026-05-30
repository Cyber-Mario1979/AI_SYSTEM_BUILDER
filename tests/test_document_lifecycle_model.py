from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.document_lifecycle_model import (
    DocumentLifecycleRecordModel,
    DocumentLifecycleRuleLibraryModel,
)
from asbp.document_lifecycle_store import load_default_document_lifecycle_rule_library


REQUIRED_CLAIMS = [
    "does_not_create_qms_approval_records",
    "does_not_create_electronic_signatures",
    "does_not_validate_product_ready_output",
    "does_not_release_or_deploy_documents",
]


def _minimal_obligation(obligation_id: str, obligation_type: str) -> dict:
    return {
        "obligation_id": obligation_id,
        "obligation_type": obligation_type,
        "description": "Controlled obligation.",
        "required": True,
        "resolved": False,
    }


def _minimal_record_payload() -> dict:
    return {
        "lifecycle_record_id": "LIFECYCLE-QUALIFICATION-PLAN@v1",
        "version": "v1",
        "status": "runtime_facing_document_lifecycle_record",
        "lifecycle_state": "draft",
        "source_artifact_id": "ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        "source_draft_id": "DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "standards_control_packet_id": "STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        "output_format": "markdown",
        "artifact_metadata_ref": "ART-QUALIFICATION-PLAN-MARKDOWN@v1::metadata",
        "review_obligations": [
            _minimal_obligation("OBL-TECHNICAL-REVIEW@v1", "technical_review"),
        ],
        "approval_obligations": [
            _minimal_obligation("OBL-APPROVAL-READINESS@v1", "approval_readiness"),
        ],
        "task_closure_dependencies": [
            _minimal_obligation("OBL-TASK-CLOSURE-DEPENDENCIES@v1", "task_closure_dependency"),
        ],
        "placeholder_present": True,
        "limitation_present": True,
        "standards_warning_present": True,
        "carried_forward_limitations": [
            "Renderer metadata indicates visible placeholders are present.",
        ],
        "transition_history": [
            {
                "from_state": None,
                "to_state": "draft",
                "transition_reason": "Lifecycle record created.",
            }
        ],
        "explicit_non_implementation_claims": REQUIRED_CLAIMS,
    }


def test_default_document_lifecycle_rule_library_loads():
    library = load_default_document_lifecycle_rule_library()

    assert library.library_id == "M29_DOCUMENT_LIFECYCLE_RULE_LIBRARY@v1"
    assert library.lifecycle_rules[0].rule_id == "LIFERULE-M29-DOCUMENT-WORKFLOW@v1"
    assert "draft" in library.lifecycle_rules[0].allowed_states
    assert "superseded" in library.lifecycle_rules[0].allowed_states


def test_lifecycle_record_accepts_controlled_draft_state():
    record = DocumentLifecycleRecordModel(**_minimal_record_payload())

    assert record.lifecycle_state == "draft"
    assert record.placeholder_present is True


def test_approved_ready_requires_review_obligations_resolved():
    payload = _minimal_record_payload()
    payload["lifecycle_state"] = "approved_ready"

    with pytest.raises(ValidationError) as exc_info:
        DocumentLifecycleRecordModel(**payload)

    assert "requires resolved review obligations" in str(exc_info.value)


def test_final_ready_requires_task_dependencies_resolved():
    payload = _minimal_record_payload()
    payload["lifecycle_state"] = "final_ready"
    payload["review_obligations"][0]["resolved"] = True
    payload["approval_obligations"][0]["resolved"] = True

    with pytest.raises(ValidationError) as exc_info:
        DocumentLifecycleRecordModel(**payload)

    assert "requires resolved task closure dependencies" in str(exc_info.value)


def test_superseded_requires_replacement_record_reference():
    payload = _minimal_record_payload()
    payload["lifecycle_state"] = "superseded"

    with pytest.raises(ValidationError) as exc_info:
        DocumentLifecycleRecordModel(**payload)

    assert "requires superseded_by_record_id" in str(exc_info.value)


def test_lifecycle_rule_library_rejects_duplicate_rule_ids():
    library = load_default_document_lifecycle_rule_library().model_dump()
    library["lifecycle_rules"].append(deepcopy(library["lifecycle_rules"][0]))

    with pytest.raises(ValidationError) as exc_info:
        DocumentLifecycleRuleLibraryModel(**library)

    assert "Duplicate document lifecycle rule id" in str(exc_info.value)


def test_lifecycle_record_requires_non_implementation_claims():
    payload = _minimal_record_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_create_qms_approval_records",
    ]

    with pytest.raises(ValidationError) as exc_info:
        DocumentLifecycleRecordModel(**payload)

    assert "missing explicit" in str(exc_info.value)
