---
doc_type: remediation_coverage_matrix
canonical_name: M29_CQV_CONTENT_LIBRARY_COVERAGE_MATRIX
status: READY_FOR_OWNER_REVIEW_REVISED
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 1 — Coverage matrix and MVP scope lock
execution_mode: Governance-only
application_mode: user_applied_package
live_repo_write: NO
source_authority_note: Owner decisions plus repo-backed blocker/remediation evidence
---

# M29 — CQV Content Library Coverage Matrix

## 1. Purpose

This document defines the revised Wave 1 MVP scope lock for the M29.12 CQV content-library completion blocker.

Wave 1 does not implement source JSON, code, tests, task pools, templates, schemas, or runtime behavior.

Wave 1 only locks the intended MVP content scope so that the next remediation waves can return to build/content work without reopening the same scope debate repeatedly.

## 2. Owner Decisions Captured

The following Project Owner decisions are captured as the Wave 1 scope baseline:

1. M29.12 UAT remains blocked until CQV content-library completion is sufficiently remediated or explicitly carried forward.
2. Decommissioning must be included. It was not considered in the previous draft and is a real gap.
3. QC laboratory equipment / lab equipment is P0, not P1.
4. Document families must be derived from the concrete must-have document list, not vague generic families.
5. DQ / design qualification / design review is not a low-priority optional afterthought for qualification lifecycles. For new installation or design-relevant qualification routes, it is P0 or conditionally P0.
6. Process equipment must be split into named equipment archetypes / preset candidates, not treated as one vague domain.
7. Utilities must be split into priority utility systems. The detailed P0 utility systems are:
   - Compressed Air System
   - Purified / Refined Water System
   - HVAC System
   - Chilled Water System
8. Other utility systems remain in scope as general-first or later-detail systems unless elevated by owner decision:
   - Steam System
   - Hot Water System
   - Vacuum System
   - Nitrogen System
   - Drainage System
   - Electrical Power System
9. EMS and BMS are not treated as standalone utility splits in this matrix. They are treated as room / cleanroom / HVAC supporting systems where relevant.
10. The uploaded deployment/work-package preset file is used only as an equipment/utility name source. It is not used as work-package authority, task logic, source-code authority, or architecture authority.
11. Codes from the uploaded preset file must not be used in the MVP matrix. Human-readable asset names are used instead.
12. Vertical Granulator is the correct name. It must not be called Vacuum Granulator.

## 3. Architecture Interpretation for Wave 1

The scope matrix defines asset archetypes, utility systems, lifecycle routes, and document coverage needs.

It does not assign Work Packages directly to equipment.

Current Wave 1 architecture interpretation:

- Equipment / utility entries are content coverage targets and preset candidates.
- Work Packages remain execution objects or workflow instances, not content-library source truth in this document.
- Task pools, profiles, mappings, templates, schemas, and validation assets will be expanded in later build/content waves.
- If later architecture requires Work Package assignment by equipment archetype, that must be decided during the relevant source-to-execution mapping or workflow implementation wave, not silently introduced here.

## 4. Priority Definitions

| Priority | Meaning |
|---|---|
| P0 | Must be covered for the approved MVP CQV content-library baseline before M29.12 owner acceptance may resume, unless explicitly carried by owner decision. |
| P1 | Important but may follow P0 if the owner accepts a staged MVP boundary. |
| P2 | Later enhancement or non-MVP scope. |
| General-first | Included at parent/general level now, with detailed subtype expansion deferred unless owner elevates it. |
| TBD | Requires owner decision before being marked included, excluded, or carried. |

## 5. MVP Domain Classification

