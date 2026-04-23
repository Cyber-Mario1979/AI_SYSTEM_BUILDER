# M9_UAT_PROTOCOL

## Milestone

Milestone 9 — Hybrid Runtime

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 9 boundary.

It is intended to confirm that the current Milestone 9 runtime behaves correctly for:

- runtime boundary definition over repo-real deterministic state
- prompt contract construction over the runtime boundary
- deterministic-to-LLM handoff structure with separated structured facts and prose instructions
- validation-loop behavior for candidate output acceptance and rejection
- retry / fail decision behavior over accepted and rejected candidate outputs
- controlled generation request payload construction
- preserved runtime contract behavior after the M9.7 consolidation refactor
- preserved adapter/core boundaries at the repo-real M9 implementation surface

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M9_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `469 passed in 44.92s`

## Operator Fields

- UAT date: `()`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 9 UAT should be executed against the repo-real Milestone 9 boundary.

That means:

- CLI-first execution for the public runtime surfaces
- controlled inline Python execution only where the repo-real M9 boundary still relies on model/state-store setup for committed planning state
- candidate-response validation through the repo-real file-based runtime CLI
- no live LLM call, no free-form agentic expansion, and no out-of-scope redesign during UAT execution

This is aligned with the current implementation boundary.

## Scope Covered

The following Milestone 9 surfaces are in scope:

- runtime boundary payload generation
- prompt contract payload generation
- runtime handoff payload generation
- controlled generation request payload generation
- candidate-response validation acceptance and rejection
- retry / fail decision behavior
- repo-real runtime state behavior for blocked and execution-ready work packages
- post-consolidation contract preservation after M9.7

## Test Data / Pre-Setup

Use a controlled temporary test state.

Back up the current state file before execution and restore it after execution.

If `candidate_response.json` already exists under `data/state/`, back it up and restore it after execution.

## Command Execution Sequence

### Step 1 — Create backup folder and back up the current state file and candidate file if they exist

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

if (Test-Path '.\data\state\state.json') {
    Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.original.bak') -Force
}

if (Test-Path '.\data\state\candidate_response.json') {
    Copy-Item '.\data\state\candidate_response.json' (Join-Path $backupDir 'candidate_response.original.bak') -Force
}
```

**Expected output / pass signal**

- no PowerShell error is raised
- backup folder exists
- if the files existed before UAT, backup copies now exist in the backup folder

---

### Step 2 — Initialize a clean controlled UAT state

```powershell
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp state show
```

**Expected output / pass signal**

- `state init` completes successfully
- `state set-status in_flight` confirms the status update
- `state show` returns valid JSON including `status: in_flight`

---

### Step 3 — Create the blocked Work Package baseline

```powershell
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp state show
```

**Expected output / pass signal**

- `wp add` confirms `WP-001` was added
- current state remains valid
- `WP-001` exists with no selector context, no committed collection, and no plan

---

### Step 4 — Execute the runtime boundary blocked-state check

```powershell
python -m asbp runtime wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `runtime_boundary_state = deterministic_blocked`
- `eligible_for_prompt_contract = false`
- `deterministic_facts.orchestration_stage = binding_context_required`
- `deterministic_facts.blocking_conditions` includes `selector_context_missing`

---

### Step 5 — Execute the prompt-contract blocked-state check

```powershell
python -m asbp runtime prompt-contract-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `prompt_contract_id = work_package_runtime_prompt_contract_v1`
- `prompt_contract_state = blocked`
- `prompt_contract_mode = blocked_explainer`
- `eligible_for_prompt_contract = false`

---

### Step 6 — Execute the runtime handoff blocked-state check

```powershell
python -m asbp runtime handoff-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `handoff_metadata.handoff_contract_id = work_package_llm_handoff_v1`
- `handoff_metadata.handoff_state = blocked`
- `handoff_metadata.generation_allowed = false`
- `prose_generation_instructions.response_mode = blocked_explainer`

---

### Step 7 — Execute the controlled generation request blocked-state check

