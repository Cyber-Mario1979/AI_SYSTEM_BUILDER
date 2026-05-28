---
doc_type: canonical_roadmap
canonical_name: ROADMAP_CANONICAL
status: ACTIVE_APPROVED
governs_execution: true
document_state_mode: state_agnostic
authority: canonical_strategic_source_of_truth
version: v5
supersedes: ROADMAP_CANONICAL v4
source_change_control: docs/change_control/ROADMAP_CHANGE_CONTROL_2026-05-25_ROADMAP_V5_LOCAL_CQV_PRODUCT_REDIRECT.md
change_control_id: RCC-ROADMAP-001
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
source_branch: feature/m25-productization-boundary-assessment
approval_state: PROJECT_OWNER_APPROVED
approved_date: 2026-05-25
application_mode: user_applied_package
live_repo_write: NO
---

# AI Systems Builder Program (ASBP) — Canonical Roadmap v5

## Approval and Application Notice

This file is the Project Owner-approved `ROADMAP_CANONICAL.md` v5 replacement for the local integrated CQV product redirect.

It becomes the active canonical roadmap when applied to the repository root as `ROADMAP_CANONICAL.md` together with the approved change-control record and tracker alignment package.

This roadmap supersedes `ROADMAP_CANONICAL.md` v4 for forward execution direction after repository application.

This roadmap application does not perform cleanup, implementation work, PR/issue creation, live repository writing, or executable validation by itself.

---

## 1. Approval Basis and Change-Control Linkage

Roadmap v5 exists because the project reached early Phase 9 productization-readiness assessment before the local integrated CQV product core was complete.

The approved change-control direction is:

`Roadmap v5 local integrated CQV product redirect.`

The approved storage/disposition decision for the change-control record is:

`docs/change_control/ROADMAP_CHANGE_CONTROL_2026-05-25_ROADMAP_V5_LOCAL_CQV_PRODUCT_REDIRECT.md`

The approved change-control clarifications are binding for this roadmap:

1. **Cleanup scope is all repository non-code documents.** After v5 is approved and applied, every non-code repository document is subject to inventory and disposition review. Code and tests are excluded unless a future approved work item explicitly reclassifies them.
2. **Roadmap v5 must be granular and execution-ready.** It must not be a placeholder roadmap whose detailed milestone ladders are deferred until later. Drafting may be chunked for review control, but the approved v5 must consolidate the execution path into one canonical source.

---

## 2. Why v5 Exists

Roadmap v4 correctly established that deterministic layers must precede AI, UI/API, cloud, deployment, and productization. It also correctly kept later Phase 7-9 work downstream from stable internal boundaries.

However, execution later expanded Phase 7, Phase 8, and early Phase 9 through detailed addenda and reached `M25.3 — Commercial and packaging readiness assessment`. That early readiness probe showed that ASBP has a strong deterministic engine and governance foundation, but it is not yet a complete local integrated CQV product.

The product core is incomplete in these areas:

- governed CQV libraries
- runtime-authoritative presets, selectors, task pools, profiles, calendars, planning basis, and mappings
- standards source/citation/applicability authority usable by the product
- complete product-ready document factory / document engine workflow, including rationale/logic, DCF intake, template selection, generation, rendering, lifecycle, and review/approval controls
- retrieval/indexing only after authoritative sources exist and only where justified
- AI assistance only above governed context, data, source, and output boundaries
- local AI model/runtime strategy that can run with the app during controlled heavy-use testing where AI assistance is in scope
- local usable workflow/UI sufficient for real user trials
- local validation and user-trial/UAT evidence
- later productization/SaaS re-entry evidence

Roadmap v5 therefore redirects execution away from premature productization/SaaS readiness and toward a local integrated CQV product build path before any renewed productization or SaaS readiness work.

---

## 3. Purpose

This roadmap defines:

- phase order
- milestone order
- milestone intent
- milestone boundaries
- detailed checkpoint ladders
- allowed and not-allowed work
- milestone entry and exit criteria
- validation and UAT gates
- deferred-dependency placement
- product-core completion gates
- non-code document cleanup sequencing
- productization/SaaS re-entry conditions

This roadmap does **not** function as:

- a live progress tracker
- a session log
- a repo evidence substitute
- a code implementation specification
- a cleanup execution package
- a PR body
- an issue tracker
- a license/legal decision
- a product launch authorization

The tracker records current position. The repo proves implementation reality. The roadmap defines the intended execution ladder.

---

## 4. Canonical Authority Contract

### 4.1 Direction source of truth

After approval and repository application, `ROADMAP_CANONICAL.md` v5 is the single active roadmap authority for:

- phase order
- milestone order
- checkpoint order
- roadmap-level scope boundaries
- milestone entry and exit gates
- product-core sequencing
- validation and UAT gate expectations
- later productization/SaaS re-entry conditions

### 4.2 Implementation source of truth

Repo reality is the source of truth for what actually exists:

- code
- tests
- package structure
- commands
- runtime behavior
- validation evidence
- UAT evidence
- milestone closeout evidence

The roadmap may define intended future behavior, but it does not prove implementation.

### 4.3 Progress source of truth

`PROGRESS_TRACKER.md` remains the short current-position pointer only.

It may record:

- current phase
- current milestone
- current approved checkpoint family
- latest completed checkpoint
- exact next unfinished checkpoint
- latest verified validation result
- milestone UAT status
- repo alignment status
- relevant deferred-dependency gate status

It does not override roadmap direction or repo implementation truth.

### 4.4 Architecture source of truth

`ARCHITECTURE_GUARDRAILS.md` remains permanent architecture governance.

The following are binding unless changed by approved architecture governance:

- CLI is an adapter only.
- New domain behavior must attach through approved core/module boundaries.
- State and persistence access must go through approved state boundary helpers/modules.
- If future work requires bypassing those boundaries, implementation pauses for planning before coding.

### 4.5 Deferred-dependency gate truth

`docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` remains active gate memory.

It must be checked when work touches:

- productization
- Phase 8 / Phase 9 / later product phases
- API / external contract work and UI/API product-surface work
- document generation/templates/output rendering
- standards/citation/embedding/retrieval
- governed library runtime promotion
- presets/selectors/task pools/profiles/calendars/planning basis/mappings
- model/provider integration
- live AI runtime integration
- deployment, pre-go-live, or operational-readiness work

The register does not create roadmap checkpoints by itself. Roadmap v5 places or carries DDR work into explicit milestones.

### 4.6 Historical evidence role

Completed milestone evidence, UAT records, closeout records, decision gates, addenda, and supporting artifacts preserve traceability.

They do not govern future execution unless this roadmap or another approved active authority explicitly says so.

---

## 5. Addendum and Change-Control Policy

### 5.1 No-active-addenda default

Roadmap v5 is intended to remove the need for active roadmap addenda for the current redirect path.

After v5 approval and application:

- `ROADMAP_CANONICAL.md` v5 is the only active roadmap authority.
- Addenda may remain as historical evidence only.
- No new active roadmap addendum should be created by default.
- Temporary overlays are allowed only through explicit change control and only for bounded exceptional situations.

### 5.2 Roadmap change-control rule

Any future roadmap-direction change must go through change control when it affects:

- phase order
- milestone order
- checkpoint order
- product-core gates
- validation/UAT gate policy
- deferred-dependency closure or reclassification
- productization/SaaS re-entry conditions
- architecture governance
- cleanup authority for non-code documents

Minimum roadmap change-control content:

- change title and ID
- reason for change
- affected roadmap areas
- affected tracker state
- affected DDRs
- affected completed milestone interpretation
- impact on validation/UAT
- impact on cleanup and evidence retention
- risks if changed
- risks if not changed
- explicit approval state
- exact application plan

### 5.3 Post-v5 cleanup gate

Cleanup must not happen before v5 approval and application.

After v5 is applied, a dedicated non-code document cleanup lane must inventory and classify every non-code document in the repository before any relocation, archive, supersession, or deletion occurs.

---

## 6. Roadmap Design Principles

