# ASBP Assistant Ops

Status: ACTIVE  
Scope: ASBP Product Rebuild  
Branch: product-rebuild-from-pre-pr23  
Baseline: c17b7893c6e58b8bf3b3651a0232214eb2584956  

## Purpose

This folder is the assistant operation pack for the ASBP product rebuild.

It tells any new assistant chat how to start, what to read, what not to assume, and how to avoid returning to the old governance/productization drift path.

This folder does not replace:

- `PRODUCT_BUILD_ROADMAP.md`
- repo reality
- local git output
- tests

## Required read order in a new chat

1. User-provided local git output:
   - `git branch --show-current`
   - `git log -1 --oneline`
   - `git status --short`
2. `PRODUCT_BUILD_ROADMAP.md`
3. `assistant_ops/CURRENT_STATE.md`
4. `assistant_ops/OPERATING_RULES.md`
5. `assistant_ops/SESSION_CHECKLIST.md`
6. Relevant repo files for the current step

## Current direction

Current product step after this ops pack is committed:

`P1 — Product Application Service Layer`

## Non-negotiable rule

After P0, product milestones cannot close by documents only.

Each product step must ship at least one of:

- executable code
- tests
- runnable local behavior
- generated artifact
- product UI behavior
- validated product scenario evidence
