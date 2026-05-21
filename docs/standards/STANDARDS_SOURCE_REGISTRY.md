---
doc_type: standards_registry
canonical_name: STANDARDS_SOURCE_REGISTRY
status: ACTIVE_APPROVED
governs_execution: false
document_state_mode: source_authority_model
authority: standards_source_registry
source_ddr: DDR-004
source_closure_plan: docs/milestones/M25/DDR_004_STANDARDS_SOURCE_REGISTRY_AND_CITATION_AUTHORITY_PLAN.md
phase: Phase 9 — SaaS Readiness / Productization
milestone: M25 — SaaS Readiness Assessment
checkpoint: M25.DDR-004
approval_state: APPROVED_BY_PROJECT_OWNER
approved_by: Project Owner
approved_date: 2026-05-21
approval_basis: Project Owner approval during M25.DDR-004 closure review
registry_version: v0.1
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
- verification status model
- controlled placeholder and verification limitation rules
- citation model
- applicability model
- stricter-requirement precedence rule
- controlled override rule
- local/company/site standards intake model
- cleanroom local matrix capture
- registry lifecycle and change-control rules
- non-authority rule for embedding and retrieval

This file does not embed controlled standards text.

This file does not claim clause-level content unless the source and clause are verified.

This file is an approved live governance document for the DDR-004 standards registry and citation authority model.

This file does not mean that every listed source is verified, adopted, clause-mapped, version-confirmed, or approved for mandatory productized use.

## 2. Registry Status

Current registry status:

`ACTIVE_APPROVED`

Approval state:

`APPROVED_BY_PROJECT_OWNER`

Registry version:

`v0.1`

Approved date:

`2026-05-21`

The registry may be used as live governance evidence for the standards source registry and citation authority model.

It must not be treated as a final validated standards engine unless later executable validation is completed for any runtime behavior that consumes this registry.

`DDR-004` closure may confirm that ASBP has a controlled standards source registry and citation authority model.

`DDR-004` closure must not be interpreted to mean that every registered standard has been fully verified, adopted, clause-mapped, or approved for mandatory productized use.

Unverified, pending, TBD, or user-provided standards records may remain in this registry only as controlled candidate records subject to the rules in this file.

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
9. Pending, TBD, and user-provided source records must not support mandatory, audit-ready, clause-level, or productized standards-backed output until their authority and verification limitations are resolved or explicitly accepted.
10. Post-go-live standards registry amendments must be controlled through change control, impact assessment, approval, and forward revision. Historical approved evidence must be superseded or corrected, not silently overwritten.

## 4. Authority Status Model

| Authority status | Meaning                                                                                       | May drive mandatory output? |
| ---------------- | --------------------------------------------------------------------------------------------- | --------------------------: |
| `Authoritative`  | External regulatory, compendial, legal, or formally adopted standard applicable to the scope. |                         Yes |
| `Reference`      | Useful supporting source, not independently mandatory unless adopted by project/user/company. |          No, unless adopted |
| `Internal`       | Company/site/client/project standard approved as binding for the declared scope.              |                         Yes |
| `Recommendation` | Useful suggested practice or unverified matrix/rule; not binding.                             |                          No |
| `Draft`          | Source model or proposed rule under review.                                                   |                          No |
| `Retired`        | Historical source no longer active for new decisions.                                         |                          No |
| `TBD`            | Authority status not confirmed.                                                               |                          No |

Authority status is a controlled registry field.

It may be amended after trial, pilot, or go-live only through controlled registry change control, documented impact assessment, and approval.

Authority status changes must not silently alter historical outputs, historical decisions, validation records, UAT records, or released baselines.

## 5. Verification Status Model

| Verification status         | Meaning                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| `Verified`                  | Source identity/version/applicability has been confirmed against controlled evidence.       |
| `User-provided`             | User supplied the source/requirement; not independently verified yet.                       |
| `Pending verification`      | Source expected but version or applicability is not confirmed.                              |
| `Unavailable`               | Source details are not available.                                                           |
| `Not externally verifiable` | Internal/local/company source cannot be verified externally but may be approved internally. |

Verification status is a controlled registry field.

It may be amended after new source evidence, user approval, internal approval, external verification, supplier/client evidence, regulatory update, or source retirement.

