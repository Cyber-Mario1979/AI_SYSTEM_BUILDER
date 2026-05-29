from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.document_template_store import (
    list_document_template_ids,
    load_default_document_template_library,
)
from asbp.mapping_source_model import MappingLibraryModel
from asbp.mapping_source_store import (
    assert_resolved_references_exist,
    build_mapping_reference_definition_id,
    find_missing_resolved_reference_ids,
    get_mapping_by_id,
    list_mapping_ids,
    list_mappings_by_kind,
    load_default_mapping_library,
    load_mapping_library_from_payload,
)
from asbp.profile_source_store import list_profile_ids, load_default_profile_library
from asbp.standards_bundle_binding_store import (
    list_standards_bundle_ids,
    load_default_standards_bundle_binding_library,
)
from asbp.task_pool_source_store import list_task_pool_ids, load_default_task_pool_library


EXPECTED_MAPPING_IDS = [
    "MAP-PRESET-CLEANROOM-TO-PROFILE@v1",
    "MAP-PRESET-PE-TO-PROFILE@v1",
    "MAP-PRESET-QCLAB-TO-PROFILE@v1",
    "MAP-PRESET-UTILITIES-TO-PROFILE@v1",
    "MAP-PRESET-CSV-TO-PROFILE@v1",
    "MAP-PRESET-MANUAL-FALLBACK-TO-PROFILE@v1",
    "MAP-SELECTOR-PE-E2E-TO-TASK-POOL@v1",
    "MAP-SELECTOR-QCLAB-TO-TASK-POOL@v1",
    "MAP-SELECTOR-CLEANROOM-HVAC-TO-TASK-POOL@v1",
    "MAP-SELECTOR-UTILITIES-TO-TASK-POOL@v1",
    "MAP-SELECTOR-CSV-TO-TASK-POOL@v1",
    "MAP-SELECTOR-MANUAL-FALLBACK-TO-TASK-POOL@v1",
    "MAP-TASK-PE-SCOPE-TO-DOC@v1",
    "MAP-TASK-QCLAB-CSV-LINK-TO-DOC@v1",
    "MAP-TASK-CRHVAC-OQ-TO-DOC@v1",
    "MAP-TASK-UT-PQ-TO-DOC@v1",
    "MAP-TASK-CSV-TESTING-TO-DOC@v1",
    "MAP-TASK-MF-ROUTE-TO-DOC@v1",
    "MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1",
    "MAP-STD-CSV-GXP-TO-CSV-TEMPLATE@v1"
]


def _minimal_mapping_payload() -> dict:
    return {
        "mapping_id": "MAP-TEST-PRESET-TO-PROFILE@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test preset to profile mapping",
        "mapping_kind": "preset_to_profile",
        "source_refs": [
            {
                "reference_id": "PF-PROCESS-EQUIPMENT",
                "reference_type": "preset_family",
                "reference_status": "resolved_source",
            }
        ],
        "target_refs": [
            {
                "reference_id": "PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1",
                "reference_type": "profile",
                "reference_status": "resolved_source",
            }
        ],
        "applicability_tags": ["test"],
        "mapping_controls": ["Mapping records source relationships only."],
    }


def _minimal_library_payload(mapping: dict | None = None) -> dict:
    return {
        "library_id": "TEST_MAPPING_LIBRARY@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "mappings": [mapping or _minimal_mapping_payload()],
    }


def _minimal_standard_to_template_mapping_payload() -> dict:
    return {
        "mapping_id": "MAP-TEST-STANDARD-TO-TEMPLATE@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test standards bundle to template mapping",
        "mapping_kind": "standard_to_template",
        "source_refs": [
            {
                "reference_id": "SB-CQV-GMP@v1",
                "reference_type": "standard_bundle",
                "reference_status": "resolved_source",
            }
        ],
        "target_refs": [
            {
                "reference_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
                "reference_type": "template",
                "reference_status": "resolved_source",
            }
        ],
        "applicability_tags": ["standards", "template"],
        "mapping_controls": [
            "Mapping resolves standards-bundle source and M29.2 template record only.",
            "Template loading, selection, generation, and rendering remain later M29 work.",
        ],
    }


