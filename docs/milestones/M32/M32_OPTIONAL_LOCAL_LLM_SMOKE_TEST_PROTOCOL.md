# M32 Optional Local/Offline LLM Smoke Test Protocol

Status: Optional supporting protocol  
Mode: Manual smoke-test protocol  
Branch: `m32-local-llm-smoke-test-protocol`  
Protocol date: 2026-06-04

## Purpose

Define an optional manual smoke-test protocol for local/offline LLM draft support before M32.10 UAT, without changing the official M32 roadmap sequence.

This protocol is not a roadmap addendum, not a checkpoint, not an implementation authorization, not a tracker-advancing item, and not required for normal validation.

## Relationship to M32

Official M32 sequence remains unchanged:

```text
M32.9 — Validation checkpoint
M32.10 — Milestone UAT / owner acceptance
M32.11 — Milestone closeout
```

This protocol may be referenced as optional supporting evidence during M32.10 only if the project owner chooses to run it.

## Scope

Allowed scope:

- optional local/offline LLM smoke test only;
- manual-only evidence;
- local/Ollama-style runtime only if available;
- draft-support behavior only;
- human-review-required output only;
- no normal pytest dependency on Ollama or any live model;
- skipped/failed-to-run state is acceptable when local LLM runtime is unavailable.

Out of scope:

- roadmap addendum;
- checkpoint advancement;
- code implementation;
- provider/cloud API use;
- API key generation, storage, or use;
- raw provider payload storage;
- raw Ollama response dumps as product evidence;
- raw model output as accepted product evidence;
- autonomous agentic execution;
- model-owned state mutation;
- AI approval authority;
- AI release/certification authority;
- customer-facing AI behavior;
- product-ready generated output;
- release readiness;
- deployment readiness;
- SaaS readiness;
- commercial readiness;
- customer-ready output;
- full product/runtime AI readiness.

## Required boundaries

Any manual smoke test must preserve these boundaries:

- CLI/local workflow remains an adapter-only path;
- no CQV domain logic is placed in the CLI surface;
- state/persistence access continues through approved state boundaries;
- LLM output is draft/support only;
- LLM output remains human-review-required;
- source/citation, standards, retrieval, output, validation, and AI limitations remain visible;
- no output is silently accepted, signed, approved, released, certified, or marked product-ready;
- absence of Ollama/local model availability must not fail normal tests or block M32.10 UAT unless the owner explicitly chooses to make it a trial limitation.

## Recommended prerequisites

Before running this optional protocol, verify the deterministic local workflow baseline remains valid:

```text
python -m pytest tests/test_m32_8_end_to_end_local_scenario.py -q
python -m pytest tests/test_m32_3_local_workflow_cli_adapter.py tests/test_m32_4_controlled_input_surfaces.py tests/test_m32_5_workflow_visibility_surfaces.py tests/test_m32_6_output_review_download_surfaces.py tests/test_m32_7_local_workflow_failure_handling.py tests/test_m32_8_end_to_end_local_scenario.py -q
python -m pytest -q
```

These tests must not require Ollama or a live model.

## Optional local LLM availability check

The project owner may check local runtime availability outside the repo validation contract.

Example manual checks:

```text
ollama --version
ollama list
```

If Ollama or a suitable local model is unavailable, record:

```text
Optional local LLM smoke test skipped: local runtime unavailable.
```

Skipping this optional protocol is not a validation failure.

## Optional smoke-test evidence template

When a local/offline LLM runtime is available, capture evidence in this form:

```text
Protocol: M32 Optional Local/Offline LLM Smoke Test Protocol
Date:
Operator:
Local runtime:
Model:
Scenario/work package:
Prompt source:
Draft output destination:
AI call performed: true
Provider/cloud call performed: false
Ollama/local call performed: true
Human review required: true
Approval claimed: false
Release claimed: false
Certification claimed: false
Product-ready claimed: false
Customer-ready claimed: false
Raw model output stored as product evidence: false
Runtime state mutation performed by model: false
Limitations visible: true
Result: PASS / LIMITED / SKIPPED / FAIL
Notes:
```

## Safe prompt constraints

Manual prompts must be bounded and scenario-specific.

Allowed prompt intent:

```text
Create a draft-support summary for the WP-032 cleanroom HVAC qualification-only scenario using only visible scenario facts. Keep the output human-review-required. Do not claim approval, release, certification, compliance, or product readiness.
```

Required prompt constraints:

- use known scenario identifiers only: `WP-032`, `TC-032`, `PLAN-032`;
- state that the result is draft/support only;
- state that human review is required;
- do not ask the model to invent standards clauses, source citations, acceptance criteria, signatures, approvals, release claims, or compliance conclusions;
- do not store raw model response as product evidence;
- do not let the model mutate repo state or validated runtime state.

## Prohibited prompt/output claims

The smoke test must reject or mark invalid any output that claims:

- approved;
- signed;
- released;
- certified;
- validated by AI;
- compliance confirmed;
- customer-ready;
- product-ready;
- deployment-ready;
- SaaS-ready;
- commercially ready;
- source/standards authority beyond repo-visible identifiers.

## Evidence interpretation

Permitted interpretation:

```text
Optional local/offline LLM draft-support smoke test was run/skipped and recorded with limitations.
```

Not permitted:

```text
AI draft output is accepted product evidence.
AI can approve/release/certify CQV output.
Local/offline LLM support is product-ready.
M32.10 UAT is automatically accepted.
M32 closeout is complete.
```

## M32.10 usage

If this optional protocol is run before M32.10, the M32.10 UAT record may reference it only as supporting evidence with limitations.

M32.10 owner acceptance must still explicitly state whether local/offline LLM draft support is:

```text
accepted as optional trial limitation,
deferred,
or excluded from trial acceptance.
```

## Close condition

This protocol is complete when the document exists and is available for optional manual use.

No tracker advancement is allowed from this protocol alone.