A source with `Pending verification`, `User-provided`, `Unavailable`, or `TBD` limitations may remain in the registry, but those limitations must be visible wherever the source is used.

## 6. Controlled Placeholder and Verification Limitation Rule

This registry may contain controlled placeholder records.

A controlled placeholder is a source record where one or more fields are not yet fully verified, such as:

- version or effective date
- authority status
- verification status
- source location
- applicability conditions
- clause/section references
- internal approval status
- jurisdiction or owner
- mandatory flag

Controlled placeholders are allowed only when they are explicit and constrained.

A controlled placeholder must not be treated as final source authority.

A source record marked `Pending verification`, `TBD`, `User-provided`, `Unavailable`, `Draft`, or `Recommendation` must not be used to support:

- audit-ready citation
- clause-level citation
- mandatory acceptance criteria
- regulatory equivalence claims
- standards-backed product output
- standards-backed CQV/GMP advice
- standards-backed document generation
- standards embedding or retrieval authority
- productized compliance claims

Such records may be used only for:

- planning
- gap analysis
- source identification
- candidate applicability assessment
- user review
- internal/company standard intake
- preliminary comparison
- controlled future closure planning

If a pending or placeholder source is referenced, ASBP must state the limitation clearly.

Examples:

- `STD-ICH-Q9` and `STD-ICH-Q10` may remain `Reference` or become `Authoritative` only when adopted, required, or otherwise approved for the applicable scope.
- `STD-ISO-14644` may remain `Reference` or become `Authoritative` only when adopted, required, or selected as an acceptance basis for the applicable cleanroom scope.
- `STD-LOCAL-CLEANROOM-NONSTERILE` may remain `TBD` / `User-provided` until approved as `Internal` or downgraded to `Recommendation`.
- Any source with `TBD` version or effective date must not be used for audit-ready citation until the version/effective date is confirmed or the citation limitation is explicitly accepted.

## 7. Required Source Record Fields

Every standards source record must support these fields:

| Field                       |               Required? | Description                                                                                                                                    |
| --------------------------- | ----------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `std_id`                    |                     Yes | Stable source identifier.                                                                                                                      |
| `source_name`               |                     Yes | Human-readable source name.                                                                                                                    |
| `source_type`               |                     Yes | Regulation, standard, guideline, industry guide, internal standard, recommendation, site standard, client standard, or local authority source. |
| `authority_status`          |                     Yes | One of the authority statuses defined in this registry.                                                                                        |
| `verification_status`       |                     Yes | One of the verification statuses defined in this registry.                                                                                     |
| `version_or_effective_date` |     Required when known | Version, edition, effective date, or revision marker.                                                                                          |
| `jurisdiction_or_owner`     |     Required when known | EU, FDA, ICH, ISO, ASTM, ISPE, company, site, local authority, or client.                                                                      |
| `applicability_scope`       |                     Yes | Where the source may apply.                                                                                                                    |
| `applicability_conditions`  |  Required when relevant | Triggers or constraints for applicability.                                                                                                     |
| `citation_depth`            |                     Yes | Document-level, section-level, clause-level, table-row-level, or requirement-level.                                                            |
| `source_location`           | Required when available | Repo path, uploaded file reference, controlled document location, or user-provided reference.                                                  |
| `mandatory_flag`            |                     Yes | Whether ASBP may treat the source as mandatory inside the declared applicability boundary.                                                     |
| `notes`                     |                Optional | Limitations, warnings, or interpretation notes.                                                                                                |

## 8. Initial Standards Source Records

