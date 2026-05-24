---
doc_type: milestone_evidence
canonical_name: M25_2_DDR_CLOSURE_PLAN
status: IN_PROGRESS
governs_execution: false
document_state_mode: milestone_checkpoint_planning_evidence
authority: checkpoint_evidence
source_register: docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md
source_disposition_review: docs/milestones/M25/M25_2_DEFERRED_DEPENDENCY_DISPOSITION_REVIEW.md
checkpoint: M25.2
milestone: M25 — SaaS Readiness Assessment
phase: Phase 9 — SaaS Readiness / Productization
approval_state: PARTIAL_PROJECT_OWNER_APPROVAL_DDR_004_CLOSED_DDR_001_002_CLOSED_DDR_003_CLOSED_DDR_006_CLOSURE_PLANNED_DDR_007_PLACEMENT_APPROVED
---

# M25.2 — DDR Closure Plan

## 1. Purpose

This document converts the M25.2 DDR disposition review into an executable closure plan.

The plan defines:

- which DDRs should be handled first
- which DDRs depend on other DDRs
- what repo evidence is needed to close each DDR
- what Project Owner input is needed
- what must be implemented, documented, verified, deferred, reclassified, or invalidated
- where each DDR belongs inside Phase 9 before normal roadmap execution resumes

This document remains an in-progress M25.2 closure plan.

DDR-004 closure has been approved by the Project Owner.

DDR-001 and DDR-002 closure-path sequencing has been approved by the Project Owner.

DDR-001 and DDR-002 governance/model closure has been approved by the Project Owner.

No DDR other than DDR-004, DDR-001, and DDR-002 is closed, reclassified, invalidated, or deferred by this plan.

DDR-001 and DDR-002 are closed for governance/model scope only; executable implementation remains M26-scoped.

DDR-003 is closed for governance/model scope only; executable implementation remains M26-scoped.

DDR-006 is Closure Planned only; executable generation/rendering implementation remains M26-scoped.

DDR-007 is Closure Planned for placement only; live provider/model implementation remains blocked until roadmap-authorized adapter, smoke-test, operational-test, local heavy-use shakedown, validation, and UAT evidence exist.

## 2. Control Principle

Before normal Phase 9 route resumes, every DDR must have a Project Owner-approved verdict:

- closed with repo evidence
- assigned to an immediate closure action
- deferred to a named checkpoint
- reclassified with repo-persistent decision evidence
- invalidated / marked not applicable with evidence
- carried forward as a blocker with a named gate

No DDR may remain in vague `Open`, `Deferred`, or `Watch` status without a named owner decision and checkpoint placement.

## 3. Dependency Chain

The closure order should follow dependency impact, not DDR number order.

```text
DDR-004
  └─ enables DDR-005
  └─ required before standards-backed document/product output
  └─ required before standards-backed CQV/GMP advice

DDR-001
  └─ supports DDR-002
  └─ contributes to DDR-003 and DDR-006 readiness

DDR-002
  └─ supports DDR-003 and DDR-006
  └─ required before productized runtime-authoritative library dependence

DDR-003
  └─ required before DDR-006 if product-ready document generation is in scope

DDR-006
  └─ depends on DDR-003, DDR-004, and relevant library readiness from DDR-001/DDDR-002

DDR-007
  └─ independent of document/template/library closure
  └─ closure planned for placement only
  └─ blocks product/SaaS-facing live model/provider integration until provider boundary, smoke tests, operational test plan, local heavy-use shakedown evidence, validation, and UAT exist

DDR-005
  └─ depends on DDR-004
  └─ should not start before DDR-004 closure is recorded and a retrieval/index checkpoint is authorized

DDR-009
  └─ requires repo evidence verification from M21 external contract work
  └─ can likely close/reclassify if placeholders/extensions were proven

DDR-008
  └─ can close/reclassify only after Phase 9 expansion and M25.2 full DDR disposition evidence are approved
```

## 4. Recommended Closure Order

