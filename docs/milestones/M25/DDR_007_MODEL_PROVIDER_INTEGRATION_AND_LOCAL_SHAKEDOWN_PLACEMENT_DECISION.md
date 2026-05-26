---
doc_type: milestone_evidence
canonical_name: DDR_007_MODEL_PROVIDER_INTEGRATION_AND_LOCAL_SHAKEDOWN_PLACEMENT_DECISION
status: APPROVED_PLACEMENT_DECISION
governs_execution: false
document_state_mode: milestone_checkpoint_governance_evidence
authority: checkpoint_evidence
source_register: docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md
source_disposition_review: docs/milestones/M25/M25_2_DEFERRED_DEPENDENCY_DISPOSITION_REVIEW.md
source_closure_plan: docs/milestones/M25/M25_2_DDR_CLOSURE_PLAN.md
related_issue: GitHub Issue #16
checkpoint: M25.2
milestone: M25 — SaaS Readiness Assessment
phase: Phase 9 — SaaS Readiness / Productization
dependency_id: DDR-007
approval_date: 2026-05-24
---

# DDR-007 — Model/Provider Integration and Local Heavy-Use Shakedown Placement Decision

## 1. Purpose

This document records the `DDR-007` placement decision inside `M25.2` — Deferred dependency disposition review.

`DDR-007` controls actual model/provider integration and the pre-go-live operational testing path.

This decision is a placement and gate-control decision only.

It does not implement live model/provider calls.
It does not authorize product/SaaS-facing live AI runtime.
It does not authorize production operation, SaaS go-live, commercial release, or uncontrolled agentic operation.

## 2. Source Basis

This decision is based on:

- `ROADMAP_ADDENDUM_10_PHASE_9_DETAILED_CHECKPOINT_LADDER.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/milestones/M25/M25_2_DEFERRED_DEPENDENCY_DISPOSITION_REVIEW.md`
- `docs/milestones/M25/M25_2_DDR_CLOSURE_PLAN.md`
- GitHub Issue #16 — `design: define roadmap path for model integration and pre-go-live testing`

The active Phase 9 addendum states that live model/provider integration must not be introduced before a roadmap-authorized path and pre-go-live operational testing plan exist.

The deferred dependency register states that model/provider integration must not proceed without a roadmap-authorized path and pre-go-live operational testing plan.

## 3. Approved Decision

Project Owner approved the following `DDR-007` placement decision on `2026-05-24`:

`DDR-007` may move from `Watch` to `Closure Planned` for placement only.

Approved placement meaning:

- `DDR-007` is formally placed as `M25.DDR-007-PLACEMENT`.
- Live model/provider implementation is not authorized by this placement decision.
- Product/SaaS-facing live model/provider calls remain blocked.
- A provider adapter boundary must be defined before implementation.
- Smoke tests must be defined before live-provider acceptance.
- A pre-go-live operational test plan must be defined before any product/SaaS go-live claim.
- A local heavy-use / operational shakedown gate is mandatory before SaaS go-live.
- `DDR-007` can be closed only after adapter, smoke-test, operational-test, local-shakedown, validation, and UAT / acceptance evidence exists, or after a formal reclassification decision.

## 4. Meaning of “Blocked”

For `DDR-007`, “blocked” does not mean manual-only testing forever.

It means:

- product/SaaS-facing live model/provider calls are blocked;
- production-like live AI runtime is blocked;
- SaaS go-live using live model/provider behavior is blocked;
- uncontrolled provider calls are blocked;
- direct provider coupling without an approved adapter boundary is blocked.

The following remain allowed when roadmap-authorized later:

- controlled local/pilot testing;
- smoke testing through an approved provider adapter;
- local heavy-use operational shakedown;
- repeated user/profile testing;
- issue capture and feedback-driven iteration;
- regression checks after fixes;
- UAT and go/no-go decision evidence.

## 5. Local Heavy-Use / Operational Shakedown Gate

A local heavy-use / operational shakedown phase is mandatory before any SaaS go-live or productized live-provider use.

This gate must occur after provider adapter boundary and smoke-test planning are defined, and before product/SaaS go-live.

The shakedown must support:

- a controlled local or pilot station;
- repeated use over many sessions;
- multiple users or user profiles where practical;
- different opinions, workflows, and input styles;
- realistic task/document/advisory scenarios;
- failure, refusal, ambiguity, and correction scenarios;
- capture of defects, weak outputs, confusing UX, operational problems, and governance gaps;
- iteration on the system where needed;
- regression checks after amendments;
- a final go/no-go acceptance decision before SaaS go-live.

The shakedown must not be treated as production operation.
The shakedown must not use uncontrolled production data unless a later approved policy explicitly allows it.
The shakedown must not replace validation or UAT.

## 6. Provider Strategy Boundary

This placement decision does not force a provider strategy yet.

Allowed future provider strategies may include:

- OpenAI-specific provider path;
- provider-agnostic adapter path;
- local/offline model provider path;
- delayed provider decision.

A local/offline model may be considered later, but it is not assumed by this placement decision.

The mandatory requirement is not “local LLM.”
The mandatory requirement is a controlled local/pilot operational shakedown gate before go-live.

## 7. Required Future Evidence

`DDR-007` closure requires later repo evidence covering the affected execution path.

Required future evidence includes, where applicable:

- provider strategy decision;
- provider adapter boundary;
- provider-call permission and refusal rules;
- secrets/configuration boundary;
- smoke-test plan;
- live-provider smoke-test evidence;
- operational test plan;
- local heavy-use / operational shakedown protocol or plan;
- local heavy-use / operational shakedown report or evidence record;
- issue/defect capture and disposition evidence;
- iteration and regression evidence after amendments;
- validation evidence;
- UAT / acceptance evidence;
- explicit go/no-go decision before SaaS go-live.

## 8. Phase 9 Placement

Approved Phase 9 placement:

| Placement | Purpose |
|---|---|
| `M25.DDR-007-PLACEMENT` | Record the formal placement decision and local shakedown gate requirement. |
| `M26.1` | Decide whether provider integration is inside the M26 productization foundation scope or deferred/excluded by M25.5. |
| `M26.5` or later roadmap-authorized dependency-closure work | Define or implement provider adapter boundary, smoke tests, operational test plan, and related closure evidence if authorized. |
| `M27` go/no-go path or later release-readiness gate | Confirm local heavy-use shakedown, validation, UAT, and residual dependency disposition before SaaS go-live. |

If M25.5 excludes or defers live provider/model integration from the first productization foundation scope, this placement decision remains valid as a carry-forward blocker with a named gate.

## 9. Register Effect

After this decision is applied:

- `DDR-007` status should move from `Watch` to `Closure Planned`.
- `DDR-007` remains `Critical`.
- `DDR-007` remains a productization blocker for affected live model/provider behavior.
- `DDR-007` does not block unrelated M25 assessment work.
- `DDR-007` does block product/SaaS-facing live model/provider integration, pre-go-live execution, and SaaS go-live claims until closure evidence exists or a formal reclassification is approved.

## 10. Issue #16 Effect

GitHub Issue #16 may remain open until the Project Owner decides whether the placement decision should be referenced in an issue comment or closed through normal issue workflow.

This document does not update, comment on, or close the issue.

## 11. Validation Note

No executable validation is required for this placement decision because it is documentation/governance evidence only and does not alter code, tests, commands, imports, runtime behavior, CLI behavior, or executable contracts.

If later work touches executable behavior, validation must be run using:

`python -m pytest -q`
