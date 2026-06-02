---
doc_type: checkpoint_plan
canonical_name: M31_7_EVALUATION_REGRESSION_HARNESS_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M31
checkpoint: M31.7
checkpoint_title: Evaluation and regression harness
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m317-evaluation-regression-harness
created_date: 2026-06-02
source_baseline_commit: 370d34de49a049d8030d33af865c878bf9fbd831
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_AND_BOUNDED_GO_SCOPE
---

# M31.7 — Evaluation and Regression Harness Plan

## 1. Purpose

This plan defines M31.7 as a hybrid checkpoint: evaluation/regression harness plus first controlled provider/local runtime smoke scaffolding.

M31.7 creates repeatable evaluation evidence over the M31.3 through M31.6 AI safety boundaries and introduces disabled-by-default smoke scaffolding for a future provider/local runtime call path. M31.7 does not authorize app-coupled heavy-use testing, UI/API behavior, productization, deployment, release, SaaS readiness, or customer-ready output.

## 2. Execution Mode

```text
Hybrid — evaluation/regression harness + first controlled provider/local runtime smoke scaffolding.
```

## 3. Source Baseline

M31.7 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31.7;
- `PROGRESS_TRACKER.md` after PR #82;
- M31.3 provider-neutral adapter boundary;
- M31.4 provider-facing context packet contract;
- M31.5 refusal and limitation rules;
- M31.6 output acceptance and review rules;
- M30 retrieval boundary and carried-forward DDRs.

## 4. Approved Build Scope for GO M31.7

GO M31.7 may implement only evaluation/regression harness scaffolding and first controlled provider/local runtime smoke scaffolding.

Allowed build/content:

- evaluation/regression harness baseline;
- regression case schema;
- context packet regression checks;
- refusal/limitation regression checks;
- output acceptance/review regression checks;
- provider-adapter boundary regression checks;
- provider/local smoke request contract;
- disabled-by-default smoke gate;
- smoke result/evidence status;
- pass/fail/fail-closed statuses;
- M31.8 heavy-use boundary statement;
- tests proving smoke is disabled by default and explicitly gated.

Expected files:

```text
asbp/ai_runtime/evaluation_harness.py
tests/test_ai_evaluation_regression_harness.py
docs/milestones/M31/M31_7_EVALUATION_REGRESSION_HARNESS.md
```

## 5. Not Allowed in GO M31.7

GO M31.7 must not implement or authorize:

- app-coupled heavy-use testing before M31.8;
- UI/API behavior;
- autonomous agentic execution;
- unbounded prompt execution;
- productization or release claims;
- customer-ready output;
- SaaS readiness;
- AI approval authority;
- AI release/certification authority;
- model-owned state mutation;
- retrieval-backed source/compliance truth;
- embeddings/vector store implementation;
- live source lookup.

## 6. Provider/Local Runtime Smoke Scope

M31.7 may define the first provider/local runtime smoke path only as disabled-by-default scaffolding.

Rules:

- smoke is blocked by default;
- explicit opt-in is required;
- prompt execution opt-in is separately required;
- provider adapter execution remains blocked unless a later accepted M31.7 smoke evidence step explicitly changes the status within bounded test scope;
- no app-coupled heavy-use testing;
- no UI/API exposure;
- no generated output acceptance;
- no productization claim.

## 7. Regression Dependencies

M31.7 harness must check or record dependency on:

- M31.3 provider boundary;
- M31.4 context packet contract;
- M31.5 refusal/limitation decisions;
- M31.6 output acceptance/review decisions.

## 8. DDR Impact

### DDR-005

DDR-005 remains partially closed for deterministic retrieval controls only. M31.7 must prove retrieval remains support-only and cannot become source/compliance truth.

### DDR-006

DDR-006 remains relevant for generated output. M31.7 may test output acceptance/review rules but must not claim product-ready generated output.

### DDR-007

DDR-007 remains closure-planned and active. M31.7 may begin controlled smoke scaffolding, but this does not close DDR-007 or authorize product/runtime AI behavior.

## 9. Validation Requirement

Because GO M31.7 changes code and tests, executable validation is required:

```text
python -m pytest tests/test_ai_evaluation_regression_harness.py -q
python -m pytest -q
```

If validation cannot be run in the current environment, the PR must state that executable validation was not run and must remain unmerged until validation is run locally or in CI.

## 10. Tracker Movement Rule

Tracker movement from M31.7 remains blocked until:

1. this M31.7 hybrid plan is accepted;
2. evaluation/regression harness exists;
3. regression case schema exists;
4. tests prove M31.3 provider boundary is respected;
5. tests prove M31.4 context packet dependency is respected;
6. tests prove M31.5 refusal/limitation dependency is respected;
7. tests prove M31.6 output acceptance/review dependency is respected;
8. provider/local smoke path is disabled by default;
9. any real smoke execution is explicit, bounded, and evidence-recorded;
10. failure handling is fail-closed;
11. DDR-005, DDR-006, and DDR-007 impacts are explicit;
12. validation passes;
13. next checkpoint is set to `PLAN M31.8 — Local AI heavy-use shakedown protocol`.

## 11. Explicit Non-Implementation Claims

This M31.7 plan may authorize evaluation/regression harness and disabled-by-default smoke scaffolding.

This M31.7 plan does not authorize:

- app-coupled heavy-use testing;
- UI/API behavior;
- productization;
- deployment;
- release readiness;
- commercial launch readiness;
- SaaS readiness;
- customer-ready output.

## 12. Immediate Next Action

After this plan is accepted, the bounded GO action is:

```text
GO M31.7 — implement evaluation/regression harness and first controlled provider/local runtime smoke scaffolding.
```
