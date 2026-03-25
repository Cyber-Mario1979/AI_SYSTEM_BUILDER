# ROADMAP_UPDATED_2026-03-25.md

## Phase 1 — Foundations

### Milestone 1 — CLI + State Core

Status: Completed

Delivered:

- CLI structure
- State model
- Validation
- State commands

---

### Milestone 2 — Mini Deterministic Engine

Status: In Progress

#### Completed

- task add
- task list
- task list --status
- task update-status
- task delete
- task show
- Refactor checkpoint (task_logic extraction)
  - logic layer expanded
  - CLI rewired
  - tests added
  - full validation passed

#### Current Step

Milestone 2 Planning Checkpoint

Goal:

- Define next exact build slice post-refactor

---

### Next (To Be Defined)

- Next deterministic capability slice
- Potential candidates:
  - task sequencing / ordering
  - task dependency handling
  - advanced filtering / querying
  - state transition rules

---

## Rules

- Follow roadmap → tracker → execution
- One step at a time
- No drift
- Local repo is source of truth
