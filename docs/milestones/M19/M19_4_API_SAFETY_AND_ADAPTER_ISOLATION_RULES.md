# M19.4 — API Safety and Adapter Isolation Rules

## Purpose

This checkpoint defines fail-closed API safety behavior before minimal read or command/intake surfaces are introduced.

The API layer remains an adapter. It may validate boundary-safe intake categories, but it must not execute commands, mutate state, own domain logic, introduce route handlers, or become a source of validation truth.

## Scope

M19.4 defines:

- API adapter isolation vocabulary
- deterministic API intake safety decisions
- safe intake action categories
- unsafe intake action categories
- fail-closed rejection behavior for unknown, invalid, command-like, and mutation-like actions
- deterministic success/error responses using the M19.2 API contract layer

## Safety module

The safety module is:

`asbp/api/safety.py`

## Safe action categories

Currently safe categories are:

- `read_only`
- `contract_validation`

These categories only represent safety classification. They do not implement read surfaces, endpoints, routes, or command execution.

## Unsafe action categories

Currently unsafe categories are:

- `state_changing`
- `command`

Mutation-like aliases such as `create`, `update`, `delete`, `write`, and `mutation` normalize to `state_changing` and fail closed.

Command-like aliases such as `command` and `execute` normalize to `command` and fail closed.

## Fail-closed behavior

Invalid intake actions return:

`API_SAFETY_INVALID_ACTION`

Known unsafe intake actions return:

`API_SAFETY_UNSAFE_ACTION`

Unknown intake actions return:

`API_SAFETY_UNKNOWN_ACTION`

## Explicit non-goals

This checkpoint does not introduce:

- authentication/authorization production design
- external network deployment assumptions
- cloud runtime assumptions
- UI behavior
- HTTP routes
- endpoint handlers
- command execution
- state mutation
- raw persistence access
- service/domain logic relocation into API safety code
- AI/provider behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.4 establishes API safety and adapter isolation rules only. Minimal read surfaces begin in `M19.5`.
