# smoke_test_interim_M5

python -m asbp state init
python -m asbp state set-status in_flight
python -m asbp wp add WP-001 "Tablet press qualification"
python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
python -m asbp task set-work-package "prepare-fat" WP-001
python -m asbp task list --show-work-package-id
python -m asbp task show "prepare-fat" --show-work-package-id
python -m asbp task list --work-package-id WP-001
python -m asbp wp show WP-001 --show-task-ids
python -m asbp wp list --task-id TASK-001
python -m asbp wp list --show-task-ids
python -m asbp task clear-work-package "prepare-fat"
python -m asbp wp show WP-001 --show-task-ids


(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Copy-Item '.\data\state\state.json' (Join-Path $backupDir 'state.json.bak') -Force
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state init
State initialized at: C:\Dev\GitHub\AI_SYSTEM_BUILDER\data\state\state.json
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp state set-status in_flight
State status updated to: in_flight
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp add WP-001 "Tablet press qualification"
Work Package added: WP-001 - Tablet press qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task add "Prepare FAT" --task-key "prepare-fat"
Task added: TASK-001 - Prepare FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task set-work-package "prepare-fat" WP-001
Task work package updated: TASK-001 -> WP-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task list --show-work-package-id
Tasks:
- TASK-001 | planned | work_package_id=WP-001 | Prepare FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task show "prepare-fat" --show-work-package-id
{
  "task_id": "TASK-001",
  "order": 1,
  "title": "Prepare FAT",
  "description": null,
  "owner": null,
  "duration": null,
  "start_date": null,
  "end_date": null,
  "task_key": "prepare-fat",
  "work_package_id": "WP-001",
  "status": "planned",
  "dependencies": []
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task list --work-package-id WP-001
Tasks:
- TASK-001 | planned | Prepare FAT
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp show WP-001 --show-task-ids
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "task_ids": [
    "TASK-001"
  ]
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp list --task-id TASK-001
Work Packages:
- WP-001 | open | Tablet press qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp list --show-task-ids
Work Packages:
- WP-001 | open | task_ids=[TASK-001] | Tablet press qualification
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp task clear-work-package "prepare-fat"
Task work package cleared: TASK-001
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> python -m asbp wp show WP-001 --show-task-ids       
{
  "wp_id": "WP-001",
  "title": "Tablet press qualification",
  "status": "open",
  "task_ids": []
}
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> $backupDir = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ASBP_UAT_Backup'
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Copy-Item (Join-Path $backupDir 'state.json.bak') '.\data\state\state.json' -Force
(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> Get-Content .\data\state\state.json
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [
    {
      "task_id": "TASK-001",
      "order": 1,
      "title": "Task A",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": []
    },
    {
      "task_id": "TASK-003",
      "order": 2,
      "title": "Task C",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": ["TASK-001", "TASK-004"]
    },
    {
      "task_id": "TASK-004",
      "order": 3,
      "title": "Task D",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": []
    },
    {
      "task_id": "TASK-005",
      "order": 4,
      "title": "Task E",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "in_progress",
      "dependencies": []
    },
    {
      "task_id": "TASK-006",
      "order": 5,
      "title": "Ordering verification task",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": ["TASK-005"]
    },
    {
      "task_id": "TASK-007",
      "order": 6,
      "title": "Dependency task for completion gating",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": ["TASK-008"]
    },
    {
      "task_id": "TASK-008",
      "order": 7,
      "title": "Blocked completion task",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": []
    },
    {
      "task_id": "TASK-009",
      "order": 8,
      "title": "Predecessor",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": []
    },
    {
      "task_id": "TASK-010",
      "order": 9,
      "title": "Successor",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "completed",
      "dependencies": ["TASK-009"]
    },
    {
      "task_id": "TASK-011",
      "order": 10,
      "title": "New test task",
      "description": "Test",
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "in_progress",
      "dependencies": []
    },
    {
      "task_id": "TASK-012",
      "order": 11,
      "title": "Prepare FAT protocol",
      "description": "Draft",
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "planned",
      "dependencies": ["TASK-011"]
    },
    {
      "task_id": "TASK-013",
      "order": 12,
      "title": "Prepare DQ",
      "description": null,
      "owner": null,
      "duration": null,
      "start_date": null,
      "end_date": null,
      "task_key": null,
      "status": "planned",
      "dependencies": []
    }
  ]
}


(.venv) PS C:\Dev\GitHub\AI_SYSTEM_BUILDER> 
