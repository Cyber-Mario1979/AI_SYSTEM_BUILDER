---
doc_type: remediation_coverage_matrix
canonical_name: M29_CQV_CONTENT_LIBRARY_COVERAGE_MATRIX
status: WAVE_1_SCOPE_LOCK_READY_FOR_OWNER_USE
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker
remediation_wave: Wave 1 — Coverage matrix and MVP scope lock
execution_mode: Governance-only
application_mode: user_applied_package
live_repo_write: NO
tracker_movement: NO
next_wave_after_acceptance: Wave 2 — Task-pool expansion
---

# M29 — CQV Content Library Coverage Matrix

## Purpose

This document completes CQV content-library remediation Wave 1.

It locks the MVP coverage decision surface needed to prevent M29.12 UAT from being accepted against starter-only CQV content. It does not implement library expansion, source JSON changes, code changes, tests, tracker movement, M29.12 acceptance, or M29.13 closeout.

This document is intentionally limited to six outputs:

1. Define MVP scope.
2. Classify included / excluded domains.
3. Classify document families.
4. Create the coverage matrix.
5. Map gaps to remediation waves.
6. Define return-to-UAT criteria.

After this document is applied and accepted by the Project Owner, the next normal remediation action is Wave 2 build/content work: task-pool and source-library expansion. This document must not create a new open-ended governance loop.

## Current Control State

- Latest completed checkpoint: `M29.11 — Validation checkpoint`
- Active checkpoint: `M29.12 — Milestone UAT / owner acceptance`
- Active M29.12 status: `BLOCKED`
- Active blocker: `M29.12 CQV Content Library Completion Blocker`
- Latest validation: `python -m pytest -q — 1416 passed in 44.97s`
- M29.13 closeout: blocked while the M29.12 content-library blocker remains active

## 1. MVP Scope Definition

The MVP scope is the minimum CQV content-library scope required before M29.12 owner acceptance can reasonably resume.

The MVP does not mean all possible CQV work, all industries, all equipment types, all regions, all standards, all client templates, or all document formats. It means a controlled local CQV product baseline sufficient to prove that the document/output factory is not merely an engine skeleton with starter samples.

## 2. Domain Classification

| Domain | MVP decision | Priority | Rationale | Required next work |
|---|---|---:|---|---|
| Cleanroom / HVAC qualification | Included | P0 | Existing starter task pool/profile/trial relevance and strong local CQV relevance. | Expand cleanroom/HVAC task pool, profile fields, mappings, templates, schemas, standards linkage, and trial scenario. |
| Process equipment qualification | Included | P0 | Existing process-equipment E2E task pool and general CQV applicability. | Expand IQ/OQ/PQ depth, readiness, risk, summary, template/schema coverage. |
| Utilities qualification | Included | P0 | Existing utilities task pool and common CQV workflow relevance. | Expand utility-specific IQ/OQ/PQ/sampling paths, planning basis, and document templates. |
| Computerized system validation | Included | P0 | Existing CSV baseline task pool and CSV validation plan template/schema path. | Expand URS/risk/spec/trace/testing/access/data-integrity document coverage. |
| QC laboratory equipment qualification / calibration linkage | Included | P1 | Existing starter coverage exists, but it can remain shallower than P0 domains for first remediation pass. | Expand qualification/calibration/CSV-linkage task and document coverage enough for local trial. |
| Manual fallback / unsupported-scope routing | Included as safety boundary | P0 safety | Required to prevent unsupported cases from being silently treated as mature source-library coverage. | Maintain route assessment, manual confirmation, temporary plan, and source-expansion review records. |
| Sterile/aseptic process-specific validation | Later enhancement | Later | Too broad for first MVP; needs separate domain-specific scope. | Explicitly excluded from MVP unless owner reclassifies. |
| Warehouse/cold-chain/temperature-mapping depth | Later enhancement | Later | Not covered by current source files as a mature domain. | Defer to later library expansion. |
| Water/steam/gas utility deep sampling libraries | Later enhancement | Later | Utilities are included, but detailed utility-specific sampling libraries are not first-pass MVP. | Add later expansion after utility baseline proves route. |
| MES/ERP/LIMS deep system-specific CSV packs | Later enhancement | Later | CSV baseline is included, but individual system-family packs are not first-pass MVP. | Add later CSV specialty waves. |

