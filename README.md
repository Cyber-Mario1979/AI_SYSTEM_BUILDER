<p align="center">
  <img src="assets/banner.png" alt="AI_SYSTEM_BUILDER Banner"/>
</p>

<h1 align="center">AI_SYSTEM_BUILDER</h1><p align="center">
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

| Not this                       | Because                                                     |
| ------------------------------ | ----------------------------------------------------------- |
| A general AI agent framework   | AI/runtime expansion is downstream, not the starting point. |
| A CQV-only application         | CQV is the proving ground, not the product identity.        |
| A vibe-coded prototype         | Checkpoints are validated before progression.               |
| A free-form automation sandbox | Mutation rules are explicit; nothing happens implicitly.    |

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

| Surface                      | Purpose                                                   |
| ---------------------------- | --------------------------------------------------------- |
| `README.md`                  | Public overview and onboarding                            |
| `PROGRESS_TRACKER.md`        | Current implementation position and validation status     |
| `ROADMAP_CANONICAL.md`       | Roadmap direction and checkpoint sequence                 |
| `ROADMAP_ADDENDUM_*.md`      | Bounded overlays for controlled exceptions or transitions |
| `ARCHITECTURE_GUARDRAILS.md` | Permanent architectural boundaries                        |
| `asbp/` and `tests/`         | Implementation truth and validation evidence              |

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

<p align="center">
  <strong>A deterministic Python system for building trustworthy workflow engines — one validated layer at a time.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tests-524%20passed-brightgreen" alt="524 passed"/>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-lightgrey" alt="GPLv3"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/ROADMAP_CANONICAL.md"><img src="https://img.shields.io/badge/Roadmap-Canonical-blueviolet" alt="Roadmap"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/README.md#quick-start"><img src="https://img.shields.io/badge/Quick%20Start-Guide-success" alt="Quick Start"/></a>
</p>

---

## The core idea

Most workflow systems are built fast and trusted late — if ever.

**AI_SYSTEM_BUILDER** inverts that. It builds trust into every layer from day one:

- **Deterministic before smart** — behavior is explicit and predictable before any automation is layered on top
- **Validated before convenient** — state mutations are controlled and persisted with evidence
- **Governed before expanded** — milestones are closed by acceptance, not by assumption

The result is a workflow engine you can reason about, extend with confidence, and eventually hand off to richer runtime layers — because the foundation was designed to hold that weight.

---

## What this project is — and what it is not

### What it is

**AI_SYSTEM_BUILDER** is a roadmap-driven Python system for modeling workflow entities, their relationships, and the validation rules that govern them. It is built to demonstrate that a serious, trustworthy workflow engine can be constructed by a solo builder working in structured cooperation with an AI platform.

The project proves three things simultaneously:

1. That deterministic behavior must be **designed** — not assumed or retrofitted
2. That milestone governance produces a codebase that can be navigated by someone other than its author
3. That a real engineering foundation can be built through human + AI co-building under strict execution discipline

### What it is not

| Not this                       | Because                                                    |
| ------------------------------ | ---------------------------------------------------------- |
| A general AI agent framework   | AI/runtime expansion is downstream, not the starting point |
| A CQV application              | CQV is the proving ground, not the product identity        |
| A vibe-coded prototype         | Every checkpoint is validated before progression           |
| A free-form automation sandbox | Mutation rules are explicit; nothing happens implicitly    |

> **On CQV:** Pharmaceutical commissioning, qualification, and validation was chosen as the test domain precisely because it is demanding, regulated, and unforgiving. When the system holds up under CQV pressure, it holds up everywhere.

---

## Current live boundary

> **Controlled post-M11 transition window under `ROADMAP_ADDENDUM_07_POST_M11_TRANSITION_AND_ROADMAP_EXTENSION_GATE.md`**

| Tracker field                    | Current value                                                          |
| -------------------------------- | ---------------------------------------------------------------------- |
| Current phase                    | Phase 4 closeout to Phase 5 transition window                          |
| Current milestone                | Post-M11 transition under Addendum 07                                  |
| Current approved slice family    | `A07.4` — Public-surface and export-surface audit                      |
| Latest completed checkpoint      | `A07.3` — README and runtime/operator-document normalization completed |
| Exact next unfinished checkpoint | `A07.4` — Public-surface and export-surface audit                      |
| Milestone UAT status             | `PASSED`                                                               |
| Validation status                | `python -m pytest -q` → `524 passed in 45.65s`                         |

**Stable capabilities at this boundary:**

- Deterministic state, task, Work Package, collection, and planning-foundation layers
- Selector-context and standards-bundle binding on Work Packages
- Cross-entity read/update/validation behavior across Work Packages, collections, tasks, and plans
- Canonical versioning surface through `asbp.versioning`
- Governed-versus-probabilistic retrieval separation through `asbp.retrieval`
- Deterministic blocked-state and execution-ready runtime boundary/control behavior through the runtime package
- Deterministic candidate-response validation, retry/fail behavior, output acceptance, and output-retry behavior
- Preserved package-aligned runtime and retrieval exports after the Milestone 11 cleanup and closeout

