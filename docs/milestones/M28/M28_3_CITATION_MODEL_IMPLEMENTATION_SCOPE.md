---
doc_type: milestone_evidence_record
canonical_name: M28_3_CITATION_MODEL_IMPLEMENTATION_SCOPE
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.3
checkpoint_title: Citation model implementation scope
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M28.3 — Citation Model Implementation Scope

## Purpose

M28.3 creates the runtime-facing citation contract/model that governs how ASBP may represent standards citations for downstream M28 behavior.

This checkpoint prevents standards-backed output from fabricating source text, clause numbers, versions, section references, regulatory meaning, or audit-ready authority when the registry evidence does not support that citation depth.

## Execution Mode

Hybrid.

This checkpoint creates implementation/source-contract assets and governance evidence.

## Implementation / Source Minimum

M28.3 adds:

- `asbp/standards_citation_model.py`
- `tests/test_standards_citation_model.py`

The implementation minimum is the citation model/contract covering:

- document-level citation behavior;
- version-level citation behavior;
- section-level citation behavior;
- clause-level citation behavior;
- table-row-level citation behavior;
- requirement-level citation behavior;
- citation-depth eligibility;
- missing-clause and missing-depth limitation rules;
- registry-version traceability;
- no-fabrication guard for source text and regulatory meaning;
- explicit non-implementation limits.

A narrative evidence file alone is not sufficient for M28.3 completion.

## Anti-Drift Gate

| Field | M28.3 position |
|---|---|
| Execution mode | Hybrid |
| Implementation minimum | Runtime-facing standards citation contract/model plus tests |
| Governance boundary | Citation depth must not exceed available source evidence, and ASBP must not fabricate clauses, versions, source text, or regulatory meaning |
| Validation evidence required | `python -m pytest -q` is required because this package adds a runtime-facing model and tests |
| Tracker movement rule | Tracker may advance only after the citation contract/model exists, validation is run and recorded truthfully, and limitation behavior remains explicit |
| Explicit non-implementation claims | M28.3 does not parse the runtime registry, implement standards retrieval/embedding, generate product-ready standards output, claim audit-ready clause authority, store/fabricate source text, interpret regulatory meaning, close DDR-005, or close DDR-006 |

## Contract Summary

The citation model defines:

| Contract area | Control |
|---|---|
| Citation levels | Supports document, version, section, clause, table-row, and requirement-level citation records. |
| Citation-depth eligibility | A citation record cannot cite deeper than the source record declares as available. |
| Section / clause controls | Section and clause citations require verified source evidence and available verified reference IDs. |
| Table-row / requirement controls | Table-row and requirement citations require available row or requirement IDs and visible limitations when the source is user-provided, TBD, pending, reference-only, or otherwise limited. |
| Missing-depth limitation | If a deeper requested citation depth is downgraded to a lower available depth, the record must carry a visible limitation statement. |
| Limited-source visibility | Pending, TBD, user-provided, unavailable, not externally verifiable, reference, recommendation, draft, retired, or missing-version sources require visible citation limitations. |
| Audit-ready boundary | Audit-ready citation is blocked for limited sources and requires verified source evidence. |
| No-fabrication guard | M28.3 citation records must not carry source text claims or regulatory meaning claims. |
| Registry traceability | Contract-level registry version must match each citation source record. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.3 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies citation formats, source authority principles, missing-clause limitation rules, citation-depth controls, and no-fabrication boundary. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `ARCHITECTURE_GUARDRAILS.md` | Yes | Confirms no CLI/state/UI/API/AI/runtime boundary bypass is authorized. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.3 as the next unfinished checkpoint and requires PLAN before GO. |

## DDR Impact

M28.3 remains inside M28 standards applicability/citation authority work.

- DDR-004 remains the relevant standards source registry and citation authority dependency.
- DDR-004 is not reopened, downgraded, or reclassified by this checkpoint.
- DDR-005 remains deferred to M30; this checkpoint does not implement standards embedding or retrieval.
- DDR-006 remains closure-planned for M29; this checkpoint does not implement product-ready document/export/report generation or rendering.

## Architecture Boundary

M28.3 does not alter CLI behavior, state/persistence access, UI/API behavior, AI/runtime behavior, deployment behavior, or product workflow behavior.

The added model is a runtime-facing source-contract module only. If later work needs to consume it through CLI, state, UI/API, AI/runtime, deployment, or product workflow surfaces, that work must occur under a later authorized checkpoint and preserve the architecture guardrails.

## Validation Requirement

Because M28.3 adds a runtime-facing model and tests, executable validation is required after applying this package:

`python -m pytest -q`

Do not advance the tracker until validation has run and the result is recorded truthfully.

## Explicit Non-Implementation Claims

M28.3 does not:

- parse the runtime standards registry;
- implement standards embedding or retrieval;
- generate product-ready standards output;
- generate product-ready documents, exports, reports, or rendered artifacts;
- implement stricter-requirement comparison;
- implement controlled override behavior;
- implement local/company/site standards intake;
- claim audit-ready clause authority;
- store or fabricate source text;
- interpret regulatory meaning;
- change CLI behavior;
- change state or persistence behavior;
- change UI/API behavior;
- change AI/model/provider behavior;
- authorize deployment, release, productization, or SaaS action;
- execute M28 UAT;
- close M28;
- close, reopen, downgrade, or reclassify any DDR.
