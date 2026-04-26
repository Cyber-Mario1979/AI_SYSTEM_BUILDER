"""Controlled AI authoring modes and bounded invention policy for M12.4."""

from __future__ import annotations

from typing import Any

from .document_contracts import (
    GENERATED_LANGUAGE_OUTPUT_ROLE,
    validate_document_request_payload,
)

AUTHORING_CONTROL_CHECKPOINT_ID = "M12.4"
AUTHORING_CONTROL_CONTRACT_VERSION = "authoring-control-contract-v1"

AI_AUTHORING_LAYER_ROLE = "bounded_downstream_ai_authoring_layer"
EXECUTION_TRUTH_REFERENCE_ROLE = "execution_truth_reference_only"
TEMPLATE_TRUTH_REFERENCE_ROLE = "template_truth_reference_only"

STRONG_STRUCTURED_INPUT_FILL_MODE = "strong_structured_input_fill"
PARTIAL_INPUT_BOUNDED_COMPLETION_MODE = "partial_input_bounded_completion"
MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE = "minimal_input_scaffold_generation"

SUPPORTED_AUTHORING_MODES = (
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
)

BOUNDED_INVENTION_POLICY = (
    "bounded_invention_requires_guardrails_standards_and_document_family_rules"
)
UNRESTRICTED_FREE_DRAFTING_POLICY = (
    "unrestricted_free_drafting_rejected_as_execution_truth"
)
GENERATED_OUTPUT_TRUTH_BOUNDARY = (
    "generated_language_output_may_not_replace_execution_or_template_truth"
)

_REQUIRED_AUTHORING_PAYLOAD_FIELDS = (
    "checkpoint",
    "contract_version",
    "authoring_layer_role",
    "authoring_mode",
    "document_family",
    "document_request_ref",
    "document_request_snapshot",
    "input_completeness",
    "bounded_invention",
    "guardrails",
    "standards_refs",
    "document_family_rules",
    "truth_separation",
    "prohibited_behaviors",
)

_PROHIBITED_AUTHORING_FIELDS = (
    "freeform_prompt",
    "unrestricted_prompt",
    "source_authority_override",
    "execution_truth_update",
    "template_truth_update",
    "approved_document_state",
    "resolver_bypass",
)


def build_ai_authoring_control_baseline() -> dict[str, Any]:
    """Return the explicit M12.4 controlled-authoring baseline."""

    return {
        "checkpoint": AUTHORING_CONTROL_CHECKPOINT_ID,
        "contract_version": AUTHORING_CONTROL_CONTRACT_VERSION,
        "authoring_layer_role": AI_AUTHORING_LAYER_ROLE,
        "supported_authoring_modes": list(SUPPORTED_AUTHORING_MODES),
        "bounded_invention_policy": BOUNDED_INVENTION_POLICY,
        "unrestricted_free_drafting_policy": UNRESTRICTED_FREE_DRAFTING_POLICY,
        "generated_output_truth_boundary": GENERATED_OUTPUT_TRUTH_BOUNDARY,
        "required_bounded_invention_controls": [
            "guardrails",
            "standards_refs",
            "document_family_rules",
            "bounded_invention_scope",
        ],
        "downstream_boundary": (
            "ai_authoring_may_generate_language_but_may_not_create_or_replace_"
            "execution_truth_template_truth_or_approval_state"
        ),
    }


def build_authoring_mode_policy(authoring_mode: str) -> dict[str, Any]:
    """Build the deterministic policy for one controlled authoring mode."""

    _validate_authoring_mode(authoring_mode)

    if authoring_mode == STRONG_STRUCTURED_INPUT_FILL_MODE:
        return {
            "authoring_mode": authoring_mode,
            "requires_complete_structured_input": True,
            "bounded_invention_required": False,
            "allowed_output_kind": "template_fill_from_structured_input",
        }

    if authoring_mode == PARTIAL_INPUT_BOUNDED_COMPLETION_MODE:
        return {
            "authoring_mode": authoring_mode,
            "requires_complete_structured_input": False,
            "bounded_invention_required": True,
            "allowed_output_kind": "bounded_completion_with_labeled_assumptions",
        }

    return {
        "authoring_mode": authoring_mode,
        "requires_complete_structured_input": False,
        "bounded_invention_required": True,
        "allowed_output_kind": "minimal_scaffold_with_placeholders",
    }


