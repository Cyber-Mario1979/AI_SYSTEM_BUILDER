# Progress_Tracker

## Project

AI_SYSTEM_BUILDER

## Current Phase

Phase 2 — Deterministic System Modeling

## Current Milestone

Milestone 4 — Indexing Layer

## Milestone 1 — State CLI Tool v1

Status: Completed

Completed:

- package-based CLI was previously verified through the project tracker history
- state file operations exist in the current code snapshot:
  - `state init`
  - `state show`
  - `state set-version`
  - `state set-status`
- state loading handles:
  - missing file
  - invalid JSON
  - validation errors
- strict schema validation exists through Pydantic models
- state CLI tests are present in the current snapshot

## Milestone 2 — Mini Deterministic Engine

Status: Completed

Completed:

- `TaskModel` exists and currently includes:
  - `task_id`
  - `order`
  - `title`
  - `status`
  - `dependencies`
- `StateModel` includes `tasks`
- deterministic task ID generation exists
- deterministic task ordering exists
- reusable task helper logic exists, including:
  - `find_task_by_id(...)`
  - `filter_tasks_by_status(...)`
  - `filter_tasks(...)`
  - `update_task_status(...)`
  - `delete_task_by_id(...)`
  - `set_task_dependencies(...)`
  - `validate_task_dependencies(...)`
  - `validate_task_status_transition(...)`
  - `validate_task_completion_readiness(...)`
- task CLI operations exist in the current snapshot:
  - `task add`
  - `task list`
  - `task show`
  - `task update-status`
  - `task set-dependencies`
  - `task delete`
- deterministic filtering exists through:
  - `--status`
  - `--has-dependencies true|false`
- dependency validation and dependency write protection exist
- dependency-aware completion gating exists for `-> completed`
- helper-level tests and CLI tests for Milestone 2 behavior are present in the current snapshot
- Milestone 2 remains aligned with the previously verified closeout state

## Milestone 3 — Task Entity Enrichment

Status: Completed

Reality snapshot:

- pre-existing overlap:
  - `title` already exists on `TaskModel`
- implemented in the current verified live repo:
  - `description`
  - `owner`
  - `duration`
  - `start_date`
  - `end_date`
- backward compatibility currently exists for older task records missing:
  - `dependencies`
  - `description`
  - `owner`
  - `duration`
  - `start_date`
  - `end_date`
- `task add` now accepts optional:
  - `description`
  - `owner`
  - `duration`
  - `start_date`
  - `end_date`
- Milestone 3 now includes all five narrow enrichment slices
- Milestone 3 closeout was manually verified in this session through:
  - fresh-state UAT pass
  - legacy backward-compatibility UAT pass
  - original live state restore verification
  - clean git working tree verification after UAT restore

## Milestone 4 — Indexing Layer

Status: In progress

Reality snapshot:

- the Milestone 4 planning checkpoint was completed in this session
- the first narrow slice is locked as:
  - deterministic secondary task lookup surface
- the purpose of the second indexing surface is locked as:
  - reference and look up tasks without relying only on raw `task_id`
- the identity / lookup separation is locked as:
  - `task_id` = storage identity
  - secondary lookup surface = deterministic access / reference layer
- Milestone 4 slice 1 is now implemented in the current verified live repo as:
  - `task_key` model support
  - backward-compatible `task_key` normalization surface during validated state loading
  - deterministic task reference resolution helper
  - `task show` read-path fallback from exact `task_id` to normalized `task_key`
- Milestone 4 slice 1 was manually verified in this session through:
  - local full-suite pass
  - manual task lookup by `task_id`
  - manual task lookup by `task_key`
  - cleanup of temporary manual verification state edit
- Milestone 4 slice 2 is now implemented in the current verified live repo as:
  - deterministic `task_key` write-path support on task creation
  - normalized `task_key` persistence during `task add`
  - duplicate normalized `task_key` rejection before save
  - CLI support for optional `--task-key`
- Milestone 4 slice 2 was manually verified in this session through:
  - manual task add with `--task-key`
  - manual task show by exact `task_id`
  - manual task show by normalized `task_key`
  - manual duplicate normalized `task_key` rejection
  - cleanup of temporary patch/script artifacts
  - restore of `data/state/state.json` after manual verification
- the Milestone 4 slice 3 planning checkpoint was completed in this session
- the next narrow slice is locked as:
  - deterministic task reference resolution expansion across existing task mutation commands
