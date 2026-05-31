import pytest

from asbp.document_template_store import (
    assert_document_templates_exist,
    assert_template_supports_standards_bundle,
    find_missing_document_template_ids,
    get_document_template_by_id,
    list_document_template_ids,
    list_document_template_ids_by_family,
    load_default_document_template_library,
    load_document_template_library_from_payload,
)


EXPECTED_TEMPLATE_IDS = [
    "TPL-FUTURE-QUALIFICATION-PLAN@v1",
    "TPL-FUTURE-CSV-VALIDATION-PLAN@v1",
]


def test_default_document_template_library_loads_controlled_records():
    library = load_default_document_template_library()

    assert library.library_id == "M29_DOCUMENT_TEMPLATE_LIBRARY@v1"
    assert list_document_template_ids(library) == EXPECTED_TEMPLATE_IDS

    qualification_plan = get_document_template_by_id(
        library,
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
    )
    assert qualification_plan.document_family_id == "DOCF-PLAN-STRATEGY"
    assert qualification_plan.schema_binding_status == "schema_bound"
    assert qualification_plan.schema_binding_ref == (
        "SCHEMA-QUALIFICATION-PLAN@v1"
    )

    csv_plan = get_document_template_by_id(
        library,
        "TPL-FUTURE-CSV-VALIDATION-PLAN@v1",
    )
    assert csv_plan.document_type == "CSV Validation Plan"
    assert csv_plan.schema_binding_status == "schema_bound"
    assert csv_plan.schema_binding_ref == "SCHEMA-CSV-VALIDATION-PLAN@v1"


def test_document_template_family_filter_lists_known_family_records():
    library = load_default_document_template_library()

    assert list_document_template_ids_by_family(
        library,
        "DOCF-PLAN-STRATEGY",
    ) == EXPECTED_TEMPLATE_IDS


def test_document_template_missing_ids_are_reported():
    library = load_default_document_template_library()

    assert find_missing_document_template_ids(
        library,
        {"TPL-FUTURE-QUALIFICATION-PLAN@v1"},
    ) == []

    assert find_missing_document_template_ids(
        library,
        {"TPL-MISSING@v1"},
    ) == ["TPL-MISSING@v1"]

    with pytest.raises(ValueError) as exc_info:
        assert_document_templates_exist(library, {"TPL-MISSING@v1"})

    assert "TPL-MISSING@v1" in str(exc_info.value)


def test_template_standards_bundle_support_is_assertable():
    library = load_default_document_template_library()

    assert_template_supports_standards_bundle(
        library,
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "SB-CQV-GMP@v1",
    )

    with pytest.raises(ValueError) as exc_info:
        assert_template_supports_standards_bundle(
            library,
            "TPL-FUTURE-QUALIFICATION-PLAN@v1",
            "SB-CSV-GXP@v1",
        )

    assert "does not include standards bundle ref" in str(exc_info.value)


def test_persisted_state_payload_is_not_document_template_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_document_template_library_from_payload(persisted_state_payload)

    assert "document template library payload must include template_records" in str(
        exc_info.value
    )
