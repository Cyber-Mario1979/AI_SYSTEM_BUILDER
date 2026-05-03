# M14_UAT_REPORT

## Milestone

Milestone 14 — Resolver / Registry and Governed Data Layer

## Checkpoint

M14.7 — Milestone UAT checkpoint

## UAT Status

Complete

## UAT Protocol Reference

`docs/UAT/M14_UAT_PROTOCOL.md`

## UAT Scope

This UAT covers the Milestone 14 implementation boundary through:

- M14.1 — Resolver / registry boundary foundation
- M14.2 — Governed asset identity and version-pinned lookup
- M14.3 — Calendar and planning-basis resolution family
- M14.4 — Authored-source versus deployment-compiled separation
- M14.5 — Governed retrieval versus support-retrieval boundary
- M14.6 — Validation checkpoint

## Supporting Validation Evidence

Validation checkpoint evidence:

`docs/M14_VALIDATION_CHECKPOINT.md`

Latest validation result:

`python -m pytest -q` — `724 passed in 51.47s`

Latest M14.5 implementation commit:

`c66c66f` — `engine: add retrieval boundary rules`

## UAT Execution Summary

### UAT-14-01 — Resolver / registry boundary clarity

Result: Pass

The resolver / registry is represented as an explicit governed access boundary.

The implementation defines approved resolver/registry boundaries, supported asset-access entry points, source-truth separation, layer-position policy, CLI-as-adapter behavior, and fail-closed rejection of bypass or unauthorized authority fields.

### UAT-14-02 — Governed asset identity and version-pinned lookup

Result: Pass

Governed asset lookup requires canonical asset identity and explicit version pinning.

The implementation defines asset family, asset ID, asset version, asset reference, and lookup key rules. It rejects unversioned, implicit, `latest`, `current`, wildcard, duplicate, missing, or ambiguous lookup behavior. Lookup resolves identity/reference metadata only and does not load asset payloads.

### UAT-14-03 — Calendar and planning-basis resolution boundary

Result: Pass

Calendar and planning-basis resolution is explicit and bounded.

Calendar resolution returns deterministic core-engine input metadata. Planning-basis resolution returns duration/dependency-source metadata. Calendar arithmetic, schedule generation, task duration calculation, Gantt/rendering, and payload loading remain outside Milestone 14.

The resolved calendar/planning-basis records are accepted as future deterministic core-engine inputs, not as planning outputs.

### UAT-14-04 — Authored-source versus deployment-compiled separation

Result: Pass

Authored-source and deployment-compiled lookup roles are separated.

Authored source remains editable source authority. Deployment-compiled records are runtime lookup surfaces only. Compiled lookup may reference authored source identity but cannot become source authority. Source-to-compiled linkage remains version-pinned and fails closed on mismatch or authority override.

### UAT-14-05 — Governed retrieval versus support retrieval

Result: Pass

Governed retrieval and support retrieval are structurally distinct.

Governed retrieval is deterministic, version-pinned, and authority-preserving. Support retrieval is non-authoritative context only. Support retrieval cannot redefine source truth, execution truth, compiled truth, governed lookup identity, or payload authority.

Support retrieval remains compatible with later AI retrieval rules without becoming an AI runtime implementation inside Milestone 14.

### UAT-14-06 — Validation evidence alignment

Result: Pass

The Milestone 14 validation checkpoint is recorded and green.

The latest recorded validation result is:

`python -m pytest -q` — `724 passed in 51.47s`

Validation evidence exists at:

`docs/M14_VALIDATION_CHECKPOINT.md`

## Acceptance Decision

Pass

## Acceptance Rationale

Milestone 14 is accepted as a governed resolver / registry and governed data-layer boundary.

The milestone establishes explicit resolver/registry access boundaries, version-aware governed asset lookup, calendar/planning-basis resolution contracts, authored-source versus deployment-compiled separation, and governed retrieval versus support-retrieval role discipline.

The milestone does not claim to provide final UI/API delivery, support-retrieval execution, AI retrieval runtime behavior, calendar arithmetic, planning calculation, asset payload loading, or library content expansion. Those remain downstream concerns.

## Open UAT Blockers

None.

## Next Checkpoint

M14.8 — Milestone closeout

## Recorded On

2026-05-04
