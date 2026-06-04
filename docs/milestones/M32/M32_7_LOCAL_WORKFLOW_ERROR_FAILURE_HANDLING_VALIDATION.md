# M32.7 — Local Workflow Error/Failure Handling Validation

Status: Implementation branch prepared; validation pending owner/local run  
Checkpoint: M32.7  
Mode: Build/content  
Branch: `m32-7-local-workflow-failure-handling`  
Validation date: 2026-06-04

## Purpose

Record M32.7 implementation scope and required validation for visible and safe local workflow error/failure handling.

## Implementation summary

M32.7 adds bounded local workflow failure payloads and routes local workflow CLI failure cases through those payloads instead of ad hoc text-only messages.

Implemented files:

```text
asbp/local_workflow_failure_logic.py
asbp/adapters/local_workflow_cli.py
tests/test_m32_7_local_workflow_failure_handling.py
```

Updated regression tests:

```text
tests/test_m32_3_local_workflow_cli_adapter.py
tests/test_m32_4_controlled_input_surfaces.py
tests/test_m32_5_workflow_visibility_surfaces.py
tests/test_m32_6_output_review_download_surfaces.py
```

## Boundary statement

The implementation is intentionally limited.

It:

- adds structured failure payloads for missing input, missing state, invalid state, invalid references, source limitations, validation errors, and provider/AI failure visibility;
- keeps the CLI surface as an adapter only;
- preserves state loading through the approved state store boundary;
- returns non-success status for blocking local workflow failures;
- keeps readiness, validation, source, output, approval, release, and AI limitations visible;
- does not mutate state for failure handling;
- does not place CQV domain logic in the CLI adapter;
- does not generate documents, exports, reports, artifacts, downloads, signatures, approval records, release records, or product-ready output;
- does not call AI, Ollama, provider APIs, cloud services, web UI, desktop UI, SaaS/admin/customer surfaces, deployment, release, or commercialization behavior.

## Required validation

Focused M32.7 validation:

```text
python -m pytest tests/test_m32_7_local_workflow_failure_handling.py -q
```

M32 local workflow adapter regression validation:

```text
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py -q
```

Full validation:

```text
python -m pytest -q
```

## Validation evidence

Validation has not been run by the assistant in this connector-only session. The project owner must run the validation commands locally on branch `m32-7-local-workflow-failure-handling` before merge or tracker advancement.

## Scope limits

This record does not claim:

- M32.7 completion on `main`;
- M32.8 end-to-end local scenario implementation;
- M32 milestone UAT;
- product readiness;
- release readiness;
- deployment readiness;
- SaaS readiness;
- commercial readiness;
- customer-ready output;
- full product/runtime AI readiness.

## Tracker movement

M32.7 may be recorded as complete only after focused M32.7 validation, M32 local workflow regression validation, and full validation pass.

The next checkpoint after validated M32.7 completion would be:

```text
PLAN M32.8 — End-to-end local scenario implementation
```

M32.8 implementation remains blocked until M32.7 is validated, reviewed, merged, and separately authorized.
