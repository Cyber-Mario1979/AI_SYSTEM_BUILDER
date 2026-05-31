"""Tests for the M30.4 bounded retrieval skeleton."""

from __future__ import annotations

import pytest

from asbp.retrieval import InMemoryRetrievalIndex, RetrievalIndexRecord, RetrievalQuery


def _record(**overrides: str) -> RetrievalIndexRecord:
    values = {
        "source_id": "STD-001",
        "source_path": "data/source/standards/std_001.json",
        "source_version": "v1",
        "source_status": "approved",
        "authority_role": "reference_support",
        "eligibility_decision": "eligible",
        "chunk_ref": "section:1",
        "build_id": "m30-test-build",
        "text": "cleanroom airflow qualification protocol reference",
    }
    values.update(overrides)
    return RetrievalIndexRecord(**values)


def test_search_returns_helper_only_non_authoritative_traceable_result() -> None:
    index = InMemoryRetrievalIndex([_record()])

    results = index.search(RetrievalQuery(text="airflow protocol"))

    assert len(results) == 1
    result = results[0]
    assert result.source_id == "STD-001"
    assert result.source_path == "data/source/standards/std_001.json"
    assert result.source_version == "v1"
    assert result.chunk_ref == "section:1"
    assert result.helper_only is True
    assert result.non_authoritative is True
    assert "helper-only" in result.authority_statement


def test_pending_or_tbd_sources_fail_closed() -> None:
    with pytest.raises(ValueError, match="source status"):
        InMemoryRetrievalIndex([_record(source_status="pending")])

    with pytest.raises(ValueError, match="source status"):
        InMemoryRetrievalIndex([_record(source_status="TBD")])


def test_missing_traceability_metadata_fails_closed() -> None:
    with pytest.raises(ValueError, match="missing required trace fields"):
        InMemoryRetrievalIndex([_record(source_id="")])

    with pytest.raises(ValueError, match="missing required trace fields"):
        InMemoryRetrievalIndex([_record(chunk_ref="")])


def test_ineligible_sources_are_rejected() -> None:
    with pytest.raises(ValueError, match="not eligible"):
        InMemoryRetrievalIndex([_record(eligibility_decision="excluded")])


def test_authority_truth_roles_are_rejected() -> None:
    with pytest.raises(ValueError, match="authority/truth"):
        InMemoryRetrievalIndex([_record(authority_role="mandatory_authority")])


def test_metadata_filters_limit_results_without_mutating_truth() -> None:
    approved = _record(source_id="TPL-001", metadata={"family": "template"})
    other = _record(source_id="LIB-001", metadata={"family": "library"})
    index = InMemoryRetrievalIndex([approved, other])

    results = index.search(RetrievalQuery(text="protocol", metadata_filters={"family": "template"}))

    assert [result.source_id for result in results] == ["TPL-001"]
