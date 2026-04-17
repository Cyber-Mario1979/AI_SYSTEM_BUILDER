---
doc_type: roadmap_addendum
canonical_name: ROADMAP_ADDENDUM_03_PRE_M8_PRESET_SOURCE_ALIGNMENT.md
status: COMPLETED_HISTORICAL
governs_execution: false
authority: subordinate_to_ROADMAP_CANONICAL
scope_type: temporary_overlay
milestone_scope: PRE_M8_ALIGNMENT
phase_scope: Phase 3 gateway
---

# ROADMAP_ADDENDUM_03_PRE_M8_PRESET_SOURCE_ALIGNMENT

## Historical Completion Note

This addendum is no longer active.

Its exit condition was satisfied after:

- canonical roadmap amendment to v3
- tracker normalization to the corrected Milestone 8 checkpoint label

It remains in the repo for traceability only.

## Purpose

This addendum authorized a bounded pre-implementation alignment pass before further Milestone 8 execution continued.

It existed because the imported design snapshot and the current repo-real ASBP model were not merely using different wording.
They expressed different upstream product models for how work enters the system.

This addendum did not replace the canonical roadmap.
It temporarily supplemented it so the product model could be aligned explicitly before more implementation work proceeded.

## Authority

This addendum remained subordinate to `ROADMAP_CANONICAL.md`.

It was activated because the tracked next checkpoint was `M8.1 — Cross-entity relationship foundation`, while the imported design snapshot indicated a missing upstream source-of-work layer that materially affected how cross-entity relationships should be modeled.

## Historical application of this addendum

The repo-real model at the time treated:

- `tasks` as already-instantiated persisted entities
- `task_collections` as workflow-state containers over existing tasks
- `plans` as downstream schedule artifacts derived from committed tasks

The imported design snapshot made explicit a different upstream flow:

- preset
- selector context
- task pool
- staged task set
- committed task instantiation
- downstream execution and planning

Therefore, continuing normal `M8.1` implementation at that time would have risked hardening the wrong relationship model.

## Historical scope of this addendum

This addendum applied only to the bounded alignment work required to formalize the upstream source-of-work model before further Milestone 8 implementation continued.

It applied only to:

- product-model comparison between the current repo and the imported design snapshot
- explicit identification of the authoritative source-of-work path
- clarification of source vs instantiated task records
- clarification of ownership vs membership vs derived planning artifacts
- drafting and approving the required canonical roadmap amendment
- re-declaring the exact next unfinished checkpoint after roadmap amendment

## Allowed work under this addendum

Allowed work:

- import the pack into the repo as a non-authoritative design snapshot
- classify and inventory imported design files
- compare current repo behavior against imported orchestration/runtime design
- define the canonical upstream source-of-work model
- preserve the current ASBP deterministic core as the downstream execution layer if still valid
- draft a canonical roadmap amendment that formalized the corrected model
- update tracker wording after the roadmap direction was formally amended
- perform design-only normalization needed to restore checkpoint clarity

## Not allowed under this addendum

Not allowed:

- normal Milestone 8 feature coding
- silent continuation of `M8.1` as if no model conflict existed
- treating the imported pack snapshot as implementation truth
- replacing the current repo core without explicit roadmap approval
- parallel-system feature expansion
- hidden roadmap changes without explicit amendment
- using the alignment pass as a pretext for unrelated refactors

## Historical pause rule

While this addendum was active:

- further normal `M8.1` implementation was paused
- no new cross-entity runtime behavior was to be coded
- no new task-source behavior was to be implemented
  until the canonical source-of-work model was formally clarified

## Historical locked checkpoint

**Pre-M8 product-model alignment checkpoint — define the canonical source-of-work path and formalize it through a canonical roadmap amendment before resuming implementation.**

## Historical required alignment outcome

The alignment work under this addendum explicitly required deciding and documenting:

1. whether presets and selector context were only metadata or true upstream binding seeds
2. whether task pools were authoritative work sources
3. whether `state.tasks` were canonical source records or instantiated execution records
4. what role `task_collections` played relative to staged/committed task selection
5. how planning related to instantiated committed tasks
6. what exact checkpoint should follow once the roadmap was amended

## Exit condition

This addendum reached completion when all of the following became true:

- the canonical upstream source-of-work model was explicitly decided
- the canonical roadmap was amended to reflect that model
- the tracker was updated to reflect the corrected execution position
- the exact next unfinished checkpoint was re-declared without ambiguity
- normal implementation could resume without product-model conflict
