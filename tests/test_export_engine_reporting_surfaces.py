import pytest

from asbp.export_engine import (
    ASSUMPTION_SECTION_TYPE,
    DEEP_DIVE_NARRATIVE_DEPTH,
    EVIDENCE_BACKED_SECTION_TYPE,
    EXECUTION_EVIDENCE_REPORT_TYPE,
    GOVERNED_REPORT_EXPORT_FAMILY,
    MARKDOWN_REPORT_CONTRACT_SHAPE,
    MARKDOWN_REPORT_OUTPUT_KIND,
    REPORTING_SURFACE_CHECKPOINT_ID,
    REPORTING_SURFACE_CONTRACT_VERSION,
    REPORT_DETAIL_DISCIPLINE_BOUNDARY,
    REPORT_RENDERING_BOUNDARY,
    STANDARD_NARRATIVE_DEPTH,
    STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
    SUMMARY_SECTION_TYPE,
    VALIDATION_SUMMARY_REPORT_TYPE,
    build_report_evidence_ref,
    build_report_section,
    build_reporting_export_payload,
    build_reporting_export_request,
    build_reporting_export_surface_baseline,
    validate_export_request_payload,
    validate_reporting_export_payload,
)


def _evidence_refs() -> list[dict[str, object]]:
    return [
        build_report_evidence_ref(
            evidence_id="EVID-001",
            source_ref="tests",
            source_role="validation_evidence",
            evidence_label="pytest pass result",
        ),
        build_report_evidence_ref(
            evidence_id="EVID-002",
            source_ref="docs/UAT/M12_UAT_REPORT.md",
            source_role="uat_evidence",
            evidence_label="UAT acceptance report",
        ),
    ]


def _report_sections() -> list[dict[str, object]]:
    evidence_refs = _evidence_refs()
    return [
        build_report_section(
            section_id="SEC-001",
            title="Validation Summary",
            section_type=EVIDENCE_BACKED_SECTION_TYPE,
            narrative_depth=STANDARD_NARRATIVE_DEPTH,
            summary_text="Validation completed against explicit test evidence.",
            source_refs=["tests"],
            evidence_refs=[evidence_refs[0]],
        ),
        build_report_section(
            section_id="SEC-002",
            title="Operator Summary",
            section_type=SUMMARY_SECTION_TYPE,
            narrative_depth=DEEP_DIVE_NARRATIVE_DEPTH,
            summary_text="This section summarizes the operator-facing result.",
            source_refs=["docs/UAT/M12_UAT_REPORT.md"],
        ),
    ]


def test_build_reporting_export_surface_baseline_exposes_m13_5_rules() -> None:
    baseline = build_reporting_export_surface_baseline()

    assert baseline["checkpoint"] == REPORTING_SURFACE_CHECKPOINT_ID
    assert baseline["contract_version"] == REPORTING_SURFACE_CONTRACT_VERSION
    assert baseline["export_family"] == GOVERNED_REPORT_EXPORT_FAMILY
    assert VALIDATION_SUMMARY_REPORT_TYPE in baseline["supported_report_surface_types"]
    assert EVIDENCE_BACKED_SECTION_TYPE in baseline["supported_section_types"]
    assert DEEP_DIVE_NARRATIVE_DEPTH in baseline["supported_narrative_depth_levels"]
    assert MARKDOWN_REPORT_OUTPUT_KIND in baseline["supported_output_kinds"]
    assert baseline["output_shapes"][MARKDOWN_REPORT_OUTPUT_KIND] == (
        MARKDOWN_REPORT_CONTRACT_SHAPE
    )
    assert baseline["detail_discipline_boundary"] == REPORT_DETAIL_DISCIPLINE_BOUNDARY
    assert baseline["rendering_boundary"] == REPORT_RENDERING_BOUNDARY


def test_build_report_evidence_ref_returns_explicit_evidence_object() -> None:
    evidence_ref = build_report_evidence_ref(
        evidence_id="EVID-001",
        source_ref="tests",
        source_role="validation_evidence",
    )

    assert evidence_ref["checkpoint"] == REPORTING_SURFACE_CHECKPOINT_ID
    assert evidence_ref["contract_version"] == REPORTING_SURFACE_CONTRACT_VERSION
    assert evidence_ref["evidence_id"] == "EVID-001"


def test_build_report_section_requires_evidence_for_evidence_backed_section() -> None:
    with pytest.raises(ValueError, match="explicit evidence_refs"):
        build_report_section(
            section_id="SEC-001",
            title="Validation Summary",
            section_type=EVIDENCE_BACKED_SECTION_TYPE,
            narrative_depth=STANDARD_NARRATIVE_DEPTH,
            summary_text="Validation completed.",
            source_refs=["tests"],
        )


def test_build_report_section_requires_assumption_marker_for_assumption_section() -> None:
    with pytest.raises(ValueError, match="assumption_markers"):
        build_report_section(
            section_id="SEC-001",
            title="Assumption Summary",
            section_type=ASSUMPTION_SECTION_TYPE,
            narrative_depth=STANDARD_NARRATIVE_DEPTH,
            summary_text="This is based on a labelled assumption.",
            source_refs=["runtime"],
        )


