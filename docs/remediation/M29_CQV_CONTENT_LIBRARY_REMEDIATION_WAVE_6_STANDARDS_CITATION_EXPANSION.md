---
doc_type: remediation_evidence
canonical_name: M29_CQV_CONTENT_LIBRARY_REMEDIATION_WAVE_6_STANDARDS_CITATION_EXPANSION
status: READY_FOR_USER_APPLICATION_VALIDATION_PENDING
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 6 — Standards/citation expansion where approved
execution_mode: Build/content
application_mode: user_applied_package
live_repo_write: NO
---

# M29 — CQV Content Library Remediation Wave 6: Standards/Citation Expansion

## Purpose

Wave 6 implements runtime-facing document standards applicability and citation policy source records for the MVP document set.

This wave maps MVP document references to standards applicability and citation limitations only. It does not verify public regulatory meaning, embed standards text, implement standards retrieval, implement standards embeddings, generate documents, accept M29.12 UAT, close M29, or authorize productization.

## Source Assets Added

- `asbp/standards_document_applicability_model.py`
- `asbp/standards_document_applicability_store.py`
- `data/source/standards_applicability/mvp_document_standards_applicability_matrix.json`
- `data/source/standards_citation/mvp_document_citation_policy.json`
- `tests/test_mvp_standards_document_applicability.py`

## Implemented Scope

Wave 6 covers the MVP must-have document refs from the revised Wave 1 matrix and Wave 5 dependency contracts.

The records preserve these boundaries:

- document-level traceability only;
- no section, clause, version, table-row, or requirement-level public-source citation without future verified source evidence;
- no controlled standards text storage;
- no standards retrieval or embedding;
- no audit-ready output claim;
- no mandatory-use claim unless future verified or approved internal source evidence supports it;
- external/adopted and vendor documents remain source/extraction references, not ASBP-owned standards-backed templates.

## Validation Requirement

Because Wave 6 changes source JSON, source models/stores, and tests, validation requires:

    python -m pytest -q

Initial validation found policy IDs containing underscores, which violated the controlled `CITPOL-[A-Z0-9-]+@v#` policy ID pattern.

This validation fix normalizes citation policy IDs to hyphenated identifiers while preserving document references.

Validation must be re-run after applying this fix.

## DDR Impact

Wave 6 directly continues DDR-003, DDR-004, DDR-005, DDR-006, and DDR-009 awareness.

- DDR-003 remains open for product-ready document factory behavior until remaining remediation, validation, repo indexing, and owner acceptance.
- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- DDR-005 remains deferred to M30; no standards retrieval or embedding is implemented here.
- DDR-006 remains open for product-ready document/export/report generation and rendering.
- DDR-009 remains relevant for external/adopted and placeholder-backed behavior.

## Explicit Non-Implementation Claims

Wave 6 does not:

- embed controlled standards text;
- implement standards retrieval or embedding;
- verify public regulatory meaning;
- create audit-ready output;
- create product-ready standards output;
- generate documents;
- accept M29.12 UAT;
- close M29;
- release, deploy, productize, or create SaaS readiness.

## Next Expected Remediation Work

After Wave 6 validates, the next remediation wave is:

`Wave 7 — Trial scenario expansion`

After the full remediation plan is complete, the Project Owner requires a full repository index before returning to UAT or further build continuation.