---

## Architecture principles

### 1 — Determinism is a first-class design rule

Command behavior, failure behavior, state mutation rules, retrieval boundaries, and persistence validation are all explicit by design — not emergent, not discovered at runtime.

### 2 — The CLI is an adapter, not the system

Domain logic lives in core modules. The CLI is a thin adapter layer on top. This protects maintainability, future UI readiness, and the ability to layer richer runtime behavior without rewriting the engine.

### 3 — Progression is governed, not improvised

The repository uses a canonical roadmap, active roadmap addenda when needed, architecture guardrails, a current-position tracker, milestone UAT, and milestone closeout notes. The project has **direction**, not just motion.

### 4 — The goal is trustworthy runtime behavior — not just CRUD

The system now spans deterministic workflow entities, bound context, planning foundations, governed retrieval boundaries, and runtime/output validation contracts. That groundwork exists because the long-term direction is toward controlled AI/runtime orchestration — and that future needs a foundation strong enough to support it.

---

## Implemented capabilities

### Stable CLI workflow surfaces

```powershell
python -m asbp state init
python -m asbp state show
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp set-selector-type WP-001 process-equipment
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection set-work-package TC-001 WP-001
python -m asbp wp show WP-001 --show-selector-context --show-collection-ids
```

These surfaces cover deterministic state handling, task operations, Work Package management, selector-context mutation, collection membership, and cross-entity visibility on the current stable CLI boundary.

---

### Public Python package surfaces

The examples below are **curated examples** of the public Python package boundary, not an exhaustive export inventory.

```powershell
@'
from asbp.versioning import build_version_metadata
from asbp.retrieval import build_retrieval_architecture_baseline
from asbp.runtime import build_work_package_runtime_boundary_payload
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

print(build_version_metadata())
print(build_retrieval_architecture_baseline())
print(
    build_work_package_runtime_boundary_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )
)
'@ | python -
```

These package surfaces are part of the repo-real post-M11 boundary. They are public and validated, but they are still logic-first surfaces rather than a fully stabilized operator CLI workflow.

---

## Repository layout

```text
asbp/                         Application source
tests/                        Automated validation suite
docs/                         UAT records, closeout notes, supporting artifacts
assets/                       Repository presentation assets
audits/                       Filed audit observation, response, and triage records
ROADMAP_CANONICAL.md          Canonical direction and checkpoint ladder
ROADMAP_ADDENDUM_*.md         Active or historical bounded overlays
PROGRESS_TRACKER.md           Current-position tracker
ARCHITECTURE_GUARDRAILS.md    Permanent architectural boundary rules
```

---

## Governance model

This repository separates the things that many projects conflate:

| Document / surface                   | Defines                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `ROADMAP_CANONICAL.md`               | Phase order, milestone order, checkpoint ladder, transition rules                                      |
| Active `ROADMAP_ADDENDUM_*.md` files | Temporary bounded overlays when normal progression needs controlled governance                         |
| `ARCHITECTURE_GUARDRAILS.md`         | Permanent boundaries: CLI as adapter, state access rules, approved core-module attachment points       |
| Code and tests                       | What actually exists, what commands are live, what contracts are enforced                              |
| `PROGRESS_TRACKER.md`                | Latest completed checkpoint, exact next unfinished checkpoint, current validation/UAT/alignment status |

That separation is what prevents drift.

---

## Acceptance discipline

A milestone is not closed because code exists. It is closed after:

1. Implementation checkpoints are completed
2. Automated validation passes
3. Milestone UAT is conducted and recorded
4. Milestone closeout is explicitly confirmed

This discipline is non-negotiable and is one of the core things that separates this repository from a typical prototype.

---

## Quick start

**1. Create and activate a virtual environment**

```powershell
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python --version
```

**2. Run validation**

```powershell
python -m pytest -q
```

**3. Initialize local state**

```powershell
python -m asbp state init
python -m asbp state show
```

**4. Explore the stable CLI boundary**

```powershell
python -m asbp --help
python -m asbp state -h
python -m asbp task -h
python -m asbp wp -h
python -m asbp collection -h
```

---

## What comes next

The project is currently in a controlled post-M11 transition window governed by Addendum 07.

The next active transition checkpoint is:

- `A07.4` — Public-surface and export-surface audit

That means the immediate remaining work is not direct Phase 5 implementation yet. The repo is moving through:

1. public-surface and export-surface audit
2. canonical roadmap continuation packaging
3. tracker re-entry
4. clean return to normal roadmap-controlled execution

Direct feature expansion resumes only after that transition gate is finished.

---

## License

Licensed under the **GNU General Public License v3.0**.  
See `LICENSE` for full terms.
