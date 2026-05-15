---
doc_type: governance_register
canonical_name: DEFERRED_DEPENDENCIES_REGISTER
status: ACTIVE_PROPOSED
governs_execution: true
document_state_mode: living_governance_register
authority: deferred_dependency_gate
scope: productization_readiness_and_deferred_dependency_control
owner: Project Owner
---

# DEFERRED_DEPENDENCIES_REGISTER

## Purpose

This register records deferred dependencies that must not be forgotten while ASBP / ASPP continues roadmap execution.

It exists because some dependencies are not current checkpoint blockers but may become severe blockers before productization, Phase 8, Phase 9, real document generation, standards-backed citation/retrieval, model/provider integration, deployment readiness, or pre-go-live testing.

The register is a governance control, not an implementation plan.

It must be used to prevent mental-memory-only tracking of deferred work.

## Authority and Source Role

This register is a repo-persistent governance artifact.

It does not override:

- `ROADMAP_CANONICAL.md`
- active `ROADMAP_ADDENDUM_*.md` files
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`
- repo reality from code, tests, package structure, validation evidence, UAT evidence, and closeout evidence

It supplements those sources by recording deferred dependencies that require mandatory review at defined trigger points.

If this register conflicts with roadmap, active addenda, architecture guardrails, tracker, or repo reality, the authoritative source controls and this register must be corrected.

## Mandatory Read Triggers

This register must be checked during any ASBP working session when one or more of the following is true:

| Trigger | Required action |
|---|---|
| Session start / `SS` | Perform a quick register scan and state whether the active checkpoint touches any open deferred dependency. |
| `STATUS` / `NEXT` | Confirm whether the next checkpoint is affected by any open dependency in this register. |
| `PLAN` | Include dependency impact when the planned checkpoint touches any registered domain. |
| `GO` | Stop before preparing amendments if the requested work would violate an open blocker in this register. |
| Milestone start | Review all open dependencies for milestone relevance. |
| Milestone validation / UAT / closeout | Confirm whether any dependency must be closed, reclassified, or carried forward. |
| Phase 7 closeout | Mandatory full register review before Phase 8 planning. |
| Phase 8 entry | Mandatory full register review before cloud/compute/deployment planning. |
| Phase 9 entry | Mandatory full register review before SaaS/productization planning. |
| Any productization discussion | Mandatory full register review. |
| Any document generation/template implementation discussion | Mandatory review of document/template/library/standards dependencies. |
| Any standards embedding/retrieval discussion | Mandatory review of standards source/citation dependencies. |
| Any model/provider integration discussion | Mandatory review of model/provider and pre-go-live dependencies. |
| Any pre-go-live or operational-readiness discussion | Mandatory full register review. |

## Severity Scale

Severity describes the impact if the dependency is forgotten, not whether it blocks the current checkpoint.

| Severity | Meaning |
|---|---|
| Critical | Forgetting this can invalidate product readiness, compliance posture, execution truth, or go-live readiness. Must be explicitly closed or reclassified before any affected phase/productization gate proceeds. |
| Very High | Forgetting this can create major product, validation, document-generation, or library-authority failure. Must be resolved before affected productized behavior proceeds. |
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
| Closed | Closure evidence exists and the dependency no longer blocks relevant triggers. |
| Reclassified | Dependency has been moved, split, downgraded, or superseded by an approved decision. |

## Gate Decision Rules

1. An open `Critical` dependency must block any affected productization, Phase 8, Phase 9, pre-go-live, or live model/provider integration work until it is closed, deferred by explicit roadmap authority, or reclassified by an approved decision.
2. An open `Very High` dependency must block any affected product-ready document generation, standards-backed citation/retrieval, runtime-authoritative library promotion, or deployment-compiled lookup work until it is closed, deferred by explicit roadmap authority, or reclassified.
3. An open dependency does not automatically block unrelated roadmap checkpoints.
4. If a checkpoint touches a dependency domain, the dependency must be explicitly mentioned in the `PLAN` before implementation.
5. If a requested `GO` action would quietly implement behavior covered by an open dependency without closing or reclassifying it, the action must stop.
6. Standards embedding must not proceed before standards source/citation authority exists.
7. Product-ready document generation must not proceed before document templates, governed libraries, schemas, standards/citation authority, and generation/rendering boundaries are explicitly ready or reclassified.
8. Model/provider integration must not proceed without a roadmap-authorized path and pre-go-live operational testing plan.
9. Phase 8 and Phase 9 entry must include a full register review.
10. This register must not be used as a workaround to skip roadmap authority; when new execution work is needed, assign it through roadmap/checkpoint governance.

## Deferred Dependencies Table

| ID | Dependency | Domain | Description | Source evidence | Status | Severity if forgotten | Current checkpoint blocker? | Productization blocker? | Phase gate impact | Trigger events | Required closure evidence | Related issue/addendum | Owner | Last reviewed | Next mandatory review | Decision notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DDR-001 | Governed-library runtime promotion / deployment-compiled lookup | Governed libraries | Expanded governed-library draft records and mappings must be promoted or compiled into runtime-authoritative lookup behavior before productized use. | `docs/milestones/M15/M15_CLOSEOUT_NOTES.md`; post-M20 gap assessment G-04 | Deferred | Very High | No for `M21.1` | Yes | Phase 8 / Phase 9 / productization | Productization, runtime lookup generation, deployment compilation, library authority work | Runtime-authoritative library promotion path; compiled lookup generation evidence; validation evidence; UAT/acceptance where applicable | None yet | Project Owner | Post-M20 gap assessment | Phase 7 closeout and before Phase 8 planning | Not a current M21.1 blocker. Must not be forgotten before runtime/productization work. |
| DDR-002 | Consolidated runtime-authoritative libraries | Governed libraries | Presets/selectors, task pools, profiles, calendars, planning basis, standards bundles, mappings, and related library assets must be consolidated into a clear runtime-authoritative structure before productization depends on them. | `docs/milestones/M15/M15_CLOSEOUT_NOTES.md`; post-M20 gap assessment G-04 | Deferred | Very High | No for `M21.1` | Yes | Phase 8 / Phase 9 / productization | Library consolidation, document generation, productization, deployment readiness | Consolidated library package/layout; source-role rules; version/status model; validation evidence | None yet | Project Owner | Post-M20 gap assessment | Phase 7 closeout and before any productized document-generation path | Do not treat draft/scattered expansion evidence as final runtime authority. |
| DDR-003 | Product-ready document templates library | Document templates | Product-ready document templates and template implementation remain separate from the closed document-engine contracts and must be governed before actual product document generation. | `docs/milestones/M12/M12_CLOSEOUT_NOTES.md`; `docs/decision_gates/POST_M17_PRE_M18_DOCUMENT_REENTRY_DECISION.md`; post-M20 gap assessment G-05 | Deferred | Very High | No for `M21.1` | Yes | Productization / document generation | Document generation, template implementation, CQV document product readiness | Template library structure; template IDs; schema binding; lifecycle and versioning rules; validation evidence | Decision gate: Post-M17 / Pre-M18 Document Re-entry | Project Owner | Post-M20 gap assessment | Before any actual document generation or template implementation work | M12 closed document-engine contracts, not product-ready template assets. |
| DDR-004 | Standards source registry and citation authority | Standards / compliance | Standards must have source identity, version, applicability, clause/section reference model, and citation rules before embedding/retrieval or standards-backed advice becomes productized. | M12 standards guardrails; M17 standards/detail checks; post-M20 gap assessment standards readiness concern | Open | Critical | No for `M21.1` unless M21 introduces standards references beyond contract placeholders | Yes | Productization / standards-backed outputs / pre-go-live | Standards citation, standards embedding, CQV/GMP advice, document generation, audit-ready output | Standards registry; citation model; source status; clause reference format; applicability rules; validation evidence | None yet | Project Owner | Post-M20 gap assessment | Before standards embedding or standards-backed product output | Embedding is not authority. Citation/source authority must come first. |
| DDR-005 | Standards embedding / retrieval index | Standards / retrieval | Standards retrieval/indexing can only be introduced after standards source/citation authority exists and cannot become source truth. | M17 retrieval-use governance; post-M20 gap assessment standards embedding readiness concern | Deferred | High | No for `M21.1` | Yes when standards-backed retrieval is productized | Phase 8 / Phase 9 / standards-backed product behavior | Retrieval/index work, standards embedding, AI-assisted standards use | Indexing design; source registry dependency satisfied; retrieval-use rules; validation/evaluation evidence | Depends on DDR-004 | Project Owner | Post-M20 gap assessment | After DDR-004 closure path is approved | Must remain retrieval helper, not evidence authority. |
| DDR-006 | Product-ready document/export/report generation and rendering | Document/export/reporting | Current M20 document/export/reporting surfaces are visibility-only. Product-ready generation/rendering remains deferred. | `docs/milestones/M20/M20_CLOSEOUT_NOTES.md`; post-M20 gap assessment G-05 | Deferred | Very High | No for `M21.1` | Yes | Productization / document/export/reporting go-live | Document generation, report generation, export generation, renderer/product-ready output | Generation boundary; renderer/output contract; templates/schemas/libraries/citations ready; validation and UAT evidence | None yet | Project Owner | Post-M20 gap assessment | Before any generation/rendering implementation | M20 visibility surfaces must not be mistaken for generation capability. |
| DDR-007 | Actual model/provider integration and pre-go-live operational testing path | AI/runtime/product readiness | Live model/provider calls and pre-go-live operational testing require a roadmap-authorized path before implementation. | Issue #16; M20 closeout exclusions; post-M20 gap assessment G-06 | Watch | Critical | No for `M21.1` | Yes | Phase 7 closeout / Phase 8 expansion / pre-go-live | Model/provider integration, live AI runtime, deployment readiness, operational testing | Roadmap expansion/addendum; provider adapter boundary; smoke tests; operational test plan; validation/UAT evidence | Issue #16 | Project Owner | Post-M20 gap assessment | No later than Phase 7 closeout / Phase 8 expansion gate | Keep Issue #16 open until formal placement is decided. |
| DDR-008 | Phase 8 / Phase 9 productization readiness gate | Productization / deployment / SaaS | Phase 8 and Phase 9 are high-level placeholder directions and require detailed expansion plus dependency review before execution. | Roadmap continuation Part 2; Issue #16; post-M20 gap assessment | Watch | Critical | No for `M21.1` | Yes | Phase 8 / Phase 9 | Phase transition, cloud/compute/deployment planning, SaaS planning | Phase expansion addendum; full DDR review; explicit unresolved-dependency disposition | Issue #16 related | Project Owner | Post-M20 gap assessment | Before Phase 8 execution begins | Do not enter productization on vague roadmap direction alone. |
| DDR-009 | External contract placeholders for future library/template/standards references | UI/API external contracts | M21 external contracts should remain compatible with future references such as `template_id`, `schema_id`, `standards_bundle_ref`, `citation_ref`, and `library_version` without implementing those libraries now. | M21.1 roadmap scope; post-M20 gap assessment; DDR-001 through DDR-006 | Watch | High | Yes for M21 planning awareness only; not a build blocker | Indirectly | M21 | M21.1, M21.2, M21.3 | M21 contract docs/tests show placeholders or extension points without pretending the dependencies are closed | None yet | Project Owner | Post-M20 gap assessment | During M21.1 PLAN | M21 should keep doors open without smuggling deferred implementation into current scope. |

## Periodic Review Checklist

At every mandatory trigger, answer these questions:

1. Does the current checkpoint touch any dependency domain listed in the table?
2. Is any touched dependency still `Open`, `Deferred`, or `Watch`?
3. Is the dependency severity `Critical` or `Very High`?
4. Is the requested work productization, deployment, live model/provider integration, document generation, standards embedding, or product-ready output behavior?
5. Does roadmap/addendum authority explicitly allow the work now?
6. Is there closure evidence or an explicit reclassification decision?
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

Do not close a dependency based on memory, chat agreement, local notes, or unstaged/uncommitted work.

## Register Maintenance Rules

- Add new dependencies only when they are material and could be forgotten across milestones.
- Do not add tiny typos, metadata lag, stale wording, or normal repo hygiene items here.
- Repo hygiene issues belong in cleanup assessment, not this register.
- Each dependency must have a severity, trigger events, required closure evidence, and next mandatory review.
- Reclassification requires an explicit repo-persistent decision or roadmap-authorized update.
- Closed dependencies should remain in the table unless archived by a governance cleanup action.

## Current Overall Gate Status

As of the post-M20 gap assessment:

- Build may resume at `M21.1` only.
- Productization must not proceed while Critical / Very High productization dependencies remain open, deferred, or watch-only.
- Phase 8 and Phase 9 must not begin without a full register review.
- Standards embedding must not proceed before standards source/citation authority is established.
- Actual model/provider integration must not proceed without resolving or formally placing Issue #16.
