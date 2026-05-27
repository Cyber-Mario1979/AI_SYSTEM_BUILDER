---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_4_PROFILE_MODEL
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.4
execution_mode: hybrid
live_repo_write: NO
---

# M27.4 — Profile Model

## Purpose

M27.4 introduces the controlled profile source model for the local integrated CQV product path.

Profiles provide governed context records for:

- area/system profiles
- cleanroom/HVAC profiles
- equipment/system profiles
- qualification profiles
- manual fallback context

This checkpoint supports source-library determinism for downstream M27 mappings and planning work without claiming product-ready behavior.

## Execution Mode

Hybrid.

Governance defines the profile boundary. Runtime/source implementation proves the checkpoint.

## Implementation Evidence

This package adds:

- `asbp/profile_source_model.py`
- `asbp/profile_source_store.py`
- `data/source/profiles/starter_profiles.json`
- `tests/test_profile_source_model.py`

The implementation follows the M27.3 runtime/source pattern:

- strict Pydantic source models
- forbidden extra fields
- runtime-loadable JSON source records
- load/list/get helper functions
- deterministic identity validation
- pytest coverage for valid and invalid source records

## Scope Boundary

M27.4 defines profile source records only.

It does not implement:

- calendar or work-time logic
- duration or planning basis logic
- cross-library mapping logic
- standards applicability, standards citation, or standards retrieval
- document generation, document rendering, export, or report generation
- UI/API product behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Profile Source Families

The starter library contains controlled source records for:

- cleanroom / HVAC qualification context
- process equipment GMP qualification context
- QC lab equipment qualification / CSV linkage context
- GMP utility qualification context
- computerized system GxP context
- cross-family qualification strategy context
- manual fallback context

## Assumption Control

Profiles must not embed one-off local assumptions as universal truth.

Fields such as cleanroom grade, pressure cascade, equipment identity, GMP impact, utility boundary, calibration status, GxP relevance, qualification depth, and risk basis require human confirmation or downstream mapping before deterministic execution is treated as final.

## DDR Disposition

M27.4 touches the governed-library domain and remains under awareness for:

- DDR-001
- DDR-002
- DDR-009

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M27.4 to M27.5 until the profile source model, starter profile source data, helper functions, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
