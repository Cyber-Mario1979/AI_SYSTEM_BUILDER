import re

from asbp.state_model import PlanningModel, WorkPackageModel


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