# M17_UAT_PROTOCOL

## Milestone

Milestone 17 — AI Evaluation, Retrieval Use Rules, and Quality Gates

## Checkpoint

M17.6 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 17 AI evaluation, quality, groundedness, standards/detail, and retrieval-use governance boundary.

The protocol verifies that the M17 implementation is understandable, bounded, deterministic, validated, and acceptable for forward roadmap progression into M17.7 closeout.

## UAT Scope

This UAT covers the Milestone 17 implementation boundary through:

- M17.1 — AI evaluation baseline and regression harness
- M17.2 — Quality gates and groundedness checks
- M17.3 — Standards-conformance and detail-level consistency checks
- M17.4 — Retrieval-use rules and source-role discipline
- M17.5 — Validation checkpoint

## Prerequisites

- `M17.1` through `M17.4` implementation/checkpoint evidence is complete.
- `M17.5` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `835 passed in 50.02s`
- Validation evidence exists at:
  - `docs/milestones/M17/M17_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the completed M17.5 validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 17 is acceptable as an AI evaluation and governance boundary over the completed M16 AI runtime layer, not as actual LLM execution, prompt-template generation, document generation, document template/product implementation, recommendation behavior, UI/API behavior, workflow mutation, approval, or release authority.

## UAT Checks

### UAT-17-01 — AI evaluation baseline and regression harness

Confirm that Milestone 17 defines a measurable AI evaluation baseline and deterministic regression harness.

Expected result:

- Evaluation families are explicit.
- Baseline dimensions are explicit.
- Regression case and regression run results are deterministic.
- Regression harness compares expected acceptance decisions against validated M16 output-acceptance decisions.
- The baseline does not implement quality gates, groundedness checks, standards/detail checks, retrieval-use governance, recommendation behavior, UI/API behavior, workflow mutation, approval, or release behavior.

### UAT-17-02 — Quality gates and groundedness checks

Confirm that AI output quality gates and groundedness checks are bounded, deterministic, and fail closed.

Expected result:

- Quality gate result is deterministic.
- Groundedness result is deterministic.
- Evidence-link result is deterministic.
- Source-role result is deterministic.
- Attractive but ungrounded output fails the quality gate.
- Evidence claims must be supported.
- Required assumptions must be labeled.
- Missing truth must use explicit placeholders.
- Source-role discipline is preserved.
- Quality gates do not call an LLM, generate documents, mutate workflow state, approve, release, or reopen document template/product implementation.

### UAT-17-03 — Standards-conformance and detail-level consistency checks

Confirm that standards-conformance and detail-level consistency checks consume governed document-engine guardrail structures.

Expected result:

- Standards-conformance checks are deterministic.
- Detail-level consistency checks are deterministic.
- M17.3 consumes the closed M12 standards/language/evidence guardrail boundary.
- Required sections, allowed sections, standards refs, evidence refs, inference refs, assumptions, placeholders, and prohibited language patterns are checked through governed structures.
- M17.3 does not perform external clause-by-clause GMP standards judgment.
- M17.3 does not reopen document template/product implementation or actual document generation from expanded library content.

### UAT-17-04 — Retrieval-use rules and source-role discipline

Confirm that AI retrieval-use rules preserve governed retrieval and support-retrieval authority boundaries.

Expected result:

- M17.4 consumes the closed M14.5 governed retrieval/support-retrieval boundary.
- Governed retrieval remains version-pinned and governed.
- Support retrieval remains non-authoritative context only.
- Support retrieval cannot become source truth.
- Support retrieval cannot become execution truth.
- Support retrieval cannot become compiled lookup authority.
- Support retrieval cannot become approval truth, release truth, or workflow mutation authority.
- Resolver bypass, source-truth override, execution-truth override, and mixed authority states fail closed.
- M17.4 does not implement vector search, embeddings, external web search, asset payload loading, document generation, recommendation behavior, UI/API behavior, workflow mutation, approval, or release behavior.

### UAT-17-05 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/milestones/M17/M17_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `835 passed in 50.02s`
- No unresolved validation defect is identified for the M17 boundary.

### UAT-17-06 — Phase 6 boundary discipline and downstream readiness

Confirm that M17 remains correctly positioned inside Phase 6 without expanding into later AI-layer milestones or product implementation work.

Expected result:

- M17 establishes AI evaluation, quality gates, standards/detail checks, and retrieval-use governance only.
- M18 AI-assisted review/summarization/recommendation expansion remains future work.
- UI/API, cloud/compute, and productization remain later phases.
- Document template/product implementation remains deferred to a post-M17, pre-M18 decision gate.
- M17 is ready for milestone closeout after UAT acceptance.

## Acceptance Criteria

Milestone 17 UAT may pass only if all of the following are true:

- AI evaluation is measurable and deterministic.
- Quality gates fail closed for attractive but ungrounded output.
- Standards/detail checks consume governed M12 guardrail structures.
- Retrieval-use rules consume the M14.5 retrieval boundary.
- Support retrieval stays non-authoritative.
- No source truth, execution truth, validation truth, approval, release, workflow mutation, recommendation behavior, or UI/API authority is created.
- Actual LLM calls, prompt templates, document generation, document template/product implementation, and external clause-by-clause GMP standards judgment remain out of scope.
- Latest validation evidence is green.
- No unresolved UAT blocker is identified.

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M17/M17_UAT_REPORT.md`

## Recorded On

2026-05-09
