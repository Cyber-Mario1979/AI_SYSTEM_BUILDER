"""Spreadsheet and operational export surfaces for the M13.2 checkpoint."""

from __future__ import annotations

from typing import Any

from .export_contracts import (
    CSV_OUTPUT_KIND,
    EXCEL_READY_OUTPUT_KIND,
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
    SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
    build_export_request_payload,
)

SPREADSHEET_SURFACE_CHECKPOINT_ID = "M13.2"
SPREADSHEET_SURFACE_CONTRACT_VERSION = "spreadsheet-operational-surface-v1"

TASK_ROW_GRANULARITY = "task"
WORK_PACKAGE_ROW_GRANULARITY = "work_package"
PLAN_ITEM_ROW_GRANULARITY = "plan_item"
DOCUMENT_OBLIGATION_ROW_GRANULARITY = "document_obligation"
SUMMARY_ROW_GRANULARITY = "summary"

SUPPORTED_SPREADSHEET_ROW_GRANULARITIES = (
    TASK_ROW_GRANULARITY,
    WORK_PACKAGE_ROW_GRANULARITY,
    PLAN_ITEM_ROW_GRANULARITY,
    DOCUMENT_OBLIGATION_ROW_GRANULARITY,
    SUMMARY_ROW_GRANULARITY,
)

SOURCE_VALUE_POLICY = "source_value"
LITERAL_VALUE_POLICY = "literal_value"
DERIVED_VALUE_POLICY = "derived_value"
FORMULA_EXPRESSION_VALUE_POLICY = "formula_expression"

SUPPORTED_SPREADSHEET_VALUE_POLICIES = (
    SOURCE_VALUE_POLICY,
    LITERAL_VALUE_POLICY,
    DERIVED_VALUE_POLICY,
    FORMULA_EXPRESSION_VALUE_POLICY,
)

FORMULAS_DISABLED_POLICY = "formulas_disabled"
FORMULAS_EXPLICIT_ONLY_POLICY = "formulas_explicit_only"

SUPPORTED_SPREADSHEET_FORMULA_POLICIES = (
    FORMULAS_DISABLED_POLICY,
    FORMULAS_EXPLICIT_ONLY_POLICY,
)

SUPPORTED_SPREADSHEET_OPERATIONAL_OUTPUT_KINDS = (
    CSV_OUTPUT_KIND,
    EXCEL_READY_OUTPUT_KIND,
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND,
)

CSV_READY_SHAPE = "csv_ready_tabular_payload"
EXCEL_READY_SHAPE = "excel_ready_workbook_payload"
MICROSOFT_PROJECT_DROP_READY_SHAPE = "microsoft_project_drop_ready_task_table"

_OPERATIONAL_OUTPUT_SHAPES = {
    CSV_OUTPUT_KIND: CSV_READY_SHAPE,
    EXCEL_READY_OUTPUT_KIND: EXCEL_READY_SHAPE,
    MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND: MICROSOFT_PROJECT_DROP_READY_SHAPE,
}

_REQUIRED_COLUMN_CONTRACT_FIELDS = (
    "column_key",
    "header",
    "value_policy",
    "required",
)

_MICROSOFT_PROJECT_REQUIRED_HEADERS = (
    "Task Name",
    "Duration",
    "Start",
    "Finish",
    "Predecessors",
)

_ROW_KEYS_FIELD = "rows"
_COLUMNS_FIELD = "columns"
_ROW_GRANULARITY_FIELD = "row_granularity"


def build_spreadsheet_operational_surface_baseline() -> dict[str, Any]:
    """Return the explicit M13.2 spreadsheet/operational surface baseline."""

    return {
        "checkpoint": SPREADSHEET_SURFACE_CHECKPOINT_ID,
        "contract_version": SPREADSHEET_SURFACE_CONTRACT_VERSION,
        "export_family": SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
        "supported_output_kinds": list(
            SUPPORTED_SPREADSHEET_OPERATIONAL_OUTPUT_KINDS
        ),
        "supported_row_granularities": list(
            SUPPORTED_SPREADSHEET_ROW_GRANULARITIES
        ),
        "supported_value_policies": list(
            SUPPORTED_SPREADSHEET_VALUE_POLICIES
        ),
        "supported_formula_policies": list(
            SUPPORTED_SPREADSHEET_FORMULA_POLICIES
        ),
        "operational_output_shapes": dict(_OPERATIONAL_OUTPUT_SHAPES),
        "microsoft_project_required_headers": list(
            _MICROSOFT_PROJECT_REQUIRED_HEADERS
        ),
        "surface_boundary": (
            "spreadsheet_surfaces_define_deterministic_payload_shapes_not_file_rendering"
        ),
        "formula_boundary": (
            "formulas_are_contract_declarations_only_not_executed_by_this_layer"
        ),
    }


def build_spreadsheet_column_contract(
    *,
    column_key: str,
    header: str,
    value_policy: str,
    required: bool,
    source_field: str | None = None,
    formula_ref: str | None = None,
) -> dict[str, Any]:
    """Build one deterministic spreadsheet column contract."""

    column = {
        "checkpoint": SPREADSHEET_SURFACE_CHECKPOINT_ID,
        "contract_version": SPREADSHEET_SURFACE_CONTRACT_VERSION,
        "column_key": column_key,
        "header": header,
        "value_policy": value_policy,
        "required": required,
        "source_field": source_field,
        "formula_ref": formula_ref,
    }
    validate_spreadsheet_column_contract(column)
    return column


def build_spreadsheet_output_shape(
    *,
    requested_output_kind: str,
    row_granularity: str,
    formula_policy: str,
    sheet_name: str | None = None,
) -> dict[str, Any]:
    """Build the bounded operational shape for a spreadsheet export."""

    _validate_supported_output_kind(requested_output_kind)
    _validate_supported_row_granularity(row_granularity)
    _validate_supported_formula_policy(formula_policy)

    output_shape = {
        "checkpoint": SPREADSHEET_SURFACE_CHECKPOINT_ID,
        "contract_version": SPREADSHEET_SURFACE_CONTRACT_VERSION,
        "requested_output_kind": requested_output_kind,
        "operational_shape": _OPERATIONAL_OUTPUT_SHAPES[requested_output_kind],
        "row_granularity": row_granularity,
        "formula_policy": formula_policy,
        "sheet_name": sheet_name,
        "rendering_boundary": (
            "shape_contract_only_renderer_or_file_writer_is_downstream"
        ),
    }
    validate_spreadsheet_output_shape(output_shape)
    return output_shape


def build_spreadsheet_operational_export_payload(
    *,
    requested_output_kind: str,
    columns: list[dict[str, object]],
    rows: list[dict[str, object]],
    row_granularity: str,
    formula_policy: str = FORMULAS_DISABLED_POLICY,
    sheet_name: str | None = None,
) -> dict[str, Any]:
    """Build a validated operational spreadsheet export payload.

    This payload intentionally matches the M13.1 spreadsheet input contract:
    - columns
    - rows
    - row_granularity

    It adds M13.2 operational shape, value-policy, and formula-policy rules without
    rendering a spreadsheet file.
    """

    output_shape = build_spreadsheet_output_shape(
        requested_output_kind=requested_output_kind,
        row_granularity=row_granularity,
        formula_policy=formula_policy,
        sheet_name=sheet_name,
    )

    payload = {
        "checkpoint": SPREADSHEET_SURFACE_CHECKPOINT_ID,
        "contract_version": SPREADSHEET_SURFACE_CONTRACT_VERSION,
        _COLUMNS_FIELD: columns,
        _ROW_KEYS_FIELD: rows,
        _ROW_GRANULARITY_FIELD: row_granularity,
        "formula_policy": formula_policy,
        "output_shape": output_shape,
        "value_formula_policy": {
            "supported_value_policies": list(
                SUPPORTED_SPREADSHEET_VALUE_POLICIES
            ),
            "formula_policy": formula_policy,
            "execution_policy": (
                "formula_expressions_are_declared_not_executed_in_m13_2"
            ),
        },
    }
    validate_spreadsheet_operational_export_payload(
        payload,
        requested_output_kind=requested_output_kind,
    )
    return payload


def build_spreadsheet_operational_export_request(
    *,
    export_job_id: str,
    export_id: str,
    export_version: str,
    requested_output_kind: str,
    source_context_kind: str,
    source_context_ref: str,
    columns: list[dict[str, object]],
    rows: list[dict[str, object]],
    row_granularity: str,
    formula_policy: str = FORMULAS_DISABLED_POLICY,
    sheet_name: str | None = None,
) -> dict[str, Any]:
    """Build a governed M13.1 export request with an M13.2 spreadsheet payload."""

    input_payload = build_spreadsheet_operational_export_payload(
        requested_output_kind=requested_output_kind,
        columns=columns,
        rows=rows,
        row_granularity=row_granularity,
        formula_policy=formula_policy,
        sheet_name=sheet_name,
    )

    return build_export_request_payload(
        export_job_id=export_job_id,
        export_family=SPREADSHEET_OPERATIONAL_EXPORT_FAMILY,
        export_id=export_id,
        export_version=export_version,
        requested_output_kind=requested_output_kind,
        source_context_kind=source_context_kind,
        source_context_ref=source_context_ref,
        input_payload=input_payload,
    )


