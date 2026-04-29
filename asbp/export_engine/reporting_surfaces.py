"""Reporting export family and detail-level discipline for the M13.5 checkpoint."""

from __future__ import annotations

from typing import Any

from .export_contracts import (
    GOVERNED_REPORT_EXPORT_FAMILY,
    MARKDOWN_REPORT_OUTPUT_KIND,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    build_export_request_payload,
)

REPORTING_SURFACE_CHECKPOINT_ID = "M13.5"
REPORTING_SURFACE_CONTRACT_VERSION = "reporting-export-surface-v1"

VALIDATION_SUMMARY_REPORT_TYPE = "validation_summary_report"
MILESTONE_CLOSEOUT_REPORT_TYPE = "milestone_closeout_report"
EXECUTION_EVIDENCE_REPORT_TYPE = "execution_evidence_report"
DASHBOARD_NARRATIVE_REPORT_TYPE = "dashboard_narrative_report"
EXCEPTION_GAP_REPORT_TYPE = "exception_gap_report"

SUPPORTED_REPORT_SURFACE_TYPES = (
    VALIDATION_SUMMARY_REPORT_TYPE,
    MILESTONE_CLOSEOUT_REPORT_TYPE,
    EXECUTION_EVIDENCE_REPORT_TYPE,
    DASHBOARD_NARRATIVE_REPORT_TYPE,
    EXCEPTION_GAP_REPORT_TYPE,
)

SUMMARY_SECTION_TYPE = "summary"
EVIDENCE_BACKED_SECTION_TYPE = "evidence_backed"
ASSUMPTION_SECTION_TYPE = "assumption"
PLACEHOLDER_SECTION_TYPE = "placeholder"
NARRATIVE_SECTION_TYPE = "narrative"

SUPPORTED_REPORT_SECTION_TYPES = (
    SUMMARY_SECTION_TYPE,
    EVIDENCE_BACKED_SECTION_TYPE,
    ASSUMPTION_SECTION_TYPE,
    PLACEHOLDER_SECTION_TYPE,
    NARRATIVE_SECTION_TYPE,
)

CONCISE_NARRATIVE_DEPTH = "concise"
STANDARD_NARRATIVE_DEPTH = "standard"
DETAILED_NARRATIVE_DEPTH = "detailed"
DEEP_DIVE_NARRATIVE_DEPTH = "deep_dive"

SUPPORTED_NARRATIVE_DEPTH_LEVELS = (
    CONCISE_NARRATIVE_DEPTH,
    STANDARD_NARRATIVE_DEPTH,
    DETAILED_NARRATIVE_DEPTH,
    DEEP_DIVE_NARRATIVE_DEPTH,
)

SUPPORTED_REPORT_OUTPUT_KINDS = (
    MARKDOWN_REPORT_OUTPUT_KIND,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
)

MARKDOWN_REPORT_CONTRACT_SHAPE = "markdown_report_contract_payload"
STRUCTURED_REPORT_CONTRACT_SHAPE = "structured_report_contract_payload"

_REPORT_OUTPUT_SHAPES = {
    MARKDOWN_REPORT_OUTPUT_KIND: MARKDOWN_REPORT_CONTRACT_SHAPE,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND: STRUCTURED_REPORT_CONTRACT_SHAPE,
}

REPORT_RENDERING_BOUNDARY = (
    "reporting_surface_defines_report_contract_only_renderer_is_downstream"
)
REPORT_DETAIL_DISCIPLINE_BOUNDARY = (
    "report_sections_must_declare_detail_depth_and_preserve_evidence_summary_separation"
)

_PROHIBITED_REPORT_PAYLOAD_FIELDS = (
    "generated_report_body",
    "freeform_report_prompt",
    "docx_content",
    "pdf_content",
    "markdown_file_content",
    "approved_report_state",
)

_REQUIRED_EVIDENCE_REF_FIELDS = (
    "evidence_id",
    "source_ref",
    "source_role",
)

_REQUIRED_REPORT_SECTION_FIELDS = (
    "section_id",
    "title",
    "section_type",
    "narrative_depth",
    "summary_text",
    "source_refs",
    "evidence_refs",
    "assumption_markers",
    "placeholder_markers",
)


