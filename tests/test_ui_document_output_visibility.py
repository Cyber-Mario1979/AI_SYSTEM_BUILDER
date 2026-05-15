from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.ui import (
    ALLOWED_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES,
    SUPPORTED_UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACES,
    UiDocumentOutputKind,
    UiDocumentOutputStatus,
    UiDocumentOutputVisibilityPayload,
    UiDocumentOutputVisibilitySurfaceName,
    UiInteractionFlowName,
    UiInteractionMode,
    build_ui_document_output_visibility_payload,
    get_ui_document_output_visibility_surface_contract,
    list_ui_document_output_visibility_surface_contracts,
    normalize_ui_document_output_source_boundary,
    normalize_ui_document_output_visibility_surface,
)


def test_ui_document_output_visibility_surfaces_are_deterministic_and_display_only() -> None:
    contracts = list_ui_document_output_visibility_surface_contracts()

    assert tuple(contract.name for contract in contracts) == SUPPORTED_UI_DOCUMENT_OUTPUT_VISIBILITY_SURFACES
    assert all(contract.interaction_flow is UiInteractionFlowName.DOCUMENT_OUTPUT_VISIBILITY for contract in contracts)
    assert all(contract.mode is UiInteractionMode.DISPLAY_ONLY for contract in contracts)


def test_ui_document_output_visibility_payload_shape_is_deterministic() -> None:
    payload = build_ui_document_output_visibility_payload(
        surface_name="document output status",
        source_boundary="approved output boundary",
        output_kind="document",
        output_status="available",
        display_payload={"document_id": "DOC-001", "reference": "docs/out/DOC-001.md"},
        metadata={"request_id": "REQ-1"},
    )

    assert payload.to_dict() == {
        "surface_name": "document_output_status",
        "interaction_flow": "document_output_visibility",
        "mode": "display_only",
        "source_boundary": "approved_output_boundary",
        "output_kind": "document",
        "output_status": "available",
        "display_payload": {"document_id": "DOC-001", "reference": "docs/out/DOC-001.md"},
        "metadata": {"request_id": "REQ-1"},
        "generation_allowed": False,
        "renderer_allowed": False,
        "ui_owns_output": False,
    }


def test_ui_document_output_visibility_contract_preserves_generation_separation() -> None:
    contract = get_ui_document_output_visibility_surface_contract(
        UiDocumentOutputVisibilitySurfaceName.DOCUMENT_OUTPUT_STATUS
    )

    assert contract.output_kind is UiDocumentOutputKind.DOCUMENT
    assert "consume_existing_document_output_payload" in contract.source_boundary_expectations
    assert "do_not_generate_document_from_ui" in contract.source_boundary_expectations
    assert "display_only_no_document_generation" in contract.visibility_safety_rules
    assert "document_engine_remains_authoritative" in contract.visibility_safety_rules
    assert "document_generation_expansion" in contract.forbidden_behaviors
    assert "renderer_product_ready_output" in contract.forbidden_behaviors


def test_ui_output_target_visibility_contract_displays_generation_flags_without_generation() -> None:
    contract = get_ui_document_output_visibility_surface_contract("output target status")

    assert contract.output_kind is UiDocumentOutputKind.OUTPUT_TARGET
    assert "show_generation_allowed_flag_as_visibility_only" in contract.display_constraints
    assert "display_only_no_generation" in contract.visibility_safety_rules
    assert "output_target_generation_from_ui" in contract.forbidden_behaviors


def test_ui_document_output_visibility_rejects_invalid_surface_fail_closed() -> None:
    with pytest.raises(ValueError, match="unsupported UI document output visibility surface"):
        normalize_ui_document_output_visibility_surface("unknown output surface")


def test_ui_document_output_visibility_rejects_generation_source_boundaries() -> None:
    with pytest.raises(ValueError, match="forbidden UI document output source boundary"):
        normalize_ui_document_output_source_boundary("document generation engine")

    with pytest.raises(ValueError, match="forbidden UI document output source boundary"):
        normalize_ui_document_output_source_boundary("renderer engine")

    with pytest.raises(ValueError, match="unsupported UI document output source boundary"):
        normalize_ui_document_output_source_boundary("random boundary")


def test_ui_document_output_source_boundary_vocab_is_explicit() -> None:
    assert ALLOWED_UI_DOCUMENT_OUTPUT_SOURCE_BOUNDARIES == (
        "api_read_surface",
        "service_read_surface",
        "api_service_read_boundary",
        "approved_output_boundary",
        "output_target_metadata",
    )


def test_ui_document_output_visibility_rejects_non_mapping_payloads() -> None:
    with pytest.raises(TypeError, match="metadata and display_payload values must be mappings"):
        build_ui_document_output_visibility_payload(
            surface_name="document_output_status",
            source_boundary="approved_output_boundary",
            output_kind="document",
            display_payload=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_ui_document_output_visibility_payload_cannot_generate_render_or_own_output() -> None:
    with pytest.raises(ValueError, match="must not allow generation"):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.EXPORT,
            generation_allowed=True,
        )

    with pytest.raises(ValueError, match="must not allow renderer behavior"):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.EXPORT,
            renderer_allowed=True,
        )

    with pytest.raises(ValueError, match="must not make UI the output owner"):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.EXPORT_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.EXPORT,
            ui_owns_output=True,
        )


def test_ui_document_output_visibility_payload_must_remain_document_output_display_only() -> None:
    with pytest.raises(ValueError, match="document_output_visibility interaction flow"):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.REPORT,
            interaction_flow=UiInteractionFlowName.WORKFLOW_VISIBILITY,
        )

    with pytest.raises(ValueError, match="must remain display-only"):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.REPORT,
            mode=UiInteractionMode.COMMAND_CAPABLE,
        )


def test_ui_document_output_status_vocab_rejects_unsupported_values() -> None:
    with pytest.raises(ValueError):
        UiDocumentOutputVisibilityPayload(
            surface_name=UiDocumentOutputVisibilitySurfaceName.REPORTING_OUTPUT_STATUS,
            source_boundary="approved_output_boundary",
            output_kind=UiDocumentOutputKind.REPORT,
            output_status="maybe",  # type: ignore[arg-type]
        )


def test_ui_document_output_visibility_module_does_not_import_forbidden_modules() -> None:
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
