"""Export identity and contract foundations for the M13.1 checkpoint."""

from __future__ import annotations

from typing import Any

EXPORT_CONTRACT_CHECKPOINT_ID = "M13.1"

EXPORT_REQUEST_CONTRACT_VERSION = "export-request-contract-v1"
EXPORT_PAYLOAD_CONTRACT_VERSION = "export-payload-contract-v1"
EXPORT_OUTPUT_CONTRACT_VERSION = "export-output-contract-v1"

SOURCE_CONTEXT_SOURCE_ROLE = "execution_or_governed_source_truth_reference_only"
EXPORT_PAYLOAD_ROLE = "structured_export_input_only"
RENDERED_EXPORT_OUTPUT_ROLE = "downstream_rendered_artifact_only"
EXPORT_OUTPUT_TRUTH_BOUNDARY = (
    "export_output_may_not_replace_execution_planning_document_or_governed_source_truth"
)

SPREADSHEET_OPERATIONAL_EXPORT_FAMILY = "spreadsheet_operational"
GANTT_PLANNING_EXPORT_FAMILY = "gantt_planning"
DASHBOARD_STATUS_EXPORT_FAMILY = "dashboard_status"
GOVERNED_REPORT_EXPORT_FAMILY = "governed_report"

SUPPORTED_EXPORT_FAMILIES = (
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    GANTT_PLANNING_EXPORT_FAMILY,
    DASHBOARD_STATUS_EXPORT_FAMILY,
    GOVERNED_REPORT_EXPORT_FAMILY,
)

CSV_OUTPUT_KIND = "csv"
EXCEL_READY_OUTPUT_KIND = "excel_ready"
MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND = "microsoft_project_drop_ready"
GANTT_TIMELINE_OUTPUT_KIND = "gantt_timeline"
DASHBOARD_SNAPSHOT_OUTPUT_KIND = "dashboard_snapshot"
MARKDOWN_REPORT_OUTPUT_KIND = "markdown_report"
STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND = "structured_report_payload"

_EXPORT_FAMILY_OUTPUT_KINDS: dict[str, tuple[str, ...]] = {
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY: (
        CSV_OUTPUT_KIND,
        EXCEL_READY_OUTPUT_KIND,
        MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
    ),
    GANTT_PLANNING_EXPORT_FAMILY: (
        GANTT_TIMELINE_OUTPUT_KIND,
        CSV_OUTPUT_KIND,
    ),
    DASHBOARD_STATUS_EXPORT_FAMILY: (
        DASHBOARD_SNAPSHOT_OUTPUT_KIND,
        STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    ),
    GOVERNED_REPORT_EXPORT_FAMILY: (
        MARKDOWN_REPORT_OUTPUT_KIND,
        STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    ),
}

SUPPORTED_EXPORT_OUTPUT_KINDS = tuple(
    dict.fromkeys(
        output_kind
        for output_kinds in _EXPORT_FAMILY_OUTPUT_KINDS.values()
        for output_kind in output_kinds
    )
)

SUPPORTED_EXPORT_SOURCE_CONTEXT_KINDS = (
    "work_package",
    "task_collection",
    "plan",
    "document_artifact",
    "standalone_governed_export_request",
)

_EXPORT_IDENTITY_REQUIRED_FIELDS = (
    "export_job_id",
    "export_family",
    "export_id",
    "export_version",
    "requested_output_kind",
)

_REQUIRED_EXPORT_REQUEST_FIELDS = (
    "checkpoint",
    "contract_version",
    "export_job_id",
    "export_family",
    "export_id",
    "export_version",
    "requested_output_kind",
    "source_context",
    "input_payload",
    "payload_contract",
    "output_contract",
    "truth_separation",
)

_REQUIRED_SOURCE_CONTEXT_FIELDS = (
    "kind",
    "ref",
    "source_role",
)

_EXPORT_FAMILY_REQUIRED_PAYLOAD_FIELDS: dict[str, tuple[str, ...]] = {
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY: (
        "columns",
        "rows",
        "row_granularity",
    ),
    GANTT_PLANNING_EXPORT_FAMILY: (
        "planning_items",
        "dependency_refs",
        "timeline_basis",
    ),
    DASHBOARD_STATUS_EXPORT_FAMILY: (
        "status_items",
        "summary_metrics",
        "snapshot_basis",
    ),
    GOVERNED_REPORT_EXPORT_FAMILY: (
        "report_sections",
        "evidence_refs",
        "summary_basis",
    ),
}

_PROHIBITED_INPUT_PAYLOAD_FIELDS = (
    "raw_freeform_prompt",
    "execution_truth_override",
    "resolver_bypass",
    "rendered_file_content",
    "approved_state_override",
)

_OUTPUT_CONTRACT_FIELDS = (
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
)


