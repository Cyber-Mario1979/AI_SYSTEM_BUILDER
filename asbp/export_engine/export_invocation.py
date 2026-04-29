"""Export invocation and validation behavior for the M13.6 checkpoint."""

from __future__ import annotations

from typing import Any, Callable

from .dashboard_surfaces import validate_dashboard_status_export_payload
from .export_contracts import (
    CSV_OUTPUT_KIND,
    DASHBOARD_SNAPSHOT_OUTPUT_KIND,
    DASHBOARD_STATUS_EXPORT_FAMILY,
    EXCEL_READY_OUTPUT_KIND,
    EXPORT_OUTPUT_CONTRACT_VERSION,
    EXPORT_OUTPUT_TRUTH_BOUNDARY,
    GANTT_PLANNING_EXPORT_FAMILY,
    GANTT_TIMELINE_OUTPUT_KIND,
    GOVERNED_REPORT_EXPORT_FAMILY,
    MARKDOWN_REPORT_OUTPUT_KIND,
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
    RENDERED_EXPORT_OUTPUT_ROLE,
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    validate_export_request_payload,
)
from .gantt_surfaces import validate_gantt_planning_export_payload
from .reporting_surfaces import validate_reporting_export_payload
from .spreadsheet_surfaces import validate_spreadsheet_operational_export_payload

EXPORT_INVOCATION_CHECKPOINT_ID = "M13.6"
EXPORT_INVOCATION_CONTRACT_VERSION = "export-invocation-validation-v1"

CORE_EXPORT_SERVICE_BOUNDARY = "core_export_service_boundary"
RUNTIME_EXPORT_SERVICE_BOUNDARY = "runtime_export_service_boundary"

SUPPORTED_EXPORT_INVOCATION_BOUNDARIES = (
    CORE_EXPORT_SERVICE_BOUNDARY,
    RUNTIME_EXPORT_SERVICE_BOUNDARY,
)

STRICT_EXPORT_VALIDATION_MODE = "strict"
SUPPORTED_EXPORT_VALIDATION_MODES = (STRICT_EXPORT_VALIDATION_MODE,)

READY_FOR_RENDERER_INVOCATION_STATUS = "ready_for_renderer"
GENERATED_EXPORT_ARTIFACT_STATE = "generated"
ACCEPTED_EXPORT_ARTIFACT_DECISION = "accepted"
REJECTED_EXPORT_ARTIFACT_DECISION = "rejected"

SUPPORTED_EXPORT_ARTIFACT_ACCEPTANCE_DECISIONS = (
    ACCEPTED_EXPORT_ARTIFACT_DECISION,
    REJECTED_EXPORT_ARTIFACT_DECISION,
)

EXPORT_INVOCATION_RENDERING_BOUNDARY = (
    "export_invocation_validates_requests_and_outputs_but_does_not_render_files"
)
EXPORT_INVOCATION_FAILURE_POLICY = (
    "export_invocation_fails_closed_on_invalid_incomplete_or_ambiguous_inputs"
)
EXPORT_ARTIFACT_ACCEPTANCE_POLICY = (
    "generated_export_artifacts_are_accepted_only_against_the_export_request_output_contract"
)

CSV_EXPORT_ARTIFACT_KIND = "csv_artifact"
EXCEL_READY_EXPORT_ARTIFACT_KIND = "excel_ready_artifact"
MICROSOFT_PROJECT_DROP_READY_EXPORT_ARTIFACT_KIND = (
    "microsoft_project_drop_ready_artifact"
)
GANTT_TIMELINE_EXPORT_ARTIFACT_KIND = "gantt_timeline_artifact"
DASHBOARD_SNAPSHOT_EXPORT_ARTIFACT_KIND = "dashboard_snapshot_artifact"
MARKDOWN_REPORT_EXPORT_ARTIFACT_KIND = "markdown_report_artifact"
STRUCTURED_REPORT_PAYLOAD_EXPORT_ARTIFACT_KIND = "structured_report_payload_artifact"