```powershell
python -m asbp runtime generate-request-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `generation_surface_metadata.generation_state = blocked`
- `generation_surface_metadata.generation_allowed = false`
- `candidate_response_template.response_mode = blocked_explainer`

---

### Step 8 — Create a valid blocked candidate response file

```powershell
$blockedCandidate = @'
{
  "response_mode": "blocked_explainer",
  "operator_message": "Selector context is still required before generation can proceed.",
  "recommended_next_actions": [
    "Complete deterministic selector context before orchestration can proceed."
  ],
  "grounded_input_fields_used": [
    "wp_id",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.next_actions"
  ]
}
'@
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText('.\data\state\candidate_response.json', $blockedCandidate, $utf8NoBom)
```

**Expected output / pass signal**

- no PowerShell error
- `data/state/candidate_response.json` exists
- file content is valid JSON

---

### Step 9 — Execute the candidate-response acceptance check for the blocked state

```powershell
python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.json
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = accepted`
- `candidate_response_mode = blocked_explainer`
- `errors = []`

---

### Step 10 — Execute the accepted decision-path check for the blocked state

```powershell
python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.json 1 2
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = accepted`
- `decision_state = accepted`
- `fallback_action = use_validated_output`
- `retry_policy.retries_remaining = 1`

---

### Step 11 — Create an invalid candidate response file to test deterministic rejection

```powershell
$invalidCandidate = @'
{
  "response_mode": "execution_ready_summary",
  "operator_message": "",
  "recommended_next_actions": "not-a-list",
  "grounded_input_fields_used": [
    "wp_id",
    "disallowed.field"
  ],
  "extra_field": "unexpected"
}
'@
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText('.\data\state\candidate_response.invalid.json', $invalidCandidate, $utf8NoBom)
```

**Expected output / pass signal**

- no PowerShell error
- `data/state/candidate_response.invalid.json` exists
- file content is valid JSON

---

### Step 12 — Execute the candidate-response rejection check

```powershell
python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.invalid.json
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = rejected`
- `validated_output = null`
- `errors` include:
  - unexpected extra field rejection
  - response-mode mismatch
  - empty operator-message rejection
  - list-type rejection for `recommended_next_actions`
  - disallowed grounded-field rejection

---

### Step 13 — Execute the retry-allowed decision-path check

```powershell
python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.invalid.json 1 2
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = rejected`
- `decision_state = retry_allowed`
- `fallback_action = request_new_candidate_from_same_handoff_contract`
- `retry_policy.retries_remaining = 1`

---

### Step 14 — Execute the fail-closed exhausted-retry check

```powershell
python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.invalid.json 2 2
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = rejected`
- `decision_state = fail_closed`
- `fallback_action = return_deterministic_rejection_without_acceptance`
- `retry_policy.retries_remaining = 0`

---

### Step 15 — Enrich the state into an execution-ready Work Package baseline

```powershell
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp task add "Prepare FAT" --duration 1 --task-key prepare-fat
python -m asbp task set-work-package TASK-001 WP-001
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection add-task TC-001 TASK-001
python -m asbp collection set-work-package TC-001 WP-001
```

**Expected output / pass signal**

- selector-context mutations succeed
- `TASK-001` is created and associated to `WP-001`
- `TC-001` is created, gets `TASK-001`, and is bound to `WP-001`

---

### Step 16 — Inject a committed plan through approved state-model/state-store usage

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
    )
]

save_validated_state_to_path(state, state_path)
print("Injected PLAN-001 into controlled UAT state.")
'@ | python -
```

**Expected output / pass signal**

- command prints:

```text
Injected PLAN-001 into controlled UAT state.
```

- no traceback is raised
- subsequent runtime behavior reflects committed `PLAN-001` on `WP-001`

---

### Step 17 — Execute the runtime boundary execution-ready check

```powershell
python -m asbp runtime wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `runtime_boundary_state = eligible_for_prompt_contract`
- `eligible_for_prompt_contract = true`
- `selected_plan_id = PLAN-001`
- `deterministic_facts.orchestration_stage = execution_ready`

---

### Step 18 — Execute the prompt-contract execution-ready check

```powershell
python -m asbp runtime prompt-contract-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `prompt_contract_state = ready`
- `prompt_contract_mode = execution_ready_summary`
- `eligible_for_prompt_contract = true`

---

### Step 19 — Execute the runtime handoff execution-ready check

```powershell
python -m asbp runtime handoff-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `handoff_metadata.handoff_state = ready_for_generation`
- `handoff_metadata.generation_allowed = true`
- `handoff_metadata.selected_plan_id = PLAN-001`
- `prose_generation_instructions.response_mode = execution_ready_summary`

---

### Step 20 — Execute the controlled generation request execution-ready check

```powershell
python -m asbp runtime generate-request-wp WP-001
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `generation_surface_metadata.generation_state = ready`
- `generation_surface_metadata.generation_allowed = true`
- `generation_surface_metadata.selected_plan_id = PLAN-001`
- `candidate_response_template.response_mode = execution_ready_summary`

---

### Step 21 — Create a valid execution-ready candidate response file

```powershell
$readyCandidate = @'
{
  "response_mode": "execution_ready_summary",
  "operator_message": "The work package is ready for generation using the selected committed plan.",
  "recommended_next_actions": [
    "Execution-ready deterministic state reached."
  ],
  "grounded_input_fields_used": [
    "wp_id",
    "selected_plan_id",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.plan_ids"
  ]
}
'@
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText('.\data\state\candidate_response.ready.json', $readyCandidate, $utf8NoBom)
```

**Expected output / pass signal**

- no PowerShell error
- `data/state/candidate_response.ready.json` exists
- file content is valid JSON

---

### Step 22 — Execute the candidate-response acceptance check for the execution-ready state

```powershell
python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.ready.json
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = accepted`
- `candidate_response_mode = execution_ready_summary`
- `errors = []`

---

### Step 23 — Execute the invalid retry-control fail-closed check

```powershell
python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.ready.json 3 2
```

**Expected output / pass signal**

JSON output must show:

- `wp_id = WP-001`
- `validation_state = accepted`
- `decision_state = fail_closed`
- `fallback_action = return_deterministic_rejection_without_acceptance`
- `decision_rationale` includes `invalid_retry_control_state:attempt_number_exceeds_max_attempts`