1. Deterministic foundations come before AI assistance.
2. Governed source authority comes before retrieval and productized output.
3. Runtime-authoritative libraries come before product behavior that depends on them.
4. Standards source/citation/applicability authority comes before standards-backed product claims.
5. Product-ready document output requires a complete document factory / document engine workflow, not templates alone.
6. DCF intake, document logic/rationale, template selection, controlled generation, rendering, lifecycle, and review/approval controls must be governed before product-ready document claims.
7. Retrieval is a helper, not source authority.
8. AI assistance operates only above governed context, data, source, and output boundaries.
9. Local AI model/runtime testing must be explicitly scoped, app-coupled, and controlled before heavy-use AI trial claims.
10. UI/API are downstream product surfaces, not execution truth.
11. API and external contracts must remain downstream of approved core/service/runtime boundaries.
12. Cloud/deployment/productization are downstream of a working local product, not substitutes for one.
13. Validation and UAT evidence must support milestone closure.
14. Completed milestones remain closed for their approved scope unless explicitly reopened by change control.
15. Governance/model closure must never be mistaken for executable/product capability closure.
16. Cleanup preserves traceability before it improves tidiness.
17. The local integrated CQV product must be usable locally before productization/SaaS resumes.
18. Productization re-entry requires product-core completion, validation, user trial/UAT, and owner acceptance.

---

## 7. Validation and UAT Policy

### 7.1 Validation policy

Code-affecting work requires:

`python -m pytest -q`

Do not claim tests passed unless they were actually run and passed in the current environment.

Docs-only work does not require pytest unless it changes:

- executable commands
- imports
- package behavior claims
- code examples that must be verified
- validation truth
- runtime contracts
- CLI behavior

Docs-only governance work still requires document consistency review before approval.

### 7.2 UAT policy

From Milestone 4 onward, milestone transition requires UAT or owner acceptance evidence appropriate to the milestone.

Minimum UAT evidence:

- milestone identifier
- scope/coverage statement
- acceptance decision
- rationale
- date
- reference to validation evidence when applicable
- owner/reviewer field when used

For the local integrated CQV product path, UAT must include real local workflow trial evidence before productization/SaaS re-entry.

### 7.3 Checkpoint Execution Mode and Completion-Minimum Control

This section was added under `CONTROL-RECOVERY-001 — Roadmap / Governance / Operation-Pack Anti-Drift Repair`.

It does not reopen completed milestones by itself. It controls active and future execution and may be used to interpret completed evidence truthfully during recovery review.

#### 7.3.1 Execution mode is mandatory

Every active checkpoint from M26 onward must have an explicit execution mode before `PLAN` or `GO`.

Allowed execution modes:

| Execution mode | Meaning |
|---|---|
| `Governance-only` | Decision, scope lock, review, acceptance, closeout, or planning artifact only. |
| `Build/content` | Runtime code, source data, executable model, source library, validator, loader, output, retrieval, AI, UI, or product workflow. |
| `Hybrid` | Governance boundary plus implementation/source/runtime content. |
| `Validation` | Validation evidence checkpoint. |
| `UAT` | Actual user acceptance testing, owner acceptance, or both, explicitly stated. |
| `Closeout` | Milestone boundary freeze. |

#### 7.3.2 Completion minimum is mandatory

Every active checkpoint from M26 onward must define these fields before execution:

1. execution mode;
2. required completion artifact;
3. implementation/source minimum;
4. validation requirement;
5. tracker movement rule;
6. explicit non-implementation claims.

If any field is missing, the checkpoint is ambiguous and must not proceed to `GO`.

#### 7.3.3 Default classification for Phase 9 product-core work

For Phase 9 local integrated CQV product-core work, a checkpoint must not be treated as governance-only merely because its wording says `define`, `scope`, `model`, `review`, `decide`, `assess`, `gate`, `framework`, `authority`, or `behavior`.

If the checkpoint is not explicitly labelled `Governance-only`, `Validation`, `UAT`, or `Closeout`, the default classification is `Hybrid` or `Build/content`.

#### 7.3.4 Ambiguity stop rule

If checkpoint wording is ambiguous, execution stops before `PLAN` or `GO`.

Ambiguous wording includes, but is not limited to:

- `define`
- `scope`
- `model`
- `review`
- `decide`
- `assess`
- `gate`
- `framework`
- `authority`
- `behavior`

These words are allowed in the roadmap, but they must be paired with an explicit execution mode and completion minimum.

#### 7.3.5 Evidence document limitation

A milestone evidence document may support tracker movement only when the checkpoint is explicitly `Governance-only`, `Validation`, `UAT`, or `Closeout`.

For `Hybrid` and `Build/content` checkpoints, a milestone evidence document is not sufficient by itself. Tracker movement requires the required implementation/source minimum and validation evidence where applicable.

#### 7.3.6 `GO` package generation rule

`GO` must not prepare an implementation package, replacement file, tracker update, or `apply.py` until the anti-drift preflight confirms:

- execution mode;
- completion minimum;
- DDR impact;
- architecture boundary;
- validation requirement;
- tracker movement rule;
- explicit non-implementation claims.

#### 7.3.7 M29-M34 pre-execution classification gate

M29 through M34 must not execute until the active checkpoint has been classified with execution mode and completion minimum.

If a future M29-M34 checkpoint table does not yet include these fields, the checkpoint requires a roadmap interpretation or amendment before `PLAN` or `GO`.


---

## 8. Phase Summary

| Phase | Milestones | Status / v5 treatment |
|---|---|---|
| Phase 1 — Foundations | M1-M2 | Historical/completed foundation; retained for traceability |
| Phase 2 — Deterministic System Modeling | M3-M7 | Historical/completed deterministic model; retained for traceability |
| Phase 3 — AI Runtime Architecture | M8-M10 | Historical/completed runtime/output boundary foundation; retained for traceability |
| Phase 4 — Professionalization | M11 | Historical/completed professionalization boundary; retained for traceability |
| Phase 5 — Core Engine Completion | M12-M15 | Historical/completed core-engine/document/export/resolver/library framework; reinterpreted where product capability remains incomplete |
| Phase 6 — AI Layer | M16-M18 | Historical/completed AI boundary/evaluation/advisory governance; not live/product AI provider integration |
| Phase 7 — UI and API Layer | M19-M21 | Historical/completed external-surface governance; not complete local usable product UI |
| Phase 8 — Cloud / Compute Layer | M22-M24 | Historical/completed cloud/deployment/operational boundary planning; not product deployment readiness |
| Phase 9 — Roadmap Reset and Local Integrated CQV Product Core | M25-M34 | Active future v5 path after approval/application |
| Phase 10 — Productization / SaaS Re-entry | M35-M38 | Deferred until local product core is validated, trialed, and accepted |

---

## 9. Historical Foundation Roadmap — Preserved and Not Reopened by Default

This section preserves the completed foundation roadmap at the canonical level without reopening closed milestones.

Detailed historical evidence remains in milestone documents, UAT records, closeout notes, and historical addenda until the comprehensive non-code document cleanup lane classifies them.

### Phase 1 — Foundations

#### Milestone 1 — State CLI Tool v1

Goal: Build a package-based CLI tool capable of evolving into a deterministic system backbone.

Checkpoint ladder:

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

Exit interpretation: package structure, state init/show/update, schema validation, and baseline tests were foundation concerns.

#### Milestone 2 — Mini Deterministic Engine

Goal: Build a small rule-based task engine without LLM dependency.

Checkpoint ladder:

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

Exit interpretation: deterministic task mutations, dependency validation, filtering, ordering, and corruption-prevention were foundation concerns.

### Phase 2 — Deterministic System Modeling

#### Milestone 3 — Task Entity Enrichment

Goal: Upgrade Task from a minimal record into a useful system entity.

Checkpoint ladder:

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

#### Milestone 4 — Indexing Layer

Goal: Introduce explicit indexing surfaces so the system can reference and organize entities deterministically.

Checkpoint ladder:

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

#### Milestone 5 — Work Package Model

Goal: Introduce Work Package as a first-class deterministic entity.

Checkpoint ladder:

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

#### Milestone 6 — Binding Context and Task Collections

Goal: Introduce deterministic selector context and bound collections.

Checkpoint ladder:

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

#### Milestone 7 — Planning Layer

Goal: Introduce deterministic planning above committed task collections and before output generation.

Checkpoint ladder:

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

### Phase 3 — AI Runtime Architecture

#### Milestone 8 — Multi-Entity Coordination

