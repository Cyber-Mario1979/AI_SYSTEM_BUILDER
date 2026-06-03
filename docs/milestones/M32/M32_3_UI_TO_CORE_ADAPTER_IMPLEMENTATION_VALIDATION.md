# M32.3 — UI-to-core Adapter Implementation Validation

Status: Completed on implementation branch  
Checkpoint: M32.3  
Mode: Build/content  
Branch: `m32-3-cli-workflow-adapter`  
Validation date: 2026-06-03

## Purpose

Record M32.3 implementation and validation evidence for the minimal CLI-enhanced local workflow adapter.

## Implementation summary

M32.3 added a minimal read-only local workflow adapter path.

Implemented files:

```text
asbp/local_workflow_logic.py
asbp/adapters/local_workflow_cli.py
tests/test_m32_3_local_workflow_cli_adapter.py
```

The local workflow adapter command is:

```text
python -m asbp.adapters.local_workflow_cli plan --wp-id WP-001
```

## Boundary statement

The implementation is intentionally limited.

It:

- reads validated local state;
- builds a local workflow planning payload;
- exposes selected work package, selector context, staged tasks, source collection bindings, review gates, readiness gaps, and limitations;
- uses existing core/service boundary wrappers;
- keeps the CLI surface as an adapter only;
- does not mutate state;
- does not write raw files directly;
- does not treat free-form user text as truth;
- does not call AI, Ollama, provider APIs, cloud services, web UI, desktop UI, SaaS/admin/customer surfaces, deployment, release, or commercialization behavior.

## Validation evidence

Focused validation:

```text
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py -q
4 passed in 0.73s
```

Full validation:

```text
python -m pytest -q
1583 passed in 49.47s
```

## Scope limits

This record does not claim:

- M32.4 controlled input surfaces;
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

M32.3 may be recorded as complete because adapter behavior exists and full validation passed.

The next checkpoint is:

```text
PLAN M32.4 — Controlled input surfaces
```

M32.4 implementation remains blocked until separately planned and authorized.
