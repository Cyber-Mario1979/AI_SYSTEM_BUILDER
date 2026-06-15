<p align="center">
  <img src="assets/banner.png" alt="AI_SYSTEM_BUILDER Banner"/>
</p>

<h1 align="center">AI_SYSTEM_BUILDER</h1>

<p align="center">
  <strong>A deterministic Python system for building trustworthy workflow engines — one validated layer at a time.</strong>
</p>

<p align="center">
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-lightgrey" alt="GPLv3"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/ROADMAP_CANONICAL.md"><img src="https://img.shields.io/badge/Roadmap-v7-blueviolet" alt="Roadmap v7"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/PROGRESS_TRACKER.md"><img src="https://img.shields.io/badge/Current-M34.2%20PLAN%20ONLY-blue" alt="Current checkpoint"/></a>
  <a href="https://github.com/Cyber-Mario1979/AI_SYSTEM_BUILDER/blob/main/README.md#quick-start"><img src="https://img.shields.io/badge/Quick%20Start-Guide-success" alt="Quick Start"/></a>
</p>

---

# Important Note:

This repository content has been deprecated on the 15-06-2026 becuase of a massive scope drift.

`PUBLIC ARCHIVE`

---

## Project status

**AI_SYSTEM_BUILDER** is under active development.

Current roadmap authority:

```text
ROADMAP_CANONICAL.md v7
```

Current execution position after the M34.1 assessment PR is accepted and merged:

```text
Phase 9 — Full Local Integrated CQV Product Core
M34 — Local Product-Core Closeout and Local Release-Candidate Gate
PLAN M34.2 — DDR closure/reclassification review
```

The current checkpoint is **PLAN only**, not GO. It does not authorize DDR closure/reclassification, local release-candidate approval, engineering readiness entry, deployment, release, SaaS readiness, commercialization, customer-ready output, or full product/runtime AI readiness.

For exact live state, read:

- [`PROGRESS_TRACKER.md`](PROGRESS_TRACKER.md) — current position, latest validation evidence, and next checkpoint
- [`ROADMAP_CANONICAL.md`](ROADMAP_CANONICAL.md) — canonical roadmap direction and checkpoint deliverables
- [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md) — permanent architecture boundaries
- [`docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`](docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md) — deferred/productization-sensitive dependency gate memory

The README is a public front door. It summarizes the project without replacing the tracker or roadmap.

---

## The core idea

Most workflow systems are built fast and trusted late — if ever.

**AI_SYSTEM_BUILDER** inverts that. It builds trust into every layer from day one:

- **Deterministic before smart** — behavior is explicit and predictable before automation is layered on top.
- **Validated before convenient** — state mutations are controlled and persisted with evidence.
- **Build-forward governance** — governance defines the boundary, but implementation and validation prove progress.

The goal is a workflow engine that can be reasoned about, extended with confidence, and eventually connected to richer runtime layers because the foundation was designed to hold that weight.

---

## Current roadmap direction

Roadmap v7 makes the remaining path explicit.

The greater final goal is to finish a real local integrated CQV product before any deployment or hosted-path decision. The product must be usable locally, evidence-based, validated, accepted by the owner, and explicit about limitations.

The forward path is:

1. complete the M34 local product-core closeout gates, starting with `PLAN M34.2` after M34.1 is accepted and merged;
2. review DDR closure/reclassification evidence in M34.2;
3. record product-core limitations and local release-candidate boundary decisions through M34.3-M34.5;
4. complete validation, owner acceptance, and Phase 9 closeout through M34.6-M34.8;
5. proceed to engineering readiness, packaging, installability, security/supportability, and deployment-path evaluation only after local product-core acceptance.

Roadmap v7 uses the checkpoint column:

```text
Required deliverable / completion minimum
```

This is intentional. It prevents build/content and hybrid checkpoints from being closed by documentation alone.

---

## What this project is — and what it is not

### What it is

**AI_SYSTEM_BUILDER** is a roadmap-driven Python system for modeling workflow entities, relationships, state transitions, validation rules, source boundaries, output controls, and controlled execution surfaces.

