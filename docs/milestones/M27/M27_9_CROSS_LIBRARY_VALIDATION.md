---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_9_CROSS_LIBRARY_VALIDATION
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.9
execution_mode: hybrid
live_repo_write: NO
---

# M27.9 — Cross-Library Validation

## Purpose

M27.9 introduces a dedicated cross-library validation layer for the M27 controlled source-library baseline.

This checkpoint validates relationships across:

- task-pool source records
- profile source records
- calendar source records
- planning-basis / duration source records
- mapping source records
- the M27 library baseline manifest

## Execution Mode

Hybrid / validation-heavy build-content.

Validation implementation proves the checkpoint. Governance preserves the boundary.

## Implementation Evidence

This package adds:

- `asbp/cross_library_validation_model.py`
- `asbp/cross_library_validation.py`
- `tests/test_cross_library_validation.py`

The implementation validates:

- non-empty source libraries
- task dependency references inside task pools
- task-pool duration refs covered by planning-basis records
- resolved profile mapping refs against profile source records
- resolved task-pool mapping refs against task-pool source records
- resolved atomic-task mapping refs against task-pool atomic task identities
- future document/template/standard refs remain visibly future-scoped
- mapping applicability tags are nonblank

## Scope Boundary

M27.9 validates cross-library relationships only.

It does not implement:

- source-to-execution instantiation
- selector execution
- task staging or task commitment
- scheduling or duration calculation
- standards applicability, standards citation, or standards retrieval
- template loading, template selection, or schema binding
- document generation, document rendering, export, or report generation
- UI/API product behavior
- AI routing or model/provider behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Validation Boundary

M27.9 may produce validation result objects and raise clear validation failures.

M27.9 must not auto-correct source libraries, mutate source data, generate documents, or treat future document/template/standard references as resolved runtime authority.

## DDR Disposition

M27.9 touches the governed-library validation domain and remains under awareness for:

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

Do not advance `PROGRESS_TRACKER.md` from M27.9 to M27.10 until the cross-library validation implementation, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
