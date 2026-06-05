# M32.10 — Milestone UAT / Owner Acceptance

Status: Owner accepted on UAT branch  
Checkpoint: M32.10  
Mode: UAT  
Branch: `m32-10-uat-owner-acceptance`  
Record date: 2026-06-05

## Purpose

Record M32.10 UAT / owner acceptance for the M32 local workflow/UI as trial-ready with limitations.

M32.10 is an owner acceptance checkpoint. It does not implement new product features, AI behavior, provider behavior, UI surfaces, release behavior, deployment behavior, or closeout records.

## Acceptance status

Current owner acceptance status:

```text
ACCEPTED WITH LIMITATIONS
```

M32.10 may be recorded as complete on this branch because the project owner explicitly accepted the local workflow as trial-ready with limitations recorded.

## Acceptance target

Bounded local workflow/UI trial target:

```text
scenario -> configure -> plan -> status -> outputs
```

Approved local scenario:

```text
cleanroom-hvac-qualification-basic
```

Scenario identifiers:

```text
Work package: WP-032
Task/source collection: TC-032
Plan: PLAN-032
```

## Evidence basis

Primary validation evidence:

```text
docs/milestones/M32/M32_9_VALIDATION_CHECKPOINT.md
```

M32.9 executable validation evidence:

```text
python -m pytest tests/test_m32_8_end_to_end_local_scenario.py -q — 5 passed in 1.97s
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py tests/test_m32_8_end_to_end_local_scenario.py -q — 36 passed in 7.47s
python -m pytest -q — 1615 passed in 54.03s
```

M32.9 manual scenario evidence:

```text
Scenario path: scenario -> configure -> plan -> status -> outputs
Scenario command: scenario_id cleanroom-hvac-qualification-basic; scenario_status staged; state_status in_flight; selected_work_package.wp_id WP-032; can_be_exercised_through_local_workflow true.
Configure command: updated_work_package.wp_id WP-032; selector_context cleanroom-hvac / cqv-cleanroom-hvac-basic / qualification-only / [cqv-core, cleanroom-hvac]; limitations present.
Plan command: selected_work_package.wp_id WP-032; task_count 3; task_ids TASK-M32-8-001, TASK-M32-8-002, TASK-M32-8-003; source_selection.collection_ids TC-032; readiness_gaps empty; limitations present.
Status command: workflow_state.selected_work_package.wp_id WP-032; task_lifecycle.task_count 3; status_counts planned=3; generated_schedule_present true; plan_id PLAN-032; generated_task_plan_count 3; source_and_citation_state.collection_ids TC-032; standards_bundles cqv-core and cleanroom-hvac; AI/provider/Ollama calls false; human_review_required true; readiness_gaps empty; limitations present.
Outputs command: selected_work_package.wp_id WP-032; document/export/report statuses not_available; artifact_available false; output_validation_state.validation_available false; human_review_required true; accepted false; approval_claimed false; release_claimed false; download_allowed false; download_performed false; path_exposed false; limitations present.
Runtime state restoration: data/state/state.json restored; git status reported nothing to commit, working tree clean.
```

Optional supporting LLM evidence:

```text
docs/milestones/M32/M32_OPTIONAL_LOCAL_LLM_SMOKE_TEST_PROTOCOL.md
docs/milestones/M32/M32_OPTIONAL_LOCAL_LLM_SMOKE_TEST_EVIDENCE.md
```

Optional LLM evidence summary:

```text
Ollama version: 0.30.2
Model: llama3.2:3b
Result: PASS
Classification: optional supporting evidence only
AI/local call performed: true
Cloud/provider call performed: false
Draft/support only: true
Human review required: true
Approval claimed: false
Release claimed: false
Certification claimed: false
Compliance claimed: false
Product-ready claimed: false
Customer-ready claimed: false
Deployment-ready claimed: false
Normal pytest dependency on Ollama/live model: false
```

## Owner acceptance statement

The project owner explicitly accepted M32.10 with the proposed conditional owner acceptance statement:

```text
I accept M32.10 with the proposed conditional owner acceptance statement.
```

Accepted statement:

```text
The project owner conditionally accepts the M32 local workflow/UI as trial-ready for a bounded local cleanroom HVAC qualification-only scenario, with limitations recorded.

Accepted trial scope:
- CLI-enhanced local workflow only.
- Scenario path: scenario -> configure -> plan -> status -> outputs.
- Scenario identifiers: WP-032, TC-032, PLAN-032.
- Output review remains metadata/visibility only.
- Human review remains required.
- Optional local/offline LLM draft support is accepted only as optional supporting trial evidence with limitations.

Not accepted:
- product readiness;
- commercial readiness;
- SaaS readiness;
- deployment readiness;
- release readiness;
- customer-ready output;
- AI approval authority;
- AI release/certification authority;
- provider/cloud API readiness;
- web UI readiness;
- desktop UI readiness;
- customer surface readiness;
- full product/runtime AI readiness.
```

## Optional local/offline LLM treatment

For M32.10 acceptance, optional local/offline LLM draft support is classified as:

```text
accepted as optional trial limitation
```

This means the optional local/offline LLM smoke-test evidence may support trial planning, but it does not become required workflow behavior, product evidence, output acceptance, AI authority, or readiness evidence.

## Required limitations

M32.10 acceptance preserves these limitations:

- CLI/local workflow surfaces remain adapters only;
- no CQV domain logic is added to the CLI surface;
- no raw state writes or persistence-boundary bypass is allowed;
- source/citation, standards, retrieval, output, validation, readiness, and AI limitations remain visible;
- output review remains metadata/visibility only;
- generated or assembled output remains human-review-required;
- optional local/offline LLM draft support remains optional and supporting only;
- normal pytest does not require Ollama or a live model;
- no output is accepted, signed, approved, released, certified, or treated as product-ready;
- no commercial, SaaS, deployment, release, customer-ready, or full product/runtime AI readiness is claimed.

## Acceptance decision

Owner decision:

```text
ACCEPTED WITH LIMITATIONS
```

Decision date:

```text
2026-06-05
```

Owner acceptance evidence:

```text
The project owner stated: "I accept M32.10 with the proposed conditional owner acceptance statement."
```

## Scope limits

This UAT record does not claim:

- M32.10 completion on `main` until PR merge after owner acceptance;
- M32.11 closeout;
- product readiness;
- release readiness;
- deployment readiness;
- SaaS readiness;
- commercial readiness;
- customer-ready output;
- full product/runtime AI readiness;
- AI approval authority;
- AI release/certification authority;
- provider/cloud API readiness;
- web UI readiness;
- desktop UI readiness;
- customer surface readiness.

## Tracker movement

M32.10 may be recorded as complete on this branch because explicit owner acceptance exists.

The next checkpoint after accepted M32.10 merge is:

```text
PLAN M32.11 — Milestone closeout
```

M32.11 remains blocked until M32.10 is accepted, reviewed, merged, and separately authorized.
