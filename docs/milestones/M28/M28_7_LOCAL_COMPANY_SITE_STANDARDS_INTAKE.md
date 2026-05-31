---
doc_type: milestone_evidence_record
canonical_name: M28_7_LOCAL_COMPANY_SITE_STANDARDS_INTAKE
status: IMPLEMENTED_PENDING_VALIDATION
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone: M28
checkpoint: M28.7
checkpoint_title: Local/company/site standards intake
execution_mode: Hybrid
application_mode: user_applied_package
live_repo_write: NO
---

# M28.7 — Local / Company / Site Standards Intake

## Purpose

M28.7 creates the controlled intake contract for user-provided local, company, site, and client standards.

This checkpoint prevents uploaded or internal standards from being treated as public regulation, verified authority, mandatory acceptance criteria, or productized standards-backed output unless the required authority decision, comparison path, limitation handling, and approval evidence exist.

## Execution Mode

Hybrid.

This checkpoint creates source-contract assets, tests, and governance evidence.

## Implementation / Source Minimum

M28.7 adds:

- `asbp/standards_intake_model.py`
- `tests/test_standards_intake_model.py`

The implementation minimum is a local/company/site/client standards intake contract covering:

- controlled `STD-LOCAL-*`, `STD-COMPANY-*`, `STD-SITE-*`, and `STD-CLIENT-*` source IDs;
- source metadata capture;
- authority decision status;
- verification status;
- applicability scope and conditions;
- citation-depth limits;
- source location;
- mandatory-flag handling;
- comparison path linkage to M28.5;
- override path linkage to M28.6 when a less-strict internal/local requirement is selected;
- visible limitations for draft, TBD, user-provided, pending, or recommendation-only records;
- explicit public-regulation non-claim controls;
- explicit non-implementation limits.

A narrative evidence file alone is not sufficient for M28.7 completion.

## Anti-Drift Gate

| Field | M28.7 position |
|---|---|
| Execution mode | Hybrid |
| Implementation minimum | Local/company/site/client standards intake model/contract plus tests |
| Governance boundary | Internal/user-provided standards may be captured and approved only within controlled boundaries; they are not public regulation |
| Validation evidence required | `python -m pytest -q` is required because this package adds source-contract validation behavior and tests |
| Tracker movement rule | Tracker may advance only after the intake contract exists, user-provided/internal-source limits remain explicit, and validation is run and recorded truthfully |
| Explicit non-implementation claims | M28.7 does not parse uploaded files, mutate the runtime registry, verify public-regulation status, implement retrieval/embedding, or generate product-ready standards output |

## Intake Contract Summary

The intake model defines:

| Contract area | Control |
|---|---|
| Source identity | Intake records must use controlled local/company/site/client source IDs. |
| Source metadata | Intake captures source name, type, owner, location, version/effective date, applicability scope, applicability conditions, citation depth, and mandatory flag. |
| Authority decision | Binding internal use requires approved internal authority decision with decision owner, decision reference, and rationale. |
| Limitation handling | Draft, TBD, user-provided, pending, unavailable, recommendation-only, or internally approved sources must keep limitations visible. |
| Comparison linkage | Mandatory internal use requires a completed M28.5 comparison path. |
| Override linkage | Less-strict internal/local source selection requires the M28.6 override path where completed. |
| Public regulation boundary | Local/company/site/client standards intake must not claim public regulation status in M28.7. |

## Source Coverage

| Source inspected | Found | Role |
|---|---:|---|
| `ROADMAP_CANONICAL.md` | Yes | Defines M28.7 execution mode, completion minimum, validation/review requirement, tracker rule, and not-allowed boundary. |
| `docs/standards/STANDARDS_SOURCE_REGISTRY.md` | Yes | Supplies local/company/site intake flow, source-record metadata expectations, authority/verification limitations, and public-regulation non-claim boundary. |
| `asbp/standards_requirement_comparison_model.py` | Yes | Supplies M28.5 comparison path identity and less-strict selection boundary used by intake. |
| `asbp/standards_override_model.py` | Yes | Supplies M28.6 override identity and non-equivalence boundary used by intake. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | Yes | Confirms DDR-004 relevance and DDR-005 / DDR-006 awareness. |
| `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md` | Yes | Requires hybrid/build-content checkpoints to include implementation/source evidence and validation where applicable. |
| `PROGRESS_TRACKER.md` | Yes | Confirms M28.7 as the next normal roadmap checkpoint after M28.6 validation. |

## DDR Disposition

M28.7 remains under:

- DDR-004 for standards source/citation authority model scope;
- DDR-005 awareness because retrieval/embedding remains deferred to M30;
- DDR-006 awareness because product-ready generation/rendering remains planned for M29.

This checkpoint does not close, reopen, downgrade, or reclassify any DDR.

## Validation Expectation

After applying this package, run:

    python -m pytest -q

Do not advance `PROGRESS_TRACKER.md` from M28.7 to M28.8 until the intake model/contract, tests, explicit internal-source limits, and validation evidence are present.

## Explicit Non-Implementation Claims

M28.7 does not implement:

- file upload handling;
- OCR or parsing of uploaded standards documents;
- runtime registry mutation;
- standards retrieval or embedding;
- public-regulation verification;
- legal or regulatory approval;
- product-ready standards output;
- standards-backed CQV/GMP advice;
- standards-backed document generation;
- document rendering, export, or report generation;
- UI/API behavior;
- AI/model/provider behavior;
- deployment, productization, or SaaS readiness;
- M28 UAT;
- M28 closeout.

## Tracker Movement Rule

Tracker advancement is not included in this package.

A later tracker update may be prepared only after validation evidence is available or after an unresolved validation state is explicitly recorded.
