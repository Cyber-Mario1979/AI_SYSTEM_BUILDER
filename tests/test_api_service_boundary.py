from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.api import (
    ALLOWED_API_DEPENDENCY_TARGETS,
    FORBIDDEN_API_DEPENDENCY_TARGETS,
    ApiDependencyDecision,
    evaluate_api_dependency_target,
    is_api_dependency_target_allowed,
    normalize_dependency_target,
)


def test_approved_service_runtime_core_targets_are_accepted() -> None:
    for target in ("service", "runtime", "core"):
        decision = evaluate_api_dependency_target(target)

        assert isinstance(decision, ApiDependencyDecision)
        assert decision.allowed is True
        assert decision.reason == "approved_api_boundary_target"
        assert decision.response.to_dict() == {
            "status": "success",
            "result": "accepted",
            "payload": {
                "target": target,
                "allowed": True,
                "reason": "approved_api_boundary_target",
            },
            "error": None,
            "metadata": {},
        }


def test_dependency_target_normalization_is_deterministic() -> None:
    assert normalize_dependency_target(" Service ") == "service"
    assert normalize_dependency_target("raw-state") == "raw_state"
    assert normalize_dependency_target("Direct Storage") == "direct_storage"


def test_empty_dependency_target_is_rejected() -> None:
    with pytest.raises(ValueError, match="dependency target must be a non-empty string"):
        normalize_dependency_target(" ")


def test_raw_state_persistence_and_storage_targets_are_rejected() -> None:
    for target in ("raw_state", "raw_persistence", "direct_storage"):
        decision = evaluate_api_dependency_target(target)
        response = decision.response.to_dict()

        assert decision.allowed is False
        assert decision.reason == "forbidden_raw_state_or_persistence_target"
        assert response["status"] == "error"
        assert response["result"] == "rejected"
        assert response["payload"] == {}
        assert response["error"] == {
            "code": "API_BOUNDARY_FORBIDDEN_TARGET",
            "message": (
                "API adapters must not depend on raw state, raw persistence, "
                "or direct storage targets."
            ),
            "details": {
                "target": target,
                "allowed_targets": sorted(ALLOWED_API_DEPENDENCY_TARGETS),
            },
        }


def test_unknown_dependency_target_is_rejected_without_guessing() -> None:
    decision = evaluate_api_dependency_target("database")
    response = decision.response.to_dict()

    assert decision.allowed is False
    assert decision.reason == "unknown_unapproved_api_dependency_target"
    assert response["error"] == {
        "code": "API_BOUNDARY_UNKNOWN_TARGET",
        "message": "API adapter dependency target is not approved.",
        "details": {
            "target": "database",
            "allowed_targets": sorted(ALLOWED_API_DEPENDENCY_TARGETS),
        },
    }


def test_boolean_helper_uses_same_deterministic_decision_rules() -> None:
    assert is_api_dependency_target_allowed("service") is True
    assert is_api_dependency_target_allowed("raw_state") is False
    assert is_api_dependency_target_allowed("database") is False


def test_allowed_and_forbidden_target_sets_do_not_overlap() -> None:
    assert ALLOWED_API_DEPENDENCY_TARGETS.isdisjoint(FORBIDDEN_API_DEPENDENCY_TARGETS)


def test_service_boundary_module_does_not_import_raw_state_or_persistence_modules() -> None:
    path = Path("asbp/api/service_boundary.py")
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


def test_service_boundary_module_does_not_introduce_route_or_framework_behavior() -> None:
    import asbp.api.service_boundary as service_boundary

    names = set(dir(service_boundary))

    assert "FastAPI" not in names
    assert "Flask" not in names
    assert "APIRouter" not in names
    assert "route" not in names
    assert "endpoint" not in names
