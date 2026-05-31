import pytest

from asbp.standards_registry_model import StandardsRegistrySourceRecordModel
from asbp.standards_registry_store import (
    assert_citation_depth_allowed,
    assert_registry_contains_standard_ids,
    assert_source_can_support_mandatory_use,
    get_standard_source_by_id,
    list_limited_standard_source_ids,
    list_mandatory_eligible_standard_source_ids,
    list_standard_source_ids,
    list_standard_source_ids_by_authority_status,
    load_default_standards_registry,
    load_standards_registry_from_payload,
    source_can_support_mandatory_use,
    source_requires_visible_limitations,
)


EXPECTED_SOURCE_IDS = [
    "STD-EU-GMP-ANNEX-15",
    "STD-EU-GMP-ANNEX-11",
    "STD-EU-GMP-CHAPTER-4",
    "STD-ASTM-E2500",
    "STD-ISPE-GAMP5",
    "STD-FDA-21CFR11",
    "STD-ICH-Q9",
    "STD-ICH-Q10",
    "STD-ISO-14644",
    "STD-LOCAL-CLEANROOM-NONSTERILE",
]


def test_default_runtime_standards_registry_loads_source_records():
    registry = load_default_standards_registry()

    assert registry.registry_id == "STANDARDS_SOURCE_REGISTRY@v0.1"
    assert registry.registry_version == "v0.1"
    assert list_standard_source_ids(registry) == EXPECTED_SOURCE_IDS


def test_default_runtime_registry_marks_all_current_sources_limited():
    registry = load_default_standards_registry()

    assert list_limited_standard_source_ids(registry) == EXPECTED_SOURCE_IDS
    assert list_mandatory_eligible_standard_source_ids(registry) == []


def test_pending_authoritative_source_cannot_support_mandatory_use_yet():
    registry = load_default_standards_registry()

    assert source_can_support_mandatory_use(
        registry,
        "STD-EU-GMP-ANNEX-15",
    ) is False

    with pytest.raises(ValueError) as exc_info:
        assert_source_can_support_mandatory_use(
            registry,
            "STD-EU-GMP-ANNEX-15",
        )

    assert "cannot support mandatory use" in str(exc_info.value)


def test_reference_source_cannot_support_mandatory_use():
    registry = load_default_standards_registry()

    assert source_can_support_mandatory_use(registry, "STD-ASTM-E2500") is False
    assert source_requires_visible_limitations(registry, "STD-ASTM-E2500") is True


def test_local_user_provided_source_remains_limited_and_not_public_regulation():
    registry = load_default_standards_registry()
    source = get_standard_source_by_id(
        registry,
        "STD-LOCAL-CLEANROOM-NONSTERILE",
    )

    assert source.authority_status == "tbd"
    assert source.verification_status == "user_provided"
    assert source.mandatory_flag == "not_mandatory_until_internal_approval"
    assert source.requires_visible_limitations() is True
    assert any(
        "Must not be treated as public regulation" in limitation
        for limitation in source.source_limitations
    )


def test_document_citation_is_allowed_for_pending_registry_records():
    registry = load_default_standards_registry()

    assert_citation_depth_allowed(
        registry,
        "STD-EU-GMP-ANNEX-15",
        "document",
    )


def test_clause_citation_is_blocked_for_pending_registry_records():
    registry = load_default_standards_registry()

    with pytest.raises(ValueError) as exc_info:
        assert_citation_depth_allowed(
            registry,
            "STD-EU-GMP-ANNEX-15",
            "clause",
        )

    assert "Citation depth is not available" in str(exc_info.value)


def test_table_row_citation_is_allowed_for_local_matrix_traceability_only():
    registry = load_default_standards_registry()

    assert_citation_depth_allowed(
        registry,
        "STD-LOCAL-CLEANROOM-NONSTERILE",
        "table_row",
    )


def test_authority_status_filtering_is_deterministic():
    registry = load_default_standards_registry()

    assert list_standard_source_ids_by_authority_status(
        registry,
        "reference",
    ) == [
        "STD-ASTM-E2500",
        "STD-ISPE-GAMP5",
        "STD-ICH-Q9",
        "STD-ICH-Q10",
        "STD-ISO-14644",
    ]


def test_registry_source_lookup_reports_missing_id():
    registry = load_default_standards_registry()

    with pytest.raises(ValueError) as exc_info:
        get_standard_source_by_id(registry, "STD-MISSING")

    assert "Standards registry source not found" in str(exc_info.value)


def test_payload_without_source_records_is_not_registry_truth():
    with pytest.raises(ValueError) as exc_info:
        load_standards_registry_from_payload({"registry_id": "BROKEN"})

    assert "standards registry payload must include source_records" in str(
        exc_info.value
    )


def test_registry_contains_required_standard_ids_gate():
    registry = load_default_standards_registry()

    assert_registry_contains_standard_ids(
        registry,
        {"STD-EU-GMP-ANNEX-15", "STD-FDA-21CFR11"},
    )

    with pytest.raises(ValueError) as exc_info:
        assert_registry_contains_standard_ids(
            registry,
            {"STD-MISSING"},
        )

    assert "Standards registry is missing required source IDs" in str(exc_info.value)


def test_verified_runtime_source_can_pass_mandatory_gate_when_evidence_exists():
    verified_source = StandardsRegistrySourceRecordModel(
        std_id="STD-TEST-VERIFIED",
        source_name="Verified test standard",
        source_type="regulation",
        authority_status="authoritative",
        verification_status="verified",
        version_or_effective_date="2026",
        jurisdiction_or_owner="TEST",
        applicability_scope=["test_scope"],
        applicability_conditions=["Applies to test scope."],
        citation_depths=["document", "version", "section", "clause"],
        source_location="controlled://test-source",
        mandatory_flag="mandatory_when_applicable",
        source_limitations=[],
    )

    assert verified_source.can_support_mandatory_use() is True