| STD ID                           | Source name                                                   | Source type                         | Authority status                                     | Verification status    | Version / effective date | Jurisdiction / owner                     | Initial applicability scope                                           | Citation depth                               |                  Mandatory flag | Notes                                                                          |
| -------------------------------- | ------------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------- | ---------------------- | ------------------------ | ---------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------- | ------------------------------: | ------------------------------------------------------------------------------ |
| `STD-EU-GMP-ANNEX-15`            | EU GMP Annex 15                                               | Regulation / GMP guidance           | `Authoritative` when applicable                      | `Pending verification` | `TBD`                    | EU GMP                                   | Qualification and validation expectations                             | Document / section / clause when verified    |             Yes when applicable | Version/effective date must be confirmed before audit-ready citation.          |
| `STD-EU-GMP-ANNEX-11`            | EU GMP Annex 11                                               | Regulation / GMP guidance           | `Authoritative` when applicable                      | `Pending verification` | `TBD`                    | EU GMP                                   | Computerised systems expectations                                     | Document / section / clause when verified    |             Yes when applicable | Applies when computerized systems are in scope.                                |
| `STD-EU-GMP-CHAPTER-4`           | EU GMP Chapter 4                                              | Regulation / GMP guidance           | `Authoritative` when applicable                      | `Pending verification` | `TBD`                    | EU GMP                                   | GMP documentation expectations                                        | Document / section / clause when verified    |             Yes when applicable | Applies to GMP documentation controls.                                         |
| `STD-ASTM-E2500`                 | ASTM E2500                                                    | Standard                            | `Reference` unless adopted as project authority      | `Pending verification` | `TBD`                    | ASTM                                     | Verification and science/risk-based approach                          | Document / section / clause when verified    |               No unless adopted | May support verification strategy; does not weaken mandatory GMP requirements. |
| `STD-ISPE-GAMP5`                 | ISPE GAMP 5                                                   | Industry guide                      | `Reference` unless adopted as project authority      | `Pending verification` | `TBD`                    | ISPE                                     | Computerised systems validation and assurance                         | Document / section / clause when verified    |               No unless adopted | May support approach; mandatory status depends on project/company adoption.    |
| `STD-FDA-21CFR11`                | 21 CFR Part 11 — Electronic Records; Electronic Signatures    | Regulation                          | `Authoritative` when applicable                      | `Pending verification` | `TBD`                    | FDA / US CFR                             | Electronic records and electronic signatures                          | Document / section / clause when verified    |             Yes when applicable | Applies only when relevant records/signatures fall under the scope.            |
| `STD-ICH-Q9`                     | ICH Q9 — Quality Risk Management                              | Guideline                           | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD`                    | ICH                                      | Quality risk management and risk-based decisions                      | Document / section / clause when verified    |      No unless adopted/required | Risk-based rationale must not weaken mandatory requirements.                   |
| `STD-ICH-Q10`                    | ICH Q10 — Pharmaceutical Quality System                       | Guideline                           | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD`                    | ICH                                      | PQS expectations, governance, change control, CAPA                    | Document / section / clause when verified    |      No unless adopted/required | May support PQS/governance framing.                                            |
| `STD-ISO-14644`                  | ISO 14644 — Cleanrooms and Associated Controlled Environments | Standard                            | `Reference` or `Authoritative` when adopted/required | `Pending verification` | `TBD`                    | ISO                                      | Cleanroom classification and testing references                       | Document / section / clause when verified    |      No unless adopted/required | Must be compared with GMP/local/site requirements where overlap exists.        |
| `STD-LOCAL-CLEANROOM-NONSTERILE` | Local non-sterile cleanroom classification and HVAC matrix    | Internal / recommendation candidate | `TBD`                                                | `User-provided`        | `TBD`                    | Project Owner / local or site source TBD | Non-sterile cleanroom areas, gowning, weighing, HVAC validation scope | Table-row-level until source document exists | No until approved as `Internal` | May become binding internal standard or remain recommendation only.            |

## 9. Local Cleanroom Matrix Record

Source ID:

`STD-LOCAL-CLEANROOM-NONSTERILE`

Current status:

`TBD / User-provided`

Current use:

Candidate internal/local standard or recommendation-only cleanroom matrix.

| Requirement ID | Element                     | Candidate requirement                                  | Applicability                                                | Initial citation                                          |
| -------------- | --------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------------------------- |
| `LOCAL-CR-001` | Room Classification         | ISO 8 / Grade D for gowning and weighing               | Non-sterile cleanroom scope where approved                   | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-001` |
| `LOCAL-CR-002` | Particle Limit              | `<= 3,520,000 particles >= 0.5 um/m^3` at rest         | Non-sterile cleanroom particle classification where approved | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-002` |
| `LOCAL-CR-003` | Pressure Cascade            | `10–15 Pa +/-5` between adjacent areas                 | Adjacent controlled areas where approved                     | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-003` |
| `LOCAL-CR-004` | ACH Requirement             | `15–20 Air Changes per Hour`                           | HVAC scope where approved                                    | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-004` |
| `LOCAL-CR-005` | Filtration Type             | HEPA H14 filters + prefilters + bag filters            | HVAC/filter scope where approved                             | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-005` |
| `LOCAL-CR-006` | Airflow Directionality      | Positive pressure zones for clean-to-less-clean flow   | Airflow/pressure zoning scope where approved                 | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-006` |
| `LOCAL-CR-007` | Filter Integrity Validation | Mandatory HEPA H14 leak test                           | HEPA integrity scope where approved                          | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-007` |
| `LOCAL-CR-008` | HVAC System Control         | Monitoring, alarms, BMS/SCADA control where applicable | Automated/monitored HVAC scope where approved                | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-008` |

