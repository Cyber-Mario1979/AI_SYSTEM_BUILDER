# M33.1 — Trial Scope and Protocol

Status: Completed on feature branch  
Checkpoint: M33.1  
Mode: Governance-only  
Branch: `m33-1-trial-scope-and-protocol`  
Protocol date: 2026-06-05

## Purpose

Define the local trial boundaries for M33 — Full Local Product Trial, Defect Loop, and UAT.

M33.1 is protocol and scope only. It does not run the trial, create later checkpoint deliverables, change code, update runtime behavior, or make readiness claims beyond bounded local trial planning.

## Source basis

```text
ROADMAP_CANONICAL.md
PROGRESS_TRACKER.md
docs/milestones/M32/M32_11_MILESTONE_CLOSEOUT.md
```

Roadmap v7 requires a trial protocol with scenario(s), system type, user role, acceptance criteria, data sensitivity, limitations, and trial boundaries. The required review is document consistency review.

## Trial-entry baseline

M33.1 preserves the frozen M32 MVP baseline:

```text
CLI-enhanced local workflow only.
Scenario path: scenario -> configure -> plan -> status -> outputs.
Scenario: cleanroom-hvac-qualification-basic.
Scenario identifiers: WP-032, TC-032, PLAN-032.
Output review remains metadata/visibility only.
Human review remains required.
Optional local/offline LLM draft support is accepted only as optional supporting trial evidence with limitations.
```

## Trial objective

The first M33 trial will test whether the bounded local integrated CQV workflow can be used realistically enough to reveal defects, usability friction, evidence gaps, source or standards limitations, output limitations, validation issues, and AI-boundary risks before later readiness work proceeds.

## In-scope scenario

| Field | Trial scope |
|---|---|
| Scenario name | `cleanroom-hvac-qualification-basic` |
| Work package identifier | `WP-032` |
| Test case identifier | `TC-032` |
| Plan identifier | `PLAN-032` |
| Local workflow path | `scenario -> configure -> plan -> status -> outputs` |
| Product surface | CLI-enhanced local workflow only |
| Output review scope | Metadata/visibility review only |
| Human review | Required |
| AI inclusion | Optional local/offline draft-support evidence only if explicitly invoked within bounded scope; not required for trial success |

No additional scenario or dataset is added by M33.1.

## System type

```text
Local integrated CQV product-core workflow for a bounded cleanroom HVAC qualification use case.
```

Excluded surfaces and claims: web UI, desktop UI, hosted runtime, customer/admin surfaces, release/deployment readiness, and full AI/product readiness.

## User role

```text
Local CQV reviewer / project owner operating the bounded local workflow.
```

The user reviews workflow state, limitations, output metadata, and trial observations. Human review remains required.

## Trial boundaries

### In scope

- Run the accepted local workflow path for the M32 baseline scenario in a later authorized trial checkpoint.
- Observe controlled inputs, status, planning state, source/standards references, output metadata, and limitation visibility.
- Capture observations for later M33 triage.
- Record failures, confusing behavior, missing visibility, unsafe readiness states, manual friction, and evidence gaps.
- Confirm that optional local/offline LLM support, if used, remains supporting-only.

### Out of scope

- M33.2 scenario pack creation.
- M33.3 integrated validation suite creation.
- M33.4 trial execution before separate authorization.
- M33.5 issue triage and correction planning.
- M33.6 corrective implementation.
- New code, validators, loaders, adapters, workflow behavior, or CLI behavior.
- Additional product surfaces, hosted/deployed operation, provider integration, release readiness, or commercialization planning.
- Real customer data, production records, confidential datasets, personal data, or uncontrolled prompt/model outputs.

## Data sensitivity controls

The first M33 trial must use only synthetic, local, non-confidential, non-customer, non-production data compatible with the accepted M32 scenario.

If richer scenario data is needed, it belongs to M33.2 and must be scoped separately.

## Acceptance criteria

M33.1 is complete when this protocol exists and passes document consistency review.

Later M33 trial execution may be considered protocol-compliant only if all criteria below are met.

| Criterion | Required result |
|---|---|
| Scope control | Trial remains inside the approved cleanroom HVAC local workflow scenario unless separately authorized. |
| Local operation | Workflow is exercised locally through the accepted CLI-enhanced local workflow surface. |
| Baseline preservation | M32 frozen baseline remains the trial-entry baseline. |
| Visibility | Workflow status, limitations, source/standards visibility, output metadata, validation limits, and AI limits remain visible. |
| Human review | Human review remains required for any generated or assembled output. |
| AI boundary | AI does not approve, certify, release, mutate state, or create final accepted output. |
| Data control | Only approved synthetic/non-confidential local data is used. |
| Defect capture | Observed defects, friction, unclear states, and limitations are captured for later M33 triage. |
| No false readiness | Trial does not claim readiness beyond the bounded local-trial scope. |

## Observation capture model

M33.1 defines categories only. It does not triage, prioritize, correct, or implement fixes.

| Category | Description |
|---|---|
| Bug | Incorrect behavior, failure, crash, or broken command/workflow. |
| Workflow friction | Awkward, confusing, slow, or difficult local-use step. |
| Missing visibility | Status, limitation, source, output, validation, or AI boundary is not visible enough. |
| Source/standards limitation | Source, standards, citation, retrieval, or authority boundary is unclear or insufficient. |
| Output limitation | Output artifact, review metadata, export visibility, or human-review boundary is insufficient. |
| Validation gap | Test, evidence, or scenario validation is insufficient for trial confidence. |
| AI limitation | AI/local-model/draft-support behavior is unclear, overclaimed, or out of scope. |
| Documentation gap | Instructions, protocol, acceptance criteria, or evidence record is incomplete or ambiguous. |
| Out of scope | Observation belongs to later roadmap work or separately authorized readiness work. |

## Explicit non-claims

This protocol does not claim or authorize trial execution, M33.2 or later checkpoint work, scenario pack creation, validation suite creation, issue triage, corrective implementation, release/deployment readiness, hosted readiness, customer-ready output, final AI authority, full product/runtime AI readiness, or commercialization planning.

## Document consistency review

Reviewed consistency conditions:

```text
Roadmap checkpoint: M33.1 — Trial scope and protocol.
Execution mode: Governance-only.
Required deliverable: Trial protocol with scenario(s), system type, user role, acceptance criteria, data sensitivity, limitations, and trial boundaries.
Validation/review requirement: Document consistency review.
M32 baseline: preserved as trial-entry baseline.
Trial execution: not started.
M33.2+ work: not started.
Blocked readiness claims: preserved.
Tracker movement rule: protocol exists before tracker movement.
```

Result:

```text
PASS — document consistency review complete for M33.1 trial scope and protocol.
```

## Tracker update needed

After this protocol is committed, the progress tracker may be updated to record:

```text
Latest completed roadmap checkpoint: M33.1 — Trial scope and protocol
Exact next unfinished work: PLAN M33.2 — Test dataset / scenario pack
Latest validation / review evidence: docs/milestones/M33/M33_1_TRIAL_SCOPE_AND_PROTOCOL.md — PASS document consistency review
```

M33.2 remains blocked until separately authorized.

## Next roadmap checkpoint

After M33.1 is reviewed and merged, the next normal roadmap checkpoint is:

```text
PLAN M33.2 — Test dataset / scenario pack
```

Do not start M33.2 without separate owner authorization.
