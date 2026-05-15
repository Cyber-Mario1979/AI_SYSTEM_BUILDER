# M21.7 — Phase 7 UAT Protocol

## Purpose

This protocol defines the minimal UAT coverage for Phase 7 external-surface governance under Milestone 21.

The UAT confirms that the external API/UI surfaces introduced and governed across `M21.1` through `M21.6` are understandable, bounded, safe, and downstream from stable inner layers.

## UAT scope

The UAT scope covers:

- `M21.1` — Shared external contract discipline
- `M21.2` — UI/API consistency rules
- `M21.3` — Product-surface governance foundation
- `M21.4` — External-surface boundary consolidation
- `M21.5` — Validation and acceptance discipline for external surfaces
- `M21.6` — Phase 7 validation checkpoint

The UAT also considers the completed upstream Phase 7 boundaries:

- `M19` — API Boundary Introduction
- `M20` — UI Layer Introduction

## Evidence sources

The following evidence sources are in scope for review:

- `docs/milestones/M21/M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE.md`
- `docs/milestones/M21/M21_2_UI_API_CONSISTENCY_RULES.md`
- `docs/milestones/M21/M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION.md`
- `docs/milestones/M21/M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION.md`
- `docs/milestones/M21/M21_5_VALIDATION_AND_ACCEPTANCE_DISCIPLINE.md`
- `docs/milestones/M21/M21_6_PHASE_7_VALIDATION_CHECKPOINT.md`
- `asbp/external_surface/contracts.py`
- `asbp/external_surface/consistency.py`
- `asbp/external_surface/governance.py`
- `asbp/external_surface/boundary.py`
- `asbp/external_surface/acceptance.py`
- `tests/test_external_surface_contracts.py`
- `tests/test_external_surface_consistency.py`
- `tests/test_external_surface_governance.py`
- `tests/test_external_surface_boundary.py`
- `tests/test_external_surface_acceptance.py`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`

## UAT objectives

| ID | Objective | Expected result |
|---|---|---|
| UAT-M21-001 | Confirm the external-surface role is understandable. | API/UI external surfaces are described as downstream adapter/product surfaces, not inner-layer authority. |
| UAT-M21-002 | Confirm external contract discipline is bounded. | Shared external contract vocabulary is deterministic and does not create routes, screens, deployment, or productization behavior. |
| UAT-M21-003 | Confirm UI/API consistency is understandable. | UI-visible state remains aligned with API response outcomes and governed engine truth. |
| UAT-M21-004 | Confirm product-surface governance is safe. | Public/consumer-facing, visibility, command/intake, and error/status surfaces remain bounded and non-authoritative. |
| UAT-M21-005 | Confirm command/intake discipline is bounded. | Command/intake behavior requires API/service validation before mutation and does not execute domain actions directly. |
| UAT-M21-006 | Confirm boundary consolidation is coherent. | External-surface boundary evidence consolidates M21.1 through M21.3 without behavior expansion. |
| UAT-M21-007 | Confirm validation and acceptance discipline is ready. | Required validation/UAT evidence expectations are explicit before Phase 7 closeout. |
| UAT-M21-008 | Confirm no Phase 8/productization leakage. | M21 does not introduce cloud/deployment, SaaS, model/provider integration, standards embedding, or product-ready document/report/export generation. |
| UAT-M21-009 | Confirm deferred dependencies remain visible. | Open/deferred/watch DDR items remain carried forward and are not closed by M21 UAT. |

## Acceptance criteria

M21 UAT may pass only if:

- external API/UI surfaces are understandable as bounded downstream surfaces
- shared external contract behavior is deterministic
- UI/API visible state cannot diverge from governed engine truth
- product-surface governance rejects hidden authority, hidden domain logic, uncontrolled agentic behavior, cloud/deployment, tenant/SaaS, and commercial productization behavior
- boundary consolidation does not expand behavior
- M21.6 validation evidence exists and records a passing validation result
- UAT evidence records an acceptance decision and rationale
- no deferred dependency is incorrectly closed
- no Phase 8, cloud/deployment, SaaS, or productization assumption is introduced

## Out of scope

This UAT does not cover:

- live API routes
- endpoint handlers
- UI screens
- UI framework behavior
- production deployment
- cloud/compute behavior
- SaaS/productization behavior
- tenant behavior
- live model/provider integration
- standards embedding
- standards-backed citation output
- document/report/export generation
- approval or release authority
- raw state mutation
- direct persistence access

## Execution method

The UAT is document-and-evidence based.

The operator reviews the scoped evidence and records the acceptance decision in:

`docs/UAT/M21/M21_UAT_REPORT.md`

## Closeout dependency

M21.8 Phase 7 closeout must not proceed until the M21 UAT report exists and records an acceptance decision.
