# M8_UAT_PROTOCOL

## Milestone

Milestone 8 — Multi-Entity Coordination

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 8 boundary.

It is intended to confirm that the current Milestone 8 runtime behaves correctly for:

- source-of-work contract preservation between authoritative source definitions and instantiated task records
- normalized Work Package ↔ collection relationships
- normalized task ↔ collection relationships
- binding-context consistency controls for planning-bound behavior
- deterministic cross-entity read surfaces
- deterministic cross-entity update rules
- fail-closed cross-entity validation and destructive-mutation rejection
- minimal deterministic orchestration without LLM dependency
- preserved adapter/core boundaries at the repo-real M8 implementation surface

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M8_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `436 passed in 42.29s`

## Operator Fields

- UAT date: `()`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 8 UAT should be executed against the repo-real Milestone 8 boundary.

That means:

- CLI-first execution for public Work Package, collection, task, and orchestration surfaces
- controlled inline Python execution only where the repo-real M8 behavior lives in core/state validation rather than a public CLI command
- no LLM behavior, no free-form agentic expansion, and no out-of-scope redesign during UAT execution

This is aligned with the current implementation boundary.

## Scope Covered

The following Milestone 8 surfaces are in scope:

- source-of-work contract validation for instantiated task records
- Work Package ↔ collection relationship visibility and normalization
- task ↔ collection relationship visibility and normalization
- binding-context consistency behavior that gates planning-bound orchestration
- cross-entity read visibility for tasks, collections, and Work Packages
- cross-entity update behavior for collection ↔ Work Package mutation
- cross-entity failure behavior for invalid deletes and invalid work-package clearing
- deterministic orchestration stage reporting through `python -m asbp orchestrate wp <WP-ID>`
- persisted reload rejection for invalid cross-entity state

## Test Data / Pre-Setup

Use a controlled temporary test state.

Back up the current state file before execution and restore it after execution.

## Command Execution Sequence

### Step 1 — Create backup folder and back up the current state file

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
if (Test-Path '.\data\state\state.json') {
    Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.original.bak') -Force
}
```

**Expected output / pass signal**

- no PowerShell error is raised
- backup folder exists
- if a state file existed before UAT, `state.json.original.bak` now exists in the backup folder

---

### Step 2 — Run a model-level source-of-work acceptance check without touching the repo state file

```powershell
@'
from asbp.state_model import TaskModel

manual_task = TaskModel(
    task_id="TASK-MANUAL-001",
    order=1,
    title="Manual task",
    status="planned",
)

preset_resolved_task = TaskModel(
    task_id="TASK-PRESET-001",
    order=2,
    title="Preset resolved task",
    work_package_id="WP-001",
    instantiation_mode="preset_resolved",
    source_definition_kind="task_pool",
    source_definition_id="POOL-TABPRESS-001",
    status="planned",
)

print("manual_ok", manual_task.instantiation_mode)
print(
    "preset_ok",
    preset_resolved_task.instantiation_mode,
    preset_resolved_task.source_definition_kind,
    preset_resolved_task.source_definition_id,
)
'@ | python -
```

**Expected output / pass signal**

The command should print both lines below with no traceback:

```text
manual_ok manual
preset_ok preset_resolved task_pool POOL-TABPRESS-001
```

---

### Step 3 — Confirm invalid preset-resolved source contract is rejected deterministically

```powershell
@'
from asbp.state_model import TaskModel

try:
    TaskModel(
        task_id="TASK-BAD-001",
        order=1,
        title="Invalid preset task",
        work_package_id="WP-001",
        instantiation_mode="preset_resolved",
        status="planned",
    )
except Exception as exc:
    print(type(exc).__name__)
    print(exc)
