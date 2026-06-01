---
doc_type: checkpoint_evidence
canonical_name: M31_5_REFUSAL_LIMITATION_RULES
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: refusal_limitation_rules_evidence
milestone: M31
checkpoint: M31.5
checkpoint_title: Refusal and limitation rules
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m315-refusal-limitation-rules
created_date: 2026-06-01
source_baseline_commit: fa88177804ff01b9a0d00035cba36a37b43dcd1c
live_repo_write: YES_REFUSAL_LIMITATION_SCOPE_ONLY
normal_execution_state: GO_REFUSAL_LIMITATION_CONTRACT_ONLY
project_owner_acceptance: PENDING
---

# M31.5 — Refusal and Limitation Rules Evidence

## 1. Purpose

This document records M31.5 refusal and limitation rule evidence for review.

M31.5 is a hybrid checkpoint. It defines and implements refusal/limitation scaffolding and tests without enabling real provider calls, local model inference, prompt execution, generated output acceptance, API key handling, provider SDK integration, app-coupled heavy-use testing, or production AI behavior.

## 2. Source Basis

M31.5 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31.5;
- `PROGRESS_TRACKER.md` after PR #78;
- M31.4 context packet contract;
- M31.3 provider-neutral adapter boundary;
- M31.2 local AI model/provider strategy decision;
- M31.1 AI assistance boundary confirmation;
- M30 retrieval boundary and carried-forward DDRs.

## 3. Refusal/Limitation Scaffolding Added

M31.5 adds:

```text
asbp/ai_runtime/refusal_rules.py
tests/test_ai_refusal_limitation_rules.py
```

## 4. Refusal/Limitation Behavior

The implemented contract establishes:

- refusal/limitation baseline;
- refusal trigger builder/validator;
- context item limitation propagation;
- refusal/limitation decision builder/validator;
- missing-source refusal support;
- unverified-standards refusal support;
- unsupported-claim refusal support;
- out-of-scope request deferral/refusal support;
- retrieval support-only limitation support;
- provider execution blocked / later-gate deferral support;
- state mutation, AI approval, generated-output acceptance, and productization blocking.

## 5. Blocked Runtime Scope

M31.5 does not implement or authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- local model path handling;
- raw provider response handling;
- AI-generated output;
- generated output acceptance;
- app-coupled heavy-use testing;
- embeddings or vector store execution;
- live source lookup;
- UI/API behavior;
- productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 6. Tests Added

M31.5 adds tests covering:

- baseline M31.5 refusal/limitation rules;
- missing-source refusal;
- unverified-standards limitation propagation;
- unsupported-claim refusal;
- out-of-scope request deferral;
- retrieval support-only limitation;
- provider execution blocked deferral;
- state mutation, AI approval, and productization refusal;
- prompt/provider/raw output prohibited fields;
- execution/acceptance flags remaining blocked;
- invalid trigger/decision alignment rejection.

## 7. DDR Impact

### DDR-005

DDR-005 remains partially closed from M30 for bounded deterministic retrieval controls only.

M31.5 strengthens the retrieval boundary by requiring support-only retrieval context to refuse, limit, or request source evidence instead of becoming source/compliance truth.

### DDR-006

DDR-006 remains relevant if future AI assistance contributes to generated output.

M31.5 does not authorize generated output acceptance, product-ready generated output, or document factory readiness.

### DDR-007

DDR-007 remains closure-planned and active.

M31.5 does not authorize model/provider/local runtime execution and does not close DDR-007.

## 8. Validation

Executable validation is required because M31.5 changes code and tests:

```text
python -m pytest tests/test_ai_refusal_limitation_rules.py -q
python -m pytest -q
```

Validation status at PR preparation time:

```text
NOT RUN in connector session.
```

This PR should not be treated as validated until tests are run locally or in CI.

## 9. Tracker Movement Recommendation

After this evidence is reviewed, accepted, and validated, tracker movement may record M31.5 as completed refusal/limitation rules evidence and set next work to:

```text
PLAN M31.6 — Output acceptance and review rules
```

## 10. Explicit Non-Productization Claims

M31.5 does not claim:

- AI assistance implementation;
- provider readiness;
- model readiness;
- local AI runtime readiness;
- prompt execution readiness;
- generated output acceptance readiness;
- app-coupled heavy-use readiness;
- product-ready generated output;
- UI/API readiness;
- productization;
- deployment;
- release readiness;
- commercial launch readiness;
- SaaS readiness;
- customer-ready output.
