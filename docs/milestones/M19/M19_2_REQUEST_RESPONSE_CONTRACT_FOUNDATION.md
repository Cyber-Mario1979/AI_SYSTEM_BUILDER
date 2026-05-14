# M19.2 — Request/Response Contract Foundation

## Purpose

This checkpoint establishes deterministic API request and response contract shapes before any endpoint, route, framework, UI, deployment, or command/intake behavior is introduced.

## Scope

M19.2 defines:

- stable request envelope
- stable response envelope
- common error envelope
- stable status vocabulary
- stable result vocabulary
- deterministic success and error response builders
- contract serialization through explicit `to_dict()` methods

## Contract module

The contract module is:

`asbp/api/contracts.py`

## Request contract

`ApiRequest` defines:

- `operation`
- `payload`
- `metadata`

The operation must be a non-empty string. Payload and metadata must be mapping values.

## Response contract

`ApiResponse` defines:

- `status`
- `result`
- `payload`
- `error`
- `metadata`

Success responses must not include errors.

Error responses must include an error envelope.

## Error contract

`ApiError` defines:

- `code`
- `message`
- `details`

Code and message must be non-empty strings.

## Stable vocabulary

Status values:

- `success`
- `error`

Result values:

- `accepted`
- `rejected`

Unsupported values are rejected by the enum-backed contract constructors.

## Explicit non-goals

This checkpoint does not introduce:

- HTTP routes
- endpoint handlers
- FastAPI, Flask, Django, or other web framework adoption
- public endpoint behavior
- persistence access
- state mutation
- domain operation execution
- UI behavior
- cloud/deployment behavior
- authentication/authorization behavior
- AI/provider behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.2 establishes contract determinism only. Service-boundary consumption rules begin in `M19.3`.
