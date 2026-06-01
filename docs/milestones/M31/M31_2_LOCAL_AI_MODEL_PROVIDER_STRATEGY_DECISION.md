---
doc_type: checkpoint_evidence
canonical_name: M31_2_LOCAL_AI_MODEL_PROVIDER_STRATEGY_DECISION
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: strategy_decision_evidence
milestone: M31
checkpoint: M31.2
checkpoint_title: Local AI model and provider strategy decision
execution_mode: Governance-only
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m312-strategy-decision
created_date: 2026-06-01
source_baseline_commit: 7f4b5e4beaf995deed3e671e36915f0823305232
live_repo_write: YES_EVIDENCE_SCOPE_ONLY
normal_execution_state: GO_DECISION_EVIDENCE_ONLY
project_owner_acceptance: PENDING
---

# M31.2 — Local AI Model and Provider Strategy Decision

## 1. Purpose

This document records the M31.2 local AI model and provider strategy decision evidence for review.

M31.2 is a governance-only decision checkpoint. It decides the local/offline/API/provider direction, constraints, and downstream gates before any AI model, provider adapter, local runtime, prompt execution, or app-coupled heavy-use testing is implemented.

This document does not implement AI assistance.

## 2. Source Basis

M31.2 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31 checkpoint ladder;
- `PROGRESS_TRACKER.md`, which sets current work to `PLAN M31.2` / `GO BLOCKED` until accepted evidence exists;
- `docs/milestones/M31/M31_1_AI_ASSISTANCE_BOUNDARY_CONFIRMATION_PLAN.md`;
- `docs/milestones/M31/M31_1_AI_ASSISTANCE_BOUNDARY_CONFIRMATION.md`;
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`, especially DDR-007;
- `ARCHITECTURE_GUARDRAILS.md`.

M31.1 confirmed that candidate AI assistance modes may be considered only as governed, reviewable, non-authoritative support modes. It did not authorize model/provider/runtime behavior.

## 3. Decision Status

```text
DRAFT FOR PROJECT OWNER REVIEW.
```

This evidence file records the proposed M31.2 strategy decision. Tracker movement remains blocked until this decision evidence is reviewed and accepted.

## 4. Selected Strategy Path

```text
Selected path: staged local-first / offline-preferred hybrid strategy.
```

The selected strategy is:

1. Prefer a local/offline-capable AI strategy for future local product trial work where feasible.
2. Preserve an external provider/API option only as a later explicitly gated adapter candidate.
3. Keep a no-model fallback available for workflows that can remain deterministic or human-authored.
4. Require all future model/provider/runtime work to pass through explicit adapter, context-packet, refusal, output-acceptance, evaluation, validation, and UAT gates.
5. Treat all AI output as advisory, draft, review, or comparison support until human acceptance rules and output acceptance gates are satisfied.

This strategy is local-first because ASBP is currently building a local integrated CQV product core and because privacy, traceability, source authority, limitation visibility, and controlled testing are more important than early provider capability.

This strategy is hybrid only at the strategy level. It does not authorize dual-runtime implementation, provider fallback logic, external API calls, local inference calls, or prompt execution.

## 5. Rejected or Deferred Paths

| Path | Decision | Reason |
|---|---|---|
| Immediate external provider/API integration | Rejected for M31.2 | Premature under DDR-007; no adapter boundary, context contract, evaluation harness, or operational testing evidence exists yet. |
| Immediate local model/runtime integration | Rejected for M31.2 | Premature under DDR-007; local runtime requirements and app-coupled testing protocol are not yet accepted. |
| Uncontrolled agentic AI execution | Rejected | Violates M31.1 boundary and project anti-drift controls. |
| Retrieval-to-model raw truth injection | Rejected | Violates M30 retrieval non-authority boundary and M31.1 retrieval dependency. |
| No-model-only permanent strategy | Deferred | Useful as fallback, but M31 roadmap expects a model/provider/runtime strategy for later governed assistance where approved. |

## 6. Local / Offline Option Assessment

Local/offline model use is the preferred future direction for controlled trial consideration, subject to later gates.

Allowed in future planning:

- evaluate local runtime candidates;
- define hardware/runtime assumptions;
- define local data handling constraints;
- define offline repeatability expectations;
- define local shakedown metrics;
- define failure capture and issue logging expectations.

Not authorized by M31.2:

- local model installation;
- local inference calls;
- local runtime integration;
- prompt execution;
- app-coupled heavy-use testing;
- claims that the local runtime is ready.

Local/offline strategy risks to carry forward:

- hardware variability;
- model quality limitations;
- maintenance and update control;
- evaluation burden;
- runtime packaging complexity;
- possible need for provider fallback in later phases.

## 7. External Provider / API Option Assessment

External provider/API use remains an optional later candidate, not the default execution path.

Allowed in future planning:

- define provider-neutral adapter boundaries;
- define external data exposure policy;
- define allowed and blocked data classes;
- define cost control rules;
- define provider logging / retention requirements;
- define manual approval requirements for any provider-enabled run.

Not authorized by M31.2:

- API key handling;
- provider calls;
- provider adapter implementation;
- prompt execution;
- provider fallback behavior;
- direct provider access from core, UI, or workflow surfaces;
- product/SaaS-facing AI release.

External provider/API risks to carry forward:

- confidential data exposure;
- vendor retention/logging uncertainty;
- cost unpredictability during heavy use;
- provider dependency;
- rate limits;
- source/context leakage;
- weaker local/offline repeatability.

## 8. No-Model Fallback

The no-model fallback remains an accepted safety path.

Use no-model fallback when:

- source authority is incomplete;
- user data is confidential and external provider authorization is absent;
- local runtime is unavailable;
- evaluation coverage is inadequate;
- output acceptance rules are incomplete;
- the requested task would require AI to make compliance, approval, legal, regulatory, or source-authority claims.

No-model fallback may still allow deterministic workflow, document scaffolding, review checklists, or human-authored content without AI execution.

## 9. Privacy Constraints

| Data class | Default rule |
|---|---|
| Public repo governance documents | May be used in review/planning context when source-traced. |
| Runtime-authoritative product sources | May be used only through governed context packets once authorized. |
| Standards/citation records | Must preserve registry status, applicability limits, citation limits, and no-fabrication rules. |
| User-provided confidential data | Block external provider use unless separately authorized by explicit owner decision. |
| Secrets, credentials, tokens, API keys | Never send to a model. Never include in prompts or context packets. |
| Raw retrieval chunks | Never treat as source truth. Must be packetized with source IDs, versions, limitations, and refusal triggers. |
| Draft/generated outputs | Advisory/draft/review-bound until accepted by human/output acceptance rules. |

## 10. Cost Constraints

Future model/provider/runtime work must define:

- whether paid external provider use is allowed;
- whether local-only operation is required for default trials;
- budget ceilings before heavy-use testing;
- manual approval requirements for provider calls;
- cost logging expectations for repeated runs;
- fallback behavior when budget or rate limits are reached.

M31.2 does not approve spending or provider usage.

## 11. Operational Limits

Future AI work must preserve:

- no autonomous execution;
- no autonomous repo mutation;
- no autonomous tracker movement;
- no direct model calls from core/UI;
- no untracked prompt execution;
- no source-free project claims;
- no AI approval authority;
- no standards-backed legal/regulatory authority;
- no retrieval-backed compliance truth;
- no product/SaaS-facing live AI release.

## 12. Architecture Boundary Impact

Any later model/provider work must remain downstream of approved architecture boundaries.

Future implementation, if authorized, must not place model/provider behavior directly in core, UI, or raw state mutation paths. It must pass through controlled boundaries for:

- adapter isolation;
- context packaging;
- refusal/limitation behavior;
- output acceptance;
- validation/evaluation;
- state-safe review and acceptance flow.

If future work requires bypassing architecture guardrails, implementation must pause for planning before coding.

## 13. DDR Impact

### DDR-007

DDR-007 remains closure-planned and active for model/provider/local runtime work.

M31.2 does not close DDR-007.

M31.2 satisfies only the strategy-decision portion of DDR-007 placement by selecting a staged local-first / offline-preferred hybrid strategy for review.

DDR-007 still blocks:

- model/provider implementation;
- local AI runtime integration;
- live provider calls;
- app-coupled heavy-use testing;
- pre-go-live execution;
- product/SaaS-facing AI release.

### DDR-005

DDR-005 remains relevant if future AI assistance uses retrieval.

Future AI assistance must use governed context packets and must preserve retrieval as helper-only, source-traceable, limitation-visible, evaluated, and non-authoritative.

M31.2 does not authorize embeddings, vector stores, live source lookup, retrieval-backed source authority, or raw retrieval-to-model truth injection.

### DDR-006

DDR-006 remains relevant if future AI assistance contributes to generated output.

Any generated output remains draft/advisory/review-bound until output acceptance and document-factory rules are defined and accepted.

M31.2 does not authorize product-ready document generation, output acceptance, customer-ready output, or productization.

## 14. CAPA Continuation Controls

The context-reset CAPA remains active through M31.

Controls preserved:

- repo truth first;
- PLAN before GO;
- no source-free implementation claims;
- no AI/provider/runtime claims without accepted evidence;
- no old-chat authority;
- tracker movement only after accepted evidence;
- bounded branch/PR sequence;
- no autonomous or uncontrolled agentic execution.

## 15. Validation Requirement

No executable validation is required for this M31.2 evidence file because this change is docs/governance-only and does not alter code, tests, source JSON, schemas, validators, loaders, runtime behavior, CLI behavior, provider behavior, model behavior, or executable contracts.

Latest relevant executable validation remains the prior recorded validation from M30:

```text
python -m pytest -q — 1517 passed in 46.67s
```

If later M31 work changes code, source contracts, adapters, prompts-as-contracts, runtime behavior, validators, CLI behavior, or executable integration, `python -m pytest -q` and relevant AI/evaluation evidence will be required.

## 16. Tracker Movement Rule

Tracker movement from M31.2 remains blocked until:

1. this M31.2 strategy decision evidence is reviewed and accepted;
2. selected/deferred/rejected strategy paths are explicit;
3. privacy, cost, and operational constraints are explicit;
4. DDR-007 impact is explicit;
5. DDR-005 and DDR-006 impacts are explicit where relevant;
6. non-implementation and non-productization claims are explicit;
7. next checkpoint recommendation is explicit.

Recommended next checkpoint after acceptance:

```text
PLAN M31.3 — Provider/adapter boundary if approved.
```

M31.3 should remain boundary-first and must not implement provider/model/runtime behavior unless a later accepted plan explicitly authorizes implementation scope and validation requirements.

## 17. Explicit Non-Implementation Claims

This M31.2 decision evidence does not:

- implement AI assistance;
- authorize model/provider calls;
- authorize local AI runtime integration;
- authorize provider adapter implementation;
- authorize prompt execution;
- authorize agentic execution;
- authorize autonomous repo mutation;
- authorize app-coupled heavy-use testing;
- authorize embeddings, vector stores, or live source lookup;
- authorize retrieval-backed source authority;
- authorize AI approval authority;
- authorize product-ready generated output;
- close DDR-007;
- close DDR-005;
- close DDR-006;
- move the tracker;
- authorize productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 18. Review Decision Needed

Project Owner review should decide whether to accept this M31.2 strategy evidence as the governing basis for moving the tracker to the next checkpoint.

If accepted, the recommended next work is:

```text
PLAN M31.3 — Provider/adapter boundary if approved.
```
