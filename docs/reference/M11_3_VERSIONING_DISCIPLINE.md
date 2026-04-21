# M11_3_VERSIONING_DISCIPLINE

## Status

Active reference for `M11.3` — Versioning discipline.

## Purpose

Define the minimum versioning discipline for the current Phase 4 roadmap window.

This checkpoint does not introduce packaging or release automation.

It establishes one canonical version source, one state-version rule, and one explicit release-state signal.

## Canonical version source

The canonical version source is:

`asbp/versioning.py`

This file is now the single source of truth for:

- runtime version
- state-init version
- release-state signal

## Current versioning rules

### Rule 1 — Runtime version is centralized

The CLI/runtime version must come from `asbp/versioning.py`.

No other module should hard-code the runtime version string directly.

### Rule 2 — State-init version is centralized

New state initialization must use the centralized state version from `asbp/versioning.py`.

For the current roadmap window, the local rule is:

- `STATE_VERSION = RUNTIME_VERSION`

This keeps runtime version and initial persisted state version aligned until a later checkpoint intentionally separates runtime-version and schema-version concerns.

### Rule 3 — Release-state signaling is explicit

The current release-state signal is stored in `asbp/versioning.py`.

This checkpoint introduces explicit release-state signaling in code without changing the existing CLI `--version` output contract.

The current release-state value is:

- `active_development`

### Rule 4 — One-file version bump expectation

A version bump in the current roadmap window should update:

- `asbp/versioning.py`

Then the full regression baseline must be run:

```powershell
python -m pytest -q
```

## Why M11.3 does not change CLI version output

The current local decision for this checkpoint is:

- keep CLI `--version` output stable
- centralize versioning discipline first
- avoid unnecessary user-facing contract drift in the same slice

This keeps the checkpoint narrow and production-safe.

## Future versioning extension note

A later checkpoint may intentionally introduce stricter separation between:

- runtime version
- persisted state/schema version
- release/build metadata
- package/distribution version

That separation is not required in `M11.3`.

## M11.3 checkpoint output

This checkpoint establishes:

- one canonical version source file
- one centralized runtime version rule
- one centralized state-init version rule
- one explicit release-state signal
- one-file version bump discipline for the current roadmap window
