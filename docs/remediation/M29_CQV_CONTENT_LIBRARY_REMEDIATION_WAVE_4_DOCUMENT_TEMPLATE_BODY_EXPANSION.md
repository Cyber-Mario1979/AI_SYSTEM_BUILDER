---
doc_type: remediation_evidence
canonical_name: M29_CQV_CONTENT_LIBRARY_REMEDIATION_WAVE_4_DOCUMENT_TEMPLATE_BODY_EXPANSION
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 4 — Document template body expansion
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29 — CQV Content Library Remediation Wave 4

## Purpose

Wave 4 expands MVP document template body / section-plan source assets for the approved must-have document list.

This wave uses the Project Owner-provided document-template bundle as structure reference only. It does not treat uploaded examples as uncontrolled runtime truth.

## Added / Updated Assets

- `asbp/document_template_body_model.py`
- `asbp/document_template_body_store.py`
- `data/source/document_template_bodies/mvp_document_template_bodies.json`
- `tests/test_document_template_body_model.py`
- `tests/test_document_template_body_store.py`

## Document Coverage

Wave 4 provides body / section-plan source coverage for:

- CCF
- VMP
- SIA
- URS
- Vendor Docs extraction source
- RA / FMEA
- URS Deviation List
- RTM
- DQ
- CP
- QP
- FAT Protocol / Report reference plan
- A0 Certificate
- CTOP
- A1 Certificate
- SAT Protocol / Report reference plan
- CR
- A2 Certificate
- IQ Protocol and Report
- OQ Protocol and Report
- PQ Protocol and Report
- Deviation / Incident Report
- CAPA Closure Form
- VSR
- Decommissioning Document Set

## Boundaries

Wave 4 does not:

- generate documents;
- create signed or approved records;
- replace human review;
- claim product release;
- accept M29.12 UAT;
- close M29;
- implement schemas or DCF binding;
- implement standards embedding/retrieval;
- implement renderer format expansion;
- authorize productization, deployment, release, or SaaS readiness.

## Validation Requirement

Because Wave 4 changes code, source JSON, models, stores, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this package record.

## Remaining Remediation Work

- Wave 5 — Document input schema and DCF expansion
- Wave 6 — Standards/citation expansion where approved
- Wave 7 — Trial scenario expansion
- Wave 8 — Validation and UAT return gate

## Validation Fix Note

A narrow validation fix was prepared after initial local pytest found:

- a test setup that duplicated both `body_id` and `document_ref` while asserting only duplicate `document_ref`;
- a library-control wording issue where an M29.12 boundary statement needed explicit `does not` wording.

The fix preserves Wave 4 scope and does not implement document generation, schema/DCF binding, UAT acceptance, milestone closeout, product release, deployment, productization, or SaaS readiness.
