---
doc_type: milestone_checkpoint_evidence
canonical_name: M18_WORKFLOW_EXPANSION_BOUNDARIES_AND_REFUSAL_RULES
status: IMPLEMENTED_PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_only
checkpoint: M18.4
milestone: M18
phase: Phase 6 — AI Layer
---

# M18.4 — Workflow-Expansion Boundaries and Refusal Rules

## Checkpoint

`M18.4` — Workflow-expansion boundaries and refusal rules

## Purpose

This checkpoint introduces the final governed capability boundary before M18 validation, UAT, and closeout.

The M18.4 boundary defines what AI-assisted workflow expansion is allowed to do, what remains explicitly out of scope, and how requests must fail closed or fall back when they exceed governed boundaries.

It prevents M18 workflow expansion from becoming uncontrolled agentic behavior.

## Implemented Boundary

M18.4 introduces the `asbp.ai_workflow.workflow_expansion_boundaries` boundary.

The boundary provides:

- workflow-expansion boundary baseline
- workflow-expansion boundary request construction
- workflow-expansion boundary request validation
- deterministic workflow-expansion request classification
- workflow-expansion boundary decision construction
- workflow-expansion boundary decision validation
- deterministic refusal reasons
- deterministic fallback reasons
- package exports through `asbp.ai_workflow`

## Source Dependencies

Workflow-expansion boundary decisions consume already-closed upstream evidence and do not redefine it.

They rely on:

- M16 governed AI runtime and output-acceptance contracts
- M17 quality-gate and groundedness evidence
- M17 retrieval-use and source-role discipline
- M18.1 controlled review-assistance boundary
- M18.2 controlled summarization/reporting boundary
- M18.3 controlled recommendation boundary
- the post-M17 / pre-M18 decision-gate record for deferred document template/product implementation scope

The source quality gate must pass before workflow-expansion boundary handling may proceed.

## Allowed Workflow-Expansion Request Families

Allowed request families are bounded to advisory metadata and routing decisions:

- `controlled_review_assistance_request`
- `controlled_summarization_reporting_assistance_request`
- `controlled_recommendation_assistance_request`
- `evidence_source_role_discipline_request`
- `boundary_finding_metadata_request`
- `human_review_handoff_request`

Allowed families may route to existing bounded M18 assistance surfaces.

They do not create approval authority, release authority, workflow mutation authority, action execution authority, document generation, report generation, product rendering, prompt-template behavior, direct LLM execution, validation truth, UAT truth, or UI/API/cloud/SaaS behavior.

## Fallback-Only Request Families

Fallback-only request families are:

- `insufficient_evidence_fallback_request`
- `non_authoritative_source_fallback_request`
- `missing_contract_context_fallback_request`

Fallback-only requests may emit deterministic fallback metadata and must require human review.

## Out-of-Scope Request Families

Out-of-scope request families are refused:

- `approval_or_release_request`
- `workflow_state_mutation_request`
- `action_execution_request`
- `autonomous_agentic_behavior_request`
- `document_generation_request`
- `report_generation_request`
- `product_ready_rendering_request`
- `prompt_template_request`
- `direct_llm_call_request`
- `validation_or_uat_truth_request`
- `ui_api_cloud_productization_request`

## Refusal and Fallback Rules

Workflow-expansion decisions are deterministic:

- allowed governed families return `workflow_expansion_allowed`
- fallback-only families return `workflow_expansion_fallback_only`
- out-of-scope or unsupported families return `workflow_expansion_refused`
- out-of-scope flags on otherwise allowed families force refusal
- refusal and fallback reasons must match the request classification exactly
- every decision remains advisory and requires human review

## Authority Rule

The workflow-expansion boundary cannot:

- approve
- release
- mutate workflow state
- execute actions
- run autonomously
- replace human decision-making
- generate documents
- generate reports
- render product-ready outputs
- create prompt templates
- call an LLM directly
- claim validation truth
- claim UAT truth
- create UI/API/cloud/SaaS behavior

## Deferred Scope Protection

The following remain out of scope for M18.4:

- actual LLM calls
- prompt templates
- document factory
- actual document generation from expanded governed library content
- actual report generation from expanded governed library content
- product-ready document rendering
- product-ready report rendering
- workflow state mutation
- action execution
- autonomous agentic behavior
- approval or release authority
- validation or UAT truth claims
- UI/API behavior
- cloud or SaaS productization
- M18 validation checkpoint
- M18 UAT checkpoint
- M18 closeout

## Repo Evidence

Implemented files:

- `asbp/ai_workflow/__init__.py`
- `asbp/ai_workflow/workflow_expansion_boundaries.py`
- `tests/test_ai_workflow_expansion_boundaries.py`
- `docs/design_spec/ai_workflow/M18_4_WORKFLOW_EXPANSION_BOUNDARIES_AND_REFUSAL_RULES.yaml`
- `docs/M18_WORKFLOW_EXPANSION_BOUNDARIES_AND_REFUSAL_RULES.md`

## Validation Status

Pending local validation after applying this implementation package.

Expected validation command:

```powershell
python -m pytest -q
```

## Completion Decision

Pending validation.

`M18.4` must not be marked complete until local validation passes and the tracker is updated with verified evidence.

## Next Expected Checkpoint After Validation

`M18.5` — Validation checkpoint
