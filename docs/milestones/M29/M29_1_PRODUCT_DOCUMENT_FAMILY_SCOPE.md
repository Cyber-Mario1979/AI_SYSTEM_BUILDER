---
doc_type: milestone_evidence_record
canonical_name: M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE
status: READY_FOR_USER_APPLICATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M29
checkpoint: M29.1
checkpoint_title: Product document family scope
execution_mode: Hybrid / Build-content
application_mode: user_applied_package
live_repo_write: NO
created_date: 2026-05-29
target_repo_path: docs/milestones/M29/M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE.md
---

# M29.1 — Product Document Family Scope

## Purpose

M29.1 defines the controlled product document-family scope for the local integrated CQV document factory / document engine path.

This checkpoint scopes VALOR / ASBP as a **CQV lifecycle document factory**, not as a narrow single-document generator and not as a product-ready generation engine.

The purpose of this artifact is to define:

- approved document families;
- stable document-family identifiers;
- CQV use boundaries;
- DCF relevance;
- standards-backed output relevance;
- downstream consumers for later M29 work;
- out-of-scope and deferred boundaries;
- anti-sprawl controls;
- non-product-ready implementation limits.

This artifact is a controlled scope/source artifact for later M29 work. It does not implement templates, schemas, renderers, generators, retrieval, UI, AI/runtime behavior, deployment, productization, or SaaS readiness.

## Execution Mode

Hybrid / Build-content.

M29.1 produces a controlled source-scope artifact that later checkpoints may use to govern document templates, input schemas, DCF intake, drafting modes, rendering, lifecycle workflow, review/approval controls, validation, and UAT.

Narrative discussion alone is not sufficient for M29.1. The required source artifact is this file.

## Scope Model

A document family is a controlled lifecycle lane, not necessarily one document type.

M29.1 therefore uses this rule:

> One document family may contain multiple related CQV document types when they belong to the same lifecycle lane, share a similar use boundary, and can be governed by one family-level contract.

This prevents uncontrolled family sprawl while allowing the document factory to represent real CQV work.

## Approved Core CQV Document Families

