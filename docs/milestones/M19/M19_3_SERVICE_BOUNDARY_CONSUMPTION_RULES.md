# M19.3 — Service-Boundary Consumption Rules

## Purpose

This checkpoint defines how the API layer may consume existing service/runtime/core boundaries.

The API layer remains a downstream adapter. It may depend on approved internal boundaries, but it must not access raw state, raw persistence, or direct storage targets.

## Scope

M19.3 defines:

- approved API dependency targets
- forbidden API dependency targets
- deterministic dependency-target normalization
- deterministic dependency-target approval/rejection
- API contract responses for approval/rejection decisions

## Contract module

The service-boundary module is:

`asbp/api/service_boundary.py`

## Approved dependency targets

Approved targets are:

- `service`
- `runtime`
- `core`

These represent approved service/runtime/core boundaries only. They do not authorize raw state access or direct persistence access.

## Forbidden dependency targets

Forbidden targets are:

- `raw_state`
- `raw_persistence`
- `direct_storage`

These targets must be rejected before API adapters are allowed to consume them.

## Rejection behavior

Rejected dependency targets use deterministic M19.2 API error responses.

Known forbidden targets return:

`API_BOUNDARY_FORBIDDEN_TARGET`

Unknown or unapproved targets return:

`API_BOUNDARY_UNKNOWN_TARGET`

## Explicit non-goals

This checkpoint does not introduce:

- HTTP routes
- endpoint handlers
- FastAPI, Flask, Django, or other web framework adoption
- command execution
- state mutation
- domain rule duplication
- raw persistence access
- UI behavior
- cloud/deployment behavior
- authentication/authorization behavior
- AI/provider behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.3 establishes service-boundary consumption rules only. API safety and adapter isolation rules continue in `M19.4`.
