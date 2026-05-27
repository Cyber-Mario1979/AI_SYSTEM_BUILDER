---
doc_type: milestone_checkpoint_evidence
canonical_name: M27_5_CALENDAR_AND_WORK_TIME_MODEL
status: PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_record
milestone: M27
checkpoint: M27.5
execution_mode: hybrid
live_repo_write: NO
---

# M27.5 — Calendar and Work-Time Model

## Purpose

M27.5 introduces the controlled calendar and work-time source model for the local integrated CQV product path.

Calendar records provide explicit source context for:

- workweek definitions
- workmonth framing
- holiday and site-shutdown handling
- Cairo/local starter defaults only when visibly declared
- user-amendable calendar parameters
- manual fallback when calendar context is missing or unclear

## Execution Mode

Hybrid.

Governance defines the calendar boundary. Runtime/source implementation proves the checkpoint.

## Implementation Evidence

This package adds:

- `asbp/calendar_source_model.py`
- `asbp/calendar_source_store.py`
- `data/source/calendars/starter_calendars.json`
- `tests/test_calendar_source_model.py`

The implementation follows the M27 runtime/source pattern:

- strict Pydantic source models
- forbidden extra fields
- runtime-loadable JSON source records
- load/list/get helper functions
- deterministic identity validation
- explicit regional-assumption controls
- pytest coverage for valid and invalid source records

## Scope Boundary

M27.5 defines calendar and work-time source records only.

It does not implement:

- duration estimation
- planning basis
- task scheduling
- dependency calculation
- work package schedule generation
- verified public holiday authority
- cross-library mapping logic
- standards applicability, standards citation, or standards retrieval
- document generation, document rendering, export, or report generation
- UI/API product behavior
- deployment-compiled lookup
- productization or SaaS readiness

## Calendar Source Families

The starter library contains controlled source records for:

- Cairo explicit starter five-day workweek
- Cairo explicit starter six-day workweek candidate
- generic workmonth baseline
- user-supplied holiday and site-shutdown policy
- manual calendar fallback context

## Assumption Control

Calendar records must not hide regional assumptions.

Cairo/Egypt context is stored as an explicit starter assumption and remains user-amendable.

M27.5 does not verify Egyptian public holidays. Holiday and site-shutdown dates must be supplied or confirmed by the user/site before downstream planning behavior relies on them.

## DDR Disposition

M27.5 touches the governed-library domain and remains under awareness for:

- DDR-001
- DDR-002
- DDR-009

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M27.5 to M27.6 until the calendar source model, starter calendar source data, helper functions, tests, and validation evidence are present.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