Working interpretation:

- Do not treat Grade D as ISO Grade 9.
- Treat ISO 8 / Grade D as the intended local cleanroom classification relationship unless later evidence says otherwise.
- The local matrix may become binding only if approved as `Internal`.
- Without internal approval, it remains `Recommendation`.
- The local matrix must not support mandatory acceptance criteria, audit-ready citation, or productized standards-backed output while its authority status remains `TBD`.

## 10. Citation Model

ASBP must support these citation formats:

| Citation level    | Format                                 | Example                                                                 |
| ----------------- | -------------------------------------- | ----------------------------------------------------------------------- |
| Document-level    | `STD-ID`                               | `STD-EU-GMP-ANNEX-15`                                                   |
| Version-level     | `STD-ID@version/effective-date`        | `STD-EU-GMP-ANNEX-15@TBD`                                               |
| Section-level     | `STD-ID § <section>`                   | `STD-EU-GMP-ANNEX-15 § TBD`                                             |
| Clause-level      | `STD-ID § <section.clause>`            | `STD-FDA-21CFR11 § TBD`                                                 |
| Table-row-level   | `STD-ID table:<table-id> row:<row-id>` | `STD-LOCAL-CLEANROOM-NONSTERILE table:local-cleanroom row:LOCAL-CR-002` |
| Requirement-level | `STD-ID requirement:<requirement-id>`  | `STD-LOCAL-CLEANROOM-NONSTERILE requirement:LOCAL-CR-002`               |

Rules:

- ASBP must not fabricate clause or section numbers.
- If exact clause data is unavailable, use document-level, table-row-level, or requirement-level citation.
- If a source is user-provided and not verified, ASBP must state that limitation.
- Standards-backed output must show which source record is being used and why it applies.
- Citation depth must not exceed the verified evidence available for the source.
- A source with `TBD` version/effective date must not be used for audit-ready version-level citation unless the limitation is explicitly declared and accepted.

## 11. Applicability Model

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

A source with applicable scope still cannot drive mandatory output unless its authority status, verification status, and mandatory flag allow that use.

## 12. Stricter Requirement Precedence

When multiple applicable sources define requirements for the same acceptance point, ASBP must default to the stricter applicable requirement.

ASBP must explicitly identify:

- the overlapping sources
- the compared requirements
- which requirement is stricter
- which requirement is selected
- whether any user override was applied

Risk-based reasoning may support test rationale and scope decisions.

Risk-based reasoning must not silently reduce a mandatory applicable requirement.

The stricter-requirement rule applies only to sources that are applicable and allowed to drive mandatory output.

A pending, TBD, user-provided, reference-only, or recommendation-only source may be compared as planning evidence, but it must not be treated as mandatory unless approved or adopted through the registry authority model.

## 13. Controlled Override Record

A controlled override is required when the user selects a less strict requirement than another applicable source.

Minimum override record:

| Field                           |               Required? |
| ------------------------------- | ----------------------: |
| Override ID                     |                     Yes |
| Applicable sources compared     |                     Yes |
| Stricter requirement identified |                     Yes |
| Selected requirement            |                     Yes |
| Reason for override             |                     Yes |
| Risk / quality justification    |                     Yes |
| Applicability boundary          |                     Yes |
| Approver / decision owner       |                     Yes |
| Date or decision reference      | Required when available |
| Residual risk note              |  Required when relevant |

ASBP must warn the user when an override weakens a stricter applicable requirement.

ASBP must not treat override as source closure or regulatory equivalence.

