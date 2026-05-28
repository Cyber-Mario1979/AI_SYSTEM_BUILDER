---
doc_type: corrective_control_plan
canonical_name: CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR
status: PROPOSED_FOR_OWNER_APPROVAL
governs_execution: true
document_state_mode: temporary_active_governance_until_verified
authority: corrective_control_recovery_gate
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch_context: feature/m28-1-standards-registry-baseline-review
created_date: 2026-05-28
live_repo_write: NO
archive_after: full_fix_implemented_verified_and_owner_approved
---

# CONTROL-RECOVERY-001 — Roadmap / Governance / Operation-Pack Anti-Drift Repair

## 1. Placement Decision

This corrective control plan should live in the repository, not inside the ChatGPT Project operation pack.

Recommended active location:

`docs/governance/control_recovery/CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR.md`

Recommended archive location after its role is complete:

`docs/archives/control_recovery/CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR.md`

## 2. Why It Belongs in the Repository

This plan is project-specific governance evidence. It pauses normal ASBP roadmap execution, controls repo-side governance amendment work, requires verification, and defines when normal execution may resume.

Therefore it belongs in the repository because it affects:

- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`
- M27 retrospective evidence
- M28 restart conditions
- repo-side proof that execution was paused and repaired

The operation pack should not contain the full recovery plan because Project Sources must not become a duplicate source of repo truth.

## 3. What Goes Into the Operation Pack

The operation pack should receive only the permanent assistant enforcement rules derived from this recovery plan.

The operation pack should be amended to include:

- hard stop when checkpoint execution mode is ambiguous;
- no default governance-only interpretation for Phase 9 product-core work;
- no `GO` package generation before execution mode, completion minimum, DDR status, validation rule, and tracker movement rule are confirmed;
- refusal of normal build work while a corrective-control pause is active;
- requirement to read repo-side recovery/control documents when present;
- explicit rule that operation pack text does not replace repo authority.

The operation pack should not store the full recovery plan, M27 findings, M28 state, tracker facts, or repo-specific evidence lists.

## 4. Active Control Status

Normal ASBP build execution is paused.

Allowed activities only:

1. assess the control failure;
2. amend roadmap/control documents;
3. amend the ChatGPT operation pack;
4. verify M27 evidence status;
5. verify M28.1/M28.2 state;
6. prepare and validate the corrective governance package;
7. resume normal execution only after owner approval.

Not allowed while this plan is active:

1. no M28.2 implementation;
2. no tracker advancement to M28.3;
3. no new normal roadmap checkpoint closure;
4. no PR content for normal build work;
5. no issue/PR/branch cleanup unless part of this corrective plan;
6. no generated `apply.py` for normal roadmap execution.

## 4A. Owner Decision Record — Temporary Recovery Write Authority Request

Owner decision date:

    2026-05-28

Decision summary:

    The Project Owner requested that the normal repository write-lock rule be suspended for CONTROL-RECOVERY-001 activities only, so recovery amendments can be written directly during the recovery lane and the owner may decline tool actions through the user interface when needed.

Current authority status:

    REQUESTED / TO BE IMPLEMENTED THROUGH GOVERNANCE AMENDMENT

This decision is recorded as owner intent for the recovery lane. It does not by itself complete the operation-pack amendment, build/governance policy amendment, or final recovery verification required by this plan.

Temporary recovery-write scope requested by the Project Owner:

- recovery-plan amendments;
- roadmap anti-drift amendments;
- build/governance balance policy hard-stop amendments;
- progress tracker pause/recovery-state amendments;
- M27 retrospective evidence and evidence-hygiene corrections;
- M28 restart-control evidence;
- operation-pack replacement artifacts or instructions derived from this recovery plan;
- recovery verification evidence.

Explicit exclusions:

- no normal M28.2 implementation;
- no tracker advancement to M28.3;
- no normal roadmap checkpoint closure;
- no product/runtime/code implementation outside the recovery plan;
- no PR merge;
- no branch deletion;
- no issue closure;
- no release, productization, deployment, or SaaS action;
- no operation outside CONTROL-RECOVERY-001 scope.

Expiry condition:

    This requested temporary authority expires automatically when CONTROL-RECOVERY-001 is fully implemented, verified, and owner-approved for normal roadmap resumption.

Revocation condition:

    The Project Owner may revoke this requested temporary authority at any point.

Permanent-rule requirement:

    The operation pack and repo-side governance must still be amended so future assistant behavior does not depend on memory or informal chat agreement.


## 5. Objective

Fix the control failure that allowed this pattern:

`ambiguous roadmap wording -> documentation-only package -> tracker advancement`

This plan resolves:

| Problem | Fix Target |
|---|---|
| Roadmap wording causes drift | Amend `ROADMAP_CANONICAL.md` with execution modes and completion minimums |
| Build/governance policy is weak in enforcement | Strengthen `BUILD_GOVERNANCE_BALANCE_POLICY.md` with hard-stop rules |
| Operation pack is loose | Amend ChatGPT Project operation pack rules |
| M27 acceptance may be weak | Perform M27 retrospective evidence assessment |
| M27.8-M27.10 metadata is stale | Correct evidence-status hygiene if approved |
| M28 actual UAT decision must be enforced | Make actual UAT mandatory for M28 |
| Future `GO` risk remains high | Add hard anti-drift preflight before package generation |

## 6. Phase 0 — Immediate Pause Gate

### 6.1 Freeze normal execution

All normal roadmap execution remains paused until this plan is implemented, verified, and owner-approved.

### 6.2 Establish recovery checkpoint

Temporary recovery gate name:

`CONTROL-RECOVERY-001 — Roadmap / Governance / Operation-Pack Anti-Drift Repair`

This is not a normal roadmap milestone. It is a pause-and-repair gate.

### 6.3 Tracker rule during pause

Do not advance `PROGRESS_TRACKER.md` to any new product checkpoint.

The tracker should temporarily record that the active work is the corrective control gate and that normal M28 execution is paused.

## 7. Phase 1 — Roadmap Amendment

### 7.1 Add global execution-mode rule to `ROADMAP_CANONICAL.md`

Every checkpoint from M26 onward must be classified as one of:

| Mode | Meaning |
|---|---|
| Governance-only | Decision, scope lock, review, acceptance, closeout, or planning artifact only |
| Build/content | Runtime code, source data, executable model, source library, validator, loader, output, retrieval, AI, UI, or product workflow |
| Hybrid | Governance boundary plus implementation/source/runtime content |
| Validation | Validation evidence checkpoint |
| UAT | Actual user acceptance testing, owner acceptance, or both, explicitly stated |
| Closeout | Milestone boundary freeze |

### 7.2 Add completion-minimum rule

Each active checkpoint must state:

1. execution mode;
2. required completion artifact;
3. implementation/source minimum;
4. validation requirement;
5. tracker movement rule;
6. explicit non-implementation claims.

If any of these are missing, the checkpoint is ambiguous and cannot proceed to `GO`.

### 7.3 Add default classification rule

For Phase 9 local product-core work:

If a checkpoint is not explicitly governance-only, validation-only, UAT-only, or closeout-only, it defaults to hybrid/build-content.

### 7.4 Add ambiguity stop rule

If checkpoint wording includes any of these terms without a completion minimum, `GO` must stop:

- define
- scope
- model
- review
- decide
- assess
- gate
- framework
- authority
- behavior

### 7.5 Amend M28 checkpoint ladder

M28 must be rewritten so each checkpoint has mode and completion minimum.

Recommended M28 interpretation:

| Checkpoint | Correct Mode | Completion Minimum |
|---|---|---|
| M28.1 Standards registry baseline review | Governance-only | Registry baseline review evidence only |
| M28.2 Applicability engine scope | Hybrid | Applicability contract/model sufficient to govern later runtime behavior; no tracker movement from narrative evidence alone |
| M28.3 Citation model implementation scope | Hybrid | Citation model contract/source structure sufficient for later validation |
| M28.4 Standards-bundle binding | Hybrid/build-content | Binding records or source-mapping structure, not vague labels |
| M28.5 Stricter-requirement comparison rule | Hybrid/build-content | Comparison rule model/contract plus tests if executable behavior is added |
| M28.6 Controlled override model | Hybrid | Override record model/contract; tests if executable validation exists |
| M28.7 Local/company/site standards intake | Hybrid | Intake model/record flow; tests if executable behavior exists |
| M28.8 Runtime registry consumption package | Build/content | Runtime reading/validation/parsing/source-status enforcement |
| M28.9 Standards-output limitation rules | Hybrid | Limitation behavior contract; tests if output behavior changes |
| M28.10 Validation checkpoint | Validation | Standards behavior/source validation evidence |
| M28.11 Milestone UAT | Actual UAT | Executed UAT protocol/report; owner acceptance alone is not sufficient |
| M28.12 Milestone closeout | Closeout | Closeout with DDR carry-forward and UAT reference |

### 7.6 Extend classification rule to M29-M34

M29-M34 cannot execute until their checkpoint tables are classified before work begins.

## 8. Phase 2 — Build/Governance Policy Amendment

### 8.1 Strengthen `BUILD_GOVERNANCE_BALANCE_POLICY.md`

Keep the policy, but add enforcement language.

### 8.2 Add hard-stop rule

If roadmap wording is ambiguous or the checkpoint lacks explicit execution mode and completion minimum, the assistant must stop before `PLAN` or `GO`.

It must not classify the checkpoint as governance-only by inference.

### 8.3 Add no-document-only tracker rule

A milestone evidence document may support tracker movement only when the checkpoint is explicitly governance-only, validation-only, UAT-only, or closeout-only.

For hybrid/build/content checkpoints, tracker movement requires implementation/source evidence and validation evidence where applicable.

### 8.4 Add package-generation rule

`GO` must not generate `apply.py`, replacement files, or tracker updates until the anti-drift preflight confirms:

- execution mode;
- completion minimum;
- validation requirement;
- DDR status;
- tracker movement rule.

### 8.5 Add self-audit requirement

Every future `GO` response must internally answer:

`Am I about to close a checkpoint with only a document?`

If yes, stop unless the checkpoint is explicitly governance-only.

## 9. Phase 3 — Operation Pack Amendment

### 9.1 Amend `ASBP_OPERATING_RULES.md`

Add a hard rule:

For Phase 9 and later product-core work, ambiguous checkpoint wording defaults to stop, not governance-only execution.

### 9.2 Amend `STARTER_PROMPT.md`

Add startup confirmation fields:

- current checkpoint execution mode;
- completion minimum;
- tracker movement rule;
- corrective-control pause status.

### 9.3 Amend `ASBP_BRANCH_PR_MERGE_STRATEGY.md`

Add a recovery lane:

| Lane | Scope | Branch Pattern | Review Boundary |
|---|---|---|---|
| Control recovery | Roadmap/policy/operation-pack correction after execution-control failure | `governance/control-recovery` | one control-recovery PR/package |

### 9.4 Add operation-pack refusal rule

The assistant must refuse normal `GO`, `NEXT`, `PLAN`, `UPT`, or `PR` when a corrective-control pause is active, except for corrective-plan work.

### 9.5 Add source-role rule

Do not rely on the assistant remembering this correction.

The correction must exist in repo governance and Project operation pack text.

## 10. Phase 4 — M27 Retrospective Assessment

### 10.1 Scope

Assess M27.8 through M27.13 only.

### 10.2 M27.8 implementation check

Verify:

1. source-library baseline model exists;
2. source-library baseline store exists;
3. baseline JSON exists;
4. tests exist;
5. validation was later recorded.

### 10.3 M27.9 implementation check

Verify:

1. cross-library validation model exists;
2. cross-library validation implementation exists;
3. tests exist;
4. validation coverage matches claims.

### 10.4 M27.10 implementation check

Verify:

1. stage/commit compatibility model exists;
2. compatibility implementation exists;
3. tests exist;
4. no live state mutation is claimed;
5. compatibility boundary is correctly limited.

### 10.5 M27.11 validation check

Verify validation evidence:

`python -m pytest -q — 1159 passed in 52.29s`

### 10.6 M27.12 acceptance quality check

Current concern:

M27.12 was executed as manual evidence review / owner verification, not a realistic operational UAT scenario.

Required owner decision:

| Option | Meaning |
|---|---|
| Keep as owner acceptance only | Accept M27.12 as valid for limited source-library baseline |
| Supplement with retrospective UAT | Add stronger M27 UAT evidence without reopening implementation |
| Reopen M27.12 | Only if owner decides M27 cannot close without actual UAT |

Recommended decision:

Supplement with retrospective M27 source-library UAT, not reopen M27 implementation, unless assessment finds a real implementation gap.

### 10.7 M27.13 closeout check

M27.13 may remain closed if it stays limited to controlled source-library baseline closure and does not claim product readiness.

If M27.12 is supplemented, M27.13 should reference the strengthened supplement.

## 11. Phase 5 — M27 Evidence Hygiene Correction

### 11.1 Fix stale metadata

If assessment confirms M27.8-M27.10 are complete and validated, update frontmatter statuses from:

`PENDING_VALIDATION`

to:

`COMPLETED_VALIDATED`

Files:

1. `docs/milestones/M27/M27_8_LIBRARY_CONTENT_IMPLEMENTATION_WAVE_1.md`
2. `docs/milestones/M27/M27_9_CROSS_LIBRARY_VALIDATION.md`
3. `docs/milestones/M27/M27_10_STAGE_COMMIT_COMPATIBILITY_CHECK.md`

### 11.2 Add validation-reference note

Each corrected M27.8-M27.10 file should reference M27.11 as the validation checkpoint.

### 11.3 Do not alter implementation claims

No new runtime capability should be claimed.

## 12. Phase 6 — M28 Correction State

### 12.1 Confirm M28.1 status

M28.1 can remain complete if the applied evidence file exists and tracker says M28.2 is next.

### 12.2 Nullify M28.2 package

The generated M28.2 package must be treated as invalid and not applied.

If it was applied anywhere, revert it.

If it only exists locally as an untracked file, delete it.

### 12.3 Correct M28.2 execution classification

M28.2 must not proceed until roadmap, policy, and operation-pack amendments are applied.

After correction, M28.2 restarts from the corrected execution mode and completion minimum.

## 13. Phase 7 — Verification Protocol

### 13.1 Governance consistency review

Verify:

1. roadmap contains execution-mode and completion-minimum rules;
2. M28 checkpoint ladder is classified;
3. build/governance policy contains hard-stop rules;
4. operation pack contains hard-stop rules;
5. tracker records pause/recovery truth;
6. no normal roadmap checkpoint advanced during recovery.

### 13.2 Repo evidence review

Verify:

1. M27.8-M27.10 metadata corrected if approved;
2. M27.12 supplement exists if approved;
3. M27.13 remains truthful after any supplement;
4. M28.2 was not falsely completed.

### 13.3 Validation

If only Markdown/governance files change:

`python -m pytest -q` is not required.

Document consistency review is required.

If any code, test, or runtime file changes:

`python -m pytest -q` is required.

### 13.4 Owner approval gate

Before normal build resumes, owner must approve:

1. roadmap amendment;
2. policy amendment;
3. operation pack amendment;
4. M27 retrospective disposition;
5. corrected tracker state;
6. M28.2 restart criteria.

## 14. Phase 8 — Resume Rule

Normal ASBP work resumes only when all are true:

1. corrective-control pause is recorded;
2. roadmap amendment is applied;
3. build/governance policy amendment is applied;
4. operation pack amendment is applied in the ChatGPT Project;
5. M27 retrospective is completed;
6. M27 evidence hygiene is corrected or formally deferred;
7. M28 actual UAT requirement is recorded;
8. tracker points to the correct next checkpoint;
9. owner approves resumption.

After that, the next allowed normal roadmap action is:

`PLAN M28.2`

Not `GO`.

## 15. Granular Execution Order After Authorization

When implementation is authorized, execute in this exact order:

1. Prepare control-recovery branch/package plan.
2. Prepare roadmap amendment.
3. Prepare build/governance policy amendment.
4. Prepare tracker pause/recovery update.
5. Prepare M27 retrospective assessment record.
6. Prepare M27 evidence hygiene corrections if approved.
7. Prepare M28 actual UAT control note if not already recorded clearly enough.
8. Prepare operation-pack replacement package.
9. Run document consistency review.
10. Provide commit message.
11. After application/push, perform `SS`.
12. Confirm pause gate is active and normal build remains blocked.
13. Only after owner approval, resume with `PLAN M28.2`.

## 16. Archival Rule

This document remains active only until the full corrective fix is implemented, verified, and owner-approved.

After that, it must be archived to:

`docs/archives/control_recovery/CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR.md`

The archive copy remains historical evidence.

The permanent enforcement rules remain in:

- `ROADMAP_CANONICAL.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`
- `PROGRESS_TRACKER.md`, as current state requires
- ChatGPT Project operation pack files

## 17. Final Controlling Rule

Until this recovery plan is implemented and verified, normal ASBP build execution remains paused.
