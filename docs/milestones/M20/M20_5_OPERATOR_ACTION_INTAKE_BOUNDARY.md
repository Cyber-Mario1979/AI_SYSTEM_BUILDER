# M20.5 — Operator Action/Intake Boundary

## Purpose

This checkpoint introduces a deterministic UI operator action/intake boundary.

The UI layer may collect, preview, validate, and prepare operator intent for downstream API/service command boundaries, but it must not execute actions, mutate raw state, create UI-originated hidden business rules, autonomously act, or expand approval/release authority.

## Boundary decision

The operator intake module is:

`asbp/ui/operator_intake.py`

The module defines limited intake action contracts, request envelopes, and deterministic decisions only.

It does not introduce screens, framework behavior, route behavior, command execution, workflow execution, raw state mutation, persistence access, autonomous action behavior, or approval/release authority.

## Supported operator-intake actions

The supported UI operator-intake actions are:

- `preview_operator_action`
- `validate_operator_action`
- `prepare_api_service_intake`

These actions are intake contracts only. They do not execute domain behavior.

## Target-boundary rule

Operator intake payloads may only target approved API/service command boundaries.

Allowed target-boundary names are:

- `api_command_intake`
- `service_command_boundary`
- `api_service_command_boundary`
- `approved_command_boundary`

Forbidden target-boundary names include:

- `raw_state_storage`
- `raw_persistence_helpers`
- `direct_state_mutation`
- `ui_direct_execution`
- `approval_release_authority`

## Validation-before-mutation rule

UI operator intake may prepare requests for downstream validation.

Mutation remains blocked at the UI boundary.

Any mutation-capable intent must be passed to an approved API/service command boundary for validation before mutation.

## Forbidden behavior

The UI operator-intake layer must not:

- execute actions directly
- mutate raw state
- create UI-originated hidden business rules
- autonomously act
- approve or release anything
- bypass API/service validation
- become validation truth
- access raw state or persistence
- introduce framework behavior

## M20.5 implementation evidence

This checkpoint adds:

- `asbp/ui/operator_intake.py`
- updates exports in `asbp/ui/__init__.py`
- `tests/test_ui_operator_intake.py`

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.5 only introduces the operator action/intake boundary.

UI safety and execution-truth separation remains in `M20.6`.
