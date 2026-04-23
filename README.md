<p align="center">
  <img src="assets/banner.png" alt="AI_SYSTEM_BUILDER Banner"/>
</p>

<h1 align="center">AI_SYSTEM_BUILDER</h1>

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

| Tracker field                    | Current value                                                |
| -------------------------------- | ------------------------------------------------------------ |
| Current phase                    | Phase 4 closeout to Phase 5 transition window                |
| Current milestone                | Post-M11 transition under Addendum 07                        |
| Current approved slice family    | `A07.3` — README and runtime/operator-document normalization |
| Latest completed checkpoint      | `A07.2` — Cleanup and polish pass completed                  |
| Exact next unfinished checkpoint | `A07.3` — README and runtime/operator-document normalization |
| Milestone UAT status             | `PASSED`                                                     |
| Validation status                | `python -m pytest -q` → `524 passed in 42.83s`               |

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

```powershell
@'
from asbp.versioning import build_version_metadata
from asbp.retrieval import build_retrieval_architecture_baseline
from asbp.runtime import (
    build_work_package_runtime_boundary_payload,
    build_work_package_prompt_contract_payload,
    build_work_package_llm_handoff_payload,
    build_work_package_generation_request_payload,
)

print(build_version_metadata())
print(build_retrieval_architecture_baseline())
print(build_work_package_runtime_boundary_payload)
print(build_work_package_prompt_contract_payload)
print(build_work_package_llm_handoff_payload)
print(build_work_package_generation_request_payload)
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
