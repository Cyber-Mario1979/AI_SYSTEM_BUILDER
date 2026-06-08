# M34.3 - Product-Core Limitation Register

Status: Completed on feature branch  
Checkpoint: M34.3  
Mode: Governance-only  
Branch: `m34-3-product-core-limitation-register`  
Register date: 2026-06-08

## Purpose

Record known supported scopes, unsupported scopes, source limits, standards limits, AI limits, UI limits, output limits, validation/UAT limits, install/run limits, and DDR-linked carry-forward limits before the later local release-candidate boundary decision.

M34.3 is a limitation-register checkpoint only. It does not approve a local release-candidate boundary, start M34.4, decide engineering readiness entry, close Phase 9, authorize Phase 10, change DDR statuses, implement code, or claim productization, deployment, release readiness, SaaS readiness, commercialization readiness, customer-ready output, or full product/runtime AI readiness.

## Roadmap requirement

M34.3 roadmap target:

```text
M34.3 - Product-core limitation register
```

Execution mode:

```text
Governance-only
```

Required deliverable / completion minimum:

```text
Register of supported scopes, unsupported scopes, source limits, standards limits, AI limits, UI limits, and output limits.
```

Validation / review requirement:

```text
Document consistency review.
```

Tracker movement rule:

```text
May advance only after limitation register exists.
```

Not allowed:

```text
Hide limitations.
```

## Source basis

This limitation register is based on repo-persistent evidence:

```text
ROADMAP_CANONICAL.md
PROGRESS_TRACKER.md
ARCHITECTURE_GUARDRAILS.md
docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md
docs/milestones/M34/M34_1_PRODUCT_CORE_COMPLETENESS_ASSESSMENT.md
docs/milestones/M34/M34_2_DDR_CLOSURE_RECLASSIFICATION_REVIEW.md
docs/milestones/M33/M33_11_MILESTONE_CLOSEOUT.md
docs/milestones/M33/M33_10_OWNER_ACCEPTANCE_GATE.md
docs/milestones/M33/M33_9_FINAL_VALIDATION_CHECKPOINT.md
docs/milestones/M33/validation_records/M33_9_FINAL_VALIDATION/
docs/milestones/M32/M32_11_MILESTONE_CLOSEOUT.md
docs/milestones/M31/M31_11_AI_ASSISTANCE_UAT_OWNER_ACCEPTANCE.md
docs/milestones/M31/M31_12_M31_CLOSEOUT_AI_READINESS_RECOMMENDATION.md
docs/milestones/M30/M30_11_MILESTONE_CLOSEOUT.md
docs/milestones/M29/M29_13_MILESTONE_CLOSEOUT.md
docs/milestones/M28/M28_12_MILESTONE_CLOSEOUT.md
docs/milestones/M27/M27_12_MILESTONE_UAT_OWNER_ACCEPTANCE.md
```

Repo reality remains authoritative for implementation truth. This register does not use prior chat, memory, roadmap intent, or unstaged work as evidence.

## Register result

Overall M34.3 result:

```text
PASS WITH LIMITATIONS RECORDED - product-core supported and unsupported scopes are explicit; limitations are carried forward for M34.4 boundary decision.
```

M34.3 confirms that the local product core has bounded accepted evidence for local CLI-enhanced CQV workflow progression, but it does not support an unqualified product-core readiness claim.

## Limitation record schema

| Field | Meaning |
|---|---|
| ID | Stable limitation identifier for M34.3 review and M34.4 input. |
| Domain | Affected product-core domain. |
| Supported scope | What repo evidence supports. |
| Unsupported / not accepted scope | What must not be claimed. |
| Evidence basis | Repo-persistent evidence basis. |
| DDR link | Relevant DDRs if applicable. |
| Risk if hidden | Why the limitation must remain visible. |
| Future checkpoint owner | Next checkpoint or phase that must address or preserve the limitation. |
| M34.4 disposition | How this should inform local RC boundary decision. |

