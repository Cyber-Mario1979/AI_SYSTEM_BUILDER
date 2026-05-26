---
doc_type: milestone_checkpoint_output
canonical_name: M16_OUTPUT_ACCEPTANCE
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M16.4
milestone: M16
phase: Phase 6 — AI Layer
---

# M16.4 — Output Acceptance, Bounded Retry, and Fallback Behavior

## Checkpoint

`M16.4` — Output acceptance, bounded retry, and fallback behavior

## Purpose

This document records the M16.4 AI output-acceptance boundary.

M16.4 defines deterministic acceptance, bounded retry, and fallback/refusal behavior for candidate AI output metadata after the M16.1 runtime boundary, M16.2 context-package boundary, and M16.3 generation-mode boundary have already validated the governed runtime inputs.

M16.4 does not implement actual LLM calls, prompt templates, document/report text generation, AI evaluation, retrieval-use governance, recommendation behavior, UI/API behavior, workflow-state mutation, document approval, or release behavior.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## M16.4 boundary

M16.4 attaches output acceptance downstream from:

- `M16.1` AI runtime entry boundary
- `M16.2` AI context packaging from governed engine inputs
- `M16.3` controlled generation-mode selection

M16.4 may evaluate candidate-output metadata only.

It does not carry generated document/report text in the acceptance payload.

It does not approve, release, finalize, mutate workflow state, or create validation/UAT truth.

## Candidate output metadata

A candidate output metadata payload must preserve:

- output candidate identity
- source generation request identity
- source context package identity
- runtime request identity
- job family
- output family
- generation mode
- candidate output reference
- candidate output role
- candidate output classification
- candidate evidence status
- acceptance control flags

The candidate output reference must be version-pinned.

## Acceptance policy

A candidate output may be accepted for downstream review only when all of the following are true:

- content contract is satisfied
- family constraints are satisfied
- standards guardrails are satisfied
- evidence claims are supported
- assumptions are labeled when required
- placeholders are used for missing truth

The candidate must also avoid:

- unbounded invention
- unverified standards claims
- unverified evidence claims
- execution-truth claims
- state mutation requests
- approval requests
- release requests
- validation/UAT truth claims

Acceptance means candidate output is eligible for downstream review only.

It does not mean approval, release, finalization, or workflow mutation.

## Bounded retry policy

A retry may be selected only when:

- the candidate output fails acceptance controls
- evidence is not fully unavailable
- the retry attempt number is still below the configured retry limit

Retry must preserve the same governed generation mode and contract rules.

Retry must not relax standards, evidence, source-truth, execution-truth, or family constraints.

Supported retry reasons:

- `contract_rule_failure`
- `standards_guardrail_failure`
- `evidence_support_failure`
- `assumption_labeling_failure`
- `placeholder_policy_failure`
- `prohibited_output_claim_failure`

## Fallback/refusal policy

Fallback or refusal is required when:

- evidence is insufficient or unavailable
- contracts remain broken after retry limit
- retry limit is reached
- fail-closed behavior is required

Supported fallback reasons:

- `insufficient_evidence`
- `broken_contract`
- `retry_limit_reached`
- `fail_closed_required`

Fallback/refusal must not create source truth, execution truth, approval truth, release truth, validation truth, or UAT truth.

## Repo implementation

M16.4 adds:

- `asbp/ai_runtime/output_acceptance.py`
- `tests/test_ai_runtime_output_acceptance.py`

M16.4 updates:

- `asbp/ai_runtime/__init__.py`

M16.4 records supporting rules at:

- `docs/design_spec/ai_runtime/M16_4_OUTPUT_ACCEPTANCE_RULES.yaml`

## Validation expectation

Because M16.4 introduces Python validation helpers and tests, run:

```powershell
python -m pytest -q
```

## Checkpoint decision

M16.4 creates output acceptance, bounded retry, and fallback/refusal behavior only.

The project should not proceed to `M16.5` validation checkpoint until this boundary is applied, tested, committed, pushed, and accepted.
