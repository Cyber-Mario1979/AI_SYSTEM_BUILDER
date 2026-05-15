from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.api import ApiResult, ApiStatus
from asbp.external_surface import (
    FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS,
    SUPPORTED_UI_API_CONSISTENCY_RULES,
    OperatorVisibleState,
    UiApiConsistencyResult,
    evaluate_ui_api_consistency,
    get_ui_api_consistency_rule,
    list_ui_api_consistency_rules,
    normalize_operator_visible_state,
)
from asbp.ui import UiActionIntakeDecisionResult


def test_ui_api_consistency_rule_order_is_deterministic() -> None:
    assert list_ui_api_consistency_rules() == SUPPORTED_UI_API_CONSISTENCY_RULES

    assert tuple(rule.to_dict() for rule in SUPPORTED_UI_API_CONSISTENCY_RULES) == (
        {
            "api_status": "success",
            "api_result": "accepted",
            "allowed_ui_decision_results": (
                "accepted_for_display",
                "requires_api_service_validation",
            ),
            "allowed_operator_visible_states": (
                "accepted",
                "display_only",
                "validation_required",
            ),
            "forbidden_operator_visible_states": (
                "rejected",
                "error_visible",
                "blocked",
            ),
            "required_truth_boundary": "governed engine truth remains authoritative",
            "reason": "api_success_may_be_displayed_or_require_validation_without_mutation",
        },
        {
            "api_status": "error",
            "api_result": "rejected",
            "allowed_ui_decision_results": (
                "accepted_for_display",
                "rejected",
            ),
            "allowed_operator_visible_states": (
                "rejected",
                "error_visible",
                "blocked",
            ),
            "forbidden_operator_visible_states": (
                "accepted",
                "validation_required",
            ),
            "required_truth_boundary": "governed engine rejection remains visible",
            "reason": "api_error_must_remain_rejected_or_error_visible",
        },
    )


def test_get_ui_api_consistency_rule_returns_matching_rule() -> None:
    rule = get_ui_api_consistency_rule(api_status="success", api_result="accepted")

    assert rule.api_status is ApiStatus.SUCCESS
    assert rule.api_result is ApiResult.ACCEPTED


def test_get_ui_api_consistency_rule_rejects_unsupported_combination() -> None:
    with pytest.raises(ValueError, match="unsupported API status/result combination"):
        get_ui_api_consistency_rule(api_status="success", api_result="rejected")


def test_success_api_outcome_can_map_to_display_visible_accepted_state() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
    )

    assert decision.result is UiApiConsistencyResult.CONSISTENT
    assert decision.to_dict() == {
        "result": "consistent",
        "reason": "ui_api_consistent_with_governed_truth",
        "required_boundary": "governed engine truth remains authoritative",
    }


def test_success_api_outcome_can_require_validation_for_command_capable_ui() -> None:
    decision = evaluate_ui_api_consistency(
        api_status=ApiStatus.SUCCESS,
        api_result=ApiResult.ACCEPTED,
        ui_decision_result=UiActionIntakeDecisionResult.REQUIRES_API_SERVICE_VALIDATION,
        operator_visible_state=OperatorVisibleState.VALIDATION_REQUIRED,
    )

    assert decision.to_dict() == {
        "result": "consistent",
        "reason": "ui_api_consistent_with_governed_truth",
        "required_boundary": "governed engine truth remains authoritative",
    }


def test_error_api_outcome_must_remain_error_visible_or_rejected() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="error",
        api_result="rejected",
        ui_decision_result="accepted_for_display",
        operator_visible_state="error visible",
    )

    assert decision.to_dict() == {
        "result": "consistent",
        "reason": "ui_api_consistent_with_governed_truth",
        "required_boundary": "governed engine rejection remains visible",
    }


def test_rejected_api_outcome_cannot_be_displayed_as_accepted() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="error",
        api_result="rejected",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "operator_visible_state_diverges_from_api_response",
        "required_boundary": "governed engine rejection remains visible",
    }


def test_success_api_outcome_cannot_be_displayed_as_error() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="error_visible",
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "operator_visible_state_diverges_from_api_response",
        "required_boundary": "governed engine truth remains authoritative",
    }


def test_error_api_outcome_cannot_require_mutation_validation_as_success_like_state() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="error",
        api_result="rejected",
        ui_decision_result="requires_api_service_validation",
        operator_visible_state="validation_required",
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "ui_decision_diverges_from_api_response",
        "required_boundary": "governed engine rejection remains visible",
    }


def test_missing_governed_truth_reference_is_rejected() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
        governed_truth_reference=None,
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "missing_governed_truth_reference",
        "required_boundary": "operator-visible state must reference governed engine truth",
    }


def test_ui_api_consistency_rejects_inner_authority_claims() -> None:
    decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
        authority_claims=("source_truth",),
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "ui_api_consistency_cannot_claim_inner_authority",
        "required_boundary": "preserve governed engine source/validation/execution truth",
    }


def test_ui_api_consistency_rejects_hidden_domain_logic_or_service_bypass() -> None:
    hidden_logic_decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
        behaviors=("ui_api_hidden_domain_logic",),
    )

    bypass_decision = evaluate_ui_api_consistency(
        api_status="success",
        api_result="accepted",
        ui_decision_result="accepted_for_display",
        operator_visible_state="accepted",
        behaviors=("service boundary bypass",),
    )

    expected = {
        "result": "rejected",
        "reason": "ui_api_consistency_behavior_outside_m21_2_scope",
        "required_boundary": "service boundary and future roadmap-authorized checkpoint required",
    }

    assert hidden_logic_decision.to_dict() == expected
    assert bypass_decision.to_dict() == expected


def test_operator_visible_state_normalizer_accepts_supported_values_and_fails_closed() -> None:
    assert normalize_operator_visible_state("error visible") is OperatorVisibleState.ERROR_VISIBLE
    assert normalize_operator_visible_state("validation-required") is (
        OperatorVisibleState.VALIDATION_REQUIRED
    )

    with pytest.raises(ValueError, match="unsupported operator visible state"):
        normalize_operator_visible_state("silently_corrected")


def test_unsupported_api_status_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported API status"):
        evaluate_ui_api_consistency(
            api_status="partial",
            api_result="accepted",
            ui_decision_result="accepted_for_display",
            operator_visible_state="accepted",
        )


def test_ui_api_consistency_forbidden_behavior_list_is_explicit() -> None:
    assert "ui_api_hidden_domain_logic" in FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
    assert "service_boundary_bypass" in FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
    assert "governed_truth_override" in FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS
    assert "silent_status_translation" in FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS


def test_external_surface_consistency_module_does_not_import_forbidden_modules() -> None:
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