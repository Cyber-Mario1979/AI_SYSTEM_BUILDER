"""Document request/input/output contracts for the M12.2 checkpoint."""

from __future__ import annotations

from typing import Any

from .template_governance import (
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    SUPPORTED_TEMPLATE_FAMILIES,
    validate_template_identity,
)

DOCUMENT_CONTRACT_CHECKPOINT_ID = "M12.2"

DOCUMENT_REQUEST_CONTRACT_VERSION = "document-request-contract-v1"
DOCUMENT_OUTPUT_CONTRACT_VERSION = "document-output-contract-v1"

EXECUTION_CONTEXT_SOURCE_ROLE = "execution_truth_reference_only"
TEMPLATE_IDENTITY_SOURCE_ROLE = "governed_template_truth_reference_only"
GENERATED_LANGUAGE_OUTPUT_ROLE = "downstream_generated_artifact_only"

SUPPORTED_EXECUTION_CONTEXT_KINDS = (
    "work_package",
    "task",
    "collection",
    "plan",
    "standalone_governed_request",
)

_DOCUMENT_FAMILY_REQUIRED_INPUTS: dict[str, tuple[str, ...]] = {
    "urs": (
        "system_name",
        "system_type",
        "intended_use",
        "user_requirements",
    ),
    "dcf": (
        "target_document_family",
        "collection_scope",
        "requested_fields",
    ),
    "protocol": (
        "protocol_title",
        "scope",
        "acceptance_criteria",
    ),
    "report": (
        "report_title",
        "source_protocol_ref",
        "execution_summary",
    ),
    "other_governed_document": (
        "document_title",
        "scope",
        "purpose",
    ),
}

_REQUIRED_REQUEST_FIELDS = (
    "checkpoint",
    "contract_version",
    "document_job_id",
    "document_family",
    "document_id",
    "template_identity",
    "execution_context",
    "input_data",
    "input_contract",
    "output_contract",
    "truth_separation",
)

_REQUIRED_EXECUTION_CONTEXT_FIELDS = (
    "kind",
    "ref",
    "source_role",
)

_PROHIBITED_INPUT_FIELDS = (
    "generated_content",
    "generated_language_output",
    "approved_document_state",
    "template_body",
    "freeform_prompt",
    "source_authority_override",
    "resolver_bypass",
)

_OUTPUT_CONTRACT_FIELDS = (
    "document_job_id",
    "document_family",
    "document_id",
    "template_identity",
    "execution_context",
    "input_snapshot",
    "generated_language_output",
    "assumptions",
    "placeholders",
    "evidence_refs",
    "output_contract_version",
)


def build_document_request_contract_baseline() -> dict[str, Any]:
    """Return the explicit M12.2 document request/input/output contract baseline."""

    return {
        "checkpoint": DOCUMENT_CONTRACT_CHECKPOINT_ID,
        "request_contract_version": DOCUMENT_REQUEST_CONTRACT_VERSION,
        "output_contract_version": DOCUMENT_OUTPUT_CONTRACT_VERSION,
        "supported_document_families": list(SUPPORTED_TEMPLATE_FAMILIES),
        "supported_execution_context_kinds": list(
            SUPPORTED_EXECUTION_CONTEXT_KINDS
        ),
        "family_required_inputs": {
            family: list(fields)
            for family, fields in _DOCUMENT_FAMILY_REQUIRED_INPUTS.items()
        },
        "truth_separation": {
            "execution_context": EXECUTION_CONTEXT_SOURCE_ROLE,
            "template_identity": TEMPLATE_IDENTITY_SOURCE_ROLE,
            "generated_language_output": GENERATED_LANGUAGE_OUTPUT_ROLE,
        },
        "prohibited_input_fields": list(_PROHIBITED_INPUT_FIELDS),
        "output_contract_fields": list(_OUTPUT_CONTRACT_FIELDS),
    }


def build_document_input_contract(document_family: str) -> dict[str, Any]:
    """Build the input contract for one governed document family."""

    _validate_supported_document_family(document_family)

    return {
        "checkpoint": DOCUMENT_CONTRACT_CHECKPOINT_ID,
        "contract_version": DOCUMENT_REQUEST_CONTRACT_VERSION,
        "document_family": document_family,
        "required_input_fields": list(
            _DOCUMENT_FAMILY_REQUIRED_INPUTS[document_family]
        ),
        "prohibited_input_fields": list(_PROHIBITED_INPUT_FIELDS),
        "input_truth_boundary": "input_data_is_structured_request_data_only",
    }


def build_document_output_contract(document_family: str) -> dict[str, Any]:
    """Build the output contract for one governed document family."""

    _validate_supported_document_family(document_family)

    return {
        "checkpoint": DOCUMENT_CONTRACT_CHECKPOINT_ID,
        "contract_version": DOCUMENT_OUTPUT_CONTRACT_VERSION,
        "document_family": document_family,
        "required_output_fields": list(_OUTPUT_CONTRACT_FIELDS),
        "generated_language_role": GENERATED_LANGUAGE_OUTPUT_ROLE,
        "output_truth_boundary": "output_may_not_replace_execution_or_template_truth",
    }


