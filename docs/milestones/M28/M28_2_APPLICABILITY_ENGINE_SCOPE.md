---
doc_type: milestone_evidence_record
canonical_name: M28_2_APPLICABILITY_ENGINE_SCOPE
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.2
checkpoint_title: Applicability engine scope
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M28.2 — Applicability Engine Scope

## Purpose

M28.2 creates the runtime-facing applicability contract/model that governs how standards sources may become applicable for downstream M28 behavior.

This checkpoint prevents a registered standards source from being treated as universally applicable or automatically mandatory merely because it exists in the standards registry.

## Execution Mode

Hybrid.

This checkpoint creates implementation/source-contract assets and governance evidence.

## Implementation / Source Minimum

M28.2 adds:

- `asbp/standards_applicability_model.py`
- `tests/test_standards_applicability_model.py`

The implementation minimum is the applicability contract/model covering:

- applicability trigger taxonomy;
- input dimensions;
- applicability decision states;
- mandatory-use eligibility;
- limitation propagation;
- rejection cases;
- explicit non-implementation limits.

A narrative evidence file alone is not sufficient for M28.2 completion.

## Anti-Drift Gate

| Field | M28.2 position |
|---|---|
| Execution mode | Hybrid |
| Implementation minimum | Runtime-facing standards applicability contract/model plus tests |
| Governance boundary | Registry presence alone does not make a source applicable or mandatory |
| Validation evidence required | `python -m pytest -q` is required because this package adds a runtime-facing model and tests |
| Tracker movement rule | Tracker may advance only after the contract/model exists, validation is run and recorded truthfully, and non-implementation limits remain explicit |
| Explicit non-implementation claims | M28.2 does not implement runtime registry parsing, citation validation, standards retrieval/embedding, product-ready standards output, UI/API behavior, AI/runtime behavior, deployment, productization, or SaaS readiness |

## Contract Summary

The applicability model defines:

| Contract area | Control |
|---|---|
| Trigger taxonomy | Applicability may be triggered by real context such as GMP relevance, lifecycle phase, system type, electronic-record scope, cleanroom scope, regulatory market, user selection, and related dimensions. Registry presence is captured only as a traceability trigger and cannot be the sole applicability basis. |
| Input dimensions | Applicability decisions must record the input dimensions used to support applicable or conditional decisions. |
| Decision states | `applicable`, `not_applicable`, `conditional`, `insufficient_evidence`, and `rejected`. |
| Mandatory-use eligibility | Mandatory use requires an applicable decision plus authoritative/internal source status, valid mandatory flag, and verified or approved internal source evidence. |
| Limitation propagation | Pending, TBD, user-provided, reference-only, recommendation-only, draft, retired, unavailable, or non-mandatory source limitations must remain visible in the applicability decision. |
| Rejection cases | Not-applicable, insufficient-evidence, and rejected decisions must include explicit rejection cases and cannot allow mandatory use. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.2 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies registry authority, verification, citation, applicability, mandatory-flag, stricter-requirement, override, and intake rules. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.2 as the next normal roadmap checkpoint after final SS. |

## DDR Disposition

M28.2 is relevant to:

- DDR-004 — Standards source registry and citation authority;
- DDR-005 — Standards embedding / retrieval index awareness;
- DDR-006 — Product-ready document/export/report generation and rendering awareness.

Disposition:

- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- M28.2 does not expand DDR-004 closure into executable runtime registry consumption, productized standards-backed output, audit-ready clause-level citation, or verified source-version authority.
- DDR-005 remains deferred to M30; no standards embedding or retrieval is implemented or authorized by this checkpoint.
- DDR-006 remains closure-planned for M29; no product-ready document/export/report generation or rendering is implemented or authorized by this checkpoint.
- No DDR is closed, reopened, downgraded, or reclassified by M28.2.

## Architecture Boundary

No CLI behavior is changed.

No persistence/state behavior is changed.

No UI/API, AI/runtime, deployment, productization, or SaaS behavior is introduced.

The model is a runtime-facing source contract only. Future executable consumers must attach through approved core/module boundaries and remain subject to architecture guardrails.

## Validation Requirement

Required local validation after package application:

    python -m pytest -q

Validation status:

    PENDING_LOCAL_EXECUTION

No validation is claimed by this evidence record until the command is run and passed in the local repository.

## Explicit Non-Implementation Claims

This checkpoint does not:

- parse the standards registry at runtime;
- validate citations;
- implement standards retrieval or embedding;
- generate product-ready standards output;
- generate product-ready documents, exports, or reports;
- implement stricter-requirement comparison behavior;
- implement controlled override workflow;
- implement local/company/site standards intake workflow;
- change CLI behavior;
- change persisted state;
- authorize UI/API behavior;
- authorize AI/model/provider behavior;
- authorize deployment, release, productization, or SaaS action;
- close M28;
- execute M28 UAT.

## Handoff

After this package is applied, run:

    python -m pytest -q

If validation passes, the next allowed action is a validation/tracker update for M28.2.

The exact next unfinished checkpoint after successful M28.2 validation and tracker movement will be:

    M28.3 — Citation model implementation scope