## Limitation register

| ID | Domain | Supported scope | Unsupported / not accepted scope | Evidence basis | DDR link | Risk if hidden | Future checkpoint owner | M34.4 disposition |
|---|---|---|---|---|---|---|---|---|
| LIB-001 | Libraries / source authority | Bounded downstream local CQV workflow source-library use accepted through M27/M34.1 evidence. | Productized runtime-authoritative library use beyond validated local scope; deployment-compiled lookup; customer-facing library authority. | M27 owner acceptance; M34.1 library assessment; M34.2 DDR review. | DDR-001, DDR-002 | Could imply productized source authority that is not proven. | M34.4, M35, M36 | Include only bounded local source-library use in RC boundary. |
| LIB-002 | Runtime library promotion | Existing source-library baseline can support the accepted local workflow evidence path. | New runtime promotion, compiled lookup generation, or productized dependency expansion without evidence. | M34.2 DDR-001/002 decisions. | DDR-001, DDR-002 | Could bypass library authority gates. | M35/M36 if release/product package depends on it. | Exclude productized runtime promotion from first RC boundary unless separately proven. |
| STD-001 | Standards authority | Bounded standards applicability, citation, registry consumption, controlled override, and output limitation evidence. | Clause-level legal/regulatory authority; mandatory-use product authority; unsupported source verification; product-ready standards advice/output. | M28 closeout; M34.1 standards assessment; M34.2 DDR-004 decision. | DDR-004, DDR-005, DDR-006 | Could overstate compliance authority. | M34.4, M35/M36/M37 where affected. | RC boundary must preserve bounded standards authority only. |
| STD-002 | Standards source limits | Known standards/source statuses can be shown with limitation visibility. | Treating pending, TBD, user-provided, reference-only, or limited sources as verified public regulation or final compliance truth. | M28/M34.1 standards limitation evidence. | DDR-004 | Could create false compliance claims. | M34.4; future standards maintenance if scope expands. | RC boundary must keep source status limitations visible. |
| RET-001 | Retrieval | Helper-only, source-traceable, deterministic retrieval controls accepted for bounded local product-source evidence. | Embeddings, vector store, external search, live lookup, ranking expansion, productized retrieval operations, retrieval-backed source/compliance authority, UI/API retrieval integration. | M30 closeout; M34.1 retrieval assessment; M34.2 DDR-005 decision. | DDR-005 | Could turn helper output into authority. | M34.4, M37, M38 where affected. | RC boundary may include helper-only retrieval only. |
| DOC-001 | Document/output behavior | Document/output baseline evidence exists with metadata/visibility and human-review requirements. | Customer-ready output; final generated/assembled output approval; release output; product-ready document/download/export behavior in current local workflow. | M29 closeout; M33 trial/UAT evidence; M34.1 output assessment. | DDR-003, DDR-006 | Could imply deliverables are ready for customer or release use. | M34.4, M36, M37 where affected. | RC boundary must exclude customer-ready/release-ready output. |
| DOC-002 | Artifact lifecycle | Output metadata and visibility can support review in bounded local workflow. | Supported distribution artifact, release artifact, final validated package, or approved regulated deliverable lifecycle. | M33/M34.1 output and install/run limits. | DDR-006 | Could imply product/package release readiness. | M34.4, M36 | RC boundary must not claim release artifact lifecycle. |
| AI-001 | Local/offline AI support | Optional local/offline AI assistance exists only as supporting evidence under strict limits. | Live provider/cloud API behavior, customer-facing AI, autonomous agent behavior, model-owned state mutation, AI approval/certification/release authority, full product/runtime AI readiness. | M31 acceptance; M33 optional model evidence; M34.1 AI assessment; M34.2 DDR-007 decision. | DDR-007 | Could imply AI is product-authoritative or production-ready. | M34.4, M37, M38 | RC boundary must treat AI as optional/supporting only or exclude it from RC claims. |
| AI-002 | Model runtime testing | Normal pytest and accepted validation do not require live model or Ollama. | App-coupled heavy-use/pre-go-live AI evidence, provider smoke/operational readiness, or SaaS/live model behavior. | M33.9 validation; M34.1/M34.2 AI limits. | DDR-007 | Could imply operational AI readiness exists. | M37 if provider/deployment path starts. | RC boundary must not depend on live model behavior. |
| UI-001 | CLI surface | CLI-enhanced local workflow path supports scenario -> configure -> plan -> status -> outputs -> trial-summary. | Web UI, desktop UI, customer/admin UI, API product surface, hosted/cloud/SaaS workflow. | M32 closeout; M33 trial evidence; M34.1 UI/CLI assessment. | DDR-009 | Could imply external/customer surface readiness. | M34.4, M35/M36/M38 if surface expands. | RC boundary may include CLI-enhanced local workflow only. |
| UI-002 | External contracts/placeholders | Placeholder compatibility remains limited to prior approved placeholder scope. | Productized placeholder-backed behavior or external contracts relying on unresolved library/template/standards/output dependencies. | M34.2 DDR-009 decision. | DDR-009 | Could expose unsupported product contracts. | M35/M36/M38 if UI/API/product boundary expands. | RC boundary must exclude productized UI/API placeholders. |
| VAL-001 | Validation evidence | Full M33.9 pytest and integrated scenario validation evidence support bounded M33 local product-trial baseline. | Full product-core completeness across categories; multi-scenario/product-wide validation; release validation. | M33.9 validation; M34.1 validation assessment. | DDR-008 awareness | Could overstate validation breadth. | M34.6; M34.7 | RC boundary must be conditional on one-scenario validation limits. |
| UAT-001 | UAT / owner acceptance | M33.8 UAT and M33.10 owner acceptance support conditional progression into M34. | Full product readiness, launch approval, customer acceptance, or final RC acceptance. | M33.8, M33.10, M33.11, M34.1. | DDR-008 awareness | Could convert conditional acceptance into launch approval. | M34.7 owner acceptance. | RC boundary must require later owner review/acceptance. |
| INS-001 | Install/run | README includes virtual environment, dependency install, pytest, CLI exploration, and state init instructions. | RC-verified installability, packaging readiness, supported distribution, installer, upgrade path, platform support matrix. | README; M34.1 install/run assessment. | DDR-008 awareness | Could imply packaging/release readiness. | M34.4, M36 | RC boundary must not claim packaging/installability readiness. |
| GOV-001 | DDR status | M34.2 reviewed all DDRs and carried forward productization-sensitive limits. | Treating M34.2 as a DDR register rewrite, global dependency closure, or productization approval. | M34.2 DDR review. | All DDRs | Could erase blockers needed for later gates. | M34.4, M34.5, M34.8 | RC boundary must respect all carried DDR limits. |
| GOV-002 | Phase 10 / readiness | M34.3 can feed later M34 boundary decisions. | Phase 10 entry, engineering readiness, deployment readiness, release readiness, SaaS readiness, commercialization readiness. | Roadmap M34 sequence; tracker; M34.1/M34.2 non-claims. | DDR-008 | Could skip required re-entry gates. | M34.5, M34.8 | RC boundary must not approve Phase 10 or productization. |

