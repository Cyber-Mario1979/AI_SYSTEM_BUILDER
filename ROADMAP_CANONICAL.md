---
doc_type: canonical_roadmap
canonical_name: ROADMAP_CANONICAL
status: ACTIVE_APPROVED
governs_execution: true
document_state_mode: state_agnostic
authority: canonical_strategic_source_of_truth
version: v4
supersedes: ROADMAP_CANONICAL v3
---

# AI Systems Builder Program (ASBP) — Canonical Roadmap v4

## Full checkpoint-ladder version

## Approval Note

This roadmap v4 is approved and authoritative once adopted in place of v3.

It is a real roadmap extension, not a wording-only refresh.

It preserves the completed deterministic foundation, the completed Milestone 11 closeout, and the established design-readiness direction while extending the canonical roadmap into the next forward phases.

It makes all of the following explicit for post-`M11.9` execution direction:

- core-engine completion comes before broader product-facing growth
- the document engine is a real governed engine layer
- export and reporting are core-engine concerns
- resolver / registry and governed data access come before broader retrieval and before UI/API
- governed library expansion must become real and structured
- the AI layer is downstream from the completed core engine
- UI/API, cloud/compute, and SaaS/productization remain later layers downstream from stable internal boundaries

---

## Why v4 exists

Roadmap v4 exists because the project completed `M11.9`, entered a governed post-M11 transition window, and needed the next forward direction to become explicit in the canonical roadmap itself.

The completed destination-alignment blueprint already made the following future direction clear:

- governed source and library expansion must become real
- document/output capability must not remain a loose side-surface
- resolver / registry must become explicit before broader retrieval and product expansion
- AI must remain downstream from governed boundaries
- UI/API must remain downstream adapter/product surfaces
- cloud/deployment direction must come later, after stable internal boundaries exist

That direction must now be represented in the roadmap as real canonical phase and milestone structure.

---

## Purpose

This roadmap is the strategic direction for ASBP.

It defines:

- phase order
- milestone order
- milestone intent
- milestone boundaries
- canonical checkpoint ladders inside milestones
- allowed work families inside milestones
- milestone exit criteria
- gate policies that govern milestone-to-milestone transition
- forward system-model direction where it materially affects later milestones

It does not function as:

- a live progress tracker
- a diary
- a session log
- a repo evidence substitute
- a giant implementation-spec encyclopedia for every local parameter

---

## Canonical Planning Contract

### 1) Direction source of truth

The roadmap is the source of truth for:

- phase order
- milestone order
- milestone intent
- milestone boundaries
- canonical checkpoint order inside each milestone
- allowed work inside each checkpoint
- milestone exit criteria
- gate policies that govern milestone-to-milestone transition

### 2) Implementation source of truth

The repository `main` branch is the source of truth for:

- what is actually implemented
- what code exists now
- what tests exist now
- what helpers, commands, and contracts are live now

### 3) Execution evidence source of truth

The progress tracker is the source of truth for:

- latest completed checkpoint
- exact next unfinished checkpoint
- latest explicitly recorded validation result
- short current-state execution evidence

### 4) State-agnostic rule

The roadmap must remain state-agnostic.

It must not contain:

- current milestone position claims
- in-progress-now claims
- latest completed checkpoint claims
- exact next-session instructions tied to temporary repo state
- temporary operating rules that are valid only for one current session window

The roadmap may define the full checkpoint ladder.
The tracker records where the project currently sits on that ladder.

### 5) Conflict rule

If roadmap, tracker, and repo disagree:

1. roadmap decides intended direction
2. repo decides actual implementation reality
3. tracker must be corrected to reflect both
4. if direction itself needs an exception or temporary overlay, use an addendum explicitly

### 6) Checkpoint-ladder rule

A session slice may only be created if it clearly maps to a declared roadmap checkpoint or an explicitly active addendum.

Every milestone in this roadmap version defines a canonical checkpoint ladder.
A checkpoint ladder may include:

- main checkpoints such as `M6.1`, `M6.2`, `M6.3`
- sub-checkpoints such as `M5.6A`, `M5.6B`, `M5.6C`
- terminal checkpoints such as:
  - validation checkpoint
  - milestone UAT checkpoint
  - milestone closeout

### 7) Local decision policy

The roadmap defines strategic direction, milestone order, checkpoint order, layer intent, and allowed work.

It does not need to pre-decide every minor implementation parameter in advance.

If a checkpoint contains local design choices that materially affect behavior, user-facing flexibility, regional assumptions, defaults, or contract shape, those choices must be discussed and fixed immediately before implementation of that checkpoint.

Examples may include:

- calendar defaults
- weekend definition
- user-amendable planning parameters
- local default policies
- bounded contract decisions inside an already-approved checkpoint

Rule:

- if the choice stays inside the checkpoint boundary, do not expand the roadmap unnecessarily
- discuss the local decision first
- then implement the checkpoint with that decision made explicitly
- if the choice changes milestone direction or checkpoint meaning, amend the roadmap instead

---

## Addendum / Overlay Policy

Addenda are temporary authorized overlays on top of the canonical roadmap.

They are allowed only when a bounded corrective or architectural situation needs explicit temporary governance.

Every roadmap addendum must include:

- purpose
- authority relationship to the canonical roadmap
- exact scope
- allowed work
- not-allowed work
- locked checkpoint if applicable
- exit condition
- explicit status

Allowed statuses:

- `ACTIVE`
- `COMPLETED_HISTORICAL`
- `ARCHIVED`

Rules:

- only addenda explicitly marked `ACTIVE` may govern execution
- addenda marked `COMPLETED_HISTORICAL` may remain in the repo for traceability, but they must not govern future sessions
- addenda that are no longer needed may be archived or removed
- if a historical addendum remains in the repo, its completed status must be obvious from the file itself or its title

---

## Delivery Style

- Daily cadence when possible
- 3–4 hours per day when possible
- Balanced but structured
- Build-first learning
- English-only working material for project artifacts
- One recommended path at a time

---

## Roadmap Design Principles

1. Deterministic layers come before AI-assisted layers.
2. Useful core data models come before orchestration.
3. Binding context comes before planning.
4. Planning comes before export/report/document generation.
5. Work structures come before AI writing contracts.
6. Validation discipline is preserved at every stage.
7. The roadmap defines structure and checkpoint order, not live session state.
8. The tracker records execution evidence; it does not decide strategic direction.
9. The repo proves implementation reality; it does not replace the roadmap.
10. Every milestone defines explicit checkpoints and exit criteria.
11. Future UI and documentation paths may be reserved early, but they must not distort the active build order.
12. From Milestone 4 onward, milestone transition requires both technical validation and milestone-level UAT evidence.
13. Work Package is the canonical parent-facing unit from the deterministic CQV-system perspective.
14. Preset/binding direction, standards bundles, and scope/intent selector logic are roadmap-level concerns, not hidden implementation assumptions.
15. The system is timestamp-aware by design even before full planning implementation is complete.
16. None of the deterministic foundation layers cancels the broader AI / UI / production-grade SaaS direction.
17. Authoritative work-definition sources must be explicitly separated from instantiated execution records.
18. Preset-driven flow may resolve work from source libraries before execution records are instantiated.
19. Persisted tasks are execution-state records and must not be treated as the only possible upstream source-of-work model.
20. Collections govern workflow-state handling over instantiated tasks.
21. Planning is downstream from committed instantiated tasks, even when the original source-of-work came from task pools or selector-bound libraries.
22. The manual-first task path remains valid as a lower-automation fallback and must stay compatible with the deterministic execution core.

---

## UAT Gate Policy (active from Milestone 4 onward)

For Milestone 4 and every milestone after it, the required transition sequence is:

1. implementation checkpoints complete for the milestone boundary being closed
2. internal validation / tests pass
3. milestone UAT checkpoint complete
4. milestone closeout complete
5. only then may the next milestone begin

