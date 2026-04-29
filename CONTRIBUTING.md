# Contributing to AI_SYSTEM_BUILDER

Thank you for your interest in contributing.

**AI_SYSTEM_BUILDER** is built with a strong emphasis on deterministic behavior, explicit validation, milestone-based progression, and architecture discipline.

Contributions are welcome when they fit the operating model of the project.

---

## Before you contribute

Please read these files first:

- [`README.md`](README.md)
- [`PROGRESS_TRACKER.md`](PROGRESS_TRACKER.md)
- [`ROADMAP_CANONICAL.md`](ROADMAP_CANONICAL.md)
- [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md)

These files define:

- what the project is
- where the project currently is
- what the next approved checkpoint is
- which architecture boundaries must not be violated

The README is the public overview. It is not the current-state authority.

Use:

- `PROGRESS_TRACKER.md` for current project position
- `ROADMAP_CANONICAL.md` for roadmap direction
- `ARCHITECTURE_GUARDRAILS.md` for architecture boundaries
- code and tests for implementation truth

---

## Core contribution rules

Contributions should follow these principles:

- keep behavior deterministic
- do not bypass validation discipline
- do not introduce hidden automation
- do not collapse architecture boundaries
- do not move domain logic into CLI parsing or command wiring
- do not add features outside the current approved direction without explicit approval
- keep changes narrow, reviewable, and easy to validate

---

## Contribution scope

Good contribution types include:

- bug fixes that preserve intended behavior
- test additions or corrections
- documentation improvements
- public-surface improvements
- narrow refactors that improve clarity without changing behavior
- implementation work that clearly aligns with the current approved checkpoint

Contributions that are likely to be rejected include:

- speculative features outside the current milestone path
- UI-first expansions that bypass the CLI/domain layering
- hidden or implicit state behavior
- architecture shortcuts
- broad refactors without checkpoint alignment
- changes that weaken deterministic validation or persistence guarantees

---

## Public-surface changes

Public-surface changes are welcome when they improve clarity without changing project behavior.

Public-surface files include:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- GitHub issue templates
- GitHub pull request template
- public quickstart or overview documentation

Public-surface changes should not be treated as roadmap, architecture, validation, or code behavior changes unless they explicitly modify those things.

For example:

- improving README wording is a documentation change
- adding an issue template is a repository-maintenance change
- changing command behavior is a code behavior change
- changing milestone sequence is a roadmap change

Keep those categories separate.

---

## How to propose a change

For most changes, open an issue or discussion first if the change affects:

- behavior
- scope
- architecture
- roadmap direction
- milestone progression
- validation rules

When proposing a change, explain:

- what you want to change
- why it matters
- whether behavior changes
- whether tests are needed
- how it aligns with the roadmap and guardrails

Small documentation fixes may go directly to a pull request.

---

## Pull request expectations

A pull request should make the review easy.

Include:

- what changed
- why it changed
- whether behavior changed
- whether the change is public-surface only
- which tests were run
- which issue or checkpoint it relates to, if applicable

If the PR changes behavior, state that clearly.

If the PR only changes documentation or repository surface, state that clearly too.

---

## Validation requirement

All code contributions must pass the repository validation suite before they are considered ready.

Run:

```powershell
python -m pytest -q
```

If validation fails, the contribution is not ready.

Documentation-only changes do not require full validation unless they also affect executable examples, CLI instructions, or test expectations.

---

## Architecture expectations

This repository treats the CLI as an adapter layer.

That means contributors should prefer placing behavior in domain or logic modules rather than embedding business rules directly into CLI parsing or command wiring.

Changes that violate architecture guardrails are expected to be rejected.

Before making architectural changes, read:

- [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md)
- [`ROADMAP_CANONICAL.md`](ROADMAP_CANONICAL.md)
- [`PROGRESS_TRACKER.md`](PROGRESS_TRACKER.md)

---

## Documentation expectations

If a change affects public understanding, developer usage, or milestone evidence, update the relevant documentation.

This may include:

- `README.md`
- `CONTRIBUTING.md`
- files under `docs/`
- UAT-related notes when applicable
- closeout notes when applicable

Do not duplicate live milestone status in the README. Use `PROGRESS_TRACKER.md` for current-state information.

---

## Commit guidance

Prefer clear, specific commit messages.

Good examples:

```text
docs: convert README to evergreen overview
tests: add validation coverage for invalid task status
fix: preserve deterministic task ordering
```

Avoid vague messages such as:

```text
update
fix stuff
changes
```

---

## Conduct

Be respectful, explicit, and technically grounded.

This repository values clarity over noise, determinism over improvisation, and evidence over assumption.

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
