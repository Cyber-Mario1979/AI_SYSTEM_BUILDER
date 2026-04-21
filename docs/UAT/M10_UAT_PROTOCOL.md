# M10_UAT_PROTOCOL

## Milestone

Milestone 10 — Runtime-Orchestrated Outputs

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 10 boundary.

It is intended to confirm that the current Milestone 10 runtime-output layer behaves correctly for:

- output target definition over repo-real deterministic state
- output contract construction over the repo-real M10 boundary
- deterministic input-to-output mapping over bounded deterministic inputs
- output acceptance behavior for valid and contract-breaking candidate outputs
- regeneration / retry behavior over accepted, retryable, and fail-closed attempts
- output family expansion behavior for blocked and execution-ready response modes
- output consistency controls over family selection and family-ready output
- output failure handling over retry-needed and fail-closed outcomes
- preserved runtime-output contract behavior after the M10.7 consolidation refactor
- preserved adapter/core boundaries at the repo-real M10 implementation surface

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M10_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `502 passed in 49.25s`

## Operator Fields

- UAT date: `21-04-2026`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 10 UAT should be executed against the repo-real Milestone 10 boundary.

That means:

- use normal CLI/state setup only where it already exists and helps produce a controlled deterministic state
- use controlled inline Python for the M10 output-layer logic surfaces because the repo-real boundary for these slices is logic-first
- do not invent new CLI adapters during UAT
- no live LLM call, no free-form generation, and no out-of-scope redesign during UAT execution
- all output-layer checks must stay inside the approved Milestone 10 boundary through M10.7

This is aligned with the current implementation boundary.

## Scope Covered

The following Milestone 10 surfaces are in scope:

- output target payload generation
- output contract payload generation
- deterministic output mapping payload generation
- output acceptance behavior
- output retry behavior
- output family payload behavior
- output consistency behavior
- output failure behavior
- post-consolidation contract preservation after M10.7

## Test Data / Pre-Setup

Use a controlled temporary in-memory test state through inline Python.

No persisted-state mutation is required for this UAT protocol.

## Command Execution Sequence

### Step 1 — Verify the technical baseline before UAT execution

```powershell
python -m pytest -q
```

**Expected output / pass signal**

- full suite is green
- recorded repo-real baseline matches:

```text
502 passed
```

---

### Step 2 — Execute the missing Work Package rejection checks across the full M10 output chain

```powershell
@'
from asbp.output_acceptance_logic import validate_work_package_output_before_acceptance
from asbp.output_consistency_logic import validate_work_package_output_family_consistency
from asbp.output_contract_logic import build_work_package_output_contract
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.output_family_logic import build_work_package_output_family_payload
from asbp.output_mapping_logic import build_work_package_output_mapping_payload
from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.output_target_logic import build_work_package_output_target_payload

candidate_output = {}

checks = {
    "output_target": build_work_package_output_target_payload([], [], [], [], wp_id="WP-404"),
    "output_contract": build_work_package_output_contract([], [], [], [], wp_id="WP-404"),
    "output_mapping": build_work_package_output_mapping_payload([], [], [], [], wp_id="WP-404"),
    "output_acceptance": validate_work_package_output_before_acceptance([], [], [], [], wp_id="WP-404", candidate_output=candidate_output),
    "output_retry": evaluate_work_package_output_attempt([], [], [], [], wp_id="WP-404", candidate_output=candidate_output, attempt_number=1, max_attempts=2),
    "output_family": build_work_package_output_family_payload([], [], [], [], wp_id="WP-404", candidate_output=candidate_output, attempt_number=1, max_attempts=2),
    "output_consistency": validate_work_package_output_family_consistency([], [], [], [], wp_id="WP-404", candidate_output=candidate_output, attempt_number=1, max_attempts=2),
    "output_failure": build_work_package_output_failure_payload([], [], [], [], wp_id="WP-404", candidate_output=candidate_output, attempt_number=1, max_attempts=2),
}

print(checks)
'@ | python -
```

**Expected output / pass signal**

All returned values must be `None`.

---

### Step 3 — Execute the blocked output-target check

```powershell
@'
from asbp.output_target_logic import build_work_package_output_target_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

payload = build_work_package_output_target_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `wp_id = WP-001`
- `output_target_metadata.output_target_id = work_package_operator_response_target_v1`
- `output_target_metadata.target_state = blocked`
- `output_target_metadata.selected_plan_id = None`
- `output_target_metadata.generation_allowed = False`
- `current_response_mode = blocked_explainer`

---

### Step 4 — Execute the blocked output-contract check

```powershell
@'
from asbp.output_contract_logic import build_work_package_output_contract
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

