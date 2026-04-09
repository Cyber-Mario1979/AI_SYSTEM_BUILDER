# UAT README

## Purpose of this folder

This folder contains milestone-level User Acceptance Testing (UAT) documents for the AI System Builder project.

The intent of UAT in this repository is not to replace automated tests.
Instead, it serves as the final milestone-facing acceptance layer after implementation and validation have already reached a stable checkpoint.

Each milestone UAT cycle is documented through two files:

- `M*_UAT_PROTOCOL.md`
- `M*_UAT_Report.md`

## Why this process exists

This process was formally introduced starting at Milestone 4.

The reason was practical rather than ceremonial.
During Milestone 4, execution remained productive, but some milestone-boundary drift became visible in how scope, validation surfaces, and user-facing acceptance evidence were being closed.

That drift was later rebaselined and directed.
After that rebaseline, it became clear that each milestone needed a more explicit acceptance closeout layer.

UAT was therefore adopted as a recurring milestone-close practice in order to:

- confirm that the delivered runtime behavior matches the intended milestone boundary
- create a human-readable acceptance record in addition to automated validation
- reduce ambiguity when deciding whether a milestone is actually closed
- provide a stable review artifact before advancing into the next checkpoint family

## Relationship to automated tests

UAT is not a substitute for `python -m pytest -q`.

The intended sequence is:

1. implementation work reaches the approved milestone boundary
2. automated validation passes
3. milestone UAT is executed against the milestone-facing behavior
4. the UAT result is recorded
5. only then is milestone closeout treated as complete

In other words:

- automated tests prove technical consistency
- UAT proves milestone-facing acceptance

Both are useful, but they are not the same thing.

## Protocol vs Report

### Protocol

The protocol defines:

- what is in scope for milestone acceptance
- what checks must be executed
- what commands or controlled setup are required
- what pass/fail expectations apply

The protocol is the planned acceptance method.

### Report

The report records:

- who executed the UAT
- when it was executed
- whether validation before and after was acceptable
- the pass/fail result of each check
- any notes, deviations, or restoration details
- the final milestone acceptance decision

The report is the execution evidence.

## Folder usage rule

This folder should contain only milestone UAT documents and closely related acceptance records.

Recommended pattern:

- one protocol per milestone when UAT is used
- one report per executed UAT cycle
- no ad-hoc experiment notes here
- no smoke test notes here

## Naming pattern

Current naming pattern:

- `M4_UAT_PROTOCOL.md`
- `M4_UAT_Report.md`
- `M5_UAT_PROTOCOL.md`
- `M5_UAT_Report.md`

This pattern should be preserved going forward for consistency.

## When to create a UAT package

A milestone should receive a UAT package when:

- the milestone boundary is materially complete
- the implementation has passed the required validation checkpoint
- the project is ready for human acceptance review at milestone level

## What UAT is not

UAT in this repository is not:

- a runtime log
- an ad-hoc scratch note
- a substitute for unit or CLI tests
- a replacement for roadmap or tracker governance

## Summary

This folder exists to hold the milestone-level acceptance layer of the project.

It was introduced after Milestone 4 drift exposed the need for a cleaner closeout process.
That drift was rebaselined and redirected, and UAT became the standard milestone acceptance pattern from that point forward.
