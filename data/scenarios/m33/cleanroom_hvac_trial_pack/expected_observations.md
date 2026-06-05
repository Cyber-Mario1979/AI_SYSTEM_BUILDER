# Expected Observations — M33 Cleanroom HVAC Trial Scenario Pack

Checkpoint: M33.2 — Test dataset / scenario pack  
Scenario pack: `cleanroom_hvac_trial_pack`  
Scenario: `cleanroom-hvac-qualification-basic`

## Purpose

This file defines expected observation categories for later authorized M33 trial execution. It does not execute the trial, classify findings, triage issues, or apply corrections.

## Expected observation categories

| Category | Expected focus |
|---|---|
| Bug | Broken local command, incorrect payload, failed state persistence, or unexpected error. |
| Workflow friction | Confusing command sequence, unclear operator prompt, or awkward manual step. |
| Missing visibility | Hidden source, standards, output, validation, or AI limitation. |
| Source/standards limitation | Unclear bundle visibility or unsupported authority assumption. |
| Output limitation | Artifact metadata, review status, or safe access limitation unclear. |
| Validation gap | Evidence insufficient for later trial confidence. |
| AI limitation | Optional local/offline support unclear, overclaimed, or treated as authority. |
| Documentation gap | Scenario instructions or acceptance criteria unclear. |
| Out of scope | Request belongs to M33.3 or later, productization, deployment, release, SaaS, or commercialization. |

## Expected local workflow visibility

Later trial execution should observe whether the following remain visible:

- selected work package `WP-032`;
- task collection `TC-032`;
- plan `PLAN-032`;
- cleanroom HVAC system type;
- qualification-only scope intent;
- standards bundles `cqv-core` and `cleanroom-hvac`;
- output metadata and human-review-required state;
- no approval, release, certification, or product-readiness claim;
- AI/provider/local-model limitations.

## Stop conditions for later trial work

Later M33 trial execution should stop or be marked blocked if it requires real confidential data, customer data, production records, uncontrolled model output, provider calls, new product surfaces, or readiness claims outside the approved local-trial boundary.

## M33.2 boundary

This observation model prepares the scenario pack only. It does not create M33.4 trial evidence and does not start M33.5 triage.