Goal: Stabilize deterministic relationships across sources, Work Packages, tasks, collections, planning, and downstream layers.

Checkpoint ladder:

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

#### Milestone 9 — Hybrid Runtime

Goal: Combine deterministic core with a controlled AI writing layer.

Checkpoint ladder:

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

#### Milestone 10 — Runtime-Orchestrated Outputs

Goal: Generate useful outputs from deterministic state without collapsing system discipline.

Checkpoint ladder:

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

### Phase 4 — Professionalization

#### Milestone 11 — Production-Grade Micro AI System

Goal: Build a small but serious end-to-end AI system.

Checkpoint ladder:

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

### Phase 5 — Core Engine Completion

Interpretation in v5: Phase 5 created strong governed engine boundaries. It does not prove every local CQV product library, template, or output behavior is product-ready.

#### Milestone 12 — Governed Document Engine

Checkpoint ladder:

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

V5 interpretation: preserved as governed document-engine foundation; product-ready template loading, rendering, and product document generation remain future product-core work unless already proven by repo reality.

#### Milestone 13 — Export and Reporting Engine

Checkpoint ladder:

- `M13.1` Export identity and contract foundation
- `M13.2` Spreadsheet and operational export surfaces
- `M13.3` Gantt and planning visualization exports
- `M13.4` Dashboard and status summary exports
- `M13.5` Reporting export family and detail-level discipline
- `M13.6` Export invocation and validation behavior
- `M13.7` Validation checkpoint
- `M13.8` Milestone UAT checkpoint
- `M13.9` Milestone closeout

V5 interpretation: preserved as export/reporting contract foundation; product-ready rendering and distribution remain future product-core work unless proven by repo reality.

#### Milestone 14 — Resolver / Registry and Governed Data Layer

Checkpoint ladder:

- `M14.1` Resolver / registry boundary foundation
- `M14.2` Governed asset identity and version-pinned lookup
- `M14.3` Calendar and planning-basis resolution family
- `M14.4` Authored-source versus deployment-compiled separation
- `M14.5` Governed retrieval versus support-retrieval boundary
- `M14.6` Validation checkpoint
- `M14.7` Milestone UAT checkpoint
- `M14.8` Milestone closeout

V5 interpretation: preserved as resolver/source-role foundation; runtime-authoritative CQV product libraries and registry-consuming standards behavior remain future product-core work where not already implemented and validated.

#### Milestone 15 — Governed Library Expansion and Engine Hardening

Checkpoint ladder:

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

V5 interpretation: preserved as governed-library framework and hardening foundation; executable runtime-authoritative library promotion, deployment-compiled lookup, complete product task pools, and consolidated product library package/layout remain future product-core work where not already implemented and validated.

### Phase 6 — AI Layer

Interpretation in v5: Phase 6 established controlled AI boundary/evaluation/advisory foundations. It does not prove live model/provider integration or product-facing AI assistant readiness.

#### Milestone 16 — AI Runtime for Governed Document and Reporting Workflows

Checkpoint ladder:

- `M16.1` AI runtime boundary for document/reporting jobs
- `M16.2` Context packaging from governed engine inputs
- `M16.3` Controlled generation modes for document/reporting families
- `M16.4` Output acceptance, bounded retry, and fallback behavior
- `M16.5` Validation checkpoint
- `M16.6` Milestone UAT checkpoint
- `M16.7` Milestone closeout

#### Milestone 17 — AI Evaluation, Retrieval Use Rules, and Quality Gates

Checkpoint ladder:

- `M17.1` AI evaluation baseline and regression harness
- `M17.2` Quality gates and groundedness checks
- `M17.3` Standards-conformance and detail-level consistency checks
- `M17.4` Retrieval-use rules and source-role discipline
- `M17.5` Validation checkpoint
- `M17.6` Milestone UAT checkpoint
- `M17.7` Milestone closeout

#### Milestone 18 — AI-Assisted Workflow Expansion

Checkpoint ladder:

- `M18.1` Controlled review assistance
- `M18.2` Controlled summarization and reporting assistance
- `M18.3` Controlled recommendation behavior
- `M18.4` Workflow-expansion boundaries and refusal rules
- `M18.5` Validation checkpoint
- `M18.6` Milestone UAT checkpoint
- `M18.7` Milestone closeout

### Phase 7 — UI and API Layer

Interpretation in v5: Phase 7 established external API/UI contract and product-surface governance boundaries. It does not prove a complete usable local CQV product UI/workflow.

#### Milestone 19 — API Boundary Introduction

Checkpoint family retained by v5:

- API boundary foundation
- request/response contract foundation
- service-boundary consumption rules
- API safety and adapter isolation rules
- minimal read surfaces
- minimal command/intake surfaces
- validation checkpoint
- UAT checkpoint
- closeout

#### Milestone 20 — UI Layer Introduction

Checkpoint family retained by v5:

- UI boundary foundation
- interaction-flow foundation
- workflow visibility surfaces
- document/export/reporting visibility surfaces
- review/approval/operator interaction direction
- UI safety and adapter isolation rules
- validation checkpoint
- UAT checkpoint
- closeout

#### Milestone 21 — UI/API Consolidation and Product-Surface Governance

Checkpoint family retained by v5:

- shared external contract discipline
- product-surface consistency rules
- external-surface governance
- placeholder compatibility discipline
- validation checkpoint
- UAT checkpoint
- closeout

### Phase 8 — Cloud / Compute Layer

Interpretation in v5: Phase 8 established cloud/compute/deployment/operational boundary planning and governance evidence. It does not prove deployable product packaging, go-live readiness, or SaaS readiness.

#### Milestone 22 — Cloud / Compute Foundation

Checkpoint family retained by v5:

- cloud/compute boundary foundation
- environment boundary direction
- runtime placement assumptions
- local/dev/test/prod separation
- validation checkpoint
- UAT checkpoint
- closeout

#### Milestone 23 — Deployment / Packaging / Configuration Boundary

Checkpoint family retained by v5:

- deployment packaging boundary
- configuration versus code/artifact separation
- environment/config discipline
- deployment artifact family expectations
- source asset versus deployable surface boundary
- validation checkpoint
- UAT checkpoint
- closeout

#### Milestone 24 — Operational Hardening and Cloud-Governance Readiness

Checkpoint family retained by v5:

- observability direction
- evaluation hooks
- operational validation direction
- runtime health and failure-governance surfaces
- bounded operational hardening families
- validation checkpoint
- UAT checkpoint
- closeout

---

## 10. Phase 9 — Roadmap Reset and Local Integrated CQV Product Core

### Phase goal

Redirect execution from premature productization/SaaS readiness to a local integrated CQV product core that can be used, validated, trialed, and accepted before any productization/SaaS re-entry.

### Phase 9 must include

- canonical roadmap reset
- comprehensive non-code document cleanup planning and application
- runtime-authoritative CQV library/source authority
- presets/selectors/task pools/profiles/calendars/planning basis/mappings
- standards applicability/citation/runtime consumption where authorized
- complete product-ready document factory / document engine workflow, including DCF intake, document logic, controlled generation, rendering, lifecycle, and review/approval controls
- retrieval/indexing only after authoritative sources exist
- AI assistance only over governed sources and accepted output boundaries
- local AI model/runtime strategy and controlled app-coupled heavy-use testing where AI assistance is in trial scope
- local usable workflow/UI
- integrated validation and user trial/UAT
- product-core closeout and re-entry gate

### Phase 9 must not include

- product/SaaS launch
- production deployment
- tenant/subscription behavior
- commercial release
- license change without product-boundary decision
- repository visibility change without product-boundary decision
- uncontrolled model/provider integration, including local model runtime, outside the approved M31/M33/M37 path and DDR-007 closure/control path
- standards embedding/retrieval before DDR-005 authority conditions
- product-ready document generation before DDR-003/DDR-006 closure evidence
- cleanup before the v5 approval/application gate

---

### Milestone 25 — Roadmap Reset, Evidence Preservation, and Non-Code Document Cleanup Gate

**Goal:** Complete the roadmap direction reset, apply v5, align tracker/DDR placement, and perform controlled non-code document cleanup before build execution resumes.

#### Entry gate

