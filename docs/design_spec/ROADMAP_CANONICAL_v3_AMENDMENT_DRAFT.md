---
doc_type: canonical_roadmap_amendment_draft
canonical_name: ROADMAP_CANONICAL_v3_AMENDMENT_DRAFT
status: DRAFT_FOR_REVIEW
target_file: ROADMAP_CANONICAL.md
intended_result: ROADMAP_CANONICAL v3
supersedes_on_approval: ROADMAP_CANONICAL v2
---

# ROADMAP_CANONICAL v3 — Amendment Draft

## Approval Status

This document is a draft for review.

It is not the canonical roadmap yet.

The canonical roadmap remains `ROADMAP_CANONICAL.md` until this amendment draft is explicitly approved and its content is merged into the canonical roadmap.

---

## Amendment Intent

This amendment updates the canonical roadmap so the upstream source-of-work model becomes explicit and governable.

This is a permanent product-model clarification, not a temporary overlay.

It preserves the existing deterministic core while making the following distinctions explicit:

- presets and selector context are true upstream binding seeds
- task pools or equivalent source libraries are authoritative work-definition sources when the preset-driven path is used
- persisted `tasks` are instantiated execution records, not the only possible upstream work-definition source
- task collections operate on instantiated task records
- planning operates on committed instantiated tasks, not directly on library definitions
- the manual-first task path remains valid as a lower-automation fallback path

---

## Why v3 exists

Roadmap v2 already made preset-first direction, selector context, standards bundles, collection workflow states, and planning direction explicit.

However, it still left one product-model distinction too implicit:

the difference between **authoritative work-definition sources** and **instantiated execution records**.

That distinction must now be explicit.

The following directions must become canonical and no longer remain inferred:

- preset and selector context are upstream binding seeds, not decorative metadata
- task pools or equivalent source libraries are authoritative work-definition sources when preset-driven flow is used
- persisted `tasks` represent instantiated execution records inside the active deterministic system state
- task collections organize and govern instantiated execution records, not raw library definitions
- planning consumes committed instantiated tasks, not task-pool library entries directly
- the deterministic execution core remains valid, but it must be understood as downstream from source resolution and instantiation
- the manual-first task path remains a valid lower-automation fallback and must remain explicit rather than accidental

---

## Strategic Change Summary

The canonical roadmap must now explicitly distinguish between:

### 1) Source definitions

These are authoritative upstream work-definition sources.

Examples:

- presets
- selector presets
- task pools
- profiles
- calendars
- standards bundles

### 2) Instantiated execution records

These are persisted execution-state records inside the active deterministic system state.

Examples:

- persisted tasks attached to execution context

### 3) Workflow-state containers

These organize instantiated execution records through deterministic workflow states.

Examples:

- source collections
- staged collections
- committed collections
- refined collections

### 4) Derived downstream artifacts

These are produced after instantiation and workflow commitment.

Examples:

- planning state
- schedule outputs
- later runtime-generated outputs

This amendment preserves the current deterministic execution core and introduces the missing source-of-work clarification above it.

---

## Manual-Path Clarification

The manual-first path remains valid as a lower-automation fallback.

In that path, tasks may be created directly as instantiated execution records without prior task-pool resolution.

The preset-driven path is the preferred upstream source-resolution path, not the only valid system entry path.

This means the current ASBP deterministic execution core remains valid.

It must simply be interpreted correctly:

- as the downstream execution layer when preset-driven source resolution is used
- and as the direct entry path when the operator chooses the manual-first lower-automation flow

---

## Canonical Product Model for v3

The canonical forward model becomes:

- user-facing preset selection
- selector-context resolution
- authoritative source lookup such as task pool / profile / calendar / standards bundle
- staged selection where applicable
- task instantiation into persisted deterministic execution state
- workflow-state handling over instantiated tasks through collections
- planning from committed instantiated tasks
- later downstream runtime and output layers

This model does not require source libraries to share the same persisted representation as execution tasks.

It requires only that source authority, instantiation rules, and downstream handoff boundaries are explicit and deterministic.

This model must preserve deterministic boundaries between:

- source definition
- instantiated execution record
- ownership
- membership
- reference
- derived planning artifact

The roadmap must not collapse these layers into one ambiguous task model.

---

## Proposed Canonical Front Matter for v3

When approved, the canonical roadmap front matter should be:

```md
---
doc_type: canonical_roadmap
canonical_name: ROADMAP_CANONICAL
status: ACTIVE_APPROVED
governs_execution: true
document_state_mode: state_agnostic
authority: canonical_strategic_source_of_truth
version: v3
supersedes: ROADMAP_CANONICAL v2
---
```

---

## Proposed Canonical Approval Note for v3

When approved, the canonical roadmap approval note should state:

- this roadmap v3 is approved and authoritative
- it is a real roadmap amendment, not a minor wording cleanup
- it preserves the completed deterministic foundation and planning history
- it makes the upstream source-of-work model explicit for forward execution from Milestone 8 onward

---

## Proposed Roadmap Design Principle Additions

