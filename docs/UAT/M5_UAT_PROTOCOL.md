# M5_UAT_PROTOCOL

## Milestone

Milestone 5 — Work Package Model

## Protocol Purpose

This protocol defines the user-facing acceptance checks for the Milestone 5 Work Package Model boundary.

It is intended to confirm that the current Milestone 5 runtime behaves correctly for:

- Work Package CRUD surfaces
- task-to-work-package association surfaces
- inverse Work Package visibility surfaces
- deterministic validation and failure behavior

This file is a UAT protocol only.
Execution evidence and the final acceptance decision should be recorded after execution in the milestone UAT summary/report artifact.

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- expected supporting result: `241 passed in 24.51s`

## Operator Fields

- UAT date: `(TBD)`
- Operator: `(TBD)`
- Reviewer: `(TBD)`
- Result: `(TBD)`

## Scope Covered

The following Milestone 5 surfaces are in scope:

- `wp list`
- `wp list --status <status>`
- `wp list --title <title>`
- `wp list --wp-id <wp_id>`
- `wp list --task-id <task_id>`
- `wp list --show-task-ids`
- `wp show <wp_id>`
- `wp show <wp_id> --show-task-ids`
- `wp add <wp_id> <title>`
- `wp update-status <wp_id> <status>`
- `wp update-title <wp_id> <title>`
- `wp delete <wp_id>`
- `task set-work-package <task_ref> <wp_id>`
- `task clear-work-package <task_ref>`
- `task list --show-work-package-id`
- `task show <task_ref> --show-work-package-id`
- `task list --work-package-id <wp_id>`
- persisted dangling-link rejection at load time
- delete protection while associated tasks remain present
- conflicting reassignment rejection until the current association is cleared
- idempotent reattach to the same work package

## Test Data / Pre-Setup

Use a controlled temporary test state.
Back up the current state file before execution and restore it after execution.

