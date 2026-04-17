---
doc_type: canonical_roadmap_amendment_draft
canonical_name: ROADMAP_CANONICAL_v3_AMENDMENT_DRAFT
status: DRAFT_FOR_REVIEW
target_file: ROADMAP_CANONICAL.md
intended_result: ROADMAP_CANONICAL v3
supersedes_on_approval: ROADMAP_CANONICAL v2
---

# ROADMAP_CANONICAL v3 — Amendment Draft

## Amendment Intent

This amendment updates the canonical roadmap so the upstream source-of-work model becomes explicit and governable.

This is a permanent product-model clarification, not a temporary overlay.

It preserves the existing deterministic core while making the following distinctions explicit:

- presets and selector context are true upstream binding seeds
- task pools or equivalent source libraries are authoritative work-definition sources when the preset-driven path is used
- persisted `tasks` are instantiated execution records, not the only possible upstream work-definition source
- task collections operate on instantiated task records
- planning operates on committed instantiated tasks, not directly on library definitions

This draft is intentionally delta-scoped.
It is meant to amend the existing canonical roadmap rather than replace unrelated sections.

---

## Strategic Change Summary

The canonical roadmap must now explicitly distinguish between:

1. **source definitions**
   - presets
   - selector presets
   - task pools
   - profiles
   - calendars
   - standards bundles

2. **instantiated execution records**
   - persisted tasks attached to execution context

3. **workflow-state containers**
   - source / staged / committed / refined collections over instantiated task records

4. **derived downstream artifacts**
   - planning state
   - schedule outputs
   - later runtime-generated outputs

This amendment preserves the current deterministic execution core and introduces the missing source-of-work clarification above it.

---

## Replacement Block 1 — Front Matter

Replace the current front matter in `ROADMAP_CANONICAL.md` with:

```md
---
doc_type: canonical_roadmap
canonical_name: ROADMAP_CANONICAL
status: ACTIVE_APPROVED
governs_execution: true
document_state_mode: state_agnostic
authority: canonical_strategic_source_of_truth
version: v3
supersedes: ROADMAP_CANONICAL v2
---
```
