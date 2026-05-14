# M19_UAT_PROTOCOL

## Milestone

Milestone 19 — API Boundary Introduction

## Checkpoint

M19.8 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 19 API boundary.

The protocol verifies that the M19 implementation is understandable, bounded, deterministic, validated, and acceptable for forward roadmap progression into M19.9 closeout.

## UAT Scope

This UAT covers the Milestone 19 implementation boundary through:

- M19.1 — API boundary foundation
- M19.2 — Request/response contract foundation
- M19.3 — Service-boundary consumption rules
- M19.4 — API safety and adapter isolation rules
- M19.5 — Minimal API read surfaces
- M19.6 — Minimal API command/intake surfaces
- M19.7 — API validation checkpoint

## Prerequisites

- M19.1 through M19.6 implementation/checkpoint evidence is complete.
- M19.7 validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `944 passed in 46.94s`
- Validation evidence exists at:
  - `docs/milestones/M19/M19_7_API_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the completed M19.7 validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 19 is acceptable as a bounded API boundary introduction layer over the completed core, document/reporting, governed data, and governed AI-layer boundaries.

This UAT does not accept M19 as a production web API, UI implementation, cloud deployment, SaaS/productization layer, live AI/model-provider integration, document/report generator, approval/release authority, or broad workflow-orchestration layer.

## UAT Checks

### UAT-19-01 — API boundary role and adapter discipline

Confirm that the API boundary is understandable as a downstream adapter layer.

Expected result:

- API package/module boundary is explicit under `asbp/api/`.
- API role is downstream adapter only.
- API does not own source truth, execution truth, validation truth, domain logic, approval authority, release authority, or raw persistence/state behavior.
- API boundary evidence exists and is understandable.

### UAT-19-02 — Request/response/error contract clarity

Confirm that API request/response/error contracts are deterministic and understandable.

Expected result:

- Request, response, error, status, and result contract shapes are explicit.
- Success and error response helpers produce deterministic payloads.
- Unsupported status/result vocabulary fails through controlled contract behavior.
- Response bodies are structured and not ambiguous free-form operation payloads.

### UAT-19-03 — Service-boundary consumption and raw-state rejection

Confirm that API service-boundary rules are understandable and safe.

Expected result:

- Approved API dependency targets are limited to `service`, `runtime`, and `core`.
- Raw state, raw persistence, and direct storage targets are rejected.
- Unknown dependency targets fail closed.
- API adapters do not bypass approved service/runtime/core boundaries.

### UAT-19-04 — Safety rules and fail-closed intake behavior

Confirm that API safety behavior is deterministic and fails closed.

Expected result:

- Safe intake categories remain limited and explicit.
- Invalid, unknown, command-like, and mutation-like intake fails closed unless bounded by the M19.6 preview/validation-only intake surface.
- No silent mutation or no-guess behavior is introduced.
- Unsafe requests produce deterministic error responses.

### UAT-19-05 — Minimal read surfaces

Confirm that minimal read surfaces are deterministic, understandable, and read-only.

Expected result:

- Supported read surfaces are explicit.
- API read surfaces expose governed API metadata only.
- Invalid or unknown read-surface names fail closed.
- Read responses are deterministic.
- Read surfaces do not mutate source data or persisted state.

### UAT-19-06 — Minimal command/intake surfaces

Confirm that minimal command/intake surfaces are bounded to validation and preview behavior only.

Expected result:

- Supported command/intake vocabulary is explicit.
- Valid command/intake requests return deterministic accepted preview/validation responses.
- `execution_allowed` remains `False`.
- Direct execution requests fail closed.
- Unsupported commands fail closed.
- Forbidden raw state/persistence/storage targets fail closed.
- Command/intake behavior does not execute workflow actions or mutate state.

### UAT-19-07 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/milestones/M19/M19_7_API_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `944 passed in 46.94s`
- No unresolved validation defect is identified for the M19 boundary.

### UAT-19-08 — Downstream readiness for M20 UI layer

Confirm that M19 is ready to hand off to M20 without expanding into UI, cloud, or model-provider behavior.

Expected result:

- API boundary is stable enough for the next UI-layer milestone to consume.
- M19 remains correctly bounded as API boundary introduction only.
- M20 UI implementation remains future work.
- Cloud/deployment remains Phase 8 work.
- SaaS/productization remains Phase 9 work.
- Actual AI model/provider integration remains outside M19 and is tracked separately as a roadmap design concern.
- Issue #16 remains a forward roadmap/design concern, not an M19 UAT blocker.

## Acceptance Criteria

Milestone 19 UAT may pass only if all of the following are true:

- API boundary role is explicit and understandable.
- API contracts are deterministic and understandable.
- API service-boundary consumption remains downstream from approved service/runtime/core boundaries.
- Raw state, raw persistence, and direct storage access from API adapters are rejected.
- API safety behavior fails closed for invalid, unknown, command-like, and mutation-like intake.
- Minimal read surfaces remain deterministic and read-only.
- Minimal command/intake surfaces remain preview/validation-only and do not execute commands.
- No API feature expands into UI behavior, cloud/deployment behavior, model/provider integration, document/report generation, approval/release authority, or broad workflow orchestration.
- Latest validation evidence is green.
- No unresolved UAT blocker is identified.

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M19/M19_UAT_REPORT.md`

## Recorded On

2026-05-15
