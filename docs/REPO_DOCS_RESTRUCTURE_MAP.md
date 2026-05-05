---
doc_type: repo_hygiene_map
canonical_name: REPO_DOCS_RESTRUCTURE_MAP
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: planning_record
authority: planning_only
checkpoint: PRE_M16_REPO_HYGIENE
phase_position: Between Phase 5 closeout and Phase 6 implementation
---

# REPO_DOCS_RESTRUCTURE_MAP

## Purpose

This document records the proposed documentation restructure map before any file movement.

It is a planning artifact only. It does not move files and does not change repository authority.

## Mapping status

Status: `draft_for_review`

No file movement is authorized until this map is accepted.

---

## Root authority files — do not move

| Current path | Proposed action | Reason |
|---|---|---|
| `ROADMAP_CANONICAL.md` | Keep | Canonical roadmap authority |
| `ROADMAP_CANONICAL_CONTINUATION_PART_1_PHASES_5_6.md` | Keep | Roadmap continuation support artifact |
| `ARCHITECTURE_GUARDRAILS.md` | Keep | Permanent architecture governance |
| `PROGRESS_TRACKER.md` | Keep | Current-position execution evidence |
| `README.md` | Keep | Public surface / root navigation |
| `CONTRIBUTING.md` | Keep | Public contribution surface |
| `LICENSE` | Keep | Legal/public surface |

---

## Already organized — do not move in first wave

| Current path / area | Proposed action | Reason |
|---|---|---|
| `docs/design_spec/valor_pack_snapshot/extracted/` | Keep | Existing structured source snapshot area |
| `docs/design_spec/valor_pack_snapshot/expansion/` | Keep | Existing structured M15 expansion area |
| `docs/archives/roadmap_addenda/` | Keep | Existing archive structure |
| `docs/reference/` | Keep | Existing reference structure |
| `docs/design_notes/` | Keep | Existing design notes structure |
| `docs/design_future/` | Keep | Existing future-design structure |
| `docs/planning/` | Keep | Existing planning reference structure |

---

## Proposed M12 moves

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/M12_CLOSEOUT_NOTES.md` | `docs/milestones/M12/M12_CLOSEOUT_NOTES.md` | 2 | Closed milestone evidence |
| `docs/UAT/M12_UAT_PROTOCOL.md` | `docs/UAT/M12/M12_UAT_PROTOCOL.md` | 2 | UAT evidence grouping |
| `docs/UAT/M12_UAT_REPORT.md` | `docs/UAT/M12/M12_UAT_REPORT.md` | 2 | UAT evidence grouping |

---

## Proposed M13 moves

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/M13_VALIDATION_CHECKPOINT.md` | `docs/milestones/M13/M13_VALIDATION_CHECKPOINT.md` | 2 | Validation evidence |
| `docs/M13_CLOSEOUT_NOTES.md` | `docs/milestones/M13/M13_CLOSEOUT_NOTES.md` | 2 | Closeout evidence |
| `docs/UAT/M13_UAT_PROTOCOL.md` | `docs/UAT/M13/M13_UAT_PROTOCOL.md` | 2 | UAT evidence grouping |
| `docs/UAT/M13_UAT_REPORT.md` | `docs/UAT/M13/M13_UAT_REPORT.md` | 2 | UAT evidence grouping |

---

## Proposed M14 moves

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/M14_VALIDATION_CHECKPOINT.md` | `docs/milestones/M14/M14_VALIDATION_CHECKPOINT.md` | 2 | Validation evidence |
| `docs/M14_CLOSEOUT_NOTES.md` | `docs/milestones/M14/M14_CLOSEOUT_NOTES.md` | 2 | Closeout evidence |
| `docs/UAT/M14_UAT_PROTOCOL.md` | `docs/UAT/M14/M14_UAT_PROTOCOL.md` | 2 | UAT evidence grouping |
| `docs/UAT/M14_UAT_REPORT.md` | `docs/UAT/M14/M14_UAT_REPORT.md` | 2 | UAT evidence grouping |

---

## Proposed M15 root-doc moves

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/M15_COVERAGE_PACK_EXPANSION_FRAMEWORK.md` | `docs/milestones/M15/M15_COVERAGE_PACK_EXPANSION_FRAMEWORK.md` | 2 | Checkpoint evidence |
| `docs/M15_PRESET_SELECTOR_LIBRARY_EXPANSION.md` | `docs/milestones/M15/M15_PRESET_SELECTOR_LIBRARY_EXPANSION.md` | 2 | Checkpoint evidence |
| `docs/M15_TASK_POOL_EXPANSION.md` | `docs/milestones/M15/M15_TASK_POOL_EXPANSION.md` | 2 | Checkpoint evidence |
| `docs/M15_SUPPORT_LIBRARY_EXPANSION.md` | `docs/milestones/M15/M15_SUPPORT_LIBRARY_EXPANSION.md` | 2 | Checkpoint evidence |
| `docs/M15_LIBRARY_VALIDATION_FREEZE_RELEASE.md` | `docs/milestones/M15/M15_LIBRARY_VALIDATION_FREEZE_RELEASE.md` | 2 | Checkpoint evidence |
| `docs/M15_ORCHESTRATION_SERVICE_HARDENING.md` | `docs/milestones/M15/M15_ORCHESTRATION_SERVICE_HARDENING.md` | 2 | Checkpoint evidence |
| `docs/M15_VALIDATION_CHECKPOINT.md` | `docs/milestones/M15/M15_VALIDATION_CHECKPOINT.md` | 2 | Validation evidence |
| `docs/M15_CLOSEOUT_NOTES.md` | `docs/milestones/M15/M15_CLOSEOUT_NOTES.md` | 2 | Closeout evidence |

