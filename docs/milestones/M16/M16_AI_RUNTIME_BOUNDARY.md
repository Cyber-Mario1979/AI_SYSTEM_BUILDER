---
doc_type: milestone_checkpoint_output
canonical_name: M16_AI_RUNTIME_BOUNDARY
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M16.1
milestone: M16
phase: Phase 6 — AI Layer
---

# M16.1 — AI Runtime Boundary for Document/Reporting Jobs

## Checkpoint

`M16.1` — AI runtime boundary for document/reporting jobs

## Purpose

This document records the first AI runtime boundary for governed document and reporting workflows.

M16.1 defines when AI runtime entry is eligible, which caller boundaries are allowed, which runtime states are blocked, and what the model is explicitly prohibited from doing.

M16.1 does not implement actual LLM calls, prompt templates, context packaging, generation modes, output acceptance/retry/fallback behavior, AI evaluation, retrieval-use governance, recommendation behavior, UI/API behavior, runtime document generation, or runtime export generation.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## M16.1 boundary

M16.1 attaches the AI runtime boundary downstream from:

- governed document-engine contracts and controls
- governed export/reporting-engine contracts and controls
- governed resolver / registry and retrieval boundaries
- governed library and service-hardening boundaries

AI runtime entry is not source truth, execution truth, approval authority, workflow mutation authority, or validation/UAT authority.

## Allowed job families

- `governed_document_job`
- `governed_reporting_job`

## Allowed caller boundaries

- `document_engine_boundary`
- `export_engine_boundary`
- `orchestration_service_boundary`

## Blocked caller boundaries

- `cli_adapter`
- `ui_adapter`
- `direct_user_prompt`
- `free_form_chat`
- `ungoverned_ai_runtime`

## Allowed model permission profiles

- `controlled_language_drafting`
- `bounded_summarization`
- `candidate_wording_generation`

## AI may do

- draft controlled language
- summarize governed inputs
- prepare candidate wording
- produce bounded document/reporting text
- return candidate output for downstream acceptance

## AI must not do

- own source truth
- own execution truth
- approve documents
- release tasks
- mutate workflow state
- replace template/document/export contracts
- replace standards guardrails
- replace validation or UAT evidence
- bypass governed retrieval
- invent standards or evidence

## Repo implementation

M16.1 adds:

- `asbp/ai_runtime/__init__.py`
- `asbp/ai_runtime/runtime_boundary.py`
- `tests/test_ai_runtime_boundary.py`

M16.1 records supporting rules at:

- `docs/design_spec/ai_runtime/M16_1_AI_RUNTIME_BOUNDARY_RULES.yaml`

## Validation expectation

Because M16.1 introduces Python validation helpers and tests, run:

```powershell
python -m pytest -q
```

## Checkpoint decision

M16.1 creates the AI runtime entry boundary only.

The project should not proceed to context packaging, generation modes, or output acceptance behavior until this boundary is applied, tested, committed, pushed, and accepted.