| Order | DDR       | Why this position                                                                                                                                  |
| ----: | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
|     1 | `DDR-004` | Critical standards authority blocker. It gates standards-backed output, CQV/GMP advice, standards embedding, retrieval, and audit-ready citation.  |
|     2 | `DDR-001` | Very High runtime-authoritative governed-library promotion blocker. Needed before productized runtime lookup / deployment-compiled lookup.         |
|     3 | `DDR-002` | Very High consolidated runtime-authoritative libraries blocker. Builds on or pairs with `DDR-001`.                                                 |
|     4 | `DDR-003` | Very High product-ready template blocker. Needed before document-generation productization.                                                        |
|     5 | `DDR-006` | Very High product-ready generation/rendering blocker. Depends on templates, standards, libraries, schemas, and renderer/output contract readiness. |
|     6 | `DDR-007` | Critical live model/provider and pre-go-live blocker. Needs formal roadmap placement before any live runtime work.                                 |
|     7 | `DDR-005` | Standards retrieval/index blocker. Must wait for `DDR-004`.                                                                                        |
|     8 | `DDR-009` | M21 placeholder verification. Likely evidence-check/reclassify item rather than major build item.                                                  |
|     9 | `DDR-008` | Phase 8/9 readiness gate candidate closure/reclassification after M25.2 evidence approval.                                                         |

## 5. Closure Plan Table