- `M25.1`, `M25.2`, and `M25.3` early readiness evidence exists.
- Post-`M25.3` redirect decision is approved.
- Roadmap change-control direction is approved.
- Storage/disposition decision for the change-control record is approved.

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M25.1` Productization boundary assessment | Preserve early readiness probe evidence | Retain as evidence; interpret as assessment-only | Treat as product readiness |
| `M25.2` Deferred dependency disposition review | Preserve DDR disposition and closure-scope evidence | Retain DDR placement evidence; distinguish governance/model closure from executable closure | Close product blockers by assertion |
| `M25.3` Commercial and packaging readiness assessment | Preserve commercial/packaging assessment | Retain as early evidence; preserve conclusion that ASBP is not product-package/commercial/SaaS ready | Continue to M25.4 operational readiness under archived Addendum 10 |
| `M25.4` Roadmap change-control record application | Apply approved change-control record to `docs/change_control/` | Add approved record; preserve approval clarifications | Implement build work or cleanup actions |
| `M25.5` Canonical roadmap v5 approval and application | Approve and apply `ROADMAP_CANONICAL.md` v5 | Replace canonical roadmap with approved v5; preserve source lock in change-control record | Create active addendum instead of v5 |
| `M25.6` Tracker and DDR alignment after v5 | Align current position to v5 | Update tracker to exact next v5 checkpoint; review DDR placement text | Claim validation not performed |
| `M25.7` Comprehensive non-code document inventory | Inventory all non-code repo documents | Classify every non-code document; assign disposition candidates | Move/delete/archive files |
| `M25.8` Cleanup package planning | Prepare approved cleanup package | Propose exact file moves/revisions/archives/deletions; preserve traceability | Apply cleanup before approval |
| `M25.9` Cleanup package application | Apply only approved cleanup actions | User-applied package or live write only if separately authorized | Modify code/tests or expand cleanup scope silently |
| `M25.10` Post-cleanup alignment review | Confirm repo authority surfaces are coherent | Check roadmap/tracker/DDR/guardrails/docs index/public surface | Resume build before alignment is complete |
| `M25.11` Roadmap reset validation checkpoint | Validate docs-only consistency | No pytest unless code/commands/imports/behavior claims changed; document consistency review | Claim executable validation if not run |
| `M25.12` Roadmap reset UAT / owner acceptance | Accept reset and cleanup lane outcome | Owner acceptance of readiness to resume build | Treat acceptance as product UAT |
| `M25.13` Milestone closeout | Freeze reset boundary | Close roadmap reset; point tracker to `M26.1` | Resume productization/SaaS |

#### Exit criteria

- Change-control record is repo-retained.
- `ROADMAP_CANONICAL.md` v5 is approved and applied.
- Tracker points to the exact first local CQV product-core checkpoint.
- DDR placement is reviewed for v5 consistency.
- All non-code documents have been inventoried and dispositioned.
- Approved cleanup actions, if any, are applied.
- Final alignment review confirms no active parallel roadmap authority remains.
- Owner acceptance is recorded.

---

### Milestone 26 — CQV Source Authority and Runtime Library Architecture

**Goal:** Convert governed CQV source families from framework/reference foundations into a coherent runtime-authoritative local product source architecture.

#### Entry gate

- M25 reset and cleanup closeout complete.
- Tracker points to `M26.1`.
- DDR register reviewed.

#### DDR focus

- DDR-001
- DDR-002
- DDR-003 dependency awareness
- DDR-004 dependency awareness
- DDR-006 dependency awareness

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M26.1` Local product source-boundary scope lock | Define local CQV product MVP source boundary | Decide included CQV asset families; define local product MVP scope; map source roles | Implement content beyond approved boundary |
| `M26.2` Authoritative source taxonomy | Define source families and identities | CQV libraries, presets, selectors, task pools, profiles, calendars, planning basis, mappings, standards bundles, templates | Treat scattered docs as runtime authority |
| `M26.3` Runtime-authoritative library package layout | Define package/layout for runtime authority | Source folders, version/status fields, release states, ownership, source/compiled separation | Bypass resolver/source-role rules |
| `M26.4` Authored-source to compiled-runtime promotion model | Define promotion/compile path | Validation rules, compiled lookup generation expectations, traceability | Make compiled lookup source truth |
| `M26.5` Library source validation contracts | Define validation schema/contracts | Identity uniqueness, cross-reference checks, status/version validation | Accept unchecked library assets |
| `M26.6` Product-core source registry model | Define registry for local product source assets | Asset records, versions, applicability, source location, lifecycle state | Collapse registry with tracker or roadmap |
| `M26.7` Runtime lookup adapter boundary | Define approved runtime lookup access | Resolver-bound access, no raw file lookup from UI/API/AI | Add hidden direct file access |
| `M26.8` Library authority implementation package | Implement only approved source-authority primitives | User-applied code/docs package; tests where executable | Productize unvalidated content |
| `M26.9` Validation checkpoint | Validate implementation | `python -m pytest -q` if code changed; source validation evidence | Claim runtime authority without validation |
| `M26.10` Milestone UAT / owner acceptance | Accept source-authority architecture | Confirm library authority model is usable for next milestones | Treat acceptance as full product UAT |
| `M26.11` Milestone closeout | Freeze M26 boundary | Record remaining dependencies | Continue to M27 with open source-boundary ambiguity |

#### Exit criteria

- Runtime-authoritative source architecture is explicit.
- Authored-source versus compiled-runtime roles are controlled.
- Library package/layout is defined and validated where implemented.
- Resolver/runtime access boundary is clear.
- DDR-001 and DDR-002 are either directly addressed for this layer or carried forward with exact remaining closure scope.

---

### Milestone 27 — Presets, Selectors, Task Pools, Profiles, Calendars, Planning Basis, and Mappings

**Goal:** Build the local CQV product’s operational source libraries that determine what work is selected, staged, committed, planned, and executed.

#### Entry gate

- M26 source authority boundary complete.
- Runtime-authoritative library package/layout exists or is explicitly approved as the target for this milestone.

#### DDR focus

