import pytest
from pydantic import ValidationError

from asbp.trial_scenario_coverage_model import (
    TrialScenarioCoverageLibraryModel,
    TrialScenarioCoverageRecordModel,
)
from asbp.trial_scenario_coverage_store import (
    assert_trial_scenario_domains_exist,
    collect_trial_scenario_asset_archetypes,
    collect_trial_scenario_document_refs,
    collect_trial_scenario_domains,
    collect_trial_scenario_utility_systems,
    load_default_trial_scenario_coverage_library,
)


REQUIRED_DOMAINS = {
    "cleanroom_hvac",
    "process_equipment",
    "utilities",
    "csv",
    "qc_lab_equipment",
    "decommissioning",
    "manual_fallback",
}

DETAILED_P0_UTILITIES = {
    "Compressed Air System",
    "Purified / Refined Water System",
    "HVAC System",
    "Chilled Water System",
}

MUST_HAVE_DOCUMENT_REFS = {
    "CCF",
    "VMP",
    "SIA",
    "URS",
    "VENDOR_DOC_EXTRACTION_SOURCE",
    "RA_FMEA",
    "URS_DEVIATION_LIST",
    "RTM",
    "DQ",
    "CP",
    "QP",
    "FAT_PROTOCOL_REPORT",
    "A0_CERTIFICATE",
    "CTOP",
    "A1_CERTIFICATE",
    "SAT_PROTOCOL_REPORT",
    "CR",
    "A2_CERTIFICATE",
    "IQ_PROTOCOL_REPORT",
    "OQ_PROTOCOL_REPORT",
    "PQ_PROTOCOL_REPORT",
    "DEVIATION_INCIDENT_REPORT",
    "CAPA_CLOSURE_FORM",
    "VSR",
    "DECOMMISSIONING_DOCUMENT_SET",
}


def test_mvp_trial_scenario_coverage_library_loads():
    library = load_default_trial_scenario_coverage_library()

    assert library.library_id == "M29_MVP_TRIAL_SCENARIO_COVERAGE_LIBRARY@v1"
    assert len(library.scenarios) >= 12
    assert collect_trial_scenario_domains(library) >= REQUIRED_DOMAINS


def test_mvp_trial_scenario_coverage_covers_detailed_utilities_and_process_equipment():
    library = load_default_trial_scenario_coverage_library()

    assert collect_trial_scenario_utility_systems(library) >= DETAILED_P0_UTILITIES
    assert "Tablet Compression Machine" in collect_trial_scenario_asset_archetypes(library)


def test_mvp_trial_scenario_coverage_covers_must_have_document_refs():
    library = load_default_trial_scenario_coverage_library()

    assert MUST_HAVE_DOCUMENT_REFS <= collect_trial_scenario_document_refs(library)


def test_urs_dcf_boundary_is_urs_only_for_trial_coverage():
    library = load_default_trial_scenario_coverage_library()

    for scenario in library.scenarios:
        if scenario.urs_dcf_required:
            assert scenario.urs_dcf_route_ref is not None
            assert "URS" in scenario.urs_dcf_route_ref
            assert "URS" in scenario.document_refs
        else:
            assert scenario.urs_dcf_route_ref is None


def test_vendor_document_extraction_requires_vendor_source_refs():
    payload = {
        "scenario_id": "TRIALCOV-TEST-VENDOR-MISSING@v1",
        "version": "v1",
        "status": "mvp_trial_scenario_coverage_record",
        "display_name": "Invalid vendor extraction coverage",
        "domain": "process_equipment",
        "priority": "P0",
        "scenario_type": "local_review_flow",
        "lifecycle_event": "LE-NEW-INSTALLATION",
        "asset_archetype": "Tablet Compression Machine",
        "urs_dcf_required": True,
        "urs_dcf_route_ref": "DCF-PROCESS-EQUIPMENT-URS@v1",
        "task_pool_refs": ["TP-MVP-PE-TABCOMP-QUAL@v1"],
        "profile_refs": ["PROF-MVP-PE-TABCOMP@v1"],
        "planning_basis_refs": ["M29_WAVE3_MVP_PLANNING_BASIS_LIBRARY@v1"],
        "mapping_refs": ["MAP-MVP-PRESET-PF-PROCESS-EQUIPMENT-TO-PROF-MVP-PE-TABCOMP@v1"],
        "document_refs": ["URS", "VENDOR_DOC_EXTRACTION_SOURCE"],
        "downstream_dependency_refs": ["M29_DOCUMENT_DEPENDENCY_CONTRACT_LIBRARY@v1"],
        "standards_policy_refs": ["CITPOL-URS@v1"],
        "output_validation_expectations": ["Output validation remains required."],
        "coverage_controls": ["Local review coverage only."],
        "explicit_non_implementation_claims": [
            "does_not_create_uat_acceptance",
            "does_not_release_or_deploy_documents",
            "does_not_create_customer_ready_output",
            "does_not_create_qms_approval_records",
            "does_not_generate_documents",
            "does_not_productize_or_deploy_outputs",
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        TrialScenarioCoverageRecordModel(**payload)

    assert "vendor_source_refs" in str(exc_info.value)


def test_mvp_trial_scenarios_do_not_claim_uat_release_or_productization():
    library = load_default_trial_scenario_coverage_library()

    for scenario in library.scenarios:
        assert scenario.local_review_only is True
        assert scenario.uat_acceptance_claimed is False
        assert scenario.customer_ready_release_claimed is False
        assert scenario.productization_claimed is False
        assert "does_not_create_uat_acceptance" in scenario.explicit_non_implementation_claims
        assert "does_not_productize_or_deploy_outputs" in scenario.explicit_non_implementation_claims


def test_trial_scenario_domain_assert_helper_reports_missing_domain():
    library = load_default_trial_scenario_coverage_library()

    assert_trial_scenario_domains_exist(library, REQUIRED_DOMAINS)

    with pytest.raises(ValueError) as exc_info:
        assert_trial_scenario_domains_exist(library, {"missing_domain"})

    assert "missing_domain" in str(exc_info.value)


def test_trial_scenario_coverage_rejects_duplicate_scenario_ids():
    library = load_default_trial_scenario_coverage_library()
    payload = library.model_dump()
    payload["scenarios"].append(payload["scenarios"][0])

    with pytest.raises(ValidationError) as exc_info:
        TrialScenarioCoverageLibraryModel(**payload)

    assert "Duplicate trial scenario coverage id" in str(exc_info.value)
