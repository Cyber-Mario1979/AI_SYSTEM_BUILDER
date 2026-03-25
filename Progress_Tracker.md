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
  - introduced explicit `TaskStatus` typing for task-domain helpers
- Refactor Step 2 completed:
  - added direct helper-level tests in `tests/test_task_logic.py`
  - validated through full-suite pass and narrower helper checks
- Refactor Step 3 completed:
  - rewired `asbp/cli.py` task handlers to call extracted functions from `asbp/task_logic.py`
  - preserved CLI behavior and user-facing output
- Refactor checkpoint committed locally after validation

## Current verified test status

- Full suite passed:
  - `39 passed`

## Current verified runtime behavior

- `python -m asbp task show TASK-001` returns the correct task JSON
- `python -m asbp task list` works
- `python -m asbp task list --status planned` works
- `python -m asbp task update-status TASK-001 completed` works
- `python -m asbp task delete TASK-002` works
- Follow-up CLI verification confirmed expected persisted state changes after update and delete

## Current verified state of the system

- Project state is persisted and validated.
- Tasks can be added deterministically.
- Tasks can be listed in full.
- Tasks can be filtered by status.
- Tasks can be shown by identity.
- Tasks can have status updated deterministically.
- Tasks can be deleted by identity.
- New task IDs are generated sequentially:
  - `TASK-001`, `TASK-002`, etc.
- Task-domain logic is now separated more cleanly from CLI handler logic.
- The task-engine feature slice is implemented, refactored, tested, and checkpoint-committed.

## Latest completed step

Milestone 2 task-engine refactor checkpoint:

- extracted repeated task-domain logic into `asbp/task_logic.py`
- added direct helper tests
- rewired CLI handlers to call extracted helpers
- validated with `python -m pytest -q`
- manually verified real CLI behavior
- committed the refactor checkpoint locally

## Exact next unfinished step

Milestone 2 planning checkpoint:

- lock the next post-refactor build slice before coding
- keep the work inside Milestone 2
- choose the next deterministic engine target from the roadmap instead of jumping ahead

## Refactor mode status

- Refactor checkpoint completed
- No open refactor step remains from the task-logic extraction plan
- Resume normal milestone sequencing from the next locked Milestone 2 build slice

# Progress Tracker Update

## Phase 1 --- Foundations

## Milestone 2 --- Mini Deterministic Engine

### Completed

- Task CRUD
- Task Ordering
- Dependency Data Support
- Dependency Validation Helpers (Step 2)

### Next

- Dependency Enforcement (Step 3)