| Family ID | Family | Includes | CQV use boundary | DCF relevance | Standards-backed output relevance | Expected downstream consumers |
|---|---|---|---|---|---|---|
| `DOCF-PLAN-STRATEGY` | Strategy Documents | Validation Master Plan (VMP), Qualification Plan (QP), CQV Plan, Cleaning Validation Strategy | Defines validation / qualification strategy, scope, approach, responsibilities, and execution logic. | High. Strategy documents require structured project, scope, system, facility, responsibility, and lifecycle inputs. | High where GMP, validation, cleaning validation, or site procedure references govern the strategy. | DCF intake, template selection, drafting modes, review/approval workflow, validation/UAT evidence. |
| `DOCF-REQ-SPEC` | Requirements / Specifications | User Requirements Specification (URS), Functional Design Specification (FDS), System/Software Design Specification (SDS), URS Deviation / Gap List | Defines user, functional, system, and design-related requirements and records requirement gaps/deviations. | High. Requirements documents depend on structured user, system, process, utility, facility, regulatory, and local constraints. | High where requirements are GMP, GxP, safety, data integrity, automation, cleaning, environmental, or standards-related. | DCF intake, template selection, traceability, drafting modes, requirement-test mapping, validation/UAT evidence. |
| `DOCF-RISK-IMPACT` | Risk / Impact Documents | Risk Assessment, System Impact Assessment (SIA), Criticality Assessment, GxP Impact Assessment | Defines risk, impact, criticality, and GxP relevance used to justify validation depth and controls. | High. Risk and impact documents require structured scope, system boundaries, process impact, product impact, patient/user impact, and control inputs. | High where risk ranking, GxP impact, data integrity, GMP, cleaning, utilities, or regulatory expectations apply. | DCF intake, template selection, drafting modes, traceability, protocol depth, review/approval workflow, validation/UAT evidence. |
| `DOCF-TRACEABILITY` | Traceability Documents | Requirements Traceability Matrix (RTM), Requirement-Test Matrix, Standards Mapping Matrix | Links requirements, risks, standards, tests, protocols, reports, and closure evidence. | Medium to High. Traceability requires structured IDs, source records, family links, requirement/test relationships, and evidence references. | High where standards mapping or standards-backed output is in scope. | Template selection, source/library links, drafting modes, validation evidence, UAT evidence, review/approval workflow. |
| `DOCF-DESIGN` | Design Documents | Design Qualification (DQ), Design Review, Equipment Footprint, General Arrangement Drawings | Records design evidence and design review outcomes for equipment/system qualification readiness. | Medium to High. Design records require structured equipment, system, interface, drawing, access, connection, and operating-context inputs. | Medium to High where GMP design, cleanability, maintainability, automation, data integrity, safety, or facility interface expectations apply. | Template selection, design evidence linkage, traceability, protocol scope, review/approval workflow, validation/UAT evidence. |
| `DOCF-PROTOCOL` | Protocol Documents | FAT Protocol, SAT Protocol, IQ Protocol, OQ Protocol, PQ Protocol | Defines controlled test scripts, checks, acceptance criteria, execution evidence, deviations, and references. | High. Protocols require structured scope, system, test, acceptance, prerequisite, instrument, procedure, and evidence inputs. | High where acceptance criteria, qualification scope, regulatory expectations, or standards-backed requirements apply. | Template selection, drafting modes, execution forms, report generation, lifecycle workflow, review/approval workflow, validation/UAT evidence. |
| `DOCF-REPORT` | Report / Closeout Documents | FAT Report, SAT Report, IQ Report, OQ Report, PQ Report, Validation Summary Report (VSR), Summary Report | Summarizes execution, deviations, results, acceptance, unresolved items, and validation closure status. | High. Reports require structured execution data, result evidence, deviation links, open item status, and acceptance outcomes. | High where results are interpreted against approved protocols, requirements, GMP, standards, or validation strategy. | Rendering/export, report generation, lifecycle workflow, review/approval workflow, validation/UAT evidence. |
| `DOCF-EXCEPTION-CONTROL` | Exception / Gap / Open Item Documents | Exception Report, Gap Register, Open Item List, Protocol Exception Log | Controls CQV execution exceptions, gaps, protocol exceptions, unresolved items, and closure tracking. | High. Exception documents require structured issue, source, impact, decision, action, owner, due date, and closure inputs. | Medium to High where exception acceptance or gap disposition depends on GMP, standards, risk, or site procedure logic. | DCF intake, drafting modes, traceability, report closeout, review/approval workflow, validation/UAT evidence. |
| `DOCF-FORM-CHECKLIST` | Forms / Checklists / Registers | Data Collection Form (DCF), Execution Forms, Review Checklist, Attachment Register | Supports structured data collection, execution recording, review checks, and attachment/evidence control. | Core. DCF is part of this family and may also feed other families. | Medium to High depending on the controlled checklist/form and whether the form verifies standards-backed requirements. | DCF intake, schema binding, template selection, drafting modes, execution support, rendering/export, validation/UAT evidence. |
| `DOCF-SOP-TRAINING` | SOP / Training Support Documents | SOP Draft/Support, Training Matrix, Training Record Support | Supports operational handover and training readiness without replacing the local QMS. | Medium. Inputs may include role, SOP, process, equipment/system, training audience, and handover status. | Medium to High where GMP procedure expectations, training expectations, or site SOP references apply. | Drafting support, review workflow, local QMS linkage, handover readiness, validation/UAT evidence where applicable. |

## Approved Supporting CQV / QMS / Site Families

These families are in scope because they directly affect CQV readiness, execution truth, exception handling, and closure. They are not arbitrary product-surface expansion.

| Family ID | Family | Includes | CQV use boundary | DCF relevance | Standards-backed output relevance | Expected downstream consumers |
|---|---|---|---|---|---|---|
| `DOCF-CHANGE-CONTROL` | Change Management | Change Control Form, Change Impact Linkage, Change Reference Summary | Supports change control interpretation, linkage, and CQV impact references. The local QMS remains the system of record where applicable. | Medium to High. Inputs include change scope, affected systems, affected documents, impact, approval status, and QMS reference. | Medium to High where change impact depends on GMP, GxP, validation, data integrity, or site procedure expectations. | DCF intake, local QMS integration layer, traceability, report closeout, review/approval workflow. |
| `DOCF-DEVIATION-CAPA` | Quality Incident / Deviation / CAPA | Incident Report, Deviation Record, CAPA Form, CAPA Tracker | Supports quality incident, deviation, investigation, CAPA, and CAPA tracking linkage. The local QMS remains the system of record where applicable. | High. Inputs include incident/deviation details, affected systems, impact, root cause, CAPA, owner, due date, and closure evidence. | Medium to High where deviation/CAPA impact depends on GMP, GxP, standards, risk, or site procedure logic. | DCF intake, local QMS integration layer, traceability, report closeout, review/approval workflow, validation/UAT evidence. |
| `DOCF-CONSTRUCTION` | Construction Turnover / Site Readiness Documentation | Construction Package (CP), Construction Records (CR), Construction Turnover Package (CTOP), A0 Set Completion, A1 Mechanical Completion Certificate, A2 Commissioning Completion Certificate, A3 Qualification Completion Certificate, Facility / Room / Construction Layout Drawings | Supports construction turnover, site readiness, handover, and qualification-readiness evidence where the construction/facility boundary affects CQV. | Medium to High. Inputs include area, facility, room, equipment/system, turnover boundary, gate status, construction record status, and certificate applicability. | Medium to High where site readiness, construction handover, cleanroom/facility state, utilities, equipment installation, or GMP readiness affects qualification. | DCF intake, prerequisite checks, protocol readiness, report closeout, readiness gating, validation/UAT evidence. |

