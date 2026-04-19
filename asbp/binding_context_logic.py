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


def build_work_package_binding_context_blockers(
    work_packages: list[WorkPackageModel],
    *,
    work_package_id: str,
) -> list[str]:
    work_package = _find_work_package_by_id(
        work_packages,
        work_package_id=work_package_id,
    )
    if work_package is None:
        return ["work_package_missing"]

    selector_context = work_package.selector_context
    if selector_context is None:
        return ["selector_context_missing"]

    blockers: list[str] = []
    if selector_context.scope_intent is None:
        blockers.append("scope_intent_missing")
    if not selector_context.standards_bundles:
        blockers.append("standards_bundles_missing")

    return blockers


def validate_work_package_binding_context_for_planning(
    work_packages: list[WorkPackageModel],
    *,
    work_package_id: str,
    plan_id: str,
) -> None:
    blockers = build_work_package_binding_context_blockers(
        work_packages,
        work_package_id=work_package_id,
    )

    if not blockers:
        return

    primary_blocker = blockers[0]

    if primary_blocker == "work_package_missing":
        raise ValueError(
            "Planning-bound Work Package not found: "
            f"{plan_id} -> {work_package_id}"
        )

    if primary_blocker == "selector_context_missing":
        raise ValueError(
            "Planning-bound Work Package must declare selector_context: "
            f"{plan_id} -> {work_package_id}"
        )

    if primary_blocker == "scope_intent_missing":
        raise ValueError(
            "Planning-bound Work Package must declare "
            "selector_context.scope_intent: "
            f"{plan_id} -> {work_package_id}"
        )

    if primary_blocker == "standards_bundles_missing":
        raise ValueError(
            "Planning-bound Work Package must declare "
            "selector_context.standards_bundles: "
            f"{plan_id} -> {work_package_id}"
        )

    raise ValueError(
        "Unknown binding-context blocker encountered: "
        f"{plan_id} -> {work_package_id} -> {primary_blocker}"
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
