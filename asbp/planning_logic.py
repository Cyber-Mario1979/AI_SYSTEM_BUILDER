import re
from datetime import datetime, timedelta

from asbp.state_model import (
    DurationSourceId,
    GeneratedTaskPlanModel,
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WeekdayId,
    WorkPackageModel,
    WorkmonthModeId,
)
_WEEKDAY_TO_PYTHON_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def generate_next_plan_id(plans: list[PlanningModel]) -> str:
    if not plans:
        return "PLAN-001"

    max_number = 0

    for plan in plans:
        match = re.fullmatch(r"PLAN-(\d{3})", plan.plan_id)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    return f"PLAN-{max_number + 1:03d}"


def find_plan_by_id(
    plans: list[PlanningModel],
    plan_id: str,
) -> PlanningModel | None:
    for plan in plans:
        if plan.plan_id == plan_id:
            return plan
    return None

def _build_committed_task_id_set(
    task_collections: list[TaskCollectionModel],
) -> set[str]:
    committed_task_ids: set[str] = set()

    for task_collection in task_collections:
        if task_collection.collection_state != "committed":
            continue
        committed_task_ids.update(task_collection.task_ids)

    return committed_task_ids


def _build_eligible_plan_tasks(
    tasks: list[TaskModel],
    *,
    work_package_id: str,
    committed_task_ids: set[str],
) -> list[TaskModel]:
    eligible_tasks = [
        task
        for task in tasks
        if task.work_package_id == work_package_id
        and task.task_id in committed_task_ids
    ]
    return sorted(eligible_tasks, key=lambda task: (task.order, task.task_id))


def _advance_to_next_working_day(
    start_at: datetime,
    working_day_indices: set[int],
) -> datetime:
    candidate = start_at + timedelta(days=1)

    while candidate.weekday() not in working_day_indices:
        candidate += timedelta(days=1)

    return candidate


def _build_task_window(
    start_at: datetime,
    *,
    duration_days: int,
    planning_calendar: PlanningCalendarModel,
) -> tuple[datetime, datetime]:
    working_day_indices = {
        _WEEKDAY_TO_PYTHON_INDEX[weekday]
        for weekday in planning_calendar.working_days
    }
    current_day_start = start_at

    for day_index in range(duration_days):
        current_day_finish = current_day_start + timedelta(
            hours=planning_calendar.workday_hours
        )

        if day_index == duration_days - 1:
            next_task_start = _advance_to_next_working_day(
                current_day_start,
                working_day_indices,
            )
            return current_day_finish, next_task_start

        current_day_start = _advance_to_next_working_day(
            current_day_start,
            working_day_indices,
        )

    raise ValueError("duration_days must be at least 1")


def _validate_plan_generation_preconditions(plan: PlanningModel) -> None:
    if plan.planning_basis is None:
        raise ValueError(
            "Plan planning_basis must exist before baseline generation: "
            f"{plan.plan_id}"
        )

    if plan.planned_start_at is None:
        raise ValueError(
            "Plan planned_start_at must exist before baseline generation: "
            f"{plan.plan_id}"
        )

    if plan.planning_calendar is None:
        raise ValueError(
            "Plan planning_calendar must exist before baseline generation: "
            f"{plan.plan_id}"
        )

    working_day_indices = {
        _WEEKDAY_TO_PYTHON_INDEX[weekday]
        for weekday in plan.planning_calendar.working_days
    }
    if plan.planned_start_at.weekday() not in working_day_indices:
        raise ValueError(
            "Plan planned_start_at must fall on a configured working day: "
            f"{plan.plan_id}"
        )


def _validate_eligible_tasks_for_generation(
    eligible_tasks: list[TaskModel],
    *,
    plan_id: str,
) -> None:
    if not eligible_tasks:
        raise ValueError(
            f"No eligible committed tasks found for baseline generation: {plan_id}"
        )

    eligible_task_ids = {task.task_id for task in eligible_tasks}

    for task in eligible_tasks:
        if task.duration is None:
            raise ValueError(
                "Task duration is required for baseline generation: "
                f"{task.task_id}"
            )

        invalid_dependencies = [
            dependency_task_id
            for dependency_task_id in task.dependencies
            if dependency_task_id not in eligible_task_ids
        ]
        if invalid_dependencies:
            dependency_display = ", ".join(invalid_dependencies)
            raise ValueError(
                "Task dependency is outside eligible committed plan scope: "
                f"{task.task_id} -> [{dependency_display}]"
            )


