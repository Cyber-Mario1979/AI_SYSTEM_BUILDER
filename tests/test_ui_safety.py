from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.ui import (
    ALLOWED_UI_SAFETY_CONTEXT_BOUNDARIES,
    SUPPORTED_UI_SAFETY_CHECKS,
    UiSafetyCheckName,
    UiSafetyDecisionResult,
    UiSafetyState,
    build_ui_safety_evaluation_request,
    evaluate_ui_safety,
    get_ui_safety_rule_contract,
    list_ui_safety_rule_contracts,
    normalize_ui_safety_check,
    normalize_ui_safety_context_boundary,
    normalize_ui_safety_state,
)


def test_ui_safety_rule_contracts_are_deterministic() -> None:
    contracts = list_ui_safety_rule_contracts()

    assert tuple(contract.check_name for contract in contracts) == SUPPORTED_UI_SAFETY_CHECKS
    assert contracts[0].separation_rule == "ui_must_not_become_source_truth"
    assert contracts[-1].failure_behavior == "reject_silent_mutation"


def test_ui_safety_safe_display_decision_shape_is_deterministic() -> None:
    request = build_ui_safety_evaluation_request(
        check_name="stale ui state",
        state="valid",
        context_boundary="api service boundary",
        metadata={"request_id": "REQ-1"},
    )

    decision = evaluate_ui_safety(request)

    assert request.to_dict() == {
        "check_name": "stale_ui_state",
        "state": "valid",
        "context_boundary": "api_service_boundary",
        "metadata": {"request_id": "REQ-1"},
        "claims_source_truth": False,
        "claims_validation_truth": False,
        "claims_execution_truth": False,
        "bypasses_api_service_boundary": False,
        "mutation_requested": False,
        "no_guess_required": True,
    }
    assert decision.to_dict() == {
        "check_name": "stale_ui_state",
        "result": "safe_for_display",
        "accepted_for_display": True,
        "execution_allowed": False,
        "mutation_allowed": False,
        "reason": "ui_state_safe_for_display_only",
        "required_boundary": None,
        "no_guess_enforced": True,
    }


def test_ui_safety_rejects_source_truth_claim() -> None:
    request = build_ui_safety_evaluation_request(
        check_name=UiSafetyCheckName.SOURCE_TRUTH_CLAIM,
        claims_source_truth=True,
    )

    decision = evaluate_ui_safety(request)

    assert decision.result is UiSafetyDecisionResult.REJECTED
    assert decision.accepted_for_display is False
    assert decision.execution_allowed is False
    assert decision.mutation_allowed is False
    assert decision.reason == "ui_cannot_become_source_truth"
    assert decision.required_boundary == "api/service source boundary"


def test_ui_safety_rejects_validation_truth_claim() -> None:
    request = build_ui_safety_evaluation_request(
        check_name=UiSafetyCheckName.VALIDATION_TRUTH_CLAIM,
        claims_validation_truth=True,
    )

    decision = evaluate_ui_safety(request)

    assert decision.result is UiSafetyDecisionResult.REJECTED
    assert decision.reason == "ui_cannot_become_validation_truth"
    assert decision.required_boundary == "api/service validation boundary"


def test_ui_safety_rejects_execution_truth_claim() -> None:
    request = build_ui_safety_evaluation_request(
        check_name=UiSafetyCheckName.EXECUTION_TRUTH_CLAIM,
        claims_execution_truth=True,
    )

    decision = evaluate_ui_safety(request)

    assert decision.result is UiSafetyDecisionResult.REJECTED
    assert decision.reason == "ui_cannot_become_execution_truth"
    assert decision.required_boundary == "api/service execution boundary"


def test_ui_safety_rejects_api_service_boundary_bypass() -> None:
    request = build_ui_safety_evaluation_request(
        check_name=UiSafetyCheckName.API_SERVICE_BOUNDARY_BYPASS,
        bypasses_api_service_boundary=True,
    )

    decision = evaluate_ui_safety(request)

    assert decision.result is UiSafetyDecisionResult.REJECTED
    assert decision.reason == "api_service_boundary_bypass_rejected"
    assert decision.required_boundary == "approved API/service boundary"


def test_ui_safety_rejects_silent_or_direct_mutation() -> None:
    request = build_ui_safety_evaluation_request(
        check_name=UiSafetyCheckName.SILENT_MUTATION_ATTEMPT,
        mutation_requested=True,
    )

    decision = evaluate_ui_safety(request)

    assert decision.result is UiSafetyDecisionResult.REJECTED
    assert decision.reason == "ui_safety_rejects_silent_or_direct_mutation"
    assert decision.required_boundary == "approved command boundary"


def test_ui_safety_requires_refresh_for_stale_invalid_or_unknown_ui_states() -> None:
    for state in (UiSafetyState.STALE, UiSafetyState.INVALID, UiSafetyState.UNKNOWN):
        request = build_ui_safety_evaluation_request(
            check_name=UiSafetyCheckName.STALE_UI_STATE,
            state=state,
        )

        decision = evaluate_ui_safety(request)

        assert decision.result is UiSafetyDecisionResult.REQUIRES_API_SERVICE_REFRESH
        assert decision.accepted_for_display is False
        assert decision.execution_allowed is False
        assert decision.mutation_allowed is False
        assert decision.reason == "ui_state_requires_api_service_refresh"
        assert decision.no_guess_enforced is True


def test_ui_safety_rule_contracts_preserve_no_guess_failure_behavior() -> None:
    stale_contract = get_ui_safety_rule_contract(UiSafetyCheckName.STALE_UI_STATE)
    invalid_contract = get_ui_safety_rule_contract(UiSafetyCheckName.INVALID_UI_STATE)

    assert stale_contract.no_guess_behavior == "present_stale_state_as_blocked_or_unknown"
    assert "guess_from_stale_display" in stale_contract.forbidden_behaviors
    assert invalid_contract.no_guess_behavior == "present_invalid_state_without_auto_correction"
    assert "silent_error_correction" in invalid_contract.forbidden_behaviors


def test_ui_safety_rejects_invalid_check_state_and_boundary_fail_closed() -> None:
    with pytest.raises(ValueError, match="unsupported UI safety check"):
        normalize_ui_safety_check("unknown_check")

    with pytest.raises(ValueError, match="unsupported UI safety state"):
        normalize_ui_safety_state("maybe")

    with pytest.raises(ValueError, match="forbidden UI safety context boundary"):
        normalize_ui_safety_context_boundary("ui source truth")

    with pytest.raises(ValueError, match="unsupported UI safety context boundary"):
        normalize_ui_safety_context_boundary("random boundary")


def test_ui_safety_context_boundary_vocab_is_explicit() -> None:
    assert ALLOWED_UI_SAFETY_CONTEXT_BOUNDARIES == (
        "api_service_boundary",
        "api_read_surface",
        "service_read_surface",
        "approved_ui_boundary",
    )


def test_ui_safety_rejects_non_mapping_metadata() -> None:
    with pytest.raises(TypeError, match="metadata values must be mappings"):
        build_ui_safety_evaluation_request(
            check_name=UiSafetyCheckName.STALE_UI_STATE,
            metadata=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_ui_safety_module_does_not_import_forbidden_modules() -> None:
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
