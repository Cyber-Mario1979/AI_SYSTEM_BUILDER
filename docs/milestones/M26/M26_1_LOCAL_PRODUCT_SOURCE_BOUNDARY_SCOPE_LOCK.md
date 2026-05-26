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
last_updated_date: 2026-05-26
---

# M26.1 — Local Product Source-Boundary Scope Lock

## Purpose

This is the single M26 authority lock.

Its purpose is to keep M26 small and prevent a document series from delaying CQV library work.

It locks the local CQV product MVP source boundary at high level only, so source expansion can proceed as implementation/content work rather than more planning paperwork.

## Compression Decision

M26 is compressed into this single authority artifact.

No separate M26.2, M26.3, M26.4, M26.5, M26.6, or M26.7 artifact is required unless the Project Owner explicitly requests one.

M26 does not populate CQV source content.

M27 is the execution lane for CQV library/content expansion.

## Locked MVP Source Families

The following source families are inside the local CQV product MVP boundary:

| Source family | Boundary decision | Product role |
|---|---|---|
| CQV Libraries | Included | Canonical CQV knowledge/source content |
| Task Pools | Included | CQV execution activity content by asset, system, area, and workflow context |
| Profiles | Included | Equipment, process, utility, area, and system context records |
| Calendars | Included | Work calendars and scheduling basis |
| Presets | Included | Controlled package/context selection inputs |
| Selectors | Included | Deterministic source and workflow selection controls |
| Planning Basis | Included | Planning assumptions and duration logic |
| Duration References | Included | Controlled duration references and estimates |
| Mappings | Included | Links across profiles, task pools, standards references, templates, planning basis, and workflow context |
| Standards Bundles | Included as controlled references | Registry-linked standards reference groupings |
| Standards Source Registry references | Included as controlled references | Controlled standard/source/citation reference authority |
| Document Template Families | Included as boundary only | Template-family identity and selection boundary |
| Document Factory Inputs | Included as boundary only | DCF/intake/input boundary |
| Export/Report Source Families | Included as boundary only | Reporting/export source context boundary |
| Compiled Runtime Lookup | Generated artifact only | Derived runtime artifact, never authored source truth |
| Retrieval Indexes | Consumer/helper only | Uses governed source authority; does not define it |
| AI Runtime Inputs | Consumer only | Uses governed context; does not define source authority |
| UI/API Product Surfaces | Consumer only | Uses governed source authority through approved adapters |

## Authority Rules

1. The included source families are not open questions.
2. Scattered documents, notes, drafts, chat output, generated files, and support artifacts are not runtime authority.
3. Authored source families become runtime-authoritative only through controlled source structure, validation, promotion, and accepted lookup behavior.
4. Compiled runtime lookup is generated from authored sources and cannot become source truth.
5. Retrieval, AI, UI, and API consume governed source authority and cannot define it.
6. Product-ready document generation/rendering is not authorized by this artifact.
7. Standards embedding/retrieval is not authorized by this artifact.
8. Productization, SaaS, deployment, live model/provider calls, and local model/runtime trial claims are not authorized by this artifact.
9. New source-family inclusion requires an explicit Project Owner decision.
10. Content decisions made during CQV library expansion must preserve these source-role boundaries.

## M27 Execution Mandate

M27 must start CQV source content expansion for the included authored source families:

- CQV Libraries
- Task Pools
- Profiles
- Calendars
- Presets
- Selectors
- Planning Basis
- Duration References
- Mappings

M27 must create and refine actual CQV content. It must not reopen whether these families belong in the MVP boundary.

## DDR Impact

- DDR-001 and DDR-002 are directly addressed at boundary level because this artifact locks the source families that enter the runtime-authority path.
- DDR-003 is recognized through Document Template Families as boundary only; no product-ready template execution is authorized here.
- DDR-004 is recognized through standards references; no executable standards registry consumption, embedding, or retrieval is authorized here.
- DDR-006 is recognized through document factory and export/report boundaries; no product-ready generation, rendering, export, or reporting execution is authorized here.

No DDR is closed, reopened, downgraded, or reclassified by this artifact.

## Acceptance Criteria

M26.1 is acceptable when this artifact confirms:

- the local CQV MVP source boundary is locked;
- CQV Libraries, Task Pools, Profiles, Calendars, Presets, Selectors, Planning Basis, Duration References, and Mappings are included;
- standards references are controlled references, not embedded retrieval authority;
- document template, document factory, and export/report families are boundary-level inclusions only;
- compiled runtime lookup is generated artifact only;
- retrieval, AI, UI, and API are consumer surfaces only;
- M27 can start CQV content expansion without another M26 planning artifact.

## Validation Expectation

This is a documentation/governance artifact only.

No executable validation is required unless a separate change modifies code, commands, imports, schemas, tests, runtime behavior, CLI behavior, or executable contracts.

## Live Write Source Lock

This artifact was updated by live repository write authorization for this exact action only.

Authorization scope:

- update this M26.1 single artifact;
- update `PROGRESS_TRACKER.md` for M26.1 status;
- branch: `feature/m26-cqv-source-authority`;
- do not continue beyond M26.1.

No standing live-write authorization remains after this action.