'@ | python -
```

**Expected output / pass signal**

- command prints an exception type
- output includes a deterministic rejection message related to missing source contract fields
- acceptable signal includes text such as:

```text
ValidationError
Preset-resolved task must declare source_definition_kind=task_pool
```

or

```text
Preset-resolved task must declare source_definition_id
```

The important point is: the invalid task is rejected deterministically, not accepted silently.

---

### Step 4 — Initialize a clean controlled UAT state

```powershell
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp state show
```

**Expected output / pass signal**

- `state init` reports the state file path
- `state set-status in_flight` confirms the status update
- `state show` returns valid JSON including project and `status: in_flight`

---

### Step 5 — Create the Work Package test set

```powershell
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp add WP-002 "Autoclave qualification"
python -m asbp wp add WP-003 "Line clearance package"
python -m asbp wp add WP-004 "Plan-only package"
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp show WP-001 --show-selector-context
```

**Expected output / pass signal**

- each `wp add` confirms the Work Package was added
- each selector-context mutation confirms the update
- final `wp show` for `WP-001` prints JSON containing:
  - `preset_id = oral-solid-dose-standard`
  - `scope_intent = qualification-only`
  - `standards_bundles = ["cqv-core", "automation"]`

---

### Step 6 — Create the task set and associate the tasks to Work Packages

```powershell
python -m asbp task add "Prepare FAT" --duration 1 --task-key prepare-fat
python -m asbp task add "Execute FAT" --duration 1 --task-key execute-fat
python -m asbp task add "Autoclave FAT" --duration 1 --task-key autoclave-fat
python -m asbp task set-work-package TASK-001 WP-001
python -m asbp task set-work-package TASK-002 WP-001
python -m asbp task set-work-package TASK-003 WP-002
python -m asbp task list --show-task-key --show-work-package-id
```

**Expected output / pass signal**

- each `task add` confirms a task was added
- task IDs should be sequential, typically `TASK-001`, `TASK-002`, `TASK-003`
- each `set-work-package` confirms the association
- final `task list` should show:
  - `TASK-001` with `task_key=prepare-fat` and `work_package_id=WP-001`
  - `TASK-002` with `task_key=execute-fat` and `work_package_id=WP-001`
  - `TASK-003` with `task_key=autoclave-fat` and `work_package_id=WP-002`

---

### Step 7 — Create the committed collection set and valid Work Package binding

```powershell
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection add-task TC-001 TASK-001
python -m asbp collection add-task TC-001 TASK-002
python -m asbp collection set-work-package TC-001 WP-001
python -m asbp collection show TC-001 --show-work-package-id
```

**Expected output / pass signal**

- collection add confirms `TC-001`
- both task-add operations succeed
- `set-work-package` succeeds
- final `collection show` includes:
  - `collection_id = TC-001`
  - `collection_state = committed`
  - `work_package_id = WP-001`
  - task membership for `TASK-001` and `TASK-002`

---

### Step 8 — Execute the cross-entity read-surface checks

```powershell
python -m asbp wp show WP-001 --show-task-ids --show-collection-ids --show-selector-context
python -m asbp wp list --show-task-ids --show-collection-ids
python -m asbp collection show TC-001 --show-work-package-id
python -m asbp collection list --show-work-package-id --show-task-ids
python -m asbp task show TASK-001 --show-work-package-id --show-collection-ids
python -m asbp task list --show-task-key --show-work-package-id --show-collection-ids
```

**Expected output / pass signal**

Cross-entity visibility must be consistent across all read surfaces:

- `wp show WP-001` includes `TASK-001`, `TASK-002`, and `TC-001`
- `collection show TC-001` includes `work_package_id = WP-001`
- `task show TASK-001` includes `work_package_id = WP-001`
- `task show TASK-001` includes `collection_ids` with `TC-001`

Any mismatch here is a UAT failure.

---

### Step 9 — Execute the valid collection ↔ Work Package update acceptance check

```powershell
python -m asbp collection clear-work-package TC-001
python -m asbp collection set-work-package TC-001 WP-001
python -m asbp collection show TC-001 --show-work-package-id
```

**Expected output / pass signal**

- clear command succeeds
- re-bind command succeeds
- final `collection show` again reports `work_package_id = WP-001`
- no task membership corruption appears

---

### Step 10 — Execute the invalid collection ↔ Work Package bind rejection check

```powershell
python -m asbp collection add "Conflicting Selection" --collection-state committed
python -m asbp collection add-task TC-002 TASK-003
python -m asbp collection set-work-package TC-002 WP-001
```

**Expected output / pass signal**

The final command must fail deterministically.

Expected rejection meaning:

```text
Collection work package cannot be bound because member task has a different work package
```

and it should reference the mismatch between `TASK-003`, `WP-002`, and `WP-001`.

---

### Step 11 — Execute the invalid task-delete rejection check while collection membership still exists

```powershell
python -m asbp task delete TASK-001
```

**Expected output / pass signal**

The command must fail deterministically with a message equivalent to:

```text
Task cannot be deleted while still associated with collections: TASK-001 -> [TC-001]
```

If the task is actually deleted, UAT fails.

---

### Step 12 — Execute the invalid Work Package delete rejection check for bound collections with no tasks

```powershell
python -m asbp collection add "Empty Bound Selection" --collection-state committed
python -m asbp collection set-work-package TC-003 WP-003
python -m asbp wp delete WP-003
```

**Expected output / pass signal**

The final command must fail deterministically with a message equivalent to:

```text
Work Package cannot be deleted while collections are bound: WP-003 -> [TC-003]
```

This check is specifically for the collection-bound case without task interference.

---

### Step 13 — Snapshot the working UAT state before plan-injection checks

```powershell
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.uat-working.bak') -Force
```

**Expected output / pass signal**

- no PowerShell error
- `state.uat-working.bak` exists in the backup folder

---

### Step 14 — Inject repo-real draft and committed plan state through approved state-model/state-store usage

```powershell
@'
from datetime import datetime, timezone