_OUTPUT_KIND_ARTIFACT_KINDS: dict[str, tuple[str, ...]] = {
    CSV_OUTPUT_KIND: (CSV_EXPORT_ARTIFACT_KIND,),
    EXCEL_READY_OUTPUT_KIND: (EXCEL_READY_EXPORT_ARTIFACT_KIND,),
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND: (
        MICROSOFT_PROJECT_DROP_READY_EXPORT_ARTIFACT_KIND,
    ),
    GANTT_TIMELINE_OUTPUT_KIND: (GANTT_TIMELINE_EXPORT_ARTIFACT_KIND,),
    DASHBOARD_SNAPSHOT_OUTPUT_KIND: (DASHBOARD_SNAPSHOT_EXPORT_ARTIFACT_KIND,),
    MARKDOWN_REPORT_OUTPUT_KIND: (MARKDOWN_REPORT_EXPORT_ARTIFACT_KIND,),
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND: (
        STRUCTURED_REPORT_PAYLOAD_EXPORT_ARTIFACT_KIND,
    ),
}

SUPPORTED_RENDERED_EXPORT_ARTIFACT_KINDS = tuple(
    dict.fromkeys(
        artifact_kind
        for artifact_kinds in _OUTPUT_KIND_ARTIFACT_KINDS.values()
        for artifact_kind in artifact_kinds
    )
)

_PROHIBITED_INVOCATION_FIELDS = (
    "raw_freeform_prompt",
    "execution_truth_override",
    "source_truth_override",
    "task_state_override",
    "document_lifecycle_override",
    "approved_state_override",
    "resolver_bypass",
    "renderer_bypass",
)

_PROHIBITED_RENDERED_ARTIFACT_FIELDS = (
    *_PROHIBITED_INVOCATION_FIELDS,
    "file_content",
    "markdown_file_content",
    "docx_content",
    "pdf_content",
    "workbook_binary",
    "chart_image_content",
    "ui_rendered_content",
)

_REQUIRED_INVOCATION_FIELDS = (
    "checkpoint",
    "contract_version",
    "invocation_id",
    "invocation_boundary",
    "requested_by",
    "validation_mode",
    "export_request",
    "validation_result",
    "failure_behavior",
    "renderer_boundary",
    "invocation_status",
)

_REQUIRED_RENDERED_OUTPUT_FIELDS = (
    "artifact_id",
    "artifact_kind",
    "artifact_version",
    "artifact_ref",
    "artifact_role",
    "rendering_boundary",
)

_REQUIRED_GENERATED_ARTIFACT_FIELDS = (
    "checkpoint",
    "contract_version",
    "export_job_id",
    "export_family",
    "export_id",
    "export_version",
    "requested_output_kind",
    "source_context",
    "input_snapshot",
    "rendered_export_output",
    "output_metadata",
    "output_contract_version",
    "output_truth_boundary",
    "acceptance_state",
)

_REQUIRED_ACCEPTANCE_FIELDS = (
    "checkpoint",
    "contract_version",
    "acceptance_id",
    "accepted_by",
    "acceptance_decision",
    "invocation_id",
    "export_job_id",
    "export_family",
    "export_id",
    "export_version",
    "requested_output_kind",
    "artifact_ref",
    "acceptance_policy",
    "output_truth_boundary",
)


def build_export_invocation_baseline() -> dict[str, Any]:
    """Return the explicit M13.6 export invocation/validation baseline."""

    return {
        "checkpoint": EXPORT_INVOCATION_CHECKPOINT_ID,
        "contract_version": EXPORT_INVOCATION_CONTRACT_VERSION,
        "supported_invocation_boundaries": list(
            SUPPORTED_EXPORT_INVOCATION_BOUNDARIES
        ),
        "supported_validation_modes": list(SUPPORTED_EXPORT_VALIDATION_MODES),
        "supported_artifact_kinds": list(SUPPORTED_RENDERED_EXPORT_ARTIFACT_KINDS),
        "supported_acceptance_decisions": list(
            SUPPORTED_EXPORT_ARTIFACT_ACCEPTANCE_DECISIONS
        ),
        "failure_policy": EXPORT_INVOCATION_FAILURE_POLICY,
        "artifact_acceptance_policy": EXPORT_ARTIFACT_ACCEPTANCE_POLICY,
        "renderer_boundary": EXPORT_INVOCATION_RENDERING_BOUNDARY,
        "required_invocation_fields": list(_REQUIRED_INVOCATION_FIELDS),
        "required_generated_artifact_fields": list(
            _REQUIRED_GENERATED_ARTIFACT_FIELDS
        ),
        "required_acceptance_fields": list(_REQUIRED_ACCEPTANCE_FIELDS),
        "boundary_policy": (
            "m13_6_invokes_and_validates_export_contracts_without_rendering_files_or_delivery_surfaces"
        ),
    }


