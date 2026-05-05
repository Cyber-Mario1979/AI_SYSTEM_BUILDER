---
doc_type: milestone_checkpoint_output
canonical_name: M15_PRESET_SELECTOR_LIBRARY_EXPANSION
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.3
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.3 — Preset / Selector Library Expansion

## Checkpoint

`M15.3` — Preset / selector library expansion

## Purpose

This document records the agreed M15.3 preset / selector expansion direction before ASBP-native library migration.

The purpose of this checkpoint output is to expand the current library coverage model first, then use that agreed coverage map as the input boundary for later governed ASBP-native implementation.

This file is checkpoint evidence only. It does not override `ROADMAP_CANONICAL.md`, `ARCHITECTURE_GUARDRAILS.md`, repo reality, or `PROGRESS_TRACKER.md`.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

The current VALOR snapshot remains candidate design/spec input only. It is not automatically ASBP execution authority.

## M15.3 allowed-work interpretation

For this checkpoint, M15.3 is interpreted as:

- expand selector / preset coverage definitions
- preserve selector context as a first-class binding seed
- avoid one-domain or one-family shortcuts disguised as general design
- define the intended selector scope matrix before migrating assets into ASBP-native governed library code

## Current snapshot baseline

The current snapshot already contains these domain/scope combinations:

| Domain | Existing selector scopes |
|---|---|
| PE — Process Equipment | `E2E`, `PV`, `POST-DEV`, `POST-CHANGE` |
| UT — Utilities | `E2E`, `QUAL`, `COMM`, `POST-DEV`, `POST-CHANGE` |
| CR — Cleanroom | `E2E`, `PV`, `QUAL`, `COMM` |
| CS — Computerized Systems legacy acronym | `E2E` |

The current user-facing Process Equipment WP header presets already include:

- `RC` — Roller Compactor
- `MILL` — Mill / milling equipment
- `BIN_BLENDER` — Bin Blender / blending equipment

Therefore these three equipment families are treated as already present in the current preset surface, not as new equipment additions.

## Naming decision

The legacy snapshot uses `CS` for two meanings:

- context selector prefix
- computerized systems domain acronym

This creates confusing IDs such as `CS-CS-E2E`.

M15.3 records this naming decision:

- `CS` remains the context-selector prefix only.
- `CSV` becomes the future canonical computerized systems domain acronym.
- legacy `CS-CS-*` IDs are treated as snapshot-era IDs only.
- future ASBP-native selector IDs for computerized systems should use `CS-CSV-*`.

Example:

| Legacy snapshot ID | Future ASBP-native canonical ID |
|---|---|
| `CS-CS-E2E` | `CS-CSV-E2E` |

## Scope token set

The expanded scope token set is:

| Scope | Meaning |
|---|---|
| `E2E` | End-to-end CQV lifecycle / new build / major project / equipment introduction |
| `PV` | Periodic verification / periodic review / periodic reclassification as applicable |
| `QUAL` | Qualification only; commissioning handled separately |
| `COMM` | Commissioning only; qualification deliverables out of scope |
| `POST-DEV` | Targeted re-qualification / retest after deviation |
| `POST-CHANGE` | Change-control requalification after controlled modification |
| `DECOM` | Decommissioning / controlled retirement / removal from GMP use |

## Decommissioning definition

`DECOM` means controlled removal, retirement, deactivation, or decommissioning of an equipment, utility, cleanroom area, or computerized system, including impact assessment, evidence preservation, safe retirement verification, and closure documentation.

Boundary rule:

- `POST-CHANGE` means the asset continues in use after modification.
- `DECOM` means the asset, area, or system is retired, removed, disabled, or taken out of GMP use.

## Target domain support matrix