- DDR-001
- DDR-002
- DDR-009 awareness for external placeholders

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M27.1` CQV preset family scope | Define initial preset families | Cleanroom, process equipment, utilities, computerized systems, manual fallback | Unlimited preset sprawl |
| `M27.2` Selector and scope-intent model hardening | Define selector inputs | Type, scope, lifecycle event, risk, standards bundle, user intent | Work selection from WP type alone |
| `M27.3` Task-pool source model | Define authoritative task-pool records | Atomic task IDs, dependencies, owners/roles, durations, prerequisites, document links | Treat persisted tasks as source library |
| `M27.4` Profile model | Define profile records | Area/system profiles, cleanroom/HVAC profile, equipment/system profile, qualification profile | Embed one-off local assumptions as universal truth |
| `M27.5` Calendar and work-time model | Define calendar source records | Workweek, workmonth, holidays, Cairo/local defaults if approved, user-amendable parameters | Hide regional assumptions |
| `M27.6` Planning basis and duration model | Define duration sources | Duration refs, estimation source, scope rules, task-pool links | Use untraceable durations |
| `M27.7` Mapping model | Define mapping records | Preset-to-profile, selector-to-task-pool, standard-to-template, task-to-document links | Duplicate logic in UI/API/AI layers |
| `M27.8` Library content implementation wave 1 | Implement first local product CQV library set | Use M26 package/layout; preserve validation | Product-ready claims before trial |
| `M27.9` Cross-library validation | Validate relationships | Identity, refs, dependencies, mappings, applicability, duration refs | Accept dangling or ambiguous refs |
| `M27.10` Stage/commit compatibility check | Confirm source-to-execution path | Source selection → staged tasks → committed tasks → planning input | Plan directly from source definitions without instantiation |
| `M27.11` Validation checkpoint | Validate executable behavior | `python -m pytest -q` if code changed; library validation report | Skip source validation |
| `M27.12` Milestone UAT / owner acceptance | Accept library usability | Owner confirms source libraries support local CQV flow | Treat as full product acceptance |
| `M27.13` Milestone closeout | Freeze library content baseline | Baseline v0.x source libraries | Continue with unresolved core library ambiguity |

#### Exit criteria

- Presets/selectors/task pools/profiles/calendars/planning basis/mappings exist as controlled source families.
- Source-to-instantiated-execution path is deterministic.
- Cross-library references validate.
- Library baseline is accepted for downstream standards/document/UI work.

---

### Milestone 28 — Standards Applicability, Citation, and Runtime Consumption Authority

**Goal:** Make standards source/citation/applicability authority usable by the local product without overclaiming audit-ready or clause-level authority where evidence is incomplete.

#### Entry gate

- M26 source authority boundary complete.
- M27 relevant standards-bundle mappings are available or scoped.
- Standards source registry v0.1 exists as approved DDR-004 model evidence.

#### DDR focus

- DDR-004
- DDR-005 awareness
- DDR-006 awareness

#### Checkpoint ladder

| Checkpoint | Execution mode | Purpose | Completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M28.1` Standards registry baseline review | `Governance-only` | Review registry records | Registry baseline review evidence confirming statuses, TBD fields, verification limits, and mandatory flags. | Document consistency review. No executable validation unless code, commands, schemas, runtime behavior, or executable contracts change. | May advance only after the baseline review evidence exists. | Treat pending/TBD as verified authority. |
| `M28.2` Applicability engine scope | `Hybrid` | Define applicability behavior and the future runtime-facing applicability contract. | Applicability contract/model sufficient to govern later runtime behavior, including trigger taxonomy, input dimensions, applicability decision states, mandatory-use eligibility, limitation propagation, and rejection cases. A narrative evidence file alone is not sufficient. | Document consistency review is required. If code, source contracts, schemas, validators, or executable behavior are added or changed, `python -m pytest -q` is required. | May advance only after the applicability contract/model exists and explicitly records non-implementation limits. | Universal standards application or mandatory use from registry presence alone. |
| `M28.3` Citation model implementation scope | `Hybrid` | Define citation depth behavior and the future runtime-facing citation contract. | Citation model/contract covering document, version, section, clause, table-row, and requirement-level citation behavior; citation-depth eligibility; missing-clause limitation rules; and no-fabrication guard. A narrative evidence file alone is not sufficient. | Document consistency review is required. If code, source contracts, schemas, validators, or executable behavior are added or changed, `python -m pytest -q` is required. | May advance only after the citation model/contract exists and limitation behavior is explicit. | Fabricate clauses, versions, source text, or regulatory meaning. |
| `M28.4` Standards-bundle binding | `Hybrid` / `Build/content` | Link standards bundles to selectors, profiles, templates, or source mappings where authority supports it. | Standards-bundle binding records, mapping records, or source-contract updates that identify source IDs, applicability boundaries, authority/verification limits, and downstream consumers. Vague labels are not sufficient. | Source consistency review is required. If source data, schemas, validators, or executable behavior change, `python -m pytest -q` is required. | May advance only after binding artifacts exist and unresolved/pending sources remain visibly limited. | Treat standards bundles as vague labels or universal authority. |
| `M28.5` Stricter-requirement comparison rule | `Hybrid` / `Build/content` | Define and, where approved, implement comparison governance. | Comparison rule model/contract identifying applicable sources, compared requirements, selected stricter requirement, override path, and limitation behavior. Tests are required if executable comparison behavior is implemented. | Document/source consistency review is required. `python -m pytest -q` is required if executable behavior changes. | May advance only after comparison rule evidence or implementation exists with explicit boundary limits. | Use risk-based reasoning to weaken mandatory requirements silently. |
| `M28.6` Controlled override model | `Hybrid` | Define controlled override records. | Override model/contract covering approver, rationale, residual risk, applicability boundary, source comparison, decision reference, and limitation statement. Tests are required if executable validation behavior is implemented. | Document/source consistency review is required. `python -m pytest -q` is required if executable behavior changes. | May advance only after override record structure and non-equivalence limits exist. | Treat override as regulatory equivalence or source closure. |
| `M28.7` Local/company/site standards intake | `Hybrid` | Define user-uploaded/internal standards flow. | Intake model/contract or record flow covering draft source record, authority decision, comparison, approval, limitation handling, and local/company/site/client source status. Tests are required if executable intake behavior is implemented. | Document/source consistency review is required. `python -m pytest -q` is required if executable behavior changes. | May advance only after intake flow artifacts exist and user-provided/internal-source limits are explicit. | Treat user-provided local matrix as public regulation. |
| `M28.8` Runtime registry consumption package | `Build/content` | Implement registry reading and validation where approved. | Runtime registry reading/parsing/source-status enforcement and related tests, or an explicit owner-approved decision to defer runtime consumption with limitations. | `python -m pytest -q` is required when runtime code, validators, schemas, or executable behavior change. | May advance only after runtime/source implementation and validation evidence exist, or after a formal deferral decision is recorded. | Product standards output without tests. |
| `M28.9` Standards-output limitation rules | `Hybrid` | Define output warning and limitation behavior. | Limitation contract/model covering pending/TBD/user-provided/reference-only sources, citation-depth limits, registry-version traceability, and visible output warnings. Tests are required if output behavior is executable. | Document/source consistency review is required. `python -m pytest -q` is required if executable behavior changes. | May advance only after limitation behavior is explicit and not hidden from downstream output. | Hide limitations in generated output. |
| `M28.10` Validation checkpoint | `Validation` | Validate standards behavior. | Standards behavior/source validation evidence, including `python -m pytest -q` if executable behavior changed and standards registry/source consistency validation where applicable. | Validation evidence must be recorded truthfully. | May advance only after required validation evidence exists or unresolved validation state is explicitly recorded. | Claim audit-ready output without verified sources. |
| `M28.11` Milestone UAT / owner acceptance | `UAT` | Accept standards authority use for the approved M28 scope. | Executed M28 UAT protocol/report covering applicability, citation, limitation visibility, and runtime-consumption boundaries where implemented. Owner acceptance alone is not sufficient for M28 closeout. | UAT evidence is required. Validation reference is required where executable behavior was validated. | May advance only after actual M28 UAT evidence exists and limitations are accepted. | Treat as regulatory/legal approval. |
| `M28.12` Milestone closeout | `Closeout` | Freeze standards authority boundary. | Closeout record referencing M28 validation, actual UAT, DDR-004 scope, DDR-005 carry-forward if retrieval remains deferred, and DDR-006 awareness. | Document consistency review. No executable validation unless new executable behavior changes. | May advance only after M28.12 closeout record exists and all required carry-forward limitations are explicit. | Start retrieval before authority is ready. |

#### Exit criteria

- Standards applicability and citation behavior is controlled.
- Registry limitations remain visible.
- Runtime consumption exists only where implemented and validated.
- DDR-005 remains deferred until retrieval/indexing prerequisites are satisfied.

---

### Milestone 29 — Product-Ready Document Factory, Document Engine Workflow, and Output Rendering

**Goal:** Convert document/template/output foundations into a complete local product-ready document factory / document engine for CQV documents and reports, including document rationale/logic, DCF intake, deterministic template selection, controlled drafting, rendering, lifecycle, traceability, and review/approval workflow.

#### Entry gate

- M26 source authority boundary complete.
- M27 relevant task/document mappings available.
- M28 standards applicability/citation behavior available where standards-backed output is required.

#### DDR focus

