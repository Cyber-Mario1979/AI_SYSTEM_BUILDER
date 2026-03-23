# Milestone 1 Scope — State CLI Tool v1

## Phase

Phase 1 — Foundations

## Milestone

Milestone 1 — State CLI Tool v1

## Status

Completed

## Purpose

Establish the first real local software backbone for the AI Systems Builder Program by building a package-based CLI tool that manages validated persistent runtime state safely and predictably.

## Why this milestone exists

This milestone introduces the first deterministic system layer in the project.

It is meant to teach and prove the foundations of:

- package-based execution
- CLI structure
- argument parsing
- persistent state handling
- validation
- safe mutation
- basic testing discipline

This milestone is intentionally small, local, and rule-based.

## Scope Goal

Build a working local CLI for the `asbp` package that can initialize, show, and update persistent runtime state.

## In Scope

### Package and CLI foundation

- package-based execution through `python -m asbp`
- CLI entry flow
- parser-driven command routing
- central parser construction pattern

### Runtime state management

- initialize a state file
- display current state
- update simple state fields
- persist state safely to disk

### State commands

- `state init`
- `state show`
- `state set-version`
- `state set-status`

### Validation and safety

- Pydantic-backed runtime state validation
- safe JSON loading
- safe validated saving
- missing-file handling
- invalid JSON handling
- validation error handling

### Refactoring targets

- separate parser construction from command behavior
- keep handlers thinner
- extract repeated logic into shared helpers
- introduce reusable mutation flow

### Minimum testing scope

- basic automated CLI verification
- core command behavior checks
- invalid input / invalid file handling checks

## Out of Scope

The following are explicitly not part of Milestone 1:

- task models
- task creation
- task export
- deterministic planning logic
- scheduling
- dependency graphs
- LLM integration
- API integration
- advanced logging architecture
- multi-entity domain models

## Expected Deliverable

A local CLI that:

- runs through `python -m asbp`
- creates and reads a persistent runtime state file
- validates state structure
- updates simple validated fields
- handles common file/state failure cases safely
- has minimal automated tests

## Final Delivered Outcome

Milestone 1 finished with:

- working package-based CLI
- `state init`
- `state show`
- `state set-version`
- `state set-status`
- strict `StateModel` validation
- safe file handling
- shared helpers and handler refactor
- minimal milestone test suite passing

## Final Runtime State at Milestone Close

- project: `AI_SYSTEM_BUILDER`
- version: `0.8.0`
- status: `in_progress`

## Success Criteria

Milestone 1 is considered complete when:

- the package runs correctly from the CLI
- runtime state can be initialized
- runtime state can be shown
- version can be updated safely
- status can be updated safely
- persisted data is validated
- bad file/state conditions are handled safely
- minimal automated tests pass

## Architectural Outcome

This milestone establishes the foundation for future milestones by proving:

- local deterministic execution
- validated state as a system backbone
- separation between parsing, handling, validation, mutation, and persistence
- a maintainable path toward a larger deterministic engine

## Next Milestone

Milestone 2 — Mini Deterministic Engine
