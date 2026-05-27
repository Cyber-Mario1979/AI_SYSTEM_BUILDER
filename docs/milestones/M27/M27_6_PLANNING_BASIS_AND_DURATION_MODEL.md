---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_6_PLANNING_BASIS_AND_DURATION_MODEL
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.6
execution_mode: hybrid
live_repo_write: NO
---

# M27.6 — Planning Basis and Duration Model

## Purpose

M27.6 introduces the controlled planning-basis and duration source model for the local integrated CQV product path.

Planning-basis records provide explicit source context for:

- duration reference records
- starter estimate source status
- duration ranges in working days
- scope rules and human-amendment expectations
- task-pool duration-ref links
- calendar awareness without schedule generation

## Execution Mode

Hybrid.

Governance defines the planning-basis boundary. Runtime/source implementation proves the checkpoint.

## Implementation Evidence

This package adds:

- `asbp/planning_basis_source_model.py`
- `asbp/planning_basis_source_store.py`
- `data/source/planning_basis/starter_planning_basis.json`
- `tests/test_planning_basis_source_model.py`

The implementation follows the M27 runtime/source pattern:

- strict Pydantic source models
- forbidden extra fields
- runtime-loadable JSON source records
- load/list/get helper functions
- deterministic duration-ref identity validation
- task-pool duration-ref coverage check
- pytest coverage for valid and invalid source records

## Scope Boundary

M27.6 defines planning-basis and duration source records only.

It does not implement:

- task scheduling
- dependency calculation
- calendar capacity calculation
- work package schedule generation
- mapping model behavior
- task staging or task commitment behavior
- standards-backed duration claims
- document generation, document rendering, export, or report generation
- UI/API product behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Duration Source Coverage

The starter planning-basis library resolves the `duration_ref_id` values introduced in M27.3 task-pool source records.

M27.6 may check whether task-pool duration refs have matching planning-basis records.

This is not full cross-library validation. Broader relationship validation remains deferred to M27.9.

## Assumption Control

Duration estimates are traceable starter source data, not universal truth.

Each duration source remains user-amendable and requires human confirmation before downstream planning or scheduling relies on it.

Calendar awareness in M27.6 does not calculate capacity and does not create schedules.

## DDR Disposition

M27.6 touches the governed-library domain and remains under awareness for:

- DDR-001
- DDR-002
- DDR-009

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M27.6 to M27.7 until the planning-basis source model, starter duration source data, helper functions, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