## 3. Document-Family Classification

| Document family | MVP decision | Priority | Required coverage for MVP |
|---|---|---:|---|
| URS / requirements basis | Included | P0 | Required for process equipment, QC lab, CSV, and where user requirements drive qualification scope. |
| Risk / impact assessment | Included | P0 | Required as source rationale for scope, testing depth, GxP impact, and CSV/data-integrity decisions. |
| Qualification Plan | Included | P0 | Must be real template/body/section-plan coverage, not only a template registry record. |
| CSV Validation Plan | Included | P0 | Must be real template/body/section-plan coverage, not only a starter record. |
| DQ / design review record | Conditional MVP | P1 | Required where design/readiness evidence is material; may be sectioned into readiness/design review first. |
| IQ protocol / IQ report | Included | P0 | Required for process equipment, utilities, cleanroom/HVAC installation readiness, and QC lab equipment as applicable. |
| OQ protocol / OQ report | Included | P0 | Required for process equipment, utilities, cleanroom/HVAC operational tests, and QC lab equipment as applicable. |
| PQ / performance verification / sampling report | Included where applicable | P0 | Required for process equipment, utilities, cleanroom/HVAC performance, or sampling-based utility verification where scope requires. |
| Traceability matrix | Included | P0 for CSV, P1 for other CQV | Required for CSV; can be lightweight trace basis for other CQV domains in first pass. |
| Readiness / turnover checklist | Included | P0 | Required to connect task readiness evidence to document workflow. |
| Execution report family | Included | P0 | Required to avoid plans-only output. Must preserve deviations, results, limits, and review points. |
| Summary report | Included | P0 | Required for package closeout. |
| Route decision / fallback assessment record | Included | P0 safety | Required for manual fallback / unsupported routing. |
| Full formal SOP set | Later enhancement | Later | Out of MVP unless owner explicitly scopes it. |
| Full eQMS approval package / e-signature record | Excluded | Out | Not M29 remediation scope; must not be claimed. |

## 4. Coverage Matrix

Status legend:

- `Covered for engine test` — sufficient for deterministic tests only, not content maturity.
- `Starter only` — source exists but is intentionally starter/baseline.
- `Partial` — some usable coverage exists but not enough for MVP acceptance.
- `Missing` — no adequate controlled source coverage exists.
- `Blocked` — cannot be treated as accepted until remediation or owner-approved carry-forward.
- `Later enhancement` — intentionally out of first MVP.

| Area | Current repo state | MVP status | Required remediation wave |
|---|---|---|---|
| Task pools | Starter task-pool records exist for process equipment, QC lab, cleanroom/HVAC, utilities, CSV, and manual fallback. | Starter only | Wave 2 |
| Task dependencies / owner roles | Basic dependency and owner-role structures exist. | Partial | Wave 2 |
| Task-to-document expectations | Many document expectations are future expected rather than resolved real document outputs. | Blocked | Waves 2, 4, 5 |
| Profiles | Starter profile records exist for main candidate domains. | Starter only | Wave 3 |
| Profile context fields | Human-input fields exist, but not mature product profile coverage. | Partial | Wave 3 |
| Calendars | Starter Cairo/user-defined calendar records exist. | Starter only | Wave 3 |
| Holidays / shutdowns | User-supplied and unverified holiday handling exists. | Partial | Wave 3 |
| Planning basis / durations | Starter estimates exist, human confirmation required. | Starter only | Wave 3 |
| Mappings | Starter mappings exist for preset-to-profile, selector-to-task-pool, task-to-document, standards-to-template. | Starter only / partial | Wave 3 |
| Document template records | Only QP and CSV validation plan template records exist. | Blocked | Wave 4 |
| Document template bodies / section plans | No mature template body/section-plan library for the MVP document set. | Missing | Wave 4 |
| Document input schemas | QP and CSV validation plan schemas exist only. | Partial / blocked | Wave 5 |
| DCF / skip-DCF coverage | DCF and skip-DCF routes exist for QP/CSV only. | Partial | Wave 5 |
| Controlled drafting modes | Four modes exist as bounded draft-packet controls. | Covered for engine test | Wave 4/5 integration as needed |
| Standards registry | Standards registry v0.1 exists with many pending/TBD records. | Partial | Wave 6 |
| Standards bundles | CQV GMP and CSV/GxP bundles exist with visible limitations. | Partial | Wave 6 |
| Standards citation depth | Document-level mostly; clause/requirement depth limited or blocked by source status. | Partial / blocked for rich claims | Wave 6 |
| Renderer formats | Markdown and CSV summary supported; DOCX/PDF/Excel blocked. | Partial | Later unless MVP requires DOCX/PDF now |
| Lifecycle/workflow | Lifecycle records and transitions exist. | Covered for engine test | Validate during Waves 7/8 |
| Output validation | Output validation exists for current renderer artifacts. | Covered for engine test | Expand with new artifacts in Waves 7/8 |
| Trial scenarios | Two local trial scenarios exist: QP and CSV. | Starter only | Wave 7 |
| UAT evidence | M29.12 not accepted; blocker active. | Blocked | Wave 8 |