- the slice 3 scope boundary is locked as:
  - expand target-task resolution in:
    - `task update-status`
    - `task delete`
    - `task set-dependencies`
  - resolve by exact `task_id` first, then normalized `task_key`
  - preserve `task_id` as storage identity
  - preserve existing CLI contract / output behavior
  - keep dependency payload inputs `task_id`-based in this slice
- Milestone 4 slice 3 is now implemented in the current verified live repo as:
  - deterministic task reference resolution expansion across existing task mutation commands
  - `task update-status` target resolution by exact `task_id` first, then normalized `task_key`
  - `task delete` target resolution by exact `task_id` first, then normalized `task_key`
  - `task set-dependencies` target resolution by exact `task_id` first, then normalized `task_key`
  - dependency payload inputs remain `task_id`-based in this slice
  - dependency validation output contract is preserved:
    - `Dependency validation failed:`
    - `- <error>`
- Milestone 4 slice 3 was manually verified in this session through:
  - manual `task update-status` pass by exact `task_id`
  - manual `task update-status` pass by normalized `task_key`
  - manual `task delete` pass by exact `task_id`
  - manual `task delete` pass by normalized `task_key`
  - manual `task set-dependencies` pass by exact `task_id`
  - manual `task set-dependencies` pass by normalized `task_key`
  - manual unknown-target dependency contract pass
  - manual dependency-validation contract pass through normalized `task_key` target
  - restore of `data/state/state.json` after manual verification
  - clean git working tree verification after restore
- the Milestone 4 slice 4 planning checkpoint was completed in this session
- the next narrow slice is locked as:
  - deterministic dependency reference resolution expansion
- the slice 4 scope boundary is locked as:
  - expand dependency input resolution in:
    - `task set-dependencies`
  - resolve each dependency input by exact `task_id` first, then normalized `task_key`
  - preserve `task_id` as storage identity for persisted dependencies
  - preserve existing CLI contract / output behavior
  - do not add new indexing surfaces in this slice
- Milestone 4 slice 4 is now implemented in the current verified local repo as:
  - deterministic dependency reference resolution expansion in `task set-dependencies`
  - dependency inputs resolve by exact `task_id` first, then normalized `task_key`
  - resolved dependency references persist as `task_id` only
  - dependency validation output contract is preserved:
    - `Dependency validation failed:`
    - `- <error>`
- Milestone 4 slice 4 was manually verified in this session through:
  - temporary manual verification state creation with:
    - `TASK-001` / `prepare-fat`
    - `TASK-002` / `execute-fat`
    - `TASK-003` / `review-fat-package`
  - manual `task set-dependencies "review-fat-package" TASK-001 " execute-fat "` success pass
  - manual unknown dependency contract pass through:
    - `task set-dependencies TASK-003 "prepare-fat" "missing-key"`
  - manual self-dependency validation contract pass through:
    - `task set-dependencies "review-fat-package" "review-fat-package"`
  - manual persisted-storage verification through:
    - `task show TASK-003`
    - stored dependencies remained:
      - `TASK-001`
      - `TASK-002`
- Milestone 4 remains in progress after slice 4 implementation:
  - slice 5 planning is still pending
  - no Milestone 5 work package drift
  - no multiple indexing surfaces in the same slice

## Current verified validation status

- fresh local full-suite result verified in this session:
  - `68 passed in 5.82s`
- targeted local dependency CLI tests verified in this session:
  - `8 passed, 23 deselected in 1.32s`
- manual Milestone 4 slice 4 verification completed in this session:
  - `task set-dependencies "review-fat-package" TASK-001 " execute-fat "` succeeded with:
    - `Task dependencies updated: TASK-003 -> ['TASK-001', 'TASK-002']`
  - `task set-dependencies TASK-003 "prepare-fat" "missing-key"` preserved:
    - `Dependency validation failed:`
    - `- Dependency task not found: missing-key`
  - `task set-dependencies "review-fat-package" "review-fat-package"` preserved:
    - `Dependency validation failed:`
    - `- Task cannot depend on itself: TASK-003`
  - `task show TASK-003` confirmed persisted dependencies as:
    - `TASK-001`
    - `TASK-002`
- previous fresh local full-suite result verified in this session:
  - `64 passed in 4.90s`