def build_ai_authoring_request_payload(
    *,
    document_request_payload: dict[str, object],
    authoring_mode: str,
    standards_refs: list[str] | tuple[str, ...],
    guardrails: list[str] | tuple[str, ...],
    document_family_rules: dict[str, object],
    allow_bounded_invention: bool = False,
    bounded_invention_scope: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build a governed M12.4 AI-authoring request payload.

    This is intentionally a control contract, not an LLM runtime.
    It constrains whether and how downstream language generation may happen.
    """

    validate_document_request_payload(document_request_payload)
    _validate_authoring_mode(authoring_mode)

    document_family = str(document_request_payload["document_family"])
    missing_input_fields = _find_missing_input_fields(document_request_payload)
    scope = list(bounded_invention_scope or [])

    payload: dict[str, Any] = {
        "checkpoint": AUTHORING_CONTROL_CHECKPOINT_ID,
        "contract_version": AUTHORING_CONTROL_CONTRACT_VERSION,
        "authoring_layer_role": AI_AUTHORING_LAYER_ROLE,
        "authoring_mode": authoring_mode,
        "authoring_mode_policy": build_authoring_mode_policy(authoring_mode),
        "document_family": document_family,
        "document_request_ref": {
            "document_job_id": document_request_payload["document_job_id"],
            "document_id": document_request_payload["document_id"],
            "document_request_contract_version": document_request_payload[
                "contract_version"
            ],
        },
        "document_request_snapshot": document_request_payload,
        "input_completeness": {
            "missing_input_fields": missing_input_fields,
            "has_missing_input": bool(missing_input_fields),
        },
        "bounded_invention": {
            "allowed": allow_bounded_invention,
            "policy": (
                BOUNDED_INVENTION_POLICY
                if allow_bounded_invention
                else "bounded_invention_not_allowed"
            ),
            "scope": scope,
        },
        "guardrails": list(guardrails),
        "standards_refs": list(standards_refs),
        "document_family_rules": document_family_rules,
        "truth_separation": {
            "execution_truth": EXECUTION_TRUTH_REFERENCE_ROLE,
            "template_truth": TEMPLATE_TRUTH_REFERENCE_ROLE,
            "generated_language_output": GENERATED_LANGUAGE_OUTPUT_ROLE,
            "generated_output_boundary": GENERATED_OUTPUT_TRUTH_BOUNDARY,
        },
        "prohibited_behaviors": list(_PROHIBITED_AUTHORING_FIELDS),
    }
    validate_ai_authoring_request_payload(payload)
    return payload


def validate_ai_authoring_request_payload(payload: dict[str, object]) -> None:
    """Validate a governed M12.4 AI-authoring request payload."""

    _validate_required_payload_fields(payload)
    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=AUTHORING_CONTROL_CHECKPOINT_ID,
        error_prefix="AI authoring payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=AUTHORING_CONTROL_CONTRACT_VERSION,
        error_prefix="AI authoring payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="authoring_layer_role",
        expected_value=AI_AUTHORING_LAYER_ROLE,
        error_prefix="AI authoring payload",
    )

    authoring_mode = payload["authoring_mode"]
    if not isinstance(authoring_mode, str):
        raise ValueError("AI authoring payload must declare authoring_mode.")
    _validate_authoring_mode(authoring_mode)

    document_request_snapshot = payload["document_request_snapshot"]
    if not isinstance(document_request_snapshot, dict):
        raise ValueError(
            "AI authoring payload must declare document_request_snapshot."
        )
    validate_document_request_payload(document_request_snapshot)

    document_family = payload["document_family"]
    if document_family != document_request_snapshot["document_family"]:
        raise ValueError(
            "AI authoring payload document_family must match the "
            "document_request_snapshot document_family."
        )

    _validate_no_prohibited_authoring_fields(payload)
    _validate_non_empty_string_list(payload["guardrails"], "guardrails")
    _validate_non_empty_string_list(payload["standards_refs"], "standards_refs")
    _validate_document_family_rules(payload, document_request_snapshot)
    _validate_truth_separation(payload["truth_separation"])
    _validate_bounded_invention_controls(payload)
    _validate_mode_specific_controls(payload)


def _find_missing_input_fields(
    document_request_payload: dict[str, object],
) -> list[str]:
    input_data = document_request_payload.get("input_data")
    if not isinstance(input_data, dict):
        return []

    missing_fields: list[str] = []
    for value in input_data.values():
        if (
            isinstance(value, dict)
            and value.get("status") == "missing"
            and isinstance(value.get("field_name"), str)
        ):
            missing_fields.append(str(value["field_name"]))
    return missing_fields


def _validate_mode_specific_controls(payload: dict[str, object]) -> None:
    authoring_mode = str(payload["authoring_mode"])
    input_completeness = payload["input_completeness"]
    bounded_invention = payload["bounded_invention"]

    if not isinstance(input_completeness, dict):
        raise ValueError("AI authoring payload must declare input_completeness.")
    if not isinstance(bounded_invention, dict):
        raise ValueError("AI authoring payload must declare bounded_invention.")

    missing_fields = input_completeness.get("missing_input_fields")
    if not isinstance(missing_fields, list):
        raise ValueError(
            "AI authoring payload input_completeness must declare "
            "missing_input_fields."
        )

    bounded_allowed = bounded_invention.get("allowed") is True

    if authoring_mode == STRONG_STRUCTURED_INPUT_FILL_MODE:
        if missing_fields:
            raise ValueError(
                "strong_structured_input_fill requires complete structured "
                "input and cannot receive missing input markers."
            )
        if bounded_allowed:
            raise ValueError(
                "strong_structured_input_fill must not allow bounded invention."
            )
        return

    if not bounded_allowed:
        raise ValueError(
            f"{authoring_mode} requires bounded invention controls."
        )


def _validate_bounded_invention_controls(payload: dict[str, object]) -> None:
    bounded_invention = payload["bounded_invention"]
    if not isinstance(bounded_invention, dict):
        raise ValueError("AI authoring payload must declare bounded_invention.")

    allowed = bounded_invention.get("allowed")
    if not isinstance(allowed, bool):
        raise ValueError("bounded_invention.allowed must be a boolean.")

    scope = bounded_invention.get("scope")
    if not isinstance(scope, list):
        raise ValueError("bounded_invention.scope must be a list.")

    if allowed:
        _validate_non_empty_string_list(scope, "bounded_invention.scope")
        _validate_non_empty_string_list(payload["guardrails"], "guardrails")
        _validate_non_empty_string_list(payload["standards_refs"], "standards_refs")
        if not isinstance(payload["document_family_rules"], dict):
            raise ValueError(
                "bounded invention requires document_family_rules."
            )
        return

    if scope:
        raise ValueError(
            "bounded_invention.scope must be empty when bounded invention is "
            "not allowed."
        )


def _validate_document_family_rules(
    payload: dict[str, object],
    document_request_snapshot: dict[str, object],
) -> None:
    document_family_rules = payload["document_family_rules"]
    if not isinstance(document_family_rules, dict) or not document_family_rules:
        raise ValueError("AI authoring payload must declare document_family_rules.")

    declared_family = document_family_rules.get("document_family")
    if declared_family != document_request_snapshot["document_family"]:
        raise ValueError(
            "document_family_rules.document_family must match the governed "
            "document request family."
        )


def _validate_truth_separation(truth_separation: object) -> None:
    if not isinstance(truth_separation, dict):
        raise ValueError("AI authoring payload must declare truth_separation.")

    expected_values = {
        "execution_truth": EXECUTION_TRUTH_REFERENCE_ROLE,
        "template_truth": TEMPLATE_TRUTH_REFERENCE_ROLE,
        "generated_language_output": GENERATED_LANGUAGE_OUTPUT_ROLE,
        "generated_output_boundary": GENERATED_OUTPUT_TRUTH_BOUNDARY,
    }
    for field_name, expected_value in expected_values.items():
        actual_value = truth_separation.get(field_name)
        if actual_value != expected_value:
            raise ValueError(
                "AI authoring truth_separation declares an invalid "
                f"{field_name}: expected {expected_value!r}, got "
                f"{actual_value!r}."
            )


def _validate_no_prohibited_authoring_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_AUTHORING_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in AI authoring payloads."
            )


def _validate_authoring_mode(authoring_mode: str) -> None:
    if authoring_mode not in SUPPORTED_AUTHORING_MODES:
        raise ValueError(
            "Unsupported authoring_mode. "
            f"Expected one of: {', '.join(SUPPORTED_AUTHORING_MODES)}."
        )


def _validate_required_payload_fields(payload: dict[str, object]) -> None:
    for field_name in _REQUIRED_AUTHORING_PAYLOAD_FIELDS:
        if field_name not in payload:
            raise ValueError(
                f"AI authoring payload must declare {field_name}."
            )


def _validate_non_empty_string_list(value: object, field_name: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field_name} must be a non-empty list of strings.")

    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings.")


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )
