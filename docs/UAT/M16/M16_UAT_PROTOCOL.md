# M16_UAT_PROTOCOL

## Milestone

Milestone 16 — AI Runtime for Governed Document and Reporting Workflows

## Checkpoint

M16.6 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 16 governed AI runtime boundary.

The protocol verifies that the M16 implementation is understandable, bounded, deterministic, validated, and acceptable for forward roadmap progression into M16.7 closeout.

## UAT Scope

This UAT covers the Milestone 16 implementation boundary through:

- M16.1 — AI runtime boundary for document/reporting jobs
- M16.2 — Context packaging from governed engine inputs
- M16.3 — Controlled generation modes for document/reporting families
- M16.4 — Output acceptance, bounded retry, and fallback behavior
- M16.5 — Validation checkpoint

## Prerequisites

- `M16.1` through `M16.4` implementation/checkpoint evidence is complete.
- `M16.5` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `792 passed in 42.79s`
- Validation evidence exists at:
  - `docs/milestones/M16/M16_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the completed M16.5 validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 16 is acceptable as a governed AI runtime boundary over completed document/reporting workflows, not as actual LLM execution, prompt-template generation, AI evaluation, retrieval-use governance, recommendation behavior, UI/API behavior, workflow mutation, approval, or release authority.

## UAT Checks

### UAT-16-01 — AI runtime entry boundary

Confirm that Milestone 16 defines a bounded AI runtime entry boundary for governed document/reporting jobs.

Expected result:

- Supported job families are explicit.
- Supported caller boundaries are explicit.
- Supported model permission profiles are explicit.
- AI output roles remain candidate/supporting output roles only.
- AI runtime cannot own source truth, execution truth, validation truth, approval, release, or workflow mutation authority.
- Actual LLM calls and prompt templates remain out of scope.

### UAT-16-02 — Context packaging and source-role clarity

Confirm that governed engine inputs can be packaged for AI runtime use without changing source authority.

Expected result:

- Context source families are explicit.
- Context source roles are explicit.
- Payload classifications are explicit.
- Evidence statuses are explicit.
- Required document/reporting context families are enforced.
- Support context cannot be promoted into authority.
- Context packages cannot define execution truth.
- Raw prompts, prompt templates, direct LLM call fields, and state mutation payloads remain blocked.

### UAT-16-03 — Controlled generation-mode contracts

Confirm that controlled generation modes are bounded by document/reporting family and evidence requirements.

Expected result:

- Supported document output families are explicit.
- Supported reporting output families are explicit.
- Supported generation modes are explicit.
- Generation modes are validated against output family and job family.
- Standards guardrail context is required and version-pinned.
- Bounded invention is mode-specific, labeled where allowed, and never creates source truth, execution truth, standards truth, or evidence truth.
- Generation-mode requests do not generate document/report text and do not accept, retry, or fallback outputs.

### UAT-16-04 — Output acceptance, bounded retry, and fallback behavior

Confirm that candidate AI output handling is bounded, fail-closed, and isolated from workflow authority.

Expected result:

- Candidate output acceptance rules are explicit.
- Output acceptance fails closed when required evidence or contract rules are missing.
- Bounded retry behavior is explicit and limited.
- Fallback/refusal behavior exists when evidence is insufficient or contract rules are broken.
- Accepted candidate output does not approve documents, mutate workflow state, release tasks, or bypass downstream review.
- Output acceptance does not implement AI evaluation, retrieval-use governance, recommendation behavior, UI/API behavior, or actual LLM execution.

### UAT-16-05 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/milestones/M16/M16_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `792 passed in 42.79s`
- No unresolved validation defect is identified for the M16 boundary.

### UAT-16-06 — Phase 6 boundary discipline

Confirm that M16 remains correctly positioned inside Phase 6 without expanding into later AI-layer milestones.

Expected result:

- M16 establishes governed AI runtime behavior only.
- M17 AI evaluation, retrieval-use rules, and quality gates remain future work.
- M18 AI-assisted review/summarization/recommendation expansion remains future work.
- UI/API, cloud/compute, and productization remain later phases.
- M16 is ready for milestone closeout after UAT acceptance.

## Acceptance Criteria

Milestone 16 UAT may pass only if all of the following are true:

- AI runtime entry boundary is explicit and bounded
- context packaging preserves source-role clarity
- controlled generation modes are family-specific and standards-aware
- output acceptance is fail-closed and candidate-output-only
- retry and fallback behavior are bounded
- AI runtime does not own source truth, execution truth, validation truth, approval, release, or workflow mutation authority
- actual LLM calls, prompt templates, AI evaluation, retrieval-use governance, recommendation behavior, and UI/API behavior remain out of scope
- latest validation evidence is green
- no unresolved UAT blocker is identified

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M16/M16_UAT_REPORT.md`

## Recorded On

2026-05-06
