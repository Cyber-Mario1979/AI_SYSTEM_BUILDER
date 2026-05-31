---
doc_type: remediation_plan
canonical_name: M29_CQV_CONTENT_LIBRARY_COMPLETION_REMEDIATION_PLAN
status: PROPOSED_FOR_OWNER_REVIEW
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M29 — CQV Content Library Completion Remediation Plan

## Purpose

This plan defines a controlled remediation path for the M29.12 UAT blocker caused by incomplete CQV content libraries and incomplete document-factory content.

The plan prevents M29.12 owner acceptance and M29.13 closeout from proceeding while known content-library gaps remain unaddressed or unapproved.

## Remediation objective

Convert the current starter/baseline content source set into an approved MVP-scoped CQV content-library baseline sufficient to support M29.12 owner acceptance or explicitly carry remaining gaps with owner approval.

## Scope principle

The remediation must not attempt to build all possible CQV content for all industries and all scenarios.

The remediation must first define an approved MVP scope.

Proposed MVP scope candidates:

- Cleanroom / HVAC qualification
- Process equipment qualification
- Utilities qualification
- Computerized system validation
- QC laboratory equipment qualification / calibration linkage
- Manual fallback / unsupported-scope routing

Proposed MVP document families:

- URS or requirements/risk basis
- Qualification plan
- Validation plan
- DQ/IQ/OQ/PQ protocol family where in MVP scope
- Execution report family
- Traceability matrix
- Risk / impact assessment
- Readiness / turnover checklist
- Summary report
- Route decision / fallback assessment record

## Remediation waves

### Wave 1 — Coverage matrix and MVP scope lock

Output:

- `docs/remediation/M29_CQV_CONTENT_LIBRARY_COVERAGE_MATRIX.md`

Purpose:

- define approved MVP domains;
- define included/excluded document families;
- define required source libraries per domain;
- classify must-have versus later-enhancement content.

Completion minimum:

- owner-approved MVP scope;
- clear in/out boundary;
- explicit non-infinite-scope control.

### Wave 2 — Task-pool expansion

Output candidates:

- update/add task-pool source JSON;
- add validation tests where source contracts change;
- add evidence record.

Purpose:

- expand task pools from starter records to MVP coverage;
- resolve document expectations into controlled document references where possible;
- preserve dependency and owner-role rules.

Completion minimum:

- expanded task pools for approved MVP domains;
- no dangling duration/document refs;
- validation passes.

### Wave 3 — Profiles, calendars, planning basis, and mappings expansion

Output candidates:

- update/add profile source JSON;
- update/add calendar/planning-basis source JSON;
- update/add mapping source JSON;
- add cross-library validation.

Purpose:

- turn starter context into usable MVP source families;
- preserve human-confirmation controls where assumptions remain site-specific;
- improve source-to-execution routing.

Completion minimum:

- profile/task/calendar/duration/mapping references validate;
- regional assumptions remain visible;
- validation passes.

### Wave 4 — Document template body expansion

Output candidates:

- add document template body/section-plan source files;
- expand template records or add linked body records;
- add tests for template body loading/selection.

Purpose:

- convert template records into real document template structures;
- support major MVP document families, not only QP/CSV validation plan.

Completion minimum:

- real section/body structures exist for approved MVP documents;
- templates are versioned, statused, and source-located;
- validation passes.

### Wave 5 — Document input schema and DCF expansion

Output candidates:

- expand document input schema source JSON;
- define DCF/minimum-input mappings for additional document families;
- add field/section binding validation.

Purpose:

- support real inputs for expanded templates;
- block hidden assumptions;
- preserve placeholders and missing-data behavior.

Completion minimum:

- schemas exist for all approved MVP templates;
- DCF and skip-DCF paths are explicit;
- validation passes.

### Wave 6 — Standards/citation expansion where approved

Output candidates:

- expand standards registry/bundle records only where source authority permits;
- preserve pending/TBD limitations;
- avoid invented clause-level claims.

Purpose:

- deepen standards applicability and citation support without overclaiming regulatory authority.

Completion minimum:

- source limitations remain visible;
- no standards retrieval/embedding unless separately approved;
- validation passes.

### Wave 7 — Trial scenario expansion

Output candidates:

- expand trial scenarios beyond two local samples;
- include scenario coverage for approved MVP domains/document families.

Purpose:

- prove the expanded content library supports realistic local review flows.

Completion minimum:

- local trial sample coverage matches MVP scope;
- output validation passes;
- no UAT/customer-ready claims.

### Wave 8 — Validation and UAT return gate

Output candidates:

- validation evidence;
- UAT return decision record;
- tracker update only after required evidence.

Purpose:

- prove remediation is complete enough to resume M29.12.

Completion minimum:

- full test suite passes;
- content coverage matrix status is closed or explicitly carried;
- Project Owner approves return to M29.12 UAT.

## Blocked during remediation

- M29.12 acceptance
- M29.13 closeout
- productization
- deployment
- SaaS readiness
- customer-ready release claims
- standards embedding/retrieval unless separately approved
- UI/API product behavior unless roadmap-authorized
- hidden source/content limitations

## Required governance decision

Because this remediation may affect product-core gates and M29.12 acceptance criteria, a roadmap/change-control decision is required before inserting new execution waves into the active checkpoint order.

## Validation policy

Docs-only remediation planning does not require pytest.

Any implementation wave that changes source JSON, schemas, runtime models, stores, validators, mappings, tests, or executable behavior requires:

`python -m pytest -q`

## Tracker policy

Tracker must not advance to M29.13 while this blocker remains active.

Tracker may either:

1. stay at M29.12 with blocker status recorded, or
2. move to a remediation checkpoint only after a roadmap/change-control decision authorizes that movement.

## Explicit non-implementation claims

This remediation plan does not:

- implement library expansion;
- modify source JSON;
- modify code;
- update tests;
- update tracker;
- change roadmap order;
- accept M29.12;
- close M29;
- productize, deploy, or create SaaS readiness.
