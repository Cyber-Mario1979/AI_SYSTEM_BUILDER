---
doc_type: milestone_checkpoint_output
canonical_name: M15_TASK_POOL_EXPANSION
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.4
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.4 — Task-Pool Expansion

## Checkpoint

`M15.4` — Task-pool expansion

## Purpose

This document records the M15.4 governed task-pool expansion package.

The package expands the task-pool coverage model identified in M15.3 while preserving M15.4 boundaries:

- task-pool source-definition identity
- task definition row shape
- duration references by profile key only
- deterministic dependency wiring
- downstream workflow compatibility

This checkpoint does not migrate the draft task pools into runtime authority and does not update the deployment-compiled task-pool surface.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This file is checkpoint evidence only.

## Input from M15.3

M15.3 recorded the expanded selector/scope target and identified missing selector records and their target task-pool references.

M15.4 uses that accepted selector/scope matrix as input.

## Deliverables

This package adds:

- `docs/milestones/M15/M15_TASK_POOL_EXPANSION.md`
- `docs/design_spec/valor_pack_snapshot/expansion/M15_4_TASK_POOL_EXPANSION_MAP.yaml`
- `docs/design_spec/valor_pack_snapshot/expansion/task_pools/M15_4_TASK_POOLS_DRAFT_v1.yaml`

## Runtime authority rule

The draft task pools in this package are not runtime authority and must not be treated as deployment-compiled lookup records.

## Draft task-pool records

| Task pool | Domain | Scope | Task count | Bound profile |
|---|---:|---:|---:|---|
| `TP-PE-QUAL@v1` | PE | QUAL | 9 | `PROF-PE-QUAL@v1` |
| `TP-PE-COMM@v1` | PE | COMM | 8 | `PROF-PE-COMM@v1` |
| `TP-PE-DECOM@v1` | PE | DECOM | 9 | `PROF-PE-DECOM@v1` |
| `TP-UT-PV@v1` | UT | PV | 8 | `PROF-UT-PV@v1` |
| `TP-UT-DECOM@v1` | UT | DECOM | 9 | `PROF-UT-DECOM@v1` |
| `TP-CR-POST-DEV@v1` | CR | POST-DEV | 9 | `PROF-CR-POST-DEV@v1` |
| `TP-CR-POST-CHANGE@v1` | CR | POST-CHANGE | 8 | `PROF-CR-POST-CHANGE@v1` |
| `TP-CR-DECOM@v1` | CR | DECOM | 9 | `PROF-CR-DECOM@v1` |
| `TP-CSV-PV@v1` | CSV | PV | 8 | `PROF-CSV-PV@v1` |
| `TP-CSV-POST-DEV@v1` | CSV | POST-DEV | 9 | `PROF-CSV-POST-DEV@v1` |
| `TP-CSV-POST-CHANGE@v1` | CSV | POST-CHANGE | 8 | `PROF-CSV-POST-CHANGE@v1` |
| `TP-CSV-DECOM@v1` | CSV | DECOM | 9 | `PROF-CSV-DECOM@v1` |

## CSV naming rule

`CS` remains the context-selector prefix only.
`CSV` is the future canonical computerized-systems domain acronym.

| Legacy snapshot ref | Future canonical ref |
|---|---|
| `TP-CS-E2E@v1` | `TP-CSV-E2E@v1` |

The E2E computerized-system task-pool rename/mapping is recorded, but runtime migration is not performed in M15.4.

## Task-row shape

Every draft task row follows the current task-pool row shape:

- `atomic_task_id`
- `name`
- `phase`
- `task_type`
- `owner_role_default`
- `applicability_tags`
- `required_inputs`
- `outputs`
- `duration_ref.profile_key`
- `dependency_wiring.predecessors`
- `flags`
- `notes` where needed

## Duration policy

No numeric durations are defined in M15.4. All tasks reference `duration_ref.profile_key`.

Profile duration values and planning-basis linkage are downstream work for M15.5.

## Dependency policy

Dependencies are deterministic and use `atomic_task_id` references only.

## Document obligation policy

M15.4 does not create formal document-obligation mapping metadata.

Document obligations are only signaled through task names, outputs, phases, and task types.

Formal task-to-document obligation mapping belongs to M15.5 mapping metadata.

## Not in M15.4 scope

M15.4 does not implement:

- profile duration values
- calendar expansion
- standards-bundle expansion
- mapping metadata expansion
- deployment compiled lookup
- task-pool validation/freeze engine
- CLI changes
- orchestration/service hardening
- runtime migration
- AI runtime behavior

## Checkpoint decision

M15.4 records draft task-pool source definitions for the missing coverage families identified by M15.3.

The project should not treat these records as runtime-authoritative until M15.6 validation/freeze/release discipline and M15.7 service hardening are complete.

## Validation note

This checkpoint package is documentation/specification-only.

No Python code or runtime behavior was changed.

`python -m pytest -q` was not run for this generated package. The latest verified validation status remains the tracker-recorded result until validation is run again.
