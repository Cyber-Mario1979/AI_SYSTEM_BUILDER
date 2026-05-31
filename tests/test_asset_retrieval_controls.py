"""Tests for M30.6 library/template retrieval controls."""

from __future__ import annotations

import pytest

from asbp.retrieval import RetrievalIndexRecord, RetrievalQuery
from asbp.retrieval.assets import AssetRetrievalControls, DEFAULT_ASSET_LIMITATION


def _asset(**overrides: object) -> RetrievalIndexRecord:
    values = {
        "source_id": "TPL-001",
        "source_path": "data/source/templates/tpl_001.json",
        "source_version": "v1",
        "source_status": "approved",
        "authority_role": "reference_support",
        "eligibility_decision": "eligible",
        "chunk_ref": "template:TPL-001:v1:summary:chunk-1",
        "build_id": "m30-6-test-build",
        "text": "TPL-001 v1 summary cleanroom protocol template context",
        "limitation_trace": (),
        "metadata": {"asset_family": "template", "asset_id": "TPL-001", "asset_version": "v1", "context_type": "summary"},
    }
    values.update(overrides)
    return RetrievalIndexRecord(**values)


def test_asset_search_preserves_helper_only_non_authority_behavior() -> None:
    controls = AssetRetrievalControls([_asset()])

    results = controls.search(RetrievalQuery(text="cleanroom template"))

    assert len(results) == 1
    result = results[0]
    assert result.helper_only is True
    assert result.non_authoritative is True
    assert result.retrieval_result.helper_only is True
    assert result.retrieval_result.non_authoritative is True
    assert DEFAULT_ASSET_LIMITATION in result.authority_statement
    assert DEFAULT_ASSET_LIMITATION in result.retrieval_result.limitation_trace


def test_asset_context_fetch_uses_asset_id_version_and_context_type() -> None:
    summary = _asset(chunk_ref="template:TPL-001:v1:summary:chunk-1", text="TPL-001 v1 summary context")
    detail = _asset(chunk_ref="template:TPL-001:v1:detail:chunk-2", text="TPL-001 v1 detail context", metadata={"asset_family": "template", "asset_id": "TPL-001", "asset_version": "v1", "context_type": "detail"})
    other = _asset(source_id="TPL-002", chunk_ref="template:TPL-002:v1:summary:chunk-1", text="TPL-002 v1 summary context", metadata={"asset_family": "template", "asset_id": "TPL-002", "asset_version": "v1", "context_type": "summary"})
    controls = AssetRetrievalControls([summary, detail, other])

    results = controls.fetch_context("TPL-001", "v1", "detail")

    assert [result.asset_id for result in results] == ["TPL-001"]
    assert [result.context_type for result in results] == ["detail"]


def test_asset_family_filtering_keeps_template_and_library_records() -> None:
    template = _asset(source_id="TPL-001", chunk_ref="template:TPL-001:v1:summary:chunk-1")
    library = _asset(source_id="LIB-001", source_path="data/source/library/lib_001.json", chunk_ref="library:LIB-001:v2:summary:chunk-1", text="LIB-001 v2 summary library context", metadata={"asset_family": "library", "asset_id": "LIB-001", "asset_version": "v2", "context_type": "summary"})
    controls = AssetRetrievalControls([template, library])

    results = controls.search(RetrievalQuery(text="summary", metadata_filters={"asset_family": "library"}))

    assert [result.asset_family for result in results] == ["library"]
    assert [result.asset_id for result in results] == ["LIB-001"]


def test_missing_asset_metadata_fails_closed() -> None:
    with pytest.raises(ValueError, match="asset metadata"):
        AssetRetrievalControls([_asset(metadata={"asset_family": "template", "asset_version": "v1"})])

    with pytest.raises(ValueError, match="asset metadata"):
        AssetRetrievalControls([_asset(metadata={"asset_family": "template", "asset_id": "TPL-001"})])


def test_non_asset_family_records_are_rejected() -> None:
    with pytest.raises(ValueError, match="template/library"):
        AssetRetrievalControls([_asset(metadata={"asset_family": "standards", "asset_id": "STD-001", "asset_version": "v1"})])


def test_resolver_or_template_selector_authority_roles_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot replace"):
        AssetRetrievalControls([_asset(authority_role="deterministic_resolver")])

    with pytest.raises(ValueError, match="cannot replace"):
        AssetRetrievalControls([_asset(authority_role="template_selector")])


def test_asset_controls_do_not_mix_standards_family_records() -> None:
    with pytest.raises(ValueError, match="template/library"):
        AssetRetrievalControls([_asset(metadata={"source_family": "standards", "asset_family": "standards", "asset_id": "STD-001", "asset_version": "v1"})])
