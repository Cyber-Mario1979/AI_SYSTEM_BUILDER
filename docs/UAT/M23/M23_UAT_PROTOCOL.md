# M23_UAT_PROTOCOL

## Milestone

Milestone 23 — Deployment / Packaging / Configuration Boundary

## Phase

Phase 8 — Cloud / Compute Layer

## Checkpoint

`M23.7` — Milestone UAT checkpoint

## Protocol status

Prepared for user-applied repository update.

This protocol defines the minimal UAT review for M23.

It does not introduce new deployment features, production release behavior, Phase 9 work, productization behavior, standards embedding, live model/provider calls, or product-ready document/report/export generation.

## UAT purpose

The purpose of this UAT is to confirm that the M23 deployment, packaging, configuration, artifact, and governed-source boundaries are understandable, bounded, and non-productizing.

This UAT is acceptance evidence for the milestone boundary.

It is not implementation evidence for deployment, packaging automation, configuration loading, artifact generation, or productized runtime behavior.

## UAT scope

The UAT scope covers review of:

- `docs/milestones/M23/M23_1_DEPLOYMENT_BOUNDARY_FOUNDATION.md`
- `docs/milestones/M23/M23_2_PACKAGING_STRATEGY_FOUNDATION.md`
- `docs/milestones/M23/M23_3_CONFIGURATION_BOUNDARY_MODEL.md`
- `docs/milestones/M23/M23_4_ARTIFACT_BOUNDARY_MODEL.md`
- `docs/milestones/M23/M23_5_GOVERNED_SOURCE_ASSETS_VS_DEPLOYABLE_OPERATIONAL_SURFACES.md`
- `docs/milestones/M23/M23_6_DEPLOYMENT_PACKAGING_VALIDATION_CHECKPOINT.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`

## Acceptance criteria

M23 UAT passes when all criteria below are satisfied:

1. The deployment boundary is understandable and clearly downstream from stable system boundaries.
2. Packaging strategy is understandable and separates source packages from deployable packages.
3. Configuration boundaries are understandable and preserve code/configuration separation.
4. No-secret-in-source expectations are explicit.
5. Artifact families and runtime-authority limits are understandable.
6. Governed source assets are clearly separated from deployable operational surfaces.
7. `DDR-001` and `DDR-002` are explicitly carried forward without closure.
8. M23 does not claim runtime-authoritative library promotion or deployment-compiled lookup.
9. M23 does not claim production deployment, production release behavior, SaaS/productization behavior, or Phase 9 work.
10. M23.6 validation evidence exists and records a passing validation result.
11. The next checkpoint remains milestone closeout after UAT acceptance.

## Operator-facing review checklist

| Item | Expected answer |
|---|---|
| Is the M23 deployment boundary understandable? | Yes |
| Is deployment clearly downstream from stable package/runtime/service/API boundaries? | Yes |
| Is packaging clearly separated from release packaging and commercial distribution? | Yes |
| Is configuration clearly separated from code and domain logic? | Yes |
| Are secrets prohibited from source? | Yes |
| Are source, generated, operational, evidence, test, temporary, archive, and product artifacts distinguishable? | Yes |
| Are evidence artifacts preserved without becoming runtime authority? | Yes |
| Are governed source assets separated from deployable operational surfaces? | Yes |
| Are `DDR-001` and `DDR-002` carried forward without closure? | Yes |
| Is M23 non-productizing? | Yes |

## Not-allowed behavior checklist

The reviewer must confirm that M23 UAT does not accept or introduce:

- new deployment features
- production release behavior
- Phase 9 work
- milestone closeout before UAT evidence
- production deployment
- provider-specific production infrastructure
- tenant/SaaS implementation
- commercial productization
- live model/provider integration
- standards embedding
- product-ready document/report/export generation
- runtime-authoritative library promotion
- deployment-compiled lookup implementation
- closing `DDR-001` or `DDR-002` without evidence

## Deferred dependency carry-forward check

M23 UAT must confirm:

- `DDR-001` remains deferred.
- `DDR-002` remains deferred.
- `DDR-003` remains deferred.
- `DDR-004` remains open and Critical.
- `DDR-005` remains deferred and dependent on `DDR-004`.
- `DDR-006` remains deferred.
- `DDR-007` remains watch.
- `DDR-008` remains watch.
- `DDR-009` remains watch/planning-awareness.

No deferred dependency is closed by M23.7.

## Required evidence for UAT completion

UAT completion requires:

- this protocol
- a completed UAT report under `docs/UAT/M23/M23_UAT_REPORT.md`
- acceptance decision
- rationale
- tracker update to `M23.8` after acceptance

## Protocol decision

Protocol decision: ready for UAT report.

## Generation note

Generated as a user-applied local documentation package.

Live repository write: `NO`.
