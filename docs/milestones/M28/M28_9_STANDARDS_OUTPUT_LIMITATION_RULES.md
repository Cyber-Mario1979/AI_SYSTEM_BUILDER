---
doc_type: milestone_evidence_record
canonical_name: M28_9_STANDARDS_OUTPUT_LIMITATION_RULES
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.9
checkpoint_title: Standards-output limitation rules
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M28.9 — Standards-Output Limitation Rules

## Purpose

M28.9 creates the runtime-facing standards-output limitation contract for the local integrated CQV product path.

This checkpoint prevents pending, TBD, user-provided, reference-only, recommendation-only, or otherwise limited standards sources from being hidden inside downstream output. It also preserves registry-version traceability, citation-depth limits, and visible warning behavior.

## Execution Mode

Hybrid.

This checkpoint creates source-contract assets, tests, and governance evidence.

## Implementation / Source Minimum

M28.9 adds:

- `asbp/standards_output_limitation_model.py`
- `tests/test_standards_output_limitation_model.py`

The implementation minimum is a standards-output limitation model covering:

- pending / TBD / user-provided / reference-only source limits;
- citation-depth downgrade behavior;
- registry-version traceability;
- visible warning behavior;
- audit-ready and product-ready claim restrictions;
- downstream use limits;
- explicit non-implementation claims.

A narrative evidence file alone is not sufficient for M28.9 completion.

## Anti-Drift Gate

| Field | M28.9 position |
|---|---|
| Execution mode | Hybrid |
| Implementation minimum | Runtime-facing standards-output limitation contract/model plus tests |
| Governance boundary | Limited source, citation-depth, and registry-version limitations must remain visible and must not be hidden from downstream output |
| Validation evidence required | `python -m pytest -q` is required because this package adds source-contract model behavior and tests |
| Tracker movement rule | Tracker may advance only after limitation behavior is explicit, not hidden, and validation is run and recorded truthfully |
| Explicit non-implementation claims | M28.9 does not implement retrieval/embedding, product-ready standards output, document rendering, UI/API display, AI/runtime behavior, deployment, productization, or SaaS readiness |

## Contract Summary

The limitation model defines:

| Contract area | Control |
|---|---|
| Source limitation detection | Pending, TBD, user-provided, reference-only, recommendation-only, draft, retired, unavailable, non-mandatory, or citation-depth-downgraded sources require visible limitations. |
| Citation-depth behavior | Rendered citation depth must be available for the source and cannot be more specific than the requested depth; section/clause output requires verified source evidence. |
| Warning visibility | Hidden source or output limitation warnings are rejected. |
| Registry traceability | Source registry versions must match the output limitation record and contract registry version. |
| Output claim limits | Product-ready standards output claims are blocked in M28.9; audit-ready output is blocked when limited sources are present. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.9 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies registry authority, source limitation, citation-depth, and non-authority rules for standards-backed output. |
| `asbp/standards_registry_model.py` | Yes | Supplies runtime source-status concepts used by the limitation model. |
| `asbp/standards_registry_store.py` | Yes | Supplies runtime registry helper behavior that M28.9 aligns with. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.9 as the next normal roadmap checkpoint after M28.8 validation. |

## DDR Disposition

M28.9 remains under:

- DDR-004 for standards source/citation authority model scope;
- DDR-005 awareness because retrieval/embedding remains deferred to M30;
- DDR-006 awareness because product-ready generation/rendering remains planned for M29.

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M28.9 to M28.10 until the limitation model, visible warning behavior, tests, and validation evidence are present.

## Explicit Non-Implementation Claims

M28.9 does not implement:

- standards retrieval or embedding;
- product-ready standards output;
- controlled standards text storage;
- document generation, rendering, export, or report generation;
- UI/API display behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness;
- M28 validation checkpoint;
- M28 UAT;
- M28 closeout.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
