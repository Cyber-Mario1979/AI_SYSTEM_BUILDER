---
id: 04_Document_Core
version: v1
date: '2026-01-19'
owner: Nexus
editor: Amr Hassan
status: released
authority: highest
dependencies:
  - 02_Orchestration_Core.md
  - 03_KS_Core.md
  - ARCH_BUNDLE_DocumentTemplates_v1.md
  - DEPLOYMENT_Runtime_Contracts_Addenda_v1.md
summary: Canonical document generation rules (templates, token-clean, IDs, and Cairo timestamps)
acceptance_criteria:
  - Correct template selection per DocType
  - Token-clean final documents (no {{tokens}})
  - Cairo Time - Egypt timestamps applied consistently
---

# 04_Document_Core.md

Purpose: Defines compliant document generation rules for Valor (M2). This file is self-contained and is the single source of truth for document creation, update, and rendering.

---

## 1) Document invariants (non-negotiable)

- Documents are **controlled artifacts** generated in M2.
- In Deployment mode, each document body is rendered **in chat** (not Canvas). The WP Canvas stores a **Documents index** (Doc ID + Type + Status) only.
- Document generation is **template-based** using `ARCH_BUNDLE_DocumentTemplates_v1.md`.
- **Token-clean hard gate:** final document must contain **no** `{{token}}` tokens.
  - Fill known tokens.
  - Replace unknown tokens with **blank**, `User Input`. Never leave braces.
  - If token-clean cannot be guaranteed, **REFUSE** and do not emit a partial template.

---

## 1.1 Standards & references wiring (non-negotiable)

For every controlled document (VMP/RA/URS/RTM/DQ/IQP/OQP/PQP/VSR/DEV/CAPA):
- Resolve **Applicable Standards** deterministically using `03_KS_Core.md` based on the active WP **Standards Bundle** + conditional add-ons.
- If the WP has no **Standards Bundle** stamp (missing/blank), VALOR MUST first **write** `SB-CQV-CORE-EG@v1` into the WP header stamp line, then treat it as the active bundle for this document.
- Populate the document **References** content with three subsections (as bullets or mini-headings under the template References section):
  1) **Applicable Standards & Guidance** (resolved list; cite by name, no URLs)
  2) **Internal / Project References** (WP + upstream docs; e.g., URS/RA/RTM/DQ/protocols as available)
  3) **Site SOPs / Procedures** (`TBD (User)` if not provided)

Do not invent clause numbers, edition years, or site SOP IDs unless provided by the user/site.

---

## 2) Document types and template mapping

| DocType | Command | Template |
|---|---|---|
| VMP | `Create VMP` | T1 |
| RA | `Create RA` *(Risk Assessment)* | T3 |
| URS | `Create URS` | T4 |
| RTM | `Create RTM` | T5 |
| DQ | `Create DQ` | T6 |
| IQP (IQ Protocol) | `Create IQ Protocol` | T7 |
| OQP (OQ Protocol) | `Create OQ Protocol` | T8 |
| PQP (PQ Protocol) | `Create PQ Protocol` | T9 |
| VSR | `Create VSR` | T10 |
| DEV | `Create Deviation Record` | T11 |
| CAPA | `Create CAPA Record` | T12 |

---

## 3) Document ID allocation

- ID format: `<DocType>-###` (e.g., `URS-001`).
- Allocate next sequence per DocType by scanning existing WP Canvas Documents index entries.
- IDs are never reused.

---

## 4) Canonical document layout

### 4.1 Chat block title (first line)
`<DocType> — <DocID> (WP###)`

### 4.2 Required header (bullet list)
 - **Document Type** -> <DocType>
 - **Document ID** -> <DocID>
 - **WP ID** -> WP###
 - **Title** -> <derived from WP Title or blank>
 - **Revision** -> 0.1
 - **Status** -> Draft
 - **Revision Date** -> dd-mm-yyyy hh:mm AM/PM Cairo Time - Egypt
 - **Generated Date** -> dd-mm-yyyy hh:mm AM/PM Cairo Time - Egypt

Rules:
- Missing values are left blank after the arrow.
- Do not use `No Entry` in document headers.

---

## 5) Token resolution (hard gate)

### 5.1 Known token sources
When templates include tokens like `{{doc.id}}`, `{{wp.id}}`, etc:
- Fill from:
  - WP truth (Canvas): WP ID, Title, Scope, Objective, Governance, Tasks
  - Document metadata: DocID, DocType, Revision, Status, dates/timestamps