---

### Step 24 — Execute the missing Work Package runtime-surface rejection checks

```powershell
python -m asbp runtime wp WP-404
python -m asbp runtime prompt-contract-wp WP-404
python -m asbp runtime handoff-wp WP-404
python -m asbp runtime generate-request-wp WP-404
python -m asbp runtime validate-response-wp WP-404 .\data\state\candidate_response.ready.json
python -m asbp runtime decide-response-wp WP-404 .\data\state\candidate_response.ready.json 1 2
```

**Expected output / pass signal**

Each command must return the deterministic message:

```text
Work Package not found: WP-404
```

No traceback or malformed JSON should appear.

---

### Step 25 — Re-run the full validation baseline after UAT execution

```powershell
python -m pytest -q
```

**Expected output / pass signal**

The suite must be green.

Expected acceptance signal:

```text
469 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

---

### Step 26 — Restore the original pre-UAT state file and candidate files

```powershell
if (Test-Path (Join-Path $backupDir 'state.json.original.bak')) {
    Copy-Item (Join-Path $backupDir 'state.json.original.bak') '.\data\state\state.json' -Force
} else {
    Remove-Item '.\data\state\state.json' -ErrorAction SilentlyContinue
}

if (Test-Path (Join-Path $backupDir 'candidate_response.original.bak')) {
    Copy-Item (Join-Path $backupDir 'candidate_response.original.bak') '.\data\state\candidate_response.json' -Force
} else {
    Remove-Item '.\data\state\candidate_response.json' -ErrorAction SilentlyContinue
}

Remove-Item '.\data\state\candidate_response.invalid.json' -ErrorAction SilentlyContinue
Remove-Item '.\data\state\candidate_response.ready.json' -ErrorAction SilentlyContinue
```

**Expected output / pass signal**

- restore command completes without PowerShell error
- repo state file is back to its pre-UAT condition
- original candidate file is restored if it existed before UAT
- temporary UAT candidate files are removed

## Protocol Checks

| Check ID  | Check                                                                                                                                | Acceptance Criteria                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| UAT-M9-01 | Runtime boundary surface reports deterministic blocked state for an incomplete Work Package                                          | Step 4 returns `deterministic_blocked` with `selector_context_missing`              |
| UAT-M9-02 | Prompt contract surface reports blocked contract mode for a blocked runtime boundary                                                 | Step 5 returns blocked prompt-contract payload                                      |
| UAT-M9-03 | Runtime handoff surface separates handoff metadata, structured facts, and prose instructions deterministically                       | Step 6 returns blocked handoff payload with the expected separated sections         |
| UAT-M9-04 | Controlled generation request surface returns blocked generation metadata and candidate template deterministically                   | Step 7 returns blocked generation payload                                           |
| UAT-M9-05 | Output validation accepts a valid blocked-state candidate response                                                                   | Step 9 returns `validation_state = accepted`                                        |
| UAT-M9-06 | Retry / decision surface accepts a valid blocked-state candidate response deterministically                                          | Step 10 returns `decision_state = accepted`                                         |
| UAT-M9-07 | Output validation rejects a contract-breaking candidate response deterministically                                                   | Step 12 returns `validation_state = rejected` with the expected rejection reasons   |
| UAT-M9-08 | Retry / decision surface allows retry while budget remains after validation rejection                                                | Step 13 returns `decision_state = retry_allowed`                                    |
| UAT-M9-09 | Retry / decision surface fails closed when retry budget is exhausted                                                                 | Step 14 returns `decision_state = fail_closed`                                      |
| UAT-M9-10 | Runtime surfaces become execution-ready when selector context, committed collection, committed task, and committed plan are coherent | Steps 17 through 20 all return execution-ready / ready-for-generation states        |
| UAT-M9-11 | Output validation accepts a valid execution-ready candidate response deterministically                                               | Step 22 returns `validation_state = accepted`                                       |
| UAT-M9-12 | Retry / decision surface fails closed on invalid retry-control state even when candidate output is otherwise valid                   | Step 23 returns `decision_state = fail_closed` with invalid-retry-control rationale |
| UAT-M9-13 | All runtime CLI surfaces reject missing Work Package references deterministically                                                    | Step 24 returns `Work Package not found: WP-404` across all runtime CLI surfaces    |
| UAT-M9-14 | Full validation baseline remains green after UAT execution                                                                           | Step 25 returns a green `pytest` result                                             |
| UAT-M9-15 | Original pre-UAT state and candidate-file condition is restored successfully                                                         | Step 26 completes and restores the original condition                               |

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

Milestone 9 UAT may be accepted only if:

- all defined checks pass
- no in-scope deterministic runtime contract is contradicted during execution
- no hidden runtime-boundary ambiguity is observed
- candidate acceptance, rejection, and fail-closed paths remain deterministic
- the repo remains aligned with the approved Milestone 9 boundary through M9.7

## Out of Scope

The following items are not part of M9 UAT acceptance execution:

- Milestone 9 closeout
- Milestone 10 output-family expansion
- live LLM generation
- external model invocation
- free-form agentic behavior
- post-roadmap redesign
