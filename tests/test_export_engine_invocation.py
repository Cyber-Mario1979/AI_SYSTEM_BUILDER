import pytest

from asbp.export_engine import (
    ACCEPTED_EXPORT_ARTIFACT_DECISION,
    CORE_EXPORT_SERVICE_BOUNDARY,
    EXCEL_READY_EXPORT_ARTIFACT_KIND,
    EXCEL_READY_OUTPUT_KIND,
    EXPORT_INVOCATION_CHECKPOINT_ID,
    EXPORT_INVOCATION_CONTRACT_VERSION,
    EXPORT_INVOCATION_FAILURE_POLICY,
    EXPORT_INVOCATION_RENDERING_BOUNDARY,
    READY_FOR_RENDERER_INVOCATION_STATUS,
    REJECTED_EXPORT_ARTIFACT_DECISION,
    SOURCE_VALUE_POLICY,
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    STRICT_EXPORT_VALIDATION_MODE,
    TASK_ROW_GRANULARITY,
    build_export_artifact_acceptance_record,
    build_export_invocation_baseline,
    build_export_invocation_request,
    build_export_request_payload,
    build_generated_export_artifact,
    build_spreadsheet_column_contract,
    build_spreadsheet_operational_export_request,
    validate_export_artifact_acceptance_record,
    validate_export_input_payload_for_invocation,
    validate_export_invocation_request,
    validate_generated_export_artifact,
)


def _columns() -> list[dict[str, object]]:
    return [
        build_spreadsheet_column_contract(
            column_key="task_id",
            header="Task ID",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="task_id",
        ),
        build_spreadsheet_column_contract(
            column_key="title",
            header="Title",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="title",
        ),
    ]


def _rows() -> list[dict[str, object]]:
    return [{"task_id": "TASK-001", "title": "Prepare URS"}]


def _spreadsheet_request() -> dict[str, object]:
    return build_spreadsheet_operational_export_request(
        export_job_id="EXPJOB-006",
        export_id="TASK-SPREADSHEET-001",
        export_version="1.0.0",
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        source_context_kind="work_package",
        source_context_ref="WP-001",
        columns=_columns(),
        rows=_rows(),
        row_granularity=TASK_ROW_GRANULARITY,
    )


def _invocation_request() -> dict[str, object]:
    return build_export_invocation_request(
        invocation_id="EXPINV-001",
        invocation_boundary=CORE_EXPORT_SERVICE_BOUNDARY,
        requested_by="operator",
        export_request=_spreadsheet_request(),
    )


def _generated_artifact() -> dict[str, object]:
    return build_generated_export_artifact(
        export_request=_spreadsheet_request(),
        artifact_id="ART-001",
        artifact_kind=EXCEL_READY_EXPORT_ARTIFACT_KIND,
        artifact_version="1.0.0",
        artifact_ref="exports/EXPJOB-006.xlsx",
        output_metadata={"created_by": "downstream_renderer"},
    )


def test_build_export_invocation_baseline_exposes_m13_6_rules() -> None:
    baseline = build_export_invocation_baseline()

    assert baseline["checkpoint"] == EXPORT_INVOCATION_CHECKPOINT_ID
    assert baseline["contract_version"] == EXPORT_INVOCATION_CONTRACT_VERSION
    assert CORE_EXPORT_SERVICE_BOUNDARY in baseline["supported_invocation_boundaries"]
    assert EXCEL_READY_EXPORT_ARTIFACT_KIND in baseline["supported_artifact_kinds"]
    assert ACCEPTED_EXPORT_ARTIFACT_DECISION in baseline["supported_acceptance_decisions"]
    assert baseline["failure_policy"] == EXPORT_INVOCATION_FAILURE_POLICY
    assert baseline["renderer_boundary"] == EXPORT_INVOCATION_RENDERING_BOUNDARY