def build_reporting_export_surface_baseline() -> dict[str, Any]:
    """Return the explicit M13.5 reporting export/detail-discipline baseline."""

    return {
        "checkpoint": REPORTING_SURFACE_CHECKPOINT_ID,
        "contract_version": REPORTING_SURFACE_CONTRACT_VERSION,
        "export_family": GOVERNED_REPORT_EXPORT_FAMILY,
        "supported_report_surface_types": list(SUPPORTED_REPORT_SURFACE_TYPES),
        "supported_section_types": list(SUPPORTED_REPORT_SECTION_TYPES),
        "supported_narrative_depth_levels": list(SUPPORTED_NARRATIVE_DEPTH_LEVELS),
        "supported_output_kinds": list(SUPPORTED_REPORT_OUTPUT_KINDS),
        "output_shapes": dict(_REPORT_OUTPUT_SHAPES),
        "evidence_summary_policy": (
            "summary_text_must_not_replace_explicit_evidence_references"
        ),
        "detail_discipline_boundary": REPORT_DETAIL_DISCIPLINE_BOUNDARY,
        "rendering_boundary": REPORT_RENDERING_BOUNDARY,
        "prohibited_report_payload_fields": list(_PROHIBITED_REPORT_PAYLOAD_FIELDS),
    }


def build_report_evidence_ref(
    *,
    evidence_id: str,
    source_ref: str,
    source_role: str,
    evidence_label: str | None = None,
) -> dict[str, Any]:
    """Build one explicit report evidence reference."""

    evidence_ref = {
        "checkpoint": REPORTING_SURFACE_CHECKPOINT_ID,
        "contract_version": REPORTING_SURFACE_CONTRACT_VERSION,
        "evidence_id": evidence_id,
        "source_ref": source_ref,
        "source_role": source_role,
        "evidence_label": evidence_label,
    }
    validate_report_evidence_ref(evidence_ref)
    return evidence_ref


def build_report_section(
    *,
    section_id: str,
    title: str,
    section_type: str,
    narrative_depth: str,
    summary_text: str,
    source_refs: list[str] | None = None,
    evidence_refs: list[dict[str, object]] | None = None,
    assumption_markers: list[str] | None = None,
    placeholder_markers: list[str] | None = None,
) -> dict[str, Any]:
    """Build one governed report section contract."""

    section = {
        "checkpoint": REPORTING_SURFACE_CHECKPOINT_ID,
        "contract_version": REPORTING_SURFACE_CONTRACT_VERSION,
        "section_id": section_id,
        "title": title,
        "section_type": section_type,
        "narrative_depth": narrative_depth,
        "summary_text": summary_text,
        "source_refs": list(source_refs or []),
        "evidence_refs": list(evidence_refs or []),
        "assumption_markers": list(assumption_markers or []),
        "placeholder_markers": list(placeholder_markers or []),
        "detail_discipline_boundary": REPORT_DETAIL_DISCIPLINE_BOUNDARY,
    }
    validate_report_section(section)
    return section


def build_reporting_export_payload(
    *,
    requested_output_kind: str,
    report_surface_type: str,
    report_title: str,
    report_sections: list[dict[str, object]],
    evidence_refs: list[dict[str, object]],
    summary_basis: str,
) -> dict[str, Any]:
    """Build a validated governed reporting export payload.

    This payload intentionally matches the M13.1 governed report input contract:
    - report_sections
    - evidence_refs
    - summary_basis

    It adds M13.5 report-family structure, evidence-versus-summary policy,
    narrative-depth expectations, and detail-level discipline without rendering
    Markdown, DOCX, PDF, dashboard, or AI-written report bodies.
    """

    _validate_supported_output_kind(requested_output_kind)
    _validate_supported_report_surface_type(report_surface_type)
    if not report_title.strip():
        raise ValueError("Reporting export payload must declare non-empty report_title.")
    if not summary_basis.strip():
        raise ValueError("Reporting export payload must declare non-empty summary_basis.")

    payload = {
        "checkpoint": REPORTING_SURFACE_CHECKPOINT_ID,
        "contract_version": REPORTING_SURFACE_CONTRACT_VERSION,
        "report_surface_type": report_surface_type,
        "report_title": report_title,
        "report_sections": report_sections,
        "evidence_refs": evidence_refs,
        "summary_basis": summary_basis,
        "output_shape": {
            "requested_output_kind": requested_output_kind,
            "report_shape": _REPORT_OUTPUT_SHAPES[requested_output_kind],
            "rendering_boundary": REPORT_RENDERING_BOUNDARY,
        },
        "detail_discipline": {
            "boundary": REPORT_DETAIL_DISCIPLINE_BOUNDARY,
            "summary_policy": (
                "summary_text_must_not_replace_explicit_evidence_references"
            ),
            "later_phase_policy": (
                "later_reporting_layers_must_inherit_declared_detail_depth"
            ),
        },
    }
    validate_reporting_export_payload(payload)
    return payload


