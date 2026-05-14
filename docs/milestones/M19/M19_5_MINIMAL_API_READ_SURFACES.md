# M19.5 — Minimal API Read Surfaces

## Purpose

This checkpoint introduces the first minimal read-only API surfaces.

The read surfaces expose already-governed API metadata only. They do not read persisted task, Work Package, collection, planning, document, report, AI, or workflow state.

## Scope

M19.5 defines:

- supported read-only API surface names
- deterministic read-surface normalization
- deterministic read responses using M19.2 API contracts
- fail-closed behavior for invalid or unknown read surfaces
- read-only metadata payloads for existing API boundary, contract, service-boundary, and safety policy surfaces

## Read surface module

The read surface module is:

`asbp/api/read_surface.py`

## Supported read surfaces

Supported surfaces are:

- `api_boundary`
- `api_contracts`
- `service_boundary`
- `safety_policy`

Aliases such as `boundary`, `contracts`, `service`, and `safety` normalize to the supported surface names.

## Read-only boundary

These surfaces read static governed API metadata only.

They do not:

- access raw state
- access persistence
- mutate state
- execute commands
- introduce HTTP routes
- introduce endpoint handlers
- introduce web framework behavior
- introduce UI behavior
- introduce product-ready deployment behavior

## Rejection behavior

Invalid read-surface names return:

`API_READ_SURFACE_INVALID`

Unknown read-surface names return:

`API_READ_SURFACE_UNKNOWN`

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.5 introduces minimal read-only API surfaces only. Minimal command/intake surfaces begin in `M19.6`.
