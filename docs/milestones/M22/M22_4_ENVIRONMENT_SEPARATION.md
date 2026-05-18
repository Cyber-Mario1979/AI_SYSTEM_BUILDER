# M22_4_ENVIRONMENT_SEPARATION

## Milestone

Milestone 22 — Cloud / Compute Foundation

## Phase

Phase 8 — Cloud / Compute Layer

## Checkpoint

`M22.4` — Local / development / test / production separation

## Checkpoint status

Prepared for user-applied repository update.

This document is environment-separation evidence for `M22.4`.

It defines separation expectations, non-production validation evidence rules, future production-like revalidation expectations, and no-promotion-without-evidence rules.

It does not introduce production readiness claims, deployment automation, operational release process, tenant/SaaS promotion rules, environment provisioning, secrets management implementation, production configuration, operational monitoring, productization behavior, live model/provider calls, standards embedding, or product-ready document/export/report generation.

## Source basis

This checkpoint evidence is based on:

- `ROADMAP_CANONICAL.md` v4
- `ROADMAP_ADDENDUM_09_PHASE_8_DETAILED_CHECKPOINT_LADDER.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/milestones/M22/M22_1_CLOUD_COMPUTE_BOUNDARY.md`
- `docs/milestones/M22/M22_2_RUNTIME_PLACEMENT_MODEL.md`
- `docs/milestones/M22/M22_3_ENVIRONMENT_BOUNDARY_MODEL.md`

## Purpose

The purpose of `M22.4` is to define clear separation expectations between local, development, test, and future production contexts.

This checkpoint clarifies what can be accepted as non-production validation evidence and what must be revalidated before any future production-like or production use.

It also establishes the principle that nothing is promoted across environments without explicit evidence.

`M22.4` remains governance and boundary evidence only.

It does not implement deployment, release, production, SaaS, or operational procedures.

## Relationship to M22.1, M22.2, and M22.3

`M22.1` defined cloud/compute as a downstream placement and operational boundary.

`M22.2` defined runtime placement vocabulary and separated runtime role from deployment implementation.

`M22.3` defined environment-boundary concepts and environment roles.

`M22.4` builds on those decisions by defining separation expectations and evidence rules across those environment categories.

The environment-separation model must preserve the following prior decisions:

- cloud/compute remains downstream from governed inner layers
- runtime placement is conceptual until deployment checkpoints authorize implementation
- environment labels are not evidence by themselves
- source truth does not change because environment changes
- validation truth does not change because environment changes
- domain rules do not change because environment changes
- state/persistence authority does not change because environment changes
- API/UI surfaces remain downstream across environments
- production-like and production claims require later roadmap authority and evidence

## Separation model

The project recognizes the following separated contexts:

1. local context
2. development context
3. test / validation context
4. future production-like context
5. future production context

These contexts are not interchangeable.

A result from one context may inform another context, but it does not automatically authorize promotion, release, production use, SaaS use, or productization.

## Local context separation

The local context is used for:

- user-applied file changes
- local development support
- local checks
- local pytest runs
- local documentation review
- local command rehearsal
- learning and exploration

Local context evidence may support:

- confirming a file exists
- confirming a command runs locally
- confirming local tests pass
- confirming local documentation content was reviewed
- confirming a user-applied script changed the intended files

Local context evidence does not automatically prove:

- deployment readiness
- operational readiness
- production readiness
- productization readiness
- SaaS readiness
- provider compatibility
- production-like security posture
- production-like monitoring readiness
- production-like performance
- live model/provider readiness
- audit-ready standards output readiness

## Development context separation

The development context is used for:

- implementation work
- exploratory integration checks
- development-only configuration review
- early adapter or runtime wiring checks when roadmap-authorized
- development verification before controlled test evidence

Development context evidence may support:

- confirming implementation intent
- confirming development behavior
- confirming integration direction
- confirming early design feasibility
- identifying issues before controlled validation

Development context evidence does not automatically prove:

- release readiness
- production readiness
- deployment readiness
- validation acceptance
- UAT acceptance
- productization readiness
- operational readiness
- security readiness
- SaaS readiness

## Test / validation context separation

The test / validation context is used for controlled verification and evidence collection.

Test / validation context evidence may support:

- milestone validation
- regression verification
- acceptance preparation
- controlled command results
- controlled behavior confirmation
- controlled evidence records

Test / validation evidence must identify:

- what was tested
- what command or procedure was run
- which branch or artifact was used
- which files or behavior were covered
- what environment/context produced the evidence
- whether the result was pass, conditional pass, or fail
- any limitation or excluded scope

Test / validation evidence must not be overstated beyond what was actually verified.

## Future production-like context separation

A future production-like context may eventually be used for:

- deployment-readiness assessment
- production-like verification
- operational-readiness assessment
- pre-go-live evidence
- environment promotion checks

At `M22.4`, this is a future conceptual context only.

Before any future production-like use, the project must revalidate or reconfirm:

- relevant deterministic behavior
- state and persistence boundary behavior
- API/UI boundary behavior
- cloud/compute boundary behavior
- configuration assumptions
- environment-specific differences
- validation evidence applicability
- deferred dependency status
- productization blockers
- operational test requirements
- live model/provider gates, if applicable

## Future production context separation

A future production context is reserved for live, productized, operational use after later roadmap authorization.

At `M22.4`, production context is not implemented or approved.

Production context must not be claimed from:

- local testing
- development testing
- documentation evidence alone
- a successful local pytest result alone
- conceptual runtime placement language
- conceptual environment boundary language
- deployment package existence alone
- cloud hosting existence alone
- UI/API surface existence alone

Production use requires later roadmap-authorized implementation, validation, UAT or acceptance evidence where applicable, operational readiness evidence, and deferred dependency disposition.

## Non-production validation evidence rules

Non-production validation evidence may be accepted only within its proven scope.

Acceptable non-production evidence may include:

- local command output
- local pytest result
- controlled test result
- validation checkpoint document
- UAT protocol or report
- user-applied file evidence
- branch comparison evidence
- documented review decision
- closeout note
- decision-gate record

Non-production evidence must not be used to claim production readiness unless a later roadmap-authorized checkpoint explicitly defines that evidence as sufficient for a production-like or production gate.

## Local evidence limitations

Local evidence is useful and valid for local claims.

Examples of valid local claims:

- the file was created locally
- the branch contains the expected documentation file
- local pytest passed
- no code files were changed
- a user-applied package produced the intended repository change

Examples of invalid local-only claims:

- the system is production-ready
- the system is deployable
- the system is operationally ready
- the system is SaaS-ready
- live provider integration is ready
- standards-backed output is audit-ready
- product-ready document generation is complete

## Development evidence limitations

Development evidence is useful for proving development progress.

It must not be used as final release, production, or productization evidence unless later checkpoint rules explicitly allow it.

Development evidence must be converted into controlled validation evidence before it supports milestone acceptance, production-like verification, or go-live decisions.

## Test / validation evidence rules

Test / validation evidence must be controlled, repeatable, and scoped.

At minimum, validation evidence should preserve:

- branch or revision context
- command or procedure
- result
- date or session context when recorded
- scope covered
- exclusions
- decision

Validation evidence must remain tied to actual behavior or artifact review.

Environment names alone do not count as validation evidence.

## Future production-like revalidation rules

Before any future production-like environment can be treated as production-like evidence, the following must be revalidated or formally justified:

- all relevant behavior since the last validated baseline
- environment-specific configuration assumptions
- state/persistence boundary behavior
- API/UI interaction boundaries
- cloud/compute placement assumptions
- runtime placement assumptions
- dependency gate status
- security and access assumptions when later authorized
- operational test path when later authorized
- evidence applicability from prior local/development/test runs

No previous local or development evidence may be promoted silently.

## No-promotion-without-evidence rule

No artifact, runtime, configuration, document, library, model behavior, adapter, or environment assumption may be promoted from one context to another without explicit evidence.

Promotion requires:

- source context
- target context
- artifact or behavior being promoted
- supporting evidence
- known limitations
- required revalidation, if any
- acceptance or decision record when applicable

This rule applies to:

- local to development
- development to test
- test to production-like
- production-like to production
- local directly to production-like
- any non-production context to any future productized context

## What may be reused across environments

The following may be reused across environments if still valid and explicitly checked:

- approved source documents
- governed code artifacts
- roadmap-approved boundaries
- architecture guardrails
- deterministic test procedures
- validation commands
- UAT procedures
- documentation evidence
- decision records
- approved vocabulary
- non-secret configuration concepts
- reviewed assumptions

Reuse does not remove the need to verify applicability.

## What must be revalidated before production-like use

Before future production-like use, the following must be revalidated or formally addressed:

- domain behavior affected by the target context
- state/persistence behavior affected by the target context
- API/UI behavior affected by the target context
- runtime placement behavior affected by the target context
- cloud/compute boundary assumptions
- environment-specific configuration
- evidence traceability
- operational constraints when later authorized
- deferred dependencies related to the target behavior
- any productization, standards, document generation, or model/provider gates

## Source-truth preservation rule

Source truth remains in approved repository and governance artifacts.

Environment movement must not alter source truth.

The following remain authoritative regardless of environment:

- `ROADMAP_CANONICAL.md`
- active `ROADMAP_ADDENDUM_*.md` files
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md` as current-position pointer
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- code and tests as implementation reality
- validation and UAT evidence as evidence records

## State and persistence preservation rule

State and persistence boundaries must be preserved across all contexts.

No context may authorize:

- direct raw state access from adapters
- hidden persistence mutation
- environment-specific persistence bypass
- unvalidated state migration
- deployment convenience overriding save/validation discipline
- cloud/compute wrappers becoming persistence authority

## Deferred dependency disposition

The deferred dependency register remains active.

No deferred dependency is closed by `M22.4`.

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

`M22.4` is allowed to proceed because it defines environment-separation and evidence rules only.

It does not perform deployment automation, operational release implementation, tenant/SaaS promotion, standards embedding, product-ready generation/rendering, productization, or live model/provider integration.

## Explicit non-goals

`M22.4` does not introduce or approve:

- production readiness claims
- deployment automation
- operational release process
- tenant/SaaS promotion rules
- environment provisioning
- secrets management implementation
- production configuration
- deployment pipeline implementation
- SaaS tenant environment design
- actual deployment
- provider-specific infrastructure
- operational monitoring implementation
- productized runtime claims
- go-live readiness claims
- live model/provider calls
- standards embedding
- standards-backed citation output
- standards source/citation authority
- standards retrieval/index behavior
- document generation
- report generation
- export generation
- product-ready document/export/report rendering
- governed-library runtime promotion
- deployment-compiled lookup behavior
- runtime-authoritative library consolidation
- raw state access from cloud adapters
- direct persistence access from cloud adapters
- domain logic relocation into cloud/deployment code
- uncontrolled agentic behavior

## Boundary rules frozen by this checkpoint

The following rules are frozen for downstream Phase 8 work unless a later roadmap-authorized checkpoint changes them:

1. Local, development, test, production-like, and production contexts are separated.
2. Non-production evidence is valid only within its proven scope.
3. Local and development evidence do not automatically become validation evidence.
4. Test / validation evidence must record scope, command or procedure, result, and limitations.
5. Future production-like use requires revalidation or formal applicability review.
6. No context promotion may occur without explicit evidence.
7. Environment labels are not evidence by themselves.
8. Deployment packaging or cloud hosting alone must not be treated as production readiness.
9. Productization, SaaS readiness, and go-live readiness require later roadmap authority and evidence.
10. Deferred dependencies must remain gate-checked before affected future work.

## Implementation decision

`M22.4` is completed as documentation/environment-separation evidence only.

No code package, skeleton package, environment provisioning file, secrets/config template, deployment automation, release process, tenant/SaaS promotion rule, or executable validation package is introduced in this checkpoint.

If a later checkpoint needs executable environment or promotion validation, that work should be planned under the matching later roadmap checkpoint and kept inside the approved scope.

## Validation expectation

Because this checkpoint is documentation-only, test execution is not required to prove code behavior.

Recommended local verification after applying this file:

- confirm the new file exists at `docs/milestones/M22/M22_4_ENVIRONMENT_SEPARATION.md`
- confirm no code files changed
- optionally run `python -m pytest -q` if the user wants a fresh repo-wide validation baseline after the documentation update

## Acceptance criteria

`M22.4` is acceptable when:

- local / development / test / production context separation expectations are documented
- non-production validation evidence rules are defined
- local evidence limitations are defined
- development evidence limitations are defined
- test / validation evidence rules are defined
- future production-like revalidation rules are defined
- no-promotion-without-evidence rules are defined
- what may be reused across environments is explicit
- what must be revalidated before production-like use is explicit
- deferred dependencies are carried forward and not falsely closed
- no production readiness claim is made
- no deployment automation is introduced
- no operational release process is introduced
- no tenant/SaaS promotion rule is introduced
- no code behavior is changed

## Next checkpoint

After `M22.4` is applied and accepted, the next roadmap checkpoint is:

`M22.5` — Cloud assumptions and non-assumptions register

## Generation note

Generated as a user-applied local documentation package.

Live repository write: `NO`.
