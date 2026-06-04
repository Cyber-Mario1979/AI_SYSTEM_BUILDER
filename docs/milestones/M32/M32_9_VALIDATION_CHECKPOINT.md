# M32.9 — Validation Checkpoint

Status: Completed on validation branch  
Checkpoint: M32.9  
Mode: Validation  
Branch: `m32-9-validation-checkpoint`  
Validation date: 2026-06-04

## Purpose

Record M32.9 validation evidence for the merged local workflow/UI path.

M32.9 is a validation checkpoint. It does not add product features, AI behavior, provider behavior, UI surfaces, release behavior, deployment behavior, UAT acceptance, or closeout records.

## Validation target

Validate the approved M32 local workflow/UI scenario path:

```text
scenario -> configure -> plan -> status -> outputs
```

Approved scenario:

```text
cleanroom-hvac-qualification-basic
```

Scenario identifiers:

```text
Work package: WP-032
Task/source collection: TC-032
Plan: PLAN-032
```

## Validation commands

Focused M32.8 scenario validation:

```text
python -m pytest tests/test_m32_8_end_to_end_local_scenario.py -q
```

M32 local workflow regression validation:

```text
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py tests/test_m32_8_end_to_end_local_scenario.py -q
```

Full validation:

```text
python -m pytest -q
```

Manual scenario evidence commands:

```text
python -m asbp.adapters.local_workflow_cli scenario --scenario-id cleanroom-hvac-qualification-basic
python -m asbp.adapters.local_workflow_cli configure --wp-id WP-032 --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac
python -m asbp.adapters.local_workflow_cli plan --wp-id WP-032
python -m asbp.adapters.local_workflow_cli status --wp-id WP-032
python -m asbp.adapters.local_workflow_cli outputs --wp-id WP-032
```

Runtime state restoration after manual scenario exercise:

```text
git restore data/state/state.json
git status — nothing to commit, working tree clean
```

## Validation evidence

Validation was run locally by the project owner in the checked-out feature branch.

Executable validation:

```text
Focused M32.8 validation: python -m pytest tests/test_m32_8_end_to_end_local_scenario.py -q — 5 passed in 1.97s
M32 local workflow regression validation: python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py tests/test_m32_8_end_to_end_local_scenario.py -q — 36 passed in 7.47s
Full validation: python -m pytest -q — 1615 passed in 54.03s
```

Manual scenario evidence:

```text
Scenario command: scenario_id cleanroom-hvac-qualification-basic; scenario_status staged; state_status in_flight; selected_work_package.wp_id WP-032; can_be_exercised_through_local_workflow true.
Configure command: updated_work_package.wp_id WP-032; selector_context cleanroom-hvac / cqv-cleanroom-hvac-basic / qualification-only / [cqv-core, cleanroom-hvac]; limitations present.
Plan command: selected_work_package.wp_id WP-032; task_count 3; task_ids TASK-M32-8-001, TASK-M32-8-002, TASK-M32-8-003; source_selection.collection_ids TC-032; readiness_gaps empty; limitations present.
Status command: workflow_state.selected_work_package.wp_id WP-032; task_lifecycle.task_count 3; status_counts planned=3; generated_schedule_present true; plan_id PLAN-032; generated_task_plan_count 3; source_and_citation_state.collection_ids TC-032; standards_bundles cqv-core and cleanroom-hvac; AI/provider/Ollama calls false; human_review_required true; readiness_gaps empty; limitations present.
Outputs command: selected_work_package.wp_id WP-032; document/export/report statuses not_available; artifact_available false; output_validation_state.validation_available false; human_review_required true; accepted false; approval_claimed false; release_claimed false; download_allowed false; download_performed false; path_exposed false; limitations present.
Runtime state restoration: data/state/state.json restored; git status reported nothing to commit, working tree clean.
```

## Scenario evidence interpretation

Manual scenario evidence confirms:

- scenario command returns the M32.8 scenario payload;
- configure command returns controlled input payload for `WP-032`;
- plan command returns task staging and source selection for `WP-032`;
- status command returns workflow visibility, schedule lifecycle, source/citation state, and AI limitation state;
- outputs command returns output review/access visibility with human review required;
- no command claims product readiness, release, deployment, approval, signature, certification, SaaS readiness, commercial readiness, or customer-ready output.

## Boundary statement

M32.9 validation preserves the following boundaries:

- CLI/local workflow surfaces remain adapters only;
- no CQV domain logic is added to the CLI surface;
- no raw state writes or persistence-boundary bypass is allowed;
- source/citation, output, AI, validation, readiness, and scenario limitations must remain visible;
- no false success states are accepted;
- no AI, Ollama, provider API, cloud service, web UI, desktop UI, SaaS/admin/customer surface, deployment, release, or commercialization behavior is added;
- no output is accepted, signed, approved, released, certified, or treated as product-ready;
- human review remains required.

## Scope limits

This validation record does not claim:

- M32.9 completion on `main` until PR merge;
- M32.10 UAT / owner acceptance;
- M32.11 closeout;
- product readiness;
- release readiness;
- deployment readiness;
- SaaS readiness;
- commercial readiness;
- customer-ready output;
- full product/runtime AI readiness.

## Tracker movement

M32.9 may be recorded as complete on the validation branch because focused M32.8 validation, M32 local workflow regression validation, full validation, manual scenario evidence, and runtime state restoration evidence exist.

The next checkpoint after validated M32.9 merge is:

```text
PLAN M32.10 — Milestone UAT / owner acceptance
```

M32.10 remains blocked until M32.9 is merged and separately authorized.
