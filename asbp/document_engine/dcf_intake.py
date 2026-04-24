"""DCF intake, extraction, and normalization for the M12.3 checkpoint."""

from __future__ import annotations

from typing import Any

from .document_contracts import build_document_input_contract
from .template_governance import (
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    build_governed_template_retrieval_request,
    validate_template_identity,
)

DCF_INTAKE_CHECKPOINT_ID = "M12.3"
DCF_INTAKE_CONTRACT_VERSION = "dcf-intake-contract-v1"

DCF_RAW_USER_CONTENT_ROLE = "raw_user_filled_dcf_content"
DCF_EXTRACTED_DATA_ROLE = "extracted_structured_dcf_data"
DCF_NORMALIZED_INPUT_ROLE = "normalized_document_input_data"
DCF_DOWNSTREAM_OUTPUT_ROLE = "downstream_generated_document_output_reference"

MISSING_DCF_DATA_POLICY = "missing_required_data_marked_explicitly"
AMBIGUOUS_DCF_DATA_POLICY = "ambiguous_field_values_rejected_without_guessing"

KEY_VALUE_TEXT_CONTENT_FORMAT = "key_value_text"
MAPPING_CONTENT_FORMAT = "mapping"

SUPPORTED_DCF_CONTENT_FORMATS = (
    KEY_VALUE_TEXT_CONTENT_FORMAT,
    MAPPING_CONTENT_FORMAT,
)

_REQUIRED_DCF_INTAKE_FIELDS = (
    "checkpoint",
    "contract_version",
    "dcf_artifact_id",
    "target_document_family",
    "dcf_template_retrieval_request",
    "template_identity",
    "raw_user_content",
    "extracted_data",
    "normalized_document_input",
    "traceability",
    "missing_data_policy",
    "ambiguous_data_policy",
)


def build_dcf_intake_baseline() -> dict[str, Any]:
    """Return the explicit M12.3 DCF intake/extraction baseline."""

    return {
        "checkpoint": DCF_INTAKE_CHECKPOINT_ID,
        "contract_version": DCF_INTAKE_CONTRACT_VERSION,
        "supported_content_formats": list(SUPPORTED_DCF_CONTENT_FORMATS),
        "traceability_chain": [
            DCF_RAW_USER_CONTENT_ROLE,
            DCF_EXTRACTED_DATA_ROLE,
            DCF_NORMALIZED_INPUT_ROLE,
            DCF_DOWNSTREAM_OUTPUT_ROLE,
        ],
        "missing_data_policy": MISSING_DCF_DATA_POLICY,
        "ambiguous_data_policy": AMBIGUOUS_DCF_DATA_POLICY,
        "template_retrieval_family": "dcf",
        "normalization_boundary": (
            "extracted_dcf_data_may_feed_document_input_but_may_not_replace_"
            "execution_truth_or_template_truth"
        ),
    }


def build_dcf_template_retrieval_request(
    *,
    template_id: str,
    template_version: str,
) -> dict[str, Any]:
    """Build a governed retrieval request for a DCF template."""

    return build_governed_template_retrieval_request(
        template_family="dcf",
        template_id=template_id,
        template_version=template_version,
    )


