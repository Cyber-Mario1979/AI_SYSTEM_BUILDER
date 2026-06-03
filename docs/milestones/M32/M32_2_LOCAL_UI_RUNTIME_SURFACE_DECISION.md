# M32.2 — Local UI/runtime Surface Decision

Status: Accepted in owner session  
Checkpoint: M32.2  
Mode: PLAN / decision record  
Implementation authorized: No  
Tracker movement authorized: Yes, only as alignment to M32.3  
Accepted date: 2026-06-03

## Decision

The first local workflow surface is:

CLI-enhanced controlled local workflow.

## Meaning

The user operates the first local product workflow through guided local commands, prompts, or structured local inputs.

The surface must be easier than raw internal CLI mechanics, but it remains an adapter.

## Why this surface

This is the simplest safe path because it:

- avoids web/desktop complexity during the first workflow build
- keeps execution local
- reuses existing command/runtime patterns where appropriate
- preserves approved core/service boundaries
- lets M32 prove the workflow before adding heavier UI layers

## Adapter boundary

The CLI-enhanced surface may:

- collect controlled inputs
- show available workflow choices
- show selected project/profile/source boundaries
- call approved core/service functions
- display validation and limitation messages
- guide the user to review outputs

The CLI-enhanced surface must not:

- contain domain logic
- write raw state directly
- bypass approved persistence/state helpers
- treat free-form user text as truth
- silently accept outputs
- hide source, standards, retrieval, AI, or validation limitations

## Deferred surfaces

The following are deferred:

- local web UI
- desktop-like UI
- controlled browser forms
- SaaS/admin/customer surfaces

## AI boundary

No new AI behavior is authorized by M32.2.

If AI appears later in M32, it remains optional local/offline draft support only and human-review-required.

## Validation

No pytest is required for this decision record because no executable behavior changes.

Tests are required if later checkpoints change code, commands, imports, runtime behavior, schemas, validators, loaders, adapters, or persistence behavior.

## Acceptance record

The project owner accepted the CLI-enhanced controlled local workflow surface decision in session on 2026-06-03.

## Next checkpoint

M32.3 — UI-to-core adapter implementation.

M32.3 requires separate GO authorization before implementation.
