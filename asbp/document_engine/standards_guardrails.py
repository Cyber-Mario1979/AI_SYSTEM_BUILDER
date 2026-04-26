"""Standards, language, and evidence guardrails for M12.5."""

from __future__ import annotations

from typing import Any

from .authoring_controls import validate_ai_authoring_request_payload

STANDARDS_GUARDRAIL_CHECKPOINT_ID = "M12.5"
STANDARDS_GUARDRAIL_CONTRACT_VERSION = "standards-language-evidence-guardrail-contract-v1"

CONTROLLED_GMP_CQV_LANGUAGE_PROFILE = "controlled_gmp_cqv_language"
ASSUMPTION_LABELING_POLICY = "assumptions_must_be_explicitly_labeled"
PLACEHOLDER_POLICY = "missing_evidence_uses_explicit_placeholders"
EVIDENCE_INFERENCE_SEPARATION_POLICY = "evidence_and_inference_must_be_separated"
SECTION_LEVEL_AUTHORING_CONSTRAINT_POLICY = "section_level_authoring_constraints_required"
DETAIL_LEVEL_CONSISTENCY_POLICY = "detail_level_consistency_required_across_document_family"

EVIDENCE_SUPPORTED_CLASSIFICATION = "evidence_supported"
BOUNDED_INFERENCE_CLASSIFICATION = "bounded_inference"
EXPLICIT_ASSUMPTION_CLASSIFICATION = "explicit_assumption"
PLACEHOLDER_ONLY_CLASSIFICATION = "placeholder_only"

SUPPORTED_EVIDENCE_CLASSIFICATIONS = (
    EVIDENCE_SUPPORTED_CLASSIFICATION,
    BOUNDED_INFERENCE_CLASSIFICATION,
    EXPLICIT_ASSUMPTION_CLASSIFICATION,
    PLACEHOLDER_ONLY_CLASSIFICATION,
)

DEFAULT_PROHIBITED_LANGUAGE_PATTERNS = (
    "guaranteed compliant",
    "fully compliant",
    "validated by ai",
    "approved by ai",
    "no deviation possible",
    "no risk",
    "will pass",
    "regulatory approval guaranteed",
)

_REQUIRED_POLICY_FIELDS = (
    "checkpoint",
    "contract_version",
    "document_family",
    "language_profile",
    "standards_refs",
    "document_family_structure_rules",
    "standards_aware_phrasing_rules",
    "assumption_labeling_policy",
    "placeholder_policy",
    "evidence_inference_separation_policy",
    "prohibited_language_patterns",
    "section_level_authoring_constraints",
    "detail_level_consistency_rules",
)

_REQUIRED_SECTION_FIELDS = (
    "section_id",
    "section_title",
    "content",
    "evidence_classification",
    "standards_refs",
    "evidence_refs",
    "inference_refs",
    "assumptions",
    "placeholders",
)

_REQUIRED_OUTPUT_FIELDS = (
    "checkpoint",
    "contract_version",
    "document_family",
    "authoring_request_ref",
    "authoring_request_snapshot",
    "document_family_guardrail_policy",
    "sections",
    "guardrail_enforcement",
)

_PROHIBITED_OUTPUT_FIELDS = (
    "approval_decision",
    "approved_document_state",
    "execution_truth_update",
    "template_truth_update",
    "unsupported_claims_allowed",
    "unlabeled_assumptions_allowed",
)


def build_standards_language_evidence_guardrail_baseline() -> dict[str, Any]:
    """Return the explicit M12.5 standards/language/evidence baseline."""

    return {
        "checkpoint": STANDARDS_GUARDRAIL_CHECKPOINT_ID,
        "contract_version": STANDARDS_GUARDRAIL_CONTRACT_VERSION,
        "language_profile": CONTROLLED_GMP_CQV_LANGUAGE_PROFILE,
        "document_family_structure_rule": "document_sections_must_follow_declared_family_policy",
        "standards_aware_phrasing_rule": "claims_must_reference_declared_standards_or_be_labeled",
        "assumption_labeling_policy": ASSUMPTION_LABELING_POLICY,
        "placeholder_policy": PLACEHOLDER_POLICY,
        "evidence_inference_separation_policy": EVIDENCE_INFERENCE_SEPARATION_POLICY,
        "section_level_authoring_constraint_policy": SECTION_LEVEL_AUTHORING_CONSTRAINT_POLICY,
        "detail_level_consistency_policy": DETAIL_LEVEL_CONSISTENCY_POLICY,
        "supported_evidence_classifications": list(SUPPORTED_EVIDENCE_CLASSIFICATIONS),
        "default_prohibited_language_patterns": list(DEFAULT_PROHIBITED_LANGUAGE_PATTERNS),
    }


