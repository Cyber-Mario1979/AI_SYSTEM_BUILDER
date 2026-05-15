from __future__ import annotations

import ast
from pathlib import Path

import pytest

from asbp.external_surface import (
    EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE,
    EXPECTED_UAT_EVIDENCE_CATEGORIES,
    EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
    FORBIDDEN_ACCEPTANCE_ASSUMPTIONS,
    AcceptanceDecision,
    ExternalSurfaceAcceptanceEvidenceCategory,
    ExternalSurfaceAcceptanceReadinessResult,
    build_external_surface_acceptance_discipline,
    evaluate_external_surface_acceptance_readiness,
    get_expected_phase_7_closeout_evidence,
    get_expected_uat_evidence_categories,
    get_expected_validation_evidence_categories,
    normalize_acceptance_decision,
    normalize_acceptance_evidence_category,
)


def test_acceptance_evidence_category_order_is_deterministic() -> None:
    assert get_expected_validation_evidence_categories() == EXPECTED_VALIDATION_EVIDENCE_CATEGORIES
    assert get_expected_uat_evidence_categories() == EXPECTED_UAT_EVIDENCE_CATEGORIES
    assert get_expected_phase_7_closeout_evidence() == EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE

    assert tuple(value.value for value in EXPECTED_VALIDATION_EVIDENCE_CATEGORIES) == (
        "m21_1_shared_external_contract_discipline",
        "m21_2_ui_api_consistency_rules",
        "m21_3_product_surface_governance_foundation",
        "m21_4_external_surface_boundary_consolidation",
        "phase_7_full_validation_result",
    )

    assert tuple(value.value for value in EXPECTED_UAT_EVIDENCE_CATEGORIES) == (
        "phase_7_uat_protocol",
        "phase_7_uat_report",
    )


def test_acceptance_discipline_shape_is_deterministic() -> None:
    discipline = build_external_surface_acceptance_discipline()

    assert discipline.to_dict() == {
        "validation_evidence_categories": (
            "m21_1_shared_external_contract_discipline",
            "m21_2_ui_api_consistency_rules",
            "m21_3_product_surface_governance_foundation",
            "m21_4_external_surface_boundary_consolidation",
            "phase_7_full_validation_result",
        ),
        "uat_evidence_categories": (
            "phase_7_uat_protocol",
            "phase_7_uat_report",
        ),
        "phase_7_closeout_evidence": (
            "m21_1_shared_external_contract_discipline",
            "m21_2_ui_api_consistency_rules",
            "m21_3_product_surface_governance_foundation",
            "m21_4_external_surface_boundary_consolidation",
            "phase_7_full_validation_result",
            "phase_7_uat_protocol",
            "phase_7_uat_report",
            "phase_7_closeout_notes",
            "deferred_dependency_disposition",
        ),
        "allowed_acceptance_decisions": (
            "pass",
            "conditional_pass",
            "fail",
            "not_ready",
        ),
        "forbidden_assumptions": FORBIDDEN_ACCEPTANCE_ASSUMPTIONS,
        "explicit_non_goals": (
            "phase_8_execution",
            "cloud_deployment",
            "tenant_saas_behavior",
            "commercial_productization",
            "model_provider_integration",
            "product_ready_document_generation",
            "standards_embedding_or_citation_authority",
        ),
    }


def test_acceptance_readiness_is_ready_when_all_evidence_exists() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        provided_closeout_evidence=(
            ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_CLOSEOUT_NOTES,
            ExternalSurfaceAcceptanceEvidenceCategory.DEFERRED_DEPENDENCY_DISPOSITION,
        ),
        acceptance_decision="pass",
    )

    assert decision.result is ExternalSurfaceAcceptanceReadinessResult.READY
    assert decision.to_dict() == {
        "result": "ready",
        "reason": "external_surface_acceptance_evidence_ready_for_closeout_review",
        "missing_evidence": (),
        "required_boundary": "Phase 7 closeout review may proceed without implying Phase 8 or productization readiness",
    }


