from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.api import (
    SUPPORTED_API_COMMANDS,
    ApiCommandIntakeDecision,
    ApiCommandName,
    build_api_command_intake_request,
    evaluate_api_command_intake,
    normalize_api_command_name,
)


def test_supported_api_commands_are_deterministic() -> None:
    assert SUPPORTED_API_COMMANDS == {"preview_command", "validate_contract"}
    assert [command.value for command in ApiCommandName] == [
        "preview_command",
        "validate_contract",
    ]


def test_api_command_name_normalization_is_deterministic() -> None:
    assert normalize_api_command_name(" Preview ") == "preview_command"
    assert normalize_api_command_name("command-preview") == "preview_command"
    assert normalize_api_command_name("validate") == "validate_contract"
    assert normalize_api_command_name("contract validation") == "validate_contract"


def test_api_command_intake_request_shape_is_deterministic() -> None:
    request = build_api_command_intake_request(
        command=" preview ",
        target=" service ",
        payload={"operation": "show_task"},
        metadata={"request_id": "REQ-1"},
    )

    assert request.to_dict() == {
        "command": "preview",
        "target": "service",
        "payload": {"operation": "show_task"},
        "metadata": {"request_id": "REQ-1"},
        "execute": False,
    }


def test_api_command_intake_request_rejects_invalid_shape() -> None:
    with pytest.raises(ValueError, match="API command must be a non-empty string"):
        build_api_command_intake_request(command=" ")

    with pytest.raises(ValueError, match="API command target must be a non-empty string"):
        build_api_command_intake_request(command="preview", target=" ")

    with pytest.raises(TypeError, match="payload and metadata values must be mappings"):
        build_api_command_intake_request(
            command="preview",
            payload=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_valid_preview_intake_returns_observable_accepted_response_without_execution() -> None:
    request = build_api_command_intake_request(
        command="preview",
        target="service",
        payload={"operation": "show_task", "task_id": "T001"},
        metadata={"request_id": "REQ-1"},
    )

    decision = evaluate_api_command_intake(request)

    assert isinstance(decision, ApiCommandIntakeDecision)
    assert decision.accepted is True
    assert decision.execution_allowed is False
    assert decision.reason == "api_command_intake_accepted_without_execution"
    assert decision.response.to_dict() == {
        "status": "success",
        "result": "accepted",
        "payload": {
            "command": "preview_command",
            "target": "service",
            "accepted": True,
            "execution_allowed": False,
            "mode": "intake_preview_only",
            "request_payload": {"operation": "show_task", "task_id": "T001"},
            "request_metadata": {"request_id": "REQ-1"},
        },
        "error": None,
        "metadata": {},
    }


def test_valid_contract_validation_intake_returns_observable_accepted_response_without_execution() -> None:
    request = build_api_command_intake_request(
        command="validate",
        target="runtime",
        payload={"operation": "contract_check"},
    )

    decision = evaluate_api_command_intake(request)
    body = decision.response.to_dict()

    assert decision.accepted is True
    assert decision.execution_allowed is False
    assert body["payload"] == {
        "command": "validate_contract",
        "target": "runtime",
        "accepted": True,
        "execution_allowed": False,
        "mode": "contract_validation_only",
        "request_payload": {"operation": "contract_check"},
        "request_metadata": {},
    }


def test_unsupported_command_name_fails_closed() -> None:
    request = build_api_command_intake_request(command="approve_release", target="service")
    decision = evaluate_api_command_intake(request)
    body = decision.response.to_dict()

    assert decision.accepted is False
    assert decision.execution_allowed is False
    assert decision.reason == "unsupported_api_command"
    assert body["status"] == "error"
    assert body["result"] == "rejected"
    assert body["error"] == {
        "code": "API_COMMAND_UNSUPPORTED",
        "message": "API command is not supported by the M19.6 intake boundary.",
        "details": {
            "command": "approve_release",
            "supported_commands": sorted(SUPPORTED_API_COMMANDS),
        },
    }


def test_direct_execution_request_fails_closed_through_safety_rules() -> None:
    request = build_api_command_intake_request(
        command="preview",
        target="service",
        execute=True,
    )

    decision = evaluate_api_command_intake(request)
    body = decision.response.to_dict()

    assert decision.accepted is False
    assert decision.execution_allowed is False
    assert decision.reason == "api_intake_action_fails_closed"
    assert body["error"]["code"] == "API_SAFETY_UNSAFE_ACTION"
    assert body["error"]["details"]["action"] == "command"


def test_raw_state_persistence_and_storage_targets_fail_closed() -> None:
    for target in ("raw_state", "raw_persistence", "direct_storage"):
        request = build_api_command_intake_request(command="preview", target=target)
        decision = evaluate_api_command_intake(request)
        body = decision.response.to_dict()

        assert decision.accepted is False
        assert decision.execution_allowed is False
        assert decision.reason == "forbidden_raw_state_or_persistence_target"
        assert body["status"] == "error"
        assert body["result"] == "rejected"
        assert body["error"]["code"] == "API_BOUNDARY_FORBIDDEN_TARGET"


def test_unknown_target_fails_closed() -> None:
    request = build_api_command_intake_request(command="preview", target="database")
    decision = evaluate_api_command_intake(request)
    body = decision.response.to_dict()

    assert decision.accepted is False
    assert decision.execution_allowed is False
    assert decision.reason == "unknown_unapproved_api_dependency_target"
    assert body["error"] == {
        "code": "API_BOUNDARY_UNKNOWN_TARGET",
        "message": "API adapter dependency target is not approved.",
        "details": {
            "target": "database",
            "allowed_targets": ["core", "runtime", "service"],
        },
    }


def test_response_payload_mutation_does_not_change_subsequent_intake_responses() -> None:
    request = build_api_command_intake_request(
        command="preview",
        target="service",
        payload={"operation": "show_task"},
    )

    first = evaluate_api_command_intake(request).response.to_dict()
    first["payload"]["request_payload"]["operation"] = "mutated"

    second = evaluate_api_command_intake(request).response.to_dict()

    assert second["payload"]["request_payload"] == {"operation": "show_task"}


def test_command_intake_module_does_not_import_raw_state_or_persistence_modules() -> None:
    path = Path("asbp/api/command_intake.py")
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


def test_command_intake_module_does_not_introduce_route_framework_ui_cloud_or_ai_behavior() -> None:
    import asbp.api.command_intake as command_intake

    names = set(dir(command_intake))

    assert "FastAPI" not in names
    assert "Flask" not in names
    assert "APIRouter" not in names
    assert "route" not in names
    assert "endpoint" not in names
    assert "ui" not in names
    assert "cloud" not in names
    assert "OpenAI" not in names
    assert "Anthropic" not in names
