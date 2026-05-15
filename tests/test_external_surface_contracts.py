from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.api import ApiResult, ApiStatus
from asbp.external_surface import (
    FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    FORBIDDEN_EXTERNAL_BEHAVIORS,
    SUPPORTED_EXTERNAL_CONTRACT_FIELDS,
    ExternalContractCompatibilityResult,
    ExternalContractField,
    ExternalSurfaceChannel,
    ExternalSurfaceRole,
    build_external_contract_discipline,
    evaluate_external_contract_compatibility,
    get_supported_external_contract_fields,
    normalize_external_contract_field,
    normalize_external_surface_channel,
    normalize_external_surface_role,
)
from asbp.ui import UiActionIntakeDecisionResult, UiInteractionFlowName, UiInteractionMode


def test_supported_external_contract_field_order_is_deterministic() -> None:
    assert get_supported_external_contract_fields() == SUPPORTED_EXTERNAL_CONTRACT_FIELDS

    assert tuple(field.value for field in SUPPORTED_EXTERNAL_CONTRACT_FIELDS) == (
        "status",
        "result",
        "error",
        "payload",
        "metadata",
        "request_id",
        "operation",
        "action_name",
        "flow_name",
        "required_boundary",
        "template_id",
        "schema_id",
        "standards_bundle_ref",
        "citation_ref",
        "library_version",
    )


def test_external_contract_discipline_aligns_api_and_ui_vocabularies() -> None:
    discipline = build_external_contract_discipline(
        channel=ExternalSurfaceChannel.API,
        role=ExternalSurfaceRole.DOWNSTREAM_ADAPTER,
    )

    assert discipline.shared_status_values == tuple(status.value for status in ApiStatus)
    assert discipline.shared_result_values == tuple(result.value for result in ApiResult)
    assert discipline.shared_ui_decision_values == tuple(
        result.value for result in UiActionIntakeDecisionResult
    )
    assert discipline.shared_ui_flow_values == tuple(flow.value for flow in UiInteractionFlowName)
    assert discipline.shared_ui_mode_values == tuple(mode.value for mode in UiInteractionMode)

    assert "code" in discipline.shared_error_fields
    assert "message" in discipline.shared_error_fields
    assert "details" in discipline.shared_error_fields


def test_external_contract_discipline_preserves_future_reference_placeholders_only() -> None:
    discipline = build_external_contract_discipline(
        channel="ui",
        role="product_visibility_surface",
    )

    assert discipline.future_reference_placeholders == (
        "template_id",
        "schema_id",
        "standards_bundle_ref",
        "citation_ref",
        "library_version",
    )

    assert "document_generation" in discipline.forbidden_behaviors
    assert "standards_embedding" in discipline.forbidden_behaviors
    assert "model_provider_integration" in discipline.forbidden_behaviors


def test_external_contract_normalizers_accept_supported_values_and_fail_closed() -> None:
    assert normalize_external_surface_channel("API") is ExternalSurfaceChannel.API
    assert normalize_external_surface_role("operator intake surface") is (
        ExternalSurfaceRole.OPERATOR_INTAKE_SURFACE
    )
    assert normalize_external_contract_field("standards-bundle-ref") is (
        ExternalContractField.STANDARDS_BUNDLE_REF
    )

    with pytest.raises(ValueError, match="unsupported external surface channel"):
        normalize_external_surface_channel("mobile")

    with pytest.raises(ValueError, match="unsupported external surface role"):
        normalize_external_surface_role("autonomous_agent")

    with pytest.raises(ValueError, match="unsupported external contract field"):
        normalize_external_contract_field("tenant_runtime")


def test_external_contract_compatibility_accepts_shared_core_fields() -> None:
    decision = evaluate_external_contract_compatibility(
        channel="api",
        role="downstream_adapter",
        fields=("status", "result", "error", "payload", "metadata"),
    )

    assert decision.result is ExternalContractCompatibilityResult.COMPATIBLE
    assert decision.to_dict() == {
        "result": "compatible",
        "reason": "compatible_with_shared_external_contract_discipline",
        "required_boundary": None,
    }


def test_external_contract_compatibility_accepts_future_placeholders_without_closure() -> None:
    decision = evaluate_external_contract_compatibility(
        channel="ui",
        role="product_visibility_surface",
        fields=("template_id", "schema_id", "citation_ref"),
    )

    assert decision.to_dict() == {
        "result": "compatible",
        "reason": "compatible_with_deferred_future_reference_placeholders",
        "required_boundary": (
            "placeholder reference only; deferred dependency closure required "
            "before productized implementation"
        ),
    }


def test_external_contract_compatibility_rejects_forbidden_authority_claims() -> None:
    decision = evaluate_external_contract_compatibility(
        channel="api",
        role="downstream_adapter",
        fields=("status", "result"),
        authority_claims=("source_truth",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "external_surface_cannot_claim_inner_authority",
        "required_boundary": "preserve governed engine source/validation/execution truth",
    }


def test_external_contract_compatibility_rejects_out_of_scope_behaviors() -> None:
    decision = evaluate_external_contract_compatibility(
        channel="ui",
        role="operator_intake_surface",
        fields=("action_name", "payload"),
        behaviors=("document_generation",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "external_surface_behavior_outside_m21_1_scope",
        "required_boundary": "future roadmap-authorized checkpoint required",
    }


def test_external_contract_compatibility_rejects_string_for_fields() -> None:
    with pytest.raises(TypeError, match="fields must be an iterable"):
        evaluate_external_contract_compatibility(
            channel="api",
            role="downstream_adapter",
            fields="status",  # type: ignore[arg-type]
        )


def test_external_surface_forbidden_lists_are_explicit() -> None:
    assert "source_truth" in FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    assert "validation_truth" in FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS
    assert "execution_truth" in FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS

    assert "raw_state_access" in FORBIDDEN_EXTERNAL_BEHAVIORS
    assert "raw_persistence_access" in FORBIDDEN_EXTERNAL_BEHAVIORS
    assert "cloud_deployment" in FORBIDDEN_EXTERNAL_BEHAVIORS
    assert "saas_productization" in FORBIDDEN_EXTERNAL_BEHAVIORS


def test_external_surface_module_does_not_import_forbidden_runtime_or_framework_modules() -> None:
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