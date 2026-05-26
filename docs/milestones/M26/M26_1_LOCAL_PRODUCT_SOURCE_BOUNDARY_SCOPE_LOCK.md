---
doc_type: milestone_decision_record
canonical_name: M26_1_LOCAL_PRODUCT_SOURCE_BOUNDARY_SCOPE_LOCK
status: ACTIVE_LOCK
milestone: M26
checkpoint: M26.1
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
checkpoint_title: Local product source-boundary scope lock
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: feature/m26-cqv-source-authority
live_repo_write: YES
created_date: 2026-05-26
---

# M26.1 — Local Product Source-Boundary Scope Lock

## Purpose

This artifact is the single M26.1 decision lock.

It defines the local CQV product MVP source boundary and removes ambiguity before source taxonomy, package layout, promotion model, validation contracts, registry modeling, lookup adapter work, and CQV source expansion proceed.

This artifact is not a discussion note, not a placeholder, not a product-readiness claim, and not an implementation package.

## Checkpoint Authority

M26.1 locks three things:

1. Which CQV asset families are inside the local MVP source boundary.
2. Which role each family plays as authored source, controlled reference, generated runtime artifact, or excluded execution scope for this checkpoint.
3. Which direct roadmap checkpoint receives the next action for each family.

After this checkpoint, the included source families are no longer open questions unless a formal change-control decision changes the boundary.

## Core Decision

The local integrated CQV product MVP includes governed CQV source families as first-class product assets.

Task Pools, Profiles, Calendars, Presets, Selectors, Planning Basis, Duration References, Mappings, CQV Libraries, Standards Bundle references, Document Template family boundaries, Document Factory input boundaries, and Export/Report source families are inside the product source boundary.

M26.1 does not populate their full content. It locks them into the product boundary so M26 can define authority controls and M27 can expand the CQV source content without reopening the inclusion question.

## Source Family Boundary Table

| Source family | Boundary decision | MVP source role | Direct action route |
|---|---|---|---|
| CQV Libraries | Included | Authored source family for controlled CQV knowledge assets | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Task Pools | Included | Authored source family for CQV activity libraries by domain, asset, and workflow context | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Profiles | Included | Authored source family for equipment, process, utility, area, and system context profiles | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Calendars | Included | Authored source family for work calendars and scheduling basis | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Presets | Included | Authored source family for controlled package/context selection inputs | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Selectors | Included | Authored source family for deterministic source and workflow selection controls | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Planning Basis | Included | Authored source family for planning assumptions, duration classes, and scheduling basis | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Duration References | Included | Authored source family for controlled duration references and planning estimates | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Mappings | Included | Authored source family for cross-family links among profiles, task pools, standards references, templates, planning basis, and workflow context | M26.2 taxonomy; M26.3 layout; M27 content expansion |
| Standards Bundles | Included as controlled references | Registry-linked references, not embedded retrieval authority | M26.2 taxonomy; M26.3 layout; M28 standards consumption |
| Standards Source Registry references | Included as controlled references | Controlled standard/source/citation reference authority | M26.2 taxonomy; M28 standards consumption |
| Document Template Families | Included as source-family boundary | Governed template-family identity and selection boundary, not product-ready templates in M26.1 | M26.2 taxonomy; M29 document factory |
| Document Factory Inputs | Included as source-family boundary | DCF/intake/source input boundary, not product-ready generation in M26.1 | M26.2 taxonomy; M29 document factory |
| Export/Report Source Families | Included as source-family boundary | Controlled reporting/export source definitions and contexts, not rendering in M26.1 | M26.2 taxonomy; M29 output/rendering |
| Compiled Runtime Lookup | Generated artifact, not source truth | Runtime artifact generated from authored sources under controlled promotion | M26.4 promotion model; M26.7 lookup boundary; M26.8 primitives |
| Retrieval Indexes | Excluded from M26.1 execution | Helper artifacts only after source authority exists | M30 governed retrieval/indexing |
| AI Runtime Inputs | Excluded from M26.1 execution | Governed context consumer, not source authority | M31 governed AI assistance |
| UI/API Product Surfaces | Excluded from M26.1 execution | Adapter/product-surface consumer, not source authority | M32 local workflow/UI MVP |

## M26.1 Execution Exclusions

The following work is not performed in M26.1:

- writing full task-pool rows
- writing full profile records
- writing full calendar records
- writing full preset records
- writing full selector records
- writing full planning-basis records
- writing full mapping records
- generating compiled lookup files
- implementing runtime lookup access
- implementing validation schemas
- implementing product-ready document templates
- generating product-ready documents
- rendering documents, reports, exports, or dashboards
- implementing standards embedding or retrieval
- implementing AI/model/provider behavior
- implementing UI/API behavior

These exclusions protect checkpoint order. They do not remove the included source families from the MVP boundary.

## Direct M27 Expansion Mandate

M27 must expand the included CQV source content for the included families that require authored content:

- CQV Libraries
- Task Pools
- Profiles
- Calendars
- Presets
- Selectors
- Planning Basis
- Duration References
- Mappings

M27 must not reopen whether these families belong in the MVP source boundary. That question is locked by M26.1.

## Source Role Model