def build_reporting_export_request(
    *,
    export_job_id: str,
    export_id: str,
    export_version: str,
    requested_output_kind: str,
    source_context_kind: str,
    source_context_ref: str,
    report_surface_type: str,
    report_title: str,
    report_sections: list[dict[str, object]],
    evidence_refs: list[dict[str, object]],
    summary_basis: str,
) -> dict[str, Any]:
    """Build a governed M13.1 export request with an M13.5 reporting payload."""

    input_payload = build_reporting_export_payload(
        requested_output_kind=requested_output_kind,
        report_surface_type=report_surface_type,
        report_title=report_title,
        report_sections=report_sections,
        evidence_refs=evidence_refs,
        summary_basis=summary_basis,
    )

    return build_export_request_payload(
        export_job_id=export_job_id,
        export_family=GOVERNED_REPORT_EXPORT_FAMILY,
        export_id=export_id,
        export_version=export_version,
        requested_output_kind=requested_output_kind,
        source_context_kind=source_context_kind,
        source_context_ref=source_context_ref,
        input_payload=input_payload,
    )


def validate_reporting_export_payload(payload: dict[str, object]) -> None:
    """Validate a governed reporting export payload."""

    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=REPORTING_SURFACE_CHECKPOINT_ID,
        error_prefix="Reporting export payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=REPORTING_SURFACE_CONTRACT_VERSION,
        error_prefix="Reporting export payload",
    )
    _validate_prohibited_report_payload_fields(payload)

    report_surface_type = payload.get("report_surface_type")
    if not isinstance(report_surface_type, str):
        raise ValueError("Reporting export payload must declare report_surface_type.")
    _validate_supported_report_surface_type(report_surface_type)

    _validate_required_string_fields(
        payload,
        ("report_title", "summary_basis"),
        error_prefix="Reporting export payload",
    )

    report_sections = payload.get("report_sections")
    if not isinstance(report_sections, list) or not report_sections:
        raise ValueError(
            "Reporting export payload must declare non-empty report_sections."
        )

    evidence_refs = payload.get("evidence_refs")
    if not isinstance(evidence_refs, list):
        raise ValueError(
            "Reporting export payload must declare evidence_refs as a list."
        )

    global_evidence_ids: set[str] = set()
    for evidence_ref in evidence_refs:
        if not isinstance(evidence_ref, dict):
            raise ValueError("Reporting evidence_refs must contain mappings.")
        validate_report_evidence_ref(evidence_ref)
        evidence_id = str(evidence_ref["evidence_id"])
        if evidence_id in global_evidence_ids:
            raise ValueError(f"Duplicate report evidence_id {evidence_id!r}.")
        global_evidence_ids.add(evidence_id)

    section_ids: set[str] = set()
    for section in report_sections:
        if not isinstance(section, dict):
            raise ValueError("Reporting report_sections must contain mappings.")
        validate_report_section(section)
        section_id = str(section["section_id"])
        if section_id in section_ids:
            raise ValueError(f"Duplicate report section_id {section_id!r}.")
        section_ids.add(section_id)

        section_evidence_refs = section.get("evidence_refs")
        assert isinstance(section_evidence_refs, list)
        for section_evidence_ref in section_evidence_refs:
            assert isinstance(section_evidence_ref, dict)
            evidence_id = str(section_evidence_ref["evidence_id"])
            if evidence_id not in global_evidence_ids:
                raise ValueError(
                    f"Report section references evidence_id {evidence_id!r} "
                    "not declared in payload evidence_refs."
                )

    output_shape = payload.get("output_shape")
    if not isinstance(output_shape, dict):
        raise ValueError("Reporting export payload must declare output_shape.")
    requested_output_kind = output_shape.get("requested_output_kind")
    if not isinstance(requested_output_kind, str):
        raise ValueError("Reporting output_shape must declare requested_output_kind.")
    _validate_supported_output_kind(requested_output_kind)
    if output_shape.get("report_shape") != _REPORT_OUTPUT_SHAPES[requested_output_kind]:
        raise ValueError("Reporting output_shape declares an invalid report_shape.")
    if output_shape.get("rendering_boundary") != REPORT_RENDERING_BOUNDARY:
        raise ValueError("Reporting output_shape declares an invalid rendering boundary.")