- manual Milestone 4 slice 3 verification completed in this session:
  - `task update-status TASK-001 in_progress` succeeded
  - `task update-status " Execute_FAT " in_progress` resolved successfully to `TASK-002`
  - `task set-dependencies TASK-003 TASK-001 TASK-002` succeeded
  - `task set-dependencies " Review_FAT Package " TASK-001 TASK-002` resolved successfully to `TASK-003`
  - `task delete TASK-002` succeeded
  - `task delete " Review_FAT Package "` resolved successfully to `TASK-003`
  - `task set-dependencies TASK-999 TASK-001` preserved:
    - `Dependency validation failed:`
    - `- Task not found: TASK-999`
  - `task set-dependencies " Review_FAT Package " TASK-003 TASK-999` preserved:
    - `Dependency validation failed:`
    - `- Task cannot depend on itself: TASK-003`
    - `- Dependency task not found: TASK-999`
  - `data/state/state.json` was restored with `git restore`
  - `git status` was clean after restore
- previous fresh local full-suite result verified in this session:
  - `64 passed in 4.84s`
- current local slice 3 code/test evidence reviewed in this session:
  - full suite passes with the slice 3 patch present in the local editor
  - `handle_task_update_status(...)` resolves the target task through `find_task_by_reference(...)`
  - `handle_task_delete(...)` resolves the target task through `find_task_by_reference(...)`
  - `handle_task_set_dependencies(...)` resolves the target task through `find_task_by_reference(...)`
  - dependency validation output remains two-line in the local patch:
    - `Dependency validation failed:`
    - `- <error>`
- previous fresh local full-suite result verified in this session:
  - `64 passed in 4.92s`
- manual Milestone 4 slice 2 verification completed in this session:
  - `task add "Prepare FAT protocol" --task-key " Prepare_FAT Protocol "` succeeded
  - persisted `task_key` normalized to `prepare-fat-protocol`
  - `task show TASK-011` resolved successfully by `task_id`
  - `task show prepare-fat-protocol` resolved successfully by normalized `task_key`
  - duplicate normalized `task_key` add attempt was rejected with:
    - `Duplicate task_key is not allowed: prepare-fat-protocol`
  - temporary patch/script artifacts were removed after verification
  - `data/state/state.json` was restored before post-verification `git status`
- previous fresh local full-suite result verified in this session:
  - `60 passed in 4.59s`
- manual Milestone 4 slice 1 verification completed in this session:
  - `task show TASK-001` resolved successfully by `task_id`
  - `task show prepare-fat-protocol` resolved successfully by `task_key`
  - temporary manual verification state edit was cleaned up
  - `task show prepare-fat-protocol` returned not found after cleanup
  - `data/state/state.json` was removed from `git status` before commit flow
- previous fresh local full-suite result verified in this session:
  - `57 passed in 5.63s`
- manual Milestone 3 closeout verification completed in this session:
  - fresh-state UAT passed
  - legacy backward-compatibility UAT passed
  - original live state restored successfully
  - git working tree clean after restore
- previous green result recorded after the `start_date` slice:
  - `56 passed in 5.32s`
- previous green result recorded after the duration slice:
  - `55 passed in 4.39s`
- previous green baseline recorded before the duration slice:
  - `52 passed`
- note:
  - the current local repo verifies cleanly at the test-suite level after the slice 4 implementation and targeted validation
  - manual slice 4 verification used a temporary verification state payload
  - restore of `data/state/state.json` after the temporary slice 4 manual verification has not been re-verified in this tracker update

## Current snapshot evidence reviewed in this session

- uploaded code files reviewed:
  - `cli.py`
  - `state_model.py`
  - `task_logic.py`
- uploaded state snapshot reviewed:
  - `state.json`
- uploaded test files reviewed:
  - `test_state_cli.py`
  - `test_task_cli.py`
  - `test_task_logic.py`
