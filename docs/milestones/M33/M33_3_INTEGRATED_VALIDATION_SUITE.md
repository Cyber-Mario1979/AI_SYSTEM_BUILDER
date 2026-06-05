# M33.3 — Integrated Validation Suite

Status: Completed on feature branch  
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

## Validation result

Validation command:

```text
python -m pytest -q
```

Local validation result recorded from owner terminal:

```text
1623 passed in 57.98s
```

Result:

```text
PASS — integrated validation suite complete for M33.3.
```

## Validation interpretation

The full test suite passed after adding M33.3 executable validation code and tests.

This validates the integrated M33 pre-trial path at the test-suite level. It does not replace M33.4 trial execution, and it does not create real UAT/trial evidence.

## Tracker movement status

Tracker movement is now allowed because integrated validation exists and the full suite passed.

The tracker may record:

```text
Latest completed roadmap checkpoint: M33.3 — Integrated validation suite
Exact next unfinished work: PLAN M33.4 — Trial execution round 1
Latest validation / review evidence: docs/milestones/M33/M33_3_INTEGRATED_VALIDATION_SUITE.md — PASS integrated validation; python -m pytest -q — 1623 passed in 57.98s
```

M33.4 remains blocked until separately authorized.

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

## Next roadmap checkpoint

After M33.3 is reviewed and merged, the next normal roadmap checkpoint is:

```text
PLAN M33.4 — Trial execution round 1
```

Do not start M33.4 without separate owner authorization.
