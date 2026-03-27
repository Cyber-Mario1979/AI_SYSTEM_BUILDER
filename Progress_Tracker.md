# Progress_Tracker

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
- Dependency Handling — Step 3 completed:
  - added `set_task_dependencies(...)` to `asbp/task_logic.py`
  - wired dependency validation into the real mutation/update path
  - added CLI mutation path for dependency updates:
    - `python -m asbp task set-dependencies <TASK_ID> [DEPENDENCY_IDS...]`
  - rejected invalid dependency writes before save
  - preserved last valid dependency state after invalid write attempts
  - kept patch surface minimal without unrelated refactors
- Advanced Filtering / Querying — Step 1 completed:
  - added read-only helper `filter_tasks(...)`
  - supports deterministic multi-condition filtering by:
    - `status`
    - `has_dependencies`
  - preserves original task order
  - added direct helper-level tests for advanced filtering behavior
- Advanced Filtering / Querying — Step 2 completed:
  - extended `task list` CLI surface with:
    - `--has-dependencies true`
    - `--has-dependencies false`
  - wired CLI filtering through `filter_tasks(...)`
  - preserved existing `--status` filtering behavior
  - validated helper behavior, CLI behavior, and full-suite compatibility
- State Transition Rules — Step 1 completed:
  - added `validate_task_status_transition(...)`
  - defined allowed task transitions:
    - `planned -> in_progress`
    - `in_progress -> completed`
  - rejected:
    - same-status transitions
    - reverse transitions
    - skipped transitions
    - transitions out of `completed`
    - transitions out of `over_due`
  - added direct helper-level tests for transition validation
- State Transition Rules — Step 2 completed:
  - enforced `validate_task_status_transition(...)` inside `update_task_status(...)`
  - kept CLI command surface unchanged:
    - `python -m asbp task update-status <TASK_ID> <STATUS>`
  - updated test coverage to validate enforcement on real `TaskModel` objects
  - validated helper enforcement, CLI mutation behavior, and persisted runtime behavior
  - committed and pushed after validation

## Current verified test status

- Full suite passed:
  - `44 passed`

## Current verified runtime behavior

- `python -m asbp task show TASK-003` returns task JSON including `dependencies`
- valid dependency write succeeds through CLI mutation path
- invalid dependency write is rejected and does not save
- prior valid dependency state remains unchanged after failed invalid write
- `python -m asbp task list --status completed` returns only completed tasks
- `python -m asbp task list --has-dependencies true` returns only tasks with one or more dependencies
- `python -m asbp task list --has-dependencies false` returns only tasks with zero dependencies
- combined filtering works through:
  - `python -m asbp task list --status planned --has-dependencies true`
- `python -m asbp task update-status TASK-004 in_progress` succeeds
- `python -m asbp task update-status TASK-004 planned` is rejected with:
  - `Invalid status transition: in_progress -> planned`
- rejected invalid transition does not persist
- `python -m asbp task update-status TASK-004 completed` succeeds after `in_progress`
- `python -m asbp task show TASK-004` confirms the final persisted status after each runtime check
- note:
  - `TASK-002` had already been deleted in prior delete-feature testing
  - manual dependency validation previously used `TASK-004` as the second valid dependency target

## Current verified state of the system

- Project state is persisted and validated
- Tasks can be added deterministically
- Tasks can be listed in full
- Tasks can be filtered by status
- Tasks can be filtered by dependency presence
- Tasks can be filtered by combined deterministic query conditions
- Tasks can be shown by identity
- Tasks can have status updated deterministically
- Tasks can have status transitions validated before save
- Invalid task status transitions are blocked before state save
- Tasks can be deleted by identity
- Task ordering is explicit and deterministic
- Tasks support dependency data
- Dependency validation exists as reusable helper logic
- Dependency enforcement now exists in the real mutation/update path
- Invalid dependency writes are blocked before state save

## Latest completed step

State Transition Rules — Step 2 (Enforcement)

Completed:

- transition validation wired into the real task status mutation path
- invalid status transitions rejected
- invalid task status state prevented from being saved
- helper and CLI behavior validated locally
- narrower/manual verification completed successfully
- committed and pushed after validation

## Exact next unfinished step

Milestone 2 planning checkpoint after State Transition Rules — Step 2

Next objective:

- confirm the next exact unfinished Milestone 2 slice from the local roadmap/tracker
- do not reopen Advanced Filtering / Querying or State Transition Rules Steps 1–2
- continue only from the next agreed post-Step-2 item
