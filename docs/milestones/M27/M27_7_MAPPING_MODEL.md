---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_7_MAPPING_MODEL
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.7
execution_mode: hybrid
live_repo_write: NO
---

# M27.7 — Mapping Model

## Purpose

M27.7 introduces the controlled source mapping model for the local integrated CQV product path.

Mapping records provide explicit source relationships for:

- preset-to-profile links
- selector-to-task-pool links
- task-to-document expectation links
- future standard-to-template links with visible limitation status

## Execution Mode

Hybrid.

Governance defines the mapping boundary. Runtime/source implementation proves the checkpoint.

## Implementation Evidence

This package adds:

- `asbp/mapping_source_model.py`
- `asbp/mapping_source_store.py`
- `data/source/mappings/starter_mappings.json`
- `tests/test_mapping_source_model.py`

The implementation follows the M27 runtime/source pattern:

- strict Pydantic source models
- forbidden extra fields
- runtime-loadable JSON source records
- load/list/get helper functions
- deterministic mapping identity validation
- resolved-reference coverage helpers
- pytest coverage for valid and invalid source records

## Scope Boundary

M27.7 defines mapping source records only.

It does not implement:

- selector execution
- task staging or task commitment
- scheduling or duration calculation
- standards applicability, standards citation, standards retrieval, or executable standards consumption
- template loading, template selection, or schema binding
- document generation, document rendering, export, or report generation
- UI/API product behavior
- AI routing or model/provider behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Mapping Source Families

The starter library contains controlled mapping records for:

- preset family to profile source records
- selector context to task-pool source records
- selected task source to future document expectation links
- future standards bundle to future template links

## Assumption Control

Mappings connect source families; they do not execute product behavior.

Future document, template, and standards references must remain visibly marked as future or placeholder references until their roadmap-authorized milestones provide implementation, validation, and acceptance evidence.

## DDR Disposition

M27.7 touches the governed-library and external-placeholder domains and remains under awareness for:

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

Do not advance `PROGRESS_TRACKER.md` from M27.7 to M27.8 until the mapping source model, starter mapping source data, helper functions, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
