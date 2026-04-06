# ROADMAP_ADDENDUM_TEST_INTEGRITY_RESTORATION

## Purpose

This addendum authorizes a corrective restoration path when previously validated test coverage is accidentally reduced, overwritten, fragmented, or misplaced during later milestone work.

It does not replace the canonical roadmap.
It temporarily supplements it for corrective recovery only.

## Authority

This addendum is subordinate to `ROADMAP_CANONICAL.md`.

It exists because the canonical roadmap requires direction to be updated before execution continues when a proposed slice does not clearly fit the currently declared slice family.

## Scope of this addendum

This addendum applies only to:

- accidental loss of already validated tests
- accidental replacement of one test surface by another
- accidental fragmentation of test coverage that materially reduces validation breadth
- restoration work needed to recover prior validated coverage without changing runtime behavior

This addendum does not authorize:

- new feature expansion
- milestone drift
- behavioral redesign
- bypassing milestone boundaries
- bypassing UAT policy

## Corrective integrity restoration rule

If later implementation work accidentally overwrites, removes, replaces, fragments, or materially reduces previously validated test coverage:

1. pause further feature expansion
2. classify the situation as corrective integrity restoration
3. restore the lost or overwritten tests first
4. separate misplaced tests into the correct files when needed
5. preserve current runtime behavior during restoration
6. resume normal milestone slicing only after validation breadth is restored

## Allowed corrective work under this addendum

Allowed work:

- restore overwritten task CLI tests
- recover previously validated test cases from repo history
- move WP CLI tests into a dedicated WP test file
- re-establish clean task test versus WP test separation
- perform test-only structural cleanup needed to restore validation breadth
- run full validation and record the corrected result

## Not allowed under this addendum

Not allowed:

- adding new runtime commands
- extending CLI behavior
- introducing new filters or new entity relationships
- changing persistence contracts
- changing model behavior
- using restoration as a pretext for new feature delivery

## Pause rule

While this addendum is active, the following planned slice is paused:

- Milestone 5 tenth implementation checkpoint — deterministic `wp list --title <title>` read surface

No further Milestone 5 feature expansion should continue until corrective restoration is completed and validated.

## Current application of this addendum

This addendum is activated by the observed validation regression during Milestone 5, where:

- the recorded validated count dropped from the earlier higher full-suite level to a much lower count
- repo history shows the drop coincided with changes to `tests/test_task_cli.py`
- the earlier repo version contained a large task CLI suite
- the later repo state shows WP-focused tests occupying that file instead

Therefore, corrective restoration is authorized before any further WP feature slices continue.

## Locked next checkpoint under this addendum

Corrective integrity restoration checkpoint — restore the overwritten task CLI test suite and separate WP CLI tests into their own dedicated test file, with no runtime behavior changes.

## Exit condition for this addendum

This addendum remains active until all of the following are true:

- the overwritten task CLI tests are restored
- WP CLI tests are separated into their own dedicated file
- no runtime behavior changes were introduced during restoration
- full validation passes
- normal milestone slicing can resume from the last valid roadmap-aligned position