def build_export_invocation_request(
    *,
    invocation_id: str,
    invocation_boundary: str,
    requested_by: str,
    export_request: dict[str, object],
    validation_mode: str = STRICT_EXPORT_VALIDATION_MODE,
) -> dict[str, Any]:
    """Build a governed export invocation request.

    M13.6 invocation intentionally stays inside approved service/runtime
    boundaries. It validates the M13.1 export request plus the family-specific
    M13.2-M13.5 payload contract, then marks the request ready for a downstream
    renderer without rendering files itself.
    """

    invocation = {
        "checkpoint": EXPORT_INVOCATION_CHECKPOINT_ID,
        "contract_version": EXPORT_INVOCATION_CONTRACT_VERSION,
        "invocation_id": invocation_id,
        "invocation_boundary": invocation_boundary,
        "requested_by": requested_by,
        "validation_mode": validation_mode,
        "export_request": export_request,
        "validation_result": {
            "request_contract_validated": True,
            "family_payload_validated": True,
            "incomplete_input_policy": "reject_before_renderer_invocation",
        },
        "failure_behavior": {
            "policy": EXPORT_INVOCATION_FAILURE_POLICY,
            "blocked_conditions": [
                "invalid_export_request_contract",
                "invalid_family_payload_contract",
                "unsupported_invocation_boundary",
                "unsupported_validation_mode",
                "incomplete_input_payload",
                "ambiguous_or_mismatched_generated_artifact",
            ],
        },
        "renderer_boundary": EXPORT_INVOCATION_RENDERING_BOUNDARY,
        "invocation_status": READY_FOR_RENDERER_INVOCATION_STATUS,
    }
    validate_export_invocation_request(invocation)
    return invocation


def validate_export_invocation_request(invocation: dict[str, object]) -> None:
    """Validate a governed export invocation request."""

    _validate_prohibited_fields(invocation, _PROHIBITED_INVOCATION_FIELDS)
    _validate_required_string_fields(
        invocation,
        (
            "checkpoint",
            "contract_version",
            "invocation_id",
            "invocation_boundary",
            "requested_by",
            "validation_mode",
            "renderer_boundary",
            "invocation_status",
        ),
        error_prefix="Export invocation request",
    )

    for field_name in _REQUIRED_INVOCATION_FIELDS:
        if field_name not in invocation:
            raise ValueError(f"Export invocation request must declare {field_name}.")

    _validate_expected_exact_value(
        invocation,
        field_name="checkpoint",
        expected_value=EXPORT_INVOCATION_CHECKPOINT_ID,
        error_prefix="Export invocation request",
    )
    _validate_expected_exact_value(
        invocation,
        field_name="contract_version",
        expected_value=EXPORT_INVOCATION_CONTRACT_VERSION,
        error_prefix="Export invocation request",
    )

    invocation_boundary = str(invocation["invocation_boundary"])
    _validate_supported_invocation_boundary(invocation_boundary)

    validation_mode = str(invocation["validation_mode"])
    _validate_supported_validation_mode(validation_mode)

    if invocation["renderer_boundary"] != EXPORT_INVOCATION_RENDERING_BOUNDARY:
        raise ValueError("Export invocation request declares an invalid renderer boundary.")

    if invocation["invocation_status"] != READY_FOR_RENDERER_INVOCATION_STATUS:
        raise ValueError(
            "Export invocation request must use ready_for_renderer invocation_status."
        )

    export_request = invocation.get("export_request")
    if not isinstance(export_request, dict):
        raise ValueError("Export invocation request must declare export_request as a mapping.")

    validate_export_request_payload(export_request)
    validate_export_input_payload_for_invocation(export_request)

    validation_result = invocation.get("validation_result")
    if not isinstance(validation_result, dict):
        raise ValueError(
            "Export invocation request must declare validation_result as a mapping."
        )
    if validation_result.get("request_contract_validated") is not True:
        raise ValueError("Export invocation validation_result must confirm request validation.")
    if validation_result.get("family_payload_validated") is not True:
        raise ValueError(
            "Export invocation validation_result must confirm family payload validation."
        )

    failure_behavior = invocation.get("failure_behavior")
    if not isinstance(failure_behavior, dict):
        raise ValueError(
            "Export invocation request must declare failure_behavior as a mapping."
        )
    if failure_behavior.get("policy") != EXPORT_INVOCATION_FAILURE_POLICY:
        raise ValueError("Export invocation request declares an invalid failure policy.")


