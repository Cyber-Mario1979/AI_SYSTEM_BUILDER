# M20_UAT_PROTOCOL

## Milestone

Milestone 20 — UI Layer Introduction

## Checkpoint

M20.8 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal UAT checks required to accept the Milestone 20 UI boundary.

## UAT Scope

This UAT covers:

- M20.1 — UI boundary foundation
- M20.2 — UI interaction-flow contract foundation
- M20.3 — Governed workflow visibility surfaces
- M20.4 — Document/export/reporting visibility surfaces
- M20.5 — Operator action/intake boundary
- M20.6 — UI safety and execution-truth separation
- M20.7 — UI validation checkpoint

## Prerequisites

- M20.1 through M20.6 evidence is complete.
- M20.7 validation evidence is complete.
- Latest validation result: `python -m pytest -q` — `1008 passed in 46.37s`.
- Validation evidence: `docs/milestones/M20/M20_7_UI_VALIDATION_CHECKPOINT.md`.

## UAT Method

Review the M20 UI boundary from an operator-facing and project-owner-facing perspective.

This UAT confirms that UI boundary behavior is understandable, bounded, deterministic, safe, and ready for milestone closeout review.

This UAT does not approve production UI screens, UI framework adoption, cloud deployment, SaaS/productization, raw state access, output generation expansion, or approval/release expansion.

## UAT Checks

### UAT-20-01 — UI boundary role

Expected result:

- UI package boundary is explicit under `asbp/ui/`.
- UI remains a downstream product surface and visibility adapter.
- UI does not own domain logic, source truth, validation truth, or execution truth.

### UAT-20-02 — Interaction-flow clarity

Expected result:

- Interaction-flow families are explicit.
- Display-only and command-capable behavior are separated.
- Command-capable behavior requires API/service validation before mutation.

### UAT-20-03 — Workflow visibility

Expected result:

- Workflow visibility surfaces are explicit and deterministic.
- UI displays governed workflow state without changing it.
- Invalid visibility requests fail closed.

### UAT-20-04 — Document/export/reporting visibility

Expected result:

- Output visibility surfaces are explicit and deterministic.
- UI displays existing output payloads or metadata only.
- Existing document/report/export engines remain authoritative.

### UAT-20-05 — Operator intake

Expected result:

- Operator intake actions are explicit and deterministic.
- UI may preview or prepare operator intent.
- UI does not directly perform the downstream action.
- Downstream API/service validation remains required where applicable.

### UAT-20-06 — UI safety

Expected result:

- UI source-truth, validation-truth, and execution-truth claims are rejected.
- API/service boundary bypass is rejected.
- Invalid, stale, or unknown UI states fail closed.
- No-guess behavior is preserved.

### UAT-20-07 — Validation alignment

Expected result:

- M20.7 validation evidence records `1008 passed in 46.37s`.
- No unresolved M20 validation defect is identified.

### UAT-20-08 — Closeout readiness

Expected result:

- UI boundary behavior is understandable, bounded, and safe.
- M20 remains correctly bounded as UI Layer Introduction only.
- M20 is ready to proceed to M20.9 closeout if this UAT passes.

## Acceptance Criteria

Milestone 20 UAT may pass only if all UAT checks pass and no unresolved M20 blocker remains.

## UAT Output

The executed UAT result is recorded in:

`docs/UAT/M20/M20_UAT_REPORT.md`
