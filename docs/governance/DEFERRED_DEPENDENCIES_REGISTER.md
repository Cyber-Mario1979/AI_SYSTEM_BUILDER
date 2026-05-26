---
doc_type: governance_register
canonical_name: DEFERRED_DEPENDENCIES_REGISTER
status: ACTIVE
governs_execution: true
document_state_mode: living_governance_register
authority: deferred_dependency_gate
scope: productization_readiness_and_deferred_dependency_control
owner: Project Owner
source_roadmap: ROADMAP_CANONICAL.md v5
last_alignment_checkpoint: M25.6 — Tracker and DDR alignment after v5
---

# DEFERRED_DEPENDENCIES_REGISTER

## Purpose

This register records deferred dependencies that must not be forgotten while ASBP / ASPP continues roadmap execution.

It exists because some dependencies are not current checkpoint blockers but may become severe blockers before local integrated CQV product-core work, productization, Phase 8 / Phase 9 / Phase 10 work, real document factory / document engine implementation, standards-backed citation/retrieval, API or external contract product behavior, model/provider/local AI runtime integration, deployment readiness, or pre-go-live testing.

The register is a governance control, not an implementation plan.

It must be used to prevent mental-memory-only tracking of deferred work.

## Authority and Source Role

This register is a repo-persistent governance artifact.

It does not override:

- `ROADMAP_CANONICAL.md`
- active `ROADMAP_ADDENDUM_*.md` files, if any are explicitly approved in the future
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`
- repo reality from code, tests, package structure, validation evidence, UAT evidence, and closeout evidence

It supplements those sources by recording deferred dependencies that require mandatory review at defined trigger points.

If this register conflicts with roadmap, active addenda, architecture guardrails, tracker, or repo reality, the authoritative source controls and this register must be corrected through a controlled update.

## M25.6 Alignment Note

This register was aligned after roadmap v5 application during:

`M25.6 — Tracker and DDR alignment after v5`

This alignment:

- preserves all DDR IDs
- preserves closure-scope truth
- preserves blocker logic
- preserves required evidence expectations
- aligns future placement language to roadmap v5
- adds API / external contract trigger coverage
- clarifies document factory / document engine wording
- clarifies local AI model/runtime and app-coupled heavy-use testing under DDR-007
- does not close any DDR by assertion
- does not implement product-core behavior
- does not perform cleanup

## Mandatory Read Triggers

This register must be checked during any ASBP working session when one or more of the following is true:

| Trigger | Required action |
|---|---|
| Session start / `SS` | Perform a quick register scan and state whether the active checkpoint touches any open, deferred, closure-planned, or productization-sensitive dependency. |
| `STATUS` / `NEXT` | Confirm whether the next checkpoint is affected by any dependency in this register. |
| `PLAN` | Include dependency impact when the planned checkpoint touches any registered domain. |
| `GO` | Stop before preparing amendments if the requested work would violate an open, deferred, closure-planned, or productization-sensitive blocker in this register. |
| Milestone start | Review all registered dependencies for milestone relevance. |
| Milestone validation / UAT / closeout | Confirm whether any dependency must be closed, reclassified, carried forward, or explicitly excluded from scope. |
| Phase 7 / Phase 8 / Phase 9 / Phase 10 work | Review relevant DDRs before external surface, cloud/compute, local product-core, or productization/SaaS work. |
| Any productization or SaaS discussion | Mandatory full register review. |
| Any local integrated CQV product-core work | Mandatory review of source authority, library, standards, document factory/output, AI/runtime, UI/API, and UAT dependencies. |
| Any document generation, document factory, template, output rendering, export/report generation, or artifact lifecycle discussion | Mandatory review of document/template/library/standards/output dependencies. |
| Any standards citation, applicability, embedding, retrieval, or standards-backed advice/output discussion | Mandatory review of standards source/citation/retrieval dependencies. |
| Any governed library, preset, selector, task pool, profile, calendar, planning basis, standards bundle, or mapping work | Mandatory review of runtime-authoritative library dependencies. |
| Any API, UI/API, external contract, or product-surface work | Mandatory review of external contract placeholder and underlying library/template/standards dependencies. |
| Any model/provider, live AI runtime, local AI model/runtime, or app-coupled heavy-use testing discussion | Mandatory review of model/provider/local runtime and pre-go-live dependencies. |
| Any deployment, pre-go-live, operational-readiness, shakedown, or go/no-go work | Mandatory full register review. |

## Severity Scale

Severity describes the impact if the dependency is forgotten, not whether it blocks the current checkpoint.

| Severity | Meaning |
|---|---|
| Critical | Forgetting this can invalidate product readiness, compliance posture, execution truth, or go-live readiness. Must be explicitly closed or reclassified before any affected phase/productization gate proceeds. |
| Very High | Forgetting this can create major product, validation, document-generation, output, or library-authority failure. Must be resolved before affected productized behavior proceeds. |
| High | Forgetting this can create bounded but material design/implementation risk in the affected work family. Must be reviewed before related implementation. |
| Medium | Important dependency but not likely to invalidate a major gate alone. Review at milestone boundaries. |
| Low | Minor dependency or localized cleanup watch item. Review when touching the related area. |

## Status Values

| Status | Meaning |
|---|---|
| Open | Dependency is not closed and must be checked at trigger points. |
| Deferred | Dependency is acknowledged and deliberately assigned to later roadmap/phase work. |
| Watch | Dependency does not need action now but may become relevant if adjacent work begins. |
| Closure Planned | Dependency has an approved closure path but is not yet closed. |
| Closed | Closure evidence exists and the dependency no longer blocks the specific approved scope named in the closure evidence. |
| Reclassified | Dependency has been moved, split, downgraded, or superseded by an approved decision. |

## Gate Decision Rules

1. A `Critical` dependency must block any affected productization, SaaS, pre-go-live, live model/provider integration, local AI model/runtime deployment, or operational-readiness work until it is closed, deferred by explicit roadmap authority, or reclassified by an approved decision.
2. A `Very High` dependency must block any affected product-ready document factory/output generation, standards-backed citation/retrieval, runtime-authoritative library promotion, deployment-compiled lookup, or productized CQV source behavior until it is closed, deferred by explicit roadmap authority, or reclassified.
3. A dependency does not automatically block unrelated roadmap checkpoints.
4. If a checkpoint touches a dependency domain, the dependency must be explicitly mentioned in the `PLAN` before implementation.
5. If a requested `GO` action would quietly implement behavior covered by an open, deferred, closure-planned, or limited-scope closed dependency without closing, carrying, or reclassifying it, the action must stop.
6. Standards embedding/retrieval must not proceed before standards source/citation/applicability authority exists and the roadmap-authorized retrieval checkpoint is active.
7. Product-ready document generation must not proceed before document factory workflow, product templates, governed libraries, schemas, standards/citation authority, generation/rendering boundaries, validation, and UAT/acceptance evidence are explicitly ready or reclassified.
8. Model/provider integration, live AI runtime, or local AI model/runtime behavior must not proceed without a roadmap-authorized strategy/path, adapter/runtime boundary, smoke tests where applicable, operational/heavy-use test plan, validation evidence, and acceptance evidence.
9. API and external contracts may preserve placeholders, but productized placeholder-backed behavior must not proceed until the underlying library/template/standards/output dependencies are closed, reclassified, or explicitly carried with limitations.
10. Phase 9 local product-core work and Phase 10 productization/SaaS re-entry must include register review at each relevant milestone gate.
11. This register must not be used as a workaround to skip roadmap authority; when new execution work is needed, assign it through roadmap/checkpoint governance.

## Deferred Dependencies Table

| ID | Dependency | Domain | Status | Severity if forgotten | v5 placement | Current checkpoint blocker? | Productization blocker? | Required closure evidence | Decision notes |
|---|---|---|---|---|---|---|---|---|---|
| DDR-001 | Governed-library runtime promotion / deployment-compiled lookup | Governed libraries | Closed | Very High | M26, M27 | No for M25.6 docs-only alignment. Yes before executable runtime-authoritative lookup, deployment-compiled lookup, or productized governed-library dependence. | No for the approved governance/model gap. Yes for affected executable/productized behavior until v5 source-authority/library evidence exists. | Runtime-authoritative library promotion path; compiled lookup generation evidence if used; validation evidence; UAT/acceptance where applicable. | Closed for governance/model scope only. Runtime migration, deployment-compiled lookup generation, runtime lookup implementation, and productized library dependence are not implemented by this closure and are placed in v5 M26/M27 unless explicitly excluded or reclassified later. |
| DDR-002 | Consolidated runtime-authoritative libraries | Governed libraries | Closed | Very High | M26, M27 | No for M25.6 docs-only alignment. Yes before productized use of presets/selectors/task pools/profiles/calendars/planning basis/standards bundles/mappings as runtime authority. | No for the approved governance/model gap. Yes for affected executable/productized behavior until v5 runtime-authoritative library package/layout evidence exists. | Consolidated library package/layout; source-role rules; version/status model; cross-library validation; validation evidence; acceptance where applicable. | Closed for governance/model scope only. Draft/scattered expansion evidence remains non-final runtime authority until v5 M26/M27 implements and validates the product source/library structure where productized use requires it. |
| DDR-003 | Product-ready document templates library | Document templates / document factory | Closed | Very High | M29 | No for M25.6 docs-only alignment. Yes before executable product-ready template loading, selection, schema binding, or product document generation. | No for the approved governance/model gap. Yes for affected product document factory/template behavior until v5 M29 evidence exists. | Template library structure; template IDs; schema binding; lifecycle/versioning rules; deterministic template selection/loading; validation evidence; UAT/acceptance where applicable. | Closed for governance/model scope only. Product-ready template implementation, template loading/selection, schema-binding validation, and document factory integration are not implemented by this closure and are placed in v5 M29 unless explicitly excluded or reclassified later. |
| DDR-004 | Standards source registry and citation authority | Standards / compliance | Closed | Critical | M28 | No for M25.6 docs-only alignment. Yes before executable registry consumption or productized standards-backed use beyond the approved registry model. | No for the DDR-004 source/citation authority model gap. Downstream productization may still be blocked by DDR-003, DDR-005, DDR-006, DDR-007, source-specific verification limits, or v5 implementation scope. | Standards registry; citation model; source status; clause reference format; applicability rules; validation evidence for executable use; stricter-requirement rule; controlled override rule; local/company standards intake flow. | Closed after Project Owner approved `docs/standards/STANDARDS_SOURCE_REGISTRY.md` v0.1 as DDR-004 closure evidence. Closure establishes a controlled standards source registry and citation authority model only. Executable registry consumption and productized standards-backed behavior are placed in v5 M28 unless explicitly excluded or reclassified later. DDR-005 still governs standards embedding/retrieval. |
| DDR-005 | Standards embedding / retrieval index | Standards / retrieval | Deferred | High | M30 | No for M25.6 docs-only alignment. Yes before standards embedding/retrieval implementation or productized standards-backed retrieval. | Yes when standards-backed retrieval is productized. | Indexing design; source registry dependency satisfied; source eligibility rules; retrieval-use rules; proof retrieval remains helper-only and not evidence authority; validation/evaluation evidence; UAT/acceptance where applicable. | Deferred to roadmap v5 M30. No standards embedding/retrieval implementation is authorized during M25. Retrieval must remain helper-only, source-traceable, and non-authoritative. |
| DDR-006 | Product-ready document/export/report generation and rendering | Document factory / export / reporting | Closure Planned | Very High | M29 | No for M25.6 docs-only alignment. Yes before product-ready generation/rendering behavior. | Yes for affected product-ready document/export/report generation and rendering until closed, partially closed, or formally reclassified. | Complete document factory workflow; generation boundary; renderer/output contract; templates/schemas/libraries/citations ready; artifact metadata; validation evidence; UAT/acceptance evidence. | Closure path approved only. DDR-006 remains productization-blocking for affected output behavior until v5 M29 provides document factory workflow, renderer/output contract, implementation, validation evidence, and UAT/acceptance evidence or a formal reclassification. |
| DDR-007 | Actual model/provider integration and pre-go-live operational testing path | AI/runtime/product readiness | Closure Planned | Critical | M31, M33, M37 | No for M25.6 docs-only alignment. Yes before model/provider implementation, local AI model/runtime integration, app-coupled heavy-use testing, or pre-go-live execution. | Yes for product/SaaS-facing live model/provider calls and for local AI runtime claims beyond a roadmap-authorized trial path. | Provider/local runtime strategy decision; adapter/runtime boundary; smoke tests where applicable; operational/heavy-use test plan; local app-coupled heavy-use/shakedown protocol and evidence; issue/iteration evidence; validation evidence; UAT/acceptance evidence. | Closure planned for placement only. Product/SaaS-facing live model/provider calls remain blocked. Local/offline/app-coupled model runtime is now explicitly placed in v5 M31/M33/M37, but it remains blocked until strategy, boundary, tests, shakedown/validation, and acceptance evidence exist. |
| DDR-008 | Phase 8 / Phase 9 productization readiness gate | Productization / deployment / SaaS | Closed | Critical | M25, M34 | No for M25.6 docs-only alignment. Yes if future work tries to bypass v5 product-core or re-entry gates. | No for gate-control closure. Downstream productization blockers remain governed by their own DDRs and v5 M34/Phase 10 re-entry. | Phase expansion/roadmap authority; full DDR review; explicit unresolved-dependency disposition; gate closure or re-entry decision evidence. | Closed for gate-control scope only. Closure does not claim product readiness, SaaS readiness, Phase 9 completion, or downstream blocker closure. V5 replaces the archived Addendum 10 productization path with M25-M34 local product-core work and M35-M38 productization/SaaS re-entry gates. |
| DDR-009 | External contract placeholders for future library/template/standards references | UI/API external contracts | Closed | High | M27, M32 | No for M25.6 docs-only alignment. Yes before productized placeholder-backed behavior or external contract changes that rely on unresolved libraries/templates/standards/output dependencies. | No for placeholder compatibility. Underlying productized behavior remains governed by related DDRs. | External contract evidence showing placeholders/extension points remain compatible without pretending underlying dependencies are closed; validation evidence when external contract behavior changes. | Closed for M21 external contract placeholder compatibility evidence. Closure does not implement or authorize runtime libraries, product-ready templates, standards embedding/retrieval, citation authority, product-ready generation, or productized placeholder behavior. V5 places future dependency-aware external/product UI/API work in M27/M32. |

## v5 Placement Matrix

| Work family | Primary v5 milestone(s) | Relevant DDRs |
|---|---|---|
| Roadmap reset / DDR alignment / cleanup gate | M25 | DDR-008, all DDRs for placement awareness |
| Source authority and runtime library architecture | M26 | DDR-001, DDR-002, DDR-003/004/006 awareness |
| Presets, selectors, task pools, profiles, calendars, planning basis, mappings | M27 | DDR-001, DDR-002, DDR-009 awareness |
| Standards applicability, citation, and runtime consumption | M28 | DDR-004, DDR-005/006 awareness |
| Product-ready document factory / document engine workflow and output rendering | M29 | DDR-003, DDR-006, DDR-004/005 awareness |
| Governed retrieval and indexing | M30 | DDR-005, DDR-004, DDR-007 awareness |
| Governed AI assistance and local AI model/runtime strategy | M31 | DDR-007, DDR-005/006 awareness |
| Local usable CQV workflow/UI MVP and external/product surfaces | M32 | DDR-009, DDR-001/002/006 awareness |
| Local integrated product validation, trial, and UAT | M33 | Full DDR review, especially DDR-005/006/007 |
| Product-core closeout and productization re-entry gate | M34 | Full DDR review, especially DDR-005/006/007/008 |
| Product boundary / license / repository / commercial direction | M35 | DDR-008 and productization-sensitive DDR carry-forward |
| Packaging / release governance / security / supportability | M36 | DDR-006/007 and productization-sensitive DDR carry-forward |
| Operational shakedown / provider/deployment gate / go-no-go | M37 | DDR-007, DDR-005/006 where affected |
| SaaS/product boundary consolidation | M38 | Full DDR review |

## Periodic Review Checklist

At every mandatory trigger, answer these questions:

1. Does the current checkpoint touch any dependency domain listed in the table?
2. Is any touched dependency still `Open`, `Deferred`, `Watch`, or `Closure Planned`, or closed only for a limited governance/model scope?
3. Is the dependency severity `Critical` or `Very High`?
4. Is the requested work productization, deployment, live/local AI model integration, document factory generation/rendering, standards embedding/retrieval, API/external contract product behavior, or product-ready output behavior?
5. Does roadmap authority explicitly allow the work now?
6. Is there closure evidence, acceptance evidence, or an explicit reclassification decision?
7. If not, should the work stop, be narrowed, or be converted into a planning/decision-gate action?

## Closure Evidence Rules

A dependency may be marked `Closed` only when evidence exists in the repo.

Acceptable closure evidence may include:

- roadmap-authorized checkpoint completion
- implementation evidence in code
- tests proving the required behavior or boundary
- validation evidence
- UAT evidence where applicable
- closeout notes
- decision gate record approving deferral/reclassification
- updated architecture/roadmap/governance artifact where appropriate

Do not close a dependency based on memory, chat agreement, local notes, unstaged/uncommitted work, or roadmap placement alone.

## Register Maintenance Rules

- Add new dependencies only when they are material and could be forgotten across milestones.
- Do not add tiny typos, metadata lag, stale wording, or normal repo hygiene items here.
- Repo hygiene issues belong in cleanup assessment, not this register.
- Each dependency must have a severity, trigger events, required closure evidence, and next mandatory review.
- Reclassification requires an explicit repo-persistent decision or roadmap-authorized update.
- Closed dependencies should remain in the table unless archived by a governance cleanup action.
- During M25.7-M25.9 cleanup, this register may be inventoried as a non-code document, but DDR statuses and blocker logic must not be altered by cleanup unless an approved governance update explicitly authorizes it.

## Current Overall Gate Status

As of `M25.6 — Tracker and DDR alignment after v5`:

- Active work moves next to `M25.7 — Comprehensive non-code document inventory`.
- `DDR-001`, `DDR-002`, `DDR-003`, and `DDR-004` remain closed only for their approved governance/model/source-authority scopes.
- `DDR-005` remains deferred and is placed in roadmap v5 M30 for standards embedding/retrieval/indexing work.
- `DDR-006` remains `Closure Planned` and productization-blocking for affected product-ready document/export/report generation and rendering until v5 M29 provides required closure evidence or a formal reclassification.
- `DDR-007` remains `Closure Planned` for placement only. Model/provider integration, live AI runtime, local AI model/runtime integration, app-coupled heavy-use testing, pre-go-live execution, or SaaS go-live remain blocked until the roadmap-authorized path and evidence exist.
- `DDR-008` remains closed for gate-control scope only. It does not claim product readiness, SaaS readiness, Phase 9 completion, or downstream blocker closure.
- `DDR-009` remains closed for M21 external contract placeholder compatibility only. It does not authorize productized placeholder-backed behavior.
- No deferred dependency is closed, reopened, downgraded, or reclassified by M25.6 alignment alone.
- Productization/SaaS readiness remains blocked until the local integrated CQV product core is built, validated, accepted, locally trialed, and approved through the roadmap v5 re-entry gate.
- No executable validation is required for M25.6 because it is documentation/governance-only and does not alter code, tests, commands, imports, runtime behavior, CLI behavior, or executable contracts.
