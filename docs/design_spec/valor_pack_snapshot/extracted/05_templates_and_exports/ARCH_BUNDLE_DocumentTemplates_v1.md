---
id: ARCH_BUNDLE_DocumentTemplates_v1
version: v1
date: '2026-02-25'
owner: Amr Hassan
editor: Amr Hassan
status: released
dependencies:
  - 03_KS_Core.md
  - 04_Document_Core.md
  - ARCH_BUNDLE_Schemas_v1.json
summary: Controlled document templates bundle for M2 document generation (VMP/RA/URS/RTM/DQ/IQP/OQP/PQP/VSR/DEV/CAPA).
acceptance_criteria:
  - Template IDs and source labels align with pack libraries/schemas naming.
  - Usage contract matches current schema coverage for DEV/CAPA placeholder schemas.
  - Cross-references to 03_KS_Core, 04_Document_Core, and ARCH_BUNDLE_Schemas remain valid.
---

# ARCH Bundle — Document Templates — v1

Controlled document templates from  (full content).

## Usage Contract
- Schema-indexed templates in `ARCH_BUNDLE_Schemas_v1.json` cover T1,T3,T4,T5,T6,T7,T8,T9,T10; placeholder render-input schemas are also present for T11 (DEV) and T12 (CAPA) in this pack.
- When generating a controlled document (URS/RA/RTM/DQ/IQP/OQP/PQP/VSR/VMP/DEV/CAPA), use the matching template below as the base.
- Treat `{{token}}` items as template tokens; populate what can from state; otherwise replace with **blank**, `TBD`, or `TBD (User)` (plain text). Never leave `{ }`, `No Entry`, or bracket placeholders like `[ ... ]`.
- Do not alter section headings or numbering unless the user requests.
- Expand placeholder tables as needed to meet the DocType completeness baselines in `04_Document_Core.md` (minimum row counts / test case counts).
- Populate each document **References** section with **Applicable Standards & Guidance** resolved from `03_KS_Core.md` (based on WP **Standards Bundle**) plus internal/project document references.
- Render generated documents to **Canvas**.

---

## Source: `T1_VMP_Template_V1_0_1.md`

```markdown

# Source: T1_VMP_Template_V1_0_1.md

## Template Metadata
- ID: T1
- Title: Validation Master Plan (VMP) Extract
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Validation Master Plan (VMP) Extract Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `VMP`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## 1. Purpose and Scope
### 1.1 Purpose
Describe validation strategy, lifecycle approach, and documentation requirements aligned to corporate policies and regulatory guidelines.

### 1.2 Scope
Applies to the subject system/equipment at the specified facility. Outlines planned validation activities from URS through PQ; defines responsibilities; references applicable standards and procedures.

## 2. Validation Strategy
### 2.1 Lifecycle Approach
Adopt lifecycle methodology consistent with ASTM E2500 and EU GMP Annex 15: URS, DQ, IQ, OQ, PQ.

### 2.2 Risk Management
Employ risk-based thinking throughout lifecycle. Conduct RA (e.g., FMEA) to identify failure modes, rate S/O/D, calculate RPN, define mitigation actions, and drive testing focus.

### 2.3 Documentation and Deliverables
Use standardized templates for URS, DQ, IQ, OQ, PQ, RA, RTM, VSR. Deviations are managed via site deviation/CAPA system.

## 3. Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| Project Manager | Timelines, resources, deliverables aligned with VMP extract |
| System/Process Owner | User and process requirements |
| CQV | Protocols, traceability, risk assessments |
| QA | Reviews/approves validation documents; ensures compliance |
| Engineering/Automation | Design/installation; support IQ/OQ execution |
| Production/Operations | PQ runs |
| QC | Analytical testing supporting PQ |

## 4. References
- Site Validation Master Plan (VMP)
- EU GMP Annex 15
- ASTM E2500
- ICH Q8/Q9/Q10
- Company SOPs

## 5. Document History
| Rev | Date | Summary of Changes | Author |
| --- | --- | --- | --- |
| 0.1 | dd-mm-yyyy | Initial draft issued | CQV |

## 6. Approval Signatures
| Name | Title | Department | Date | Signature |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

---
```