def build_document_family_guardrail_policy(
    *,
    document_family: str,
    standards_refs: list[str] | tuple[str, ...],
    allowed_sections: list[str] | tuple[str, ...],
    required_sections: list[str] | tuple[str, ...] | None = None,
    prohibited_language_patterns: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build section, standards, language, and evidence rules for one family."""

    _validate_non_empty_string(document_family, "document_family")
    standards = _as_non_empty_string_list(list(standards_refs), "standards_refs")
    allowed = _as_non_empty_string_list(list(allowed_sections), "allowed_sections")
    required = list(required_sections or [])
    _validate_string_list(required, "required_sections")

    unknown_required = [section_id for section_id in required if section_id not in allowed]
    if unknown_required:
        raise ValueError(
            "required_sections must be included in allowed_sections: "
            f"{', '.join(unknown_required)}."
        )

    patterns = list(prohibited_language_patterns or DEFAULT_PROHIBITED_LANGUAGE_PATTERNS)
    _validate_string_list(patterns, "prohibited_language_patterns")

    policy: dict[str, Any] = {
        "checkpoint": STANDARDS_GUARDRAIL_CHECKPOINT_ID,
        "contract_version": STANDARDS_GUARDRAIL_CONTRACT_VERSION,
        "document_family": document_family,
        "language_profile": CONTROLLED_GMP_CQV_LANGUAGE_PROFILE,
        "standards_refs": standards,
        "document_family_structure_rules": {
            "allowed_sections": allowed,
            "required_sections": required,
            "section_order_policy": "declared_allowed_section_order",
        },
        "standards_aware_phrasing_rules": [
            "standards_claims_must_use_declared_standards_refs",
            "unsupported_claims_must_not_be_presented_as_evidence",
            "generated_language_must_not_create_approval_or_validation_truth",
        ],
        "assumption_labeling_policy": ASSUMPTION_LABELING_POLICY,
        "placeholder_policy": PLACEHOLDER_POLICY,
        "evidence_inference_separation_policy": EVIDENCE_INFERENCE_SEPARATION_POLICY,
        "prohibited_language_patterns": patterns,
        "section_level_authoring_constraints": {
            section_id: {
                "requires_evidence_classification": True,
                "requires_standards_refs": True,
                "requires_evidence_or_explicit_assumption_or_placeholder": True,
            }
            for section_id in allowed
        },
        "detail_level_consistency_rules": [
            DETAIL_LEVEL_CONSISTENCY_POLICY,
            "same_document_family_policy_applies_to_all_sections",
            "section_standards_refs_must_be_declared_in_family_policy",
            "required_sections_must_be_present_before_acceptance",
        ],
    }
    validate_document_family_guardrail_policy(policy)
    return policy


def build_guarded_document_section(
    *,
    section_id: str,
    section_title: str,
    content: str,
    evidence_classification: str,
    standards_refs: list[str] | tuple[str, ...],
    evidence_refs: list[str] | tuple[str, ...] | None = None,
    inference_refs: list[str] | tuple[str, ...] | None = None,
    assumptions: list[str] | tuple[str, ...] | None = None,
    placeholders: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build one guarded section output with explicit evidence status."""

    section = {
        "section_id": section_id,
        "section_title": section_title,
        "content": content,
        "evidence_classification": evidence_classification,
        "standards_refs": list(standards_refs),
        "evidence_refs": list(evidence_refs or []),
        "inference_refs": list(inference_refs or []),
        "assumptions": list(assumptions or []),
        "placeholders": list(placeholders or []),
    }
    _validate_section_shape(section)
    _validate_section_evidence_rules(section)
    return section


def build_guarded_authoring_output_payload(
    *,
    authoring_request_payload: dict[str, object],
    document_family_guardrail_policy: dict[str, object],
    sections: list[dict[str, object]] | tuple[dict[str, object], ...],
) -> dict[str, Any]:
    """Build a guarded M12.5 authoring output payload."""

    validate_ai_authoring_request_payload(authoring_request_payload)
    validate_document_family_guardrail_policy(document_family_guardrail_policy)

    document_family = str(authoring_request_payload["document_family"])
    if document_family_guardrail_policy["document_family"] != document_family:
        raise ValueError(
            "Guardrail policy document_family must match the authoring request document_family."
        )

    guarded_sections = list(sections)
    if not guarded_sections:
        raise ValueError("Guarded authoring output must include sections.")

    document_request_ref = authoring_request_payload["document_request_ref"]
    if not isinstance(document_request_ref, dict):
        raise ValueError("Authoring request must declare document_request_ref.")

    payload: dict[str, Any] = {
        "checkpoint": STANDARDS_GUARDRAIL_CHECKPOINT_ID,
        "contract_version": STANDARDS_GUARDRAIL_CONTRACT_VERSION,
        "document_family": document_family,
        "authoring_request_ref": {
            "document_job_id": document_request_ref["document_job_id"],
            "document_id": document_request_ref["document_id"],
            "authoring_contract_version": authoring_request_payload["contract_version"],
        },
        "authoring_request_snapshot": authoring_request_payload,
        "document_family_guardrail_policy": document_family_guardrail_policy,
        "sections": guarded_sections,
        "guardrail_enforcement": {
            "assumption_labeling_policy": ASSUMPTION_LABELING_POLICY,
            "placeholder_policy": PLACEHOLDER_POLICY,
            "evidence_inference_separation_policy": EVIDENCE_INFERENCE_SEPARATION_POLICY,
            "section_level_authoring_constraint_policy": SECTION_LEVEL_AUTHORING_CONSTRAINT_POLICY,
            "detail_level_consistency_policy": DETAIL_LEVEL_CONSISTENCY_POLICY,
            "acceptance_boundary": (
                "guardrails_accept_language_shape_only_not_document_approval_or_execution_truth"
            ),
        },
    }
    validate_guarded_authoring_output_payload(payload)
    return payload


def validate_document_family_guardrail_policy(policy: dict[str, object]) -> None:
    """Validate an M12.5 document-family guardrail policy."""

    _validate_required_fields(policy, _REQUIRED_POLICY_FIELDS, "Guardrail policy")
    _validate_expected_exact_value(
        policy,
        field_name="checkpoint",
        expected_value=STANDARDS_GUARDRAIL_CHECKPOINT_ID,
        error_prefix="Guardrail policy",
    )
    _validate_expected_exact_value(
        policy,
        field_name="contract_version",
        expected_value=STANDARDS_GUARDRAIL_CONTRACT_VERSION,
        error_prefix="Guardrail policy",
    )
    _validate_expected_exact_value(
        policy,
        field_name="language_profile",
        expected_value=CONTROLLED_GMP_CQV_LANGUAGE_PROFILE,
        error_prefix="Guardrail policy",
    )
    _validate_expected_exact_value(
        policy,
        field_name="assumption_labeling_policy",
        expected_value=ASSUMPTION_LABELING_POLICY,
        error_prefix="Guardrail policy",
    )
    _validate_expected_exact_value(
        policy,
        field_name="placeholder_policy",
        expected_value=PLACEHOLDER_POLICY,
        error_prefix="Guardrail policy",
    )
    _validate_expected_exact_value(
        policy,
        field_name="evidence_inference_separation_policy",
        expected_value=EVIDENCE_INFERENCE_SEPARATION_POLICY,
        error_prefix="Guardrail policy",
    )

    _validate_non_empty_string(str(policy["document_family"]), "document_family")
    _as_non_empty_string_list(policy["standards_refs"], "standards_refs")
    _as_non_empty_string_list(policy["standards_aware_phrasing_rules"], "standards_aware_phrasing_rules")
    _as_non_empty_string_list(policy["prohibited_language_patterns"], "prohibited_language_patterns")

    structure_rules = policy["document_family_structure_rules"]
    if not isinstance(structure_rules, dict):
        raise ValueError("Guardrail policy must declare structure rules.")
    allowed_sections = _as_non_empty_string_list(structure_rules.get("allowed_sections"), "allowed_sections")
    required_sections = structure_rules.get("required_sections")
    if not isinstance(required_sections, list):
        raise ValueError("required_sections must be a list.")
    _validate_string_list(required_sections, "required_sections")
    for section_id in required_sections:
        if section_id not in allowed_sections:
            raise ValueError("required_sections must be included in allowed_sections.")

    section_constraints = policy["section_level_authoring_constraints"]
    if not isinstance(section_constraints, dict):
        raise ValueError("Guardrail policy must declare section_level_authoring_constraints.")
    for section_id in allowed_sections:
        if section_id not in section_constraints:
            raise ValueError(
                "section_level_authoring_constraints must cover every allowed section: "
                f"missing {section_id!r}."
            )


def validate_guarded_authoring_output_payload(payload: dict[str, object]) -> None:
    """Validate a guarded M12.5 authoring output payload."""

    _validate_required_fields(payload, _REQUIRED_OUTPUT_FIELDS, "Guarded authoring output")
    _validate_no_prohibited_output_fields(payload)
    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=STANDARDS_GUARDRAIL_CHECKPOINT_ID,
        error_prefix="Guarded authoring output",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=STANDARDS_GUARDRAIL_CONTRACT_VERSION,
        error_prefix="Guarded authoring output",
    )

    authoring_request_snapshot = payload["authoring_request_snapshot"]
    if not isinstance(authoring_request_snapshot, dict):
        raise ValueError("Guarded authoring output must declare authoring_request_snapshot.")
    validate_ai_authoring_request_payload(authoring_request_snapshot)

    policy = payload["document_family_guardrail_policy"]
    if not isinstance(policy, dict):
        raise ValueError("Guarded authoring output must declare document_family_guardrail_policy.")
    validate_document_family_guardrail_policy(policy)

    if payload["document_family"] != authoring_request_snapshot["document_family"]:
        raise ValueError("Guarded authoring output document_family must match the authoring request document_family.")
    if payload["document_family"] != policy["document_family"]:
        raise ValueError("Guarded authoring output document_family must match the guardrail policy document_family.")

    sections = payload["sections"]
    if not isinstance(sections, list) or not sections:
        raise ValueError("Guarded authoring output must include sections.")

    _validate_sections_against_policy(sections, policy)


