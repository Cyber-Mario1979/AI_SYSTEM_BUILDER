# AI Systems Builder Program (ASBP) — Deterministic Roadmap Rebase

## Why this version exists

This roadmap fixes the planning gap between:
- the canonical roadmap structure
- session-written tracker execution notes
- the actual repository implementation state

It is designed to make direction deterministic again.

---

## Canonical Planning Contract

### 1) Direction source of truth
The roadmap is the source of truth for:
- phase order
- milestone order
- milestone intent
- milestone boundaries
- what kinds of slices are allowed inside each milestone
- milestone exit criteria

### 2) Implementation source of truth
The repository `main` branch is the source of truth for:
- what is actually implemented
- what code exists now
- what tests exist now
- what helpers, commands, and contracts are live now

### 3) Execution evidence source of truth
The progress tracker is the source of truth for:
- what happened in a session
- what was validated in a session
- the last explicitly recorded completed checkpoint
- the next explicitly recorded checkpoint candidate

### 4) Conflict rule
If roadmap, tracker, and repo disagree:
1. roadmap decides intended direction
2. repo decides actual implementation reality
3. tracker is corrected to match both

### 5) Slice rule
A session slice may only be created if it clearly fits one of the allowed slice families already declared in the roadmap.
If not, the roadmap must be updated first before execution continues.

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
3. Indexing and retrieval surfaces come before hybrid runtime behavior.
4. Work structures come before AI writing contracts.
5. Validation discipline is preserved at every stage.
6. Roadmap defines structure and milestone boundaries, not session history.
7. The tracker records execution evidence; it does not decide strategic direction.
8. The repo proves reality; it does not replace the roadmap.
9. Every milestone needs allowed slice families and exit criteria.
10. Future UI and documentation paths may be reserved early, but they must not distort the active build order.

---

## Phase 1 — Foundations

### Milestone 1 — State CLI Tool v1
**Goal:** Build a real package-based CLI tool that can evolve into a deterministic system backbone.

#### Core outcomes
- Python package structure
- CLI entry point
- argument handling
- basic state file handling
- validation mindset
- logs
- first tests

#### Target deliverable
A local CLI that can:
- initialize a state file
- show a state summary
- validate structure
- update simple fields
- support basic task operations

#### Exit criteria
- package-based CLI structure is stable
- state file init/show/update paths exist
- schema validation exists
- baseline tests exist and pass

---

### Milestone 2 — Mini Deterministic Engine
**Goal:** Build a small rule-based task engine without LLM dependency.

#### Core outcomes
- deterministic state transitions
- task IDs
- task ordering
- task dependency handling
- deterministic filtering/querying
- rule-based validation
- mutation-before-save protection

#### Target deliverable
A mini deterministic engine that can:
- load state
- apply deterministic task changes
- validate before save
- reject invalid transitions
- reject invalid dependency writes
- preserve deterministic task behavior through CLI operations

#### Exit criteria
- deterministic task mutations are stable
- dependency validation is stable
- filtering and ordering are deterministic
- invalid writes are rejected without corrupting state

---

## Phase 2 — Deterministic System Modeling

### Milestone 3 — Task Entity Enrichment
**Goal:** Upgrade Task from a minimal operational record into a useful system entity.

#### Core outcomes
- add task title
- preserve task description
- add task owner
- add task start date
- add task end date
- add task duration
- preserve task status
- preserve dependencies
- maintain backward compatibility for older task records

#### Target deliverable
A richer task entity model that is still deterministic, validated, and backward-compatible.

#### Exit criteria
- enriched fields exist on the model
- enriched fields are accepted through controlled CLI paths
- backward compatibility is preserved for older persisted task records
- validation and save discipline remain intact

---

### Milestone 4 — Indexing Layer
**Goal:** Introduce explicit indexing surfaces so the system can reference and organize entities deterministically.