## Design Terminology Control

`DOCF-DESIGN` must preserve the following terminology distinctions.

| Term | Controlled meaning in this scope | Primary family |
|---|---|---|
| Equipment Footprint | The machine/equipment occupied space or envelope. | `DOCF-DESIGN` |
| General Arrangement Drawing | Equipment/system arrangement with surrounding operational context, access, clearances, interfaces, connections, platforms, HMI, tanks, split butterfly valves, and related workspace/operability context. | `DOCF-DESIGN` |
| Layout Drawing | Facility, room, building, construction, or space arrangement. Layout is not treated as a machine drawing in this scope. | `DOCF-CONSTRUCTION` |

General Arrangement and Layout are not synonyms in this artifact.

## Construction Turnover Gate Model

`DOCF-CONSTRUCTION` uses a scope-dependent turnover/gating model.

| Gate | Meaning | Scope rule |
|---|---|---|
| `A0` | Set Completion | Used where the project/site turnover scope requires a pre-mechanical-completion set completion gate. |
| `A1` | Mechanical Completion | Used where mechanical/construction completion is required for the defined scope. |
| `A2` | Commissioning Completion | Used where commissioning completion is required for the defined scope. |
| `A3` | Qualification Completion | Used where qualification completion is required for the defined scope. |

Gate applicability is scope-dependent. VALOR must not force every project to use every gate.

Example boundary rule:

- Building/facility scope may require A0 through A3.
- Equipment, utility, process-system, GMP-system, or modification scope may require only the applicable gate subset.
- Local/site terminology may be mapped, but the lifecycle meaning must remain explicit.

## Cross-Family Support Layers

These layers are not standalone document families. They are controls or support models that may apply across multiple families.

| Layer ID | Layer | Purpose | Applies to |
|---|---|---|---|
| `LAYER-STANDARDS-BACKED-OUTPUT` | Standards-backed output / citation relevance | Identifies whether a family or document type requires standards-backed drafting, citation support, standards mapping, limitation statements, or local SOP/site-standard references. | Strategy, requirements, risk/impact, traceability, design, protocols, reports, SOP/training support, construction where applicable. |
| `LAYER-LOCAL-REALITY-CONSTRAINTS` | Local reality constraints | Captures local availability, substitutions, vendor-document gaps, local service/calibration/testing limits, assumptions, limitations, and risk-based alternatives. | Requirements, design, risk, protocols, reports, construction, change control, deviation/CAPA. |
| `LAYER-LOCAL-QMS-INTEGRATION` | Local QMS integration boundary | Keeps local QMS as the system of record while allowing VALOR to support drafting, intake, linkage, CQV impact interpretation, and evidence organization. | Change control, deviation/CAPA, incident, SOP/training, exception control where applicable. |

## Family Activation Levels

M29.1 approves family scope. It does not implement product-ready output.

| Activation level | Meaning | M29.1 position |
|---|---|---|
| Scope-defined | Family exists as a controlled M29 document-family scope lane. | Approved by this artifact. |
| Template/schema-ready | Family has implemented templates, input schemas, selection rules, and validation evidence. | Not implemented by M29.1. Later M29 work only. |
| Product-ready generation | Family can produce controlled product-ready output with rendering/export, lifecycle, review/approval, validation, and UAT evidence. | Not implemented by M29.1. Later M29 gates only. |

## Anti-Sprawl Rule

M29.1 does not authorize unlimited document family expansion.

A new family must not be added later unless all of the following are true:

1. The candidate is a distinct CQV/GMP/QMS/site-readiness lifecycle lane, not merely another document title.
2. The candidate cannot be safely represented as a subtype under an approved family.
3. The candidate has a defined CQV use boundary.
4. The candidate has a defined DCF, standards-backed output, or local/QMS integration relevance where applicable.
5. The candidate is introduced through a future approved checkpoint, controlled amendment, or roadmap-authorized decision.