Clarification:

- validation / tests confirm technical correctness
- UAT confirms milestone-level acceptance against intended user-facing or operator-facing behavior
- historical milestones before Milestone 4 do not require retrospective UAT backfill to preserve transition validity

---

## UAT Evidence Policy

From Milestone 4 onward, minimal UAT evidence must be stored in the repository under:

`docs/UAT/`

The roadmap does not require full protocol packages by default.
Minimal repo evidence is sufficient unless a richer artifact is intentionally chosen.

Minimum evidence expectation per milestone:

- milestone identifier
- short scope / coverage statement
- acceptance decision (`pass`, `conditional pass`, or `fail`)
- short rationale
- date
- reference to the latest supporting validation result when applicable
- signer / reviewer / owner field if used in the project workflow

Recommended file style:

- one Markdown summary or report per milestone, for example:
  - `docs/UAT/M4_UAT_Report.md`
  - `docs/UAT/M5_UAT_REPORT.md`

Rules:

- the tracker may reference UAT status, but the roadmap does not act as the evidence record
- full UAT packages may be stored externally if desired
- milestone transition is governed by the existence of adequate UAT evidence, not by the roadmap declaring a live current state

---

## Phase 1 — Foundations

### Milestone 1 — State CLI Tool v1

**Goal:** Build a real package-based CLI tool that can evolve into a deterministic system backbone.

#### Canonical checkpoint ladder

- `M1.1` Package structure foundation
- `M1.2` CLI entrypoint foundation
- `M1.3` Argument parsing baseline
- `M1.4` State file model introduction
- `M1.5` State init/show baseline
- `M1.6` Simple state mutation commands
- `M1.7` Validation hardening
- `M1.8` Test baseline
- `M1.9` In-milestone cleanup and coherence
- `M1.10` Milestone closeout

#### Exit criteria

- package-based CLI structure is stable
- state file init/show/update paths exist
- schema validation exists
- baseline tests exist and pass

---

### Milestone 2 — Mini Deterministic Engine

**Goal:** Build a small rule-based task engine without LLM dependency.

#### Canonical checkpoint ladder

- `M2.1` Task entity baseline
- `M2.2` Deterministic add/list/show surfaces
- `M2.3` Deterministic update/delete surfaces
- `M2.4` Status transition controls
- `M2.5` Ordering / sequencing controls
- `M2.6` Dependency model introduction
- `M2.7` Dependency validation hardening
- `M2.8` Filtering / query determinism
- `M2.9` In-milestone cleanup and coherence
- `M2.10` Milestone closeout

#### Exit criteria

- deterministic task mutations are stable
- dependency validation is stable
- filtering and ordering are deterministic
- invalid writes are rejected without corrupting state

---

## Phase 2 — Deterministic System Modeling

### Milestone 3 — Task Entity Enrichment

**Goal:** Upgrade Task from a minimal operational record into a useful system entity.

#### Canonical checkpoint ladder

- `M3.1` Title field introduction
- `M3.2` Description preservation hardening
- `M3.3` Owner field introduction
- `M3.4` Date fields introduction
- `M3.5` Duration field introduction
- `M3.6` Backward-compatibility preservation
- `M3.7` CLI acceptance path extension
- `M3.8` Validation hardening
- `M3.9` Read-surface consistency and cleanup
- `M3.10` Milestone closeout

#### Exit criteria

- enriched fields exist on the model
- enriched fields are accepted through controlled CLI paths
- backward compatibility is preserved for older persisted task records
- validation and save discipline remain intact

---

### Milestone 4 — Indexing Layer

**Goal:** Introduce explicit indexing surfaces so the system can reference and organize entities deterministically.

#### Canonical checkpoint ladder

- `M4.A` Secondary reference foundation
- `M4.B` Reference resolution expansion
- `M4.C` Safety and validation controls
- `M4.D` Secondary key lifecycle controls
- `M4.E` Index-aware list and filter surfaces
- `M4.F` Read-surface consolidation
- `M4.G` Milestone closeout and anti-fragmentation
- `M4.H` Validation checkpoint
- `M4.I` Milestone UAT checkpoint
- `M4.J` Milestone closeout

#### M4.A — Secondary reference foundation

Allowed work:

- secondary key introduction
- normalization rules
- exact identity vs secondary reference separation
- read lookup fallback from `task_id` to normalized `task_key`

#### M4.B — Reference resolution expansion

Allowed work:

- extend task reference resolution into existing mutation paths
- extend reference resolution into dependency inputs
- keep persisted storage identity on `task_id`

#### M4.C — Safety and validation controls

Allowed work:

- ambiguous reference detection
- reserved namespace protection
- persisted-load validation for indexing state
- deterministic no-guess failure behavior

#### M4.D — Secondary key lifecycle controls

Allowed work:

- set/update secondary key for existing tasks
- clear/remove secondary key for existing tasks
- preserve current lookup behavior after mutation or clear

#### M4.E — Index-aware list and filter surfaces

Allowed work:

- list visibility of `task_key`
- presence filters
- exact-key filters
- exact task-reference filters
- dependency/dependent reference filters
- deterministic AND logic across filters

#### M4.F — Read-surface consolidation

Allowed work:

- shared helper consolidation for list filters
- shared helper consolidation for reference views
- shared helper consolidation for task-read payload preparation
- shared helper consolidation for reference-visibility option preparation
- internal refactors that preserve existing CLI contracts exactly

#### M4.G — Milestone closeout and anti-fragmentation

Allowed work:

- consolidate indexing helper architecture
- remove avoidable duplication inside read/list/indexing flows
- verify milestone-level coherence
- define what belongs to Milestone 4 versus what must wait for Milestone 5
- freeze the indexing contract for downstream entity expansion

#### Not allowed inside Milestone 4

- Work Package entity introduction
- task-to-work-package association rules
- collection structures
- orchestration behaviors outside indexing/read surfaces
- AI runtime behaviors
- UI implementation

#### Exit criteria

- identity vs reference separation is stable
- all current task read/mutation/filter surfaces follow one deterministic reference contract
- ambiguous and invalid reference states fail deterministically
- no critical indexing behavior depends on duplicated helper logic scattered across CLI paths
- the boundary between Indexing Layer and Work Package Model is explicitly frozen

---

### Milestone 5 — Work Package Model

**Goal:** Introduce Work Package as a first-class deterministic entity that can hold and organize work.

#### Canonical checkpoint ladder

- `M5.1` Work package identity foundation
- `M5.2` Work package schema foundation
- `M5.3` Work package persistence and validated load/save
- `M5.4A` Work package create surface
- `M5.4B` Work package read surface
- `M5.4C` Work package list / visibility surface
- `M5.5` Work package update surface
- `M5.6A` Associate task to work package
- `M5.6B` Initial membership rules
- `M5.6C` Task-to-work-package validation and failure behavior
- `M5.7` Work package read/write surface consolidation
- `M5.8` Validation checkpoint
- `M5.9` Milestone UAT checkpoint
- `M5.10` Milestone closeout

#### Allowed work mapping

##### `M5.1` — Work package identity foundation

Allowed work:

- introduce deterministic WP identifier model
- define identity uniqueness rules
- define canonical persisted identity field
- preserve separation from task indexing identity

##### `M5.2` — Work package schema foundation

Allowed work:

- introduce `WorkPackageModel`
- define required and optional WP fields
- define schema-level validation rules
- define backward-compatible defaults if needed

##### `M5.3` — Work package persistence and validated load/save

Allowed work:

- introduce WP persistence store
- validated load/save paths
- persisted structure normalization
- error handling for missing/invalid WP persistence state

##### `M5.4A` — Work package create surface

Allowed work:

- create CLI/API surface for WP creation
- deterministic creation rules
- duplicate-identity rejection
- creation response contract

##### `M5.4B` — Work package read surface

