---
doc_type: milestone_evidence_record
canonical_name: M29_5_CONTROLLED_DRAFTING_MODES
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.5
checkpoint_title: Controlled drafting modes
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29.5 — Controlled Drafting Modes

## Purpose

M29.5 implements controlled drafting mode source records and deterministic draft-packet behavior for the local integrated CQV document factory path.

This checkpoint implements bounded drafting packets only. It does not implement standards-backed output controls, renderer/export behavior, lifecycle workflow, review/approval workflow, UI/API behavior, AI/runtime behavior, deployment, productization, or SaaS readiness.

## Implementation Assets

The M29.5 user-applied package adds:

- `asbp/controlled_drafting_model.py`
- `asbp/controlled_drafting_store.py`
- `asbp/controlled_drafting.py`
- `data/source/controlled_drafting/starter_controlled_drafting_modes.json`
- `tests/test_controlled_drafting_model.py`
- `tests/test_controlled_drafting_store.py`
- `tests/test_controlled_drafting.py`

## Implemented Drafting Modes

The starter controlled drafting library implements source records for:

| Mode ID | Drafting mode |
|---|---|
| `DRAFTMODE-STRONG-INPUT-FILL@v1` | strong input fill |
| `DRAFTMODE-PARTIAL-BOUNDED-COMPLETION@v1` | partial bounded completion |
| `DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1` | minimal scaffold with placeholders |
| `DRAFTMODE-RATIONALE-BOUND-SECTION-DRAFTING@v1` | rationale-bound section drafting |

## Validation Requirement

Because M29.5 changes code, source data, source contracts, drafting behavior, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this user-applied package record.

## DDR Impact

- DDR-003 is directly touched because controlled drafting modes depend on product template records, deterministic template selection/loading, and document input schema binding.
- DDR-006 remains carried forward because product-ready document/export/report generation and rendering are not implemented by M29.5.
- DDR-005 remains deferred to M30; no retrieval or embedding is implemented.

## Explicit Non-Implementation Claims

This M29.5 package does not:

- create product-ready documents;
- render or export files;
- apply standards-backed output controls;
- mutate lifecycle, task, review, or approval state;
- implement UI/API behavior;
- implement AI/model/provider behavior;
- authorize deployment, productization, or SaaS readiness.

## Tracker Movement Rule

`PROGRESS_TRACKER.md` must not be advanced until the package is applied locally and `python -m pytest -q` is run with truthful recorded validation status.
