from __future__ import annotations

from typing import Any

from asbp.calendar_source_store import list_calendar_ids
from asbp.cross_library_validation_model import (
    CrossLibraryValidationIssueModel,
    CrossLibraryValidationResultModel,
    build_validation_result,
)
from asbp.planning_basis_source_store import (
    find_missing_task_pool_duration_refs,
    list_duration_ref_ids,
)
from asbp.profile_source_store import list_profile_ids
from asbp.source_library_baseline_store import (
    load_default_source_library_baseline_runtime,
)
from asbp.standards_bundle_binding_store import (
    list_standards_bundle_ids,
    load_default_standards_bundle_binding_library,
)
from asbp.task_pool_source_store import list_task_pool_ids


def validate_default_cross_library_baseline() -> CrossLibraryValidationResultModel:
    runtime = load_default_source_library_baseline_runtime()
    return validate_cross_library_runtime(runtime)


def assert_default_cross_library_validation_passes() -> None:
    runtime = load_default_source_library_baseline_runtime()
    assert_cross_library_validation_passes(runtime)


def assert_cross_library_validation_passes(runtime: Any) -> None:
    result = validate_cross_library_runtime(runtime)
    if result.status != "passed":
        issue_summary = "; ".join(
            f"{issue.issue_code}: {issue.message}"
            for issue in result.issues
        )
        raise ValueError(f"Cross-library validation failed: {issue_summary}")


def validate_cross_library_runtime(runtime: Any) -> CrossLibraryValidationResultModel:
    issues: list[CrossLibraryValidationIssueModel] = []
    standards_bundle_library = load_default_standards_bundle_binding_library()

    _validate_non_empty_libraries(runtime, standards_bundle_library, issues)
    _validate_task_dependencies(runtime, issues)
    _validate_duration_refs(runtime, issues)
    _validate_mapping_references(runtime, standards_bundle_library, issues)
    _validate_mapping_applicability(runtime, issues)

    return build_validation_result(issues)


def build_cross_library_validation_issue_id(
    issue_code: str,
    related_ids: list[str],
) -> str:
    return f"M27.9::{issue_code}::{'|'.join(related_ids)}"


def _validate_non_empty_libraries(
    runtime: Any,
    standards_bundle_library: Any,
    issues: list[CrossLibraryValidationIssueModel],
) -> None:
    library_checks = [
        ("task_pools", "task_pools", runtime.task_pool_library.task_pools),
        ("profiles", "profiles", runtime.profile_library.profiles),
        ("calendars", "calendars", runtime.calendar_library.calendars),
        (
            "planning_basis",
            "duration_sources",
            runtime.planning_basis_library.duration_sources,
        ),
        ("mappings", "mappings", runtime.mapping_library.mappings),
        (
            "standards_bundles",
            "standards bundle bindings",
            standards_bundle_library.bindings,
        ),
    ]

    for source_family, label, collection in library_checks:
        if not collection:
            issues.append(
                CrossLibraryValidationIssueModel(
                    issue_code="EMPTY_LIBRARY",
                    source_family=source_family,
                    message=f"M28.4 validation found empty {label} library.",
                    related_ids=[label],
                )
            )


def _validate_task_dependencies(
    runtime: Any,
    issues: list[CrossLibraryValidationIssueModel],
) -> None:
    for task_pool in runtime.task_pool_library.task_pools:
        atomic_task_ids = {
            task.atomic_task_id
            for task in task_pool.tasks
        }

        for task in task_pool.tasks:
            for dependency in task.dependencies:
                if dependency.atomic_task_id not in atomic_task_ids:
                    issues.append(
                        CrossLibraryValidationIssueModel(
                            issue_code="DANGLING_ATOMIC_TASK_REF",
                            source_family="task_pools",
                            message=(
                                "Task dependency references missing atomic task "
                                f"in {task_pool.task_pool_id}: "
                                f"{task.atomic_task_id} -> "
                                f"{dependency.atomic_task_id}"
                            ),
                            related_ids=[
                                task_pool.task_pool_id,
                                task.atomic_task_id,
                                dependency.atomic_task_id,
                            ],
                        )
                    )


def _validate_duration_refs(
    runtime: Any,
    issues: list[CrossLibraryValidationIssueModel],
) -> None:
    missing_duration_refs = find_missing_task_pool_duration_refs(
        runtime.planning_basis_library,
        runtime.task_pool_library,
    )

    for duration_ref_id in missing_duration_refs:
        issues.append(
            CrossLibraryValidationIssueModel(
                issue_code="UNCOVERED_DURATION_REF",
                source_family="planning_basis",
                message=(
                    "Task-pool duration_ref_id is not covered by planning "
                    f"basis source records: {duration_ref_id}"
                ),
                related_ids=[duration_ref_id],
            )
        )