Allowed work:

- single-WP read/show surface
- deterministic read failure behavior
- canonical display payload rules

##### `M5.4C` — Work package list / visibility surface

Allowed work:

- WP list surface
- deterministic list ordering
- visibility of key WP fields
- optional visibility refinements that do not change milestone boundary

##### `M5.5` — Work package update surface

Allowed work:

- update allowed mutable WP fields
- reject immutable identity mutation unless explicitly supported
- deterministic update validation
- update response contract

##### `M5.6A` — Associate task to work package

Allowed work:

- associate task to WP
- deterministic attach behavior
- reject invalid attaches deterministically

##### `M5.6B` — Initial membership rules

Allowed work:

- define initial task membership constraints
- define allowed one-to-one or one-to-many membership policy if applicable
- define baseline reassignment expectations before detach/reassignment hardening
- keep membership rules deterministic and explicit

##### `M5.6C` — Task-to-work-package validation and failure behavior

Allowed work:

- membership validation
- duplicate or conflicting membership rejection
- dangling-reference prevention
- persisted-load validation for task/WP relationship state

##### `M5.7` — Work package read/write surface consolidation

Allowed work:

- reduce avoidable duplication inside WP handlers/helpers
- preserve existing contracts
- improve internal coherence without expanding milestone boundary

##### `M5.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M5.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 5 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M5.10` — Milestone closeout

Allowed work:

- freeze M5 boundary
- confirm what belongs to M6 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- WP exists as a validated first-class entity
- tasks can be associated to WP deterministically
- WP behavior is clearly separate from task indexing behavior

---

### Milestone 6 — Binding Context and Task Collections

**Goal:** Introduce deterministic selector context and bound collections so Work Package-centered CQV flow can move beyond isolated task attachment.

#### Canonical checkpoint ladder

- `M6.1` Collection identity foundation
- `M6.2` Collection schema foundation
- `M6.3` Collection persistence and validated load/save
- `M6.4A` Collection create surface
- `M6.4B` Collection read surface
- `M6.4C` Collection list / visibility surface
- `M6.5` Collection update surface
- `M6.6A` Task-to-collection membership attach rules
- `M6.6B` Initial collection membership rules
- `M6.6C` Collection membership validation and failure behavior
- `M6.7A` Selector context foundation
- `M6.7B` Preset-first binding direction
- `M6.7C` Standards-bundle binding direction
- `M6.7D` Scope / intent selector direction
- `M6.8` Validation checkpoint
- `M6.9` Milestone UAT checkpoint
- `M6.10` Milestone closeout

#### Design direction for Milestone 6

Milestone 6 should be interpreted broadly, not as simple passive task grouping only.

The collection model should support at least these conceptual states:

- source task pool
- staged task selection
- committed task selection
- iterative refinement after commitment when needed

Selector/binding direction in this milestone should make explicit that downstream deterministic bindings are resolved from context, not from Work Package type alone.

Clarification for v3:

The collection model does not replace authoritative task-definition libraries.

When preset-driven flow is used, selector context may resolve authoritative work-definition sources before execution tasks are instantiated.

Collections remain the deterministic workflow-state layer over instantiated task records after source resolution and instantiation occur.

Manual task entry remains valid in Milestone 6 as a direct execution-record path.

It does not replace preset-driven source resolution, but it remains a legitimate lower-automation operating mode.

#### Allowed work mapping

##### `M6.1` — Collection identity foundation

Allowed work:

- introduce deterministic collection identifier model
- define identity uniqueness rules
- define canonical persisted identity field
- preserve separation from task and work-package identity

##### `M6.2` — Collection schema foundation

Allowed work:

- introduce collection model
- define required and optional collection fields
- define schema-level validation rules
- define defaults if needed

##### `M6.3` — Collection persistence and validated load/save

Allowed work:

- introduce collection persistence store
- validated load/save paths
- normalized persisted structure
- missing/invalid persistence-state handling

##### `M6.4A` — Collection create surface

Allowed work:

- create CLI/API surface for collection creation
- duplicate-identity rejection
- deterministic creation response contract

##### `M6.4B` — Collection read surface

Allowed work:

- single-collection read/show surface
- deterministic read failure behavior
- canonical display payload rules

##### `M6.4C` — Collection list / visibility surface

Allowed work:

- collection list surface
- deterministic list ordering
- key field visibility
- bounded visibility refinements inside milestone scope

##### `M6.5` — Collection update surface

Allowed work:

- update allowed mutable collection fields
- deterministic update validation
- reject disallowed identity mutation unless explicitly supported

##### `M6.6A` — Task-to-collection membership attach rules

Allowed work:

- attach task to collection
- deterministic attach behavior
- reject invalid attaches deterministically

##### `M6.6B` — Initial collection membership rules

Allowed work:

- define baseline collection membership constraints
- define staged vs committed membership expectations where applicable
- define baseline reassignment or removal expectations before hardening

##### `M6.6C` — Collection membership validation and failure behavior

Allowed work:

- duplicate membership rejection
- conflicting membership-state rejection where applicable
- dangling-reference prevention
- persisted-load validation for task/collection relationship state

##### `M6.7A` — Selector context foundation

Allowed work:

- define selector context fields required for deterministic task-pool selection
- clarify that selector inputs go beyond Work Package type alone
- preserve deterministic boundaries between selector context and later planning behavior

##### `M6.7B` — Preset-first binding direction

Allowed work:

- define preset-first deterministic entry as the preferred future path
- clarify that manual Work Package creation is a lower-automation variant of the same overall flow
- define preset as a binding seed rather than only a template

##### `M6.7C` — Standards-bundle binding direction

Allowed work:

- define standards bundle as part of deterministic bound context
- define CQV Core as default baseline bundle
- define Cleanroom/HVAC and Automation bundles as add-ons when relevant
- keep bundle binding direction separate from final documentation generation

##### `M6.7D` — Scope / intent selector direction

Allowed work:

- define scope / intent as a first-class selector input
- clarify that task determination depends on why the object is being touched, not only what the object is
- preserve deterministic selector behavior across scopes such as end-to-end, qualification-only, commissioning-only, periodic verification, and post-change scenarios

##### `M6.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M6.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 6 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M6.10` — Milestone closeout

Allowed work:

- freeze M6 boundary
- confirm what belongs to M7 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- collection entities are explicit
- selector and binding direction is explicit
- membership rules are deterministic
- grouping behavior is validated and non-ambiguous

---

### Milestone 7 — Planning Layer

**Goal:** Introduce explicit deterministic planning behavior above committed task collections and before export/document generation.

#### Canonical checkpoint ladder

- `M7.1` Planning entity foundation
- `M7.2` Planning basis attachment rules
- `M7.3` Timestamp-aware schedule foundation
- `M7.4` Calendar model introduction
- `M7.5A` Plan generation baseline
- `M7.5B` Plan review / visibility surfaces
- `M7.5C` Plan commit behavior
- `M7.6` Planning validation and failure behavior
- `M7.7` Planning surface consolidation
- `M7.8` Validation checkpoint
- `M7.9` Milestone UAT checkpoint
- `M7.10` Milestone closeout

#### Design direction for Milestone 7

Planning is a first-class future layer.
It sits after committed task selection and before export / reporting / documentation.

Planning should use:

- user-provided start date
- durations from planning basis
- dependencies from task pool / committed task set
- timestamp-aware sequencing behavior

The roadmap does not pre-decide all local calendar parameters in advance.
Local planning decisions such as weekend defaults or user-amendable weekend policies should be discussed immediately before the relevant checkpoint implementation under the local decision policy.

Clarification for v3:

Planning consumes committed instantiated task records.

It must not plan directly from task-pool library definitions or other upstream source records without instantiation into the deterministic execution state first.

#### Allowed work mapping

##### `M7.1` — Planning entity foundation

Allowed work:

- introduce planning entity/model foundation
- define planning identity/state concepts
- preserve separation from task, Work Package, and collection identity

##### `M7.2` — Planning basis attachment rules

Allowed work:

- define how planning basis attaches to bound context
- define duration-source expectations
- preserve deterministic separation between planning basis and generated plan state

##### `M7.3` — Timestamp-aware schedule foundation

Allowed work:

- define timestamp-aware planning direction
- define start-date semantics
- define derived sequencing/finish expectations at a foundational level

##### `M7.4` — Calendar model introduction

Allowed work:

- define calendar model expectations for planning
- define workday/workweek/workmonth model boundaries
- define how local calendar decisions are handled without bloating the roadmap

##### `M7.5A` — Plan generation baseline

Allowed work:

- generate baseline plan from committed tasks + planning basis + start date
- preserve deterministic handling of durations and dependencies
- prevent hidden free-form planning behavior

##### `M7.5B` — Plan review / visibility surfaces

Allowed work:

- show plan state and derived schedule outputs
- define bounded review surfaces
- preserve separation between draft/generated plan and committed plan

##### `M7.5C` — Plan commit behavior

Allowed work:

- commit accepted plan state
- define deterministic commit expectations
- define post-commit planning state boundaries

##### `M7.6` — Planning validation and failure behavior

Allowed work:

- reject invalid plan-generation states deterministically
- define bounded failure behavior
- preserve no-guess handling of inconsistent planning inputs

##### `M7.7` — Planning surface consolidation

Allowed work:

- reduce avoidable duplication across planning handlers/helpers
- preserve current contracts
- improve internal coherence without scope expansion

##### `M7.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M7.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 7 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M7.10` — Milestone closeout

Allowed work:

- freeze M7 boundary
- confirm what belongs to M8 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- planning is explicit as a system layer
- timestamp-aware planning behavior is introduced deterministically
- generated and committed plan boundaries are clear

---

## Phase 3 — AI Runtime Architecture

### Milestone 8 — Multi-Entity Coordination

**Goal:** Stabilize deterministic relationships across authoritative work sources, Work Package context, instantiated task records, collections, planning context, and future downstream layers before introducing AI runtime behavior.

#### Design direction for Milestone 8

Milestone 8 is where the roadmap must make the source-of-work model fully explicit.

The canonical forward model is:

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

#### Canonical checkpoint ladder

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

#### Allowed work mapping

##### `M8.1` — Source-of-work and cross-entity relationship foundation

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

##### `M8.2` — Work Package ↔ collection relationship normalization

Allowed work:

- normalize Work Package / collection relationship expectations
- remove ambiguous relationship states
- define canonical persisted relationship rules

##### `M8.3` — Task ↔ collection relationship normalization

Allowed work:

- normalize task/collection relationship expectations
- preserve deterministic grouping rules
- define canonical persisted relationship rules

##### `M8.4` — Binding-context consistency controls

Allowed work:

- ensure selector, standards bundle, calendar, and planning-basis context remain coherent
- reject mixed ambiguous bound states
- preserve deterministic relation between bound context and downstream planning

##### `M8.5A` — Cross-entity read rules

Allowed work:

- define deterministic cross-entity read surfaces
- define canonical read payload expectations
- reject ambiguous reads deterministically

##### `M8.5B` — Cross-entity update rules

Allowed work:

- define deterministic cross-entity mutation/update behavior
- preserve safe write ordering
- reject invalid cross-entity updates deterministically

##### `M8.5C` — Cross-entity validation and failure behavior

Allowed work:

- relationship validation before save
- dangling or conflicting reference rejection
- persisted-load validation for cross-entity state
- deterministic no-guess failure behavior

##### `M8.6` — Minimal orchestration without LLM dependency

Allowed work:

- minimal orchestration rules that remain deterministic
- no AI runtime behavior
- no free-form agentic expansion

##### `M8.7` — Cross-entity surface consolidation

Allowed work:

- reduce avoidable duplication across cross-entity handlers/helpers
- preserve current contracts
- improve internal coherence without scope expansion

##### `M8.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M8.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 8 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M8.10` — Milestone closeout

Allowed work:

- freeze M8 boundary
- confirm what belongs to M9 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- the authoritative source-of-work model is explicit
- the distinction between source definitions and instantiated execution records is explicit
- cross-entity contracts are frozen
- relationship validation exists
- binding-context consistency is stable
- planning input boundaries are explicit and deterministic
- the lower-automation manual path remains compatible with the deterministic execution core

---

### Milestone 9 — Hybrid Runtime

**Goal:** Combine deterministic core with a controlled AI writing layer.

#### Canonical checkpoint ladder

- `M9.1` Runtime boundary definition
- `M9.2` Prompt contract foundation
- `M9.3` Deterministic-to-LLM handoff structure
- `M9.4` Validation loop foundation
- `M9.5` Retry / fail behavior rules
- `M9.6A` Controlled generation surface
- `M9.6B` Output acceptance rules
- `M9.6C` Failure recovery and retry discipline
- `M9.7` Runtime surface consolidation
- `M9.8` Validation checkpoint
- `M9.9` Milestone UAT checkpoint
- `M9.10` Milestone closeout

#### Allowed work mapping

##### `M9.1` — Runtime boundary definition

Allowed work:

- define deterministic core vs LLM boundary
- define what the model may and may not decide
- preserve deterministic logic outside the model

##### `M9.2` — Prompt contract foundation

Allowed work:

- define bounded prompt contracts
- define required inputs and expected outputs
- define prohibited free-form drift at the runtime boundary

##### `M9.3` — Deterministic-to-LLM handoff structure

Allowed work:

- structure validated deterministic inputs for generation
- preserve traceable handoff discipline
- keep structured facts separate from prose-generation instructions

##### `M9.4` — Validation loop foundation

Allowed work:

- validate generated output before acceptance
- reject malformed or contract-breaking output
- preserve deterministic acceptance rules

##### `M9.5` — Retry / fail behavior rules

Allowed work:

- define bounded retry behavior
- define fail-closed behavior where appropriate
- define deterministic fallback expectations

##### `M9.6A` — Controlled generation surface

Allowed work:

- introduce bounded generation surfaces
- keep generation scope explicit
- prevent unbounded model-led behavior

##### `M9.6B` — Output acceptance rules

Allowed work:

- define acceptance checks for generated output
- separate accepted output from rejected output paths
- preserve system facts vs prose separation

##### `M9.6C` — Failure recovery and retry discipline

Allowed work:

- define recovery behavior after validation failure
- define retry limits and retry structure
- preserve deterministic handling of repeated failure

##### `M9.7` — Runtime surface consolidation

Allowed work:

- reduce avoidable duplication inside runtime handlers/helpers
- preserve existing generation contracts
- improve internal coherence without milestone expansion

##### `M9.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M9.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 9 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M9.10` — Milestone closeout

Allowed work:

- freeze M9 boundary
- confirm what belongs to M10 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- deterministic core and AI writing paths are cleanly separated
- bounded generation contracts exist
- validation loop exists before accepting AI output

---

### Milestone 10 — Runtime-Orchestrated Outputs

**Goal:** Use the hybrid runtime to generate useful outputs from deterministic state without collapsing system discipline.

#### Canonical checkpoint ladder

- `M10.1` Output target definition
- `M10.2` Output contract foundation
- `M10.3` Deterministic input-to-output mapping
- `M10.4` Validation before acceptance
- `M10.5` Regeneration / retry structure
- `M10.6A` Output family expansion
- `M10.6B` Output consistency controls
- `M10.6C` Output failure handling
- `M10.7` Runtime-output consolidation
- `M10.8` Validation checkpoint
- `M10.9` Milestone UAT checkpoint
- `M10.10` Milestone closeout

#### Allowed work mapping

##### `M10.1` — Output target definition

Allowed work:

- define bounded output targets
- define output families within milestone scope
- keep target boundaries explicit