- DDR-003
- DDR-006
- DDR-004/005 awareness where standards-backed output is involved

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M29.1` Product document family scope | Define initial product output families | URS, QP, protocol/report families, DCF where approved | Unlimited document family sprawl |
| `M29.1A` Document factory workflow and rationale model | Define document-engine logic | DCF path, skip-DCF path, input-to-section rationale, document-family workflow, review/approval flow | Treat templates as the whole document system |
| `M29.2` Template library implementation | Implement product template records | Template IDs, versions, status, source location, applicability, schema binding | Loose templates without identity/version |
| `M29.3` Template selection/loading | Implement deterministic template selection | Based on selector/profile/standards/task/document family | AI chooses templates freely |
| `M29.4` Document input schema binding | Define schema-to-template contracts | Required/optional fields, placeholders, DCF intake/extraction/normalization mapping, missing-data behavior | Generate without input contract |
| `M29.5` Controlled drafting modes | Define document generation modes | Strong input fill, partial bounded completion, minimal scaffold with placeholders, rationale-bound section drafting | Unbounded invention |
| `M29.6` Standards-backed output controls | Bind citations/applicability to output | Citation limitations, assumptions, source records | Standards-backed claims from memory |
| `M29.7` Renderer/output contract | Implement render/export behavior | Markdown/DOCX/PDF/CSV/Excel only where approved; artifact metadata | Claim rendering when only contracts exist |
| `M29.8` Document lifecycle and workflow integration | Connect output to task/workflow/review state | Draft/review/approved/final/superseded; review/approval obligations; task closure dependencies | Let generated prose mutate truth |
| `M29.9` Product-ready output validation | Validate output contracts | File existence, schema conformance, citation presence, placeholder policy | Accept malformed output |
| `M29.10` Trial document generation set | Generate controlled local sample set | Local CQV scenario outputs for review | Release as customer-ready without UAT |
| `M29.11` Validation checkpoint | Run validation | `python -m pytest -q` if code changed; artifact validation | Skip validation for renderer behavior |
| `M29.12` Milestone UAT / owner acceptance | Accept document/output layer | Owner reviews generated sample set and limitations | Treat as full product trial acceptance |
| `M29.13` Milestone closeout | Freeze output baseline | Close or carry DDR-003/006 precisely | Proceed with output gaps hidden |

#### Exit criteria

- Product document factory / document engine workflow is explicit.
- Product template library is implemented or explicitly scoped.
- DCF intake and document input-to-output logic are controlled.
- Template selection/loading is deterministic.
- Output generation/rendering behavior is validated where implemented.
- DDR-003 and DDR-006 are closed, partially closed, or carried forward with exact remaining scope.

---

### Milestone 30 — Governed Retrieval and Indexing for Authoritative Product Sources

**Goal:** Add retrieval/indexing only after authoritative sources exist and only where retrieval improves usability without becoming source truth.

#### Entry gate

- M26 source authority boundary complete.
- M27 product libraries available.
- M28 standards authority behavior available for standards-related retrieval.
- M29 output layer dependencies understood.

#### DDR focus

- DDR-005
- DDR-004 limitations
- DDR-007 awareness for AI retrieval use

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M30.1` Retrieval justification gate | Decide where retrieval is justified | Standards lookup support, template search, library search, advisory context | Retrieval everywhere by default |
| `M30.2` Source eligibility model | Define retrievable source classes | Only approved/eligible sources; status-aware inclusion | Index pending/TBD as mandatory authority |
| `M30.3` Index metadata and traceability | Define index records | Source ID, version, chunk/ref, build date, registry version | Anonymous chunks with no source trace |
| `M30.4` Retrieval non-authority enforcement | Implement role limits | Retrieval suggests/fetches; registry/source remains authority | Retrieval decides compliance truth |
| `M30.5` Standards retrieval controls | Implement if approved | Source-status filters, citation fallback, limitation warnings | Clause claims without verified clause data |
| `M30.6` Library/template retrieval controls | Implement if approved | Asset ID/version filtering, template/library context fetch | Replace deterministic resolver with probabilistic search |
| `M30.7` Retrieval evaluation harness | Evaluate retrieval usefulness | Recall/precision-style checks, source trace checks, failure cases | Accept retrieval without evaluation |
| `M30.8` Retrieval-to-AI handoff contract | Define AI consumption boundary | Context packets, citations, limitations, refusal triggers | Raw retrieval dumped into model as truth |
| `M30.9` Validation checkpoint | Validate retrieval behavior | `python -m pytest -q` if code changed; retrieval evaluation evidence | Skip evaluation |
| `M30.10` Milestone UAT / owner acceptance | Accept retrieval usefulness | Owner trial of retrieval-supported local workflows | Productize retrieval without acceptance |
| `M30.11` Milestone closeout | Freeze retrieval boundary | Close/carry DDR-005 precisely | Expand retrieval beyond approved sources |

#### Exit criteria

- Retrieval is justified, bounded, and source-traceable.
- Retrieval does not override source/citation authority.
- DDR-005 is closed, partially closed, or carried forward with precise remaining scope.

---

### Milestone 31 — Governed AI Assistance Over Local Product Sources

**Goal:** Provide local-product AI assistance only above governed source, standards, retrieval, document, and output boundaries, with an explicit local AI model/runtime strategy for app-coupled heavy-use testing where AI assistance is included.

#### Entry gate

- M26-M29 foundations available for the assistance scope.
- M30 retrieval boundary available if AI uses retrieval.
- DDR-007 reviewed before any provider/live model work.

#### DDR focus

- DDR-007
- DDR-005 if retrieval used
- DDR-006 if generated output used

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M31.1` AI assistance scope lock | Decide assistance modes | Advisory Q&A, document drafting support, review support, comparison support, workflow guidance | Uncontrolled agentic execution |
| `M31.2` Local AI model and provider strategy decision | Decide local/offline/API/provider strategy | Local app-coupled model option, external provider option, constraints, privacy, cost, operational limits | Live/provider/local model calls without approved path |
| `M31.3` Provider/adapter boundary if approved | Define adapter boundary | No raw provider leakage, no state mutation by model | Direct model calls from core/UI |
| `M31.4` Context packet contract | Define context inputs | Source IDs, registry version, task/workflow state, retrieval results, limitations | Free-form prompt with untracked facts |
| `M31.5` Refusal and limitation rules | Define safe refusal | Missing sources, unverified standards, unsupported claims, out-of-scope requests | Model guesses missing compliance truth |
| `M31.6` Output acceptance and review rules | Define accepted AI outputs | Draft/advisory/review states; human acceptance where needed | AI approval authority |
| `M31.7` Evaluation and regression harness | Test AI behavior if implemented | Prompt/output contract tests, source-grounding checks, refusal cases | Untested AI behavior |
| `M31.8` Local AI heavy-use shakedown protocol | Plan app-coupled heavy-use local trial where AI is in scope | Local model runtime scenario, repeated use, metrics, failures, issue capture | Go-live or product AI claim without shakedown |
| `M31.9` Validation checkpoint | Validate executable integration | `python -m pytest -q` if code changed; evaluation evidence | Claim provider readiness without tests |
| `M31.10` Milestone UAT / owner acceptance | Accept AI assistance boundary | Owner accepts assistance modes and limitations | Product/SaaS-facing live AI release |
| `M31.11` Milestone closeout | Freeze AI assistance baseline | Close/carry DDR-007 precisely | Hide operational/provider risks |

#### Exit criteria

- AI assistance scope is bounded.
- Local AI model/runtime strategy is explicit where app-coupled heavy-use testing includes AI.
- Provider/model strategy is explicit.
- Context, refusal, acceptance, and evaluation behavior are controlled.
- DDR-007 is closed, partially closed, or carried forward with exact remaining scope.

---

### Milestone 32 — Local Usable CQV Workflow/UI MVP

**Goal:** Build a local usable workflow/UI path that lets a real user operate the product core without relying on raw CLI-only internal mechanics.

#### Entry gate

- M26-M29 product-core sources and outputs available for the intended workflow.
- M31 AI assistance and local AI model/runtime path available only if included in MVP scope.

#### DDR focus

- DDR-009 placeholder compatibility awareness
- DDR-001/002 source behavior dependencies
- DDR-006 output behavior dependencies

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M32.1` Local workflow MVP scope lock | Define user journey | Create/select project, bind preset/profile, stage tasks, commit tasks, schedule, generate document/output, review | Full SaaS/admin/tenant scope |
| `M32.2` UI/runtime surface selection | Decide local surface | CLI-enhanced, local web, desktop-like, or controlled forms | Cloud-first architecture bypass |
| `M32.3` Operator workflow model | Define workflow states | Project/WP/preset binding, task staging, planning, document generation, review, acceptance | Hidden state mutation from UI |
| `M32.4` UI-to-core adapter contract | Define adapter boundary | UI consumes services/contracts; no domain logic in UI | UI writes raw state/files |
| `M32.5` Forms and controlled input surfaces | Build input forms | DCF path, minimal input path, presets/selectors, standards/profile choices | Unvalidated free-form input as truth |
| `M32.6` Workflow visibility surfaces | Build visibility | WP status, task status, schedule, document lifecycle, source/citation limitations | Misleading readiness indicators |
| `M32.7` Output review/download surfaces | Build controlled review | Document/export view, artifact metadata, validation limitations | Silent output acceptance |
| `M32.8` Local workflow error/failure handling | Handle failures safely | Missing inputs, invalid refs, source limitations, validation errors | UI masks failures |
| `M32.9` End-to-end local scenario implementation | Run one local CQV workflow scenario | Cleanroom/HVAC or approved first scenario | Call it product-ready before trial |
| `M32.10` Validation checkpoint | Validate local workflow | `python -m pytest -q` if code changed; scenario validation | Skip workflow testing |
| `M32.11` Milestone UAT / owner acceptance | Accept local MVP usability | Owner confirms local workflow is trial-ready | Treat as commercial readiness |
| `M32.12` Milestone closeout | Freeze local MVP baseline | Identify remaining trial blockers | Proceed to trial with hidden gaps |

