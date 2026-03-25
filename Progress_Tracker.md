# Progress_Tracker_2026-03-25

## Project

AI_SYSTEM_BUILDER

## Current Phase

Phase 1 — Foundations

## Current Milestone

Milestone 2 — Mini Deterministic Engine

## Milestone 1 — State CLI Tool v1

Status: Completed

Completed:

- Package-based CLI via `python -m asbp`
- `state init`
- `state show`
- `state set-version`
- `state set-status`
- Safe missing-file handling
- Invalid JSON handling
- Validation error handling
- Shared helpers:
  - `load_state_or_none()`
  - `update_state_field(...)`
- Strict schema validation with Pydantic
- Milestone 1 tests passed

## Milestone 2 — Mini Deterministic Engine

Status: In Progress

Completed in Milestone 2 so far:

- Milestone 2 planning note created
- `TaskModel` added
- `StateModel` extended with `tasks`
- Project status vocabulary redesigned:
  - `not_started`
  - `in_flight`
  - `completed`
- Task status vocabulary defined:
  - `planned`
  - `in_progress`
  - `completed`
  - `over_due`
- Deterministic helper module created:
  - `asbp/task_logic.py`
- Deterministic helper implemented:
  - `generate_next_task_id(tasks)`
- Task CLI operations implemented and verified:
  - `task add`
  - `task list`
  - `task update-status`
  - `task delete`
  - `task show`
- Status-filtered task listing implemented and verified:
  - `task list --status <value>`
- Refactor Step 1 completed:
  - expanded `asbp/task_logic.py`
  - added reusable task-domain functions:
    - `find_task_by_id(...)`
    - `filter_tasks_by_status(...)`
    - `update_task_status(...)`
    - `delete_task_by_id(...)`
- Refactor Step 2 completed:
  - added direct helper-level tests in `tests/test_task_logic.py`
  - validated through full-suite pass and narrower helper checks
- Refactor Step 3 completed:
  - rewired `asbp/cli.py` task handlers to call extracted functions from `asbp/task_logic.py`
  - preserved CLI behavior and user-facing output
- Refactor checkpoint committed locally after validation
- Task sequencing / ordering completed, validated locally, and committed locally
- Dependency Handling — Step 1 completed:
  - added `dependencies` field to `TaskModel`
  - preserved backward compatibility for older task records during state loading
  - updated CLI/test expectations for normalized dependency data
- Dependency Handling — Step 2 completed:
  - added `validate_task_dependencies(...)`
  - implemented self-dependency rejection
  - implemented duplicate dependency rejection
  - implemented missing dependency ID rejection
  - added direct helper-level tests for dependency validation

## Current verified test status

- Full suite passed:
  - `40 passed`

## Current verified runtime behavior

- `python -m asbp task show TASK-001` returns task JSON including `dependencies`
- `python -m asbp task list` works
- `python -m asbp task list --status planned` works
- `python -m asbp task update-status TASK-001 completed` works
- `python -m asbp task delete TASK-002` works

## Current verified state of the system

- Project state is persisted and validated
- Tasks can be added deterministically
- Tasks can be listed in full
- Tasks can be filtered by status
- Tasks can be shown by identity
- Tasks can have status updated deterministically
- Tasks can be deleted by identity
- Task ordering is explicit and deterministic
- Tasks now support dependency data
- Dependency validation exists as reusable helper logic
- Invalid dependency detection is implemented for:
  - self-dependency
  - duplicate dependency IDs
  - missing dependency IDs

## Latest completed step

Dependency Handling — Step 2 (Validation Helpers)

Completed:

- dependency data support already in place
- dependency validation helper added
- dependency validation tests added
- validated locally with `python -m pytest -q`

## Exact next unfinished step

Dependency Handling — Step 3 (Enforcement)

Next objective:

- wire dependency validation into the real mutation/update path
- reject invalid dependency writes
- prevent saving invalid dependency state
- keep patch surface minimal
- no unrelated refactors
