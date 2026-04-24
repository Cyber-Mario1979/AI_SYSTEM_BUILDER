import pytest

from asbp.document_engine import (
    AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
    CHECKPOINT_ID,
    EXACT_VERSION_PINNED_SELECTION_MODE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY,
    SUPPORTING_TEMPLATE_ARTIFACT_KIND,
    build_governed_template_retrieval_request,
    build_template_governance_baseline,
    validate_template_identity,
    validate_template_retrieval_request,
)


def test_build_template_governance_baseline_exposes_m12_1_rules() -> None:
    baseline = build_template_governance_baseline()

    assert baseline["checkpoint"] == CHECKPOINT_ID
    assert baseline["governed_template_retrieval"]["authority_role"] == (
        AUTHORITATIVE_TEMPLATE_SOURCE_ROLE
    )
    assert baseline["governed_template_retrieval"]["selection_mode"] == (
        EXACT_VERSION_PINNED_SELECTION_MODE
    )
    assert baseline["governed_template_retrieval"][
        "supporting_content_policy"
    ] == NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY
    assert "urs" in baseline["canonical_governed_template_families"]
    assert "dcf" in baseline["canonical_governed_template_families"]


def test_build_governed_template_retrieval_request_returns_authoritative_shape() -> None:
    request = build_governed_template_retrieval_request(
        template_family="urs",
        template_id="URS_BASE_v1",
        template_version="1.0.0",
    )

    assert request["template_family"] == "urs"
    assert request["template_id"] == "URS_BASE_v1"
    assert request["template_version"] == "1.0.0"
    assert request["artifact_kind"] == GOVERNED_TEMPLATE_ARTIFACT_KIND
    assert request["selection_mode"] == EXACT_VERSION_PINNED_SELECTION_MODE
    assert request["authority_role"] == AUTHORITATIVE_TEMPLATE_SOURCE_ROLE


def test_validate_template_identity_allows_supported_supporting_identity() -> None:
    validate_template_identity(
        {
            "template_family": "report",
            "template_id": "REPORT_HELP_TEXT_v1",
            "template_version": "2026.04",
            "artifact_kind": SUPPORTING_TEMPLATE_ARTIFACT_KIND,
        }
    )


def test_validate_template_identity_rejects_unsupported_family() -> None:
    with pytest.raises(ValueError, match="Unsupported template_family"):
        validate_template_identity(
            {
                "template_family": "memo",
                "template_id": "MEMO_v1",
                "template_version": "1.0.0",
                "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
            }
        )


def test_validate_template_retrieval_request_rejects_supporting_artifact_kind() -> None:
    with pytest.raises(
        ValueError,
        match="Governed template retrieval may target only",
    ):
        validate_template_retrieval_request(
            {
                "template_family": "dcf",
                "template_id": "DCF_EQ_001",
                "template_version": "1.0.0",
                "artifact_kind": SUPPORTING_TEMPLATE_ARTIFACT_KIND,
                "selection_mode": EXACT_VERSION_PINNED_SELECTION_MODE,
                "authority_role": AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
            }
        )


def test_validate_template_retrieval_request_rejects_prohibited_fallback_field() -> None:
    with pytest.raises(
        ValueError,
        match="fallback_to_latest is not allowed",
    ):
        validate_template_retrieval_request(
            {
                "template_family": "protocol",
                "template_id": "IQ_PROTOCOL_v1",
                "template_version": "1.0.0",
                "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
                "selection_mode": EXACT_VERSION_PINNED_SELECTION_MODE,
                "authority_role": AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
                "fallback_to_latest": True,
            }
        )


def test_validate_template_retrieval_request_rejects_wrong_authority_role() -> None:
    with pytest.raises(ValueError, match="invalid authority_role"):
        validate_template_retrieval_request(
            {
                "template_family": "report",
                "template_id": "FAT_REPORT_v1",
                "template_version": "1.0.0",
                "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
                "selection_mode": EXACT_VERSION_PINNED_SELECTION_MODE,
                "authority_role": "supporting_reference_only",
            }
        )