import pytest

from asbp.renderer_output_store import (
    assert_renderer_output_format_supported,
    list_supported_renderer_output_formats,
    load_default_renderer_output_contract,
    load_renderer_output_contract_from_payload,
    media_type_for_renderer_output_format,
)


def test_default_renderer_output_contract_loads_supported_formats():
    contract = load_default_renderer_output_contract()

    assert contract.contract_id == "M29_RENDERER_OUTPUT_CONTRACT@v1"
    assert list_supported_renderer_output_formats(contract) == [
        "markdown",
        "csv_summary",
    ]
    assert "docx" in contract.blocked_formats


def test_renderer_output_format_support_guard_accepts_markdown():
    contract = load_default_renderer_output_contract()

    assert_renderer_output_format_supported(contract, "markdown")


def test_renderer_output_format_support_guard_rejects_pdf_until_implemented():
    contract = load_default_renderer_output_contract()

    with pytest.raises(ValueError) as exc_info:
        assert_renderer_output_format_supported(contract, "pdf")

    assert "Unsupported renderer output format" in str(exc_info.value)


def test_media_type_for_renderer_output_format_is_deterministic():
    assert media_type_for_renderer_output_format("markdown") == "text/markdown"
    assert media_type_for_renderer_output_format("csv_summary") == "text/csv"


def test_persisted_state_payload_is_not_renderer_output_contract_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_renderer_output_contract_from_payload(persisted_state_payload)

    assert "renderer output contract payload must include supported_formats" in str(
        exc_info.value
    )
