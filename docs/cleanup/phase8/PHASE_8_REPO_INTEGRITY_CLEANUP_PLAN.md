# PHASE_8_REPO_INTEGRITY_CLEANUP_PLAN

## Cleanup lane

`cleanup/phase-8-repo-integrity`

## Plan status

Prepared for user-applied repository update.

This is a cleanup planning/classification document only.

It does not move files, delete files, rename files, refactor code, change tests, alter governance authority, close deferred dependencies, or begin Phase 9 work.

## Source assessment

Primary source:

`docs/milestones/M24/M24_6_PHASE_8_REPOSITORY_INTEGRITY_ASSESSMENT.md`

The source assessment decision was:

`Pass with no immediate cleanup implementation`.

This plan converts the assessment into cleanup-lane classification only.

## Generated context

Generated locally at:

`2026-05-20T22:14:09`

Local branch:

`cleanup/phase-8-repo-integrity`

Local status before applying this plan:

```text
?? apply_phase8_repo_integrity_cleanup_plan.py
```

Branch diff against `main` before applying this plan:

```text
(no diff against main before applying cleanup plan)
```

## Cleanup purpose

The purpose of this cleanup plan is to decide what, if anything, should be cleaned after Phase 8 closeout and before Phase 9 planning/implementation begins.

This plan does not implement cleanup.

Cleanup implementation requires a later explicit decision, scoped branch/PR boundary, and validation expectation.

## Classification lanes

Every finding must be handled through exactly one lane:

- repo hygiene
- public surface
- operation pack cleanup
- code cleanup/refactor
- tests cleanup
- future-phase deferred item
- no-action / acceptable

## Lane count summary

| Lane | File count |
|---|---:|
| code cleanup/refactor | 123 |
| future-phase deferred item | 6 |
| no-action / acceptable | 228 |
| public surface | 9 |
| repo hygiene | 1 |
| tests cleanup | 98 |

## File-family count summary

| File family | File count |
|---|---:|
| UAT evidence | 50 |
| archive | 8 |
| audit evidence | 5 |
| data/state | 1 |
| design/spec evidence | 44 |
| documentation | 38 |
| governance | 6 |
| milestone evidence | 69 |
| other | 6 |
| public/repo surface | 5 |
| repo workflow | 4 |
| source code | 123 |
| tests | 98 |
| validation evidence | 8 |

## File-by-file cleanup classification

