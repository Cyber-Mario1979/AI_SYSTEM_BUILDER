from asbp.state_model import WorkPackageModel


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
    status: str | None = None,
    title: str | None = None,
    wp_id: str | None = None,
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
    status: str,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    work_package.status = status
    return work_package


def delete_work_package_by_id(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
) -> tuple[list[WorkPackageModel], bool]:
    updated_work_packages = [
        work_package
        for work_package in work_packages
        if work_package.wp_id != wp_id
    ]
    deleted_flag = len(updated_work_packages) != len(work_packages)
    return updated_work_packages, deleted_flag


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