#### Core outcomes
- second indexing surface beyond raw task IDs
- deterministic lookup strategy
- stable identity/reference rules
- normalized access patterns for future entities
- separation between entity storage and entity lookup surface

#### Target deliverable
A deterministic indexing layer that makes future expansion structured rather than ad hoc.

#### Allowed slice families

##### M4.A — Secondary reference foundation
Allowed work:
- secondary key introduction
- normalization rules
- exact identity vs secondary reference separation
- read lookup fallback from `task_id` to normalized `task_key`

##### M4.B — Reference resolution expansion
Allowed work:
- extend task reference resolution into existing mutation paths
- extend reference resolution into dependency inputs
- keep persisted storage identity on `task_id`

##### M4.C — Safety and validation controls
Allowed work:
- ambiguous reference detection
- reserved namespace protection
- persisted-load validation for indexing state
- deterministic no-guess failure behavior

##### M4.D — Secondary key lifecycle controls
Allowed work:
- set/update secondary key for existing tasks
- clear/remove secondary key for existing tasks
- preserve current lookup behavior after mutation or clear

##### M4.E — Index-aware list and filter surfaces
Allowed work:
- list visibility of `task_key`
- presence filters
- exact-key filters
- exact task-reference filters
- dependency/dependent reference filters
- deterministic AND logic across filters

##### M4.F — Read-surface consolidation
Allowed work:
- shared helper consolidation for list filters
- shared helper consolidation for reference views
- shared helper consolidation for task-read payload preparation
- shared helper consolidation for reference-visibility option preparation
- internal refactors that preserve existing CLI contracts exactly

##### M4.G — Milestone closeout and anti-fragmentation
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

#### Current position inside Milestone 4
Based on current tracker/repo alignment, the work has clearly advanced through:
- M4.A foundation
- M4.B reference resolution expansion
- M4.C safety and validation controls
- M4.D lifecycle controls
- M4.E list/filter surfaces
- M4.F read-surface consolidation is in progress

#### Recommended immediate next direction
Do not invent more ad hoc indexing slices without first classifying them under M4.F or M4.G.
The next work should either:
- finish the remaining read/helper consolidation under M4.F, or
- move explicitly into M4.G milestone closeout and anti-fragmentation

#### Exit criteria
Milestone 4 is complete only when all of the following are true:
- identity vs reference separation is stable
- all current task read/mutation/filter surfaces follow one deterministic reference contract
- ambiguous and invalid reference states fail deterministically
- no critical indexing behavior depends on duplicated helper logic scattered across CLI paths
- the boundary between Indexing Layer and Work Package Model is explicitly frozen

---

### Milestone 5 — Work Package Model
**Goal:** Introduce Work Package as a first-class deterministic entity that can hold and organize work.

#### Core outcomes
- `WorkPackageModel` introduced
- deterministic WP identity
- validated WP structure
- task-to-work-package association rules
- clear separation between task entity and work container entity
- deterministic WP read/write behavior

#### Target deliverable
A system that supports work packages as real validated entities rather than informal grouping.

#### Allowed slice families
- WP identity and schema
- WP persistence and validation
- WP read/write CLI surfaces
- task-to-WP association rules
- WP indexing foundations only after Milestone 4 closeout

#### Exit criteria
- WP exists as a validated first-class entity
- tasks can be associated to WP deterministically
- WP behavior is clearly separate from task indexing behavior

---

### Milestone 6 — Task Collections
**Goal:** Add deterministic grouping surfaces for planned work beyond single-task handling.

#### Core outcomes
- task lists and/or task pools as explicit system structures
- deterministic membership rules
- controlled association between:
  - tasks
  - work packages
  - task collections
- no ambiguous grouping behavior
- validated collection structure

#### Target deliverable
A deterministic multi-surface planning structure where tasks can exist both as individual entities and as members of controlled collections.

#### Exit criteria
- collection entities are explicit
- membership rules are deterministic
- grouping behavior is validated and non-ambiguous

