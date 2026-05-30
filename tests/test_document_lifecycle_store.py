import pytest

from asbp.document_lifecycle_store import (
    assert_document_lifecycle_rules_exist,
    get_default_document_lifecycle_rule,
    get_document_lifecycle_rule_by_id,
    list_document_lifecycle_rule_ids,
    load_default_document_lifecycle_rule_library,
    load_document_lifecycle_rule_library_from_payload,
)


def test_document_lifecycle_rule_store_loads_default_rule():
    library = load_default_document_lifecycle_rule_library()

    assert list_document_lifecycle_rule_ids(library) == [
        "LIFERULE-M29-DOCUMENT-WORKFLOW@v1"
    ]
    assert get_default_document_lifecycle_rule(library).rule_id == (
        "LIFERULE-M29-DOCUMENT-WORKFLOW@v1"
    )
    assert get_document_lifecycle_rule_by_id(
        library,
        "LIFERULE-M29-DOCUMENT-WORKFLOW@v1",
    ).version == "v1"


def test_document_lifecycle_rule_missing_ids_are_reported():
    library = load_default_document_lifecycle_rule_library()

    with pytest.raises(ValueError) as exc_info:
        assert_document_lifecycle_rules_exist(
            library,
            {"LIFERULE-MISSING@v1"},
        )

    assert "LIFERULE-MISSING@v1" in str(exc_info.value)


def test_persisted_state_payload_is_not_lifecycle_rule_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_document_lifecycle_rule_library_from_payload(persisted_state_payload)

    assert "document lifecycle rule library payload must include lifecycle_rules" in str(
        exc_info.value
    )