| DDR                                                                                       | Proposed current verdict                                | Immediate action                                                                                                                                     | Depends on                                                                                                   | Repo evidence needed                                                                                                                                                                                                                                                                                                                                                                        | Project Owner input needed                                                                                                                                        | Proposed Phase 9 placement                                                                                             | Exit condition                                                                                                                                                         |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DDR-004` Standards source registry and citation authority                                | Closed with repo evidence accepted                      | Completed: standards authority closure checkpoint, registry/citation model, and closure decision evidence prepared.                                  | None. This was the upstream blocker.                                                                         | `docs/milestones/M25/DDR_004_STANDARDS_SOURCE_REGISTRY_AND_CITATION_AUTHORITY_PLAN.md`; `docs/standards/STANDARDS_SOURCE_REGISTRY.md`; `docs/milestones/M25/DDR_004_CLOSURE_DECISION.md`. Executable tests not required because no executable behavior changed.                                                                                                                             | Done: Project Owner approved the amended standards registry evidence on 2026-05-21.                                                                               | Closed under `M25.DDR-004`; downstream standards embedding/retrieval remains governed by `DDR-005`.                    | Register status moves to `Closed`; closure is limited to the standards source registry and citation authority model.                                                   |
| `DDR-001` Governed-library runtime promotion / deployment-compiled lookup                 | Closed for governance/model scope                       | Runtime-authoritative promotion path and deployment-compiled lookup boundary model approved; implementation remains M26-scoped.                      | None, but future implementation must remain harmonized with `DDR-002`.                                       | `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_CLOSURE_PLAN.md`; `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_MODEL.md`; `docs/milestones/M25/DDR_001_002_CLOSURE_DECISION.md`. Future implementation still requires runtime-authoritative promotion evidence, compiled lookup evidence if implemented, validation evidence, and UAT/acceptance where applicable. | Done for governance/model scope.                                                                                                                                  | Closed under `M25.DDR-001`; executable implementation remains M26-scoped, most likely `M26.5`, after M26.1 scope lock. | Register can move to `Closed` for governance/model scope; executable/productized behavior remains blocked until M26 implementation evidence exists.                    |
| `DDR-002` Consolidated runtime-authoritative libraries                                    | Closed for governance/model scope                       | Consolidated runtime-authoritative library structure model approved; implementation remains M26-scoped.                                              | Follows `DDR-001` and remains paired with it.                                                                | `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_CLOSURE_PLAN.md`; `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_MODEL.md`; `docs/milestones/M25/DDR_001_002_CLOSURE_DECISION.md`. Future implementation still requires consolidated package/layout evidence, source-role rules, version/status model, validation evidence, and UAT/acceptance where applicable.     | Done for governance/model scope.                                                                                                                                  | Closed under `M25.DDR-002`; executable implementation remains M26-scoped, most likely `M26.5`, after M26.1 scope lock. | Register can move to `Closed` for governance/model scope; executable/productized behavior remains blocked until M26 implementation evidence exists.                    |
| `DDR-003` Product-ready document templates library | Closed for governance/model scope | Product-ready template library model approved; implementation remains M26-scoped. | Depends on productization scope; implementation later depends on `DDR-001`, `DDR-002`, and `DDR-004` implementation readiness where productized behavior requires it. | `docs/milestones/M25/DDR_003_PRODUCT_READY_TEMPLATE_LIBRARY_MODEL.md`; `docs/milestones/M25/DDR_003_CLOSURE_DECISION.md`. Future implementation still requires template package/layout evidence, template IDs, schema binding, lifecycle/versioning rules, validation evidence, and UAT/acceptance where applicable. | Done for governance/model scope. | Closed under `M25.DDR-003`; executable implementation remains M26-scoped, most likely `M26.5`, after M26.1 scope lock. | Register can move to `Closed` for governance/model scope; executable/productized behavior remains blocked until M26 implementation evidence exists. |
| `DDR-006` Product-ready document/export/report generation and rendering | Closure Planned | Product-ready generation/rendering remains inside Phase 9; define generation/rendering closure path after templates/standards/libraries. | Depends on `DDR-003`, `DDR-004`, and relevant readiness from `DDR-001`/`DDR-002`. | `docs/milestones/M25/DDR_006_PRODUCT_READY_GENERATION_RENDERING_SCOPE_PLAN.md`. Future closure still requires generation boundary, renderer/output contract, template/schema/library/citation readiness evidence, validation evidence, and UAT/acceptance where applicable. | Done for scope/closure-path approval. | Approved under `M25.DDR-006-SCOPE`; executable implementation remains M26-scoped, most likely `M26.5`, after M26.1 scope lock. | Register can move to `Closure Planned`; `Closed` only after generation/rendering evidence and validation/UAT exist or it is formally reclassified. |
| `DDR-007` Actual model/provider integration and pre-go-live operational testing path | Closure Planned for placement only | Formal placement approved; do not implement product/SaaS-facing live calls now. Mandatory local heavy-use / operational shakedown gate added before SaaS go-live. | Independent of document-library chain, but blocked before live AI runtime/product operation. | `docs/milestones/M25/DDR_007_MODEL_PROVIDER_INTEGRATION_AND_LOCAL_SHAKEDOWN_PLACEMENT_DECISION.md`. Future closure still requires provider strategy decision, provider adapter boundary, smoke-test plan/evidence, operational test plan, local shakedown protocol/report, validation evidence, and UAT/acceptance evidence. | Done for placement decision. Provider strategy remains a later scope decision unless M25.5 or M26.1 locks it. | Approved: `M25.DDR-007-PLACEMENT`; execution only in later roadmap-authorized checkpoint. | `Closure Planned` after formal placement; `Closed` only after adapter/test/operational/local-shakedown/validation/UAT evidence exists or after formal reclassification. |
| `DDR-005` Standards embedding / retrieval index                                           | Defer behind `DDR-004`                                  | Do not implement or design retrieval index until source/citation authority is approved. Define later checkpoint after `DDR-004`.                     | Depends on `DDR-004`.                                                                                        | Retrieval/index design, source registry dependency satisfaction, retrieval-use rules, validation/evaluation evidence.                                                                                                                                                                                                                                                                       | Confirm whether standards retrieval/indexing is needed for Phase 9 productization or later.                                                                       | Proposed: after `DDR-004`, likely `M26.5-DDR-005` or later.                                                            | `Deferred to named checkpoint` after Project Owner approval; `Closed` only after index/retrieval evidence and evaluation exist.                                        |
| `DDR-009` External contract placeholders for future library/template/standards references | Verify now; likely close/reclassify if evidence exists  | Inspect M21 external contract docs/tests for placeholder or extension-point evidence.                                                                | None.                                                                                                        | M21 contract docs/tests proving placeholders or future references such as `template_id`, `schema_id`, `standards_bundle_ref`, `citation_ref`, `library_version`, or equivalent extension model without pretending dependencies are closed.                                                                                                                                                  | Confirm whether M21 placeholder compatibility still matters for Phase 9 or can be treated as historical satisfied condition.                                      | Proposed: `M25.DDR-009-VERIFY` before M26.                                                                             | `Closed` or `Reclassified` only after repo evidence check and Project Owner approval.                                                                                  |
| `DDR-008` Phase 8 / Phase 9 productization readiness gate                                 | Candidate closure/reclassification after M25.2 approval | Close or reclassify after Phase 9 expansion + full M25.2 DDR disposition evidence exists and is approved.                                            | Depends on approved M25.2 disposition and closure plan.                                                      | Phase 9 expansion addendum, M25.1 boundary assessment, M25.2 disposition review, this closure plan, and any approved register update.                                                                                                                                                                                                                                                       | Approve that Phase 8/9 readiness gate has been satisfied as a gate-control dependency, while downstream DDRs remain active.                                       | Proposed: follow-up register update after M25.2 approval.                                                              | `Closed` or `Reclassified` only after M25.2 evidence is approved and register is updated.                                                                              |

## 6. What Can Be Actioned Next

### Completed: `DDR-004`

`DDR-004` closure evidence has been accepted by Project Owner approval.

Closed scope:

- standards source registry design
- source metadata model
- version/status model
- applicability model
- clause/section reference format
- citation rules
- validation expectations
- explicit non-authority rule for embeddings/retrieval
- controlled placeholder and verification limitation rules
- registry lifecycle and change-control expectations

Closure limitation:

- `DDR-004` closure does not close `DDR-005`.
- `DDR-004` closure does not implement standards embedding/retrieval.
- `DDR-004` closure does not authorize product-ready standards-backed output outside registry limitations.

### Completed governance/model closure: `DDR-001` and `DDR-002`

Approved result:

- `DDR-001` is closed for governance/model scope.
- `DDR-002` is closed for governance/model scope.
- Runtime-authoritative governed-library implementation is mandatory M26 scope unless M25.5 explicitly excludes, defers, or reclassifies it.
- Implementation should be scoped no later than M26.1 and executed through roadmap-authorized M26 dependency-closure work, most likely M26.5.

Closure limitation:

- runtime migration is not implemented.
- deployment-compiled lookup generation is not implemented.
- runtime lookup behavior is not implemented.
- consolidated runtime package/layout behavior is not implemented.
- productized runtime-authoritative library dependence remains blocked until M26 implementation evidence exists.

Evidence artifacts:

- `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_CLOSURE_PLAN.md`
- `docs/milestones/M25/DDR_001_002_RUNTIME_LIBRARY_AUTHORITY_MODEL.md`
- `docs/milestones/M25/DDR_001_002_CLOSURE_DECISION.md`

### Completed scope decision: `DDR-003` and `DDR-006`

Approved result:

- `DDR-003` is closed for governance/model scope.
- `DDR-006` moves to `Closure Planned`.
- Product-ready templates remain inside Phase 9.
- Product-ready document/export/report generation and rendering remain inside Phase 9.
- Implementation for both areas is mandatory M26 scope unless M25.5 explicitly excludes, defers, or reclassifies it.
- Implementation should be scoped no later than M26.1 and executed through roadmap-authorized M26 dependency-closure work, most likely M26.5.

Closure limitation:

- product-ready template implementation is not implemented.
- schema-binding validation is not implemented.
- template loading/selection is not implemented.
- product-ready generation/rendering is not implemented.
- renderer/output contracts are not implemented.
- `DDR-006` is not closed.

Evidence artifacts:

- `docs/milestones/M25/DDR_003_PRODUCT_READY_TEMPLATE_LIBRARY_MODEL.md`
- `docs/milestones/M25/DDR_003_CLOSURE_DECISION.md`
- `docs/milestones/M25/DDR_006_PRODUCT_READY_GENERATION_RENDERING_SCOPE_PLAN.md`

### Completed placement decision: `DDR-007`

Reason:

- `DDR-007` controls actual model/provider integration and pre-go-live operational testing path.
- It remains Critical and must be placed formally before live model/provider work.
- Product/SaaS-facing live model/provider calls remain blocked.
- A local heavy-use / operational shakedown gate is mandatory before SaaS go-live.

Approved placement:

- `DDR-007` is placed as `M25.DDR-007-PLACEMENT`.
- `DDR-007` moves to `Closure Planned` for placement only.
- Live model/provider implementation is not authorized by this placement decision.
- Local/pilot heavy-use testing may be authorized later only after provider adapter boundary, smoke-test plan, and operational test plan exist.
- A local/offline model may be considered later, but is not assumed by this placement decision.

Evidence artifact:

- `docs/milestones/M25/DDR_007_MODEL_PROVIDER_INTEGRATION_AND_LOCAL_SHAKEDOWN_PLACEMENT_DECISION.md`

### Next after `DDR-007`

Next Project Owner review order:

1. Approve named deferral for `DDR-005` behind closed `DDR-004`.
2. Approve evidence verification for `DDR-009`.
3. Approve closure/reclassification route for `DDR-008`.

## 7. Inputs Needed From Project Owner## 7. Inputs Needed From Project Owner

| Area                    | Needed from Project Owner                                                                                                        | Used for                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Standards scope         | Which standards families matter first: GMP, GAMP 5, ASTM E2500, ISO, EU GMP Annexes, FDA guidance, internal standards, or other. | `DDR-004`                       |
| Citation depth          | Whether citation must support clause/section-level references now, or document/version-level references first.                   | `DDR-004`                       |
| Standards use case      | Whether standards-backed CQV/GMP advisory answers are part of Phase 9.                                                           | `DDR-004`, `DDR-005`, `DDR-006` |
| Runtime library scope   | Which governed library families must become runtime-authoritative first.                                                         | `DDR-001`, `DDR-002`            |
| Product document scope  | Whether product-ready CQV document generation is inside Phase 9.                                                                 | `DDR-003`, `DDR-006`            |
| First document families | If document generation is in scope: first templates/documents to support.                                                        | `DDR-003`, `DDR-006`            |
| Provider strategy       | Whether live model/provider work is OpenAI-specific, provider-agnostic, local/offline-model capable, or deferred; this does not override the mandatory local heavy-use shakedown gate. | `DDR-007`                       |
| Go-live ambition        | Whether Phase 9 aims for productization design only, internal pilot readiness, or actual product/SaaS readiness.                 | all DDRs                        |
| Deferral tolerance      | Which DDRs may be deferred to named later checkpoints without blocking M26.                                                      | all DDRs                        |

## 8. Repo Evidence Needed by Category

| Evidence category         | Files or repo artifacts expected                                                                                                | DDRs supported                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Decision artifact         | M25.2 disposition review and this closure plan                                                                                  | all DDRs                                  |
| Roadmap/addendum update   | Roadmap addendum or checkpoint placement update if new DDR closure checkpoints are added                                        | all DDRs requiring new checkpoints        |
| Governance artifact       | Standards authority model, library authority model, document template governance, provider placement decision                   | `DDR-001` through `DDR-007`               |
| Implementation evidence   | Code implementing runtime lookup, compiled lookup, provider adapter, renderer, index, or generator where applicable             | only when closure includes implementation |
| Test evidence             | Unit/integration tests proving behavior or boundary where applicable                                                            | implementation DDRs                       |
| Validation evidence       | `python -m pytest -q` result if executable behavior changes                                                                     | implementation DDRs                       |
| UAT / acceptance evidence | UAT record if product behavior or milestone closure requires acceptance                                                         | productized behavior DDRs                 |
| Register update           | Updated `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` with `Closure Planned`, `Closed`, `Reclassified`, or named deferral | all DDRs after approval                   |

## 9. Phase 9 Placement Proposal

| Phase 9 placement       | DDRs      | Purpose                                                                                                                                             |
| ----------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `M25.DDR-004`           | `DDR-004` | Resolve standards source/citation authority before standards-backed output.                                                                         |
| `M25.DDR-001`           | `DDR-001` | Closed governance/model scope for runtime-authoritative governed-library promotion / deployment-compiled lookup; implementation remains M26-scoped. |
| `M25.DDR-002`           | `DDR-002` | Closed governance/model scope for consolidated runtime-authoritative library structure; implementation remains M26-scoped.                          |
| `M25.DDR-003`           | `DDR-003` | Closed governance/model scope for product-ready document template library; implementation remains M26-scoped.                                      |
| `M25.DDR-006-SCOPE`     | `DDR-006` | Approved closure path for product-ready generation/rendering; implementation and closure evidence remain M26-scoped.                              |
| `M25.DDR-007-PLACEMENT` | `DDR-007` | Place live provider/model integration and pre-go-live path; require a local heavy-use / operational shakedown gate before SaaS go-live. |
| `M25.DDR-009-VERIFY`    | `DDR-009` | Verify M21 external contract placeholder evidence.                                                                                                  |
| `M25.DDR-008-CLOSE`     | `DDR-008` | Close or reclassify Phase 8/9 readiness gate after approved M25.2 evidence.                                                                         |
| Later after `DDR-004`   | `DDR-005` | Define standards embedding/retrieval index only after source/citation authority exists.                                                             |

## 10. Proposed Register Status After Approval

| DDR       | Proposed status after Project Owner approves this plan          | Reason                                                                                                                                                                      |
| --------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DDR-004` | `Closed`                                                        | Project Owner approved the amended standards registry evidence; closure is limited to the source registry/citation authority model.                                         |
| `DDR-001` | `Closed`                                                        | Governance/model scope closed; executable runtime-authoritative promotion / compiled lookup implementation remains M26-scoped with validation/UAT where applicable.         |
| `DDR-002` | `Closed`                                                        | Governance/model scope closed; executable consolidated runtime-authoritative library package/layout implementation remains M26-scoped with validation/UAT where applicable. |
| `DDR-003` | `Closed`                                                        | Governance/model scope closed; executable product-ready template implementation remains M26-scoped with validation/UAT where applicable.                                  |
| `DDR-006` | `Closure Planned`                                               | Scope and closure path approved; executable product-ready generation/rendering implementation remains M26-scoped with validation/UAT where applicable.                    |
| `DDR-007` | `Closure Planned` | Placement approved only; live implementation remains blocked until provider adapter, smoke-test, operational-test, local-shakedown, validation, and UAT evidence exist or the dependency is formally reclassified. |
| `DDR-005` | `Deferred to named checkpoint after DDR-004`                    | Dependent on standards source/citation authority.                                                                                                                           |
| `DDR-009` | `Pending evidence verification` then `Closed` or `Reclassified` | Needs repo evidence check.                                                                                                                                                  |
| `DDR-008` | `Closed` or `Reclassified`                                      | Candidate after M25.2 evidence approval.                                                                                                                                    |

## 11. Immediate Next Step

DDR-004 closure approval is complete.

DDR-001/002 governance/model closure approval is complete.

DDR-003 governance/model closure approval is complete.

DDR-006 scope/closure-path approval is complete.

DDR-007 placement approval is complete.

Next Project Owner review order:

1. Approve named deferral for `DDR-005` behind closed `DDR-004`.
2. Approve evidence verification for `DDR-009`.
3. Approve closure/reclassification route for `DDR-008`.

After approval, the next user-applied action should prepare the approved named-deferral artifact or register/tracker amendments for `DDR-005`, unless the Project Owner redirects.

## 12. Validation Note

This closure plan is documentation/governance evidence only.

No executable validation is required for this draft because it does not alter code, tests, commands, imports, runtime behavior, CLI behavior, or executable contracts.

If later closure work touches executable behavior, validation must be run using:

`python -m pytest -q`
