# smoke_test_M6_7B_preset_binding_seed

## Purpose

Focused smoke test for `M6.7B — Preset-first binding direction`.

This smoke test checks that preset binding seed behavior is now explicit on Work Package selector context without introducing a standalone preset system.

## Scope

This protocol verifies:

- `wp set-preset <wp_id> <preset_id>` persists preset binding seed on the target Work Package
- `wp set-preset` preserves an already-set `selector_context.system_type`
- `wp show <wp_id>` preserves the default read contract and does **not** show `selector_context`
- `wp show <wp_id> --show-selector-context` shows `preset_id` cleanly without null nested fields
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
```

## Controlled setup

```powershell
python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp wp add WP-002 "Blister line upgrade"
python -m asbp wp set-selector-type WP-001 process-equipment
```

## Execution

### Step 1 — Set preset binding seed on target Work Package

```powershell
python -m asbp wp set-preset WP-001 oral-solid-dose-standard
```

Expected result:

```text
Work Package preset updated: WP-001 -> oral-solid-dose-standard
```

### Step 2 — Verify default `wp show` contract is unchanged

```powershell
python -m asbp wp show WP-001
```

Expected result:

```json
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open"
}
```

### Step 3 — Verify opt-in selector visibility shows both binding seeds

```powershell
python -m asbp wp show WP-001 --show-selector-context
```

Expected result:

```json
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "selector_context": {
    "system_type": "process-equipment",
    "preset_id": "oral-solid-dose-standard"
  }
}
```

### Step 4 — Verify second Work Package is unchanged

```powershell
python -m asbp wp show WP-002 --show-selector-context
```

Expected result:

```json
{
  "wp_id": "WP-002",
  "title": "Blister line upgrade",
  "status": "open",
  "selector_context": null
}
```

### Step 5 — Verify persisted state structure

```powershell
Get-Content .\data\state\state.json
```

Expected result:

`WP-001` contains:

```json
"selector_context": {
  "system_type": "process-equipment",
  "preset_id": "oral-solid-dose-standard"
}
```

`WP-002` does **not** contain a persisted `selector_context` block.

## Pass criteria

Smoke test passes if all of the following are true:

- preset binding seed update succeeds on `WP-001`
- existing selector type is preserved
- default `wp show` output remains unchanged
- opt-in selector visibility works correctly
- non-target Work Package remains unchanged
- persisted state matches the expected selective storage behavior

## Restore

```powershell
Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force
```

## Notes

This is a lightweight smoke test only.

It supports confidence in the `M6.7B` surface and does not replace:

- milestone validation
- milestone UAT
- milestone closeout

```

```
