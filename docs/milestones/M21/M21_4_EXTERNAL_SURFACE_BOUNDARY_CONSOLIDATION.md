# M21.4 — External-Surface Boundary Consolidation

## Purpose

This checkpoint consolidates the external-surface boundary created across M21.1, M21.2, and M21.3.

The goal is to reduce avoidable duplication inside external-surface helpers, align validation and failure behavior across external surfaces, and preserve all inner-layer authority boundaries.

## Scope

M21.4 performs bounded consolidation only inside `asbp/external_surface/`.

It consolidates:

- shared normalization helper logic
- external contract discipline boundary visibility
- UI/API consistency boundary visibility
- product-surface governance boundary visibility
- forbidden authority claims
- forbidden out-of-scope behaviors
- validation and failure alignment expectations
- explicit non-goals for the external-surface layer

## Implementation evidence

This checkpoint adds:

- `asbp/external_surface/_normalization.py`
- `asbp/external_surface/boundary.py`
- `tests/test_external_surface_boundary.py`

This checkpoint updates:

- `asbp/external_surface/__init__.py`
- `asbp/external_surface/contracts.py`
- `asbp/external_surface/consistency.py`
- `asbp/external_surface/governance.py`

The implementation remains static boundary and helper logic only.

It does not create API routes, UI screens, endpoints, framework behavior, command execution, raw state access, document generation, standards embedding, model/provider integration, cloud deployment, tenant/SaaS behavior, commercial productization, or uncontrolled agentic behavior.

## Consolidated helper rule

Repeated local token and label normalization helpers were consolidated into:

`asbp/external_surface/_normalization.py`

This helper is internal to the external-surface package.

It is not exported as public API from `asbp.external_surface`.

## Consolidated boundary rule

The consolidated external-surface boundary contract is exposed through:

`asbp/external_surface/boundary.py`

It records:

- external-surface package boundary
- discipline modules
- preserved authority boundaries
- forbidden authority claims
- consolidated forbidden behaviors
- validation and failure alignment
- explicit non-goals

## Preserved authority boundaries

M21.4 preserves:

- governed engine truth
- service/runtime/domain boundaries
- API/service validation before mutation
- UI and API as downstream adapters
- external surface is not source truth
- external surface is not validation truth
- external surface is not execution truth

## Validation and failure alignment

M21.4 aligns external-surface failure behavior around:

- fail closed for unsupported terms
- preserve API error/rejection visibility
- preserve UI/API consistency with governed truth
- preserve command-intake validation boundary
- preserve product-surface governance boundary

## Forbidden authority claims

External surfaces must continue to reject claims of:

- source truth
- validation truth
- execution truth
- domain logic ownership
- approval authority
- release authority

## Forbidden behavior

M21.4 must not introduce:

- raw state access
- raw persistence access
- direct storage access
- hidden domain mutation
- UI/API source-truth ownership
- UI/API hidden domain logic
- service-boundary bypass
- governed-truth override
- silent status translation
- document generation
- report generation
- export generation
- standards embedding
- standards citation authority
- model/provider integration
- cloud deployment
- cloud deployment implementation
- tenant/SaaS behavior
- commercial productization
- uncontrolled agentic behavior
- autonomous action execution
- approval/release expansion
- production endpoint behavior
- production UI screen behavior

## Deferred dependency impact

DDR-009 remains relevant for M21 planning awareness because external contracts must remain compatible with future library, template, standards, citation, and version references.

M21.4 does not close DDR-009.

M21.4 does not implement or close:

- governed-library runtime promotion
- consolidated runtime-authoritative libraries
- product-ready document templates
- standards source registry or citation authority
- standards embedding or retrieval index
- product-ready document/export/report generation and rendering
- actual model/provider integration
- Phase 8 or Phase 9 productization readiness

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
- tenant/SaaS behavior
- commercial productization
- raw state mutation
- direct persistence access
- uncontrolled agentic behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M21.4 consolidates the external-surface boundary only.

Validation and acceptance discipline for external surfaces begins in `M21.5`.
