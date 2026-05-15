from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.ui import (
    ALLOWED_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES,
    SUPPORTED_UI_OPERATOR_INTAKE_ACTIONS,
    UiInteractionFlowName,
    UiInteractionMode,
    UiOperatorIntakeActionName,
    UiOperatorIntakeDecisionResult,
    UiOperatorIntakeRequest,
    build_ui_operator_intake_request,
    evaluate_ui_operator_intake,
    get_ui_operator_intake_action_contract,
    list_ui_operator_intake_action_contracts,
    normalize_ui_operator_intake_action,
    normalize_ui_operator_intake_target_boundary,
)


def test_ui_operator_intake_actions_are_deterministic_and_command_capable() -> None:
    contracts = list_ui_operator_intake_action_contracts()

    assert tuple(contract.action_name for contract in contracts) == SUPPORTED_UI_OPERATOR_INTAKE_ACTIONS
    assert all(contract.interaction_flow is UiInteractionFlowName.OPERATOR_COMMAND_INTAKE for contract in contracts)
    assert all(contract.mode is UiInteractionMode.COMMAND_CAPABLE for contract in contracts)


def test_ui_operator_intake_request_shape_is_deterministic() -> None:
    request = build_ui_operator_intake_request(
        action_name="prepare api service intake",
        target_boundary="api command intake",
        payload={"intent": "plan_review"},
        metadata={"request_id": "REQ-1"},
    )

    assert request.to_dict() == {
        "action_name": "prepare_api_service_intake",
        "interaction_flow": "operator_command_intake",
        "mode": "command_capable",
        "target_boundary": "api_command_intake",
        "payload": {"intent": "plan_review"},
        "metadata": {"request_id": "REQ-1"},
        "execute": False,
        "approval_release_requested": False,
    }


def test_ui_operator_preview_is_preview_only_without_execution() -> None:
    request = build_ui_operator_intake_request(
        action_name=UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION,
        target_boundary="api_command_intake",
        payload={"intent": "preview"},
    )

    decision = evaluate_ui_operator_intake(request)

    assert decision.to_dict() == {
        "action_name": "preview_operator_action",
        "target_boundary": "api_command_intake",
        "result": "accepted_for_preview",
        "accepted": True,
        "execution_allowed": False,
        "validation_required": False,
        "reason": "operator_intent_accepted_for_preview_without_mutation",
        "required_boundary": None,
    }


def test_ui_operator_validation_requires_api_service_validation_before_mutation() -> None:
    request = build_ui_operator_intake_request(
        action_name=UiOperatorIntakeActionName.VALIDATE_OPERATOR_ACTION,
        target_boundary="service_command_boundary",
        payload={"intent": "validate"},
    )

    decision = evaluate_ui_operator_intake(request)

    assert decision.result is UiOperatorIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION
    assert decision.accepted is True
    assert decision.execution_allowed is False
    assert decision.validation_required is True
    assert decision.required_boundary == "api/service validation before mutation"


def test_ui_operator_prepare_intake_requires_api_service_validation() -> None:
    request = build_ui_operator_intake_request(
        action_name=UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE,
        target_boundary="approved_command_boundary",
        payload={"intent": "submit"},
    )

    decision = evaluate_ui_operator_intake(request)

    assert decision.result is UiOperatorIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION
    assert decision.accepted is True
    assert decision.execution_allowed is False
    assert decision.validation_required is True
    assert decision.reason == "operator_intake_requires_api_service_validation_before_mutation"


def test_ui_operator_intake_rejects_direct_execution() -> None:
    request = build_ui_operator_intake_request(
        action_name=UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE,
        target_boundary="api_command_intake",
        payload={"intent": "execute"},
        execute=True,
    )

    decision = evaluate_ui_operator_intake(request)

    assert decision.result is UiOperatorIntakeDecisionResult.REJECTED
    assert decision.accepted is False
    assert decision.execution_allowed is False
    assert decision.validation_required is True
    assert decision.reason == "ui_operator_intake_never_executes_actions_directly"


