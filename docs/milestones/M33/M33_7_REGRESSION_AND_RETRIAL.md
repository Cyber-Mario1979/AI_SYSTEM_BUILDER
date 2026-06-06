# M33.7 - Regression and Re-trial

Status: PASS
Checkpoint: M33.7
Mode: Validation / UAT
Branch: m33-7-regression-and-retrial
Date: 2026-06-06

## Purpose

Re-run affected paths after the M33.6 compact trial-summary correction.

## Source Basis

- ROADMAP_CANONICAL.md
- PROGRESS_TRACKER.md
- docs/milestones/M33/M33_6_CORRECTIVE_IMPLEMENTATION_PACKAGE.md
- asbp/local_workflow_trial_summary_logic.py
- asbp/adapters/local_workflow_cli.py
- tests/test_m33_6_trial_summary_command.py

## Affected Correction

M33.5-001 - Verbose JSON capture

M33.6 correction - compact trial-summary command

## Regression / Re-trial Scope

Primary affected path:

scenario -> configure -> trial-summary

Regression path:

scenario -> configure -> plan -> status -> outputs

## Commands Executed

| Evidence ID | Command | Exit Code |
| --- | --- | --- |
| 01_scenario | python -m asbp.adapters.local_workflow_cli scenario --scenario-id cleanroom-hvac-qualification-basic | 0 |
| 02_configure | python -m asbp.adapters.local_workflow_cli configure --wp-id WP-032 --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac | 0 |
| 03_trial_summary | python -m asbp.adapters.local_workflow_cli trial-summary --wp-id WP-032 | 0 |
| 04_plan | python -m asbp.adapters.local_workflow_cli plan --wp-id WP-032 | 0 |
| 05_status | python -m asbp.adapters.local_workflow_cli status --wp-id WP-032 | 0 |
| 06_outputs | python -m asbp.adapters.local_workflow_cli outputs --wp-id WP-032 | 0 |
| 07_pytest | python -m pytest -q | 0 |

## Evidence Locations

docs/milestones/M33/trial_records/M33_7_REGRESSION_AND_RETRIAL/

Captured files include command text, stdout, stderr, and exit code for each command.

## Trial-summary Read-only Check

| Check | Result |
| --- | --- |
| State hash before trial-summary | d711e0e6cecc0813159479a362327ccd4ea885e2afc70c127f6159dcd6ae3f46 |
| State hash after trial-summary | d711e0e6cecc0813159479a362327ccd4ea885e2afc70c127f6159dcd6ae3f46 |
| Trial-summary read-only confirmed | True |

## Boundary Confirmation

| Boundary | Expected | Actual |
| --- | --- | --- |
| human_review_required | True | True |
| accepted | False | False |
| approval_claimed | False | False |
| release_claimed | False | False |
| download_allowed | False | False |
| ai_call_performed | False | False |
| provider_call_performed | False | False |
| ollama_call_performed | False | False |

Boundary result: True

## Pytest Validation

Validation command:

python -m pytest -q

Recorded final output line:

1627 passed in 62.26s (0:01:02)

## Deviations / Blockers

None.

## Result

PASS - M33.7 regression and re-trial evidence completed.

## Tracker Movement Recommendation

Allowed: update tracker to record M33.7 complete and set exact next unfinished work to PLAN M33.8 - Local product UAT report.

## Explicit Non-claims

M33.7 does not claim productization, deployment readiness, release readiness, SaaS readiness, customer-ready output, commercialization readiness, or full product/runtime AI readiness.

## Next Roadmap Checkpoint

PLAN M33.8 - Local product UAT report

