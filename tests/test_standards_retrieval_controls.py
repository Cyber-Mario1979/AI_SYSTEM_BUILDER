"""Tests for M30.5 standards retrieval controls."""

from __future__ import annotations

import pytest

from asbp.retrieval import RetrievalIndexRecord, RetrievalQuery, StandardsRetrievalControls
from asbp.retrieval.standards import DEFAULT_STANDARDS_LIMITATION, MISSING_CLAUSE_LIMITATION


def _standard(**overrides: object) -> RetrievalIndexRecord:
    values = {
        "source_id": "STD-ISO-001",
        "source_path": "data/source/standards/iso_001.json",
        "source_version": "v1",
        "source_status": "approved",
        "authority_role": "reference_support",
        "eligibility_decision": "eligible",
        "chunk_ref": "clause:4.2",
        "build_id": "m30-5-test-build",
        "text": "cleanroom airflow monitoring standard citation",
        "limitation_trace": (),
        "metadata": {"source_family": "standards", "clause_ref": "4.2"},
    }
    values.update(overrides)
    return RetrievalIndexRecord(**values)


def test_standards_search_preserves_helper_only_non_authority_behavior() -> None:
    controls = StandardsRetrievalControls([_standard()])

    results = controls.search(RetrievalQuery(text="airflow citation"))

    assert len(results) == 1
    result = results[0]
    assert result.helper_only is True
    assert result.non_authoritative is True
    assert result.retrieval_result.helper_only is True
    assert result.retrieval_result.non_authoritative is True
    assert DEFAULT_STANDARDS_LIMITATION in result.authority_statement


def test_standards_search_returns_citation_fallback_from_trace_fields() -> None:
    controls = StandardsRetrievalControls([_standard(source_id="STD-123", source_version="2026", chunk_ref="section:7")])

    [result] = controls.search(RetrievalQuery(text="monitoring"))

    assert result.citation == "STD-123 2026 section:7"


def test_missing_clause_data_adds_visible_limitation_warning() -> None:
    record = _standard(metadata={"source_family": "standards"})
    controls = StandardsRetrievalControls([record])

    [result] = controls.search(RetrievalQuery(text="cleanroom"))

    assert DEFAULT_STANDARDS_LIMITATION in result.limitation_warnings
    assert MISSING_CLAUSE_LIMITATION in result.limitation_warnings


def test_pending_or_tbd_standards_are_blocked() -> None:
    with pytest.raises(ValueError, match="blocked"):
        StandardsRetrievalControls([_standard(source_status="pending")])

    with pytest.raises(ValueError, match="blocked"):
        StandardsRetrievalControls([_standard(source_status="TBD")])


def test_non_standards_family_records_are_rejected() -> None:
    with pytest.raises(ValueError, match="standards-family"):
        StandardsRetrievalControls([_standard(metadata={"source_family": "template"})])


def test_standards_controls_do_not_accept_authority_truth_roles() -> None:
    with pytest.raises(ValueError, match="authority/truth"):
        StandardsRetrievalControls([_standard(authority_role="compliance_truth")])


def test_metadata_filters_still_work_for_standards_controls() -> None:
    iso = _standard(source_id="ISO-001", metadata={"source_family": "standards", "standard_family": "iso"})
    astm = _standard(source_id="ASTM-001", metadata={"source_family": "standards", "standard_family": "astm"})
    controls = StandardsRetrievalControls([iso, astm])

    results = controls.search(RetrievalQuery(text="cleanroom", metadata_filters={"standard_family": "iso"}))

    assert [result.retrieval_result.source_id for result in results] == ["ISO-001"]