payload = build_work_package_output_contract(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_contract_metadata.output_contract_id = work_package_operator_response_contract_v1`
- `output_contract_metadata.contract_state = blocked`
- `output_contract_metadata.current_response_mode = blocked_explainer`
- `required_output_fields` contains exactly:
  - `response_mode`
  - `operator_message`
  - `recommended_next_actions`
  - `grounded_input_fields_used`
- `acceptance_shape.extra_fields_allowed = False`

---

### Step 5 — Execute the blocked output-mapping check

```powershell
@'
from asbp.output_mapping_logic import build_work_package_output_mapping_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

payload = build_work_package_output_mapping_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_mapping_metadata.output_mapping_id = work_package_output_mapping_v1`
- `output_mapping_metadata.mapping_state = blocked`
- `output_mapping_metadata.current_response_mode = blocked_explainer`
- `deterministic_input.structured_facts.orchestration_stage = binding_context_required`
- `mapped_output_payload.response_mode = blocked_explainer`

---

### Step 6 — Execute the blocked acceptance check for a valid blocked-state candidate

```powershell
@'
from asbp.output_acceptance_logic import validate_work_package_output_before_acceptance
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = validate_work_package_output_before_acceptance(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_acceptance_metadata.validation_state = accepted`
- `output_acceptance_metadata.acceptance_ready = True`
- `output_acceptance_metadata.current_response_mode = blocked_explainer`
- `errors = []`

---

### Step 7 — Execute the blocked retry acceptance path

```powershell
@'
from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = evaluate_work_package_output_attempt(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_retry_metadata.decision_state = accepted`
- `output_retry_metadata.regeneration_action = use_validated_output`
- `retry_policy.retries_remaining = 1`
- `decision_rationale = ['validated_output_accepted']`

---

### Step 8 — Execute the blocked output-family check

```powershell
@'
from asbp.output_family_logic import build_work_package_output_family_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = build_work_package_output_family_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_family_metadata.family_state = available`
- `output_family_metadata.current_response_mode = blocked_explainer`
- `output_family_metadata.selected_family_id = single_work_package_operator_response`
- `available_output_families` includes:
  - `single_work_package_operator_response`
  - `single_work_package_operator_response_brief`

---

### Step 9 — Execute the blocked output-consistency check

```powershell
@'
from asbp.output_consistency_logic import validate_work_package_output_family_consistency
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = validate_work_package_output_family_consistency(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_consistency_metadata.consistency_state = accepted`
- `output_consistency_metadata.current_response_mode = blocked_explainer`
- `output_consistency_metadata.resolved_family_id = single_work_package_operator_response`
- `consistency_errors = []`

---

### Step 10 — Execute the blocked output-failure accepted path

```powershell
@'
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = build_work_package_output_failure_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_failure_metadata.failure_state = accepted`
- `output_failure_metadata.failure_action = use_consistent_output`
- `output_failure_metadata.failure_reason_category = None`
- `failure_feedback = None`

---

### Step 11 — Execute the contract-breaking rejection path

```powershell
@'
from asbp.output_acceptance_logic import validate_work_package_output_before_acceptance
from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.output_family_logic import build_work_package_output_family_payload
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "execution_ready_summary",
    "operator_message": "",
    "recommended_next_actions": "not-a-list",
    "grounded_input_fields_used": [
        "wp_id",
        "disallowed.field",
    ],
    "extra_field": "unexpected",
}

acceptance_payload = validate_work_package_output_before_acceptance(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
)

retry_payload = evaluate_work_package_output_attempt(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

family_payload = build_work_package_output_family_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

failure_payload = build_work_package_output_failure_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
)

print("ACCEPTANCE:", acceptance_payload)
print("RETRY:", retry_payload)
print("FAMILY:", family_payload)
print("FAILURE:", failure_payload)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- acceptance rejected deterministically
- acceptance errors include:
  - unexpected extra field rejection
  - response-mode mismatch
  - empty operator-message rejection
  - list-type rejection for `recommended_next_actions`
  - disallowed grounded-field rejection
- retry returns:
  - `decision_state = retry_allowed`
  - `regeneration_action = request_regenerated_output_from_same_mapping_contract`
- family returns:
  - `family_state = blocked`
  - `decision_state = retry_allowed`
- failure returns:
  - `failure_state = retry_needed`
  - `failure_reason_category = retryable_generation_rejection`

---

### Step 12 — Execute the exhausted-retry fail-closed path

```powershell
@'
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "execution_ready_summary",
    "operator_message": "",
    "recommended_next_actions": "not-a-list",
    "grounded_input_fields_used": [
        "wp_id",
        "disallowed.field",
    ],
}

payload = build_work_package_output_failure_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=2,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_failure_metadata.failure_state = fail_closed`
- `output_failure_metadata.failure_reason_category = retry_budget_exhausted`
- `failure_feedback` is not `None`
- `accepted_output_family = None`
- `accepted_output_payload = None`

---

### Step 13 — Create the execution-ready baseline and execute the available-state chain

```powershell
@'
from datetime import datetime, timezone

from asbp.output_acceptance_logic import validate_work_package_output_before_acceptance
from asbp.output_consistency_logic import validate_work_package_output_family_consistency
from asbp.output_contract_logic import build_work_package_output_contract
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.output_family_logic import build_work_package_output_family_payload
from asbp.output_mapping_logic import build_work_package_output_mapping_payload
from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.output_target_logic import build_work_package_output_target_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "automation"],
        ),
    )
]

task_collections = [
    TaskCollectionModel(
        collection_id="TC-001",
        title="Committed Selection",
        collection_state="committed",
        work_package_id="WP-001",
        task_ids=["TASK-001"],
    )
]

tasks = [
    TaskModel(
        task_id="TASK-001",
        order=1,
        title="Prepare FAT",
        duration=1,
        work_package_id="WP-001",
        status="planned",
    )
]

plans = [
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
    )
]

candidate_output = {
    "response_mode": "execution_ready_summary",
    "operator_message": "The work package is ready for generation using the selected committed plan.",
    "recommended_next_actions": [
        "Execution-ready deterministic state reached."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "selected_plan_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.plan_ids",
    ],
}

print("TARGET:", build_work_package_output_target_payload(work_packages, task_collections, tasks, plans, wp_id="WP-001"))
print("CONTRACT:", build_work_package_output_contract(work_packages, task_collections, tasks, plans, wp_id="WP-001"))
print("MAPPING:", build_work_package_output_mapping_payload(work_packages, task_collections, tasks, plans, wp_id="WP-001"))
print("ACCEPTANCE:", validate_work_package_output_before_acceptance(work_packages, task_collections, tasks, plans, wp_id="WP-001", candidate_output=candidate_output))
print("RETRY:", evaluate_work_package_output_attempt(work_packages, task_collections, tasks, plans, wp_id="WP-001", candidate_output=candidate_output, attempt_number=1, max_attempts=2))
print("FAMILY:", build_work_package_output_family_payload(work_packages, task_collections, tasks, plans, wp_id="WP-001", candidate_output=candidate_output, attempt_number=1, max_attempts=2))
print("CONSISTENCY:", validate_work_package_output_family_consistency(work_packages, task_collections, tasks, plans, wp_id="WP-001", candidate_output=candidate_output, attempt_number=1, max_attempts=2, requested_family_id="single_work_package_operator_next_actions_only"))
print("FAILURE:", build_work_package_output_failure_payload(work_packages, task_collections, tasks, plans, wp_id="WP-001", candidate_output=candidate_output, attempt_number=1, max_attempts=2))
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- target available with:
  - `target_state = available`
  - `selected_plan_id = PLAN-001`
  - `generation_allowed = True`
- contract available with:
  - `contract_state = available`
  - `current_response_mode = execution_ready_summary`
- mapping available with:
  - `mapping_state = available`
  - `current_response_mode = execution_ready_summary`
  - `deterministic_input.structured_facts.orchestration_stage = execution_ready`
- acceptance accepted with:
  - `validation_state = accepted`
- retry accepted with:
  - `decision_state = accepted`
- family available with:
  - `family_state = available`
  - available families include:
    - `single_work_package_operator_response`
    - `single_work_package_operator_response_brief`
    - `single_work_package_operator_next_actions_only`
- consistency accepted with:
  - `consistency_state = accepted`
  - `resolved_family_id = single_work_package_operator_next_actions_only`
- failure accepted with:
  - `failure_state = accepted`

---

### Step 14 — Execute the unavailable requested-family fail-closed path

```powershell
@'
from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

candidate_output = {
    "response_mode": "blocked_explainer",
    "operator_message": "Generation cannot proceed until selector context is completed.",
    "recommended_next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
    ],
}

payload = build_work_package_output_failure_payload(
    work_packages,
    [],
    [],
    [],
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=1,
    max_attempts=2,
    requested_family_id="single_work_package_operator_next_actions_only",
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_failure_metadata.failure_state = fail_closed`
- `output_failure_metadata.failure_reason_category = non_retryable_output_family_rejection`
- `failure_feedback` instructs correction of the requested family selection
- `accepted_output_family = None`
- `accepted_output_payload = None`

---

### Step 15 — Execute the invalid retry-control fail-closed path on an otherwise valid execution-ready candidate

```powershell
@'
from datetime import datetime, timezone

from asbp.output_failure_logic import build_work_package_output_failure_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "automation"],
        ),
    )
]

