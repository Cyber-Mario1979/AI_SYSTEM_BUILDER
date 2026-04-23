# M11_UAT_PROTOCOL

## Milestone

Milestone 11 — Production-Grade Micro AI System

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 11 boundary.

It is intended to confirm that the current Milestone 11 implementation behaves correctly for:

- production-structure package boundaries
- canonical versioning surface behavior
- retrieval-architecture boundary behavior
- runtime blocked-state contract behavior
- runtime execution-ready contract behavior
- candidate-response validation and retry/fail behavior
- output acceptance and output-retry behavior
- maintainability-hardening surface preservation
- architecture-cleanup wrapper-export preservation

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M11_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `524 passed in 45.79s`

## Operator Fields

- UAT date: `()`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 11 UAT should be executed against the repo-real Milestone 11 boundary.

That means:

- use public package surfaces where they now exist
- use controlled inline Python where the repo-real M11 boundary is logic-first rather than CLI-first
- do not invent new adapters during UAT
- no live LLM call, no free-form generation, and no out-of-scope redesign during UAT execution
- all checks must stay inside the approved Milestone 11 boundary through `M11.6`

## Scope Covered

The following Milestone 11 surfaces are in scope:

- `asbp.versioning`
- `asbp.retrieval`
- `asbp.runtime.boundary`
- `asbp.runtime.prompt_contract`
- `asbp.runtime.handoff`
- `asbp.runtime.control`
- `asbp.runtime.generation`
- `asbp.runtime.output_validation`
- `asbp.runtime.retry_fail`
- `asbp.runtime.output_acceptance`
- `asbp.runtime.output_retry`
- runtime wrapper export cleanup introduced at `M11.6`

## Test Data / Pre-Setup

Use controlled in-memory test state through inline Python.

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
524 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

---

### Step 2 — Verify the canonical versioning surface

```powershell
@'
from asbp.versioning import (
    RELEASE_STATE,
    RUNTIME_VERSION,
    STATE_VERSION,
    build_version_metadata,
)

print(build_version_metadata())
print(RUNTIME_VERSION)
print(STATE_VERSION)
print(RELEASE_STATE)
'@ | python -
```

**Expected output / pass signal**

Observed output must show:

- `runtime_version = 0.1.0`
- `state_version = 0.1.0`
- `release_state = active_development`

---

### Step 3 — Verify the retrieval architecture baseline and both allowed retrieval request families

```powershell
@'
from asbp.retrieval import (
    build_governed_retrieval_request,
    build_probabilistic_search_retrieval_request,
    build_retrieval_architecture_baseline,
)

print("BASELINE:", build_retrieval_architecture_baseline())
print(
    "GOVERNED:",
    build_governed_retrieval_request(
        artifact_kind="task_pool",
        lookup_id="POOL-TABPRESS-001",
        compiled_surface_id="compiled-task-pools-v1",
        library_version="2026.04",
    ),
)
print(
    "PROBABILISTIC:",
    build_probabilistic_search_retrieval_request(
        query_text="tablet press FAT",
        search_scope="uat_notes",
    ),
)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- baseline checkpoint = `M11.4`
- governed request mode = `governed_deterministic`
- governed request source_of_truth_role = `downstream_consumer_only`
- probabilistic request mode = `probabilistic_search`
- probabilistic request source_of_truth_role = `non_authoritative_support_only`

---

### Step 4 — Verify retrieval boundary rejection for prohibited governed-request fields

```powershell
@'
from asbp.retrieval import validate_retrieval_request

try:
    validate_retrieval_request(
        {
            "mode": "governed_deterministic",
            "artifact_kind": "task_pool",
            "lookup_id": "POOL-TABPRESS-001",
            "compiled_surface_id": "compiled-task-pools-v1",
            "library_version": "2026.04",
            "source_of_truth_role": "downstream_consumer_only",
            "query_text": "this should not be allowed",
        }
    )
except Exception as exc:
    print(type(exc).__name__)
    print(exc)