from asbp.state_model import (
    GeneratedTaskPlanModel,
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
)
from asbp.state_store import get_state_file_path, load_validated_state, save_validated_state_to_path

state_path = get_state_file_path()
state = load_validated_state(state_path)

state.plans = [
    PlanningModel(
        plan_id="PLAN-001",
        work_package_id="WP-001",
        plan_state="committed",
        planning_basis=PlanningBasisModel(
            duration_source="task_duration",
        ),
        planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
        planning_calendar=PlanningCalendarModel(
            working_days=["monday", "wednesday", "friday"],
            workday_hours=8,
            workmonth_mode="calendar_month",
        ),
        generated_task_plans=[
            GeneratedTaskPlanModel(
                task_id="TASK-001",
                sequence_order=1,
                duration_days=1,
                dependency_task_ids=[],
                planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
                planned_finish_at=datetime(2026, 4, 13, 16, 30, tzinfo=timezone.utc),
            )
        ],
    ),
    PlanningModel(
        plan_id="PLAN-002",
        work_package_id="WP-004",
        plan_state="draft",
    ),
]

save_validated_state_to_path(state, state_path)
print("Injected PLAN-001 and PLAN-002 into controlled UAT state.")
'@ | python -
```

**Expected output / pass signal**

- command prints:

```text
Injected PLAN-001 and PLAN-002 into controlled UAT state.
```

- no traceback is raised
- subsequent behavior now reflects:
  - committed `PLAN-001` on `WP-001`
  - draft `PLAN-002` on `WP-004`

---

### Step 15 — Execute the invalid Work Package delete rejection check for plan-only linkage

```powershell
python -m asbp wp delete WP-004
```

**Expected output / pass signal**

The command must fail deterministically with a message equivalent to:

```text
Work Package cannot be deleted while plans are associated: WP-004 -> [PLAN-002]
```

---

### Step 16 — Execute the incomplete orchestration-state check

```powershell
python -m asbp orchestrate wp WP-004
```

**Expected output / pass signal**

JSON output must show an incomplete planning-ready state.

Minimum acceptance signal:

- `wp_id = WP-004`
- `orchestration_stage = planning_setup_required`
- `selected_plan_id = PLAN-002`

and `blocking_conditions` must include the missing planning setup fields.

---

### Step 17 — Execute the execution-ready orchestration-state check

```powershell
python -m asbp orchestrate wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `orchestration_stage = execution_ready`
- `selected_plan_id = PLAN-001`

and `next_actions` must indicate that execution-ready deterministic state was reached.

---

### Step 18 — Remove collection membership for TASK-001 so the plan-reference clear-work-package rejection can be observed directly

```powershell
python -m asbp collection remove-task TC-001 TASK-001
python -m asbp task clear-work-package TASK-001
```

**Expected output / pass signal**

- first command succeeds
- second command must fail deterministically because the plan still references the task

Expected rejection meaning:

```text
Task work package cannot be cleared while plans still reference it
```

and it should reference `TASK-001` and `PLAN-001`.

---

### Step 19 — Execute the intentionally invalid persisted-state reload check

```powershell
@'
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.1.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification",
      "status": "open"
    }
  ],
  "task_collections": [],
  "plans": [
    {
      "plan_id": "PLAN-900",
      "work_package_id": "WP-999",
      "plan_state": "draft"
    }
  ]
}
'@ | Set-Content -Encoding utf8 '.\data\state\state.json'

python -m asbp state show
```

**Expected output / pass signal**

The final command must fail deterministically during validated state load.

Expected rejection meaning:

```text
Persisted plan work_package_id does not exist: PLAN-900 -> WP-999
```

Any successful `state show` here is a UAT failure.

---

### Step 20 — Restore the working controlled UAT state after the invalid persisted-state check

```powershell
Copy-Item (Join-Path $backupDir 'state.uat-working.bak') '.\data\state\state.json' -Force
python -m asbp state show
```