def test_default_starter_mapping_library_loads_runtime_source_records():
    library = load_default_mapping_library()

    assert library.library_id == "M27_MAPPING_STARTER_LIBRARY@v1"
    assert list_mapping_ids(library) == EXPECTED_MAPPING_IDS

    assert len(list_mappings_by_kind(library, "preset_to_profile")) == 6
    assert len(list_mappings_by_kind(library, "selector_to_task_pool")) == 6
    assert len(list_mappings_by_kind(library, "task_to_document")) == 6
    assert len(list_mappings_by_kind(library, "standard_to_template")) == 2

    mapping = get_mapping_by_id(
        library,
        "MAP-PRESET-PE-TO-PROFILE@v1",
    )
    assert mapping.mapping_kind == "preset_to_profile"


def test_default_mapping_profile_targets_exist_in_profile_source_library():
    mapping_library = load_default_mapping_library()
    profile_library = load_default_profile_library()

    assert find_missing_resolved_reference_ids(
        mapping_library,
        "profile",
        set(list_profile_ids(profile_library)),
    ) == []

    assert_resolved_references_exist(
        mapping_library,
        "profile",
        set(list_profile_ids(profile_library)),
    )


def test_default_mapping_task_pool_targets_exist_in_task_pool_source_library():
    mapping_library = load_default_mapping_library()
    task_pool_library = load_default_task_pool_library()

    assert find_missing_resolved_reference_ids(
        mapping_library,
        "task_pool",
        set(list_task_pool_ids(task_pool_library)),
    ) == []

    assert_resolved_references_exist(
        mapping_library,
        "task_pool",
        set(list_task_pool_ids(task_pool_library)),
    )


def test_standard_template_mappings_resolve_bundle_and_template_sources():
    library = load_default_mapping_library()
    mapping = get_mapping_by_id(
        library,
        "MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1",
    )

    assert mapping.mapping_kind == "standard_to_template"
    assert mapping.source_refs[0].reference_id == "SB-CQV-GMP@v1"
    assert mapping.source_refs[0].reference_status == "resolved_source"
    assert mapping.source_refs[0].resolution_checkpoint is None
    assert mapping.target_refs[0].reference_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert mapping.target_refs[0].reference_status == "resolved_source"
    assert mapping.target_refs[0].resolution_checkpoint is None


def test_resolved_standard_bundle_mapping_sources_exist_in_binding_library():
    mapping_library = load_default_mapping_library()
    bundle_library = load_default_standards_bundle_binding_library()

    assert find_missing_resolved_reference_ids(
        mapping_library,
        "standard_bundle",
        set(list_standards_bundle_ids(bundle_library)),
    ) == []

    assert_resolved_references_exist(
        mapping_library,
        "standard_bundle",
        set(list_standards_bundle_ids(bundle_library)),
    )


def test_resolved_template_mapping_targets_exist_in_template_library():
    mapping_library = load_default_mapping_library()
    template_library = load_default_document_template_library()

    assert find_missing_resolved_reference_ids(
        mapping_library,
        "template",
        set(list_document_template_ids(template_library)),
    ) == []

    assert_resolved_references_exist(
        mapping_library,
        "template",
        set(list_document_template_ids(template_library)),
    )


def test_mapping_reference_definition_id_uses_mapping_and_reference_identity():
    assert build_mapping_reference_definition_id(
        "MAP-PRESET-PE-TO-PROFILE@v1",
        "profile",
        "PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1",
    ) == (
        "MAP-PRESET-PE-TO-PROFILE@v1::"
        "profile::PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1"
    )


def test_mapping_library_rejects_duplicate_mapping_ids():
    mapping = _minimal_mapping_payload()
    payload = _minimal_library_payload(mapping)
    payload["mappings"].append(deepcopy(mapping))

    with pytest.raises(ValidationError) as exc_info:
        MappingLibraryModel(**payload)

    assert "Duplicate mapping_id is not allowed" in str(exc_info.value)


