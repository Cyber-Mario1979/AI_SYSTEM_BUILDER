PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& d:\02_Projects\Active\AI_SYSTEM_BUILDER\.venv\Scripts\Activate.ps1)
(.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # M11_UAT_Execution
(.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 1 — Verify the technical baseline before UAT execution
(.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> python -m pytest -q
.......................................................................................................................................................... [ 29%]
.......................................................................................................................................................... [ 58%]
.......................................................................................................................................................... [ 88%]
.............................................................. [100%]
524 passed in 45.49s
(.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 2 — Verify the canonical versioning surface
(.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'

> > from asbp.versioning import (
> > RELEASE_STATE,
> > RUNTIME_VERSION,
> > STATE_VERSION,
> > build_version_metadata,
> > )
> >
> > print(build_version_metadata())
> > print(RUNTIME_VERSION)
> > print(STATE_VERSION)
> > print(RELEASE_STATE)
> > '@ | python -
> > {'runtime_version': '0.1.0', 'state_version': '0.1.0', 'release_state': 'active_development'}
> > 0.1.0
> > 0.1.0
> > active_development
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 3 — Verify the retrieval architecture baseline and both allowed retrieval request families
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from asbp.retrieval import (
> > build_governed_retrieval_request,
> > build_probabilistic_search_retrieval_request,
> > build_retrieval_architecture_baseline,
> > )
> >
> > print("BASELINE:", build_retrieval_architecture_baseline())
> > print(
> > "GOVERNED:",
> > build_governed_retrieval_request(
> > artifact_kind="task_pool",
> > lookup_id="POOL-TABPRESS-001",
> > compiled_surface_id="compiled-task-pools-v1",
> > library_version="2026.04",
> > ),
> > )
> > print(
> > "PROBABILISTIC:",
> > build_probabilistic_search_retrieval_request(
> > query_text="tablet press FAT",
> > search_scope="uat_notes",
> > ),
> > )
> > '@ | python -
> > BASELINE: {'checkpoint': 'M11.4', 'resolver_registry_dependency': 'required_before_live_governed_retrieval', 'retrieval_categories': {'governed_deterministic': {'source_of_truth_role': 'downstream_consumer_only', 'target_surfaces': 'compiled_governed_lookup_only', 'allowed_future_purpose': 'version_pinned_governed_lookup', 'authority_boundary': 'may_not_redefine_source_authority'}, 'probabilistic_search': {'source_of_truth_role': 'non_authoritative_support_only', 'target_surfaces': 'search_or_index_surfaces_only', 'allowed_future_purpose': 'broad_search_support', 'authority_boundary': 'may_not_redefine_source_authority'}}}
> > GOVERNED: {'mode': 'governed_deterministic', 'artifact_kind': 'task_pool', 'lookup_id': 'POOL-TABPRESS-001', 'compiled_surface_id': 'compiled-task-pools-v1', 'library_version': '2026.04', 'source_of_truth_role': 'downstream_consumer_only'}
> > PROBABILISTIC: {'mode': 'probabilistic_search', 'query_text': 'tablet press FAT', 'search_scope': 'uat_notes', 'source_of_truth_role': 'non_authoritative_support_only'}
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 4 — Verify retrieval boundary rejection for prohibited governed-request fields
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from asbp.retrieval import validate_retrieval_request
> >
> > try:
> > validate_retrieval_request(
> > {
> > "mode": "governed_deterministic",
> > "artifact_kind": "task_pool",
> > "lookup_id": "POOL-TABPRESS-001",
> > "compiled_surface_id": "compiled-task-pools-v1",
> > "library_version": "2026.04",
> > "source_of_truth_role": "downstream_consumer_only",
> > "query_text": "this should not be allowed",
> > }
> > )
> > except Exception as exc:
> > print(type(exc).**name**)
> > print(exc)
> > '@ | python -
> > ValueError
> > query_text is not allowed in this retrieval mode.
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 5 — Verify the blocked runtime chain through the public runtime boundary surfaces
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from asbp.runtime.boundary import build_work_package_runtime_boundary_payload
> > from asbp.runtime.control import build_work_package_runtime_control_payload
> > from asbp.runtime.generation import build_work_package_generation_request_payload
> > from asbp.runtime.handoff import build_work_package_llm_handoff_payload
> > from asbp.runtime.prompt_contract import build_work_package_prompt_contract_payload
> > from asbp.state_model import WorkPackageModel
> >
> > work_packages = [
> > >> WorkPackageModel(
> > >> wp_id="WP-001",
> > >> title="Tablet press qualification",
> > >> status="open",
> > >> )
> > >> ]
> >
> > print(
> > "BOUNDARY:",
> > build_work_package_runtime_boundary_payload(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "PROMPT_CONTRACT:",
> > build_work_package_prompt_contract_payload(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "HANDOFF:",
> > build_work_package_llm_handoff_payload(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "CONTROL:",
> > build_work_package_runtime_control_payload(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "GENERATION:",
> > build_work_package_generation_request_payload(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > ),
> > )
> > '@ | python -
> > BOUNDARY: {'wp_id': 'WP-001', 'runtime_boundary_state': 'deterministic_blocked', 'eligible_for_prompt_contract': False, 'selected_plan_id': None, 'deterministic_facts': {'work_package_status': 'open', 'orchestration_stage': 'binding_context_required', 'blocking_conditions': ['selector_context_missing'], 'next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'selector_context_ready': False, 'work_package_task_ids': [], 'bound_committed_collection_ids': [], 'bound_committed_task_ids': [], 'plan_ids': []}, 'model_may': ['consume only validated deterministic facts exposed through this boundary payload', 'transform those facts into bounded language outputs only after a future prompt contract is defined', 'return only fields explicitly requested by a future runtime contract'], 'model_may_not': ['mutate persisted state', 'invent facts, statuses, dates, dependencies, or identifiers', 'change selected work package, selected plan, task scope, or collection scope', 'resolve blocked deterministic state by inference', 'bypass deterministic validation or acceptance rules']}
> > PROMPT_CONTRACT: {'wp_id': 'WP-001', 'prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'prompt_contract_state': 'blocked', 'prompt_contract_mode': 'blocked_explainer', 'eligible_for_prompt_contract': False, 'required_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'expected_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred'], 'runtime_boundary': {'wp_id': 'WP-001', 'runtime_boundary_state': 'deterministic_blocked', 'eligible_for_prompt_contract': False, 'selected_plan_id': None, 'deterministic_facts': {'work_package_status': 'open', 'orchestration_stage': 'binding_context_required', 'blocking_conditions': ['selector_context_missing'], 'next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'selector_context_ready': False, 'work_package_task_ids': [], 'bound_committed_collection_ids': [], 'bound_committed_task_ids': [], 'plan_ids': []}, 'model_may': ['consume only validated deterministic facts exposed through this boundary payload', 'transform those facts into bounded language outputs only after a future prompt contract is defined', 'return only fields explicitly requested by a future runtime contract'], 'model_may_not': ['mutate persisted state', 'invent facts, statuses, dates, dependencies, or identifiers', 'change selected work package, selected plan, task scope, or collection scope', 'resolve blocked deterministic state by inference', 'bypass deterministic validation or acceptance rules']}}
> > HANDOFF: {'wp_id': 'WP-001', 'handoff_metadata': {'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'handoff_state': 'blocked', 'generation_allowed': False, 'selected_plan_id': None, 'prompt_contract_state': 'blocked', 'prompt_contract_mode': 'blocked_explainer'}, 'structured_facts': {'work_package_status': 'open', 'orchestration_stage': 'binding_context_required', 'blocking_conditions': ['selector_context_missing'], 'next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'selector_context_ready': False, 'work_package_task_ids': [], 'bound_committed_collection_ids': [], 'bound_committed_task_ids': [], 'plan_ids': []}, 'prose_generation_instructions': {'response_mode': 'blocked_explainer', 'writing_goal': 'Explain why generation cannot proceed yet using only the structured facts, blockers, and next actions in this handoff payload.', 'required_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'grounded_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred']}}
> > CONTROL: {'wp_id': 'WP-001', 'handoff_metadata': {'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'handoff_state': 'blocked', 'generation_allowed': False, 'selected_plan_id': None, 'prompt_contract_state': 'blocked', 'prompt_contract_mode': 'blocked_explainer'}, 'runtime_control_metadata': {'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'runtime_control_state': 'blocked_explainer_only', 'control_action': 'explain_blocked_state', 'generation_allowed': False, 'operator_response_allowed': True, 'selected_plan_id': None, 'allowed_response_modes': ['blocked_explainer'], 'default_response_mode': 'blocked_explainer'}, 'structured_facts': {'work_package_status': 'open', 'orchestration_stage': 'binding_context_required', 'blocking_conditions': ['selector_context_missing'], 'next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'selector_context_ready': False, 'work_package_task_ids': [], 'bound_committed_collection_ids': [], 'bound_committed_task_ids': [], 'plan_ids': []}, 'prose_generation_instructions': {'response_mode': 'blocked_explainer', 'writing_goal': 'Explain why generation cannot proceed yet using only the structured facts, blockers, and next actions in this handoff payload.', 'required_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'grounded_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred']}}
> > GENERATION: {'wp_id': 'WP-001', 'generation_surface_metadata': {'generation_surface_id': 'work_package_controlled_generation_surface_v1', 'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'generation_state': 'blocked', 'generation_allowed': False, 'operator_response_allowed': True, 'runtime_control_state': 'blocked_explainer_only', 'control_action': 'explain_blocked_state', 'allowed_response_modes': ['blocked_explainer'], 'generation_mode': 'blocked_explainer', 'generation_scope': 'single_work_package_operator_response', 'selected_plan_id': None}, 'deterministic_input': {'handoff_metadata': {'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'handoff_state': 'blocked', 'generation_allowed': False, 'selected_plan_id': None, 'prompt_contract_state': 'blocked', 'prompt_contract_mode': 'blocked_explainer'}, 'runtime_control_metadata': {'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'runtime_control_state': 'blocked_explainer_only', 'control_action': 'explain_blocked_state', 'generation_allowed': False, 'operator_response_allowed': True, 'selected_plan_id': None, 'allowed_response_modes': ['blocked_explainer'], 'default_response_mode': 'blocked_explainer'}, 'structured_facts': {'work_package_status': 'open', 'orchestration_stage': 'binding_context_required', 'blocking_conditions': ['selector_context_missing'], 'next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'selector_context_ready': False, 'work_package_task_ids': [], 'bound_committed_collection_ids': [], 'bound_committed_task_ids': [], 'plan_ids': []}}, 'generation_instructions': {'writing_goal': 'Explain why generation cannot proceed yet using only the structured facts, blockers, and next actions in this handoff payload.', 'grounded_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred']}, 'output_contract': {'required_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'field_types': {'response_mode': 'string', 'operator_message': 'string', 'recommended_next_actions': 'list[string]', 'grounded_input_fields_used': 'list[string]'}}, 'candidate_response_template': {'response_mode': 'blocked_explainer', 'operator_message': '', 'recommended_next_actions': [], 'grounded_input_fields_used': []}}
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 6 — Verify candidate-response validation and retry/fail behavior for a valid blocked-state candidate
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from asbp.runtime.output_validation import validate_work_package_candidate_response
> > from asbp.runtime.retry_fail import evaluate_work_package_candidate_response_attempt
> > from asbp.state_model import WorkPackageModel
> >
> > work_packages = [
> > >> WorkPackageModel(
> > >> wp_id="WP-001",
> > >> title="Tablet press qualification",
> > >> status="open",
> > >> )
> > >> ]
> >
> > candidate_output = {
> > "response_mode": "blocked_explainer",
> > "operator_message": "Generation cannot proceed until selector context is completed.",
> > "recommended_next_actions": [
> > >> "Complete deterministic selector context before orchestration can proceed."
> > >> ],
> > "grounded_input_fields_used": [
> > >> "wp_id",
> > >> "deterministic_facts.orchestration_stage",
> > >> "deterministic_facts.blocking_conditions",
> > >> "deterministic_facts.next_actions",
> > >> ],
> > }
> >
> > print(
> > "VALIDATION:",
> > validate_work_package_candidate_response(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > ),
> > )
> > print(
> > "RETRY_FAIL:",
> > evaluate_work_package_candidate_response_attempt(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > attempt_number=1,
> > max_attempts=2,
> > ),
> > )
> > '@ | python -
> > VALIDATION: {'wp_id': 'WP-001', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'validation_state': 'accepted', 'expected_response_mode': 'blocked_explainer', 'candidate_response_mode': 'blocked_explainer', 'errors': [], 'validated_output': {'response_mode': 'blocked_explainer', 'operator_message': 'Generation cannot proceed until selector context is completed.', 'recommended_next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'grounded_input_fields_used': ['wp_id', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions']}}
> > RETRY_FAIL: {'wp_id': 'WP-001', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'validation_state': 'accepted', 'decision_state': 'accepted', 'fallback_action': 'use_validated_output', 'retry_policy': {'attempt_number': 1, 'max_attempts': 2, 'retries_remaining': 1}, 'decision_rationale': ['validated_output_accepted'], 'validation_errors': [], 'validated_output': {'response_mode': 'blocked_explainer', 'operator_message': 'Generation cannot proceed until selector context is completed.', 'recommended_next_actions': ['Complete deterministic selector context before orchestration can proceed.'], 'grounded_input_fields_used': ['wp_id', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions']}}
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 7 — Verify output acceptance and output retry behavior for a contract-breaking blocked-state candidate
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from asbp.runtime.output_acceptance import validate_work_package_output_before_acceptance
> > from asbp.runtime.output_retry import evaluate_work_package_output_attempt
> > from asbp.state_model import WorkPackageModel
> >
> > work_packages = [
> > >> WorkPackageModel(
> > >> wp_id="WP-001",
> > >> title="Tablet press qualification",
> > >> status="open",
> > >> )
> > >> ]
> >
> > candidate_output = {
> > "response_mode": "execution_ready_summary",
> > "operator_message": "",
> > "recommended_next_actions": "not-a-list",
> > "grounded_input_fields_used": [
> > >> "wp_id",
> > >> "disallowed.field",
> > >> ],
> > "extra_field": "unexpected",
> > }
> >
> > print(
> > "ACCEPTANCE:",
> > validate_work_package_output_before_acceptance(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > ),
> > )
> > print(
> > "OUTPUT_RETRY:",
> > evaluate_work_package_output_attempt(
> > work_packages,
> > [],
> > [],
> > [],
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > attempt_number=1,
> > max_attempts=2,
> > ),
> > )
> > '@ | python -
> > ACCEPTANCE: {'wp_id': 'WP-001', 'output_acceptance_metadata': {'output_acceptance_id': 'work_package_output_acceptance_v1', 'output_mapping_id': 'work_package_output_mapping_v1', 'output_contract_id': 'work_package_operator_response_contract_v1', 'validation_state': 'rejected', 'acceptance_ready': False, 'current_response_mode': 'blocked_explainer', 'selected_plan_id': None}, 'errors': ['Unexpected output fields: extra_field', 'response_mode must be one of: blocked_explainer', "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'", 'operator_message must be a non-empty string.', 'recommended_next_actions must be a list of strings.', 'grounded_input_fields_used contains disallowed fields: disallowed.field'], 'validated_output': None}
> > OUTPUT_RETRY: {'wp_id': 'WP-001', 'output_retry_metadata': {'output_retry_id': 'work_package_output_retry_v1', 'output_acceptance_id': 'work_package_output_acceptance_v1', 'output_mapping_id': 'work_package_output_mapping_v1', 'output_contract_id': 'work_package_operator_response_contract_v1', 'validation_state': 'rejected', 'decision_state': 'retry_allowed', 'regeneration_action': 'request_regenerated_output_from_same_mapping_contract', 'current_response_mode': 'blocked_explainer', 'selected_plan_id': None}, 'retry_policy': {'attempt_number': 1, 'max_attempts': 2, 'retries_remaining': 1}, 'decision_rationale': ['validation_rejected_but_retry_budget_remaining'], 'validation_errors': ['Unexpected output fields: extra_field', 'response_mode must be one of: blocked_explainer', "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'", 'operator_message must be a non-empty string.', 'recommended_next_actions must be a list of strings.', 'grounded_input_fields_used contains disallowed fields: disallowed.field'], 'validated_output': None}
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > from datetime import datetime, timezone
> >
> > from asbp.runtime.control import build_work_package_runtime_control_payload
> > from asbp.runtime.generation import build_work_package_generation_request_payload
> > from asbp.runtime.output_acceptance import validate_work_package_output_before_acceptance
> > from asbp.runtime.output_retry import evaluate_work_package_output_attempt
> > from asbp.runtime.output_target import build_work_package_output_target_payload
> > from asbp.state_model import (
> > PlanningBasisModel,
> > PlanningCalendarModel,
> > PlanningModel,
> > SelectorContextModel,
> > TaskCollectionModel,
> > TaskModel,
> > WorkPackageModel,
> > )
> >
> > work_packages = [
> > WorkPackageModel(
> > wp_id="WP-001",
> > title="Tablet press qualification",
> > status="open",
> > selector_context=SelectorContextModel(
> > preset_id="oral-solid-dose-standard",
> > scope_intent="qualification-only",
> > standards_bundles=["cqv-core", "automation"],
> > ),
> > )
> > ]
> >
> > task_collections = [
> > TaskCollectionModel(
> > collection_id="TC-001",
> > title="Committed Selection",
> > collection_state="committed",
> > work_package_id="WP-001",
> > task_ids=["TASK-001"],
> > )
> > ]
> >
> > tasks = [
> > >> TaskModel(
> > >> task_id="TASK-001",
> > >> order=1,
> > >> title="Prepare FAT",
> > >> duration=1,
> > >> work_package_id="WP-001",
> > >> status="planned",
> > >> )
> > >> ]
> >
> > plans = [
> > PlanningModel(
> > plan_id="PLAN-001",
> > work_package_id="WP-001",
> > plan_state="committed",
> > planning_basis=PlanningBasisModel(
> > duration_source="task_duration",
> > ),
> > planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
> > planning_calendar=PlanningCalendarModel(
> > working_days=["monday", "wednesday", "friday"],
> > workday_hours=8,
> > workmonth_mode="calendar_month",
> > ),
> > )
> > ]
> >
> > candidate_output = {
> > "response_mode": "execution_ready_summary",
> > "operator_message": "The work package is ready for generation using the selected committed plan.",
> > "recommended_next_actions": [
> > >> "Execution-ready deterministic state reached."
> > >> ],
> > "grounded_input_fields_used": [
> > >> "wp_id",
> > >> "selected_plan_id",
> > >> "deterministic_facts.orchestration_stage",
> > >> "deterministic_facts.plan_ids",
> > >> ],
> > }
> >
> > print(
> > "CONTROL:",
> > build_work_package_runtime_control_payload(
> > work_packages,
> > task_collections,
> > tasks,
> > plans,
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "GENERATION:",
> > build_work_package_generation_request_payload(
> > work_packages,
> > task_collections,
> > tasks,
> > plans,
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "TARGET:",
> > build_work_package_output_target_payload(
> > work_packages,
> > task_collections,
> > tasks,
> > plans,
> > wp_id="WP-001",
> > ),
> > )
> > print(
> > "ACCEPTANCE:",
> > validate_work_package_output_before_acceptance(
> > work_packages,
> > task_collections,
> > tasks,
> > plans,
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > ),
> > )
> > print(
> > "OUTPUT_RETRY:",
> > evaluate_work_package_output_attempt(
> > work_packages,
> > task_collections,
> > tasks,
> > plans,
> > wp_id="WP-001",
> > candidate_output=candidate_output,
> > attempt_number=1,
> > max_attempts=2,
> > ),
> > )
> > '@ | python -
> > CONTROL: {'wp_id': 'WP-001', 'handoff_metadata': {'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'handoff_state': 'ready_for_generation', 'generation_allowed': True, 'selected_plan_id': 'PLAN-001', 'prompt_contract_state': 'ready', 'prompt_contract_mode': 'execution_ready_summary'}, 'runtime_control_metadata': {'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'runtime_control_state': 'execution_ready_summary_only', 'control_action': 'summarize_execution_ready_state', 'generation_allowed': True, 'operator_response_allowed': True, 'selected_plan_id': 'PLAN-001', 'allowed_response_modes': ['execution_ready_summary'], 'default_response_mode': 'execution_ready_summary'}, 'structured_facts': {'work_package_status': 'open', 'orchestration_stage': 'execution_ready', 'blocking_conditions': [], 'next_actions': ['Execution-ready deterministic state reached.'], 'selector_context_ready': True, 'work_package_task_ids': ['TASK-001'], 'bound_committed_collection_ids': ['TC-001'], 'bound_committed_task_ids': ['TASK-001'], 'plan_ids': ['PLAN-001']}, 'prose_generation_instructions': {'response_mode': 'execution_ready_summary', 'writing_goal': 'Summarize execution-ready deterministic state for the operator using only the structured facts in this handoff payload.', 'required_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'grounded_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred']}}
> > GENERATION: {'wp_id': 'WP-001', 'generation_surface_metadata': {'generation_surface_id': 'work_package_controlled_generation_surface_v1', 'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'generation_state': 'ready', 'generation_allowed': True, 'operator_response_allowed': True, 'runtime_control_state': 'execution_ready_summary_only', 'control_action': 'summarize_execution_ready_state', 'allowed_response_modes': ['execution_ready_summary'], 'generation_mode': 'execution_ready_summary', 'generation_scope': 'single_work_package_operator_response', 'selected_plan_id': 'PLAN-001'}, 'deterministic_input': {'handoff_metadata': {'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'handoff_state': 'ready_for_generation', 'generation_allowed': True, 'selected_plan_id': 'PLAN-001', 'prompt_contract_state': 'ready', 'prompt_contract_mode': 'execution_ready_summary'}, 'runtime_control_metadata': {'runtime_control_id': 'work_package_runtime_control_v1', 'handoff_contract_id': 'work_package_llm_handoff_v1', 'source_prompt_contract_id': 'work_package_runtime_prompt_contract_v1', 'runtime_control_state': 'execution_ready_summary_only', 'control_action': 'summarize_execution_ready_state', 'generation_allowed': True, 'operator_response_allowed': True, 'selected_plan_id': 'PLAN-001', 'allowed_response_modes': ['execution_ready_summary'], 'default_response_mode': 'execution_ready_summary'}, 'structured_facts': {'work_package_status': 'open', 'orchestration_stage': 'execution_ready', 'blocking_conditions': [], 'next_actions': ['Execution-ready deterministic state reached.'], 'selector_context_ready': True, 'work_package_task_ids': ['TASK-001'], 'bound_committed_collection_ids': ['TC-001'], 'bound_committed_task_ids': ['TASK-001'], 'plan_ids': ['PLAN-001']}}, 'generation_instructions': {'writing_goal': 'Summarize execution-ready deterministic state for the operator using only the structured facts in this handoff payload.', 'grounded_input_fields': ['wp_id', 'runtime_boundary_state', 'eligible_for_prompt_contract', 'selected_plan_id', 'deterministic_facts.work_package_status', 'deterministic_facts.orchestration_stage', 'deterministic_facts.blocking_conditions', 'deterministic_facts.next_actions', 'deterministic_facts.selector_context_ready', 'deterministic_facts.work_package_task_ids', 'deterministic_facts.bound_committed_collection_ids', 'deterministic_facts.bound_committed_task_ids', 'deterministic_facts.plan_ids'], 'prohibited_freeform_drift': ['omit required output fields', 'add output fields outside the declared contract', 'invent facts outside the validated deterministic inputs', 'change or reinterpret blocking conditions', 'change selected plan, task scope, or collection scope', 'propose state mutation as if it already occurred']}, 'output_contract': {'required_output_fields': ['response_mode', 'operator_message', 'recommended_next_actions', 'grounded_input_fields_used'], 'field_types': {'response_mode': 'string', 'operator_message': 'string', 'recommended_next_actions': 'list[string]', 'grounded_input_fields_used': 'list[string]'}}, 'candidate_response_template': {'response_mode': 'execution_ready_summary', 'operator_message': '', 'recommended_next_actions': [], 'grounded_input_fields_used': []}}
> > TARGET: {'wp_id': 'WP-001', 'output_target_metadata': {'output_target_id': 'work_package_operator_response_target_v1', 'output_target_family': 'single_work_package_operator_response', 'target_scope': 'single_work_package', 'target_audience': 'operator', 'delivery_format': 'chat_text', 'target_state': 'available', 'generation_surface_id': 'work_package_controlled_generation_surface_v1', 'selected_plan_id': 'PLAN-001', 'generation_allowed': True, 'operator_response_allowed': True, 'runtime_control_state': 'execution_ready_summary_only'}, 'allowed_response_modes': ['execution_ready_summary'], 'current_response_mode': 'execution_ready_summary', 'target_boundaries': {'multi_work_package_output': False, 'document_artifact_output': False, 'file_export_output': False}}
> > ACCEPTANCE: {'wp_id': 'WP-001', 'output_acceptance_metadata': {'output_acceptance_id': 'work_package_output_acceptance_v1', 'output_mapping_id': 'work_package_output_mapping_v1', 'output_contract_id': 'work_package_operator_response_contract_v1', 'validation_state': 'accepted', 'acceptance_ready': True, 'current_response_mode': 'execution_ready_summary', 'selected_plan_id': 'PLAN-001'}, 'errors': [], 'validated_output': {'response_mode': 'execution_ready_summary', 'operator_message': 'The work package is ready for generation using the selected committed plan.', 'recommended_next_actions': ['Execution-ready deterministic state reached.'], 'grounded_input_fields_used': ['wp_id', 'selected_plan_id', 'deterministic_facts.orchestration_stage', 'deterministic_facts.plan_ids']}}
> > OUTPUT_RETRY: {'wp_id': 'WP-001', 'output_retry_metadata': {'output_retry_id': 'work_package_output_retry_v1', 'output_acceptance_id': 'work_package_output_acceptance_v1', 'output_mapping_id': 'work_package_output_mapping_v1', 'output_contract_id': 'work_package_operator_response_contract_v1', 'validation_state': 'accepted', 'decision_state': 'accepted', 'regeneration_action': 'use_validated_output', 'current_response_mode': 'execution_ready_summary', 'selected_plan_id': 'PLAN-001'}, 'retry_policy': {'attempt_number': 1, 'max_attempts': 2, 'retries_remaining': 1}, 'decision_rationale': ['validated_output_accepted'], 'validation_errors': [], 'validated_output': {'response_mode': 'execution_ready_summary', 'operator_message': 'The work package is ready for generation using the selected committed plan.', 'recommended_next_actions': ['Execution-ready deterministic state reached.'], 'grounded_input_fields_used': ['wp_id', 'selected_plan_id', 'deterministic_facts.orchestration_stage', 'deterministic_facts.plan_ids']}}
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 9 — Verify the M11.6 wrapper cleanup preserved explicit exports and package-aligned public surfaces
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> @'
> > import asbp.runtime as runtime_pkg
> > import asbp.runtime.boundary as runtime_boundary_module
> > import asbp.runtime.contracts as runtime_contracts_module
> > import asbp.runtime.generation as runtime_generation_module
> > import asbp.runtime.output_retry as runtime_output_retry_module
> > import asbp.retrieval as retrieval_pkg
> >
> > print("RUNTIME_BOUNDARY_ALL:", runtime_boundary_module.**all**)
> > print("RUNTIME_CONTRACTS_ALL:", runtime_contracts_module.**all**)
> > print("RUNTIME_GENERATION_ALL:", runtime_generation_module.**all**)
> > print("RUNTIME_OUTPUT_RETRY_ALL:", runtime_output_retry_module.**all**)
> > print("RUNTIME_PACKAGE_HAS_OUTPUT_RETRY:", hasattr(runtime_pkg, "evaluate_work_package_output_attempt"))
> > print("RETRIEVAL_ALL:", retrieval_pkg.**all**)
> > '@ | python -
> > RUNTIME_BOUNDARY_ALL: ['build_work_package_runtime_boundary_payload']
> > RUNTIME_CONTRACTS_ALL: ['EXPECTED_OUTPUT_FIELDS', 'GENERATION_SURFACE_ID', 'HANDOFF_CONTRACT_ID', 'MODEL_MAY', 'MODEL_MAY_NOT', 'OUTPUT_FIELD_TYPES', 'PROMPT_CONTRACT_ID', 'PROHIBITED_FREEFORM_DRIFT', 'REQUIRED_INPUT_FIELDS', 'build_candidate_response_template', 'build_generation_state', 'build_handoff_state', 'build_output_contract', 'build_prompt_contract_state_and_mode', 'build_prose_generation_instructions', 'build_runtime_boundary_state']
> > RUNTIME_GENERATION_ALL: ['build_work_package_generation_request_payload']
> > RUNTIME_OUTPUT_RETRY_ALL: ['evaluate_work_package_output_attempt']
> > RUNTIME_PACKAGE_HAS_OUTPUT_RETRY: True
> > RETRIEVAL_ALL: ['GOVERNED_DETERMINISTIC_RETRIEVAL_MODE', 'GOVERNED_SOURCE_OF_TRUTH_ROLE', 'PROBABILISTIC_SEARCH_RETRIEVAL_MODE', 'PROBABILISTIC_SOURCE_OF_TRUTH_ROLE', 'build_governed_retrieval_request', 'build_probabilistic_search_retrieval_request', 'build_retrieval_architecture_baseline', 'validate_retrieval_request']
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> # Step 10 — Re-run the full validation baseline after UAT execution
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER> python -m pytest -q
> > .......................................................................................................................................................... [ 29%]
> > .......................................................................................................................................................... [ 58%]
> > .......................................................................................................................................................... [ 88%]
> > .............................................................. [100%]
> > 524 passed in 42.83s
> > (.venv) PS D:\02_Projects\Active\AI_SYSTEM_BUILDER>