It is also a build-in-public engineering experiment: a serious codebase being developed by a solo builder in structured cooperation with an AI platform, under strict execution discipline.

The project is designed to prove three things:

1. Deterministic behavior must be **designed**, not assumed.
2. Milestone governance is useful only when it protects real implementation and validation.
3. Human + AI co-building can produce real engineering structure when constrained by explicit rules, tests, and acceptance gates.

### What it is not

| Not this | Because |
| --- | --- |
| A general AI agent framework | AI/runtime expansion is downstream and bounded, not the starting point. |
| A CQV-only application | CQV is the pressure-test domain; the long-term system identity is broader. |
| A vibe-coded prototype | Checkpoints require evidence before progression. |
| A free-form automation sandbox | Mutation rules are explicit; nothing happens implicitly. |
| A commercialization launch plan | Business/commercial launch work is outside ASBP unless separately approved later. |

> **On CQV:** Pharmaceutical commissioning, qualification, and validation was chosen as a pressure-test domain because it is demanding, regulated, and unforgiving. The long-term system identity is broader than CQV.

---

## Architecture principles

### 1. Determinism is a first-class design rule

Command behavior, failure behavior, state mutation rules, retrieval boundaries, AI boundaries, output controls, and persistence validation are explicit by design.

### 2. The CLI, API, and UI are adapters, not the system

Domain logic belongs in core modules and governed service boundaries. External surfaces should expose behavior without becoming the place where business rules are hidden.

### 3. Progression is governed, not improvised

The repository uses a canonical roadmap, current-position tracker, architecture guardrails, validation evidence, closeout discipline, and deferred dependency gate memory to avoid drift.

### 4. Code, source data, and tests remain implementation truth

Documentation explains intent and operating context. The codebase, source data, automated tests, validation evidence, and UAT evidence define what actually exists.

### 5. Documentation alone does not prove product capability

Roadmap v7 explicitly blocks `Build/content` and `Hybrid` checkpoints from being closed by documentation alone unless an approved deferral is recorded.

---

## Repository layout

```text
asbp/                         Application source
tests/                        Automated validation suite
data/source/                  Source data used by governed loaders and stores
docs/                         UAT records, closeout notes, supporting artifacts
docs/governance/              Governance registers and dependency gates
docs/milestones/              Milestone plans, evidence, validation, UAT, and closeout records
docs/repo_index/              Repository index evidence
assets/                       Repository presentation assets
audits/                       Filed audit observations, responses, and triage records
ROADMAP_CANONICAL.md          Canonical roadmap direction and checkpoint deliverables
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
| `ROADMAP_CANONICAL.md` | Roadmap direction, checkpoint sequence, and required deliverables |
| `ARCHITECTURE_GUARDRAILS.md` | Permanent architectural boundaries |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Persistent gate memory for deferred/productization-sensitive dependencies |
| `asbp/`, `data/source/`, and `tests/` | Implementation truth and validation evidence |

This separation is intentional. It keeps the README stable while allowing actual project state to evolve through controlled files.

---

## Quick start

### 1. Create and activate a virtual environment

```powershell
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python --version
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Run validation

```powershell
python -m pytest -q
```

### 4. Explore the CLI

```powershell
python -m asbp --help
python -m asbp state -h
python -m asbp task -h
python -m asbp wp -h
python -m asbp collection -h
```

### 5. Initialize local state

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
4. [`docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`](docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md), when the work touches deferred/productization-sensitive dependencies
5. [`CONTRIBUTING.md`](CONTRIBUTING.md)

For code changes, run the validation suite before opening a pull request:

```powershell
python -m pytest -q
```

For documentation changes, keep the change narrow and avoid turning the README into the live tracker.

---

## Contributing

Contributions are welcome when they preserve the project’s operating model.

Good contribution areas include:

- documentation clarity;
- tests;
- focused bug fixes;
- narrow refactors that preserve behavior;
- public-surface improvements;
- implementation aligned with the current roadmap checkpoint.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request.

---

## License

Licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](LICENSE) for full terms.
