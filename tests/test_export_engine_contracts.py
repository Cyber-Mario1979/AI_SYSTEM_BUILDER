import pytest

from asbp.export_engine import (
    DASHBOARD_SNAPSHOT_OUTPUT_KIND,
    DASHBOARD_STATUS_EXPORT_FAMILY,
    EXCEL_READY_OUTPUT_KIND,
    EXPORT_CONTRACT_CHECKPOINT_ID,
    EXPORT_OUTPUT_CONTRACT_VERSION,
    EXPORT_PAYLOAD_CONTRACT_VERSION,
    EXPORT_REQUEST_CONTRACT_VERSION,
    EXPORT_OUTPUT_TRUTH_BOUNDARY,
    GANTT_PLANNING_EXPORT_FAMILY,
    GOVERNED_REPORT_EXPORT_FAMILY,
    MARKDOWN_REPORT_OUTPUT_KIND,
    RENDERED_EXPORT_OUTPUT_ROLE,
    SOURCE_CONTEXT_SOURCE_ROLE,
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    build_export_contract_baseline,
    build_export_output_contract,
    build_export_payload_contract,
    build_export_request_payload,
    validate_export_request_payload,
)


def _spreadsheet_payload() -> dict[str, object]:
    return {
        "columns": ["task_id", "title", "status"],
        "rows": [
            {"task_id": "TASK-001", "title": "Prepare URS", "status": "open"}
        ],
        "row_granularity": "task",
    }


def test_build_export_contract_baseline_exposes_m13_1_rules() -> None:
    baseline = build_export_contract_baseline()

    assert baseline["checkpoint"] == EXPORT_CONTRACT_CHECKPOINT_ID
    assert baseline["request_contract_version"] == EXPORT_REQUEST_CONTRACT_VERSION
    assert baseline["payload_contract_version"] == EXPORT_PAYLOAD_CONTRACT_VERSION
    assert baseline["output_contract_version"] == EXPORT_OUTPUT_CONTRACT_VERSION
    assert SPREADSHEET_OPERATIONAL_EXPORT_FAMILY in baseline["supported_export_families"]
    assert GANTT_PLANNING_EXPORT_FAMILY in baseline["supported_export_families"]
    assert DASHBOARD_STATUS_EXPORT_FAMILY in baseline["supported_export_families"]
    assert GOVERNED_REPORT_EXPORT_FAMILY in baseline["supported_export_families"]
    assert baseline["truth_separation"]["source_context"] == SOURCE_CONTEXT_SOURCE_ROLE
    assert baseline["truth_separation"]["rendered_export_output"] == (
        RENDERED_EXPORT_OUTPUT_ROLE
    )
    assert baseline["boundary_policy"] == (
        "export_families_are_core_engine_output_contracts_not_ui_api_delivery"
    )


def test_build_export_payload_contract_returns_family_required_fields() -> None:
    contract = build_export_payload_contract(SPREADSHEET_OPERATIONAL_EXPORT_FAMILY)

    assert contract["checkpoint"] == EXPORT_CONTRACT_CHECKPOINT_ID
    assert contract["contract_version"] == EXPORT_PAYLOAD_CONTRACT_VERSION
    assert contract["export_family"] == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY
    assert "columns" in contract["required_payload_fields"]
    assert "raw_freeform_prompt" in contract["prohibited_input_payload_fields"]


def test_build_export_output_contract_preserves_downstream_only_boundary() -> None:
    contract = build_export_output_contract(
        export_family=GOVERNED_REPORT_EXPORT_FAMILY,
        requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
    )

    assert contract["checkpoint"] == EXPORT_CONTRACT_CHECKPOINT_ID
    assert contract["contract_version"] == EXPORT_OUTPUT_CONTRACT_VERSION
    assert contract["export_family"] == GOVERNED_REPORT_EXPORT_FAMILY
    assert contract["requested_output_kind"] == MARKDOWN_REPORT_OUTPUT_KIND
    assert contract["rendered_output_role"] == RENDERED_EXPORT_OUTPUT_ROLE
    assert contract["output_truth_boundary"] == EXPORT_OUTPUT_TRUTH_BOUNDARY
    assert contract["delivery_surface_boundary"] == (
        "output_contract_defines_artifact_shape_not_ui_or_api_delivery"
    )


