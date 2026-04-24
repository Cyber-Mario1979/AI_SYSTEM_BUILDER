---
doc_type: runtime_cheat_sheet
canonical_name: ASBP_RUNTIME_CHEAT_SHEET
status: ACTIVE
governs_execution: false
document_state_mode: repo_aligned_convenience_reference
authority: non_authoritative_operator_reference
scope_type: runtime_command_surface
---

# ASBP Runtime Cheat Sheet

Non-authoritative convenience snapshot aligned to the current repo boundary.

Source of truth remains:

- repo code
- `ROADMAP_CANONICAL.md`
- active `ROADMAP_ADDENDUM_*.md` files when present
- `ARCHITECTURE_GUARDRAILS.md`
- `PROGRESS_TRACKER.md`

---

## Current execution context

- Current phase: **Phase 4 closeout to Phase 5 transition window**
- Current milestone: **Post-M11 transition under Addendum 07**
- Current approved slice family: **`A07.4` — Public-surface and export-surface audit**
- Latest completed checkpoint: **`A07.3` — README and runtime/operator-document normalization completed**
- Exact next unfinished checkpoint: **`A07.4` — Public-surface and export-surface audit**
- Milestone UAT status: **`PASSED`**
- Latest verified validation status: **`python -m pytest -q` → `524 passed in 45.65s`**

---

## Important scope note

This cheat sheet separates two kinds of public surfaces that now coexist in the repo:

1. **stable operator CLI surfaces**
2. **validated public Python package surfaces** introduced through the M11 boundary

Because the architecture guardrails keep the CLI as an adapter only, not every validated public surface is primarily exposed as an operator-first CLI workflow.

The public Python examples below are curated examples of the package boundary, not an exhaustive export inventory.

---

## Base entry

```powershell
python -m asbp
```

## Global

```powershell
python -m asbp --version
```

Version metadata in repo code:

```text
runtime_version = 0.1.0
state_version = 0.1.0
release_state = active_development
```

---

## Stable CLI surfaces

### State commands

#### Initialize state file

```powershell
python -m asbp state init
```

#### Show current state

```powershell
python -m asbp state show
```

#### Set state version

```powershell
python -m asbp state set-version <value>
```

Example:

```powershell
python -m asbp state set-version 0.1.0
```

#### Set state status

Allowed values:

- `not_started`
- `in_flight`
- `completed`

```powershell
python -m asbp state set-status <value>
```

Example:

```powershell
python -m asbp state set-status in_flight
```

---

### Work Package commands

#### Add work package

```powershell
python -m asbp wp add <wp_id> "<title>"
```

Example:

```powershell
python -m asbp wp add WP-001 "Tablet press qualification"
```

#### Show work package

```powershell
python -m asbp wp show <wp_id> [--show-task-ids] [--show-selector-context] [--show-collection-ids]
```

Examples:

```powershell
python -m asbp wp show WP-001
python -m asbp wp show WP-001 --show-task-ids
python -m asbp wp show WP-001 --show-selector-context
python -m asbp wp show WP-001 --show-selector-context --show-collection-ids
```

#### List work packages

```powershell
python -m asbp wp list [--status <value>] [--title "<value>"] [--wp-id <value>] [--task-id <value>] [--collection-id <value>] [--show-task-ids] [--show-collection-ids]
```

Allowed `--status` values:

- `open`
- `in_progress`
- `completed`

Useful examples:

```powershell
python -m asbp wp list
python -m asbp wp list --status open
python -m asbp wp list --wp-id WP-001
python -m asbp wp list --task-id TASK-001
python -m asbp wp list --collection-id TC-001
python -m asbp wp list --show-task-ids
python -m asbp wp list --show-collection-ids
```

#### Update work package title

```powershell
python -m asbp wp update-title <wp_id> "<new_title>"
```

#### Update work package status

Allowed values:

- `open`
- `in_progress`
- `completed`

```powershell
python -m asbp wp update-status <wp_id> <status>
```

#### Delete work package

```powershell
python -m asbp wp delete <wp_id>
```

#### Set selector type

```powershell
python -m asbp wp set-selector-type <wp_id> "<system_type>"
```

Example:

```powershell
python -m asbp wp set-selector-type WP-001 "process-equipment"
```

#### Set preset

```powershell
python -m asbp wp set-preset <wp_id> "<preset_id>"
```

Example:

```powershell
python -m asbp wp set-preset WP-001 "oral-solid-dose-standard"
```

#### Set standards bundles

