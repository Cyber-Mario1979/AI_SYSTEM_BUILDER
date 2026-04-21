"""Canonical versioning surface for the M11.3 versioning-discipline checkpoint."""

RUNTIME_VERSION = "0.1.0"
STATE_VERSION = RUNTIME_VERSION
RELEASE_STATE = "active_development"


def build_version_metadata() -> dict[str, str]:
    return {
        "runtime_version": RUNTIME_VERSION,
        "state_version": STATE_VERSION,
        "release_state": RELEASE_STATE,
    }
