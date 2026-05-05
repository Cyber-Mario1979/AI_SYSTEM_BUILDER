---
doc_type: milestone_checkpoint_output
canonical_name: M15_LIBRARY_VALIDATION_FREEZE_RELEASE
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.6
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.6 — Library Validation, Freeze, and Release Discipline

## Checkpoint

`M15.6` — Library validation, freeze, and release discipline

## Purpose

This document records the M15.6 validation, freeze, and release discipline for the governed library expansion built across M15.2 through M15.5.

M15.6 defines validation rules and supporting testable helpers. It does not perform runtime migration, generate deployment-compiled lookup, harden orchestration/service behavior, or close the M15 validation/UAT gates.

## Scope

M15.6 introduces:

- structural validity rules
- taxonomy / identity validity rules
- cross-library linkage validity rules
- compiled lookup consistency rules
- freeze / release status expectations
- pure Python validation helpers
- pytest coverage for accepted and rejected release-manifest cases

## Repo implementation

M15.6 adds:

- `asbp/governed_library/library_release_validation.py`
- `tests/test_governed_library_release_validation.py`

M15.6 updates:

- `asbp/governed_library/__init__.py`

## Validation rule families

### Structural validity

A release manifest must declare:

- selector refs
- task-pool refs
- profile refs
- standards-bundle refs
- calendar refs
- planning-basis refs
- mapping-metadata refs
- link records
- task/profile-key mappings
- document-obligation mappings

Every required list must be non-empty.

### Taxonomy / identity validity

The validator enforces:

- all refs must be version-pinned
- `latest`, `current`, wildcard, and unversioned refs are rejected
- `CS` is reserved as the context-selector prefix
- `CSV` is the computerized-systems domain acronym
- future canonical release manifests reject legacy `CS-CS`, `TP-CS`, `PROF-CS`, and `PB-CS` computerized-system refs

### Cross-library linkage validity

The validator checks that link records connect declared library references:

- selector to task pool
- selector to profile
- selector to calendar
- selector to standards bundle
- selector to planning basis
- task pool/profile-key mappings to declared task pools and profiles
- document obligation mappings to declared task pools

### Compiled lookup consistency

M15.6 defines candidate checks only.

Compiled lookup candidates must:

- link back to an included authored source ref
- never become source authority

M15.6 does not generate compiled lookup files.

### Freeze / release status expectations

Supported release statuses:

- `draft_not_runtime_authority`
- `validation_candidate`
- `freeze_candidate`
- `frozen_released`
- `rejected`

M15.6 validators preserve `runtime_authority_status = not_runtime_authority` and `deployment_compiled_status = not_compiled`.

## Not in M15.6 scope

M15.6 does not implement:

- runtime migration
- deployment compiled lookup generation
- CLI changes
- orchestration/service hardening
- AI runtime behavior
- M15.8 validation checkpoint closure
- M15.9 UAT
- M15.10 closeout

## Validation expectation

Because M15.6 introduces Python validation helpers and tests, the expected validation command is:

```powershell
python -m pytest -q
```

## Checkpoint decision

M15.6 creates the first testable validation/freeze/release discipline over the M15 governed library expansion.

The project may proceed to M15.7 only after the package is applied, committed, pushed, and full pytest validation passes.
