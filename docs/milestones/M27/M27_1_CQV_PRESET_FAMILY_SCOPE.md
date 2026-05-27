---
doc_type: milestone_decision_record
canonical_name: M27_1_CQV_PRESET_FAMILY_SCOPE
status: ACTIVE_SCOPE
milestone: M27
checkpoint: M27.1
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
checkpoint_title: CQV preset family scope
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: feature/m27-cqv-source-content-expansion
created_date: 2026-05-26
last_updated_date: 2026-05-26
application_mode: user_applied_package
live_repo_write: NO
---

# M27.1 — CQV Preset Family Scope

## Purpose

This artifact defines the initial CQV preset family scope for the local integrated CQV product core.

It starts M27 by defining the controlled preset families that will later connect to selectors, task pools, profiles, calendars, planning basis, duration references, and mappings.

This checkpoint defines scope only. It does not implement executable runtime-authoritative library content.

## Roadmap Alignment

M27 is the execution lane for CQV source content expansion.

M27.1 is limited to defining the initial preset families.

The controlled initial preset families are:

- Cleanroom
- Process Equipment
- QC Lab Equipment
- Utilities
- Computerized Systems
- Manual Fallback

QC Lab Equipment is included as a bounded equipment-class preset family because GMP laboratory instruments and QC laboratory equipment require different downstream selector, profile, task-pool, calibration, and CSV-linkage handling from manufacturing process equipment.

M27.1 must not create unlimited preset sprawl.

## Source Boundary Basis

M26 locked Presets as an included authored source family inside the local CQV product MVP boundary.

M27.1 does not reopen whether Presets belong in the product source boundary.

M27.1 only defines the first controlled preset-family scope so later M27 checkpoints can harden selectors, task pools, profiles, calendars, planning basis, duration references, and mappings against known preset families.

## Preset Family Scope Table

| Preset Family ID | Display Name | Intended Use | Allowed Asset / System Types | Explicitly Excluded Scope |
|---|---|---|---|---|
| `PF-CLEANROOM` | Cleanroom | Entry point for cleanroom, controlled area, and HVAC-related qualification package context. | Cleanrooms, controlled areas, HVAC zones, classified rooms, area qualification contexts. | Process-equipment-only qualification, QC-lab-equipment-only qualification, utility-only qualification, computerized-system validation as the primary scope. |
| `PF-PROCESS-EQUIPMENT` | Process Equipment | Entry point for manufacturing/process equipment qualification package context. | Manufacturing equipment, packaging equipment, process skids, standalone GMP process equipment, equipment qualification contexts. | Area/HVAC-only qualification, QC laboratory instruments as the primary scope, pure utility-system qualification, computerized-system-only validation as the primary scope. |
| `PF-QC-LAB-EQUIPMENT` | QC Lab Equipment | Entry point for QC laboratory equipment and laboratory instrument qualification package context. | GMP QC laboratory instruments, analytical instruments, balances, incubators, HPLC/GC systems as equipment contexts, dissolution testers, TOC/pH/conductivity instruments, temperature-controlled laboratory equipment, standalone lab equipment requiring qualification/calibration/CSV linkage. | Manufacturing process equipment as the primary scope, area/HVAC-only qualification, utility-system-only qualification, computerized-system-only validation where the software/system is the primary scope rather than the laboratory equipment or instrument. |
| `PF-UTILITIES` | Utilities | Entry point for utility system qualification package context. | GMP utilities, clean utilities, black utilities where qualification is required, distribution systems, generation systems, utility qualification contexts. | Cleanroom-only area qualification, process-equipment-only qualification, QC-lab-equipment-only qualification, computerized-system-only validation as the primary scope. |
| `PF-COMPUTERIZED-SYSTEMS` | Computerized Systems | Entry point for computerized system validation or computerized-system qualification context. | GxP computerized systems, automation systems, control systems, software-supported GMP workflows, CSV-relevant system contexts. | Physical equipment/area/utility qualification when computerized-system validation is not the primary scope. |
| `PF-MANUAL-FALLBACK` | Manual Fallback | Controlled fallback when no specific preset family is mature enough or applicable yet. | Transitional CQV planning cases, early intake, temporary manual classification, unsupported or mixed contexts requiring user confirmation. | Permanent substitute for defined preset families, bypass of selector hardening, uncontrolled custom presets. |

## Family-Level Rules

