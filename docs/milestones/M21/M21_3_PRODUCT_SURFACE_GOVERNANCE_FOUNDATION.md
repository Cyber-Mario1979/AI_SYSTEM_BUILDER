# M21.3 — Product-Surface Governance Foundation

## Purpose

This checkpoint establishes deterministic product-surface governance rules for external API/UI surfaces.

The goal is to define public/consumer-facing discipline, bounded visibility discipline, and bounded command/intake discipline without introducing cloud deployment, tenant/SaaS behavior, commercial productization, or uncontrolled agentic behavior.

## Scope

M21.3 defines:

- product-surface exposure vocabulary
- product-surface capability vocabulary
- product-surface governance rules by external-surface role
- public/consumer-facing surface discipline
- bounded visibility discipline
- bounded command/intake discipline
- forbidden Phase 7 product-surface behaviors
- deterministic product-surface governance evaluation
- validation evidence for bounded governance behavior

## Implementation evidence

This checkpoint adds:

- `asbp/external_surface/governance.py`
- updated exports in `asbp/external_surface/__init__.py`
- `tests/test_external_surface_governance.py`

The implementation is static product-surface governance logic only.

It does not create API routes, UI screens, endpoints, framework behavior, command execution, raw state access, document generation, standards embedding, model/provider integration, cloud deployment, tenant/SaaS behavior, commercial productization, or uncontrolled agentic behavior.

## Product-surface exposure vocabulary

Supported exposure values:

- `internal_governed`
- `operator_facing`
- `public_consumer_facing`

## Product-surface capability vocabulary

Supported capability values:

- `visibility`
- `command_intake`
- `error_status_presentation`
- `public_contract_reference`

## Governance rules

### Downstream adapter

A downstream adapter may expose bounded public contract reference or error/status presentation only.

It must remain downstream from inner service, runtime, and domain boundaries.

It must not perform command intake.

### Product visibility surface

A product visibility surface may expose bounded visibility, error/status presentation, and public contract reference behavior.

It must remain downstream from governed engine truth.

It must not become source truth, validation truth, execution truth, or domain logic.

### Operator intake surface

An operator intake surface may collect bounded operator intent.

Command intake requires API/service validation before mutation.

It must not execute domain action directly.

### Error/status surface

An error/status surface may present bounded safe status and error information.

It must remain non-mutating.

## Forbidden authority claims

Product surfaces must reject claims of:

- source truth
- validation truth
- execution truth
- domain logic ownership
- approval authority
- release authority

## Forbidden behavior

M21.3 must reject:

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

DDR-009 remains relevant for M21 planning awareness because product-surface governance must keep future external references compatible without implementing deferred dependencies.

M21.3 does not close DDR-009.

M21.3 does not implement or close:

- governed-library runtime promotion
- consolidated runtime-authoritative libraries
- product-ready document templates
- standards source registry or citation authority
- standards embedding or retrieval index
- product-ready document/export/report generation and rendering
- actual model/provider integration
- Phase 8 or Phase 9 productization readiness

## Boundary preservation

M21.3 preserves the completed M19 API boundary.

The API layer remains a downstream adapter and does not become source truth, validation truth, execution truth, domain logic, approval authority, or release authority.

M21.3 preserves the completed M20 UI boundary.

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
- tenant/SaaS behavior
- commercial productization
- raw state mutation
- direct persistence access
- uncontrolled agentic behavior

## Validation expectation

Run:

    python -m pytest -q

## Closeout note

M21.3 establishes product-surface governance foundation only.

External-surface boundary consolidation begins in `M21.4`.
