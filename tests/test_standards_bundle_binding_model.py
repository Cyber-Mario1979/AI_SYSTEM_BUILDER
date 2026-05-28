from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.standards_bundle_binding_model import (
    StandardsBundleBindingLibraryModel,
    StandardsBundleSourceBindingModel,
)
from asbp.standards_bundle_binding_store import (
    assert_downstream_consumers_exist,
    find_missing_downstream_consumer_ids,
    get_standards_bundle_binding_by_id,
    list_standard_ids_for_bundle,
    list_standards_bundle_ids,
    load_default_standards_bundle_binding_library,
    load_standards_bundle_binding_library_from_payload,
)


EXPECTED_STANDARDS_BUNDLE_IDS = [
    "SB-CQV-GMP@v1",
    "SB-CSV-GXP@v1",
]


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_execute_runtime_registry_consumption",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_load_or_select_templates",
        "does_not_generate_product_ready_standards_output",
    ]


def _minimal_source_binding_payload() -> dict:
    return {
        "std_id": "STD-EU-GMP-ANNEX-15",
        "registry_version": "v0.1",
        "source_role": "primary_authority_candidate",
        "authority_status": "authoritative",
        "verification_status": "pending_verification",
        "mandatory_flag": "mandatory_when_applicable",
        "allowed_citation_depths": ["document"],
        "applicability_boundaries": ["qualification"],
        "source_limitations": [
            "Version/effective date remains TBD in registry v0.1."
        ],
        "supports_mandatory_use": False,
    }


def _minimal_consumer_payload() -> dict:
    return {
        "consumer_id": "MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1",
        "consumer_type": "mapping_record",
        "consumer_status": "resolved_mapping_record",
        "limitation_statement": (
            "Mapping resolves bundle source only; template remains future-scoped."
        ),
    }


def _minimal_binding_payload() -> dict:
    return {
        "bundle_id": "SB-TEST-CQV@v1",
        "version": "v1",
        "status": "runtime_facing_source_contract",
        "display_name": "Test standards bundle binding",
        "registry_version": "v0.1",
        "binding_scope": ["qualification"],
        "source_bindings": [_minimal_source_binding_payload()],
        "downstream_consumers": [_minimal_consumer_payload()],
        "binding_controls": ["Binding records source relationships only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_library_payload(binding: dict | None = None) -> dict:
    return {
        "library_id": "TEST_STANDARDS_BUNDLE_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_source_contract",
        "bindings": [binding or _minimal_binding_payload()],
    }


def test_default_standards_bundle_binding_library_loads_controlled_bindings():
    library = load_default_standards_bundle_binding_library()

    assert library.library_id == "M28_STANDARDS_BUNDLE_BINDING_LIBRARY@v1"
    assert list_standards_bundle_ids(library) == EXPECTED_STANDARDS_BUNDLE_IDS

    cqv_bundle = get_standards_bundle_binding_by_id(library, "SB-CQV-GMP@v1")
    assert cqv_bundle.registry_version == "v0.1"
    assert "STD-EU-GMP-ANNEX-15" in list_standard_ids_for_bundle(
        library,
        "SB-CQV-GMP@v1",
    )
    assert "STD-LOCAL-CLEANROOM-NONSTERILE" in list_standard_ids_for_bundle(
        library,
        "SB-CQV-GMP@v1",
    )

    csv_bundle = get_standards_bundle_binding_by_id(library, "SB-CSV-GXP@v1")
    assert "STD-FDA-21CFR11" in [
        source.std_id for source in csv_bundle.source_bindings
    ]


def test_downstream_mapping_consumers_are_explicitly_identified():
    library = load_default_standards_bundle_binding_library()
    expected_mapping_consumers = {
        "MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1",
        "MAP-STD-CSV-GXP-TO-CSV-TEMPLATE@v1",
    }

    assert find_missing_downstream_consumer_ids(
        library,
        "mapping_record",
        expected_mapping_consumers,
    ) == []

    assert_downstream_consumers_exist(
        library,
        "mapping_record",
        expected_mapping_consumers,
    )


def test_limited_bundle_source_requires_visible_limitations():
    source = _minimal_source_binding_payload()
    source["source_limitations"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsBundleSourceBindingModel(**source)

    assert "Limited standards bundle source requires source_limitations" in str(
        exc_info.value
    )


def test_pending_source_cannot_claim_section_or_clause_depth():
    source = _minimal_source_binding_payload()
    source["allowed_citation_depths"] = ["document", "clause"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsBundleSourceBindingModel(**source)

    assert "Section or clause citation depth requires verified source evidence" in str(
        exc_info.value
    )


def test_pending_source_cannot_support_mandatory_use():
    source = _minimal_source_binding_payload()
    source["supports_mandatory_use"] = True

    with pytest.raises(ValidationError) as exc_info:
        StandardsBundleSourceBindingModel(**source)

    assert "Mandatory standards bundle use requires verified source evidence" in str(
        exc_info.value
    )


def test_binding_library_rejects_duplicate_bundle_ids():
    binding = _minimal_binding_payload()
    payload = _minimal_library_payload(binding)
    payload["bindings"].append(deepcopy(binding))

    with pytest.raises(ValidationError) as exc_info:
        StandardsBundleBindingLibraryModel(**payload)

    assert "Duplicate standards bundle id is not allowed" in str(exc_info.value)


def test_binding_rejects_duplicate_source_ids():
    binding = _minimal_binding_payload()
    binding["source_bindings"].append(deepcopy(binding["source_bindings"][0]))

    with pytest.raises(ValidationError) as exc_info:
        load_standards_bundle_binding_library_from_payload(
            _minimal_library_payload(binding)
        )

    assert "Duplicate standards bundle source id is not allowed" in str(
        exc_info.value
    )


def test_future_consumer_requires_resolution_checkpoint():
    binding = _minimal_binding_payload()
    binding["downstream_consumers"].append(
        {
            "consumer_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
            "consumer_type": "template_future_contract",
            "consumer_status": "future_expected",
            "limitation_statement": "Template remains future-scoped.",
        }
    )

    with pytest.raises(ValidationError) as exc_info:
        load_standards_bundle_binding_library_from_payload(
            _minimal_library_payload(binding)
        )

    assert "requires resolution_checkpoint" in str(exc_info.value)


def test_binding_requires_explicit_non_implementation_claims():
    binding = _minimal_binding_payload()
    binding["explicit_non_implementation_claims"] = [
        "does_not_execute_runtime_registry_consumption"
    ]

    with pytest.raises(ValidationError) as exc_info:
        load_standards_bundle_binding_library_from_payload(
            _minimal_library_payload(binding)
        )

    assert "M28.4 standards bundle binding is missing explicit" in str(
        exc_info.value
    )


def test_persisted_state_payload_is_not_standards_bundle_binding_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_standards_bundle_binding_library_from_payload(persisted_state_payload)

    assert "standards bundle binding library payload must include bindings" in str(
        exc_info.value
    )