def validate_export_input_payload_for_invocation(
    export_request: dict[str, object],
) -> None:
    """Validate the family-specific export input payload for M13.6 invocation."""

    validate_export_request_payload(export_request)

    export_family = str(export_request["export_family"])
    requested_output_kind = str(export_request["requested_output_kind"])
    input_payload = export_request.get("input_payload")
    if not isinstance(input_payload, dict):
        raise ValueError("Export request input_payload must be a mapping.")

    validator = _family_payload_validator(export_family)
    if export_family == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY:
        validator(input_payload, requested_output_kind=requested_output_kind)
    else:
        validator(input_payload)


def build_generated_export_artifact(
    *,
    export_request: dict[str, object],
    artifact_id: str,
    artifact_kind: str,
    artifact_version: str,
    artifact_ref: str,
    output_metadata: dict[str, object] | None = None,
) -> dict[str, Any]:
    """Build generated export artifact metadata for acceptance validation.

    This does not render or store a file. It records the downstream artifact
    reference and validates that the artifact metadata matches the source export
    request and its output contract.
    """

    validate_export_request_payload(export_request)
    validate_export_input_payload_for_invocation(export_request)

    rendered_export_output = {
        "artifact_id": artifact_id,
        "artifact_kind": artifact_kind,
        "artifact_version": artifact_version,
        "artifact_ref": artifact_ref,
        "artifact_role": RENDERED_EXPORT_OUTPUT_ROLE,
        "rendering_boundary": EXPORT_INVOCATION_RENDERING_BOUNDARY,
    }

    artifact = {
        "checkpoint": EXPORT_INVOCATION_CHECKPOINT_ID,
        "contract_version": EXPORT_INVOCATION_CONTRACT_VERSION,
        "export_job_id": export_request["export_job_id"],
        "export_family": export_request["export_family"],
        "export_id": export_request["export_id"],
        "export_version": export_request["export_version"],
        "requested_output_kind": export_request["requested_output_kind"],
        "source_context": dict(export_request["source_context"]),  # type: ignore[arg-type]
        "input_snapshot": dict(export_request["input_payload"]),  # type: ignore[arg-type]
        "rendered_export_output": rendered_export_output,
        "output_metadata": dict(output_metadata or {}),
        "output_contract_version": EXPORT_OUTPUT_CONTRACT_VERSION,
        "output_truth_boundary": EXPORT_OUTPUT_TRUTH_BOUNDARY,
        "acceptance_state": GENERATED_EXPORT_ARTIFACT_STATE,
    }
    validate_generated_export_artifact(export_request, artifact)
    return artifact


