---
doc_type: runtime_cheat_sheet
canonical_name: ASBP_RUNTIME_CHEAT_SHEET
status: ACTIVE
governs_execution: false
document_state_mode: session_validated_convenience_reference
authority: non_authoritative_operator_reference
scope_type: runtime_command_surface
---

# ASBP Runtime Cheat Sheet V6

Non-authoritative convenience snapshot based on the latest locally validated runtime command surface in the current session.

Source of truth remains:

- repo code
- `ROADMAP_CANONICAL.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`

---

## Current checkpoint context

- Current milestone: **Milestone 8 — Multi-Entity Coordination**
- Current approved slice family: **M8.5A — Cross-entity read rules**
- Latest completed checkpoint: **M8.4 — Binding-context consistency controls completed**
- Exact next unfinished checkpoint: **M8.5A — Cross-entity read rules**
- Latest locally verified validation status: **402 passed in 37.56s**

---

## Base entry

```bash
python -m asbp
```

## Global

```bash
python -m asbp --version
```

---

## State commands

### Initialize state file

```bash
python -m asbp state init
```

### Show current state

```bash
python -m asbp state show
```

### Set state version

```bash
python -m asbp state set-version <value>
```

Example:

```bash
python -m asbp state set-version 0.8.0
```

### Set state status

Allowed values:

- `not_started`
- `in_flight`
- `completed`

```bash
python -m asbp state set-status <value>
```

Example:

```bash
python -m asbp state set-status in_flight
```

---

## Work Package commands

### List work packages

```bash
python -m asbp wp list [--status <value>] [--title "<value>"] [--wp-id <value>] [--task-id <value>] [--show-task-ids]
```

Allowed `--status` values:

- `open`
- `in_progress`
- `completed`

Useful examples:

```bash
python -m asbp wp list
python -m asbp wp list --status open
python -m asbp wp list --title "Tablet press qualification"
python -m asbp wp list --wp-id WP-001
python -m asbp wp list --task-id TASK-001
python -m asbp wp list --show-task-ids
python -m asbp wp list --task-id TASK-001 --show-task-ids
```

### Show work package

```bash
python -m asbp wp show <wp_id> [--show-task-ids] [--show-selector-context]
```

Examples:

```bash
python -m asbp wp show WP-001
python -m asbp wp show WP-001 --show-task-ids
python -m asbp wp show WP-001 --show-selector-context
python -m asbp wp show WP-001 --show-task-ids --show-selector-context
```

### Add work package

```bash
python -m asbp wp add <wp_id> "<title>"
```

Example:

```bash
python -m asbp wp add WP-001 "Tablet press qualification"
```

### Update work package status

Allowed values:

- `open`
- `in_progress`
- `completed`

```bash
python -m asbp wp update-status <wp_id> <status>
```

Example:

```bash
python -m asbp wp update-status WP-001 in_progress
```

### Update work package title

```bash
python -m asbp wp update-title <wp_id> "<new_title>"
```

Example:

```bash
python -m asbp wp update-title WP-001 "Updated tablet press qualification"
```

### Delete work package

```bash
python -m asbp wp delete <wp_id>
```

Example:

```bash
python -m asbp wp delete WP-001
```

### Set work package selector type

```bash
python -m asbp wp set-selector-type <wp_id> "<system_type>"
```

Example:

```bash
python -m asbp wp set-selector-type WP-001 "process-equipment"
```

### Set work package preset

```bash
python -m asbp wp set-preset <wp_id> "<preset_id>"
```

Example:

```bash
python -m asbp wp set-preset WP-001 "oral-solid-dose-standard"
```

### Set work package standards bundles

CLI accepts only add-on bundle IDs. `cqv-core` is injected automatically as the baseline bundle.

Allowed add-on bundle values:

- `cleanroom-hvac`
- `automation`

```bash
python -m asbp wp set-standards-bundles <wp_id> [add_on_bundle_id_1] [add_on_bundle_id_2]
```

Examples:

```bash
python -m asbp wp set-standards-bundles WP-001
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-standards-bundles WP-001 cleanroom-hvac automation
```

### Set work package scope intent

Allowed values:

- `end-to-end`
- `qualification-only`
- `commissioning-only`
- `periodic-verification`
- `post-change`
- `post-deviation`

```bash
python -m asbp wp set-scope-intent <wp_id> <scope_intent>
```

Examples:

```bash
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp wp set-scope-intent WP-001 end-to-end
```

---

## Collection commands

### List collections

```bash
python -m asbp collection list [--collection-state <value>] [--title "<value>"] [--collection-id <value>]
```

Allowed `--collection-state` values:

- `source`
- `staged`
- `committed`
- `refined`

Useful examples:

```bash
python -m asbp collection list
python -m asbp collection list --collection-state committed
python -m asbp collection list --title "Committed Selection"
python -m asbp collection list --collection-id TC-001
```

### Add collection

```bash
python -m asbp collection add "<title>" [--collection-state <value>]
```

Examples:

```bash
python -m asbp collection add "Source Pool"
python -m asbp collection add "Committed Selection" --collection-state committed
```

### Show collection

```bash
python -m asbp collection show <collection_id>
```

Example:

```bash
python -m asbp collection show TC-001
```

### Update collection title

```bash
python -m asbp collection update-title <collection_id> "<new_title>"
```

Example:

```bash
python -m asbp collection update-title TC-001 "Updated Committed Selection"
```

### Update collection state

```bash
python -m asbp collection update-state <collection_id> <collection_state>
```

Example:

```bash
python -m asbp collection update-state TC-001 staged
```

### Add task to collection

Task reference resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp collection add-task <collection_id> <task_reference>
```

Examples:

```bash
python -m asbp collection add-task TC-001 TASK-001
python -m asbp collection add-task TC-001 "prepare-fat"
```

### Remove task from collection

Task reference resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp collection remove-task <collection_id> <task_reference>
```

Examples:

```bash
python -m asbp collection remove-task TC-001 TASK-001
python -m asbp collection remove-task TC-001 "prepare-fat"
```

---

## Task commands

### Add task

```bash
python -m asbp task add "<title>" [--description "<text>"] [--owner "<name>"] [--duration <days>] [--start-date "<yyyy-mm-dd>"] [--end-date "<yyyy-mm-dd>"] [--task-key "<key>"]
```

Example:

```bash
python -m asbp task add "Prepare FAT" --description "Draft FAT package" --owner "Amr" --duration 3 --start-date "2026-03-31" --end-date "2026-04-02" --task-key "prepare-fat"
```

### List tasks

```bash
python -m asbp task list [--status <value>] [--has-dependencies true|false] [--has-dependents true|false] [--show-task-key] [--show-work-package-id] [--show-dependency-refs] [--show-dependent-refs] [--has-task-key true|false] [--task-key "<value>"] [--task-ref "<value>"] [--dependency-ref "<value>"] [--dependent-ref "<value>"] [--work-package-id <wp_id>]
```

Allowed `--status` values:

- `planned`
- `in_progress`
- `completed`
- `over_due`

Useful examples:

```bash
python -m asbp task list
python -m asbp task list --show-task-key
python -m asbp task list --show-work-package-id
python -m asbp task list --show-task-key --show-work-package-id --show-dependency-refs --show-dependent-refs
python -m asbp task list --status completed
python -m asbp task list --has-dependencies true
python -m asbp task list --has-dependents true
python -m asbp task list --has-task-key false --show-task-key
python -m asbp task list --task-key "prepare-fat" --show-task-key
python -m asbp task list --task-ref "TASK-001" --show-task-key
python -m asbp task list --dependency-ref "execute-fat" --show-task-key
python -m asbp task list --dependent-ref "review-fat-package" --show-task-key
python -m asbp task list --work-package-id WP-001 --show-task-key --show-work-package-id
```

### Show task

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task show <task_reference> [--show-work-package-id] [--show-dependency-refs] [--show-dependent-refs]
```

Examples:

```bash
python -m asbp task show TASK-001
python -m asbp task show "prepare-fat"
python -m asbp task show "prepare-fat" --show-work-package-id
python -m asbp task show "review-fat-package" --show-work-package-id --show-dependency-refs --show-dependent-refs
```

### Set task key

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task set-key <task_reference> "<new_task_key>"
```

Example:

```bash
python -m asbp task set-key TASK-001 "prepare-fat"
```

### Clear task key

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task clear-key <task_reference>
```

Example:

```bash
python -m asbp task clear-key TASK-001
```

### Update task status

Allowed values:

- `planned`
- `in_progress`
- `completed`
- `over_due`

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task update-status <task_reference> <status>
```

Examples:

```bash
python -m asbp task update-status TASK-001 in_progress
python -m asbp task update-status "prepare-fat" completed
```

### Set task dependencies

Target resolves by exact `task_id` first, then normalized `task_key`.

Each dependency input also resolves by exact `task_id` first, then normalized `task_key`, but persisted dependency storage remains `task_id`-based.

```bash
python -m asbp task set-dependencies <task_reference> [dependency_1] [dependency_2] [...]
```

Examples:

```bash
python -m asbp task set-dependencies TASK-003 TASK-001 TASK-002
python -m asbp task set-dependencies "review-fat-package" TASK-001 "execute-fat"
```

### Set task work package

Target task resolves by exact `task_id` first, then normalized `task_key`.

The work package input is exact `wp_id`.

```bash
python -m asbp task set-work-package <task_reference> <wp_id>
```

Examples:

```bash
python -m asbp task set-work-package TASK-001 WP-001
python -m asbp task set-work-package "prepare-fat" WP-001
```

### Clear task work package

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task clear-work-package <task_reference>
```

Examples:

```bash
python -m asbp task clear-work-package TASK-001
python -m asbp task clear-work-package "prepare-fat"
```

### Delete task

Target resolves by exact `task_id` first, then normalized `task_key`.

```bash
python -m asbp task delete <task_reference>
```

Examples:

```bash
python -m asbp task delete TASK-001
python -m asbp task delete "prepare-fat"
```

---

## Minimal current runtime verification flow

```bash
python -m pytest -q
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp set-selector-type WP-001 "process-equipment"
python -m asbp wp set-preset WP-001 "oral-solid-dose-standard"
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task set-work-package "prepare-fat" WP-001
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection add-task TC-001 "prepare-fat"
python -m asbp wp show WP-001 --show-task-ids --show-selector-context
python -m asbp task show "prepare-fat" --show-work-package-id
python -m asbp collection show TC-001
python -m pytest -q
```

Expected:

- both pytest runs pass
- the work package can be seeded with selector type, preset, standards bundles, and scope intent
- selector context is visible through `wp show --show-selector-context`
- the task can be associated to `WP-001`
- the collection can own task membership
- WP and task read surfaces show current cross-entity visibility already exposed by the CLI

---

## Runtime notes

### Task reference resolution

Where a command accepts a task reference, resolution is:

1. exact `task_id`
2. normalized `task_key`

### Work package reference resolution

Current work package operations use exact `wp_id`.

### Current work package list surface

`wp list` currently supports:

- `--status`
- `--title`
- `--wp-id`
- `--task-id`
- `--show-task-ids`

### Current work package show surface

`wp show` currently supports:

- `--show-task-ids`
- `--show-selector-context`

### Current work package binding surface

Current selector / binding support includes:

- `wp set-selector-type <wp_id> <system_type>`
- `wp set-preset <wp_id> <preset_id>`
- `wp set-standards-bundles <wp_id> [add_on_bundle_ids...]`
- `wp set-scope-intent <wp_id> <scope_intent>`

### Current collection surface

Current collection support includes:

- `collection list`
- `collection add`
- `collection show`
- `collection update-title`
- `collection update-state`
- `collection add-task`
- `collection remove-task`

### Current task list filter and visibility surface

`task list` currently supports:

- `--status`
- `--has-dependencies`
- `--has-dependents`
- `--show-task-key`
- `--show-work-package-id`
- `--show-dependency-refs`
- `--show-dependent-refs`
- `--has-task-key`
- `--task-key`
- `--task-ref`
- `--dependency-ref`
- `--dependent-ref`
- `--work-package-id`

### Current task show visibility surface

`task show` currently supports:

- `--show-work-package-id`
- `--show-dependency-refs`
- `--show-dependent-refs`

### Current task-to-work-package surface

Current association support includes:

- `task set-work-package <task_reference> <wp_id>`
- `task clear-work-package <task_reference>`
- `task list --show-work-package-id`
- `task show --show-work-package-id`
- `task list --work-package-id <wp_id>`
- `wp show <wp_id> --show-task-ids`
- `wp list --task-id <task_id>`
- `wp list --show-task-ids`

### Planning surface status

Planning exists in core logic and tests, but there is no stabilized planning CLI surface yet.

### Current state path

The runtime uses:

```text
data/state/state.json
```

### Package version

Current CLI version string:

```text
0.1.0
```
