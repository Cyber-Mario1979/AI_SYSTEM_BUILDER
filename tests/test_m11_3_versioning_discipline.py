from types import SimpleNamespace

import asbp.cli as cli
from asbp.state import load_validated_state
from asbp.versioning import (
    RELEASE_STATE,
    RUNTIME_VERSION,
    STATE_VERSION,
    build_version_metadata,
)


def test_m11_3_cli_version_is_centralized() -> None:
    assert cli.VERSION == RUNTIME_VERSION


def test_m11_3_release_state_is_explicit() -> None:
    metadata = build_version_metadata()

    assert metadata["runtime_version"] == RUNTIME_VERSION
    assert metadata["state_version"] == STATE_VERSION
    assert metadata["release_state"] == RELEASE_STATE


def test_m11_3_state_init_uses_centralized_state_version(
    tmp_path,
    monkeypatch,
) -> None:
    state_file_path = tmp_path / "state.json"

    monkeypatch.setattr(cli, "get_state_file_path", lambda: state_file_path)

    cli.handle_state_init(SimpleNamespace())

    loaded_state = load_validated_state(state_file_path)

    assert loaded_state.version == STATE_VERSION
