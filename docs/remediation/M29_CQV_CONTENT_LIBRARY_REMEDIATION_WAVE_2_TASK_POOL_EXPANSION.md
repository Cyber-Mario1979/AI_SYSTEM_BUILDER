---
doc_type: remediation_evidence
canonical_name: M29_CQV_CONTENT_LIBRARY_REMEDIATION_WAVE_2_TASK_POOL_EXPANSION
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 2 — Task-pool expansion
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29 — CQV Content Library Remediation Wave 2: Task-Pool Expansion

## Purpose

This evidence record supports Wave 2 of the M29.12 CQV content-library completion remediation.

Wave 2 expands task-pool source content for the approved MVP scope from the revised coverage matrix. It does not accept M29.12, close M29, implement document templates, implement schemas/DCF, implement standards retrieval, or create productization/SaaS readiness.

## Implementation Assets

The Wave 2 package adds or updates:

- `asbp/task_pool_source_model.py`
- `asbp/task_pool_source_store.py`
- `data/source/task_pools/mvp_cleanroom_hvac_task_pools.json`
- `data/source/task_pools/mvp_process_equipment_task_pools.json`
- `data/source/task_pools/mvp_utilities_task_pools.json`
- `data/source/task_pools/mvp_csv_task_pools.json`
- `data/source/task_pools/mvp_qc_lab_equipment_task_pools.json`
- `data/source/task_pools/mvp_decommissioning_task_pools.json`
- `data/source/task_pools/mvp_manual_fallback_task_pools.json`
- `tests/test_mvp_task_pool_expansion.py`

## Covered P0 Domains

Wave 2 adds task-pool source coverage for:

- Cleanroom / HVAC qualification
- Process equipment qualification
- Utilities qualification
- Computerized system validation / CSV
- QC laboratory equipment / calibration linkage
- Decommissioning
- Manual fallback / unsupported-scope routing

## Covered Process Equipment Archetypes

Wave 2 includes task-pool coverage for:

- Tablet Compression Machine
- Pan Coater
- Capsule Filling Machine
- Bin Blender
- Vertical Granulator
- Fluid Bed Dryer
- Roller Compactor
- Blister Line
- Tablet Sorter
- Mill

## Covered Utility Systems

Wave 2 includes detailed P0 utility task-pool coverage for:

- Compressed Air System
- Purified / Refined Water System
- HVAC System
- Chilled Water System

It also includes general-first utility task-pool coverage for:

- Steam System
- Hot Water System
- Vacuum System
- Nitrogen System
- Drainage System
- Electrical Power System

## Document Expectation Handling

Wave 2 does not generate documents.

Task pools carry controlled document expectation references to support later Wave 4 template-body expansion and Wave 5 schema/DCF expansion.

## Remaining Gaps

Remaining remediation waves are still required:

- Wave 3 — profiles, calendars, planning basis, and mappings expansion
- Wave 4 — document template body expansion
- Wave 5 — document input schema and DCF expansion
- Wave 6 — standards/citation expansion where approved
- Wave 7 — trial scenario expansion
- Wave 8 — validation and UAT return gate

## Validation Requirement

Because Wave 2 changes source JSON, source models/stores, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this user-applied package record.

## Explicit Non-Implementation Claims

Wave 2 does not:

- accept M29.12;
- close M29;
- implement document template bodies;
- implement document input schemas or DCF expansion;
- implement standards retrieval or embedding;
- implement trial scenario expansion;
- create customer-ready release;
- deploy or productize outputs;
- create SaaS readiness.

## Tracker Movement Rule

Tracker must not advance to M29.13.

After successful validation, tracker may record Wave 2 remediation progress while keeping M29.12 blocked and latest completed roadmap checkpoint as M29.11.

## Validation Fix Note

A Wave 2 validation fix was applied after the first pytest run identified two source/test alignment gaps:

- `QP` was not explicitly represented in MVP task-pool document expectations.
- Non-authorization language for productization, deployment, SaaS readiness, release, and UAT acceptance needed to be visible in task-pool source records.

This fix updates task-pool source JSON only. It does not implement document templates, schemas, rendering, UAT acceptance, M29 closeout, productization, deployment, or SaaS readiness.
