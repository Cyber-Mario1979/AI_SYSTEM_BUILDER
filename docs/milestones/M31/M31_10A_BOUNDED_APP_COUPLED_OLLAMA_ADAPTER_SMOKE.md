---
doc_type: checkpoint_evidence
canonical_name: M31_10A_BOUNDED_APP_COUPLED_OLLAMA_ADAPTER_SMOKE
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: ollama_adapter_smoke_contract_evidence
milestone: M31
checkpoint: M31.10-A
checkpoint_title: Bounded app-coupled Ollama adapter smoke
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m3110a-ollama-adapter-smoke
created_date: 2026-06-02
source_baseline_commit: 58ab5b5ff4ba3f24405a42882e27f768fd478b18
live_repo_write: YES_CODE_AND_TEST_SCOPE
normal_execution_state: GO_OLLAMA_ADAPTER_SMOKE_CONTRACT_ONLY
project_owner_acceptance: PENDING
---

# M31.10-A — Bounded App-Coupled Ollama Adapter Smoke Evidence

## 1. Purpose

This document records M31.10-A bounded app-coupled Ollama adapter smoke contract evidence for review.

The implementation creates a local/offline smoke contract and testable adapter-facing path for Ollama without making normal pytest depend on Ollama.

## 2. Implementation Added

```text
asbp/ai_runtime/ollama_adapter.py
tests/test_ai_ollama_adapter_smoke_contract.py
```

## 3. Contract Behavior

The contract defines:

- M31.10-A smoke baseline;
- local Ollama provider kind;
- localhost-only endpoint validation;
- explicit local runtime opt-in;
- explicit prompt-execution opt-in;
- bounded generate payload construction;
- injected `post_json` caller for smoke execution;
- bounded evidence record;
- forbidden claim detection and fail-closed result status;
- no API key requirement;
- no cloud/provider call authorization;
- no UI/API/productization/customer-ready claims.

## 4. Runtime Boundary

Runtime target:

```text
Ollama 0.30.0 + llama3.2:3b
```

Endpoint:

```text
http://localhost:11434/api/generate
```

API key required:

```text
no
```

Cloud/provider call allowed:

```text
no
```

Normal pytest requires Ollama:

```text
no
```

## 5. Tests Added

Focused tests cover:

- local-only baseline and no API key policy;
- explicit runtime and prompt opt-in gates;
- API key, cloud endpoint, raw prompt, raw provider payload, and raw model output rejection;
- bounded generate payload construction;
- injected `post_json` execution without requiring Ollama;
- bounded evidence capture;
- forbidden claim detection and fail-closed evidence;
- productization/customer-ready/commercialization flag rejection.

## 6. Validation Required

Because this PR changes code/tests, validation is required before merge:

```text
python -m pytest tests/test_ai_ollama_adapter_smoke_contract.py -q
python -m pytest -q
```

Validation status at PR preparation time:

```text
NOT RUN in connector session.
```

## 7. Manual Smoke Requirement

After focused and full tests pass, the Project Owner should run a controlled manual local smoke against Ollama and record bounded evidence.

Manual smoke should not be hidden inside normal pytest.

Manual smoke evidence must not include:

- API keys;
- raw provider payload dumps;
- raw Ollama response dumps;
- customer-ready output;
- approval/release/certification claims;
- productization claims.

## 8. DDR Impact

### DDR-005

Retrieval remains support-only. The M31.10-A smoke must not treat retrieval as source authority or compliance truth.

### DDR-006

Generated output remains draft/review-bound. M31.10-A evidence must not claim product-ready generated output or customer-ready output.

### DDR-007

DDR-007 remains active. M31.10-A creates local/offline app-coupled smoke evidence path, but cloud/provider API behavior remains unproven.

### DDR-009

M31.10-A does not authorize UI/API behavior.

## 9. Explicit Non-Implementation Claims

M31.10-A does not:

- require API keys;
- store API keys;
- execute cloud/provider calls;
- prove cloud/provider behavior;
- close DDR-007;
- authorize full product/runtime AI readiness;
- authorize unbounded prompt execution;
- authorize autonomous agentic execution;
- authorize model-owned state mutation;
- authorize AI approval authority;
- authorize release/certification authority;
- authorize UI/API behavior;
- authorize customer-ready output;
- authorize productization;
- authorize deployment;
- authorize release readiness;
- authorize SaaS readiness;
- authorize commercialization launch planning;
- close M31.