Recommended pre-run backup pattern:

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force
```

Initialize the test state:

```powershell
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp add WP-002 "Blister line upgrade"
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task add "Execute FAT" --task-key "execute-fat"
```

## Acceptance Checks

### UAT-M5-01 — Base Work Package list surface

Command:

```powershell
python -m asbp wp list
```

Acceptance:

- command succeeds
- `Work Packages:` header is shown
- `WP-001` and `WP-002` are listed in persisted order
- output remains in the established readable list format

### UAT-M5-02 — Base Work Package show surface

Command:

```powershell
python -m asbp wp show WP-001
```

Acceptance:

- command succeeds
- JSON output contains `wp_id`, `title`, and `status`
- no extra inverse task field is shown unless explicitly requested

### UAT-M5-03 — Work Package update surfaces

Commands:

```powershell
python -m asbp wp update-status WP-002 in_progress
python -m asbp wp update-title WP-002 "Blister line modernization"
python -m asbp wp show WP-002
```

Acceptance:

- both update commands succeed
- `wp show` confirms the updated status and title
- no unrelated work package is changed

### UAT-M5-04 — Task-to-work-package association write surface

Command:

```powershell
python -m asbp task set-work-package prepare-fat WP-001
```

Acceptance:

- command succeeds
- output confirms `TASK-001 -> WP-001`
- persisted state now carries `work_package_id` for the target task

### UAT-M5-05 — Task list association visibility

Command:

```powershell
python -m asbp task list --show-work-package-id
```

Acceptance:

- command succeeds
- associated task shows `work_package_id=WP-001`
- unassociated task shows `work_package_id=<none>`
- default task list contract remains unchanged when the flag is absent

### UAT-M5-06 — Task show association visibility

Command:

```powershell
python -m asbp task show prepare-fat --show-work-package-id
```

Acceptance:

- command succeeds
- JSON includes `work_package_id: "WP-001"`
- default task show contract remains unchanged when the flag is absent

### UAT-M5-07 — Forward exact-match association filter

Command:

```powershell
python -m asbp task list --work-package-id WP-001
```

Acceptance:

- command succeeds
- only tasks associated with `WP-001` are listed
- behavior remains unchanged when the filter is absent

### UAT-M5-08 — Inverse Work Package show visibility

Command:

```powershell
python -m asbp wp show WP-001 --show-task-ids
```

Acceptance:

- command succeeds
- JSON includes `task_ids`
- associated task IDs are correct and complete
- default `wp show` contract remains unchanged when the flag is absent

### UAT-M5-09 — Inverse Work Package list filter

Command:

```powershell
python -m asbp wp list --task-id TASK-001
```

Acceptance:

- command succeeds
- only the matching associated work package is listed
- behavior remains unchanged when the filter is absent

### UAT-M5-10 — Inverse Work Package list visibility

Command:

```powershell
python -m asbp wp list --show-task-ids
```

Acceptance:

- command succeeds
- matching `task_ids=[...]` bundle is displayed per row
- default `wp list` contract remains unchanged when the flag is absent

### UAT-M5-11 — Clear association and persistence cleanup

Commands:

```powershell
python -m asbp task clear-work-package prepare-fat
python -m asbp wp show WP-001 --show-task-ids
python -m asbp task show prepare-fat --show-work-package-id
```

Acceptance:

- clear command succeeds
- `wp show --show-task-ids` no longer lists `TASK-001`
- `task show --show-work-package-id` returns `null`
- persisted save omits `work_package_id` again when the association is removed

### UAT-M5-12 — Delete protection while tasks remain associated

Commands:

```powershell
python -m asbp task set-work-package execute-fat WP-001
python -m asbp wp delete WP-001
```

Acceptance:

- delete command is rejected deterministically
- message clearly states that the Work Package cannot be deleted while tasks are associated
- no state mutation occurs to the targeted Work Package

### UAT-M5-13 — Conflicting reassignment rejection

Commands:

```powershell
python -m asbp wp add WP-003 "Granulation refresh"
python -m asbp task set-work-package execute-fat WP-003
```

Acceptance:

- reassignment is rejected deterministically while `execute-fat` is still attached to `WP-001`
- message clearly identifies the existing current Work Package association
- no state mutation occurs to the task association

### UAT-M5-14 — Idempotent reattach to same Work Package

Command:

```powershell
python -m asbp task set-work-package execute-fat WP-001
```

Acceptance:

- command succeeds
- same-target reattach remains allowed
- association remains unchanged and valid

### UAT-M5-15 — Allowed Work Package deletion after clearing association

Commands:

```powershell
python -m asbp task clear-work-package execute-fat
python -m asbp wp delete WP-001
python -m asbp wp list
```

Acceptance:

- clear command succeeds
- delete command succeeds after the final association is removed
- `WP-001` no longer appears in the Work Package list
- unrelated Work Packages remain intact

### UAT-M5-16 — Persisted dangling-link rejection at load time

Preparation:

- manually edit the state file so a task contains `work_package_id` pointing to a non-existent Work Package ID

Execution command:

```powershell
python -m asbp task list --show-work-package-id
```

Acceptance:

- state load is rejected deterministically
- output clearly reports state validation failure
- output clearly reports that the persisted `work_package_id` does not exist

## General Acceptance Decision Rule

Recommended milestone decision logic:

- `PASS` if all protocol checks pass with no material deviation
- `CONDITIONAL PASS` if core milestone acceptance is achieved with only minor documented deviations that do not invalidate the Milestone 5 boundary
- `FAIL` if one or more core milestone acceptance checks fail

## Post-Execution Restore

Recommended restore command after UAT execution:

```powershell
Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force
```

## Execution Notes

- Record any deviations under the final UAT summary/report
- Record the final decision in the Milestone 5 UAT summary/report
- Do not advance milestone state until UAT execution is completed and recorded