def test_build_export_invocation_request_validates_and_marks_ready() -> None:
    invocation = _invocation_request()

    assert invocation["checkpoint"] == EXPORT_INVOCATION_CHECKPOINT_ID
    assert invocation["contract_version"] == EXPORT_INVOCATION_CONTRACT_VERSION
    assert invocation["validation_mode"] == STRICT_EXPORT_VALIDATION_MODE
    assert invocation["invocation_status"] == READY_FOR_RENDERER_INVOCATION_STATUS
    assert invocation["renderer_boundary"] == EXPORT_INVOCATION_RENDERING_BOUNDARY
    assert invocation["validation_result"]["request_contract_validated"] is True
    assert invocation["validation_result"]["family_payload_validated"] is True
    validate_export_invocation_request(invocation)


def test_invocation_rejects_incomplete_payload_not_caught_by_m13_1_shape_only_validation() -> None:
    request = _spreadsheet_request()
    input_payload = request["input_payload"]
    assert isinstance(input_payload, dict)
    input_payload["columns"] = []

    with pytest.raises(ValueError, match="non-empty columns"):
        validate_export_input_payload_for_invocation(request)


def test_invocation_rejects_unsupported_service_boundary() -> None:
    with pytest.raises(ValueError, match="Unsupported export invocation boundary"):
        build_export_invocation_request(
            invocation_id="EXPINV-001",
            invocation_boundary="cli_adapter_direct_write",
            requested_by="operator",
            export_request=_spreadsheet_request(),
        )


def test_build_generated_export_artifact_returns_acceptance_ready_metadata() -> None:
    artifact = _generated_artifact()

    assert artifact["checkpoint"] == EXPORT_INVOCATION_CHECKPOINT_ID
    assert artifact["contract_version"] == EXPORT_INVOCATION_CONTRACT_VERSION
    assert artifact["export_job_id"] == "EXPJOB-006"
    assert artifact["requested_output_kind"] == EXCEL_READY_OUTPUT_KIND
    assert artifact["rendered_export_output"]["artifact_kind"] == (
        EXCEL_READY_EXPORT_ARTIFACT_KIND
    )
    assert artifact["rendered_export_output"]["rendering_boundary"] == (
        EXPORT_INVOCATION_RENDERING_BOUNDARY
    )
    validate_generated_export_artifact(_spreadsheet_request(), artifact)


def test_generated_artifact_rejects_mismatched_request_identity() -> None:
    artifact = _generated_artifact()
    artifact["export_id"] = "OTHER-EXPORT"

    with pytest.raises(ValueError, match="export_id does not match request"):
        validate_generated_export_artifact(_spreadsheet_request(), artifact)


def test_generated_artifact_rejects_wrong_artifact_kind_for_requested_output() -> None:
    with pytest.raises(ValueError, match="Unsupported rendered export artifact kind"):
        build_generated_export_artifact(
            export_request=_spreadsheet_request(),
            artifact_id="ART-001",
            artifact_kind="csv_artifact",
            artifact_version="1.0.0",
            artifact_ref="exports/EXPJOB-006.csv",
        )


def test_build_export_artifact_acceptance_record_accepts_matching_artifact() -> None:
    acceptance = build_export_artifact_acceptance_record(
        invocation_request=_invocation_request(),
        generated_export_artifact=_generated_artifact(),
        acceptance_id="ACCEPT-001",
        accepted_by="operator",
    )

    assert acceptance["checkpoint"] == EXPORT_INVOCATION_CHECKPOINT_ID
    assert acceptance["acceptance_decision"] == ACCEPTED_EXPORT_ARTIFACT_DECISION
    assert acceptance["artifact_ref"] == "exports/EXPJOB-006.xlsx"
    validate_export_artifact_acceptance_record(
        invocation_request=_invocation_request(),
        generated_export_artifact=_generated_artifact(),
        acceptance_record=acceptance,
    )


def test_rejected_export_artifact_acceptance_record_requires_reason() -> None:
    with pytest.raises(ValueError, match="Rejected export artifacts must declare"):
        build_export_artifact_acceptance_record(
            invocation_request=_invocation_request(),
            generated_export_artifact=_generated_artifact(),
            acceptance_id="ACCEPT-002",
            accepted_by="operator",
            acceptance_decision=REJECTED_EXPORT_ARTIFACT_DECISION,
        )
