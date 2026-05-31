---
doc_type: checkpoint_plan
canonical_name: M30_2_SOURCE_ELIGIBILITY_MODEL
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: checkpoint_planning_evidence
milestone: M30
checkpoint: M30.2
checkpoint_title: Source eligibility model
execution_mode: Hybrid
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: main
created_date: 2026-05-31
source_baseline_commit: 0d722cd58cbe4a9e1d7ec8d2a027ec18969c8472
live_repo_write: NO
normal_execution_state: PLAN_ONLY
---

# M30.2 — Source Eligibility Model

## 1. Purpose

This plan defines the controlled Hybrid source-eligibility model for M30.2 — Source eligibility model.

M30.2 defines which source classes may be eligible for later retrieval/indexing work, which source classes must be excluded, how source status controls eligibility, and how pending/TBD/draft/archived/superseded/limited-scope material is prevented from becoming mandatory authority.

This plan does not implement retrieval, indexing, embeddings, standards-backed live lookup, retrieval-backed source authority, AI/model/provider behavior, UI/API behavior, deployment, release, productization, SaaS readiness, or customer-ready output.

## 2. Active Execution Declaration

Active execution context:

    Repo-driven connector session after M30.1 PLAN-only completion and tracker alignment.

Active source set:

- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`
- `docs/milestones/M30/M30_1_RETRIEVAL_JUSTIFICATION_GATE_PLAN.md`
- current repo reality from tracked repository files where needed

Active branch:

    main

Current phase:

    Phase 9 — Roadmap Reset and Local Integrated CQV Product Core

Current milestone:

    M30 — Governed Retrieval and Indexing for Authoritative Product Sources

Current checkpoint:

    M30.2 — Source eligibility model

Checkpoint execution mode:

    Hybrid

Implementation/source minimum:

    Controlled Hybrid source-eligibility model only.
    No retrieval runtime behavior.
    No index build.
    No embeddings.
    No source loader/validator changes.

Validation evidence required:

    Document consistency review only.
    No executable validation unless code, tests, commands, imports, schemas, runtime behavior, validators, loaders, source data, or executable contracts change.

Tracker movement rule:

    Tracker must not advance from M30.2 until the accepted M30.2 source-eligibility model exists and the tracker records M30.2 completion as planning/source-control evidence only.

Explicit non-implementation claims:

    M30.2 does not implement retrieval, indexing, embeddings, source authority, AI, UI/API, deployment, productization, SaaS readiness, or customer-ready output.

## 3. Roadmap Authority

Roadmap v5 defines M30 as governed retrieval and indexing for authoritative product sources.

M30 goal:

    Add retrieval/indexing only after authoritative sources exist and only where retrieval improves usability without becoming source truth.

M30.2 checkpoint:

| Checkpoint                       | Purpose                           | Allowed work                                           | Not allowed                              |
| -------------------------------- | --------------------------------- | ------------------------------------------------------ | ---------------------------------------- |
| `M30.2` Source eligibility model | Define retrievable source classes | Only approved/eligible sources; status-aware inclusion | Index pending/TBD as mandatory authority |

M30 exit criteria require retrieval to be justified, bounded, source-traceable, and unable to override source/citation authority. DDR-005 must be closed, partially closed, or carried forward with precise remaining scope by M30 closeout.

## 4. Relationship to M30.1

M30.1 established that retrieval is justified only where it improves usability while remaining helper-only, source-traceable, limitation-visible, and non-authoritative.

M30.2 carries that decision forward by defining source eligibility before later M30 checkpoints define index metadata, traceability, non-authority enforcement, standards retrieval controls, library/template retrieval controls, evaluation, validation, UAT, and closeout.

M30.2 must preserve the following M30.1 decisions:

- retrieval is not enabled everywhere by default;
- retrieval must not decide compliance truth;
- retrieval must not decide source authority;
- retrieval must not treat pending/TBD/reference-only records as mandatory authority;
- retrieval must not create anonymous chunks without source trace;
- retrieval must not replace deterministic template selection, resolver behavior, source-library authority, standards registry authority, workflow state, UAT, or human acceptance;
- raw retrieval-to-AI truth injection remains rejected.

## 5. Source Eligibility Principles

A source class is eligible for later retrieval/indexing only when all of the following are true:

1. The source has an identifiable source path, source ID, registry entry, document ID, template ID, library ID, standards source ID, or equivalent traceable anchor.
2. The source has a known status that can be evaluated before inclusion.
3. The source status is approved, active, accepted for current scope, or otherwise explicitly eligible under this model.
4. The source has enough version, scope, or authority metadata to prevent silent overreach.
5. Retrieval can point back to the source without turning retrieval output into authority.
6. Retrieval can expose limitations to the user when authority, applicability, status, version, clause coverage, template readiness, library readiness, or scope is limited.
7. Later validation/evaluation can test whether retrieval respects source traceability and exclusion rules.

A source class is ineligible when any of the following are true:

1. The source is pending, TBD, placeholder-only, draft-only, reference-only, archived, superseded, obsolete, experimental, or unapproved unless an explicit later plan limits it to non-authoritative discovery with visible limitation warnings.
2. The source lacks source traceability.
3. The source lacks a status field or reliable status inference.
4. The source would be treated as mandatory authority merely because it appeared in retrieval results.
5. The source would cause retrieval to bypass standards registry authority, source-library authority, deterministic resolver behavior, document-factory controls, workflow state, UAT, or human acceptance.
6. The source would create product/customer/SaaS/release/deployment claims.

## 6. Source Status Model

| Source status                          | Eligibility decision                                                               | Permitted retrieval role                                                                                       | Mandatory limitation                                                        |
| -------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Approved / Active                      | Eligible                                                                           | Later retrieval may fetch or suggest context if traceable and scoped.                                          | Must cite/trace source ID, version/status, and limitation where applicable. |
| Accepted for limited scope             | Conditionally eligible                                                             | Later retrieval may fetch only within the accepted scope.                                                      | Must expose the limitation and must not generalize beyond accepted scope.   |
| Closed for governance/model scope only | Conditionally eligible                                                             | Later retrieval may expose the governance/model record as evidence of that limited closure only.               | Must not imply executable/productized closure.                              |
| Closure planned                        | Not eligible as completed authority                                                | Later retrieval may mention as a planned dependency only if explicitly included by future checkpoint controls. | Must state not closed and not product-ready authority.                      |
| Deferred                               | Not eligible as completed authority                                                | Later retrieval may mention dependency status only where governance context is needed.                         | Must state deferred and not implemented/closed.                             |
| Watch                                  | Conditionally eligible for awareness only                                          | Later retrieval may surface as watch context only if source-traceable.                                         | Must not treat as blocker or completed authority by default.                |
| Draft                                  | Not eligible as authority                                                          | Retrieval from draft material is rejected unless future checkpoint explicitly allows draft discovery.          | Must state draft/non-authoritative.                                         |
| Pending / TBD                          | Rejected                                                                           | No retrieval as mandatory authority.                                                                           | Must not be indexed as mandatory authority.                                 |
| Placeholder-only                       | Rejected as authority                                                              | No retrieval as completed source authority.                                                                    | Must not imply underlying dependency is ready.                              |
| Archived / historical                  | Rejected for current authority unless explicitly referenced as historical evidence | May be used only for historical trace if future controls allow.                                                | Must state historical/archived and not active authority.                    |
| Superseded / obsolete                  | Rejected                                                                           | No retrieval as active authority.                                                                              | Must not appear as current truth except as trace/history.                   |
| Unknown status                         | Rejected                                                                           | No retrieval until status is known.                                                                            | Must fail closed.                                                           |

## 7. Source Class Decision Table

| Source class                                                                | Eligibility decision                                                      | Rationale                                                                                                                  | Required later control                                                       |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Approved roadmap and tracker authority files                                | Eligible for governance context only                                      | They define direction and current state but do not implement retrieval truth.                                              | M30.3 traceability, M30.4 non-authority enforcement                          |
| Active governance policies and registers                                    | Eligible within their authority scope                                     | They define gates, limitations, and dependency state.                                                                      | M30.3 traceability, M30.4 non-authority enforcement                          |
| Standards source registry records with approved status                      | Conditionally eligible                                                    | Useful for standards source/citation support but must preserve DDR-004 limits.                                             | M30.3 traceability, M30.5 standards retrieval controls, M30.7 evaluation     |
| Standards records with pending/TBD/missing clause status                    | Rejected as mandatory authority                                           | Pending/TBD data must not become compliance truth through retrieval.                                                       | M30.5 limitation warnings if future discovery support is allowed             |
| Approved source-library records                                             | Eligible                                                                  | Presets, task pools, profiles, calendars, planning basis, and mappings may be useful for source-library retrieval support. | M30.3 traceability, M30.6 library/template retrieval controls                |
| Source-library records that are draft, placeholder, or unknown status       | Rejected as authority                                                     | Product behavior must not depend on unresolved source material.                                                            | Future controlled reclassification or source completion evidence             |
| Approved product templates and schemas                                      | Conditionally eligible                                                    | Useful for template search/support where template identity, version, schema binding, and status are traceable.             | M30.3 traceability, M30.6 library/template controls                          |
| Draft templates, incomplete schemas, or template notes                      | Rejected as authority                                                     | Must not replace deterministic template selection or imply product-ready generation.                                       | Future M29/M30 evidence if promoted                                          |
| Milestone evidence files                                                    | Conditionally eligible as historical/current evidence according to status | They may explain scope, closure, validation, UAT, or limitations.                                                          | M30.3 traceability and status-aware metadata                                 |
| Closed control-recovery records                                             | Eligible as historical/re-entry authority only                            | They can explain re-entry and limitation state but must not remain active blockers.                                        | M30.3 metadata marking historical/closed status                              |
| Active control-recovery plans                                               | Eligible only while active                                                | They can govern current execution when active.                                                                             | Must be status-aware and superseded when closed                              |
| Archived roadmap addenda                                                    | Rejected as active authority                                              | They are historical only unless explicitly reactivated by change control.                                                  | Historical trace only if future controls allow                               |
| Public-surface README or marketing-style docs                               | Rejected as execution authority                                           | Public surface is not project truth.                                                                                       | May be searchable only as public-facing explanation if future controls allow |
| Raw chat history, memory, local notes, temporary files, and stale downloads | Rejected                                                                  | Non-authoritative and unsafe for source-traceable product retrieval.                                                       | Not eligible                                                                 |
| Anonymous chunks without source ID/version/status                           | Rejected                                                                  | Violates source traceability and M30.3 direction.                                                                          | Not eligible                                                                 |

## 8. Inclusion Rules

Later retrieval/indexing may include a source only when the future M30 implementation checkpoint can prove all required inclusion fields:

- source class;
- source path or source ID;
- version or revision where applicable;
- status;
- authority role;
- scope limitation;
- date or build/reference timestamp where applicable;
- owner/approval or acceptance status where applicable;
- relationship to DDRs where applicable;
- rule for visible limitations;
- rule for exclusion when status becomes invalid.

If any required inclusion field is missing, the source must fail closed and remain out of retrieval/indexing until a later checkpoint supplies an approved rule.

## 9. Exclusion Rules

The following must not be included as authoritative retrieval/index sources:

- pending/TBD material as mandatory authority;
- draft-only material as current product truth;
- archived or superseded material as active authority;
- README/public-surface wording as execution state;
- raw prior chat, assistant memory, stale generated notes, or local temporary files;
- anonymous chunks;
- source fragments without traceability;
- standards references with missing or unverified clause data when the output would imply clause-level authority;
- templates/schemas that are not approved or not traceably bound;
- libraries or mappings that are not approved, status-known, and source-traceable;
- model/provider outputs;
- AI-generated content unless separately accepted into an approved source class by future governance.

## 10. DDR Impact

### DDR-005 — Standards embedding / retrieval index

Status:

    Deferred

M30.2 touches DDR-005 directly.

M30.2 does not close DDR-005.

M30.2 supplies a controlled source-eligibility planning model that DDR-005 requires before later standards embedding/retrieval implementation can be considered. DDR-005 remains deferred until later M30 evidence exists for indexing design, source eligibility, retrieval-use rules, helper-only/non-authority behavior, validation/evaluation evidence, and UAT/acceptance where applicable.

### DDR-004 — Standards source registry and citation authority

Status:

    Closed for approved standards source/citation authority model scope only.

M30.2 must preserve DDR-004 limitations.

M30.2 does not upgrade standards records into clause-level executable authority, mandatory-use authority, legal/regulatory truth, or standards-backed product authority beyond the approved registry/citation model scope.

### DDR-007 — Model/provider integration and pre-go-live operational testing path

Status:

    Closure Planned

M30.2 preserves DDR-007 awareness only.

M30.2 does not implement retrieval-to-AI handoff, AI/model/provider behavior, local AI runtime integration, app-coupled heavy-use testing, or pre-go-live execution.

If later M30.8 or M31 uses retrieval in AI context, the handoff must use context packets, citations, limitations, refusal triggers, strategy, validation, and acceptance controls.

## 11. Architecture Boundary Impact

M30.2 does not change runtime architecture.

No code, CLI behavior, state/persistence access, loaders, validators, source files, schemas, services, UI/API surfaces, AI/runtime adapters, or executable contracts are changed by this plan.

Future implementation must preserve these guardrails:

- CLI is an adapter only.
- New domain behavior must attach through approved core module boundaries.
- State and persistence access must go through approved state boundary helpers/modules.
- Any need to bypass these boundaries requires implementation pause and planning before coding.

## 12. Completion Minimum for M30.2

M30.2 is complete only when the accepted source-eligibility model exists and includes:

- active execution declaration;
- execution mode: Hybrid;
- eligible source classes;
- non-eligible source classes;
- source status model;
- source inclusion rules;
- source exclusion rules;
- DDR-005 direct impact;
- DDR-004 limitation impact;
- DDR-007 awareness;
- architecture boundary impact;
- validation expectation;
- tracker movement rule;
- explicit non-implementation claims.

This file is intended to satisfy the M30.2 planning/source-control evidence requirement after Project Owner review and acceptance.

## 13. Tracker Movement Rule

Tracker movement from M30.2 must not occur until:

1. this M30.2 source-eligibility model is reviewed and accepted;
2. the tracker records M30.2 completion as Hybrid planning/source-control evidence, not runtime implementation;
3. the tracker points to `M30.3 — Index metadata and traceability` as the next normal checkpoint only after acceptance;
4. the tracker preserves GO/implementation restrictions for M30.3 until M30.3 receives its own anti-drift PLAN/GO controls;
5. the Active Assistant Execution Gate is replaced with a new checkpoint-specific gate for M30.3 or clearly records why no gate is active.

## 14. Validation Expectation

This M30.2 plan is documentation/governance/source-control planning only.

No executable validation was run or required because this file does not modify code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, source data, or executable contracts.

If later M30 work changes code, tests, source JSON, validators, loaders, schemas, runtime behavior, or executable contracts, validation must include:

    python -m pytest -q

## 15. Explicit Non-Implementation Claims

This M30.2 plan does not:

- complete M30.3 or any later M30 checkpoint;
- authorize tracker advancement by itself without Project Owner review/acceptance;
- implement retrieval;
- implement indexing;
- implement embeddings;
- create a vector store;
- implement standards-backed live lookup;
- implement retrieval-backed source authority;
- implement source filters in runtime code;
- implement source loaders or validators;
- alter deterministic resolver behavior;
- alter template selection/loading behavior;
- alter document generation or rendering behavior;
- alter standards authority;
- implement AI/model/provider behavior;
- implement retrieval-to-AI handoff;
- implement UI/API behavior;
- authorize deployment, release, productization, commercial launch, SaaS readiness, or customer-ready output;
- close DDR-005;
- expand DDR-004 beyond its approved standards source/citation authority model scope;
- close or reclassify DDR-007;
- close the active CAPA.

## 16. Immediate Next Action

After this plan is reviewed and accepted, prepare a bounded tracker update to record:

    M30.2 complete as Hybrid planning/source-control evidence.
    Next checkpoint: M30.3 — Index metadata and traceability.
    GO and implementation remain blocked until M30.3 receives its own anti-drift PLAN/GO control.