#### Exit criteria

- Local user workflow is usable enough for real trial.
- UI/workflow surfaces remain downstream adapters.
- Source, standards, output, and validation limitations are visible to the user.

---

### Milestone 33 — Local Integrated Product Validation, Trial, and UAT

**Goal:** Prove the local integrated CQV product core works in realistic local use before productization/SaaS re-entry.

#### Entry gate

- M32 local workflow MVP accepted as trial-ready.
- Known DDR blockers are either closed, carried with explicit limitations, or excluded from trial scope.

#### DDR focus

- Full DDR review before product-core acceptance
- DDR-005/006/007 especially if retrieval/output/AI/local AI model runtime are in trial scope

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M33.1` Trial scope and protocol | Define trial boundaries | Scenario, systems, user role, acceptance criteria, limitations | Trial without scope |
| `M33.2` Test dataset / scenario pack | Prepare local CQV scenario | Cleanroom/HVAC/equipment/computerized system as approved | Real confidential data without control |
| `M33.3` End-to-end validation suite | Validate integrated path | Source selection, staging, planning, standards, document factory workflow, UI/API, AI/local model if included | Unit-only confidence for product trial |
| `M33.4` Trial execution round 1 | Run realistic local workflow | Capture issues, errors, friction, wrong outputs, local AI model behavior where in scope | Ignore observed failures |
| `M33.5` Issue triage and correction plan | Classify trial findings | Bug/fix/refactor/doc/library/standards/UI/AI issue types | Patch randomly outside roadmap |
| `M33.6` Corrective implementation package | Apply approved corrections | User-applied code/docs package; tests | Scope creep beyond trial findings |
| `M33.7` Regression and re-trial | Re-run affected paths | Confirm corrections and no regressions | Close without re-check |
| `M33.8` Local product UAT report | Produce UAT evidence | Scope, results, limitations, acceptance decision | Productization claim without UAT |
| `M33.9` Validation checkpoint | Final validation | `python -m pytest -q` if code changed; integrated scenario validation | Claim validation by memory |
| `M33.10` Owner acceptance gate | Accept/reject local product core | Pass/conditional pass/fail with rationale | Treat conditional pass as full readiness |
| `M33.11` Milestone closeout | Freeze trial evidence | Define remaining gaps and next gate | Re-enter productization automatically |

#### Exit criteria

- Integrated local product trial evidence exists.
- Validation results are recorded truthfully.
- UAT decision is recorded.
- Remaining limitations are explicit.

---

### Milestone 34 — Local Product-Core Closeout and Productization Re-entry Gate

**Goal:** Decide whether the local integrated CQV product core is complete enough to re-enter productization/SaaS readiness.

#### Entry gate

- M33 local integrated product validation and UAT complete.
- Full DDR register reviewed.
- Product-core gaps and trial findings resolved, accepted, or explicitly carried.

#### Checkpoint ladder

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M34.1` Product-core completeness assessment | Assess all core categories | Libraries, standards, document factory/output, retrieval, local AI model/AI assistance, UI/API, validation, UAT | Assume readiness from one scenario only |
| `M34.2` DDR closure/reclassification review | Review all DDR statuses | Close/reclassify/carry dependencies with evidence | Close dependencies without evidence |
| `M34.3` Product-core limitation register | Record known limits | Supported scopes, unsupported scopes, source limitations, standards limits | Hide limitations |
| `M34.4` Release-candidate boundary decision | Decide local RC boundary | Define what is in/out of first productizable form | Expand to SaaS prematurely |
| `M34.5` Productization re-entry readiness assessment | Decide if Phase 10 may begin | Evidence-based pass/conditional pass/fail | Resume productization automatically |
| `M34.6` Validation checkpoint | Validate any final changes | `python -m pytest -q` if code changed | Claim closure without validation |
| `M34.7` Product-core UAT/owner acceptance | Accept product-core closeout | Owner decision with rationale | Treat as commercial launch approval |
| `M34.8` Phase 9 closeout | Freeze local product-core path | Tracker points to Phase 10 only if approved | Skip re-entry gate |

#### Exit criteria

- Product-core completeness decision exists.
- DDR statuses are aligned with evidence.
- Product-core limitations are recorded.
- Productization/SaaS re-entry is explicitly approved or denied.

---

## 11. Phase 10 — Productization / SaaS Re-entry

### Phase goal

Resume productization only after the local integrated CQV product core has been built, validated, trialed, accepted, and explicitly approved for productization re-entry.

### Phase 10 entry gate

Phase 10 may begin only if all are true:

- M34 closeout approves productization re-entry.
- Local product core is accepted.
- DDR blockers are closed, reclassified, or explicitly carried with approved limitations.
- Product-core limitations are recorded.
- Owner approves a product boundary decision path.

### Phase 10 must not include

- erasing local product limitations
- tenant/SaaS behavior before product boundary decision
- live provider integration unless DDR-007 path is closed/approved
- commercial release before licensing/support/security/release governance decisions
- production deployment before operational testing and go/no-go evidence

---

### Milestone 35 — Product Boundary, License, Repository, and Commercial Direction Decision

**Goal:** Decide what ASBP becomes as a product: open-source, proprietary, open-core, split repo, local-only, cloud-ready, SaaS-bound, or another controlled path.

Checkpoint ladder:

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M35.1` Product identity and boundary assessment | Define product vs build project | Product name, audience, supported scope, excluded scope | Commercial claim without boundary |
| `M35.2` License strategy assessment | Decide license path | GPLv3 continuation, dual license, proprietary future repo, open-core, legal review need | Legal/license change without approval |
| `M35.3` Repository visibility / split decision | Decide repo structure | Public/private split, future product repo, archive/public docs | Make repo private silently |
| `M35.4` Commercial model direction | Decide commercial posture | Local product, services, SaaS later, internal tool, open-source | Pricing/sales implementation |
| `M35.5` Product support boundary | Define support obligations | Bug/security/support channels, SLA/no-SLA policy | Promise unsupported obligations |
| `M35.6` Validation checkpoint | Validate docs-only consistency | No pytest unless executable claims changed | Claim code validation if not run |
| `M35.7` Owner acceptance | Approve product boundary | Decision record | Begin packaging without boundary |
| `M35.8` Milestone closeout | Freeze product boundary | Tracker to M36 if approved | Skip license/support/security decisions |

---

### Milestone 36 — Product Packaging, Release Governance, Security, and Supportability

**Goal:** Make the accepted local product governable as a release candidate.

Checkpoint ladder:

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M36.1` Packaging strategy | Define package/build path | `pyproject.toml`, console script, local install path, versioning | Production package without tests |
| `M36.2` Release artifact policy | Define release artifacts | Version tags, artifact metadata, release notes, checksums if needed | Ad hoc release files |
| `M36.3` Security policy | Define vulnerability/security reporting | `SECURITY.md`, contact/process, scope | Claim enterprise security posture |
| `M36.4` Supportability policy | Define support/maintenance | Issue templates, support boundary, lifecycle policy | SLA without approval |
| `M36.5` Product documentation package | Build user-facing docs | Install/use guide, limitations, supported scopes | Replace governance docs with marketing |
| `M36.6` Release validation package | Validate packaged product | Install test, command test, artifact checks, `python -m pytest -q` where code changed | Release without validation |
| `M36.7` UAT / owner acceptance | Accept packaging/release governance | Owner signoff | Commercial launch |
| `M36.8` Milestone closeout | Freeze release candidate governance | Record remaining release blockers | Skip operational shakedown |

