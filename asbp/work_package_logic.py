from typing import Literal

from asbp.collection_logic import validate_task_work_package_membership_change
from asbp.task_logic import find_task_by_reference
from asbp.state_model import (
    ScopeIntentId,
    SelectorContextModel,
    StandardsBundleId,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)




def find_work_package_by_id(
    work_packages: list[WorkPackageModel],
    wp_id: str,
) -> WorkPackageModel | None:
    for work_package in work_packages:
        if work_package.wp_id == wp_id:
            return work_package
    return None


def filter_work_packages(
    work_packages: list[WorkPackageModel],
    *,
    tasks: list[TaskModel] | None = None,
    status: str | None = None,
    title: str | None = None,
    wp_id: str | None = None,
    task_id: str | None = None,
) -> list[WorkPackageModel]:
    filtered = list(work_packages)

    if status is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.status == status
        ]

    if title is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.title == title
        ]

    if wp_id is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.wp_id == wp_id
        ]

    if task_id is not None:
        matching_work_package_ids = {
            task.work_package_id
            for task in (tasks or [])
            if task.task_id == task_id and task.work_package_id is not None
        }
        filtered = [
            work_package
            for work_package in filtered
            if work_package.wp_id in matching_work_package_ids
        ]

    return filtered


def create_work_package(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    title: str,
) -> WorkPackageModel:
    if find_work_package_by_id(work_packages, wp_id) is not None:
        raise ValueError(f"Duplicate wp_id is not allowed: {wp_id}")

    return WorkPackageModel(
        wp_id=wp_id,
        title=title,
        status="open",
    )


