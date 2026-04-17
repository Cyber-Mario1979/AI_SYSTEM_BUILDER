# M7_UAT_PROTOCOL

## Milestone

Milestone 7 — Planning Layer

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 7 boundary.

It is intended to confirm that the current Milestone 7 runtime behaves correctly for:

- plan identity and deterministic work-package linkage
- planning-basis attachment behavior
- timezone-aware planned-start attachment behavior
- planning-calendar attachment and working-day normalization
- dependency-aware baseline generation from committed collection scope
- ordered plan review payload generation
- deterministic draft-to-committed plan transition
- persisted reload validation for committed plan state
- deterministic failure behavior when generation or commit preconditions are missing

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M7_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `383 passed in 34.98s`

## Operator Fields

- UAT date: `17-04-2026`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 7 currently has no plan CLI adapter in `asbp/cli.py`.

Therefore this UAT is intentionally executed against the repo-real planning/state contract rather than against non-existent CLI plan commands.

This is aligned with the current implementation boundary.

## Scope Covered

The following Milestone 7 surfaces are in scope:

- `generate_next_plan_id(...)`
- `PlanningModel(plan_id, work_package_id, plan_state)`
- `set_plan_planning_basis(...)`
- `set_plan_planned_start_at(...)`
- `set_plan_planning_calendar(...)`
- `generate_plan_baseline(...)`
- `list_plan_review_rows(...)`
- `build_plan_review_payload(...)`
- `commit_plan(...)`
- persisted reload validation for committed plan state
- deterministic rejection when `planning_basis` is missing before baseline generation
- deterministic rejection when `generated_task_plans` is missing before commit

## Test Data / Pre-Setup

Use a controlled temporary test state.

Back up the current state file before execution and restore it after execution.

Recommended pre-run backup pattern:

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force
```
