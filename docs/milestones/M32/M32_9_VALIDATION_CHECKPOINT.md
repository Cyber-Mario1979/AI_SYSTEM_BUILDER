# M32.9 — Validation Checkpoint

Status: Validation branch prepared; validation pending owner/local run  
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

## Required validation commands

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
git checkout -- data/state/state.json
```

## Validation evidence

Validation has not been run by the assistant in this connector-only session.

The project owner must run the validation commands locally on branch `m32-9-validation-checkpoint` before tracker advancement, PR readiness, or merge.

Pending evidence fields:

```text
Focused M32.8 validation: PENDING
M32 local workflow regression validation: PENDING
Full validation: PENDING
Manual scenario evidence: PENDING
Runtime state restoration: PENDING
```

## Scenario evidence expectations

Manual scenario evidence should confirm:

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

M32.9 may be recorded as complete only after focused M32.8 validation, M32 local workflow regression validation, full validation, manual scenario evidence, and runtime state restoration evidence exist.

The next checkpoint after validated M32.9 completion would be:

```text
PLAN M32.10 — Milestone UAT / owner acceptance
```

M32.10 remains blocked until M32.9 is validated, reviewed, merged, and separately authorized.