## Supported scopes summary

The following scopes are supported for consideration in later M34 boundary work:

- bounded local CLI-enhanced CQV workflow evidence;
- accepted M27 source-library baseline for limited downstream local workflow use;
- bounded standards applicability/citation/source-status visibility;
- helper-only deterministic retrieval controls;
- document/output metadata and visibility review with human review required;
- optional local/offline AI assistance only as supporting evidence;
- one accepted cleanroom HVAC scenario validation path;
- conditional UAT/owner acceptance for bounded M33 evidence;
- README quick-start guidance as non-RC-verified install/run guidance.

## Unsupported scopes summary

The following scopes are not accepted by M34.3 and must not be implied by later M34 work unless separately proven and authorized:

- customer-ready output;
- product-ready generated/assembled output approval;
- release-ready document/export/report lifecycle;
- web UI;
- desktop UI;
- customer/admin UI;
- API product surface;
- hosted/cloud/SaaS workflow;
- live provider/cloud AI behavior;
- customer-facing AI;
- autonomous agent behavior;
- AI approval/certification/release authority;
- embeddings/vector store/external search/live lookup/productized retrieval;
- clause-level legal/regulatory standards authority;
- productized runtime-authoritative library expansion;
- packaging/installability/readiness claims;
- local release-candidate boundary approval;
- engineering readiness entry;
- Phase 10 entry;
- productization/deployment/release/SaaS/commercial readiness.

