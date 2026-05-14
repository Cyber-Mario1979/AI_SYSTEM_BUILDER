# M19.1 — API Boundary Foundation

## Purpose

This checkpoint establishes the first API-layer boundary for ASBP.

The API layer is introduced as a downstream adapter over stable internal service/runtime/core boundaries. It does not create a product-ready API, does not adopt a web framework, and does not add routes or endpoints.

## Boundary decision

The API package boundary is:

`asbp/api/`

## API role

The API layer is an adapter only.

It may expose governed internal behavior through explicit request/response contracts in later M19 checkpoints, but it must not become the owner of domain rules, validation truth, source truth, workflow execution authority, persistence behavior, or AI/provider behavior.

## Allowed dependency direction

The allowed direction is:

`api -> approved service/runtime/core boundaries`

The API layer must remain downstream from the existing governed engine layers.

## Forbidden access and responsibilities

The API layer must not:

- access raw state/storage directly
- bypass approved persistence/state boundary helpers
- mutate raw state directly
- move domain logic into API code
- move validation truth into API code
- become source truth
- introduce UI behavior
- introduce cloud/deployment behavior
- call AI/provider services directly
- implement authentication/authorization beyond later roadmap-authorized placeholder direction

## M19.1 implementation evidence

This checkpoint adds a minimal API package skeleton:

- `asbp/api/__init__.py`
- `asbp/api/boundary.py`

The skeleton exposes a static boundary contract only. It does not expose routes, endpoints, framework objects, network behavior, or command/intake behavior.

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M19.1 only establishes the boundary foundation. Request/response contracts begin in `M19.2`.
