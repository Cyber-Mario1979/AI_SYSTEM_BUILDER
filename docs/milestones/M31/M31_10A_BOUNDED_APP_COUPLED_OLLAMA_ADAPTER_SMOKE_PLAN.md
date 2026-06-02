---
doc_type: checkpoint_plan
canonical_name: M31_10A_BOUNDED_APP_COUPLED_OLLAMA_ADAPTER_SMOKE_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
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
---

# M31.10-A — Bounded App-Coupled Ollama Adapter Smoke Plan

## 1. Purpose

M31.10-A implements the bounded local/offline app-coupled Ollama adapter smoke contract required by M31.10 Decision B.

The checkpoint proves the narrow integration path from ASBP-side smoke request construction to an injected local Ollama caller and bounded evidence record without requiring Ollama in normal pytest.

## 2. Execution Mode

```text
Hybrid — bounded local runtime adapter smoke contract + focused tests + later manual local smoke evidence
```

## 3. Scope

Allowed:

- local/offline Ollama smoke request contract;
- localhost-only endpoint validation;
- explicit local runtime opt-in;
- explicit prompt execution opt-in;
- bounded generate payload construction;
- injected post function for app-coupled smoke execution;
- bounded evidence record;
- forbidden claim fail-closed detection;
- focused pytest contract tests independent of Ollama;
- documentation of manual smoke boundary.

Not allowed:

- API key handling;
- cloud/provider API calls;
- normal pytest dependency on Ollama, downloaded model, GPU, or running service;
- raw provider payload persistence;
- raw model output storage as product evidence;
- UI/API behavior;
- productization or customer-ready claims.

## 4. Files

```text
asbp/ai_runtime/ollama_adapter.py
tests/test_ai_ollama_adapter_smoke_contract.py
docs/milestones/M31/M31_10A_BOUNDED_APP_COUPLED_OLLAMA_ADAPTER_SMOKE_PLAN.md
docs/milestones/M31/M31_10A_BOUNDED_APP_COUPLED_OLLAMA_ADAPTER_SMOKE.md
```

## 5. Local Runtime Target

Target runtime:

```text
Ollama 0.30.0 + llama3.2:3b
```

Endpoint policy:

```text
http://localhost:11434/api/generate only
```

API key required:

```text
no
```

Cloud/provider call allowed:

```text
no
```

## 6. Validation Requirement

Focused validation:

```text
python -m pytest tests/test_ai_ollama_adapter_smoke_contract.py -q
```

Full validation:

```text
python -m pytest -q
```

These tests must not require Ollama to be installed, a model to be downloaded, a GPU to exist, or an Ollama service to be running.

## 7. Manual Smoke Evidence Requirement

After code/tests are locally validated, the Project Owner may perform a manual local smoke using the bounded contract and the local Ollama service.

Manual smoke evidence must report only bounded summary fields:

- smoke run ID;
- model name;
- endpoint URL;
- result status;
- response summary;
- limitation summary;
- forbidden terms detected;
- output review state.

Manual smoke evidence must not include API keys, raw provider payloads, raw Ollama response dumps, or customer-ready output.

## 8. Tracker Movement Rule

M31.10-A tracker movement remains blocked until:

- adapter smoke contract exists;
- focused tests pass;
- full tests pass;
- manual local Ollama smoke evidence exists or an approved deferral is recorded;
- limitations are documented;
- next checkpoint is explicitly identified.

## 9. Explicit Non-Implementation Claims

M31.10-A does not:

- require API keys;
- execute cloud/provider calls;
- prove cloud/provider behavior;
- close DDR-007;
- authorize full AI integration readiness;
- authorize UI/API behavior;
- authorize customer-ready output;
- authorize productization;
- authorize deployment;
- authorize release readiness;
- authorize SaaS readiness;
- authorize commercialization launch planning;
- close M31.
