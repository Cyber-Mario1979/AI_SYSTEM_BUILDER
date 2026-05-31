import pytest

from asbp.document_input_schema_store import (
    assert_document_input_schemas_exist,
    find_missing_document_input_schema_ids,
    get_document_input_schema_by_id,
    get_document_input_schema_by_template_id,
    list_document_input_schema_ids,
    list_document_input_schema_ids_by_template,
    load_default_document_input_schema_library,
    load_document_input_schema_library_from_payload,
)

EXPECTED_SCHEMA_IDS = [
    "SCHEMA-QUALIFICATION-PLAN@v1",
    "SCHEMA-CSV-VALIDATION-PLAN@v1",
]


def test_default_document_input_schema_library_loads_controlled_records():
    library = load_default_document_input_schema_library()

    assert library.library_id == "M29_DOCUMENT_INPUT_SCHEMA_LIBRARY@v1"
    assert list_document_input_schema_ids(library) == EXPECTED_SCHEMA_IDS

    qualification_schema = get_document_input_schema_by_id(
        library,
        "SCHEMA-QUALIFICATION-PLAN@v1",
    )
    assert qualification_schema.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert qualification_schema.document_type == "Qualification Plan"


def test_schema_ids_by_template_are_reported():
    library = load_default_document_input_schema_library()

    assert list_document_input_schema_ids_by_template(
        library,
        "TPL-FUTURE-CSV-VALIDATION-PLAN@v1",
    ) == ["SCHEMA-CSV-VALIDATION-PLAN@v1"]

    schema = get_document_input_schema_by_template_id(
        library,
        "TPL-FUTURE-CSV-VALIDATION-PLAN@v1",
    )
    assert schema.schema_id == "SCHEMA-CSV-VALIDATION-PLAN@v1"


def test_missing_schema_ids_are_reported():
    library = load_default_document_input_schema_library()

    assert find_missing_document_input_schema_ids(
        library,
        {"SCHEMA-MISSING@v1"},
    ) == ["SCHEMA-MISSING@v1"]

    with pytest.raises(ValueError) as exc_info:
        assert_document_input_schemas_exist(
            library,
            {"SCHEMA-MISSING@v1"},
        )

    assert "SCHEMA-MISSING@v1" in str(exc_info.value)


def test_persisted_state_payload_is_not_document_input_schema_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_document_input_schema_library_from_payload(persisted_state_payload)

    assert "document input schema library payload must include schema_records" in str(
        exc_info.value
    )
