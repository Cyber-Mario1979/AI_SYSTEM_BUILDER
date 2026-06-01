---
doc_type: checkpoint_plan
canonical_name: M31_5_REFUSAL_LIMITATION_RULES_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M31
checkpoint: M31.5
checkpoint_title: Refusal and limitation rules
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m315-refusal-limitation-rules
created_date: 2026-06-01
source_baseline_commit: fa88177804ff01b9a0d00035cba36a37b43dcd1c
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_AND_BOUNDED_GO_SCOPE
---

# M31.5 — Refusal and Limitation Rules Plan

## 1. Purpose

This plan defines M31.5 as a hybrid checkpoint: refusal/limitation rule contract plus bounded builder/validator scaffolding and tests.

M31.5 creates the safety rule layer that decides when future AI assistance must refuse, limit, request source evidence, request human review, or defer until later gates. It does not authorize provider/model execution, prompt execution, generated output acceptance, or production AI behavior.

## 2. Execution Mode

```text
Hybrid — refusal/limitation contract + bounded builder/validator scaffolding/tests.
```

## 3. Source Baseline

M31.5 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31.5;
- `PROGRESS_TRACKER.md` after PR #78;
- M31.4 provider-facing context packet contract;
- M31.3 provider-neutral adapter boundary;
- M31.2 local AI model/provider strategy decision;
- M31.1 AI assistance boundary confirmation;
- M30 retrieval boundary and carried-forward DDRs.

## 4. Approved Build Scope for GO M31.5

After this plan is accepted, GO M31.5 may implement only refusal/limitation rule scaffolding and tests.

Allowed build/content:

- refusal/limitation baseline;
- refusal trigger builder/validator;
- context item limitation propagation;
- refusal/limitation decision builder/validator;
- missing-source refusal rules;
- unverified-standards refusal rules;
- unsupported-claim refusal rules;
- out-of-scope request refusal rules;
- retrieval support-only limitation rules;
- provider execution blocked / later-gate deferral rules;
- tests proving model/provider execution and generated output acceptance remain blocked.

Expected files:

```text
asbp/ai_runtime/refusal_rules.py
tests/test_ai_refusal_limitation_rules.py
docs/milestones/M31/M31_5_REFUSAL_LIMITATION_RULES.md
```

## 5. Not Allowed in GO M31.5

GO M31.5 must not implement or authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- AI-generated output;
- output acceptance;
- evaluation harness execution;
- app-coupled heavy-use testing;
- embeddings/vector store implementation;
- live source lookup;
- UI/API behavior;
- productization or release claims.

## 6. Required Refusal/Limitation Rules

M31.5 must enforce or record refusal/limitation behavior for:

- missing source evidence;
- unverified or insufficient standards context;
- unsupported claims;
- out-of-scope requests;
- retrieval context being support-only;
- provider/model execution being blocked;
- state mutation requests;
- AI approval/release/certification requests;
- generated output acceptance requests;
- productization/release/SaaS/customer-ready claims.

## 7. Decision Outcomes

M31.5 supports these safe outcomes:

```text
refuse
limited_answer
request_source
request_human_review
defer_until_later_gate
```

These outcomes are rule decisions only. They are not provider/model outputs and do not accept generated output.

## 8. Context Packet Dependency

M31.5 depends on M31.4 context packets.

Refusal rules may inspect:

- context item source references;
- source family;
- source role;
- authority status;
- evidence status;
- limitation summary;
- allowed use;
- blocked use.

Refusal rules must not inspect raw prompts, raw retrieval dumps, provider payloads, or model output.

## 9. Provider Boundary Dependency

M31.5 depends on M31.3 provider boundary status but does not call providers or models.

Provider/model execution remains blocked and may only result in a later-gate deferral decision.

## 10. DDR Impact

### DDR-005

M31.5 strengthens DDR-005 by refusing or limiting retrieval-backed source/compliance truth when retrieval context is support-only.

### DDR-006

M31.5 does not accept generated output. It only defines refusal/limitation decisions and keeps output acceptance for a later checkpoint.

### DDR-007

DDR-007 remains closure-planned and active. M31.5 does not close DDR-007 and does not authorize model/provider/local runtime execution.

## 11. CAPA Continuation Controls

M31.5 preserves:

- repo truth first;
- PLAN before GO;
- no source-free implementation claims;
- no AI/provider/runtime execution claims without accepted evidence;
- no old-chat authority;
- tracker movement only after accepted evidence;
- bounded branch/PR sequence;
- no autonomous or uncontrolled agentic execution.

## 12. Validation Requirement

Because GO M31.5 changes code and tests, executable validation is required:

```text
python -m pytest tests/test_ai_refusal_limitation_rules.py -q
python -m pytest -q
```

If validation cannot be run in the current environment, the PR must state that executable validation was not run and must remain unmerged until validation is run locally or in CI.

## 13. Tracker Movement Rule

Tracker movement from M31.5 remains blocked until:

1. this M31.5 hybrid plan is accepted;
2. refusal/limitation rule contract exists;
3. refusal trigger builder/validator exists;
4. tests prove missing-source refusal;
5. tests prove unverified-standards refusal;
6. tests prove unsupported-claim refusal;
7. tests prove out-of-scope request refusal;
8. tests prove retrieval support-only context cannot become source truth;
9. tests prove model/provider execution remains blocked;
10. DDR-005, DDR-006, and DDR-007 impacts are explicit;
11. validation passes;
12. next checkpoint is set to `PLAN M31.6 — Output acceptance and review rules`.

## 14. Explicit Non-Implementation Claims

This M31.5 plan may authorize refusal/limitation rule scaffolding and tests.

This M31.5 plan does not authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- model-generated output;
- generated output acceptance;
- app-coupled heavy-use testing;
- tracker movement by itself;
- productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 15. Immediate Next Action

After this plan is accepted, the bounded GO action is:

```text
GO M31.5 — implement refusal and limitation rule scaffolding and tests.
```
