---
doc_type: recovery_rebaseline_decision
canonical_name: CONTROL_RECOVERY_002_REBASELINE_DECISION
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: recovery_decision_evidence
authority: control_recovery_002_phase_3_rebaseline_decision
control_recovery_id: CONTROL-RECOVERY-002
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-cr002-phase3-rebaseline
created_date: 2026-05-31
source_baseline_commit: 227549101e924f81a9916fcb99d29b19c5fa8a5a
live_repo_write: YES_RECOVERY_SCOPE_ONLY
normal_execution_state: PAUSED
---

# CONTROL-RECOVERY-002 — Tracker and Authority Rebaseline Decision

## 1. Purpose

This record supports CONTROL-RECOVERY-002 Phase 3 by deciding the current recovery authority state after completion of:

- CONTROL-RECOVERY-002 Phase 0 — recovery gate opening;
- CONTROL-RECOVERY-002 Phase 1 — M23-to-M30 evidence matrix;
- CONTROL-RECOVERY-002 Phase 2 — claim quarantine review.

The decision establishes whether normal M30.1 planning may resume, whether recovery remains active, what authority surfaces govern next work, and what tracker alignment is required before any normal roadmap execution continues.

This record is recovery decision evidence only. It does not advance normal roadmap progress and does not authorize retrieval, indexing, embeddings, AI, UI/API, deployment, release, productization, SaaS readiness, or customer-ready output.

## 2. Source Basis

This decision is based on repository evidence only:

- `docs/governance/control_recovery/CONTROL_RECOVERY_002_M23_TO_M30_DRIFT_AUDIT_AND_REBASELINE.md`
- `docs/governance/control_recovery/CONTROL_RECOVERY_002_M23_TO_M30_EVIDENCE_MATRIX.md`
- `docs/governance/control_recovery/CONTROL_RECOVERY_002_CLAIM_QUARANTINE_REVIEW.md`
- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`
- `docs/governance/ACTIVE_CONTEXT_BOUNDARY_POLICY.md`
- `docs/governance/ASBP_CONTEXT_RESET_CAPA.md`
- M23 through M30 milestone, validation, UAT, remediation, index, and closeout evidence
- current `asbp/`, `data/source/`, and `tests/` repo reality as summarized by the recovery matrix

Old Project chat history, memory, uncommitted files, stale temporary notes, and local-only assumptions are not execution authority.

## 3. Recovery Findings Accepted for Rebaseline

The following findings are accepted for this rebaseline decision:

1. Drift exists primarily as execution-governance drift, not simple code drift.
2. M23 and M24 remain valid as historical Phase 8 boundary/governance evidence but do not prove deployment, go-live, productization, or SaaS readiness.
3. M25.3 is the major visible transition point where commercial/productization assessment language created readiness-overclaim risk.
4. Roadmap v5 and M25 closeout redirected execution away from premature productization/SaaS readiness.
5. M26 remains useful as a compressed source-boundary authority lock but is not source-content/runtime implementation.
6. M27 contains supportable implementation evidence for the controlled source-library baseline scope, with previously identified metadata hygiene issues handled under CONTROL-RECOVERY-001.
7. CONTROL-RECOVERY-001 remains historical recovery evidence only; permanent controls remain in active governance files.
8. M28 and M29 appear supportable for their recorded limited scopes, with DDR and claim limitations carried forward.
9. M29 is the latest supportable implementation/validation baseline, but it remains milestone-scope only and not product/customer/SaaS readiness.
10. M30.1 normal planning should not resume until tracker state explicitly reflects CONTROL-RECOVERY-002 and the Project Owner accepts the rebaseline path.

## 4. Authority Rebaseline Decision

Decision:

```text
Current main must stay in CONTROL-RECOVERY-002 recovery mode.
Normal M30.1 planning remains paused.
Proceed next to controlled tracker recovery-state alignment, then CONTROL-RECOVERY-002 closeout preparation if the Project Owner accepts this rebaseline.
```

This decision does not invalidate M27-M29 implementation evidence.

This decision does not roll back the repository to M23.

This decision preserves useful evidence and quarantines broad readiness claims instead of deleting or rewriting history.

## 5. Active Authority Stack After This Decision

Until CONTROL-RECOVERY-002 closes, the active authority stack for execution is:

1. repo reality from `main`;
2. `ROADMAP_CANONICAL.md`;
3. active recovery authority: `docs/governance/control_recovery/CONTROL_RECOVERY_002_M23_TO_M30_DRIFT_AUDIT_AND_REBASELINE.md`;
4. Phase 1 recovery matrix: `docs/governance/control_recovery/CONTROL_RECOVERY_002_M23_TO_M30_EVIDENCE_MATRIX.md`;
5. Phase 2 claim quarantine: `docs/governance/control_recovery/CONTROL_RECOVERY_002_CLAIM_QUARANTINE_REVIEW.md`;
6. this rebaseline decision;
7. `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`;
8. `docs/governance/ACTIVE_CONTEXT_BOUNDARY_POLICY.md`;
9. `docs/governance/ASBP_CONTEXT_RESET_CAPA.md`;
10. `PROGRESS_TRACKER.md`, after recovery-state alignment is applied.

CONTROL-RECOVERY-001 remains historical evidence only and does not govern active execution.

## 6. Tracker Rebaseline Requirement

`PROGRESS_TRACKER.md` must be aligned before normal M30.1 planning resumes.

Required tracker state:

- Current milestone remains `M30 — Governed Retrieval and Indexing for Authoritative Product Sources`.
- Current status must state `PAUSED BY CONTROL-RECOVERY-002` until recovery closes.
- Active control recovery gate must be `CONTROL-RECOVERY-002`.
- Exact next unfinished work must be recovery work, not normal M30.1.
- Normal next roadmap checkpoint must be preserved as paused: `PLAN M30.1 — Retrieval justification gate`.
- Latest completed roadmap checkpoint remains `M29.13 — Milestone closeout`.
- Latest completed control actions include post-M29 full repository index, CONTROL-RECOVERY-002 Phase 1 evidence matrix, and CONTROL-RECOVERY-002 Phase 2 claim quarantine review after their PRs are merged.
- Latest executable validation remains the M29/CQV content-library validation record unless later executable changes occur.
- CAPA remains active until Project Owner accepts that the context-boundary/build-first control is working after qualifying future execution.

This rebaseline decision does not itself replace the tracker. It defines the required tracker alignment for the next bounded recovery PR or targeted tracker update.

## 7. Normal M30.1 Re-Entry Conditions

Normal M30.1 planning may resume only after all of the following are true:

1. CONTROL-RECOVERY-002 Phase 3 rebaseline decision is reviewed and accepted.
2. `PROGRESS_TRACKER.md` is aligned to the recovery state or recovery closeout state.
3. Project Owner accepts that broad readiness claims are quarantined or limited.
4. CONTROL-RECOVERY-002 closure record either closes the recovery gate or explicitly authorizes normal M30.1 planning to resume.
5. M30.1 resumes only from the prior accepted classification:

```text
M30.1 is Hybrid.
```

6. M30.1 resumes as planning only, not implementation.
7. M30.1 must still preserve DDR-005, DDR-004 limitations, DDR-007 awareness, source authority, and non-authoritative retrieval boundaries.

## 8. Required Next Recovery Step

Next recovery action:

```text
CONTROL-RECOVERY-002 Phase 3A — Tracker recovery-state alignment
```

Minimum tracker alignment scope:

- mark CONTROL-RECOVERY-002 as active;
- mark normal M30.1 planning as paused;
- record Phase 1 and Phase 2 recovery evidence as completed recovery actions;
- set exact next unfinished work to recovery closeout preparation or tracker alignment review;
- keep CAPA active;
- avoid normal roadmap advancement.

If tracker replacement is not performed by tool due to platform constraints, the tracker patch must be provided as a targeted manual edit or separate PR-ready file.

## 9. Validation Expectation

This rebaseline decision is documentation/governance-only.

No executable validation was run or required because this file does not modify code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, source data, or executable contracts.

If later recovery work changes code, tests, source JSON, validators, loaders, schemas, runtime behavior, or executable contracts, validation must include:

```text
python -m pytest -q
```

## 10. Explicit Non-Implementation Claims

This rebaseline decision does not:

- resume normal M30.1 planning;
- complete M30.1;
- authorize `GO`;
- advance the tracker as normal roadmap progress;
- implement retrieval;
- implement indexing;
- implement embeddings;
- implement standards-backed live lookup;
- implement retrieval-backed source authority;
- implement AI/model/provider behavior;
- implement UI/API behavior;
- authorize deployment, release, productization, commercial launch, SaaS readiness, or customer-ready output;
- delete, archive, move, rename, promote, or canonicalize repository files;
- close CONTROL-RECOVERY-002.
