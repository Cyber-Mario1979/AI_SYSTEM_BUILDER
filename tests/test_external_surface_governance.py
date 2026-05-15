from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.external_surface import (
    FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS,
    SUPPORTED_PRODUCT_SURFACE_CAPABILITIES,
    SUPPORTED_PRODUCT_SURFACE_EXPOSURES,
    SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES,
    ExternalSurfaceRole,
    ProductSurfaceCapability,
    ProductSurfaceExposure,
    ProductSurfaceGovernanceResult,
    evaluate_product_surface_governance,
    get_product_surface_governance_rule,
    list_product_surface_governance_rules,
    normalize_product_surface_capability,
    normalize_product_surface_exposure,
)


def test_supported_product_surface_vocabularies_are_deterministic() -> None:
    assert tuple(value.value for value in SUPPORTED_PRODUCT_SURFACE_EXPOSURES) == (
        "internal_governed",
        "operator_facing",
        "public_consumer_facing",
    )

    assert tuple(value.value for value in SUPPORTED_PRODUCT_SURFACE_CAPABILITIES) == (
        "visibility",
        "command_intake",
        "error_status_presentation",
        "public_contract_reference",
    )


def test_product_surface_governance_rule_order_is_deterministic() -> None:
    assert list_product_surface_governance_rules() == SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES

    assert tuple(rule.role for rule in SUPPORTED_PRODUCT_SURFACE_GOVERNANCE_RULES) == (
        ExternalSurfaceRole.DOWNSTREAM_ADAPTER,
        ExternalSurfaceRole.PRODUCT_VISIBILITY_SURFACE,
        ExternalSurfaceRole.OPERATOR_INTAKE_SURFACE,
        ExternalSurfaceRole.ERROR_STATUS_SURFACE,
    )


def test_visibility_surface_allows_public_bounded_visibility() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="product_visibility_surface",
        exposure="public consumer facing",
        capabilities=("visibility", "public_contract_reference"),
    )

    assert decision.result is ProductSurfaceGovernanceResult.ALLOWED
    assert decision.to_dict() == {
        "result": "allowed",
        "reason": "product_surface_governance_allowed",
        "required_boundary": "visibility remains downstream from governed engine truth",
    }


def test_downstream_adapter_allows_public_contract_reference_only() -> None:
    decision = evaluate_product_surface_governance(
        channel="api",
        role="downstream_adapter",
        exposure="public_consumer_facing",
        capabilities=("public_contract_reference", "error_status_presentation"),
    )

    assert decision.to_dict() == {
        "result": "allowed",
        "reason": "product_surface_governance_allowed",
        "required_boundary": "inner service/runtime/domain boundaries remain authoritative",
    }


def test_downstream_adapter_rejects_command_intake() -> None:
    decision = evaluate_product_surface_governance(
        channel="api",
        role="downstream_adapter",
        exposure="internal_governed",
        capabilities=("command_intake",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "command_intake_requires_operator_intake_surface",
        "required_boundary": "operator intake must remain bounded and validated",
    }


def test_operator_intake_surface_allows_bounded_command_intake_with_validation() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="operator_intake_surface",
        exposure="operator_facing",
        capabilities=("command_intake", "visibility"),
        validation_boundary="api/service validation before mutation",
    )

    assert decision.to_dict() == {
        "result": "allowed",
        "reason": "product_surface_governance_allowed",
        "required_boundary": "command intake requires API/service validation before mutation",
    }


def test_operator_intake_requires_validation_boundary() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="operator_intake_surface",
        exposure="operator_facing",
        capabilities=("command_intake",),
        validation_boundary=None,
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "command_intake_requires_api_service_validation_boundary",
        "required_boundary": "api/service validation before mutation",
    }


def test_public_consumer_surface_cannot_accept_command_intake() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="operator_intake_surface",
        exposure="public_consumer_facing",
        capabilities=("command_intake",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "product_surface_exposure_not_allowed_for_role",
        "required_boundary": "command intake requires API/service validation before mutation",
    }


def test_product_surface_rejects_inner_authority_claims() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="product_visibility_surface",
        exposure="operator_facing",
        capabilities=("visibility",),
        authority_claims=("execution_truth",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "product_surface_cannot_claim_inner_authority",
        "required_boundary": "preserve governed engine source/validation/execution truth",
    }


def test_product_surface_rejects_productization_and_agentic_behaviors() -> None:
    productization_decision = evaluate_product_surface_governance(
        channel="ui",
        role="product_visibility_surface",
        exposure="operator_facing",
        capabilities=("visibility",),
        behaviors=("commercial productization",),
    )

    agentic_decision = evaluate_product_surface_governance(
        channel="ui",
        role="operator_intake_surface",
        exposure="operator_facing",
        capabilities=("command_intake",),
        behaviors=("uncontrolled_agentic_behavior",),
    )

    expected = {
        "result": "rejected",
        "reason": "product_surface_behavior_outside_phase_7_scope",
        "required_boundary": "future roadmap-authorized checkpoint required",
    }

    assert productization_decision.to_dict() == expected
    assert agentic_decision.to_dict() == expected


def test_product_surface_rejects_cloud_and_saas_behaviors() -> None:
    cloud_decision = evaluate_product_surface_governance(
        channel="api",
        role="downstream_adapter",
        exposure="public_consumer_facing",
        capabilities=("public_contract_reference",),
        behaviors=("cloud_deployment_implementation",),
    )

    saas_decision = evaluate_product_surface_governance(
        channel="ui",
        role="product_visibility_surface",
        exposure="public_consumer_facing",
        capabilities=("visibility",),
        behaviors=("tenant_saas_behavior",),
    )

    assert cloud_decision.to_dict()["result"] == "rejected"
    assert saas_decision.to_dict()["result"] == "rejected"


def test_missing_governed_truth_reference_is_rejected() -> None:
    decision = evaluate_product_surface_governance(
        channel="ui",
        role="product_visibility_surface",
        exposure="operator_facing",
        capabilities=("visibility",),
        governed_truth_reference=None,
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "missing_governed_truth_reference",
        "required_boundary": "product surfaces must remain downstream from governed engine truth",
    }


def test_product_surface_normalizers_accept_supported_values_and_fail_closed() -> None:
    assert normalize_product_surface_exposure("operator facing") is (
        ProductSurfaceExposure.OPERATOR_FACING
    )
    assert normalize_product_surface_capability("error-status-presentation") is (
        ProductSurfaceCapability.ERROR_STATUS_PRESENTATION
    )

    with pytest.raises(ValueError, match="unsupported product surface exposure"):
        normalize_product_surface_exposure("tenant_facing")

    with pytest.raises(ValueError, match="unsupported product surface capability"):
        normalize_product_surface_capability("autonomous_execution")


def test_capabilities_reject_string_input() -> None:
    with pytest.raises(TypeError, match="capabilities must be an iterable"):
        evaluate_product_surface_governance(
            channel="ui",
            role="product_visibility_surface",
            exposure="operator_facing",
            capabilities="visibility",  # type: ignore[arg-type]
        )


def test_unknown_governance_role_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported external surface role"):
        get_product_surface_governance_rule("autonomous_agent")


def test_product_surface_forbidden_behavior_list_is_explicit() -> None:
    assert "tenant_saas_behavior" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    assert "commercial_productization" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    assert "cloud_deployment_implementation" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    assert "uncontrolled_agentic_behavior" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    assert "production_endpoint_behavior" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS
    assert "production_ui_screen_behavior" in FORBIDDEN_PRODUCT_SURFACE_BEHAVIORS


def test_external_surface_governance_module_does_not_import_forbidden_modules() -> None:
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