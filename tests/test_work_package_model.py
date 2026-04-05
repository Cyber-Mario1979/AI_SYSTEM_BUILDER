import pytest

from asbp.cli import load_validated_state
from asbp.state_model import StateModel, WorkPackageModel


def test_state_model_defaults_work_packages_to_empty_list():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        tasks=[],
    )

    assert state.work_packages == []


def test_state_model_accepts_valid_work_package_collection():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        tasks=[],
        work_packages=[
            WorkPackageModel(
                wp_id="WP-001",
                title="Tablet press qualification",
                status="open",
            )
        ],
    )

    assert len(state.work_packages) == 1
    assert state.work_packages[0].wp_id == "WP-001"
    assert state.work_packages[0].title == "Tablet press qualification"
    assert state.work_packages[0].status == "open"


def test_work_package_model_rejects_invalid_wp_id_format():
    with pytest.raises(ValueError, match="String should match pattern"):
        WorkPackageModel.model_validate(
            {
                "wp_id": "WP-1",
                "title": "Tablet press qualification",
                "status": "open",
            }
        )


def test_work_package_model_rejects_invalid_status():
    with pytest.raises(ValueError, match="Input should be"):
        WorkPackageModel.model_validate(
            {
                "wp_id": "WP-001",
                "title": "Tablet press qualification",
                "status": "planned",
            }
        )


def test_state_model_rejects_duplicate_wp_id():
    with pytest.raises(ValueError, match="Duplicate wp_id is not allowed: WP-001"):
        StateModel(
            project="AI_SYSTEM_BUILDER",
            version="0.8.0",
            status="in_flight",
            tasks=[],
            work_packages=[
                WorkPackageModel(
                    wp_id="WP-001",
                    title="Tablet press qualification A",
                    status="open",
                ),
                WorkPackageModel(
                    wp_id="WP-001",
                    title="Tablet press qualification B",
                    status="in_progress",
                ),
            ],
        )


def test_load_validated_state_accepts_legacy_state_without_work_packages(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": []
}
""".strip(),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert state.work_packages == []