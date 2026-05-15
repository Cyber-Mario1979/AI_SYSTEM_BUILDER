from __future__ import annotations

import ast
from pathlib import Path

from asbp.external_surface import (
    EXTERNAL_SURFACE_BOUNDARY_CONTRACT,
    FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS,
    FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS,
    ExternalSurfaceBoundaryContract,
    get_external_surface_boundary_contract,
)
from asbp.external_surface.contracts import FORBIDDEN_EXTERNAL_BEHAVIORS


def test_external_surface_boundary_contract_is_deterministic() -> None:
    contract = get_external_surface_boundary_contract()

    assert contract is EXTERNAL_SURFACE_BOUNDARY_CONTRACT
    assert isinstance(contract, ExternalSurfaceBoundaryContract)
    assert contract.to_dict()["package_boundary"] == "asbp.external_surface"
    assert contract.to_dict()["discipline_modules"] == (
        "asbp.external_surface.contracts",
        "asbp.external_surface.consistency",
        "asbp.external_surface.governance",
    )


def test_external_surface_boundary_preserves_inner_authority_boundaries() -> None:
    contract = get_external_surface_boundary_contract()

    assert contract.preserved_authority_boundaries == (
        "governed_engine_truth",
        "service_runtime_domain_boundaries",
        "api_service_validation_before_mutation",
        "ui_and_api_remain_downstream_adapters",
        "external_surface_is_not_source_truth",
        "external_surface_is_not_validation_truth",
        "external_surface_is_not_execution_truth",
    )


def test_external_surface_boundary_keeps_forbidden_authority_claims_visible() -> None:
    contract = get_external_surface_boundary_contract()

    assert contract.forbidden_authority_claims == FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    assert "source_truth" in contract.forbidden_authority_claims
    assert "validation_truth" in contract.forbidden_authority_claims
    assert "execution_truth" in contract.forbidden_authority_claims


def test_external_surface_boundary_consolidates_forbidden_behaviors() -> None:
    contract = get_external_surface_boundary_contract()

    for behavior in FORBIDDEN_EXTERNAL_BEHAVIORS:
        assert behavior in contract.forbidden_behaviors

    for behavior in FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS:
        assert behavior in contract.forbidden_behaviors

    for behavior in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS:
        assert behavior in contract.forbidden_behaviors

    assert "document_generation" in contract.forbidden_behaviors
    assert "standards_embedding" in contract.forbidden_behaviors
    assert "model_provider_integration" in contract.forbidden_behaviors
    assert "cloud_deployment_implementation" in contract.forbidden_behaviors
    assert "commercial_productization" in contract.forbidden_behaviors


def test_external_surface_boundary_aligns_validation_and_failure_behaviors() -> None:
    contract = get_external_surface_boundary_contract()

    assert contract.validation_and_failure_alignment == (
        "fail_closed_for_unsupported_terms",
        "preserve_api_error_rejection_visibility",
        "preserve_ui_api_consistency_with_governed_truth",
        "preserve_command_intake_validation_boundary",
        "preserve_product_surface_governance_boundary",
    )


def test_external_surface_boundary_records_explicit_non_goals() -> None:
    contract = get_external_surface_boundary_contract()

    assert "api_routes" in contract.explicit_non_goals
    assert "ui_screens" in contract.explicit_non_goals
    assert "command_execution" in contract.explicit_non_goals
    assert "cloud_deployment" in contract.explicit_non_goals
    assert "tenant_saas_behavior" in contract.explicit_non_goals
    assert "commercial_productization" in contract.explicit_non_goals


def test_external_surface_boundary_module_does_not_import_forbidden_modules() -> None:
    external_surface_root = Path("asbp/external_surface")
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

    for path in external_surface_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names = {alias.name for alias in node.names}
                assert imported_names.isdisjoint(forbidden_import_roots)

            if isinstance(node, ast.ImportFrom) and node.module is not None:
                assert node.module not in forbidden_import_roots
