# M32.5 — Workflow Visibility Surfaces Validation

Status: Completed on implementation branch  
Checkpoint: M32.5  
Mode: Build/content  
Branch: `m32-5-workflow-visibility-surface`  
Validation date: 2026-06-04

## Purpose

Record M32.5 implementation and validation evidence for the read-only local workflow visibility surface.

## Implementation summary

M32.5 added a read-only workflow visibility surface to the existing CLI-enhanced local workflow adapter.

Implemented files:

```text
asbp/local_workflow_visibility_logic.py
asbp/adapters/local_workflow_cli.py
tests/test_m32_5_workflow_visibility_surfaces.py
```

The local workflow visibility command is:

```text
python -m asbp.adapters.local_workflow_cli status --wp-id WP-001
```

The existing commands remain available:

```text
python -m asbp.adapters.local_workflow_cli plan --wp-id WP-001
python -m asbp.adapters.local_workflow_cli configure --wp-id WP-001 --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac
```

## Boundary statement

The implementation is intentionally limited.

It:

- adds a read-only `status` command for workflow visibility;
- keeps the CLI surface as an adapter only;
- reads validated local state through the existing state store boundary;
- exposes workflow state, task lifecycle, schedule lifecycle, document lifecycle limitation, source/citation state, AI limitation state, input warnings, readiness gaps, limitations, and next safe actions;
- makes document lifecycle status explicit as not implemented in the current surface and assigned to M32.6 unless separately scoped;
- makes AI/provider/Ollama/live-model non-use visible;
- does not mutate state;
- does not place CQV domain logic in the CLI adapter;
- does not write raw state/files directly;
- does not treat retrieval or standards identifiers as upgraded source authority;
- does not call AI, Ollama, provider APIs, cloud services, web UI, desktop UI, SaaS/admin/customer surfaces, deployment, release, or commercialization behavior.

## Validation evidence

Focused M32.5 validation:

```text
python -m pytest tests/test_m32_5_workflow_visibility_surfaces.py -q
6 passed in 1.00s
```

M32 local workflow adapter regression validation:

```text
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py -q
16 passed in 2.81s
```

Full validation:

```text
python -m pytest -q
1595 passed in 49.76s
```

Validation was run locally by the project owner in the checked-out feature branch after the M32.5 timestamp-expectation test correction.

## Scope limits

This record does not claim:

- M32.6 output review/download surfaces;
- M32.7 local workflow failure-handling completion;
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

M32.5 may be recorded as complete because workflow visibility behavior exists and full validation passed.

The next checkpoint is:

```text
PLAN M32.6 — Output review/download surfaces
```

M32.6 implementation remains blocked until separately planned and authorized.
