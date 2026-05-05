---
doc_type: milestone_checkpoint_output
canonical_name: M15_COVERAGE_PACK_EXPANSION_FRAMEWORK
status: READY_FOR_REPO_APPLICATION
governs_execution: false
document_state_mode: checkpoint_output
authority: execution_evidence_candidate
checkpoint: M15.2
milestone: M15
phase: Phase 5 — Core Engine Completion
---

# M15.2 — Coverage-Pack Expansion Framework

## Checkpoint

`M15.2` — Coverage-pack expansion framework

## Purpose

This document records the M15.2 coverage-pack expansion framework.

The framework defines the bounded expansion unit for governed library growth before M15.3 through M15.5 add actual library content.

## Scope

M15.2 defines:

- a bounded coverage-pack model
- expansion-unit expectations
- coordination rules across multiple governed artifact families
- alignment with library taxonomy
- alignment with authored-source versus deployment-compiled separation rules

## Not in scope

M15.2 does not perform:

- selector content expansion
- task-pool content expansion
- calendar content expansion
- standards-bundle content expansion
- profile content expansion
- mapping metadata content expansion
- VALOR snapshot migration
- deployment compile pipeline implementation
- orchestration/service hardening
- CLI command expansion
- AI runtime behavior

## Implementation boundary

The M15.2 framework is implemented under:

`asbp/governed_library/`

The initial module is:

`asbp/governed_library/coverage_pack.py`

The package exports:

- coverage-pack baseline builder
- authored-source reference builder
- deployment-compiled reference builder
- coverage-pack builder
- reference validator
- coverage-pack validator

## Coverage-pack model

A coverage pack is the coordinated unit for governed library expansion.

A coverage pack may coordinate:

- selector/preset refs
- profile refs
- task-pool refs
- standards-bundle refs
- calendar refs
- planning-basis refs
- mapping metadata refs
- template refs
- deployment-compiled lookup refs

The pack defines coordination and linkage only. It does not contain asset payload content.

## Required coverage-pack fields

- `checkpoint`
- `contract_version`
- `coverage_pack_id`
- `coverage_pack_version`
- `coverage_pack_ref`
- `coverage_family`
- `variant_scope_layer`
- `coverage_pack_role`
- `expansion_unit_policy`
- `artifact_family_coordination_policy`
- `source_to_compiled_linkage_policy`
- `authored_source_refs`
- `deployment_compiled_refs`
- `standards_bundle_refs`
- `calendar_refs`
- `planning_basis_refs`
- `mapping_metadata_refs`
- `validation_status`
- `freeze_status`
- `content_policy`

## Source and compiled separation

The framework preserves two reference roles:

- `authored_source_truth_ref`
- `deployment_compiled_lookup_ref`

Authored-source refs remain source truth.

Deployment-compiled refs are runtime lookup refs only. They must link back to an included authored source ref and may not become source authority.

## Supported asset families

The coverage-pack framework uses the existing resolver/registry governed asset families:

- `template`
- `preset`
- `task_pool`
- `standards_bundle`
- `profile`
- `calendar`
- `planning_basis`
- `mapping_metadata`

## Validation behavior

The framework rejects:

- unsupported asset families
- empty required fields
- malformed version pins
- `latest`, `current`, or wildcard versions
- duplicate references
- missing authored-source references
- compiled references that pretend to be source authority
- compiled references that do not link to included authored source refs
- wrong-family refs in standards/calendar/planning-basis/mapping lists
- payload fields inside framework records
- adapter, orchestration, AI, or deployment-pipeline behavior inside M15.2

## Current checkpoint decision

M15.2 establishes the coverage-pack framework only.

The next checkpoint after implementation and validation is:

`M15.3` — Preset / selector library expansion
