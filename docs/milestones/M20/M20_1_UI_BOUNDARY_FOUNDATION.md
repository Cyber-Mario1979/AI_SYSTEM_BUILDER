# M20.1 — UI Boundary Foundation

## Purpose

This checkpoint establishes the first UI-layer boundary for ASBP.

The UI layer is introduced as a downstream product surface and visibility adapter over stable internal API/service boundaries. It does not create a product-ready UI, does not adopt a UI framework, and does not add screens, flows, forms, commands, or deployment behavior.

## Boundary decision

The UI package boundary is:

`asbp/ui/`

## UI role

The UI layer is a downstream product surface.

It may display governed workflow state, document/export/reporting outputs, and operator-facing error/status information through later roadmap-authorized surfaces. It must not become the owner of domain rules, validation truth, source truth, execution truth, workflow execution authority, persistence behavior, or product deployment behavior.

## Allowed dependency direction

The allowed direction is:

`ui -> api/service boundaries`

The UI layer must remain downstream from the existing governed engine and API/service layers.

## Display versus execution boundary

The UI layer may display governed information only when that information is supplied through approved API/service boundaries.

The UI layer may collect operator intent only when a later roadmap-authorized checkpoint defines the interaction or intake contract.

The UI layer must not directly execute workflow behavior, validate state truth, mutate raw state, bypass API/service validation, or become the source of execution truth.

## Forbidden access and responsibilities

The UI layer must not:

- access raw state/storage directly
- bypass approved API/service/state boundary helpers
- mutate raw state directly
- move domain logic into UI code
- move validation truth into UI code
- become source truth
- become execution truth
- create hidden workflow rules
- introduce cloud/deployment behavior
- introduce SaaS/productization behavior

## M20.1 implementation evidence

This checkpoint adds a minimal UI package skeleton:

- `asbp/ui/__init__.py`
- `asbp/ui/boundary.py`

The skeleton exposes a static boundary contract only. It does not expose screens, forms, frontend components, framework objects, network behavior, command/intake behavior, or document/report generation behavior.

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M20.1 only establishes the boundary foundation. UI interaction-flow contracts begin in `M20.2`.
