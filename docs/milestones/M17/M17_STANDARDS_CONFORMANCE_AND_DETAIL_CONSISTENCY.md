# M17.3 — Standards-Conformance and Detail-Level Consistency Checks

## Scope

`M17.3` defines deterministic AI-evaluation checks for standards conformance and detail-level consistency.

This checkpoint consumes structured guarded authoring payloads inherited from the closed `M12` governed document-engine boundary.

It does not evaluate raw generated text, call an LLM, generate documents, approve documents, release workflows, mutate state, implement retrieval-use governance, or reopen document template/product implementation.

## Relationship to M12

`M12.5` introduced standards, language, assumption, placeholder, evidence/inference, prohibited-language, section-level, and detail-consistency guardrails.

`M17.3` does not replace that document-engine logic.

It measures whether AI-facing guarded authoring payloads remain aligned with those already governed structures.

## Relationship to M17.2

`M17.2` owns:

- quality gates
- groundedness checks
- evidence-link checks
- source-role checks

`M17.3` owns:

- standards-conformance checks
- detail-level consistency checks

The two checkpoints remain separate. `M17.3` may consume an `M17.2` quality-gate result as an optional upstream signal, but it does not reopen or mutate the `M17.2` payload contract.

## Standards-conformance checks

The M17.3 standards-conformance result checks:

- declared standards references are version-pinned
- section standards references are version-pinned
- section standards references are declared in the document-family guardrail policy
- prohibited language patterns are detected
- document-family alignment remains consistent across payload, policy, and authoring snapshot

## Detail-level consistency checks

The M17.3 detail-consistency result checks:

- required sections are present
- disallowed sections fail
- duplicate section IDs fail
- evidence-supported sections include evidence references
- bounded-inference sections include inference references and labeled assumptions
- explicit-assumption sections include labeled assumptions
- placeholder-only sections include explicit placeholder markers
- document-family alignment remains consistent across payload, policy, and authoring snapshot

## Explicit exclusions

M17.3 does not implement:

- actual LLM calls
- prompt templates
- raw generated document text review
- actual document generation from expanded library content
- document template/product implementation
- retrieval-use governance
- recommendation behavior
- UI/API behavior
- workflow mutation
- document approval or release

## Template re-entry note

Document template/product implementation remains deferred to a post-M17, pre-M18 decision gate.

The re-entry scope is not the closed M12 document-engine boundary.

The re-entry scope is actual document template/product implementation from expanded governed library content.