| Domain / route | MVP status | Priority | Notes |
|---|---:|---:|---|
| Cleanroom / HVAC qualification | Included | P0 | Includes classified rooms, controlled rooms, cleanroom/HVAC qualification logic, and room/HVAC supporting systems. EMS/BMS are handled here as supporting systems where relevant. |
| Process equipment qualification | Included | P0 | Must be split into named equipment archetypes / preset candidates. Not a single vague bucket. |
| Utilities qualification | Included | P0 | Parent domain included. Detailed P0 systems are compressed air, purified/refined water, HVAC, and chilled water. |
| Computerized system validation / CSV | Included | P0 | Required for local CQV product MVP because CSV is already represented in existing M29 document/output paths. |
| QC laboratory equipment / calibration linkage | Included | P0 | Elevated to P0 by owner decision. |
| Decommissioning | Included | P0 | Must be represented as lifecycle route / document route across relevant asset classes. Document set requires owner finalization. |
| Manual fallback / unsupported-scope routing | Included as safety route | P0 | Must remain a controlled fallback, not a substitute for missing real libraries. |
| Full all-CQV universe | Excluded from MVP | P2 | The MVP must avoid infinite scope. Later expansion can add more asset families. |

## 6. Process Equipment Archetype Scope

The following are included as Process Equipment P0 archetypes / preset candidates for content-library expansion:

| Process equipment archetype | MVP status | Priority | Notes |
|---|---:|---:|---|
| Tablet Compression Machine | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Pan Coater | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Capsule Filling Machine | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Bin Blender | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Vertical Granulator | Included | P0 | Correct name. Must not be called Vacuum Granulator. |
| Fluid Bed Dryer | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Roller Compactor | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Blister Line | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Tablet Sorter | Included | P0 | Requires task-pool, document, template, and schema coverage. |
| Mill | Included | P0 | Requires task-pool, document, template, and schema coverage. |

## 7. Utilities System Scope

| Utility system | MVP status | Priority | Notes |
|---|---:|---:|---|
| Compressed Air System | Detailed included | P0 | Must receive detailed task/template/schema coverage. |
| Purified / Refined Water System | Detailed included | P0 | Must receive detailed task/template/schema coverage. Sampling points and performance/PQ logic must not be treated as later by default. |
| HVAC System | Detailed included | P0 | Must receive detailed task/template/schema coverage. Connect to Cleanroom/HVAC domain where appropriate. |
| Chilled Water System | Detailed included | P0 | Must receive detailed task/template/schema coverage. |
| Steam System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |
| Hot Water System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |
| Vacuum System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |
| Nitrogen System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |
| Drainage System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |
| Electrical Power System | General-first | P1 | Included as general utility coverage; detailed expansion can follow unless owner elevates. |

## 8. Must-Have Document List Grouped into Families

This grouping is for planning and content-library coverage. The individual document names below remain the controlling must-have list for MVP coverage.

### 8.1 Change / validation planning / strategy family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| CCF — Change Control Form | Must-have | P0 | Required to represent controlled change initiation / change context. |
| VMP — Validation Master Plan | Must-have | P0 | Required planning/governance document. |
| SIA — System Impact Assessment | Must-have | P0 | Required impact classification / routing input. |
| QP — Qualification Plan | Must-have | P0 | Existing starter template record is not enough; real body/section coverage required. |
| CP — Commissioning Plan | Must-have | P0 | Must be represented in commissioning path. |

### 8.2 Requirements / design / risk / traceability family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| URS | Must-have | P0 | Must be supported as real document family, not just field text. |
| Vendor Docs | Must-have as extraction source | P0 | No authored template required, but data extraction from FDS/SDS and vendor documents is needed for RTM and downstream documents. |
| RA / FMEA | Must-have | P0 | Risk / FMEA basis must be represented. |
| URS Deviation List | Must-have | P0 | Required to track URS deviations. |
| RTM — Requirements Traceability Matrix | Must-have | P0 | Requires inputs from URS, vendor documents, specifications, and test documents. |
| DQ — Design Qualification / Design Review | Must-have / conditionally must-have | P0 | Required for new installation/design-relevant qualification routes. Must not be treated as low-priority by default. |

