# M23_5_GOVERNED_SOURCE_ASSETS_VS_DEPLOYABLE_OPERATIONAL_SURFACES

## Milestone

Milestone 23 — Deployment / Packaging / Configuration Boundary

## Phase

Phase 8 — Cloud / Compute Layer

## Checkpoint

`M23.5` — Governed source assets vs deployable operational surfaces

## Checkpoint status

Prepared for user-applied repository update.

This document is boundary evidence for `M23.5`.

It does not implement runtime-authoritative library promotion, deployment-compiled lookup, governed-library consolidation, operational release packaging, product-ready downloadable packages, commercial distribution assets, standards embedding, live model/provider calls, or product-ready document/report/export generation.

## Source basis

This checkpoint evidence is based on:

- `ROADMAP_CANONICAL.md` v4
- `ROADMAP_ADDENDUM_09_PHASE_8_DETAILED_CHECKPOINT_LADDER.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/milestones/M23/M23_1_DEPLOYMENT_BOUNDARY_FOUNDATION.md`
- `docs/milestones/M23/M23_2_PACKAGING_STRATEGY_FOUNDATION.md`
- `docs/milestones/M23/M23_3_CONFIGURATION_BOUNDARY_MODEL.md`
- `docs/milestones/M23/M23_4_ARTIFACT_BOUNDARY_MODEL.md`

## Purpose

The purpose of `M23.5` is to define the separation between governed source assets and deployable operational surfaces before deployment validation begins.

Governed source assets may exist in the repository for governance, planning, evidence, templates, libraries, or traceability.

Deployable operational surfaces may later consume only authorized runtime surfaces and approved operational assets.

Repository presence does not make a governed source asset runtime-authoritative.

Packaging or deployment must not promote draft, evidence, planning, or governed library assets into runtime authority without a separately authorized promotion or compilation path.

## Relationship to M23.1 through M23.4

M23.1 defined deployment/package/configuration surfaces as downstream operational surfaces.

M23.2 defined source package versus deployable package boundaries.

M23.3 defined configuration boundary rules and no-secret-in-source expectations.

M23.4 defined artifact families, traceability, validation expectations, and runtime-authority limits.

M23.5 builds on these boundaries by defining which governed source assets must remain non-runtime unless promoted or compiled through a future authorized path.

M23.5 does not reopen M23.1, M23.2, M23.3, or M23.4.

M23.5 does not promote any governed source asset into runtime authority.

M23.5 does not implement deployment-compiled lookup.

## Governed source asset definition

A governed source asset is a repository-controlled file, record, mapping, library, template, register, source bundle, evidence record, or governance artifact with an explicit source role.

Governed source assets may support planning, traceability, future source resolution, documentation, validation, UAT, boundary evidence, or design governance.

A governed source asset may be authoritative for its own declared source role.

A governed source asset is not automatically authoritative for runtime execution, deployment behavior, operational lookup, product generation, or product-ready output.

## Deployable operational surface definition

A deployable operational surface is a future runtime-facing, deployment-facing, package-facing, configuration-facing, or operational-facing surface that may be included in a deployable package or used by an operational environment.

Deployable operational surfaces must depend only on approved runtime, service, package, configuration, resolver, or adapter boundaries.

Deployable operational surfaces must not depend on draft, scattered, archived, evidence-only, planning-only, or unpromoted governed source assets as if those assets were runtime authority.

M23.5 defines this separation only.

It does not create deployable operational surfaces.

## Separation rules

The following separation rules apply:

1. Repository presence does not imply runtime authority.
2. Source authority does not imply deployment authority.
3. Evidence authority does not imply runtime authority.
4. Governance authority does not imply operational package inclusion.
5. Draft library presence does not imply deployment-compiled lookup.
6. Template presence does not imply product-ready generation.
7. Standards-related artifact presence does not imply standards citation authority.
8. Generated artifact presence does not imply product-ready output.
9. Deployable surfaces must consume only promoted, compiled, or otherwise authorized operational representations.
10. Runtime authority requires explicit roadmap authorization, implementation evidence, validation evidence, and deferred-dependency disposition when relevant.

