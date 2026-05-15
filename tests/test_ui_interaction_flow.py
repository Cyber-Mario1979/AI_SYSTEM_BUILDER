from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.ui import (
    SUPPORTED_UI_INTERACTION_FLOWS,
    UiActionIntakeDecisionResult,
    UiInteractionFlowName,
    UiInteractionMode,
    build_ui_action_intake_request,
    evaluate_ui_action_intake,
    get_ui_interaction_flow_contract,
    list_ui_interaction_flow_contracts,
    normalize_ui_interaction_flow,
    normalize_ui_interaction_mode,
)


def test_supported_ui_interaction_flow_order_is_deterministic() -> None:
    assert tuple(flow.value for flow in SUPPORTED_UI_INTERACTION_FLOWS) == (
        "workflow_visibility",
        "document_output_visibility",
        "operator_command_intake",
        "error_status_presentation",
    )

    assert tuple(contract.name for contract in list_ui_interaction_flow_contracts()) == (
        UiInteractionFlowName.WORKFLOW_VISIBILITY,
        UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY,
        UiInteractionFlowName.OPERATOR_COMMAND_INTAKE,
        UiInteractionFlowName.ERROR_STATUS_PRESENTATION,
    )


def test_ui_interaction_flow_contract_defines_display_only_visibility_flows() -> None:
    workflow_contract = get_ui_interaction_flow_contract("workflow visibility")
    document_contract = get_ui_interaction_flow_contract("document-output-visibility")

    assert workflow_contract.mode is UiInteractionMode.DISPLAY_ONLY
    assert document_contract.mode is UiInteractionMode.DISPLAY_ONLY
    assert "display_only_no_mutation" in workflow_contract.execution_boundary
    assert "display_only_no_generation" in document_contract.execution_boundary


def test_ui_interaction_flow_contract_defines_command_capable_intake_flow() -> None:
    contract = get_ui_interaction_flow_contract(UiInteractionFlowName.OPERATOR_COMMAND_INTAKE)

    assert contract.mode is UiInteractionMode.COMMAND_CAPABLE
    assert "collect_operator_intent" in contract.user_action_expectations
    assert "api_service_validation_required" in contract.execution_boundary
    assert "ui_never_executes_domain_action_directly" in contract.execution_boundary
    assert "api_service_validation_bypass" in contract.forbidden_behaviors


def test_ui_action_intake_request_shape_is_deterministic() -> None:
    request = build_ui_action_intake_request(
        flow_name="operator_command_intake",
        requested_mode="command capable",
        action_name=" commit_plan ",
        payload={"plan_id": "P001"},
        metadata={"request_id": "REQ-1"},
    )

    assert request.to_dict() == {
        "flow_name": "operator_command_intake",
        "requested_mode": "command_capable",
        "action_name": "commit_plan",
        "payload": {"plan_id": "P001"},
        "metadata": {"request_id": "REQ-1"},
    }


def test_ui_action_intake_request_rejects_empty_action_or_non_mapping_payload() -> None:
    with pytest.raises(ValueError, match="action_name must be a non-empty string"):
        build_ui_action_intake_request(
            flow_name="workflow_visibility",
            requested_mode="display_only",
            action_name=" ",
        )

    with pytest.raises(TypeError, match="metadata and payload values must be mappings"):
        build_ui_action_intake_request(
            flow_name="workflow_visibility",
            requested_mode="display_only",
            action_name="view",
            payload=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_ui_interaction_flow_and_mode_normalizers_fail_closed() -> None:
    assert normalize_ui_interaction_flow("workflow visibility") is UiInteractionFlowName.WORKFLOW_VISIBILITY
    assert normalize_ui_interaction_mode("display-only") is UiInteractionMode.DISPLAY_ONLY

    with pytest.raises(ValueError, match="unsupported UI interaction flow"):
        normalize_ui_interaction_flow("unknown_flow")

    with pytest.raises(ValueError, match="unsupported UI interaction mode"):
        normalize_ui_interaction_mode("autonomous_execution")


def test_display_only_flow_rejects_command_intake() -> None:
    request = build_ui_action_intake_request(
        flow_name="workflow_visibility",
        requested_mode="command_capable",
        action_name="commit_task",
    )

    decision = evaluate_ui_action_intake(request)

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "display_only_flow_cannot_accept_command_intake",
        "required_boundary": None,
    }


def test_command_capable_flow_requires_api_service_validation_before_mutation() -> None:
    request = build_ui_action_intake_request(
        flow_name="operator_command_intake",
        requested_mode="command_capable",
        action_name="commit_task",
    )

    decision = evaluate_ui_action_intake(request)

    assert decision.result is UiActionIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION
    assert decision.to_dict() == {
        "result": "requires_api_service_validation",
        "reason": "command_capable_flow_requires_api_service_validation",
        "required_boundary": "api/service validation before mutation",
    }


def test_display_request_is_accepted_without_mutation() -> None:
    request = build_ui_action_intake_request(
        flow_name="error_status_presentation",
        requested_mode="display_only",
        action_name="show_error",
    )

    decision = evaluate_ui_action_intake(request)

    assert decision.to_dict() == {
        "result": "accepted_for_display",
        "reason": "display_only_request_allowed_without_mutation",
        "required_boundary": None,
    }


def test_ui_interaction_flow_module_does_not_import_forbidden_inner_or_framework_modules() -> None:
    ui_root = Path("asbp/ui")
    forbidden_import_roots = {
        "asbp.state",
        "asbp.storage",
        "asbp.persistence",
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