---

## Proposed M15 UAT moves

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/UAT/M15_UAT_PROTOCOL.md` | `docs/UAT/M15/M15_UAT_PROTOCOL.md` | 2 | UAT protocol |
| `docs/UAT/M15_UAT_REPORT.md` | `docs/UAT/M15/M15_UAT_REPORT.md` | 2 | UAT report |

---

## M15 design-spec files — keep in place

| Current path / pattern | Proposed action | Reason |
|---|---|---|
| `docs/design_spec/valor_pack_snapshot/expansion/M15_3_SELECTOR_SCOPE_EXPANSION_MAP.yaml` | Keep | Design-spec expansion map |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_4_TASK_POOL_EXPANSION_MAP.yaml` | Keep | Design-spec expansion map |
| `docs/design_spec/valor_pack_snapshot/expansion/task_pools/M15_4_TASK_POOLS_DRAFT_v1.yaml` | Keep | Structured task-pool draft source |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_5_SUPPORT_LIBRARY_EXPANSION_MAP.yaml` | Keep | Design-spec support expansion map |
| `docs/design_spec/valor_pack_snapshot/expansion/profiles/M15_5_PROFILES_DRAFT_v1.yaml` | Keep | Structured profile draft source |
| `docs/design_spec/valor_pack_snapshot/expansion/standards/M15_5_STANDARDS_APPLICABILITY_DRAFT_v1.yaml` | Keep | Structured standards draft source |
| `docs/design_spec/valor_pack_snapshot/expansion/calendars/M15_5_CALENDAR_PLANNING_BASIS_DRAFT_v1.yaml` | Keep | Structured calendar/planning draft source |
| `docs/design_spec/valor_pack_snapshot/expansion/mapping/M15_5_CROSS_LIBRARY_MAPPING_DRAFT_v1.yaml` | Keep | Structured mapping draft source |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_6_LIBRARY_RELEASE_RULES.yaml` | Keep | Structured rules source |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_7_ORCHESTRATION_SERVICE_HARDENING_RULES.yaml` | Keep | Structured rules source |

---

## Proposed archive cleanup

| Current path | Proposed path | Wave | Notes |
|---|---|---:|---|
| `docs/design_spec/ROADMAP_CANONICAL_v3_AMENDMENT_DRAFT.md` | `docs/archives/roadmap_drafts/ROADMAP_CANONICAL_v3_AMENDMENT_DRAFT.md` | 3 | Historical draft, not active authority |

---

## Reference updates required after Wave 2

If Wave 2 is executed, update references in:

| File / area | Update needed |
|---|---|
| `PROGRESS_TRACKER.md` | Replace moved M12–M15 evidence paths |
| `docs/milestones/M12/M12_CLOSEOUT_NOTES.md` | Update UAT/validation paths if present |
| `docs/milestones/M13/M13_CLOSEOUT_NOTES.md` | Update UAT/validation paths |
| `docs/milestones/M14/M14_CLOSEOUT_NOTES.md` | Update UAT/validation paths |
| `docs/milestones/M15/M15_CLOSEOUT_NOTES.md` | Update validation/UAT/checkpoint paths |
| `docs/milestones/M15/M15_VALIDATION_CHECKPOINT.md` | Update checkpoint evidence paths if root milestone docs moved |
| `docs/UAT/M15/M15_UAT_REPORT.md` | Update validation path and protocol path |
| `docs/UAT/README.md` | Update UAT file paths |
| `README.md` | Update docs links only if direct moved paths are referenced |

---

## New index files recommended in Wave 2

| New path | Purpose |
|---|---|
| `docs/README.md` | Main docs navigation |
| `docs/milestones/README.md` | Milestone evidence index |
| `docs/milestones/M12/README.md` | M12 evidence index |
| `docs/milestones/M13/README.md` | M13 evidence index |
| `docs/milestones/M14/README.md` | M14 evidence index |
| `docs/milestones/M15/README.md` | M15 evidence and design-spec index |
| `docs/UAT/M12/README.md` | M12 UAT index |
| `docs/UAT/M13/README.md` | M13 UAT index |
| `docs/UAT/M14/README.md` | M14 UAT index |
| `docs/UAT/M15/README.md` | M15 UAT index |

---

## Risk controls

- Do not move root authority files.
- Do not move code.
- Do not move VALOR snapshot `extracted/` or `expansion/` in the first wave.
- Do not delete old files manually without creating destination files first.
- After moving files, update references in the same package.
- Treat broken links as cleanup defects.
- Run tests only if code changes.

---

## Recommended next action after this map

Review this map.

If accepted, perform Wave 2 only:

- M12–M15 milestone docs
- M12–M15 UAT docs
- docs indexes
- reference updates
