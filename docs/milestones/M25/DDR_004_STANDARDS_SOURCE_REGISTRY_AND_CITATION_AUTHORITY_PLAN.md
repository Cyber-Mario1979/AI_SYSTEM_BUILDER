---
doc_type: ddr_closure_plan
canonical_name: DDR_004_STANDARDS_SOURCE_REGISTRY_AND_CITATION_AUTHORITY_PLAN
status: DRAFT_FOR_REVIEW
governs_execution: false
document_state_mode: ddr_closure_evidence
authority: checkpoint_evidence
source_register: docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md
source_m25_2_disposition_review: docs/milestones/M25/M25_2_DEFERRED_DEPENDENCY_DISPOSITION_REVIEW.md
source_m25_2_closure_plan: docs/milestones/M25/M25_2_DDR_CLOSURE_PLAN.md
ddr_id: DDR-004
checkpoint: M25.DDR-004
milestone: M25 — SaaS Readiness Assessment
phase: Phase 9 — SaaS Readiness / Productization
approval_state: APPROVED_TO_START_BY_PROJECT_OWNER
---

# DDR-004 — Standards Source Registry and Citation Authority Plan

## 1. Purpose

This document defines the approved starting closure path for `DDR-004` — Standards source registry and citation authority.

The purpose of `DDR-004` is to prevent ASBP from producing standards-backed advice, standards-backed product output, standards embedding, standards retrieval, audit-ready citation, CQV/GMP advisory output, or standards-backed document generation unless the underlying standards have controlled source identity, applicability, version/status handling, and citation rules.

This document does not embed standards content.

This document does not close `DDR-004`.

This document creates the closure path and the first controlled registry/citation model required to move `DDR-004` from `Open` to `Closure Planned`.

## 2. Approved Scope

The Project Owner approved starting `DDR-004` first.

The approved initial standards scope is additive.

The baseline scope includes:

| STD ID | Source name | Source type | Initial applicability |
|---|---|---|---|
| `STD-EU-GMP-ANNEX-15` | EU GMP Annex 15 | Regulation / GMP guidance | Qualification and validation expectations |
| `STD-EU-GMP-ANNEX-11` | EU GMP Annex 11 | Regulation / GMP guidance | Computerised systems expectations |
| `STD-EU-GMP-CHAPTER-4` | EU GMP Chapter 4 | Regulation / GMP guidance | Documentation expectations |
| `STD-ASTM-E2500` | ASTM E2500 | Standard | Verification / science and risk-based approach |
| `STD-ISPE-GAMP5` | ISPE GAMP 5 | Industry guide | Computerised systems validation and assurance |
| `STD-FDA-21CFR11` | 21 CFR Part 11 | Regulation | Electronic records and electronic signatures where applicable |
| `STD-ICH-Q9` | ICH Q9 — Quality Risk Management | Guideline | Risk assessment methods and risk-based decisions |
| `STD-ICH-Q10` | ICH Q10 — Pharmaceutical Quality System | Guideline | PQS expectations, governance, change control, CAPA |
| `STD-ISO-14644` | ISO 14644 — Cleanrooms and Associated Controlled Environments | Standard | Cleanroom classification and testing references where applicable |

`STD-FDA-21CFR11` appears only once in the registry even if referenced by multiple source lists.

## 3. Local / Company / Site Standards Intake Scope

ASBP must support user-provided local, company, site, client, or authority-specific standards.

A local/company/site standard may be introduced through one of two authority modes:

| Mode | Meaning | System behavior |
|---|---|---|
| `Internal Standard` | The user or organization approves the source as binding for the project/system. | ASBP may treat it as mandatory inside the declared applicability boundary. |
| `Recommendation Only` | The source is useful but is not approved as binding. | ASBP may present it as guidance/recommendation only and must not treat it as mandatory acceptance criteria. |

The cleanroom classification matrix provided by the Project Owner is treated as a candidate local/internal cleanroom standard until formal authority is confirmed.

Proposed ID:

`STD-LOCAL-CLEANROOM-NONSTERILE`

Initial authority status:

`TBD`

Permitted target statuses after Project Owner decision:

- `Internal`
- `Recommendation`
- `Reference`
- `TBD`

