---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_8_LIBRARY_CONTENT_IMPLEMENTATION_WAVE_1
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.8
execution_mode: hybrid
live_repo_write: NO
---

# M27.8 — Library Content Implementation Wave 1

## Purpose

M27.8 integrates the controlled M27 starter source libraries into one local CQV source-library baseline.

This checkpoint uses the M26 source-authority package/layout direction and the M27.3-M27.7 source-family implementations.

## Execution Mode

Hybrid / build-content.

Governance defines the baseline boundary. Runtime/source integration proves the checkpoint.

## Implementation Evidence

This package adds:

- `asbp/source_library_baseline_model.py`
- `asbp/source_library_baseline_store.py`
- `data/source/library_baseline/m27_library_baseline.json`
- `tests/test_source_library_baseline.py`

The implementation integrates:

- task-pool source library
- profile source library
- calendar source library
- planning-basis source library
- mapping source library

## Scope Boundary

M27.8 implements a controlled source-library baseline only.

It does not implement:

- product-ready CQV workflow
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

## Baseline Integration Checks

The baseline integration checks confirm that:

- all five starter source families load through approved loaders
- manifest library IDs match loaded source-library IDs
- task-pool duration refs are covered by planning-basis records
- resolved mapping profile references exist in the profile library
- resolved mapping task-pool references exist in the task-pool library
- calendars are loaded as part of the controlled baseline

Broader cross-library validation remains in M27.9.

## Assumption Control

M27.8 integrates the controlled starter source-library baseline.

It does not restart source-family governance and does not expand into product-ready content claims before trial.

## DDR Disposition

M27.8 touches the governed-library domain and remains under awareness for:

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

Do not advance `PROGRESS_TRACKER.md` from M27.8 to M27.9 until the baseline integration model, manifest, helper functions, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
