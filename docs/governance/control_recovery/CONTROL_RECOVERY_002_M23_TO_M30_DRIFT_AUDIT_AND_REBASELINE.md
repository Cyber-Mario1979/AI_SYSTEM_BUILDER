---
doc_type: corrective_control_plan
canonical_name: CONTROL_RECOVERY_002_M23_TO_M30_DRIFT_AUDIT_AND_REBASELINE
status: ACTIVE
governs_execution: true
document_state_mode: active_control_recovery_gate
authority: active_recovery_control
control_recovery_id: CONTROL-RECOVERY-002
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: vbuilder-cr002
created_date: 2026-05-31
live_repo_write: YES_RECOVERY_SCOPE_ONLY
source_baseline_commit: a69a48dc46fade495beea274c174fd1c6f5a1b39
normal_execution_state: PAUSED
normal_next_checkpoint_before_pause: PLAN M30.1 — Retrieval justification gate
---

# CONTROL-RECOVERY-002 — M23-to-M30 Drift Audit and Rebaseline

## 1. Purpose

CONTROL-RECOVERY-002 opens an active recovery lane to audit and rebaseline the drift observed from Milestone 23 through the latest pushed state before normal M30.1 planning resumes.

The recovery goal is not to continue product work. The recovery goal is to determine what evidence is trustworthy, what claims must be limited, what tracker state must be corrected, and what repo authority surfaces must be preserved or quarantined before any new M30 work proceeds.

## 2. Activation Decision

Normal roadmap execution is paused for the affected lane.

The paused normal next checkpoint is:

```text
PLAN M30.1 — Retrieval justification gate
```

M30.1 normal planning must not resume until CONTROL-RECOVERY-002 exits by recorded closeout or Project Owner decision.

## 3. Why This Control Exists

Repository evidence already shows a drift pattern beginning around the M23-M25 transition:

```text
Phase 8 boundary / deployment / operational-governance work
→ early productization and commercial-readiness assessment
→ roadmap v5 redirect
→ governance-heavy recovery controls
→ later build/content recovery attempts
→ residual active CAPA and M30 pre-plan gate controls
```

The specific risk is that governance or Markdown evidence may be mistaken for implementation, runtime source truth, product capability, validation closure, UAT closure, or readiness to enter retrieval/indexing work.

## 4. Source Basis

This control recovery lane must use repository truth only.

Required source set:

- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`
- `docs/governance/ACTIVE_CONTEXT_BOUNDARY_POLICY.md`
- `docs/governance/ASBP_CONTEXT_RESET_CAPA.md`
- `docs/governance/control_recovery/CONTROL_RECOVERY_001_CLOSURE_RECORD.md`
- `docs/archives/control_recovery/CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR.md`
- M23 through M30 milestone, UAT, validation, remediation, change-control, and closeout evidence
- current `asbp/`, `data/source/`, and `tests/` repo reality
- latest main commit before this recovery branch: `a69a48dc46fade495beea274c174fd1c6f5a1b39`

Old Project chats, memory, stale local notes, and uncommitted work are not execution authority.

## 5. Recovery Scope

### In scope

- Confirm the existence, location, and severity of drift from M23 through latest commit.
- Build an evidence matrix for every checkpoint and control action from M23 through current M30.1 pre-plan state.
- Classify each checkpoint as keep, reclassify, reopen, carry forward, quarantine, or supersede.
- Separate governance evidence from implementation/source/runtime evidence.
- Identify unsupported productization, release, customer-ready, SaaS-ready, standards-backed, retrieval-backed, AI-ready, or UAT-ready claims.
- Correct tracker recovery state if required.
- Prepare a surgical remediation and rebaseline plan.
- Preserve valid implementation evidence from M27-M29 unless the audit proves it is invalid.

### Out of scope

- Normal M30.1 planning.
- M30 implementation.
- Retrieval implementation.
- Indexing implementation.
- Embedding implementation.
- Standards-backed live lookup.
- Retrieval-backed source authority.
- AI/model/provider behavior.
- UI/API behavior.
- Deployment, release, productization, commercial-readiness, SaaS-readiness, or customer-ready claims.
- File deletion, archive moves, promotion, canonicalization, or repo surgery before the audit matrix is accepted.

## 6. Active Control Status

CONTROL-RECOVERY-002 governs the recovery lane while active.

Allowed activities:

1. `SS`, `STATUS`, and `NEXT` for recovery state only.
2. Recovery branch work for CONTROL-RECOVERY-002 only.
3. Evidence-matrix drafting for M23 through current M30.1 pre-plan state.
4. Claim quarantine review.
5. Tracker recovery-state correction that does not advance normal roadmap progress.
6. Recovery PR preparation and review.
7. Recovery closeout only after exit criteria are met.

Blocked activities:

1. Normal `PLAN M30.1`.
2. `GO` for any normal roadmap checkpoint.
3. Tracker advancement beyond the recovery state.
4. M30 retrieval/indexing/embedding implementation.
5. New checkpoint evidence that implies M30.1 progress or completion.
6. Product/runtime/source implementation outside recovery scope.
7. Productization, deployment, release, SaaS readiness, or customer-ready work.

## 7. Recovery Phases

### Phase 0 — Open the recovery gate

Deliverables:

- this control recovery plan;
- tracker recovery-state alignment, if required;
- PR opened from a dedicated recovery branch.

Completion minimum:

- CONTROL-RECOVERY-002 exists in repo governance/control recovery path;
- normal M30.1 execution is explicitly paused;
- blocked and allowed activities are clear.

### Phase 1 — M23-to-current evidence matrix

Deliverable:

```text
docs/governance/control_recovery/CONTROL_RECOVERY_002_M23_TO_M30_EVIDENCE_MATRIX.md
```

Minimum matrix fields:

- checkpoint/control action;
- declared execution mode;
- expected completion minimum;
- actual evidence;
- implementation/source files;
- data/source files;
- tests;
- validation evidence;
- UAT / owner acceptance evidence;
- DDR impact;
- claim risk;
- audit decision.

### Phase 2 — Claim quarantine review

Deliverable:

```text
docs/governance/control_recovery/CONTROL_RECOVERY_002_CLAIM_QUARANTINE_REVIEW.md
```

Minimum review target:

- product-ready;
- customer-ready;
- SaaS-ready;
- commercial-ready;
- release-ready;
- deployment-ready;
- go-live;
- AI-ready;
- retrieval-authoritative;
- standards-backed output;
- validated product;
- UAT complete.

### Phase 3 — Tracker and authority rebaseline

Deliverable:

```text
docs/governance/control_recovery/CONTROL_RECOVERY_002_REBASELINE_DECISION.md
```

The decision must state whether current main may proceed to normal M30.1 planning, must stay paused, or must undergo further repo surgery.

### Phase 4 — Surgical remediation package, if required

Possible outputs:

- metadata hygiene corrections;
- tracker corrections;
- claim corrections;
- archive / quarantine plan;
- cleanup PR plan;
- roadmap interpretation or change-control proposal.

No cleanup, deletion, relocation, or canonicalization is allowed unless the accepted rebaseline decision explicitly authorizes it.

### Phase 5 — Recovery closeout

Deliverable:

```text
docs/governance/control_recovery/CONTROL_RECOVERY_002_CLOSURE_RECORD.md
```

CONTROL-RECOVERY-002 closes only when exit criteria are met.

## 8. Exit Criteria

CONTROL-RECOVERY-002 may close only when:

1. the M23-to-current evidence matrix is complete and reviewed;
2. unsupported or ambiguous readiness claims are either corrected, limited, or explicitly carried forward;
3. tracker state is aligned to the accepted recovery outcome;
4. active CAPA status is either accepted for closure or explicitly carried forward;
5. no normal M30.1 progress is claimed during recovery unless separately authorized by a recovery closeout decision;
6. Project Owner acceptance is recorded;
7. a closure record exists in `docs/governance/control_recovery/`.

## 9. Validation Expectation

This recovery gate is documentation/governance-only.

No executable validation is required for this file because it does not modify code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, source data, or executable contracts.

If later recovery work changes code, tests, source JSON, validators, loaders, schemas, runtime behavior, or executable contracts, validation must include:

```text
python -m pytest -q
```

## 10. Explicit Non-Implementation Claims

This control recovery plan does not:

- start M30.1 normal planning;
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
- delete, archive, move, rename, promote, or canonicalize repository files.

## 11. Immediate Next Recovery Action

After this recovery gate is reviewed and accepted, the next recovery action is:

```text
CONTROL-RECOVERY-002 Phase 1 — Build M23-to-current evidence matrix
```
