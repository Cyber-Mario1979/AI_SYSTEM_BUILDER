---
doc_type: standards_registry
canonical_name: STANDARDS_SOURCE_REGISTRY
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: source_authority_model
authority: standards_source_registry
source_ddr: DDR-004
source_closure_plan: docs/milestones/M25/DDR_004_STANDARDS_SOURCE_REGISTRY_AND_CITATION_AUTHORITY_PLAN.md
phase: Phase 9 — SaaS Readiness / Productization
milestone: M25 — SaaS Readiness Assessment
checkpoint: M25.DDR-004
---

# STANDARDS_SOURCE_REGISTRY

## 1. Purpose

This registry defines the initial standards source authority model for ASBP.

It exists to support `DDR-004` — Standards source registry and citation authority.

The registry is intended to prevent standards-backed output from relying on memory, embeddings, retrieval results, generic model knowledge, or unsupported assumptions.

This file defines:

- initial standards source records
- required metadata fields
- authority status model
- citation model
- applicability model
- stricter-requirement precedence rule
- controlled override rule
- local/company/site standards intake model
- cleanroom local matrix capture
- non-authority rule for embedding and retrieval

This file does not embed controlled standards text.

This file does not claim clause-level content unless the source and clause are verified.

This file does not close `DDR-004` by itself. It provides closure evidence for source registry and citation authority design.

## 2. Registry Status

Current registry status:

`DRAFT_FOR_REVIEW`

The registry may be used as planning and governance evidence.

It must not be treated as a final validated standards engine until the Project Owner approves the model and any required executable validation is completed.

## 3. Source Authority Principles

ASBP must follow these principles:

1. Standards authority comes from registered sources, not model memory.
2. Retrieval and embedding may help find relevant content, but they are not authority.
3. Every standards-backed output must cite the source record used.
4. If exact clause/section references are not available, ASBP must state the citation limitation.
5. ASBP must not fabricate clause numbers, standard text, version status, applicability, or regulatory meaning.
6. Local/company/site/client standards may be binding only when the user or organization approves them as internal authority.
7. If two applicable sources overlap, ASBP defaults to the stricter applicable requirement.
8. A user may override the stricter requirement only through a controlled override record.

## 4. Authority Status Model

| Authority status | Meaning | May drive mandatory output? |
|---|---|---:|
| `Authoritative` | External regulatory, compendial, legal, or formally adopted standard applicable to the scope. | Yes |
| `Reference` | Useful supporting source, not independently mandatory unless adopted by project/user/company. | No, unless adopted |
| `Internal` | Company/site/client/project standard approved as binding for the declared scope. | Yes |
| `Recommendation` | Useful suggested practice or unverified matrix/rule; not binding. | No |
| `Draft` | Source model or proposed rule under review. | No |
| `Retired` | Historical source no longer active for new decisions. | No |
| `TBD` | Authority status not confirmed. | No |

## 5. Verification Status Model

| Verification status | Meaning |
|---|---|
| `Verified` | Source identity/version/applicability has been confirmed against controlled evidence. |
| `User-provided` | User supplied the source/requirement; not independently verified yet. |
| `Pending verification` | Source expected but version or applicability is not confirmed. |
| `Unavailable` | Source details are not available. |
| `Not externally verifiable` | Internal/local/company source cannot be verified externally but may be approved internally. |

## 6. Required Source Record Fields

Every standards source record must support these fields:

| Field | Required? | Description |
|---|---:|---|
| `std_id` | Yes | Stable source identifier. |
| `source_name` | Yes | Human-readable source name. |
| `source_type` | Yes | Regulation, standard, guideline, industry guide, internal standard, recommendation, site standard, client standard, or local authority source. |
| `authority_status` | Yes | One of the authority statuses defined in this registry. |
| `verification_status` | Yes | One of the verification statuses defined in this registry. |
| `version_or_effective_date` | Required when known | Version, edition, effective date, or revision marker. |
| `jurisdiction_or_owner` | Required when known | EU, FDA, ICH, ISO, ASTM, ISPE, company, site, local authority, or client. |
| `applicability_scope` | Yes | Where the source may apply. |
| `applicability_conditions` | Required when relevant | Triggers or constraints for applicability. |
| `citation_depth` | Yes | Document-level, section-level, clause-level, table-row-level, or requirement-level. |
| `source_location` | Required when available | Repo path, uploaded file reference, controlled document location, or user-provided reference. |
| `mandatory_flag` | Yes | Whether ASBP may treat the source as mandatory inside the declared applicability boundary. |
| `notes` | Optional | Limitations, warnings, or interpretation notes. |

## 7. Initial Standards Source Records

