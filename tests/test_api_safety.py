from __future__ import annotations

import ast
from pathlib import Path

from asbp.api import (
    SAFE_API_INTAKE_ACTIONS,
    UNSAFE_API_INTAKE_ACTIONS,
    ApiSafetyDecision,
    evaluate_api_intake_safety,
    is_api_intake_action_allowed,
    normalize_api_intake_action,
)


def test_safe_read_only_intake_action_is_allowed() -> None:
    decision = evaluate_api_intake_safety(" read ")

    assert isinstance(decision, ApiSafetyDecision)
    assert decision.allowed is True
    assert decision.normalized_action == "read_only"
    assert decision.reason == "api_intake_action_allowed"
    assert decision.response.to_dict() == {
        "status": "success",
        "result": "accepted",
        "payload": {
            "action": "read_only",
            "allowed": True,
            "reason": "api_intake_action_allowed",
        },
        "error": None,
        "metadata": {},
    }


def test_safe_contract_validation_intake_action_is_allowed() -> None:
    decision = evaluate_api_intake_safety("contract-check")

    assert decision.allowed is True
    assert decision.normalized_action == "contract_validation"


def test_api_intake_action_normalization_is_deterministic() -> None:
    assert normalize_api_intake_action("Read Only") == "read_only"
    assert normalize_api_intake_action("contract-check") == "contract_validation"
    assert normalize_api_intake_action("Update") == "state_changing"


def test_invalid_api_intake_action_fails_closed() -> None:
    decision = evaluate_api_intake_safety(" ")
    response = decision.response.to_dict()

    assert decision.allowed is False
    assert decision.reason == "invalid_api_intake_action"
    assert response["status"] == "error"
    assert response["result"] == "rejected"
    assert response["error"] == {
        "code": "API_SAFETY_INVALID_ACTION",
        "message": "API intake action must be a non-empty string",
        "details": {"action": " "},
    }


def test_state_changing_intake_actions_fail_closed() -> None:
    for action in ("create", "update", "delete", "write", "mutation", "state_changing"):
        decision = evaluate_api_intake_safety(action)
        response = decision.response.to_dict()

        assert decision.allowed is False
        assert decision.normalized_action == "state_changing"
        assert decision.reason == "api_intake_action_fails_closed"
        assert response["error"] == {
            "code": "API_SAFETY_UNSAFE_ACTION",
            "message": (
                "API intake action is unsafe for the current checkpoint "
                "and must fail closed."
            ),
            "details": {
                "action": "state_changing",
                "safe_actions": sorted(SAFE_API_INTAKE_ACTIONS),
            },
        }


def test_command_like_intake_actions_fail_closed() -> None:
    for action in ("command", "execute"):
        decision = evaluate_api_intake_safety(action)
        response = decision.response.to_dict()

        assert decision.allowed is False
        assert decision.normalized_action == "command"
        assert decision.reason == "api_intake_action_fails_closed"
        assert response["error"]["code"] == "API_SAFETY_UNSAFE_ACTION"


def test_unknown_api_intake_action_fails_closed_without_guessing() -> None:
    decision = evaluate_api_intake_safety("approve_release")
    response = decision.response.to_dict()

    assert decision.allowed is False
    assert decision.reason == "unknown_api_intake_action_fails_closed"
    assert response["error"] == {
        "code": "API_SAFETY_UNKNOWN_ACTION",
        "message": "API intake action is not recognized and must fail closed.",
        "details": {
            "action": "approve_release",
            "safe_actions": sorted(SAFE_API_INTAKE_ACTIONS),
        },
    }


def test_boolean_helper_uses_same_fail_closed_rules() -> None:
    assert is_api_intake_action_allowed("read") is True
    assert is_api_intake_action_allowed("contract_validation") is True
    assert is_api_intake_action_allowed("update") is False
    assert is_api_intake_action_allowed("approve_release") is False


def test_safe_and_unsafe_action_sets_do_not_overlap() -> None:
    assert SAFE_API_INTAKE_ACTIONS.isdisjoint(UNSAFE_API_INTAKE_ACTIONS)


def test_safety_module_does_not_import_raw_state_or_persistence_modules() -> None:
    path = Path("asbp/api/safety.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))

    forbidden_import_roots = {
        "asbp.state",
        "asbp.storage",
        "asbp.persistence",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names = {alias.name for alias in node.names}
            assert imported_names.isdisjoint(forbidden_import_roots)

        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module not in forbidden_import_roots


def test_safety_module_does_not_introduce_route_framework_ui_or_cloud_behavior() -> None:
    import asbp.api.safety as safety

    names = set(dir(safety))

    assert "FastAPI" not in names
    assert "Flask" not in names
    assert "APIRouter" not in names
    assert "route" not in names
    assert "endpoint" not in names
    assert "ui" not in names
    assert "cloud" not in names
