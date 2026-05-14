from __future__ import annotations

import ast
from pathlib import Path

from asbp.api import (
    SUPPORTED_API_READ_SURFACES,
    ApiReadSurface,
    list_api_read_surfaces,
    normalize_api_read_surface,
    read_api_surface,
)


def test_supported_read_surfaces_are_deterministic() -> None:
    assert SUPPORTED_API_READ_SURFACES == {
        "api_boundary",
        "api_contracts",
        "service_boundary",
        "safety_policy",
    }

    assert [surface.value for surface in ApiReadSurface] == [
        "api_boundary",
        "api_contracts",
        "service_boundary",
        "safety_policy",
    ]


def test_list_api_read_surfaces_returns_deterministic_response() -> None:
    response = list_api_read_surfaces()

    assert response.to_dict() == {
        "status": "success",
        "result": "accepted",
        "payload": {
            "surfaces": sorted(SUPPORTED_API_READ_SURFACES),
            "read_only": True,
        },
        "error": None,
        "metadata": {},
    }


def test_read_surface_normalization_is_deterministic() -> None:
    assert normalize_api_read_surface(" Boundary ") == "api_boundary"
    assert normalize_api_read_surface("api-contracts") == "api_contracts"
    assert normalize_api_read_surface("service") == "service_boundary"
    assert normalize_api_read_surface("safety") == "safety_policy"


def test_api_boundary_read_surface_is_read_only_and_deterministic() -> None:
    response = read_api_surface("boundary")
    payload = response.to_dict()["payload"]

    assert payload["surface"] == "api_boundary"
    assert payload["read_only"] is True
    assert payload["data"] == {
        "layer_name": "api",
        "role": "downstream_adapter",
        "allowed_dependency_direction": [
            "api -> approved service/runtime/core boundaries",
        ],
        "forbidden_responsibilities": [
            "domain_logic_ownership",
            "validation_truth_ownership",
            "source_truth_ownership",
            "workflow_execution_authority",
            "direct_ai_provider_calls",
            "ui_behavior",
            "cloud_or_deployment_behavior",
        ],
        "forbidden_direct_access": [
            "raw_state_storage",
            "raw_persistence_helpers",
            "direct_state_mutation",
        ],
    }


def test_api_contracts_read_surface_is_read_only_and_deterministic() -> None:
    response = read_api_surface("contracts")

    assert response.to_dict()["payload"] == {
        "surface": "api_contracts",
        "read_only": True,
        "data": {
            "request_fields": ["operation", "payload", "metadata"],
            "response_fields": ["status", "result", "payload", "error", "metadata"],
            "error_fields": ["code", "message", "details"],
            "status_values": ["error", "success"],
            "result_values": ["accepted", "rejected"],
        },
    }


def test_service_boundary_read_surface_is_read_only_and_deterministic() -> None:
    response = read_api_surface("service")

    assert response.to_dict()["payload"] == {
        "surface": "service_boundary",
        "read_only": True,
        "data": {
            "allowed_dependency_targets": ["core", "runtime", "service"],
            "forbidden_dependency_targets": [
                "direct_storage",
                "raw_persistence",
                "raw_state",
            ],
        },
    }


def test_safety_policy_read_surface_is_read_only_and_deterministic() -> None:
    response = read_api_surface("safety")

    assert response.to_dict()["payload"] == {
        "surface": "safety_policy",
        "read_only": True,
        "data": {
            "safe_intake_actions": ["contract_validation", "read_only"],
            "unsafe_intake_actions": ["command", "state_changing"],
            "fail_closed": True,
        },
    }


def test_unknown_read_surface_fails_closed() -> None:
    response = read_api_surface("tasks")
    body = response.to_dict()

    assert body["status"] == "error"
    assert body["result"] == "rejected"
    assert body["payload"] == {}
    assert body["error"] == {
        "code": "API_READ_SURFACE_UNKNOWN",
        "message": "API read surface is not recognized and must fail closed.",
        "details": {
            "surface": "tasks",
            "supported_surfaces": sorted(SUPPORTED_API_READ_SURFACES),
        },
    }


def test_invalid_read_surface_fails_closed() -> None:
    response = read_api_surface(" ")
    body = response.to_dict()

    assert body["status"] == "error"
    assert body["result"] == "rejected"
    assert body["error"] == {
        "code": "API_READ_SURFACE_INVALID",
        "message": "API read surface must be a non-empty string",
        "details": {"surface": " "},
    }


def test_read_surface_payload_mutation_does_not_change_subsequent_reads() -> None:
    first = list_api_read_surfaces().to_dict()
    first["payload"]["surfaces"].append("mutated")

    second = list_api_read_surfaces().to_dict()

    assert "mutated" not in second["payload"]["surfaces"]


def test_read_surface_module_does_not_import_raw_state_or_persistence_modules() -> None:
    path = Path("asbp/api/read_surface.py")
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


def test_read_surface_module_does_not_introduce_route_framework_ui_cloud_or_command_behavior() -> None:
    import asbp.api.read_surface as read_surface

    names = set(dir(read_surface))

    assert "FastAPI" not in names
    assert "Flask" not in names
    assert "APIRouter" not in names
    assert "route" not in names
    assert "endpoint" not in names
    assert "command" not in names
    assert "ui" not in names
    assert "cloud" not in names
