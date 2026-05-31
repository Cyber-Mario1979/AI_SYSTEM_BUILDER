from asbp.calendar_source_store import load_mvp_calendar_library
from asbp.mapping_source_store import load_mvp_mapping_library, list_mappings_by_kind
from asbp.planning_basis_source_model import collect_planning_basis_duration_refs, collect_task_pool_duration_refs
from asbp.planning_basis_source_store import load_mvp_planning_basis_library
from asbp.profile_source_store import load_mvp_profile_libraries
from asbp.task_pool_source_store import load_mvp_task_pool_libraries


P0_PROCESS_EQUIPMENT_PROFILE_NAMES = {
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

P0_UTILITY_PROFILE_NAMES = {
    "Compressed Air System",
    "Purified / Refined Water System",
    "HVAC System",
    "Chilled Water System",
}


def _mvp_task_pools():
    return [task_pool for library in load_mvp_task_pool_libraries() for task_pool in library.task_pools]


def _mvp_profiles():
    return [profile for library in load_mvp_profile_libraries() for profile in library.profiles]


def _atomic_task_source_ids():
    return {
        f"{task_pool.task_pool_id}::{task.atomic_task_id}"
        for task_pool in _mvp_task_pools()
        for task in task_pool.tasks
    }


def test_mvp_profile_libraries_cover_wave_1_domains_and_archetypes():
    profiles = _mvp_profiles()
    profile_ids = {profile.profile_id for profile in profiles}
    display_names = {profile.display_name for profile in profiles}

    assert "PROF-MVP-CLEANROOM-HVAC@v1" in profile_ids
    assert "PROF-MVP-CSV-GXP-SYSTEM@v1" in profile_ids
    assert "PROF-MVP-QC-LAB-EQUIPMENT@v1" in profile_ids
    assert "PROF-MVP-DECOMMISSIONING-ROUTE@v1" in profile_ids
    assert "PROF-MVP-MANUAL-FALLBACK-CONTEXT@v1" in profile_ids

    for expected_name in P0_PROCESS_EQUIPMENT_PROFILE_NAMES:
        assert any(expected_name in name for name in display_names)

    for expected_name in P0_UTILITY_PROFILE_NAMES:
        assert any(expected_name in name for name in display_names)


def test_mvp_calendar_library_preserves_visible_calendar_assumptions():
    calendar_library = load_mvp_calendar_library()
    calendar_ids = {calendar.calendar_id for calendar in calendar_library.calendars}

    assert "CAL-MVP-CAIRO-FIVE-DAY-WORKWEEK@v1" in calendar_ids
    assert "CAL-MVP-CAIRO-SIX-DAY-WORKWEEK@v1" in calendar_ids
    assert "CAL-MVP-SITE-HOLIDAY-SHUTDOWN-POLICY@v1" in calendar_ids

    assert all(calendar.assumption_controls for calendar in calendar_library.calendars)
    assert any(
        rule.scope == "user_supplied_holidays"
        for calendar in calendar_library.calendars
        for rule in calendar.holiday_rules
    )


def test_mvp_planning_basis_covers_all_wave_2_duration_refs():
    planning_basis = load_mvp_planning_basis_library()
    planning_refs = collect_planning_basis_duration_refs(planning_basis)

    for task_pool_library in load_mvp_task_pool_libraries():
        task_refs = collect_task_pool_duration_refs(task_pool_library)
        assert task_refs <= planning_refs

    assert all(source.user_amendable for source in planning_basis.duration_sources)
    assert all(
        source.calendar_dependency_status == "calendar_required_before_scheduling"
        for source in planning_basis.duration_sources
    )


def test_mvp_mapping_library_resolves_profile_task_pool_and_atomic_task_refs():
    mapping_library = load_mvp_mapping_library()
    profile_ids = {profile.profile_id for profile in _mvp_profiles()}
    task_pool_ids = {task_pool.task_pool_id for task_pool in _mvp_task_pools()}
    atomic_task_ids = _atomic_task_source_ids()

    for mapping in mapping_library.mappings:
        for ref in [*mapping.source_refs, *mapping.target_refs]:
            if ref.reference_status != "resolved_source":
                continue
            if ref.reference_type == "profile":
                assert ref.reference_id in profile_ids
            if ref.reference_type == "task_pool":
                assert ref.reference_id in task_pool_ids
            if ref.reference_type == "atomic_task":
                assert ref.reference_id in atomic_task_ids


def test_mvp_mappings_cover_task_pools_and_task_document_expectations():
    mapping_library = load_mvp_mapping_library()
    selector_targets = {
        ref.reference_id
        for mapping in list_mappings_by_kind(mapping_library, "selector_to_task_pool")
        for ref in mapping.target_refs
        if ref.reference_type == "task_pool"
    }
    task_document_sources = {
        ref.reference_id
        for mapping in list_mappings_by_kind(mapping_library, "task_to_document")
        for ref in mapping.source_refs
        if ref.reference_type == "atomic_task"
    }

    task_pool_ids = {task_pool.task_pool_id for task_pool in _mvp_task_pools()}
    expected_document_task_ids = {
        f"{task_pool.task_pool_id}::{task.atomic_task_id}"
        for task_pool in _mvp_task_pools()
        for task in task_pool.tasks
        if task.document_expectations
    }

    assert task_pool_ids <= selector_targets
    assert expected_document_task_ids <= task_document_sources


def test_wave_3_sources_do_not_claim_uat_release_or_productization():
    blocked_terms = [
        "does_not_accept_m29_12_uat",
        "does_not_close_m29",
        "does_not_authorize_productization",
        "does_not_authorize_deployment",
        "does_not_authorize_saas_readiness",
    ]

    claim_text = " ".join(
        [
            *load_mvp_calendar_library().explicit_non_implementation_claims,
            *load_mvp_planning_basis_library().explicit_non_implementation_claims,
            *load_mvp_mapping_library().explicit_non_implementation_claims,
            *[
                claim
                for library in load_mvp_profile_libraries()
                for claim in library.explicit_non_implementation_claims
            ],
        ]
    ).casefold()

    for blocked_term in blocked_terms:
        assert blocked_term in claim_text