task_collections = [
    TaskCollectionModel(
        collection_id="TC-001",
        title="Committed Selection",
        collection_state="committed",
        work_package_id="WP-001",
        task_ids=["TASK-001"],
    )
]

tasks = [
    TaskModel(
        task_id="TASK-001",
        order=1,
        title="Prepare FAT",
        duration=1,
        work_package_id="WP-001",
        status="planned",
    )
]

plans = [
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
    )
]

candidate_output = {
    "response_mode": "execution_ready_summary",
    "operator_message": "The work package is ready for generation using the selected committed plan.",
    "recommended_next_actions": [
        "Execution-ready deterministic state reached."
    ],
    "grounded_input_fields_used": [
        "wp_id",
        "selected_plan_id",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.plan_ids",
    ],
}

payload = build_work_package_output_failure_payload(
    work_packages,
    task_collections,
    tasks,
    plans,
    wp_id="WP-001",
    candidate_output=candidate_output,
    attempt_number=3,
    max_attempts=2,
)

print(payload)
'@ | python -
```

**Expected output / pass signal**

Payload must show:

- `output_failure_metadata.failure_state = fail_closed`
- `output_failure_metadata.failure_reason_category = non_retryable_retry_control_rejection`
- `decision_rationale` includes:
- `invalid_retry_control_state:attempt_number_exceeds_max_attempts`

---

### Step 16 — Re-run the full validation baseline after UAT execution

```powershell
python -m pytest -q
```

**Expected output / pass signal**

The suite must remain green.

Expected acceptance signal:

```text
502 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