Document types may be added under existing families only when they preserve the family boundary and do not create new runtime/product claims.

## Explicit Out-of-Scope / Deferred Boundaries

The following are not implemented or made product-ready by M29.1:

- final templates;
- product-ready template library;
- document input schemas;
- schema binding;
- DCF form implementation;
- template selection or loading;
- controlled drafting modes;
- rendering/export/reporting;
- standards-backed generation;
- standards retrieval or embedding;
- document lifecycle workflow;
- review/approval workflow implementation;
- artifact validation workflow;
- trial document generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment;
- productization;
- SaaS readiness.

The following document areas are also out of initial M29.1 family scope unless a future controlled decision brings them in:

- procurement/commercial documents;
- finance/costing documents;
- HR documents;
- legal contracts;
- regulatory submission dossiers;
- full eQMS replacement records;
- batch manufacturing records;
- routine maintenance management records;
- environmental/health/safety permitting records;
- warehouse/logistics records;
- analytical method validation packages unless later mapped through an approved family decision;
- other non-CQV document classes that do not directly support CQV lifecycle, site readiness, or QMS-linked CQV closure.

## DDR Impact

M29.1 touches the following deferred-dependency domains:

| DDR | M29.1 impact |
|---|---|
| DDR-003 — Product-ready document templates library | Family scope informs later template-library work. M29.1 does not implement or close product-ready templates. |
| DDR-006 — Product-ready document/export/report generation and rendering | Family scope informs later generation/rendering scope. M29.1 does not implement or close product-ready generation/rendering. |
| DDR-004 — Standards source registry and citation authority | Awareness required where standards-backed output is marked relevant. M29.1 does not expand or close DDR-004. |
| DDR-005 — Standards embedding / retrieval index | Awareness required where standards-backed retrieval would be relevant later. Retrieval remains deferred to M30. |

DDR carry-forward truth:

- DDR-003 remains closed only for the approved governance/model scope until product-ready template implementation and document factory integration evidence exists.
- DDR-006 remains closure-planned and is not closed by family scoping alone.
- DDR-004 remains closed only for the approved standards source/citation authority model scope.
- DDR-005 remains deferred to M30.
- M29.1 does not close, reopen, downgrade, or reclassify any DDR.

## Architecture Boundary Impact

M29.1 does not change:

- CLI behavior;
- state/persistence boundaries;
- runtime loaders;
- validators;
- executable source contracts;
- UI/API behavior;
- AI/runtime behavior;
- deployment behavior;
- productization behavior;
- SaaS behavior.

If later work attempts to turn these family definitions into runtime loaders, validators, source contracts, schemas, templates, generation behavior, or UI/API behavior, that work must be handled by the applicable later M29 checkpoint with tests and validation where required.

## Validation Requirement

M29.1 requires document/source consistency review.

`python -m pytest -q` is not required for this artifact if M29.1 creates only this controlled scope document and does not change code, tests, schemas, runtime behavior, validators, loaders, source contracts, CLI behavior, executable commands, or executable behavior.

If any future M29.1 package expands beyond this artifact into executable/source-contract changes, pytest becomes required.

## Tracker Movement Rule

The tracker must not advance from `PLAN M29.1` merely because discussion occurred.

Tracker movement is allowed only after:

1. this artifact exists in the repository at `docs/milestones/M29/M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE.md`;
2. approved document families are explicitly listed;
3. family identifiers are stable;
4. DCF relevance is recorded;
5. standards-backed output relevance is recorded;
6. downstream consumers are recorded;
7. out-of-scope and deferred boundaries are explicit;
8. DDR-003 and DDR-006 impact is recorded;
9. DDR-004 / DDR-005 awareness is recorded where standards-backed output is involved;
10. anti-sprawl boundaries are visible;
11. explicit non-product-ready claims are visible.

## Explicit Non-Implementation Claims

This artifact does not implement:

- product-ready document families;
- template records;
- DCF intake;
- template selection/loading;
- input schemas;
- schema binding;
- controlled drafting modes;
- standards-backed output generation;
- rendering/export/reporting;
- document lifecycle workflow;
- review/approval workflow;
- artifact validation;
- trial document generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment;
- productization;
- SaaS readiness.

This artifact defines scope only.

## Completion Position

M29.1 is ready for user-applied repository placement when this file is added at:

`docs/milestones/M29/M29_1_PRODUCT_DOCUMENT_FAMILY_SCOPE.md`

After placement, tracker advancement requires the evidence listed in the Tracker Movement Rule and must not claim product-ready generation, rendering, templates, schemas, or validation behavior.
