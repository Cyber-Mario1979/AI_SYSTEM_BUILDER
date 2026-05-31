---
doc_type: repository_index
canonical_name: FULL_REPOSITORY_INDEX
status: GENERATED
governs_execution: false
document_state_mode: repository_index_evidence
authority: repo_index_control_evidence
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: Post-M29 repository index control before M30
execution_mode: Governance-only / repository-index control
source_branch: repo-index/full-repository-index-before-m30
source_commit: 2824bdc7a2190e5e84d0c0503d7f08590ff7a8dd
generated_utc: 2026-05-31T05:34:20+00:00
---

# Full Repository Index

## Purpose

This file records the full repository index control package required after M29.13 and before M30 planning.

This index is generated from tracked repository files using `git ls-files`.

## Scope

The full repository index covers the required post-M29 areas:

- root files;
- `.github/`;
- `asbp/`;
- `data/`;
- `tests/`;
- `docs/`, including reconciliation with the earlier docs-only index evidence.

## Required Coverage Check

| Area | Count | Status |
|---|---:|---|
| `root` | 9 | Covered |
| `.github` | 4 | Covered |
| `asbp` | 182 | Covered |
| `data` | 41 | Covered |
| `tests` | 149 | Covered |
| `docs` | 325 | Covered |

## Summary Counts

- Total tracked files indexed: 717
- Source branch: `repo-index/full-repository-index-before-m30`
- Source commit: `2824bdc7a2190e5e84d0c0503d7f08590ff7a8dd`
- Generated UTC: `2026-05-31T05:34:20+00:00`

### Counts by required area

| Required area | File count |
|---|---:|
| `"docs` | 1 |
| `.github` | 4 |
| `asbp` | 182 |
| `assets` | 1 |
| `audits` | 5 |
| `data` | 41 |
| `docs` | 325 |
| `root` | 9 |
| `tests` | 149 |

### Counts by role

| Role | File count |
|---|---:|
| Archived historical evidence | 15 |
| Change-control evidence | 4 |
| Documentation evidence — README.md | 1 |
| Documentation evidence — REPO_DOCS_RESTRUCTURE_MAP.md | 1 |
| Documentation evidence — REPO_DOCS_RESTRUCTURE_PLAN.md | 1 |
| Documentation evidence — REPO_DOCS_RESTRUCTURE_WAVE2_SUMMARY.md | 1 |
| Documentation evidence — cleanup | 1 |
| Documentation evidence — decision_gates | 2 |
| Documentation evidence — design_future | 2 |
| Documentation evidence — design_notes | 3 |
| Documentation evidence — design_spec | 44 |
| Documentation evidence — planning | 1 |
| Documentation evidence — reference | 3 |
| Documentation evidence — smoke_tests | 8 |
| Documentation evidence — standards | 1 |
| Gap assessment evidence | 1 |
| Governance evidence | 10 |
| Governed source data — calendars | 2 |
| Governed source data — controlled_drafting | 1 |
| Governed source data — document_input_schemas | 4 |
| Governed source data — document_lifecycle | 1 |
| Governed source data — document_template_bodies | 1 |
| Governed source data — document_templates | 1 |
| Governed source data — library_baseline | 1 |
| Governed source data — mappings | 2 |
| Governed source data — output_validation | 1 |
| Governed source data — planning_basis | 2 |
| Governed source data — profiles | 8 |
| Governed source data — renderer_output | 1 |
| Governed source data — standards_applicability | 1 |
| Governed source data — standards_backed_output | 1 |
| Governed source data — standards_bundles | 1 |
| Governed source data — standards_citation | 1 |
| Governed source data — standards_registry | 1 |
| Governed source data — task_pools | 8 |
| Governed source data — trial_documents | 2 |
| Issue template | 3 |
| Milestone evidence — M10 | 2 |
| Milestone evidence — M11 | 2 |
| Milestone evidence — M12 | 2 |
| Milestone evidence — M13 | 3 |
| Milestone evidence — M14 | 3 |
| Milestone evidence — M15 | 9 |
| Milestone evidence — M16 | 6 |
| Milestone evidence — M17 | 6 |
| Milestone evidence — M18 | 6 |
| Milestone evidence — M19 | 8 |
| Milestone evidence — M20 | 8 |
| Milestone evidence — M21 | 7 |
| Milestone evidence — M22 | 7 |
| Milestone evidence — M23 | 7 |
| Milestone evidence — M24 | 8 |
| Milestone evidence — M25 | 19 |
| Milestone evidence — M26 | 2 |
| Milestone evidence — M27 | 13 |
| Milestone evidence — M28 | 11 |
| Milestone evidence — M29 | 16 |
| Milestone evidence — M4 | 1 |
| Milestone evidence — M5 | 1 |
| Milestone evidence — M6 | 1 |
| Milestone evidence — M7 | 1 |
| Milestone evidence — M8 | 2 |
| Milestone evidence — M9 | 2 |
| Milestone evidence — README.md | 1 |
| Other tracked repository file | 7 |
| Pull request template | 1 |
| Pytest validation file | 149 |
| Remediation evidence | 10 |
| Repository data | 1 |
| Repository index/control evidence | 7 |
| Root repository file | 9 |
| Runtime module | 131 |
| Runtime/source contract model | 30 |
| Store/loader/persistence boundary | 21 |
| UAT evidence | 55 |

## Related Index Evidence

The earlier docs-only index evidence remains partial repository-index progress and is superseded only for full-repository coverage by this package:

- `docs/repo_index/DOCS_FOLDER_INDEX.md`
- `docs/repo_index/DOCS_FOLDER_INDEX.csv`
- `docs/repo_index/DOCS_FOLDER_TREE.md`
- `docs/repo_index/DOCS_CLEANUP_REVIEW_LIST.md`
- `docs/repo_index/DOCS_PROMOTION_CANDIDATES.md`
- `docs/repo_index/DOCS_INDEX_GENERATION_NOTES.md`
- `docs/repo_index/DOCS_REFERENCE_REVIEW_DECISIONS.md`

## Machine-Readable Inventory

The row-level inventory is stored in:

- `docs/repo_index/FULL_REPOSITORY_INDEX.csv`

## Tree Snapshot

The tracked file tree snapshot is stored in:

- `docs/repo_index/FULL_REPOSITORY_TREE.md`

## Governance Boundary

This index does not:

- start M30;
- implement retrieval;
- implement standards embedding;
- implement standards-backed live lookup;
- change runtime behavior;
- change source-library behavior;
- authorize productization, deployment, release, commercial launch, SaaS readiness, or customer-ready output;
- delete, archive, move, rename, promote, or canonicalize repository files;
- close DDR-005.

## Next Control Use

This index package can support tracker movement only after review confirms the required coverage and the completion gate remains accurate.