It must not be presented as an external regulation unless a traceable regulatory source, document name, version, and applicability statement are provided.

## 4. Local Cleanroom Matrix Capture

The following Project Owner-provided matrix is captured as a candidate local/internal non-sterile cleanroom requirement set.

| Element | Candidate local specification | Initial ASBP interpretation |
|---|---|---|
| Room Classification | ISO 8 / Grade D for gowning and weighing | Scope must state cleanroom grade explicitly. |
| Particle Limit | `<= 3,520,000 particles >= 0.5 um/m^3` at rest | Particle count test to be included if applicable. |
| Pressure Cascade | `10–15 Pa +/-5` between adjacent areas | Scope must reference DP sensor validation. |
| ACH Requirement | `15–20 Air Changes per Hour` | Verify design and measured ACH where applicable. |
| Filtration Type | HEPA H14 filters + prefilters + bag filters | Scope must define filter type and integrity check. |
| Airflow Directionality | Positive pressure zones for clean-to-less-clean flow | Smoke study / visual airflow checks where applicable. |
| Filter Integrity Validation | Mandatory HEPA H14 leak test | Must include DOP/PAO testing where applicable. |
| HVAC System Control | Monitoring, alarms, BMS/SCADA control where applicable | Alarm testing and logging where applicable. |

Project Owner working decision:

- Do not treat Grade D as ISO Grade 9.
- Treat ISO 8 / Grade D as the intended cleanroom classification relationship for this ASBP local cleanroom matrix unless later source evidence says otherwise.
- If local/company/site requirements are stricter than an external baseline source, ASBP must default to the stricter applicable requirement.
- If the user wants to override the stricter requirement, the override must be explicit, justified, and recorded.

## 5. Standards Registry Required Fields

Every standards source record must support these fields:

| Field | Required? | Description |
|---|---:|---|
| `std_id` | Yes | Stable source identifier, such as `STD-EU-GMP-ANNEX-15`. |
| `source_name` | Yes | Human-readable source name. |
| `source_type` | Yes | Regulation, standard, guideline, industry guide, internal standard, recommendation, client standard, or site standard. |
| `authority_status` | Yes | `Authoritative`, `Reference`, `Internal`, `Recommendation`, `Draft`, `Retired`, or `TBD`. |
| `version_or_effective_date` | Required when known | Version, edition, effective date, or revision marker. |
| `jurisdiction_or_owner` | Required when known | EU, FDA, ICH, ISO, ASTM, ISPE, local authority, company, site, or client. |
| `applicability_scope` | Yes | Where the source applies. |
| `applicability_conditions` | Required when relevant | Triggers or constraints for applicability. |
| `citation_depth` | Yes | Document-level, section-level, clause-level, table-row-level, or requirement-level. |
| `source_location` | Required when available | Repo path, uploaded file reference, public source reference, controlled document path, or user-provided reference. |
| `verification_status` | Yes | `Verified`, `User-provided`, `Pending verification`, `Unavailable`, or `Not externally verifiable`. |
| `mandatory_flag` | Yes | Whether ASBP may treat the source as mandatory inside the declared applicability boundary. |
| `notes` | Optional | Limitations, warnings, or interpretation notes. |

## 6. Citation Model

ASBP must support these citation levels:

| Citation level | Format | Use case |
|---|---|---|
| Document-level | `STD-ID` | General source reference. |
| Version-level | `STD-ID@version/effective-date` | Source version clarity. |
| Section-level | `STD-ID § section` | Standard section reference. |
| Clause-level | `STD-ID § section.clause` | Clause-specific requirement reference. |
| Table-row-level | `STD-ID table:<table-id> row:<row-id>` | Matrix/table-derived requirements, including local cleanroom matrices. |
| Requirement-level | `STD-ID requirement:<requirement-id>` | Internal parsed requirement registry, when available. |

For local or user-uploaded sources without formal clause numbering, ASBP may cite by table row, heading, file section, or requirement ID.

ASBP must not fabricate clause numbers.

If exact clause or section cannot be confirmed, ASBP must state that the citation is document-level, table-row-level, or pending verification.

## 7. Applicability Model

A standards source may apply based on:

- process area
- room classification
- equipment type
- system type
- computerized system status
- electronic records/signatures applicability
- cleanroom/non-cleanroom status
- sterile/non-sterile status
- GMP/non-GMP boundary
- lifecycle phase
- project scope
- client/company/site requirements
- regulatory market or intended use

ASBP must not apply a standard merely because it exists in the registry.

Each standards-backed output must declare why the source is applicable or why it is only referenced.

## 8. Stricter Requirement Rule

When two or more applicable sources define requirements for the same acceptance point, ASBP must default to the stricter applicable requirement.

This rule applies to:

- cleanroom classification
- particle limits
- pressure cascade / DP criteria
- ACH criteria
- filtration and HEPA integrity expectations
- computerized system controls
- documentation expectations
- risk management expectations
- validation/qualification expectations
- electronic record/e-signature controls
- any other overlapping acceptance requirement

Risk-based reasoning may support scope definition, prioritization, test rationale, and exception justification.

Risk-based reasoning must not silently weaken a mandatory applicable requirement.

## 9. Controlled Override Rule

The user may override the stricter applicable requirement only through a controlled override record.

A controlled override must capture:

| Field | Required? |
|---|---:|
| Applicable sources compared | Yes |
| Stricter requirement identified | Yes |
| Selected requirement | Yes |
| Override reason | Yes |
| Risk / quality justification | Yes |
| Applicability boundary | Yes |
| Approver / decision owner | Yes |
| Date or decision reference | Required when available |
| Residual risk note | Required when relevant |

ASBP must warn the user when an override selects a less strict requirement than another applicable source.

ASBP must not treat override as source closure.

## 10. Embedding / Retrieval Non-Authority Rule

Embeddings, retrieval indexes, vector stores, search results, or AI memory must not become standards authority.

Standards authority comes from the standards registry, source identity, version/status, applicability model, citation model, and approved user/company/local authority decisions.

`DDR-005` must remain blocked until `DDR-004` is closed or has an approved closure state sufficient to define retrieval/index behavior.

## 11. User-Uploaded Local Standards Flow

ASBP must support this future flow:

1. User uploads or provides a local/company/site/client standard.
2. ASBP creates a draft source record with a unique `STD-LOCAL-*`, `STD-COMPANY-*`, `STD-SITE-*`, or `STD-CLIENT-*` identifier.
3. ASBP captures source name, owner, version/effective date when known, applicability, and authority status.
4. ASBP asks the user whether the source is binding internal standard or recommendation only.
5. ASBP compares the local source against baseline registry sources where overlap exists.
6. ASBP defaults to the stricter applicable requirement.
7. ASBP allows controlled override only with justification.
8. ASBP records citation limitations where clause/section references are missing.
9. ASBP does not claim the uploaded source is public regulation unless verified.

## 12. Validation Expectations

This closure path is currently documentation/governance-only.

No executable validation is required for this plan alone.

Executable validation becomes required if DDR-004 closure later adds:

- source registry data files consumed by runtime code
- citation validation functions
- applicability matching code
- conflict/stricter-rule selection logic
- override record validation
- standards-backed generation behavior
- standards retrieval/indexing behavior

Validation command when executable behavior is touched:

`python -m pytest -q`

## 13. Closure Evidence Checklist

`DDR-004` can move from `Open` to `Closure Planned` when:

- this plan is committed
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` updates `DDR-004` to `Closure Planned`
- Project Owner approval is recorded in repo evidence

`DDR-004` can move from `Closure Planned` to `Closed` only when repo evidence exists for:

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
- any executable validation required by implementation scope
- UAT/acceptance evidence where applicable

## 14. Current DDR-004 Decision

Current decision:

`Approved to start DDR-004 closure path.`

Current proposed register status after this plan is applied:

`Closure Planned`

Current blocked areas remain blocked until closure evidence is complete:

- standards-backed product output
- standards-backed CQV/GMP advice
- standards embedding
- standards retrieval
- audit-ready citation
- standards-backed document generation

## 15. Next Action After This Plan

After this plan is applied and committed, the next action should be one of:

1. create the actual standards registry structure as a repo artifact, or
2. update roadmap/checkpoint placement if Project Owner wants DDR closure checkpoints explicitly represented before M26.

Recommended next practical action:

`Create DDR-004 standards registry structure artifact.`
