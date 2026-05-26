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
---

# Build / Governance Balance Policy

## Purpose

This policy prevents ASBP / ASPP execution from drifting into excessive governance or documentation-only progress while preserving the governance controls that keep the project deterministic, auditable, and safe.

The governing principle is:

**Governance defines the boundary. Implementation proves progress. Validation proves truth.**

This policy does not reduce roadmap authority, architecture guardrails, DDR gate rules, validation obligations, UAT requirements, source-of-truth rules, or repository write controls.

It adds an execution-balance rule: when a roadmap checkpoint is build/content/runtime/source-library work, it must not be closed by documentation alone.

## Authority and Source Role

This policy is a repo-side governance policy.

It governs how future checkpoints are classified and executed.

It does not override:

- `ROADMAP_CANONICAL.md`
- active roadmap addenda, if any are explicitly approved later
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `PROGRESS_TRACKER.md`
- repo reality from code, tests, package structure, validation evidence, UAT evidence, and milestone closeout evidence

If this policy appears to conflict with roadmap, guardrails, DDR, tracker state, or repo reality, execution must stop and the conflict must be resolved before implementation.

## Mandatory Read / Apply Triggers

This policy must be read and applied:

- at ASBP working-session start after the deferred dependencies register when present;
- before `STATUS`, `NEXT`, and `PLAN` when the next checkpoint is build/content/hybrid work;
- before every `GO` action;
- before tracker advancement;
- before milestone validation, UAT, or closeout;
- before any source-library, runtime model, loader/validator, document factory, standards, retrieval, AI/runtime, UI/API, product workflow, or productization work.

## Execution Modes

Every checkpoint must be classified before planning or implementation.

| Execution Mode | Meaning | Completion evidence |
|---|---|---|
| Governance-only | Scope lock, decision record, change control, cleanup planning, UAT, closeout, acceptance, or explicit governance alignment. | Governance artifact, tracker update when supported, owner acceptance where applicable. |
| Build/content | Runtime code, source data, source library records, loaders, validators, executable behavior, product workflow, or implementation assets. | Code/source assets plus tests/validation where applicable. Documentation alone is not enough. |
| Hybrid | Governance boundary plus runtime/source/content implementation. | Governance artifact plus code/source assets plus tests/validation where applicable. |

For M27 onward, build/content and hybrid checkpoints are the default unless the roadmap checkpoint is explicitly governance-only.

## Anti-Drift Gate for PLAN

Every future `PLAN` must include an anti-drift gate with these fields:

1. **Execution Mode** — governance-only, build/content, or hybrid.
2. **Implementation Minimum** — the runtime/code/source-data/test asset that must change or be created.
3. **Governance Boundary** — the policy, roadmap, DDR, or design boundary being preserved.
4. **Validation Evidence Required** — pytest, source validation, consistency review, UAT, or no executable validation with reason.
5. **Tracker Movement Rule** — what evidence must exist before the tracker advances.
6. **Explicit Non-Implementation Claims** — what the checkpoint does not implement.

If the implementation minimum is only a document, the plan must state clearly that the work is governance-only and cannot be counted as runtime/source implementation unless the checkpoint is explicitly governance-only.

## Anti-Drift Gate for GO

Every future `GO` must satisfy these rules:

1. For build/content or hybrid checkpoints, prepare implementation/source assets first.
2. Use governance artifacts to record boundaries, not to replace implementation.
3. Add or update tests when code, runtime models, validators, loaders, source contracts, or executable behavior change.
4. Run or instruct validation with `python -m pytest -q` when code changed.
5. Do not advance `PROGRESS_TRACKER.md` until required implementation evidence and validation evidence exist.
6. Do not claim checkpoint completion based on roadmap placement, memory, chat agreement, or documentation alone.
7. Do not bypass DDR blockers, architecture guardrails, source-of-truth rules, or validation truth in the name of implementation speed.

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
- build/content checkpoints must include implementation evidence;
- hybrid checkpoints must include both governance evidence and implementation evidence;
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

## Tracker Rule

`PROGRESS_TRACKER.md` must not be advanced for a build/content or hybrid checkpoint until the required implementation evidence exists.

For code-affecting work, tracker advancement must wait until validation has passed or until the tracker explicitly records an unresolved validation state.

For docs-only governance work, tracker advancement may occur only when the roadmap checkpoint is governance-only or when the tracker clearly states that no runtime/source implementation was completed.

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

## Acceptance Criteria

This policy is active when:

- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` exists in the repository;
- `PROGRESS_TRACKER.md` records that the policy is active before M27.4;
- future `PLAN` and `GO` responses classify checkpoints by execution mode;
- future build/content checkpoints are not closed by documentation-only evidence;
- governance remains mandatory and evidence-based rather than removed or weakened.

## Validation Expectation

This policy is documentation/governance-only.

No executable validation is required unless a separate change modifies code, commands, imports, schemas, tests, runtime behavior, CLI behavior, or executable contracts.
