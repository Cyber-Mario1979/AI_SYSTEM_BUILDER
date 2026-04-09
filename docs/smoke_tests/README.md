# Smoke Tests README

## Purpose of this folder

This folder contains smoke-test evidence for quick, targeted verification of already delivered behavior.

Smoke tests in this repository are intentionally lighter than milestone UAT.
They are used to confirm that a critical surface still behaves correctly without running a full milestone acceptance cycle.

## Why this process exists

As the project grew, it became useful to keep a smaller verification layer available between major milestone closeout points.

A full UAT cycle is appropriate for milestone acceptance.
A smoke test is appropriate when the goal is narrower and faster, for example:

- checking that a recently completed slice still behaves correctly
- confirming that a sensitive surface did not drift after a later change
- responding to a targeted review request
- performing a quick audit-style sanity check before or after a change

## Relationship to UAT

Smoke tests do not replace milestone UAT.

The intended distinction is:

- **UAT** = milestone-level acceptance
- **smoke test** = fast confidence check on selected critical behavior

A smoke test may support confidence, but it does not by itself close a milestone.

## Why these tests are ad hoc by request

Smoke tests in this repository are intentionally request-driven rather than mandatory after every single change.

That means they are typically created when there is a specific reason, such as:

- drift concern
- review concern
- audit-style spot check
- targeted confidence need before proceeding

This keeps them useful and lightweight instead of turning them into a second full acceptance workflow.

## What "audit-style" means here

In this repository, an audit-style smoke test means:

- a focused verification request can happen at any time
- the target is usually a narrow surface or a small group of related commands
- the goal is to quickly detect whether the current behavior still matches the expected baseline

This is especially useful when we want to catch drift early without opening a full milestone UAT package.

## Typical smoke test content

A smoke test file may contain:

- controlled setup commands
- one or more focused execution commands
- observed outputs
- optional restore steps
- brief notes about what was confirmed

The format may be lighter and more direct than a formal protocol/report pair.

## Folder usage rule

This folder should contain only smoke-test artifacts and related explanation.

Recommended usage:

- focused verification records
- interim confidence checks
- ad-hoc audit-style command/output evidence

This folder should not be used for:

- milestone UAT protocols
- milestone UAT reports
- long-form planning notes
- general development scratch notes

## Naming pattern

Keep smoke test naming explicit and narrow.

Current example:

- `smoke_test_interim_M5.md`

Future examples should follow the same idea:

- identify that the file is a smoke test
- identify the related milestone or surface
- keep the name readable and specific

## Summary

This folder exists for lightweight, request-driven verification.

Use it when a focused confidence check is needed.
Use `docs/UAT/` when a full milestone acceptance process is needed.
