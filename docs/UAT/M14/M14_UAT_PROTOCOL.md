# M14_UAT_PROTOCOL

## Milestone

Milestone 14 — Resolver / Registry and Governed Data Layer

## Checkpoint

M14.7 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 14 resolver / registry and governed data-layer boundary.

The protocol is intentionally lightweight. It verifies that the implemented milestone behavior is understandable, bounded, deterministic, and acceptable for forward roadmap progression.

## UAT Scope

This UAT covers the Milestone 14 implementation boundary through:

- M14.1 — Resolver / registry boundary foundation
- M14.2 — Governed asset identity and version-pinned lookup
- M14.3 — Calendar and planning-basis resolution family
- M14.4 — Authored-source versus deployment-compiled separation
- M14.5 — Governed retrieval versus support-retrieval boundary
- M14.6 — Validation checkpoint

## Prerequisites

- `M14.1` through `M14.5` implementation checkpoints are complete.
- `M14.6` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `724 passed in 51.47s`
- Validation evidence exists at:
  - `docs/milestones/M14/M14_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the already completed validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 14 is acceptable as a governed resolver / registry and governed data-layer boundary, not as a final UI/API layer, support-retrieval execution layer, AI retrieval runtime, or asset-content authoring system.

## UAT Checks

### UAT-14-01 — Resolver / registry boundary clarity

Confirm that the resolver / registry is an explicit governed access boundary.

Expected result:

- Resolver / registry access is defined through approved boundaries and entry points.
- CLI remains an adapter and does not own lookup authority.
- AI, UI, renderer, and API surfaces do not become source truth or execution truth.
- Prohibited bypass fields are rejected.

### UAT-14-02 — Governed asset identity and version-pinned lookup

Confirm that governed asset lookup requires explicit identity and version pinning.

Expected result:

- Governed assets use canonical asset family, asset ID, asset version, asset reference, and lookup key rules.
- Explicit pinned versions are required.
- Unversioned, implicit, `latest`, `current`, wildcard, missing, duplicate, or ambiguous lookup behavior fails closed.
- Lookup resolves identity/reference metadata only and does not load asset payloads.

### UAT-14-03 — Calendar and planning-basis resolution boundary

Confirm that calendar and planning-basis resolution is explicit and bounded.

Expected result:

- Calendar resolution returns deterministic core-engine input metadata only.
- Planning-basis resolution returns duration/dependency-source metadata only.
- Calendar arithmetic, schedule generation, task duration calculation, Gantt/rendering, and payload loading remain outside Milestone 14.
- Resolved calendar/planning-basis records are treated as future deterministic core-engine inputs, not as planning outputs.

### UAT-14-04 — Authored-source versus deployment-compiled separation

Confirm that authored source and deployment-compiled lookup roles are separated.

Expected result:

- Authored source remains editable source authority.
- Deployment-compiled records are runtime lookup surfaces only.
- Compiled lookup may reference authored source identity but cannot become source authority.
- Source-to-compiled identity linkage must remain version-pinned and fail closed on mismatch or authority override.

### UAT-14-05 — Governed retrieval versus support retrieval

Confirm that governed retrieval and support retrieval remain structurally distinct.

Expected result:

- Governed retrieval is deterministic, version-pinned, and authority-preserving.
- Support retrieval is non-authoritative context only.
- Support retrieval cannot redefine source truth, execution truth, compiled truth, governed lookup identity, or payload authority.
- Support retrieval remains compatible with later AI retrieval rules without becoming an AI runtime implementation now.

### UAT-14-06 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/milestones/M14/M14_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `724 passed in 51.47s`
- No unresolved validation defect is identified for the M14 boundary.

## Acceptance Criteria

Milestone 14 UAT may pass only if all of the following are true:

- resolver / registry boundary is explicit
- governed asset lookup is version-aware and fail-closed
- calendar/planning-basis resolution is explicit and separated from planning arithmetic/rendering
- authored-source and deployment-compiled lookup roles are separated
- governed retrieval and support retrieval roles are separated
- support retrieval cannot become authority
- validation evidence is green
- no unresolved UAT blocker is identified

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M14/M14_UAT_REPORT.md`

## Recorded On

2026-05-04
