# M19.6 — Minimal API Command/Intake Surfaces

## Purpose

This checkpoint introduces minimal API command/intake surfaces without introducing real endpoint behavior, broad workflow orchestration, raw state mutation, AI provider calls, document/report generation, approval/release authority, UI behavior, or cloud/deployment behavior.

The checkpoint creates a deterministic intake gate for command-like API requests.

## Scope

M19.6 defines:

- supported command/intake vocabulary
- deterministic command/intake request shape
- deterministic command/intake decision shape
- deterministic command normalization
- supported command rejection
- target-boundary validation through M19.3 service-boundary rules
- safety validation through M19.4 API safety rules
- success responses for validated intake/preview only
- fail-closed behavior for unsupported commands, forbidden targets, unknown targets, and direct execution requests

## Command/intake module

The command/intake module is:

`asbp/api/command_intake.py`

## Supported commands

Supported commands are:

- `preview_command`
- `validate_contract`

Aliases such as `preview`, `command_preview`, `validate`, and `contract_validation` normalize to the supported command names.

## Execution boundary

M19.6 does not execute commands.

Successful intake means:

- the command name is supported
- the target is an approved API dependency target
- the intake remains safety-valid
- the response is accepted as preview/validation only
- `execution_allowed` remains `False`

Direct execution requests fail closed through the existing M19.4 safety rules.

## Approved targets

Approved dependency targets remain inherited from M19.3:

- `service`
- `runtime`
- `core`

Forbidden targets remain rejected:

- `raw_state`
- `raw_persistence`
- `direct_storage`

## Observable behavior evidence

The tests for this checkpoint include user-flow-style behavior assertions:

- valid preview intake returns a deterministic accepted response
- valid contract-validation intake returns a deterministic accepted response
- unsupported command names fail closed
- direct execution requests fail closed
- raw state / persistence / storage targets fail closed
- unknown targets fail closed
- payload mutation after response conversion does not alter subsequent responses
- no raw persistence/state modules are imported
- no route/framework/UI/cloud/AI behavior is introduced

## Explicit non-goals

This checkpoint does not introduce:

- HTTP routes
- endpoint handlers
- FastAPI, Flask, Django, or other framework adoption
- raw state mutation
- direct persistence access
- broad workflow orchestration
- new domain behavior unrelated to API boundary introduction
- AI provider calls
- document/report generation expansion
- approval/release authority expansion
- UI behavior
- cloud/deployment behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.6 completes minimal API command/intake foundation only. M19.7 is the API validation checkpoint.