def update_work_package_status(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    status: Literal["open", "in_progress", "completed"],
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    work_package.status = status
    return work_package


def delete_work_package_by_id(
    work_packages: list[WorkPackageModel],
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> tuple[list[WorkPackageModel], bool, str | None]:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return list(work_packages), False, None

    associated_task_ids = build_work_package_task_ids(tasks, wp_id=wp_id)
    if associated_task_ids:
        task_ids_display = ", ".join(associated_task_ids)
        return (
            list(work_packages),
            False,
            f"Work Package cannot be deleted while tasks are associated: "
            f"{wp_id} -> [{task_ids_display}]",
        )

    updated_work_packages = [
        existing_work_package
        for existing_work_package in work_packages
        if existing_work_package.wp_id != wp_id
    ]
    return updated_work_packages, True, None


def update_work_package_title(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    title: str,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=title,
        status=work_package.status,
    )
    work_package.title = validated_work_package.title
    return work_package


CQV_CORE_STANDARD_BUNDLE: StandardsBundleId = "cqv-core"
CANONICAL_STANDARD_BUNDLE_ORDER: tuple[StandardsBundleId, ...] = (
    "cqv-core",
    "cleanroom-hvac",
    "automation",
)


def _build_effective_standards_bundles(
    add_on_bundle_ids: list[StandardsBundleId] | None,
) -> list[StandardsBundleId]:
    selected_add_on_bundle_ids = set(add_on_bundle_ids or [])
    effective_standards_bundles: list[StandardsBundleId] = [
        CQV_CORE_STANDARD_BUNDLE
    ]

    for bundle_id in CANONICAL_STANDARD_BUNDLE_ORDER:
        if bundle_id == CQV_CORE_STANDARD_BUNDLE:
            continue
        if bundle_id in selected_add_on_bundle_ids:
            effective_standards_bundles.append(bundle_id)

    return effective_standards_bundles


def _build_updated_selector_context(
    work_package: WorkPackageModel,
    *,
    system_type: str | None = None,
    preset_id: str | None = None,
    scope_intent: ScopeIntentId | None = None,
    standards_bundles: list[StandardsBundleId] | None = None,
) -> SelectorContextModel:
    current_selector_context = work_package.selector_context

    next_system_type = (
        system_type
        if system_type is not None
        else (
            current_selector_context.system_type
            if current_selector_context is not None
            else None
        )
    )
    next_preset_id = (
        preset_id
        if preset_id is not None
        else (
            current_selector_context.preset_id
            if current_selector_context is not None
            else None
        )
    )
    next_scope_intent = (
        scope_intent
        if scope_intent is not None
        else (
            current_selector_context.scope_intent
            if current_selector_context is not None
            else None
        )
    )
    next_standards_bundles = (
        list(standards_bundles)
        if standards_bundles is not None
        else (
            list(current_selector_context.standards_bundles)
            if current_selector_context is not None
            else []
        )
    )

    return SelectorContextModel(
        system_type=next_system_type,
        preset_id=next_preset_id,
        scope_intent=next_scope_intent,
        standards_bundles=next_standards_bundles,
    )


def set_work_package_selector_type(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    system_type: str,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=work_package.title,
        status=work_package.status,
        selector_context=_build_updated_selector_context(
            work_package,
            system_type=system_type,
        ),
    )
    work_package.selector_context = validated_work_package.selector_context
    return work_package


def set_work_package_preset(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    preset_id: str,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=work_package.title,
        status=work_package.status,
        selector_context=_build_updated_selector_context(
            work_package,
            preset_id=preset_id,
        ),
    )
    work_package.selector_context = validated_work_package.selector_context
    return work_package


def set_work_package_standards_bundles(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    add_on_bundle_ids: list[StandardsBundleId],
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    if work_package.selector_context is None:
        raise ValueError(
            "Work Package selector context seed must exist before standards bundles "
            f"can be bound: {wp_id}"
        )

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=work_package.title,
        status=work_package.status,
        selector_context=_build_updated_selector_context(
            work_package,
            standards_bundles=_build_effective_standards_bundles(
                add_on_bundle_ids,
            ),
        ),
    )
    work_package.selector_context = validated_work_package.selector_context
    return work_package


def set_work_package_scope_intent(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    scope_intent: ScopeIntentId,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    if work_package.selector_context is None:
        raise ValueError(
            "Work Package selector context seed must exist before scope intent "
            f"can be bound: {wp_id}"
        )

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=work_package.title,
        status=work_package.status,
        selector_context=_build_updated_selector_context(
            work_package,
            scope_intent=scope_intent,
        ),
    )
    work_package.selector_context = validated_work_package.selector_context
    return work_package


def set_task_work_package(
    tasks: list[TaskModel],
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    *,
    task_ref: str,
    wp_id: str,
) -> tuple[TaskModel | None, str | None]:
    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, f"Task not found: {task_ref}"

    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None, f"Work Package not found: {wp_id}"

    membership_change_error = validate_task_work_package_membership_change(
        task_collections,
        task_id=target_task.task_id,
        target_work_package_id=work_package.wp_id,
    )
    if membership_change_error is not None:
        return None, membership_change_error

    if (
        target_task.work_package_id is not None
        and target_task.work_package_id != work_package.wp_id
    ):
        return (
            None,
            "Task already associated with a different Work Package: "
            f"{target_task.task_id} -> {target_task.work_package_id}",
        )

    target_task.work_package_id = work_package.wp_id
    return target_task, None

def clear_task_work_package(
    tasks: list[TaskModel],
    task_collections: list[TaskCollectionModel],
    *,
    task_ref: str,
) -> tuple[TaskModel | None, str | None]:
    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, f"Task not found: {task_ref}"

    membership_change_error = validate_task_work_package_membership_change(
        task_collections,
        task_id=target_task.task_id,
        target_work_package_id=None,
    )
    if membership_change_error is not None:
        return None, membership_change_error

    target_task.work_package_id = None
    return target_task, None


def build_work_package_task_ids(
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> list[str]:
    return [
        task.task_id
        for task in tasks
        if task.work_package_id == wp_id
    ]


def validate_persisted_task_work_package_links(
    tasks: list[TaskModel],
    work_packages: list[WorkPackageModel],
) -> None:
    existing_wp_ids = {work_package.wp_id for work_package in work_packages}

    for task in tasks:
        if task.work_package_id is None:
            continue

        if task.work_package_id not in existing_wp_ids:
            raise ValueError(
                "Persisted task work_package_id does not exist: "
                f"{task.task_id} -> {task.work_package_id}"
            )
