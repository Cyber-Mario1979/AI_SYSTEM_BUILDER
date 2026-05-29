---
doc_type: milestone_evidence_record
canonical_name: M28_6_CONTROLLED_OVERRIDE_MODEL
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.6
checkpoint_title: Controlled override model
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M28.6 — Controlled Override Model

## Purpose

M28.6 creates the runtime-facing controlled override model for cases where the user or project selects a less-strict requirement than the stricter applicable requirement identified by M28.5.

This checkpoint prevents an override from being treated as regulatory equivalence, source closure, source reclassification, or general approval to weaken mandatory standards.

## Execution Mode

Hybrid.

This checkpoint creates source-contract assets, validation behavior, tests, and governance evidence.

## Implementation / Source Minimum

M28.6 adds:

- `asbp/standards_override_model.py`
- `tests/test_standards_override_model.py`

The implementation minimum is a controlled override record structure covering:

- override identity;
- source comparison reference;
- stricter requirement reference;
- selected less-strict requirement reference;
- approver / decision owner;
- decision reference;
- reason for override;
- risk / quality justification;
- residual risk statement;
- applicability boundary;
- limitation statement;
- non-equivalence boundary;
- no-source-closure boundary;
- downstream use limits;
- explicit non-implementation claims.

## Anti-Drift Gate

| Field | M28.6 position |
|---|---|
| Execution mode | Hybrid |
| Implementation minimum | Controlled override model/contract plus tests |
| Governance boundary | Overrides record bounded decisions; they do not create regulatory equivalence, source closure, source reclassification, or product-ready authority |
| Validation evidence required | `python -m pytest -q` is required because this package adds source-contract code and tests |
| Tracker movement rule | Tracker may advance only after the override record structure exists, non-equivalence limits are explicit, and validation is run and recorded truthfully |
| Explicit non-implementation claims | M28.6 does not implement regulatory approval, source closure, standards retrieval/embedding, product-ready standards output, document generation/rendering, UI/API, AI/runtime, deployment, productization, or SaaS readiness |

## Contract Summary

The controlled override model defines:

| Contract area | Control |
|---|---|
| Override identity | Each override record has a stable `OVR-*` identity and version. |
| Comparison link | Override records reference the M28.5 comparison path through `comparison_id` and compared requirement references. |
| Requirement linkage | Each override must identify both the stricter applicable requirement and the selected less-strict requirement. |
| Decision owner | Each override requires approver / decision-owner identity, role, decision status, and decision reference. |
| Risk and rationale | Each override requires reason, risk / quality justification, and residual risk statement. |
| Applicability boundary | Each override is bounded to declared applicability scope. |
| Limitation visibility | Each override requires a visible limitation statement and downstream use limits. |
| Non-equivalence | Each override must state that it is not regulatory equivalence. |
| Source closure boundary | Each override must state that no source or registry closure occurs. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.6 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Defines controlled override minimum fields and confirms overrides must not be treated as source closure or regulatory equivalence. |
| `asbp/standards_requirement_comparison_model.py` | Yes | Supplies M28.5 comparison path and `override_path_reference` boundary that M28.6 formalizes as a controlled override record. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.6 as the next normal roadmap checkpoint after M28.5 validation. |

## DDR Disposition

M28.6 remains under:

- DDR-004 for standards source/citation authority model scope;
- DDR-005 awareness because retrieval/embedding remains deferred to M30;
- DDR-006 awareness because product-ready generation/rendering remains planned for M29.

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M28.6 to M28.7 until the override model/contract, tests, evidence record, and validation evidence are present.

## Explicit Non-Implementation Claims

M28.6 does not implement:

- regulatory approval;
- legal equivalence;
- source closure;
- source reclassification;
- standards retrieval or embedding;
- runtime registry parsing;
- automated source interpretation;
- product-ready standards output;
- product-ready document generation;
- template loading, template selection, rendering, export, or report generation;
- local/company/site standards intake;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness;
- M28 UAT;
- M28 closeout.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
