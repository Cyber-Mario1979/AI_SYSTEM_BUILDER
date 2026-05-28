---
doc_type: governance_policy
canonical_name: BUILD_GOVERNANCE_BALANCE_POLICY
status: ACTIVE
governs_execution: true
document_state_mode: execution_governance_policy
authority: build_governance_balance_control
scope: checkpoint_execution_classification_and_anti_drift_control
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: feature/m27-cqv-source-content-expansion
created_date: 2026-05-27
live_repo_write: YES
control_recovery_amendment: CONTROL-RECOVERY-001_PHASE_2
control_recovery_amended_branch: feature/m28-1-standards-registry-baseline-review
control_recovery_amended_date: 2026-05-28
---

# Build / Governance Balance Policy

## Purpose

This policy prevents ASBP / ASPP execution from drifting into excessive governance or documentation-only progress while preserving the governance controls that keep the project deterministic, auditable, and safe.

The governing principle is:

**Governance defines the boundary. Implementation proves progress. Validation proves truth.**

This policy does not reduce roadmap authority, architecture guardrails, DDR gate rules, validation obligations, UAT requirements, source-of-truth rules, or repository write controls.

It adds an execution-balance rule: when a roadmap checkpoint is build/content/runtime/source-library work, it must not be closed by documentation alone.

This `CONTROL-RECOVERY-001` amendment strengthens the policy with hard-stop rules so ambiguous checkpoint wording cannot be interpreted as governance-only by default, and so tracker movement cannot occur for hybrid/build-content checkpoints without the required implementation/source and validation evidence.

## Authority and Source Role

This policy is a repo-side governance policy.

It governs how active and future checkpoints are classified, planned, executed, validated, and advanced in the tracker.

It does not override:

- `ROADMAP_CANONICAL.md`
- active roadmap addenda, if any are explicitly approved later
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- active `docs/governance/control_recovery/*.md` plans
- `PROGRESS_TRACKER.md`
- repo reality from code, tests, package structure, validation evidence, UAT evidence, and milestone closeout evidence

If this policy appears to conflict with roadmap, guardrails, DDR, an active control-recovery plan, tracker state, or repo reality, execution must stop and the conflict must be resolved before implementation.

## Mandatory Read / Apply Triggers

This policy must be read and applied:

- at ASBP working-session start after the deferred dependencies register when present;
- before `STATUS`, `NEXT`, and `PLAN` when the next checkpoint is build/content or hybrid work;
- before every `GO` action;
- before package generation, replacement-file generation, `apply.py` generation, tracker updates, or checkpoint closeout;
- before tracker advancement;
- before milestone validation, UAT, or closeout;
- before any source-library, runtime model, loader/validator, document factory, standards, retrieval, AI/runtime, UI/API, product workflow, or productization work.

## Execution Modes

Every checkpoint must be classified before planning or implementation.

| Execution Mode | Meaning | Completion evidence |
|---|---|---|
| Governance-only | Scope lock, decision record, change control, cleanup planning, review, explicit governance alignment, or recovery-control amendment. | Governance artifact, consistency review, tracker update when supported, owner acceptance where applicable. |
| Build/content | Runtime code, source data, source library records, loaders, validators, executable behavior, product workflow, product output, or implementation assets. | Code/source/content assets plus tests/validation where applicable. Documentation alone is not enough. |
| Hybrid | Governance boundary plus runtime/source/content implementation or future runtime-facing contract/model. | Governance artifact plus implementation/source/contract assets plus tests/validation where applicable. Narrative evidence alone is not enough unless the roadmap explicitly says governance-only. |
| Validation | Validation evidence checkpoint. | Required validation evidence, recorded truthfully, including `python -m pytest -q` when executable behavior changed. |
| UAT | Actual user acceptance testing, owner acceptance, or both, explicitly stated by the roadmap. | UAT protocol/report or owner acceptance evidence required by the checkpoint, with validation reference where applicable. |
| Closeout | Milestone boundary freeze. | Closeout record referencing required validation, UAT, DDR carry-forward, limitations, and next state. |

For M27 onward, build/content and hybrid checkpoints are the default unless the roadmap checkpoint is explicitly governance-only, validation-only, UAT-only, or closeout-only.

For Phase 9 and later local integrated CQV product-core work, wording such as `define`, `scope`, `model`, `review`, `decide`, `assess`, `gate`, `framework`, `authority`, or `behavior` must not be treated as governance-only by inference. If the roadmap does not explicitly classify the checkpoint and define the completion minimum, execution stops before `PLAN` or `GO`.

## Hard Stop for Ambiguity

Execution must stop before `PLAN`, `GO`, package generation, tracker movement, or checkpoint closeout when any required checkpoint-control field is missing, ambiguous, or conflicting.

Required checkpoint-control fields are:

1. execution mode;
2. required completion artifact;
3. implementation/source minimum;
4. validation requirement;
5. tracker movement rule;
6. explicit non-implementation claims;
7. DDR impact when the checkpoint touches a registered dependency domain;
8. architecture boundary impact when the checkpoint touches code, runtime models, source contracts, loaders, validators, state, CLI, UI/API, AI/runtime, deployment, or product behavior.

If the checkpoint-control fields cannot be proven from the active roadmap, tracker, governance files, and repo reality, the assistant must not infer the missing control field from memory, prior chat, title wording, or convenience.

The correct response is to stop and request a roadmap interpretation or controlled amendment.

## Anti-Drift Gate for PLAN

Every `PLAN` governed by this policy must include an anti-drift gate with these fields:

1. **Execution Mode** — governance-only, build/content, hybrid, validation, UAT, or closeout.
2. **Implementation Minimum** — the runtime/code/source-data/source-contract/test asset, validation evidence, UAT evidence, or governance artifact that must change or be created.
3. **Governance Boundary** — the policy, roadmap, DDR, control-recovery, or design boundary being preserved.
4. **Validation Evidence Required** — pytest, source validation, consistency review, UAT, or no executable validation with reason.
5. **Tracker Movement Rule** — what evidence must exist before the tracker advances.
6. **Explicit Non-Implementation Claims** — what the checkpoint does not implement or authorize.

If the implementation minimum is only a document, the plan must state clearly that the work is governance-only and cannot be counted as runtime/source/product implementation unless the checkpoint is explicitly governance-only, validation-only, UAT-only, or closeout-only.

If any anti-drift field is missing or uncertain, `PLAN` must stop instead of drafting an implementation path.

## Anti-Drift Gate for GO

Every `GO` governed by this policy must satisfy these rules before preparing amendments or performing allowed writes:

1. Confirm the active control state, including any active control-recovery pause.
2. Confirm execution mode.
3. Confirm completion minimum.
4. Confirm validation requirement.
5. Confirm DDR impact and blocker status when the work touches a registered dependency domain.
6. Confirm architecture boundary impact when the work touches code, source contracts, runtime models, loaders, validators, CLI, UI/API, AI/runtime, deployment, or product behavior.
7. Confirm tracker movement rule.
8. Confirm explicit non-implementation claims.

`GO` must not generate `apply.py`, replacement files, tracker updates, package content, or checkpoint-closeout content until this preflight is satisfied.

For build/content or hybrid checkpoints, `GO` must prepare implementation/source/contract assets first. Governance artifacts may record boundaries, but they must not replace implementation.

Add or update tests when code, runtime models, validators, loaders, source contracts, or executable behavior change.

Run or instruct validation with:

    python -m pytest -q

when code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, or executable contracts change.

Do not advance `PROGRESS_TRACKER.md` until required implementation evidence and validation evidence exist.

Do not claim checkpoint completion based on roadmap placement, memory, chat agreement, owner approval alone, or documentation alone.

Do not bypass DDR blockers, architecture guardrails, source-of-truth rules, validation truth, or active control-recovery limits in the name of implementation speed.

## Self-Audit Before Closure or Tracker Movement

Before preparing any checkpoint closure, milestone closeout, tracker advancement, PR body, or recovery verification that could imply completion, the assistant must internally ask:

**Am I about to close a checkpoint with only a document?**

If yes, execution must stop unless the checkpoint is explicitly classified as governance-only, validation-only, UAT-only, or closeout-only and the required non-executable evidence exists.

For hybrid or build/content checkpoints, a document may support completion only when the required implementation/source/contract assets and validation evidence also exist, or when the roadmap-authorized checkpoint explicitly records a formal deferral decision.

## Retrospective Execution Interpretation

The following recent work remains useful and valid for its approved scope, but its execution interpretation must be recorded honestly.

| Scope | Interpretation |
|---|---|
| M25 | Governance/reset milestone. Useful and intentional roadmap reset, cleanup gate, DDR alignment, and evidence preservation. Not product-build implementation. |
| M26 | Source-boundary governance milestone. Useful authority lock for local CQV MVP source families. Not runtime/source-library implementation. |
| M27.1 | Preset-family scope decision. Useful boundary lock for initial preset families. Documentation/governance/source-scope only. |
| M27.2 | Selector/scope-intent decision. Useful boundary lock for selector inputs and human confirmation gate. Documentation/governance/source-scope only. |
| M27.3 | First corrected M27 runtime/source implementation checkpoint. Introduces runtime-loadable task-pool source model, source data, loader/validator behavior, tests, and validation evidence. |

This retrospective interpretation does not invalidate M25, M26, M27.1, or M27.2.

It prevents them from being mistaken for completed runtime/source implementation.

## Build / Governance Balance Rule

Governance must remain strong, but governance must not be allowed to impersonate implementation.

Implementation must move forward, but implementation must not bypass governance.

Therefore:

- governance-only checkpoints may close with governance evidence only;
- build/content checkpoints must include implementation/source/content evidence;
- hybrid checkpoints must include both governance evidence and implementation/source/contract evidence;
- validation checkpoints must include truthful validation evidence;
- UAT checkpoints must include the UAT or acceptance evidence required by the roadmap;
- closeout checkpoints must reference required validation, UAT, DDR carry-forward, and limitations;
- validation evidence must support completion claims;
- tracker advancement must be evidence-based;
- future milestone closeout must distinguish governance closure from runtime/product capability closure.

## M27 Forward Rule

Starting before M27.4, M27 execution must proceed as controlled build/content or hybrid work unless the checkpoint is explicitly governance-only.

For M27 checkpoints:

- M27.4 profile model should include runtime/source profile structures or source assets where needed, not documentation alone.
- M27.5 calendar/work-time model should include runtime/source calendar structures or source assets where needed, not documentation alone.
- M27.6 planning basis and duration model should include runtime/source duration/planning structures or source assets where needed, not documentation alone.
- M27.7 mapping model should include source mapping structures or validation where needed, not documentation alone.
- M27.8 implementation wave must integrate the controlled source-library baseline rather than restart governance discussion.
- M27.9 and later validation checkpoints must validate actual relationships and source behavior.

## Phase 9 Product-Core Rule

For Phase 9 local integrated CQV product-core work, ambiguous wording defaults to stop or hybrid/build-content classification, never governance-only by inference.

A document-only package can close Phase 9 work only when the active roadmap checkpoint is explicitly governance-only, validation-only, UAT-only, or closeout-only and the required review, validation, UAT, or closeout evidence exists.

M29 through M34 must not execute until their active checkpoint tables include execution mode, completion minimum, validation requirement, and tracker movement rule, or until a roadmap interpretation/amendment supplies those controls.

## Tracker Rule

`PROGRESS_TRACKER.md` must not be advanced for a build/content or hybrid checkpoint until the required implementation/source/contract evidence exists.

For code-affecting work, tracker advancement must wait until validation has passed or until the tracker explicitly records an unresolved validation state.

For docs-only governance work, tracker advancement may occur only when the roadmap checkpoint is explicitly governance-only or when the tracker clearly states that no runtime/source implementation was completed.

For validation checkpoints, tracker advancement requires truthful validation evidence or an explicit unresolved validation state.

For UAT checkpoints, tracker advancement requires actual UAT or owner-acceptance evidence required by the roadmap.

For closeout checkpoints, tracker advancement requires the closeout record and required references to validation, UAT, DDR carry-forward, and limitations.

Tracker movement must not occur from:

- narrative evidence alone for hybrid/build-content checkpoints;
- roadmap placement alone;
- prior chat agreement;
- memory;
- owner approval alone where implementation or validation evidence is required;
- uncommitted local work;
- unverified generated packages;
- stale public-surface wording.

## DDR and Guardrail Protection

This policy does not downgrade DDRs, close DDRs, reopen DDRs, or reclassify DDRs.

This policy does not weaken architecture guardrails.

This policy does not authorize:

- raw state/file access outside approved boundaries;
- deployment-compiled lookup shortcuts;
- product-ready document generation without document factory readiness;
- standards retrieval/embedding before standards authority prerequisites;
- AI/model/provider behavior without roadmap-authorized strategy and evidence;
- UI/API behavior that bypasses core/service/runtime boundaries;
- productization/SaaS readiness claims without product-core validation, UAT, and re-entry approval.

## CONTROL-RECOVERY-001 Enforcement

While an active repo-side control-recovery plan governs execution, this policy must be applied inside that recovery lane only.

Normal roadmap implementation remains paused when the active control-recovery plan says it is paused.

Recovery-scope governance amendments may strengthen this policy, but they must not hide normal roadmap build work, normal tracker advancement, normal checkpoint closure, product/runtime/code implementation, PR merge, branch deletion, issue closure, release, deployment, productization, or SaaS action.

Normal roadmap execution resumes only when the active control-recovery plan is fully implemented, verified, owner-approved, and archived or closed according to its own rule.

## Acceptance Criteria

This policy is active when:

- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` exists in the repository;
- `PROGRESS_TRACKER.md` records that the policy is active before M27.4;
- active and future `PLAN` and `GO` responses classify checkpoints by execution mode;
- hard-stop rules prevent ambiguous checkpoints from proceeding before `PLAN` or `GO`;
- `GO` package generation does not occur before execution mode, completion minimum, validation requirement, DDR status, and tracker movement rule are confirmed;
- future build/content and hybrid checkpoints are not closed by documentation-only evidence;
- tracker movement remains evidence-based and cannot advance hybrid/build-content work from narrative evidence alone;
- governance remains mandatory and evidence-based rather than removed or weakened.

## Validation Expectation

This policy is documentation/governance-only.

No executable validation is required unless a separate change modifies code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, or executable contracts.

Document consistency review is required for this policy amendment.
