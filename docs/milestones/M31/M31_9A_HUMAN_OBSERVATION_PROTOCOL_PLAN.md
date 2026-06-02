---
doc_type: checkpoint_plan
canonical_name: M31_9A_HUMAN_OBSERVATION_PROTOCOL_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M31
checkpoint: M31.9-A
checkpoint_title: Human observation protocol and runtime path decision record
execution_mode: Governance-only / UAT-preparation
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m319a-human-observation-protocol
created_date: 2026-06-02
source_baseline_commit: 3366c417f38ae2a88def19ababd0ea5d9778760c
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: GO_PROTOCOL_AND_DECISION_RECORD_ONLY
---

# M31.9-A — Human Observation Protocol and Runtime Path Decision Plan

## 1. Purpose

M31.9-A prepares the real internal human AI-use shakedown required by Roadmap v6 M31.9.

This plan records the human observation protocol and runtime path decision before M31.9-B execution.

M31.9-A does not execute real shakedown scenarios, does not generate or store API keys, does not perform provider calls, does not run local model inference from repository code, and does not complete M31.9 human observation.

## 2. Execution Mode

```text
Governance-only / UAT-preparation
```

M31.9 overall remains `UAT / Hybrid` under Roadmap v6, but M31.9-A is a controlled preparatory slice for protocol and runtime-path decision only.

## 3. Source Basis

M31.9-A execution is based on:

- Roadmap Canonical v6;
- PROGRESS_TRACKER current state: READY FOR PLAN M31.9 ONLY;
- M31.3 provider-neutral adapter boundary;
- M31.4 context packet contract;
- M31.5 refusal and limitation rules;
- M31.6 output acceptance and review rules;
- M31.7 evaluation and regression harness;
- M31.8 bounded runtime shakedown protocol;
- Project Owner local runtime preparation evidence for Ollama.

## 4. Runtime Path Decision

M31.9-A selects a staged dual-path shakedown strategy:

1. Local/offline path first.
2. Cloud/provider API comparison second, after safe API key setup.

Primary local/offline runtime candidate:

```text
Ollama 0.30.0 + llama3.2:3b
```

Observed local model evidence supplied by Project Owner:

```text
ollama version is 0.30.0
ollama ps shows llama3.2:3b running 100% GPU
ollama list shows llama3.2:3b, ID a80c4f17acd5, size 2.0 GB
First measured request: approximately 2.49 seconds
Warm measured request: approximately 0.35 seconds
```

Cloud/provider path:

```text
OpenAI API key setup pending.
```

The cloud/provider path must not execute until the API key boundary is explicitly handled outside the repository.

## 5. API Key Boundary

M31.9-A does not require an API key.

M31.9-A does not store or use an API key.

If M31.9-B includes cloud/provider execution, the API key must be stored outside the repository, preferably as an environment variable such as:

```text
OPENAI_API_KEY
```

The key must not be pasted into:

- ChatGPT;
- GitHub;
- source code;
- tests;
- docs;
- PR bodies;
- logs;
- screenshots;
- observation records.

M31.9-B must check only whether the key is present, never print the key value.

## 6. Local Runtime Boundary

M31.9-A confirms that the local/offline runtime candidate is ready for bounded human observation.

The repo must not assume local runtime availability as a normal test dependency.

Normal pytest must not depend on Ollama being installed, a model being downloaded, or a GPU being available.

M31.9-B may use Ollama manually as a controlled observation target only after M31.9-A is accepted.

## 7. Scenario Set for M31.9-B

M31.9-B should inherit the M31.8 scenario family:

- advisory Q&A over governed context;
- retrieval-supported limited answer;
- missing-source refusal / request source evidence;
- draft output support;
- human-review-required output.

Minimum M31.9-B observation set:

1. one useful allowed-answer scenario;
2. one limitation/refusal scenario;
3. one output-review scenario.

The full five-scenario family may be run if time and runtime performance allow.

## 8. Observation Record Requirements

M31.9-B observation evidence must capture:

- observation ID;
- observer / owner ref;
- date;
- runtime path selected;
- runtime setup notes;
- scenario IDs run;
- prompt contract refs;
- context packet refs;
- output / response summary;
- refusal or limitation behavior;
- output-review behavior;
- failure / friction notes;
- unexpected behavior;
- stop conditions triggered;
- owner notes;
- next action recommendation.

M31.9-B evidence must not capture:

- API keys;
- raw provider payloads;
- raw unrestricted model logs;
- customer confidential data;
- customer-ready output;
- approval/release/certification claims;
- commercialization claims.

## 9. Stop Conditions

M31.9-B must stop if:

- API key is required but not safely configured;
- local runtime is unavailable or unstable beyond accepted limits;
- scenario is not predeclared;
- prompt contract is missing;
- context packet reference is missing;
- refusal/limitation behavior is missing;
- output-review behavior is missing;
- model claims approval/release/certification authority;
- model treats retrieval as source/compliance truth;
- model attempts state mutation;
- unbounded prompt execution is attempted;
- raw provider payloads would need to be stored;
- observer cannot understand or record the result.

## 10. Validation Requirement

M31.9-A is docs/governance-only and does not change code, tests, imports, runtime behavior, or executable contracts.

No pytest is required for M31.9-A.

M31.9-B must define validation requirements based on the exact execution scope. If code changes occur, validation must include:

```text
python -m pytest -q
```

## 11. Tracker Movement Rule

M31.9-A does not move the tracker beyond M31.9.

M31.9 tracker movement remains blocked until M31.9-B exists with real internal human observation evidence.

After M31.9-A is accepted, the next allowed checkpoint action is:

```text
GO M31.9-B — execute real internal human AI-use shakedown and record owner observation
```

## 12. Explicit Non-Implementation Claims

M31.9-A does not authorize:

- M31.9 tracker completion;
- M31.10 planning;
- API key generation, storage, or use in the repository;
- real provider calls;
- local model inference from repository code;
- unbounded prompt execution;
- autonomous agentic execution;
- model-owned state mutation;
- AI approval authority;
- AI release/certification authority;
- UI/API behavior;
- customer-facing AI behavior;
- customer-ready output;
- productization;
- deployment;
- release readiness;
- SaaS readiness;
- commercialization launch planning;
- pricing, sales, marketing, revenue, customer-acquisition, or business planning;
- M31 closeout.