## 14. User-Uploaded Standards Intake Flow

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
6. ASBP defaults to the stricter applicable requirement when the source is approved as applicable and mandatory.
7. ASBP allows controlled override only with justification.
8. ASBP records citation limitations where clause/section references are missing.
9. ASBP does not claim the uploaded/internal source is public regulation unless verified.

## 15. Registry Lifecycle and Change-Control Rule

The standards registry is a living controlled registry.

After trial, pilot, private use, local go-live, SaaS go-live, or any released baseline, registry amendments are expected and allowed only through controlled change control.

Change control is the first gate for any registry amendment.

The change-control process must determine:

- change classification
- impact on existing outputs
- impact on standards-backed advice
- impact on mandatory acceptance criteria
- impact on generated documents
- impact on validation and UAT evidence
- impact on audit-ready citation
- whether targeted testing is needed
- whether regression testing is needed
- whether partial or full re-validation is needed
- whether UAT or Project Owner re-approval is needed
- whether historical outputs must be superseded, corrected, or left unchanged with documented rationale

The following registry changes require documented impact assessment:

- `authority_status` change
- `verification_status` change
- `mandatory_flag` change
- citation-depth change
- applicability-scope change
- version/effective-date update
- source retirement
- source replacement
- local/company/site/client standard adoption
- local/company/site/client standard downgrade
- stricter-requirement interpretation change
- controlled override acceptance
- registry version release

Post-go-live registry amendments must create forward revisions.

Historical approved evidence must not be silently overwritten.

Historical generated outputs, validation records, UAT records, decision records, released baselines, and closed DDR evidence must be corrected, superseded, or referenced by a new version rather than edited as if the previous state never existed.

## 16. Registry Versioning Rule

Each accepted registry baseline should have a controlled version identifier.

Minimum versioning expectations:

| Field                       |                         Required? | Purpose                                            |
| --------------------------- | --------------------------------: | -------------------------------------------------- |
| Registry version            |                               Yes | Identifies the controlled source baseline.         |
| Effective date              |            Required when released | Identifies when the baseline applies.              |
| Approval status             |                               Yes | Draft, approved, released, retired, or superseded. |
| Approved by                 |            Required when approved | Identifies the decision owner.                     |
| Change reason               |            Required for revisions | Explains why the registry changed.                 |
| Supersedes                  |          Required when applicable | Identifies the prior registry baseline.            |
| Impact assessment reference | Required for post-go-live changes | Links the change to controlled impact review.      |

Any standards-backed output should record or be traceable to the registry version used when the output was created.

A later registry amendment must not retroactively change the authority basis of historical outputs unless a controlled impact assessment requires correction or supersession.

## 17. Document Approval Register Linkage

Approval for this document is disclosed in the document approval register.

The document approval register is an index and disclosure artifact.

It does not replace this document's own status, approval state, approved-by field, approved-date field, or version metadata.

If the approval register and this document disagree, the inconsistency must be corrected before relying on the approval state.

## 18. Embedding and Retrieval Non-Authority Rule

Embeddings, vector stores, retrieval indexes, search results, model memory, and AI-generated summaries are not standards authority.

They may assist retrieval and comparison only after source registry and citation authority are established.

`DDR-005` remains dependent on `DDR-004`.

Standards retrieval or embedding must not promote a pending, TBD, reference-only, recommendation-only, or user-provided source into mandatory authority.

## 19. Validation Expectations

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

## 20. DDR-004 Closure Evidence Contribution

This file contributes evidence toward:

- standards registry structure
- source metadata model
- source status model
- controlled placeholder handling
- verification limitation handling
- applicability model
- citation depth model
- stricter requirement rule
- controlled override rule
- local/company standard intake flow
- registry lifecycle and change-control rule
- registry versioning rule
- document approval register linkage
- embedding/retrieval non-authority rule
- validation expectations

`DDR-004` closure may confirm that the standards source registry and citation authority model exists.

`DDR-004` closure must not be interpreted as confirmation that every listed source is verified, adopted, version-confirmed, clause-mapped, or approved for productized mandatory use.

Remaining before `DDR-004` can be closed:

- register update to mark `DDR-004` as `Closed`, if approved
- tracker update after closure evidence is accepted
- validation evidence only if executable behavior is added