- terminal and screenshot evidence reviewed in this session:
  - duration implementation in `state_model.py`
  - duration wiring in `cli.py`
  - direct-call add test fixes for local `Args` fixtures
  - exact persisted-task assertion updates for `duration: None`
  - green full-suite validation after the duration patch
  - local git commit and push after successful validation
  - start_date implementation in `state_model.py`
  - start_date backward-compatibility normalization in `cli.py`
  - start_date wiring in `task add`
  - targeted test-fix pass and green full-suite validation after the `start_date` patch
  - end_date implementation in `state_model.py`
  - end_date backward-compatibility normalization in `cli.py`
  - end_date wiring in `task add`
  - `tests/test_task_cli.py` updates for persisted-state expectations and direct-call add coverage
  - targeted local check for the `start_date` test after file replacement
  - green full-suite validation after the `end_date` patch
  - manual fresh-state UAT backup creation using the live fixed state path
  - manual fresh-state `state init` / `state show` / `task list` pass
  - manual enriched-task `task add` / `task list` / `task show` pass
  - manual persisted JSON verification for enriched task fields
  - observed live CLI task ID pattern as `TASK-001` during manual UAT
  - manual legacy-state `state show` / `task list` / `task show` pass
  - legacy raw JSON inspection confirming old-style file remained unchanged on read-only commands
  - original live state restored from backup after UAT
  - clean `git status` verification after UAT restore
  - Milestone 4 planning checkpoint lock
  - first narrow Milestone 4 slice lock as deterministic secondary task lookup surface
  - `task_key` field addition in `TaskModel`
  - `task_key` backward-compatibility normalization in validated state loading
  - `normalize_task_key(...)` helper addition
  - `find_task_by_reference(...)` helper addition
  - `task show` fallback wiring from exact `task_id` to normalized `task_key`
  - `tests/test_task_logic.py` updates for `task_key` normalization and duplicate-key read-path coverage
  - `tests/test_task_cli.py` updates for persisted state expectations after `task_key` model expansion
  - green full-suite validation after the `task_key` slice patch
  - manual temporary `task_key` insertion into live state for read-path verification
  - manual `task show` pass by `task_id`
  - manual `task show` pass by `task_key`
  - cleanup verification showing `task show` by removed `task_key` returns not found
  - cleanup verification showing `data/state/state.json` removed from `git status`
  - live repo fetch confirmation for:
    - `asbp/cli.py`
    - `asbp/state_model.py`
    - `asbp/task_logic.py`
    - `tests/test_state_cli.py`
    - `tests/test_task_cli.py`
    - `tests/test_task_logic.py`
  - narrow slice 2 lock as deterministic `task_key` write-path support
  - scripted local patch application for:
    - `asbp/cli.py`
    - `asbp/task_logic.py`
    - `tests/test_task_logic.py`
    - `tests/test_task_cli.py`
  - green full-suite validation after the slice 2 patch
  - manual `task add` pass with `--task-key`
  - manual `task show` pass by exact `task_id` after write-path patch
  - manual `task show` pass by normalized `task_key` after write-path patch
  - manual duplicate normalized `task_key` rejection pass
  - cleanup verification showing `apply_m4_slice2.py` removed
  - cleanup verification showing `m4_slice2.patch` removed
  - cleanup verification showing only intended implementation/test files remain modified in `git status`
  - Milestone 4 slice 3 planning checkpoint lock
  - narrow slice 3 lock as deterministic task reference resolution expansion across existing task mutation commands
  - slice 3 scope lock for:
    - `task update-status`
    - `task delete`
    - `task set-dependencies`
  - iterative local `cli.py` patching for slice 3 target resolution and CLI contract preservation
  - screenshot review confirming final local `handle_task_set_dependencies(...)` no longer reassigns the returned task payload back into `state.tasks`
  - green full-suite validation after the slice 3 local patch:
    - `64 passed in 4.84s`
  - live repo re-fetch confirmation after push showing slice 3 patch present in `asbp/cli.py`
  - manual temporary test-state creation for slice 3 CLI verification
  - manual `task list` pass on the temporary slice 3 verification state
  - manual `task update-status` pass by exact `task_id`
  - manual `task update-status` pass by normalized `task_key`
  - manual `task set-dependencies` pass by exact `task_id`
  - manual `task set-dependencies` pass by normalized `task_key`
  - manual `task delete` pass by exact `task_id`
  - manual `task delete` pass by normalized `task_key`
  - manual unknown-target dependency contract pass
  - manual dependency-validation contract pass through normalized `task_key` target
  - manual `git restore data/state/state.json` pass after slice 3 verification
  - clean `git status` verification after restore
  - green full-suite validation after slice 3 manual verification:
    - `64 passed in 4.90s`
  - Milestone 4 slice 4 planning checkpoint lock
  - narrow slice 4 lock as deterministic dependency reference resolution expansion
  - slice 4 scope lock for:
    - `task set-dependencies` dependency inputs
  - repo-aligned local `cli.py` patching for slice 4 dependency input resolution and CLI contract preservation
  - repo-aligned `tests/test_task_cli.py` updates for slice 4 dependency input coverage
  - green full-suite validation after the slice 4 local patch:
    - `68 passed in 5.82s`
  - targeted local dependency CLI test pass:
    - `8 passed, 23 deselected in 1.32s`
  - temporary manual verification state creation for slice 4 CLI verification
  - manual `task set-dependencies` mixed reference success pass
  - manual unknown dependency contract pass through task_key dependency input
  - manual self-dependency validation pass through task_key dependency input
  - manual `task show TASK-003` persisted-storage verification pass after slice 4 manual verification

## Current verified code snapshot

