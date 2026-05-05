# M15_UAT_PROTOCOL

## Milestone

Milestone 15 — Governed Library Expansion and Engine Hardening

## Checkpoint

M15.9 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 15 governed library expansion and engine-hardening boundary.

The protocol verifies that the M15 implementation is understandable, bounded, deterministic, and acceptable for forward roadmap progression into M15.10 closeout.

## UAT Scope

This UAT covers the Milestone 15 implementation boundary through:

- M15.1 — Library gap analysis and coverage audit
- M15.2 — Coverage-pack expansion framework
- M15.3 — Preset / selector library expansion
- M15.4 — Task-pool expansion
- M15.5 — Calendar / standards / profile / mapping expansion
- M15.6 — Library validation, freeze, and release discipline
- M15.7 — Orchestration / service hardening on expanded governed assets
- M15.8 — Validation checkpoint

## Prerequisites

- `M15.1` through `M15.7` implementation/checkpoint evidence is complete.
- `M15.8` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `750 passed in 42.44s`
- Validation evidence exists at:
  - `docs/M15_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the completed M15.8 validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 15 is acceptable as a governed library expansion and service-hardening boundary, not as runtime migration, deployment-compiled lookup generation, CLI implementation, AI runtime behavior, or final product/UI behavior.

## UAT Checks

### UAT-15-01 — Library gap analysis and expansion framework

Confirm that Milestone 15 begins from a documented library audit and bounded coverage-pack framework.

Expected result:

- Library gaps are identified and recorded.
- Coverage-pack expansion is bounded and structured.
- Authored-source versus deployment-compiled roles remain separated.
- Expansion work does not treat VALOR snapshot material as automatic runtime authority.

### UAT-15-02 — Preset / selector expansion coverage

Confirm that preset/selector coverage is expanded and clearly bounded.

Expected result:

- Selector/scope expansion is recorded.
- `DECOM` scope is included.
- `CS` remains the context-selector prefix.
- `CSV` is used as the computerized-systems domain acronym.
- Missing PE/UT/CR/CSV selector records are identified.
- Selector expansion remains documentation/specification-only until later validation/freeze/service handling.

### UAT-15-03 — Task-pool expansion coverage

Confirm that task-pool expansion covers the missing M15.3 selector families.

Expected result:

- Draft task-pool source definitions are recorded for the missing PE/UT/CR/CSV coverage families.
- Task-pool source-definition identity is explicit.
- Duration references remain profile-key-only.
- Dependencies use deterministic `atomic_task_id` references.
- Draft task-pool records do not become runtime authority.

### UAT-15-04 — Profile / standards / calendar / mapping support linkage

Confirm that support-library records connect the expanded task-pool and selector coverage.

Expected result:

- Draft profiles are linked to draft task pools.
- `CAL-WORKWEEK@v1` is preserved as the calendar/planning-basis baseline.
- Draft planning-basis records link selector, task pool, profile, calendar, duration source, and dependency source.
- Draft standards applicability is recorded for CQV core, cleanroom add-on, and CSV add-on contexts.
- Cross-library mapping records connect selector, task pool, profile, calendar, standards, planning basis, profile keys, document obligations, and legacy `CS` to future `CSV` naming.

### UAT-15-05 — Library validation, freeze, and release discipline

Confirm that M15 introduces testable validation/freeze/release discipline over governed library releases.

Expected result:

- Structural validity rules are implemented.
- Taxonomy and identity validity rules are implemented.
- Cross-library linkage validity rules are implemented.
- Compiled lookup consistency checks are implemented.
- Release/freeze statuses are explicit.
- Runtime authority and deployment-compiled lookup remain blocked in M15.6.

### UAT-15-06 — Service hardening and adapter-leakage prevention

Confirm that M15 introduces service-hardening preflight behavior over expanded governed assets.

Expected result:

- Service request shape rules exist.
- M15.6 release-manifest preflight dependency exists.
- Adapter-owned lookup is rejected.
- Runtime migration is blocked.
- Deployment compilation is blocked.
- Support retrieval cannot define source truth.
- Document/export invocation context can be prepared only after governed-library preflight passes.
- Actual document/export generation remains out of scope.

### UAT-15-07 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/M15_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `750 passed in 42.44s`
- No unresolved validation defect is identified for the M15 boundary.

## Acceptance Criteria

Milestone 15 UAT may pass only if all of the following are true:

- library gap analysis is documented
- coverage-pack expansion framework exists
- preset/selector expansion is documented and bounded
- task-pool expansion is documented and bounded
- profile/standards/calendar/mapping support linkage is documented
- validation/freeze/release discipline exists and is testable
- service hardening and adapter-leakage prevention exist and are testable
- runtime migration and deployment-compiled lookup generation remain out of scope
- latest validation evidence is green
- no unresolved UAT blocker is identified

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M15_UAT_REPORT.md`

## Recorded On

2026-05-05
