import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "data" / "state"
STATE_FILE = STATE_DIR / "state.json"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def backup_state_file():
    if STATE_FILE.exists():
        return STATE_FILE.read_text(encoding="utf-8")
    return None


def restore_state_file(original_content):
    if original_content is None:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
    else:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(original_content, encoding="utf-8")


def test_state_init_creates_file_with_defaults():
    original = backup_state_file()
    try:
        if STATE_FILE.exists():
            STATE_FILE.unlink()

        result = run_cli("state", "init")

        assert result.returncode == 0
        assert STATE_FILE.exists()

        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        assert data["project"] == "AI_SYSTEM_BUILDER"
        assert data["version"] == "0.1.0"
        assert data["status"] == "not_started"
    finally:
        restore_state_file(original)


def test_state_show_reads_existing_state():
    original = backup_state_file()
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(
                {
                    "project": "AI_SYSTEM_BUILDER",
                    "version": "0.5.0",
                    "status": "not_started",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = run_cli("state", "show")

        assert result.returncode == 0
        output = result.stdout
        assert '"project": "AI_SYSTEM_BUILDER"' in output
        assert '"version": "0.5.0"' in output
        assert '"status": "not_started"' in output
    finally:
        restore_state_file(original)


def test_set_version_updates_only_version():
    original = backup_state_file()
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(
                {
                    "project": "AI_SYSTEM_BUILDER",
                    "version": "0.1.0",
                    "status": "not_started",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = run_cli("state", "set-version", "0.8.0")

        assert result.returncode == 0
        assert "State version updated to: 0.8.0" in result.stdout

        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        assert data["project"] == "AI_SYSTEM_BUILDER"
        assert data["version"] == "0.8.0"
        assert data["status"] == "not_started"
    finally:
        restore_state_file(original)


def test_set_status_updates_only_status():
    original = backup_state_file()
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(
                {
                    "project": "AI_SYSTEM_BUILDER",
                    "version": "0.8.0",
                    "status": "not_started",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = run_cli("state", "set-status", "completed")

        assert result.returncode == 0
        assert "State status updated to: completed" in result.stdout

        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        assert data["project"] == "AI_SYSTEM_BUILDER"
        assert data["version"] == "0.8.0"
        assert data["status"] == "completed"
    finally:
        restore_state_file(original)


def test_show_handles_missing_file():
    original = backup_state_file()
    try:
        if STATE_FILE.exists():
            STATE_FILE.unlink()

        result = run_cli("state", "show")

        assert result.returncode == 0
        assert "State file not found:" in result.stdout
    finally:
        restore_state_file(original)


def test_show_handles_invalid_json():
    original = backup_state_file()
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text("{ invalid json }", encoding="utf-8")

        result = run_cli("state", "show")

        assert result.returncode == 0
        assert "Invalid JSON in state file:" in result.stdout
    finally:
        restore_state_file(original)


def test_show_handles_validation_error():
    original = backup_state_file()
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(
                {
                    "project": "AI_SYSTEM_BUILDER",
                    "version": "0.8.0",
                    "status": "not_a_real_status",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = run_cli("state", "show")

        assert result.returncode == 0
        assert "State validation failed:" in result.stdout
    finally:
        restore_state_file(original)


def test_set_status_rejects_invalid_choice_at_parser_level():
    result = run_cli("state", "set-status", "wrong_value")

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "invalid choice" in combined_output