---

## Source: `T3_Risk_Assessment_Template_V1_0_1.md`

```markdown

# Source: T3_Risk_Assessment_Template_V1_0_1.md

## Template Metadata
- ID: T3
- Title: Risk Assessment (FMEA)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Risk Assessment (FMEA)

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `RA`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

**Project/Equipment:** [Insert]  
**Area/Line:** [Insert]  
**Document No.:** RA-XXX  
**Prepared by:** [CQV/Engineering]  
**Reviewed by:** [QA]  
**Approved by:** [Head QA/Production]  

## 1. Purpose
Identify and assess risks (failure modes) to GMP compliance and product quality.

## 2. Scope
Covers risks associated with design, installation, operation, and performance.

## 3. References
- ICH Q9 (Quality Risk Management)
- EU GMP Annex 15
- ISPE Risk-Based Guide

## 4. Risk Assessment Table
| Step/URS Ref | Requirement / Function | Failure Mode | Potential Effect | S (1-5) | O (1-5) | D (1-5) | RPN | Mitigation |
|--------------|------------------------|--------------|-----------------|---------|---------|---------|-----|------------|
| URS-001 | SS316L product contact | Material not compliant | Contamination risk | 5 | 2 | 2 | 20 | Vendor certificate + IQ check |
| URS-002 | Alarm recording | Alarm not timestamped | Data integrity failure | 4 | 3 | 3 | 36 | OQ test of audit trail |
| URS-003 | Capacity >= 100 kg | Insufficient throughput | Production delays | 3 | 2 | 3 | 18 | PQ execution with full batch |

## 5. Approval
Prepared by: ____ Date: ____  
Reviewed by: ____ Date: ____  
Approved by: ____ Date: ____  

---
```

---

## Source: `T4_URS_Template_V1_0_1.md`

```markdown

# Source: T4_URS_Template_V1_0_1.md

## Template Metadata
- ID: T4
- Title: User Requirements Specification (URS)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# User Requirements Specification (URS) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `URS`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## 1. Purpose and Scope
### 1.1 Purpose
Define the purpose of the system/equipment, including intended use and regulatory/business drivers.

### 1.2 Scope
- In Scope: [Main system functions, subsystems]
- Out of Scope: [Anything explicitly excluded]

## 2. Roles & Responsibilities
| Role | Responsibility |
|------|----------------|
| System Owner | Owns content & approvals |
| Process Owner | Confirms process fit |
| Automation/CSV | Ensures compliance with computerized systems |
| EHS/SHE | Confirms safety & sustainability inputs |
| Quality | Ensures compliance with GMP/QA |
| Project Manager | Oversees alignment with project goals |

## 3. System Description
- Overview: [Brief description of the system]
- Interfaces: [Upstream/Downstream systems]
- Main Functions: [High-level functional description]

## 4. Definitions & Abbreviations
List key terms, e.g.: CQA, CPP, DQ/IQ/OQ/PQ, etc.

## 5. Requirement Classification
- M = Mandatory
- B = Beneficial
- N = Nice-to-have

## 6. User Requirements — Functional
> **AUTO-FILL:** You can optionally inject the full requirements table as markdown via `{{urs.requirements_table_md}}`.

| URS Ref | Requirement | Priority (M/B/N) | Verification (DQ/IQ/OQ/PQ) |
|---------|-------------|------------------|-----------------------------|
| 6.1 | [System shall perform its core function reliably] | | |
| 6.2 | [System capacity/throughput requirements] | | |
| 6.3 | [Integration with related systems] | | |

## 7. User Requirements — Design & Materials
| URS Ref | Requirement | Priority | Verification |
|---------|-------------|----------|--------------|
| 7.1 | [Materials compatible with intended use] | | |
| 7.2 | [Surfaces smooth and cleanable] | | |
| 7.3 | [Non-reactive and non-shedding materials] | | |

## 8. User Requirements — Facility & Environment
| URS Ref | Requirement | Priority | Verification |
|---------|-------------|----------|--------------|
| 8.1 | [Operating temperature range] | | |
| 8.2 | [Relative humidity range] | | |
| 8.3 | [Cleanroom classification/environmental conditions] | | |

## 9. User Requirements — Utilities
| URS Ref | Utility | Requirement |
|---------|---------|-------------|
| 9.1 | Electrical | [Voltage, frequency, phases] |
| 9.2 | Air/Water | [Compressed air, cooling, vacuum] |
| 9.3 | Other | [List as needed] |

## 10. User Requirements — Computerized Systems
| URS Ref | Requirement |
|---------|-------------|
| 10.1 | [Compliance with 21 CFR Part 11, Annex 11] |
| 10.2 | [Audit trails, security, backup] |
| 10.3 | [User management and access controls] |

## 11. User Requirements — Safety, Health & Environment
| URS Ref | Requirement |
|---------|-------------|
| 11.1 | [Operator safety] |
| 11.2 | [Emergency stops and safety interlocks] |
| 11.3 | [Noise/vibration limits] |
| 11.4 | [Environmental impact] |

## 12. User Requirements — Maintenance & Support
| URS Ref | Requirement |
|---------|-------------|
| 12.1 | [Ease of maintenance and access] |
| 12.2 | [Spare parts availability] |
| 12.3 | [Training and manuals] |
| 12.4 | [Warranty and service agreements] |

## 13. Documentation Deliverables
- GA Drawings, Technical Datasheets, Manuals, Qualification Protocols, Certificates.

## 14. References
- ISPE Baseline Guide Vol.5, GAMP 5, ICH Q8/Q9/Q10, EU GMP Annex 15, ASTM E2500, local regulatory (e.g., EDA).

## 15. Traceability
- Define trace through design and testing. Reference RTM.

## 16. Risk Assessment
- Summary of initial RA, identification of critical requirements.

## 17. Acceptance Criteria
- Define general acceptance criteria for fit-for-use.

## 18. Document History
| Rev | Date | Summary of Changes | Author |
|-----|------|--------------------|--------|
| 0.1 | [dd-mmm-yyyy] | Draft issued | [Name/Role] |

## 19. Approval Signatures
| Name | Title | Department | Date | Signature |
|------|-------|------------|------|------------|
| | | | | |
| | | | | |
| | | | | |

---
```