def _validate_mapping_references(
    runtime: Any,
    standards_bundle_library: Any,
    issues: list[CrossLibraryValidationIssueModel],
) -> None:
    known_profile_ids = set(list_profile_ids(runtime.profile_library))
    known_task_pool_ids = set(list_task_pool_ids(runtime.task_pool_library))
    known_atomic_task_source_ids = _collect_atomic_task_source_ids(runtime)
    known_duration_ref_ids = set(list_duration_ref_ids(runtime.planning_basis_library))
    known_calendar_ids = set(list_calendar_ids(runtime.calendar_library))
    known_standards_bundle_ids = set(
        list_standards_bundle_ids(standards_bundle_library)
    )

    for mapping in runtime.mapping_library.mappings:
        for reference in [*mapping.source_refs, *mapping.target_refs]:
            if reference.reference_status != "resolved_source":
                if reference.resolution_checkpoint is None:
                    issues.append(
                        CrossLibraryValidationIssueModel(
                            issue_code="FUTURE_REF_WITHOUT_RESOLUTION",
                            source_family="mappings",
                            message=(
                                "Future or placeholder mapping reference is "
                                "missing resolution checkpoint: "
                                f"{reference.reference_id}"
                            ),
                            related_ids=[mapping.mapping_id, reference.reference_id],
                        )
                    )
                continue

            if reference.reference_type == "profile":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_profile_ids,
                    issue_code="DANGLING_PROFILE_REF",
                    message_prefix="Mapping profile reference does not exist",
                    mapping_id=mapping.mapping_id,
                )
            elif reference.reference_type == "task_pool":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_task_pool_ids,
                    issue_code="DANGLING_TASK_POOL_REF",
                    message_prefix="Mapping task-pool reference does not exist",
                    mapping_id=mapping.mapping_id,
                )
            elif reference.reference_type == "atomic_task":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_atomic_task_source_ids,
                    issue_code="DANGLING_ATOMIC_TASK_REF",
                    message_prefix="Mapping atomic-task reference does not exist",
                    mapping_id=mapping.mapping_id,
                )
            elif reference.reference_type == "standard_bundle":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_standards_bundle_ids,
                    issue_code="DANGLING_STANDARDS_BUNDLE_REF",
                    message_prefix="Mapping standards-bundle reference does not exist",
                    mapping_id=mapping.mapping_id,
                )
            elif reference.reference_type in {
                "document_expectation",
                "template",
            }:
                issues.append(
                    CrossLibraryValidationIssueModel(
                        issue_code="RESOLVED_FUTURE_REF",
                        source_family="mappings",
                        message=(
                            "Document and template mapping refs must not be "
                            "resolved authority before their roadmap-authorized "
                            "implementation checkpoints: "
                            f"{reference.reference_id}"
                        ),
                        related_ids=[mapping.mapping_id, reference.reference_id],
                    )
                )
            elif reference.reference_type == "calendar":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_calendar_ids,
                    issue_code="DANGLING_TASK_POOL_REF",
                    message_prefix="Mapping calendar reference does not exist",
                    mapping_id=mapping.mapping_id,
                )
            elif reference.reference_type == "duration_ref":
                _append_missing_reference_issue(
                    issues=issues,
                    reference_id=reference.reference_id,
                    known_ids=known_duration_ref_ids,
                    issue_code="UNCOVERED_DURATION_REF",
                    message_prefix="Mapping duration reference does not exist",
                    mapping_id=mapping.mapping_id,
                )


def _validate_mapping_applicability(
    runtime: Any,
    issues: list[CrossLibraryValidationIssueModel],
) -> None:
    for mapping in runtime.mapping_library.mappings:
        for tag in mapping.applicability_tags:
            if not tag.strip():
                issues.append(
                    CrossLibraryValidationIssueModel(
                        issue_code="BLANK_APPLICABILITY_TAG",
                        source_family="mappings",
                        message=(
                            "Mapping applicability tag must not be blank: "
                            f"{mapping.mapping_id}"
                        ),
                        related_ids=[mapping.mapping_id],
                    )
                )


def _collect_atomic_task_source_ids(runtime: Any) -> set[str]:
    atomic_task_source_ids: set[str] = set()

    for task_pool in runtime.task_pool_library.task_pools:
        for task in task_pool.tasks:
            atomic_task_source_ids.add(
                f"{task_pool.task_pool_id}::{task.atomic_task_id}"
            )

    return atomic_task_source_ids


def _append_missing_reference_issue(
    *,
    issues: list[CrossLibraryValidationIssueModel],
    reference_id: str,
    known_ids: set[str],
    issue_code: str,
    message_prefix: str,
    mapping_id: str,
) -> None:
    if reference_id in known_ids:
        return

    issues.append(
        CrossLibraryValidationIssueModel(
            issue_code=issue_code,
            source_family="mappings",
            message=f"{message_prefix}: {reference_id}",
            related_ids=[mapping_id, reference_id],
        )
    )