| STD ID | Source name | Source type | Authority status | Verification status | Version / effective date | Jurisdiction / owner | Initial applicability scope | Citation depth | Mandatory flag | Notes |
|---|---|---|---|---|---|---|---|---|---:|---|
| `STD-EU-GMP-ANNEX-15` | EU GMP Annex 15 | Regulation / GMP guidance | `Authoritative` when applicable | `Pending verification` | `TBD` | EU GMP | Qualification and validation expectations | Document / section / clause when verified | Yes when applicable | Version/effective date must be confirmed before audit-ready citation. |
| `STD-EU-GMP-ANNEX-11` | EU GMP Annex 11 | Regulation / GMP guidance | `Authoritative` when applicable | `Pending verification` | `TBD` | EU GMP | Computerised systems expectations | Document / section / clause when verified | Yes when applicable | Applies when computerized systems are in scope. |
| `STD-EU-GMP-CHAPTER-4` | EU GMP Chapter 4 | Regulation / GMP guidance | `Authoritative` when applicable | `Pending verification` | `TBD` | EU GMP | GMP documentation expectations | Document / section / clause when verified | Yes when applicable | Applies to GMP documentation controls. |
| `STD-ASTM-E2500` | ASTM E2500 | Standard | `Reference` unless adopted as project authority | `Pending verification` | `TBD` | ASTM | Verification and science/risk-based approach | Document / section / clause when verified | No unless adopted | May support verification strategy; does not weaken mandatory GMP requirements. |
| `STD-ISPE-GAMP5` | ISPE GAMP 5 | Industry guide | `Reference` unless adopted as project authority | `Pending verification` | `TBD` | ISPE | Computerised systems validation and assurance | Document / section / clause when verified | No unless adopted | May support approach; mandatory status depends on project/company adoption. |
| `STD-FDA-21CFR11` | 21 CFR Part 11 — Electronic Records; Electronic Signatures | Regulation | `Authoritative` when applicable | `Pending verification` | `TBD` | FDA / US CFR | Electronic records and electronic signatures | Document / section / clause when verified | Yes when applicable | Applies only when relevant records/signatures fall under the scope. |
| `STD-ICH-Q9` | ICH Q9 — Quality Risk Management | Guideline | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD` | ICH | Quality risk management and risk-based decisions | Document / section / clause when verified | No unless adopted/required | Risk-based rationale must not weaken mandatory requirements. |
| `STD-ICH-Q10` | ICH Q10 — Pharmaceutical Quality System | Guideline | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD` | ICH | PQS expectations, governance, change control, CAPA | Document / section / clause when verified | No unless adopted/required | May support PQS/governance framing. |
| `STD-ISO-14644` | ISO 14644 — Cleanrooms and Associated Controlled Environments | Standard | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD` | ISO | Cleanroom classification and testing references | Document / section / clause when verified | No unless adopted/required | Must be compared with GMP/local/site requirements where overlap exists. |
| `STD-LOCAL-CLEANROOM-NONSTERILE` | Local non-sterile cleanroom classification and HVAC matrix | Internal / recommendation candidate | `TBD` | `User-provided` | `TBD` | Project Owner / local or site source TBD | Non-sterile cleanroom areas, gowning, weighing, HVAC validation scope | Table-row-level until source document exists | No until approved as `Internal` | May become binding internal standard or remain recommendation only. |

## 8. Local Cleanroom Matrix Record

Source ID:

`STD-LOCAL-CLEANROOM-NONSTERILE`

Current status:

`TBD / User-provided`

Current use:

Candidate internal/local standard or recommendation-only cleanroom matrix.

| Requirement ID | Element | Candidate requirement | Applicability | Initial citation |
|---|---|---|---|---|
| `LOCAL-CR-001` | Room Classification | ISO 8 / Grade D for gowning and weighing | Non-sterile cleanroom scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-001` |
| `LOCAL-CR-002` | Particle Limit | `<= 3,520,000 particles >= 0.5 um/m^3` at rest | Non-sterile cleanroom particle classification where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-002` |
| `LOCAL-CR-003` | Pressure Cascade | `10–15 Pa +/-5` between adjacent areas | Adjacent controlled areas where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-003` |
| `LOCAL-CR-004` | ACH Requirement | `15–20 Air Changes per Hour` | HVAC scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-004` |
| `LOCAL-CR-005` | Filtration Type | HEPA H14 filters + prefilters + bag filters | HVAC/filter scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-005` |
| `LOCAL-CR-006` | Airflow Directionality | Positive pressure zones for clean-to-less-clean flow | Airflow/pressure zoning scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-006` |
| `LOCAL-CR-007` | Filter Integrity Validation | Mandatory HEPA H14 leak test | HEPA integrity scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-007` |
| `LOCAL-CR-008` | HVAC System Control | Monitoring, alarms, BMS/SCADA control where applicable | Automated/monitored HVAC scope where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-008` |

Working interpretation:

- Do not treat Grade D as ISO Grade 9.
- Treat ISO 8 / Grade D as the intended local cleanroom classification relationship unless later evidence says otherwise.
- The local matrix may become binding only if approved as `Internal`.
- Without internal approval, it remains `Recommendation`.

## 9. Citation Model

ASBP must support these citation formats:

| Citation level | Format | Example |
|---|---|---|
| Document-level | `STD-ID` | `STD-EU-GMP-ANNEX-15` |
| Version-level | `STD-ID@version/effective-date` | `STD-EU-GMP-ANNEX-15@TBD` |
| Section-level | `STD-ID § <section>` | `STD-EU-GMP-ANNEX-15 § TBD` |
| Clause-level | `STD-ID § <section.clause>` | `STD-FDA-21CFR11 § TBD` |
| Table-row-level | `STD-ID table:<table-id> row:<row-id>` | `STD-LOCAL-CLEANROOM-NONSTERILE table:local-cleanroom row:LOCAL-CR-002` |
| Requirement-level | `STD-ID requirement:<requirement-id>` | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-002` |