##### `M10.2` — Output contract foundation

Allowed work:

- define required output contract fields
- define acceptance shape per output family
- define prohibited contract drift

##### `M10.3` — Deterministic input-to-output mapping

Allowed work:

- define controlled mapping from validated state to output generation
- preserve traceable generation flow
- prevent ambiguous source-of-truth blending

##### `M10.4` — Validation before acceptance

Allowed work:

- validate generated outputs before acceptance
- reject contract-breaking outputs deterministically
- preserve safe acceptance discipline

##### `M10.5` — Regeneration / retry structure

Allowed work:

- define regeneration behavior
- define bounded retry structure
- preserve deterministic retry rules

##### `M10.6A` — Output family expansion

Allowed work:

- expand bounded output families inside the milestone boundary
- preserve explicit target definitions
- avoid unbounded output sprawl

##### `M10.6B` — Output consistency controls

Allowed work:

- preserve consistency across output families
- align output formatting/contract behavior where applicable
- reject internally inconsistent output states deterministically

##### `M10.6C` — Output failure handling

Allowed work:

- define deterministic handling of output-generation failures
- preserve clear accepted vs rejected vs retry-needed states
- prevent silent bad-output acceptance

##### `M10.7` — Runtime-output consolidation

Allowed work:

- reduce avoidable duplication inside output-generation handlers/helpers
- preserve current contracts
- improve internal coherence without scope expansion

##### `M10.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M10.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 10 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M10.10` — Milestone closeout

Allowed work:

- freeze M10 boundary
- confirm what belongs to M11 and beyond
- finalize milestone closeout notes if used

#### Exit criteria

- generation targets are explicit
- output validation exists
- runtime preserves system facts vs prose separation

---

## Phase 4 — Professionalization

### Milestone 11 — Production-Grade Micro AI System

**Goal:** Build a small but serious end-to-end AI system.

#### Canonical checkpoint ladder

- `M11.1` Production structure baseline
- `M11.2` Evaluation and regression baseline
- `M11.3` Versioning discipline
- `M11.4` Retrieval architecture basics
- `M11.5A` Runtime control hardening
- `M11.5B` Failure-discipline hardening
- `M11.5C` Maintainability hardening
- `M11.6` Architecture cleanup and consolidation
- `M11.7` Validation checkpoint
- `M11.8` Milestone UAT checkpoint
- `M11.9` Milestone closeout

#### Allowed work mapping

##### `M11.1` — Production structure baseline

Allowed work:

- define production-grade repository structure expectations
- define stable module boundaries
- define baseline maintainability rules

##### `M11.2` — Evaluation and regression baseline

Allowed work:

- define evaluation mindset and baseline regression checks
- define what must be revalidated after changes
- preserve deterministic release-discipline expectations

##### `M11.3` — Versioning discipline

Allowed work:

- define versioning rules
- define milestone/runtime version update expectations
- preserve explicit release-state signaling

##### `M11.4` — Retrieval architecture basics

Allowed work:

- define bounded retrieval architecture basics
- preserve separation between retrieval surfaces and generation surfaces
- avoid uncontrolled expansion beyond milestone scope

##### `M11.5A` — Runtime control hardening

Allowed work:

- strengthen runtime control behavior
- strengthen acceptance/rejection boundaries
- preserve bounded system behavior under normal conditions

##### `M11.5B` — Failure-discipline hardening

Allowed work:

- strengthen deterministic handling of failures
- prevent silent degradation
- preserve safe fail behavior

##### `M11.5C` — Maintainability hardening

Allowed work:

- strengthen maintainability-oriented structure
- reduce avoidable operational ambiguity
- improve clarity without milestone expansion

##### `M11.6` — Architecture cleanup and consolidation

Allowed work:

- reduce avoidable duplication across mature system surfaces
- preserve current contracts
- improve professionalization coherence without changing roadmap phase order

##### `M11.7` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M11.8` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 11 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M11.9` — Milestone closeout

Allowed work:

- freeze M11 boundary
- finalize milestone closeout notes if used
- confirm post-roadmap extension readiness if applicable

#### Exit criteria

- regression discipline exists
- maintainable architecture is visible in the repo
- evaluation and runtime control practices are established

---

## Post-M11 transition note

Immediately after `M11.9`, execution may still be temporarily governed by an active roadmap addendum when a bounded transition gate is required.

At v4 adoption time, the active post-M11 transition overlay is:

- `ROADMAP_ADDENDUM_07_POST_M11_TRANSITION_AND_ROADMAP_EXTENSION_GATE.md`

Rule:

- if an active addendum governs a bounded transition window, execution follows the canonical roadmap plus that active overlay
- once the active transition addendum completes, normal execution returns fully to the canonical roadmap ladder and the tracker’s explicit next checkpoint

---

## Phase 5 — Core Engine Completion

### Phase goal

Finish the inner engine fully before broader AI/UI/cloud/productization expansion.

The enforced order inside this phase is:

1. governed document engine
2. export and reporting engine
3. governed data / resolver / registry layer
4. governed library expansion
5. orchestration / retrieval / service hardening over the expanded engine

This phase must close the remaining “basic engine” work before broader product-facing growth.

---

### Milestone 12 — Governed Document Engine

**Goal:** Turn document generation into a real governed engine layer with template retrieval, DCF intake, controlled AI authoring, and document lifecycle ↔ workflow-state integration.

#### Canonical checkpoint ladder

- `M12.1` Template retrieval and template governance foundation
- `M12.2` Document request/input contract foundation
- `M12.3` DCF intake, extraction, and structured normalization
- `M12.4` Controlled AI authoring modes and bounded invention policy
- `M12.5` Standards, language, and evidence guardrails
- `M12.6` Document artifact lifecycle model
- `M12.7` Document lifecycle ↔ task/workflow-state integration
- `M12.8` Validation checkpoint
- `M12.9` Milestone UAT checkpoint
- `M12.10` Milestone closeout

#### Allowed work mapping

##### `M12.1` — Template retrieval and template governance foundation

Allowed work:

- define template identity and artifact-kind rules
- define template retrieval as a governed retrieval family
- define version-pinned template selection rules
- define authoritative template surfaces versus supporting/non-authoritative content
- support canonical governed families such as:
  - URS
  - DCF
  - protocol families
  - report families
  - other governed document artifacts

##### `M12.2` — Document request/input contract foundation

Allowed work:

- define document job/request model
- define document input contract
- define document output contract
- define document-family-specific required inputs
- define how document generation attaches to approved core/service/runtime boundaries
- preserve separation between execution truth, template truth, and generated language output

##### `M12.3` — DCF intake, extraction, and structured normalization

Allowed work:

- retrieve DCF templates through governed lookup
- ingest user-filled DCF artifacts
- extract structured fields from DCF content
- normalize extracted data into bounded document-input structures
- preserve traceability between:
  - raw uploaded user content
  - extracted structured data
  - downstream generated document output
- define missing/ambiguous data behavior

##### `M12.4` — Controlled AI authoring modes and bounded invention policy

Allowed work:

- define AI-assisted authoring as a bounded downstream layer inside the document engine
- define controlled generation modes such as:
  - strong-structured-input fill
  - partial-input bounded completion
  - minimal-input scaffold generation
- allow bounded invention only when:
  - governed by guardrails
  - governed by standards
  - bounded by document-family rules
- prevent unrestricted free drafting from becoming execution truth

##### `M12.5` — Standards, language, and evidence guardrails

Allowed work:

- define document-family structure rules
- define standards-aware phrasing rules
- define assumption-labeling policy
- define placeholder policy
- define evidence-versus-inference separation
- define prohibited language patterns where needed
- define section-level authoring constraints
- define detail-level consistency rules across document families

##### `M12.6` — Document artifact lifecycle model

Allowed work:

