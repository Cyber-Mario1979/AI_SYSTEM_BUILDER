# Documentation

## Purpose

This folder contains project documentation, milestone evidence, UAT records, governance records, decision records, standards records, design specifications, planning references, archives, and controlled reference material for AI_SYSTEM_BUILDER.

## Main areas

| Area | Purpose |
|---|---|
| `milestones/` | Milestone evidence, validation checkpoints, closeout notes, and checkpoint decision records grouped by milestone. |
| `UAT/` | Milestone User Acceptance Testing protocols, reports, and acceptance evidence. |
| `governance/` | Living governance registers and gate-memory records, including deferred dependency governance. |
| `decision_gates/` | Project execution decisions and redirect/transition decisions. |
| `change_control/` | Approved roadmap or governance change-control records. |
| `standards/` | Standards source registry, citation authority model, and standards-governance evidence. |
| `cleanup/` | Cleanup planning and cleanup evidence packages when approved. |
| `design_spec/` | Design specifications, source snapshots, VALOR reference snapshots, and structured expansion records. |
| `design_notes/` | Design notes, acknowledgments, and design-review support material. |
| `design_future/` | Future-facing design records and deferred design tracks. |
| `planning/` | Planning references that do not directly govern execution. |
| `reference/` | Reference guides and cheat sheets. |
| `archives/` | Historical addenda, roadmap-support files, drafts, and archived governance/support documents retained for traceability. |

## Authority note

Root-level project authority remains outside this folder unless explicitly stated:

- `ROADMAP_CANONICAL.md`
- active `ROADMAP_ADDENDUM_*.md` files, when explicitly present and marked `ACTIVE`
- `ARCHITECTURE_GUARDRAILS.md`
- repo reality from code, tests, package structure, commands, behavior, validation evidence, and UAT evidence
- `PROGRESS_TRACKER.md`

Repo-side governance files inside this folder may also be active within their declared scope, especially:

- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/standards/STANDARDS_SOURCE_REGISTRY.md`
- approved records under `docs/change_control/` and `docs/decision_gates/`

This folder helps organize evidence and support material. It does not replace the authority order.

## Post-roadmap-v5 cleanup note

After roadmap v5, root-level historical roadmap addenda and roadmap-support files may be archived under `docs/archives/` through controlled cleanup only. Archived files remain traceability evidence and do not become active roadmap authority unless a later approved change explicitly says so.