def test_preset_to_profile_rejects_invalid_target_reference_type():
    mapping = _minimal_mapping_payload()
    mapping["target_refs"][0]["reference_type"] = "task_pool"

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "preset_to_profile mapping has invalid target reference_type" in str(
        exc_info.value
    )


def test_selector_to_task_pool_requires_resolved_references():
    mapping = _minimal_mapping_payload()
    mapping["mapping_id"] = "MAP-TEST-SELECTOR-TO-TASK-POOL@v1"
    mapping["mapping_kind"] = "selector_to_task_pool"
    mapping["source_refs"] = [
        {
            "reference_id": "SEL-TEST",
            "reference_type": "selector_context",
            "reference_status": "resolved_source",
        }
    ]
    mapping["target_refs"] = [
        {
            "reference_id": "TP-TEST-POOL@v1",
            "reference_type": "task_pool",
            "reference_status": "future_expected",
            "resolution_checkpoint": "M27.8",
        }
    ]

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "selector_to_task_pool mapping requires resolved_source" in str(
        exc_info.value
    )


def test_task_to_document_rejects_resolved_document_target_in_m27_7():
    mapping = _minimal_mapping_payload()
    mapping["mapping_id"] = "MAP-TEST-TASK-TO-DOC@v1"
    mapping["mapping_kind"] = "task_to_document"
    mapping["source_refs"] = [
        {
            "reference_id": "TP-TEST-POOL@v1::TEST-SCOPE",
            "reference_type": "atomic_task",
            "reference_status": "resolved_source",
        }
    ]
    mapping["target_refs"] = [
        {
            "reference_id": "TEST_DOCUMENT",
            "reference_type": "document_expectation",
            "reference_status": "resolved_source",
        }
    ]

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "task_to_document document targets must remain future" in str(
        exc_info.value
    )


def test_standard_to_template_requires_resolved_standard_bundle_source():
    mapping = _minimal_standard_to_template_mapping_payload()
    mapping["source_refs"][0]["reference_status"] = "future_expected"
    mapping["source_refs"][0]["resolution_checkpoint"] = "M28"

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "standard_to_template source standard_bundle must be resolved_source" in str(
        exc_info.value
    )


def test_standard_to_template_requires_resolved_template_target_after_m29_2():
    mapping = _minimal_standard_to_template_mapping_payload()
    mapping["target_refs"][0] = {
        "reference_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "reference_type": "template",
        "reference_status": "future_expected",
        "resolution_checkpoint": "M29",
    }

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "template targets must be resolved_source after M29.2" in str(
        exc_info.value
    )


def test_future_or_placeholder_reference_requires_resolution_checkpoint():
    mapping = _minimal_mapping_payload()
    mapping["source_refs"][0]["reference_status"] = "future_expected"

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "requires resolution_checkpoint" in str(exc_info.value)


def test_resolved_reference_rejects_resolution_checkpoint():
    mapping = _minimal_mapping_payload()
    mapping["source_refs"][0]["resolution_checkpoint"] = "M27.7"

    with pytest.raises(ValidationError) as exc_info:
        load_mapping_library_from_payload(_minimal_library_payload(mapping))

    assert "Resolved mapping reference cannot include" in str(exc_info.value)


def test_missing_resolved_reference_ids_are_reported():
    library = load_mapping_library_from_payload(_minimal_library_payload())

    assert find_missing_resolved_reference_ids(
        library,
        "profile",
        set(),
    ) == ["PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1"]

    with pytest.raises(ValueError) as exc_info:
        assert_resolved_references_exist(
            library,
            "profile",
            set(),
        )

    assert "PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1" in str(exc_info.value)


def test_persisted_state_payload_is_not_mapping_source_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_mapping_library_from_payload(persisted_state_payload)

    assert "mapping library payload must include mappings" in str(exc_info.value)