---

### Milestone 37 — Operational Shakedown, Provider/Deployment Gate, and Go/No-Go Readiness

**Goal:** Decide whether any provider, deployment, operational, or pre-go-live path is safe to pursue.

Checkpoint ladder:

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M37.1` Operational scope lock | Decide local/private/cloud/SaaS operational scope | Scope, environment, users, data sensitivity | Production deployment by default |
| `M37.2` Provider integration gate | Revisit DDR-007 | Provider boundary, smoke tests, cost/privacy/risk controls | Live calls without approved adapter/test plan |
| `M37.3` Deployment environment gate | Decide environment path | Local package, internal server, cloud staging, SaaS later | Tenant behavior without SaaS gate |
| `M37.4` Monitoring and failure handling | Define operational controls | Logs, health checks, failure escalation, rollback | Silent failure |
| `M37.5` Local heavy-use / operational shakedown | Execute shakedown | Repeated realistic use, issue capture, performance/friction notes | Go-live after single happy path |
| `M37.6` Corrective action loop | Fix shakedown issues | Prioritized fixes with validation | Hide unresolved issues |
| `M37.7` Go/no-go evidence pack | Produce readiness evidence | Validation, UAT, issue status, limitations, decision | Launch without go/no-go |
| `M37.8` UAT / owner acceptance | Accept operational readiness result | Pass/conditional/fail | Treat conditional pass as SaaS-ready |
| `M37.9` Milestone closeout | Freeze operational gate | Decide M38 entry | Skip unresolved DDR-007 |

---

### Milestone 38 — SaaS / Product Boundary Consolidation

**Goal:** Consolidate the final product/SaaS-facing boundary only after local product, packaging, release governance, and operational readiness gates are satisfied.

Checkpoint ladder:

| Checkpoint | Purpose | Allowed work | Not allowed |
|---|---|---|---|
| `M38.1` SaaS suitability reassessment | Decide if SaaS remains valid | Product fit, data/privacy, tenant need, cost, support | SaaS because it sounds commercial |
| `M38.2` Tenant/customer boundary plan | Define if SaaS approved | Tenant model, customer data separation, access assumptions | Tenant implementation without approval |
| `M38.3` Compliance and audit boundary | Define compliance limits | Validation package, audit trail needs, standards limitations | Regulated claims without evidence |
| `M38.4` Commercial release gate | Decide release posture | Release candidate, pilot, private beta, public release, no-go | Full launch by default |
| `M38.5` Final validation and regression | Validate release boundary | Full tests, scenario checks, documentation checks | Release without regression |
| `M38.6` Final UAT / owner acceptance | Owner acceptance | Pass/conditional/fail | Skip owner signoff |
| `M38.7` Phase 10 closeout | Close or pause productization | Record next strategic path | Hide remaining gaps |

---

## 12. DDR Placement Matrix

| DDR | v5 placement | Required interpretation |
|---|---|---|
| DDR-001 Governed-library runtime promotion / deployment-compiled lookup | M26, M27 | Closed governance/model evidence does not equal executable runtime-authoritative product library behavior |
| DDR-002 Consolidated runtime-authoritative libraries | M26, M27 | Product library package/layout must be implemented/validated before productized dependence |
| DDR-003 Product-ready document templates library | M29 | Governance/model closure does not equal executable product template implementation/loading/selection or complete document factory workflow |
| DDR-004 Standards source registry and citation authority | M28 | Registry model exists; runtime consumption/verification limits must remain explicit |
| DDR-005 Standards embedding / retrieval index | M30 | Retrieval remains deferred until authority and applicability prerequisites are ready |
| DDR-006 Product-ready document/export/report generation/rendering | M29 | Product-ready output requires document factory workflow, generation/rendering contract, implementation, validation, and UAT |
| DDR-007 Model/provider integration and pre-go-live operational testing | M31, M33, M37 | Live provider/product AI and local app-coupled AI model runtime remain blocked until strategy, boundary, smoke tests, heavy-use shakedown, validation, and acceptance exist |
| DDR-008 Phase 8/9 readiness gate | M25, M34 | Historical gate-control closure only; not product readiness |
| DDR-009 External contract placeholders | M27, M32 | API/external contract placeholder compatibility does not authorize productized placeholder-backed behavior |

---

## 13. Non-Code Document Cleanup Policy After v5

### 13.1 Cleanup lane classification

The post-v5 cleanup lane is:

`Comprehensive non-code repository document cleanup`

It is not code cleanup, not tests cleanup, and not implementation refactor.

### 13.2 In-scope documents

Every non-code repository document is in scope for assessment, including:

- root roadmap files
- roadmap addenda
- roadmap continuation/support files
- tracker
- architecture guardrails
- governance registers
- decision gates
- standards registry and standards support files
- milestone evidence
- UAT evidence
- closeout notes
- archive files
- public-surface docs such as README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY if present
- GitHub PR and issue templates
- document approval registers
- planning/reference/design notes
- any Markdown/text/YAML documentation file outside code/test runtime behavior

### 13.3 Out-of-scope by default

- source code
- tests
- package runtime behavior
- executable contracts
- dependencies
- workflow automation that affects execution

If cleanup discovers code-adjacent changes are required, those must be reclassified into a code/refactor/tests lane before action.

### 13.4 Required disposition categories

Each document must receive one disposition:

| Disposition | Meaning |
|---|---|
| Keep active | Retain as active authority/current surface |
| Keep historical | Retain as traceability/evidence only |
| Revise | Correct wording/status/links/supersession without changing authority unexpectedly |
| Relocate | Move to a clearer location while preserving traceability |
| Archive | Move out of active surface while preserving evidence |
| Supersede | Replace with a newer controlled version and preserve reference trail |
| Delete | Remove only if redundant, obsolete, not needed for traceability, and approved |

### 13.5 Cleanup acceptance criteria

Cleanup is complete only when:

- every non-code document has been inventoried
- each document has a proposed disposition
- owner approves the disposition matrix
- approved cleanup package is prepared
- only approved actions are applied
- final alignment confirms root authority surfaces are clear
- tracker, roadmap, DDR, guardrails, docs index, and public surface do not contradict the approved v5 path

---

## 14. First Active Checkpoint After v5 Approval/Application

After this roadmap is approved and applied, the tracker should point to the first not-yet-complete v5 checkpoint.

Expected first active checkpoint after application:

`M25.4 — Roadmap change-control record application`

If the change-control record and roadmap v5 are applied together in one approved package, the tracker may instead point to:

`M25.6 — Tracker and DDR alignment after v5`

If tracker alignment is included in the same approved application package, the tracker may then point to:

`M25.7 — Comprehensive non-code document inventory`

The tracker must record the exact truth based on what was actually applied.

---

## 15. v5 Approval Acceptance Criteria

Roadmap v5 may be approved only if Project Owner confirms that it:

- absorbs the local integrated CQV product redirect
- replaces active reliance on roadmap addenda for future direction
- preserves closed milestones for their original scope
- distinguishes governance/model closure from executable/product closure
- places DDR-001 through DDR-009 explicitly
- includes the comprehensive non-code document cleanup lane
- defines a granular local CQV product build path
- defines product-core validation and UAT expectations
- defines productization/SaaS re-entry conditions
- does not authorize implementation, cleanup, PR/issue creation, license change, or live repo writes by itself

---

## 16. Final v5 Direction Statement

ASBP must not resume normal productization/SaaS readiness execution from archived Addendum 10.

The next strategic path is:

1. complete roadmap reset and non-code document cleanup gates
2. build local integrated CQV product source authority
3. implement runtime-authoritative CQV libraries and mappings
4. implement standards applicability/citation authority where justified
5. implement a complete product-ready document factory / document engine workflow, including DCF, document logic, template selection, generation, rendering, lifecycle, and review/approval controls
6. add retrieval only after authoritative sources exist
7. add AI assistance only over governed sources and accepted boundaries
8. define and test the local app-coupled AI model/runtime path during controlled heavy-use testing where AI is in scope
9. build local usable workflow/UI and API/external contract surfaces only as downstream adapters
10. validate and trial the local product
11. close product-core readiness
12. only then decide whether productization/SaaS re-entry is allowed

This is the canonical v5 direction proposed for Project Owner review.