---

## Source: `T5_RTM_Template_V1_0_1.md`

```markdown

# Source: T5_RTM_Template_V1_0_1.md

## Template Metadata
- ID: T5
- Title: Requirements Traceability Matrix (RTM)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# CQV Traceability Matrix Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `RTM`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

Ensures traceability of URS requirements through validation lifecycle (DQ, IQ, OQ, PQ, VSR).

| URS_ID | Requirement Description | Risk Assessment Ref | DQ Verification (Design Review) | IQ Verification (Installation) | OQ Verification (Operation) | PQ Verification (Performance) | VSR Reference | Release Decision |
|---------|-------------------------------|---------------------|---------------------------------|-------------------------------|-----------------------------|-------------------------------|----------------|-----------------|
| URS-XXX | [Enter requirement] | RA-XXX | [DQ method] | [IQ method] | [OQ method] | [PQ method] | [VSR] | Accepted/Rejected |
| URS-XXX | [Enter requirement] | RA-XXX | [DQ method] | [IQ method] | [OQ method] | [PQ method] | [VSR] | Accepted/Rejected |

---
```

---

## Source: `T6_DQ_Template_V1_0_1.md`

```markdown

# Source: T6_DQ_Template_V1_0_1.md

## Template Metadata
- ID: T6
- Title: Design Qualification (DQ)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Design Qualification (DQ) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `DQ`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## Purpose and Scope
Verify proposed design meets URS and standards; review documentation, drawings, specs, and supplier responses.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| System Owner | Ensures design meets business/process needs |
| Engineering | Collates design documentation and vendor responses |
| CQV | Reviews design for GMP and URS |
| Quality Assurance | Approves DQ and monitors quality standards |
| Supplier | Provides detailed design documentation and responses |

## Design Compliance Matrix
| URS ID | Requirement | Design Response | Compliance (Y/N) | Evidence/Comments |
| --- | --- | --- | --- | --- |
| URS-001 | [Describe requirement] | [Design solution] |  |  |
| URS-002 | [Describe requirement] | [Design solution] |  |  |

## Deviations & Resolutions
Document deviations and actions taken.

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- Approved URS
- EU GMP Annex 15
- ASTM E2500
- Company design guidelines

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---
```

