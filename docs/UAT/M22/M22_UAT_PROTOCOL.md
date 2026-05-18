# M22_UAT_PROTOCOL

## Milestone

Milestone 22 — Cloud / Compute Foundation

## Phase

Phase 8 — Cloud / Compute Layer

## UAT checkpoint

`M22.7` — Milestone UAT checkpoint

## Protocol status

Prepared for user-applied repository update.

## Purpose

This UAT protocol defines the minimal acceptance check for the M22 cloud/compute foundation boundary.

The purpose is to confirm that the M22 boundary package is understandable, bounded, non-productizing, and ready for milestone closeout consideration.

## UAT scope

This UAT covers:

- `M22.1` — Cloud / compute boundary foundation
- `M22.2` — Runtime placement model
- `M22.3` — Environment boundary model
- `M22.4` — Local / development / test / production separation
- `M22.5` — Cloud assumptions and non-assumptions register
- `M22.6` — Cloud / compute validation checkpoint

## Source evidence

The UAT reviewer should inspect:

- `docs/milestones/M22/M22_1_CLOUD_COMPUTE_BOUNDARY.md`
- `docs/milestones/M22/M22_2_RUNTIME_PLACEMENT_MODEL.md`
- `docs/milestones/M22/M22_3_ENVIRONMENT_BOUNDARY_MODEL.md`
- `docs/milestones/M22/M22_4_ENVIRONMENT_SEPARATION.md`
- `docs/milestones/M22/M22_5_CLOUD_ASSUMPTIONS_REGISTER.md`
- `docs/milestones/M22/M22_6_CLOUD_COMPUTE_VALIDATION_CHECKPOINT.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`

## Supporting validation evidence

Supporting validation checkpoint:

`docs/milestones/M22/M22_6_CLOUD_COMPUTE_VALIDATION_CHECKPOINT.md`

Recorded validation result:

`python -m pytest -q` — `1072 passed in 48.85s`

## Acceptance criteria

| ID | Acceptance criterion | Expected result |
|---|---|---|
| UAT-M22-001 | Cloud/compute is understandable as a downstream boundary. | Pass |
| UAT-M22-002 | Runtime placement is clearly separated from deployment implementation. | Pass |
| UAT-M22-003 | Environment roles and boundaries are understandable. | Pass |
| UAT-M22-004 | Local/development/test/production separation is clear. | Pass |
| UAT-M22-005 | Non-production validation evidence limits are clear. | Pass |
| UAT-M22-006 | Cloud assumptions and non-assumptions prevent premature provider or hosting commitment. | Pass |
| UAT-M22-007 | Deferred decisions remain explicit. | Pass |
| UAT-M22-008 | Deferred dependency alignment is present without replacing the deferred dependency register. | Pass |
| UAT-M22-009 | No production readiness, deployment, SaaS, productization, standards, model/provider, or product-ready generation capability is claimed. | Pass |
| UAT-M22-010 | The M22 boundary is understandable, bounded, and non-productizing. | Pass |

## UAT method

The reviewer should perform a document review and confirm each acceptance criterion.

No executable test is required for UAT beyond the supporting M22.6 validation evidence.

## Not allowed during this UAT

This UAT must not introduce:

- new cloud/compute features
- deployment implementation
- Phase 9 work
- milestone closeout before UAT evidence exists
- production readiness claims
- SaaS/productization claims
- live model/provider calls
- standards embedding
- product-ready document/export/report generation

## UAT decision options

Allowed UAT decisions:

- `Pass`
- `Conditional pass`
- `Fail`

## Planned evidence output

The UAT result is recorded in:

`docs/UAT/M22/M22_UAT_REPORT.md`

## Generation note

Generated as a user-applied local UAT protocol package.

Live repository write: `NO`.
