---
doc_type: checkpoint_plan
canonical_name: M30_6_LIBRARY_TEMPLATE_RETRIEVAL_CONTROLS_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M30
checkpoint: M30.6
checkpoint_title: Library/template retrieval controls
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m306-plan
created_date: 2026-05-31
source_baseline_commit: 25360fab76ee2289fd46c08eb615e0481ce8474f
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_ONLY
---

# M30.6 — Library / Template Retrieval Controls Plan

## 1. Purpose

This plan defines the controlled implementation gate for M30.6 — Library/template retrieval controls.

M30.6 is an implementation-gate checkpoint. Its purpose is to authorize the next bounded GO slice: asset ID/version filtering and library/template context fetch on top of the existing deterministic retrieval skeleton.

It must not replace deterministic resolver, template selection, source-library authority, stage/commit compatibility, or source truth with probabilistic search.

## 2. Execution Mode

```text
Hybrid — implementation-gate plan for bounded library/template retrieval controls.
```

M30.6 planning is complete only if it clearly defines the next small implementation slice and keeps GO blocked until the plan is accepted.

## 3. Required Next GO Scope

After this plan is accepted, GO M30.6 may implement only:

```text
library/template retrieval controls for approved asset IDs, versions, families, and context fetch using the existing deterministic in-memory retrieval skeleton.
```

Recommended implementation files:

```text
asbp/retrieval/assets.py
tests/test_asset_retrieval_controls.py
```

Optional update if needed:

```text
asbp/retrieval/__init__.py
```

## 4. Implementation Minimum

GO M30.6 must create code and tests. Documentation alone is not enough.

Minimum implementation requirements:

1. filter retrievable records by asset family, such as template or library;
2. require asset ID and asset version metadata for asset retrieval controls;
3. support deterministic context fetch by asset ID/version and optional context type;
4. preserve source traceability from M30.3;
5. preserve helper-only / non-authoritative result behavior from M30.4;
6. preserve standards-specific controls from M30.5 without mixing standards authority into library/template retrieval;
7. reject records that would replace deterministic resolver/template selection with probabilistic search;
8. include tests for asset ID/version filtering, context fetch, family isolation, non-authority preservation, and rejection of missing asset metadata.

## 5. Explicitly Not Allowed

GO M30.6 must not implement:

- embeddings;
- vector store;
- external search service;
- live source lookup;
- deterministic resolver replacement;
- template-selection replacement;
- source-library authority replacement;
- stage/commit compatibility replacement;
- retrieval-backed source authority;
- AI/model/provider behavior;
- UI/API behavior;
- productization, release, SaaS readiness, commercial launch, or customer-ready output.

## 6. Governance Boundary

M30.6 must preserve:

- M30.1: retrieval is helper-only, source-traceable, and non-authoritative;
- M30.2: only approved/eligible/status-aware sources may be considered;
- M30.3: source ID/path, version/status, authority role, eligibility decision, chunk/ref, build metadata, and limitation traceability remain required;
- M30.4: retrieval results must remain helper-only and non-authoritative, and must fail closed when required metadata is missing;
- M30.5: standards retrieval controls remain standards-specific and must not become general source authority.

Roadmap M30.6 allowed work is asset ID/version filtering and template/library context fetch. The not-allowed boundary is replacing deterministic resolver behavior with probabilistic search.

## 7. DDR Impact

### DDR-005

DDR-005 applies directly and remains deferred.

M30.6 may add library/template retrieval controls to the bounded skeleton, but it must not close DDR-005. DDR-005 can only be closed, partially closed, or carried at M30 closeout with precise evidence.

### DDR-004

DDR-004 limitations remain active for standards-related behavior.

M30.6 must not alter or expand standards authority through library/template retrieval.

### DDR-007

DDR-007 awareness remains only awareness.

M30.6 must not implement retrieval-to-AI handoff, model/provider behavior, local AI runtime, or app-coupled heavy-use behavior.

## 8. Validation Requirement

GO M30.6 changes code/tests and therefore requires:

```text
python -m pytest -q
```

A PR may not claim M30.6 implementation completion without validation evidence.

## 9. Tracker Movement Rule

Tracker movement from M30.6 remains blocked until:

1. this M30.6 plan is accepted;
2. bounded M30.6 implementation evidence exists;
3. tests covering library/template retrieval controls exist;
4. `python -m pytest -q` passes;
5. DDR-005 is carried forward truthfully, not closed by assertion;
6. the tracker records M30.6 completion as bounded implementation only.

## 10. Explicit Non-Implementation Claims

This M30.6 plan does not:

- implement M30.6 by itself;
- authorize tracker movement by itself;
- authorize embeddings;
- authorize vector stores;
- authorize live source lookup;
- authorize retrieval-backed source authority;
- authorize deterministic resolver replacement;
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
GO M30.6 — implement library/template retrieval controls on the existing bounded retrieval skeleton.
```
