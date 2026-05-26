# M17_RETRIEVAL_USE_RULES_AND_SOURCE_ROLE_DISCIPLINE

## Milestone checkpoint

`M17.4` — Retrieval-use rules and source-role discipline

## Scope

This checkpoint defines deterministic AI-layer rules for consuming retrieval context.

It consumes the closed M14.5 governed retrieval versus support-retrieval boundary and evaluates whether AI usage preserves source-role discipline.

## Owned by M17.4

- AI retrieval-use rule baseline
- governed deterministic retrieval consumption checks
- support retrieval consumption checks
- source-role discipline checks
- support-retrieval non-authority enforcement
- fail-closed behavior for source-truth override, execution-truth override, resolver bypass, and mixed authority states

## Boundary inherited from M14.5

Governed deterministic retrieval may be consumed only as governed version-pinned retrieval.

Support retrieval may be consumed only as non-authoritative context.

Support retrieval must not become:

- source truth
- execution truth
- compiled lookup authority
- governed evidence
- workflow mutation authority
- document approval or release authority

## Relationship to M16

M16 context packaging remains the AI-runtime input boundary.

M17.4 does not change M16 context packaging; it evaluates whether retrieval-origin context is being consumed with the correct source-role discipline.

## Relationship to M17.2 and M17.3

M17.2 evaluates groundedness, evidence-link checks, and source-role checks over candidate output metadata.

M17.3 evaluates standards-conformance and detail-level consistency over governed document-engine guardrail payloads.

M17.4 evaluates retrieval-use rules and source-role discipline specifically for governed and support retrieval inputs.

## Explicit non-scope

M17.4 does not implement:

- vector search
- embeddings
- external web search
- asset payload loading
- document generation
- document template/product implementation
- standards-conformance checks
- detail-level consistency checks
- recommendation behavior
- UI/API behavior
- workflow mutation
- approval or release behavior

## Deferred document template/product work

Document template/product implementation and actual document generation from expanded governed library content remain deferred to a post-M17, pre-M18 decision gate.