def build_document_request_payload(
    *,
    document_job_id: str,
    document_family: str,
    document_id: str,
    template_identity: dict[str, object],
    execution_context_kind: str,
    execution_context_ref: str,
    input_data: dict[str, object],
) -> dict[str, Any]:
    """Build a governed document request payload.

    The M12.2 contract is intentionally structural:
    - it binds request identity
    - it binds governed template identity
    - it binds execution context by reference
    - it validates family-specific required inputs
    - it preserves generated language as downstream output only
    """

    request: dict[str, Any] = {
        "checkpoint": DOCUMENT_CONTRACT_CHECKPOINT_ID,
        "contract_version": DOCUMENT_REQUEST_CONTRACT_VERSION,
        "document_job_id": document_job_id,
        "document_family": document_family,
        "document_id": document_id,
        "template_identity": template_identity,
        "execution_context": {
            "kind": execution_context_kind,
            "ref": execution_context_ref,
            "source_role": EXECUTION_CONTEXT_SOURCE_ROLE,
        },
        "input_data": input_data,
        "input_contract": build_document_input_contract(document_family),
        "output_contract": build_document_output_contract(document_family),
        "truth_separation": {
            "execution_context": EXECUTION_CONTEXT_SOURCE_ROLE,
            "template_identity": TEMPLATE_IDENTITY_SOURCE_ROLE,
            "generated_language_output": GENERATED_LANGUAGE_OUTPUT_ROLE,
        },
    }
    validate_document_request_payload(request)
    return request


def validate_document_request_payload(request: dict[str, object]) -> None:
    """Validate a governed document request payload."""

    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "document_job_id",
            "document_family",
            "document_id",
        ),
        error_prefix="Document request payload",
    )
    _validate_required_mapping_fields(
        request,
        (
            "template_identity",
            "execution_context",
            "input_data",
            "input_contract",
            "output_contract",
            "truth_separation",
        ),
        error_prefix="Document request payload",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=DOCUMENT_CONTRACT_CHECKPOINT_ID,
        error_prefix="Document request payload",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=DOCUMENT_REQUEST_CONTRACT_VERSION,
        error_prefix="Document request payload",
    )

    document_family = str(request["document_family"])
    _validate_supported_document_family(document_family)

    template_identity = request["template_identity"]
    assert isinstance(template_identity, dict)
    validate_template_identity(template_identity, allow_supporting_artifacts=False)
    _validate_expected_exact_value(
        template_identity,
        field_name="artifact_kind",
        expected_value=GOVERNED_TEMPLATE_ARTIFACT_KIND,
        error_prefix="Template identity",
    )

    execution_context = request["execution_context"]
    assert isinstance(execution_context, dict)
    _validate_execution_context(execution_context)

    input_data = request["input_data"]
    assert isinstance(input_data, dict)
    _validate_input_data_for_family(document_family, input_data)
    _validate_prohibited_fields(input_data, _PROHIBITED_INPUT_FIELDS)


def _validate_supported_document_family(document_family: str) -> None:
    if document_family not in SUPPORTED_TEMPLATE_FAMILIES:
        raise ValueError(
            "Unsupported document_family. "
            f"Expected one of: {', '.join(SUPPORTED_TEMPLATE_FAMILIES)}."
        )


def _validate_execution_context(execution_context: dict[str, object]) -> None:
    _validate_required_string_fields(
        execution_context,
        _REQUIRED_EXECUTION_CONTEXT_FIELDS,
        error_prefix="Execution context",
    )

    kind = execution_context.get("kind")
    if kind not in SUPPORTED_EXECUTION_CONTEXT_KINDS:
        raise ValueError(
            "Unsupported execution context kind. "
            f"Expected one of: {', '.join(SUPPORTED_EXECUTION_CONTEXT_KINDS)}."
        )

    source_role = execution_context.get("source_role")
    if source_role != EXECUTION_CONTEXT_SOURCE_ROLE:
        raise ValueError(
            "Execution context declares an invalid source_role: "
            f"expected {EXECUTION_CONTEXT_SOURCE_ROLE!r}, got {source_role!r}."
        )


def _validate_input_data_for_family(
    document_family: str,
    input_data: dict[str, object],
) -> None:
    required_fields = _DOCUMENT_FAMILY_REQUIRED_INPUTS[document_family]

    for field_name in required_fields:
        value = input_data.get(field_name)
        if value is None:
            raise ValueError(
                f"Document input_data must declare required {field_name} "
                f"for {document_family!r} documents."
            )


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        value = payload.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{error_prefix} must declare non-empty {field_name}."
            )


def _validate_required_mapping_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        value = payload.get(field_name)
        if not isinstance(value, dict):
            raise ValueError(
                f"{error_prefix} must declare mapping field {field_name}."
            )


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


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in document input_data."
            )