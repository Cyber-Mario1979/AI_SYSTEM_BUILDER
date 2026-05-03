---
doc_type: milestone_checkpoint_output
canonical_name: M15_LIBRARY_GAP_ANALYSIS_AND_COVERAGE_AUDIT
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.1
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.1 — Library Gap Analysis and Coverage Audit

## Checkpoint

`M15.1` — Library gap analysis and coverage audit

## Purpose

This document records the M15.1 audit of current governed-library coverage and defines the first governed expansion map for Milestone 15.

This is a checkpoint output, not a new roadmap authority file.

## Authority and source role

Authoritative execution order remains:

1. `ROADMAP_CANONICAL.md`
2. active `ROADMAP_ADDENDUM_*.md` files, when present
3. `ARCHITECTURE_GUARDRAILS.md`
4. repo reality
5. `PROGRESS_TRACKER.md`

This audit uses repo reality and closed milestone evidence to identify gaps. It does not reopen M12, M13, or M14.

## M15.1 allowed-work mapping

The checkpoint permits:

- audit current preset coverage
- audit current task-pool coverage
- audit current calendar coverage
- audit current standards-bundle coverage
- audit profile and mapping coverage where applicable
- identify:
  - foundation gaps
  - content gaps
  - taxonomy gaps
  - validation gaps
  - deployment-compiled gaps
- produce a real governed expansion map

## Audited repo surfaces

The current audit reviewed these repo-real surfaces and design references:

- `PROGRESS_TRACKER.md`
- `ROADMAP_CANONICAL.md`
- `ROADMAP_CANONICAL_CONTINUATION_PART_1_PHASES_5_6.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/M12_CLOSEOUT_NOTES.md`
- `docs/M13_CLOSEOUT_NOTES.md`
- `docs/M14_CLOSEOUT_NOTES.md`
- `asbp/document_engine/*`
- `asbp/export_engine/*`
- `asbp/resolver_registry/*`
- resolver / registry tests
- document-engine tests
- export-engine tests
- design-future library expansion notes in `docs/design_future/PRE_M11_DESTINATION_ALIGNMENT_BLUEPRINT.md`
- existing VALOR library snapshot material under `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/`

## Current repo-real baseline

### M12 document-engine baseline

The repo has a governed document-engine boundary with:

- template governance
- document request/input/output contracts
- DCF intake and normalization
- controlled authoring modes
- standards/language/evidence guardrails
- document artifact lifecycle
- document lifecycle to task/workflow readiness logic

This is a strong contract baseline, but it is not yet a governed library expansion layer.

### M13 export/reporting baseline

The repo has a governed export/reporting boundary with:

- export request/payload/output contracts
- spreadsheet operational export surfaces
- Gantt/planning visualization surfaces
- dashboard/status summary surfaces
- reporting surface depth rules
- export invocation, validation, generated-artifact metadata, and acceptance rules

This is a strong output-engine baseline, but it does not define governed library content coverage.

### M14 resolver/registry baseline

The repo has a governed resolver/registry and governed data-layer boundary with:

- resolver/registry access boundary
- supported asset families
- version-pinned governed asset identity and lookup
- calendar and planning-basis resolution contracts
- authored-source versus deployment-compiled separation
- governed deterministic retrieval versus support retrieval separation

M14 intentionally excludes asset payload loading, asset content editing, library content expansion, support-retrieval execution, AI retrieval consumption, final rendering, calendar arithmetic, and planning calculation.

Therefore M15 starts from a mature lookup/resolution contract but not from a complete governed library system.

## Current coverage audit by governed asset family

### 1. Preset / selector coverage

Current state:

- Selector context is protected as a real binding seed from earlier design work.
- `preset_id`, `scope_intent`, and `standards_bundles` are protected as meaningful binding fields.
- Existing VALOR snapshot material contains context selector libraries for some coverage families, especially Process Equipment, Utilities, and Cleanroom examples.

Gap:

- No current ASBP-native authored selector library package or document exists as the active repo-real source of truth.
- No canonical ASBP selector schema is frozen for M15 expansion.
- No ASBP-native coverage-pack model links selectors to profiles, task pools, standards bundles, calendar, and mapping metadata.
- No deployment-compiled selector lookup manifest exists as a current governed runtime surface.

Classification:

- Foundation gap: yes
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 2. Task-pool coverage

Current state:

- The source-of-work model already distinguishes manual task records from preset-resolved task instantiation.
- `task_pool` is protected as an authoritative source-definition kind.
- `source_definition_id` is protected as the bridge from instantiated execution task back to source definition.
- Existing VALOR snapshot material contains task-pool-oriented bundle content for several domains.

Gap:

- No ASBP-native task-pool library schema is frozen as a current authored source.
- No active task-pool content is compiled into resolver/registry lookup surfaces.
- No task-pool-to-task instantiation compiler exists for governed library content.
- No complete validation layer checks task-pool row shape, identity, duration references, dependency references, document obligations, workflow compatibility, or downstream planning/export readiness.

