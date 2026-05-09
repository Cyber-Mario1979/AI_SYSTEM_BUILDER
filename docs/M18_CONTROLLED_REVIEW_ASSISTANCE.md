---
doc_type: milestone_checkpoint_evidence
canonical_name: M18_CONTROLLED_REVIEW_ASSISTANCE
status: IMPLEMENTED_PENDING_VALIDATION
governs_execution: false
document_state_mode: checkpoint_evidence
authority: implementation_evidence_only
checkpoint: M18.1
milestone: M18
phase: Phase 6 — AI Layer
---

# M18.1 — Controlled Review Assistance

## Checkpoint

`M18.1` — Controlled review assistance

## Purpose

This checkpoint introduces the first governed AI-assisted workflow expansion boundary.

The M18.1 boundary supports controlled review assistance as advisory metadata only.

It does not create approval authority, release authority, workflow mutation authority, document-generation authority, document-template product implementation, document factory behavior, or library-architecture remediation behavior.

## Implemented Boundary

M18.1 introduces the `asbp.ai_workflow.review_assistance` boundary.

The boundary provides:

- controlled review-assistance baseline
- controlled review request construction
- controlled review request validation
- controlled review finding construction
- controlled review finding validation
- controlled review assistance result construction
- controlled review assistance result validation
- package exports through `asbp.ai_workflow`

## Source Dependencies

Controlled review assistance consumes already-closed upstream evidence and does not redefine it.

It relies on:

- M16 governed AI runtime and output-acceptance contracts
- M17 quality-gate and groundedness evidence
- M17 source-role and evidence discipline
- the post-M17 / pre-M18 decision-gate record for deferred document template/product implementation scope

The source quality gate must pass before controlled review assistance may proceed.

If the source quality gate fails, the controlled review request fails closed.

## Review Target Families

Supported review target families are:

- `document_artifact_review_target`
- `reporting_artifact_review_target`
- `workflow_state_review_target`
- `ai_output_review_target`

These are review targets only.

They do not create direct document generation, report generation, workflow mutation, approval, or release behavior.

## Review Modes

Supported review modes are:

- `evidence_bound_review`
- `contract_alignment_review`
- `gap_and_risk_review`

The review mode controls the classification of advisory review assistance only.

It does not authorize generation, approval, release, state mutation, recommendation behavior, or downstream product rendering.

## Advisory Authority Rule

Controlled review assistance is advisory only.

The AI review result cannot:

- approve
- release
- mutate workflow state
- claim validation truth
- claim UAT truth
- create approval payloads
- create release payloads
- create workflow mutation payloads
- replace human review
- replace CQV/GMP acceptance judgment

## Evidence and Source-Role Discipline

Controlled review requests must be tied to a passing M17 quality-gate result.

Review evidence references and source-truth references must be drawn from the passed source quality-gate payload.

References outside the passed quality-gate scope are rejected.

Review findings must also reference evidence and source references inside the controlled review request scope.

## Findings

Supported review finding categories include:

- `contract_alignment_finding`
- `evidence_gap_finding`
- `assumption_labeling_finding`
- `source_role_discipline_finding`
- `approval_authority_boundary_finding`
- `workflow_state_mutation_boundary_finding`
- `document_generation_boundary_finding`
- `document_template_product_boundary_finding`
- `library_architecture_deferred_scope_finding`

The final three categories are deliberate boundary-protection findings.

They allow the review layer to identify deferred-scope pressure without implementing deferred-scope behavior.

## Deferred Scope Protection

The following remain out of scope for M18.1:

- document factory
- document template/product implementation
- actual document generation from expanded governed library content
- product-ready document rendering
- library architecture cleanup
- profile/calendar/common-library reorganization
- actual LLM calls
- prompt templates
- UI/API behavior
- cloud or SaaS productization

This protects the explicit post-M17 / pre-M18 decision that deferred document template/product implementation beyond `M18`.

## Repo Evidence

Implemented files:

- `asbp/ai_workflow/__init__.py`
- `asbp/ai_workflow/review_assistance.py`
- `tests/test_ai_review_assistance.py`
- `docs/design_spec/ai_workflow/M18_1_CONTROLLED_REVIEW_ASSISTANCE_RULES.yaml`
- `docs/M18_CONTROLLED_REVIEW_ASSISTANCE.md`

## Validation Status

Validation is pending.

The expected validation command is:

```powershell
python -m pytest -q
```

The latest previously recorded validation result remains:

```text
835 passed in 50.02s
```

This document must not be used as proof of passing validation until the validation command is run and recorded.

## Next Expected Step

Run validation:

```powershell
python -m pytest -q
```

If validation passes, update `PROGRESS_TRACKER.md` to mark `M18.1` complete and set `M18.2` as the exact next unfinished checkpoint.
