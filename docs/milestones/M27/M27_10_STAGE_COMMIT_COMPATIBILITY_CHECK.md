---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_10_STAGE_COMMIT_COMPATIBILITY_CHECK
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.10
execution_mode: hybrid
live_repo_write: NO
---

# M27.10 — Stage/Commit Compatibility Check

## Purpose

M27.10 introduces a non-mutating compatibility layer that proves the M27 source-library baseline can support the path from source selection to staged task candidates, committed task candidates, and planning-input candidates.

This checkpoint confirms:

- source selection through selector-to-task-pool mappings
- task-pool source records can instantiate deterministic task candidates
- staged task candidates preserve source identity
- committed task collections derive from staged collections
- planning input derives from committed instantiated tasks
- planning input uses duration and calendar references without generating schedules

## Execution Mode

Hybrid / compatibility-validation build-content.

Compatibility implementation proves the checkpoint. Governance preserves the boundary.

## Implementation Evidence

This package adds:

- `asbp/stage_commit_compatibility_model.py`
- `asbp/stage_commit_compatibility.py`
- `tests/test_stage_commit_compatibility.py`

The implementation validates:

- selector mapping to task-pool source record
- task candidate instantiation from task-pool atomic tasks
- task source-definition identity
- dependency translation from atomic-task references to task IDs
- staged collection candidate creation
- committed collection candidate derivation
- planning-input candidate creation from committed instantiated tasks
- rejection of direct planning from source definitions
- duration-ref and calendar-ref lookup before planning input is accepted

## Scope Boundary

M27.10 proves compatibility only.

It does not implement:

- live state mutation
- CLI `stage`, `commit`, or `schedule` commands
- persisted work-package execution
- schedule generation
- date calculation
- document generation, document rendering, export, or report generation
- standards applicability, standards citation, or standards retrieval
- UI/API product behavior
- AI routing or model/provider behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Compatibility Boundary

M27.10 may create in-memory candidate objects and raise validation failures.

M27.10 must not write to `data/state/state.json`, mutate persisted state, or plan directly from source definitions without instantiated committed task candidates.

## DDR Disposition

M27.10 touches the governed-library and source-to-execution compatibility domains and remains under awareness for:

- DDR-001
- DDR-002
- DDR-003
- DDR-004
- DDR-005
- DDR-006
- DDR-009

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M27.10 to M27.11 until the compatibility implementation, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
