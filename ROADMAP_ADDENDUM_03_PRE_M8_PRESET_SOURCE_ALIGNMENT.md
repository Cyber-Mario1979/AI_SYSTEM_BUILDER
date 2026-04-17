---
doc_type: roadmap_addendum
canonical_name: ROADMAP_ADDENDUM_03_PRE_M8_PRESET_SOURCE_ALIGNMENT.md
status: ACTIVE
governs_execution: true
authority: subordinate_to_ROADMAP_CANONICAL
scope_type: temporary_overlay
milestone_scope: PRE_M8_ALIGNMENT
phase_scope: Phase 3 gateway
---

# ROADMAP_ADDENDUM_03_PRE_M8_PRESET_SOURCE_ALIGNMENT

## Purpose

This addendum authorizes a bounded pre-implementation alignment pass before further Milestone 8 execution continues.

It exists because the imported design snapshot and the current repo-real ASBP model are not merely using different wording.
They currently express different upstream product models for how work enters the system.

This addendum does not replace the canonical roadmap.
It temporarily supplements it so the product model can be aligned explicitly before more implementation work proceeds.

## Authority

This addendum is subordinate to `ROADMAP_CANONICAL.md`.

It is active because the next tracked checkpoint is currently `M8.1 — Cross-entity relationship foundation`, while the current imported design snapshot indicates a missing upstream source-of-work layer that materially affects how cross-entity relationships should be modeled.

## Current application of this addendum

The current repo-real model treats:

- `tasks` as already-instantiated persisted entities
- `task_collections` as workflow-state containers over existing tasks
- `plans` as downstream schedule artifacts derived from committed tasks

The imported design snapshot instead makes explicit a different upstream flow:

- preset
- selector context
- task pool
- staged task set
- committed task instantiation
- downstream execution and planning

Therefore, continuing normal `M8.1` implementation immediately would risk hardening the wrong relationship model.

## Scope of this addendum

This addendum applies only to the bounded alignment work required to formalize the upstream source-of-work model before further Milestone 8 implementation continues.

It applies only to:

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
- draft a canonical roadmap amendment that formalizes the corrected model
- update tracker wording only after the roadmap direction is formally amended
- perform design-only normalization needed to restore checkpoint clarity

## Not allowed under this addendum

Not allowed:

- normal Milestone 8 feature coding
- silent continuation of `M8.1` as if no model conflict exists
- treating the imported pack snapshot as implementation truth
- replacing the current repo core without explicit roadmap approval
- parallel-system feature expansion
- hidden roadmap changes without explicit amendment
- using this alignment pass as a pretext for unrelated refactors

## Pause rule

While this addendum is active:

- further normal `M8.1` implementation is paused
- no new cross-entity runtime behavior should be coded
- no new task-source behavior should be implemented
  until the canonical source-of-work model is formally clarified

## Locked next checkpoint under this addendum

Locked checkpoint:

**Pre-M8 product-model alignment checkpoint — define the canonical source-of-work path and formalize it through a canonical roadmap amendment before resuming implementation.**

## Required alignment outcome

The alignment work under this addendum must explicitly decide and document:

1. whether presets and selector context are only metadata or true upstream binding seeds
2. whether task pools are authoritative work sources
3. whether `state.tasks` are canonical source records or instantiated execution records
4. what role `task_collections` play relative to staged/committed task selection
5. how planning relates to instantiated committed tasks
6. what exact checkpoint should follow once the roadmap is amended

## Exit condition for this addendum

This addendum remains active until all of the following are true:

- the canonical upstream source-of-work model is explicitly decided
- the canonical roadmap is amended to reflect that model
- the tracker is updated to reflect the corrected execution position
- the exact next unfinished checkpoint is re-declared without ambiguity
- normal implementation can resume without product-model conflict