def _order_tasks_for_generation(
    eligible_tasks: list[TaskModel],
    *,
    plan_id: str,
) -> list[TaskModel]:
    tasks_by_id = {task.task_id: task for task in eligible_tasks}
    remaining_dependencies = {
        task.task_id: {
            dependency_task_id
            for dependency_task_id in task.dependencies
            if dependency_task_id in tasks_by_id
        }
        for task in eligible_tasks
    }
    dependent_task_ids: dict[str, set[str]] = {
        task.task_id: set() for task in eligible_tasks
    }

    for task in eligible_tasks:
        for dependency_task_id in remaining_dependencies[task.task_id]:
            dependent_task_ids[dependency_task_id].add(task.task_id)

    available_tasks = sorted(
        [
            tasks_by_id[task_id]
            for task_id, dependency_ids in remaining_dependencies.items()
            if not dependency_ids
        ],
        key=lambda task: (task.order, task.task_id),
    )

    ordered_tasks: list[TaskModel] = []

    while available_tasks:
        current_task = available_tasks.pop(0)
        ordered_tasks.append(current_task)

        newly_available_tasks: list[TaskModel] = []
        for dependent_task_id in sorted(dependent_task_ids[current_task.task_id]):
            dependency_ids = remaining_dependencies[dependent_task_id]
            dependency_ids.discard(current_task.task_id)

            if not dependency_ids:
                newly_available_tasks.append(tasks_by_id[dependent_task_id])

        available_tasks = sorted(
            available_tasks + newly_available_tasks,
            key=lambda task: (task.order, task.task_id),
        )

    if len(ordered_tasks) != len(eligible_tasks):
        raise ValueError(
            "Plan generation failed due to cyclic dependencies within eligible "
            f"committed scope: {plan_id}"
        )

    return ordered_tasks


def _build_sorted_generated_task_plan_payloads(
    generated_task_plans: list[GeneratedTaskPlanModel],
) -> list[dict]:
    payloads = [
        generated_task_plan.model_dump(mode="json")
        for generated_task_plan in generated_task_plans
    ]
    return sorted(
        payloads,
        key=lambda payload: (payload["sequence_order"], payload["task_id"]),
    )




def _validate_plan_commit_preconditions(plan: PlanningModel) -> None:
    if plan.plan_state == "committed":
        raise ValueError(f"Plan is already committed: {plan.plan_id}")

    _validate_plan_generation_preconditions(plan)

    if not plan.generated_task_plans:
        raise ValueError(
            "Plan generated_task_plans must exist before commit: "
            f"{plan.plan_id}"
        )


def commit_plan(
    plans: list[PlanningModel],
    *,
    plan_id: str,
) -> PlanningModel | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    _validate_plan_commit_preconditions(plan)

    validated_plan = PlanningModel(
        plan_id=plan.plan_id,
        work_package_id=plan.work_package_id,
        plan_state="committed",
        planning_basis=plan.planning_basis,
        planned_start_at=plan.planned_start_at,
        planning_calendar=plan.planning_calendar,
        generated_task_plans=plan.generated_task_plans,
    )
    plan.plan_state = validated_plan.plan_state
    return plan

def set_plan_planning_basis(
    plans: list[PlanningModel],
    *,
    plan_id: str,
    duration_source: DurationSourceId,
    basis_label: str | None = None,
) -> PlanningModel | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    validated_plan = PlanningModel(
        plan_id=plan.plan_id,
        work_package_id=plan.work_package_id,
        plan_state=plan.plan_state,
        planning_basis=PlanningBasisModel(
            duration_source=duration_source,
            basis_label=basis_label,
        ),
        planned_start_at=plan.planned_start_at,
        planning_calendar=plan.planning_calendar,
    )
    plan.planning_basis = validated_plan.planning_basis
    return plan


def set_plan_planned_start_at(
    plans: list[PlanningModel],
    *,
    plan_id: str,
    planned_start_at: datetime,
) -> PlanningModel | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    validated_plan = PlanningModel(
        plan_id=plan.plan_id,
        work_package_id=plan.work_package_id,
        plan_state=plan.plan_state,
        planning_basis=plan.planning_basis,
        planned_start_at=planned_start_at,
        planning_calendar=plan.planning_calendar,
    )
    plan.planned_start_at = validated_plan.planned_start_at
    return plan


