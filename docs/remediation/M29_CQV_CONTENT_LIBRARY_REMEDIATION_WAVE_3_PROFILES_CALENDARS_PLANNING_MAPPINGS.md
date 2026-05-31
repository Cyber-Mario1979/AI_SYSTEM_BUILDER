---
doc_type: remediation_evidence
canonical_name: M29_CQV_CONTENT_LIBRARY_REMEDIATION_WAVE_3_PROFILES_CALENDARS_PLANNING_MAPPINGS
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 3 — Profiles, calendars, planning basis, and mappings expansion
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29 CQV Content Library Remediation — Wave 3

## Purpose

Wave 3 expands MVP profile, calendar, planning-basis, and mapping source records so that the Wave 2 MVP task-pool expansion is supported by traceable source families instead of starter-only context records.

## Implementation Assets

This package adds or updates:

- `asbp/profile_source_model.py`
- `asbp/profile_source_store.py`
- `asbp/calendar_source_model.py`
- `asbp/calendar_source_store.py`
- `asbp/planning_basis_source_model.py`
- `asbp/planning_basis_source_store.py`
- `asbp/mapping_source_model.py`
- `asbp/mapping_source_store.py`
- `data/source/profiles/mvp_cleanroom_hvac_profiles.json`
- `data/source/profiles/mvp_process_equipment_profiles.json`
- `data/source/profiles/mvp_utilities_profiles.json`
- `data/source/profiles/mvp_csv_profiles.json`
- `data/source/profiles/mvp_qc_lab_equipment_profiles.json`
- `data/source/profiles/mvp_decommissioning_profiles.json`
- `data/source/profiles/mvp_manual_fallback_profiles.json`
- `data/source/calendars/mvp_calendars.json`
- `data/source/planning_basis/mvp_planning_basis_duration_refs.json`
- `data/source/mappings/mvp_mappings.json`
- `tests/test_mvp_profile_calendar_planning_mapping_expansion.py`

## Scope Covered

Wave 3 covers:

- Cleanroom / HVAC profile context;
- process equipment archetype profile context;
- detailed P0 utility system profile context;
- CSV/GxP system profile context;
- QC laboratory equipment/calibration/CSV-linkage profile context;
- decommissioning lifecycle route profile context;
- manual fallback context;
- MVP calendar assumptions and site holiday/shutdown visibility;
- duration references for Wave 2 task pools;
- mappings from presets/profiles/selectors/task pools/tasks to document expectations.

## Validation Requirement

Because Wave 3 changes source JSON, source models/stores, mappings, planning-basis records, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this package record.

## Remaining Gaps

Remaining remediation waves:

- Wave 4 — Document template body expansion;
- Wave 5 — Document input schema and DCF expansion;
- Wave 6 — Standards/citation expansion where approved;
- Wave 7 — Trial scenario expansion;
- Wave 8 — Validation and UAT return gate.

## Explicit Non-Implementation Claims

Wave 3 does not:

- implement document template bodies;
- implement document input schemas or DCF expansion;
- implement standards retrieval or embedding;
- implement trial scenario expansion;
- accept M29.12 UAT;
- close M29;
- authorize productization, deployment, commercial release, or SaaS readiness.

## Validation Fix Note

The Wave 3 validation fix preserves the existing profile context-field rule that `starter_default` fields require explicit `value` content. The fix adds explicit default values to MVP process-equipment and utility profile fields instead of weakening validation.
