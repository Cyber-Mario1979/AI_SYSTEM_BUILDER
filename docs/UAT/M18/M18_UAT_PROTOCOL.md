# M18_UAT_PROTOCOL

## Milestone

Milestone 18 — AI-Assisted Workflow Expansion

## Checkpoint

M18.6 — Milestone UAT checkpoint

## Protocol Status

Approved for execution

## Purpose

This protocol defines the minimal operator-facing and project-owner-facing UAT checks required to accept the Milestone 18 AI-assisted workflow expansion boundary.

The protocol verifies that the M18 implementation is understandable, bounded, deterministic, validated, and acceptable for forward roadmap progression into M18.7 closeout.

## UAT Scope

This UAT covers the Milestone 18 implementation boundary through:

- M18.1 — Controlled review assistance
- M18.2 — Controlled summarization and reporting assistance
- M18.3 — Controlled recommendation behavior
- M18.4 — Workflow-expansion boundaries and refusal rules
- M18.5 — Validation checkpoint

## Prerequisites

- `M18.1` through `M18.4` implementation/checkpoint evidence is complete.
- `M18.5` validation checkpoint is complete.
- Latest validation result is green:
  - `python -m pytest -q` — `885 passed in 42.73s`
- Validation evidence exists at:
  - `docs/milestones/M18/M18_VALIDATION_CHECKPOINT.md`

## UAT Method

Review the milestone behavior from an operator-facing and project-owner-facing perspective.

This UAT does not require new code execution beyond the completed M18.5 validation checkpoint unless a defect is identified during review.

The review confirms that Milestone 18 is acceptable as a bounded AI-assisted workflow expansion layer over the completed M16 AI runtime and M17 quality/retrieval governance boundaries, not as actual LLM execution, prompt-template generation, document generation, report generation, product-ready rendering, workflow mutation, approval, release, UI/API, cloud, SaaS/productization, or uncontrolled autonomous agent behavior.

## UAT Checks

### UAT-18-01 — Controlled review assistance

Confirm that controlled review assistance is bounded, advisory, and evidence/source-role disciplined.

Expected result:

- Review assistance supports governed review target families.
- Review modes are explicit and deterministic.
- Review findings are metadata-only.
- Review evidence refs and source refs stay inside the passed source quality-gate scope.
- Review assistance requires a passing M17 quality-gate result.
- Review assistance does not approve, release, mutate workflow state, generate documents, implement document templates/products, change library architecture, call an LLM, or create prompt templates.

### UAT-18-02 — Controlled summarization and reporting assistance

Confirm that controlled summarization/reporting assistance is bounded, advisory, and detail-disciplined.

Expected result:

- Summary target families are explicit.
- Summarization modes and reporting assistance modes are explicit.
- Summary/report findings are metadata-only.
- Summary evidence refs and source refs stay inside the passed source quality-gate scope.
- Summarization/reporting assistance requires a passing M17 quality-gate result.
- Summarization/reporting assistance preserves document/report family rules, evidence traceability, source-role discipline, and detail discipline.
- Summarization/reporting assistance does not generate documents, generate reports, render product-ready outputs, approve, release, mutate workflow state, issue recommendations, call an LLM, create prompt templates, or claim validation/UAT truth.

### UAT-18-03 — Controlled recommendation behavior

Confirm that controlled recommendation behavior is bounded, advisory, and human-decision dependent.

Expected result:

- Recommendation target families are explicit.
- Recommendation modes, categories, priorities, and boundary-finding categories are explicit.
- Recommendation items are metadata-only and require human decision.
- Recommendation item refs and boundary-finding refs stay inside the controlled recommendation request scope.
- Recommendation behavior requires a passing M17 quality-gate result.
- Recommendation behavior may identify bounded evidence, contract, gap, risk, human-review, source-role, detail-discipline, or workflow-readiness suggestions.
- Recommendation behavior does not approve, release, mutate workflow state, execute actions, replace human decisions, generate documents, generate reports, render product-ready outputs, call an LLM, create prompt templates, or claim validation/UAT truth.

### UAT-18-04 — Workflow-expansion boundaries and refusal rules

Confirm that workflow-expansion boundaries deterministically classify allowed, refused, and fallback-only requests.

Expected result:

- Allowed workflow-expansion families stay inside M18 bounded advisory surfaces.
- Out-of-scope workflow-expansion families are explicit.
- Refusal/fallback reasons are explicit and deterministic.
- Requests outside governed M18 boundaries fail closed or produce bounded refusal/fallback metadata.
- Workflow-expansion behavior does not become uncontrolled agentic behavior.
- Workflow-expansion behavior does not approve, release, mutate workflow state, execute actions, generate documents, generate reports, render product-ready outputs, create prompt templates, call an LLM, implement UI/API, implement cloud/SaaS behavior, or claim validation/UAT truth.

### UAT-18-05 — Validation evidence alignment

Confirm that technical validation supports milestone acceptance.

Expected result:

- `docs/milestones/M18/M18_VALIDATION_CHECKPOINT.md` records successful validation.
- Latest validation result is:
  - `python -m pytest -q` — `885 passed in 42.73s`
- No unresolved validation defect is identified for the M18 boundary.

### UAT-18-06 — Phase 6 boundary discipline and downstream readiness

Confirm that M18 remains correctly positioned inside Phase 6 without expanding into later UI/API, cloud, or SaaS/productization work.

Expected result:

- M18 establishes bounded AI-assisted review, summarization/reporting, recommendation, and workflow-expansion refusal behavior only.
- M18 remains downstream from the completed M16 AI runtime boundary and M17 quality/retrieval governance boundary.
- UI/API, cloud/compute, and productization remain later phases.
- Document template/product implementation and actual document generation from expanded governed library content remain deferred beyond M18.
- M18 is ready for milestone closeout after UAT acceptance.

## Acceptance Criteria

Milestone 18 UAT may pass only if all of the following are true:

- Controlled review assistance is bounded, advisory, and evidence/source-role disciplined.
- Controlled summarization/reporting assistance is bounded, advisory, and detail-disciplined.
- Controlled recommendation behavior is bounded, advisory, and human-decision dependent.
- Workflow-expansion boundaries classify allowed, refused, and fallback-only requests deterministically.
- Requests outside governed M18 boundaries fail closed or produce bounded refusal/fallback metadata.
- No source truth, execution truth, validation truth, approval, release, workflow mutation, action execution, document/report generation, product-ready rendering, uncontrolled agentic behavior, UI/API authority, cloud behavior, or SaaS/productization authority is created.
- Actual LLM calls, prompt templates, document template/product implementation, and actual document generation from expanded governed library content remain out of scope.
- Latest validation evidence is green.
- No unresolved UAT blocker is identified.

## Acceptance Decision Options

Allowed UAT decisions:

- pass
- conditional pass
- fail

## UAT Record Location

The executed UAT report must be stored at:

`docs/UAT/M18/M18_UAT_REPORT.md`

## Recorded On

2026-05-10
