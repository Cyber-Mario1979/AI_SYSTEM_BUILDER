---
id: 03_KS_Core
version: v1
status: released
summary: Canonical KS core (reference standards logic and standards list)
authority: highest
---

# 03_KS_Core.md




---

## Source: (merged content)

# References and Standards Logic

## Using the internal standards list

Always refer to the internal curated standards list when citing or grounding standards that feeds your CQV advice.  This file contains a curated list of internationally recognized guidelines (e.g., ISPE Baseline Guides, EU GMP Annex 15 and ASTM E2500) and an example compliance matrix, with short descriptions of each standard.

## When the user asks about references or standards

When a user wants to know which standards apply or requests references:

* **Provide a list of the relevant standards** extracted from the internal curated standards list, including their names and short descriptions of their purpose (for example, "ISPE Baseline Guide Vol. 5 - Commissioning and Qualification: advocates a science- and risk-based approach").
* **Explain how to use them**: briefly describe how each standard should be applied in the context of CQV tasks (e.g., use EU GMP Annex 15 to set qualification requirements; apply ASTM E2500 principles for science- and risk-based verification).
* **Avoid external links**: do not send users to a Google Drive or external repository.  Instead, summarize the standards in your reply using information from the internal list.
---

---
## Note
* When advising on standards, cite the internal curated list only. 
* Do not output external `URLs`. Prefer short, numbered recommendations. 
* End with **"Next suggested step"** tailored to the context.
* ***EDA compliance Matrix*** is the source of truth for **Cleanrooms Introduction & Qualifications**; feed figures from it directly into **replies and `documents`**


---

## Source: (merged content)

# Valor References and Standards List  

**Valor** follows internationally recognized standards and best practices for Commissioning, Qualification and Validation (CQV) of pharmaceutical facilities, equipment, and systems.

**Key Standards and Guidelines Adopted By Valor.**
---

**1- ISPE Baseline Guides (Especially GAMP 5 and ISPE Baseline Guide Volume 5):**
Valor leverages ISPE's Good Practice Guides for C&Q. The ISPE Baseline Guide Volume 5: Commissioning and Qualification (Second Edition) is a core reference, advocating a science- and risk-based approach. GAMP 5 (Good Automated Manufacturing Practice) provides further guidance for computer system validation, which is also foundational to CQV.
---

**2- EU GMP Annex 15 (Qualification and Validation):**
Valor references EU GMP Annex 15. This annex sets the requirements for qualification and validation of facilities, utilities, equipment, and processes.
---

**3- ASTM E2500 Standard:**
Incorporate principles from the ASTM E2500 standard, which promotes a science- and risk-based approach to verification of manufacturing systems and equipment.
---

**4- EDA Compliance Validation Matrix for Work Package Development (Non-Sterile Areas):**

| Element                     | EDA Specification                                      | Inclusion in WP Scope                         |
| --------------------------- | ------------------------------------------------------ | --------------------------------------------- |
| Room Classification         | ISO 8 / Grade D for gowning & weighing                 | Scope must state cleanroom grade explicitly   |
| Particle Limit              | <= 3,520,000 particles >= 0.5 um/m^3 (at rest)            | Particle count test to be included if needed  |
| Pressure Cascade            | 10-15 Pa +/-5 between adjacent areas                     | Scope must reference DP sensor validation     |
| ACH Requirement             | 15-20 Air Changes per Hour                             | Verify design & measured ACH                  |
| Filtration Type             | HEPA H14 filters + prefilters + bag filters            | Scope must define filter type/integrity check |
| Airflow Directionality      | Positive pressure zones for clean-to-less-clean flow   | Smoke study/visual airflow checks             |
| Filter Integrity Validation | Mandatory (HEPA H14 Leak test)                         | Must include DOP/PAO testing                  |
| HVAC System Control         | Monitoring, alarms, BMS/SCADA control where applicable | Alarm testing and logging                     |
---

**Valor adopts a lifecycle approach to CQV, which may include:**
- User Requirements Specification (URS)
- Design Qualification (DQ)
- Factory and Site Acceptance Testing (FAT/SAT)
- Installation Qualification (IQ)
- Operational Qualification (OQ)
- Performance Qualification (PQ)

>- Note: C&Q is risk-based, focusing efforts on systems that impact product quality, patient safety, or regulatory compliance. Documentation, traceability, and data integrity are emphasized throughout the process.
---


---

## Standards Registry (canonical IDs; internal)

Use these IDs internally for deterministic selection. In documents, cite the **standard name** (optionally include the ID in parentheses). Do not output external URLs.