## 5. Gap-to-Wave Mapping

| Gap group | Description | Wave | Completion condition |
|---|---|---:|---|
| G1 | Task-pool depth and document expectation resolution | Wave 2 | MVP domains have expanded task pools with no dangling duration/document refs. |
| G2 | Profiles, calendar, planning basis, and mappings maturity | Wave 3 | Source-to-execution routing validates across MVP scope. |
| G3 | Real document template body / section-plan coverage | Wave 4 | MVP document families have versioned template bodies/section plans. |
| G4 | Input schemas, DCF, skip-DCF, and field/section bindings | Wave 5 | Every MVP template has controlled input schema and intake route mapping. |
| G5 | Standards/citation applicability depth where approved | Wave 6 | Standards limitations remain visible; no invented clause or mandatory claims. |
| G6 | Trial scenario expansion | Wave 7 | Trial scenarios cover MVP domains/document families sufficiently for owner review. |
| G7 | Integrated validation and return-to-UAT gate | Wave 8 | Tests pass, coverage matrix is closed/carried, owner approves M29.12 return. |

## 6. Return-to-UAT Criteria

M29.12 UAT may resume only when all of the following are true:

1. This coverage matrix is accepted by the Project Owner as the current MVP scope lock.
2. All P0 MVP domains are either implemented to MVP source/content depth or explicitly carried forward by owner-approved decision.
3. All P0 MVP document families have either real controlled template/body/schema coverage or explicit owner-approved carry-forward status.
4. Source JSON, schema, mapping, validation, and trial scenario changes from remediation waves are applied and validated.
5. `python -m pytest -q` passes after source/content/code/test changes.
6. The active M29.12 blocker is updated to closed or owner-approved carry-forward.
7. Tracker, DDR, and milestone evidence state the remaining limitations truthfully.
8. The Project Owner explicitly approves returning to M29.12 UAT.

## Non-Infinite-Scope Control

This matrix is intended to prevent endless scope expansion.

Once accepted, Wave 2 begins with the included MVP scope above. New domains or document families may be added only by explicit Project Owner decision and must not silently delay the first MVP completion path.

## Next Allowed Work After Wave 1

The next allowed remediation work after this matrix is accepted is:

`Wave 2 — Task-pool expansion`

Wave 2 is build/content work and is expected to update or add source JSON and tests where source contracts change.

## Explicit Non-Implementation Claims

This coverage matrix does not:

- implement task-pool expansion;
- implement profile/calendar/planning-basis/mapping expansion;
- implement document template body expansion;
- implement document input schema or DCF expansion;
- implement standards/citation expansion;
- implement trial scenario expansion;
- update source JSON;
- update code;
- update tests;
- update tracker;
- accept M29.12;
- close M29;
- authorize productization, deployment, release, or SaaS readiness.
