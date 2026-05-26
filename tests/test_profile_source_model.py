from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.profile_source_model import ProfileLibraryModel
from asbp.profile_source_store import (
    build_profile_context_definition_id,
    get_profile_by_id,
    get_profile_context_field_by_id,
    list_profile_ids,
    list_profiles_by_preset_family,
    load_default_profile_library,
    load_profile_library_from_payload,
)


def _minimal_profile_payload() -> dict:
    return {
        "profile_id": "PROF-TEST-PROFILE@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test profile",
        "profile_type": "equipment_system",
        "related_preset_families": ["PF-PROCESS-EQUIPMENT"],
        "selector_context_tags": ["test-profile"],
        "lifecycle_events": ["LE-NEW-INSTALLATION"],
        "qualification_validation_intents": ["INT-E2E-QUALIFICATION"],
        "context_fields": [
            {
                "field_id": "test_context",
                "label": "Test context",
                "value_status": "human_input_required",
                "notes": "Test context must be confirmed.",
            }
        ],
        "assumption_controls": [
            "Human confirmation is required before deterministic execution."
        ],
    }


def _minimal_library_payload(profile: dict | None = None) -> dict:
    return {
        "library_id": "TEST_PROFILE_LIBRARY@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "profiles": [profile or _minimal_profile_payload()],
    }


def test_default_starter_profile_library_loads_runtime_source_records():
    library = load_default_profile_library()

    assert library.library_id == "M27_PROFILE_STARTER_LIBRARY@v1"
    assert list_profile_ids(library) == [
        "PROF-CLEANROOM-HVAC-BASELINE@v1",
        "PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1",
        "PROF-QCLAB-EQUIPMENT-BASELINE@v1",
        "PROF-UTILITIES-GMP-BASELINE@v1",
        "PROF-COMPUTERIZED-SYSTEM-BASELINE@v1",
        "PROF-QUALIFICATION-STRATEGY-BASELINE@v1",
        "PROF-MANUAL-FALLBACK-CONTEXT@v1",
    ]

    cleanroom_profile = get_profile_by_id(
        library,
        "PROF-CLEANROOM-HVAC-BASELINE@v1",
    )
    assert cleanroom_profile.profile_type == "cleanroom_hvac"
    assert cleanroom_profile.related_preset_families == ["PF-CLEANROOM"]

    area_classification = get_profile_context_field_by_id(
        cleanroom_profile,
        "area_classification",
    )
    assert area_classification.value_status == "human_input_required"

    process_equipment_profiles = list_profiles_by_preset_family(
        library,
        "PF-PROCESS-EQUIPMENT",
    )
    assert [
        profile.profile_id for profile in process_equipment_profiles
    ] == [
        "PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1",
        "PROF-QUALIFICATION-STRATEGY-BASELINE@v1",
    ]


def test_profile_context_definition_id_uses_profile_and_field_identity():
    assert build_profile_context_definition_id(
        "PROF-CLEANROOM-HVAC-BASELINE@v1",
        "area_classification",
    ) == "PROF-CLEANROOM-HVAC-BASELINE@v1::area_classification"


def test_profile_library_rejects_duplicate_profile_ids():
    profile = _minimal_profile_payload()
    payload = _minimal_library_payload(profile)
    payload["profiles"].append(deepcopy(profile))

    with pytest.raises(ValidationError) as exc_info:
        ProfileLibraryModel(**payload)

    assert "Duplicate profile_id is not allowed: PROF-TEST-PROFILE@v1" in str(
        exc_info.value
    )


def test_profile_rejects_duplicate_context_field_ids():
    profile = _minimal_profile_payload()
    profile["context_fields"].append(deepcopy(profile["context_fields"][0]))

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert "Duplicate profile context field_id is not allowed: test_context" in str(
        exc_info.value
    )


def test_profile_rejects_invalid_related_preset_family():
    profile = _minimal_profile_payload()
    profile["related_preset_families"] = ["PF-UNKNOWN"]

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert "related_preset_families" in str(exc_info.value)


def test_profile_rejects_missing_context_fields():
    profile = _minimal_profile_payload()
    profile["context_fields"] = []

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert "context_fields" in str(exc_info.value)


def test_profile_rejects_blank_assumption_control():
    profile = _minimal_profile_payload()
    profile["assumption_controls"] = [" "]

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert "Blank profile context value is not allowed" in str(exc_info.value)


def test_profile_context_field_rejects_starter_default_without_value():
    profile = _minimal_profile_payload()
    profile["context_fields"][0]["value_status"] = "starter_default"

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert (
        "starter_default profile context field requires value: test_context"
    ) in str(exc_info.value)


def test_profile_context_field_rejects_not_applicable_with_value():
    profile = _minimal_profile_payload()
    profile["context_fields"][0]["value_status"] = "not_applicable"
    profile["context_fields"][0]["value"] = "Unexpected value"

    with pytest.raises(ValidationError) as exc_info:
        load_profile_library_from_payload(_minimal_library_payload(profile))

    assert (
        "not_applicable profile context field cannot include value: test_context"
    ) in str(exc_info.value)


def test_persisted_state_payload_is_not_profile_source_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_profile_library_from_payload(persisted_state_payload)

    assert "profile library payload must include profiles" in str(exc_info.value)