## Source and library limits

Source/library support is limited to the accepted source-library baseline and downstream local workflow use proven by milestone evidence.

Source/library limits carried forward:

- no deployment-compiled lookup is accepted;
- no productized runtime-authoritative library expansion is accepted;
- no customer-facing source-library authority is accepted;
- downstream product/release packaging must revisit DDR-001 and DDR-002 if it depends on runtime-authoritative libraries.

## Standards limits

Standards support is bounded and source-status-dependent.

Standards limits carried forward:

- no clause-level legal/regulatory authority is accepted;
- no unsupported source is upgraded to verified authority;
- no standards embedding or standards-backed retrieval authority is accepted;
- no product-ready standards output or compliance advice is accepted beyond evidence.

## Retrieval limits

Retrieval support is helper-only, deterministic, source-traceable, and non-authoritative.

Retrieval limits carried forward:

- retrieval does not replace source files, source registries, deterministic resolver behavior, template selection, standards/citation authority, or stage/commit controls;
- no embeddings, vector database, live lookup, external search, ranking expansion, or productized retrieval operation is accepted;
- no UI/API retrieval integration is accepted.

## Document/output limits

Document/output support is limited and human-review-required.

Document/output limits carried forward:

- customer-ready output is not accepted;
- product-ready download/export/report generation in the current local workflow is not accepted;
- generated output is not approved, certified, or released;
- artifact lifecycle remains non-release/non-distribution until later evidence.

## AI/local model limits

AI/local model support is optional and supporting-only.

AI/local model limits carried forward:

- full product/runtime AI readiness is not accepted;
- cloud/provider API behavior is not accepted;
- customer-facing AI is not accepted;
- autonomous agent behavior is not accepted;
- model-owned state mutation is not accepted;
- AI approval, certification, release, or acceptance authority is not accepted;
- normal pytest must not require Ollama or a live model;
- app-coupled heavy-use/pre-go-live AI evidence remains future gated.

## UI/CLI/API limits

The accepted surface is CLI-enhanced local workflow only.

UI/CLI/API limits carried forward:

- CLI remains an adapter only;
- no web UI is accepted;
- no desktop UI is accepted;
- no customer/admin UI is accepted;
- no API product surface is accepted;
- no hosted/cloud/SaaS workflow is accepted;
- placeholder compatibility does not authorize productized placeholder-backed behavior.

## Validation/UAT limits

Validation and UAT evidence support the bounded accepted scenario path only.

Validation/UAT limits carried forward:

- one scenario must not be treated as full product-core completeness;
- conditional acceptance must not be treated as full readiness;
- M34.6 and M34.7 remain required later checkpoints where applicable;
- latest executable validation remains M33.9 and does not prove later product/readiness claims.

## Install/run/package/release limits

README quick-start guidance exists, but M34.3 does not convert it into release-candidate installability.

Install/run/package/release limits carried forward:

- no packaging readiness is accepted;
- no installer/distribution boundary is accepted;
- no supported platform matrix is accepted;
- no release artifact is accepted;
- no upgrade/supportability boundary is accepted;
- Phase 10 readiness remains blocked pending later M34 decisions.

