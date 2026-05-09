---
doc_type: milestone_checkpoint_output
canonical_name: M17_AI_EVALUATION_BASELINE
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M17.1
milestone: M17
phase: Phase 6 — AI Layer
---

# M17.1 — AI Evaluation Baseline and Regression Harness

## Checkpoint

`M17.1` — AI evaluation baseline and regression harness

## Purpose

This document records the M17.1 AI evaluation baseline boundary.

M17.1 defines a deterministic baseline and regression harness for governed AI output records produced by the closed M16 AI runtime boundary.

M17.1 measures whether validated M16 output-acceptance decisions remain stable against explicit regression expectations over time.

M17.1 does not implement actual LLM calls, prompt templates, quality gates, groundedness checks, evidence-link checks, standards-conformance checks, detail-level consistency checks, retrieval-use governance, recommendation behavior, UI/API behavior, workflow mutation, approval, or release behavior.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## M17.1 boundary

M17.1 attaches downstream from the closed M16 governed AI runtime boundary.

An evaluation case must consume a validated M16 output-acceptance decision.

The regression harness compares:

- expected acceptance decision
- actual validated M16 acceptance decision

The comparison produces deterministic regression case and regression run results.

## Supported evaluation families

- `document_output_evaluation`
- `reporting_output_evaluation`

## Supported baseline dimensions

- `acceptance_decision_consistency`
- `candidate_contract_coverage`
- `regression_stability`

These are baseline/regression dimensions only.

They are not M17.2 quality gates, M17.2 groundedness checks, M17.3 standards-conformance checks, M17.3 detail-level consistency checks, or M17.4 retrieval-use governance rules.

## Regression behavior

A regression case passes when the source acceptance decision matches the expected acceptance decision.

A regression case fails when the source acceptance decision differs from the expected acceptance decision.

A regression run passes only when all cases pass.

A regression run fails when one or more cases fail.

## Boundary protections

M17.1 evaluation records must not include:

- actual LLM calls
- prompt templates
- generated document/report text
- quality gate decisions
- groundedness scores/checks
- evidence-link checks
- standards-conformance checks
- detail-level consistency checks
- retrieval-use decisions
- recommendation payloads
- workflow mutation payloads
- approval payloads
- release payloads
- source/execution/validation truth overrides

## Repo implementation

M17.1 adds:

- `asbp/ai_evaluation/__init__.py`
- `asbp/ai_evaluation/evaluation_baseline.py`
- `tests/test_ai_evaluation_baseline.py`

M17.1 records supporting rules at:

- `docs/design_spec/ai_evaluation/M17_1_AI_EVALUATION_BASELINE_RULES.yaml`

## Validation expectation

Because M17.1 introduces Python validation helpers and tests, run:

```powershell
python -m pytest -q
```

## Checkpoint decision

M17.1 creates the AI evaluation baseline and regression harness only.

The project should not proceed to `M17.2` quality gates and groundedness checks until this boundary is applied, tested, committed, pushed, and accepted.
