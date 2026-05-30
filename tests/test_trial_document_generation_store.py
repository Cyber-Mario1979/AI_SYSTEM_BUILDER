import pytest

from asbp.trial_document_generation_store import (
    assert_trial_document_scenarios_exist,
    get_trial_document_scenario_by_id,
    list_trial_document_scenario_ids,
    load_default_trial_document_scenario_library,
    load_trial_document_scenario_library_from_payload,
)


EXPECTED_SCENARIO_IDS = [
    "TRIAL-QP-LOCAL-CQV@v1",
    "TRIAL-CSV-LOCAL-CQV@v1",
]


def test_default_trial_document_scenario_library_loads_known_scenarios():
    library = load_default_trial_document_scenario_library()

    assert library.library_id == "M29_TRIAL_DOCUMENT_SCENARIO_LIBRARY@v1"
    assert list_trial_document_scenario_ids(library) == EXPECTED_SCENARIO_IDS

    qp_scenario = get_trial_document_scenario_by_id(
        library,
        "TRIAL-QP-LOCAL-CQV@v1",
    )
    assert qp_scenario.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert qp_scenario.output_formats == ["markdown", "csv_summary"]


def test_trial_document_scenario_missing_ids_are_reported():
    library = load_default_trial_document_scenario_library()

    assert_trial_document_scenarios_exist(library, {"TRIAL-QP-LOCAL-CQV@v1"})

    with pytest.raises(ValueError) as exc_info:
        assert_trial_document_scenarios_exist(library, {"TRIAL-MISSING@v1"})

    assert "TRIAL-MISSING@v1" in str(exc_info.value)


def test_persisted_state_payload_is_not_trial_document_scenario_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_trial_document_scenario_library_from_payload(persisted_state_payload)

    assert "trial document scenario library payload must include scenarios" in str(
        exc_info.value
    )