'@ | python -
```

**Expected output / pass signal**

The command must fail deterministically.

Expected rejection meaning:

```text
ValueError
query_text is not allowed in this retrieval mode.
```

---

### Step 5 — Verify the blocked runtime chain through the public runtime boundary surfaces

```powershell
@'
from asbp.runtime.boundary import build_work_package_runtime_boundary_payload
from asbp.runtime.control import build_work_package_runtime_control_payload
from asbp.runtime.generation import build_work_package_generation_request_payload
from asbp.runtime.handoff import build_work_package_llm_handoff_payload
from asbp.runtime.prompt_contract import build_work_package_prompt_contract_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

print(
    "BOUNDARY:",
    build_work_package_runtime_boundary_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    ),
)
print(
    "PROMPT_CONTRACT:",
    build_work_package_prompt_contract_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    ),
)
print(
    "HANDOFF:",
    build_work_package_llm_handoff_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    ),
)
print(
    "CONTROL:",
    build_work_package_runtime_control_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    ),
)
print(
    "GENERATION:",
    build_work_package_generation_request_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    ),
)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- boundary state is blocked / not eligible for prompt contract
- orchestration stage = `binding_context_required`
- prompt contract mode = `blocked_explainer`
- handoff state = `blocked`
- runtime control state = `blocked_explainer_only`
- generation state = `blocked`

---

### Step 6 — Verify candidate-response validation and retry/fail behavior for a valid blocked-state candidate

```powershell
@'
from asbp.runtime.output_validation import validate_work_package_candidate_response
from asbp.runtime.retry_fail import evaluate_work_package_candidate_response_attempt
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

print(
    "VALIDATION:",
    validate_work_package_candidate_response(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output=candidate_output,
    ),
)
print(
    "RETRY_FAIL:",
    evaluate_work_package_candidate_response_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output=candidate_output,
        attempt_number=1,
        max_attempts=2,
    ),
)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- validation state = `accepted`
- retry/fail decision state = `accepted`
- fallback action = `use_validated_output`
- retries remaining = `1`

---

### Step 7 — Verify output acceptance and output retry behavior for a contract-breaking blocked-state candidate

```powershell
@'
from asbp.runtime.output_acceptance import validate_work_package_output_before_acceptance
from asbp.runtime.output_retry import evaluate_work_package_output_attempt
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

print(
    "ACCEPTANCE:",
    validate_work_package_output_before_acceptance(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output=candidate_output,
    ),
)
print(
    "OUTPUT_RETRY:",
    evaluate_work_package_output_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output=candidate_output,
        attempt_number=1,
        max_attempts=2,
    ),
)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- output acceptance validation state = `rejected`
- output acceptance includes deterministic contract-breaking errors
- output retry decision state = `retry_allowed`
- output retry regeneration action = `request_regenerated_output_from_same_mapping_contract`

---

### Step 8 — Verify the execution-ready runtime and output chain on controlled in-memory state

```powershell
@'
from datetime import datetime, timezone

from asbp.runtime.control import build_work_package_runtime_control_payload
from asbp.runtime.generation import build_work_package_generation_request_payload
from asbp.runtime.output_acceptance import validate_work_package_output_before_acceptance
from asbp.runtime.output_retry import evaluate_work_package_output_attempt
from asbp.runtime.output_target import build_work_package_output_target_payload
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

print(
    "CONTROL:",
    build_work_package_runtime_control_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ),
)
print(
    "GENERATION:",
    build_work_package_generation_request_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ),
)
print(
    "TARGET:",
    build_work_package_output_target_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ),
)
print(
    "ACCEPTANCE:",
    validate_work_package_output_before_acceptance(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
    ),
)
print(
    "OUTPUT_RETRY:",
    evaluate_work_package_output_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
        attempt_number=1,
        max_attempts=2,
    ),
)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- runtime control state = `execution_ready_summary_only`
- generation state = `ready`
- selected plan = `PLAN-001`
- output target state = `available`
- output acceptance validation state = `accepted`
- output retry decision state = `accepted`

---

### Step 9 — Verify the M11.6 wrapper cleanup preserved explicit exports and package-aligned public surfaces

```powershell
@'
import asbp.runtime as runtime_pkg
import asbp.runtime.boundary as runtime_boundary_module
import asbp.runtime.contracts as runtime_contracts_module
import asbp.runtime.generation as runtime_generation_module
import asbp.runtime.output_retry as runtime_output_retry_module
import asbp.retrieval as retrieval_pkg

