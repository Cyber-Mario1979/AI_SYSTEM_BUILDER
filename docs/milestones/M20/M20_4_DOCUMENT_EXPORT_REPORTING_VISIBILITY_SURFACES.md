# M20.4 — Document/Export/Reporting Visibility Surfaces

## Purpose

This checkpoint introduces deterministic UI visibility surfaces for existing document, export, reporting, and output-target records.

The UI layer may display existing output payloads or metadata supplied by approved API/service/output boundaries, but it must not generate documents, generate reports, generate exports, render product-ready output, or become output truth.

## Boundary decision

The document/export/reporting visibility module is:

`asbp/ui/document_output_visibility.py`

The module defines display-only visibility contracts and payload envelopes only.

It does not introduce screens, framework behavior, route behavior, document generation, report generation, export generation, renderer behavior, command execution, persistence access, or raw state reads.

## Supported visibility surfaces

The supported output visibility surfaces are:

- `output_target_status`
- `document_output_status`
- `export_output_status`
- `reporting_output_status`

These are UI visibility contracts only. They do not define new output generation behavior.

## Source-boundary rule

Output visibility payloads may only be built from approved read/output boundaries for existing outputs.

Allowed source-boundary names are:

- `api_read_surface`
- `service_read_surface`
- `api_service_read_boundary`
- `approved_output_boundary`
- `output_target_metadata`

Forbidden source-boundary names include:

- `document_generation_engine`
- `report_generation_engine`
- `export_generation_engine`
- `renderer_engine`
- `raw_state_storage`
- `raw_persistence_helpers`
- `direct_state_mutation`
- `ui_generated_output`

## Visibility safety rules

Document/export/reporting visibility surfaces must:

- remain display-only
- preserve existing output payload truth
- display output status, reference, type, format, or availability only when supplied
- present missing output as unavailable
- present generation boundaries without generating output
- reject unsupported visibility surfaces fail-closed
- reject generation-engine, renderer, raw state, or persistence source boundaries fail-closed

## Forbidden behavior

The UI output visibility layer must not:

- generate documents
- generate reports
- generate exports
- create document/export/report artifacts
- implement renderer/product-ready output behavior
- own output truth
- access raw state or persistence
- bypass API/service/output boundaries
- silently correct missing output state

## M20.4 implementation evidence

This checkpoint adds:

- `asbp/ui/document_output_visibility.py`
- updates exports in `asbp/ui/__init__.py`
- `tests/test_ui_document_output_visibility.py`

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.4 only introduces document/export/reporting visibility contracts.

Operator action/intake remains in `M20.5`.
UI safety and execution-truth separation remains in `M20.6`.
