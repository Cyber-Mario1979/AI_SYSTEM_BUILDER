---
doc_type: milestone_evidence_record
canonical_name: M28_5_STRICTER_REQUIREMENT_COMPARISON_RULE
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.5
checkpoint_title: Stricter-requirement comparison rule
execution_mode: Hybrid / Build-content
application_mode: user_applied_package
live_repo_write: NO
---

# M28.5 — Stricter-Requirement Comparison Rule

## Purpose

M28.5 creates the runtime-facing comparison contract/model for stricter-requirement decisions in the local integrated CQV product path.

This checkpoint prevents risk-based rationale, reference standards, pending sources, or user preference from silently weakening a mandatory applicable requirement.

## Execution Mode

Hybrid / Build-content.

This checkpoint creates source-contract assets, tests, and governance evidence.

## Implementation / Source Minimum

M28.5 adds:

- `asbp/standards_requirement_comparison_model.py`
- `tests/test_standards_requirement_comparison_model.py`

The implementation minimum is a controlled comparison model/contract that identifies:

- applicable sources;
- compared requirements;
- comparison basis;
- strictness rationale;
- selected stricter requirement;
- selected requirement;
- override path reference when a less-strict requirement is selected;
- visible limitation behavior;
- explicit non-implementation limits.

A narrative evidence file alone is not sufficient for M28.5 completion.

## Anti-Drift Gate

| Field | M28.5 position |
|---|---|
| Execution mode | Hybrid / Build-content |
| Implementation minimum | Runtime-facing stricter-requirement comparison contract/model plus tests |
| Governance boundary | Risk-based reasoning may support rationale, but must not silently reduce mandatory applicable requirements |
| Validation evidence required | `python -m pytest -q` is required because this package adds source-contract code and tests |
| Tracker movement rule | Tracker may advance only after the comparison model/contract exists, explicit boundary limits are recorded, and validation is run and recorded truthfully |
| Explicit non-implementation claims | M28.5 does not implement standards retrieval/embedding, automatic standards-text interpretation, controlled override records, product-ready standards output, UI/API, AI/runtime, deployment, productization, or SaaS readiness |

## Contract Summary

The comparison model defines:

| Contract area | Control |
|---|---|
| Compared requirements | A comparison record requires at least two structured compared requirements. |
| Applicable sources | Mandatory comparison requires an applicable source with authority, verification, and mandatory flag support. |
| Strictness decision | The `stricter_requirement_id` must reference the highest supplied strictness rank. |
| Less-strict selection | Selecting a less-strict requirement requires an explicit override path reference, override limitation statement, and visible limitation statements. |
| Risk-based rationale | Risk-based rationale cannot silently weaken a mandatory applicable requirement. |
| Limited sources | Pending, TBD, user-provided, reference-only, recommendation-only, or non-mandatory limitations must remain visible. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.5 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies stricter-requirement precedence, risk-based limitation, controlled override requirement, source authority, and limitation rules. |
| `asbp/standards_applicability_model.py` | Yes | Supplies the prior applicability boundary that mandatory use requires applicable source status. |
| `asbp/standards_citation_model.py` | Yes | Supplies the prior citation/no-fabrication boundary. |
| `asbp/standards_bundle_binding_model.py` | Yes | Supplies current standards-bundle source authority and limitation patterns. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.5 as the next normal roadmap checkpoint after M28.4 validation. |

## DDR Disposition

M28.5 remains under:

- DDR-004 for standards source/citation authority and comparison-scope behavior;
- DDR-005 awareness because retrieval/embedding remains deferred to M30;
- DDR-006 awareness because product-ready generation/rendering remains planned for M29.

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M28.5 to M28.6 until the comparison model, tests, explicit boundary limits, and validation evidence are present.

## Explicit Non-Implementation Claims

M28.5 does not implement:

- standards retrieval or embedding;
- runtime registry parsing;
- automated semantic/legal interpretation of standards text;
- controlled override records beyond override-path reference fields;
- local/company/site standards intake;
- product-ready standards output;
- product-ready document generation;
- template loading, template selection, rendering, export, or report generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness;
- M28 UAT;
- M28 closeout.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
