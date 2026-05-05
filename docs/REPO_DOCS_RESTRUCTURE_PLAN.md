---
doc_type: repo_hygiene_plan
canonical_name: REPO_DOCS_RESTRUCTURE_PLAN
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: planning_record
authority: planning_only
checkpoint: PRE_M16_REPO_HYGIENE
phase_position: Between Phase 5 closeout and Phase 6 implementation
---

# REPO_DOCS_RESTRUCTURE_PLAN

## Purpose

This document records a bounded pre-M16 repository hygiene and documentation-restructure plan.

The pass is intended to clean up and organize repository documentation before starting:

`M16.1` — AI runtime boundary for document/reporting jobs

This plan is not a roadmap addendum, not a governance change, and not a feature implementation.

## Current repo state

The project has completed:

- Phase 5 — Core Engine Completion
- Milestone 15 — Governed Library Expansion and Engine Hardening
- `M15.10` — Milestone closeout

The tracker now points to:

- Phase 6 — AI Layer
- `M16.1` — AI runtime boundary for document/reporting jobs

## Why this pass exists

Before entering Phase 6, the repository now needs a docs cleanup pass because the `docs/` folder contains multiple document roles mixed together:

- milestone evidence documents in `docs/`
- UAT protocol/report files in `docs/UAT/`
- UAT evidence logs in `docs/UAT/evidence/`
- design notes in `docs/design_notes/`
- future-facing design records in `docs/design_future/`
- reference material in `docs/reference/`
- roadmap archives in `docs/archives/`
- VALOR snapshot and expansion specifications in `docs/design_spec/valor_pack_snapshot/`
- planning references in `docs/planning/`

The goal is to improve discoverability without changing source-of-truth authority.

## Boundaries

This pass may:

- audit repo and docs structure
- define a target docs layout
- define a migration map
- define reference update requirements
- create documentation indexes
- move documentation files only after the move map is approved
- update references after approved file moves

This pass must not:

- change roadmap sequence
- change architecture guardrails
- change execution governance
- change Python behavior
- change CLI behavior
- change runtime behavior
- change AI behavior
- rename root authority files
- move root authority files
- silently demote validation/UAT/closeout evidence
- treat planning/support docs as execution authority

## Root files to preserve

The following root-level files must remain where they are:

- `ROADMAP_CANONICAL.md`
- `ROADMAP_CANONICAL_CONTINUATION_PART_1_PHASES_5_6.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`
- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`

These files have root visibility and/or authority roles and should not be moved as part of docs restructuring.

## Proposed target docs layout

```text
docs/
  README.md

  milestones/
    M12/
    M13/
    M14/
    M15/

  UAT/
    README.md
    M12/
    M13/
    M14/
    M15/
    evidence/

  design_spec/
    valor_pack_snapshot/
      extracted/
      expansion/

  design_notes/
  design_future/
  planning/
  reference/

  archives/
    roadmap_addenda/
    roadmap_drafts/
```

## First restructure wave

The recommended first actual restructure wave should focus on closed Phase 5 / recent milestones:

- M12
- M13
- M14
- M15

Reason:

- these milestones are now closed and accepted
- they have consistent validation/UAT/closeout patterns
- they directly anchor the transition into Phase 6
- this avoids a risky one-shot reorganization of every historical milestone file

## Second restructure wave

After the first wave is stable, historical UAT and milestone artifacts from earlier milestones may be moved into the same folder pattern:

- M4
- M5
- M6
- M8
- M9
- M10
- M11 where applicable

This second wave should be map-driven and should update references.

## VALOR snapshot handling

Do not move `docs/design_spec/valor_pack_snapshot/` in the first restructure wave.

Reason:

- it already has an internal structure
- it contains extracted source snapshots and expansion drafts
- it is heavily referenced by M15 evidence
- moving it would create a high link-break risk with limited organizational benefit

The better first action is to index it from `docs/README.md` and from the future `docs/milestones/M15/README.md`.

## UAT folder handling

The target UAT structure should group milestone UAT records by milestone:

```text
docs/UAT/M15/M15_UAT_PROTOCOL.md
docs/UAT/M15/M15_UAT_REPORT.md
```

The current flat UAT files should move only after all references are updated.

## Milestone folder handling

Closed milestone evidence should be grouped under:

```text
docs/milestones/Mxx/
```

Example:

```text
docs/milestones/M15/M15_VALIDATION_CHECKPOINT.md
docs/milestones/M15/M15_CLOSEOUT_NOTES.md
```

For M15, root milestone evidence docs may move into `docs/milestones/M15/`, while VALOR snapshot expansion YAMLs should remain in `docs/design_spec/valor_pack_snapshot/expansion/`.

## Reference update requirements

If files are moved, references must be updated in:

- `PROGRESS_TRACKER.md`
- milestone closeout notes
- validation checkpoint docs
- UAT reports
- `docs/UAT/README.md`
- `docs/README.md` if created
- root `README.md` if it links to moved docs
- any docs that cite the old file paths

Moving files without reference updates is not acceptable.

## Proposed execution sequence

### Pass 1 — Audit/map only

Create:

- `docs/REPO_DOCS_RESTRUCTURE_PLAN.md`
- `docs/REPO_DOCS_RESTRUCTURE_MAP.md`

No files are moved.

### Pass 2 — M12–M15 structure and references

After approval:

- create `docs/README.md`
- create `docs/milestones/M12/` through `docs/milestones/M15/`
- create `docs/UAT/M12/` through `docs/UAT/M15/`
- move M12–M15 milestone evidence docs
- move M12–M15 UAT protocol/report docs
- update references
- leave VALOR snapshot files in place
- leave root authority files in place

### Pass 3 — earlier milestone cleanup

After Pass 2 is stable:

- map earlier milestone docs
- move older UAT artifacts into milestone folders where appropriate
- update references

## Validation expectation

If the pass remains docs-only, no pytest run is required.

If any Python/package/runtime file changes, run:

```powershell
python -m pytest -q
```

## Approval status

This document is planning evidence only.

It does not authorize file moves until the restructure map is reviewed and accepted.
