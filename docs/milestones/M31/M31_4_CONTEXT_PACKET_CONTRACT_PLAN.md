---
doc_type: checkpoint_plan
canonical_name: M31_4_CONTEXT_PACKET_CONTRACT_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M31
checkpoint: M31.4
checkpoint_title: Context packet contract
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-m314-context-packet-contract
created_date: 2026-06-01
source_baseline_commit: fa7871b2505786bc854e2f9cbd5a478eaec72e6c
live_repo_write: YES_PLAN_SCOPE_ONLY
normal_execution_state: PLAN_AND_BOUNDED_GO_SCOPE
---

# M31.4 — Context Packet Contract Plan

## 1. Purpose

This plan defines M31.4 as a hybrid checkpoint: provider-facing context packet contract plus bounded builder/validator scaffolding and tests.

M31.4 creates the structured context layer that can later feed the provider adapter boundary without allowing free-form prompt facts, raw retrieval truth injection, prompt execution, model/provider calls, or AI-owned state mutation.

## 2. Execution Mode

```text
Hybrid — context packet contract + bounded builder/validator scaffolding/tests.
```

M31.4 is not provider execution. It prepares structured, source-traced, limitation-visible context only.

## 3. Source Baseline

M31.4 execution is based on:

- `ROADMAP_CANONICAL.md` v5, M31.4;
- `PROGRESS_TRACKER.md` after PR #76;
- M31.3 provider-neutral adapter boundary scaffolding;
- M31.2 local AI model/provider strategy decision;
- M31.1 AI assistance boundary confirmation;
- M30 retrieval boundary and DDR-005 carry-forward;
- DDR-006 generated-output carry-forward;
- DDR-007 provider/model/runtime carry-forward.

## 4. Approved Build Scope for GO M31.4

After this plan is accepted, GO M31.4 may implement only context packet contract scaffolding and tests.

Allowed build/content:

- provider-facing context packet baseline;
- context packet item builder/validator;
- context packet builder/validator;
- source/version/reference checks;
- standards registry reference checks;
- retrieval-as-support-only checks;
- limitation visibility checks;
- provider boundary dependency checks;
- tests proving free-form prompt facts and raw retrieval dumps are blocked.

Expected files:

```text
asbp/ai_runtime/context_packets.py
tests/test_ai_context_packet_contract.py
docs/milestones/M31/M31_4_CONTEXT_PACKET_CONTRACT.md
```

## 5. Not Allowed in GO M31.4

GO M31.4 must not implement or authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- AI-generated output;
- refusal-rule execution;
- output acceptance;
- evaluation harness execution;
- app-coupled heavy-use testing;
- embeddings/vector store implementation;
- live source lookup;
- UI/API behavior;
- productization or release claims.

## 6. Required Context Packet Contract Rules

M31.4 must enforce or record:

- every context item must declare a version-pinned source reference;
- every context item must declare source family, role, authority status, evidence status, limitation summary, allowed use, and blocked use;
- standards context must preserve registry/version and limitation visibility;
- task/workflow state context may describe state but must not authorize mutation;
- retrieval context must remain support-only and non-authoritative;
- free-form prompt facts are blocked;
- raw retrieval dumps are blocked;
- provider execution remains blocked;
- prompt execution remains blocked.

## 7. Boundary Model

M31.4 builds the structured context packet that may later be consumed by an approved provider adapter boundary.

Approved boundary shape:

```text
Governed product sources / workflow state / retrieval support -> context packet -> provider adapter boundary
```

Blocked boundary shape:

```text
Free-form prompt / raw retrieval dump / anonymous facts -> provider/model
```

## 8. Retrieval Handling

Retrieval context, if included, must declare:

- source reference;
- source family;
- support-only source role;
- support-only authority status;
- limitation summary;
- allowed use;
- blocked use.

Retrieval must not define source truth, standards truth, compliance truth, execution truth, or approval authority.

## 9. Real Provider Entry Point

M31.4 does not authorize provider execution.

Real provider or local runtime execution remains downstream of:

- M31.5 refusal and limitation rules;
- M31.6 output acceptance and review rules;
- M31.7 evaluation/regression harness;
- later validation and acceptance gates.

## 10. DDR Impact

### DDR-005

DDR-005 remains partially closed for deterministic retrieval controls only. M31.4 prevents raw retrieval-to-model truth injection.

### DDR-006

DDR-006 remains relevant for generated output. M31.4 does not authorize generated output acceptance or document factory readiness.

### DDR-007

DDR-007 remains closure-planned and active. M31.4 does not close DDR-007 and does not authorize model/provider/local runtime execution.

## 11. CAPA Continuation Controls

M31.4 preserves:

- repo truth first;
- PLAN before GO;
- no source-free implementation claims;
- no AI/provider/runtime execution claims without accepted evidence;
- no old-chat authority;
- tracker movement only after accepted evidence;
- bounded branch/PR sequence;
- no autonomous or uncontrolled agentic execution.

## 12. Validation Requirement

Because GO M31.4 changes code and tests, executable validation is required:

```text
python -m pytest tests/test_ai_context_packet_contract.py -q
python -m pytest -q
```

If validation cannot be run in the current environment, the PR must state that executable validation was not run and must remain unmerged until validation is run locally or in CI.

## 13. Tracker Movement Rule

Tracker movement from M31.4 remains blocked until:

1. this M31.4 hybrid plan is accepted;
2. context packet contract exists;
3. context packet builder/validator exists;
4. tests prove source references must be version-pinned;
5. tests prove limitation visibility is required;
6. tests prove raw/free-form prompt facts are rejected;
7. tests prove raw retrieval dumps are rejected;
8. tests prove retrieval remains support-only;
9. DDR-005, DDR-006, and DDR-007 impacts are explicit;
10. validation passes;
11. next checkpoint is set to `PLAN M31.5 — Refusal and limitation rules`.

## 14. Explicit Non-Implementation Claims

This M31.4 plan may authorize context packet contract scaffolding and tests.

This M31.4 plan does not authorize:

- real provider calls;
- local model inference;
- prompt execution;
- API key handling;
- provider SDK integration;
- model-generated output;
- app-coupled heavy-use testing;
- tracker movement by itself;
- productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output.

## 15. Immediate Next Action

After this plan is accepted, the bounded GO action is:

```text
GO M31.4 — implement context packet contract scaffolding and tests.
```