def _validate_sections_against_policy(sections: list[object], policy: dict[str, object]) -> None:
    structure_rules = policy["document_family_structure_rules"]
    assert isinstance(structure_rules, dict)
    allowed_sections = structure_rules["allowed_sections"]
    required_sections = structure_rules["required_sections"]
    assert isinstance(allowed_sections, list)
    assert isinstance(required_sections, list)

    policy_standards_refs = policy["standards_refs"]
    prohibited_language_patterns = policy["prohibited_language_patterns"]
    assert isinstance(policy_standards_refs, list)
    assert isinstance(prohibited_language_patterns, list)

    seen_section_ids: set[str] = set()

    for section in sections:
        if not isinstance(section, dict):
            raise ValueError("Each guarded output section must be a mapping.")
        _validate_section_shape(section)
        _validate_section_evidence_rules(section)

        section_id = str(section["section_id"])
        if section_id not in allowed_sections:
            raise ValueError(
                f"Section {section_id!r} is not allowed by the document-family guardrail policy."
            )
        if section_id in seen_section_ids:
            raise ValueError(f"Duplicate section_id is not allowed: {section_id}.")
        seen_section_ids.add(section_id)

        for standards_ref in section["standards_refs"]:
            if standards_ref not in policy_standards_refs:
                raise ValueError(
                    "Section standards_refs must be declared in the document-family policy: "
                    f"{standards_ref!r}."
                )

        _validate_no_prohibited_language(
            str(section["content"]),
            prohibited_language_patterns,
            section_id,
        )

    missing_required = [section_id for section_id in required_sections if section_id not in seen_section_ids]
    if missing_required:
        raise ValueError(
            "Guarded authoring output is missing required sections: "
            f"{', '.join(missing_required)}."
        )


