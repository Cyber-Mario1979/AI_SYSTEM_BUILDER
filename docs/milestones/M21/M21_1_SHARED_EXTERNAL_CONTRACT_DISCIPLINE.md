# M21.1 — Shared External Contract Discipline

## Purpose

This checkpoint establishes shared external contract discipline between the completed API boundary from Milestone 19 and the completed UI boundary from Milestone 20.

The goal is to align API/UI vocabulary and external-surface rules without reopening closed M19 or M20 behavior.

## Scope

M21.1 defines:

- shared external-surface channel vocabulary
- shared external-surface role vocabulary
- shared contract field vocabulary
- shared status/result/error vocabulary alignment
- UI decision/flow/mode vocabulary visibility for external-surface consistency
- future-reference placeholder compatibility
- explicit forbidden authority claims
- explicit forbidden out-of-scope behaviors
- deterministic compatibility evaluation for external contract terms

## Implementation evidence

This checkpoint adds:

- `asbp/external_surface/__init__.py`
- `asbp/external_surface/contracts.py`
- `tests/test_external_surface_contracts.py`

The implementation is static contract discipline only.

It does not introduce API routes, UI screens, endpoint behavior, framework behavior, state mutation, document generation, standards embedding, model/provider integration, cloud deployment, or SaaS/productization behavior.

## Shared external-surface channels

Supported channels:

- `api`
- `ui`

## Shared external-surface roles

Supported roles:

- `downstream_adapter`
- `product_visibility_surface`
- `operator_intake_surface`
- `error_status_surface`

## Shared contract fields

Supported shared fields:

- `status`
- `result`
- `error`
- `payload`
- `metadata`
- `request_id`
- `operation`
- `action_name`
- `flow_name`
- `required_boundary`
- `template_id`
- `schema_id`
- `standards_bundle_ref`
- `citation_ref`
- `library_version`

## Future-reference placeholder rule

The following fields are allowed as placeholder-compatible fields only:

- `template_id`
- `schema_id`
- `standards_bundle_ref`
- `citation_ref`
- `library_version`

Their presence in the shared contract vocabulary does not close or implement deferred dependencies.

They remain compatibility placeholders for future roadmap-authorized work.

## Forbidden authority claims

External API/UI surfaces must not claim:

- source truth
- validation truth
- execution truth
- domain logic ownership
- approval authority
- release authority

## Forbidden behaviors

M21.1 must not introduce:

- raw state access
- raw persistence access
- direct storage access
- hidden domain mutation
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

DDR-009 is relevant for M21.1 planning awareness because shared external contracts should remain compatible with future library, template, standards, citation, and version references.

M21.1 does not close DDR-009.

M21.1 keeps placeholders possible without implementing:

- governed-library runtime promotion
- consolidated runtime-authoritative libraries
- product-ready document templates
- standards source registry or citation authority
- standards embedding or retrieval index
- product-ready document/export/report generation and rendering

## Boundary preservation

M21.1 preserves the completed M19 API boundary.

The API layer remains a downstream adapter and does not become source truth, validation truth, execution truth, domain logic, approval authority, or release authority.

M21.1 preserves the completed M20 UI boundary.

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

M21.1 establishes shared external contract discipline only.

UI/API consistency rules begin in `M21.2`.