| Std ID           | Standard / Guidance                                                                       | Category            | Primary use within VALOR                                                      |
| ---------------- | ----------------------------------------------------------------------------------------- | ------------------- | ----------------------------------------------------------------------------- |
| `STD-ISPE-BG5`     | ISPE Baseline Guide Vol. 5 - Commissioning & Qualification                                | Guidance            | Lifecycle C&Q approach, deliverables, roles                                   |
| `STD-ISPE-GAMP5`   | ISPE GAMP 5 - Computerized Systems                                                        | Guidance            | CSV approach; applicable when software/automation/data integrity are in scope |
| `STD-EU-GMP-ANN15` | EU GMP Annex 15 - Qualification & Validation                                              | Regulatory guidance | Qualification/validation expectations and lifecycle structure                 |
| `STD-EU-GMP-ANN11` | EU GMP Annex 11 - Computerised Systems                                                    | Regulatory guidance | CSV expectations for regulated systems (when applicable)                      |
| `STD-ASTM-E2500`   | ASTM E2500 - Specification, Design & Verification of Pharmaceutical Manufacturing Systems | Standard            | Science- and risk-based verification framework                                |
| `STD-ICH-Q9`       | ICH Q9 - Quality Risk Management                                                          | Guideline           | Risk assessment methods and risk-based decisions (RA/controls)                |
| `STD-ICH-Q10`      | ICH Q10 - Pharmaceutical Quality System                                                   | Guideline           | PQS expectations; governance, change control, CAPA                            |
| `STD-FDA-21CFR11`  | 21 CFR Part 11 - Electronic Records; Electronic Signatures                                | Regulation          | E-records/signature requirements (when applicable)                            |
| `STD-ISO-14644`    | ISO 14644 - Cleanrooms and Associated Controlled Environments                             | Standard            | Cleanroom classification/testing references (when applicable)                 |
| `STD-LOCAL-EDA`    | Local regulator / site GMP requirements (e.g., EDA)                                       | Local regulatory    | Site/regulator-specific GMP expectations; user/site-owned reference           |

---

## Standards Bundles (deterministic)

A Standards Bundle is a named set of standards applied to a WP. Bundles are referenced as `<BUNDLE-ID>@<ver>` in the WP header (example: `SB-CQV-CORE-EG@v1`) and used to populate document **References** sections.

| Bundle ID          | Version | Intended use                                       | Included Std IDs                                                                       |
| ------------------ | ------: | -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `SB-CQV-CORE-EG`     |  v1 | Default CQV lifecycle bundle (Egypt site basis)    | `STD-LOCAL-EDA`, `STD-EU-GMP-ANN15`, `STD-ASTM-E2500`, `STD-ISPE-BG5`, `STD-ICH-Q9`, `STD-ICH-Q10` |
| `SB-CSV-ADDON`       |  v1 | Add-on for computerized / automated systems        | `STD-ISPE-GAMP5`, `STD-EU-GMP-ANN11`, `STD-FDA-21CFR11`                                      |
| `SB-CLEANROOM-ADDON` |  v1 | Add-on for cleanrooms/HVAC classified environments | `STD-ISO-14644`                                                                          |

---

**Canonical bundle token format (Canvas-safe; mandatory):**
- Use: `<BUNDLE-ID>@<ver>`  (example: `SB-CQV-CORE-EG@v1`)
- `@v1` is the version token used in Planning Invariants (do not use `-v1` in bindings).
- Bundles whose Intended use starts with **Default** are eligible for automatic binding.
- Bundles whose Intended use starts with **Add-on** are **never** auto-bound into the WP header; they must be explicitly added by the operator.
- Add-ons may still be **conditionally applied** during standards resolution for document References (document-level only) based on WP keywords (deterministic).


## Standards resolution rules (deterministic)

When generating controlled documents:
1) Start with the WP field **Standards Bundle**.
   - If missing -> set `SB-CQV-CORE-EG@v1` (default) and stamp it into the WP header.
2) Apply conditional add-ons for standards resolution (merge unique Std IDs; document-level only):
   - If WP Title/Scope/Objective contains any of: `CSV`, `software`, `PLC`, `SCADA`, `BMS`, `EMS`, `automation`, `data integrity` -> add `SB-CSV-ADDON@v1`.
   - If WP Title/Scope/Objective contains any of: `cleanroom`, `classified`, `HVAC`, `ISO 8`, `Grade` -> add `SB-CLEANROOM-ADDON@v1`.
3) Render the final list into the document **References** section as:
   - **Applicable Standards & Guidance** (resolved list)
   - **Internal / Project References** (WP + upstream docs)
   - **Site SOPs / Procedures** (`User input` if not provided)

Notes:
- Do not invent clause numbers or edition years unless provided by the user/site.
- If the user provides a site standards list, prefer it and treat the internal bundles as defaults only.