def set_plan_planning_calendar(
    plans: list[PlanningModel],
    *,
    plan_id: str,
    working_days: list[WeekdayId],
    workday_hours: int,
    workmonth_mode: WorkmonthModeId = "calendar_month",
) -> PlanningModel | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    validated_plan = PlanningModel(
        plan_id=plan.plan_id,
        work_package_id=plan.work_package_id,
        plan_state=plan.plan_state,
        planning_basis=plan.planning_basis,
        planned_start_at=plan.planned_start_at,
        planning_calendar=PlanningCalendarModel(
            working_days=working_days,
            workday_hours=workday_hours,
            workmonth_mode=workmonth_mode,
        ),
    )
    plan.planning_calendar = validated_plan.planning_calendar
    return plan


def generate_plan_baseline(
    plans: list[PlanningModel],
    tasks: list[TaskModel],
    task_collections: list[TaskCollectionModel],
    *,
    plan_id: str,
) -> PlanningModel | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    _validate_plan_generation_preconditions(plan)

    committed_task_ids = _build_committed_task_id_set(task_collections)
    eligible_tasks = _build_eligible_plan_tasks(
        tasks,
        work_package_id=plan.work_package_id,
        committed_task_ids=committed_task_ids,
    )
    _validate_eligible_tasks_for_generation(
        eligible_tasks,
        plan_id=plan.plan_id,
    )
    ordered_tasks = _order_tasks_for_generation(
        eligible_tasks,
        plan_id=plan.plan_id,
    )

    assert plan.planning_calendar is not None
    assert plan.planned_start_at is not None

    current_start_at = plan.planned_start_at
    generated_task_plans: list[GeneratedTaskPlanModel] = []

    for sequence_order, task in enumerate(ordered_tasks, start=1):
        assert task.duration is not None

        planned_finish_at, next_task_start_at = _build_task_window(
            current_start_at,
            duration_days=task.duration,
            planning_calendar=plan.planning_calendar,
        )

        generated_task_plans.append(
            GeneratedTaskPlanModel(
                task_id=task.task_id,
                sequence_order=sequence_order,
                duration_days=task.duration,
                dependency_task_ids=list(task.dependencies),
                planned_start_at=current_start_at,
                planned_finish_at=planned_finish_at,
            )
        )
        current_start_at = next_task_start_at

    validated_plan = PlanningModel(
        plan_id=plan.plan_id,
        work_package_id=plan.work_package_id,
        plan_state=plan.plan_state,
        planning_basis=plan.planning_basis,
        planned_start_at=plan.planned_start_at,
        planning_calendar=plan.planning_calendar,
        generated_task_plans=generated_task_plans,
    )
    plan.generated_task_plans = validated_plan.generated_task_plans
    return plan



def list_plan_review_rows(
    plans: list[PlanningModel],
    *,
    plan_id: str,
) -> list[dict] | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    return _build_sorted_generated_task_plan_payloads(plan.generated_task_plans)


def build_plan_review_payload(
    plans: list[PlanningModel],
    *,
    plan_id: str,
) -> dict | None:
    plan = find_plan_by_id(plans, plan_id)
    if plan is None:
        return None

    payload = plan.model_dump(mode="json")
    generated_task_plan_rows = _build_sorted_generated_task_plan_payloads(
        plan.generated_task_plans
    )

    payload["generated_task_plans"] = generated_task_plan_rows
    payload["generated_task_plan_count"] = len(generated_task_plan_rows)

    if generated_task_plan_rows:
        payload["generated_schedule_start_at"] = generated_task_plan_rows[0][
            "planned_start_at"
        ]
        payload["generated_schedule_finish_at"] = generated_task_plan_rows[-1][
            "planned_finish_at"
        ]
    else:
        payload["generated_schedule_start_at"] = None
        payload["generated_schedule_finish_at"] = None

    return payload


def validate_persisted_plan_work_package_links(
    plans: list[PlanningModel],
    work_packages: list[WorkPackageModel],
) -> None:
    existing_wp_ids = {work_package.wp_id for work_package in work_packages}

    for plan in plans:
        if plan.work_package_id not in existing_wp_ids:
            raise ValueError(
                "Persisted plan work_package_id does not exist: "
                f"{plan.plan_id} -> {plan.work_package_id}"
            )

def validate_persisted_generated_task_plan_task_ids(
    plans: list[PlanningModel],
) -> None:
    for plan in plans:
        seen_task_ids: set[str] = set()

        for generated_task_plan in plan.generated_task_plans:
            if generated_task_plan.task_id in seen_task_ids:
                raise ValueError(
                    "Duplicate generated task plan task_id is not allowed: "
                    f"{generated_task_plan.task_id}"
                )
            seen_task_ids.add(generated_task_plan.task_id)