## Protocol Checks

| Check ID   | Check                                                                                                       | Acceptance Criteria                                                                                                              |
| ---------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| UAT-M10-01 | All M10 output-layer surfaces reject missing Work Package deterministically                                 | Step 2 returns `None` across target, contract, mapping, acceptance, retry, family, consistency, and failure                      |
| UAT-M10-02 | Output target layer reports blocked single-work-package operator output target correctly                    | Step 3 returns blocked output-target payload                                                                                     |
| UAT-M10-03 | Output contract layer reports blocked operator-response contract correctly                                  | Step 4 returns blocked output-contract payload                                                                                   |
| UAT-M10-04 | Output mapping layer reports blocked deterministic mapping correctly                                        | Step 5 returns blocked mapping payload                                                                                           |
| UAT-M10-05 | Output acceptance accepts a valid blocked-state candidate response                                          | Step 6 returns `validation_state = accepted`                                                                                     |
| UAT-M10-06 | Output retry accepts a valid blocked-state candidate response deterministically                             | Step 7 returns `decision_state = accepted`                                                                                       |
| UAT-M10-07 | Output family layer exposes the correct blocked-mode family set                                             | Step 8 returns available blocked-mode families                                                                                   |
| UAT-M10-08 | Output consistency accepts the default blocked-mode family selection deterministically                      | Step 9 returns `consistency_state = accepted`                                                                                    |
| UAT-M10-09 | Output failure layer preserves accepted-state pass-through when the output is already consistent            | Step 10 returns `failure_state = accepted`                                                                                       |
| UAT-M10-10 | Contract-breaking candidate output is rejected deterministically and mapped to retry-needed behavior        | Step 11 returns rejected acceptance, retry-allowed retry path, blocked family state, and retry-needed failure state              |
| UAT-M10-11 | Output failure layer fails closed when retry budget is exhausted                                            | Step 12 returns `failure_state = fail_closed` with `retry_budget_exhausted`                                                      |
| UAT-M10-12 | Full execution-ready output chain becomes available and internally consistent                               | Step 13 returns available/accepted results across target, contract, mapping, acceptance, retry, family, consistency, and failure |
| UAT-M10-13 | Output failure layer fails closed on an unavailable requested family deterministically                      | Step 14 returns `non_retryable_output_family_rejection`                                                                          |
| UAT-M10-14 | Output failure layer fails closed on invalid retry-control state even for a valid execution-ready candidate | Step 15 returns `non_retryable_retry_control_rejection`                                                                          |
| UAT-M10-15 | Full validation baseline remains green after UAT execution                                                  | Step 16 returns a green `pytest` result                                                                                          |

## Failure Handling Rule

If any step produces a result that does not match the expected output above:

- stop the UAT run at that point
- do not continue guessing
- record the exact step number
- record the exact command that failed
- record the actual output shown
- classify the issue as one of:
  - execution mistake
  - protocol ambiguity
  - runtime/logic defect
  - environment/state contamination

## Acceptance Rule

Milestone 10 UAT may be accepted only if:

- all defined checks pass
- no in-scope deterministic output-layer contract is contradicted during execution
- no hidden output-family or failure-handling ambiguity is observed
- accepted, retry-needed, and fail-closed paths remain deterministic
- the repo remains aligned with the approved Milestone 10 boundary through M10.7

## Out of Scope

The following items are not part of M10 UAT acceptance execution:

- Milestone 10 closeout
- the mandatory `M10.10` full repo pass
- the hard integration decision before `M11.1`
- live LLM generation
- external model invocation
- free-form agentic behavior
- post-roadmap redesign