Classification:

- Foundation gap: partial
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 3. Calendar coverage

Current state:

- M14 defines calendar family resolution contracts.
- Calendar resolution returns identity and planning-use metadata only.
- Calendar arithmetic, workday calculation, regional defaults, schedule generation, and rendering remain outside M14.

Gap:

- No ASBP-native authored calendar library content is frozen for M15.
- No regional or workweek calendar coverage set is currently expanded under ASBP governance.
- No calendar payload schema is frozen.
- No calendar validation/freeze discipline exists beyond resolver entry validation.
- No deployment-compiled calendar payload or lookup manifest exists.

Classification:

- Foundation gap: partial
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 4. Planning-basis coverage

Current state:

- M14 defines planning-basis resolution contracts.
- Planning-basis resolution exposes duration-source, dependency-source, and calendar-requirement metadata.
- Planning calculation remains outside resolver/registry.

Gap:

- No ASBP-native authored planning-basis library content is frozen.
- No profile-to-planning-basis bridge is finalized.
- No profile duration defaults are compiled into a planning-basis source.
- No end-to-end check confirms that selector/profile/task-pool/calendar references resolve into a complete planning-basis package.

Classification:

- Foundation gap: yes
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 5. Standards-bundle coverage

Current state:

- Standards bundles are protected as explicit bound context.
- The system direction treats standards bundles as governed context, not loose notes.
- M12 includes standards/language/evidence guardrails for document output behavior.

Gap:

- No ASBP-native standards-bundle library with versioned bundle records is currently frozen as an authored source.
- No standards-bundle-to-document-family mapping is compiled into the resolver/registry layer.
- No standards-bundle validation checks exist for bundle identity, supported document families, evidence requirements, applicability boundaries, or clause/reference placeholders.
- No deployment-compiled standards bundle manifest exists.

Classification:

- Foundation gap: partial
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 6. Profile coverage

Current state:

- Existing VALOR snapshot material contains profile library examples.
- The design direction expects profiles to coordinate duration defaults and coverage-specific operating assumptions.

Gap:

- No current ASBP-native profile schema is frozen.
- No active profile library content is compiled into governed lookup.
- No profile-to-calendar, profile-to-planning-basis, or profile-to-task-pool linkage validation exists.
- No deployment-compiled profile lookup manifest exists.

Classification:

- Foundation gap: yes
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 7. Mapping metadata coverage

Current state:

- M14 recognizes `mapping_metadata` as a governed asset family.
- Earlier design work identifies taxonomy and cross-link declarations as authored-source surfaces.

Gap:

- No ASBP-native mapping metadata schema is frozen.
- No mapping tables exist for selector-to-task-pool, selector-to-profile, standards-bundle applicability, document-obligation mapping, or export/report family mapping.
- No cross-library link validator exists.
- No compiled mapping table exists for runtime lookup.

Classification:

- Foundation gap: yes
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

### 8. Template coverage

Current state:

- M12 defines template governance and template retrieval behavior.
- M14 supports `template` as a version-pinned governed asset family.

Gap:

- No ASBP-native template library payload set is frozen.
- No versioned document template manifest exists for URS, DCF, protocol, report, or other governed document artifacts.
- No deployment-compiled template lookup manifest exists.
- No template-to-document-family validation bridge exists beyond request/template governance contracts.

Classification:

- Foundation gap: partial
- Content gap: yes
- Taxonomy gap: yes
- Validation gap: yes
- Deployment-compiled gap: yes

## Cross-family gap summary

| Gap type | Finding | Impact |
|---|---|---|
| Foundation gaps | Resolver/registry contracts exist, but ASBP-native authored library schemas and coverage-pack model are not frozen. | M15.2 must define the coverage-pack framework before content expansion. |
| Content gaps | Existing VALOR snapshot libraries are useful candidates but not current ASBP governed library truth. | M15.3–M15.5 must expand curated ASBP-native governed assets. |
| Taxonomy gaps | Artifact-kind-first taxonomy exists as design direction, but not yet as active repo-real M15 structure. | M15.2 must freeze artifact-kind, coverage-family, and variant/scope taxonomy. |
| Validation gaps | Existing validation is strong for contracts, identity, resolver entries, document, export, and runtime boundaries, but not for complete governed library packs. | M15.6 must introduce structural, identity/taxonomy, cross-library, and compiled-lookup validation. |
| Deployment-compiled gaps | M14 supports compiled lookup records, but no generated compiled library surfaces are present. | M15.6 must define freeze/release rules, and M15.7 must harden orchestration/service behavior on compiled governed assets. |

## Governed expansion map

### Expansion principle

M15 should not expand isolated assets one by one.

The expansion unit should be a bounded coverage pack.

A coverage pack should coordinate, where applicable:

- selector entries
- profile entries
- task-pool entries
- standards-bundle references or overlays
- calendar references
- planning-basis references
- mapping metadata
- template/document obligation mappings
- deployment-compiled lookup projections

### Recommended M15 sequence

#### M15.2 — Coverage-pack expansion framework

Define the governed coverage-pack model before expanding content.

Minimum required framework:

- `coverage_pack_id`
- `coverage_pack_version`
- `coverage_family`
- `variant_scope_layer`
- authored-source artifact refs
- standards-bundle refs
- calendar refs
- planning-basis refs
- mapping metadata refs
- deployment-compiled refs
- validation status
- freeze status
- source-to-compiled linkage rules

Deliverable:

- framework document and/or module defining the coverage-pack contract
- no large content expansion yet

#### M15.3 — Preset / selector library expansion

Expand authored selector/preset records using the coverage-pack framework.

Minimum required output:

- selector identity rules
- selector applicability fields
- selector binding refs
- selector-to-profile refs
- selector-to-task-pool refs
- selector-to-standards-bundle refs
- selector-to-calendar/planning-basis refs where applicable

Deliverable:

- ASBP-native selector/preset authored-source records for the first approved pilot coverage packs

#### M15.4 — Task-pool expansion

Expand governed task-pool source definitions.

Minimum required output:

- task-pool identity rules
- source-definition identity rules
- task definition row schema
- duration reference rules
- dependency reference rules
- document obligation references
- downstream instantiation compatibility rules

Deliverable:

- ASBP-native task-pool authored-source records for the first approved pilot coverage packs

#### M15.5 — Calendar / standards / profile / mapping expansion

Expand the supporting governed families that make selector/task-pool content executable and standards-aware.

Minimum required output:

- calendar family authored records
- planning-basis/profile records
- standards-bundle records
- mapping metadata records
- document obligation mapping
- cross-library link records

Deliverable:

- coordinated support-library content for the first approved pilot coverage packs

#### M15.6 — Library validation, freeze, and release discipline

Define and implement validation/freeze checks.

Minimum required checks:

- structural validity
- required-field validity
- duplicate identity rejection
- taxonomy validity
- cross-library linkage validity
- no dangling refs
- authored-source to deployment-compiled consistency
- deterministic compile output
- freeze manifest coherence

Deliverable:

- validation/freeze policy and supporting tests or validation helpers

#### M15.7 — Orchestration / service hardening on expanded governed assets

Harden runtime use of expanded governed assets without adapter leakage.

Minimum required behavior:

- orchestration/service layer consumes governed compiled lookup surfaces
- CLI remains an adapter only
- document/export invocation remains through approved boundaries
- mutation ordering and preflight validation remain deterministic
- support retrieval remains non-authoritative
- AI/runtime remains downstream and blocked until Phase 6

Deliverable:

- service/orchestration hardening over expanded assets

## Candidate pilot coverage packs for M15 planning

This audit does not approve content expansion yet, but it identifies safe candidates for the first coverage-pack decision in M15.2.

Candidate sources from current design/spec material:

| Candidate pack | Evidence source | Reason |
|---|---|---|
| Process Equipment — E2E / post-change style coverage | Existing VALOR PE library snapshot | Useful for CQV equipment flow and current user domain fit. |
| Utilities — commissioning / qualification style coverage | Existing VALOR UT library snapshot | Useful for utilities/HVAC/PWS-style workflows and standards/calendar linkage. |
| Cleanroom — qualification / periodic verification style coverage | Existing VALOR CR library snapshot | Useful for cleanroom/area workflows and standards-bundle pressure testing. |

Decision rule for M15.2:

- choose one pilot pack only for the first framework validation pass
- do not expand all domain content at once
- preserve authored-source versus compiled-output separation
- do not treat VALOR snapshot files as automatic ASBP source truth
- migrate or adapt only after M15.2 defines the ASBP coverage-pack contract

## M15.1 audit decision

M15.1 finds that:

1. The repo has strong governed contract foundations from M12, M13, and M14.
2. The repo does not yet have ASBP-native governed library coverage sufficient for M15 exit.
3. Existing VALOR snapshot material is a useful candidate input source, not live ASBP execution authority.
4. The next required checkpoint is `M15.2` — Coverage-pack expansion framework.
5. `M15.2` should define the coverage-pack model before any large content expansion is attempted.

## Validation note

This checkpoint output is documentation/audit-only.

No code changes are included in this checkpoint output.

`python -m pytest -q` was not run for this generated audit file. The latest verified validation status remains the tracker-recorded result: `724 passed in 51.47s`.

## Recommended repo path

Store this file as:

`docs/M15_LIBRARY_GAP_ANALYSIS_AND_COVERAGE_AUDIT.md`

## Tracker implication after repo application

After this file is added to the repository and accepted, the tracker may be updated to:

- Latest completed checkpoint: `M15.1` — Library gap analysis and coverage audit completed
- Exact next unfinished checkpoint: `M15.2` — Coverage-pack expansion framework
- Latest verified validation status: unchanged unless tests are run again
- Active note: M15.1 audit confirms strong M12–M14 foundations but identifies authored library, coverage-pack, validation, and deployment-compiled gaps requiring M15.2–M15.7 work