---

## Source: `T7_IQ_Protocol_Template_V1_0_1.md`

```markdown

# Source: T7_IQ_Protocol_Template_V1_0_1.md

## Template Metadata
- ID: T7
- Title: Installation Qualification (IQ) Protocol
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Installation Qualification (IQ) Protocol

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `IQP`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## Purpose and Scope
Verify installation per design/manufacturer recommendations/regulatory requirements. OQ covers operational testing.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| CQV Engineer | Executes installation checks |
| Quality | Reviews IQ results |
| Engineering/Maintenance | Ensures compliant utilities/services |
| Supplier | Provides guidelines and certificates |

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- URS, DQ
- EU GMP Annex 15
- ASTM E2500

## Installation Checklist
| Item | Requirement | Verification Method | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Utilities | Connected per approved P&ID | Visual inspection |  |  |
| Materials of Construction | Compliant (e.g., SS316L) | Certificate review |  |  |
| Calibration Certificates | Instruments in date | Certificate review |  |  |
| Documentation | Manuals/drawings/spare parts list | Document review |  |  |

## Deviations
Describe non-conformances and corrective actions.

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---
```

---

## Source: `T8_OQ_Protocol_Template_V1_0_1.md`

```markdown

# Source: T8_OQ_Protocol_Template_V1_0_1.md

## Template Metadata
- ID: T8
- Title: Operational Qualification (OQ) Protocol
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Operational Qualification (OQ) Protocol

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `OQP`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## Purpose and Scope
Verify operational performance across ranges; confirm critical functions, alarms, interlocks; ensure data integrity.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| CQV Engineer | Executes OQ scripts and records results |
| Process Owner | Reviews parameters and accepts outcomes |
| Quality | Ensures compliance; approves deviations |
| Automation/CSV | Supports software testing and DI verification |

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- URS, DQ, IQ
- EU GMP Annex 15
- ASTM E2500

## Test Matrix
| Test ID | Objective | Method | Acceptance Criteria | Records |
| --- | --- | --- | --- | --- |
| OQ-001 | Verify alarm activation | Force alarm; monitor response | Alarm logs with correct timestamp | Event log capture |
| OQ-002 | Verify temperature control | Operate at setpoints across range | Maintain within +/- 2 deg C of setpoint | Recorder printout |
| OQ-003 | Verify safety interlock | Attempt unsafe start | Prevented; warning displayed | Checklist |

## Deviations
Record deviations, impact, corrective actions.

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---
```

---

## Source: `T9_PQ_Protocol_Template_V1_0_1.md`

```markdown

# Source: T9_PQ_Protocol_Template_V1_0_1.md

## Template Metadata
- ID: T9
- Title: Performance Qualification (PQ) Protocol
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Performance Qualification (PQ) Protocol

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `PQP`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## Purpose and Scope
Demonstrate consistent performance under routine conditions; assess throughput, product quality, reproducibility.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| CQV | Plans and executes PQ runs |
| Production | Operates equipment per batch records |
| QC | Conducts analytical testing |
| QA | Reviews PQ documentation; approves status |

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- URS, DQ, IQ, OQ
- Process validation master plan
- EU GMP Annex 15; ICH Q8/Q9/Q10

## Test Matrix
| Test ID | Objective | Method | Acceptance Criteria | Records |
| --- | --- | --- | --- | --- |
| PQ-001 | Verify throughput | Full-scale batch | >= target throughput within tolerance | Batch record |
| PQ-002 | Verify product quality | In-process and final QC | All within specifications | QC certificates |
| PQ-003 | Verify reproducibility | Three consecutive runs | No critical deviations; consistent results | VSR summary |

## Deviations
List deviations, impact, corrective actions.

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---
```

---

## Source: `T11_Deviation_Record_Template_V1_0_1.md`

