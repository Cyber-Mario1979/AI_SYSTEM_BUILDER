---
doc_type: milestone_checkpoint_output
canonical_name: M15_SUPPORT_LIBRARY_EXPANSION
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.5
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.5 — Calendar / Standards / Profile / Mapping Expansion

## Checkpoint

`M15.5` — Calendar / standards / profile / mapping expansion

## Purpose

This document records the M15.5 support-library expansion package.

The package connects the accepted M15.3 selector expansion and M15.4 draft task-pool expansion to their draft support assets:

- profiles
- standards applicability
- calendar / planning-basis bridge records
- cross-library mapping metadata
- document-obligation mapping metadata

This checkpoint is documentation/specification-only and does not create runtime authority.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## Input from M15.3 and M15.4

M15.3 defined the expanded selector/scope matrix and the `CSV` naming decision.

M15.4 defined 12 draft task-pool source definitions and left profile duration values, standards applicability, calendar/planning-basis linkage, and mapping metadata pending M15.5.

## Deliverables

This package adds:

- `docs/M15_SUPPORT_LIBRARY_EXPANSION.md`
- `docs/design_spec/valor_pack_snapshot/expansion/M15_5_SUPPORT_LIBRARY_EXPANSION_MAP.yaml`
- `docs/design_spec/valor_pack_snapshot/expansion/profiles/M15_5_PROFILES_DRAFT_v1.yaml`
- `docs/design_spec/valor_pack_snapshot/expansion/standards/M15_5_STANDARDS_APPLICABILITY_DRAFT_v1.yaml`
- `docs/design_spec/valor_pack_snapshot/expansion/calendars/M15_5_CALENDAR_PLANNING_BASIS_DRAFT_v1.yaml`
- `docs/design_spec/valor_pack_snapshot/expansion/mapping/M15_5_CROSS_LIBRARY_MAPPING_DRAFT_v1.yaml`

## Runtime authority rule

All records in this checkpoint are draft support-library records.

They are not runtime authority and must not be treated as deployment-compiled lookup records.

## Draft profile records

| Profile | Bound task pool | Profile key count | Calendar |
|---|---|---:|---|
| `PROF-PE-QUAL@v1` | `TP-PE-QUAL@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-PE-COMM@v1` | `TP-PE-COMM@v1` | 8 | `CAL-WORKWEEK@v1` |
| `PROF-PE-DECOM@v1` | `TP-PE-DECOM@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-UT-PV@v1` | `TP-UT-PV@v1` | 8 | `CAL-WORKWEEK@v1` |
| `PROF-UT-DECOM@v1` | `TP-UT-DECOM@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-CR-POST-DEV@v1` | `TP-CR-POST-DEV@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-CR-POST-CHANGE@v1` | `TP-CR-POST-CHANGE@v1` | 8 | `CAL-WORKWEEK@v1` |
| `PROF-CR-DECOM@v1` | `TP-CR-DECOM@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-CSV-PV@v1` | `TP-CSV-PV@v1` | 8 | `CAL-WORKWEEK@v1` |
| `PROF-CSV-POST-DEV@v1` | `TP-CSV-POST-DEV@v1` | 9 | `CAL-WORKWEEK@v1` |
| `PROF-CSV-POST-CHANGE@v1` | `TP-CSV-POST-CHANGE@v1` | 8 | `CAL-WORKWEEK@v1` |
| `PROF-CSV-DECOM@v1` | `TP-CSV-DECOM@v1` | 9 | `CAL-WORKWEEK@v1` |

## Calendar decision

M15.5 does not introduce a new calendar family.

All draft support records bind to:

`CAL-WORKWEEK@v1`

This preserves the existing Sun–Thu workweek and Fri–Sat weekend baseline.

## Standards applicability decision

M15.5 records draft standards applicability as follows:

- `SB-CQV-CORE-EG@v1` is the default core baseline for all PE, UT, CR, and CSV coverage.
- `SB-CLEANROOM-ADDON@v1` is applied to CR coverage.
- `SB-CSV-ADDON@v1` is applied to CSV coverage.
- UT-HVAC or classified-area-impacting variants may receive the cleanroom add-on later through more specific mapping.

Bundle IDs remain draft applicability records until validated/frozen in M15.6.

## Mapping metadata decision

M15.5 creates draft mapping metadata for:

- selector to task pool
- selector to profile
- selector to calendar
- selector to standards bundle
- selector to planning basis
- task pool to profile
- task segment to profile key
- task pool to document obligation families
- legacy CS to future CSV naming

## Not in M15.5 scope

M15.5 does not implement:

- deployment compiled lookup
- runtime migration
- validation/freeze engine
- CLI changes
- orchestration/service hardening
- AI runtime behavior
- final canonical release

## Checkpoint decision

M15.5 records the support-library expansion needed to make the M15.3/M15.4 draft selector and task-pool coverage structurally connected.

The project should not treat these records as runtime-authoritative until M15.6 validation/freeze/release discipline and M15.7 service hardening are complete.

## Validation note

This checkpoint package is documentation/specification-only.

No Python code or runtime behavior was changed.

`python -m pytest -q` was not run for this generated package. The latest verified validation status remains the tracker-recorded result until validation is run again.
