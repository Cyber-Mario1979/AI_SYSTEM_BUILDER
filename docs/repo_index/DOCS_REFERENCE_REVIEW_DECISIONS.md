---
doc_type: repo_index_review_decision_record
canonical_name: DOCS_REFERENCE_REVIEW_DECISIONS
status: PROPOSED_FOR_OWNER_REVIEW
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
milestone_context: M29
checkpoint_context: M29.12 blocker / repository index control
review_scope: docs/reference
execution_mode: Governance / review-only
application_mode: user_applied_package
live_repo_write: NO
tracker_movement: NO
---

# Docs Reference Review Decisions

## Purpose

This document records the first folder-bounded review of the `docs/reference/` folder following the Docs Folder Index pass.

This is a review/control record only. It does not delete, rename, archive, promote, or modify any reviewed source document.

## Current Control State

- M29.12 remains blocked.
- The CQV content-library remediation waves are completed through Wave 8.
- The next required control action remains full repository indexing / index review before returning to UAT or further build continuation.
- This review is part of the repository index control path, not M29.12 acceptance and not build continuation.

## Reviewed Folder

`docs/reference/`

Tracked files reviewed:

| # | Path | Review decision | Rationale | Proposed follow-up |
|---:|---|---|---|---|
| 1 | `docs/reference/asbp_runtime_cheat_sheet.md` | Cleanup / archive candidate | The file declares itself non-authoritative and points source of truth to repo code, roadmap, guardrails, and tracker. Its embedded execution state is obsolete compared with the current M29.12 blocker / remediation state. | Owner review: archive or remove later. Do not use as active execution reference. |
| 2 | `docs/reference/M11_3_VERSIONING_DISCIPLINE.md` | Keep as historical/reference for now | The file contains useful versioning discipline and identifies `asbp/versioning.py` as the canonical version source for its checkpoint scope. However, it is scoped to the Phase 4 / M11.3 window, so it should not be promoted as current authority without checking current code and roadmap alignment. | Keep as reference. Later review for promotion only if current code and roadmap still support it. |
| 3 | `docs/reference/M11_4_RETRIEVAL_ARCHITECTURE_BASICS.md` | Keep as future-relevant reference / M30 review candidate | The file defines retrieval boundary concepts, separates governed deterministic retrieval from probabilistic support search, and protects source authority. It is relevant to future retrieval/indexing work but should not become active authority until the M30 retrieval/indexing scope is reviewed. | Keep as reference. Re-review during M30 retrieval/indexing planning for possible promotion or update. |

## Owner Decision Needed

The Project Owner should confirm or revise the following review decisions:

1. `asbp_runtime_cheat_sheet.md` should not remain an active execution reference.
2. `M11_3_VERSIONING_DISCIPLINE.md` should remain reference-only for now.
3. `M11_4_RETRIEVAL_ARCHITECTURE_BASICS.md` should remain reference-only until M30 retrieval/indexing review.

## Boundaries

This review does not:

- delete files;
- move files;
- rename files;
- promote files to authoritative/canonical status;
- update the tracker;
- accept M29.12 UAT;
- close M29.12;
- close M29;
- return to build continuation;
- authorize productization, deployment, release, or SaaS readiness.

## Suggested Next Review Scope

After owner review of this decision record, the next docs review scope should be:

`docs/design_future/` and `docs/design_notes/`

These folders contain likely promotion candidates and should be reviewed before broader cleanup or canonicalization decisions.