def build_export_contract_baseline() -> dict[str, Any]:
    """Return the explicit M13.1 export identity/request/payload/output baseline."""

    return {
        "checkpoint": EXPORT_CONTRACT_CHECKPOINT_ID,
        "request_contract_version": EXPORT_REQUEST_CONTRACT_VERSION,
        "payload_contract_version": EXPORT_PAYLOAD_CONTRACT_VERSION,
        "output_contract_version": EXPORT_OUTPUT_CONTRACT_VERSION,
        "supported_export_families": list(SUPPORTED_EXPORT_FAMILIES),
        "supported_output_kinds": list(SUPPORTED_EXPORT_OUTPUT_KINDS),
        "family_output_kinds": {
            export_family: list(output_kinds)
            for export_family, output_kinds in _EXPORT_FAMILY_OUTPUT_KINDS.items()
        },
        "supported_source_context_kinds": list(
            SUPPORTED_EXPORT_SOURCE_CONTEXT_KINDS
        ),
        "identity_required_fields": list(_EXPORT_IDENTITY_REQUIRED_FIELDS),
        "request_required_fields": list(_REQUIRED_EXPORT_REQUEST_FIELDS),
        "family_required_payload_fields": {
            export_family: list(fields)
            for export_family, fields in _EXPORT_FAMILY_REQUIRED_PAYLOAD_FIELDS.items()
        },
        "truth_separation": {
            "source_context": SOURCE_CONTEXT_SOURCE_ROLE,
            "input_payload": EXPORT_PAYLOAD_ROLE,
            "rendered_export_output": RENDERED_EXPORT_OUTPUT_ROLE,
        },
        "prohibited_input_payload_fields": list(
            _PROHIBITED_INPUT_PAYLOAD_FIELDS
        ),
        "output_contract_fields": list(_OUTPUT_CONTRACT_FIELDS),
        "boundary_policy": (
            "export_families_are_core_engine_output_contracts_not_ui_api_delivery"
        ),
    }


def build_export_payload_contract(export_family: str) -> dict[str, Any]:
    """Build the structured payload contract for one governed export family."""

    _validate_supported_export_family(export_family)

    return {
        "checkpoint": EXPORT_CONTRACT_CHECKPOINT_ID,
        "contract_version": EXPORT_PAYLOAD_CONTRACT_VERSION,
        "export_family": export_family,
        "required_payload_fields": list(
            _EXPORT_FAMILY_REQUIRED_PAYLOAD_FIELDS[export_family]
        ),
        "prohibited_input_payload_fields": list(
            _PROHIBITED_INPUT_PAYLOAD_FIELDS
        ),
        "payload_truth_boundary": EXPORT_PAYLOAD_ROLE,
    }


def build_export_output_contract(
    *,
    export_family: str,
    requested_output_kind: str,
) -> dict[str, Any]:
    """Build the downstream output contract for one governed export family."""

    _validate_supported_export_family(export_family)
    _validate_output_kind_for_family(export_family, requested_output_kind)

    return {
        "checkpoint": EXPORT_CONTRACT_CHECKPOINT_ID,
        "contract_version": EXPORT_OUTPUT_CONTRACT_VERSION,
        "export_family": export_family,
        "requested_output_kind": requested_output_kind,
        "required_output_fields": list(_OUTPUT_CONTRACT_FIELDS),
        "rendered_output_role": RENDERED_EXPORT_OUTPUT_ROLE,
        "output_truth_boundary": EXPORT_OUTPUT_TRUTH_BOUNDARY,
        "delivery_surface_boundary": (
            "output_contract_defines_artifact_shape_not_ui_or_api_delivery"
        ),
    }


def build_export_request_payload(
    *,
    export_job_id: str,
    export_family: str,
    export_id: str,
    export_version: str,
    requested_output_kind: str,
    source_context_kind: str,
    source_context_ref: str,
    input_payload: dict[str, object],
) -> dict[str, Any]:
    """Build a governed export request payload.

    The M13.1 contract is intentionally structural:
    - it binds export identity and version expectations
    - it binds a source context by reference only
    - it validates family-specific payload requirements
    - it keeps rendered export output downstream from execution/data truth
    - it stays separate from later UI/API delivery surfaces
    """

    request: dict[str, Any] = {
        "checkpoint": EXPORT_CONTRACT_CHECKPOINT_ID,
        "contract_version": EXPORT_REQUEST_CONTRACT_VERSION,
        "export_job_id": export_job_id,
        "export_family": export_family,
        "export_id": export_id,
        "export_version": export_version,
        "requested_output_kind": requested_output_kind,
        "source_context": {
            "kind": source_context_kind,
            "ref": source_context_ref,
            "source_role": SOURCE_CONTEXT_SOURCE_ROLE,
        },
        "input_payload": input_payload,
        "payload_contract": build_export_payload_contract(export_family),
        "output_contract": build_export_output_contract(
            export_family=export_family,
            requested_output_kind=requested_output_kind,
        ),
        "truth_separation": {
            "source_context": SOURCE_CONTEXT_SOURCE_ROLE,
            "input_payload": EXPORT_PAYLOAD_ROLE,
            "rendered_export_output": RENDERED_EXPORT_OUTPUT_ROLE,
        },
    }
    validate_export_request_payload(request)
    return request


