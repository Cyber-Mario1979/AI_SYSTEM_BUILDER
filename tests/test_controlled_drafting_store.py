import pytest

from asbp.controlled_drafting_store import (
    assert_controlled_drafting_modes_exist,
    assert_drafting_mode_supports_template_and_schema,
    get_controlled_drafting_mode_by_id,
    get_controlled_drafting_mode_by_mode,
    list_controlled_drafting_mode_ids,
    load_controlled_drafting_library_from_payload,
    load_default_controlled_drafting_library,
)


EXPECTED_DRAFTING_MODE_IDS = [
    "DRAFTMODE-STRONG-INPUT-FILL@v1",
    "DRAFTMODE-PARTIAL-BOUNDED-COMPLETION@v1",
    "DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
    "DRAFTMODE-RATIONALE-BOUND-SECTION-DRAFTING@v1",
]


def test_default_controlled_drafting_library_loads_modes():
    library = load_default_controlled_drafting_library()

    assert library.library_id == "M29_CONTROLLED_DRAFTING_LIBRARY@v1"
    assert list_controlled_drafting_mode_ids(library) == EXPECTED_DRAFTING_MODE_IDS

    mode = get_controlled_drafting_mode_by_id(
        library,
        "DRAFTMODE-STRONG-INPUT-FILL@v1",
    )
    assert mode.drafting_mode == "strong_input_fill"


def test_get_controlled_drafting_mode_by_mode():
    library = load_default_controlled_drafting_library()

    mode = get_controlled_drafting_mode_by_mode(
        library,
        "minimal_scaffold_with_placeholders",
    )

    assert mode.drafting_mode_id == "DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1"


def test_assert_controlled_drafting_modes_exist():
    library = load_default_controlled_drafting_library()

    assert_controlled_drafting_modes_exist(
        library,
        {"DRAFTMODE-STRONG-INPUT-FILL@v1"},
    )

    with pytest.raises(ValueError) as exc_info:
        assert_controlled_drafting_modes_exist(
            library,
            {"DRAFTMODE-MISSING@v1"},
        )

    assert "DRAFTMODE-MISSING@v1" in str(exc_info.value)


def test_drafting_mode_template_schema_support_is_assertable():
    library = load_default_controlled_drafting_library()
    mode = get_controlled_drafting_mode_by_id(
        library,
        "DRAFTMODE-STRONG-INPUT-FILL@v1",
    )

    assert_drafting_mode_supports_template_and_schema(
        mode,
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "SCHEMA-QUALIFICATION-PLAN@v1",
    )

    with pytest.raises(ValueError) as exc_info:
        assert_drafting_mode_supports_template_and_schema(
            mode,
            "TPL-MISSING@v1",
            "SCHEMA-QUALIFICATION-PLAN@v1",
        )

    assert "does not support template" in str(exc_info.value)


def test_persisted_state_payload_is_not_controlled_drafting_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_controlled_drafting_library_from_payload(persisted_state_payload)

    assert "controlled drafting library payload must include drafting_modes" in str(
        exc_info.value
    )
