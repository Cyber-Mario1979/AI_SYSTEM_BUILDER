import json
import subprocess
import sys
from pathlib import Path

import pytest

from asbp.state_store import load_validated_state


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def restore_state_file():
    original_exists = STATE_FILE.exists()
    original_text = STATE_FILE.read_text(encoding="utf-8") if original_exists else None

    yield

    if original_exists and original_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(original_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()


def test_load_validated_state_rejects_persisted_task_work_package_id_when_wp_is_missing(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [
    {
      "task_id": "TASK-001",
      "order": 1,
      "title": "Prepare FAT",
      "description": null,
      "owner": null,
      "status": "planned",
      "work_package_id": "WP-999",
      "dependencies": []
    }
  ],
  "work_packages": []
}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Persisted task work_package_id does not exist: TASK-001 -> WP-999",
    ):
        load_validated_state(state_file)


def test_task_list_rejects_persisted_dangling_task_work_package_link(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-999",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--show-work-package-id")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert (
        "Persisted task work_package_id does not exist: TASK-001 -> WP-999"
        in result.stdout
    )


def test_wp_list_rejects_persisted_dangling_task_work_package_link(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-999",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Tablet press qualification",
                        "status": "open",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--show-task-ids")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert (
        "Persisted task work_package_id does not exist: TASK-001 -> WP-999"
        in result.stdout
    )

    