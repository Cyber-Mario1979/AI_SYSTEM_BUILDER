---
id: 16_Valor_ID_Numbering_Spec
version: v1
status: released
summary: Canonical ID numbering and allocation rules for WPs and tasks (Canvas-only source of truth).
dependencies:
  - 02_Orchestration_Core.md
authority: supporting
---

# Valor ID Numbering Spec

## Purpose
Eliminate blank and duplicate IDs; prevent presets from overriding existing IDs.

## Critical Rule — Ignore Example IDs

IDs that appear inside:
- few-shot examples,
- templates,
- the golden runtime log,
- documentation samples,

**must never** be treated as “already used” for the current session.

Only IDs that exist in the **active Canvas objects** count as “in use” (not chat previews or examples).

## Source of Truth — Canvas Only

- Each Work Package is stored in its **own** Canvas object titled `Work Package WP###`.
- When allocating new IDs, scan **Canvas objects only** (Work Package and Task records rendered in Canvas).
- **Do not** scan the chat transcript for IDs.
- If Canvas is empty or not accessible, assume **no IDs exist** unless the user explicitly provides an existing ID to continue.

## WP ID Initialization (New Session)

### Testing note
- A “fresh session” means **a new chat with an empty Canvas** (no existing WP objects). In the same chat, additional `Create WP` calls will naturally produce `WP002`, `WP003`, etc.

- If **no** Work Package exists in the active session/canvas: the first created WP **must** be `WP001`.
- Otherwise: the next WP ID is `max(existing_WP_numbers) + 1` (monotonic; do not backfill gaps).


## Algorithm
1. **Scan existing IDs in Canvas** (source of truth):
   - WP IDs `WPxxx`
   - Task IDs `WPxxx-Txxx` (per-WP scope)
   - Ignore any IDs appearing in chat text, examples, templates, or logs.
2. **Determine the next available integer** for each class (global for WPs; per-WP for tasks; per-DocType for documents).
3. **Never reuse deleted IDs** within the project/session scope (mandated uniqueness).
4. **On `Load Preset <Code> Scope=<SCOPE>`** (pack-canonical behavior):
   - ORCH MUST allocate a **new** WP ID via `Create WP` / `WP_CREATE` and create a new Canvas titled `Work Package WP###`.
   - Then bind/import the preset header/context into **that new WP** (do **not** overwrite another WP canvas).
   - No tasks are preloaded; stage later from the bound Task Pool via `Stage Tasks <WP###>`, then write tasks only with `Commit Tasks <WP###> [<indices>]`.
5. **On Task Creation**:
   - Use `WPxxx-T###` numbering; allocate next available `T###` within that WP.
6. **On Document Creation**:
   - Use `<DocType>-###` scheme; allocate next per-DocType number; do not collide with existing docs.
   - Examples: `URS-001`, `DQ-001`, `IQP-001`, `VSR-001`, `DEV-001`, `CAPA-001`.

## Enforcement
- **Reject** any operation that would produce a blank or duplicate ID.
- **Warn and block** if a preset import attempts to write into an ID already allocated to another WP.
- **State Echo** should include the IDs in use after any create/edit (at minimum the affected WP/task/doc IDs).
