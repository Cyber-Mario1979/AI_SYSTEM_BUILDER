from __future__ import annotations

import ast
from pathlib import Path

from asbp.api import API_BOUNDARY_CONTRACT, get_api_boundary_contract


def test_api_boundary_contract_identifies_api_as_downstream_adapter() -> None:
    contract = get_api_boundary_contract()

    assert contract is API_BOUNDARY_CONTRACT
    assert contract.layer_name == "api"
    assert contract.role == "downstream_adapter"
    assert "api -> approved service/runtime/core boundaries" in contract.allowed_dependency_direction


def test_api_boundary_contract_forbids_raw_state_and_persistence_access() -> None:
    contract = get_api_boundary_contract()

    assert "raw_state_storage" in contract.forbidden_direct_access
    assert "raw_persistence_helpers" in contract.forbidden_direct_access
    assert "direct_state_mutation" in contract.forbidden_direct_access


def test_api_boundary_contract_forbids_domain_logic_and_non_api_expansion() -> None:
    contract = get_api_boundary_contract()

    assert "domain_logic_ownership" in contract.forbidden_responsibilities
    assert "validation_truth_ownership" in contract.forbidden_responsibilities
    assert "direct_ai_provider_calls" in contract.forbidden_responsibilities
    assert "ui_behavior" in contract.forbidden_responsibilities
    assert "cloud_or_deployment_behavior" in contract.forbidden_responsibilities


def test_api_boundary_module_does_not_import_raw_state_or_persistence_modules() -> None:
    api_root = Path("asbp/api")
    forbidden_import_roots = {
        "asbp.state",
        "asbp.storage",
        "asbp.persistence",
    }

    for path in api_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names = {alias.name for alias in node.names}
                assert imported_names.isdisjoint(forbidden_import_roots)

            if isinstance(node, ast.ImportFrom) and node.module is not None:
                assert node.module not in forbidden_import_roots