def test_build_export_request_payload_returns_valid_governed_shape() -> None:
    payload = build_export_request_payload(
        export_job_id="EXPJOB-001",
        export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
        export_id="TASK-EXPORT-001",
        export_version="1.0.0",
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        source_context_kind="work_package",
        source_context_ref="WP-001",
        input_payload=_spreadsheet_payload(),
    )

    assert payload["checkpoint"] == EXPORT_CONTRACT_CHECKPOINT_ID
    assert payload["contract_version"] == EXPORT_REQUEST_CONTRACT_VERSION
    assert payload["export_family"] == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY
    assert payload["requested_output_kind"] == EXCEL_READY_OUTPUT_KIND
    assert payload["source_context"]["kind"] == "work_package"
    assert payload["source_context"]["source_role"] == SOURCE_CONTEXT_SOURCE_ROLE


def test_validate_export_request_payload_rejects_missing_family_required_payload_field() -> None:
    input_payload = _spreadsheet_payload()
    del input_payload["columns"]

    with pytest.raises(ValueError, match="required columns"):
        build_export_request_payload(
            export_job_id="EXPJOB-001",
            export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
            export_id="TASK-EXPORT-001",
            export_version="1.0.0",
            requested_output_kind=EXCEL_READY_OUTPUT_KIND,
            source_context_kind="work_package",
            source_context_ref="WP-001",
            input_payload=input_payload,
        )


def test_validate_export_request_payload_rejects_unsupported_export_family() -> None:
    with pytest.raises(ValueError, match="Unsupported export_family"):
        build_export_request_payload(
            export_job_id="EXPJOB-001",
            export_family="visual_slide_deck",
            export_id="TASK-EXPORT-001",
            export_version="1.0.0",
            requested_output_kind=EXCEL_READY_OUTPUT_KIND,
            source_context_kind="work_package",
            source_context_ref="WP-001",
            input_payload=_spreadsheet_payload(),
        )


def test_validate_export_request_payload_rejects_wrong_output_kind_for_family() -> None:
    with pytest.raises(ValueError, match="Unsupported requested_output_kind"):
        build_export_request_payload(
            export_job_id="EXPJOB-001",
            export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
            export_id="TASK-EXPORT-001",
            export_version="1.0.0",
            requested_output_kind=DASHBOARD_SNAPSHOT_OUTPUT_KIND,
            source_context_kind="work_package",
            source_context_ref="WP-001",
            input_payload=_spreadsheet_payload(),
        )


def test_validate_export_request_payload_rejects_unsupported_source_context_kind() -> None:
    with pytest.raises(ValueError, match="Unsupported source context kind"):
        build_export_request_payload(
            export_job_id="EXPJOB-001",
            export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
            export_id="TASK-EXPORT-001",
            export_version="1.0.0",
            requested_output_kind=EXCEL_READY_OUTPUT_KIND,
            source_context_kind="raw_database_row",
            source_context_ref="WP-001",
            input_payload=_spreadsheet_payload(),
        )


def test_validate_export_request_payload_rejects_prohibited_payload_field() -> None:
    input_payload = _spreadsheet_payload()
    input_payload["resolver_bypass"] = True

    with pytest.raises(ValueError, match="resolver_bypass is not allowed"):
        build_export_request_payload(
            export_job_id="EXPJOB-001",
            export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
            export_id="TASK-EXPORT-001",
            export_version="1.0.0",
            requested_output_kind=EXCEL_READY_OUTPUT_KIND,
            source_context_kind="work_package",
            source_context_ref="WP-001",
            input_payload=input_payload,
        )


def test_validate_export_request_payload_accepts_existing_valid_payload() -> None:
    payload = build_export_request_payload(
        export_job_id="EXPJOB-001",
        export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
        export_id="TASK-EXPORT-001",
        export_version="1.0.0",
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        source_context_kind="work_package",
        source_context_ref="WP-001",
        input_payload=_spreadsheet_payload(),
    )

    validate_export_request_payload(payload)
