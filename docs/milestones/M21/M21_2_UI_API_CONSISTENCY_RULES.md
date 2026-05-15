# M21.2 — UI/API Consistency Rules

## Purpose

This checkpoint establishes deterministic consistency rules between UI-visible state and API response outcomes.

The goal is to prevent API/UI divergence from governed engine truth while preserving the completed M19 API boundary and completed M20 UI boundary.

## Scope

M21.2 defines:

- API response outcome to UI-visible state consistency rules
- allowed operator-visible states for API success/accepted outcomes
- allowed operator-visible states for API error/rejected outcomes
- forbidden UI/API divergence states
- governed-truth reference requirement for operator-visible state
- rejection of UI/API source-truth, validation-truth, execution-truth, and domain-logic claims
- rejection of UI/API-specific hidden domain behavior
- rejection of service-boundary bypass behavior
- validation evidence for consistency behavior

## Implementation evidence

This checkpoint adds:

- `asbp/external_surface/consistency.py`
- updated exports in `asbp/external_surface/__init__.py`
- `tests/test_external_surface_consistency.py`

The implementation is static consistency-rule logic only.

It does not create API routes, UI screens, endpoints, framework behavior, command execution, raw state access, document generation, standards embedding, model/provider integration, cloud deployment, or SaaS/productization behavior.

## Consistency rules

### API success / accepted

An API response outcome of:

- `status = success`
- `result = accepted`

may be presented by the UI as:

- accepted
- display-only
- validation required

It must not be presented as:

- rejected
- error visible
- blocked

### API error / rejected

An API response outcome of:

- `status = error`
- `result = rejected`

may be presented by the UI as:

- rejected
- error visible
- blocked

It must not be presented as:

- accepted
- validation required

A UI display request may be accepted for display while still showing the API rejection/error outcome. This does not convert the API error into success.

## Governed-truth reference rule

Operator-visible state must remain tied to governed engine truth.

UI/API consistency checks must not allow the UI or API layer to invent state truth, validation truth, execution truth, or domain authority.

## Forbidden authority claims

UI/API consistency must reject external-surface claims of:

- source truth
- validation truth
- execution truth
- domain logic ownership
- approval authority
- release authority

## Forbidden behavior

M21.2 must reject:

- raw state access
- raw persistence access
- direct storage access
- hidden domain mutation
- UI/API hidden domain logic
- service-boundary bypass
- governed-truth override
- silent status translation
- UI/API source-truth ownership
- document generation
- report generation
- export generation
- standards embedding
- standards citation authority
- model/provider integration
- cloud deployment
- SaaS/productization behavior

## Deferred dependency impact

DDR-009 remains relevant for M21 planning awareness because M21 external contracts must remain compatible with future library, template, standards, citation, and version references.

M21.2 does not close DDR-009.

M21.2 does not implement or close:

- governed-library runtime promotion
- consolidated runtime-authoritative libraries
- product-ready document templates
- standards source registry or citation authority
- standards embedding or retrieval index
- product-ready document/export/report generation and rendering

## Boundary preservation

M21.2 preserves the completed M19 API boundary.

The API layer remains a downstream adapter and does not become source truth, validation truth, execution truth, domain logic, approval authority, or release authority.

M21.2 preserves the completed M20 UI boundary.

The UI layer remains a downstream product surface and visibility/intake adapter. It does not become source truth, validation truth, execution truth, domain logic, approval authority, or release authority.

## Explicit non-goals

This checkpoint does not introduce:

- HTTP routes
- endpoint handlers
- API framework adoption
- UI screens
- UI framework adoption
- command execution
- workflow orchestration expansion
- document generation
- report generation
- export generation
- standards embedding
- standards-backed citation output
- model/provider integration
- cloud deployment
- SaaS/productization behavior
- raw state mutation
- direct persistence access

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M21.2 establishes UI/API consistency rules only.

Product-surface governance foundation begins in `M21.3`.