- define document artifact states such as:
  - draft
  - in_review
  - approved
  - finalized
  - superseded
  - reopened if explicitly needed
- define lifecycle transition rules
- define family-specific lifecycle constraints where needed
- preserve deterministic lifecycle truth independent of AI phrasing behavior

##### `M12.7` — Document lifecycle ↔ task/workflow-state integration

Allowed work:

- define task ↔ document binding rules
- define which tasks require which document artifacts
- define whether closure requires one or multiple finalized document obligations
- define how document-finalization affects task-state progression
- define reopen/supersede effects on dependent task/workflow state where applicable
- define whether document state also affects higher-level readiness / reporting / dashboard signals
- preserve deterministic state propagation through approved orchestration/service boundaries

##### `M12.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M12.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 12 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M12.10` — Milestone closeout

Allowed work:

- freeze the governed document-engine boundary
- confirm what belongs to later export/data/library/AI work
- finalize milestone closeout notes if used

#### Exit criteria

- template retrieval is governed and version-aware
- document request/input/output contracts are explicit
- DCF intake and extraction are explicit
- AI-assisted authoring is bounded and standards-governed
- documents have explicit lifecycle truth
- document lifecycle can affect task/workflow state deterministically
- validation and UAT pass

---

### Milestone 13 — Export and Reporting Engine

**Goal:** Turn exports into a real engine layer with explicit export families, contracts, rendering rules, and reporting depth expectations.

#### Canonical checkpoint ladder

- `M13.1` Export identity and contract foundation
- `M13.2` Spreadsheet and operational export surfaces
- `M13.3` Gantt and planning visualization exports
- `M13.4` Dashboard and status summary exports
- `M13.5` Reporting export family and detail-level discipline
- `M13.6` Export invocation and validation behavior
- `M13.7` Validation checkpoint
- `M13.8` Milestone UAT checkpoint
- `M13.9` Milestone closeout

#### Allowed work mapping

##### `M13.1` — Export identity and contract foundation

Allowed work:

- define canonical export families
- define export request contract
- define export payload contract
- define export output contract
- define export identity/versioning expectations
- define export-family boundaries separate from later UI/API delivery surfaces

##### `M13.2` — Spreadsheet and operational export surfaces

Allowed work:

- define spreadsheet export families
- define column contracts
- define row granularity
- define value/formula policy
- define operational drop-ready export shapes such as:
  - Excel-ready
  - CSV-ready
  - Microsoft Project drop-ready where approved
- keep operational exports bounded and deterministic

##### `M13.3` — Gantt and planning visualization exports

Allowed work:

- define Gantt/planning visualization export families
- define consumed input data
- define grouping behavior
- define dependency visibility rules
- define planning/status visibility rules
- define export rendering expectations at a governed contract level

##### `M13.4` — Dashboard and status summary exports

Allowed work:

- define dashboard export family
- define audience-facing summary surfaces
- define KPI/status/progress visibility boundaries
- define snapshot/report/dashboard distinctions
- preserve deterministic input-to-output contract expectations

##### `M13.5` — Reporting export family and detail-level discipline

Allowed work:

- define reporting export families
- define report structure expectations
- define evidence-versus-summary rules
- define narrative depth expectations
- define detail-level discipline that later phases must inherit
- prevent later shallow reporting behavior after deep Phase 5 foundations

##### `M13.6` — Export invocation and validation behavior

Allowed work:

- define export invocation through approved service/runtime boundaries
- define bounded failure behavior
- define export validation rules
- define incomplete-input handling
- define acceptance rules for generated export artifacts

##### `M13.7` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M13.8` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 13 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M13.9` — Milestone closeout

Allowed work:

- freeze export/reporting engine boundary
- confirm what belongs to later AI/UI/product-facing work
- finalize milestone closeout notes if used

#### Exit criteria

- export families are explicit
- spreadsheet, Gantt, dashboard, and reporting outputs are bounded
- reporting detail expectations are explicit
- export validation and failure behavior are explicit
- validation and UAT pass

---

### Milestone 14 — Resolver / Registry and Governed Data Layer

**Goal:** Establish the first true post-core executable boundary for governed asset resolution and governed data access.

#### Canonical checkpoint ladder

- `M14.1` Resolver / registry boundary foundation
- `M14.2` Governed asset identity and version-pinned lookup
- `M14.3` Calendar and planning-basis resolution family
- `M14.4` Authored-source versus deployment-compiled separation
- `M14.5` Governed retrieval versus support-retrieval boundary
- `M14.6` Validation checkpoint
- `M14.7` Milestone UAT checkpoint
- `M14.8` Milestone closeout

#### Allowed work mapping

##### `M14.1` — Resolver / registry boundary foundation

Allowed work:

- define explicit resolver/registry access boundary
- define approved asset-access entry points
- define how resolver/registry attaches above deterministic state/core truth and below broader AI/product surfaces
- preserve CLI-as-adapter governance

##### `M14.2` — Governed asset identity and version-pinned lookup

Allowed work:

- define canonical governed asset identities
- define version-pinned lookup rules
- define governed lookup for assets such as:
  - templates
  - presets
  - task pools
  - standards bundles
  - profiles where applicable
  - mapping metadata
- preserve deterministic lookup behavior

##### `M14.3` — Calendar and planning-basis resolution family

Allowed work:

- define calendar family resolution
- define planning-basis data-resolution expectations
- define new calendar family addition rules where needed
- preserve separation between resolved calendar truth and later planning/rendering outputs

##### `M14.4` — Authored-source versus deployment-compiled separation

Allowed work:

- define authored-source truth versus deployment-compiled lookup surfaces
- preserve source-editability versus compiled-runtime lookup roles
- define allowed compiled lookup families
- prevent compiled lookup from becoming source authority

##### `M14.5` — Governed retrieval versus support-retrieval boundary

Allowed work:

- define structural distinction between governed deterministic retrieval and broader support/probabilistic retrieval
- prevent support retrieval from redefining source authority
- define allowed source-role behavior at the boundary
- preserve future compatibility with later AI retrieval usage rules

##### `M14.6` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M14.7` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 14 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M14.8` — Milestone closeout

Allowed work:

- freeze governed resolver/registry and data-layer boundary
- confirm what belongs to later library expansion and AI consumption
- finalize milestone closeout notes if used

#### Exit criteria

- resolver/registry is explicit
- governed asset lookup is explicit and version-aware
- calendar/planning-basis resolution family is explicit
- authored-source versus compiled separation is explicit
- governed versus support retrieval roles are explicit
- validation and UAT pass

---

### Milestone 15 — Governed Library Expansion and Engine Hardening

**Goal:** Audit the current governed libraries, define the expansion framework, expand the needed families, and harden orchestration/service behavior over the expanded engine.

#### Canonical checkpoint ladder

- `M15.1` Library gap analysis and coverage audit
- `M15.2` Coverage-pack expansion framework
- `M15.3` Preset / selector library expansion
- `M15.4` Task-pool expansion
- `M15.5` Calendar / standards / profile / mapping expansion
- `M15.6` Library validation, freeze, and release discipline
- `M15.7` Orchestration / service hardening on expanded governed assets
- `M15.8` Validation checkpoint
- `M15.9` Milestone UAT checkpoint
- `M15.10` Milestone closeout

#### Allowed work mapping

##### `M15.1` — Library gap analysis and coverage audit

Allowed work:

- audit current preset coverage
- audit current task-pool coverage
- audit current calendar coverage
- audit current standards-bundle coverage
- audit profile and mapping coverage where applicable
- identify:
  - foundation gaps
  - content gaps
  - taxonomy gaps
  - validation gaps
  - deployment-compiled gaps
- produce a real governed expansion map

##### `M15.2` — Coverage-pack expansion framework

Allowed work:

- define bounded coverage-pack model
- define expansion unit expectations
- define how multiple governed artifact families coordinate inside one pack
- align expansion framework with library taxonomy and authored-source / compiled separation rules

