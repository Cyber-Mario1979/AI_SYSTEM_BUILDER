# Contributing to AI_SYSTEM_BUILDER

Thank you for your interest in contributing.

This repository is being built with a strong emphasis on deterministic behavior, explicit validation, milestone-based progression, and architecture discipline. Contributions are welcome, but they must fit the operating model of the project.

## Before You Contribute

Please read these repository files first:

- `README.md`
- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `ARCHITECTURE_GUARDRAILS.md`

These files define:

- what the project is
- where the project currently is
- what the next approved checkpoint is
- what architectural boundaries must not be violated

## Core Contribution Rules

Contributions should follow these principles:

- keep behavior deterministic
- do not bypass validation discipline
- do not introduce hidden automation
- do not collapse architectural boundaries
- do not add features outside the current approved direction without explicit approval

The roadmap defines direction.
The tracker defines current position.
The code and tests define implementation truth.

## Contribution Scope

Good contribution types include:

- bug fixes that preserve intended behavior
- test additions or corrections
- documentation improvements
- refactors that improve clarity without changing approved behavior
- implementation work that clearly aligns with the current approved checkpoint

Contributions that are likely to be rejected include:

- speculative features outside the current milestone path
- UI-first expansions that bypass the CLI/domain layering
- hidden or implicit state behavior
- architecture shortcuts that move domain logic into the CLI layer
- broad refactors without checkpoint alignment

## Validation Requirement

All code contributions must pass the repository validation suite before they are considered ready.

Run:

```powershell
python -m pytest -q
```

If validation fails, the contribution is not ready.

How to Propose a Change

For now, the preferred contribution flow is:

open an issue or discussion first if the change affects behavior, scope, architecture, or milestone direction
keep the proposed change narrow and explicit
explain how the change aligns with the roadmap and guardrails
include tests when behavior is added or changed
keep commit messages clear and specific
Pull Request Expectations

A pull request should make it easy to review:

what changed
why it changed
what checkpoint or purpose it supports
what tests were run
whether behavior changed or only structure/docs changed

If a PR changes behavior, the description should state that clearly.

Architecture Expectations

This repository treats the CLI as an adapter layer.

That means contributors should prefer placing behavior in domain or logic modules rather than embedding business rules directly into CLI parsing or command wiring.

Changes that violate architecture guardrails are expected to be rejected.

Documentation Expectations

If a change affects public understanding, developer usage, or milestone evidence, update the relevant documentation too.

This may include:

README.md
milestone notes in docs/
UAT-related docs when applicable
closeout notes when applicable
Conduct

Be respectful, explicit, and technically grounded.

This repository values clarity over noise, determinism over improvisation, and evidence over assumption.