def validate_generated_export_artifact(
    export_request: dict[str, object],
    artifact: dict[str, object],
) -> None:
    """Validate generated export artifact metadata against an export request."""

    validate_export_request_payload(export_request)
    validate_export_input_payload_for_invocation(export_request)

    _validate_prohibited_fields(artifact, _PROHIBITED_RENDERED_ARTIFACT_FIELDS)
    for field_name in _REQUIRED_GENERATED_ARTIFACT_FIELDS:
        if field_name not in artifact:
            raise ValueError(f"Generated export artifact must declare {field_name}.")

    _validate_required_string_fields(
        artifact,
        (
            "checkpoint",
            "contract_version",
            "export_job_id",
            "export_family",
            "export_id",
            "export_version",
            "requested_output_kind",
            "output_contract_version",
            "output_truth_boundary",
            "acceptance_state",
        ),
        error_prefix="Generated export artifact",
    )
    _validate_expected_exact_value(
        artifact,
        field_name="checkpoint",
        expected_value=EXPORT_INVOCATION_CHECKPOINT_ID,
        error_prefix="Generated export artifact",
    )
    _validate_expected_exact_value(
        artifact,
        field_name="contract_version",
        expected_value=EXPORT_INVOCATION_CONTRACT_VERSION,
        error_prefix="Generated export artifact",
    )
    _validate_expected_exact_value(
        artifact,
        field_name="output_contract_version",
        expected_value=EXPORT_OUTPUT_CONTRACT_VERSION,
        error_prefix="Generated export artifact",
    )
    _validate_expected_exact_value(
        artifact,
        field_name="output_truth_boundary",
        expected_value=EXPORT_OUTPUT_TRUTH_BOUNDARY,
        error_prefix="Generated export artifact",
    )
    _validate_expected_exact_value(
        artifact,
        field_name="acceptance_state",
        expected_value=GENERATED_EXPORT_ARTIFACT_STATE,
        error_prefix="Generated export artifact",
    )

    _validate_artifact_identity_matches_request(export_request, artifact)

    source_context = artifact.get("source_context")
    if not isinstance(source_context, dict):
        raise ValueError("Generated export artifact must declare source_context as a mapping.")
    if source_context != export_request["source_context"]:
        raise ValueError("Generated export artifact source_context does not match request.")

    input_snapshot = artifact.get("input_snapshot")
    if not isinstance(input_snapshot, dict):
        raise ValueError("Generated export artifact must declare input_snapshot as a mapping.")
    if input_snapshot != export_request["input_payload"]:
        raise ValueError("Generated export artifact input_snapshot does not match request.")

    rendered_output = artifact.get("rendered_export_output")
    if not isinstance(rendered_output, dict):
        raise ValueError(
            "Generated export artifact must declare rendered_export_output as a mapping."
        )
    validate_rendered_export_output_metadata(
        rendered_output,
        requested_output_kind=str(export_request["requested_output_kind"]),
    )

    output_metadata = artifact.get("output_metadata")
    if not isinstance(output_metadata, dict):
        raise ValueError("Generated export artifact must declare output_metadata as a mapping.")
    _validate_prohibited_fields(output_metadata, _PROHIBITED_RENDERED_ARTIFACT_FIELDS)


def validate_rendered_export_output_metadata(
    rendered_output: dict[str, object],
    *,
    requested_output_kind: str,
) -> None:
    """Validate one rendered-output metadata object without inspecting file content."""

    _validate_prohibited_fields(rendered_output, _PROHIBITED_RENDERED_ARTIFACT_FIELDS)
    _validate_required_string_fields(
        rendered_output,
        _REQUIRED_RENDERED_OUTPUT_FIELDS,
        error_prefix="Rendered export output metadata",
    )

    artifact_kind = str(rendered_output["artifact_kind"])
    _validate_artifact_kind_for_output_kind(
        requested_output_kind=requested_output_kind,
        artifact_kind=artifact_kind,
    )

    if rendered_output["artifact_role"] != RENDERED_EXPORT_OUTPUT_ROLE:
        raise ValueError("Rendered export output metadata declares an invalid artifact_role.")
    if rendered_output["rendering_boundary"] != EXPORT_INVOCATION_RENDERING_BOUNDARY:
        raise ValueError(
            "Rendered export output metadata declares an invalid rendering boundary."
        )


