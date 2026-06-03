# M32.1 — Full Local Workflow Scope Lock

Status: Accepted in owner session  
Checkpoint: M32.1  
Mode: PLAN / governance-only  
Implementation authorized: No  
Tracker movement authorized: Yes, only as alignment to M32.2  
Accepted date: 2026-06-03

## Purpose

Lock the first local ASBP workflow scope before choosing or building the UI.

M32.1 does not implement UI, runtime behavior, document generation, AI behavior, retrieval behavior, or product readiness.

## First workflow scope

The first local workflow will let the user:

1. Create or select a local CQV project.
2. Select an approved workflow/profile/source boundary.
3. Enter controlled inputs.
4. Stage tasks or planning inputs.
5. Move toward a document/output review path.
6. See limitations before accepting anything.
7. Review outputs manually before acceptance.

## Included

- Local project/workspace selection
- Controlled input path
- Preset/profile/source selection
- Task or planning staging
- Document/output review path
- Human review gates
- Visible limitations
- Safe error/failure visibility

## Excluded

- SaaS
- cloud-first workflow
- deployment
- commercialization
- customer-ready output
- product-ready claims
- autonomous AI
- AI approval authority
- raw free-form input as truth
- retrieval as source authority

## AI boundary

AI may be included later only as optional local/offline draft support.

AI output must remain human-review-required.

Normal tests must not require Ollama or a live model.

## Architecture boundary

UI/CLI/local workflow surfaces are adapters only.

Domain behavior must stay in approved core/service boundaries.

## DDR boundary

DDR-001, DDR-002, DDR-005, DDR-006, DDR-007, and DDR-009 are carried forward as limitations.

No dependency is closed by this record.

## Acceptance record

The project owner accepted this simplified M32.1 scope record in session on 2026-06-03.

## Next checkpoint

M32.2 — Local UI/runtime surface decision.
