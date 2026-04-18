---
doc_type: design_acknowledgment_note
canonical_name: M8_DESIGN_ACKNOWLEDGMENTS
status: ACTIVE_WORKING_NOTE
governs_execution: false
authority: non_authoritative_design_capture
---

# M8 Design Acknowledgments

## Purpose

Capture acknowledged design items so they do not drift during Milestone 8 execution,
without changing the roadmap or the progress tracker unless a real checkpoint block appears.

## M8-sensitive reservations before M8 closeout

These items do not stop current execution now, but they must remain explicitly reserved
before Milestone 8 closeout:

- Cross-work-package dependency linkage
- Multiple calendar support

## Acknowledge now, defer after M8

These items should be recorded now so later scheduling semantics do not drift,
but they do not block current M8 execution:

- Automated overdue detection and reporting
- Configurable work week / non-working day model

## Safe later

These items are mainly scale expectations and do not interrupt current build flow:

- Preset library expansion
- Task pool expansion

## Execution rule

- Current execution continues on the exact approved M8 checkpoint path.
- No roadmap amendment is required unless one of the reserved items becomes a real blocker.
- No tracker update is required unless milestone state or the next unfinished checkpoint changes.
- Before M8 closeout, review this note and either:
  - map reserved items to a future checkpoint / milestone explicitly, or
  - confirm they remain intentionally deferred.