def build_export_artifact_acceptance_record(
    *,
    invocation_request: dict[str, object],
    generated_export_artifact: dict[str, object],
    acceptance_id: str,
    accepted_by: str,
    acceptance_decision: str = ACCEPTED_EXPORT_ARTIFACT_DECISION,
    rejection_reason: str | None = None,
) -> dict[str, Any]:
    """Build deterministic acceptance evidence for a generated export artifact."""

    validate_export_invocation_request(invocation_request)
    export_request = invocation_request["export_request"]
    assert isinstance(export_request, dict)
    validate_generated_export_artifact(export_request, generated_export_artifact)

    rendered_output = generated_export_artifact["rendered_export_output"]
    assert isinstance(rendered_output, dict)

    acceptance_record = {
        "checkpoint": EXPORT_INVOCATION_CHECKPOINT_ID,
        "contract_version": EXPORT_INVOCATION_CONTRACT_VERSION,
        "acceptance_id": acceptance_id,
        "accepted_by": accepted_by,
        "acceptance_decision": acceptance_decision,
        "rejection_reason": rejection_reason,
        "invocation_id": invocation_request["invocation_id"],
        "export_job_id": generated_export_artifact["export_job_id"],
        "export_family": generated_export_artifact["export_family"],
        "export_id": generated_export_artifact["export_id"],
        "export_version": generated_export_artifact["export_version"],
        "requested_output_kind": generated_export_artifact["requested_output_kind"],
        "artifact_ref": rendered_output["artifact_ref"],
        "acceptance_policy": EXPORT_ARTIFACT_ACCEPTANCE_POLICY,
        "acceptance_rules": [
            "export_identity_must_match_invocation_request",
            "source_context_must_match_invocation_request",
            "input_snapshot_must_match_invocation_request",
            "requested_output_kind_must_match_artifact_kind",
            "output_contract_version_must_match_export_output_contract",
            "rendered_output_must_remain_downstream_artifact_reference_only",
        ],
        "output_truth_boundary": EXPORT_OUTPUT_TRUTH_BOUNDARY,
    }
    validate_export_artifact_acceptance_record(
        invocation_request=invocation_request,
        generated_export_artifact=generated_export_artifact,
        acceptance_record=acceptance_record,
    )
    return acceptance_record


def validate_export_artifact_acceptance_record(
    *,
    invocation_request: dict[str, object],
    generated_export_artifact: dict[str, object],
    acceptance_record: dict[str, object],
) -> None:
    """Validate deterministic acceptance evidence for a generated artifact."""

    validate_export_invocation_request(invocation_request)
    export_request = invocation_request["export_request"]
    assert isinstance(export_request, dict)
    validate_generated_export_artifact(export_request, generated_export_artifact)

    _validate_prohibited_fields(acceptance_record, _PROHIBITED_INVOCATION_FIELDS)
    for field_name in _REQUIRED_ACCEPTANCE_FIELDS:
        if field_name not in acceptance_record:
            raise ValueError(f"Export artifact acceptance record must declare {field_name}.")

    _validate_required_string_fields(
        acceptance_record,
        (
            "checkpoint",
            "contract_version",
            "acceptance_id",
            "accepted_by",
            "acceptance_decision",
            "invocation_id",
            "export_job_id",
            "export_family",
            "export_id",
            "export_version",
            "requested_output_kind",
            "artifact_ref",
            "acceptance_policy",
            "output_truth_boundary",
        ),
        error_prefix="Export artifact acceptance record",
    )
    _validate_expected_exact_value(
        acceptance_record,
        field_name="checkpoint",
        expected_value=EXPORT_INVOCATION_CHECKPOINT_ID,
        error_prefix="Export artifact acceptance record",
    )
    _validate_expected_exact_value(
        acceptance_record,
        field_name="contract_version",
        expected_value=EXPORT_INVOCATION_CONTRACT_VERSION,
        error_prefix="Export artifact acceptance record",
    )
    _validate_expected_exact_value(
        acceptance_record,
        field_name="acceptance_policy",
        expected_value=EXPORT_ARTIFACT_ACCEPTANCE_POLICY,
        error_prefix="Export artifact acceptance record",
    )
    _validate_expected_exact_value(
        acceptance_record,
        field_name="output_truth_boundary",
        expected_value=EXPORT_OUTPUT_TRUTH_BOUNDARY,
        error_prefix="Export artifact acceptance record",
    )

    decision = str(acceptance_record["acceptance_decision"])
    _validate_supported_acceptance_decision(decision)
    rejection_reason = acceptance_record.get("rejection_reason")
    if decision == ACCEPTED_EXPORT_ARTIFACT_DECISION and rejection_reason:
        raise ValueError("Accepted export artifacts must not declare rejection_reason.")
    if decision == REJECTED_EXPORT_ARTIFACT_DECISION:
        if not isinstance(rejection_reason, str) or not rejection_reason.strip():
            raise ValueError("Rejected export artifacts must declare rejection_reason.")

    if acceptance_record["invocation_id"] != invocation_request["invocation_id"]:
        raise ValueError("Export artifact acceptance record invocation_id mismatch.")

    _validate_artifact_identity_matches_request(
        export_request,
        acceptance_record,
        error_prefix="Export artifact acceptance record",
    )

    rendered_output = generated_export_artifact["rendered_export_output"]
    assert isinstance(rendered_output, dict)
    if acceptance_record["artifact_ref"] != rendered_output["artifact_ref"]:
        raise ValueError("Export artifact acceptance record artifact_ref mismatch.")


