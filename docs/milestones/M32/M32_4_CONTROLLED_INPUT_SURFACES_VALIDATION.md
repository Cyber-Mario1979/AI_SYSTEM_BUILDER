# M32.4 — Controlled Input Surfaces Validation

Status: Completed on implementation branch  
Checkpoint: M32.4  
Mode: Build/content  
Branch: `m32-4-controlled-input-surface`  
Validation date: 2026-06-03

## Purpose

Record M32.4 implementation and validation evidence for the controlled local workflow input surface.

## Implementation summary

M32.4 added a controlled `configure` command to the existing CLI-enhanced local workflow adapter.

Implemented files:

```text
asbp/local_workflow_input_logic.py
asbp/adapters/local_workflow_cli.py
asbp/local_workflow_logic.py
tests/test_m32_4_controlled_input_surfaces.py
```

The controlled input command is:

```text
python -m asbp.adapters.local_workflow_cli configure --wp-id WP-001 --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac
```

The read-only planning command remains:

```text
python -m asbp.adapters.local_workflow_cli plan --wp-id WP-001
```

## Boundary statement

The implementation is intentionally limited.

It:

- applies controlled selector/profile/source choices;
- uses explicit CLI parser choices for allowed controlled inputs;
- uses existing work-package core functions for selector/profile/source binding;
- saves through the approved state store helper;
- preserves `cqv-core` as the baseline standards bundle;
- exposes non-blocking `input_warnings` for title/profile mismatch review;
- keeps the CLI surface as an adapter only;
- does not place CQV domain logic in the CLI adapter;
- does not treat free-form user text as source truth;
- does not call AI, Ollama, provider APIs, cloud services, web UI, desktop UI, SaaS/admin/customer surfaces, deployment, release, or commercialization behavior.

## Manual smoke evidence

Manual smoke check confirmed that the read-only plan payload surfaces a warning when a work package title may not match the selected controlled system/profile boundary.

Observed warning:

```text
Selected system_type cleanroom-hvac may not match work package title: Tablet press qualification
```

## Validation evidence

Focused validation:

```text
python -m pytest tests/test_m32_4_controlled_input_surfaces.py -q
6 passed in 1.28s
```

Full validation:

```text
python -m pytest -q
1589 passed in 54.47s
```

## Scope limits

This record does not claim:

- M32.5 workflow visibility surfaces;
- M32.6 output review/download surfaces;
- M32.7 failure-handling completion;
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

M32.4 may be recorded as complete because controlled input behavior exists and full validation passed.

The next checkpoint is:

```text
PLAN M32.5 — Workflow visibility surfaces
```

M32.5 implementation remains blocked until separately planned and authorized.
