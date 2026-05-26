---
doc_type: milestone_implementation_candidate
canonical_name: M27_3_TASK_POOL_SOURCE_MODEL
status: IMPLEMENTATION_CANDIDATE_PENDING_VALIDATION
milestone: M27
checkpoint: M27.3
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
checkpoint_title: Task-pool source model
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: feature/m27-cqv-source-content-expansion
created_date: 2026-05-27
last_updated_date: 2026-05-27
application_mode: user_applied_package
live_repo_write: NO
---

# M27.3 — Task-Pool Source Model

## Purpose

This checkpoint introduces the runtime-loadable task-pool source model for the local integrated CQV product core.

It converts the M27.1 preset-family scope and M27.2 selector/scope-intent model into a bounded runtime source surface for starter task-pool records.

M27.3 is not a documentation-only checkpoint.

## Implemented Candidate Scope

This package adds:

- `asbp/task_pool_source_model.py`
- `asbp/task_pool_source_store.py`
- `data/source/task_pools/starter_task_pools.json`
- `tests/test_task_pool_source_model.py`
- `docs/milestones/M27/M27_3_TASK_POOL_SOURCE_MODEL.md`

## Runtime Source Boundary

The task-pool source library is separate from persisted project tasks.

Task-pool source records define candidate work content and source identity.

Persisted tasks remain execution/runtime instances created by downstream staging or commit behavior.

M27.3 does not stage, commit, schedule, or mutate persisted tasks.

## Starter Task-Pool Families

The starter runtime source library includes:

| Task Pool ID | Preset Family | Scope |
|---|---|---|
| `TP-PE-E2E-QUAL@v1` | `PF-PROCESS-EQUIPMENT` | Process equipment end-to-end qualification |
| `TP-QCLAB-QUAL-CAL-LINK@v1` | `PF-QC-LAB-EQUIPMENT` | QC lab equipment qualification and calibration linkage |
| `TP-CLEANROOM-HVAC-QUAL@v1` | `PF-CLEANROOM` | Cleanroom and HVAC qualification |
| `TP-UTILITIES-QUAL@v1` | `PF-UTILITIES` | Utility system qualification |
| `TP-CSV-BASELINE@v1` | `PF-COMPUTERIZED-SYSTEMS` | Computerized system validation baseline |
| `TP-MANUAL-FALLBACK-ASSESS@v1` | `PF-MANUAL-FALLBACK` | Controlled manual fallback assessment |

## Source Record Shape

Each task-pool source record carries:

- task-pool identity;
- version;
- runtime-source status;
- display name;
- preset-family binding;
- selector context tags;
- lifecycle events;
- qualification/validation intents;
- atomic task records.

Each atomic task source record carries:

- atomic task ID;
- title;
- purpose;
- task type;
- owner role;
- prerequisites;
- deterministic dependencies;
- duration reference placeholder;
- document expectation placeholder;
- notes where needed.

## Validation Rules

The runtime model validates:

- duplicate task-pool IDs are rejected;
- duplicate atomic task IDs inside a task pool are rejected;
- dependencies must reference atomic task IDs inside the same task pool;
- self-dependencies are rejected;
- invalid preset families are rejected;
- owner role is required;
- duration reference is required;
- persisted state payloads are not accepted as task-pool source-library payloads.

## Duration Boundary

M27.3 requires duration references but does not define real duration values.

Duration-reference resolution remains downstream to M27.6.

## Document Expectation Boundary

M27.3 records document expectation placeholders only.

It does not implement document templates, document generation, rendering, export, report generation, or document lifecycle behavior.

## DDR Impact

M27.3 touches DDR-001 and DDR-002 at runtime task-pool source-model level.

M27.3 has DDR-009 awareness because later UI/API or external contract behavior may consume task-pool source outputs through approved adapters.

M27.3 does not close, reopen, downgrade, or reclassify any DDR by itself.

M27.3 does not implement deployment-compiled lookup, UI/API behavior, document generation, standards retrieval, AI/runtime behavior, or productization behavior.

## Not Completed / Not Claimed

M27.3 does not claim completion of:

- task staging;
- task commit behavior;
- scheduling;
- profile records;
- calendar records;
- planning-basis records;
- real duration values;
- mapping records;
- cross-library validation beyond task-pool self-validation;
- source-to-execution compatibility validation;
- product-ready document templates;
- document generation;
- rendering, export, or reporting behavior;
- standards embedding or retrieval;
- AI/model/provider behavior;
- UI/API behavior;
- productization, SaaS, deployment, or commercial readiness.

## Validation Expectation

This checkpoint changes runtime code and tests.

`python -m pytest -q` must pass before M27.3 is treated as complete or before the tracker is advanced to M27.4.

## Handoff After Validation

After validation passes, the tracker may be updated to record M27.3 completion and point to:

`M27.4 — Profile model`
