# M32.7 — Local Workflow Error/Failure Handling Validation

Status: Completed on implementation branch  
Checkpoint: M32.7  
Mode: Build/content  
Branch: `m32-7-local-workflow-failure-handling`  
Validation date: 2026-06-04

## Purpose

Record M32.7 implementation and validation evidence for visible and safe local workflow error/failure handling.

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

The implementation covers visible and safe handling for:

- missing command/input;
- missing state file;
- invalid JSON/state validation;
- invalid work-package references;
- source/citation limitations;
- output validation errors/limitations;
- provider/AI failure visibility where in scope.

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

## Validation evidence

Focused M32.7 validation:

```text
python -m pytest tests/test_m32_7_local_workflow_failure_handling.py -q
8 passed in 1.22s
```

M32 local workflow adapter regression validation:

```text
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py -q
31 passed in 5.64s
```

Full validation:

```text
python -m pytest -q
1610 passed in 53.65s
```

Validation was run locally by the project owner in the checked-out feature branch.

## Scope limits

This record does not claim:

- M32.7 completion on `main` until PR merge;
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

M32.7 may be recorded as complete on the implementation branch because failure behavior exists and focused M32.7 validation, M32 local workflow regression validation, and full validation passed.

The next checkpoint after M32.7 merge is:

```text
PLAN M32.8 — End-to-end local scenario implementation
```

M32.8 implementation remains blocked until M32.7 is merged and separately authorized.
