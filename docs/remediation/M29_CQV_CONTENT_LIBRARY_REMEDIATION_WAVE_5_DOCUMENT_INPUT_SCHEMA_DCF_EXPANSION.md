---
doc_type: remediation_evidence_record
canonical_name: M29_CQV_CONTENT_LIBRARY_REMEDIATION_WAVE_5_DOCUMENT_INPUT_SCHEMA_DCF_EXPANSION
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 5 — URS DCF intake and downstream document dependency contracts
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# Wave 5 — URS DCF Intake and Downstream Document Dependency Contracts

## Purpose

Wave 5 corrects the document-input design so that DCFs are used only for URS intake.

This wave does not create one DCF per document. Downstream CQV documents derive from URS, vendor documents, risk/traceability records, task pools, profiles, mappings, execution evidence, and human review.

## Source Inputs

The uploaded DCF files were used as structure references only:

- `VALOR_DCF_Cleanroom_v1.docx`
- `VALOR_DCF_Process_Equipment_v1.docx`
- `VALOR_DCF_Utilities_v1.docx`
- `VALOR_DCF_Computerized_Systems_v1.docx`

## Implementation Assets

Wave 5 adds:

- `asbp/document_input_dependency_model.py`
- `asbp/document_input_dependency_store.py`
- `data/source/document_input_schemas/mvp_urs_dcf_intake_catalog.json`
- `data/source/document_input_schemas/mvp_downstream_document_dependency_contracts.json`
- `data/source/document_input_schemas/mvp_vendor_document_extraction_sources.json`
- `tests/test_document_input_dependency_model.py`
- `tests/test_document_input_dependency_store.py`

## Implemented Boundary

Implemented:

- four URS DCF intake structures: cleanroom/HVAC, process equipment, utilities, computerized systems;
- downstream document dependency contracts for the MVP document set;
- vendor document extraction source contracts;
- guardrails preventing downstream documents from using raw DCF intake;
- explicit external/adopted handling for CCF;
- explicit vendor document extraction handling for FDS/SDS/P&ID/manuals/certificates.

Not implemented:

- document generation;
- document rendering;
- DCF-per-document behavior;
- UAT acceptance;
- release or productization claims;
- final decommissioning document names beyond route representation.

## Validation Requirement

Because Wave 5 changes code, source JSON, stores/models, and tests, validation requires:

    python -m pytest -q

Validation has not been executed by this user-applied package record.

## Remaining Work

Wave 6 remains standards/citation expansion where approved.

Wave 7 remains trial scenario expansion.

Wave 8 remains validation and UAT return gate.

## Explicit Non-Implementation Claims

Wave 5 does not:

- generate documents;
- create UAT acceptance;
- approve, release, deploy, or productize outputs;
- implement one DCF per document;
- replace human review;
- close M29;
- authorize productization, deployment, commercial release, or SaaS readiness.

## Validation Fix Note

A Wave 5 validation fix removed ASBP-owned template-body references from external/adopted flow records for FAT Protocol / Report, A0 Certificate, CTOP, A1 Certificate, and SAT Protocol / Report.

These records remain dependency contracts only. They are not DCF-driven documents and do not require ASBP-owned template bodies in Wave 5.

