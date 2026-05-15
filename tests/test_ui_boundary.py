from __future__ import annotations

import ast
from pathlib import Path

from asbp.ui import UI_BOUNDARY_CONTRACT, get_ui_boundary_contract


def test_ui_boundary_contract_identifies_ui_as_downstream_product_surface() -> None:
    contract = get_ui_boundary_contract()

    assert contract is UI_BOUNDARY_CONTRACT
    assert contract.layer_name == "ui"
    assert contract.role == "downstream_product_surface"
    assert "ui -> api/service boundaries" in contract.allowed_dependency_direction


def test_ui_boundary_contract_defines_display_without_execution_authority() -> None:
    contract = get_ui_boundary_contract()

    assert "governed_workflow_state_visibility" in contract.allowed_display_responsibilities
    assert "governed_document_export_reporting_visibility" in contract.allowed_display_responsibilities
    assert "operator_facing_error_and_status_visibility" in contract.allowed_display_responsibilities
    assert "no_direct_execution_authority" in contract.execution_authority
    assert "no_source_truth_authority" in contract.execution_authority
    assert "no_validation_truth_authority" in contract.execution_authority
    assert "no_raw_state_mutation_authority" in contract.execution_authority


def test_ui_boundary_contract_forbids_domain_logic_and_truth_ownership() -> None:
    contract = get_ui_boundary_contract()

    assert "domain_logic_ownership" in contract.forbidden_responsibilities
    assert "validation_truth_ownership" in contract.forbidden_responsibilities
    assert "source_truth_ownership" in contract.forbidden_responsibilities
    assert "execution_truth_ownership" in contract.forbidden_responsibilities
    assert "hidden_workflow_rules" in contract.forbidden_responsibilities


def test_ui_boundary_contract_forbids_raw_state_and_productization_expansion() -> None:
    contract = get_ui_boundary_contract()

    assert "raw_state_storage" in contract.forbidden_direct_access
    assert "raw_persistence_helpers" in contract.forbidden_direct_access
    assert "direct_state_mutation" in contract.forbidden_direct_access
    assert "cloud_or_deployment_behavior" in contract.forbidden_responsibilities
    assert "saas_productization_behavior" in contract.forbidden_responsibilities


def test_ui_boundary_module_does_not_import_forbidden_inner_or_framework_modules() -> None:
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
