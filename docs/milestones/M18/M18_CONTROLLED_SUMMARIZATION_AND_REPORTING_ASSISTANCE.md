---
doc_type: milestone_checkpoint_evidence
canonical_name: M18_CONTROLLED_SUMMARIZATION_AND_REPORTING_ASSISTANCE
status: IMPLEMENTED_PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_only
checkpoint: M18.2
milestone: M18
phase: Phase 6 — AI Layer
---

# M18.2 — Controlled Summarization and Reporting Assistance

## Checkpoint

`M18.2` — Controlled summarization and reporting assistance

## Purpose

This checkpoint introduces the second governed AI-assisted workflow expansion boundary.

The M18.2 boundary supports bounded summarization assistance and bounded reporting assistance as advisory metadata only.

It does not create approval authority, release authority, workflow mutation authority, actual document-generation authority, actual report-generation authority, product-ready report rendering, recommendation behavior, prompt-template behavior, direct LLM execution, or validation/UAT truth.

## Implemented Boundary

M18.2 introduces the `asbp.ai_workflow.summarization_reporting` boundary.

The boundary provides:

- controlled summarization/reporting baseline
- controlled summarization/reporting request construction
- controlled summarization/reporting request validation
- controlled summarization/reporting finding construction
- controlled summarization/reporting finding validation
- controlled summarization/reporting result construction
- controlled summarization/reporting result validation
- package exports through `asbp.ai_workflow`

## Source Dependencies

Controlled summarization and reporting assistance consumes already-closed upstream evidence and does not redefine it.

It relies on:

- M16 governed AI runtime and output-acceptance contracts
- M17 quality-gate and groundedness evidence
- M17 source-role and evidence discipline
- M18.1 controlled review-assistance boundary patterns
- the post-M17 / pre-M18 decision-gate record for deferred document template/product implementation scope

The source quality gate must pass before controlled summarization/reporting assistance may proceed.

If the source quality gate fails, the controlled summarization/reporting request fails closed.

## Summary Target Families

Supported summary target families are:

- `document_artifact_summary_target`
- `reporting_artifact_summary_target`
- `workflow_state_summary_target`
- `ai_output_summary_target`

These are summary/reporting assistance targets only.

They do not create direct document generation, report generation, workflow mutation, approval, release, recommendation, or product-ready rendering behavior.

## Summarization Modes

Supported summarization modes are:

- `evidence_bound_summarization`
- `contract_aligned_summarization`
- `gap_and_risk_summarization`

The summarization mode controls the classification of advisory summarization assistance only.

It does not authorize free-form summarization, document generation, report generation, recommendation behavior, approval, release, state mutation, or downstream product rendering.

## Reporting Assistance Modes

Supported reporting assistance modes are:

- `status_summary_reporting`
- `detail_discipline_reporting`
- `evidence_trace_reporting`

The reporting assistance mode controls the classification of advisory reporting assistance only.

It does not authorize actual report generation, export rendering, dashboard rendering, product-ready output, validation truth, UAT truth, recommendation behavior, or workflow mutation.

## Advisory Authority Rule

Controlled summarization/reporting assistance is advisory only.

The AI summarization/reporting result cannot:

- approve
- release
- mutate workflow state
- claim validation truth
- claim UAT truth
- generate documents
- generate reports
- render product-ready reports
- create approval payloads
- create release payloads
- create workflow mutation payloads
- create recommendation payloads
- replace human review
- replace CQV/GMP acceptance judgment

## Evidence and Source-Role Discipline

Controlled summarization/reporting requests must be tied to a passing M17 quality-gate result.

Summary evidence references and source-truth references must be drawn from the passed source quality-gate payload.

References outside the passed quality-gate scope are rejected.

Summarization/reporting findings must also reference evidence and source references inside the controlled summarization/reporting request scope.

## Findings

Supported summarization/reporting finding categories include:

- `summary_contract_alignment_finding`
- `summary_evidence_gap_finding`
- `summary_assumption_labeling_finding`
- `summary_source_role_discipline_finding`
- `reporting_detail_discipline_finding`
- `summary_report_approval_authority_boundary_finding`
- `summary_report_workflow_state_mutation_boundary_finding`
- `summary_report_document_generation_boundary_finding`
- `summary_report_report_generation_boundary_finding`
- `summary_report_product_rendering_boundary_finding`
- `summary_report_recommendation_boundary_finding`
- `summary_report_validation_truth_boundary_finding`

Boundary-protection findings allow the summarization/reporting layer to identify out-of-scope pressure without implementing out-of-scope behavior.

## Deferred Scope Protection

The following remain out of scope for M18.2:

- document factory
- document template/product implementation
- actual document generation from expanded governed library content
- actual report generation from expanded governed library content
- product-ready document rendering
- product-ready report rendering
- recommendation behavior
- workflow state mutation
- approval or release authority
- validation or UAT truth claims
- actual LLM calls
- prompt templates
- UI/API behavior
- cloud or SaaS productization

This preserves the explicit post-M17 / pre-M18 decision that deferred document template/product implementation beyond `M18`.

## Repo Evidence

Implemented files:

- `asbp/ai_workflow/__init__.py`
- `asbp/ai_workflow/summarization_reporting.py`
- `tests/test_ai_summarization_reporting.py`
- `docs/design_spec/ai_workflow/M18_2_CONTROLLED_SUMMARIZATION_AND_REPORTING_ASSISTANCE_RULES.yaml`
- `docs/milestones/M18/M18_CONTROLLED_SUMMARIZATION_AND_REPORTING_ASSISTANCE.md`

## Validation Status

Pending local validation after applying this implementation package.

Expected validation command:

```powershell
python -m pytest -q
```

## Completion Decision

Pending validation.

`M18.2` must not be marked complete until local validation passes and the tracker is updated with verified evidence.

## Next Expected Checkpoint After Validation

`M18.3` — Controlled recommendation behavior