| Domain | Target supported scopes |
|---|---|
| PE — Process Equipment | `E2E`, `PV`, `QUAL`, `COMM`, `POST-DEV`, `POST-CHANGE`, `DECOM` |
| UT — Utilities | `E2E`, `PV`, `QUAL`, `COMM`, `POST-DEV`, `POST-CHANGE`, `DECOM` |
| CR — Cleanroom | `E2E`, `PV`, `QUAL`, `COMM`, `POST-DEV`, `POST-CHANGE`, `DECOM` |
| CSV — Computerized Systems / CSV | `E2E`, `PV`, `POST-DEV`, `POST-CHANGE`, `DECOM` |

`CSV-COMM` and `CSV-QUAL` are intentionally deferred.

Rationale:

- CSV commissioning-only is less clean than PE/UT/CR commissioning and may overlap with technical configuration or non-GxP commissioning.
- CSV qualification-only may overlap with change-control validation and periodic validation review until the CSV rules mature.

## Missing selector records to add or define

### PE — Process Equipment

Existing:

- `CS-PE-E2E`
- `CS-PE-PV`
- `CS-PE-POST-DEV`
- `CS-PE-POST-CHANGE`

Missing:

- `CS-PE-QUAL`
- `CS-PE-COMM`
- `CS-PE-DECOM`

### UT — Utilities

Existing:

- `CS-UT-E2E`
- `CS-UT-QUAL`
- `CS-UT-COMM`
- `CS-UT-POST-DEV`
- `CS-UT-POST-CHANGE`

Missing:

- `CS-UT-PV`
- `CS-UT-DECOM`

### CR — Cleanroom

Existing:

- `CS-CR-E2E`
- `CS-CR-PV`
- `CS-CR-QUAL`
- `CS-CR-COMM`

Missing:

- `CS-CR-POST-DEV`
- `CS-CR-POST-CHANGE`
- `CS-CR-DECOM`

### CSV — Computerized Systems

Existing legacy snapshot:

- `CS-CS-E2E`

Future canonical:

- `CS-CSV-E2E`

Missing:

- `CS-CSV-PV`
- `CS-CSV-POST-DEV`
- `CS-CSV-POST-CHANGE`
- `CS-CSV-DECOM`

## Minimum CSV decommissioning requirements

`CS-CSV-DECOM` should start with a minimal requirements model and be refined later when CSV maturity increases.

Minimum coverage expectations:

- system retirement / deactivation scope
- GxP impact assessment
- data retention / archival decision
- user access shutdown or role removal confirmation
- interface / integration shutdown check
- backup / restore or final data export evidence where applicable
- audit trail / record preservation decision
- retirement approval / QA closure

## Selector binding policy for new records

New selector records should preserve the same binding pattern as existing selector records:

- selector ID and version
- applicability fields
- task pool reference
- profile reference
- calendar reference
- standards bundle reference or deterministic default-core behavior
- matching rules
- staging rules
- selector/profile/calendar/task-pool stamps

New selector definitions may name planned task pool and profile refs, but those downstream assets are not implemented in M15.3.

Downstream records must be created or expanded in later checkpoints:

- M15.4 — Task-pool expansion
- M15.5 — Calendar / standards / profile / mapping expansion

## Not in M15.3 scope

M15.3 does not implement:

- task-pool payload expansion
- profile duration expansion
- standards-bundle expansion
- calendar expansion
- mapping metadata expansion
- deployment compile pipeline
- orchestration/service hardening
- CLI commands
- AI runtime behavior
- migration into ASBP-native runtime assets beyond the selector expansion agreement

## Companion expansion map

The structured expansion map is stored as:

`docs/design_spec/valor_pack_snapshot/expansion/M15_3_SELECTOR_SCOPE_EXPANSION_MAP.yaml`

## Checkpoint decision

M15.3 records the expanded preset / selector coverage target and naming decision.

The project should not proceed to runtime migration or downstream task-pool/profile expansion until this selector/scope matrix is accepted.

## Validation note

This checkpoint package is documentation/specification-only.

No code changes are included.

`python -m pytest -q` was not run for this generated package. The latest verified validation status remains the tracker-recorded result until validation is run again.