| Source role | Meaning | Source families |
|---|---|---|
| Authored source | Human-controlled canonical source data maintained as product source truth | CQV Libraries, Task Pools, Profiles, Calendars, Presets, Selectors, Planning Basis, Duration References, Mappings |
| Controlled reference | Governed reference into an approved authority model; not copied into uncontrolled runtime behavior | Standards Bundles, Standards Source Registry references |
| Source-family boundary | Product source family recognized at boundary level, with content execution governed by its roadmap checkpoint | Document Template Families, Document Factory Inputs, Export/Report Source Families |
| Generated runtime artifact | Derived artifact produced from authored sources through controlled promotion; not source truth | Compiled Runtime Lookup |
| Consumer surface | Uses governed source authority but cannot define it | Retrieval Indexes, AI Runtime Inputs, UI/API Product Surfaces |

## Runtime Authority Rule

Authored source families can become runtime-authoritative only through M26 authority controls:

- taxonomy
- package/layout control
- authored-source to compiled-runtime promotion model
- validation contracts
- source registry model
- runtime lookup adapter boundary
- implementation primitives
- validation evidence
- owner acceptance where applicable

No scattered document, note, table, draft, chat output, generated file, or support artifact becomes runtime authority by being mentioned here.

## DDR Impact

### DDR-001 — Governed-library runtime promotion / deployment-compiled lookup

M26.1 directly touches DDR-001 because it defines which source families can enter the runtime-authority path.

DDR-001 remains closed only for its approved governance/model scope. This artifact does not implement runtime migration, deployment-compiled lookup generation, runtime lookup implementation, or productized library dependence.

M26.1 satisfies the boundary prerequisite for M26 source-authority work by naming the included authored source families and identifying compiled runtime lookup as generated artifact, not source truth.

### DDR-002 — Consolidated runtime-authoritative libraries

M26.1 directly touches DDR-002 because it defines which source families are part of the consolidated product source boundary.

DDR-002 remains closed only for its approved governance/model scope. This artifact does not implement consolidated library package layout, version/status fields, cross-library validation, or runtime lookup behavior.

M26.1 satisfies the boundary prerequisite for M26/M27 by locking the included product source families and preventing scattered drafts from becoming runtime authority.

### DDR-003 — Product-ready document templates library

M26.1 carries DDR-003 awareness by including Document Template Families as a source-family boundary.

This artifact does not implement template files, template loading, template selection, schema binding, or product-ready document generation.

### DDR-004 — Standards source registry and citation authority

M26.1 carries DDR-004 awareness by including Standards Bundles and Standards Source Registry references as controlled reference families.

This artifact does not implement executable registry consumption, standards-backed runtime behavior, standards embedding, or retrieval.

### DDR-006 — Product-ready document/export/report generation and rendering

M26.1 carries DDR-006 awareness by including Document Factory Inputs and Export/Report Source Families as source-family boundaries.

This artifact does not implement product-ready generation, rendering, export, reporting, artifact metadata, or output acceptance behavior.

## Boundary Rules

1. Included source families are in the local CQV MVP boundary.
2. Included source families must receive taxonomy and source identity in M26.2.
3. Included authored source families must receive package/layout placement in M26.3.
4. Included authored source families must use controlled promotion before runtime use.
5. Compiled runtime lookup is generated from authored source and cannot become source truth.
6. Retrieval, AI, UI, and API layers consume governed source authority and cannot define it.
7. Product-ready document/output behavior remains blocked until its dedicated document factory and rendering evidence exists.
8. Standards-backed runtime use remains controlled by the standards registry and its dedicated roadmap checkpoint.
9. No productization, SaaS, deployment, or live/local AI runtime claim is created by this artifact.
10. No additional source family is added to the local MVP boundary without change control.

## M26.2 Handoff

M26.2 must define authoritative source taxonomy for the included families listed in this artifact.

M26.2 must produce canonical family names, identity rules, and source-family definitions for:

- CQV Libraries
- Task Pools
- Profiles
- Calendars
- Presets
- Selectors
- Planning Basis
- Duration References
- Mappings
- Standards Bundles
- Standards Source Registry references
- Document Template Families
- Document Factory Inputs
- Export/Report Source Families
- Compiled Runtime Lookup

M26.2 must not treat scattered documents as runtime authority.

## Acceptance Criteria

M26.1 is complete when this artifact is present in the repository and confirms:

- The local CQV MVP source boundary is locked.
- Task Pools, Profiles, Calendars, Presets, Selectors, Planning Basis, Duration References, Mappings, and CQV Libraries are included.
- Document Template Families, Document Factory Inputs, and Export/Report Source Families are recognized as source-family boundaries without product-ready execution in M26.1.
- Standards Bundles and Standards Source Registry references are included as controlled references.
- Compiled Runtime Lookup is classified as generated runtime artifact, not authored source truth.
- Retrieval, AI runtime, and UI/API are classified as consumer surfaces, not source authority.
- DDR-001 and DDR-002 are directly addressed at boundary level.
- DDR-003, DDR-004, and DDR-006 are carried as awareness dependencies without unauthorized implementation.
- M26.2 can proceed to authoritative source taxonomy without reopening source-family inclusion.
- M27 content expansion has a direct, locked set of included authored source families.

## Validation Expectation

This is a documentation/governance checkpoint artifact only.

No executable validation is required unless a separate change modifies code, commands, imports, schemas, tests, runtime behavior, CLI behavior, or executable contracts.

## Live Write Source Lock

This artifact was created by live repository write authorization for this exact action only.

Authorization scope:

- create and commit only this M26.1 single artifact
- branch: `feature/m26-cqv-source-authority`
- do not continue beyond M26.1

No standing live-write authorization remains after this artifact creation.