def validate_export_request_payload(request: dict[str, object]) -> None:
    """Validate a governed export request payload."""

    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "export_job_id",
            "export_family",
            "export_id",
            "export_version",
            "requested_output_kind",
        ),
        error_prefix="Export request payload",
    )
    _validate_required_mapping_fields(
        request,
        (
            "source_context",
            "input_payload",
            "payload_contract",
            "output_contract",
            "truth_separation",
        ),
        error_prefix="Export request payload",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=EXPORT_CONTRACT_CHECKPOINT_ID,
        error_prefix="Export request payload",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=EXPORT_REQUEST_CONTRACT_VERSION,
        error_prefix="Export request payload",
    )

    export_family = str(request["export_family"])
    requested_output_kind = str(request["requested_output_kind"])

    _validate_supported_export_family(export_family)
    _validate_output_kind_for_family(export_family, requested_output_kind)

    source_context = request["source_context"]
    assert isinstance(source_context, dict)
    _validate_source_context(source_context)

    input_payload = request["input_payload"]
    assert isinstance(input_payload, dict)
    _validate_input_payload_for_family(export_family, input_payload)
    _validate_prohibited_payload_fields(
        input_payload,
        _PROHIBITED_INPUT_PAYLOAD_FIELDS,
    )

    payload_contract = request["payload_contract"]
    assert isinstance(payload_contract, dict)
    _validate_expected_exact_value(
        payload_contract,
        field_name="checkpoint",
        expected_value=EXPORT_CONTRACT_CHECKPOINT_ID,
        error_prefix="Export payload contract",
    )
    _validate_expected_exact_value(
        payload_contract,
        field_name="contract_version",
        expected_value=EXPORT_PAYLOAD_CONTRACT_VERSION,
        error_prefix="Export payload contract",
    )

    output_contract = request["output_contract"]
    assert isinstance(output_contract, dict)
    _validate_expected_exact_value(
        output_contract,
        field_name="checkpoint",
        expected_value=EXPORT_CONTRACT_CHECKPOINT_ID,
        error_prefix="Export output contract",
    )
    _validate_expected_exact_value(
        output_contract,
        field_name="contract_version",
        expected_value=EXPORT_OUTPUT_CONTRACT_VERSION,
        error_prefix="Export output contract",
    )


def _validate_supported_export_family(export_family: str) -> None:
    if export_family not in SUPPORTED_EXPORT_FAMILIES:
        raise ValueError(
            "Unsupported export_family. "
            f"Expected one of: {', '.join(SUPPORTED_EXPORT_FAMILIES)}."
        )


def _validate_output_kind_for_family(
    export_family: str,
    requested_output_kind: str,
) -> None:
    allowed_output_kinds = _EXPORT_FAMILY_OUTPUT_KINDS[export_family]
    if requested_output_kind not in allowed_output_kinds:
        raise ValueError(
            "Unsupported requested_output_kind for export_family "
            f"{export_family!r}. Expected one of: "
            f"{', '.join(allowed_output_kinds)}."
        )


def _validate_source_context(source_context: dict[str, object]) -> None:
    _validate_required_string_fields(
        source_context,
        _REQUIRED_SOURCE_CONTEXT_FIELDS,
        error_prefix="Source context",
    )

    kind = source_context.get("kind")
    if kind not in SUPPORTED_EXPORT_SOURCE_CONTEXT_KINDS:
        raise ValueError(
            "Unsupported source context kind. "
            f"Expected one of: {', '.join(SUPPORTED_EXPORT_SOURCE_CONTEXT_KINDS)}."
        )

    source_role = source_context.get("source_role")
    if source_role != SOURCE_CONTEXT_SOURCE_ROLE:
        raise ValueError(
            "Source context declares an invalid source_role: "
            f"expected {SOURCE_CONTEXT_SOURCE_ROLE!r}, got {source_role!r}."
        )


def _validate_input_payload_for_family(
    export_family: str,
    input_payload: dict[str, object],
) -> None:
    required_fields = _EXPORT_FAMILY_REQUIRED_PAYLOAD_FIELDS[export_family]

    for field_name in required_fields:
        value = input_payload.get(field_name)
        if value is None:
            raise ValueError(
                f"Export input_payload must declare required {field_name} "
                f"for {export_family!r} exports."
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


def _validate_prohibited_payload_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in export input_payload."
            )
