import pytest

from asbp.standards_backed_output_store import (
    assert_standards_backed_output_packets_exist,
    get_standards_backed_output_packet_by_id,
    list_standards_backed_output_packet_ids,
    list_standards_backed_output_packet_ids_by_template,
    load_default_standards_backed_output_library,
    load_standards_backed_output_library_from_payload,
)

EXPECTED_PACKET_IDS = [
    "STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
    "STDOUT-CSV-VALIDATION-PLAN-CONTROLS@v1",
]


def test_default_standards_backed_output_library_loads_controlled_packets():
    library = load_default_standards_backed_output_library()

    assert library.library_id == "M29_STANDARDS_BACKED_OUTPUT_LIBRARY@v1"
    assert list_standards_backed_output_packet_ids(library) == EXPECTED_PACKET_IDS

    packet = get_standards_backed_output_packet_by_id(
        library,
        "STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
    )
    assert packet.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert packet.standards_bundle_refs == ["SB-CQV-GMP@v1"]


def test_standards_backed_output_library_filters_by_template():
    library = load_default_standards_backed_output_library()

    assert list_standards_backed_output_packet_ids_by_template(
        library,
        "TPL-FUTURE-CSV-VALIDATION-PLAN@v1",
    ) == ["STDOUT-CSV-VALIDATION-PLAN-CONTROLS@v1"]


def test_standards_backed_output_missing_packet_ids_are_reported():
    library = load_default_standards_backed_output_library()

    assert_standards_backed_output_packets_exist(
        library,
        {"STDOUT-QUALIFICATION-PLAN-CONTROLS@v1"},
    )

    with pytest.raises(ValueError) as exc_info:
        assert_standards_backed_output_packets_exist(
            library,
            {"STDOUT-MISSING@v1"},
        )

    assert "STDOUT-MISSING@v1" in str(exc_info.value)


def test_persisted_state_payload_is_not_standards_backed_output_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_standards_backed_output_library_from_payload(persisted_state_payload)

    assert "standards-backed output library payload must include control_packets" in str(
        exc_info.value
    )
