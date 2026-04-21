# docs/reference/M11_4_RETRIEVAL_ARCHITECTURE_BASICS.md

# M11_4_RETRIEVAL_ARCHITECTURE_BASICS

## Status

Active reference for `M11.4` — Retrieval architecture basics.

## Purpose

Define the minimum retrieval architecture baseline for the current Phase 4 roadmap window.

This checkpoint does not implement resolver/registry behavior.
This checkpoint does not implement live search behavior.
This checkpoint does not introduce AI generation behavior.

It establishes explicit retrieval categories, explicit separation rules, and explicit non-authority rules so later retrieval work cannot blur governed source resolution with broader search behavior.

## Current local decision

The current local decision for `M11.4` is:

- introduce a dedicated retrieval boundary package
- define retrieval architecture contracts and validation rules only
- avoid live retrieval execution in this slice
- keep retrieval downstream from future resolver/registry foundations
- keep retrieval separate from adapters and separate from runtime generation helpers

## Canonical retrieval categories

### Rule 1 — Governed deterministic retrieval is explicit

Governed deterministic retrieval is the future category for:

- version-pinned governed lookup
- compiled library surfaces
- deterministic downstream consumption of governed assets

In the current slice, this category is represented by an explicit request contract only.

Its current required fields are:

- `artifact_kind`
- `lookup_id`
- `compiled_surface_id`
- `library_version`

Its current source-of-truth role is:

- `downstream_consumer_only`

This means retrieval may consume governed lookup outputs later, but it may not redefine source authority.

### Rule 2 — Probabilistic search retrieval is explicit

Probabilistic search retrieval is the future category for:

- broader search
- broader indexing
- non-authoritative support retrieval

In the current slice, this category is represented by an explicit request contract only.

Its current required fields are:

- `query_text`
- `search_scope`

Its current source-of-truth role is:

- `non_authoritative_support_only`

This means probabilistic retrieval may assist later workflows, but it may not act as governed source resolution.

## Separation rules

### Rule 3 — Governed deterministic retrieval may not accept search-shaped inputs

Governed deterministic retrieval may not declare:

- `query_text`
- `search_scope`

This preserves a clean separation between governed lookup and broad search semantics.

### Rule 4 — Probabilistic search retrieval may not declare governed lookup identity

Probabilistic search retrieval may not declare:

- `artifact_kind`
- `lookup_id`
- `compiled_surface_id`
- `library_version`

This preserves a clean separation between non-authoritative search behavior and governed lookup identity.

### Rule 5 — No retrieval mode may claim source-authority override

Retrieval request contracts in the current slice may not declare:

- `source_authority_override`
- `resolver_bypass`

This keeps retrieval from becoming hidden source-of-truth logic.

## Resolver dependency rule

The current baseline rule is:

- live governed retrieval is not considered ready before future resolver/registry foundations exist

This checkpoint therefore prepares retrieval architecture without letting `M11.4` absorb unresolved resolver concerns.

## Why this checkpoint is intentionally narrow

The current roadmap window requires retrieval basics, not a hidden resolver, not a hidden product search stack, and not a hidden generation feature.

So the current checkpoint establishes:

- one dedicated retrieval boundary
- two explicit retrieval categories
- one explicit non-authority rule-set
- one explicit resolver dependency rule

That is enough to make later retrieval work safer without violating the future architecture direction.

## M11.4 checkpoint output

This checkpoint establishes:

- a dedicated retrieval boundary package
- explicit governed deterministic retrieval contracts
- explicit probabilistic search retrieval contracts
- deterministic validation that prevents category blur
- explicit protection against source-authority override
- explicit dependency on future resolver/registry foundations before live governed retrieval