##### `M15.3` — Preset / selector library expansion

Allowed work:

- add/expand presets and selector definitions
- preserve selector-context truth as a first-class binding seed
- avoid hard-coded one-family shortcuts disguised as general design

##### `M15.4` — Task-pool expansion

Allowed work:

- add/expand governed task-pool families
- preserve explicit source-definition identity
- preserve deterministic instantiation and downstream workflow compatibility

##### `M15.5` — Calendar / standards / profile / mapping expansion

Allowed work:

- add/expand calendar families
- add/expand standards bundles
- add/expand profiles where needed
- add/expand mapping metadata needed for deterministic resolution
- preserve coordinated governed growth across related artifact families

##### `M15.6` — Library validation, freeze, and release discipline

Allowed work:

- define structural validity rules
- define taxonomy/identity validity rules
- define cross-library linkage validity rules
- define compiled lookup consistency rules
- define freeze/release acceptance expectations for governed coverage packs

##### `M15.7` — Orchestration / service hardening on expanded governed assets

Allowed work:

- harden orchestration/service behavior over expanded governed assets
- preserve mutation ordering and preflight validation through approved boundaries
- preserve document/export invocation through approved boundaries
- preserve governed deterministic retrieval versus support retrieval separation
- prevent adapter leakage and free-form runtime mixing

##### `M15.8` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M15.9` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 15 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M15.10` — Milestone closeout

Allowed work:

- freeze the full Core Engine Completion boundary
- confirm what belongs to Phase 6 AI-layer work and what must remain later
- finalize milestone closeout notes if used

#### Exit criteria

- real gap analysis exists
- expansion framework exists
- presets, task pools, calendars, standards, and related governed assets are expanded in a structured way
- library validation/freeze discipline exists
- orchestration/service behavior is hardened on top of expanded governed assets
- Phase 5 closes on a stable core-engine boundary
- validation and UAT pass

---

## Phase 5 exit criteria

Phase 5 is complete only when all of the following are true:

- governed document engine is explicit
- document lifecycle and task/workflow integration are explicit
- export/reporting engine is explicit
- governed resolver/registry and governed data layer are explicit
- library gap analysis and structured expansion are explicit
- orchestration/service hardening is complete on top of the expanded engine
- Phase 5 validation passes
- Phase 5 UAT passes
- Phase 5 closeout is complete

---

## Phase 6 — AI Layer

### Phase goal

Build the AI layer only after the core engine, document/export engine, governed data layer, and governed libraries are stable enough.

AI in this phase must remain downstream from deterministic truth, governed retrieval, document/export contracts, and runtime boundaries.

---

### Milestone 16 — AI Runtime for Governed Document and Reporting Workflows

**Goal:** Turn bounded AI assistance into a governed runtime layer over the completed document/export/core-engine boundary.

#### Canonical checkpoint ladder

- `M16.1` AI runtime boundary for document/reporting jobs
- `M16.2` Context packaging from governed engine inputs
- `M16.3` Controlled generation modes for document/reporting families
- `M16.4` Output acceptance, bounded retry, and fallback behavior
- `M16.5` Validation checkpoint
- `M16.6` Milestone UAT checkpoint
- `M16.7` Milestone closeout

#### Allowed work mapping

##### `M16.1` — AI runtime boundary for document/reporting jobs

Allowed work:

- define AI runtime entry boundary for governed document/reporting workflows
- define eligible and blocked runtime states
- preserve explicit permissions and prohibitions for the model
- prevent AI runtime from becoming a substitute for missing engine truth

##### `M16.2` — Context packaging from governed engine inputs

Allowed work:

- define how AI runtime packages context from:
  - template retrieval
  - DCF/extracted structured input
  - document lifecycle state
  - resolved library assets
  - task/workflow state where applicable
  - export/reporting requirements
- preserve source-role clarity across context packaging

##### `M16.3` — Controlled generation modes for document/reporting families

Allowed work:

- define generation modes by document/report family
- preserve family-specific constraints
- preserve standards-aware generation control
- preserve bounded invention policy inherited from Phase 5

##### `M16.4` — Output acceptance, bounded retry, and fallback behavior

Allowed work:

- define AI output acceptance rules for document/reporting families
- define bounded retry behavior
- define fallback/refusal behavior where evidence is insufficient or contract rules are broken
- preserve fail-closed behavior where required

##### `M16.5` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M16.6` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 16 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M16.7` — Milestone closeout

Allowed work:

- freeze governed AI runtime boundary for document/reporting workflows
- confirm what belongs to later AI evaluation and workflow-expansion work
- finalize milestone closeout notes if used

#### Exit criteria

- AI runtime boundary is explicit
- context packaging is explicit
- controlled generation modes are explicit
- output acceptance/retry/fallback behavior is explicit
- validation and UAT pass

---

### Milestone 17 — AI Evaluation, Retrieval Use Rules, and Quality Gates

**Goal:** Measure whether AI output is acceptable, grounded, standards-conformant, and detail-consistent rather than merely possible.

#### Canonical checkpoint ladder

- `M17.1` AI evaluation baseline and regression harness
- `M17.2` Quality gates and groundedness checks
- `M17.3` Standards-conformance and detail-level consistency checks
- `M17.4` Retrieval-use rules and source-role discipline
- `M17.5` Validation checkpoint
- `M17.6` Milestone UAT checkpoint
- `M17.7` Milestone closeout

#### Allowed work mapping

##### `M17.1` — AI evaluation baseline and regression harness

Allowed work:

- define evaluation baseline for governed AI outputs
- define regression expectations for document/reporting families
- preserve measurable quality over time

##### `M17.2` — Quality gates and groundedness checks

Allowed work:

- define quality gates
- define groundedness checks
- define evidence-link and source-role checks where applicable
- prevent attractive but ungrounded output from being treated as acceptable

##### `M17.3` — Standards-conformance and detail-level consistency checks

Allowed work:

- define standards-conformance checks
- define structure/detail-level consistency checks
- preserve the deep-detail standard established in Phase 5 and carried through Phase 6
- prevent later shallow AI outputs after deep engine foundations

##### `M17.4` — Retrieval-use rules and source-role discipline

Allowed work:

- define how AI may consume governed deterministic retrieval
- define how AI may consume support/non-authoritative retrieval where allowed later
- preserve source-of-truth role discipline
- prevent support retrieval from being promoted into execution truth by the model

##### `M17.5` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M17.6` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 17 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M17.7` — Milestone closeout

Allowed work:

- freeze AI evaluation and retrieval-use governance boundary
- confirm what belongs to later AI-assisted workflow expansion
- finalize milestone closeout notes if used

#### Exit criteria

- AI evaluation baseline exists
- quality and groundedness gates exist
- standards/detail consistency gates exist
- retrieval-use rules and source-role discipline are explicit
- validation and UAT pass

---

### Milestone 18 — AI-Assisted Workflow Expansion

**Goal:** Expand AI use only after governed document/reporting/runtime/evaluation behavior is stable.

#### Canonical checkpoint ladder

- `M18.1` Controlled review assistance
- `M18.2` Controlled summarization and reporting assistance
- `M18.3` Controlled recommendation behavior
- `M18.4` Workflow-expansion boundaries and refusal rules
- `M18.5` Validation checkpoint
- `M18.6` Milestone UAT checkpoint
- `M18.7` Milestone closeout

#### Allowed work mapping

##### `M18.1` — Controlled review assistance

Allowed work:

- define AI-assisted review support where bounded and governed
- preserve separation between assistance and approval authority
- preserve evidence/source-role discipline

##### `M18.2` — Controlled summarization and reporting assistance

Allowed work:

- define bounded summarization assistance
- define bounded reporting assistance
- preserve document/report family rules and detail discipline

##### `M18.3` — Controlled recommendation behavior

Allowed work:

- define bounded recommendation or suggestion behavior where allowed
- define prohibited recommendation classes where unsafe or out-of-scope
- preserve governed runtime and retrieval-use constraints

##### `M18.4` — Workflow-expansion boundaries and refusal rules

Allowed work:

- define what AI-assisted workflow expansion is allowed to do
- define what remains explicitly out of scope
- define refusal/fallback behavior when requests exceed governed boundaries
- prevent AI-assisted workflow expansion from becoming uncontrolled agentic behavior

##### `M18.5` — Validation checkpoint

Allowed work:

- full milestone validation pass
- remaining in-scope bug fixes only
- validation evidence preparation

##### `M18.6` — Milestone UAT checkpoint

Allowed work:

- minimal UAT evidence for Milestone 18 under `docs/UAT/`
- acceptance decision and rationale
- milestone-level operator-facing confirmation

##### `M18.7` — Milestone closeout

Allowed work:

- freeze Phase 6 AI-layer boundary
- confirm what belongs to later UI/API/cloud/productization phases
- finalize milestone closeout notes if used

#### Exit criteria

- AI-assisted review/summarization/recommendation behavior is bounded
- workflow-expansion boundaries and refusal rules are explicit
- Phase 6 closes without uncontrolled agentic drift
- validation and UAT pass

---

## Phase 6 exit criteria

Phase 6 is complete only when all of the following are true:

- governed AI runtime over the completed core engine is explicit
- AI evaluation and retrieval-use governance are explicit
- AI-assisted workflow expansion remains bounded and governed
- Phase 6 validation passes
- Phase 6 UAT passes
- Phase 6 closeout is complete

---

## Phase 7 — UI and API Layer

### Phase goal

Introduce downstream user-facing and programmatic product surfaces only after the core engine, governed AI/runtime boundaries, and governed data/retrieval boundaries are stable enough.

These surfaces must remain consumers of stable inner layers.

They must not redefine the internal architecture.

### Placeholder milestone family

#### Milestone 19 — API Boundary Introduction

**Placeholder intent**

Introduce the first stable external programmatic surface over the governed core.

**Reserved scope**

- API boundary definition
- request/response contract families
- service-boundary consumption rules
- approval/auth boundary direction if later needed
- prevention of direct adapter coupling to raw state/storage surfaces

**Reserved anti-drift rule**

The API layer must consume stable service/runtime boundaries and must not become the hidden home of domain logic.

---

#### Milestone 20 — UI Layer Introduction

**Placeholder intent**

Introduce user-facing product surfaces on top of stable internal boundaries.

**Reserved scope**

- UI boundary definition
- interaction-flow families
- governed workflow visibility surfaces
- document/export/reporting visibility families
- review/approval/operator interaction direction
- separation between UI convenience and execution truth

**Reserved anti-drift rule**

The UI layer must remain downstream from stable inner layers and must not force premature redesign of resolver/orchestration/runtime contracts.

---

#### Milestone 21 — UI/API Consolidation and Product-Surface Governance

**Placeholder intent**

Stabilize the relationship between UI, API, and the governed engine.

**Reserved scope**

- shared external contract discipline
- product-surface consistency rules
- external-surface governance
- bounded surface consolidation
- validation/UAT/closeout expectations for the phase

**Reserved anti-drift rule**

UI/API surface growth must not weaken deterministic truth, governed source roles, or runtime acceptance discipline.

### Phase 7 exit intent

Phase 7 should close only when:

- API and UI boundaries are explicit
- external product surfaces consume stable inner layers correctly
- surface governance is explicit
- validation and milestone UAT pass at the future detailed-ladder stage

---

## Phase 8 — Cloud / Compute Layer

### Phase goal

Introduce cloud, compute, deployment, packaging, and operational runtime direction only after stable internal and external product boundaries exist.

Cloud direction must target mature architecture.

It must not shape immature architecture prematurely.

### Placeholder milestone family

#### Milestone 22 — Cloud / Compute Foundation

**Placeholder intent**

Introduce foundational cloud and compute direction for the governed system.

**Reserved scope**

- compute model direction
- cloud-hosting shape
- environment-boundary direction
- runtime placement assumptions
- separation between local/dev/test/prod expectations

**Reserved anti-drift rule**

Cloud assumptions must not recenter the architecture around deployment convenience while inner boundaries are still the real design authority.

---

#### Milestone 23 — Deployment / Packaging / Configuration Boundary

**Placeholder intent**

Define deployment packaging and configuration shape over stable system boundaries.

**Reserved scope**

- packaging strategy
- configuration versus code/artifact separation
- environment/config discipline
- deployment artifact family expectations
- boundary between governed source assets and deployable operational surfaces

**Reserved anti-drift rule**

Deployment packaging must target stable resolver/service/runtime/product boundaries rather than temporary implementation shortcuts.

---

#### Milestone 24 — Operational Hardening and Cloud-Governance Readiness

**Placeholder intent**

Prepare the system for operational reliability in cloud/compute environments.

**Reserved scope**

- observability direction
- evaluation hooks
- operational validation direction
- runtime health and failure-governance surfaces
- bounded operational hardening families

**Reserved anti-drift rule**

Operational hardening must extend the governed architecture, not create a second hidden architecture outside the roadmap.

### Phase 8 exit intent

Phase 8 should close only when:

- cloud/compute direction is explicit
- deployment/config boundaries are explicit
- operational hardening direction is explicit
- the cloud/deployment layer still respects all earlier architectural guardrails
- validation and milestone UAT pass at the future detailed-ladder stage

---

## Phase 9 — SaaS Readiness / Productization

### Phase goal

Assess and implement what is needed to turn the system into a true product/SaaS offering only after the core engine, AI layer, UI/API layer, and cloud/compute direction are all sufficiently stable.

This phase is about productization on top of stable architecture.

It is not a substitute for unfinished foundations.

### Placeholder milestone family

#### Milestone 25 — SaaS Readiness Assessment

**Placeholder intent**

Evaluate readiness for SaaS/productization against the real system boundary at that future time.

**Reserved scope**

- gap assessment
- commercial-readiness assessment
- operational-readiness assessment
- product-boundary review
- licensing/packaging/commercial model review where applicable
- identify what is roadmap-ready versus later-program material

**Reserved anti-drift rule**

The desire to commercialize must not back-drive premature shortcuts into core architecture or governed engine truth.

---

#### Milestone 26 — Productization Foundation

**Placeholder intent**

Establish the minimum architectural and operational productization foundations required for a serious SaaS trajectory.

**Reserved scope**

- tenant/boundary direction if later adopted
- product-governance direction
- supportability/maintainability direction
- commercial delivery readiness
- bounded productization foundations that fit the stabilized system

**Reserved anti-drift rule**

Productization foundations must extend the approved system architecture and must not replace it with product-only shortcuts.

---

#### Milestone 27 — SaaS / Product Boundary Consolidation

**Placeholder intent**

Stabilize the final product-facing boundary for the first serious SaaS-ready form.

**Reserved scope**

- product-boundary consolidation
- operational-commercial handoff readiness
- final SaaS-boundary governance
- validation/UAT/closeout expectations for the phase

**Reserved anti-drift rule**

SaaS consolidation must not erase the governed distinctions that make the system trustworthy in the first place.

### Phase 9 exit intent

Phase 9 should close only when:

- SaaS/productization readiness has been explicitly assessed
- productization foundations are explicit
- product-boundary governance is explicit
- the resulting product direction still rests on stable earlier layers rather than bypassing them
- validation and milestone UAT pass at the future detailed-ladder stage

---

## Reserved forward-order summary

The intended forward order after Phase 6 remains:

1. complete Phase 7 UI/API boundaries
2. complete Phase 8 cloud/compute/deployment direction
3. assess and execute Phase 9 SaaS/productization

No later phase may leapfrog unresolved earlier foundations.