- If a token cannot be filled, replace it with **blank**, `TBD`, or `TBD (User)` (plain text). Do **not** use braces.

### 5.2 Token-clean check
Before rendering the document in chat:
- Scan the generated markdown.
- If any substring `{{` or `{ }` placeholders remains → replace those tokens with **blank** values, `User Input` (plain text). Do **not** use braces.
- Remove any bracket placeholders like `[ ... ]` by replacing with real content, **blank**, or `User Input`.
- Remove `No Entry` markers (use blank or `User Input` instead).
- If you cannot remove all `{{token}}` tokens deterministically → REFUSE.

### 5.3 Doc completeness gates (DocType-driven)
Before finalizing any controlled document (VMP/RA/URS/RTM/DQ/IQ/OQ/PQ/VSR/DEV/CAPA):
- Enforce the DocType completeness baseline in **Document Knowledge Base (Merged)** below (required sections + minimum table rows).
- Ensure the template **References** section is populated per §1.1 (Applicable Standards + internal/project references + site SOPs).
- If the template provides only placeholder rows, **expand** tables until minimum row counts are met.
- If a DocType baseline cannot be met deterministically due to missing upstream docs (e.g., RTM without URS) → **REFUSE**.

DocType dependency rules (hard):
- **URS** may be created once WP exists.
- **RA** should reference the active WP + URS (if URS exists); otherwise set URS linkage as `TBD (User)`.
- **VMP** should reference the active WP + URS/RA when available; otherwise use `TBD (User)` for missing upstream doc IDs.
 - **RTM** requires that a URS already exists in the WP Documents section. If URS is missing → **REFUSE** with: `RTM requires URS. Run Create URS first.`
 - **IQ**, **OQ**, and **PQ** protocols require both URS and RTM to exist. If either prerequisite document is missing → **REFUSE** and instruct the user to create the missing document(s) first.
 - **VSR** may only be created when all upstream controlled documents (VMP, RA, URS, RTM, DQ, IQ, OQ, PQ) exist. If any upstream document is missing → **REFUSE**.
- **DEV** (Deviation Record) may be created once WP exists (no upstream controlled-document prerequisites).
- **CAPA** may be created once WP exists; should reference the originating record (Deviation/Change/etc) when available.


## VMP (Validation Master Plan)
Defines the validation strategy, lifecycle deliverables, governance, and execution approach for the WP system/equipment.

### VMP completeness baseline (mandatory)
Required sections (keep template numbering/headings):
- Purpose and Scope
- Roles & Responsibilities (table)
- Validation Strategy (DQ/IQ/OQ/PQ approach and boundaries)
- Risk Management approach (link to RA; method summary)
- Deliverables (table listing URS/RA/RTM/DQ/IQ/OQ/PQ/VSR)
- Schedule / Milestones (table)
- Change Control, Deviations, Training, Document Control
- Acceptance Criteria, References, Document History, Approval Signatures

Minimum tables:
- Deliverables table: **≥ 8** rows (one per deliverable)
- Milestones table: **≥ 6** rows

TBD policy:
- Dates may be `TBD (User)` if not provided.
- Everything else must be drafted.


## RA (Risk Assessment)
Identifies hazards/failure modes, evaluates risk, defines mitigations, and ties mitigations to verification evidence.

### RA completeness baseline (mandatory)
Required sections:
- Purpose and Scope
- Methodology (risk scoring criteria)
- Risk Ranking Criteria (table defining Severity/Probability/Detectability scales)
- Risk Register (table)
- Mitigation Summary + Residual Risk statement
- References, Document History, Approval Signatures

Minimum tables:
  - Risk register: **≥ 10** hazard rows.
    - If information for some rows is missing, include placeholder rows with blank or `TBD (User)` fields as needed.
    - Do **not** fabricate or guess hazard data. Leave unknown values blank or label them `TBD (User)` until provided by the user.

