"""Validation and acceptance discipline for external API/UI surfaces.

M21.5 defines validation and UAT acceptance expectations for Phase 7 external
surfaces. It does not run the Phase 7 validation checkpoint, complete UAT,
enter Phase 8, or introduce cloud, deployment, SaaS, or productization behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from ._normalization import normalize_labels, normalize_token


class ExternalSurfaceAcceptanceEvidenceCategory(StrEnum):
    """Stable evidence categories for external-surface validation/UAT discipline."""

    M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE = "m21_1_shared_external_contract_discipline"
    M21_2_UI_API_CONSISTENCY_RULES = "m21_2_ui_api_consistency_rules"
    M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION = "m21_3_product_surface_governance_foundation"
    M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION = "m21_4_external_surface_boundary_consolidation"
    PHASE_7_FULL_VALIDATION_RESULT = "phase_7_full_validation_result"
    PHASE_7_UAT_PROTOCOL = "phase_7_uat_protocol"
    PHASE_7_UAT_REPORT = "phase_7_uat_report"
    PHASE_7_CLOSEOUT_NOTES = "phase_7_closeout_notes"
    DEFERRED_DEPENDENCY_DISPOSITION = "deferred_dependency_disposition"


class AcceptanceDecision(StrEnum):
    """Stable acceptance-decision vocabulary for external-surface evidence."""

    PASS_ = "pass"
    CONDITIONAL_PASS = "conditional_pass"
    FAIL = "fail"
    NOT_READY = "not_ready"


class ExternalSurfaceAcceptanceReadinessResult(StrEnum):
    """Stable readiness result vocabulary."""

    READY = "ready"
    NOT_READY = "not_ready"
    REJECTED = "rejected"


EXPECTED_VALIDATION_EVIDENCE_CATEGORIES: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...] = (
    ExternalSurfaceAcceptanceEvidenceCategory.M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE,
    ExternalSurfaceAcceptanceEvidenceCategory.M21_2_UI_API_CONSISTENCY_RULES,
    ExternalSurfaceAcceptanceEvidenceCategory.M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION,
    ExternalSurfaceAcceptanceEvidenceCategory.M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION,
    ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_FULL_VALIDATION_RESULT,
)

EXPECTED_UAT_EVIDENCE_CATEGORIES: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...] = (
    ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_UAT_PROTOCOL,
    ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_UAT_REPORT,
)

EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...] = (
    *EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
    *EXPECTED_UAT_EVIDENCE_CATEGORIES,
    ExternalSurfaceAcceptanceEvidenceCategory.PHASE_7_CLOSEOUT_NOTES,
    ExternalSurfaceAcceptanceEvidenceCategory.DEFERRED_DEPENDENCY_DISPOSITION,
)

FORBIDDEN_ACCEPTANCE_ASSUMPTIONS: tuple[str, ...] = (
    "phase_8_readiness",
    "phase_9_readiness",
    "cloud_deployment_readiness",
    "saas_productization_readiness",
    "tenant_model_readiness",
    "commercial_launch_readiness",
    "model_provider_operational_readiness",
    "product_ready_document_generation",
    "standards_citation_authority",
)


def normalize_acceptance_evidence_category(
    value: ExternalSurfaceAcceptanceEvidenceCategory | str,
) -> ExternalSurfaceAcceptanceEvidenceCategory:
    """Normalize an acceptance evidence category or fail closed."""

    if isinstance(value, ExternalSurfaceAcceptanceEvidenceCategory):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("acceptance evidence category must be a non-empty string")

    try:
        return ExternalSurfaceAcceptanceEvidenceCategory(normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported acceptance evidence category: {value}") from exc


def normalize_acceptance_decision(value: AcceptanceDecision | str) -> AcceptanceDecision:
    """Normalize an acceptance decision or fail closed."""

    if isinstance(value, AcceptanceDecision):
        return value

    if not isinstance(value, str) or not value.strip():
        raise ValueError("acceptance decision must be a non-empty string")

    try:
        return AcceptanceDecision(normalize_token(value))
    except ValueError as exc:
        raise ValueError(f"unsupported acceptance decision: {value}") from exc


def _normalize_evidence_categories(
    values: Iterable[ExternalSurfaceAcceptanceEvidenceCategory | str],
    *,
    field_name: str,
) -> tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of acceptance evidence categories")

    return tuple(normalize_acceptance_evidence_category(value) for value in values)


def get_expected_validation_evidence_categories() -> tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]:
    """Return expected validation evidence categories in deterministic order."""

    return EXPECTED_VALIDATION_EVIDENCE_CATEGORIES


def get_expected_uat_evidence_categories() -> tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]:
    """Return expected UAT evidence categories in deterministic order."""

    return EXPECTED_UAT_EVIDENCE_CATEGORIES


def get_expected_phase_7_closeout_evidence() -> tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]:
    """Return expected Phase 7 closeout evidence categories in deterministic order."""

    return EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE


@dataclass(frozen=True)
class ExternalSurfaceAcceptanceDiscipline:
    """Static validation/UAT acceptance discipline for Phase 7 external surfaces."""

    validation_evidence_categories: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]
    uat_evidence_categories: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]
    phase_7_closeout_evidence: tuple[ExternalSurfaceAcceptanceEvidenceCategory, ...]
    allowed_acceptance_decisions: tuple[AcceptanceDecision, ...]
    forbidden_assumptions: tuple[str, ...]
    explicit_non_goals: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "validation_evidence_categories",
            _normalize_evidence_categories(
                self.validation_evidence_categories,
                field_name="validation_evidence_categories",
            ),
        )
        object.__setattr__(
            self,
            "uat_evidence_categories",
            _normalize_evidence_categories(
                self.uat_evidence_categories,
                field_name="uat_evidence_categories",
            ),
        )
        object.__setattr__(
            self,
            "phase_7_closeout_evidence",
            _normalize_evidence_categories(
                self.phase_7_closeout_evidence,
                field_name="phase_7_closeout_evidence",
            ),
        )
        object.__setattr__(
            self,
            "allowed_acceptance_decisions",
            tuple(normalize_acceptance_decision(value) for value in self.allowed_acceptance_decisions),
        )

        if not isinstance(self.forbidden_assumptions, tuple):
            raise TypeError("forbidden_assumptions must be a tuple")

        if not isinstance(self.explicit_non_goals, tuple):
            raise TypeError("explicit_non_goals must be a tuple")

        if any(not isinstance(value, str) or not value.strip() for value in self.forbidden_assumptions):
            raise ValueError("forbidden_assumptions must contain non-empty strings")

        if any(not isinstance(value, str) or not value.strip() for value in self.explicit_non_goals):
            raise ValueError("explicit_non_goals must contain non-empty strings")

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "validation_evidence_categories": tuple(value.value for value in self.validation_evidence_categories),
            "uat_evidence_categories": tuple(value.value for value in self.uat_evidence_categories),
            "phase_7_closeout_evidence": tuple(value.value for value in self.phase_7_closeout_evidence),
            "allowed_acceptance_decisions": tuple(value.value for value in self.allowed_acceptance_decisions),
            "forbidden_assumptions": self.forbidden_assumptions,
            "explicit_non_goals": self.explicit_non_goals,
        }


@dataclass(frozen=True)
class ExternalSurfaceAcceptanceReadinessDecision:
    """Deterministic readiness decision for external-surface acceptance evidence."""

    result: ExternalSurfaceAcceptanceReadinessResult
    reason: str
    missing_evidence: tuple[str, ...] = ()
    required_boundary: str | None = None

    def __post_init__(self) -> None:
        result = (
            self.result
            if isinstance(self.result, ExternalSurfaceAcceptanceReadinessResult)
            else ExternalSurfaceAcceptanceReadinessResult(self.result)
        )

        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")

        if not isinstance(self.missing_evidence, tuple):
            raise TypeError("missing_evidence must be a tuple")

        if any(not isinstance(value, str) or not value.strip() for value in self.missing_evidence):
            raise ValueError("missing_evidence must contain non-empty strings")

        object.__setattr__(self, "result", result)
        object.__setattr__(self, "reason", self.reason.strip())

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation."""

        return {
            "result": self.result.value,
            "reason": self.reason,
            "missing_evidence": self.missing_evidence,
            "required_boundary": self.required_boundary,
        }


