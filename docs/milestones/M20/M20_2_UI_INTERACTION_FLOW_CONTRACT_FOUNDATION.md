# M20.2 — UI Interaction-Flow Contract Foundation

## Purpose

This checkpoint establishes deterministic UI interaction-flow contracts for ASBP.

The UI layer remains a downstream product surface over approved API/service boundaries. This checkpoint does not introduce screens, frontend framework behavior, routes, endpoint behavior, command execution, raw state access, cloud behavior, or SaaS/productization behavior.

## Boundary decision

The UI interaction-flow contract module is:

`asbp/ui/interaction_flow.py`

## Interaction-flow families

M20.2 defines these initial interaction-flow families:

- `workflow_visibility`
- `document_output_visibility`
- `operator_command_intake`
- `error_status_presentation`

These families are contract definitions only. They do not implement product screens or execution workflows.

## Display-only versus command-capable behavior

Display-only flows may present governed state, output status, or error/status information without mutation.

Command-capable flows may collect operator intent and prepare command/intake envelopes, but they must not execute domain actions directly. Command-capable intake requires API/service validation before any mutation can occur.

## User action/intake contract expectations

The checkpoint adds a stable UI action/intake request envelope that records:

- flow name
- requested interaction mode
- action name
- payload
- metadata

The request envelope is deterministic and rejects invalid contract shapes.

## Error and invalid-state presentation expectations

Invalid or stale UI states must be presented as blocked or rejected states.

The UI layer must not silently correct, retry, mutate, or bypass validation when invalid state is detected.

## Forbidden behavior

The UI layer must not:

- move domain logic into UI code
- move validation truth into UI code
- introduce UI-only hidden workflow rules
- bypass API/service validation
- mutate raw state directly
- access raw state/storage/persistence directly
- introduce screens, routes, frameworks, cloud behavior, or SaaS/productization behavior in this checkpoint

## M20.2 implementation evidence

This checkpoint adds:

- `asbp/ui/interaction_flow.py`
- updated exports in `asbp/ui/__init__.py`
- `tests/test_ui_interaction_flow.py`

The implementation is static contract logic only. It does not create UI screens or product runtime behavior.

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.2 only establishes the interaction-flow contract foundation. Governed workflow visibility surfaces begin in `M20.3`.