def _validate_section_shape(section: dict[str, object]) -> None:
    _validate_required_fields(section, _REQUIRED_SECTION_FIELDS, "Guarded section")
    _validate_non_empty_string(str(section["section_id"]), "section_id")
    _validate_non_empty_string(str(section["section_title"]), "section_title")
    _validate_non_empty_string(str(section["content"]), "content")

    evidence_classification = section["evidence_classification"]
    if evidence_classification not in SUPPORTED_EVIDENCE_CLASSIFICATIONS:
        raise ValueError(
            "Unsupported evidence_classification. Expected one of: "
            f"{', '.join(SUPPORTED_EVIDENCE_CLASSIFICATIONS)}."
        )

    _as_non_empty_string_list(section["standards_refs"], "standards_refs")
    _validate_string_list(section["evidence_refs"], "evidence_refs")
    _validate_string_list(section["inference_refs"], "inference_refs")
    _validate_string_list(section["assumptions"], "assumptions")
    _validate_string_list(section["placeholders"], "placeholders")


def _validate_section_evidence_rules(section: dict[str, object]) -> None:
    evidence_classification = section["evidence_classification"]
    evidence_refs = section["evidence_refs"]
    inference_refs = section["inference_refs"]
    assumptions = section["assumptions"]
    placeholders = section["placeholders"]

    assert isinstance(evidence_refs, list)
    assert isinstance(inference_refs, list)
    assert isinstance(assumptions, list)
    assert isinstance(placeholders, list)

    if evidence_classification == EVIDENCE_SUPPORTED_CLASSIFICATION:
        _as_non_empty_string_list(evidence_refs, "evidence_refs")
        return

    if evidence_classification == BOUNDED_INFERENCE_CLASSIFICATION:
        _as_non_empty_string_list(inference_refs, "inference_refs")
        _validate_labeled_assumptions(assumptions)
        return

    if evidence_classification == EXPLICIT_ASSUMPTION_CLASSIFICATION:
        _validate_labeled_assumptions(assumptions)
        return

    if evidence_classification == PLACEHOLDER_ONLY_CLASSIFICATION:
        _validate_placeholder_entries(placeholders)
        return