def validate_spreadsheet_operational_export_payload(
    payload: dict[str, object],
    *,
    requested_output_kind: str,
) -> None:
    """Validate a spreadsheet operational export payload."""

    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=SPREADSHEET_SURFACE_CHECKPOINT_ID,
        error_prefix="Spreadsheet operational export payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=SPREADSHEET_SURFACE_CONTRACT_VERSION,
        error_prefix="Spreadsheet operational export payload",
    )

    columns = payload.get(_COLUMNS_FIELD)
    if not isinstance(columns, list) or not columns:
        raise ValueError(
            "Spreadsheet operational export payload must declare non-empty columns."
        )

    rows = payload.get(_ROW_KEYS_FIELD)
    if not isinstance(rows, list):
        raise ValueError(
            "Spreadsheet operational export payload must declare rows as a list."
        )

    row_granularity = payload.get(_ROW_GRANULARITY_FIELD)
    if not isinstance(row_granularity, str):
        raise ValueError(
            "Spreadsheet operational export payload must declare row_granularity."
        )
    _validate_supported_row_granularity(row_granularity)

    formula_policy = payload.get("formula_policy")
    if not isinstance(formula_policy, str):
        raise ValueError(
            "Spreadsheet operational export payload must declare formula_policy."
        )
    _validate_supported_formula_policy(formula_policy)

    for column in columns:
        if not isinstance(column, dict):
            raise ValueError(
                "Spreadsheet operational export payload columns must be mappings."
            )
        validate_spreadsheet_column_contract(column)

    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(
                "Spreadsheet operational export payload rows must be mappings."
            )

    _validate_required_row_values(columns, rows)
    _validate_formula_policy_for_columns(columns, formula_policy)
    _validate_microsoft_project_shape_if_requested(
        requested_output_kind=requested_output_kind,
        columns=columns,
    )


def validate_spreadsheet_column_contract(column: dict[str, object]) -> None:
    """Validate one spreadsheet column contract."""

    _validate_required_string_fields(
        column,
        ("checkpoint", "contract_version", "column_key", "header", "value_policy"),
        error_prefix="Spreadsheet column contract",
    )
    _validate_expected_exact_value(
        column,
        field_name="checkpoint",
        expected_value=SPREADSHEET_SURFACE_CHECKPOINT_ID,
        error_prefix="Spreadsheet column contract",
    )
    _validate_expected_exact_value(
        column,
        field_name="contract_version",
        expected_value=SPREADSHEET_SURFACE_CONTRACT_VERSION,
        error_prefix="Spreadsheet column contract",
    )

    for field_name in _REQUIRED_COLUMN_CONTRACT_FIELDS:
        if field_name not in column:
            raise ValueError(
                f"Spreadsheet column contract must declare {field_name}."
            )

    required = column.get("required")
    if not isinstance(required, bool):
        raise ValueError(
            "Spreadsheet column contract must declare required as a boolean."
        )

    value_policy = str(column["value_policy"])
    if value_policy not in SUPPORTED_SPREADSHEET_VALUE_POLICIES:
        raise ValueError(
            "Unsupported spreadsheet value_policy. "
            f"Expected one of: {', '.join(SUPPORTED_SPREADSHEET_VALUE_POLICIES)}."
        )

    source_field = column.get("source_field")
    if value_policy in (SOURCE_VALUE_POLICY, DERIVED_VALUE_POLICY):
        if not isinstance(source_field, str) or not source_field.strip():
            raise ValueError(
                "Spreadsheet column contract must declare source_field for "
                f"{value_policy!r}."
            )

    formula_ref = column.get("formula_ref")
    if value_policy == FORMULA_EXPRESSION_VALUE_POLICY:
        if not isinstance(formula_ref, str) or not formula_ref.strip():
            raise ValueError(
                "Spreadsheet column contract must declare formula_ref for "
                "formula_expression value policy."
            )


