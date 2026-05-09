# M17.2 — Quality Gates and Groundedness Checks

## Checkpoint

`M17.2` — Quality gates and groundedness checks

## Status

Implementation package prepared.

## Scope

This checkpoint defines deterministic metadata-level quality gates for governed AI outputs.

The M17.2 gate consumes the closed M16 output-acceptance boundary and checks whether a candidate output can pass a quality gate without becoming ungrounded, unsupported, or source-role unsafe.

## In-scope behavior

M17.2 defines:

- quality gate result contract
- groundedness check result contract
- evidence-link checks
- source-role checks
- deterministic pass/fail quality gate behavior
- fail-closed treatment of attractive but ungrounded output
- explicit prohibition on state mutation, approval, release, and template implementation inside this checkpoint

## Required pass rule

A quality gate may pass only when all of the following pass:

- groundedness check
- evidence-link check
- source-role check

If any sub-check fails, the quality gate fails.

## Groundedness checks

Groundedness fails when any candidate output or acceptance decision declares or implies:

- unsupported evidence claims
- unlabeled assumptions where labeling is required
- missing truth without placeholder handling
- unbounded invention
- unverified evidence claims
- unverified standards claims
- execution-truth claims
- state mutation requests
- approval or release requests
- an M16 acceptance decision other than `accept_candidate_output`

## Evidence-link checks

Evidence-link checks verify that evidence references used by the gate:

- are version-pinned
- exist in the source AI context package
- are generation-eligible
- do not have unavailable evidence status

## Source-role checks

Source-role checks verify that references used as truth:

- exist in the source AI context package
- are authoritative
- use an authoritative source role
- do not define execution truth

Non-authoritative support context may exist, but it must not be promoted into source truth or execution truth.

## Relationship to M17.1

M17.1 created the AI evaluation baseline and regression harness.

M17.2 does not mutate the M17.1 baseline payloads. It introduces a separate quality-gate contract because M17.1 correctly excluded quality-gate and groundedness fields from baseline regression records.

## Relationship to M17.3

M17.2 does not implement standards-conformance or detail-level consistency scoring.

Those checks remain deferred to:

`M17.3` — Standards-conformance and detail-level consistency checks

## Relationship to M17.4

M17.2 does not implement full retrieval-use governance.

Retrieval-use rules and source-role discipline remain deferred to:

`M17.4` — Retrieval-use rules and source-role discipline

M17.2 only checks source-role misuse for the references explicitly used by a quality-gate payload.

## Document template boundary decision

M17.2 must not re-open document template implementation.

The re-entry scope for future document template work is not the closed M12 document-engine boundary. The re-entry scope is actual document template/product implementation from expanded governed library content.

Decision:

```text
Document template/product implementation is deferred to a post-M17, pre-M18 decision gate.
```

At that gate, the project must decide whether the missing work is:

- a small bounded gap requiring a roadmap addendum, or
- a larger product-scope gap requiring a new roadmap milestone before M18

## Not in scope

M17.2 does not implement:

- actual LLM calls
- prompt templates
- generated document text
- generated report text
- document template/product implementation
- actual document generation from expanded library content
- standards-conformance checks
- detail-level consistency checks
- retrieval-use governance
- recommendation behavior
- UI/API behavior
- workflow mutation
- approval or release behavior