def build_external_surface_acceptance_discipline() -> ExternalSurfaceAcceptanceDiscipline:
    """Build the static Phase 7 external-surface validation/UAT discipline."""

    return ExternalSurfaceAcceptanceDiscipline(
        validation_evidence_categories=EXPECTED_VALIDATION_EVIDENCE_CATEGORIES,
        uat_evidence_categories=EXPECTED_UAT_EVIDENCE_CATEGORIES,
        phase_7_closeout_evidence=EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE,
        allowed_acceptance_decisions=(
            AcceptanceDecision.PASS_,
            AcceptanceDecision.CONDITIONAL_PASS,
            AcceptanceDecision.FAIL,
            AcceptanceDecision.NOT_READY,
        ),
        forbidden_assumptions=FORBIDDEN_ACCEPTANCE_ASSUMPTIONS,
        explicit_non_goals=(
            "phase_8_execution",
            "cloud_deployment",
            "tenant_saas_behavior",
            "commercial_productization",
            "model_provider_integration",
            "product_ready_document_generation",
            "standards_embedding_or_citation_authority",
        ),
    )


def evaluate_external_surface_acceptance_readiness(
    *,
    provided_validation_evidence: Iterable[ExternalSurfaceAcceptanceEvidenceCategory | str],
    provided_uat_evidence: Iterable[ExternalSurfaceAcceptanceEvidenceCategory | str],
    provided_closeout_evidence: Iterable[ExternalSurfaceAcceptanceEvidenceCategory | str] = (),
    acceptance_decision: AcceptanceDecision | str = AcceptanceDecision.NOT_READY,
    assumptions: Iterable[str] = (),
) -> ExternalSurfaceAcceptanceReadinessDecision:
    """Evaluate whether external-surface evidence is ready for acceptance review."""

    normalized_validation = set(
        _normalize_evidence_categories(
            provided_validation_evidence,
            field_name="provided_validation_evidence",
        )
    )
    normalized_uat = set(
        _normalize_evidence_categories(
            provided_uat_evidence,
            field_name="provided_uat_evidence",
        )
    )
    normalized_closeout = set(
        _normalize_evidence_categories(
            provided_closeout_evidence,
            field_name="provided_closeout_evidence",
        )
    )
    normalized_decision = normalize_acceptance_decision(acceptance_decision)
    normalized_assumptions = normalize_labels(assumptions, field_name="assumptions")

    forbidden_assumptions = set(normalized_assumptions).intersection(FORBIDDEN_ACCEPTANCE_ASSUMPTIONS)
    if forbidden_assumptions:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.REJECTED,
            reason="acceptance_discipline_cannot_assume_productization_readiness",
            required_boundary="Phase 7 acceptance does not authorize Phase 8, cloud, deployment, SaaS, or productization readiness",
        )

    missing_validation = tuple(
        category.value
        for category in EXPECTED_VALIDATION_EVIDENCE_CATEGORIES
        if category not in normalized_validation
    )
    if missing_validation:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.NOT_READY,
            reason="missing_required_validation_evidence",
            missing_evidence=missing_validation,
            required_boundary="M21.6 validation evidence required before Phase 7 closeout",
        )

    missing_uat = tuple(
        category.value
        for category in EXPECTED_UAT_EVIDENCE_CATEGORIES
        if category not in normalized_uat
    )
    if missing_uat:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.NOT_READY,
            reason="missing_required_uat_evidence",
            missing_evidence=missing_uat,
            required_boundary="M21.7 UAT evidence required before Phase 7 closeout",
        )

    if normalized_decision is AcceptanceDecision.FAIL:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.REJECTED,
            reason="acceptance_decision_failed",
            required_boundary="external surfaces must pass or be conditionally accepted before closeout",
        )

    if normalized_decision is AcceptanceDecision.NOT_READY:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.NOT_READY,
            reason="acceptance_decision_not_ready",
            required_boundary="acceptance decision must be pass or conditional_pass before closeout",
        )

    missing_closeout = tuple(
        category.value
        for category in EXPECTED_PHASE_7_CLOSEOUT_EVIDENCE
        if category not in normalized_validation
        and category not in normalized_uat
        and category not in normalized_closeout
    )
    if missing_closeout:
        return ExternalSurfaceAcceptanceReadinessDecision(
            result=ExternalSurfaceAcceptanceReadinessResult.NOT_READY,
            reason="missing_required_phase_7_closeout_evidence",
            missing_evidence=missing_closeout,
            required_boundary="M21.8 closeout evidence and deferred dependency disposition required before Phase 7 closeout",
        )

    return ExternalSurfaceAcceptanceReadinessDecision(
        result=ExternalSurfaceAcceptanceReadinessResult.READY,
        reason="external_surface_acceptance_evidence_ready_for_closeout_review",
        required_boundary="Phase 7 closeout review may proceed without implying Phase 8 or productization readiness",
    )