Rules:

- ASBP must not fabricate clause or section numbers.
- If exact clause data is unavailable, use document-level, table-row-level, or requirement-level citation.
- If a source is user-provided and not verified, ASBP must state that limitation.
- Standards-backed output must show which source record is being used and why it applies.

## 10. Applicability Model

ASBP must evaluate applicability before using a source.

Applicability may depend on:

- GMP relevance
- sterile/non-sterile classification
- cleanroom/non-cleanroom scope
- room classification
- equipment type
- system type
- computerized system status
- electronic records/e-signatures applicability
- process area
- lifecycle phase
- regulatory market
- company/site/client standards
- project acceptance criteria
- URS or design basis

A source in the registry is not automatically applicable to every output.

## 11. Stricter Requirement Precedence

When multiple applicable sources define requirements for the same acceptance point, ASBP must default to the stricter applicable requirement.

ASBP must explicitly identify:

- the overlapping sources
- the compared requirements
- which requirement is stricter
- which requirement is selected
- whether any user override was applied

Risk-based reasoning may support test rationale and scope decisions.

Risk-based reasoning must not silently reduce a mandatory applicable requirement.

## 12. Controlled Override Record

A controlled override is required when the user selects a less strict requirement than another applicable source.

Minimum override record:

| Field | Required? |
|---|---:|
| Override ID | Yes |
| Applicable sources compared | Yes |
| Stricter requirement identified | Yes |
| Selected requirement | Yes |
| Reason for override | Yes |
| Risk / quality justification | Yes |
| Applicability boundary | Yes |
| Approver / decision owner | Yes |
| Date or decision reference | Required when available |
| Residual risk note | Required when relevant |

ASBP must warn the user when an override weakens a stricter applicable requirement.

ASBP must not treat override as source closure or regulatory equivalence.

## 13. User-Uploaded Standards Intake Flow

ASBP must support future user-uploaded sources:

1. User uploads or provides a local/company/site/client standard.
2. ASBP creates a draft source record with one of:
   - `STD-LOCAL-*`
   - `STD-COMPANY-*`
   - `STD-SITE-*`
   - `STD-CLIENT-*`
3. ASBP captures source metadata and authority status.
4. ASBP asks whether the source is binding internal standard or recommendation only.
5. ASBP compares the uploaded source with applicable baseline sources.
6. ASBP defaults to the stricter applicable requirement.
7. ASBP allows controlled override only with justification.
8. ASBP records citation limitations where clause/section references are missing.
9. ASBP does not claim the uploaded/internal source is public regulation unless verified.

## 14. Embedding and Retrieval Non-Authority Rule

Embeddings, vector stores, retrieval indexes, search results, model memory, and AI-generated summaries are not standards authority.

They may assist retrieval and comparison only after source registry and citation authority are established.

`DDR-005` remains dependent on `DDR-004`.

## 15. Validation Expectations

This registry is documentation/governance evidence only.

No executable validation is required for this file alone.

Executable validation is required if later work adds:

- runtime registry parsing
- citation validation
- applicability matching
- stricter-requirement comparison logic
- override validation
- standards-backed output generation
- standards retrieval or embedding behavior

Validation command when executable behavior is touched:

`python -m pytest -q`

## 16. DDR-004 Closure Evidence Contribution

This file contributes evidence toward:

- standards registry structure
- source metadata model
- source status model
- applicability model
- citation depth model
- stricter requirement rule
- controlled override rule
- local/company standard intake flow
- embedding/retrieval non-authority rule
- validation expectations

Remaining before `DDR-004` can be closed:

- Project Owner review/acceptance of this registry
- register update to mark `DDR-004` as `Closed`, if approved
- tracker update after closure evidence is accepted
- validation evidence only if executable behavior is added
