---
doc_type: checkpoint_control_interpretation
canonical_name: M29_1_CONTROL_CHECK_BEFORE_PLAN
status: READY_FOR_PLAN_M29_1
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.1
checkpoint_title: Product document family scope
execution_mode: Governance-only
application_mode: user_applied_package
live_repo_write: NO
---

# M29.1 Control Check Before PLAN

## Purpose

This control check resolves the minimum execution-control fields required before `PLAN M29.1 — Product document family scope`.

It exists because the M29 roadmap table defines checkpoint, purpose, allowed work, and not-allowed work, but it does not explicitly list all execution-control fields required by the build/governance balance policy.

This control check does not execute M29.1.

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

M29.1 roadmap row:

- Checkpoint: `M29.1` Product document family scope
- Purpose: Define initial product output families
- Allowed work: URS, QP, protocol/report families, DCF where approved
- Not allowed: Unlimited document family sprawl

## Control Interpretation for M29.1

### Execution Mode

`Hybrid / Build-content`

M29.1 is not governance-only by inference.

It defines initial product output families for the local integrated CQV product document factory path. Because those family definitions will become downstream source truth for templates, schemas, DCF intake, drafting modes, rendering, validation, and UAT, M29.1 must produce controlled source-scope artifacts rather than narrative discussion alone.

### Required Completion Artifact

M29.1 must produce a controlled product document family scope artifact.

Expected artifact:

`docs/milestones/M29/M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE.md`

The artifact must define the initial product document family scope and identify which document families are in scope, which are out of scope, and which are deferred.

### Implementation / Source Minimum

M29.1 must define controlled document-family source scope sufficient to govern later M29 work.

Minimum content:

1. Initial approved document families.
2. Stable family identifiers.
3. Family purpose and CQV use boundary.
4. DCF relevance.
5. Standards-backed output relevance.
6. Expected downstream consumers such as templates, input schemas, drafting modes, rendering, lifecycle, review/approval, validation, and UAT.
7. Explicit out-of-scope and deferred document families.
8. Anti-sprawl rule preventing unlimited document family expansion.
9. Explicit non-product-ready boundary.

Recommended initial family scope:

- `DOCF-URS` — User Requirements Specification family.
- `DOCF-QP` — Qualification Plan / qualification strategy family.
- `DOCF-PROTOCOL-REPORT` — Protocol and report family for IQ/OQ/PQ or related qualification/testing outputs.
- `DOCF-DCF` — Data Collection Form / structured intake family where approved.

The exact set may be narrowed during M29.1, but it must not expand beyond the roadmap-approved family types without a future controlled decision.

### Validation Requirement

M29.1 requires document/source consistency review.

`python -m pytest -q` is required only if M29.1 changes code, tests, schemas, runtime behavior, validators, loaders, source contracts, CLI behavior, executable commands, or executable behavior.

If M29.1 creates only the controlled document family scope artifact and no executable source contract, no pytest is required.

### Tracker Movement Rule

The tracker may move from `PLAN M29.1` to the next checkpoint only after:

1. the M29.1 document family scope artifact exists;
2. initial approved document families are explicitly listed;
3. out-of-scope and deferred families are explicit;
4. DDR-003 and DDR-006 impact is recorded;
5. DDR-004 / DDR-005 awareness is recorded where standards-backed output is involved;
6. anti-sprawl boundaries are visible;
7. non-implementation claims are explicit.

M29.1 must not be closed by a vague narrative note.

### DDR Impact

M29.1 touches:

- DDR-003 — Product-ready document templates library
- DDR-006 — Product-ready document/export/report generation and rendering
- DDR-004 awareness — Standards source/citation authority where standards-backed output is involved
- DDR-005 awareness — Retrieval/indexing remains deferred to M30

M29.1 does not close, reopen, downgrade, or reclassify any DDR.

M29.1 must carry forward that:

- DDR-003 remains closed only for the approved governance/model scope until product-ready template implementation and document factory integration evidence exists.
- DDR-006 remains closure-planned and is not closed by family scoping alone.
- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- DDR-005 remains deferred to M30.

### Architecture Boundary Impact

M29.1 must not change CLI behavior, state/persistence boundaries, UI/API behavior, AI/runtime behavior, deployment behavior, productization behavior, or SaaS behavior.

If future M29.1 execution attempts to add runtime loaders, validators, schemas, source contracts, or code, architecture impact must be reviewed before implementation and tests must be added where required.

### Explicit Non-Implementation Claims

This control check does not implement:

- M29.1 product document family scope;
- product-ready document families;
- template records;
- DCF intake;
- template selection or loading;
- document input schemas;
- controlled drafting modes;
- standards-backed output generation;
- rendering, export, or reporting;
- document lifecycle or review workflow;
- artifact validation;
- trial document generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness.

M29.1 itself, when executed later, must not implement:

- template library implementation;
- template selection/loading;
- schema binding;
- drafting modes;
- rendering/export/reporting;
- document lifecycle integration;
- trial document generation;
- M29 validation;
- M29 UAT;
- M29 closeout.

Those remain later M29 checkpoints.

## Control Decision

M29.1 may proceed to `PLAN M29.1` after this control-check artifact is applied.

`PLAN M29.1` must use the control interpretation above and must not infer governance-only completion.

## Tracker Movement

This control check does not update `PROGRESS_TRACKER.md`.

After this artifact exists, `UPT CONTROL CHECK M29.1` may update the tracker exact next unfinished checkpoint to:

`PLAN M29.1 — Product document family scope`

provided no conflicting authority is introduced.
