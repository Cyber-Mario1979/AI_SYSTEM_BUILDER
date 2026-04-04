from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    repo_root = Path.cwd()

    cli_path = repo_root / "asbp" / "cli.py"
    test_cli_path = repo_root / "tests" / "test_task_cli.py"

    cli_text = cli_path.read_text(encoding="utf-8")
    test_cli_text = test_cli_path.read_text(encoding="utf-8")

    cli_text = replace_once(
        cli_text,
        '''def _prepare_task_show_payload(
    tasks,
    task,
    *,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    task_payload = task.model_dump()

    if not show_dependency_refs and not show_dependent_refs:
        return task_payload

    return _attach_reference_views_to_task_payload(
        tasks,
        task_payload,
        show_dependency_refs=show_dependency_refs,
        show_dependent_refs=show_dependent_refs,
    )
''',
        '''def _prepare_task_read_payload(
    tasks,
    task,
    *,
    show_dependency_refs=False,
    show_dependent_refs=False,
):
    if hasattr(task, "model_dump"):
        task_payload = task.model_dump()
    else:
        task_payload = dict(task)

    if not show_dependency_refs and not show_dependent_refs:
        return task_payload

    return _attach_reference_views_to_task_payload(
        tasks,
        task_payload,
        show_dependency_refs=show_dependency_refs,
        show_dependent_refs=show_dependent_refs,
    )
''',
        "replace _prepare_task_show_payload helper",
    )

    cli_text = replace_once(
        cli_text,
        '''        task_output = _attach_reference_views_to_task_payload(
            state.tasks,
            dict(task),
            show_dependency_refs=args.show_dependency_refs,
            show_dependent_refs=args.show_dependent_refs,
        )
''',
        '''        task_output = _prepare_task_read_payload(
            state.tasks,
            task,
            show_dependency_refs=args.show_dependency_refs,
            show_dependent_refs=args.show_dependent_refs,
        )
''',
        "route task list through shared read payload helper",
    )

    cli_text = replace_once(
        cli_text,
        '''    task_payload = _attach_reference_views_to_task_payload(
        state.tasks,
        task.model_dump(),
        show_dependency_refs=args.show_dependency_refs,
        show_dependent_refs=args.show_dependent_refs,
    )
''',
        '''    task_payload = _prepare_task_read_payload(
        state.tasks,
        task,
        show_dependency_refs=args.show_dependency_refs,
        show_dependent_refs=args.show_dependent_refs,
    )
''',
        "route task show through shared read payload helper",
    )

    test_cli_text = replace_once(
        test_cli_text,
        '''    _prepare_task_show_payload,
''',
        '''    _prepare_task_read_payload,
''',
        "update helper import",
    )

    test_cli_text = replace_once(
        test_cli_text,
        '''def test_prepare_task_show_payload_preserves_default_contract_without_reference_visibility_flags():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key="execute-fat",
            status="planned",
            dependencies=["TASK-001"],
        ),
    ]

    result = _prepare_task_show_payload(
        tasks,
        tasks[0],
        show_dependency_refs=False,
        show_dependent_refs=False,
    )

    assert result == tasks[0].model_dump()
''',
        '''def test_prepare_task_read_payload_preserves_default_contract_without_reference_visibility_flags():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key="execute-fat",
            status="planned",
            dependencies=["TASK-001"],
        ),
    ]

    result = _prepare_task_read_payload(
        tasks,
        tasks[0],
        show_dependency_refs=False,
        show_dependent_refs=False,
    )

    assert result == tasks[0].model_dump()
''',
        "rename default-contract helper test",
    )

    test_cli_text = replace_once(
        test_cli_text,
        '''def test_prepare_task_show_payload_attaches_both_reference_views_when_enabled():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key=None,
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Review FAT Package",
            task_key="review-fat-package",
            status="completed",
            dependencies=["TASK-001", "TASK-002"],
        ),
        TaskModel(
            task_id="TASK-004",
            order=4,
            title="Archive FAT Package",
            task_key="archive-fat-package",
            status="planned",
            dependencies=["TASK-003"],
        ),
    ]

    result = _prepare_task_show_payload(
        tasks,
        tasks[2],
        show_dependency_refs=True,
        show_dependent_refs=True,
    )

    assert result["dependency_refs"] == [
        {"task_id": "TASK-001", "task_key": "prepare-fat"},
        {"task_id": "TASK-002", "task_key": "<none>"},
    ]
    assert result["dependent_refs"] == [
        {"task_id": "TASK-004", "task_key": "archive-fat-package"},
    ]
''',
        '''def test_prepare_task_read_payload_attaches_both_reference_views_for_mapping_payload_when_enabled():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key=None,
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Review FAT Package",
            task_key="review-fat-package",
            status="completed",
            dependencies=["TASK-001", "TASK-002"],
        ),
        TaskModel(
            task_id="TASK-004",
            order=4,
            title="Archive FAT Package",
            task_key="archive-fat-package",
            status="planned",
            dependencies=["TASK-003"],
        ),
    ]

    result = _prepare_task_read_payload(
        tasks,
        tasks[2].model_dump(),
        show_dependency_refs=True,
        show_dependent_refs=True,
    )

    assert result["dependency_refs"] == [
        {"task_id": "TASK-001", "task_key": "prepare-fat"},
        {"task_id": "TASK-002", "task_key": "<none>"},
    ]
    assert result["dependent_refs"] == [
        {"task_id": "TASK-004", "task_key": "archive-fat-package"},
    ]
''',
        "rename shared read helper test and cover mapping payload",
    )

    cli_path.write_text(cli_text, encoding="utf-8")
    test_cli_path.write_text(test_cli_text, encoding="utf-8")

    print("apply_slice29.py patch logic completed successfully.")
    print(f"Updated: {cli_path}")
    print(f"Updated: {test_cli_path}")


if __name__ == "__main__":
    main()
