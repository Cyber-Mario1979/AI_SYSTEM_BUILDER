import json

import pytest

from asbp.cli import load_validated_state, save_validated_state
from asbp.state_model import SelectorContextModel, StateModel, WorkPackageModel


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


def test_save_validated_state_persists_work_packages(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))

    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_load_validated_state_reloads_valid_persisted_work_packages(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification",
      "status": "open"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert len(state.work_packages) == 1
    assert state.work_packages[0].wp_id == "WP-001"
    assert state.work_packages[0].title == "Tablet press qualification"
    assert state.work_packages[0].status == "open"


def test_load_validated_state_rejects_invalid_persisted_work_package_wp_id(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-1",
      "title": "Tablet press qualification",
      "status": "open"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="String should match pattern"):
        load_validated_state(state_file)


def test_load_validated_state_rejects_invalid_persisted_work_package_status(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification",
      "status": "planned"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Input should be"):
        load_validated_state(state_file)


def test_load_validated_state_rejects_duplicate_persisted_wp_id(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [],
  "work_packages": [
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification A",
      "status": "open"
    },
    {
      "wp_id": "WP-001",
      "title": "Tablet press qualification B",
      "status": "in_progress"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate wp_id is not allowed: WP-001"):
        load_validated_state(state_file)


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

def test_work_package_model_accepts_selector_context_system_type():
    work_package = WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
        selector_context=SelectorContextModel(system_type="process-equipment"),
    )

    assert work_package.selector_context is not None
    assert work_package.selector_context.system_type == "process-equipment"


def test_save_validated_state_omits_null_selector_context_for_work_package(
    tmp_path,
    monkeypatch,
):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_save_validated_state_persists_selector_context_for_work_package(
    tmp_path,
    monkeypatch,
):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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
                selector_context=SelectorContextModel(system_type="process-equipment"),
            )
        ],
    )

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "system_type": "process-equipment",
            },
        }
    ]
def test_work_package_model_accepts_selector_context_preset_id():
    work_package = WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
        ),
    )

    assert work_package.selector_context is not None
    assert work_package.selector_context.system_type is None
    assert work_package.selector_context.preset_id == "oral-solid-dose-standard"


def test_save_validated_state_persists_selector_context_preset_id_without_null_system_type(
    tmp_path,
    monkeypatch,
):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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
                selector_context=SelectorContextModel(
                    preset_id="oral-solid-dose-standard",
                ),
            )
        ],
    )

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "preset_id": "oral-solid-dose-standard",
            },
        }
    ]


def test_save_validated_state_persists_selector_context_with_system_type_and_preset_id(
    tmp_path,
    monkeypatch,
):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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
                selector_context=SelectorContextModel(
                    system_type="process-equipment",
                    preset_id="oral-solid-dose-standard",
                ),
            )
        ],
    )

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "system_type": "process-equipment",
                "preset_id": "oral-solid-dose-standard",
            },
        }
    ]

def test_work_package_model_accepts_selector_context_standards_bundles():
    work_package = WorkPackageModel(
        wp_id="WP-001",
        title="Tablet press qualification",
        status="open",
        selector_context=SelectorContextModel(
            system_type="process-equipment",
            standards_bundles=["cqv-core", "automation"],
        ),
    )

    assert work_package.selector_context is not None
    assert work_package.selector_context.standards_bundles == [
        "cqv-core",
        "automation",
    ]


def test_work_package_model_rejects_standards_bundles_without_cqv_core():
    with pytest.raises(
        ValueError,
        match="standards_bundles must include cqv-core as the baseline bundle",
    ):
        WorkPackageModel.model_validate(
            {
                "wp_id": "WP-001",
                "title": "Tablet press qualification",
                "status": "open",
                "selector_context": {
                    "system_type": "process-equipment",
                    "standards_bundles": ["automation"],
                },
            }
        )


def test_save_validated_state_persists_selector_context_with_standards_bundles(
    tmp_path,
    monkeypatch,
):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("asbp.cli.get_state_file_path", lambda: state_file)

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
                selector_context=SelectorContextModel(
                    system_type="process-equipment",
                    preset_id="oral-solid-dose-standard",
                    standards_bundles=["cqv-core", "automation"],
                ),
            )
        ],
    )

    save_validated_state(state)

    saved = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "system_type": "process-equipment",
                "preset_id": "oral-solid-dose-standard",
                "standards_bundles": ["cqv-core", "automation"],
            },
        }
    ]
