PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Dev\GitHub\AI_SYSTEM_BUILDER\.venv\Scripts\Activate.ps1)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> if (Test-Path '.\data\state\state.json') {
>>     Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.original.bak') -Force
>> }
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> @'
>> from asbp.state_model import TaskModel
>> 
>> manual_task = TaskModel(
>>     task_id="TASK-MANUAL-001",
>>     order=1,
>>     title="Manual task",
>>     status="planned",
>> )
>> 
>> preset_resolved_task = TaskModel(
>>     task_id="TASK-PRESET-001",
>>     order=2,
>>     title="Preset resolved task",
>>     work_package_id="WP-001",
>>     instantiation_mode="preset_resolved",
>>     source_definition_kind="task_pool",
>>     source_definition_id="POOL-TABPRESS-001",
>>     status="planned",
>> )
>> 
>> print("manual_ok", manual_task.instantiation_mode)
>> print(
>>     "preset_ok",
>>     preset_resolved_task.instantiation_mode,
>>     preset_resolved_task.source_definition_kind,
>>     preset_resolved_task.source_definition_id,
>> )
>> '@ | python -
manual_ok manual
preset_ok preset_resolved task_pool POOL-TABPRESS-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> @'
>> from asbp.state_model import TaskModel
>> 
>> try:
>>     TaskModel(
>>         task_id="TASK-BAD-001",
>>         order=1,
>>         title="Invalid preset task",
>>         work_package_id="WP-001",
>>         instantiation_mode="preset_resolved",
>>         status="planned",
>>     )
>> except Exception as exc:
>>     print(type(exc).__name__)
>>     print(exc)
>> '@ | python -
ValidationError
1 validation error for TaskModel
  Value error, Preset-resolved task must declare source_definition_kind=task_pool [type=value_error, input_value={'task_id': 'TASK-BAD-001...d', 'status': 'planned'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/value_error
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
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-001 "Tablet press qualification"
Work Package added: WP-001 - Tablet press qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-002 "Autoclave qualification"
Work Package added: WP-002 - Autoclave qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-003 "Line clearance package"
Work Package added: WP-003 - Line clearance package
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-004 "Plan-only package"
Work Package added: WP-004 - Plan-only package
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-preset WP-001 oral-solid-dose-standard
Work Package preset updated: WP-001 -> oral-solid-dose-standard
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-scope-intent WP-001 qualification-only
Work Package scope intent updated: WP-001 -> qualification-only
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp set-standards-bundles WP-001 automation
Work Package standards bundles updated: WP-001 -> [cqv-core, automation]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp show WP-001 --show-selector-context
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "selector_context": {
    "preset_id": "oral-solid-dose-standard",
    "scope_intent": "qualification-only",
    "standards_bundles": [
      "cqv-core",
      "automation"
    ]
  }
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task add "Prepare FAT" --duration 1 --task-key prepare-fat
>> python -m asbp task add "Execute FAT" --duration 1 --task-key execute-fat
>> python -m asbp task add "Autoclave FAT" --duration 1 --task-key autoclave-fat
>> python -m asbp task set-work-package TASK-001 WP-001
>> python -m asbp task set-work-package TASK-002 WP-001
>> python -m asbp task set-work-package TASK-003 WP-002
>> python -m asbp task list --show-task-key --show-work-package-id
Task added: TASK-001 - Prepare FAT
Task added: TASK-002 - Execute FAT
Task added: TASK-003 - Autoclave FAT
Task work package updated: TASK-001 -> WP-001
Task work package updated: TASK-002 -> WP-001
Task work package updated: TASK-003 -> WP-002
Tasks:
- TASK-001 | planned | task_key=prepare-fat | work_package_id=WP-001 | Prepare FAT
- TASK-002 | planned | task_key=execute-fat | work_package_id=WP-001 | Execute FAT
- TASK-003 | planned | task_key=autoclave-fat | work_package_id=WP-002 | Autoclave FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add "Committed Selection" --collection-state committed
Collection added: TC-001 - Committed Selection (committed)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add-task TC-001 TASK-001
Task added to collection: TC-001 <- TASK-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add-task TC-001 TASK-002
Task added to collection: TC-001 <- TASK-002
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection set-work-package TC-001 WP-001
Collection work package updated: TC-001 -> WP-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection show TC-001 --show-work-package-id
{
  "collection_id": "TC-001",
  "title": "Committed Selection",
  "collection_state": "committed",
  "task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "work_package_id": "WP-001"
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp show WP-001 --show-task-ids --show-collection-ids --show-selector-context
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "selector_context": {
    "preset_id": "oral-solid-dose-standard",
    "scope_intent": "qualification-only",
    "standards_bundles": [
      "cqv-core",
      "automation"
    ]
  },
  "task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "collection_ids": [
    "TC-001"
  ]
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp list --show-task-ids --show-collection-ids
Work Packages:
- WP-001 | open | task_ids=[TASK-001, TASK-002] | collection_ids=[TC-001] | Tablet press qualification
- WP-002 | open | task_ids=[TASK-003] | collection_ids=[] | Autoclave qualification
- WP-003 | open | task_ids=[] | collection_ids=[] | Line clearance package
- WP-004 | open | task_ids=[] | collection_ids=[] | Plan-only package
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection show TC-001 --show-work-package-id
{
  "collection_id": "TC-001",
  "title": "Committed Selection",
  "collection_state": "committed",
  "task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "work_package_id": "WP-001"
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection list --show-work-package-id --show-task-ids
Collections:
- TC-001 | committed | work_package_id=WP-001 | task_ids=[TASK-001, TASK-002] | Committed Selection
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task show TASK-001 --show-work-package-id --show-collection-ids
{
  "task_id": "TASK-001",
  "order": 1,
  "title": "Prepare FAT",
  "description": null,
  "owner": null,
  "duration": 1,
  "start_date": null,
  "end_date": null,
  "task_key": "prepare-fat",
  "work_package_id": "WP-001",
  "status": "planned",
  "dependencies": [],
  "collection_ids": [
    "TC-001"
  ]
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task list --show-task-key --show-work-package-id --show-collection-ids
Tasks:
- TASK-001 | planned | task_key=prepare-fat | work_package_id=WP-001 | collection_ids=[TC-001] | Prepare FAT
- TASK-002 | planned | task_key=execute-fat | work_package_id=WP-001 | collection_ids=[TC-001] | Execute FAT
- TASK-003 | planned | task_key=autoclave-fat | work_package_id=WP-002 | collection_ids=[] | Autoclave FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection clear-work-package TC-001
Collection work package cleared: TC-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection set-work-package TC-001 WP-001
Collection work package updated: TC-001 -> WP-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection show TC-001 --show-work-package-id
{
  "collection_id": "TC-001",
  "title": "Committed Selection",
  "collection_state": "committed",
  "task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "work_package_id": "WP-001"
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add "Conflicting Selection" --collection-state committed
Collection added: TC-002 - Conflicting Selection (committed)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add-task TC-002 TASK-003
Task added to collection: TC-002 <- TASK-003
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection set-work-package TC-002 WP-001
Collection work package cannot be bound because member task has a different work package: TC-002 -> TASK-003 (WP-002 != WP-001)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task delete TASK-001
Task cannot be deleted while still associated with collections: TASK-001 -> [TC-001]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection add "Empty Bound Selection" --collection-state committed
Collection added: TC-003 - Empty Bound Selection (committed)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection set-work-package TC-003 WP-003
Collection work package updated: TC-003 -> WP-003
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp delete WP-003
Work Package cannot be deleted while collections are bound: WP-003 -> [TC-003]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.uat-working.bak') -Force
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
>>     ),
>>     PlanningModel(
>>         plan_id="PLAN-002",
>>         work_package_id="WP-004",
>>         plan_state="draft",
>>     ),
>> ]
>> 
>> save_validated_state_to_path(state, state_path)
>> print("Injected PLAN-001 and PLAN-002 into controlled UAT state.")
>> '@ | python -
Injected PLAN-001 and PLAN-002 into controlled UAT state.
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp delete WP-004
Work Package cannot be deleted while plans are associated: WP-004 -> [PLAN-002]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp orchestrate wp WP-004
{
  "wp_id": "WP-004",
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
  "plan_ids": [
    "PLAN-002"
  ],
  "selected_plan_id": null
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp orchestrate wp WP-001
{
  "wp_id": "WP-001",
  "work_package_status": "open",
  "orchestration_stage": "execution_ready",
  "blocking_conditions": [],
  "next_actions": [
    "Execution-ready deterministic state reached."
  ],
  "selector_context_ready": true,
  "work_package_task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "bound_committed_collection_ids": [
    "TC-001"
  ],
  "bound_committed_task_ids": [
    "TASK-001",
    "TASK-002"
  ],
  "plan_ids": [
    "PLAN-001"
  ],
  "selected_plan_id": "PLAN-001"
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp collection remove-task TC-001 TASK-001
Task removed from collection: TC-001 <- TASK-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task clear-work-package TASK-001
Task work package cannot be cleared while plans still reference it: TASK-001 -> [PLAN-001 (WP-001)]
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> @'
>> {
>>   "project": "AI_SYSTEM_BUILDER",
>>   "version": "0.1.0",
>>   "status": "in_flight",
>>   "tasks": [],
>>   "work_packages": [
>>     {
>>       "wp_id": "WP-001",
>>       "title": "Tablet press qualification",
>>       "status": "open"
>>     }
>>   ],
>>   "task_collections": [],
>>   "plans": [
>>     {
>>       "plan_id": "PLAN-900",
>>       "work_package_id": "WP-999",
>>       "plan_state": "draft"
>>     }
>>   ]
>> }
>> '@ | Set-Content -Encoding utf8 '.\data\state\state.json'
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state show
Invalid JSON in state file: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Copy-Item (Join-Path $backupDir 'state.uat-working.bak') '.\data\state\state.json' -Force
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state show
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.1.0",
  "status": "in_flight",
  "tasks": [
    {
      "task_id": "TASK-001",
      "order": 1,
      "title": "Prepare FAT",
      "description": null,
      "owner": null,
      "duration": 1,
      "start_date": null,
      "end_date": null,
      "task_key": "prepare-fat",
      "work_package_id": "WP-001",
      "status": "planned",
      "dependencies": []
    },
    {
      "task_id": "TASK-002",
      "order": 2,
      "title": "Execute FAT",
      "description": null,
      "owner": null,
      "duration": 1,
      "start_date": null,
      "end_date": null,
      "task_key": "execute-fat",
      "work_package_id": "WP-001",
      "status": "planned",
      "dependencies": []
    },
    {
      "task_id": "TASK-003",
      "order": 3,
      "title": "Autoclave FAT",
      "description": null,
      "owner": null,
      "duration": 1,
      "start_date": null,
      "end_date": null,
      "task_key": "autoclave-fat",
      "work_package_id": "WP-002",
      "status": "planned",
      "dependencies": []
    }
  ],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification",
      "status": "open",
      "selector_context": {
        "system_type": null,
        "preset_id": "oral-solid-dose-standard",
        "scope_intent": "qualification-only",
        "standards_bundles": [
          "cqv-core",
          "automation"
        ]
      }
    },
    {
      "wp_id": "WP-002",
      "title": "Autoclave qualification",
      "status": "open",
      "selector_context": null
    },
    {
      "wp_id": "WP-003",
      "title": "Line clearance package",
      "status": "open",
      "selector_context": null
    },
    {
      "wp_id": "WP-004",
      "title": "Plan-only package",
      "status": "open",
      "selector_context": null
    }
  ],
  "task_collections": [
    {
      "collection_id": "TC-001",
      "title": "Committed Selection",
      "collection_state": "committed",
      "task_ids": [
        "TASK-001",
        "TASK-002"
      ]
    },
    {
      "collection_id": "TC-002",
      "title": "Conflicting Selection",
      "collection_state": "committed",
      "task_ids": [
        "TASK-003"
      ]
    },
    {
      "collection_id": "TC-003",
      "title": "Empty Bound Selection",
      "collection_state": "committed",
      "task_ids": []
    }
  ],
  "plans": []
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m pytest -q
........................................................................................................................................... [ 31%]
........................................................................................................................................... [ 63%]
........................................................................................................................................... [ 95%]
...................                                                                                                                         [100%]
436 passed in 41.07s
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 