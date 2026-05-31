from pathlib import Path

import pytest

from asbp.task_pool_source_store import (
    MVP_TASK_POOL_SOURCE_PATHS,
    load_mvp_task_pool_libraries,
    load_task_pool_library_from_path,
)


P0_PROCESS_EQUIPMENT_ARCHETYPES = {
    "Tablet Compression Machine",
    "Pan Coater",
    "Capsule Filling Machine",
    "Bin Blender",
    "Vertical Granulator",
    "Fluid Bed Dryer",
    "Roller Compactor",
    "Blister Line",
    "Tablet Sorter",
    "Mill",
}

P0_DETAILED_UTILITIES = {
    "Compressed Air System",
    "Purified / Refined Water System",
    "HVAC System",
    "Chilled Water System",
}

P0_DOMAINS = {
    "cleanroom_hvac",
    "process_equipment",
    "utilities",
    "computerized_system_validation",
    "qc_lab_equipment",
    "decommissioning",
    "manual_fallback",
}

MUST_HAVE_DOCUMENT_REFS = {
    "CCF",
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
}


def test_mvp_task_pool_source_files_exist_and_load():
    for path in MVP_TASK_POOL_SOURCE_PATHS:
        assert Path(path).exists(), path
        library = load_task_pool_library_from_path(Path(path))
        assert library.status == "mvp_remediation_source"
        assert library.task_pools
        assert "does_not_generate_documents" in library.explicit_non_implementation_claims


def test_mvp_task_pool_ids_are_globally_unique():
    libraries = load_mvp_task_pool_libraries()
    task_pool_ids = [
        task_pool.task_pool_id
        for library in libraries
        for task_pool in library.task_pools
    ]

    assert len(task_pool_ids) == len(set(task_pool_ids))


def test_mvp_task_pool_domains_are_represented():
    libraries = load_mvp_task_pool_libraries()
    domains = {
        task_pool.domain
        for library in libraries
        for task_pool in library.task_pools
    }

    assert P0_DOMAINS <= domains


def test_mvp_process_equipment_archetypes_are_represented_without_codes():
    libraries = load_mvp_task_pool_libraries()
    archetypes = {
        task_pool.asset_archetype
        for library in libraries
        for task_pool in library.task_pools
        if task_pool.asset_archetype is not None
    }

    assert P0_PROCESS_EQUIPMENT_ARCHETYPES <= archetypes
    assert "Vacuum Granulator" not in archetypes
    assert "Vertical Granulator" in archetypes


def test_mvp_detailed_utilities_are_represented():
    libraries = load_mvp_task_pool_libraries()
    utilities = {
        task_pool.utility_system
        for library in libraries
        for task_pool in library.task_pools
        if task_pool.utility_system is not None
    }

    assert P0_DETAILED_UTILITIES <= utilities


def test_mvp_task_dependencies_reference_existing_atomic_tasks():
    for library in load_mvp_task_pool_libraries():
        for task_pool in library.task_pools:
            atomic_task_ids = {task.atomic_task_id for task in task_pool.tasks}
            for task in task_pool.tasks:
                for dependency in task.dependencies:
                    assert dependency.atomic_task_id in atomic_task_ids


def test_mvp_duration_refs_are_provisional_for_wave_3():
    for library in load_mvp_task_pool_libraries():
        for task_pool in library.task_pools:
            assert any("Wave 3" in limitation for limitation in task_pool.source_limitations)
            for task in task_pool.tasks:
                assert task.duration_ref.duration_ref_id.endswith("_DUR")


def test_mvp_must_have_document_expectations_are_represented():
    libraries = load_mvp_task_pool_libraries()
    document_refs = {
        expectation.document_ref
        for library in libraries
        for task_pool in library.task_pools
        for task in task_pool.tasks
        for expectation in task.document_expectations
    }

    assert MUST_HAVE_DOCUMENT_REFS <= document_refs


def test_mvp_task_pools_do_not_claim_release_or_uat_acceptance():
    blocked_terms = {
        "customer-ready",
        "release",
        "uat acceptance",
        "productization",
        "deployment",
        "saas",
    }

    for library in load_mvp_task_pool_libraries():
        searchable_text = " ".join(
            [
                *library.library_controls,
                *library.explicit_non_implementation_claims,
                *[
                    value
                    for task_pool in library.task_pools
                    for value in [
                        *task_pool.source_limitations,
                        *task_pool.explicit_non_implementation_claims,
                    ]
                ],
            ]
        ).casefold()

        assert "does_not_approve_release_or_uat_acceptance" in searchable_text
        for blocked_term in blocked_terms:
            if blocked_term in {"release", "productization", "deployment", "saas"}:
                assert f"does_not_{blocked_term}" in searchable_text or blocked_term in searchable_text
