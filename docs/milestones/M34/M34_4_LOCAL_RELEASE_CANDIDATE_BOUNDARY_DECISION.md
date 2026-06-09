# M34.4 - Local Release-Candidate Boundary Decision

Status: Completed on feature branch  
Checkpoint: M34.4  
Mode: Governance-only  
Branch: `m34-4-local-rc-boundary-decision`  
Decision date: 2026-06-09

## Purpose

Define the in/out boundary for the first local enterprise-grade product baseline before any later engineering readiness, validation, owner acceptance, or Phase 9 closeout decision.

M34.4 is a local release-candidate boundary decision checkpoint only. It does not implement code, change runtime behavior, decide engineering readiness entry, start Phase 10, approve deployment, authorize release readiness, authorize SaaS readiness, approve commercialization, claim customer-ready output, or claim full product/runtime AI readiness.

## Roadmap requirement

M34.4 roadmap target:

```text
M34.4 - Local release-candidate boundary decision
```

Execution mode:

```text
Governance-only
```

Required deliverable / completion minimum:

```text
In/out boundary for the first local enterprise-grade product baseline.
```

Validation / review requirement:

```text
Owner review required.
```

Tracker movement rule:

```text
May advance only after local RC boundary is explicit.
```

Not allowed:

```text
Expand to deployment/SaaS prematurely.
```

## Source basis

This decision is based on repo-persistent evidence:

```text
ROADMAP_CANONICAL.md
PROGRESS_TRACKER.md
ARCHITECTURE_GUARDRAILS.md
docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md
docs/milestones/M34/M34_1_PRODUCT_CORE_COMPLETENESS_ASSESSMENT.md
docs/milestones/M34/M34_2_DDR_CLOSURE_RECLASSIFICATION_REVIEW.md
docs/milestones/M34/M34_3_PRODUCT_CORE_LIMITATION_REGISTER.md
docs/milestones/M33/M33_11_MILESTONE_CLOSEOUT.md
docs/milestones/M33/M33_10_OWNER_ACCEPTANCE_GATE.md
docs/milestones/M33/M33_9_FINAL_VALIDATION_CHECKPOINT.md
docs/milestones/M33/validation_records/M33_9_FINAL_VALIDATION/
docs/milestones/M32/M32_11_MILESTONE_CLOSEOUT.md
README.md
```

Repo reality remains authoritative for implementation truth. This decision does not use prior chat, memory, roadmap intent, or unstaged work as evidence.

## Decision summary

M34.4 decision:

```text
CONDITIONAL LOCAL RC BOUNDARY / LIMITATIONS CARRIED FORWARD
```

Decision meaning:

The first local enterprise-grade product baseline may be bounded as a local-only, CLI-enhanced CQV workflow release-candidate candidate for later M34 review, but only with explicit limitations carried forward. This boundary is not deployment-ready, release-ready, SaaS-ready, commercialization-ready, customer-ready, or full product/runtime AI ready.

This decision supports progression to M34.5 planning after owner review and merge. It does not itself authorize engineering readiness entry.

## Boundary status

| Area | Decision |
|---|---|
| Local RC boundary exists | Yes - conditional and limited. |
| Engineering readiness entry | Not decided by M34.4. |
| Phase 10 entry | Not authorized. |
| Deployment/SaaS expansion | Explicitly excluded. |
| Customer-ready output | Explicitly excluded. |
| Full product/runtime AI readiness | Explicitly excluded. |

## In-scope local RC boundary

The first local enterprise-grade product baseline may include only the following supported scopes:

| Scope | In-bound definition | Evidence basis | Boundary condition |
|---|---|---|---|
| Local CLI-enhanced CQV workflow | Bounded local workflow path exercised through scenario, configure, plan, status, outputs, and trial-summary. | M32 closeout; M33 trial/validation/UAT; M34.1/M34.3. | Local only; CLI-enhanced only; no web/API/customer surface. |
| Cleanroom HVAC scenario baseline | One accepted synthetic cleanroom HVAC scenario used for product-core evidence. | M33 scenario pack; M33 validation; M34.1/M34.3. | One-scenario limitation must remain visible. |
| Source-library baseline | Accepted M27 source-library baseline for downstream local CQV workflow use. | M27 owner acceptance; M34.1/M34.2/M34.3. | No productized runtime-authoritative expansion or deployment-compiled lookup. |
| Standards visibility and bounded authority | Standards applicability, citation, source-status visibility, and limitation-aware standards handling. | M28 closeout; M34.1/M34.3. | No clause-level legal/regulatory authority or product-ready standards advice. |
| Helper-only retrieval | Deterministic, source-traceable, helper-only retrieval controls. | M30 closeout; M34.1/M34.2/M34.3. | Retrieval is non-authoritative and not productized retrieval infrastructure. |
| Output metadata/visibility review | Output review can expose metadata, visibility, and human-review-required boundaries. | M29 closeout; M33 trial/UAT; M34.1/M34.3. | No customer-ready output, final approval, release output, or product-ready export/report lifecycle. |
| Optional local/offline AI assistance | Optional supporting-only local/offline AI assistance evidence. | M31 acceptance; M33 optional supporting evidence; M34.1/M34.2/M34.3. | Optional/supporting only; no live provider, customer-facing AI, autonomous agent, or AI approval authority. |
| Validation evidence | M33.9 pytest and integrated scenario validation evidence. | M33.9 final validation; M34.1/M34.3. | Supports bounded baseline only; later M34.6 remains required where applicable. |
| Conditional UAT/owner acceptance evidence | M33.8 UAT and M33.10 owner acceptance for bounded M33 local product-core evidence. | M33.8, M33.10, M33.11. | Conditional only; later M34.7 remains required. |
| README quick-start guidance | Local development quick-start instructions for venv, dependencies, pytest, CLI exploration, and state init. | README; M34.1/M34.3. | Not RC-verified installability, packaging, distribution, or supportability. |

## Out-of-scope local RC boundary

The following are explicitly outside the first local RC boundary:

- customer-ready output;
- product-ready generated or assembled output approval;
- release-ready document/export/report lifecycle;
- web UI;
- desktop UI;
- customer/admin UI;
- API product surface;
- hosted/cloud/SaaS workflow;
- live provider/cloud AI behavior;
- customer-facing AI;
- autonomous agent behavior;
- AI approval, certification, release, or acceptance authority;
- embeddings, vector store, external search, live lookup, or productized retrieval;
- retrieval-backed source authority or compliance authority;
- clause-level legal/regulatory standards authority;
- product-ready standards advice or output;
- productized runtime-authoritative library expansion;
- deployment-compiled lookup;
- RC-verified installability;
- packaging readiness;
- installer or distribution boundary;
- supported platform matrix;
- release artifact;
- upgrade/supportability boundary;
- engineering readiness entry;
- Phase 10 entry;
- productization, deployment, release, SaaS, or commercialization readiness.

## Conditional inclusions

The following may remain inside the local RC boundary only with visible limitations:

| Conditional item | Required limitation |
|---|---|
| Local CLI-enhanced workflow | Must remain local and CLI-enhanced only. |
| Cleanroom HVAC scenario | Must be described as one accepted scenario, not broad product proof. |
| Source-library baseline | Must remain limited to accepted downstream local workflow use. |
| Standards visibility | Must preserve source-status and authority limitations. |
| Retrieval | Must remain helper-only and non-authoritative. |
| Output review | Must remain human-review-required and not customer-ready. |
| Optional local/offline AI | Must remain optional/supporting-only and not product-authoritative. |
| README quick-start | Must remain guidance, not packaging/installability readiness. |

## Explicit non-claims for the boundary

This local RC boundary does not claim:

- engineering readiness entry;
- Phase 10 entry;
- productization readiness;
- deployment readiness;
- release readiness;
- SaaS readiness;
- commercialization readiness;
- customer-ready output;
- final regulated deliverable approval;
- full product/runtime AI readiness;
- live provider/cloud AI readiness;
- customer-facing UI/API readiness;
- packaging/installability readiness.

## Limitation inheritance from M34.3

M34.4 inherits the full M34.3 limitation register.

Key inherited limitation classes:

- source/library limits;
- standards limits;
- retrieval limits;
- document/output limits;
- AI/local model limits;
- UI/CLI/API limits;
- validation/UAT limits;
- install/run/package/release limits;
- DDR-linked carry-forward limits.

M34.4 does not soften, hide, downgrade, or close these limitations.

## DDR boundary impact

M34.4 preserves M34.2 and M34.3 DDR-linked carry-forward decisions:

- DDR-001 and DDR-002 remain limited-scope closures only; productized runtime-authoritative libraries and deployment-compiled lookup remain outside the boundary.
- DDR-003 remains limited to accepted M29 baseline with clarifications; product-ready template behavior remains outside the boundary.
- DDR-004 remains limited to approved standards source/citation authority model; clause-level or product-ready standards authority remains outside the boundary.
- DDR-005 remains partially closed only for bounded deterministic retrieval controls; productized retrieval remains outside the boundary.
- DDR-006 remains productization-sensitive; customer-ready/product-ready output/export/report behavior remains outside the boundary.
- DDR-007 remains limited to bounded local/offline supporting evidence only; live provider/customer-facing/full runtime AI remains outside the boundary.
- DDR-008 remains gate-control only; productization readiness, Phase 9 closeout, and Phase 10 entry remain outside this decision.
- DDR-009 remains placeholder compatibility only; productized UI/API behavior remains outside the boundary.

## Owner review

Owner review requirement:

```text
Owner review required by ROADMAP_CANONICAL.md for M34.4.
```

Owner review decision for this PR:

```text
Pending owner review through PR review/merge.
```

Proposed owner decision to accept by merge:

```text
CONDITIONAL LOCAL RC BOUNDARY / LIMITATIONS CARRIED FORWARD
```

Owner rationale to preserve in review:

The first local RC boundary is allowed only as a bounded local CLI-enhanced CQV workflow baseline with the M34.3 limitation register carried forward. It is not engineering readiness, Phase 10 entry, productization readiness, release readiness, SaaS readiness, customer-ready output, or full product/runtime AI readiness.

## M34.5 input summary

M34.5 should decide whether the project may enter Phase 10 engineering-readiness work based on this conditional local RC boundary.

Recommended M34.5 inputs:

- M34.1 product-core completeness assessment;
- M34.2 DDR closure/reclassification review;
- M34.3 product-core limitation register;
- M34.4 conditional local RC boundary decision;
- latest executable validation evidence from M33.9;
- owner review outcome for M34.4;
- explicit Phase 10 non-claims and readiness blockers.

M34.5 must not resume readiness automatically.

## Architecture guardrail impact

M34.4 is governance-only and does not change architecture.

Architecture guardrail status:

- CLI remains an adapter only.
- New domain behavior remains required to attach through approved core module boundaries.
- State/persistence access remains required to go through approved state boundary helpers/modules.
- No bypass, new domain behavior, or persistence change is introduced by this decision.

## Document consistency review

Review result:

```text
PASS WITH LIMITATIONS RECORDED - local RC boundary is explicit; in-scope and out-of-scope baseline are recorded; deployment/SaaS expansion is excluded.
```

Review checks:

| Check | Result |
|---|---|
| M34.4 deliverable exists | PASS |
| Local RC boundary decision explicit | PASS |
| In-scope baseline explicit | PASS |
| Out-of-scope baseline explicit | PASS |
| Conditional inclusions explicit | PASS |
| Owner review requirement visible | PASS |
| M34.3 limitations carried forward | PASS |
| DDR-linked blockers preserved | PASS |
| Deployment/SaaS expansion excluded | PASS |
| Engineering readiness not approved | PASS |
| Phase 10 not authorized | PASS |
| Productization/release/commercial claims avoided | PASS |
| Architecture guardrails preserved | PASS |

## Tracker movement recommendation

Tracker movement is allowed after this decision is reviewed and merged because the local RC boundary is explicit.

If accepted, the tracker may record:

```text
Latest completed roadmap checkpoint: M34.4 - Local release-candidate boundary decision
Exact next unfinished work: PLAN M34.5 - Engineering readiness entry decision
Latest validation / review evidence: docs/milestones/M34/M34_4_LOCAL_RELEASE_CANDIDATE_BOUNDARY_DECISION.md - PASS WITH LIMITATIONS RECORDED document consistency review
```

M34.5 remains blocked until separately planned and authorized.

## Explicit non-claims

M34.4 does not claim:

- M34.5 engineering readiness entry decision;
- M34.6 validation checkpoint completion;
- M34.7 product-core UAT/owner acceptance;
- M34.8 Phase 9 closeout;
- Phase 10 entry approval;
- productization readiness;
- deployment readiness;
- release readiness;
- SaaS readiness;
- commercialization readiness;
- customer-ready output;
- full product/runtime AI readiness.

## Next roadmap checkpoint

After M34.4 is reviewed and merged, the next normal roadmap checkpoint is:

```text
PLAN M34.5 - Engineering readiness entry decision
```

Do not start M34.5 without separate owner authorization.