def extract_structured_fields_from_dcf_content(
    raw_content: str | dict[str, object],
    *,
    content_format: str = KEY_VALUE_TEXT_CONTENT_FORMAT,
) -> dict[str, object]:
    """Extract deterministic key/value fields from user-filled DCF content.

    Supported input is intentionally bounded for M12.3:
    - mapping content, where keys are already explicit
    - key/value text lines using ":" or "=" separators

    Duplicate fields with different values are ambiguous and are rejected.
    """

    _validate_content_format(content_format)

    if content_format == MAPPING_CONTENT_FORMAT:
        if not isinstance(raw_content, dict):
            raise ValueError("DCF mapping content must be a dictionary.")
        return {
            _normalize_field_name(key): value
            for key, value in raw_content.items()
            if _normalize_field_name(key)
        }

    if not isinstance(raw_content, str):
        raise ValueError("DCF key_value_text content must be a string.")

    extracted: dict[str, object] = {}

    for line_number, raw_line in enumerate(raw_content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        key, value = _split_key_value_line(line, line_number)
        field_name = _normalize_field_name(key)
        field_value = value.strip()

        if not field_name:
            raise ValueError(f"DCF line {line_number} has an empty field name.")

        if field_name in extracted and extracted[field_name] != field_value:
            raise ValueError(
                f"Ambiguous DCF field {field_name!r}: multiple different "
                "values were provided."
            )

        extracted[field_name] = field_value

    return extracted


def normalize_dcf_extracted_data(
    *,
    target_document_family: str,
    extracted_fields: dict[str, object],
) -> dict[str, Any]:
    """Normalize extracted DCF fields into bounded document input data."""

    input_contract = build_document_input_contract(target_document_family)
    required_fields = input_contract["required_input_fields"]

    normalized_input_data: dict[str, object] = {}
    missing_fields: list[str] = []

    for field_name in required_fields:
        value = extracted_fields.get(field_name)
        if _is_missing_value(value):
            missing_fields.append(field_name)
            normalized_input_data[field_name] = _build_missing_field_marker(
                field_name
            )
            continue

        normalized_input_data[field_name] = value

    additional_extracted_fields = {
        field_name: value
        for field_name, value in extracted_fields.items()
        if field_name not in required_fields
    }

    return {
        "checkpoint": DCF_INTAKE_CHECKPOINT_ID,
        "contract_version": DCF_INTAKE_CONTRACT_VERSION,
        "source_role": DCF_NORMALIZED_INPUT_ROLE,
        "target_document_family": target_document_family,
        "input_contract": input_contract,
        "input_data": normalized_input_data,
        "missing_fields": missing_fields,
        "additional_extracted_fields": additional_extracted_fields,
        "missing_data_policy": MISSING_DCF_DATA_POLICY,
    }


def build_dcf_intake_payload(
    *,
    dcf_artifact_id: str,
    target_document_family: str,
    template_identity: dict[str, object],
    raw_content: str | dict[str, object],
    content_format: str = KEY_VALUE_TEXT_CONTENT_FORMAT,
    downstream_document_id: str | None = None,
) -> dict[str, Any]:
    """Build a traceable DCF intake payload for downstream document input."""

    _validate_non_empty_string(dcf_artifact_id, "dcf_artifact_id")
    _validate_dcf_template_identity(template_identity)

    extracted_fields = extract_structured_fields_from_dcf_content(
        raw_content,
        content_format=content_format,
    )
    normalized_document_input = normalize_dcf_extracted_data(
        target_document_family=target_document_family,
        extracted_fields=extracted_fields,
    )

    payload: dict[str, Any] = {
        "checkpoint": DCF_INTAKE_CHECKPOINT_ID,
        "contract_version": DCF_INTAKE_CONTRACT_VERSION,
        "dcf_artifact_id": dcf_artifact_id,
        "target_document_family": target_document_family,
        "dcf_template_retrieval_request": build_dcf_template_retrieval_request(
            template_id=str(template_identity["template_id"]),
            template_version=str(template_identity["template_version"]),
        ),
        "template_identity": template_identity,
        "raw_user_content": {
            "source_role": DCF_RAW_USER_CONTENT_ROLE,
            "content_format": content_format,
            "content": raw_content,
        },
        "extracted_data": {
            "source_role": DCF_EXTRACTED_DATA_ROLE,
            "fields": extracted_fields,
        },
        "normalized_document_input": normalized_document_input,
        "traceability": {
            "raw_content_ref": dcf_artifact_id,
            "extracted_data_ref": f"{dcf_artifact_id}:extracted_fields",
            "normalized_input_ref": f"{dcf_artifact_id}:normalized_input",
            "downstream_document_id": downstream_document_id,
            "downstream_output_role": DCF_DOWNSTREAM_OUTPUT_ROLE,
        },
        "missing_data_policy": MISSING_DCF_DATA_POLICY,
        "ambiguous_data_policy": AMBIGUOUS_DCF_DATA_POLICY,
    }
    validate_dcf_intake_payload(payload)
    return payload


def validate_dcf_intake_payload(payload: dict[str, object]) -> None:
    """Validate a DCF intake payload produced for M12.3."""

    _validate_required_payload_fields(payload)
    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=DCF_INTAKE_CHECKPOINT_ID,
        error_prefix="DCF intake payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=DCF_INTAKE_CONTRACT_VERSION,
        error_prefix="DCF intake payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="missing_data_policy",
        expected_value=MISSING_DCF_DATA_POLICY,
        error_prefix="DCF intake payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="ambiguous_data_policy",
        expected_value=AMBIGUOUS_DCF_DATA_POLICY,
        error_prefix="DCF intake payload",
    )

    template_identity = payload["template_identity"]
    if not isinstance(template_identity, dict):
        raise ValueError("DCF intake payload must declare template_identity.")
    _validate_dcf_template_identity(template_identity)

    raw_user_content = payload["raw_user_content"]
    if not isinstance(raw_user_content, dict):
        raise ValueError("DCF intake payload must declare raw_user_content.")
    _validate_expected_exact_value(
        raw_user_content,
        field_name="source_role",
        expected_value=DCF_RAW_USER_CONTENT_ROLE,
        error_prefix="DCF raw user content",
    )

    extracted_data = payload["extracted_data"]
    if not isinstance(extracted_data, dict):
        raise ValueError("DCF intake payload must declare extracted_data.")
    _validate_expected_exact_value(
        extracted_data,
        field_name="source_role",
        expected_value=DCF_EXTRACTED_DATA_ROLE,
        error_prefix="DCF extracted data",
    )
    if not isinstance(extracted_data.get("fields"), dict):
        raise ValueError("DCF extracted_data must declare fields.")

    normalized_document_input = payload["normalized_document_input"]
    if not isinstance(normalized_document_input, dict):
        raise ValueError(
            "DCF intake payload must declare normalized_document_input."
        )
    _validate_expected_exact_value(
        normalized_document_input,
        field_name="source_role",
        expected_value=DCF_NORMALIZED_INPUT_ROLE,
        error_prefix="DCF normalized document input",
    )
    if not isinstance(normalized_document_input.get("input_data"), dict):
        raise ValueError(
            "DCF normalized_document_input must declare input_data."
        )

    traceability = payload["traceability"]
    if not isinstance(traceability, dict):
        raise ValueError("DCF intake payload must declare traceability.")
    _validate_expected_exact_value(
        traceability,
        field_name="downstream_output_role",
        expected_value=DCF_DOWNSTREAM_OUTPUT_ROLE,
        error_prefix="DCF traceability",
    )