```markdown

# Source: T11_Deviation_Record_Template_V1_0_1.md

## Template Metadata
- ID: T11
- Title: Deviation Record (DEV)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Deviation Record (DEV) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `DEV`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author/Initiator:** `{{doc.actors.author}}`  |  **Reviewer (QA):** `{{doc.actors.reviewer}}`  |  **Approver (QA):** `{{doc.actors.approver}}`

## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Initiator | {{doc.actors.author}} |
| QA Reviewer | {{doc.actors.reviewer}} |
| QA Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Initiator | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| QA Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| QA Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## 1. Deviation Summary

| Field | Value |
|---|---|
| Deviation raised date/time | {{dev.raised_datetime}} |
| Raised by (name/role) | {{dev.raised_by}} |
| Area/Room/Line | {{dev.area}} |
| System/Equipment | {{dev.system}} |
| Related lifecycle stage | {{dev.stage}} |
| Related protocol/report | {{dev.related_doc}} |
| Related test case / step | {{dev.test_case_ref}} |
| Batch/Lot (if applicable) | {{dev.batch_lot}} |
| Deviation category | {{dev.category}} |
| Deviation criticality | {{dev.criticality}} |

## 2. Description of Deviation
Describe what happened, where, when, and how it was detected.

## 3. Immediate Actions / Containment
List immediate actions taken to control impact (e.g., stop activity, quarantine, re-check calibration, repeat test).

| Action | Owner | Date | Evidence/Record |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 4. Impact Assessment
Assess potential impact on product quality, patient safety, GMP compliance, data integrity, and validated state.

| Impact Domain | Impact? (Yes/No) | Rationale / Assessment | Required follow-up |
|---|---|---|---|
| Product quality | | | |
| Patient safety | | | |
| GMP compliance | | | |
| Data integrity | | | |
| Validated state / qualification | | | |

## 5. Investigation and Root Cause
Describe investigation method (e.g., 5-Why, Fishbone) and findings.

### 5.1 Investigation details
- Method: {{dev.investigation_method}}
- Findings summary: {{dev.findings}}

### 5.2 Root cause statement
{{dev.root_cause}}

## 6. Disposition / Decision
Describe disposition (e.g., accept as-is with justification, re-execute test, revise protocol, rework installation).

| Decision | Justification | QA disposition | Additional testing required? |
|---|---|---|---|
| | | | |

## 7. CAPA Requirement
- CAPA required? {{dev.capa_required}}
- CAPA record reference (if opened): {{dev.capa_ref}}

## 8. Impact on Traceability / Documents
List documents that require update due to this deviation (URS/RTM/Protocols/Reports), or state none.

| Document | Impact / Change Needed | Owner | Target date |
|---|---|---|---|
| | | | |
| | | | |

## 9. Attachments / Evidence
List evidence files/records supporting investigation and closure.

## 10. Closure Summary
State closure conclusion and remaining actions (if any).

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- Site deviation/CAPA SOP: `TBD (User)`
- Related validation documents: URS/RTM/Protocols/Reports (as applicable)

## Document History

| Rev | Date | Summary of Changes | Author |
|---|---|---|---|
| 0.1 | {{doc.revision_date}} | Initial deviation record issued | {{doc.actors.author}} |

## Approval Signatures

| Name | Title | Department | Date | Signature |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

---
```

---

## Source: `T12_CAPA_Record_Template_V1_0_1.md`