## DDR-linked carry-forward summary

M34.3 preserves the M34.2 DDR conclusions:

- DDR-001 and DDR-002: limited-source-library closure only; productized runtime-authoritative behavior remains carried forward.
- DDR-003: M29 baseline accepted with limitations; product-ready templates remain carried forward.
- DDR-004: standards source/citation authority limited to approved scope; unsupported standards authority remains carried forward.
- DDR-005: partial closure for bounded deterministic retrieval only; productized retrieval remains carried forward.
- DDR-006: productization-sensitive output/export/report limitations remain carried forward.
- DDR-007: bounded local/offline support only; live/provider/customer-facing/full runtime AI remains carried forward.
- DDR-008: gate-control closure only; Phase 10/productization readiness remains carried forward.
- DDR-009: placeholder compatibility only; productized UI/API behavior remains carried forward.

## M34.4 input summary

M34.4 should use this register to define an explicit local release-candidate boundary.

Recommended M34.4 inputs:

- include only bounded local CLI-enhanced CQV workflow evidence unless owner explicitly narrows or expands with evidence;
- preserve one-scenario validation limitation;
- preserve human-review-required output boundary;
- preserve metadata/visibility-only output limitation;
- preserve helper-only retrieval limitation;
- preserve optional/supporting-only AI limitation;
- preserve no-web/no-desktop/no-API/no-hosted/no-SaaS surface limitation;
- preserve no customer-ready output limitation;
- preserve no packaging/release/deployment readiness limitation;
- explicitly decide whether a first local RC boundary is allowed, conditional, or blocked.

M34.4 must remain a boundary decision, not an implementation checkpoint.

## Architecture guardrail impact

M34.3 is governance-only and does not change architecture.

Architecture guardrail status:

- CLI remains an adapter only.
- New domain behavior remains required to attach through approved core module boundaries.
- State/persistence access remains required to go through approved state boundary helpers/modules.
- No bypass, new domain behavior, or persistence change is introduced by this register.

## Document consistency review

Review result:

```text
PASS WITH LIMITATIONS RECORDED - M34.3 limitation register exists; supported and unsupported scopes are explicit; limitations are visible and mapped to future boundary decisions.
```

Review checks:

| Check | Result |
|---|---|
| M34.3 deliverable exists | PASS |
| Supported scopes recorded | PASS |
| Unsupported scopes recorded | PASS |
| Source/library limits recorded | PASS |
| Standards limits recorded | PASS |
| Retrieval limits recorded | PASS |
| Document/output limits recorded | PASS |
| AI/local model limits recorded | PASS |
| UI/CLI/API limits recorded | PASS |
| Validation/UAT limits recorded | PASS |
| Install/run/package/release limits recorded | PASS |
| DDR-linked carry-forward limits recorded | PASS |
| Limitations not hidden or softened | PASS |
| M34.4 input summary included | PASS |
| Productization/release/deployment/SaaS/commercial claims avoided | PASS |
| Architecture guardrails preserved | PASS |

## Tracker movement recommendation

Tracker movement is allowed after this register is reviewed and merged because the M34.3 limitation register exists.

If accepted, the tracker may record:

```text
Latest completed roadmap checkpoint: M34.3 - Product-core limitation register
Exact next unfinished work: PLAN M34.4 - Local release-candidate boundary decision
Latest validation / review evidence: docs/milestones/M34/M34_3_PRODUCT_CORE_LIMITATION_REGISTER.md - PASS WITH LIMITATIONS RECORDED document consistency review
```

M34.4 remains blocked until separately planned and authorized.

## Explicit non-claims

M34.3 does not claim:

- M34.4 local release-candidate boundary decision;
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

After M34.3 is reviewed and merged, the next normal roadmap checkpoint is:

```text
PLAN M34.4 - Local release-candidate boundary decision
```

Do not start M34.4 without separate owner authorization.
