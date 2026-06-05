# M33.3 — Integrated Validation Suite

Status: Validation pending on feature branch  
Checkpoint: M33.3  
Mode: Build/content  
Branch: `m33-3-integrated-validation-suite`  
Validation evidence date: 2026-06-05

## Purpose

Create an integrated validation suite for the M33 local product trial path.

M33.3 validates the scenario-pack contract, source and standards boundaries, output and human-review boundaries, AI/local-model boundaries, and the executable local workflow path before M33.4 trial execution is authorized.

## Source basis

```text
ROADMAP_CANONICAL.md
PROGRESS_TRACKER.md
docs/milestones/M33/M33_1_TRIAL_SCOPE_AND_PROTOCOL.md
docs/milestones/M33/M33_2_TEST_DATASET_SCENARIO_PACK.md
data/scenarios/m33/cleanroom_hvac_trial_pack/
asbp/local_workflow_scenario_logic.py
asbp/m33_scenario_pack_validation.py
tests/test_m32_8_end_to_end_local_scenario.py
tests/test_m33_3_integrated_validation_suite.py
```

Roadmap v7 requires:

```text
Integrated validation covering source selection, staging, planning, standards, document factory, UI, retrieval, and AI/local model where included.
```

Validation requirement:

```text
python -m pytest -q if code changed; integrated validation evidence.
```

## Deliverables

```text
asbp/m33_scenario_pack_validation.py
tests/test_m33_3_integrated_validation_suite.py
docs/milestones/M33/M33_3_INTEGRATED_VALIDATION_SUITE.md
```

## Integrated validation scope

The validation suite covers:

- required M33.2 scenario-pack files;
- valid JSON scenario-pack payloads;
- scenario identity alignment with `cleanroom-hvac-qualification-basic`;
- work package `WP-032`;
- task collection `TC-032`;
- plan `PLAN-032`;
- workflow path `scenario -> configure -> plan -> status -> outputs`;
- synthetic/non-confidential data controls;
- standards visibility without authority upgrade;
- retrieval boundary;
- AI/provider/local-model boundary;
- expected observation category coverage;
- executable local CLI path through scenario, configure, plan, status, and outputs;
- output and human-review boundary.

## Test coverage added

```text
test_m33_3_scenario_pack_required_files_exist
test_m33_3_scenario_pack_json_files_are_valid_objects
test_m33_3_scenario_identity_matches_trial_scope
test_m33_3_user_inputs_preserve_data_sensitivity_controls
test_m33_3_source_inventory_preserves_authority_and_ai_boundaries
test_m33_3_expected_observations_cover_trial_categories
test_m33_3_integrated_scenario_pack_validation_passes
test_m33_3_cli_path_exercises_cleanroom_hvac_scenario
```

## Validation status

Validation command required before checkpoint closure:

```text
python -m pytest -q
```

Current validation state:

```text
PENDING — executable validation must be run locally before tracker movement and checkpoint closure.
```

Reason:

```text
M33.3 adds executable code and tests. The full test suite must pass before M33.3 can be recorded as complete.
```

## Tracker movement status

Tracker movement is blocked until integrated validation passes.

Do not update `PROGRESS_TRACKER.md` to M33.3 complete until the following is available:

```text
python -m pytest -q — PASS
```

After validation passes, update this document and the tracker to record:

```text
Latest completed roadmap checkpoint: M33.3 — Integrated validation suite
Exact next unfinished work: PLAN M33.4 — Trial execution round 1
Latest validation / review evidence: docs/milestones/M33/M33_3_INTEGRATED_VALIDATION_SUITE.md — PASS integrated validation
```

## Explicit non-claims

This checkpoint does not claim or authorize:

- M33.4 trial execution;
- M33.5 issue triage;
- M33.6 corrective implementation;
- product readiness;
- customer readiness;
- customer-ready output;
- customer-facing AI behavior;
- AI approval, release, or certification authority;
- provider/cloud API readiness;
- web UI readiness;
- desktop UI readiness;
- customer surface readiness;
- full product/runtime AI readiness;
- deployment readiness;
- release readiness;
- SaaS readiness;
- commercialization planning.

## Next action

Run from repo root after pulling this branch locally:

```text
python -m pytest -q
```

Then update this evidence document and tracker only if the full suite passes.