```markdown

# Source: T12_CAPA_Record_Template_V1_0_1.md

## Template Metadata
- ID: T12
- Title: CAPA Record (CAPA)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# CAPA Record (CAPA) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `CAPA`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author/Owner:** `{{doc.actors.author}}`  |  **Reviewer (QA):** `{{doc.actors.reviewer}}`  |  **Approver (QA):** `{{doc.actors.approver}}`

## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| CAPA Owner | {{doc.actors.author}} |
| QA Reviewer | {{doc.actors.reviewer}} |
| QA Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| CAPA Owner | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| QA Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| QA Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## 1. CAPA Summary

| Field | Value |
|---|---|
| CAPA opened date/time | {{capa.opened_datetime}} |
| CAPA opened by | {{capa.opened_by}} |
| Source type | {{capa.source_type}} |
| Source reference (Deviation/Change/Complaint) | {{capa.source_ref}} |
| Area/System | {{capa.area_system}} |
| Problem statement (short) | {{capa.problem_statement_short}} |
| CAPA priority | {{capa.priority}} |
| Target closure date | {{capa.target_closure_date}} |

## 2. Problem Statement (Detailed)
Describe the issue requiring CAPA, including where/when discovered and scope.

## 3. Root Cause Analysis

| Item | Details |
|---|---|
| Method | {{capa.rca_method}} |
| Root cause(s) | {{capa.root_cause}} |
| Contributing factors | {{capa.contributing_factors}} |
| Evidence supporting root cause | {{capa.evidence}} |

## 4. Corrective Actions
Actions that correct the detected issue (short-term / remediation).

| Action ID | Corrective Action | Owner | Due Date | Evidence of completion | Status |
|---|---|---|---|---|---|
| CA-01 | | | | | |
| CA-02 | | | | | |
| CA-03 | | | | | |

## 5. Preventive Actions
Actions that prevent recurrence (systemic / long-term).

| Action ID | Preventive Action | Owner | Due Date | Evidence of completion | Status |
|---|---|---|---|---|---|
| PA-01 | | | | | |
| PA-02 | | | | | |
| PA-03 | | | | | |

## 6. Implementation Plan / Milestones
Summarize implementation sequencing and dependencies.

| Milestone | Description | Owner | Target date | Notes |
|---|---|---|---|---|
| M1 | | | | |
| M2 | | | | |
| M3 | | | | |

## 7. Effectiveness Check Plan
Define how effectiveness will be verified and when.

| Check | Method / Criteria | Owner | Due date | Result |
|---|---|---|---|---|
| EC-01 | | | | |
| EC-02 | | | | |

## 8. Impact on Validation State / Documents
List any validation deliverables impacted and required updates.

| Document | Impact / Change Needed | Owner | Target date |
|---|---|---|---|
| | | | |
| | | | |

## 9. Closure and QA Disposition
Summarize closure decision, residual risk, and QA disposition.

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- Site CAPA SOP: `TBD (User)`
- Source record (Deviation/Change/etc): `TBD (User)`

## Document History

| Rev | Date | Summary of Changes | Author |
|---|---|---|---|
| 0.1 | {{doc.revision_date}} | Initial CAPA record issued | {{doc.actors.author}} |

## Approval Signatures

| Name | Title | Department | Date | Signature |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

---
```

---

## Source: `T10_VSR_Template_V1_0_1.md`

```markdown

# Source: T10_VSR_Template_V1_0_1.md

## Template Metadata
- ID: T10
- Title: Validation Summary Report (VSR)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Validation Summary Report (VSR) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `VSR`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.selector.id}}@{{doc.stamps.selector.version}}` | `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` | `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` | `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_cairo}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (Cairo Time - Egypt) | {{doc.generated_cairo}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Domain (CS) | {{doc.stamps.selector.id}}@{{doc.stamps.selector.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## 1. Purpose and Scope
Summarize URS, DQ, IQ, OQ, PQ outcomes; assess compliance, deviations/CAPAs, residual risks; support release decision.

## 2. Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| System/Process Owner | Confirms system meets requirements; authorizes release |
| CQV | Prepares VSR; collates data; assesses compliance |
| QA | Reviews/approves VSR; verifies deviations/CAPAs closure |
| Engineering/Automation | Provides design/install data; evaluates technical issues |
| Production/Operations | Executes PQ runs; verifies user acceptance |
| QC | Provides analytical data supporting PQ |

## 3. Validation Lifecycle Summary
- URS Compliance
- Design Qualification
- Installation Qualification
- Operational Qualification
- Performance Qualification

## 4. Risk Assessment and Mitigation
Summarize RA (e.g., FMEA), significant risks, RPN, mitigations, residual risk acceptance.

## 5. Deviations and Corrective Actions
List deviations across URS/DQ/IQ/OQ/PQ; root cause, impact, CAPA; closure status.

## 6. Conclusion and Recommendation
Overall evaluation of validation status; recommend qualified release or conditions.

## 7. References, Document History, Approval Signatures
List referenced documents; revision table; signatures.

---
```
