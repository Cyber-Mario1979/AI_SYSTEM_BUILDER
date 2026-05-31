import pytest
from pydantic import ValidationError

from asbp.renderer_output_model import (
    RendererArtifactMetadataModel,
    RendererOutputArtifactModel,
    RendererOutputContractModel,
)


def _required_claims() -> list[str]:
    return [
        "does_not_create_product_ready_documents",
        "does_not_mutate_lifecycle_or_review_state",
        "does_not_create_signed_or_approved_records",
        "does_not_call_ai_or_retrieve_standards",
    ]


def _metadata_payload() -> dict:
    return {
        "artifact_id": "ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        "output_format": "markdown",
        "artifact_filename": "art_qualification_plan_markdown_v1.md",
        "media_type": "text/markdown",
        "source_draft_id": "DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "standards_control_packet_id": "STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        "placeholder_present": True,
        "limitation_present": True,
        "standards_warning_present": True,
        "non_product_ready": True,
        "lifecycle_state_mutated": False,
        "approval_claimed": False,
    }


def _artifact_payload() -> dict:
    return {
        "artifact_id": "ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        "version": "v1",
        "status": "controlled_renderer_output_artifact",
        "output_format": "markdown",
        "artifact_filename": "art_qualification_plan_markdown_v1.md",
        "media_type": "text/markdown",
        "metadata": _metadata_payload(),
        "rendered_content": "# Controlled Renderer Output",
        "explicit_non_implementation_claims": _required_claims(),
    }


def test_renderer_output_contract_accepts_supported_formats():
    contract = RendererOutputContractModel(
        contract_id="M29_RENDERER_OUTPUT_CONTRACT@v1",
        version="v1",
        supported_formats=["markdown", "csv_summary"],
        blocked_formats=["docx", "pdf", "excel"],
        metadata_controls=["Metadata must remain visible."],
        explicit_non_implementation_claims=_required_claims(),
    )

    assert contract.supported_formats == ["markdown", "csv_summary"]


def test_renderer_output_contract_rejects_supported_blocked_overlap():
    with pytest.raises(ValidationError) as exc_info:
        RendererOutputContractModel(
            contract_id="M29_RENDERER_OUTPUT_CONTRACT@v1",
            version="v1",
            supported_formats=["markdown"],
            blocked_formats=["markdown"],
            metadata_controls=["Metadata must remain visible."],
            explicit_non_implementation_claims=_required_claims(),
        )

    assert "both supported and blocked" in str(exc_info.value)


def test_renderer_metadata_rejects_product_ready_claim():
    metadata = _metadata_payload()
    metadata["non_product_ready"] = False

    with pytest.raises(ValidationError) as exc_info:
        RendererArtifactMetadataModel(**metadata)

    assert "non-product-ready" in str(exc_info.value)


def test_renderer_metadata_rejects_lifecycle_mutation():
    metadata = _metadata_payload()
    metadata["lifecycle_state_mutated"] = True

    with pytest.raises(ValidationError) as exc_info:
        RendererArtifactMetadataModel(**metadata)

    assert "must not mutate lifecycle state" in str(exc_info.value)


def test_renderer_artifact_requires_explicit_non_implementation_claims():
    payload = _artifact_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_create_product_ready_documents",
    ]

    with pytest.raises(ValidationError) as exc_info:
        RendererOutputArtifactModel(**payload)

    assert "M29.7 renderer output artifact is missing explicit" in str(exc_info.value)
