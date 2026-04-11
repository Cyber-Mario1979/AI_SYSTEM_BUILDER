# smoke_test_M6_7C_standards_bundle_binding

## Purpose

Focused smoke test for `M6.7C — Standards-bundle binding direction`.

This smoke test checks that standards bundles are now part of deterministic bound context on the Work Package selector context, with `cqv-core` acting as the default baseline bundle and add-ons remaining explicit.

## Scope

This protocol verifies:

- `wp set-standards-bundles <wp_id> [<add_on_bundle> ...]` persists standards bundle binding on the target Work Package
- `cqv-core` is included automatically as the baseline bundle
- existing selector seed fields remain preserved
- `wp show <wp_id>` preserves the default read contract and does **not** show `selector_context`
- `wp show <wp_id> --show-selector-context` shows standards bundle binding correctly
- non-target Work Packages remain unchanged

## Pre-conditions

- run from repo root
- virtual environment active
- current implementation already validated locally before smoke execution

## Backup

```powershell
$backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_Smoke_Backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force


## Controlled setup
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp add WP-002 "Blister line upgrade"
python -m asbp wp set-selector-type WP-001 process-equipment
python -m asbp wp set-preset WP-001 oral-solid-dose-standard

##Execution

- Step 1 — Bind standards bundles on target Work Package
python -m asbp wp set-standards-bundles WP-001 automation

Expected result:

Work Package standards bundles updated: WP-001 -> [cqv-core, automation]


- Step 2 — Verify default wp show contract is unchanged
python -m asbp wp show WP-001

Expected result:

{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open"
}


- Step 3 — Verify opt-in selector visibility shows standards binding
python -m asbp wp show WP-001 --show-selector-context

Expected result:

{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "selector_context": {
    "system_type": "process-equipment",
    "preset_id": "oral-solid-dose-standard",
    "standards_bundles": [
      "cqv-core",
      "automation"
    ]
  }
}


- Step 4 — Verify second Work Package is unchanged
python -m asbp wp show WP-002 --show-selector-context

Expected result:

{
  "wp_id": "WP-002",
  "title": "Blister line upgrade",
  "status": "open",
  "selector_context": null
}


- Step 5 — Verify persisted state structure
Get-Content .\data\state\state.json

Expected result:

WP-001 contains:

"selector_context": {
  "system_type": "process-equipment",
  "preset_id": "oral-solid-dose-standard",
  "standards_bundles": [
    "cqv-core",
    "automation"
  ]
}

WP-002 does not contain a persisted selector_context block.

Pass criteria

Smoke test passes if all of the following are true:

standards bundle binding succeeds on WP-001
cqv-core is included automatically
existing selector seed fields remain preserved
default wp show output remains unchanged
opt-in selector visibility works correctly
non-target Work Package remains unchanged
persisted state matches the expected selective storage behavior


# Restore

Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force

# Notes

This is a lightweight smoke test only.

It supports confidence in the M6.7C surface and does not replace:

milestone validation
milestone UAT
milestone closeout

```
