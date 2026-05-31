import pytest

from asbp.output_validation_store import (
    assert_output_validation_rules_exist,
    get_output_validation_rule_by_id,
    get_output_validation_rule_for_format,
    list_output_validation_rule_ids,
    load_default_output_validation_rule_library,
    load_output_validation_rule_library_from_payload,
)


EXPECTED_RULE_IDS = [
    "OUTVALRULE-MARKDOWN-ARTIFACT@v1",
    "OUTVALRULE-CSV-SUMMARY-ARTIFACT@v1",
]


def test_default_output_validation_rule_library_loads_controlled_rules():
    library = load_default_output_validation_rule_library()

    assert library.library_id == "M29_OUTPUT_VALIDATION_RULE_LIBRARY@v1"
    assert list_output_validation_rule_ids(library) == EXPECTED_RULE_IDS

    markdown_rule = get_output_validation_rule_by_id(
        library,
        "OUTVALRULE-MARKDOWN-ARTIFACT@v1",
    )
    assert markdown_rule.supported_formats == ["markdown"]

    csv_rule = get_output_validation_rule_for_format(library, "csv_summary")
    assert csv_rule.rule_id == "OUTVALRULE-CSV-SUMMARY-ARTIFACT@v1"


def test_output_validation_missing_rule_ids_are_reported():
    library = load_default_output_validation_rule_library()

    assert_output_validation_rules_exist(
        library,
        {"OUTVALRULE-MARKDOWN-ARTIFACT@v1"},
    )

    with pytest.raises(ValueError) as exc_info:
        assert_output_validation_rules_exist(
            library,
            {"OUTVALRULE-MISSING@v1"},
        )

    assert "OUTVALRULE-MISSING@v1" in str(exc_info.value)


def test_unknown_output_format_rule_is_rejected():
    library = load_default_output_validation_rule_library()

    with pytest.raises(ValueError) as exc_info:
        get_output_validation_rule_for_format(library, "excel")  # type: ignore[arg-type]

    assert "not found for format" in str(exc_info.value)


def test_persisted_state_payload_is_not_output_validation_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_output_validation_rule_library_from_payload(persisted_state_payload)

    assert "output validation rule library payload must include validation_rules" in str(
        exc_info.value
    )
