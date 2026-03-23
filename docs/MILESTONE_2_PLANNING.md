# Milestone 2 Planning — Mini Deterministic Engine

## Phase

Phase 1 — Foundations

## Milestone

Milestone 2 — Mini Deterministic Engine

## Purpose

Build the first small deterministic core on top of the existing `asbp` CLI and validated runtime state.

This milestone must stay:

- local
- rule-based
- deterministic
- no LLM
- small enough to finish cleanly

## Starting Point

Already completed in Milestone 1:

- package-based CLI
- parser + handlers structure
- validated persistent state
- safe load/save flow
- shared helpers
- minimal tests

## Milestone 2 Goal

Add a tiny rule-based engine that can deterministically create, validate, store, and export simple task records.

## Recommended v1 Scope

### Entity to introduce

A single deterministic `Task` model.

### Minimum task fields

- `task_id`
- `title`
- `status`

### Allowed task statuses

- `planned`
- `in_progress`
- `done`

### Deterministic rules

- task IDs are generated sequentially
- no duplicate task IDs
- no empty title
- status must be valid
- persisted data must validate before save
- export output must be structured and predictable

## Target Deliverable

A mini engine that can:

- load the current state
- create tasks deterministically
- list tasks deterministically
- update task status deterministically
- validate before save
- export tasks into a structured file

## Recommended CLI surface for Milestone 2

- `task add`
- `task list`
- `task set-status`
- `task export`

## Recommended deterministic ID format

Use a simple sequential ID format:

- `TASK-001`
- `TASK-002`
- `TASK-003`

This is preferred over UUIDs for Milestone 2 because:

- easier to read
- easier to test
- fully deterministic
- fits the milestone goal better

## Recommended state shape extension

Extend the existing runtime state with a `tasks` collection.

Example direction:

- existing top-level state remains
- add:
  - `tasks: list[TaskModel]`

## Build Order

1. Define `TaskModel`
2. Extend `StateModel` to include `tasks`
3. Add deterministic task ID generator
4. Add `task add`
5. Add `task list`
6. Add `task set-status`
7. Add `task export`
8. Add tests for deterministic behavior

## What is explicitly out of scope

Do not add these yet:

- priorities
- due dates
- dependencies
- scheduling
- planning graph logic
- multiple export formats
- task deletion
- task editing beyond status
- any LLM behavior

## Success Criteria

Milestone 2 is complete when:

- a task can be added through CLI
- task ID generation is deterministic
- task status updates are validated
- task data persists safely
- task data exports in a predictable structure
- automated tests cover the main flows

## Exact first implementation step

Define the new data contract first:

- create `TaskModel`
- extend `StateModel` with `tasks: list[TaskModel]`

No CLI command changes before the models are defined and validated.
