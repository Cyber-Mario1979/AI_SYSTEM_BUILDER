# M20.6 — UI Safety and Execution-Truth Separation

## Purpose

This checkpoint introduces cross-cutting UI safety and execution-truth separation rules.

The UI layer may display governed state, output, and intake decisions, but it must not become source truth, validation truth, execution truth, or bypass approved API/service boundaries.

## Boundary decision

The UI safety module is:

`asbp/ui/safety.py`

The module defines safety contracts, evaluation requests, and deterministic safety decisions only.

It does not introduce new UI features, screens, framework behavior, workflow execution, command execution, raw state access, persistence access, source-truth ownership, validation-truth ownership, or execution-truth ownership.

## Supported safety checks

The supported UI safety checks are:

- `source_truth_claim`
- `validation_truth_claim`
- `execution_truth_claim`
- `api_service_boundary_bypass`
- `stale_ui_state`
- `invalid_ui_state`
- `silent_mutation_attempt`

## Safety context-boundary rule

UI safety evaluation may only use approved context boundaries.

Allowed context-boundary names are:

- `api_service_boundary`
- `api_read_surface`
- `service_read_surface`
- `approved_ui_boundary`

Forbidden context-boundary names include:

- `raw_state_storage`
- `raw_persistence_helpers`
- `direct_state_mutation`
- `ui_source_truth`
- `ui_validation_truth`
- `ui_execution_truth`
- `api_service_boundary_bypass`

## No-guess behavior

Invalid, stale, or unknown UI state must fail closed.

The UI must present the state as blocked, unknown, invalid, or requiring API/service refresh. It must not guess, silently correct, mutate, execute, or treat display state as truth.

## Forbidden behavior

The UI safety layer must reject:

- UI source-truth claims
- UI validation-truth claims
- UI execution-truth claims
- API/service boundary bypass
- silent/direct mutation attempts
- execution from stale or invalid state
- validation truth from UI display
- raw state or persistence access

## M20.6 implementation evidence

This checkpoint adds:

- `asbp/ui/safety.py`
- updates exports in `asbp/ui/__init__.py`
- `tests/test_ui_safety.py`

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.6 closes the implementation checkpoint family before M20 validation.

M20.7 is the UI validation checkpoint.
