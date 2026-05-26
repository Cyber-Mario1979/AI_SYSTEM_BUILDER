---
doc_type: milestone_checkpoint_output
canonical_name: M16_GENERATION_MODES
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M16.3
milestone: M16
phase: Phase 6 — AI Layer
---

# M16.3 — Controlled Generation Modes for Document/Reporting Families

## Checkpoint

`M16.3` — Controlled generation modes for document/reporting families

## Purpose

This document records the M16.3 AI controlled-generation-mode boundary.

M16.3 defines which controlled generation modes may be requested for governed document and reporting output families after the M16.1 runtime boundary and M16.2 context-packaging boundary have already validated the request inputs.

M16.3 does not implement actual LLM calls, prompt templates, document/report text generation, output acceptance, retry/fallback behavior, AI evaluation, retrieval-use governance, recommendation behavior, or UI/API behavior.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## M16.3 boundary

M16.3 attaches controlled generation-mode selection downstream from:

- `M16.1` AI runtime entry boundary
- `M16.2` AI context packaging from governed engine inputs

A generation-mode request must consume a validated M16.2 context package.

It may select an approved output family and an approved generation mode only when the selection is aligned with:

- the runtime job family
- the output family
- the generation mode family map
- the declared standards guardrail context
- the evidence status required by the selected mode

## Supported document output families

- `urs_document`
- `dcf_document`
- `protocol_document`
- `report_document`

## Supported reporting output families

- `status_summary_reporting`
- `dashboard_summary_reporting`
- `exception_narrative_reporting`

## Supported generation modes

### `strong_structured_input_fill`

Use when structured and contract inputs are validated enough to fill candidate language without bounded invention.

Rules:

- bounded invention is not allowed
- all generation-eligible context must be validated
- placeholder policy remains required for any unavailable field
- output remains candidate language only

### `partial_input_bounded_completion`

Use when some governed inputs are partial but sufficient for bounded completion.

Rules:

- bounded invention is allowed only inside the selected document/report family rules
- assumptions must be labeled
- placeholders must be used where truth is missing
- no standards, evidence, execution truth, or source truth may be invented

### `minimal_input_scaffold_generation`

Use when the system may create a governed scaffold but cannot claim unverified evidence.

Rules:

- bounded invention is allowed only for scaffold structure and neutral candidate wording
- assumptions must be labeled
- placeholders must be used for missing facts
- no evidence claims may be created without governed context

### `evidence_bound_report_narrative`

Use for narrative reporting where validated evidence exists.

Rules:

- bounded invention is not allowed
- all generation-eligible context must be validated
- reporting language must narrate governed evidence without adding new claims

### `bounded_report_summary`

Use for bounded status or dashboard summary language.

Rules:

- bounded invention is not allowed
- all generation-eligible context must be validated
- summary language must remain tied to governed reporting inputs

## Standards-aware generation control

Every generation-mode request must declare a version-pinned `standards_guardrail_ref`.

The declared ref must match a generation-eligible context item with source family:

```text
standards_guardrail_context
```

The AI runtime may use the declared standards guardrail context only as governed context.
It may not invent standards, replace standards, or treat support context as standards authority.

## Bounded invention policy

Bounded invention is mode-specific.

When allowed, it remains limited to controlled candidate wording, structure, neutral bridge text, labeled assumptions, and placeholder handling.

Bounded invention never grants authority to:

- create source truth
- create execution truth
- invent evidence
- invent standards
- mutate workflow state
- approve output
- release downstream work

## Repo implementation

M16.3 adds:

- `asbp/ai_runtime/generation_modes.py`
- `tests/test_ai_runtime_generation_modes.py`

M16.3 updates:

- `asbp/ai_runtime/__init__.py`

M16.3 records supporting rules at:

- `docs/design_spec/ai_runtime/M16_3_GENERATION_MODE_RULES.yaml`

## Validation expectation

Because M16.3 introduces Python validation helpers and tests, run:

```powershell
python -m pytest -q
```

## Checkpoint decision

M16.3 creates the controlled generation-mode selection boundary only.

The project should not proceed to `M16.4` output acceptance, bounded retry, and fallback behavior until this boundary is applied, tested, committed, pushed, and accepted.
