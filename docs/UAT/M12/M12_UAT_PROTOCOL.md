# M12_UAT_PROTOCOL

## Milestone

Milestone 12 — Governed Document Engine

## Protocol Purpose

This protocol defines the milestone-facing acceptance checks for the Milestone 12 governed document-engine boundary.

It is intended to confirm that the current Milestone 12 implementation behaves acceptably for:

- governed template retrieval
- document request/input/output contracts
- DCF intake, extraction, normalization, missing-data behavior, ambiguity rejection, and traceability
- controlled AI authoring modes and bounded invention policy
- standards, language, assumption, placeholder, evidence/inference, prohibited-language, section-level, and detail-consistency guardrails
- GMP/CQV document artifact lifecycle states and transition rules
- document lifecycle to task/workflow readiness evaluation
- milestone validation health

This file is a UAT protocol only.

Execution evidence and the final acceptance decision must be recorded after execution in:

- `docs/UAT/M12/M12_UAT_REPORT.md`

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- recorded supporting result: `596 passed in 46.46s`

## Operator Fields

- UAT date: `27-04-2026`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Repo-Reality Note

Milestone 12 UAT should be executed against the repo-real governed document-engine boundary.

That means:

- use the implemented `asbp.document_engine` package surfaces
- use repo-real tests and committed checkpoint evidence
- do not introduce new feature behavior during UAT
- do not invoke live LLM generation
- do not treat generated language as execution truth
- do not mutate persisted task/workflow state during UAT
- all checks must stay inside the approved Milestone 12 boundary through `M12.8`

## Scope Covered

The following Milestone 12 surfaces are in scope:

- `asbp.document_engine.template_governance`
- `asbp.document_engine.document_contracts`
- `asbp.document_engine.dcf_intake`
- `asbp.document_engine.authoring_controls`
- `asbp.document_engine.standards_guardrails`
- `asbp.document_engine.artifact_lifecycle`
- `asbp.document_engine.workflow_integration`

## Command Execution Sequence

### Step 1 — Verify the technical baseline before UAT execution

```powershell
python -m pytest -q
```

Expected output / pass signal:

```text
596 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

### Step 2 — Confirm governed template/document contract boundary

Acceptance criteria:

- governed template identity is version-aware
- document request/input/output contracts are explicit
- execution truth, template truth, and generated-language output remain separated

### Step 3 — Confirm DCF intake boundary

Acceptance criteria:

- DCF template lookup is governed
- user-filled DCF intake preserves raw content, extracted data, normalized input, and downstream traceability
- missing required values are marked explicitly
- ambiguous data is rejected without guessing

### Step 4 — Confirm controlled AI authoring boundary

Acceptance criteria:

- supported authoring modes are explicit
- bounded invention requires guardrails, standards, document-family rules, and scope
- unrestricted free drafting is rejected as execution truth

### Step 5 — Confirm standards/language/evidence guardrails

Acceptance criteria:

- assumption labeling is explicit
- placeholders are explicit
- evidence and inference are separated
- prohibited language patterns are rejected
- section-level and detail-consistency rules are enforced

### Step 6 — Confirm GMP/CQV document lifecycle model

Acceptance criteria:

- supported states are `draft`, `in_review`, `in_approval`, optional `training_delivery`, `active`, `superseded`, `expired`, and `archived`
- `reopened`, `approved`, and `finalized` are not accepted lifecycle states
- post-active changes require a new version path
- superseded/expired artifacts move to archive under retention metadata

### Step 7 — Confirm document lifecycle to task/workflow readiness integration

Acceptance criteria:

- task/document obligations can be evaluated deterministically
- task closure readiness requires all required document obligations to be satisfied
- `active` document artifacts can satisfy active closure obligations
- `superseded`, `expired`, and `archived` artifacts do not satisfy active closure obligations
- integration output recommends effects but does not directly mutate persisted task/workflow state

### Step 8 — Re-run the full validation baseline after UAT execution

```powershell
python -m pytest -q
```

Expected output / pass signal:

```text
596 passed
```

A higher count is acceptable if the repo advanced cleanly before execution, but a red run is a UAT failure.

## Protocol Checks

| Check ID | Check | Acceptance Criteria |
|---|---|---|
| UAT-M12-01 | Technical validation baseline | Step 1 returns green `pytest` result |
| UAT-M12-02 | Template/document contract boundary | Step 2 acceptance criteria are satisfied |
| UAT-M12-03 | DCF intake boundary | Step 3 acceptance criteria are satisfied |
| UAT-M12-04 | Controlled AI authoring boundary | Step 4 acceptance criteria are satisfied |
| UAT-M12-05 | Standards/language/evidence guardrails | Step 5 acceptance criteria are satisfied |
| UAT-M12-06 | GMP/CQV document lifecycle model | Step 6 acceptance criteria are satisfied |
| UAT-M12-07 | Document lifecycle ↔ task/workflow readiness | Step 7 acceptance criteria are satisfied |
| UAT-M12-08 | Post-UAT validation baseline | Step 8 returns green `pytest` result |

## Failure Handling Rule

If any step produces a result that does not match the expected outcome:

- stop the UAT run at that point
- do not continue guessing
- record the exact step number
- record the actual output or observed mismatch
- classify the issue as one of:
  - execution mistake
  - protocol ambiguity
  - runtime/logic defect
  - environment/state contamination
  - acceptance-boundary gap

## Acceptance Rule

Milestone 12 UAT may be accepted only if:

- all defined checks pass
- no in-scope deterministic document-engine contract is contradicted
- generated language remains downstream output only
- controlled document lifecycle truth remains deterministic
- task/workflow integration remains readiness/effect evaluation only
- full validation remains green

## Out of Scope

The following items are not part of M12 UAT acceptance execution:

- Milestone 12 closeout
- Milestone 13 export/reporting work
- resolver/registry work
- broader library expansion
- live LLM generation
- UI/API work
- cloud/productization work
