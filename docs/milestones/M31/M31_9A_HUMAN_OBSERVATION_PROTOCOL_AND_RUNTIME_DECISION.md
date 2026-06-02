---
doc_type: checkpoint_evidence
canonical_name: M31_9A_HUMAN_OBSERVATION_PROTOCOL_AND_RUNTIME_DECISION
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: runtime_path_decision_and_uat_preparation
milestone: M31
checkpoint: M31.9-A
checkpoint_title: Human observation protocol and runtime path decision record
execution_mode: Governance-only / UAT-preparation
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m319a-human-observation-protocol
created_date: 2026-06-02
source_baseline_commit: 3366c417f38ae2a88def19ababd0ea5d9778760c
live_repo_write: YES_DECISION_RECORD_ONLY
normal_execution_state: GO_PROTOCOL_AND_DECISION_RECORD_ONLY
project_owner_acceptance: PENDING
---

# M31.9-A — Human Observation Protocol and Runtime Path Decision Record

## 1. Decision Summary

M31.9-A selects a staged dual-path approach for M31.9-B real internal human AI-use shakedown:

```text
1. Run local/offline Ollama observation first.
2. Run cloud/provider API comparison second after safe API key setup.
```

M31.9-A does not execute M31.9-B observation and does not complete M31.9.

## 2. Local Runtime Candidate

Primary local/offline candidate:

```text
Ollama 0.30.0 + llama3.2:3b
```

Project Owner supplied local setup evidence:

```text
ollama version is 0.30.0
ollama run llama3.2:3b completed model pull and produced local runtime response
ollama ps showed llama3.2:3b running with 100% GPU processor allocation
ollama list showed llama3.2:3b, ID a80c4f17acd5, size 2.0 GB
First measured request: approximately 2.49 seconds
Warm measured request: approximately 0.35 seconds
```

Local runtime decision:

```text
READY for bounded offline human observation in M31.9-B.
```

Limitations:

```text
First-run warm-up latency exists.
Ollama/model availability remains a manual local environment precondition.
Normal pytest must not require Ollama, the local model, or GPU availability.
```

## 3. Cloud / Provider Candidate

Provider candidate:

```text
OpenAI API path — pending key setup.
```

Decision:

```text
Cloud/provider execution is allowed for planning only in M31.9-A and remains blocked for execution until safe API key setup is completed and M31.9-B GO explicitly authorizes the provider comparison scope.
```

## 4. API Key Safety Rule

API keys must not be stored or exposed in the repository or project evidence.

Forbidden locations:

- ChatGPT;
- GitHub;
- source code;
- tests;
- docs;
- PR bodies;
- issue bodies;
- logs;
- screenshots;
- observation records.

Allowed handling for later M31.9-B provider comparison:

```text
Use local environment variable only, e.g. OPENAI_API_KEY.
Check presence without printing value.
```

Example presence check for later use:

```powershell
if ($env:OPENAI_API_KEY) { "OPENAI_API_KEY is set" } else { "OPENAI_API_KEY is missing" }
```

## 5. Human Observation Protocol for M31.9-B

M31.9-B must produce a human observation record, not just test output.

Minimum observation set:

```text
S1 — useful allowed-answer scenario
S2 — limitation/refusal scenario
S3 — output-review scenario
```

Optional extended scenario set:

```text
S4 — retrieval-supported limited answer
S5 — human-review-required output
```

M31.9-B observation must capture:

- observation ID;
- observer / owner ref;
- date;
- runtime path selected;
- runtime setup notes;
- scenario IDs run;
- prompt contract refs;
- context packet refs;
- response/output summary;
- refusal or limitation behavior;
- output-review behavior;
- failure / friction notes;
- unexpected behavior;
- stop conditions triggered;
- owner notes;
- next action recommendation.

## 6. M31.9-B Execution Order

Approved planned order:

```text
1. Local/offline Ollama bounded observation.
2. Review local/offline result, latency, usefulness, and limitations.
3. Configure API key outside repo if provider comparison is still desired.
4. Cloud/provider bounded comparison using the same or comparable scenarios.
5. Record owner observation and decide M31.10 readiness.
```

## 7. Stop Conditions for M31.9-B

Stop if:

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

## 8. DDR Impact

### DDR-005

Retrieval remains support-only. M31.9-B must not allow model output to treat retrieval as source authority or compliance truth.

### DDR-006

Generated output remains review-bound. M31.9-B may observe draft/support behavior only and must not claim product-ready generated output or customer-ready output.

### DDR-007

DDR-007 remains active. M31.9-A selects runtime paths and prepares observation, but does not close DDR-007 and does not authorize product/runtime AI behavior.

### DDR-009

M31.9-A does not authorize UI/API behavior.

## 9. Validation Status

M31.9-A is docs/governance-only and does not change code, tests, imports, runtime behavior, or executable contracts.

No pytest is required for M31.9-A.

Latest relevant executable validation remains:

```text
python -m pytest -q — 1572 passed in 48.64s
```

## 10. Acceptance Criteria

M31.9-A may be accepted if the Project Owner confirms:

- local/offline path is ready for bounded observation;
- cloud/provider path remains pending API key setup;
- API keys remain outside the repository and project evidence;
- M31.9-B will run local/offline first;
- M31.9-B will record real human observation evidence;
- M31.9 tracker completion remains blocked until observation evidence exists.

## 11. Explicit Non-Implementation Claims

M31.9-A does not:

- execute M31.9-B observation;
- authorize M31.9 tracker completion;
- authorize M31.10 planning;
- generate, request, store, or use API keys in the repository;
- execute provider calls;
- execute local model inference from repository code;
- authorize unbounded prompt execution;
- authorize autonomous agentic execution;
- authorize model-owned state mutation;
- authorize AI approval authority;
- authorize release/certification authority;
- authorize UI/API behavior;
- authorize customer-facing AI behavior;
- authorize customer-ready output;
- authorize productization;
- authorize deployment;
- authorize release readiness;
- authorize SaaS readiness;
- authorize commercialization launch planning;
- authorize pricing, sales, marketing, revenue, customer-acquisition, or business planning;
- close M31.
