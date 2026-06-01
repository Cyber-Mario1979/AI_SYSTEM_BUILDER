---
doc_type: checkpoint_plan
canonical_name: M31_3_PROVIDER_ADAPTER_BOUNDARY_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M31
checkpoint: M31.3
checkpoint_title: Provider/adapter boundary if approved
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m313-provider-adapter-boundary
created_date: 2026-06-01
source_baseline_commit: 8279023210e7c5c9d735192cb61baf3e0993146f
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_AND_BOUNDED_GO_SCOPE
---

# M31.3 — Provider/Adapter Boundary Plan

## 1. Purpose

This revised plan defines M31.3 as a hybrid checkpoint: provider/adapter boundary definition plus provider-neutral adapter scaffolding and tests.

The plan corrects the overly conservative governance-only interpretation. M31.3 should create the safe code boundary where future local/offline or external provider behavior can attach later, while still blocking real provider calls, local model inference, prompt execution, API key handling, and production AI behavior.

## 2. Execution Mode

```text
Hybrid — boundary definition + provider-neutral adapter scaffolding/tests.
```

M31.3 is not a real-provider implementation checkpoint. It is also not paper governance only.

## 3. Source Baseline

M31.3 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31.3 checkpoint;
- `PROGRESS_TRACKER.md` after PR #74, which sets M31.3 to PLAN-only;
- M31.1 boundary confirmation evidence;
- M31.2 local AI model/provider strategy decision evidence;
- DDR-007, DDR-005, and DDR-006 carry-forward constraints;
- `ARCHITECTURE_GUARDRAILS.md`.

M31.2 selected a staged local-first / offline-preferred hybrid strategy at strategy level only. It did not authorize model/provider calls, local runtime integration, prompt execution, adapter implementation beyond a later approved boundary, or app-coupled heavy-use testing.

## 4. Approved Build Scope for GO M31.3

After this plan is accepted, GO M31.3 may implement only provider-neutral adapter boundary scaffolding and tests.

Allowed build/content:

- provider adapter boundary contracts;
- provider-neutral request/status validation;
- disabled/null adapter implementation;
- provider registry shape;
- tests proving no direct provider/model execution path is enabled;
- tests proving raw provider payloads, prompts, API keys, local model paths, and provider responses are rejected;
- tests proving model output cannot mutate state;
- tests proving local/offline and external provider kinds remain strategy-only until later checkpoints.

Expected files:

```text
asbp/ai_runtime/provider_contracts.py
asbp/ai_runtime/provider_adapter.py
asbp/ai_runtime/provider_registry.py
tests/test_ai_provider_adapter_boundary.py
docs/milestones/M31/M31_3_PROVIDER_ADAPTER_BOUNDARY.md
```

## 5. Not Allowed in GO M31.3

GO M31.3 must not implement or authorize:

- real OpenAI / Anthropic / Ollama / LM Studio / other provider adapters;
- API key handling;
- provider SDK calls;
- local model inference;
- prompt execution;
- actual AI-generated output;
- app-coupled heavy-use testing;
- embedding/vector store implementation;
- live source lookup;
- UI/API behavior;
- productization or release claims.

## 6. Boundary Model

M31.3 builds the socket, not the electricity.

Approved boundary shape:

```text
Core/workflow/UI -> governed AI runtime/context boundary -> provider adapter boundary -> disabled/null adapter
```

Blocked boundary shape:

```text
Core/workflow/UI -> real provider/model
```

Provider/model/local-runtime behavior may exist later only behind a controlled adapter boundary and after later context packet, refusal, output acceptance, evaluation, validation, and UAT gates.

## 7. Required Boundary Rules

M31.3 must enforce or record:

- no direct model calls from core/UI;
- no raw provider leakage;
- no model-owned state mutation;
- no AI approval authority;
- context packet contract required before model input;
- refusal and limitation rules required before execution;
- output acceptance rules required before accepted output;
- evaluation/validation required before behavior readiness claims.

## 8. Provider Strategy Split

### Disabled provider

M31.3 may implement a disabled/null provider adapter as executable scaffolding. It may build and validate boundary requests but must block execution.

### Local/offline provider

Local/offline provider kind may be represented as a strategy candidate only. It must not execute local inference in M31.3.

### External API provider

External API provider kind may be represented as a strategy candidate only. It must not handle API keys, create provider SDK clients, or make provider calls in M31.3.

## 9. Real Provider Entry Point

Real provider or local runtime execution should enter only after:

- M31.4 context packet contract is accepted;
- M31.5 refusal and limitation rules are accepted;
- M31.6 output acceptance and review rules are accepted;
- M31.7 evaluation/regression harness is available or explicitly scoped.

A later checkpoint may then authorize a first real provider/local runtime smoke path, disabled by default and covered by validation/evaluation evidence.

## 10. DDR Impact

### DDR-007

DDR-007 remains closure-planned and active. M31.3 does not close DDR-007.

M31.3 contributes boundary scaffolding only. Model/provider/local runtime execution remains blocked.

### DDR-005

DDR-005 remains relevant if future AI assistance uses retrieval. M31.3 must not enable raw retrieval-to-model truth injection.

### DDR-006

DDR-006 remains relevant if future AI assistance contributes to generated output. M31.3 must not authorize product-ready generated output or AI output acceptance.

## 11. CAPA Continuation Controls

M31.3 preserves:

- repo truth first;
- PLAN before GO;
- no source-free implementation claims;
- no AI/provider/runtime execution claims without accepted evidence;
- no old-chat authority;
- tracker movement only after accepted evidence;
- bounded branch/PR sequence;
- no autonomous or uncontrolled agentic execution.

## 12. Validation Requirement

Because GO M31.3 changes code and tests, executable validation is required:

```text
python -m pytest -q
```

If validation cannot be run in the current environment, the PR must state that executable validation was not run and must remain unmerged until validation is run locally or in CI.

## 13. Tracker Movement Rule

Tracker movement from M31.3 remains blocked until:

1. this revised M31.3 hybrid plan is accepted;
2. provider-neutral boundary scaffolding exists;
3. disabled/null adapter exists;
4. request/response/status contracts exist;
5. tests prove no direct model/provider calls from core/UI;
6. tests prove no model state mutation;
7. tests prove raw provider payloads, prompt fields, credentials, and local runtime fields are rejected;
8. DDR-007 remains carried forward;
9. next checkpoint is set to `PLAN M31.4 — Context packet contract`.

## 14. Explicit Non-Implementation Claims

This M31.3 plan may authorize provider-neutral boundary scaffolding and tests.

This M31.3 plan does not authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- model-generated output;
- app-coupled heavy-use testing;
- tracker movement by itself;
- productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 15. Immediate Next Action

After this revised plan is accepted, the bounded GO action is:

```text
GO M31.3 — implement provider-neutral AI adapter boundary scaffolding and tests.
```
