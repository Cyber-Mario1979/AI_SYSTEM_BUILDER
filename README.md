<p align="center">
  <img src="assets/banner.png" alt="AI_SYSTEM_BUILDER Banner"/>
</p>

<h1 align="center">AI_SYSTEM_BUILDER</h1>

<p align="center">
  <strong>A deterministic Python system for building trustworthy workflow engines — one validated layer at a time.</strong>
</p>

<p align="center">
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-lightgrey" alt="GPLv3"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/ROADMAP_CANONICAL.md"><img src="https://img.shields.io/badge/Roadmap-Canonical-blueviolet" alt="Roadmap"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/PROGRESS_TRACKER.md"><img src="https://img.shields.io/badge/Status-Progress%20Tracker-blue" alt="Progress Tracker"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/README.md#quick-start"><img src="https://img.shields.io/badge/Quick%20Start-Guide-success" alt="Quick Start"/></a>
</p>

---

## Project status

**AI_SYSTEM_BUILDER** is under active development.

This README is the public front door for the project. It explains the purpose, operating model, repository layout, and how to get started.

For the current implementation state, validation status, latest completed checkpoint, and exact next checkpoint, use:

- [`PROGRESS_TRACKER.md`](PROGRESS_TRACKER.md) — current project position
- [`ROADMAP_CANONICAL.md`](ROADMAP_CANONICAL.md) — canonical roadmap direction
- [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md) — permanent architecture boundaries

The README intentionally avoids live milestone tables or manual test-count badges so it does not drift behind the repository.

---

## The core idea

Most workflow systems are built fast and trusted late — if ever.

**AI_SYSTEM_BUILDER** inverts that. It builds trust into every layer from day one:

- **Deterministic before smart** — behavior is explicit and predictable before automation is layered on top
- **Validated before convenient** — state mutations are controlled and persisted with evidence
- **Governed before expanded** — progression is closed by acceptance, not by assumption

The goal is a workflow engine that can be reasoned about, extended with confidence, and eventually connected to richer runtime layers because the foundation was designed to hold that weight.

---

## What this project is — and what it is not

### What it is

**AI_SYSTEM_BUILDER** is a roadmap-driven Python system for modeling workflow entities, relationships, state transitions, validation rules, and controlled execution boundaries.

It is also a build-in-public engineering experiment: a serious codebase being developed by a solo builder in structured cooperation with an AI platform, under strict execution discipline.

The project is designed to prove three things:

1. Deterministic behavior must be **designed**, not assumed.
2. Milestone governance makes a codebase easier to review, extend, and maintain.
3. Human + AI co-building can produce real engineering structure when constrained by explicit rules, tests, and acceptance gates.

### What it is not

| Not this | Because |
| --- | --- |
| A general AI agent framework | AI/runtime expansion is downstream, not the starting point. |
| A CQV-only application | CQV is the proving ground, not the product identity. |
| A vibe-coded prototype | Checkpoints are validated before progression. |
| A free-form automation sandbox | Mutation rules are explicit; nothing happens implicitly. |

> **On CQV:** Pharmaceutical commissioning, qualification, and validation was chosen as a pressure-test domain because it is demanding, regulated, and unforgiving. The long-term system identity is broader than CQV.

---

## Architecture principles

### 1. Determinism is a first-class design rule

Command behavior, failure behavior, state mutation rules, retrieval boundaries, and persistence validation are explicit by design.

### 2. The CLI is an adapter, not the system

Domain logic belongs in core modules. The CLI should expose behavior without becoming the place where business rules are hidden.

### 3. Progression is governed, not improvised

The repository uses a canonical roadmap, current-position tracker, architecture guardrails, validation evidence, and closeout discipline to avoid drift.

### 4. Code and tests remain implementation truth

Documentation explains intent and operating context. The codebase and automated tests define what actually exists and what is currently enforced.

---

## Repository layout

```text
asbp/                         Application source
tests/                        Automated validation suite
docs/                         UAT records, closeout notes, supporting artifacts
assets/                       Repository presentation assets
audits/                       Filed audit observations, responses, and triage records
ROADMAP_CANONICAL.md          Canonical roadmap direction and checkpoint ladder
ROADMAP_ADDENDUM_*.md         Bounded roadmap overlays when active or retained for history
PROGRESS_TRACKER.md           Current project position and validation status
ARCHITECTURE_GUARDRAILS.md    Permanent architecture boundary rules
CONTRIBUTING.md               Contribution expectations and review discipline
LICENSE                       GPLv3 license terms
```

---

## Governance model

This repository separates public explanation, project control, and implementation truth:

| Surface | Purpose |
| --- | --- |
| `README.md` | Public overview and onboarding |
| `PROGRESS_TRACKER.md` | Current implementation position and validation status |
| `ROADMAP_CANONICAL.md` | Roadmap direction and checkpoint sequence |
| `ROADMAP_ADDENDUM_*.md` | Bounded overlays for controlled exceptions or transitions |
| `ARCHITECTURE_GUARDRAILS.md` | Permanent architectural boundaries |
| `asbp/` and `tests/` | Implementation truth and validation evidence |

This separation is intentional. It keeps the README stable while allowing the actual project state to evolve through controlled files.

---

## Quick start

### 1. Create and activate a virtual environment

```powershell
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python --version
```

### 2. Run validation

```powershell
python -m pytest -q
```

### 3. Explore the CLI

```powershell
python -m asbp --help
python -m asbp state -h
python -m asbp task -h
python -m asbp wp -h
python -m asbp collection -h
```

### 4. Initialize local state

```powershell
python -m asbp state init
python -m asbp state show
```

---

## Working with the project

Before making a change, read:

1. [`PROGRESS_TRACKER.md`](PROGRESS_TRACKER.md)
2. [`ROADMAP_CANONICAL.md`](ROADMAP_CANONICAL.md)
3. [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md)
4. [`CONTRIBUTING.md`](CONTRIBUTING.md)

For code changes, run the validation suite before opening a pull request:

```powershell
python -m pytest -q
```

For public-surface documentation changes, keep the change narrow and avoid turning the README into a live project tracker.

---

## Contributing

Contributions are welcome when they preserve the project’s operating model.

Good contribution areas include:

- documentation clarity
- tests
- focused bug fixes
- narrow refactors that preserve behavior
- public-surface improvements
- implementation aligned with the current roadmap checkpoint

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request.

---

## License

Licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](LICENSE) for full terms.