1. Preset families are controlled package/context selection inputs.
2. Preset families are not persisted tasks.
3. Preset families are not task pools.
4. Preset families are not profiles.
5. Preset families are not standards bundles.
6. Preset families are not document templates.
7. Preset families do not generate work by themselves.
8. Preset families must route into selector and scope-intent logic before task-pool selection.
9. QC Lab Equipment is separated from Process Equipment to avoid forcing analytical/laboratory qualification logic into manufacturing-equipment routing.
10. The Manual Fallback family is temporary and controlled; it must not become a silent expansion path.
11. New preset-family inclusion requires a later explicit Project Owner decision or roadmap-authorized checkpoint.

## Downstream Selector Expectations

M27.2 must harden selector and scope-intent behavior using these preset families as controlled inputs.

Selector behavior must consider, at minimum:

- preset family;
- asset/system type;
- lifecycle event;
- qualification or validation intent;
- GMP impact and operating context where approved;
- laboratory/QC role where applicable;
- risk or complexity where approved;
- standards bundle or standards applicability where available;
- user intent or manual confirmation where needed.

Work selection means the controlled routing decision that determines which downstream work package path, candidate task-pool family, profile class, planning basis, and document expectations may apply.

Work selection must not depend on preset family alone.

## Downstream Task-Pool Expectations

M27.3 must define authoritative task-pool records separately from preset families.

Preset families may help select candidate task-pool families, but task-pool source records must remain separate and must define their own:

- atomic task IDs;
- dependencies;
- owner/role expectations;
- duration references;
- prerequisites;
- document links.

Persisted project tasks must not be treated as preset or task-pool source truth.

## Downstream Profile Expectations

M27.4 must define profile records separately from preset families.

Preset families may identify the expected profile class, but profiles must carry the actual area, equipment, utility, system, laboratory instrument, qualification, or validation context.

## Downstream Calendar and Planning Expectations

M27.5 and M27.6 must define calendar, work-time, planning basis, and duration logic separately from preset families.

Preset families must not hide regional assumptions, working-day assumptions, duration estimates, or planning-basis rules.

## Downstream Mapping Expectations

M27.7 must define mappings between preset families and downstream source families.

Expected mapping relationships include:

- preset family to selector model;
- preset family to profile class;
- selector to task-pool family;
- preset/profile/selector to standards bundle where authority exists;
- task family to document family where later M29 authority exists;
- planning basis and duration references where later M27 checkpoints define them.

## Not Completed / Not Claimed

M27.1 does not claim completion of:

- selector and scope-intent hardening;
- authoritative task-pool records;
- profile records;
- calendar records;
- planning-basis records;
- duration-reference records;
- mapping records;
- executable runtime-authoritative library loading;
- compiled lookup generation;
- runtime lookup behavior;
- cross-library validation;
- source-to-execution compatibility validation;
- product-ready document templates;
- document generation;
- rendering, export, or reporting behavior;
- standards embedding or retrieval;
- AI/model/provider behavior;
- UI/API behavior;
- productization, SaaS, deployment, or commercial readiness.

## DDR Impact

M27.1 touches DDR-001 and DDR-002 at preset-family scope level only.

M27.1 has DDR-009 awareness because later UI/API or external contract behavior may consume preset families through approved adapters.

M27.1 does not close, reopen, downgrade, or reclassify any DDR.

M27.1 does not implement runtime lookup, compiled lookup, productized placeholder-backed behavior, UI/API behavior, document generation, standards retrieval, AI/runtime behavior, or productization behavior.

## Acceptance Criteria

M27.1 is acceptable when this artifact confirms:

- initial preset families are defined and bounded;
- Cleanroom, Process Equipment, QC Lab Equipment, Utilities, Computerized Systems, and Manual Fallback are the first controlled preset families;
- each preset family has an intended use and explicit exclusions;
- QC Lab Equipment is bounded as a distinct laboratory equipment/instrument preset family rather than hidden under manufacturing Process Equipment;
- Manual Fallback is controlled and cannot become unlimited preset sprawl;
- preset families are separated from selectors, task pools, profiles, calendars, planning basis, duration references, mappings, standards bundles, and document templates;
- M27.2 can proceed to selector and scope-intent model hardening without reopening preset-family scope.

## Validation Expectation

This is a documentation/governance/source-scope artifact only.

No executable validation is required unless a separate change modifies code, commands, imports, schemas, tests, runtime behavior, CLI behavior, or executable contracts.

## Handoff to M27.2

M27.2 must harden selector and scope-intent behavior using the preset families defined here.

M27.2 must not reopen the initial preset-family list unless the Project Owner explicitly authorizes a scope change.
