from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.ui import (
    ALLOWED_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES,
    SUPPORTED_UI_WORKFLOW_VISIBILITY_SURFACES,
    UiInteractionFlowName,
    UiInteractionMode,
    UiWorkflowVisibilityPayload,
    UiWorkflowVisibilitySurfaceName,
    build_ui_workflow_visibility_payload,
    get_ui_workflow_visibility_surface_contract,
    list_ui_workflow_visibility_surface_contracts,
    normalize_ui_workflow_visibility_source_boundary,
    normalize_ui_workflow_visibility_surface,
)


def test_ui_workflow_visibility_surfaces_are_deterministic_and_display_only() -> None:
    contracts = list_ui_workflow_visibility_surface_contracts()

    assert tuple(contract.name for contract in contracts) == SUPPORTED_UI_WORKFLOW_VISIBILITY_SURFACES
    assert all(contract.interaction_flow is UiInteractionFlowName.WORKFLOW_VISIBILITY for contract in contracts)
    assert all(contract.mode is UiInteractionMode.DISPLAY_ONLY for contract in contracts)


def test_ui_workflow_visibility_payload_shape_is_deterministic() -> None:
    payload = build_ui_workflow_visibility_payload(
        surface_name="workflow overview",
        source_boundary="api read surface",
        display_payload={"work_package_id": "WP001", "status": "Open"},
        metadata={"request_id": "REQ-1"},
    )

    assert payload.to_dict() == {
        "surface_name": "workflow_overview",
        "interaction_flow": "workflow_visibility",
        "mode": "display_only",
        "source_boundary": "api_read_surface",
        "display_payload": {"work_package_id": "WP001", "status": "Open"},
        "metadata": {"request_id": "REQ-1"},
        "mutation_allowed": False,
        "ui_owns_state": False,
    }


def test_ui_workflow_visibility_contract_preserves_visibility_safety_rules() -> None:
    contract = get_ui_workflow_visibility_surface_contract(
        UiWorkflowVisibilitySurfaceName.WORKFLOW_OVERVIEW
    )

    assert "consume_api_or_service_read_payload" in contract.source_boundary_expectations
    assert "do_not_fetch_raw_state" in contract.source_boundary_expectations
    assert "display_only_no_mutation" in contract.visibility_safety_rules
    assert "preserve_api_service_payload_truth" in contract.visibility_safety_rules
    assert "hidden_mutation" in contract.forbidden_behaviors
    assert "ui_workflow_state_ownership" in contract.forbidden_behaviors


def test_ui_workflow_visibility_rejects_invalid_surface_fail_closed() -> None:
    with pytest.raises(ValueError, match="unsupported UI workflow visibility surface"):
        normalize_ui_workflow_visibility_surface("unknown surface")


def test_ui_workflow_visibility_rejects_raw_state_source_boundaries() -> None:
    with pytest.raises(ValueError, match="forbidden UI workflow visibility source boundary"):
        normalize_ui_workflow_visibility_source_boundary("raw state storage")

    with pytest.raises(ValueError, match="unsupported UI workflow visibility source boundary"):
        normalize_ui_workflow_visibility_source_boundary("random boundary")


def test_ui_workflow_visibility_source_boundary_vocab_is_explicit() -> None:
    assert ALLOWED_UI_WORKFLOW_VISIBILITY_SOURCE_BOUNDARIES == (
        "api_read_surface",
        "service_read_surface",
        "api_service_read_boundary",
        "approved_api_service_boundary",
    )


def test_ui_workflow_visibility_rejects_non_mapping_payloads() -> None:
    with pytest.raises(TypeError, match="metadata and display_payload values must be mappings"):
        build_ui_workflow_visibility_payload(
            surface_name="workflow_overview",
            source_boundary="api_read_surface",
            display_payload=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_ui_workflow_visibility_payload_cannot_mutate_or_own_state() -> None:
    with pytest.raises(ValueError, match="must not allow mutation"):
        UiWorkflowVisibilityPayload(
            surface_name=UiWorkflowVisibilitySurfaceName.TASK_STATUS,
            source_boundary="api_read_surface",
            mutation_allowed=True,
        )

    with pytest.raises(ValueError, match="must not make UI the state owner"):
        UiWorkflowVisibilityPayload(
            surface_name=UiWorkflowVisibilitySurfaceName.TASK_STATUS,
            source_boundary="api_read_surface",
            ui_owns_state=True,
        )


def test_ui_workflow_visibility_payload_must_remain_workflow_display_only() -> None:
    with pytest.raises(ValueError, match="workflow_visibility interaction flow"):
        UiWorkflowVisibilityPayload(
            surface_name=UiWorkflowVisibilitySurfaceName.TASK_STATUS,
            source_boundary="api_read_surface",
            interaction_flow=UiInteractionFlowName.ERROR_STATUS_PRESENTATION,
        )

    with pytest.raises(ValueError, match="must remain display-only"):
        UiWorkflowVisibilityPayload(
            surface_name=UiWorkflowVisibilitySurfaceName.TASK_STATUS,
            source_boundary="api_read_surface",
            mode=UiInteractionMode.COMMAND_CAPABLE,
        )


def test_ui_workflow_visibility_module_does_not_import_forbidden_modules() -> None:
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
