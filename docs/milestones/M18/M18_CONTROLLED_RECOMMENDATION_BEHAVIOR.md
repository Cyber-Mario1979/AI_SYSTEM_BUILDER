---
doc_type: milestone_checkpoint_evidence
canonical_name: M18_CONTROLLED_RECOMMENDATION_BEHAVIOR
status: IMPLEMENTED_PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_only
checkpoint: M18.3
milestone: M18
phase: Phase 6 — AI Layer
---

# M18.3 — Controlled Recommendation Behavior

## Checkpoint

`M18.3` — Controlled recommendation behavior

## Purpose

This checkpoint introduces the third governed AI-assisted workflow expansion boundary.

The M18.3 boundary supports bounded recommendation and suggestion behavior as advisory metadata only.

It does not create approval authority, release authority, workflow mutation authority, action execution authority, autonomous agentic behavior, actual document-generation authority, actual report-generation authority, product-ready rendering, prompt-template behavior, direct LLM execution, validation truth, or UAT truth.

## Implemented Boundary

M18.3 introduces the `asbp.ai_workflow.recommendation_behavior` boundary.

The boundary provides:

- controlled recommendation-behavior baseline
- controlled recommendation request construction
- controlled recommendation request validation
- controlled recommendation item construction
- controlled recommendation item validation
- controlled recommendation boundary-finding construction
- controlled recommendation boundary-finding validation
- controlled recommendation result construction
- controlled recommendation result validation
- package exports through `asbp.ai_workflow`

## Source Dependencies

Controlled recommendation behavior consumes already-closed upstream evidence and does not redefine it.

It relies on:

- M16 governed AI runtime and output-acceptance contracts
- M17 quality-gate and groundedness evidence
- M17 retrieval-use and source-role discipline
- M18.1 controlled review-assistance boundary patterns
- M18.2 controlled summarization/reporting boundary patterns
- the post-M17 / pre-M18 decision-gate record for deferred document template/product implementation scope

The source quality gate must pass before controlled recommendation behavior may proceed.

If the source quality gate fails, the controlled recommendation request fails closed.

## Recommendation Target Families

Supported recommendation target families are:

- `document_artifact_recommendation_target`
- `reporting_artifact_recommendation_target`
- `workflow_state_recommendation_target`
- `ai_output_recommendation_target`

These are recommendation-assistance targets only.

They do not create direct document generation, report generation, workflow mutation, approval, release, action execution, validation truth, UAT truth, or product-ready rendering behavior.

## Recommendation Modes

Supported recommendation modes are:

- `evidence_bound_recommendation`
- `contract_aligned_recommendation`
- `gap_and_risk_recommendation`

The recommendation mode controls the classification of advisory recommendation behavior only.

It does not authorize free-form advice, approval, release, state mutation, action execution, direct LLM calls, prompt-template behavior, document generation, report generation, or product-ready rendering.

## Supported Recommendation Categories

Supported controlled recommendation categories are:

- `evidence_followup_recommendation`
- `contract_alignment_recommendation`
- `gap_closure_recommendation`
- `risk_mitigation_recommendation`
- `human_review_escalation_recommendation`
- `source_role_discipline_recommendation`
- `detail_discipline_recommendation`
- `workflow_readiness_recommendation`

Each recommendation item is structured metadata only and must require human decision before acceptance.

## Advisory Authority Rule

Controlled recommendation behavior is advisory only.

The AI recommendation result can issue controlled recommendation metadata, but cannot:

- approve
- release
- mutate workflow state
- execute actions
- replace human decision
- claim validation truth
- claim UAT truth
- generate documents
- generate reports
- render product-ready documents
- render product-ready reports
- create approval payloads
- create release payloads
- create workflow mutation payloads
- create action execution payloads
- replace CQV/GMP acceptance judgment

## Evidence and Source-Role Discipline

Controlled recommendation requests must be tied to a passing M17 quality-gate result.

Recommendation evidence references and source-truth references must be drawn from the passed source quality-gate payload.

References outside the passed quality-gate scope are rejected.

Recommendation items and boundary findings must also reference evidence and source references inside the controlled recommendation request scope.

## Boundary Findings

Supported controlled recommendation boundary-finding categories include:

- `recommendation_approval_authority_boundary_finding`
- `recommendation_release_authority_boundary_finding`
- `recommendation_workflow_state_mutation_boundary_finding`
- `recommendation_action_execution_boundary_finding`
- `recommendation_document_generation_boundary_finding`
- `recommendation_report_generation_boundary_finding`
- `recommendation_product_rendering_boundary_finding`
- `recommendation_validation_truth_boundary_finding`
- `recommendation_autonomous_agentic_behavior_boundary_finding`
- `recommendation_ungrounded_action_boundary_finding`

Boundary-protection findings allow the recommendation layer to identify out-of-scope pressure without implementing out-of-scope behavior.

## Deterministic Result Rule

Controlled recommendation result status is deterministic:

- no recommendation items and no boundary findings: `recommendation_assistance_ready`
- one or more recommendation items only: `recommendation_assistance_recommendations_identified`
- one or more boundary findings only: `recommendation_assistance_boundary_findings_identified`
- both recommendation items and boundary findings: `recommendation_assistance_recommendations_and_boundary_findings_identified`

## Deferred Scope Protection

The following remain out of scope for M18.3:

- document factory
- document template/product implementation
- actual document generation from expanded governed library content
- actual report generation from expanded governed library content
- product-ready document rendering
- product-ready report rendering
- workflow state mutation
- action execution
- autonomous agentic behavior
- approval or release authority
- validation or UAT truth claims
- actual LLM calls
- prompt templates
- UI/API behavior
- cloud or SaaS productization

This preserves the explicit post-M17 / pre-M18 decision that deferred document template/product implementation beyond `M18` and preserves the M18.4 boundary/refusal checkpoint for later workflow-expansion boundary consolidation.

## Repo Evidence

Implemented files:

- `asbp/ai_workflow/__init__.py`
- `asbp/ai_workflow/recommendation_behavior.py`
- `tests/test_ai_recommendation_behavior.py`
- `docs/design_spec/ai_workflow/M18_3_CONTROLLED_RECOMMENDATION_BEHAVIOR_RULES.yaml`
- `docs/milestones/M18/M18_CONTROLLED_RECOMMENDATION_BEHAVIOR.md`

## Validation Status

Pending local validation after applying this implementation package.

Expected validation command:

```powershell
python -m pytest -q
```

## Completion Decision

Pending validation.

`M18.3` must not be marked complete until local validation passes and the tracker is updated with verified evidence.

## Next Expected Checkpoint After Validation

`M18.4` — Workflow-expansion boundaries and refusal rules