CLI accepts add-on bundle IDs and persists `cqv-core` as the baseline bundle.

Allowed add-on bundle values:

- `cleanroom-hvac`
- `automation`

```powershell
python -m asbp wp set-standards-bundles <wp_id> [add_on_bundle_id_1] [add_on_bundle_id_2]
```

Examples:

```powershell
python -m asbp wp set-standards-bundles WP-001
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-standards-bundles WP-001 cleanroom-hvac automation
```

#### Set scope intent

Allowed values:

- `end-to-end`
- `qualification-only`
- `commissioning-only`
- `periodic-verification`
- `post-change`
- `post-deviation`

```powershell
python -m asbp wp set-scope-intent <wp_id> <scope_intent>
```

Examples:

```powershell
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp wp set-scope-intent WP-001 end-to-end
```

---

### Collection commands

#### Add collection

```powershell
python -m asbp collection add "<title>" [--collection-state <value>]
```

Allowed `--collection-state` values:

- `source`
- `staged`
- `committed`
- `refined`

Examples:

```powershell
python -m asbp collection add "Source Pool"
python -m asbp collection add "Committed Selection" --collection-state committed
```

#### List collections

```powershell
python -m asbp collection list [--collection-state <value>] [--title "<value>"] [--collection-id <value>] [--work-package-id <wp_id>] [--task-id <task_id>] [--show-work-package-id] [--show-task-ids]
```

Examples:

```powershell
python -m asbp collection list
python -m asbp collection list --collection-state committed
python -m asbp collection list --work-package-id WP-001 --show-work-package-id
python -m asbp collection list --task-id TASK-001 --show-task-ids
```

#### Show collection

```powershell
python -m asbp collection show <collection_id> [--show-work-package-id]
```

Examples:

```powershell
python -m asbp collection show TC-001
python -m asbp collection show TC-001 --show-work-package-id
```

#### Update collection title

```powershell
python -m asbp collection update-title <collection_id> "<new_title>"
```

#### Update collection state

```powershell
python -m asbp collection update-state <collection_id> <collection_state>
```

#### Add task to collection

Task reference resolves by exact `task_id` first, then normalized `task_key`.

```powershell
python -m asbp collection add-task <collection_id> <task_reference>
```

#### Remove task from collection

Task reference resolves by exact `task_id` first, then normalized `task_key`.

```powershell
python -m asbp collection remove-task <collection_id> <task_reference>
```

#### Set collection work package

```powershell
python -m asbp collection set-work-package <collection_id> <wp_id>
```

#### Clear collection work package

```powershell
python -m asbp collection clear-work-package <collection_id>
```

---

### Task commands

#### Add task

```powershell
python -m asbp task add "<title>" [--description "<text>"] [--owner "<name>"] [--duration <days>] [--start-date "<yyyy-mm-dd>"] [--end-date "<yyyy-mm-dd>"] [--task-key "<key>"]
```

Example:

```powershell
python -m asbp task add "Prepare FAT" --description "Draft FAT package" --owner "Amr" --duration 3 --start-date "2026-03-31" --end-date "2026-04-02" --task-key "prepare-fat"
```

#### List tasks

```powershell
python -m asbp task list [--status <value>] [--has-dependencies true|false] [--has-dependents true|false] [--show-task-key] [--show-work-package-id] [--show-dependency-refs] [--show-dependent-refs] [--has-task-key true|false] [--task-key "<value>"] [--task-ref "<value>"] [--dependency-ref "<value>"] [--dependent-ref "<value>"] [--work-package-id <wp_id>]
```

Allowed `--status` values:

- `planned`
- `in_progress`
- `completed`
- `over_due`

Useful examples:

```powershell
python -m asbp task list
python -m asbp task list --show-task-key
python -m asbp task list --show-work-package-id
python -m asbp task list --status completed
python -m asbp task list --has-dependencies true
python -m asbp task list --task-key "prepare-fat" --show-task-key
python -m asbp task list --task-ref "TASK-001" --show-task-key
python -m asbp task list --dependency-ref "execute-fat" --show-task-key
python -m asbp task list --dependent-ref "review-fat-package" --show-task-key
python -m asbp task list --work-package-id WP-001 --show-task-key --show-work-package-id
```

#### Show task

Target resolves by exact `task_id` first, then normalized `task_key`.

```powershell
python -m asbp task show <task_reference> [--show-work-package-id] [--show-dependency-refs] [--show-dependent-refs]
```

Examples:

```powershell
python -m asbp task show TASK-001
python -m asbp task show "prepare-fat"
python -m asbp task show "prepare-fat" --show-work-package-id
python -m asbp task show "review-fat-package" --show-work-package-id --show-dependency-refs --show-dependent-refs
```

#### Set task key

```powershell
python -m asbp task set-key <task_reference> "<new_task_key>"
```

#### Clear task key

```powershell
python -m asbp task clear-key <task_reference>
```

#### Update task status

Allowed values:

- `planned`
- `in_progress`
- `completed`
- `over_due`

```powershell
python -m asbp task update-status <task_reference> <status>
```

#### Set task dependencies

Each dependency input resolves by exact `task_id` first, then normalized `task_key`, while persisted dependency storage remains `task_id`-based.

```powershell
python -m asbp task set-dependencies <task_reference> [dependency_1] [dependency_2] [...]
```

#### Set task work package

```powershell
python -m asbp task set-work-package <task_reference> <wp_id>
```

#### Clear task work package

```powershell
python -m asbp task clear-work-package <task_reference>
```

#### Delete task

```powershell
python -m asbp task delete <task_reference>
```

---

## Verified public Python package surfaces

These are repo-real public surfaces and part of the accepted M11 boundary. They are useful for operator/developer inspection and controlled inline execution.

### Versioning

```powershell
@'
from asbp.versioning import (
    RELEASE_STATE,
    RUNTIME_VERSION,
    STATE_VERSION,
    build_version_metadata,
)

print(build_version_metadata())
print(RUNTIME_VERSION)
print(STATE_VERSION)
print(RELEASE_STATE)
'@ | python -
```

### Retrieval

```powershell
@'
from asbp.retrieval import (
    build_governed_retrieval_request,
    build_probabilistic_search_retrieval_request,
    build_retrieval_architecture_baseline,
)

print(build_retrieval_architecture_baseline())
print(
    build_governed_retrieval_request(
        artifact_kind="task_pool",
        lookup_id="POOL-TABPRESS-001",
        compiled_surface_id="compiled-task-pools-v1",
        library_version="2026.04",
    )
)
print(
    build_probabilistic_search_retrieval_request(
        query_text="tablet press FAT",
        search_scope="uat_notes",
    )
)
'@ | python -
```

### Runtime

```powershell
@'
from asbp.runtime import (
    build_work_package_runtime_boundary_payload,
    build_work_package_prompt_contract_payload,
    build_work_package_llm_handoff_payload,
    build_work_package_generation_request_payload,
)
from asbp.state_model import WorkPackageModel

work_packages = [
    WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
    )
]

print(
    build_work_package_runtime_boundary_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )
)
print(
    build_work_package_prompt_contract_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )
)
print(
    build_work_package_llm_handoff_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )
)
print(
    build_work_package_generation_request_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )
)
'@ | python -
```

---

## Minimal current runtime verification flow

```powershell
python -m pytest -q
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp set-selector-type WP-001 process-equipment
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp set-scope-intent WP-001 qualification-only
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task set-work-package "prepare-fat" WP-001
python -m asbp collection add "Committed Selection" --collection-state committed
python -m asbp collection set-work-package TC-001 WP-001
python -m asbp collection add-task TC-001 "prepare-fat"
python -m asbp wp show WP-001 --show-selector-context --show-collection-ids
python -m asbp collection show TC-001 --show-work-package-id
python -m asbp task show "prepare-fat" --show-work-package-id
python -m pytest -q
```

Expected:

- both pytest runs pass
- the Work Package can be seeded with selector type, preset, standards bundles, and scope intent
- the task can be associated to `WP-001`
- the collection can be bound to `WP-001`
- cross-entity read surfaces reflect the current deterministic state

---

## Runtime notes

### Task reference resolution

Where a command accepts a task reference, resolution is:

1. exact `task_id`
2. normalized `task_key`

### Work package reference resolution

Current Work Package operations use exact `wp_id`.

### Collection reference resolution

Current collection operations use exact `collection_id`.

### Planning surface status

Planning entities and validation exist in repo reality, but a fully stabilized operator-first CLI planning workflow is not the main public runtime surface at this boundary.

### Current state path

```text
data/state/state.json
```

### Why this cheat sheet does not guess extra runtime CLI spellings

The repo now includes validated runtime package surfaces beyond the older CRUD-style CLI framing. This cheat sheet documents:

- stable CLI surfaces that are already operator-usable
- curated public Python package surfaces that are validated and supported

It intentionally does not invent or rename additional operator commands that are not yet documented as a stabilized operator contract.