**Expected output / pass signal**

- restore copy succeeds
- `state show` returns valid JSON again
- restored state contains the controlled UAT entities rather than the invalid `PLAN-900` payload

---

### Step 21 — Re-run the full validation baseline after UAT execution

```powershell
python -m pytest -q
```

**Expected output / pass signal**

The suite must be green.

Expected acceptance signal:

```text
436 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

---

### Step 22 — Restore the original pre-UAT state file

```powershell
if (Test-Path (Join-Path $backupDir 'state.json.original.bak')) {
    Copy-Item (Join-Path $backupDir 'state.json.original.bak') '.\data\state\state.json' -Force
} else {
    Remove-Item '.\data\state\state.json' -ErrorAction SilentlyContinue
}
```

**Expected output / pass signal**

- restore command completes without PowerShell error
- repo state file is back to its pre-UAT condition
- if no original state existed, the temporary UAT state file is removed

## Protocol Checks

| Check ID  | Check                                                                                                    | Acceptance Criteria                                                                    |
| --------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| UAT-M8-01 | Model-level source-of-work contract accepts valid manual and valid preset-resolved task definitions      | Step 2 prints both success lines and no traceback                                      |
| UAT-M8-02 | Invalid preset-resolved source contract is rejected deterministically                                    | Step 3 prints a validation rejection tied to missing preset source fields              |
| UAT-M8-03 | Controlled M8 test state initializes successfully                                                        | Steps 4 through 7 complete cleanly and produce the expected seeded entities            |
| UAT-M8-04 | Work Package, collection, and task read/list surfaces show cross-entity visibility deterministically     | Step 8 shows consistent WP / collection / task linkage across all read surfaces        |
| UAT-M8-05 | Collection ↔ Work Package update surface accepts a valid explicit bind and preserves state consistency   | Step 9 succeeds and `TC-001` ends bound again to `WP-001`                              |
| UAT-M8-06 | Invalid collection ↔ Work Package bind is rejected deterministically when member-task scope conflicts    | Step 10 rejects the invalid bind with a mismatch message                               |
| UAT-M8-07 | Invalid task delete is rejected deterministically when collection membership still exists                | Step 11 rejects deletion of `TASK-001` because of `TC-001` membership                  |
| UAT-M8-08 | Invalid Work Package delete is rejected deterministically when bound collections still reference it      | Step 12 rejects deletion of `WP-003` because `TC-003` is still bound                   |
| UAT-M8-09 | Invalid Work Package delete is rejected deterministically when plans still reference it                  | Step 15 rejects deletion of `WP-004` because `PLAN-002` is associated                  |
| UAT-M8-10 | Orchestration surface reports the correct stage and next action for an incomplete planning-ready state   | Step 16 returns `planning_setup_required` for `WP-004` with missing setup blockers     |
| UAT-M8-11 | Orchestration surface reports `execution_ready` when one committed plan is present and state is coherent | Step 17 returns `execution_ready` and selects `PLAN-001` for `WP-001`                  |
| UAT-M8-12 | Invalid task clear-work-package is rejected deterministically when plan references still exist           | Step 18 rejects the clear because `PLAN-001` still references `TASK-001`               |
| UAT-M8-13 | Persisted reload rejects intentionally invalid cross-entity state deterministically                      | Step 19 rejects the invalid persisted state and does not render a normal state payload |
| UAT-M8-14 | Full validation baseline remains green after UAT execution                                               | Step 21 returns a green `pytest` result                                                |
| UAT-M8-15 | Original pre-UAT state file is restored successfully                                                     | Step 22 completes and restores the original state condition                            |

## Failure Handling Rule

If any step produces a result that does not match the expected output above:

- stop the UAT run at that point
- do not continue guessing
- restore the working or original backup state first
- record the exact step number
- record the exact command that failed
- record the actual output shown
- classify the issue as one of:
  - execution mistake
  - protocol ambiguity
  - runtime/logic defect
  - environment/state contamination

## Acceptance Rule

Milestone 8 UAT may be accepted only if:

- all defined checks pass
- no in-scope deterministic contract is contradicted during execution
- no hidden cross-entity ambiguity is observed
- the repo remains aligned with the M8 addendum gate and closeout reservations remain explicitly preserved for later review

## Out of Scope

The following items are not part of M8 UAT acceptance execution:

- Milestone 8 closeout
- disposition of the reserved addendum items for M8 closeout
- AI runtime behavior
- free-form generation behavior
- Milestone 9 handoff behavior