## Source assets that must not become runtime authority by presence alone

The following asset families must not be treated as runtime authority merely because they are present in the repository:

- governed library drafts
- task pool drafts
- preset definitions
- selector mappings
- profile records
- calendar records
- planning basis records
- standards bundle records
- document templates
- schema drafts
- generated documents
- generated reports
- generated exports
- validation evidence
- UAT evidence
- milestone evidence
- roadmap addenda
- deferred dependency rows
- archived materials
- local helper scripts
- temporary apply scripts
- source examples or samples

Any later runtime use requires explicit authorization and evidence.

## Promotion and compilation gate concept

A promotion or compilation gate is a future authorized path that may turn a governed source asset into a runtime-authoritative operational representation.

A valid future promotion or compilation gate should define:

- eligible source asset family
- source role before promotion
- operational role after promotion
- transformation or compilation rules
- validation expectations
- version/status model
- traceability back to the source asset
- failure behavior
- rollback or invalidation expectations
- dependency closure or reclassification evidence
- UAT/acceptance evidence when applicable

M23.5 defines the gate concept only.

It does not implement any promotion or compilation path.

## DDR-001 impact

`DDR-001` remains deferred for governed-library runtime promotion / deployment-compiled lookup.

M23.5 does not close `DDR-001`.

M23.5 does not implement governed-library runtime promotion.

M23.5 does not implement deployment-compiled lookup.

Deployment must not consume governed library drafts, mappings, task pools, presets, profiles, calendars, planning basis records, or standards bundle records as runtime authority unless a later authorized checkpoint closes or reclassifies `DDR-001` with evidence.

## DDR-002 impact

`DDR-002` remains deferred for consolidated runtime-authoritative libraries.

M23.5 does not close `DDR-002`.

M23.5 does not create a consolidated runtime-authoritative library structure.

M23.5 does not claim that existing scattered or draft library assets are sufficient for productized runtime use.

Deployment must preserve compatibility with future consolidation without pretending that consolidation is complete.

## Deployment impact

Deployment boundaries must treat unpromoted governed source assets as non-runtime unless a future roadmap-authorized path explicitly promotes or compiles them.

Deployable operational surfaces must not:

- read draft library assets as runtime truth
- compile governed source assets without authorization
- use milestone evidence as runtime data
- use UAT evidence as runtime data
- infer configuration from governance documents
- infer standards authority from standards-related notes
- infer product generation readiness from templates or generated examples
- package source assets into operational surfaces without classification and authorization

## Packaging impact

Packaging must preserve separation between source packages and deployable packages.

A source package may contain governed source assets for development, governance, validation, and traceability.

A deployable package must include only authorized operational assets.

Governed source assets may remain in repository source without being included in deployable packages.

If a later package includes compiled or promoted operational representations derived from source assets, that package must preserve traceability and validation evidence.

## Configuration impact

Configuration must not turn source assets into runtime authority.

Configuration may later reference approved operational representations only when those representations exist and are authorized.

Configuration must not point deployment at draft governed libraries, source evidence, archive files, or unpromoted mappings as operational truth.

## Artifact impact

Artifact classification must distinguish source assets from deployable operational surfaces.

Evidence artifacts must remain evidence.

Generated artifacts must remain generated outputs unless promoted or validated under an authorized path.

Operational artifacts must not be produced or used before the matching roadmap checkpoint authorizes them.

## Explicit non-goals

`M23.5` does not introduce or approve:

- runtime-authoritative library promotion
- deployment-compiled lookup implementation
- consolidated runtime-authoritative library implementation
- closure of `DDR-001`
- closure of `DDR-002`
- operational release artifact production
- product-ready downloadable packages
- commercial distribution assets
- release packaging
- publishing artifacts
- installer or distribution behavior
- deployment output production
- artifact registry implementation
- artifact manifest implementation
- configuration loading implementation
- secrets management implementation
- tenant/SaaS implementation
- commercial productization
- production deployment
- cloud release process
- live model/provider integration
- pre-go-live operational testing
- standards embedding
- standards-backed citation output
- standards source/citation authority
- standards retrieval/index behavior
- document generation
- report generation
- export generation
- product-ready document/report/export rendering
- raw state access from deployment or packaging adapters
- domain logic relocation into deployment/package/configuration code
- production readiness claims
- go-live readiness claims

