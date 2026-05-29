---
doc_type: uat_protocol
canonical_name: M28_UAT_PROTOCOL
status: READY_FOR_UAT_EXECUTION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.11
checkpoint_title: Milestone UAT / owner acceptance
execution_mode: UAT
application_mode: user_applied_package
live_repo_write: NO
---

# M28 — UAT Protocol

## Purpose

This protocol defines the M28 UAT review for Standards Applicability, Citation, and Runtime Consumption Authority.

M28 UAT confirms that the implemented standards authority surface is understandable, bounded, validated, and ready for M28.12 closeout review.

This UAT is not implementation work and does not create new standards behavior.

## UAT Scope

The UAT scope covers M28.3 through M28.10 evidence and implemented source-contract surfaces:

- M28.3 — Citation model implementation scope
- M28.4 — Standards-bundle binding
- M28.5 — Stricter-requirement comparison rule
- M28.6 — Controlled override model
- M28.7 — Local/company/site standards intake
- M28.8 — Runtime registry consumption package
- M28.9 — Standards-output limitation rules
- M28.10 — Validation checkpoint

## UAT Evidence Sources

| Evidence source | Expected role |
|---|---|
| `docs/milestones/M28/M28_3_CITATION_MODEL_IMPLEMENTATION_SCOPE.md` | Citation behavior evidence |
| `docs/milestones/M28/M28_4_STANDARDS_BUNDLE_BINDING.md` | Standards-bundle binding evidence |
| `docs/milestones/M28/M28_5_STRICTER_REQUIREMENT_COMPARISON_RULE.md` | Stricter-requirement comparison evidence |
| `docs/milestones/M28/M28_6_CONTROLLED_OVERRIDE_MODEL.md` | Controlled override model evidence |
| `docs/milestones/M28/M28_7_LOCAL_COMPANY_SITE_STANDARDS_INTAKE.md` | Local/company/site standards intake evidence |
| `docs/milestones/M28/M28_8_RUNTIME_REGISTRY_CONSUMPTION_PACKAGE.md` | Runtime registry consumption evidence |
| `docs/milestones/M28/M28_9_STANDARDS_OUTPUT_LIMITATION_RULES.md` | Standards-output limitation behavior evidence |
| `docs/milestones/M28/M28_10_VALIDATION_CHECKPOINT.md` | Validation evidence |
| `PROGRESS_TRACKER.md` | Current checkpoint and validation state |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | DDR status and carry-forward controls |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Execution-mode and anti-drift controls |

## Validation Reference

M28 UAT must reference the M28.10 validation result:

`python -m pytest -q — 1258 passed in 48.01s`

## Acceptance Criteria

M28 UAT passes only when all criteria below are satisfied:

1. Standards applicability behavior is controlled and understandable.
2. Citation behavior is controlled and prevents fabricated clauses, versions, source text, or regulatory meaning.
3. Standards-bundle binding records identify source IDs, applicability boundaries, authority / verification limits, and downstream consumer boundaries.
4. Stricter-requirement comparison behavior prevents silent weakening of mandatory applicable requirements.
5. Controlled override records preserve approver, rationale, residual risk, applicability boundary, source comparison, decision reference, limitation statement, and non-equivalence boundaries.
6. Local/company/site standards intake preserves draft source records, authority decisions, comparison requirements, approval state, limitation handling, and local/company/site/client source status.
7. Runtime registry consumption reads controlled source data and enforces source-status limitations.
8. Standards-output limitation rules keep pending, TBD, user-provided, reference-only, and limitation states visible.
9. Registry version traceability remains visible.
10. DDR-004 is not overclaimed beyond the approved source/citation authority model scope.
11. DDR-005 remains deferred to M30; no standards retrieval or embedding is accepted by this UAT.
12. DDR-006 remains closure-planned for M29; no product-ready document/export/report generation or rendering is accepted by this UAT.
13. No product-ready standards output, UI/API behavior, AI/model/provider behavior, deployment, productization, or SaaS readiness is accepted by this UAT.
14. M28.10 validation evidence exists and records a passing validation result.

## Operator-Facing Review Checklist

| Item | Expected answer |
|---|---|
| Is standards applicability behavior controlled? | Yes |
| Is standards citation behavior controlled? | Yes |
| Are citation-depth limitations visible? | Yes |
| Are pending/TBD/user-provided/reference-only source limitations visible? | Yes |
| Are standards-bundle bindings explicit and not vague labels? | Yes |
| Does stricter-requirement comparison preserve mandatory applicable requirements? | Yes |
| Are override records non-equivalence records, not regulatory approval? | Yes |
| Does local/company/site intake avoid treating uploaded sources as public regulation? | Yes |
| Does runtime registry consumption use controlled source data only? | Yes |
| Are standards-output limitations visible and not hidden? | Yes |
| Is M28.10 validation evidence present? | Yes |
| Is DDR-005 carried forward to M30? | Yes |
| Is DDR-006 carried forward to M29? | Yes |
| Is M28 non-productizing? | Yes |

## Not-Allowed Behavior Checklist

The reviewer must confirm that M28 UAT does not accept or introduce:

- standards retrieval or embedding
- product-ready standards output
- product-ready document generation
- document rendering, export, or reporting
- audit-ready clause-level authority for pending/TBD sources
- public-regulation claims for user-provided/local/internal sources
- regulatory/legal approval
- source closure by override
- UI/API product behavior
- AI/model/provider behavior
- deployment, productization, or SaaS readiness
- M28 closeout before UAT evidence is accepted

## DDR Carry-Forward Check

M28 UAT must confirm:

- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- DDR-005 remains deferred to M30 for standards embedding / retrieval index work.
- DDR-006 remains closure-planned for M29 for product-ready document/export/report generation and rendering.
- M28.11 does not close, reopen, downgrade, or reclassify any DDR.

## Required Evidence for UAT Completion

UAT completion requires:

- this protocol;
- a completed UAT report under `docs/UAT/M28/M28_UAT_REPORT.md`;
- acceptance decision;
- rationale;
- reviewer / owner field;
- validation evidence reference;
- limitation acceptance statement;
- tracker update to `M28.12` only after acceptance.

## Protocol Decision

Protocol decision: ready for M28 UAT report execution.

## Generation Note

Generated as a user-applied local documentation package.

Live repository write: `NO`.