def _family_payload_validator(export_family: str) -> Callable[..., None]:
    if export_family == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY:
        return validate_spreadsheet_operational_export_payload
    if export_family == GANTT_PLANNING_EXPORT_FAMILY:
        return validate_gantt_planning_export_payload
    if export_family == DASHBOARD_STATUS_EXPORT_FAMILY:
        return validate_dashboard_status_export_payload
    if export_family == GOVERNED_REPORT_EXPORT_FAMILY:
        return validate_reporting_export_payload
    raise ValueError(f"Unsupported export_family for invocation: {export_family!r}.")


def _validate_artifact_identity_matches_request(
    export_request: dict[str, object],
    artifact_like: dict[str, object],
    *,
    error_prefix: str = "Generated export artifact",
) -> None:
    for field_name in (
        "export_job_id",
        "export_family",
        "export_id",
        "export_version",
        "requested_output_kind",
    ):
        if artifact_like.get(field_name) != export_request.get(field_name):
            raise ValueError(f"{error_prefix} {field_name} does not match request.")


def _validate_supported_invocation_boundary(invocation_boundary: str) -> None:
    if invocation_boundary not in SUPPORTED_EXPORT_INVOCATION_BOUNDARIES:
        raise ValueError(
            "Unsupported export invocation boundary. "
            f"Expected one of: {', '.join(SUPPORTED_EXPORT_INVOCATION_BOUNDARIES)}."
        )


def _validate_supported_validation_mode(validation_mode: str) -> None:
    if validation_mode not in SUPPORTED_EXPORT_VALIDATION_MODES:
        raise ValueError(
            "Unsupported export validation mode. "
            f"Expected one of: {', '.join(SUPPORTED_EXPORT_VALIDATION_MODES)}."
        )


def _validate_artifact_kind_for_output_kind(
    *,
    requested_output_kind: str,
    artifact_kind: str,
) -> None:
    allowed_kinds = _OUTPUT_KIND_ARTIFACT_KINDS.get(requested_output_kind)
    if allowed_kinds is None:
        raise ValueError(f"Unsupported output kind for artifact acceptance: {requested_output_kind!r}.")
    if artifact_kind not in allowed_kinds:
        raise ValueError(
            "Unsupported rendered export artifact kind for requested_output_kind "
            f"{requested_output_kind!r}. Expected one of: {', '.join(allowed_kinds)}."
        )


def _validate_supported_acceptance_decision(acceptance_decision: str) -> None:
    if acceptance_decision not in SUPPORTED_EXPORT_ARTIFACT_ACCEPTANCE_DECISIONS:
        raise ValueError(
            "Unsupported export artifact acceptance_decision. "
            f"Expected one of: {', '.join(SUPPORTED_EXPORT_ARTIFACT_ACCEPTANCE_DECISIONS)}."
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
            raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")


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
            raise ValueError(f"{field_name} is not allowed in export invocation records.")
