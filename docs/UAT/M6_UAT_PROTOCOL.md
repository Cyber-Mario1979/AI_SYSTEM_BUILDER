# M6_UAT_PROTOCOL

## Milestone

Milestone 6 — Binding Context and Task Collections

## Protocol Purpose

This protocol defines the user-facing acceptance checks for the Milestone 6 boundary.

It is intended to confirm that the current Milestone 6 runtime behaves correctly for:

- collection CRUD surfaces
- task-to-collection membership behavior
- collection-state workflow handling
- selector-context binding on Work Packages
- deterministic selector visibility behavior
- deterministic failure behavior for invalid binding states

This file is a UAT protocol only.
Execution evidence and the final acceptance decision should be recorded after execution in `docs/UAT/M6_UAT_Report.md`.

## Protocol Status

Planned / ready for execution

## Validation Prerequisite

Latest validated technical baseline at protocol issue time:

- `python -m pytest -q`
- expected supporting result: `332 passed in 34.48s`

## Operator Fields

- UAT date: `12-04-2026`
- Operator: `Amr Hassan`
- Reviewer: `N/A`
- Result: `()`

## Scope Covered

The following Milestone 6 surfaces are in scope:

- `collection add <title> [--collection-state <state>]`
- `collection list [--collection-state <state>] [--title <title>] [--collection-id <id>]`
- `collection show <collection_id>`
- `collection update-title <collection_id> <title>`
- `collection update-state <collection_id> <collection_state>`
- `collection add-task <collection_id> <task_ref>`
- `collection remove-task <collection_id> <task_ref>`
- deterministic duplicate-membership rejection
- deterministic conflicting non-source membership rejection
- `wp set-selector-type <wp_id> <system_type>`
- `wp set-preset <wp_id> <preset_id>`
- `wp set-standards-bundles <wp_id> [<add_on_bundle_id> ...]`
- `wp set-scope-intent <wp_id> <scope_intent>`
- `wp show <wp_id>`
- `wp show <wp_id> --show-selector-context`
- deterministic rejection when selector seed is missing for downstream binding operations

## Test Data / Pre-Setup

Use a controlled temporary test state.
Back up the current state file before execution and restore it after execution.

Recommended pre-run backup pattern:

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force

Initialize the controlled M6 UAT state:

python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp add WP-002 "Blister line upgrade"
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task add "Execute FAT" --task-key "execute-fat"
python -m asbp collection add "Source Pool"
python -m asbp collection add "Staged Selection" --collection-state staged
python -m asbp collection add "Committed Selection" --collection-state committed

Expected collection identities after setup:

TC-001 = Source Pool
TC-002 = Staged Selection
TC-003 = Committed Selection
Acceptance Checks
UAT-M6-01 — Base collection list surface

Command:

python -m asbp collection list

Acceptance:

command succeeds
Collections: header is shown
TC-001, TC-002, and TC-003 are listed in persisted order
output remains in the established readable list format
UAT-M6-02 — Base collection show surface

Command:

python -m asbp collection show TC-001

Acceptance:

command succeeds
JSON output contains collection_id, title, collection_state, and task_ids
initial task_ids is empty before membership writes begin
UAT-M6-03 — Collection update surfaces

Commands:

python -m asbp collection update-title TC-002 "Refined Staged Selection"
python -m asbp collection update-state TC-003 refined
python -m asbp collection show TC-002
python -m asbp collection show TC-003

Acceptance:

both update commands succeed
TC-002 title is updated only
TC-003 workflow state is updated only
unrelated collections remain unchanged
UAT-M6-04 — Source collection membership attach

Commands:

python -m asbp collection add-task TC-001 prepare-fat
python -m asbp collection show TC-001

Acceptance:

attach command succeeds
output confirms TC-001 <- TASK-001
TC-001 now includes TASK-001 in task_ids
UAT-M6-05 — Source and non-source membership coexistence

Commands:

python -m asbp collection add-task TC-003 prepare-fat
python -m asbp collection show TC-001
python -m asbp collection show TC-003

Acceptance:

attach command succeeds
source membership remains preserved on TC-001
non-source membership on TC-003 is accepted alongside source membership
both collection payloads show TASK-001 correctly
UAT-M6-06 — Conflicting non-source membership rejection

Command:

python -m asbp collection add-task TC-002 prepare-fat

Acceptance:

command is rejected deterministically
output clearly states that the task is already associated with a different non-source collection
no state mutation occurs to TC-002
UAT-M6-07 — Remove membership and reattach to another non-source collection

Commands:

python -m asbp collection remove-task TC-003 prepare-fat
python -m asbp collection add-task TC-002 prepare-fat
python -m asbp collection show TC-002

Acceptance:

remove command succeeds
reattach command succeeds after the earlier non-source membership is cleared
TC-002 now includes TASK-001 in task_ids
deterministic non-source exclusivity is preserved
UAT-M6-08 — Selector type binding surface

Commands:

python -m asbp wp set-selector-type WP-001 process-equipment
python -m asbp wp show WP-001 --show-selector-context

Acceptance:

selector-type command succeeds
output confirms WP-001 -> process-equipment
opt-in selector-context output shows system_type
default wp show contract is not changed by this step alone
UAT-M6-09 — Preset binding surface

Commands:

python -m asbp wp set-preset WP-001 oral-solid-dose-standard
python -m asbp wp show WP-001 --show-selector-context

Acceptance:

preset command succeeds
output confirms WP-001 -> oral-solid-dose-standard
selector-context output now includes both system_type and preset_id
existing selector seed is preserved
UAT-M6-10 — Standards-bundle binding surface

Commands:

python -m asbp wp set-standards-bundles WP-001 automation
python -m asbp wp show WP-001 --show-selector-context

Acceptance:

standards-bundle command succeeds
output confirms WP-001 -> [cqv-core, automation]
selector-context output includes standards_bundles
cqv-core is present automatically as the baseline bundle
UAT-M6-11 — Scope / intent selector binding and visibility behavior

Commands:

python -m asbp wp set-scope-intent WP-001 post-deviation
python -m asbp wp show WP-001
python -m asbp wp show WP-001 --show-selector-context

Acceptance:

scope-intent command succeeds
output confirms WP-001 -> post-deviation
default wp show output remains unchanged and does not include selector_context
opt-in --show-selector-context output includes:
system_type
preset_id
standards_bundles
scope_intent
UAT-M6-12 — Missing selector-seed rejection for downstream binding

Commands:

python -m asbp wp set-standards-bundles WP-002 automation
python -m asbp wp set-scope-intent WP-002 post-deviation

Acceptance:

both commands are rejected deterministically
output clearly states that selector context seed must exist first
WP-002 remains unchanged
General Acceptance Decision Rule

Recommended milestone decision logic:

PASS if all protocol checks pass with no material deviation
CONDITIONAL PASS if core milestone acceptance is achieved with only minor documented deviations that do not invalidate the Milestone 6 boundary
FAIL if one or more core milestone acceptance checks fail
Post-Execution Restore

Recommended restore command after UAT execution:

Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force
Execution Notes
Record the actual execution evidence and final decision in docs/UAT/M6_UAT_Report.md
Do not advance milestone state until UAT execution is completed and recorded
Keep any deviations specific and milestone-facing, not diary-style
```
