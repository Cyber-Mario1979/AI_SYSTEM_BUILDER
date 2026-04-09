# M4_UAT_PROTOCOL

## Milestone

Milestone 4 — Indexing Layer

## Protocol Purpose

This protocol defines the user-facing acceptance checks for the Milestone 4 Indexing Layer boundary.

It is intended to confirm that the current Milestone 4 runtime behaves correctly for:

- base task list visibility
- full list visibility bundle behavior
- indexed lookup by `task_key`
- reference-based list filters
- presence-based list filters
- deterministic key lifecycle controls
- invalid reference handling

This file is a UAT protocol only.
Execution evidence and the final acceptance decision should be recorded after execution in the milestone UAT report artifact.

## Protocol Status

Issued for documentation consistency

## Validation Prerequisite

Latest validated technical baseline at original M4 UAT execution time:

- validation before: Pass
- validation after: Pass

## Operator Fields

- UAT date: `(TBD)`
- Operator: `(TBD)`
- Reviewer: `(TBD)`
- Result: `(TBD)`

## Scope Covered

The following Milestone 4 indexing surfaces are in scope:

- base task list surface
- full list visibility bundle
- show by `task_key` with references
- task reference filter
- dependency reference filter
- dependent reference filter
- presence filters
- key lifecycle controls
- invalid reference handling

## Test Data / Pre-Setup

Use a controlled temporary test state.
Back up the current state file before execution and restore it after execution.

Recommended pre-run backup pattern:

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force
```

Initialize the required indexing test state with multiple tasks covering:

- tasks with and without `task_key`
- tasks with dependencies
- tasks with dependents
- valid resolvable task references
- invalid task references for failure behavior checks

## Acceptance Checks

### UAT-M4-01 — Base list surface

Acceptance:

- base task list command succeeds
- list output remains readable and deterministic
- baseline task rows are visible without extra optional surfaces

### UAT-M4-02 — Full list visibility bundle

Acceptance:

- full visibility bundle command succeeds
- the enabled visibility surfaces render together without contract breakage
- default list behavior remains unchanged when bundle flags are absent

### UAT-M4-03 — Show by `task_key` with references

Acceptance:

- show by deterministic `task_key` succeeds
- reference views are shown correctly when requested
- resolved references remain accurate and stable

### UAT-M4-04 — Task reference filter

Acceptance:

- exact task reference filter succeeds
- matching task is returned deterministically
- unrelated tasks are excluded

### UAT-M4-05 — Dependency reference filter

Acceptance:

- dependency reference filter succeeds
- only tasks depending on the specified reference are returned
- unrelated tasks are excluded

### UAT-M4-06 — Dependent reference filter

Acceptance:

- dependent reference filter succeeds
- only tasks that the specified target feeds into are returned through derived dependent logic
- unrelated tasks are excluded

### UAT-M4-07 — Presence filters

Acceptance:

- presence-based filters succeed
- `has_task_key`, `has_dependencies`, and `has_dependents` style checks behave deterministically
- filtered output reflects correct AND logic where combined

### UAT-M4-08 — Key lifecycle controls

Acceptance:

- task key set/clear flows succeed
- normalized key storage remains deterministic
- duplicate or reserved key cases are rejected without invalid mutation

### UAT-M4-09 — Invalid reference handling

Acceptance:

- invalid or unresolved references are handled deterministically
- the runtime returns the expected failure or no-results contract
- valid persisted state remains unchanged after failure handling

## General Acceptance Decision Rule

Recommended milestone decision logic:

- `PASS` if all protocol checks pass with no material deviation
- `CONDITIONAL PASS` if core milestone acceptance is achieved with only minor documented deviations that do not invalidate the Milestone 4 boundary
- `FAIL` if one or more core milestone acceptance checks fail

## Post-Execution Restore

Recommended restore command after UAT execution:

```powershell
Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force
```

## Execution Notes

- Record execution evidence and the final decision in `docs/UAT/M4_UAT_Report.md`
- The existing M4 report remains the execution record for the already completed UAT cycle
- This protocol file is added afterward to keep the UAT document pattern consistent across milestones