def _validate_labeled_assumptions(assumptions: list[object]) -> None:
    _as_non_empty_string_list(assumptions, "assumptions")
    for assumption in assumptions:
        if not str(assumption).startswith("Assumption:"):
            raise ValueError("Assumptions must be explicitly labeled with 'Assumption:'.")


def _validate_placeholder_entries(placeholders: list[object]) -> None:
    _as_non_empty_string_list(placeholders, "placeholders")
    for placeholder in placeholders:
        text = str(placeholder)
        if not (text.startswith("(TBD)") or text.startswith("TBD:") or text.startswith("Placeholder:")):
            raise ValueError("Placeholders must be explicitly labeled as '(TBD)', 'TBD:', or 'Placeholder:'.")


def _validate_no_prohibited_language(content: str, prohibited_language_patterns: list[object], section_id: str) -> None:
    content_lower = content.lower()
    for pattern in prohibited_language_patterns:
        pattern_text = str(pattern).strip().lower()
        if pattern_text and pattern_text in content_lower:
            raise ValueError(
                f"Section {section_id!r} contains prohibited language pattern: {pattern_text!r}."
            )


def _validate_no_prohibited_output_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_OUTPUT_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in guarded authoring output.")


def _validate_required_fields(payload: dict[str, object], required_fields: tuple[str, ...], error_prefix: str) -> None:
    for field_name in required_fields:
        if field_name not in payload:
            raise ValueError(f"{error_prefix} must declare {field_name}.")


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _as_non_empty_string_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field_name} must be a non-empty list of strings.")
    _validate_string_list(value, field_name)
    return [str(item) for item in value]


def _validate_string_list(value: object, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list of strings.")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings.")


def _validate_expected_exact_value(payload: dict[str, object], *, field_name: str, expected_value: str, error_prefix: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: expected {expected_value!r}, got {actual_value!r}."
        )