def test_build_report_section_rejects_hidden_evidence_claim() -> None:
    with pytest.raises(ValueError, match="hidden evidence claims"):
        build_report_section(
            section_id="SEC-001",
            title="Hidden Evidence",
            section_type=SUMMARY_SECTION_TYPE,
            narrative_depth=STANDARD_NARRATIVE_DEPTH,
            summary_text="[Evidence] This claim has no explicit evidence object.",
            source_refs=["tests"],
        )


def test_build_reporting_export_payload_returns_m13_1_compatible_shape() -> None:
    payload = build_reporting_export_payload(
        requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
        report_surface_type=VALIDATION_SUMMARY_REPORT_TYPE,
        report_title="M13 Validation Summary",
        report_sections=_report_sections(),
        evidence_refs=_evidence_refs(),
        summary_basis="validation_checkpoint",
    )

    assert payload["checkpoint"] == REPORTING_SURFACE_CHECKPOINT_ID
    assert payload["contract_version"] == REPORTING_SURFACE_CONTRACT_VERSION
    assert payload["report_surface_type"] == VALIDATION_SUMMARY_REPORT_TYPE
    assert "report_sections" in payload
    assert "evidence_refs" in payload
    assert "summary_basis" in payload
    assert payload["output_shape"]["report_shape"] == MARKDOWN_REPORT_CONTRACT_SHAPE
    assert payload["output_shape"]["rendering_boundary"] == REPORT_RENDERING_BOUNDARY
    assert payload["detail_discipline"]["boundary"] == (
        REPORT_DETAIL_DISCIPLINE_BOUNDARY
    )


def test_build_reporting_export_request_returns_valid_m13_1_request() -> None:
    request = build_reporting_export_request(
        export_job_id="EXPJOB-005",
        export_id="REPORT-001",
        export_version="1.0.0",
        requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
        source_context_kind="standalone_governed_export_request",
        source_context_ref="REPORT-SOURCE-001",
        report_surface_type=VALIDATION_SUMMARY_REPORT_TYPE,
        report_title="M13 Validation Summary",
        report_sections=_report_sections(),
        evidence_refs=_evidence_refs(),
        summary_basis="validation_checkpoint",
    )

    assert request["export_family"] == GOVERNED_REPORT_EXPORT_FAMILY
    assert request["requested_output_kind"] == MARKDOWN_REPORT_OUTPUT_KIND
    assert request["input_payload"]["checkpoint"] == REPORTING_SURFACE_CHECKPOINT_ID
    validate_export_request_payload(request)


def test_reporting_export_payload_accepts_structured_report_payload_output() -> None:
    payload = build_reporting_export_payload(
        requested_output_kind=STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND,
        report_surface_type=EXECUTION_EVIDENCE_REPORT_TYPE,
        report_title="Execution Evidence Summary",
        report_sections=_report_sections(),
        evidence_refs=_evidence_refs(),
        summary_basis="execution_evidence",
    )

    assert payload["output_shape"]["requested_output_kind"] == (
        STRUCTURED_REPORT_PAYLOAD_OUTPUT_KIND
    )


def test_reporting_export_payload_rejects_unknown_section_evidence_reference() -> None:
    section = build_report_section(
        section_id="SEC-001",
        title="Validation Summary",
        section_type=EVIDENCE_BACKED_SECTION_TYPE,
        narrative_depth=STANDARD_NARRATIVE_DEPTH,
        summary_text="Validation completed against explicit test evidence.",
        source_refs=["tests"],
        evidence_refs=[
            build_report_evidence_ref(
                evidence_id="EVID-404",
                source_ref="tests",
                source_role="validation_evidence",
            )
        ],
    )

    with pytest.raises(ValueError, match="not declared in payload evidence_refs"):
        build_reporting_export_payload(
            requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
            report_surface_type=VALIDATION_SUMMARY_REPORT_TYPE,
            report_title="M13 Validation Summary",
            report_sections=[section],
            evidence_refs=_evidence_refs(),
            summary_basis="validation_checkpoint",
        )


def test_reporting_export_payload_rejects_duplicate_section_ids() -> None:
    section = _report_sections()[0]

    with pytest.raises(ValueError, match="Duplicate report section_id"):
        build_reporting_export_payload(
            requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
            report_surface_type=VALIDATION_SUMMARY_REPORT_TYPE,
            report_title="M13 Validation Summary",
            report_sections=[section, section],
            evidence_refs=_evidence_refs(),
            summary_basis="validation_checkpoint",
        )


def test_validate_reporting_export_payload_rejects_prohibited_freeform_generation_field() -> None:
    payload = build_reporting_export_payload(
        requested_output_kind=MARKDOWN_REPORT_OUTPUT_KIND,
        report_surface_type=VALIDATION_SUMMARY_REPORT_TYPE,
        report_title="M13 Validation Summary",
        report_sections=_report_sections(),
        evidence_refs=_evidence_refs(),
        summary_basis="validation_checkpoint",
    )
    payload["freeform_report_prompt"] = "Write any report you want."

    with pytest.raises(ValueError, match="freeform_report_prompt is not allowed"):
        validate_reporting_export_payload(payload)