## Deferred dependency disposition

The deferred dependency register remains active.

No deferred dependency is closed by `M23.5`.

Current disposition for this checkpoint:

- `DDR-001` remains deferred for governed-library runtime promotion / deployment-compiled lookup.
- `DDR-002` remains deferred for consolidated runtime-authoritative libraries.
- `DDR-003` remains deferred for product-ready document templates.
- `DDR-004` remains open and Critical for standards source registry and citation authority.
- `DDR-005` remains deferred for standards embedding / retrieval index and depends on `DDR-004`.
- `DDR-006` remains deferred for product-ready document/export/report generation and rendering.
- `DDR-007` remains watch for actual model/provider integration and pre-go-live operational testing.
- `DDR-008` remains watch for Phase 8 / Phase 9 productization-readiness planning.
- `DDR-009` remains watch/planning-awareness for future external contract placeholders.

`M23.5` is allowed to proceed because it is boundary evidence only.

It does not perform productization, runtime-authoritative library promotion, deployment-compiled lookup, consolidated runtime-authoritative library implementation, standards embedding, standards-backed output, product-ready document/export/report generation, or live model/provider integration.

## Boundary rules frozen by this checkpoint

The following rules are frozen for downstream M23 work unless a later roadmap-authorized checkpoint changes them:

1. Governed source assets and deployable operational surfaces are separate.
2. Repository presence does not create runtime authority.
3. Deployment must not consume draft governed source assets as runtime truth.
4. Packaging must not turn governed source assets into deployable runtime assets by accident.
5. Configuration must not point operational surfaces at unpromoted source assets.
6. Evidence artifacts remain evidence, not runtime data.
7. Runtime authority requires explicit promotion, compilation, or authorization.
8. `DDR-001` remains deferred and open for future governed-library runtime promotion / deployment-compiled lookup.
9. `DDR-002` remains deferred and open for future consolidated runtime-authoritative libraries.
10. M23.5 does not close any deferred dependency.
11. Deployable operational surfaces must preserve deterministic behavior and fail-closed safety.
12. Productization and commercial distribution remain outside M23.5 scope.

## Implementation decision

`M23.5` is completed as documentation/boundary evidence only.

No runtime library, compiled lookup, deployment adapter, package manifest, artifact generator, configuration loader, deployable operational surface, release artifact, downloadable package, or distribution asset is introduced in this checkpoint.

If a later checkpoint needs runtime-authoritative library promotion, deployment-compiled lookup, or consolidated runtime-authoritative libraries, that work must follow the relevant roadmap and deferred-dependency closure or reclassification path.

## Validation expectation

Because this checkpoint is documentation-only, test execution is not required to prove code behavior.

Recommended local verification after applying this file:

- confirm the new file exists at `docs/milestones/M23/M23_5_GOVERNED_SOURCE_ASSETS_VS_DEPLOYABLE_OPERATIONAL_SURFACES.md`
- confirm `PROGRESS_TRACKER.md` advances the exact next unfinished checkpoint to `M23.6`
- confirm no production code files changed
- optionally run `python -m pytest -q` if the user wants a fresh repo-wide validation baseline after the documentation update

## Acceptance criteria

`M23.5` is acceptable when:

- governed source asset definition is documented
- deployable operational surface definition is documented
- separation rules are explicit
- source assets that must not become runtime authority by presence alone are identified
- promotion/compilation gate concept is defined
- deployment impact of `DDR-001` and `DDR-002` is explicit
- no runtime-authoritative library promotion is claimed
- no deployment-compiled lookup implementation is claimed
- no deferred dependency is falsely closed
- no code behavior is changed
- no unsupported production, deployment, SaaS, standards, model/provider, package publishing, release artifact, or product-ready output capability is claimed

## Next checkpoint

After `M23.5` is applied and accepted, the next roadmap checkpoint is:

`M23.6` — Deployment / packaging validation checkpoint

## Generation note

Generated as a user-applied local documentation package.

Live repository write: `NO`.