---

### Milestone 7 — Multi-Entity Coordination
**Goal:** Stabilize the deterministic relationships between the now-expanded entity types before introducing AI runtime behavior.

#### Core outcomes
- task ↔ work package relationship rules
- task ↔ collection relationship rules
- indexing consistency across entities
- relationship validation before save
- deterministic cross-entity read/update behavior
- minimal orchestration rules without LLM dependency

#### Target deliverable
A deterministic system model where multiple entity types coexist cleanly and safely.

#### Exit criteria
- cross-entity contracts are frozen
- relationship validation exists
- indexing consistency across entities is stable

---

## Phase 3 — AI Runtime Architecture

### Milestone 8 — Hybrid Runtime
**Goal:** Combine deterministic core with a controlled LLM writing layer.

#### Core outcomes
- API call basics
- prompt contracts
- validation loop
- retry/fail rules
- separation between logic and language generation
- deterministic core remains outside the model
- controlled model-writing boundaries
- safe handoff between structured state and generated language

#### Target deliverable
A runtime where deterministic logic remains outside the model, and the model is used in controlled, validated, and limited ways.

#### Exit criteria
- deterministic core and AI writing paths are cleanly separated
- bounded generation contracts exist
- validation loop exists before accepting AI output

---

### Milestone 9 — Runtime-Orchestrated Outputs
**Goal:** Use the hybrid runtime to generate useful outputs from deterministic state without collapsing system discipline.

#### Core outcomes
- structured generation targets
- output contracts
- validation before acceptance
- regeneration rules
- deterministic input → controlled output flow
- separation between system facts and generated prose

#### Target deliverable
A runtime that can generate bounded useful outputs while preserving system integrity.

#### Exit criteria
- generation targets are explicit
- output validation exists
- runtime preserves system facts vs prose separation

---

## Phase 4 — Professionalization

### Milestone 10 — Production-Grade Micro AI System
**Goal:** Build a small but serious end-to-end AI system.

#### Core outcomes
- evaluation mindset
- regression checks
- versioning
- retrieval architecture basics
- testing discipline
- production structure
- maintainability mindset
- architecture clarity

#### Target deliverable
A professional small-scale AI system with architecture, controls, maintainability, and disciplined runtime behavior.

#### Exit criteria
- regression discipline exists
- maintainable architecture is visible in the repo
- evaluation and runtime control practices are established

---

## Reserved Future Extensions (not active build target yet)

These are intentionally reserved now so the foundation does not ignore them, but they do not override the active build order.

### Reserved Extension A — Documented Logic Layer
Purpose:
- formalize system logic in documentation form
- make architecture, contracts, and behavior explainable and reviewable
- support future handoff, maintenance, and onboarding

This should build on top of the deterministic core and stable runtime contracts, not replace them.

### Reserved Extension B — Front-End UI Layer
Purpose:
- add an interface over a stable deterministic/hybrid backend
- surface structured state, actions, and outputs through a controlled user experience
- avoid coupling UI decisions to still-changing core behavior

This should happen after the core model, relationships, and runtime boundaries are sufficiently stable.

---

## Working Rules

1. Do not let the tracker invent direction.
2. Do not let the repo silently redefine roadmap intent.
3. Do not create a new slice unless its milestone family is already declared here.
4. Update roadmap first when a proposed slice does not fit.
5. Validate before declaring completion.
6. Freeze milestone boundaries before moving forward.
7. Reserve future UI/documentation needs early, but do not let them hijack the active core path.

---

## Immediate Operating Rule for Next Sessions

Until Milestone 4 is formally closed:
- all new work must be justified as M4.F or M4.G
- if a proposed slice smells like Work Package behavior, it belongs to Milestone 5 and must not be executed under Milestone 4
- if a proposed slice changes direction rather than consolidating indexing, stop and update this roadmap first
