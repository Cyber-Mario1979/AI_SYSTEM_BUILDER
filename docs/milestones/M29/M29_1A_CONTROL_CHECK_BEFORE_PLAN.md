---
doc_type: checkpoint_control_interpretation
canonical_name: M29_1A_CONTROL_CHECK_BEFORE_PLAN
status: READY_FOR_PLAN_M29_1A
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.1A
checkpoint_title: Document factory workflow and rationale model
execution_mode: Governance-only
application_mode: user_applied_package
live_repo_write: NO
created_date: 2026-05-29
target_repo_path: docs/milestones/M29/M29_1A_CONTROL_CHECK_BEFORE_PLAN.md
---

# M29.1A Control Check Before PLAN

## Purpose

This control check resolves the minimum execution-control fields required before `PLAN M29.1A — Document factory workflow and rationale model`.

It exists because the M29 roadmap table defines the M29.1A checkpoint, purpose, allowed work, and not-allowed work, but does not explicitly list all execution-control fields required by the build/governance balance policy.

This control check does not execute M29.1A.

## Source Basis

M29 roadmap goal:

Convert document/template/output foundations into a complete local product-ready document factory / document engine for CQV documents and reports, including document rationale/logic, DCF intake, deterministic template selection, controlled drafting, rendering, lifecycle, traceability, and review/approval workflow.

M29 entry gate:

- M26 source authority boundary complete.
- M27 relevant task/document mappings available.
- M28 standards applicability/citation behavior available where standards-backed output is required.

M29 DDR focus:

- DDR-003
- DDR-006
- DDR-004 / DDR-005 awareness where standards-backed output is involved

M29.1A roadmap row:

- Checkpoint: `M29.1A` Document factory workflow and rationale model
- Purpose: Define document-engine logic
- Allowed work: DCF path, skip-DCF path, input-to-section rationale, document-family workflow, review/approval flow
- Not allowed: Treat templates as the whole document system

M29.1 source basis:

- `docs/milestones/M29/M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE.md` defines the approved product document family scope.
- M29.1A must use the M29.1 family scope as input and must not expand the approved family set without a future controlled decision.

## Control Interpretation for M29.1A

### Execution Mode

`Hybrid / Build-content`

M29.1A is not governance-only by inference.

It defines the document-factory workflow and rationale model that later M29 checkpoints will use for template records, DCF intake, input schemas, drafting modes, standards-backed output controls, rendering, lifecycle integration, validation, trial document generation, UAT, and closeout.

Because M29.1A will become downstream source truth for document-engine behavior, it must produce a controlled source/workflow artifact rather than narrative discussion alone.

### Required Completion Artifact

M29.1A must produce a controlled document factory workflow and rationale model artifact.

Expected artifact:

`docs/milestones/M29/M29_1A_DOCUMENT_FACTORY_WORKFLOW_AND_RATIONALE_MODEL.md`

The artifact must define the document-engine workflow and rationale model using the approved M29.1 document-family scope.

### Implementation / Source Minimum

M29.1A must define controlled source/workflow scope sufficient to govern later M29 work.

Minimum content:

1. DCF path workflow.
2. Skip-DCF path workflow.
3. Minimum input rules for both paths.
4. Input-to-section rationale model.
5. Document-family workflow model using the approved M29.1 family scope.
6. Review/approval flow model.
7. Document-engine stage model covering intake, classification, family workflow selection, rationale creation, drafting handoff, review handoff, output handoff, and closeout handoff.
8. Local reality constraint handling, including missing inputs, substitutions, vendor-document gaps, and limitation statements.
9. Standards-backed relevance handling, including when standards/citation awareness is required and when standards retrieval remains out of scope.
10. Expected downstream consumers such as M29.2 template records, M29.3 template selection/loading, M29.4 schema binding, M29.5 controlled drafting modes, M29.6 standards-backed output controls, M29.7 renderer/output contract, M29.8 lifecycle integration, M29.9 output validation, M29.10 trial document generation, M29.12 UAT, and M29.13 closeout.
11. Explicit out-of-scope and deferred boundaries.
12. Anti-template-only rule preventing templates from being treated as the whole document system.
13. Explicit non-product-ready boundary.

M29.1A may define workflow and rationale contracts in a controlled artifact.

M29.1A must not implement product-ready generation, template loading, schema validation, rendering/export, lifecycle persistence, review/approval runtime behavior, UI/API behavior, AI/model/provider behavior, deployment, productization, or SaaS readiness.

### Required Workflow Coverage

The M29.1A artifact must at minimum distinguish:

| Workflow area | Required coverage |
|---|---|
| DCF path | How structured DCF intake feeds document-family workflow, section rationale, missing-input handling, drafting handoff, review, and later output. |
| Skip-DCF path | How minimal user inputs can still produce bounded scaffolds or placeholder-aware drafts without pretending missing data exists. |
| Input-to-section rationale | How each document section records why it exists, which inputs support it, what sources or constraints affect it, and what limitations remain. |
| Document-family workflow | How the approved M29.1 families move through the document engine without creating uncontrolled family expansion. |
| Review/approval flow | How drafts, technical review, QA/reviewer review, approval readiness, and local QMS boundaries are represented without implementing a workflow engine. |

### DCF Path Boundary

The DCF path may define:

- structured intake role;
- required and optional input categories;
- normalization expectations;
- missing-data visibility;
- family-specific intake differences;
- local reality constraints;
- standards-backed relevance flags;
- rationale handoff to document sections.

The DCF path must not implement final DCF forms, extraction logic, schemas, validators, UI/API input forms, database persistence, or product-ready workflow behavior.

### Skip-DCF Path Boundary

The skip-DCF path may define:

- minimum input acceptance rules;
- safe scaffold generation boundaries;
- placeholder policy;
- visible missing-data limitations;
- user-confirmation boundaries;
- rationale notes for missing or assumed inputs.

The skip-DCF path must not authorize unbounded completion, invented site data, invented standards claims, invented acceptance criteria, hidden assumptions, or product-ready output from incomplete data.

### Input-to-Section Rationale Boundary

M29.1A must define how document sections are justified by visible rationale.

The rationale model should identify, where applicable:

- section purpose;
- source input;
- required user input;
- optional user input;
- upstream document family or source reference;
- standards-backed relevance;
- local reality constraints;
- assumptions;
- missing-data placeholders;
- reviewer attention points;
- downstream consumer.

The rationale model must not fabricate technical, regulatory, site, vendor, test, acceptance, or standards content.

### Review / Approval Flow Boundary

M29.1A may define review/approval flow at workflow-model level.

It may define:

- draft;
- internal technical review;
- QA / validation review where applicable;
- user or owner approval readiness;
- finalization handoff;
- local QMS reference boundaries.

It must not implement a review engine, signature workflow, eQMS integration, approval persistence, electronic signature controls, or QMS system-of-record behavior.

## Validation Requirement

M29.1A requires document/source consistency review.

`python -m pytest -q` is required only if M29.1A changes code, tests, schemas, runtime behavior, validators, loaders, source contracts, CLI behavior, executable commands, or executable behavior.

If M29.1A creates only the controlled workflow/rationale model artifact and no executable source contract, no pytest is required.

## Tracker Movement Rule

The tracker may move from `PLAN M29.1A` to the next checkpoint only after:

1. the M29.1A document factory workflow and rationale model artifact exists;
2. the DCF path workflow is explicit;
3. the skip-DCF path workflow is explicit;
4. the input-to-section rationale model is explicit;
5. the document-family workflow model uses the approved M29.1 family scope;
6. the review/approval flow model is explicit;
7. local reality constraint handling is explicit;
8. standards-backed relevance handling is explicit;
9. DDR-003 and DDR-006 impact is recorded;
10. DDR-004 / DDR-005 awareness is recorded where standards-backed output or retrieval would be relevant;
11. anti-template-only boundaries are visible;
12. non-implementation claims are explicit.

M29.1A must not be closed by a vague workflow note.

## DDR Impact

M29.1A touches:

- DDR-003 — Product-ready document templates library
- DDR-006 — Product-ready document/export/report generation and rendering
- DDR-004 awareness — Standards source/citation authority where standards-backed output is involved
- DDR-005 awareness — Retrieval/indexing remains deferred to M30

M29.1A does not close, reopen, downgrade, or reclassify any DDR.

M29.1A must carry forward that:

- DDR-003 remains closed only for the approved governance/model scope until product-ready template implementation and document factory integration evidence exists.
- DDR-006 remains closure-planned and is not closed by workflow/rationale scoping alone.
- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- DDR-005 remains deferred to M30.

## Architecture Boundary Impact

M29.1A must not change CLI behavior, state/persistence boundaries, UI/API behavior, AI/runtime behavior, deployment behavior, productization behavior, or SaaS behavior.

If future M29.1A execution attempts to add runtime loaders, validators, schemas, executable source contracts, code, persistence, CLI behavior, UI/API behavior, or executable workflow behavior, architecture impact must be reviewed before implementation and tests must be added where required.

## Explicit Non-Implementation Claims

This control check does not implement:

- M29.1A document factory workflow and rationale model;
- DCF intake;
- skip-DCF execution behavior;
- input schemas;
- template records;
- template selection or loading;
- controlled drafting modes;
- standards-backed output generation;
- rendering, export, or reporting;
- document lifecycle persistence;
- review/approval runtime workflow;
- artifact validation;
- trial document generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness.

M29.1A itself, when executed later, must not implement:

- product-ready template library implementation;
- deterministic template selection/loading;
- schema binding;
- controlled drafting modes;
- standards-backed output controls beyond workflow/rationale relevance;
- rendering/export/reporting;
- lifecycle persistence;
- review/approval runtime behavior;
- trial document generation;
- M29 validation;
- M29 UAT;
- M29 closeout.

Those remain later M29 checkpoints.

## Control Decision

M29.1A may proceed to `PLAN M29.1A` after this control-check artifact is applied.

`PLAN M29.1A` must use the control interpretation above and must not infer governance-only completion.

## Tracker Movement

This control check does not update `PROGRESS_TRACKER.md`.

After this artifact exists, the tracker remains at:

`PLAN M29.1A — Document factory workflow and rationale model`

No tracker movement is required for this control check because the tracker already points to `PLAN M29.1A`.

## Completion Position

This control-check artifact is ready for user-applied repository placement at:

`docs/milestones/M29/M29_1A_CONTROL_CHECK_BEFORE_PLAN.md`

After placement, the next allowed action is:

`PLAN M29.1A`
