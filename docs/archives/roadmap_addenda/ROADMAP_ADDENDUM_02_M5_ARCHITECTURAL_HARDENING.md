---
doc_type: roadmap_addendum
canonical_name: ROADMAP_ADDENDUM_02_M5_ARCHITECHTURAL_HARDENING.md
status: COMPLETED_HISTORICAL
governs_execution: false
authority: subordinate_to_ROADMAP_CANONICAL
scope_type: temporary_overlay
milestone_scope: M5
phase_scope: Phase 2
archive_location: docs/archives/roadmap_addenda/
reason_kept: historical_traceability
---

# ROADMAP_ADDENDUM_02_M5_ARCHITECTURAL_HARDENING

## Purpose

This addendum authorizes a bounded architectural hardening path inside Milestone 5 when the current implementation remains functionally correct but the adapter/core boundary is becoming too CLI-heavy for safe downstream expansion.

It does not replace the canonical roadmap.
It temporarily supplements it for architectural hardening only.

## Authority

This addendum is subordinate to `ROADMAP_CANONICAL.md`.

It exists because the canonical roadmap requires direction to be updated before execution continues when a proposed slice does not clearly fit the currently declared slice family in its current narrow form.

## Scope of this addendum

This addendum applies only to:

- bounded refactor work needed to reduce current CLI concentration
- improving attachment readiness for future AI and UI layers
- clarifying adapter vs logic vs state responsibilities
- preserving current runtime contracts while relocating logic to cleaner boundaries
- reducing future refactor cost before additional Milestone 5 feature expansion

This addendum does not authorize:

- milestone drift
- moving to Milestone 6
- AI runtime implementation
- UI implementation
- new entity introduction
- task-to-work-package association delivery
- persistence contract redesign
- behavioral redesign of already validated surfaces

## Architectural hardening rule

If the current milestone remains roadmap-aligned functionally, but implementation concentration in CLI risks larger downstream refactor cost, then:

1. pause further feature expansion temporarily
2. classify the work as bounded architectural hardening
3. preserve all validated runtime behavior
4. preserve current persistence contracts
5. preserve current CLI command contracts
6. move logic only where needed to establish cleaner attachment boundaries
7. resume normal milestone slicing only after validation passes

## Current application of this addendum

This addendum is activated during Milestone 5 because:

- Work Package read/write CLI surfaces are expanding
- deterministic behavior remains valid
- current implementation concentration in `cli.py` is becoming architecturally heavier than desired
- future AI/UI attachment readiness should be protected now with a bounded refactor rather than a larger later refactor

Therefore, temporary architectural hardening is authorized before continuing normal Milestone 5 feature expansion.

## Allowed work under this addendum

Allowed work:

- thin the CLI without changing user-facing command behavior
- extract currently implemented Work Package operational logic from `cli.py` into dedicated module(s)
- extract state access/load-save helpers into dedicated module(s) if needed
- consolidate current read/write orchestration boundaries
- preserve exact command names, exact persistence shape, and exact validated behavior
- add or move tests required to preserve or prove behavior during refactor
- run full validation and record the corrected result

## Not allowed under this addendum

Not allowed:

- adding new runtime commands
- extending current behavior beyond existing validated contracts
- adding task-to-work-package association
- changing model invariants
- changing persisted schema shape
- introducing AI adapters
- introducing UI adapters
- using hardening as a pretext for feature expansion

## Pause rule

While this addendum is active, further normal Milestone 5 feature expansion is paused after:

- Milestone 5 eleventh implementation checkpoint — deterministic `wp list --wp-id <wp_id>` read surface

No additional Milestone 5 feature slices should continue until the bounded architectural hardening path is completed and validated.

## Locked next checkpoint under this addendum

Milestone 5 architectural hardening implementation checkpoint 1 — extract current Work Package read/write operational logic out of `cli.py` into dedicated module boundaries while preserving current CLI behavior, persistence contracts, and validated runtime outputs exactly.

## Exit condition for this addendum

This addendum remains active until all of the following are true:

- the approved bounded refactor is completed
- current CLI behavior remains unchanged for already validated surfaces
- persistence contracts remain unchanged
- full validation passes
- tracker explicitly records return to normal Milestone 5 slicing
- session-start continuity note no longer marks this addendum as active