def test_ui_operator_intake_rejects_approval_release_expansion() -> None:
    request = build_ui_operator_intake_request(
        action_name=UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE,
        target_boundary="api_command_intake",
        payload={"intent": "approve"},
        approval_release_requested=True,
    )

    decision = evaluate_ui_operator_intake(request)

    assert decision.result is UiOperatorIntakeDecisionResult.REJECTED
    assert decision.accepted is False
    assert decision.execution_allowed is False
    assert decision.reason == "approval_release_expansion_not_authorized_for_ui_intake"


def test_ui_operator_intake_contract_preserves_hidden_business_rule_prohibition() -> None:
    contract = get_ui_operator_intake_action_contract(
        UiOperatorIntakeActionName.PREPARE_API_SERVICE_INTAKE
    )

    assert "stable_api_service_command_boundary_required" in contract.target_boundary_expectations
    assert "api_service_validation_required_before_mutation" in contract.target_boundary_expectations
    assert "execution_not_allowed_from_ui" in contract.validation_rules
    assert "ui_originated_hidden_business_rules" in contract.forbidden_behaviors
    assert "autonomous_action_execution" in contract.forbidden_behaviors
    assert "approval_release_expansion" in contract.forbidden_behaviors


def test_ui_operator_intake_rejects_invalid_actions_fail_closed() -> None:
    with pytest.raises(ValueError, match="unsupported UI operator intake action"):
        normalize_ui_operator_intake_action("approve_release")


def test_ui_operator_intake_rejects_forbidden_target_boundaries() -> None:
    with pytest.raises(ValueError, match="forbidden UI operator intake target boundary"):
        normalize_ui_operator_intake_target_boundary("raw state storage")

    with pytest.raises(ValueError, match="forbidden UI operator intake target boundary"):
        normalize_ui_operator_intake_target_boundary("approval release authority")

    with pytest.raises(ValueError, match="unsupported UI operator intake target boundary"):
        normalize_ui_operator_intake_target_boundary("random boundary")


def test_ui_operator_intake_target_boundary_vocab_is_explicit() -> None:
    assert ALLOWED_UI_OPERATOR_INTAKE_TARGET_BOUNDARIES == (
        "api_command_intake",
        "service_command_boundary",
        "api_service_command_boundary",
        "approved_command_boundary",
    )


def test_ui_operator_intake_rejects_non_mapping_payloads() -> None:
    with pytest.raises(TypeError, match="metadata and payload values must be mappings"):
        build_ui_operator_intake_request(
            action_name="preview_operator_action",
            target_boundary="api_command_intake",
            payload=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_ui_operator_intake_request_must_use_operator_command_flow_and_command_mode() -> None:
    with pytest.raises(ValueError, match="operator_command_intake interaction flow"):
        UiOperatorIntakeRequest(
            action_name=UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION,
            target_boundary="api_command_intake",
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
        )

    with pytest.raises(ValueError, match="command-capable mode"):
        UiOperatorIntakeRequest(
            action_name=UiOperatorIntakeActionName.PREVIEW_OPERATOR_ACTION,
            target_boundary="api_command_intake",
            mode=UiInteractionMode.DISPLAY_ONLY,
        )


def test_ui_operator_intake_module_does_not_import_forbidden_modules() -> None:
    ui_root = Path("asbp/ui")
    forbidden_import_roots = {
        "asbp.state",
        "asbp.storage",
        "asbp.persistence",
        "asbp.output_target_logic",
        "asbp.ai_workflow.summarization_reporting",
        "fastapi",
        "flask",
        "django",
        "streamlit",
        "gradio",
    }

    for path in ui_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names = {alias.name for alias in node.names}
                assert imported_names.isdisjoint(forbidden_import_roots)

            if isinstance(node, ast.ImportFrom) and node.module is not None:
                assert node.module not in forbidden_import_roots