def validate_report_section(section: dict[str, object]) -> None:
    """Validate one report section contract."""

    _validate_expected_exact_value(
        section,
        field_name="checkpoint",
        expected_value=REPORTING_SURFACE_CHECKPOINT_ID,
        error_prefix="Report section",
    )
    _validate_expected_exact_value(
        section,
        field_name="contract_version",
        expected_value=REPORTING_SURFACE_CONTRACT_VERSION,
        error_prefix="Report section",
    )

    _validate_required_string_fields(
        section,
        (
            "section_id",
            "title",
            "section_type",
            "narrative_depth",
            "summary_text",
        ),
        error_prefix="Report section",
    )

    for field_name in _REQUIRED_REPORT_SECTION_FIELDS:
        if field_name not in section:
            raise ValueError(f"Report section must declare {field_name}.")

    section_type = str(section["section_type"])
    _validate_supported_section_type(section_type)
    narrative_depth = str(section["narrative_depth"])
    _validate_supported_narrative_depth(narrative_depth)

    source_refs = section.get("source_refs")
    evidence_refs = section.get("evidence_refs")
    assumption_markers = section.get("assumption_markers")
    placeholder_markers = section.get("placeholder_markers")

    if not isinstance(source_refs, list):
        raise ValueError("Report section must declare source_refs as a list.")
    if not isinstance(evidence_refs, list):
        raise ValueError("Report section must declare evidence_refs as a list.")
    if not isinstance(assumption_markers, list):
        raise ValueError("Report section must declare assumption_markers as a list.")
    if not isinstance(placeholder_markers, list):
        raise ValueError("Report section must declare placeholder_markers as a list.")

    for evidence_ref in evidence_refs:
        if not isinstance(evidence_ref, dict):
            raise ValueError("Report section evidence_refs must contain mappings.")
        validate_report_evidence_ref(evidence_ref)

    if section_type == EVIDENCE_BACKED_SECTION_TYPE and not evidence_refs:
        raise ValueError(
            "Evidence-backed report sections must declare explicit evidence_refs."
        )

    if section_type == ASSUMPTION_SECTION_TYPE and not assumption_markers:
        raise ValueError(
            "Assumption report sections must declare assumption_markers."
        )

    if section_type == PLACEHOLDER_SECTION_TYPE and not placeholder_markers:
        raise ValueError(
            "Placeholder report sections must declare placeholder_markers."
        )

    summary_text = str(section["summary_text"]).lower()
    if "[evidence]" in summary_text and not evidence_refs:
        raise ValueError(
            "Report section summary_text must not make hidden evidence claims."
        )

    if section.get("detail_discipline_boundary") != REPORT_DETAIL_DISCIPLINE_BOUNDARY:
        raise ValueError("Report section declares an invalid detail discipline boundary.")


def validate_report_evidence_ref(evidence_ref: dict[str, object]) -> None:
    """Validate one explicit report evidence reference."""

    _validate_expected_exact_value(
        evidence_ref,
        field_name="checkpoint",
        expected_value=REPORTING_SURFACE_CHECKPOINT_ID,
        error_prefix="Report evidence reference",
    )
    _validate_expected_exact_value(
        evidence_ref,
        field_name="contract_version",
        expected_value=REPORTING_SURFACE_CONTRACT_VERSION,
        error_prefix="Report evidence reference",
    )
    _validate_required_string_fields(
        evidence_ref,
        _REQUIRED_EVIDENCE_REF_FIELDS,
        error_prefix="Report evidence reference",
    )


def _validate_supported_report_surface_type(report_surface_type: str) -> None:
    if report_surface_type not in SUPPORTED_REPORT_SURFACE_TYPES:
        raise ValueError(
            "Unsupported report surface type. "
            f"Expected one of: {', '.join(SUPPORTED_REPORT_SURFACE_TYPES)}."
        )


def _validate_supported_section_type(section_type: str) -> None:
    if section_type not in SUPPORTED_REPORT_SECTION_TYPES:
        raise ValueError(
            "Unsupported report section type. "
            f"Expected one of: {', '.join(SUPPORTED_REPORT_SECTION_TYPES)}."
        )


def _validate_supported_narrative_depth(narrative_depth: str) -> None:
    if narrative_depth not in SUPPORTED_NARRATIVE_DEPTH_LEVELS:
        raise ValueError(
            "Unsupported narrative depth. "
            f"Expected one of: {', '.join(SUPPORTED_NARRATIVE_DEPTH_LEVELS)}."
        )


def _validate_supported_output_kind(requested_output_kind: str) -> None:
    if requested_output_kind not in SUPPORTED_REPORT_OUTPUT_KINDS:
        raise ValueError(
            "Unsupported reporting output kind. "
            f"Expected one of: {', '.join(SUPPORTED_REPORT_OUTPUT_KINDS)}."
        )


def _validate_prohibited_report_payload_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_REPORT_PAYLOAD_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M13.5 reporting payloads."
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
