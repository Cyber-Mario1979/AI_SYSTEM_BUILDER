---
doc_type: milestone_evidence_record
canonical_name: M29_4_DOCUMENT_INPUT_SCHEMA_BINDING
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.4
checkpoint_title: Document input schema binding
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29.4 — Document Input Schema Binding

## Purpose

M29.4 implements controlled document input schema binding for the local integrated CQV document factory path.

This checkpoint binds controlled template records to controlled document input schema source records. It defines required fields, optional fields, conditional fields, DCF intake mapping, skip-DCF minimum input mapping, placeholder / missing-data controls, and schema-to-template consistency checks.

This checkpoint does not draft document content, generate product-ready documents, render/export documents, implement lifecycle workflow, implement review/approval workflow, implement UI/API behavior, implement AI/runtime behavior, authorize deployment, authorize productization, or authorize SaaS readiness.

## Implementation Assets

The M29.4 user-applied package adds:

- `asbp/document_input_schema_model.py`
- `asbp/document_input_schema_store.py`
- `asbp/document_input_schema_binding.py`
- `data/source/document_input_schemas/starter_document_input_schemas.json`
- `tests/test_document_input_schema_model.py`
- `tests/test_document_input_schema_store.py`
- `tests/test_document_input_schema_binding.py`
- `tests/test_document_template_schema_binding.py`

The package also updates:

- `asbp/document_template_model.py`
- `data/source/document_templates/starter_document_templates.json`
- `asbp/cross_library_validation_model.py`
- `asbp/cross_library_validation.py`
- `tests/test_cross_library_validation.py`

## Implemented Schema Bindings

The starter input schema library implements controlled schema records for the current M29 template records:

| Schema ID | Template ID | Family | Document type |
|---|---|---|---|
| `SCHEMA-QUALIFICATION-PLAN@v1` | `TPL-FUTURE-QUALIFICATION-PLAN@v1` | `DOCF-PLAN-STRATEGY` | Qualification Plan |
| `SCHEMA-CSV-VALIDATION-PLAN@v1` | `TPL-FUTURE-CSV-VALIDATION-PLAN@v1` | `DOCF-PLAN-STRATEGY` | CSV Validation Plan |

The template records are updated from pending `SCHEMA-FUTURE-*` references to controlled schema-bound references.

## Validation Requirement

Because M29.4 changes code, source data, source contracts, cross-library validation behavior, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this user-applied package record.

## DDR Impact

- DDR-003 is directly touched because this package implements document input schema binding for product template records.
- DDR-006 remains carried forward because product-ready document/export/report generation and rendering are not implemented by M29.4.
- DDR-005 remains deferred to M30; no retrieval or embedding is implemented.

## Explicit Non-Implementation Claims

This M29.4 package does not:

- draft document content;
- generate product-ready documents;
- validate final document output;
- implement controlled drafting modes;
- implement standards-backed output generation;
- render, export, or report documents;
- implement document lifecycle persistence;
- implement review/approval runtime workflow;
- implement UI/API behavior;
- implement AI/model/provider behavior;
- authorize deployment, productization, or SaaS readiness.

## Tracker Movement Rule

`PROGRESS_TRACKER.md` must not be advanced until the package is applied locally and `python -m pytest -q` is run with truthful recorded validation status.