def _validate_dcf_template_identity(template_identity: dict[str, object]) -> None:
    validate_template_identity(
        template_identity,
        allow_supporting_artifacts=False,
    )

    template_family = template_identity.get("template_family")
    if template_family != "dcf":
        raise ValueError(
            "DCF intake requires a governed DCF template identity: "
            f"expected template_family 'dcf', got {template_family!r}."
        )

    artifact_kind = template_identity.get("artifact_kind")
    if artifact_kind != GOVERNED_TEMPLATE_ARTIFACT_KIND:
        raise ValueError(
            "DCF intake requires a governed document template artifact."
        )


def _split_key_value_line(line: str, line_number: int) -> tuple[str, str]:
    for separator in (":", "="):
        if separator in line:
            key, value = line.split(separator, 1)
            return key, value

    raise ValueError(
        f"DCF line {line_number} is not a supported key/value line."
    )


def _normalize_field_name(field_name: str) -> str:
    return (
        field_name.strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def _build_missing_field_marker(field_name: str) -> dict[str, str]:
    return {
        "status": "missing",
        "field_name": field_name,
        "policy": MISSING_DCF_DATA_POLICY,
    }


def _is_missing_value(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _validate_content_format(content_format: str) -> None:
    if content_format not in SUPPORTED_DCF_CONTENT_FORMATS:
        raise ValueError(
            "Unsupported DCF content_format. "
            f"Expected one of: {', '.join(SUPPORTED_DCF_CONTENT_FORMATS)}."
        )


def _validate_required_payload_fields(payload: dict[str, object]) -> None:
    for field_name in _REQUIRED_DCF_INTAKE_FIELDS:
        if field_name not in payload:
            raise ValueError(
                f"DCF intake payload must declare {field_name}."
            )


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


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
