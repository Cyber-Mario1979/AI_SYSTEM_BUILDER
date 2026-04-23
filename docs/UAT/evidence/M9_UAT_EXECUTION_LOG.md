PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Dev\GitHub\AI_SYSTEM_BUILDER\.venv\Scripts\Activate.ps1)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> #M9_UAT execution
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Test pre setup
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> if (Test-Path '.\data\state\state.json') {
>>     Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.original.bak') -Force
>> }
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> if (Test-Path '.\data\state\candidate_response.json') {
>>     Copy-Item '.\data\state\candidate_response.json' (Join-Path $backupDir 'candidate_response.original.bak') -Force
>> }
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 2 — Initialize a clean controlled UAT state
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state init
State initialized at: C:\Dev\GitHub\AI_SYSTEM_BUILDER\data\state\state.json
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state set-status in_flight
State status updated to: in_flight
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state show
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.1.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [],
  "task_collections": [],
  "plans": []
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 3 — Create the blocked Work Package baseline
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-001 "Tablet press qualification"
Work Package added: WP-001 - Tablet press qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state show
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.1.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification",
      "status": "open",
      "selector_context": null
    }
  ],
  "task_collections": [],
  "plans": []
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 4 — Execute the runtime boundary blocked-state check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime wp WP-001
{
  "wp_id": "WP-001",
  "runtime_boundary_state": "deterministic_blocked",
  "eligible_for_prompt_contract": false,
  "selected_plan_id": null,
  "deterministic_facts": {
    "work_package_status": "open",
    "orchestration_stage": "binding_context_required",
    "blocking_conditions": [
      "selector_context_missing"
    ],
    "next_actions": [
      "Complete deterministic selector context before orchestration can proceed."
    ],
    "selector_context_ready": false,
    "work_package_task_ids": [],
    "bound_committed_collection_ids": [],
    "bound_committed_task_ids": [],
    "plan_ids": []
  },
  "model_may": [
    "consume only validated deterministic facts exposed through this boundary payload",
    "transform those facts into bounded language outputs only after a future prompt contract is defined",
    "return only fields explicitly requested by a future runtime contract"
  ],
  "model_may_not": [
    "mutate persisted state",
    "invent facts, statuses, dates, dependencies, or identifiers",
    "change selected work package, selected plan, task scope, or collection scope",
    "resolve blocked deterministic state by inference",
    "bypass deterministic validation or acceptance rules"
  ]
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 5 — Execute the prompt-contract blocked-state check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime prompt-contract-wp WP-001
{
  "wp_id": "WP-001",
  "prompt_contract_id": "work_package_runtime_prompt_contract_v1",
  "prompt_contract_state": "blocked",
  "prompt_contract_mode": "blocked_explainer",
  "eligible_for_prompt_contract": false,
  "required_input_fields": [
    "wp_id",
    "runtime_boundary_state",
    "eligible_for_prompt_contract",
    "selected_plan_id",
    "deterministic_facts.work_package_status",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.blocking_conditions",
    "deterministic_facts.next_actions",
    "deterministic_facts.selector_context_ready",
    "deterministic_facts.work_package_task_ids",
    "deterministic_facts.bound_committed_collection_ids",
    "deterministic_facts.bound_committed_task_ids",
    "deterministic_facts.plan_ids"
  ],
  "expected_output_fields": [
    "response_mode",
    "operator_message",
    "recommended_next_actions",
    "grounded_input_fields_used"
  ],
  "prohibited_freeform_drift": [
    "omit required output fields",
    "add output fields outside the declared contract",
    "invent facts outside the validated deterministic inputs",
    "change or reinterpret blocking conditions",
    "change selected plan, task scope, or collection scope",
    "propose state mutation as if it already occurred"
  ],
  "runtime_boundary": {
    "wp_id": "WP-001",
    "runtime_boundary_state": "deterministic_blocked",
    "eligible_for_prompt_contract": false,
    "selected_plan_id": null,
    "deterministic_facts": {
      "work_package_status": "open",
      "orchestration_stage": "binding_context_required",
      "blocking_conditions": [
        "selector_context_missing"
      ],
      "next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
      ],
      "selector_context_ready": false,
      "work_package_task_ids": [],
      "bound_committed_collection_ids": [],
      "bound_committed_task_ids": [],
      "plan_ids": []
    },
    "model_may": [
      "consume only validated deterministic facts exposed through this boundary payload",
      "transform those facts into bounded language outputs only after a future prompt contract is defined",
      "return only fields explicitly requested by a future runtime contract"
    ],
    "model_may_not": [
      "mutate persisted state",
      "invent facts, statuses, dates, dependencies, or identifiers",
      "change selected work package, selected plan, task scope, or collection scope",
      "resolve blocked deterministic state by inference",
      "bypass deterministic validation or acceptance rules"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 6 — Execute the runtime handoff blocked-state check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime handoff-wp WP-001
{
  "wp_id": "WP-001",
  "handoff_metadata": {
    "handoff_contract_id": "work_package_llm_handoff_v1",
    "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
    "handoff_state": "blocked",
    "generation_allowed": false,
    "selected_plan_id": null,
    "prompt_contract_state": "blocked",
    "prompt_contract_mode": "blocked_explainer"
  },
  "structured_facts": {
    "work_package_status": "open",
    "orchestration_stage": "binding_context_required",
    "blocking_conditions": [
      "selector_context_missing"
    ],
    "next_actions": [
      "Complete deterministic selector context before orchestration can proceed."
    ],
    "selector_context_ready": false,
    "work_package_task_ids": [],
    "bound_committed_collection_ids": [],
    "bound_committed_task_ids": [],
    "plan_ids": []
  },
  "prose_generation_instructions": {
    "response_mode": "blocked_explainer",
    "writing_goal": "Explain why generation cannot proceed yet using only the structured facts, blockers, and next actions in this handoff payload.",
    "required_output_fields": [
      "response_mode",
      "operator_message",
      "recommended_next_actions",
      "grounded_input_fields_used"
    ],
    "grounded_input_fields": [
      "wp_id",
      "runtime_boundary_state",
      "eligible_for_prompt_contract",
      "selected_plan_id",
      "deterministic_facts.work_package_status",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.blocking_conditions",
      "deterministic_facts.next_actions",
      "deterministic_facts.selector_context_ready",
      "deterministic_facts.work_package_task_ids",
      "deterministic_facts.bound_committed_collection_ids",
      "deterministic_facts.bound_committed_task_ids",
      "deterministic_facts.plan_ids"
    ],
    "prohibited_freeform_drift": [
      "omit required output fields",
      "add output fields outside the declared contract",
      "invent facts outside the validated deterministic inputs",
      "change or reinterpret blocking conditions",
      "change selected plan, task scope, or collection scope",
      "propose state mutation as if it already occurred"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 7 — Execute the controlled generation request blocked-state check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime generate-request-wp WP-001
{
  "wp_id": "WP-001",
  "generation_surface_metadata": {
    "generation_surface_id": "work_package_controlled_generation_surface_v1",
    "handoff_contract_id": "work_package_llm_handoff_v1",
    "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
    "generation_state": "blocked",
    "generation_allowed": false,
    "generation_mode": "blocked_explainer",
    "generation_scope": "single_work_package_operator_response",
    "selected_plan_id": null
  },
  "deterministic_input": {
    "handoff_metadata": {
      "handoff_contract_id": "work_package_llm_handoff_v1",
      "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
      "handoff_state": "blocked",
      "generation_allowed": false,
      "selected_plan_id": null,
      "prompt_contract_state": "blocked",
      "prompt_contract_mode": "blocked_explainer"
    },
    "structured_facts": {
      "work_package_status": "open",
      "orchestration_stage": "binding_context_required",
      "blocking_conditions": [
        "selector_context_missing"
      ],
      "next_actions": [
        "Complete deterministic selector context before orchestration can proceed."
      ],
      "selector_context_ready": false,
      "work_package_task_ids": [],
      "bound_committed_collection_ids": [],
      "bound_committed_task_ids": [],
      "plan_ids": []
    }
  },
  "generation_instructions": {
    "writing_goal": "Explain why generation cannot proceed yet using only the structured facts, blockers, and next actions in this handoff payload.",
    "grounded_input_fields": [
      "wp_id",
      "runtime_boundary_state",
      "eligible_for_prompt_contract",
      "selected_plan_id",
      "deterministic_facts.work_package_status",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.blocking_conditions",
      "deterministic_facts.next_actions",
      "deterministic_facts.selector_context_ready",
      "deterministic_facts.work_package_task_ids",
      "deterministic_facts.bound_committed_collection_ids",
      "deterministic_facts.bound_committed_task_ids",
      "deterministic_facts.plan_ids"
    ],
    "prohibited_freeform_drift": [
      "omit required output fields",
      "add output fields outside the declared contract",
      "invent facts outside the validated deterministic inputs",
      "change or reinterpret blocking conditions",
      "change selected plan, task scope, or collection scope",
      "propose state mutation as if it already occurred"
    ]
  },
  "output_contract": {
    "required_output_fields": [
      "response_mode",
      "operator_message",
      "recommended_next_actions",
      "grounded_input_fields_used"
    ],
    "field_types": {
      "response_mode": "string",
      "operator_message": "string",
      "recommended_next_actions": "list[string]",
      "grounded_input_fields_used": "list[string]"
    }
  },
  "candidate_response_template": {
    "response_mode": "blocked_explainer",
    "operator_message": "",
    "recommended_next_actions": [],
    "grounded_input_fields_used": []
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 8 — Create a valid blocked candidate response file
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $blockedCandidate = @'
>> {
>>   "response_mode": "blocked_explainer",
>>   "operator_message": "Selector context is still required before generation can proceed.",
>>   "recommended_next_actions": [
>>     "Complete deterministic selector context before orchestration can proceed."
>>   ],
>>   "grounded_input_fields_used": [
>>     "wp_id",
>>     "deterministic_facts.orchestration_stage",
>>     "deterministic_facts.next_actions"
>>   ]
>> }
>> '@
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> [System.IO.File]::WriteAllText('.\data\state\candidate_response.json', $blockedCandidate, $utf8NoBom)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 9 — Execute the candidate-response acceptance check for the blocked state
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.json
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "accepted",
  "expected_response_mode": "blocked_explainer",
  "candidate_response_mode": "blocked_explainer",
  "errors": [],
  "validated_output": {
    "response_mode": "blocked_explainer",
    "operator_message": "Selector context is still required before generation can proceed.",
    "recommended_next_actions": [
      "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
      "wp_id",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.next_actions"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 10 — Execute the accepted decision-path check for the blocked state
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.json 1 2
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "accepted",
  "decision_state": "accepted",
  "fallback_action": "use_validated_output",
  "retry_policy": {
    "attempt_number": 1,
    "max_attempts": 2,
    "retries_remaining": 1
  },
  "decision_rationale": [
    "validated_output_accepted"
  ],
  "validation_errors": [],
  "validated_output": {
    "response_mode": "blocked_explainer",
    "operator_message": "Selector context is still required before generation can proceed.",
    "recommended_next_actions": [
      "Complete deterministic selector context before orchestration can proceed."
    ],
    "grounded_input_fields_used": [
      "wp_id",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.next_actions"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 11 — Create an invalid candidate response file to test deterministic rejection
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $invalidCandidate = @'
>> {
>>   "response_mode": "execution_ready_summary",
>>   "operator_message": "",
>>   "recommended_next_actions": "not-a-list",
>>   "grounded_input_fields_used": [
>>     "wp_id",
>>     "disallowed.field"
>>   ],
>>   "extra_field": "unexpected"
>> }
>> '@
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> [System.IO.File]::WriteAllText('.\data\state\candidate_response.invalid.json', $invalidCandidate, $utf8NoBom)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 12 — Execute the candidate-response rejection check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.invalid.json
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "rejected",
  "expected_response_mode": "blocked_explainer",
  "candidate_response_mode": "execution_ready_summary",
  "errors": [
    "Unexpected output fields: extra_field",
    "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'",
    "operator_message must be a non-empty string.",
    "recommended_next_actions must be a list of strings.",
    "grounded_input_fields_used contains disallowed fields: disallowed.field"
  ],
  "validated_output": null
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 13 — Execute the retry-allowed decision-path check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.invalid.json 1 2
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "rejected",
  "decision_state": "retry_allowed",
  "fallback_action": "request_new_candidate_from_same_handoff_contract",
  "retry_policy": {
    "attempt_number": 1,
    "max_attempts": 2,
    "retries_remaining": 1
  },
  "decision_rationale": [
    "validation_rejected_but_retry_budget_remaining"
  ],
  "validation_errors": [
    "Unexpected output fields: extra_field",
    "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'",
    "operator_message must be a non-empty string.",
    "recommended_next_actions must be a list of strings.",
    "grounded_input_fields_used contains disallowed fields: disallowed.field"
  ],
  "validated_output": null
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 14 — Execute the fail-closed exhausted-retry check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.invalid.json 2 2
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "rejected",
  "decision_state": "fail_closed",
  "fallback_action": "return_deterministic_rejection_without_acceptance",
  "retry_policy": {
    "attempt_number": 2,
    "max_attempts": 2,
    "retries_remaining": 0
  },
  "decision_rationale": [
    "validation_rejected_and_retry_budget_exhausted"
  ],
  "validation_errors": [
    "Unexpected output fields: extra_field",
    "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'",
    "operator_message must be a non-empty string.",
    "recommended_next_actions must be a list of strings.",
    "grounded_input_fields_used contains disallowed fields: disallowed.field"
  ],
  "validated_output": null
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 15 — Enrich the state into an execution-ready Work Package baseline
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-preset WP-001 oral-solid-dose-standard
Work Package preset updated: WP-001 -> oral-solid-dose-standard
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-scope-intent WP-001 qualification-only
Work Package scope intent updated: WP-001 -> qualification-only
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-standards-bundles WP-001 automation
Work Package standards bundles updated: WP-001 -> [cqv-core, automation]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task add "Prepare FAT" --duration 1 --task-key prepare-fat
Task added: TASK-001 - Prepare FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task set-work-package TASK-001 WP-001
Task work package updated: TASK-001 -> WP-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add "Committed Selection" --collection-state committed
Collection added: TC-001 - Committed Selection (committed)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add-task TC-001 TASK-001
Task added to collection: TC-001 <- TASK-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection set-work-package TC-001 WP-001
Collection work package updated: TC-001 -> WP-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 16 — Inject a committed plan through approved state-model/state-store usage
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> @'
>> from datetime import datetime, timezone
>> 
>> from asbp.state_model import (
>>     GeneratedTaskPlanModel,
>>     PlanningBasisModel,
>>     PlanningCalendarModel,
>>     PlanningModel,
>> )
>> from asbp.state_store import get_state_file_path, load_validated_state, save_validated_state_to_path
>> 
>> state_path = get_state_file_path()
>> state = load_validated_state(state_path)
>> 
>> state.plans = [
>>     PlanningModel(
>>         plan_id="PLAN-001",
>>         work_package_id="WP-001",
>>         plan_state="committed",
>>         planning_basis=PlanningBasisModel(
>>             duration_source="task_duration",
>>         ),
>>         planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
>>         planning_calendar=PlanningCalendarModel(
>>             working_days=["monday", "wednesday", "friday"],
>>             workday_hours=8,
>>             workmonth_mode="calendar_month",
>>         ),
>>         generated_task_plans=[
>>             GeneratedTaskPlanModel(
>>                 task_id="TASK-001",
>>                 sequence_order=1,
>>                 duration_days=1,
>>                 dependency_task_ids=[],
>>                 planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
>>                 planned_finish_at=datetime(2026, 4, 13, 16, 30, tzinfo=timezone.utc),
>>             )
>>         ],
>>     )
>> ]
>> 
>> save_validated_state_to_path(state, state_path)
>> print("Injected PLAN-001 into controlled UAT state.")
>> '@ | python -
Injected PLAN-001 into controlled UAT state.
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 17 — Execute the runtime boundary execution-ready check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime wp WP-001
{
  "wp_id": "WP-001",
  "runtime_boundary_state": "eligible_for_prompt_contract",
  "eligible_for_prompt_contract": true,
  "selected_plan_id": "PLAN-001",
  "deterministic_facts": {
    "work_package_status": "open",
    "orchestration_stage": "execution_ready",
    "blocking_conditions": [],
    "next_actions": [
      "Execution-ready deterministic state reached."
    ],
    "selector_context_ready": true,
    "work_package_task_ids": [
      "TASK-001"
    ],
    "bound_committed_collection_ids": [
      "TC-001"
    ],
    "bound_committed_task_ids": [
      "TASK-001"
    ],
    "plan_ids": [
      "PLAN-001"
    ]
  },
  "model_may": [
    "consume only validated deterministic facts exposed through this boundary payload",
    "transform those facts into bounded language outputs only after a future prompt contract is defined",
    "return only fields explicitly requested by a future runtime contract"
  ],
  "model_may_not": [
    "mutate persisted state",
    "invent facts, statuses, dates, dependencies, or identifiers",
    "change selected work package, selected plan, task scope, or collection scope",
    "resolve blocked deterministic state by inference",
    "bypass deterministic validation or acceptance rules"
  ]
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 18 — Execute the prompt-contract execution-ready check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime prompt-contract-wp WP-001
{
  "wp_id": "WP-001",
  "prompt_contract_id": "work_package_runtime_prompt_contract_v1",
  "prompt_contract_state": "ready",
  "prompt_contract_mode": "execution_ready_summary",
  "eligible_for_prompt_contract": true,
  "required_input_fields": [
    "wp_id",
    "runtime_boundary_state",
    "eligible_for_prompt_contract",
    "selected_plan_id",
    "deterministic_facts.work_package_status",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.blocking_conditions",
    "deterministic_facts.next_actions",
    "deterministic_facts.selector_context_ready",
    "deterministic_facts.work_package_task_ids",
    "deterministic_facts.bound_committed_collection_ids",
    "deterministic_facts.bound_committed_task_ids",
    "deterministic_facts.plan_ids"
  ],
  "expected_output_fields": [
    "response_mode",
    "operator_message",
    "recommended_next_actions",
    "grounded_input_fields_used"
  ],
  "prohibited_freeform_drift": [
    "omit required output fields",
    "add output fields outside the declared contract",
    "invent facts outside the validated deterministic inputs",
    "change or reinterpret blocking conditions",
    "change selected plan, task scope, or collection scope",
    "propose state mutation as if it already occurred"
  ],
  "runtime_boundary": {
    "wp_id": "WP-001",
    "runtime_boundary_state": "eligible_for_prompt_contract",
    "eligible_for_prompt_contract": true,
    "selected_plan_id": "PLAN-001",
    "deterministic_facts": {
      "work_package_status": "open",
      "orchestration_stage": "execution_ready",
      "blocking_conditions": [],
      "next_actions": [
        "Execution-ready deterministic state reached."
      ],
      "selector_context_ready": true,
      "work_package_task_ids": [
        "TASK-001"
      ],
      "bound_committed_collection_ids": [
        "TC-001"
      ],
      "bound_committed_task_ids": [
        "TASK-001"
      ],
      "plan_ids": [
        "PLAN-001"
      ]
    },
    "model_may": [
      "consume only validated deterministic facts exposed through this boundary payload",
      "transform those facts into bounded language outputs only after a future prompt contract is defined",
      "return only fields explicitly requested by a future runtime contract"
    ],
    "model_may_not": [
      "mutate persisted state",
      "invent facts, statuses, dates, dependencies, or identifiers",
      "change selected work package, selected plan, task scope, or collection scope",
      "resolve blocked deterministic state by inference",
      "bypass deterministic validation or acceptance rules"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 19 — Execute the runtime handoff execution-ready check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime handoff-wp WP-001
{
  "wp_id": "WP-001",
  "handoff_metadata": {
    "handoff_contract_id": "work_package_llm_handoff_v1",
    "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
    "handoff_state": "ready_for_generation",
    "generation_allowed": true,
    "selected_plan_id": "PLAN-001",
    "prompt_contract_state": "ready",
    "prompt_contract_mode": "execution_ready_summary"
  },
  "structured_facts": {
    "work_package_status": "open",
    "orchestration_stage": "execution_ready",
    "blocking_conditions": [],
    "next_actions": [
      "Execution-ready deterministic state reached."
    ],
    "selector_context_ready": true,
    "work_package_task_ids": [
      "TASK-001"
    ],
    "bound_committed_collection_ids": [
      "TC-001"
    ],
    "bound_committed_task_ids": [
      "TASK-001"
    ],
    "plan_ids": [
      "PLAN-001"
    ]
  },
  "prose_generation_instructions": {
    "response_mode": "execution_ready_summary",
    "writing_goal": "Summarize execution-ready deterministic state for the operator using only the structured facts in this handoff payload.",
    "required_output_fields": [
      "response_mode",
      "operator_message",
      "recommended_next_actions",
      "grounded_input_fields_used"
    ],
    "grounded_input_fields": [
      "wp_id",
      "runtime_boundary_state",
      "eligible_for_prompt_contract",
      "selected_plan_id",
      "deterministic_facts.work_package_status",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.blocking_conditions",
      "deterministic_facts.next_actions",
      "deterministic_facts.selector_context_ready",
      "deterministic_facts.work_package_task_ids",
      "deterministic_facts.bound_committed_collection_ids",
      "deterministic_facts.bound_committed_task_ids",
      "deterministic_facts.plan_ids"
    ],
    "prohibited_freeform_drift": [
      "omit required output fields",
      "add output fields outside the declared contract",
      "invent facts outside the validated deterministic inputs",
      "change or reinterpret blocking conditions",
      "change selected plan, task scope, or collection scope",
      "propose state mutation as if it already occurred"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 20 — Execute the controlled generation request execution-ready check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime generate-request-wp WP-001
{
  "wp_id": "WP-001",
  "generation_surface_metadata": {
    "generation_surface_id": "work_package_controlled_generation_surface_v1",
    "handoff_contract_id": "work_package_llm_handoff_v1",
    "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
    "generation_state": "ready",
    "generation_allowed": true,
    "generation_mode": "execution_ready_summary",
    "generation_scope": "single_work_package_operator_response",
    "selected_plan_id": "PLAN-001"
  },
  "deterministic_input": {
    "handoff_metadata": {
      "handoff_contract_id": "work_package_llm_handoff_v1",
      "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
      "handoff_state": "ready_for_generation",
      "generation_allowed": true,
      "selected_plan_id": "PLAN-001",
      "prompt_contract_state": "ready",
      "prompt_contract_mode": "execution_ready_summary"
    },
    "structured_facts": {
      "work_package_status": "open",
      "orchestration_stage": "execution_ready",
      "blocking_conditions": [],
      "next_actions": [
        "Execution-ready deterministic state reached."
      ],
      "selector_context_ready": true,
      "work_package_task_ids": [
        "TASK-001"
      ],
      "bound_committed_collection_ids": [
        "TC-001"
      ],
      "bound_committed_task_ids": [
        "TASK-001"
      ],
      "plan_ids": [
        "PLAN-001"
      ]
    }
  },
  "generation_instructions": {
    "writing_goal": "Summarize execution-ready deterministic state for the operator using only the structured facts in this handoff payload.",
    "grounded_input_fields": [
      "wp_id",
      "runtime_boundary_state",
      "eligible_for_prompt_contract",
      "selected_plan_id",
      "deterministic_facts.work_package_status",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.blocking_conditions",
      "deterministic_facts.next_actions",
      "deterministic_facts.selector_context_ready",
      "deterministic_facts.work_package_task_ids",
      "deterministic_facts.bound_committed_collection_ids",
      "deterministic_facts.bound_committed_task_ids",
      "deterministic_facts.plan_ids"
    ],
    "prohibited_freeform_drift": [
      "omit required output fields",
      "add output fields outside the declared contract",
      "invent facts outside the validated deterministic inputs",
      "change or reinterpret blocking conditions",
      "change selected plan, task scope, or collection scope",
      "propose state mutation as if it already occurred"
    ]
  },
  "output_contract": {
    "required_output_fields": [
      "response_mode",
      "operator_message",
      "recommended_next_actions",
      "grounded_input_fields_used"
    ],
    "field_types": {
      "response_mode": "string",
      "operator_message": "string",
      "recommended_next_actions": "list[string]",
      "grounded_input_fields_used": "list[string]"
    }
  },
  "candidate_response_template": {
    "response_mode": "execution_ready_summary",
    "operator_message": "",
    "recommended_next_actions": [],
    "grounded_input_fields_used": []
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 21 — Create a valid execution-ready candidate response file
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $readyCandidate = @'
>> {
>>   "response_mode": "execution_ready_summary",
>>   "operator_message": "The work package is ready for generation using the selected committed plan.",
>>   "recommended_next_actions": [
>>     "Execution-ready deterministic state reached."
>>   ],
>>   "grounded_input_fields_used": [
>>     "wp_id",
>>     "selected_plan_id",
>>     "deterministic_facts.orchestration_stage",
>>     "deterministic_facts.plan_ids"
>>   ]
>> }
>> '@
>> $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
>> [System.IO.File]::WriteAllText('.\data\state\candidate_response.ready.json', $readyCandidate, $utf8NoBom)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 22 — Execute the candidate-response acceptance check for the execution-ready state
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime validate-response-wp WP-001 .\data\state\candidate_response.ready.json
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "accepted",
  "expected_response_mode": "execution_ready_summary",
  "candidate_response_mode": "execution_ready_summary",
  "errors": [],
  "validated_output": {
    "response_mode": "execution_ready_summary",
    "operator_message": "The work package is ready for generation using the selected committed plan.",
    "recommended_next_actions": [
      "Execution-ready deterministic state reached."
    ],
    "grounded_input_fields_used": [
      "wp_id",
      "selected_plan_id",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.plan_ids"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 23 — Execute the invalid retry-control fail-closed check
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime decide-response-wp WP-001 .\data\state\candidate_response.ready.json 3 2
{
  "wp_id": "WP-001",
  "handoff_contract_id": "work_package_llm_handoff_v1",
  "validation_state": "accepted",
  "decision_state": "fail_closed",
  "fallback_action": "return_deterministic_rejection_without_acceptance",
  "retry_policy": {
    "attempt_number": 3,
    "max_attempts": 2,
    "retries_remaining": 0
  },
  "decision_rationale": [
    "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
  ],
  "validation_errors": [],
  "validated_output": {
    "response_mode": "execution_ready_summary",
    "operator_message": "The work package is ready for generation using the selected committed plan.",
    "recommended_next_actions": [
      "Execution-ready deterministic state reached."
    ],
    "grounded_input_fields_used": [
      "wp_id",
      "selected_plan_id",
      "deterministic_facts.orchestration_stage",
      "deterministic_facts.plan_ids"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 24 — Execute the missing Work Package runtime-surface rejection checks
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime wp WP-404
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime prompt-contract-wp WP-404
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime handoff-wp WP-404
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime generate-request-wp WP-404
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime validate-response-wp WP-404 .\data\state\candidate_response.ready.json
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp runtime decide-response-wp WP-404 .\data\state\candidate_response.ready.json 1 2
Work Package not found: WP-404
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> # Step 25 — Re-run the full validation baseline after UAT execution
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m pytest -q
........................................................................................................................................ [ 28%]
........................................................................................................................................ [ 57%]
........................................................................................................................................ [ 86%]
.............................................................                                                                            [100%]
469 passed in 44.73s
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> if (Test-Path (Join-Path $backupDir 'state.json.original.bak')) {
>>     Copy-Item (Join-Path $backupDir 'state.json.original.bak') '.\data\state\state.json' -Force
>> } else {
>>     Remove-Item '.\data\state\state.json' -ErrorAction SilentlyContinue
>> }
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> if (Test-Path (Join-Path $backupDir 'candidate_response.original.bak')) {
>>     Copy-Item (Join-Path $backupDir 'candidate_response.original.bak') '.\data\state\candidate_response.json' -Force
>> } else {
>>     Remove-Item '.\data\state\candidate_response.json' -ErrorAction SilentlyContinue
>> }
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Remove-Item '.\data\state\candidate_response.invalid.json' -ErrorAction SilentlyContinue
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Remove-Item '.\data\state\candidate_response.ready.json' -ErrorAction SilentlyContinue
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
