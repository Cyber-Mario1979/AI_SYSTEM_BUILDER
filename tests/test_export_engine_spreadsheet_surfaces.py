import pytest

from asbp.export_engine import (
    CSV_OUTPUT_KIND,
    CSV_READY_SHAPE,
    EXCEL_READY_OUTPUT_KIND,
    EXCEL_READY_SHAPE,
    FORMULAS_DISABLED_POLICY,
    FORMULAS_EXPLICIT_ONLY_POLICY,
    FORMULA_EXPRESSION_VALUE_POLICY,
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
    MICROSOFT_PROJECT_DROP_READY_SHAPE,
    PLAN_ITEM_ROW_GRANULARITY,
    SOURCE_CONTEXT_SOURCE_ROLE,
    SOURCE_VALUE_POLICY,
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    SPREADSHEET_SURFACE_CHECKPOINT_ID,
    SPREADSHEET_SURFACE_CONTRACT_VERSION,
    TASK_ROW_GRANULARITY,
    build_spreadsheet_column_contract,
    build_spreadsheet_operational_export_payload,
    build_spreadsheet_operational_export_request,
    build_spreadsheet_operational_surface_baseline,
    build_spreadsheet_output_shape,
    validate_export_request_payload,
    validate_spreadsheet_operational_export_payload,
)


def _task_columns() -> list[dict[str, object]]:
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
        build_spreadsheet_column_contract(
            column_key="status",
            header="Status",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="status",
        ),
    ]


def _task_rows() -> list[dict[str, object]]:
    return [
        {"task_id": "TASK-001", "title": "Prepare URS", "status": "open"},
        {"task_id": "TASK-002", "title": "Review URS", "status": "planned"},
    ]


def _microsoft_project_columns() -> list[dict[str, object]]:
    return [
        build_spreadsheet_column_contract(
            column_key="task_name",
            header="Task Name",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="task_name",
        ),
        build_spreadsheet_column_contract(
            column_key="duration",
            header="Duration",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="duration",
        ),
        build_spreadsheet_column_contract(
            column_key="start",
            header="Start",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="start",
        ),
        build_spreadsheet_column_contract(
            column_key="finish",
            header="Finish",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="finish",
        ),
        build_spreadsheet_column_contract(
            column_key="predecessors",
            header="Predecessors",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
            source_field="predecessors",
        ),
    ]


def _microsoft_project_rows() -> list[dict[str, object]]:
    return [
        {
            "task_name": "Prepare URS",
            "duration": "2d",
            "start": "2026-05-01",
            "finish": "2026-05-02",
            "predecessors": "",
        }
    ]


def test_build_spreadsheet_operational_surface_baseline_exposes_m13_2_rules() -> None:
    baseline = build_spreadsheet_operational_surface_baseline()

    assert baseline["checkpoint"] == SPREADSHEET_SURFACE_CHECKPOINT_ID
    assert baseline["contract_version"] == SPREADSHEET_SURFACE_CONTRACT_VERSION
    assert baseline["export_family"] == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY
    assert CSV_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert EXCEL_READY_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert TASK_ROW_GRANULARITY in baseline["supported_row_granularities"]
    assert baseline["operational_output_shapes"][CSV_OUTPUT_KIND] == CSV_READY_SHAPE
    assert baseline["operational_output_shapes"][EXCEL_READY_OUTPUT_KIND] == (
        EXCEL_READY_SHAPE
    )
    assert baseline["operational_output_shapes"][
        MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND
    ] == MICROSOFT_PROJECT_DROP_READY_SHAPE
    assert baseline["surface_boundary"] == (
        "spreadsheet_surfaces_define_deterministic_payload_shapes_not_file_rendering"
    )


def test_build_spreadsheet_column_contract_validates_source_columns() -> None:
    column = build_spreadsheet_column_contract(
        column_key="task_id",
        header="Task ID",
        value_policy=SOURCE_VALUE_POLICY,
        required=True,
        source_field="task_id",
    )

    assert column["checkpoint"] == SPREADSHEET_SURFACE_CHECKPOINT_ID
    assert column["contract_version"] == SPREADSHEET_SURFACE_CONTRACT_VERSION
    assert column["column_key"] == "task_id"
    assert column["source_field"] == "task_id"


def test_build_spreadsheet_column_contract_rejects_source_column_without_source_field() -> None:
    with pytest.raises(ValueError, match="source_field"):
        build_spreadsheet_column_contract(
            column_key="task_id",
            header="Task ID",
            value_policy=SOURCE_VALUE_POLICY,
            required=True,
        )


def test_build_spreadsheet_column_contract_rejects_formula_column_without_formula_ref() -> None:
    with pytest.raises(ValueError, match="formula_ref"):
        build_spreadsheet_column_contract(
            column_key="percent_complete",
            header="% Complete",
            value_policy=FORMULA_EXPRESSION_VALUE_POLICY,
            required=False,
        )


def test_build_spreadsheet_output_shape_returns_csv_shape() -> None:
    output_shape = build_spreadsheet_output_shape(
        requested_output_kind=CSV_OUTPUT_KIND,
        row_granularity=TASK_ROW_GRANULARITY,
        formula_policy=FORMULAS_DISABLED_POLICY,
    )

    assert output_shape["checkpoint"] == SPREADSHEET_SURFACE_CHECKPOINT_ID
    assert output_shape["operational_shape"] == CSV_READY_SHAPE
    assert output_shape["rendering_boundary"] == (
        "shape_contract_only_renderer_or_file_writer_is_downstream"
    )