The canonical roadmap design principles should explicitly include:

- authoritative work-definition sources must be explicitly separated from instantiated execution records
- preset-driven flow may resolve work from source libraries before execution records are instantiated
- persisted tasks are execution-state records and must not be treated as the only possible upstream source-of-work model
- collections govern workflow-state handling over instantiated tasks
- planning is downstream from committed instantiated tasks, even when the original source-of-work came from task pools or selector-bound libraries
- the manual-first task path remains valid as a lower-automation fallback and must stay compatible with the deterministic execution core

---

## Milestone 6 Clarification for v3

Milestone 6 must be read with this clarification:

The collection model does not replace authoritative task-definition libraries.

When preset-driven flow is used, selector context may resolve authoritative work-definition sources before execution tasks are instantiated.

Collections remain the deterministic workflow-state layer over instantiated task records after source resolution and instantiation occur.

Manual task entry remains valid in Milestone 6 as a direct execution-record path.

It does not replace preset-driven source resolution, but it remains a legitimate lower-automation operating mode.

---

## Milestone 7 Clarification for v3

Milestone 7 must be read with this clarification:

Planning consumes committed instantiated task records.

It must not plan directly from task-pool library definitions or other upstream source records without instantiation into the deterministic execution state first.

---

## Proposed Milestone 8 Definition for v3

### Milestone 8 — Multi-Entity Coordination

**Goal:** Stabilize deterministic relationships across authoritative work sources, Work Package context, instantiated task records, collections, planning context, and future downstream layers before introducing AI runtime behavior.

### Milestone 8 design direction

Milestone 8 is where the roadmap must make the source-of-work model fully explicit.

The canonical forward model inside Milestone 8 is:

- user-facing preset selection
- selector-context resolution
- authoritative source lookup such as task pool / profile / calendar / standards bundle
- staged selection where applicable
- task instantiation into persisted deterministic execution state
- workflow-state handling over instantiated tasks through collections
- planning from committed instantiated tasks
- later downstream runtime and output layers

This milestone does not require source libraries to share the same persisted representation as execution tasks.

It requires only that source authority, instantiation rules, and downstream handoff boundaries are explicit and deterministic.

This milestone must preserve deterministic boundaries between:

- source definition
- instantiated execution record
- ownership
- membership
- reference
- derived planning artifact

This milestone must not collapse those layers into one ambiguous task model.

### Proposed Milestone 8 checkpoint ladder

- `M8.1` Source-of-work and cross-entity relationship foundation
- `M8.2` Work Package ↔ collection relationship normalization
- `M8.3` Task ↔ collection relationship normalization
- `M8.4` Binding-context consistency controls
- `M8.5A` Cross-entity read rules
- `M8.5B` Cross-entity update rules
- `M8.5C` Cross-entity validation and failure behavior
- `M8.6` Minimal orchestration without LLM dependency
- `M8.7` Cross-entity surface consolidation
- `M8.8` Validation checkpoint
- `M8.9` Milestone UAT checkpoint
- `M8.10` Milestone closeout

### Proposed M8.1 meaning

#### `M8.1` — Source-of-work and cross-entity relationship foundation

Allowed work:

- define the canonical source-of-work path for preset-driven deterministic flow
- define preset and selector context as upstream binding seeds where applicable
- define task pools or equivalent bound libraries as authoritative work-definition sources where applicable
- define persisted `tasks` as instantiated execution records inside system state
- define the deterministic boundary between source definition and instantiated execution record
- define the manual-first fallback path as direct task instantiation without prior library resolution
- define ownership vs membership vs reference distinctions across Work Package, task, collection, and planning layers
- define how staged selection relates to later instantiated task state
- define how committed instantiated task state becomes the valid planning input boundary
- preserve deterministic identity boundaries across source records, instantiated tasks, collections, and plans

### Proposed Milestone 8 exit criteria

- the authoritative source-of-work model is explicit
- the distinction between source definitions and instantiated execution records is explicit
- cross-entity contracts are frozen
- relationship validation exists
- binding-context consistency is stable
- planning input boundaries are explicit and deterministic
- the lower-automation manual path remains compatible with the deterministic execution core

---

## Proposed Working Rule Addition

The canonical roadmap working rules should explicitly include this rule:

If forward execution depends on distinguishing source definitions from instantiated execution records, that distinction must be made explicit in the roadmap before implementation continues.

---

## Intended Post-Approval Execution Effect

Once this amendment is approved and merged into `ROADMAP_CANONICAL.md`:

- the active addendum may remain in force only until tracker correction and checkpoint re-declaration are completed
- the corrected next unfinished checkpoint should remain within Milestone 8
- the expected corrected checkpoint label should be:

`M8.1 — Source-of-work and cross-entity relationship foundation`

This preserves the current milestone boundary while correcting its meaning.

---

## Draft Approval Outcome

If approved, this draft should be merged into `ROADMAP_CANONICAL.md` and the canonical roadmap version should become:

- `ROADMAP_CANONICAL v3`
