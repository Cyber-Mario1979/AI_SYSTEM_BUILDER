from asbp.state_model import TaskModel


def validate_persisted_task_source_contracts(
    tasks: list[TaskModel],
) -> None:
    for task in tasks:
        if task.instantiation_mode == "manual":
            continue

        if task.source_definition_kind != "task_pool":
            raise ValueError(
                "Persisted preset-resolved task must declare "
                "source_definition_kind=task_pool: "
                f"{task.task_id}"
            )

        if task.source_definition_id is None:
            raise ValueError(
                "Persisted preset-resolved task must declare "
                f"source_definition_id: {task.task_id}"
            )

        if task.work_package_id is None:
            raise ValueError(
                "Persisted preset-resolved task must declare "
                f"work_package_id: {task.task_id}"
            )