def test_build_spreadsheet_operational_export_payload_returns_m13_1_compatible_payload() -> None:
    payload = build_spreadsheet_operational_export_payload(
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        columns=_task_columns(),
        rows=_task_rows(),
        row_granularity=TASK_ROW_GRANULARITY,
        formula_policy=FORMULAS_DISABLED_POLICY,
        sheet_name="Tasks",
    )

    assert payload["checkpoint"] == SPREADSHEET_SURFACE_CHECKPOINT_ID
    assert payload["contract_version"] == SPREADSHEET_SURFACE_CONTRACT_VERSION
    assert "columns" in payload
    assert "rows" in payload
    assert payload["row_granularity"] == TASK_ROW_GRANULARITY
    assert payload["output_shape"]["operational_shape"] == EXCEL_READY_SHAPE


def test_validate_spreadsheet_operational_export_payload_rejects_missing_required_row_value() -> None:
    payload = build_spreadsheet_operational_export_payload(
        requested_output_kind=CSV_OUTPUT_KIND,
        columns=_task_columns(),
        rows=_task_rows(),
        row_granularity=TASK_ROW_GRANULARITY,
    )
    del payload["rows"][0]["task_id"]

    with pytest.raises(ValueError, match="required value for column 'task_id'"):
        validate_spreadsheet_operational_export_payload(
            payload,
            requested_output_kind=CSV_OUTPUT_KIND,
        )


def test_validate_spreadsheet_operational_export_payload_rejects_formula_column_when_formulas_disabled() -> None:
    columns = _task_columns()
    columns.append(
        build_spreadsheet_column_contract(
            column_key="progress_formula",
            header="Progress Formula",
            value_policy=FORMULA_EXPRESSION_VALUE_POLICY,
            required=False,
            formula_ref="=IF(status='done',100,0)",
        )
    )

    with pytest.raises(ValueError, match="formulas_explicit_only"):
        build_spreadsheet_operational_export_payload(
            requested_output_kind=EXCEL_READY_OUTPUT_KIND,
            columns=columns,
            rows=_task_rows(),
            row_granularity=TASK_ROW_GRANULARITY,
            formula_policy=FORMULAS_DISABLED_POLICY,
        )


def test_build_spreadsheet_operational_export_payload_accepts_explicit_formula_policy() -> None:
    columns = _task_columns()
    columns.append(
        build_spreadsheet_column_contract(
            column_key="progress_formula",
            header="Progress Formula",
            value_policy=FORMULA_EXPRESSION_VALUE_POLICY,
            required=False,
            formula_ref="=IF(status='done',100,0)",
        )
    )

    payload = build_spreadsheet_operational_export_payload(
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        columns=columns,
        rows=_task_rows(),
        row_granularity=TASK_ROW_GRANULARITY,
        formula_policy=FORMULAS_EXPLICIT_ONLY_POLICY,
    )

    assert payload["formula_policy"] == FORMULAS_EXPLICIT_ONLY_POLICY
    assert payload["value_formula_policy"]["execution_policy"] == (
        "formula_expressions_are_declared_not_executed_in_m13_2"
    )


def test_build_spreadsheet_operational_export_payload_rejects_incomplete_microsoft_project_shape() -> None:
    with pytest.raises(ValueError, match="Microsoft Project drop-ready"):
        build_spreadsheet_operational_export_payload(
            requested_output_kind=MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
            columns=_task_columns(),
            rows=_task_rows(),
            row_granularity=PLAN_ITEM_ROW_GRANULARITY,
        )


def test_build_spreadsheet_operational_export_payload_accepts_microsoft_project_drop_ready_shape() -> None:
    payload = build_spreadsheet_operational_export_payload(
        requested_output_kind=MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
        columns=_microsoft_project_columns(),
        rows=_microsoft_project_rows(),
        row_granularity=PLAN_ITEM_ROW_GRANULARITY,
    )

    assert payload["output_shape"]["operational_shape"] == (
        MICROSOFT_PROJECT_DROP_READY_SHAPE
    )


def test_build_spreadsheet_operational_export_request_returns_valid_m13_1_request() -> None:
    request = build_spreadsheet_operational_export_request(
        export_job_id="EXPJOB-002",
        export_id="TASK-SPREADSHEET-001",
        export_version="1.0.0",
        requested_output_kind=EXCEL_READY_OUTPUT_KIND,
        source_context_kind="work_package",
        source_context_ref="WP-001",
        columns=_task_columns(),
        rows=_task_rows(),
        row_granularity=TASK_ROW_GRANULARITY,
        formula_policy=FORMULAS_DISABLED_POLICY,
        sheet_name="Tasks",
    )

    assert request["export_family"] == SPREADSHEET_OPERATIONAL_EXPORT_FAMILY
    assert request["source_context"]["source_role"] == SOURCE_CONTEXT_SOURCE_ROLE
    assert request["input_payload"]["checkpoint"] == SPREADSHEET_SURFACE_CHECKPOINT_ID
    validate_export_request_payload(request)