def _is_legacy_generated_plan_snapshot(plan: PlanningModel) -> bool:
    return (
        plan.plan_state == "draft"
        and bool(plan.generated_task_plans)
        and plan.planning_basis is None
        and plan.planned_start_at is None
        and plan.planning_calendar is None
    )


def _validate_generated_task_plan_schedule_context(plan: PlanningModel) -> None:
    if plan.plan_state == "committed" and not plan.generated_task_plans:
        raise ValueError(
            "Committed plan must include generated_task_plans: "
            f"{plan.plan_id}"
        )

    if not plan.generated_task_plans:
        return

    if _is_legacy_generated_plan_snapshot(plan):
        return

    if plan.planning_basis is None:
        raise ValueError(
            "Plan with generated_task_plans must include planning_basis: "
            f"{plan.plan_id}"
        )

    if plan.planned_start_at is None:
        raise ValueError(
            "Plan with generated_task_plans must include planned_start_at: "
            f"{plan.plan_id}"
        )

    if plan.planning_calendar is None:
        raise ValueError(
            "Plan with generated_task_plans must include planning_calendar: "
            f"{plan.plan_id}"
        )


def validate_persisted_generated_task_plan_consistency(
    plans: list[PlanningModel],
    tasks: list[TaskModel],
) -> None:
    tasks_by_id = {task.task_id: task for task in tasks}

    for plan in plans:
        _validate_generated_task_plan_schedule_context(plan)

        if not plan.generated_task_plans:
            continue

        seen_task_ids: set[str] = set()
        seen_sequence_orders: set[int] = set()
        generated_task_id_set = {
            generated_task_plan.task_id
            for generated_task_plan in plan.generated_task_plans
        }

        for generated_task_plan in plan.generated_task_plans:
            if generated_task_plan.task_id in seen_task_ids:
                raise ValueError(
                    "Duplicate generated task plan task_id is not allowed: "
                    f"{generated_task_plan.task_id}"
                )
            seen_task_ids.add(generated_task_plan.task_id)

            if generated_task_plan.sequence_order in seen_sequence_orders:
                raise ValueError(
                    "Duplicate generated task plan sequence_order is not allowed: "
                    f"{plan.plan_id} -> {generated_task_plan.sequence_order}"
                )
            seen_sequence_orders.add(generated_task_plan.sequence_order)

            seen_dependency_ids: set[str] = set()

            for dependency_task_id in generated_task_plan.dependency_task_ids:
                if dependency_task_id == generated_task_plan.task_id:
                    raise ValueError(
                        "Generated task plan dependency cannot reference the same "
                        f"task: {plan.plan_id} -> {generated_task_plan.task_id}"
                    )

                if dependency_task_id in seen_dependency_ids:
                    raise ValueError(
                        "Duplicate generated task plan dependency is not allowed: "
                        f"{plan.plan_id} -> {generated_task_plan.task_id} -> "
                        f"{dependency_task_id}"
                    )
                seen_dependency_ids.add(dependency_task_id)

                if dependency_task_id not in generated_task_id_set:
                    raise ValueError(
                        "Generated task plan dependency must exist inside plan "
                        f"scope: {plan.plan_id} -> "
                        f"{generated_task_plan.task_id} -> {dependency_task_id}"
                    )

        expected_sequence_orders = list(range(1, len(plan.generated_task_plans) + 1))
        actual_sequence_orders = sorted(seen_sequence_orders)
        if actual_sequence_orders != expected_sequence_orders:
            raise ValueError(
                "Generated task plan sequence_order must be contiguous starting at 1: "
                f"{plan.plan_id}"
            )

        if _is_legacy_generated_plan_snapshot(plan):
            continue

        for generated_task_plan in plan.generated_task_plans:
            task = tasks_by_id.get(generated_task_plan.task_id)
            if task is None:
                raise ValueError(
                    "Generated task plan task_id does not exist in tasks: "
                    f"{plan.plan_id} -> {generated_task_plan.task_id}"
                )

            if task.work_package_id != plan.work_package_id:
                raise ValueError(
                    "Generated task plan task belongs to different work_package: "
                    f"{plan.plan_id} -> {generated_task_plan.task_id} "
                    f"({task.work_package_id})"
                )