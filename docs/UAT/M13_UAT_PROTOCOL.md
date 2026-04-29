# M13_UAT_PROTOCOL

## Milestone

Milestone 13 — Export and Reporting Engine

## Checkpoint

M13.8 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing UAT checks required to accept the Milestone 13 export and reporting engine boundary.

The protocol is intentionally lightweight. It verifies that the implemented milestone behavior is understandable, bounded, deterministic, and acceptable for forward roadmap progression.

## UAT Scope

This UAT covers the Milestone 13 implementation boundary through:

- M13.1 — Export identity and contract foundation
- M13.2 — Spreadsheet and operational export surfaces
- M13.3 — Gantt and planning visualization exports
- M13.4 — Dashboard and status summary exports
- M13.5 — Reporting export family and detail-level discipline
- M13.6 — Export invocation and validation behavior
- M13.7 — Validation checkpoint

## Prerequisites

- `M13.1` through `M13.6` implementation checkpoints are complete.
- `M13.7` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `659 passed in 45.24s`
- Validation evidence exists at:
  - `docs/M13_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the already completed validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 13 is acceptable as a governed export/reporting engine boundary, not as a final renderer, UI/API surface, or file-writing layer.

## UAT Checks

### UAT-13-01 — Export family clarity

Confirm that supported export families are explicit and bounded:

- spreadsheet / operational exports
- Gantt / planning visualization exports
- dashboard / status summary exports
- governed report exports

Expected result:

- The export families are understandable as deterministic engine contracts.
- No unsupported export family is implied as complete.

### UAT-13-02 — Output boundary clarity

Confirm that output behavior is contract-level only.

Expected result:

- Spreadsheet, Gantt, dashboard, and report outputs are represented as deterministic payload or artifact-reference contracts.
- Rendering, workbook writing, chart generation, PDF/DOCX creation, UI delivery, and API delivery remain outside Milestone 13.

### UAT-13-03 — Reporting detail discipline

Confirm that reporting exports preserve evidence-versus-summary separation and narrative-depth discipline.

Expected result:

- Reporting sections declare structure, evidence references, assumptions, placeholders, and narrative depth where applicable.
- Free-form generated report bodies are not treated as execution truth.

### UAT-13-04 — Invocation and failure behavior

Confirm that export invocation is governed through approved boundaries and fails closed when invalid, incomplete, or ambiguous input is provided.

Expected result:

- Invocation behavior validates the base export request and family-specific payload.
- Incomplete input is rejected before renderer invocation.
- Generated export artifact acceptance requires identity, source context, input snapshot, output kind, and artifact reference consistency.

### UAT-13-05 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/M13_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is `659 passed in 45.24s`.

## Acceptance Criteria

Milestone 13 UAT may pass only if all of the following are true:

- export families are explicit
- spreadsheet, Gantt, dashboard, and reporting outputs are bounded
- reporting detail expectations are explicit
- export invocation and validation behavior are explicit
- fail-closed behavior exists for invalid or incomplete export invocation inputs
- generated export artifact acceptance rules are explicit
- validation evidence is green
- no unresolved UAT blocker is identified

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M13_UAT_REPORT.md`

## Recorded On

2026-04-29
