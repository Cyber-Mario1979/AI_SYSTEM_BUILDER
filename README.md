# AI_SYSTEM_BUILDER

A deterministic Python CLI project for building structured system-modeling workflows with strong validation discipline, milestone-based progression, and explicit operational boundaries.

This repository is being built as a serious engineering foundation first:
- deterministic before “smart”
- validated before convenient
- explicit state before hidden automation
- milestone acceptance before forward expansion

---

## What this project is

**AI_SYSTEM_BUILDER** is a roadmap-driven Python system that models operational workflow entities and their relationships through a controlled CLI.

At its current boundary, the repository provides a deterministic core for:

- tasks
- Work Packages
- task collections
- Work Package binding context
- milestone validation
- milestone-level UAT and closeout discipline

This is not a toy CLI and not a loose experiment repo.

The long-term direction is a more capable workflow engine that can eventually support richer planning, structured runtime orchestration, and controlled output generation. But the repository intentionally builds that future on top of explicit deterministic layers rather than jumping straight into AI behavior.

---

## Why this repository exists

Many workflow-oriented systems become hard to trust because they mix:
- business logic
- state mutation
- UI assumptions
- free-form behavior
- weak validation

too early.

This repository exists to do the opposite.

The project is designed to prove that a useful workflow engine can be built by establishing:

- explicit entity models
- deterministic mutation rules
- validated persistence
- stable command contracts
- checkpoint-based milestone progression
- milestone UAT before closeout

That makes the project useful both as:
- a real engineering build
- and a serious learning/building repository for deterministic system design

---

## Current public boundary

The live repository is currently beyond Milestone 6 closeout, with the next roadmap checkpoint at **Milestone 7.1 — Planning entity foundation**.

The stable completed boundary includes:

- deterministic task management
- Work Package model and task-to-Work-Package association
- task collections with controlled workflow states
- deterministic collection membership rules
- Work Package selector context with:
  - selector type
  - preset binding seed
  - standards bundles
  - scope / intent
- milestone UAT and closeout records through Milestone 6

Latest recorded validated baseline on the current repo boundary:

- `332 passed in 32.28s`

---

## What makes this repository different

### 1. Determinism is a first-class design rule

This project does not treat determinism as a cleanup step.

Deterministic behavior is part of the design from the beginning:
- command behavior is explicit
- failure behavior is explicit
- state mutation rules are explicit
- acceptance happens through validation and UAT, not assumption

### 2. The CLI is treated as an adapter, not the system itself

The repository follows an architecture where the CLI is an adapter layer and domain behavior belongs in core logic modules.

That matters because it protects:
- maintainability
- future UI readiness
- future runtime layering
- clearer separation of concerns

### 3. Progression is governed, not improvised

This repository is not advanced by random feature additions.

It uses:
- a canonical roadmap
- a current-position tracker
- validation checkpoints
- milestone UAT checkpoints
- milestone closeout notes

That means the project has direction, not just motion.

### 4. It is building toward a real workflow engine, not just CRUD

The repo already goes beyond basic entity CRUD by modeling:
- Work Package-centered workflow structure
- collection state concepts
- context-aware binding
- explicit milestone evidence

That is important because the project direction is toward structured operational workflow execution, not just storing records.

---

## Implemented capabilities

### State and task layer

Current CLI supports state initialization, inspection, and controlled mutation, plus deterministic task operations.

Examples:

```powershell
python -m asbp state init
python -m asbp state show
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task list
```

### Work Package layer

Current CLI supports Work Package creation, inspection, update, deletion, filtering, and task association surfaces.

Examples:

```powershell
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp list
python -m asbp wp show WP-001
python -m asbp task set-work-package prepare-fat WP-001
```

### Collection layer

Current CLI supports collection creation, listing, show, state/title update, and task membership add/remove behavior.

Examples:

```powershell
python -m asbp collection add "Source Pool"
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection list
python -m asbp collection show TC-001
python -m asbp collection add-task TC-001 prepare-fat
```

### Binding-context layer

Current CLI supports deterministic selector/binding surfaces on Work Packages.

Examples:

```powershell
python -m asbp wp set-selector-type WP-001 process-equipment
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-scope-intent WP-001 post-deviation
python -m asbp wp show WP-001 --show-selector-context
```

---

## Repository operating model

This repository separates direction, implementation truth, and current position.

### Roadmap

`ROADMAP_CANONICAL.md`

Defines:
- phase order
- milestone order
- checkpoint ladder
- milestone boundaries
- milestone transition rules

### Implementation truth

The code and tests in the repository

Defines:
- what actually exists now
- what commands are live
- what validations are live
- what behavior is truly implemented

### Current-position tracker

`PROGRESS_TRACKER.md`

Defines only:
- latest completed checkpoint
- exact next unfinished checkpoint
- latest recorded validation status
- milestone UAT state

This separation is intentional and is a major part of how the project avoids drift.

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

### 3. Initialize local state

```powershell
python -m asbp state init
python -m asbp state show
```

### 4. View CLI help

```powershell
python -m asbp --help
python -m asbp wp -h
python -m asbp collection -h
python -m asbp task -h
```

---

## Repository layout

```text
asbp/                         application source
tests/                        automated validation suite
docs/                         UAT records, closeout notes, supporting artifacts
ROADMAP_CANONICAL.md          canonical direction and checkpoint ladder
PROGRESS_TRACKER.md           short current-state execution tracker
ARCHITECTURE_GUARDRAILS.md    permanent architectural boundary rules
```

---

## Validation and acceptance discipline

Automated tests are required, but they are not the only acceptance layer.

This repository uses:

1. implementation checkpoints
2. automated validation
3. milestone UAT
4. milestone closeout

That means a milestone is not treated as complete just because code exists.

It must also be:
- validated
- accepted at milestone level
- explicitly closed

---

## Product direction

The next major system direction after the current boundary is the Planning Layer.

That future layer is expected to build on the already-stable foundations for:

- Work Package-centered workflow
- collection state handling
- context-aware binding
- deterministic behavior

Longer term, this project is intended to support richer workflow execution and controlled output generation, but only after the underlying deterministic model is strong enough to justify it.

That sequencing is deliberate.

---

## Public-readiness note

This repository is currently being prepared for public visibility.

That means some public-facing materials may continue to improve, especially:

- root documentation
- license clarity
- repository presentation
- onboarding polish

The implementation boundary, tests, roadmap, tracker, and milestone evidence remain the authoritative technical reference points.

---

## License

License file to be finalized as part of the public-readiness workstream.