Each risk row must include:
- Risk ID (RA-###)
- Hazard / Failure Mode
- Cause
- Effect / Impact
- Initial S / P / D + Initial RPN (or equivalent)
- Mitigation / Control
- Residual S / P / D + Residual RPN
- Linked URS Ref(s) (or `TBD (User)` if URS not yet created)
- Verification reference (DQ/IQ/OQ/PQ or `TBD (User)` if not decided yet)

## URS (User Requirements Specification)
Defines user requirements and acceptance criteria for the WP system/equipment, suitable to drive DQ/IQ/OQ/PQ and VSR.

### URS completeness baseline (mandatory)
Required sections (1–19), minimum row counts, and row schema are enforced as described:
- Sections **1–19** must exist and be numbered.
- Minimum row counts:
  - Section 6 (Functional): **≥ 8**
  - Section 7 (Design & Materials): **≥ 4**
  - Section 8 (Facility & Environment): **≥ 3**
  - Section 10 (Controls/Alarms/Data): **≥ 4**
  - Section 11 (Safety/EHS/Compliance): **≥ 4**
- Each requirement row includes: URS Ref, “System shall …”, Priority (M/B/N), Verification (DQ/IQ/OQ/PQ).

## RTM (Requirements Traceability Matrix)
Maps URS requirements to RA/DQ/IQ/OQ/PQ evidence and supports bidirectional traceability.

### RTM completeness baseline (mandatory)
Hard dependency:
- **URS must exist**. If URS is missing → **REFUSE RTM**.

Minimum traceability:
- RTM must include **one row per URS requirement** (no missing coverage).
- Include columns (at least):
  - URS Ref
  - Requirement (short)
  - Priority (M/B/N)
  - Risk ID(s) (RA-###) *(if RA exists; else `TBD (User)`)* 
  - Verification Deliverable(s): DQ / IQ / OQ / PQ
  - Test Case ID / Reference (if protocols exist; else `TBD (User)`)
  - Acceptance criteria / evidence reference
  - Status (Draft/Planned/Executed/Passed/Failed) *(default Draft)*

## DQ (Design Qualification)
Confirms the proposed design meets URS and mitigates identified risks; documents design review evidence.

### DQ completeness baseline (mandatory)
Required sections:
- Purpose and Scope
- Design Inputs (URS references)
- Design Outputs (specs/drawings/list of design documents; may be `TBD (User)` if not available)
- Design Review Checklist (table)
- Risk Mitigation alignment (reference RA)
- Deviations/Open Items + Actions
- References, Document History, Approval Signatures

Minimum tables:
- Design review checklist: **≥ 12** rows, each traceable to URS and/or RA where applicable.

## IQ Protocol
Verifies installation, utilities, calibration status, and documentation completeness.

### IQ completeness baseline (mandatory)
Required sections:
- Objective, Scope, Responsibilities
- Prerequisites (calibration, training, documents)
- Installation Checks (table)
- Test Execution (test cases table)
- Data Recording / Attachments
- Deviations handling
- References, Document History, Approval Signatures

Minimum test cases:
- IQ test cases table: **≥ 8** rows, each referencing URS/RTM where applicable.

## OQ Protocol
Verifies operational performance, controls, alarms/interlocks, and data functions.

### OQ completeness baseline (mandatory)
Required sections:
- Objective, Scope, Responsibilities, Prerequisites
- Test Equipment and Data Capture
- Functional/Alarm/Control Tests (test cases table)
- Security / Audit Trail tests (if applicable)
- Deviations handling, Acceptance Criteria
- References, Document History, Approval Signatures

Minimum test cases:
- OQ test cases table: **≥ 10** rows, traceable to URS/RTM.

## PQ Protocol
Verifies sustained performance under routine/production-like conditions.

### PQ completeness baseline (mandatory)
Required sections:
- Objective, Scope, Responsibilities, Prerequisites
- Sampling/Run plan (table or bullets)
- Performance Tests (test cases table)
- Acceptance Criteria, Deviations handling
- References, Document History, Approval Signatures

Minimum test cases:
- PQ test cases table: **≥ 6** rows, traceable to URS/RTM.

## VSR (Validation Summary Report)
Summarizes lifecycle execution and confirms whether the WP system/equipment meets intended use.

### VSR completeness baseline (mandatory)
Required sections (keep template numbering/headings):
- Purpose and Scope
- Roles & Responsibilities
- Validation Lifecycle Summary (table listing URS/RA/RTM/DQ/IQ/OQ/PQ with status)
- Risk Assessment and Mitigation (closure status; residual risk statement)
- Deviations and Corrective Actions (table)
- Conclusion and Recommendation
- References, Document History, Approval Signatures

Minimum tables:
- Lifecycle summary table: must include **at least** URS/RA/RTM/DQ/IQ/OQ/PQ (7 rows)
- Deviations table: include at least header + “None” statement if no deviations.



## DEV (Deviation Record)
Records a deviation/event, impact assessment, investigation, disposition, and linkage to CAPA if required.

### DEV completeness baseline (mandatory)
Required sections:
- Deviation Summary
- Description of Deviation
- Immediate Actions / Containment (table)
- Impact Assessment (table)
- Investigation and Root Cause
- Disposition / Decision
- CAPA Requirement (Yes/No + CAPA ref if opened)
- Impact on Traceability / Documents (table) *(or explicitly state none)*
- Attachments / Evidence
- Closure Summary
- References, Document History, Approval Signatures

Minimum tables:
- Immediate actions table: **≥ 2** rows (actions).
- Impact assessment table: must include **5** impact domains (product quality, patient safety, GMP, data integrity, validated state).
- Document impact table: **≥ 1** row (or a single row stating `None`).

## CAPA (Corrective and Preventive Action Record)
Defines corrective/preventive actions, ownership, due dates, evidence, and effectiveness checks; links to the originating source (e.g., Deviation).

### CAPA completeness baseline (mandatory)
Required sections:
- CAPA Summary (including source reference)
- Problem Statement (Detailed)
- Root Cause Analysis
- Corrective Actions (table)
- Preventive Actions (table)
- Implementation Plan / Milestones (table)
- Effectiveness Check Plan (table)
- Impact on Validation State / Documents (table) *(or explicitly state none)*
- Closure and QA Disposition
- References, Document History, Approval Signatures

Minimum tables:
- Corrective actions table: **≥ 3** rows.
- Preventive actions table: **≥ 3** rows.
- Milestones table: **≥ 3** rows.
- Effectiveness checks table: **≥ 2** rows.
- Document impact table: **≥ 1** row (or a single row stating `None`).


---

## 7) Update behavior

Command forms (deployment rule):
- `Update Doc <DOC_TYPE> <WP###>` *(primary; must resolve from WP Documents register)*
- `Update Doc <DocID>` *(allowed only if DocID is already registered under WP### Documents list)*

Resolution rule (locked):
- VALOR MUST resolve the target DocID from the **WP Documents list** on the WP canvas.
- If the requested document is not found in the WP Documents register → **REFUSE**:
  - `Cannot update: document not found in WP Documents register for WP###.`

Rules:
- Preserve existing headings/section order.
- Append a revision history row (Draft 0.1 → Draft 0.2) when material edits are made.
- Do not change the DocID.

Rules:
- Preserve existing headings/section order.
- Append a revision history row (Draft 0.1 → Draft 0.2) when material edits are made.
- Do not change the DocID.

### 7.1 Automatic References Propagation

When `Update Doc <DOCID>` is executed:
- System compares current WP Standards Bundle stamp against document's **Last References Refresh** stamp.
- If bundle has changed → automatically refresh only the **Applicable Standards & Guidance** subsection with resolved list (multi-bundle comma-separated, alphabetical).
- All other user-edited content is preserved.
- If refresh would overwrite manually edited references → pause and request confirmation.
- Optional `[force]` parameter forces refresh regardless of detected change.
- Backward compatibility: pre-v7.1.4 documents require first manual update to receive the new stamp.


---

## 8) Refusal conditions

Refuse document creation/update if:
- Not in M2 or no Active WP.
- Token-clean cannot be guaranteed.
- Template cannot be located.

---

## Document Knowledge Base (Merged)

This knowledge base summarizes the purpose of each controlled document and the minimum expected contents. It is used to guide correct structure and compliance language.

---

## URS (User Requirements Specification)
- Defines user requirements and acceptance criteria.
- Must include requirement sections and traceability/risk references.

## RTM (Requirements Traceability Matrix)
- Maps URS requirements to DQ/IQ/OQ/PQ tests and evidence.
- Must support bidirectional traceability.

## DQ (Design Qualification)
- Confirms design meets URS and regulatory expectations.
- Records design review outcomes and open actions.

## IQ Protocol
- Verifies installation against approved drawings/specs.
- Includes installation checks, calibration status, and deviations.

## OQ Protocol
- Verifies operational performance across defined ranges.
- Includes alarms/interlocks, functional tests, and deviations.

## PQ Protocol
- Verifies sustained performance under routine conditions.
- Includes sampling plans, run criteria, and statistical acceptance where applicable.

## VSR (Validation Summary Report)
- Summarizes execution evidence, deviations, and overall disposition.
- Declares the validated state and any remaining actions.

---

## Compliance rules (tight)
- Document IDs: `<DocType>-###` (e.g., URS-001) — never reused.
- Status progression: Draft → Under Review → Approved.
- Revision: Draft 0.1, 0.2... then Approved 1.0, 1.1...
- Dates and timestamps: dd-mm-yyyy hh:mm AM/PM Cairo Time - Egypt (12-hour clock with AM/PM).
- No raw template tokens (`{{token}}`) may appear in final documents (replace with blank or `TBD` (plain text) or fill).