### 8.3 Vendor testing / construction / commissioning turnover family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| FAT Protocol / Report | Must-have as vendor-provided / flow-stated | P0 | For equipment where FAT applies. Needed for correct end-to-end flow. |
| A0 Certificate — FAT Completion | Must-have for equipment where applicable | P0 | Equipment-only where FAT completion applies. |
| CTOP — Construction Turnover Package | Must-have for construction routes | P0 | Construction-only route. |
| A1 Certificate — Mechanical Completion | Must-have for construction routes | P0 | Construction-only route. |
| SAT Protocol / Report | Must-have as vendor/site testing flow | P0 | Vendor/site-provided where applicable. |
| CR — Commissioning Report | Must-have | P0 | Required to close commissioning evidence. |
| A2 Certificate — Commissioning Completion | Must-have | P0 | Required to represent commissioning completion. |

### 8.4 Qualification execution family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| IQ Protocol and Report | Must-have | P0 | Required for qualification execution routes. |
| OQ Protocol and Report | Must-have | P0 | Required for qualification execution routes. |
| PQ Protocol and Report | Must-have / conditionally must-have | P0 | Required where PQ/performance verification is in scope. Must not be downgraded generically. |

### 8.5 Deviation / CAPA / closeout family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| Deviation Report / Incident Report | Must-have | P0 | Required to represent deviations/incidents in execution. |
| CAPA Closure Form | Must-have | P0 | Required when CAPA route is triggered. |
| VSR — Validation Summary Report | Must-have | P0 | Required closeout / summary report. |

### 8.6 Decommissioning family

| Document | MVP status | Priority | Notes |
|---|---:|---:|---|
| Decommissioning document set | Required scope gap | P0 | Decommissioning is included as a lifecycle route. Exact document list must be finalized by owner before this route can be marked complete. Candidate documents must not be silently invented as approved MVP documents. |

## 9. High-Level Coverage Matrix

| Area | Current repo status | MVP required state | Gap status | Assigned wave |
|---|---|---|---|---|
| Process equipment archetypes | Starter task pools exist, but process equipment is not expanded to all approved archetypes. | P0 archetype coverage for listed process equipment. | Partial | Wave 2 |
| Utility systems | Starter utility task pool exists at parent level. Detailed P0 utility systems not sufficiently split. | Detailed P0 coverage for compressed air, purified/refined water, HVAC, chilled water. General-first coverage for remaining utilities. | Partial | Wave 2 / Wave 3 |
| QC lab equipment | Starter profile/task coverage exists but owner classifies lab equipment as P0. | P0 lab equipment coverage with calibration linkage and CSV linkage. | Partial | Wave 2 / Wave 3 |
| Cleanroom/HVAC | Starter task/profile coverage exists. | P0 detailed domain coverage with room/HVAC/EMS/BMS support where relevant. | Partial | Wave 2 / Wave 3 |
| CSV / computerized systems | Starter CSV flow exists. | P0 CSV document/task/schema coverage. | Partial | Wave 2 / Wave 5 |
| Decommissioning | Not covered in previous matrix. | P0 lifecycle route and document route coverage. | Missing | Wave 2 / Wave 4 / Wave 5 |
| Task pools | Starter task pools exist. | Expanded MVP task pools by domain/subdomain/archetype/lifecycle. | Partial | Wave 2 |
| Profiles | Starter context profiles exist. | MVP profiles with explicit context fields and human-confirmation controls. | Partial | Wave 3 |
| Calendars | Starter calendars exist. | MVP calendar assumptions explicit; user/site assumptions visible. | Partial | Wave 3 |
| Planning basis / durations | Starter estimates exist. | MVP duration refs for expanded task pools; no dangling refs. | Partial | Wave 3 |
| Mappings | Starter mappings exist. Many document expectations remain future/partial. | Resolved mapping coverage to document/template/schema references where approved. | Partial | Wave 3 / Wave 4 / Wave 5 |
| Document template records | Two starter template records exist. | Template coverage for must-have document list. | Major gap | Wave 4 |
| Document template bodies / section plans | Not complete. | Real body/section structures for must-have documents. | Major gap | Wave 4 |
| Document input schemas / DCF | QP and CSV starter schemas exist. | Schemas and DCF/min-input mappings for must-have document list. | Major gap | Wave 5 |
| Controlled drafting modes | Drafting modes exist. | Modes mapped to expanded templates/schemas and document outputs. | Partial | Wave 5 / Wave 7 |
| Standards / citation | Limited standards registry/bundles exist. | Standards/citation linkage where approved, with limitations visible. | Partial | Wave 6 |
| Renderer/output | Markdown and CSV summary supported; DOCX/PDF/Excel blocked. | MVP output format decision required. Markdown/CSV may remain MVP if owner accepts; DOCX/PDF later unless elevated. | Partial / decision needed | Wave 7 / Return gate |
| Trial scenarios | Two local trial scenarios exist. | Expanded trial scenarios matching MVP domains and document families. | Major gap | Wave 7 |
| UAT return | M29.12 blocked. | Return only after coverage matrix status is implemented/closed/carried and owner accepts return. | Blocked | Wave 8 |