def test_missing_validation_evidence_fails_closed() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=(
            "m21_1_shared_external_contract_discipline",
            "m21_2_ui_api_consistency_rules",
        ),
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        acceptance_decision="pass",
    )

    assert decision.to_dict() == {
        "result": "not_ready",
        "reason": "missing_required_validation_evidence",
        "missing_evidence": (
            "m21_3_product_surface_governance_foundation",
            "m21_4_external_surface_boundary_consolidation",
            "phase_7_full_validation_result",
        ),
        "required_boundary": "M21.6 validation evidence required before Phase 7 closeout",
    }


def test_missing_uat_evidence_fails_closed() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=("phase_7_uat_protocol",),
        acceptance_decision="pass",
    )

    assert decision.to_dict() == {
        "result": "not_ready",
        "reason": "missing_required_uat_evidence",
        "missing_evidence": ("phase_7_uat_report",),
        "required_boundary": "M21.7 UAT evidence required before Phase 7 closeout",
    }


def test_missing_closeout_evidence_fails_closed_after_pass_decision() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        acceptance_decision="conditional pass",
    )

    assert decision.to_dict() == {
        "result": "not_ready",
        "reason": "missing_required_phase_7_closeout_evidence",
        "missing_evidence": (
            "phase_7_closeout_notes",
            "deferred_dependency_disposition",
        ),
        "required_boundary": "M21.8 closeout evidence and deferred dependency disposition required before Phase 7 closeout",
    }


def test_failed_acceptance_decision_is_rejected() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        acceptance_decision="fail",
    )

    assert decision.to_dict() == {
        "result": "rejected",
        "reason": "acceptance_decision_failed",
        "missing_evidence": (),
        "required_boundary": "external surfaces must pass or be conditionally accepted before closeout",
    }


def test_not_ready_acceptance_decision_remains_not_ready() -> None:
    decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
    )

    assert decision.to_dict() == {
        "result": "not_ready",
        "reason": "acceptance_decision_not_ready",
        "missing_evidence": (),
        "required_boundary": "acceptance decision must be pass or conditional_pass before closeout",
    }


def test_acceptance_discipline_rejects_phase_8_or_productization_assumptions() -> None:
    phase_8_decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        acceptance_decision="pass",
        assumptions=("phase_8_readiness",),
    )

    productization_decision = evaluate_external_surface_acceptance_readiness(
        provided_validation_evidence=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        acceptance_decision="pass",
        assumptions=("saas productization readiness",),
    )

    expected = {
        "result": "rejected",
        "reason": "acceptance_discipline_cannot_assume_productization_readiness",
        "missing_evidence": (),
        "required_boundary": "Phase 7 acceptance does not authorize Phase 8, cloud, deployment, SaaS, or productization readiness",
    }

    assert phase_8_decision.to_dict() == expected
    assert productization_decision.to_dict() == expected


def test_acceptance_normalizers_accept_supported_values_and_fail_closed() -> None:
    assert normalize_acceptance_evidence_category("phase 7 uat report") is (
        ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_UAT_REPORT
    )
    assert normalize_acceptance_decision("conditional-pass") is AcceptanceDecision.CONDITIONAL_PASS

    with pytest.raises(ValueError, match="unsupported acceptance evidence category"):
        normalize_acceptance_evidence_category("cloud_deployment_readiness")

    with pytest.raises(ValueError, match="unsupported acceptance decision"):
        normalize_acceptance_decision("approved_for_productization")


def test_acceptance_evidence_iterables_reject_string_input() -> None:
    with pytest.raises(TypeError, match="provided_validation_evidence must be an iterable"):
        evaluate_external_surface_acceptance_readiness(
            provided_validation_evidence="phase_7_full_validation_result",  # type: ignore[arg-type]
            provided_uat_evidence=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        )


def test_forbidden_acceptance_assumptions_are_explicit() -> None:
    assert "phase_8_readiness" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS
    assert "cloud_deployment_readiness" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS
    assert "saas_productization_readiness" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS
    assert "model_provider_operational_readiness" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS
    assert "product_ready_document_generation" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS
    assert "standards_citation_authority" in FORBIDDEN_ACCEPTANCE_ASSUMPTIONS


def test_external_surface_acceptance_module_does_not_import_forbidden_modules() -> None:
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
