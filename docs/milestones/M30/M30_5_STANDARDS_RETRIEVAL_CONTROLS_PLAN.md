---
doc_type: checkpoint_plan
canonical_name: M30_5_STANDARDS_RETRIEVAL_CONTROLS_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M30
checkpoint: M30.5
checkpoint_title: Standards retrieval controls
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m30-5-plan
created_date: 2026-05-31
source_baseline_commit: 08497500af9141ddab2f3ffa7bc40a412a6c4814
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_ONLY
---

# M30.5 — Standards Retrieval Controls Plan

## 1. Purpose

This plan defines the controlled implementation gate for M30.5 — Standards retrieval controls.

M30.5 is not another open-ended planning checkpoint. Its purpose is to authorize the next bounded implementation slice: standards-specific filtering and warning behavior on top of the M30.4 deterministic retrieval skeleton.

## 2. Execution Mode

```text
Hybrid — implementation-gate plan for a bounded standards retrieval control slice.
```

M30.5 planning is complete only if it clearly authorizes or blocks a specific implementation minimum.

## 3. Required Next GO Scope

After this plan is accepted, GO M30.5 may implement only:

```text
standards-specific source-status filters, citation fallback behavior, and limitation warnings for the existing deterministic in-memory retrieval skeleton.
```

Allowed implementation files should remain limited to the retrieval package and tests unless a later review proves another path is required.

Recommended implementation files:

```text
asbp/retrieval/standards.py
tests/test_standards_retrieval_controls.py
```

Optional update if needed:

```text
asbp/retrieval/__init__.py
```

## 4. Implementation Minimum

GO M30.5 must create code and tests. Documentation alone is not enough.

Minimum implementation requirements:

1. filter standards retrieval records by source status;
2. prevent pending/TBD/reference-only records from becoming mandatory authority;
3. provide citation fallback when clause-level or requirement-level citation is unavailable;
4. attach visible limitation warnings to standards retrieval results;
5. preserve M30.4 helper-only / non-authoritative result behavior;
6. preserve source traceability from M30.3;
7. include tests for approved standards, pending/TBD rejection or limitation, citation fallback, limitation warnings, and non-authority behavior.

## 5. Explicitly Not Allowed

GO M30.5 must not implement:

- embeddings;
- vector store;
- external search service;
- live standards lookup;
- standards source mutation;
- clause text fabrication;
- verified clause-level authority where clause data is missing;
- retrieval-backed standards authority;
- AI/model/provider behavior;
- UI/API behavior;
- productization, release, SaaS readiness, commercial launch, or customer-ready output.

## 6. Governance Boundary

M30.5 must preserve:

- M30.1: retrieval is helper-only, source-traceable, and non-authoritative;
- M30.2: only approved/eligible/status-aware sources may be considered;
- M30.3: source ID/path, version/status, authority role, eligibility decision, chunk/ref, build metadata, and limitation traceability remain required;
- M30.4: retrieval results must remain helper-only and non-authoritative, and must fail closed when required metadata is missing.

Roadmap M30.5 allowed work is standards source-status filters, citation fallback, and limitation warnings. The not-allowed boundary is clause claims without verified clause data.

## 7. DDR Impact

### DDR-005

DDR-005 applies directly and remains deferred.

M30.5 may add standards retrieval controls to the bounded skeleton, but it must not close DDR-005. DDR-005 can only be closed, partially closed, or carried at M30 closeout with precise evidence.

### DDR-004

DDR-004 limitations remain active.

M30.5 must not upgrade the standards source/citation authority model into verified legal, regulatory, clause-level, mandatory-use, or audit-ready authority.

### DDR-007

DDR-007 awareness remains only awareness.

M30.5 must not implement retrieval-to-AI handoff, model/provider behavior, local AI runtime, or app-coupled heavy-use behavior.

## 8. Validation Requirement

GO M30.5 changes code/tests and therefore requires:

```text
python -m pytest -q
```

A PR may not claim M30.5 implementation completion without validation evidence.

## 9. Tracker Movement Rule

Tracker movement from M30.5 remains blocked until:

1. this M30.5 plan is accepted;
2. bounded M30.5 implementation evidence exists;
3. tests covering standards retrieval controls exist;
4. `python -m pytest -q` passes;
5. DDR-005 is carried forward truthfully, not closed by assertion;
6. the tracker records M30.5 completion as bounded implementation only.

## 10. Explicit Non-Implementation Claims

This M30.5 plan does not:

- implement M30.5 by itself;
- authorize tracker movement by itself;
- authorize embeddings;
- authorize vector stores;
- authorize live standards lookup;
- authorize retrieval-backed standards authority;
- authorize AI/model/provider behavior;
- authorize UI/API behavior;
- close DDR-005;
- close DDR-004 limitations;
- close DDR-007;
- close the active CAPA;
- authorize productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 11. Immediate Next Action

After this plan is reviewed and accepted, the next bounded action should be:

```text
GO M30.5 — implement standards retrieval controls on the existing bounded retrieval skeleton.
```
