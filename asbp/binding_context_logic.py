from asbp.state_model import PlanningModel, WorkPackageModel


def _find_work_package_by_id(
    work_packages: list[WorkPackageModel],
    *,
    work_package_id: str,
) -> WorkPackageModel | None:
    for work_package in work_packages:
        if work_package.wp_id == work_package_id:
            return work_package
    return None


def validate_work_package_binding_context_for_planning(
    work_packages: list[WorkPackageModel],
    *,
    work_package_id: str,
    plan_id: str,
) -> None:
    work_package = _find_work_package_by_id(
        work_packages,
        work_package_id=work_package_id,
    )
    if work_package is None:
        raise ValueError(
            "Planning-bound Work Package not found: "
            f"{plan_id} -> {work_package_id}"
        )

    selector_context = work_package.selector_context
    if selector_context is None:
        raise ValueError(
            "Planning-bound Work Package must declare selector_context: "
            f"{plan_id} -> {work_package_id}"
        )

    if selector_context.scope_intent is None:
        raise ValueError(
            "Planning-bound Work Package must declare "
            "selector_context.scope_intent: "
            f"{plan_id} -> {work_package_id}"
        )

    if not selector_context.standards_bundles:
        raise ValueError(
            "Planning-bound Work Package must declare "
            "selector_context.standards_bundles: "
            f"{plan_id} -> {work_package_id}"
        )


def validate_persisted_plan_binding_context_consistency(
    plans: list[PlanningModel],
    work_packages: list[WorkPackageModel],
) -> None:
    for plan in plans:
        if plan.plan_state != "committed" and not plan.generated_task_plans:
            continue

        validate_work_package_binding_context_for_planning(
            work_packages,
            work_package_id=plan.work_package_id,
            plan_id=plan.plan_id,
        )