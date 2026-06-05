# M33.4 — Trial Execution Round 1

Status: Evidence pending on feature branch  
Checkpoint: M33.4  
Mode: UAT / Hybrid  
Branch: `m33-4-trial-execution-round-1`  
Trial planning date: 2026-06-05

## Purpose

Run the first real local workflow trial for M33 and record actual observations.

M33.4 requires real trial evidence from the local workflow path. It must capture issues, errors, friction, wrong outputs, AI behavior where in scope, and user observations.

## Source basis

```text
ROADMAP_CANONICAL.md
PROGRESS_TRACKER.md
docs/milestones/M33/M33_1_TRIAL_SCOPE_AND_PROTOCOL.md
docs/milestones/M33/M33_2_TEST_DATASET_SCENARIO_PACK.md
docs/milestones/M33/M33_3_INTEGRATED_VALIDATION_SUITE.md
data/scenarios/m33/cleanroom_hvac_trial_pack/
```

Roadmap v7 requires real trial evidence and does not allow synthetic tests to substitute for trial execution.

## Trial lanes authorized for round 1

```text
Lane A — Manual local workflow trial
Lane B — Bounded optional Ollama/local-model observation
```

Lane A is required. Lane B is included as supporting local/offline observation only.

## Lane A commands

Run from repository root:

```text
python -m asbp.adapters.local_workflow_cli scenario --scenario-id cleanroom-hvac-qualification-basic
python -m asbp.adapters.local_workflow_cli configure --wp-id WP-032 --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac
python -m asbp.adapters.local_workflow_cli plan --wp-id WP-032
python -m asbp.adapters.local_workflow_cli status --wp-id WP-032
python -m asbp.adapters.local_workflow_cli outputs --wp-id WP-032
```

Record the actual terminal evidence in:

```text
docs/milestones/M33/trial_records/M33_4_TRIAL_RECORD_ROUND_1.md
```

## Lane B bounded Ollama observation

Lane B may be run only as a separated optional observation. It does not make acceptance decisions, change project state, or create product evidence.

Record bounded observation evidence in:

```text
docs/milestones/M33/trial_records/M33_4_OPTIONAL_OLLAMA_OBSERVATION.md
```

Use a local prompt like:

```text
You are reviewing a synthetic local cleanroom HVAC CQV trial context.
List possible reviewer questions and possible workflow-friction observations only.
Do not make acceptance or readiness claims.
Do not change project state or files.
Human review remains required.
```

Recommended local command shape:

```text
ollama run <LOCAL_MODEL_NAME>
```

Use summarized observation evidence unless the project later authorizes raw model-output storage.

## Evidence status

```text
PENDING — Lane A and Lane B evidence have not yet been recorded.
```

## Tracker movement status

Do not update `PROGRESS_TRACKER.md` to M33.4 complete until real trial evidence exists.

Tracker movement may occur only after:

```text
Lane A trial evidence exists.
Lane B evidence exists if Ollama was actually run.
Observed issues, errors, friction, wrong outputs, AI behavior where in scope, and user observations are captured.
M33.5 triage has not started.
```

## Explicit non-claims

M33.4 does not claim or authorize M33.5 issue triage, M33.6 corrective implementation, product readiness, customer readiness, release readiness, deployment readiness, SaaS readiness, commercialization planning, or full product/runtime AI readiness.

## Next action

Run Lane A locally, then run Lane B if available and bounded. Paste the evidence back into the session so the trial record files can be completed.