print("RUNTIME_BOUNDARY_ALL:", runtime_boundary_module.__all__)
print("RUNTIME_CONTRACTS_ALL:", runtime_contracts_module.__all__)
print("RUNTIME_GENERATION_ALL:", runtime_generation_module.__all__)
print("RUNTIME_OUTPUT_RETRY_ALL:", runtime_output_retry_module.__all__)
print("RUNTIME_PACKAGE_HAS_OUTPUT_RETRY:", hasattr(runtime_pkg, "evaluate_work_package_output_attempt"))
print("RETRIEVAL_ALL:", retrieval_pkg.__all__)
'@ | python -
```

**Expected output / pass signal**

Observed results must show:

- explicit `__all__` lists are present on the wrapper modules
- runtime package exposes `evaluate_work_package_output_attempt`
- retrieval package exposes its governed/probabilistic public surface set
- no wildcard-dependent ambiguity is visible in the exported public boundary

---

### Step 10 — Re-run the full validation baseline after UAT execution

```powershell
python -m pytest -q
```

**Expected output / pass signal**

The suite must remain green.

Expected acceptance signal:

```text
524 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

## Protocol Checks

| Check ID   | Check                                                                                                         | Acceptance Criteria                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| UAT-M11-01 | Canonical versioning surface remains stable and deterministic                                                 | Step 2 matches expected version metadata                                   |
| UAT-M11-02 | Retrieval architecture baseline preserves governed vs probabilistic separation                                | Step 3 returns correct modes and source-of-truth roles                     |
| UAT-M11-03 | Retrieval boundary rejects prohibited governed-request fields deterministically                               | Step 4 fails closed with the expected rejection meaning                    |
| UAT-M11-04 | Runtime blocked-state chain remains deterministic across boundary, contract, handoff, control, and generation | Step 5 reports blocked-state progression correctly                         |
| UAT-M11-05 | Candidate-response validation and retry/fail behavior accept a valid blocked-state candidate                  | Step 6 returns accepted validation and accepted retry/fail decision        |
| UAT-M11-06 | Output acceptance and output-retry behavior reject contract-breaking output deterministically                 | Step 7 returns rejected acceptance and retry-allowed output retry decision |
| UAT-M11-07 | Execution-ready runtime and output chain behaves deterministically on controlled in-memory state              | Step 8 returns execution-ready/available/accepted states correctly         |
| UAT-M11-08 | M11.6 architecture cleanup preserved explicit wrapper exports and stable public package surfaces              | Step 9 confirms explicit exports and package-level availability            |
| UAT-M11-09 | Full validation baseline remains green after UAT execution                                                    | Step 10 returns a green `pytest` result                                    |

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
  - environment contamination

## Acceptance Rule

Milestone 11 UAT may be accepted only if:

- all defined checks pass
- no in-scope deterministic contract is contradicted during execution
- no hidden wrapper/export ambiguity is observed
- governed retrieval remains separate from probabilistic retrieval
- blocked-state and execution-ready runtime behaviors remain deterministic
- validation and retry/fail behavior remain deterministic
- the repo remains aligned with the approved Milestone 11 boundary through `M11.6`

## Out of Scope

The following items are not part of M11 UAT acceptance execution:

- Milestone 11 closeout
- any Milestone 12 work
- live LLM generation
- external model invocation
- free-form agentic behavior
- post-roadmap productization work