def validate_spreadsheet_output_shape(output_shape: dict[str, object]) -> None:
    """Validate a bounded spreadsheet output shape."""

    _validate_expected_exact_value(
        output_shape,
        field_name="checkpoint",
        expected_value=SPREADSHEET_SURFACE_CHECKPOINT_ID,
        error_prefix="Spreadsheet output shape",
    )
    _validate_expected_exact_value(
        output_shape,
        field_name="contract_version",
        expected_value=SPREADSHEET_SURFACE_CONTRACT_VERSION,
        error_prefix="Spreadsheet output shape",
    )

    requested_output_kind = output_shape.get("requested_output_kind")
    if not isinstance(requested_output_kind, str):
        raise ValueError(
            "Spreadsheet output shape must declare requested_output_kind."
        )
    _validate_supported_output_kind(requested_output_kind)

    row_granularity = output_shape.get("row_granularity")
    if not isinstance(row_granularity, str):
        raise ValueError("Spreadsheet output shape must declare row_granularity.")
    _validate_supported_row_granularity(row_granularity)

    formula_policy = output_shape.get("formula_policy")
    if not isinstance(formula_policy, str):
        raise ValueError("Spreadsheet output shape must declare formula_policy.")
    _validate_supported_formula_policy(formula_policy)

    operational_shape = output_shape.get("operational_shape")
    if operational_shape != _OPERATIONAL_OUTPUT_SHAPES[requested_output_kind]:
        raise ValueError(
            "Spreadsheet output shape declares an invalid operational_shape."
        )


def _validate_supported_output_kind(requested_output_kind: str) -> None:
    if requested_output_kind not in SUPPORTED_SPREADSHEET_OPERATIONAL_OUTPUT_KINDS:
        raise ValueError(
            "Unsupported spreadsheet operational output kind. "
            f"Expected one of: {', '.join(SUPPORTED_SPREADSHEET_OPERATIONAL_OUTPUT_KINDS)}."
        )


def _validate_supported_row_granularity(row_granularity: str) -> None:
    if row_granularity not in SUPPORTED_SPREADSHEET_ROW_GRANULARITIES:
        raise ValueError(
            "Unsupported spreadsheet row_granularity. "
            f"Expected one of: {', '.join(SUPPORTED_SPREADSHEET_ROW_GRANULARITIES)}."
        )


def _validate_supported_formula_policy(formula_policy: str) -> None:
    if formula_policy not in SUPPORTED_SPREADSHEET_FORMULA_POLICIES:
        raise ValueError(
            "Unsupported spreadsheet formula_policy. "
            f"Expected one of: {', '.join(SUPPORTED_SPREADSHEET_FORMULA_POLICIES)}."
        )


def _validate_required_row_values(
    columns: list[dict[str, object]],
    rows: list[dict[str, object]],
) -> None:
    required_source_columns = [
        column
        for column in columns
        if column.get("required") is True
        and column.get("value_policy") != FORMULA_EXPRESSION_VALUE_POLICY
    ]

    for row in rows:
        for column in required_source_columns:
            column_key = column["column_key"]
            assert isinstance(column_key, str)
            if column_key not in row or row[column_key] is None:
                raise ValueError(
                    "Spreadsheet row is missing required value for column "
                    f"{column_key!r}."
                )


def _validate_formula_policy_for_columns(
    columns: list[dict[str, object]],
    formula_policy: str,
) -> None:
    has_formula_column = any(
        column.get("value_policy") == FORMULA_EXPRESSION_VALUE_POLICY
        for column in columns
    )

    if has_formula_column and formula_policy != FORMULAS_EXPLICIT_ONLY_POLICY:
        raise ValueError(
            "Formula-expression columns require formulas_explicit_only formula policy."
        )


def _validate_microsoft_project_shape_if_requested(
    *,
    requested_output_kind: str,
    columns: list[dict[str, object]],
) -> None:
    if requested_output_kind != MICROSOFT_PROJECT_DROP_READY_OUTPUT_KIND:
        return

    headers = {
        str(column.get("header"))
        for column in columns
        if isinstance(column.get("header"), str)
    }
    missing_headers = [
        header
        for header in _MICROSOFT_PROJECT_REQUIRED_HEADERS
        if header not in headers
    ]
    if missing_headers:
        raise ValueError(
            "Microsoft Project drop-ready exports must declare required headers: "
            f"{', '.join(missing_headers)}."
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
