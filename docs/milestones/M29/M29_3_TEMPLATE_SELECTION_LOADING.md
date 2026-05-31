---
doc_type: milestone_evidence_record
canonical_name: M29_3_TEMPLATE_SELECTION_LOADING
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.3
checkpoint_title: Template selection/loading
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29.3 — Template Selection / Loading

## Purpose

M29.3 implements deterministic template selection and loading for the local integrated CQV document factory path.

This checkpoint consumes the controlled template source records implemented in M29.2 and resolves exactly one template record when the request constraints are deterministic.

M29.3 does not implement document input schema validation, controlled drafting, standards-backed output generation, rendering/export, lifecycle workflow, review/approval workflow, UI/API behavior, AI/runtime behavior, deployment, productization, or SaaS readiness.

## Implementation Assets

The M29.3 user-applied package adds:

- `asbp/template_selection_model.py`
- `asbp/template_selection.py`
- `tests/test_template_selection_model.py`
- `tests/test_template_selection.py`

## Implemented Behavior

The package implements deterministic template selection based on:

1. document family;
2. document type;
3. standards-bundle compatibility;
4. resolved standards-to-template mappings where standards bundle refs are supplied;
5. intake route compatibility;
6. active template lifecycle status.

The package returns visible non-selected outcomes when:

- no template matches the request constraints;
- multiple templates match the request constraints;
- the requested standards bundle is unsupported;
- the requested intake route is unsupported;
- a matching template record is inactive or retired.

## Source Boundaries

M29.3 uses existing source truth from:

- `asbp/document_template_store.py`
- `data/source/document_templates/starter_document_templates.json`
- `asbp/mapping_source_store.py`
- `data/source/mappings/starter_mappings.json`

M29.3 does not create new template records and does not change source-library authority beyond deterministic selection/loading behavior.

## Validation Requirement

Because M29.3 changes code, source contracts, deterministic behavior, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this user-applied package record.

## DDR Impact

- DDR-003 is directly touched because this package implements deterministic template selection/loading over the M29.2 template records.
- DDR-006 remains carried forward because product-ready document/export/report generation and rendering are not implemented by M29.3.
- DDR-005 remains deferred to M30; no retrieval or embedding is implemented.

## Explicit Non-Implementation Claims

This M29.3 package does not:

- validate final document input schemas;
- implement DCF forms or extraction;
- implement controlled drafting modes;
- generate product-ready documents;
- render, export, or report documents;
- implement document lifecycle persistence;
- implement review/approval runtime workflow;
- implement UI/API behavior;
- implement AI/model/provider behavior;
- authorize deployment, productization, or SaaS readiness.

## Tracker Movement Rule

`PROGRESS_TRACKER.md` must not be advanced until the package is applied locally and `python -m pytest -q` is run with truthful recorded validation status.
