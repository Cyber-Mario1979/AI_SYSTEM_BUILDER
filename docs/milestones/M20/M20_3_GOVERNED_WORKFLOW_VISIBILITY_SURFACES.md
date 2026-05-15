# M20.3 — Governed Workflow Visibility Surfaces

## Purpose

This checkpoint introduces deterministic UI visibility surfaces for governed workflow state.

The UI layer may display governed workflow payloads supplied by approved API/service read boundaries, but it must not fetch raw state, mutate workflow state, execute workflow behavior, or become workflow-state truth.

## Boundary decision

The workflow visibility module is:

`asbp/ui/workflow_visibility.py`

The module defines display-only contracts and payload envelopes only.

It does not introduce screens, framework behavior, routes, endpoint behavior, workflow execution, command mutation, persistence access, or raw state reads.

## Supported visibility surfaces

The supported governed workflow visibility surfaces are:

- `workflow_overview`
- `work_package_status`
- `task_status`
- `validation_status`

These are UI visibility contracts only. They do not define new workflow behavior.

## Source-boundary rule

Workflow visibility payloads may only be built from approved API/service read boundaries.

Allowed source-boundary names are:

- `api_read_surface`
- `service_read_surface`
- `api_service_read_boundary`
- `approved_api_service_boundary`

Forbidden source-boundary names include:

- `raw_state_storage`
- `raw_persistence_helpers`
- `direct_state_mutation`
- `ui_owned_state`

## Visibility safety rules

Workflow visibility surfaces must:

- remain display-only
- preserve API/service payload truth
- present invalid or missing state without auto-correction
- expose visibility gaps as visibility gaps
- reject unsupported visibility surfaces fail-closed
- reject raw state or persistence source boundaries fail-closed

## Forbidden behavior

The UI visibility layer must not:

- mutate workflow state
- own workflow state
- create validation truth
- resolve workflow state from raw storage
- bypass API/service validation
- apply hidden workflow rules
- silently correct invalid state
- introduce UI framework or screen behavior

## M20.3 implementation evidence

This checkpoint adds:

- `asbp/ui/workflow_visibility.py`
- updates exports in `asbp/ui/__init__.py`
- `tests/test_ui_workflow_visibility.py`

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.3 only introduces governed workflow visibility contracts.

Document/export/reporting visibility remains in `M20.4`.
Operator action/intake remains in `M20.5`.
UI safety and execution-truth separation remains in `M20.6`.