| File | File family | Cleanup lane | Recommended action | Rationale |
|---|---|---|---|---|
| `"docs/design_spec/valor_pack_snapshot/source_zip/VAL\342\214\200R_v1.zip"` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | repo workflow | public surface | Review later only if needed | GitHub workflow/template surface. Public-surface cleanup must be separate. |
| `.github/ISSUE_TEMPLATE/design_question.md` | repo workflow | public surface | Review later only if needed | GitHub workflow/template surface. Public-surface cleanup must be separate. |
| `.github/ISSUE_TEMPLATE/documentation.md` | repo workflow | public surface | Review later only if needed | GitHub workflow/template surface. Public-surface cleanup must be separate. |
| `.github/PULL_REQUEST_TEMPLATE.md` | repo workflow | public surface | Review later only if needed | GitHub workflow/template surface. Public-surface cleanup must be separate. |
| `.gitignore` | public/repo surface | public surface | Review later only if needed | Repository-facing or package metadata surface. Do not mix with repo hygiene implementation. |
| `A07_5_Canonical_Roadmap_Continuation_Package.md` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `ARCHITECTURE_GUARDRAILS.md` | governance | no-action / acceptable | Keep | Active authority/tracker/roadmap material. Do not treat as cleanup target without roadmap/governance need. |
| `CODE_OF_CONDUCT.md` | public/repo surface | public surface | Review later only if needed | Repository-facing or package metadata surface. Do not mix with repo hygiene implementation. |
| `CONTRIBUTING.md` | public/repo surface | public surface | Review later only if needed | Repository-facing or package metadata surface. Do not mix with repo hygiene implementation. |
| `LICENSE` | public/repo surface | public surface | Review later only if needed | Repository-facing or package metadata surface. Do not mix with repo hygiene implementation. |
| `PROGRESS_TRACKER.md` | governance | no-action / acceptable | Keep | Active authority/tracker/roadmap material. Do not treat as cleanup target without roadmap/governance need. |
| `README.md` | public/repo surface | public surface | Review later only if needed | Repository-facing or package metadata surface. Do not mix with repo hygiene implementation. |
| `ROADMAP_ADDENDUM_08_PHASE_7_DETAILED_CHECKPOINT_LADDER.md` | governance | no-action / acceptable | Keep | Active authority/tracker/roadmap material. Do not treat as cleanup target without roadmap/governance need. |
| `ROADMAP_ADDENDUM_09_PHASE_8_DETAILED_CHECKPOINT_LADDER.md` | governance | no-action / acceptable | Keep | Active authority/tracker/roadmap material. Do not treat as cleanup target without roadmap/governance need. |
| `ROADMAP_CANONICAL.md` | governance | no-action / acceptable | Keep | Active authority/tracker/roadmap material. Do not treat as cleanup target without roadmap/governance need. |
| `ROADMAP_CANONICAL_CONTINUATION_PART_1_PHASES_5_6.md` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `ROADMAP_CANONICAL_CONTINUATION_PART_2_PHASES_7_9.md` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `asbp/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/__main__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/adapters/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/adapters/cli.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_evaluation/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_evaluation/evaluation_baseline.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_evaluation/quality_gates.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_evaluation/retrieval_use_rules.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_evaluation/standards_detail_checks.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_runtime/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_runtime/context_packaging.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_runtime/generation_modes.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_runtime/output_acceptance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_runtime/runtime_boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_workflow/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_workflow/recommendation_behavior.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_workflow/review_assistance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_workflow/summarization_reporting.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ai_workflow/workflow_expansion_boundaries.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/command_intake.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/read_surface.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/safety.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/api/service_boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/binding_context_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/cli.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/collection_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/binding_context.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/collections.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/models.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/planning.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/source_of_work.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/tasks.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/core/work_packages.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/artifact_lifecycle.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/authoring_controls.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/dcf_intake.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/document_contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/standards_guardrails.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/template_governance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/document_engine/workflow_integration.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/dashboard_surfaces.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/export_contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/export_invocation.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/gantt_surfaces.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/reporting_surfaces.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/export_engine/spreadsheet_surfaces.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/_normalization.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/acceptance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/consistency.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/external_surface/governance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/generation_surface_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/governed_library/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/governed_library/coverage_pack.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/governed_library/library_release_validation.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/governed_library/service_hardening.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/orchestration_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_acceptance_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_consistency_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_contract_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_failure_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_family_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_mapping_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_retry_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_surface_helpers.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_target_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_validation_helpers.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/output_validation_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/planning_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/prompt_contract_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/calendar_planning.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/identity.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/retrieval_boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/resolver_registry/source_compilation.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/retrieval/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/retrieval/contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/retry_decision_helpers.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/retry_fail_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/contracts.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/control.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/generation.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/handoff.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_acceptance.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_contract.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_mapping.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_retry.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_target.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/output_validation.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/prompt_contract.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime/retry_fail.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime_boundary_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime_control_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime_handoff_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/runtime_surface_helpers.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/services/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/services/orchestration.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/source_of_work_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/state/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/state/store.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/state_model.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/state_store.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/task_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/__init__.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/boundary.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/document_output_visibility.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/interaction_flow.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/operator_intake.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/safety.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/ui/workflow_visibility.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/versioning.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `asbp/work_package_logic.py` | source code | code cleanup/refactor | No action now | Code passed validation. Any cleanup/refactor must be separate and behavior-preserving. |
| `assets/banner.png` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `audits/ASBP_Audit_Closure_Note_001.md` | audit evidence | no-action / acceptable | Keep | Audit/review evidence. Preserve for traceability. |
| `audits/ASBP_Audit_Report_001.md` | audit evidence | no-action / acceptable | Keep | Audit/review evidence. Preserve for traceability. |
| `audits/ASBP_Audit_Response_001.md` | audit evidence | no-action / acceptable | Keep | Audit/review evidence. Preserve for traceability. |
| `audits/ASBP_Audit_Triage_Note_001.md` | audit evidence | no-action / acceptable | Keep | Audit/review evidence. Preserve for traceability. |
| `audits/M15_LIBRARY_GAP_ANALYSIS_AND_COVERAGE_AUDIT.md` | audit evidence | no-action / acceptable | Keep | Audit/review evidence. Preserve for traceability. |
| `data/state/state.json` | data/state | repo hygiene | Review later | Repository-tracked data/state should be reviewed before productization, but not changed in this planning pass. |
| `docs/M10_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M10_VALIDATION_CHECKPOINT.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M11_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M11_VALIDATION_CHECKPOINT.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M16_AI_RUNTIME_BOUNDARY.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M16_CONTEXT_PACKAGING.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M16_GENERATION_MODES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M16_OUTPUT_ACCEPTANCE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M17_AI_EVALUATION_BASELINE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M17_QUALITY_GATES_AND_GROUNDEDNESS.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M17_RETRIEVAL_USE_RULES_AND_SOURCE_ROLE_DISCIPLINE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M17_STANDARDS_CONFORMANCE_AND_DETAIL_CONSISTENCY.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M18_CONTROLLED_RECOMMENDATION_BEHAVIOR.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M18_CONTROLLED_REVIEW_ASSISTANCE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M18_CONTROLLED_SUMMARIZATION_AND_REPORTING_ASSISTANCE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M18_WORKFLOW_EXPANSION_BOUNDARIES_AND_REFUSAL_RULES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M4_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M5_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M6_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M7_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M8_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M8_VALIDATION_CHECKPOINT.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M9_CLOSEOUT_NOTES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/M9_VALIDATION_CHECKPOINT.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/README.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/REPO_DOCS_RESTRUCTURE_MAP.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/REPO_DOCS_RESTRUCTURE_PLAN.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/REPO_DOCS_RESTRUCTURE_WAVE2_SUMMARY.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/UAT/M10_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M10_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M11_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M11_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M12/M12_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M12/M12_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M12/README.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M13/M13_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M13/M13_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M13/README.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M14/M14_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M14/M14_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M14/README.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M15/M15_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M15/M15_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M15/README.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M16/M16_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M16/M16_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M17/M17_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M17/M17_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M18/M18_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M18/M18_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M19/M19_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M19/M19_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M20/M20_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M20/M20_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M21/M21_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M21/M21_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M22/M22_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M22/M22_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M23/M23_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M23/M23_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M24/M24_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M24/M24_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M4_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M4_UAT_Report.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M5_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M5_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M6_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M6_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M7_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M7_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M8_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M8_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M9_UAT_PROTOCOL.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/M9_UAT_REPORT.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/README.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/evidence/M11_UAT_EXECUTION_LOG.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/evidence/M8_UAT_EXECUTION_LOG.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/UAT/evidence/M9_UAT_EXECUTION_LOG.md` | UAT evidence | no-action / acceptable | Keep | UAT evidence. Preserve for traceability. |
| `docs/archives/design_notes/POST_M5_UAT_DESIGN_PATCH_PROPOSAL.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_01_TEST_INTEGRITY_RESTORATION.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_02_M5_ARCHITECTURAL_HARDENING.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_03_PRE_M8_PRESET_SOURCE_ALIGNMENT.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_04_M8_DESIGN_RESERVATIONS_GATE.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_05_PARALLEL_DESIGN_TRACK_GOVERNANCE.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_06_PRE_M11_DESTINATION_ALIGNMENT_AND_DESIGN_READINESS.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/archives/roadmap_addenda/ROADMAP_ADDENDUM_07_POST_M11_TRANSITION_AND_ROADMAP_EXTENSION_GATE.md` | archive | no-action / acceptable | Keep | Historical traceability. Archive material is acceptable unless a later archive hygiene package is approved. |
| `docs/decision_gates/POST_M17_PRE_M18_DOCUMENT_REENTRY_DECISION.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_future/PARALLEL_DESIGN_TRACK_REGISTER.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_future/PRE_M11_DESTINATION_ALIGNMENT_BLUEPRINT.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_notes/M8_DESIGN_ACKNOWLEDGMENTS.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_notes/checklists/ASBP_Design_Gate_Checklist_Pre_Milestone.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_notes/checklists/ASBP_Design_Maturity_Check_List.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/design_spec/ROADMAP_CANONICAL_v3_AMENDMENT_DRAFT.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_evaluation/M17_1_AI_EVALUATION_BASELINE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_evaluation/M17_2_QUALITY_GATES_AND_GROUNDEDNESS_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_evaluation/M17_3_STANDARDS_CONFORMANCE_AND_DETAIL_CONSISTENCY_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_evaluation/M17_4_RETRIEVAL_USE_RULES_AND_SOURCE_ROLE_DISCIPLINE.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_runtime/M16_1_AI_RUNTIME_BOUNDARY_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_runtime/M16_2_CONTEXT_PACKAGING_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_runtime/M16_3_GENERATION_MODE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_runtime/M16_4_OUTPUT_ACCEPTANCE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_workflow/M18_1_CONTROLLED_REVIEW_ASSISTANCE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_workflow/M18_2_CONTROLLED_SUMMARIZATION_AND_REPORTING_ASSISTANCE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_workflow/M18_3_CONTROLLED_RECOMMENDATION_BEHAVIOR_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/ai_workflow/M18_4_WORKFLOW_EXPANSION_BOUNDARIES_AND_REFUSAL_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/README.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_3_SELECTOR_SCOPE_EXPANSION_MAP.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_4_TASK_POOL_EXPANSION_MAP.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_5_SUPPORT_LIBRARY_EXPANSION_MAP.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_6_LIBRARY_RELEASE_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/M15_7_ORCHESTRATION_SERVICE_HARDENING_RULES.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/calendars/M15_5_CALENDAR_PLANNING_BASIS_DRAFT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/mapping/M15_5_CROSS_LIBRARY_MAPPING_DRAFT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/profiles/M15_5_PROFILES_DRAFT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/standards/M15_5_STANDARDS_APPLICABILITY_DRAFT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/expansion/task_pools/M15_4_TASK_POOLS_DRAFT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/01_orchestration/00_VALOR_Instructions_v1.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/01_orchestration/01_System_Core.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/01_orchestration/02_Orchestration_Core.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/01_orchestration/03_KS_Core.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/01_orchestration/04_Document_Core.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/02_contracts_and_schemas/ARCH_BUNDLE_Contracts_ActionBlocks_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/02_contracts_and_schemas/ARCH_BUNDLE_Schemas_v1.json` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/common/ARCH_BUNDLE_Libraries_COMMON_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/domain/ARCH_BUNDLE_Libraries_CR_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/domain/ARCH_BUNDLE_Libraries_CS_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/domain/ARCH_BUNDLE_Libraries_PE_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/03_libraries/domain/ARCH_BUNDLE_Libraries_UT_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/04_deployment_runtime/DEPLOYMENT_Runtime_Contracts_Addenda_v1.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/04_deployment_runtime/calendars/DEPLOYMENT_Canonical_Calendar_Workweek_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/04_deployment_runtime/presets/DEPLOYMENT_WP_Header_Presets_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/04_deployment_runtime/task_pools/DEPLOYMENT_TaskPools_All_v1.yaml` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/05_templates_and_exports/09_Valor_Export_Template.csv` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/05_templates_and_exports/ARCH_BUNDLE_DocumentTemplates_v1.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/06_reference_support/16_Valor_ID_Numbering_Spec.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/design_spec/valor_pack_snapshot/extracted/MANIFEST.md` | design/spec evidence | no-action / acceptable | Keep | Design/spec evidence. Preserve unless superseded by explicit cleanup decision. |
| `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` | governance | no-action / acceptable | Keep | Deferred-dependency/governance evidence. No cleanup action unless governance update is separately authorized. |
| `docs/milestones/M12/M12_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M12/README.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M13/M13_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M13/M13_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M13/README.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M14/M14_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M14/M14_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M14/README.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_COVERAGE_PACK_EXPANSION_FRAMEWORK.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_LIBRARY_VALIDATION_FREEZE_RELEASE.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_ORCHESTRATION_SERVICE_HARDENING.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_PRESET_SELECTOR_LIBRARY_EXPANSION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_SUPPORT_LIBRARY_EXPANSION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_TASK_POOL_EXPANSION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/M15_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M15/README.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M16/M16_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M16/M16_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M17/M17_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M17/M17_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M18/M18_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M18/M18_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_1_API_BOUNDARY_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_2_REQUEST_RESPONSE_CONTRACT_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_3_SERVICE_BOUNDARY_CONSUMPTION_RULES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_4_API_SAFETY_AND_ADAPTER_ISOLATION_RULES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_5_MINIMAL_API_READ_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_6_MINIMAL_API_COMMAND_INTAKE_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_7_API_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M19/M19_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_1_UI_BOUNDARY_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_2_UI_INTERACTION_FLOW_CONTRACT_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_3_GOVERNED_WORKFLOW_VISIBILITY_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_4_DOCUMENT_EXPORT_REPORTING_VISIBILITY_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_5_OPERATOR_ACTION_INTAKE_BOUNDARY.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_6_UI_SAFETY_AND_EXECUTION_TRUTH_SEPARATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_7_UI_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M20/M20_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_2_UI_API_CONSISTENCY_RULES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_5_VALIDATION_AND_ACCEPTANCE_DISCIPLINE.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_6_PHASE_7_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M21/M21_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_1_CLOUD_COMPUTE_BOUNDARY.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_2_RUNTIME_PLACEMENT_MODEL.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_3_ENVIRONMENT_BOUNDARY_MODEL.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_4_ENVIRONMENT_SEPARATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_5_CLOUD_ASSUMPTIONS_REGISTER.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_6_CLOUD_COMPUTE_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M22/M22_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_1_DEPLOYMENT_BOUNDARY_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_2_PACKAGING_STRATEGY_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_3_CONFIGURATION_BOUNDARY_MODEL.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_4_ARTIFACT_BOUNDARY_MODEL.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_5_GOVERNED_SOURCE_ASSETS_VS_DEPLOYABLE_OPERATIONAL_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_6_DEPLOYMENT_PACKAGING_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M23/M23_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_1_OPERATIONAL_HARDENING_BOUNDARY_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_2_OBSERVABILITY_DIRECTION_FOUNDATION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_3_RUNTIME_HEALTH_AND_FAILURE_GOVERNANCE_SURFACES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_4_OPERATIONAL_VALIDATION_DIRECTION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_5_PRE_GO_LIVE_READINESS_BOUNDARY_AND_DEPENDENCY_DISPOSITION.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_6_PHASE_8_REPOSITORY_INTEGRITY_ASSESSMENT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_6_PHASE_8_VALIDATION_CHECKPOINT.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/M24/M24_PHASE_8_CLOSEOUT_NOTES.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/milestones/README.md` | milestone evidence | no-action / acceptable | Keep | Milestone/checkpoint/validation/closeout evidence. Size alone is not a cleanup defect. |
| `docs/planning/UI_PRELIMINARY_BOUNDARIES.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/reference/M11_3_VERSIONING_DISCIPLINE.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/reference/M11_4_RETRIEVAL_ARCHITECTURE_BASICS.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/reference/asbp_runtime_cheat_sheet.md` | documentation | no-action / acceptable | Keep | Supporting documentation. No immediate cleanup action. |
| `docs/smoke_tests/M6.7B_Result.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/M6.7C_Result.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/M6_7A_Result.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/M6_7A_Smoke_Test_Protocol.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/M6_7B_Smoke_Test_Protocol.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/M6_7C_Smoke_Test_Protocol.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/README.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `docs/smoke_tests/smoke_test_interim_M5.md` | validation evidence | no-action / acceptable | Keep | Historical smoke-test evidence. Preserve unless replaced by a later evidence consolidation plan. |
| `requirements.txt` | other | future-phase deferred item | Review later | Unclassified path. Do not touch until a targeted cleanup decision is made. |
| `tests/test_ai_evaluation_baseline.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_quality_gates.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_recommendation_behavior.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_retrieval_use_rules.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_review_assistance.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_runtime_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_runtime_context_packaging.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_runtime_generation_modes.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_runtime_output_acceptance.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_standards_detail_checks.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_summarization_reporting.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ai_workflow_expansion_boundaries.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_command_intake.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_contracts.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_read_surface.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_safety.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_api_service_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_collection_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_collection_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_collection_persistence_validation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_collection_work_package_relationships.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_collection_work_package_update_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_artifact_lifecycle.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_authoring_controls.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_dcf_intake.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_document_contracts.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_standards_guardrails.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_template_governance.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_document_engine_workflow_integration.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_contracts.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_dashboard_surfaces.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_gantt_surfaces.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_invocation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_reporting_surfaces.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_export_engine_spreadsheet_surfaces.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_external_surface_acceptance.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_external_surface_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_external_surface_consistency.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_external_surface_contracts.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_external_surface_governance.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_generation_surface_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_generation_surface_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_governed_library_coverage_pack.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_governed_library_release_validation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_governed_library_service_hardening.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_1_production_structure_baseline.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_3_versioning_discipline.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_4_retrieval_architecture_basics.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_5a_runtime_control_hardening.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_5c_maintainability_hardening.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m11_6_architecture_cleanup_consolidation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m8_5c_cross_entity_validation_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_m8_7_cross_entity_surface_consolidation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_orchestration_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_acceptance_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_consistency_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_contract_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_failure_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_family_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_mapping_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_retry_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_target_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_validation_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_output_validation_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_planning_foundation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_prompt_contract_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_prompt_contract_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_resolver_registry_asset_identity.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_resolver_registry_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_resolver_registry_calendar_planning.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_resolver_registry_retrieval_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_resolver_registry_source_compilation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_retry_fail_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_retry_fail_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_runtime_boundary_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_runtime_boundary_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_runtime_handoff_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_runtime_handoff_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_source_of_work_foundation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_state_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_task_clear_work_package_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_task_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_task_logic.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_task_work_package_conflict_validation_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_task_work_package_persistence_validation.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_boundary.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_document_output_visibility.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_interaction_flow.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_operator_intake.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_safety.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_ui_workflow_visibility.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_delete_membership_validation_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_list_by_task_id_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_list_show_task_ids_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_model.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |
| `tests/test_work_package_show_task_ids_cli.py` | tests | tests cleanup | Review later only if needed | Tests passed. Do not reorganize now; future test cleanup should be separate. |

## Recommended cleanup decisions

### Immediate implementation

Recommended immediate implementation: `None`.

Reason:

- Phase 8 validation passed.
- Phase 8 repository integrity assessment passed with no immediate cleanup implementation.
- Most large documentation/evidence areas are traceability assets, not cleanup defects.
- Cleanup implementation now would create PR noise unless a specific bounded defect is chosen.

### Repo hygiene candidates for later review

Potential later review items:

- `data/` tracked state/sample data role before productization.
- `docs/design_spec/valor_pack_snapshot/source_zip/` snapshot/generated-like material.
- Any odd archived/snapshot path that appears generated or imported from an external pack.

Recommendation:

Defer to a later bounded repo-hygiene package only if there is a clear benefit and traceability is preserved.

### Public surface candidates for later review

Potential later review items:

- `README.md`
- `docs/README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `.github/` templates

Recommendation:

Do not mix public-surface cleanup with repo hygiene. Use a separate public-surface package if desired.

### Code cleanup/refactor candidates

Current decision: no action.

Reason:

- Code validation passed.
- Cleanup branch should not refactor code unless a specific bounded code cleanup is separately planned.

### Tests cleanup candidates

Current decision: no action.

Reason:

- Test suite passed.
- Test cleanup should be a separate tests cleanup lane if needed.

### Future-phase deferred items

Current decision: carry forward.

Reason:

- Deferred dependency items remain governed by `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`.
- Phase 9 planning must review unresolved dependencies before implementation.

## Recommended PR boundary

Recommended PR type:

`repo hygiene cleanup planning`

Recommended branch:

`cleanup/phase-8-repo-integrity`

Recommended PR scope:

- Add this cleanup plan only.
- Do not perform cleanup implementation in the same PR.

Recommended validation:

No `pytest` required for this planning-only document.

If the user wants optional assurance:

    python -m pytest -q

## Decision

Decision: `Cleanup planning complete; no immediate cleanup implementation recommended`.

## Next step after this plan

Recommended next ASBP action after merging this cleanup planning PR:

`Post-Phase-8 / Pre-Phase-9 roadmap expansion and deferred-dependency review gate`

## Generation note

Generated as a user-applied local planning package.

Live repository write: `NO`.