- state persistence and validation logic are present
- task creation is deterministic by ID and order
- task listing supports deterministic filtering
- task show returns structured task JSON
- task deletion is targeted by identity
- dependency writes are validated before save
- invalid dependency writes are rejected without overwriting prior valid state
- status transitions are validated before save
- blocked completion does not mutate task status when dependencies are incomplete
- older task records are normalized for missing `dependencies` during raw state loading
- `TaskModel` now includes optional `description`
- older task records are normalized for missing `description` during validated state loading
- `task add` now supports optional `--description`
- `TaskModel` now includes optional `owner`
- older task records are normalized for missing `owner` during validated state loading
- `task add` now supports optional `--owner`
- `TaskModel` now includes optional `duration`
- older task records are normalized for missing `duration` during validated state loading
- `task add` now supports optional `--duration`
- `TaskModel` now includes optional `start_date`
- older task records are normalized for missing `start_date` during validated state loading
- `task add` now supports optional `--start-date`
- `TaskModel` now includes optional `end_date`
- older task records are normalized for missing `end_date` during validated state loading
- `task add` now supports optional `--end-date`
- `TaskModel` now includes optional `task_key`
- older task records are normalized for missing `task_key` during validated state loading
- `normalize_task_key(...)` exists for deterministic secondary lookup normalization
- `find_task_by_reference(...)` exists for deterministic task lookup by exact `task_id` then normalized `task_key`
- duplicate normalized `task_key` lookup fails clearly rather than guessing
- `task show` now resolves by exact `task_id` first, then by normalized `task_key`
- `prepare_task_key_for_write(...)` exists for deterministic normalized `task_key` write-path validation
- `task add` now supports optional `--task-key`
- `task add` now persists normalized `task_key` values
- duplicate normalized `task_key` writes are rejected before save
- `task update-status` now resolves the target task by exact `task_id` first, then normalized `task_key`
- `task delete` now resolves the target task by exact `task_id` first, then normalized `task_key`
- `task set-dependencies` now resolves the target task by exact `task_id` first, then normalized `task_key`
- `task set-dependencies` now resolves dependency inputs by exact `task_id` first, then normalized `task_key`
- resolved dependency inputs are persisted as `task_id` only
- dependency validation output contract remains preserved in the live slice 4 implementation
- current live CLI uses a fixed state path at `data/state/state.json`
- current live repo generates task IDs in `TASK-###` format during CLI task creation
- manual closeout UAT confirms enriched task fields persist correctly from a fresh initialized state
- manual closeout UAT confirms safe load behavior for legacy task records missing enriched fields
- manual Milestone 4 slice 1 verification confirms deterministic task lookup by both `task_id` and `task_key`
- manual Milestone 4 slice 2 verification confirms deterministic `task_key` write-path behavior without reopening Milestone 2 behavior
- current local validation confirms the `description`, `owner`, `duration`, `start_date`, `end_date`, and `task_key` surfaces without reopening Milestone 2 behavior
- manual Milestone 4 slice 3 verification confirms deterministic mutation-command target resolution by both `task_id` and normalized `task_key`
- manual Milestone 4 slice 4 verification confirms deterministic dependency-input resolution by both `task_id` and normalized `task_key`
- manual Milestone 4 slice 4 verification confirms persisted dependency storage remains `task_id`-only after reference resolution

## Latest completed step

Milestone 4 slice 4 implementation checkpoint

Completed:

- verified the local repo contains slice 4 dependency-reference resolution expansion in `task set-dependencies`
- verified dependency inputs now resolve by:
  - exact `task_id`
  - normalized `task_key`
- verified resolved dependency references persist as:
  - `task_id` only
- added repo-aligned CLI tests for:
  - dependency input resolution by `task_key`
  - mixed `task_id` / `task_key` dependency inputs
  - unknown dependency contract preservation
  - self-dependency validation through `task_key` resolution
- validated the full local suite after slice 4 implementation:
  - `68 passed in 5.82s`
- validated targeted dependency CLI tests after slice 4 implementation:
  - `8 passed, 23 deselected in 1.32s`
- manually verified persisted dependency storage through:
  - `task show TASK-003`
- manually verified CLI contract preservation for:
  - unknown dependency through dependency-reference resolution
  - self-dependency through dependency-reference resolution

## Exact next unfinished step

Milestone 4 slice 5 planning checkpoint

Next objective:

- lock the next narrow Indexing Layer slice after slice 4 dependency-reference resolution expansion
- stay inside the Indexing Layer milestone
- avoid Milestone 5 drift
- do not claim slice 5 scope or implementation until the planning checkpoint is recorded