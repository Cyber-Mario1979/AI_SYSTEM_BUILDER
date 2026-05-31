---
doc_type: checkpoint_plan
canonical_name: M30_7_RETRIEVAL_EVALUATION_HARNESS_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M30
checkpoint: M30.7
checkpoint_title: Retrieval evaluation harness
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m307-plan
created_date: 2026-06-01
source_baseline_commit: 70d07aa566d978016840bb3d498239d83e4d17e4
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_ONLY
---

# M30.7 — Retrieval Evaluation Harness Plan

## 1. Purpose

This plan defines the controlled implementation gate for M30.7 — Retrieval evaluation harness.

M30.7 must evaluate the usefulness and safety of the bounded retrieval controls implemented in M30.4 through M30.6. It must not broaden retrieval scope, introduce embeddings, or accept retrieval without evaluation evidence.

## 2. Execution Mode

```text
Hybrid — implementation-gate plan for bounded retrieval evaluation harness.
```

M30.7 planning is complete only if it defines a small code/test slice for evaluation and keeps GO blocked until the plan is accepted.

## 3. Required Next GO Scope

After this plan is accepted, GO M30.7 may implement only:

```text
deterministic retrieval evaluation helpers for recall/precision-style checks, source trace checks, and failure-case checks over existing in-memory retrieval controls.
```

Recommended implementation files:

```text
asbp/retrieval/evaluation.py
tests/test_retrieval_evaluation_harness.py
```

Optional update if needed:

```text
asbp/retrieval/__init__.py
```

## 4. Implementation Minimum

GO M30.7 must create code and tests. Documentation alone is not enough.

Minimum implementation requirements:

1. define an evaluation case model with query text, expected source IDs, expected chunk refs, and optional forbidden source IDs;
2. evaluate retrieval results without mutating retrieval indexes or source data;
3. calculate simple deterministic evaluation signals, such as expected-source recall, unexpected-source count, missing-source count, and source-trace completeness;
4. detect failure cases where retrieval results lack source ID, source path, source version, chunk ref, or non-authoritative/helper-only flags;
5. support evaluating M30.4 base retrieval, M30.5 standards retrieval, and M30.6 asset retrieval result shapes without broadening their behavior;
6. include tests for successful expected-source retrieval, missing expected source, forbidden source result, missing trace metadata, helper-only/non-authoritative enforcement, and empty-result behavior.

## 5. Explicitly Not Allowed

GO M30.7 must not implement:

- embeddings;
- vector store;
- external search service;
- live source lookup;
- retrieval ranking changes outside evaluation helpers;
- standards source mutation;
- deterministic resolver replacement;
- template-selection replacement;
- retrieval-backed source authority;
- AI/model/provider behavior;
- UI/API behavior;
- productization, release, SaaS readiness, commercial launch, or customer-ready output.

## 6. Governance Boundary

M30.7 must preserve:

- M30.1: retrieval is helper-only, source-traceable, and non-authoritative;
- M30.2: only approved/eligible/status-aware sources may be considered;
- M30.3: source ID/path, version/status, authority role, eligibility decision, chunk/ref, build metadata, and limitation traceability remain required;
- M30.4: retrieval results must remain helper-only and non-authoritative;
- M30.5: standards retrieval controls remain standards-specific and limitation-visible;
- M30.6: asset retrieval controls remain asset ID/version/context-fetch helpers and do not replace deterministic resolver or template selection.

Roadmap M30.7 allowed work is recall/precision-style checks, source trace checks, and failure cases. The not-allowed boundary is accepting retrieval without evaluation.

## 7. DDR Impact

### DDR-005

DDR-005 applies directly and remains deferred.

M30.7 may create evaluation evidence for the bounded retrieval controls, but it must not close DDR-005 by assertion. DDR-005 can only be closed, partially closed, or carried at M30 closeout with precise evidence.

### DDR-004

DDR-004 limitations remain active for standards-related retrieval evaluation.

M30.7 must not upgrade standards retrieval into verified legal, regulatory, clause-level, mandatory-use, or audit-ready authority.

### DDR-007

DDR-007 awareness remains only awareness.

M30.7 must not implement retrieval-to-AI handoff, model/provider behavior, local AI runtime, or app-coupled heavy-use behavior.

## 8. Validation Requirement

GO M30.7 changes code/tests and therefore requires:

```text
python -m pytest -q
```

A PR may not claim M30.7 implementation completion without validation evidence.

## 9. Tracker Movement Rule

Tracker movement from M30.7 remains blocked until:

1. this M30.7 plan is accepted;
2. bounded M30.7 implementation evidence exists;
3. tests covering retrieval evaluation harness behavior exist;
4. `python -m pytest -q` passes;
5. evaluation evidence remains deterministic, source-traceable, and non-authoritative;
6. DDR-005 is carried forward truthfully, not closed by assertion;
7. the tracker records M30.7 completion as bounded implementation/evaluation evidence only.

## 10. Explicit Non-Implementation Claims

This M30.7 plan does not:

- implement M30.7 by itself;
- authorize tracker movement by itself;
- authorize embeddings;
- authorize vector stores;
- authorize live source lookup;
- authorize retrieval-backed source authority;
- authorize deterministic resolver replacement;
- authorize template-selection replacement;
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
GO M30.7 — implement retrieval evaluation harness for existing bounded retrieval controls.
```
