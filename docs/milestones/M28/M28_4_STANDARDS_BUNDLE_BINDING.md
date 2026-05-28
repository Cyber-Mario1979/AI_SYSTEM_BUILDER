---
doc_type: milestone_evidence_record
canonical_name: M28_4_STANDARDS_BUNDLE_BINDING
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.4
checkpoint_title: Standards-bundle binding
execution_mode: Hybrid / Build-content
application_mode: user_applied_package
live_repo_write: NO
---

# M28.4 — Standards-Bundle Binding

## Purpose

M28.4 creates controlled standards-bundle binding artifacts for the local integrated CQV product path.

This checkpoint prevents standards bundles from remaining vague labels or becoming universal authority. Each bundle must identify source IDs, applicability boundaries, authority / verification limits, citation-depth limits, and downstream consumer boundaries.

## Execution Mode

Hybrid / Build-content.

This checkpoint creates source-contract assets, source data, source mapping updates, tests, and governance evidence.

## Implementation / Source Minimum

M28.4 adds:

- `asbp/standards_bundle_binding_model.py`
- `asbp/standards_bundle_binding_store.py`
- `data/source/standards_bundles/starter_standards_bundle_bindings.json`
- `tests/test_standards_bundle_binding_model.py`

M28.4 updates:

- `asbp/mapping_source_model.py`
- `data/source/mappings/starter_mappings.json`
- `tests/test_mapping_source_model.py`

The implementation minimum is controlled standards-bundle binding evidence that identifies:

- standards source IDs;
- registry version;
- source authority status;
- source verification status;
- mandatory-use limits;
- citation-depth limits;
- applicability boundaries;
- downstream consumers;
- unresolved or future-scoped template boundaries;
- explicit non-implementation limits.

Vague standards-bundle labels are not sufficient for M28.4 completion.

## Anti-Drift Gate

| Field | M28.4 position |
|---|---|
| Execution mode | Hybrid / Build-content |
| Implementation minimum | Standards-bundle binding model/store/source data, mapping updates, tests, and evidence |
| Governance boundary | Standards bundles bind controlled source IDs and visible limitations; they do not create universal standards authority |
| Validation evidence required | `python -m pytest -q` is required because this package adds source contracts, source data, validator behavior, and tests |
| Tracker movement rule | Tracker may advance only after binding artifacts exist, limitations remain visible, and validation is run and recorded truthfully |
| Explicit non-implementation claims | M28.4 does not implement standards retrieval/embedding, product-ready output, template loading/selection, document generation/rendering, UI/API, AI/runtime, deployment, productization, or SaaS readiness |

## Binding Summary

The starter binding library contains:

| Bundle ID | Scope | Source IDs | Downstream boundary |
|---|---|---|---|
| `SB-CQV-GMP@v1` | CQV / GMP qualification, validation, cleanroom, and GMP documentation context | `STD-EU-GMP-ANNEX-15`, `STD-EU-GMP-CHAPTER-4`, `STD-ASTM-E2500`, `STD-ISO-14644`, `STD-LOCAL-CLEANROOM-NONSTERILE` | Resolves standards-bundle source for `MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1`; template target remains future-scoped to M29 |
| `SB-CSV-GXP@v1` | CSV / GxP computerized-system, electronic-records, and GMP documentation context | `STD-EU-GMP-ANNEX-11`, `STD-FDA-21CFR11`, `STD-ISPE-GAMP5`, `STD-EU-GMP-CHAPTER-4` | Resolves standards-bundle source for `MAP-STD-CSV-GXP-TO-CSV-TEMPLATE@v1`; template target remains future-scoped to M29 |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.4 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies registered standards source IDs, authority status, verification status, citation depth limits, mandatory flags, and limitation rules. |
| `data/source/mappings/starter_mappings.json` | Yes | Supplies existing future standards-bundle mapping placeholders that M28.4 resolves on the standards-bundle side only. |
| `asbp/mapping_source_model.py` | Yes | Supplies mapping-reference validation boundary updated so standard-to-template mappings may resolve standards-bundle sources after M28.4 while template targets remain future-scoped. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.4 as the next normal roadmap checkpoint after M28.3 validation. |

## DDR Disposition

M28.4 remains under:

- DDR-004 for standards source/citation authority model scope;
- DDR-005 awareness because retrieval/embedding remains deferred to M30;
- DDR-006 awareness because product-ready generation/rendering remains planned for M29.

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M28.4 to M28.5 until the binding model, binding source data, mapping updates, helper functions, tests, and validation evidence are present.

## Explicit Non-Implementation Claims

M28.4 does not implement:

- runtime registry parsing or executable standards consumption beyond controlled source-data loading;
- standards embedding or retrieval;
- product-ready standards output;
- product-ready document generation;
- template loading, template selection, rendering, export, or report generation;
- stricter-requirement comparison behavior;
- controlled override behavior;
- local/company/site standards intake;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness;
- M28 UAT;
- M28 closeout.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