## 10. Gap-to-Wave Mapping

| Gap | Required action | Wave |
|---|---|---|
| Process equipment archetype task coverage | Expand task pools for listed archetypes. | Wave 2 |
| P0 utilities detailed coverage | Expand utility task pools and related document expectations for compressed air, purified/refined water, HVAC, chilled water. | Wave 2 |
| QC lab equipment P0 coverage | Expand lab equipment/calibration/CSV-link task pools and mappings. | Wave 2 / Wave 3 |
| Decommissioning missing route | Add decommissioning lifecycle/task/document/schema route. | Wave 2 / Wave 4 / Wave 5 |
| Vague document family taxonomy | Replace generic families with must-have document list and grouped families. | Wave 4 / Wave 5 |
| Template body absence | Add template body/section-plan sources. | Wave 4 |
| Schema/DCF incompleteness | Add schemas and DCF mappings for must-have document list. | Wave 5 |
| Vendor document extraction need | Define vendor-document extraction source contracts for FDS/SDS/vendor docs feeding RTM. | Wave 5 |
| Standards/citation limitations | Expand only where approved; preserve limits. | Wave 6 |
| Trial scenario insufficiency | Expand trial scenarios to match MVP coverage. | Wave 7 |
| UAT return criteria | Validate and owner-approve return to M29.12. | Wave 8 |

## 11. Return-to-UAT Criteria

M29.12 UAT may resume only when all are true:

1. This coverage matrix is owner-reviewed and accepted as the Wave 1 scope lock.
2. P0 domains and lifecycle routes are either implemented or explicitly carried with owner approval.
3. P0 document families are either implemented as source templates/schemas or explicitly carried with owner approval.
4. Task pools, profiles, mappings, templates, schemas, standards links, renderer decisions, and trial scenarios validate for the approved MVP scope.
5. Required validation passes after any source JSON, code, model, validator, schema, test, mapping, or runtime behavior changes.
6. Remaining limitations are visible and recorded.
7. The Project Owner explicitly approves return to M29.12 UAT.
8. M29.13 remains blocked until M29.12 acceptance is actually recorded.

## 12. Explicit Non-Implementation Claims

This Wave 1 coverage matrix does not:

- implement library expansion;
- modify source JSON;
- modify code;
- update tests;
- update tracker;
- accept M29.12;
- close M29;
- claim full CQV content-library completion;
- claim product-ready document-factory completion;
- authorize productization, deployment, release, or SaaS readiness.

## 13. Next Allowed Work After Owner Acceptance of This Matrix

After owner acceptance of this revised Wave 1 matrix, the next allowed remediation work is:

`Wave 2 — Task-pool expansion`

Wave 2 must be build/content work and must update source data/tests/validation as applicable. It must not be another governance-only loop for the same scope.
